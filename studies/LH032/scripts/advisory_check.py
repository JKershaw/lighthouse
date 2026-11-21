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
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, UA, save_body, write_derived  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)

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
    at, status, body, final, error, headers = now(), None, b'', '', '', None
    try:
        request = urllib.request.Request(url, headers={'User-Agent': UA})
        with urlopen(request, timeout=25) as response:
            status, final, body, headers = response.status, response.url, response.read(512 * 1024 + 1), response.headers
    except urllib.error.HTTPError as exc:
        status, final, body, error, headers = exc.code, exc.url, exc.read(4096), 'HTTP error', exc.headers
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    body = body[:512 * 1024]
    kept, why = save_body(OUT / f'page-{i + 1}.html.gz', body, final or url, headers)  # the keeper, 21 November 2026
    row = {'url': url, 'started_utc': at, 'finished_utc': now(), 'status': status, 'final_url': final,
           'bytes_retained': len(body), 'sha256_retained_response': hashlib.sha256(body).hexdigest(),
           'file': f'page-{i + 1}.html.gz', 'error': error}
    if not kept:  # nothing kept but the facts the checkpoint uses (that the page answered)
        row['body_kept'] = 'no: ' + why
        row['file'] = f'page-{i + 1}.derived.json'
        write_derived(OUT / row['file'], url, why, {}, read_utc=at, finish_utc=row['finished_utc'], http_status=status,
                      final_url=final, bytes_retained=len(body), sha256_retained_response=row['sha256_retained_response'],
                      used_for='Advisory check: one of the sampled advisory pages; the checkpoint records only that it answered.')
    log.append(row)
    print(status, len(body), url, error, flush=True)
(OUT / 'read_log.json').write_text(json.dumps(log, indent=1) + '\n')
