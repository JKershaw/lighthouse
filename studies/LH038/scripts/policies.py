#!/usr/bin/env python3
"""Read each disclosure policy in policies.json once, raw bytes up to 4 MiB, gzipped, with a read log.

Usage: python3 studies/LH038/scripts/policies.py --read 2026-11-04T1430Z [--only key ...]
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse, json, sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
# The robots.txt gate (the keeper, 8 November 2026) and what may be kept (21 November 2026); these names were
# used below but never imported, so the script could not run (found and fixed 21 November 2026).
from lh_fetch import check as robots_check, save_body, UA  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
POLICIES = json.loads((ROOT / 'policies.json').read_text())['policies']
CEILING = 4 * 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True)
parser.add_argument('--only', nargs='*', help='read only these keys')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('policies-' + args.read)
assert not OUT.exists(), 'read already exists; do not overwrite'
OUT.mkdir(parents=True)
rows = []
for key, url in POLICIES.items():
    if args.only and key not in args.only:
        continue
    row = {'name': key, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
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
                if kept:
                    row['file'] = key + '.raw.gz'
                else:
                    row['body_kept'] = 'no: ' + why
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
