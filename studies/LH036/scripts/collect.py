#!/usr/bin/env python3
"""One LH036 read: every panel URL once, raw bytes up to 4 MiB each, gzipped, with one read log per UTC label.

Usage: python3 studies/LH036/scripts/collect.py --read 2026-11-02T1415Z [--baseline]
--baseline also reads the panel's baseline_only URLs (archived posts and the upstream commit), once, at the first read.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import gzip
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
CEILING = 4 * 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label of this read, e.g. 2026-11-02T1415Z')
parser.add_argument('--baseline', action='store_true')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists; do not overwrite'
OUT.mkdir(parents=True)
groups = ['signals', 'fixes', 'pages'] + (['baseline_only'] if args.baseline else [])
targets = [(g, key, url) for g in groups for key, url in PANEL[g].items()]
assert len(targets) <= 20
rows = []
for group, key, url in targets:
    row = {'group': group, 'name': key, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
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
                       sha256=sha256(body).hexdigest())
            if len(body) <= CEILING:
                (OUT / (key + '.raw.gz')).write_bytes(gzip.compress(body, mtime=0))
                row['file'] = key + '.raw.gz'
            else:
                row['error'] = 'over the 4 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
