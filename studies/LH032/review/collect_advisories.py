#!/usr/bin/env python3
"""One bounded late advisory check of the five predeclared entries (four URLs)."""
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
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
    at, status, body, final, error = now(), None, b'', '', ''
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Lighthouse-LH032-review/0.1'})
        with urllib.request.urlopen(request, timeout=25) as response:
            status, final, body = response.status, response.url, response.read(512 * 1024 + 1)
    except urllib.error.HTTPError as exc:
        status, final, body, error = exc.code, exc.url, exc.read(4096), 'HTTP error'
    except Exception as exc:
        error = f'{type(exc).__name__}: {exc}'
    truncated = len(body) > 512 * 1024
    body = body[:512 * 1024]
    filename = f'page-{i + 1}.html.gz'
    saved = gzip.compress(body, mtime=0)
    (OUT / filename).write_bytes(saved)
    log.append({'url': url, 'started_utc': at, 'finished_utc': now(), 'status': status,
                'final_url': final, 'bytes_retained': len(body), 'prefix_only': truncated,
                'sha256_retained_response': hashlib.sha256(body).hexdigest(),
                'file': filename, 'sha256_gzip': hashlib.sha256(saved).hexdigest(), 'error': error})
    (OUT / 'read_log.json').write_text(json.dumps(log, indent=1) + '\n')
    print(status, url, len(body), 'prefix only' if truncated else '', error, flush=True)
    if status == 429:
        break
