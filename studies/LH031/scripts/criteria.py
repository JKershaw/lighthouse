#!/usr/bin/env python3
"""LH031 amendment 3: one direct GET each of CISA's catalogue page, its 21 October alert and the BOD 26-04 guidance."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
PAGES = [('criteria', 'https://www.cisa.gov/known-exploited-vulnerabilities'),
         ('alert', 'https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching'),
         ('guidance', 'https://www.cisa.gov/news-events/directives/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk')]
CEILING = 2 * 1024 * 1024
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label, e.g. 2026-10-30T1155Z')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('criteria-' + args.read)
assert not OUT.exists(), 'read already exists'
OUT.mkdir(parents=True)
log = []
for name, url in PAGES:
    row = {'source': name, 'url': url, 'reader': 'direct', 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        try:
            response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'}), timeout=40)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(CEILING + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status, final_url=response.geturl(),
                       bytes=len(body), sha256=sha256(body).hexdigest(), content_type=response.headers.get('Content-Type', ''))
            (OUT / (name + '.raw')).write_bytes(body[:CEILING])
            row['file'] = name + '.raw'
    except Exception as error:
        row.setdefault('finish_utc', datetime.now(timezone.utc).isoformat())
        row['error'] = type(error).__name__ + ': ' + str(error)[:200]
    log.append(row)
    print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'error')}))
(OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
