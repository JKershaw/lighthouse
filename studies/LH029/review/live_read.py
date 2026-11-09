#!/usr/bin/env python3
"""R-0032 reviewer's single permitted live read of PHP's archive page, to see whether entry
2026-10-23-1 changed after LH029's 17:00 UTC read. Retains the bytes and a read log beside this script.
One GET; no other site is read."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld from kept bodies
import json

HERE = Path(__file__).resolve().parent
URL = 'https://www.php.net/archive/2026.php'
OUT = HERE / 'live-archive-2026-10-23.raw'
LOG = HERE / 'live_read_log.json'
assert not OUT.exists() and not LOG.exists(), 'the review allows one live read; do not overwrite'
row = {'url': URL, 'start_utc': datetime.now(timezone.utc).isoformat()}
try:
    req = Request(URL, headers={'User-Agent': UA})
    try:
        resp = urlopen(req, timeout=18)
    except HTTPError as err:
        resp = err
    with resp:
        body = resp.read(1024 * 1024 + 1)
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=resp.status, final_url=resp.geturl(),
                   content_type=resp.headers.get('Content-Type', ''), last_modified=resp.headers.get('Last-Modified', ''),
                   http_date=resp.headers.get('Date', ''), bytes=len(body), sha256=sha256(body).hexdigest())
        if len(body) <= 1024 * 1024:
            OUT.write_bytes(redact_bytes(body)[0])
            row['file'] = OUT.name
except Exception as err:
    row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(err).__name__ + ': ' + str(err))
LOG.write_text(json.dumps([row], indent=2) + '\n')
print(json.dumps(row, indent=2))
