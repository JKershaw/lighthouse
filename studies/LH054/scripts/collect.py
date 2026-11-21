#!/usr/bin/env python3
"""One LH054 read: a copy of LH036's collector (studies/LH036/scripts/collect.py at commit 19ac17c) with only this docstring, the usage line, the baseline option and the URL ceiling changed; it reads studies/LH054/panel.json and writes under studies/LH054/data/.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 studies/LH054/scripts/collect.py --read 2026-11-19T1415Z
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from lh_fetch import check as robots_check, save_body  # noqa: E402  the keeper's robots.txt rule (8 November 2026), what may be kept (21 November)

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'

ROOT = Path(__file__).resolve().parents[1]
PANEL = json.loads((ROOT / 'panel.json').read_text())
CEILING = 4 * 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label of this read, e.g. 2026-11-02T1415Z')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists; do not overwrite'
OUT.mkdir(parents=True)
groups = ['signals', 'fixes', 'pages']
targets = [(g, key, url) for g in groups for key, url in PANEL[g].items()]
assert len(targets) <= 12  # LH054 brief: at most 12 URLs
rows = []
for group, key, url in targets:
    row = {'group': group, 'name': key, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    ok, rinfo = robots_check(url)
    row['robots'] = rinfo
    if not ok:
        row['error'] = 'not fetched: ' + rinfo['reason']
        rows.append(row)
        print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
        continue
    try:
        request = Request(url, headers={'User-Agent': UA})
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
                kept, why = save_body(OUT / (key + '.raw.gz'), body, response.geturl() or url, response.headers)
                if kept:  # the keeper, 21 November 2026: no body kept where robots.txt or the page refuses it
                    row['file'] = key + '.raw.gz'
                else:
                    row['body_kept'] = 'no: ' + why
            else:
                row['error'] = 'over the 4 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
