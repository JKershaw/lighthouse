#!/usr/bin/env python3
"""Read each disclosure policy in policies.json once, raw bytes up to 4 MiB, gzipped, with a read log.

Usage: python3 studies/LH038/scripts/policies.py --read 2026-11-04T1430Z [--only key ...]
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse, gzip, json

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
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'error')}), flush=True)
(OUT / 'read_log.json').write_text(json.dumps(rows, indent=2) + '\n')
