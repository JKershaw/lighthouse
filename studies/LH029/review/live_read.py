#!/usr/bin/env python3
"""R-0032 reviewer's single permitted live read of PHP's archive page, to see whether entry
2026-10-23-1 changed after LH029's 17:00 UTC read. Retains the bytes and a read log beside this script.
One GET; no other site is read.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) a body is saved
only through scripts/lh_fetch.py's save_body (which withholds email addresses, as before); where it may
not be kept the .raw is not written, the row has no `file` and gets body_kept "no: <reason>". A kept body is unchanged.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH029/review/live_read.py`."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (the keeper, 8 November 2026); one keep path (21 November)
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
            kept, why = save_body(OUT, body, resp.geturl() or URL, resp.headers)
            if kept:
                row['file'] = OUT.name
            else:
                row['body_kept'] = 'no: ' + why
except Exception as err:
    row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(err).__name__ + ': ' + str(err))
LOG.write_text(json.dumps([row], indent=2) + '\n')
print(json.dumps(row, indent=2))
