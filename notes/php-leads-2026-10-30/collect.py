#!/usr/bin/env python3
"""Direct reads for the php-leads row, 30 October 2026: at most ten pages, raw bytes up to 2 MiB, one log."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import sys

HERE = Path(__file__).resolve().parent
LOG = HERE / 'read_log.json'
rows = json.loads(LOG.read_text()) if LOG.exists() else []
for name, url in zip(sys.argv[1::2], sys.argv[2::2]):
    assert len(rows) < 10, 'the row allows at most ten pages'
    assert not (HERE / 'pages' / (name + '.raw')).exists()
    row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'})
        try:
            response = urlopen(request, timeout=20)
        except HTTPError as error:
            response = error
        with response:
            body = response.read(2 * 1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                       bytes=len(body), sha256=sha256(body).hexdigest())
            if len(body) <= 2 * 1024 * 1024:
                (HERE / 'pages').mkdir(exist_ok=True)
                (HERE / 'pages' / (name + '.raw')).write_bytes(body)
                row['file'] = 'pages/' + name + '.raw'
            else:
                row['error'] = 'over 2 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps(row), flush=True)
LOG.write_text(json.dumps(rows, indent=2) + '\n')
