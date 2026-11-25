#!/usr/bin/env python3
"""LH034, post-record context: a one-off read of Node.js's own release announcements for the three in-line
versions first seen in the downloads on 11 November 2026 (v22.23.5, v24.22.3, v26.13.1).

Why: the reader review (notes/R-0131-lh034-v1-reader.md) asked whether they carry the October fix, which the
record's amended rule assumes unchecked. At most three URLs on nodejs.org, read once, through scripts/lh_fetch.py
with access='oneoff' (AGENTS.md, the keeper's decision of 21 November 2026). Bodies are saved only through
save_body; where it says no, nothing is kept but the log. Run with LIGHTHOUSE_PROVIDER=anthropic.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH034/scripts/oneoff_release_pages.py
Writes studies/LH034/oneoff-2026-11-25/fetch_log.json and any kept bodies beside it. Never overwrites a log.
"""
import datetime as dt
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
import lh_fetch  # noqa: E402

OUT = ROOT / 'studies/LH034/oneoff-2026-11-25'
VERSIONS = ['v22.23.5', 'v24.22.3', 'v26.13.1']


def now():
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log_path = OUT / 'fetch_log.json'
    if log_path.exists():
        sys.exit('fetch_log.json exists: this read is one-off and is not repeated')
    log = {'provider': os.environ.get('LIGHTHOUSE_PROVIDER'), 'access': 'oneoff', 'user_agent': lh_fetch.UA, 'reads': []}
    for v in VERSIONS:
        url = 'https://nodejs.org/en/blog/release/' + v
        rec = {'version': v, 'url': url, 'read_utc': now()}
        ok, info = lh_fetch.check(url, 'oneoff')
        rec['robots'] = {k: info.get(k) for k in ('reason', 'decided_by', 'rule', 'robots_status', 'robots_sha256')}
        try:
            req = urllib.request.Request(url, headers={'User-Agent': lh_fetch.UA})
            with lh_fetch.urlopen(req, timeout=30, check_redirects=True, access='oneoff') as r:
                body = r.read()
                rec.update(http_status=r.status, final_url=r.geturl(), content_type=r.headers.get('Content-Type'),
                           bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
                kept, why = lh_fetch.save_body(OUT / (v + '.html.gz'), body, r.geturl(), dict(r.headers), access='oneoff')
                rec['body_kept'] = ('yes: ' if kept else 'no: ') + str(why)
        except lh_fetch.NotFetched as e:
            rec.update(http_status=None, error='NotFetched: %s' % e)
        except urllib.error.HTTPError as e:
            rec.update(http_status=e.code, error='HTTPError %s' % e.code)
        except Exception as e:  # a wall or a network failure is an observation, not retried
            rec.update(http_status=None, error='%s: %s' % (type(e).__name__, e))
        rec['finish_utc'] = now()
        log['reads'].append(rec)
    log_path.write_text(json.dumps(log, indent=1) + '\n')
    print(json.dumps(log, indent=1))


if __name__ == '__main__':
    main()
