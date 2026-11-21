#!/usr/bin/env python3
"""Fetch the providers' own pages on their user-agent tokens, once, and keep them.

Each host's robots.txt is read first (redirects followed, up to five, RFC 9309) and obeyed under
scripts/robots_rules.py with provider None (every listed provider's tokens, the strictest), since
the token list was being written from these pages. Pages follow up to five redirects, each hop a
logged request and each new host's robots.txt read first. No retries, no cookies, no email
address, no JavaScript. Email addresses in kept bodies are withheld (scripts/redact_emails.py);
fetchlog.csv keeps the sha256 of the bytes received.

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md; the record of the
reads of 8 November, not run again): it still reads, logs and keeps each host's robots.txt itself and fetches
under that file (provider None, no automatic redirects), as before, so its requests are unchanged; a page
body (each hop's) is saved only through scripts/lh_fetch.py's save_body, given the robots.txt this script
already read (robots_body=, None where it answered 4xx), so nothing is read twice. Where a body may not be
kept no NNN.b is written (the NNN.h header file still is) and the robots_decision column ends
"; body_kept: no: <reason>". A kept body is unchanged.

Usage: python3 -I notes/robots-tokens-2026-11-08/fetch_sources.py OUTDIR URL...

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:notes/robots-tokens-2026-11-08/fetch_sources.py`.
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urljoin
from urllib.request import Request, build_opener, HTTPRedirectHandler, HTTPSHandler, ProxyHandler
import csv
import os
import ssl
import sys
import time

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'scripts'))
from redact_emails import redact_bytes  # noqa: E402
import robots_rules  # noqa: E402
from lh_fetch import save_body  # noqa: E402  the one keep path (21 November 2026)

UA = 'Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)'
CA = '/root/.ccr/ca-bundle.crt'
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = build_opener(ProxyHandler(), HTTPSHandler(context=CTX), _NoRedirect())


def get(url, cap):
    req = Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
    out = {'url': url, 'utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'status': '',
           'error': '', 'headers': [], 'body': b'', 'truncated': False}
    try:
        try:
            r = OPENER.open(req, timeout=25)
        except HTTPError as e:
            r = e
        out['status'] = r.status if hasattr(r, 'status') else r.code
        out['headers'] = list(r.headers.items()) if r.headers else []
        raw = r.read(cap + 1)
        out['truncated'] = len(raw) > cap
        out['body'] = raw[:cap]
    except (URLError, OSError, ValueError) as e:
        out['error'] = repr(e)[:200]
    time.sleep(1.5)
    return out


def main(outdir, urls):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    logp = out / 'fetchlog.csv'
    new = not logp.exists()
    lf = open(logp, 'a', newline='')
    w = csv.writer(lf)
    if new:
        w.writerow(['n', 'kind', 'url', 'utc', 'status', 'error', 'bytes', 'truncated', 'sha256', 'robots_decision'])
    n = len(list(out.glob('*.h')))
    robots = {}

    def keep(kind, r, note='', robots_body=None):
        nonlocal n
        n += 1
        h = 'HTTP %s\n' % r['status'] + ''.join('%s: %s\n' % kv for kv in r['headers'])
        (out / ('%03d.h' % n)).write_bytes(redact_bytes(h.encode('utf-8', 'replace'))[0])  # response headers, not a body
        if kind.startswith('robots'):  # a robots.txt copy is always kept, as before
            (out / ('%03d.b' % n)).write_bytes(redact_bytes(r['body'])[0])
        else:
            kept, why = save_body(out / ('%03d.b' % n), r['body'], r['url'], r['headers'], robots_body=robots_body)
            if not kept:
                note = (note + '; ' if note else '') + 'body_kept: no: ' + why
        w.writerow([n, kind, r['url'], r['utc'], r['status'], r['error'], len(r['body']), r['truncated'],
                    sha256(r['body']).hexdigest(), note])
        lf.flush()

    def robots_for(url):
        s = urlsplit(url)
        key = (s.scheme, s.netloc)
        if key in robots:
            return robots[key]
        cur = '%s://%s/robots.txt' % key
        res = None
        for hop in range(6):
            r = get(cur, robots_rules.READ_LIMIT)
            keep('robots' if hop == 0 else 'robots-redirect-%d' % hop, r)
            st = r['status']
            if r['error'] or not st or not (300 <= st < 400) or hop == 5:
                break
            cur = urljoin(cur, dict((k.lower(), v) for k, v in r['headers']).get('location', ''))
        if r['error'] or not r['status'] or r['status'] >= 500 or 300 <= r['status'] < 400 or r['status'] == 429:
            res = None                                   # unreachable or walled: fetch nothing
        elif r['status'] >= 400:
            res = b''                                    # unavailable: no rules
        else:
            res = (r['body'], r['truncated'])
        robots[key] = res
        return res

    for url in urls:
        cur = url
        for hop in range(6):
            rb = robots_for(cur)
            if rb is None:
                print('not fetched (robots.txt unreachable or walled):', cur)
                break
            body, tr = rb if rb else (b'', False)
            d = robots_rules.decide(body, cur, None, tr)
            if not d.allowed:
                print('not fetched (robots.txt disallows, %s: %s): %s' % (d.decided_by, d.rule, cur))
                break
            r = get(cur, 4 * 1024 * 1024)
            keep('page' if hop == 0 else 'page-redirect-%d' % hop, r,
                 'allowed (%s)' % (d.decided_by or 'no group'), robots_body=body if rb else None)
            print(r['status'], r['error'], cur, len(r['body']))
            st = r['status']
            if r['error'] or not st or not (300 <= st < 400):
                break
            cur = urljoin(cur, dict((k.lower(), v) for k, v in r['headers']).get('location', ''))
    lf.close()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
