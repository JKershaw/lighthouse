#!/usr/bin/env python3
"""One LH033 read: Censys's PHP2Shell JSON, and, when asked, W3Techs's PHP 8 pages, Packagist's PHP statistics and php.net's release dates.

Usage: collect.py --read 2026-10-25T0900Z [--parts censys,w3techs,packagist,phpnet]
Raw bodies are kept gzipped (Packagist's as its two extracted series only) with UTC times, status and SHA-256 of the uncompressed body; a read is never overwritten.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import argparse
import gzip
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from packagist_extract import extract  # noqa: E402
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, redacted, UA, may_keep  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)
from robots_rules import page_reservation  # noqa: E402  what may be kept (the keeper, 21 November 2026)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from derive_kept import w3_details, w3_history, NOTE  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
W3 = 'https://w3techs.com/technologies/'
SOURCES = {
    'censys': [('censys', 'https://php2shell.censys.com/api/data')],
    'w3techs': [(f'w3techs-{kind}-{minor}', f'{W3}{kind}/pl-php/{minor}')
                for kind in ('details', 'history_details') for minor in ('8.2', '8.3', '8.4', '8.5')],
    'packagist': [('packagist', 'https://packagist.org/php-statistics')],
    'phpnet': [(f'phpnet-releases-{minor}', f'https://www.php.net/releases/index.php?json&version={minor}&max=40')
               for minor in ('8.2', '8.3', '8.4', '8.5')],
}
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label, e.g. 2026-10-25T0900Z')
parser.add_argument('--parts', default='censys', help='comma-separated: censys, w3techs, packagist, phpnet')
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
                response = urlopen(Request(url, headers={'User-Agent': UA}), timeout=60)
            except HTTPError as error:
                response = error
            with response:
                body = response.read(16 * 1024 * 1024 + 1)
                row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status, bytes=len(body),
                           sha256=sha256(body).hexdigest(), content_type=response.headers.get('Content-Type', ''))
                body = body[:16 * 1024 * 1024]
                keep, why = may_keep(response.geturl() or url)
                reserved = page_reservation(body, response.headers)
                if keep and not reserved:
                    (OUT / (name + '.raw.gz')).write_bytes(gzip.compress(redacted(body), mtime=0))
                    row['file'] = name + '.raw.gz'
                else:
                    # brief amendment of 21 November 2026: no body kept; only the facts the study uses
                    row['body_kept'] = 'no: ' + (reserved or why)
                    if name.startswith('w3techs-'):
                        kind = name.split('-')[1]
                        ext = w3_details(body) if kind == 'details' else {'history': w3_history(body)}
                        rec = {'url': url, 'read_utc': row['start_utc'], 'finish_utc': row['finish_utc'],
                               'http_status': row['status'], 'content_type': row['content_type'], 'bytes': row['bytes'],
                               'sha256': row['sha256'], 'body_kept': row['body_kept'],
                               'body_removed': NOTE.replace('Body removed on 21 November 2026', 'Body not kept'),
                               'extracted': ext}
                        (OUT / (name + '.derived.json')).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + '\n')
                        row['file'] = name + '.derived.json'
        except Exception as error:
            row.setdefault('finish_utc', datetime.now(timezone.utc).isoformat())
            row['error'] = type(error).__name__ + ': ' + str(error)[:200]
        log.append(row)
        print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'error')}))
if (OUT / 'packagist.raw.gz').exists():
    extract(OUT)  # keeps the two series, drops the raw page (it embeds a key)
    for row in log:
        if row['source'] == 'packagist':
            row['file'] = 'packagist.json (extracted; raw not kept)'
(OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
