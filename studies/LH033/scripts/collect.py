#!/usr/bin/env python3
"""One LH033 read: Censys's PHP2Shell JSON, and, when asked, W3Techs's PHP 8 pages and Packagist's PHP statistics.

Usage: collect.py --read 2026-10-25T0900Z [--parts censys,w3techs,packagist]
Raw bodies are kept gzipped with UTC times, status and SHA-256 of the uncompressed body; a read is never overwritten.
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
W3 = 'https://w3techs.com/technologies/'
SOURCES = {
    'censys': [('censys', 'https://php2shell.censys.com/api/data')],
    'w3techs': [(f'w3techs-{kind}-{minor}', f'{W3}{kind}/pl-php/{minor}')
                for kind in ('details', 'history_details') for minor in ('8.2', '8.3', '8.4', '8.5')],
    'packagist': [('packagist', 'https://packagist.org/php-statistics')],
}
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label, e.g. 2026-10-25T0900Z')
parser.add_argument('--parts', default='censys', help='comma-separated: censys, w3techs, packagist')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
parts = args.parts.split(',')
assert set(parts) <= set(SOURCES), 'unknown part'
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists'
OUT.mkdir(parents=True)
log = []
for part in parts:
    for name, url in SOURCES[part]:
        row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
        try:
            try:
                response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'}), timeout=60)
            except HTTPError as error:
                response = error
            with response:
                body = response.read(16 * 1024 * 1024 + 1)
                row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status, bytes=len(body),
                           sha256=sha256(body).hexdigest(), content_type=response.headers.get('Content-Type', ''))
                (OUT / (name + '.raw.gz')).write_bytes(gzip.compress(body[:16 * 1024 * 1024], mtime=0))
                row['file'] = name + '.raw.gz'
        except Exception as error:
            row.setdefault('finish_utc', datetime.now(timezone.utc).isoformat())
            row['error'] = type(error).__name__ + ': ' + str(error)[:200]
        log.append(row)
        print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'error')}))
(OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
