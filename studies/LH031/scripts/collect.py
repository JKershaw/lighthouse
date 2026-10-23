#!/usr/bin/env python3
"""One LH031 read: CISA's KEV feed, or CISA's GitHub mirror if the feed refuses; extracts the three CVEs."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [('feed', 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json'),
           ('mirror', 'https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json')]
CVES = ('CVE-2026-109618', 'CVE-2026-109619', 'CVE-2026-115560')
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True, help='UTC label, e.g. 2026-10-23T1900Z')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists'
OUT.mkdir(parents=True)
log, result = [], None
for name, url in SOURCES:
    row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        try:
            response = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'}), timeout=40)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(16 * 1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status, bytes=len(body),
                       sha256=sha256(body).hexdigest(), content_type=response.headers.get('Content-Type', ''))
            (OUT / (name + '.raw')).write_bytes(body[:16 * 1024 * 1024])
            row['file'] = name + '.raw'
            data = json.loads(body)
            entries = {v['cveID']: v for v in data.get('vulnerabilities', [])}
            result = {'source': name, 'catalogVersion': data.get('catalogVersion'), 'dateReleased': data.get('dateReleased'),
                      'count': data.get('count'), 'entries': {c: entries.get(c) for c in CVES}}
    except Exception as error:
        row.setdefault('finish_utc', datetime.now(timezone.utc).isoformat())
        row['error'] = type(error).__name__ + ': ' + str(error)[:200]
    log.append(row)
    print(json.dumps({k: row.get(k) for k in ('source', 'status', 'bytes', 'error')}))
    if result:
        break
(OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
(OUT / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=1))
