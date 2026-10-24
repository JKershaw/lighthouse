#!/usr/bin/env python3
"""LH032's per-read sample check: the first five entries with a source-typed advisory URL, in the list's
case-insensitive alphabetical order (the order the pre-read plan in review/plan.md names), one GET per unique
first advisory URL, bodies kept gzip-compressed. Usage: advisory_check.py <read label>"""
from datetime import datetime, timezone
from pathlib import Path
import gzip
import hashlib
import json
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
READ = ROOT / 'data' / ('read-' + sys.argv[1])
OUT = READ / 'advisory-check'
rows = json.loads(gzip.decompress((READ / 'source_entries.json.gz').read_bytes()))
order = sorted((r for r in rows if r['advisory_urls']), key=lambda r: (r['supplier'].casefold(), r['product'].casefold()))
sample = order[:5]
urls = list(dict.fromkeys(r['advisory_urls'][0] for r in sample))
OUT.mkdir(exist_ok=False)
(OUT / 'selection.json').write_text(json.dumps(sample, indent=1) + '\n')
now = lambda: datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
log = []
for i, url in enumerate(urls):
    at, status, body, final, error = now(), None, b'', '', ''
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'})
        with urllib.request.urlopen(request, timeout=25) as response:
            status, final, body = response.status, response.url, response.read(512 * 1024 + 1)
    except urllib.error.HTTPError as exc:
        status, final, body, error = exc.code, exc.url, exc.read(4096), 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    body = body[:512 * 1024]
    saved = gzip.compress(body, mtime=0)
    (OUT / f'page-{i + 1}.html.gz').write_bytes(saved)
    log.append({'url': url, 'started_utc': at, 'finished_utc': now(), 'status': status, 'final_url': final,
                'bytes_retained': len(body), 'sha256_retained_response': hashlib.sha256(body).hexdigest(),
                'file': f'page-{i + 1}.html.gz', 'error': error})
    print(status, len(body), url, error, flush=True)
(OUT / 'read_log.json').write_text(json.dumps(log, indent=1) + '\n')
