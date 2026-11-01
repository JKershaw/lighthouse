#!/usr/bin/env python3
"""One LH037 read: every route and every recorded advisory in panel.json once, raw bytes up to 4 MiB each, gzipped.

Usage: python3 studies/LH037/scripts/collect.py --read 2026-11-02T1415Z
For each body it counts the three CVE identifiers and the word PHP (case-sensitive, word boundary); a match is a
prompt to open the body, never a finding. No retry, search, login or probe.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse, gzip, json, re

ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
CEILING = 4 * 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True)
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists; do not overwrite'
OUT.mkdir(parents=True)
targets = []
for stratum in ('rule_panel', 'named_stratum'):
    for vendor, entry in PANEL[stratum].items():
        for kind in ('routes', 'advisories'):
            for key, value in entry[kind].items():
                url = value if isinstance(value, str) else value['url']
                targets.append((stratum, vendor, kind, key, url))
assert len(targets) <= 60
php = re.compile(rb'\bPHP\b')
rows = []
for stratum, vendor, kind, key, url in targets:
    name = re.sub(r'[^a-z0-9]+', '-', vendor.lower()) + '__' + key
    row = {'stratum': stratum, 'vendor': vendor, 'kind': kind, 'name': name, 'url': url,
           'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'})
        try:
            response = urlopen(request, timeout=40)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(CEILING + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                       last_modified=response.headers.get('Last-Modified', ''), bytes=len(body),
                       sha256=sha256(body).hexdigest(),
                       mentions={c: body.count(c.encode()) for c in PANEL['cves']} | {'PHP': len(php.findall(body))})
            if len(body) <= CEILING:
                (OUT / (name + '.raw.gz')).write_bytes(gzip.compress(body, mtime=0))
                row['file'] = name + '.raw.gz'
            else:
                row['error'] = 'over the 4 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'mentions', 'error')}), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
