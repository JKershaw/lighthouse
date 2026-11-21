#!/usr/bin/env python3
"""One bounded direct read for LH029: PHP's archive page, then at most two pages its 23 October entry links to.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) a body is saved
only through scripts/lh_fetch.py's save_body (which withholds email addresses, as before); where it may
not be kept no .raw is written, the row has no `file` and gets body_kept "no: <reason>". A kept body is unchanged.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH029/scripts/collect.py`."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (the keeper, 8 November 2026); one keep path (21 November)
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'snapshot-2026-10-23'
LOG = OUT / 'read_log.json'
parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True, help='file stem for the retained body, e.g. archive')
parser.add_argument('--url', required=True)
args = parser.parse_args()
OUT.mkdir(parents=True, exist_ok=True)
rows = json.loads(LOG.read_text()) if LOG.exists() else []
assert len(rows) < 3, 'the brief allows at most three GETs'
assert not (OUT / (args.name + '.raw')).exists(), 'do not overwrite a retained body'
row = {'source': args.name, 'url': args.url, 'start_utc': datetime.now(timezone.utc).isoformat()}
try:
    request = Request(args.url, headers={'User-Agent': UA})
    try:
        response = urlopen(request, timeout=18)
    except HTTPError as error:
        response = error
    with response:
        body = response.read(1024 * 1024 + 1)
        row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status,
                   final_url=response.geturl(), content_type=response.headers.get('Content-Type', ''),
                   last_modified=response.headers.get('Last-Modified', ''), http_date=response.headers.get('Date', ''),
                   bytes=len(body), sha256=sha256(body).hexdigest())
        if len(body) <= 1024 * 1024:
            kept, why = save_body(OUT / (args.name + '.raw'), body, response.geturl() or args.url, response.headers)
            if kept:
                row['file'] = str((OUT / (args.name + '.raw')).relative_to(ROOT))
            else:
                row['body_kept'] = 'no: ' + why
        else:
            row['error'] = 'over 1 MiB ceiling; no body retained'
except Exception as error:
    row.update(finish_utc=datetime.now(timezone.utc).isoformat(), error=type(error).__name__ + ': ' + str(error))
rows.append(row)
print(json.dumps(row), flush=True)
LOG.write_text(json.dumps(rows, indent=2) + '\n')
