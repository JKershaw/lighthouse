#!/usr/bin/env python3
"""One bounded late advisory check of the five predeclared entries (four URLs).

The record of the late advisory check of 23 October 2026 (review/advisory-check-2026-10-23); it is not run
again. From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) it fetches
through scripts/lh_fetch.py's urlopen with access='oneoff' (before, urllib's urlopen with no robots check;
a refused URL is now logged with error "NotFetched: ..." and no request), and saves a page only through
lh_fetch's save_body, which withholds email addresses (the 23 October pages were saved as received); where
a page may not be kept nothing is written, `file` and `sha256_gzip` are empty and the row gets body_kept
"no: <reason>". A kept page is otherwise saved under the same name, gzipped with mtime 0, as before. Where no
response came at all, no file is written (before, an empty gzip).

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH032/review/collect_advisories.py`.
"""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parents[1] / 'scripts'))
from lh_fetch import urlopen, save_body  # noqa: E402  robots.txt gate and the one keep path (21 November 2026)
OUT = ROOT / 'review/advisory-check-2026-10-23'
rows = json.loads(gzip.decompress((ROOT / 'data/read-2026-10-23-baseline-audit/source_entries.json.gz').read_bytes()))
sample = [r for r in rows if r['advisory_urls']][:5]
urls = list(dict.fromkeys(r['advisory_urls'][0] for r in sample))
assert len(sample) == 5 and len(urls) == 4
OUT.mkdir(exist_ok=False)
(OUT / 'selection.json').write_text(json.dumps(sample, indent=1) + '\n')
now = lambda: datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
log = []
for i, url in enumerate(urls):
    at, status, body, final, error, hdrs = now(), None, b'', '', '', None
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Lighthouse-LH032-review/0.1'})
        with urlopen(request, timeout=25, access='oneoff') as response:
            status, final, body, hdrs = response.status, response.url, response.read(512 * 1024 + 1), response.headers
    except urllib.error.HTTPError as exc:
        status, final, body, error, hdrs = exc.code, exc.url, exc.read(4096), 'HTTP error', exc.headers
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    truncated = len(body) > 512 * 1024
    body = body[:512 * 1024]
    filename = f'page-{i + 1}.html.gz'
    # no response at all (network error or NotFetched): nothing to keep (before, an empty gzip was written)
    kept, why = save_body(OUT / filename, body, final or url, hdrs) if status is not None else (False, '')
    row = {'url': url, 'started_utc': at, 'finished_utc': now(), 'status': status,
           'final_url': final, 'bytes_retained': len(body), 'prefix_only': truncated,
           'sha256_retained_response': hashlib.sha256(body).hexdigest(),
           'file': filename if kept else '',
           'sha256_gzip': hashlib.sha256((OUT / filename).read_bytes()).hexdigest() if kept else '', 'error': error}
    if not kept and status is not None:
        row['body_kept'] = 'no: ' + why
    log.append(row)
    (OUT / 'read_log.json').write_text(json.dumps(log, indent=1) + '\n')
    print(status, url, len(body), 'prefix only' if truncated else '', error, flush=True)
    if status == 429:
        break
