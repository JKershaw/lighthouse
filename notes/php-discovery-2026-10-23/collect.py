#!/usr/bin/env python3
"""Direct reads for the PHP discovery pass: at most eight pages, raw bytes up to 1 MiB, one log.

The record of that pass's reads; it is not run again. From 21 November 2026 (the keeper's decision,
notes/keeper/2026-11-21-robots-intent.md) it fetches through scripts/lh_fetch.py's urlopen with
access='oneoff' (before, urllib's urlopen with no robots check; a refused URL is now logged with error
"NotFetched: ..." and no request), and saves a page only through lh_fetch's save_body, which withholds
email addresses (the pages of that pass were saved as received); where a page may not be kept nothing is
written, the row has no `file` and gets body_kept "no: <reason>". A kept page keeps its name.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:notes/php-discovery-2026-10-23/collect.py`."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from lh_fetch import urlopen, save_body  # noqa: E402  robots.txt gate and the one keep path (21 November 2026)

HERE = Path(__file__).resolve().parent
LOG = HERE / 'read_log.json'
rows = json.loads(LOG.read_text()) if LOG.exists() else []
for name, url in zip(sys.argv[1::2], sys.argv[2::2]):
    assert len(rows) < 8, 'the plan allows at most eight pages'
    assert not (HERE / 'pages' / (name + '.raw')).exists()
    row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; Lighthouse research observation)'})
        try:
            response = urlopen(request, timeout=20, access='oneoff')
        except HTTPError as error:
            response = error
        with response:
            body = response.read(1024 * 1024 + 1)
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                       final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                       bytes=len(body), sha256=sha256(body).hexdigest())
            if len(body) <= 1024 * 1024:
                (HERE / 'pages').mkdir(exist_ok=True)
                kept, why = save_body(HERE / 'pages' / (name + '.raw'), body, response.geturl() or url, response.headers)
                if kept:
                    row['file'] = 'pages/' + name + '.raw'
                else:
                    row['body_kept'] = 'no: ' + why
            else:
                row['error'] = 'over 1 MiB ceiling; no body retained'
    except Exception as error:
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
    rows.append(row)
    print(json.dumps(row), flush=True)
LOG.write_text(json.dumps(rows, indent=2) + '\n')
