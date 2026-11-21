#!/usr/bin/env python3
"""One LH034 read: nodejs.org's daily download summaries for the days asked, and dist/index.json.

Usage: collect.py --read 2026-10-27T1815Z --days 2026-09-23:2026-10-26 [--days ...]
Each day's file is kept gzipped with UTC times, status and SHA-256 of the body; a read is never overwritten.
Days already held by an earlier read are fetched again only with --refetch (brief.md, Reads).
"""
from datetime import date, datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request
import argparse
import json
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, UA, save_body, write_derived  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from derive_kept import dist_index_extract, USED  # noqa: E402  the extractor

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://storage.googleapis.com/access-logs-summaries-nodejs/nodejs.org-access.log.{}.json'
parser = argparse.ArgumentParser()
parser.add_argument('--read', required=True)
parser.add_argument('--days', action='append', required=True, help='first:last, inclusive')
parser.add_argument('--refetch', action='store_true')
args = parser.parse_args()
datetime.strptime(args.read, '%Y-%m-%dT%H%MZ')
held = {p.name.split('.')[0] for p in (ROOT / 'data').glob('read-*/day-*.raw.gz')}
OUT = ROOT / 'data' / ('read-' + args.read)
assert not OUT.exists(), 'read already exists'
OUT.mkdir(parents=True)
wanted = []
for span in args.days:
    first, last = map(date.fromisoformat, span.split(':'))
    wanted += [first + timedelta(n) for n in range((last - first).days + 1)]
jobs = [('dist-index', 'https://nodejs.org/dist/index.json')]
jobs += [(f'day-{d:%Y%m%d}', BASE.format(f'{d:%Y%m%d}')) for d in wanted if args.refetch or f'day-{d:%Y%m%d}' not in held]
log = []
for name, url in jobs:
    row = {'source': name, 'url': url, 'start_utc': datetime.now(timezone.utc).isoformat()}
    try:
        try:
            response = urlopen(Request(url, headers={'User-Agent': UA}), timeout=60)
        except HTTPError as error:
            response = error
        with response:
            body = response.read()
            row.update(finish_utc=datetime.now(timezone.utc).isoformat(), status=response.status, bytes=len(body),
                       sha256=sha256(body).hexdigest())
            if response.status == 200:
                kept, why = save_body(OUT / (name + '.raw.gz'), body, response.geturl() or url, response.headers)
                if kept:  # the keeper, 21 November 2026: no body kept where robots.txt or the page refuses it
                    row['file'] = name + '.raw.gz'
                else:
                    row['body_kept'] = 'no: ' + why
                    if name == 'dist-index':  # keep only the facts the study uses, as derive_kept.py does
                        write_derived(OUT / 'dist-index.derived.json', url, why, dist_index_extract(body),
                                      read_utc=row['start_utc'], finish_utc=row['finish_utc'], http_status=row['status'],
                                      bytes=row['bytes'], sha256=row['sha256'], used_for=USED)
                        row['file'] = 'dist-index.derived.json'
    except Exception as error:
        row.setdefault('finish_utc', datetime.now(timezone.utc).isoformat())
        row['error'] = type(error).__name__ + ': ' + str(error)[:200]
    log.append(row)
(OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
print(sum(r.get('status') == 200 for r in log), 'of', len(log), 'fetched;', [r['source'] for r in log if r.get('status') != 200], 'not')
