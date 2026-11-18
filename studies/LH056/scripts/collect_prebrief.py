#!/usr/bin/env python3
"""LH056 event-record read: the reporters' posts, OSV's records and PyPI's public project page for
agent-framework, each once, before the brief is fixed (gate of 18 November 2026, condition 2), and once
again at the closure gate with --closure.

No download count of any kind is read here: no ClickPy query, no pypistats.org request, no BigQuery,
no vendor dashboard. PyPI's JSON API (/pypi/<name>/json) is closed to Lighthouse by robots.txt and is
refused below by URL; the simple index is planned only so that the robots.txt gate's answer about it is
logged (on 18 November 2026 that answer was "Disallow: /simple/", and no request was made).

Every URL is asked of scripts/robots_gate.py first (the keeper's rule of 8 November 2026; run with
LIGHTHOUSE_PROVIDER=anthropic under Claude Code, or every provider's tokens are obeyed). A URL the gate
refuses is logged "NotFetched", a missing reading and never a negative. No retry. Bodies are kept under
data/prebrief-<UTC label>/ (or data/closure-<UTC label>/) after scripts/redact_emails.py redact_bytes;
fetchlog.csv keeps name, URL, method, request body, UTC start, status, content type, Last-Modified,
bytes received, SHA-256 of the bytes received (before redaction), emails withheld, and the robots
decision. A label already held is never overwritten.

Never requested (gate condition 6), refused by URL below: any file on files.pythonhosted.org, PyPI's JSON
API, any PyPI user page, the webhook host the reports name, github.com and its content hosts, Azure
DevOps, and any wheel or source distribution path.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH056/scripts/collect_prebrief.py [--closure]
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import csv
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from robots_gate import RobotsGate  # noqa: E402  the keeper's robots.txt rule, 8 November 2026
from redact_emails import redact_bytes  # noqa: E402  email addresses withheld

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
ROOT = Path(__file__).resolve().parents[1]
CEILING = 16 * 1024 * 1024
MAX_REQUESTS = 8   # gate condition 4: the event records at most eight requests each time
FORBIDDEN = ('files.pythonhosted.org', '/pypi/', 'pypi.org/user/', 'webhook.site', 'github.com',
             'githubusercontent.com', 'dev.azure.com', 'visualstudio.com', '.whl', '.tar.gz',
             'clickhouse', 'pypistats', 'bigquery', 'deps.dev')

OSV_ALL = json.dumps({'package': {'name': 'agent-framework', 'ecosystem': 'PyPI'}})

# (name, url, method, body, extra headers)
PLAN = [
    ('stepsecurity_post', 'https://www.stepsecurity.io/blog/microsoft-agent-framework-pypi-package-compromised',
     'GET', None, {}),
    ('socket_post', 'https://socket.dev/blog/agent-framework-pypi-package-compromised-with-credential-stealer',
     'GET', None, {}),
    ('aikido_post', 'https://www.aikido.dev/blog/two-malicious-agent-framework-releases-hit-pypi-in-33-minutes',
     'GET', None, {}),
    ('osv_query_agent_framework', 'https://api.osv.dev/v1/query', 'POST', OSV_ALL,
     {'Content-Type': 'application/json'}),
    ('pypi_project_page', 'https://pypi.org/project/agent-framework/', 'GET', None, {}),
    ('pypi_simple_index', 'https://pypi.org/simple/agent-framework/', 'GET', None, {}),
]


def fetch(gate, name, url, method, body, headers, out):
    row = {'name': name, 'url': url, 'method': method, 'request_body': body or '',
           'utc_start': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    ok, info = gate.check(url)
    row['robots'] = '%s (%s, group %s, rule %s)' % (info.get('reason'), info.get('robots_url'),
                                                     info.get('decided_by', ''), info.get('rule', ''))
    if not ok:
        row['status'] = 'NotFetched'
        return row, False
    payload = b''
    try:
        req = Request(url, data=body.encode() if body is not None else None, method=method,
                      headers={'User-Agent': UA, **headers})
        try:
            resp = urlopen(req, timeout=60)
        except HTTPError as err:
            resp = err
        with resp:
            payload = resp.read(CEILING + 1)
            row.update(status=resp.status, content_type=resp.headers.get('Content-Type', ''),
                       last_modified=resp.headers.get('Last-Modified', ''))
    except Exception as err:  # recorded, never retried, nothing invented
        row['status'] = 'error: ' + type(err).__name__ + ': ' + str(err)[:200]
    row.update(bytes=len(payload), sha256=sha256(payload).hexdigest() if payload else '')
    if payload and len(payload) <= CEILING:
        redacted, n = redact_bytes(payload)
        (out / (name + '.raw')).write_bytes(redacted)
        row.update(file=name + '.raw', emails_withheld=n)
    return row, True


def main():
    ap = argparse.ArgumentParser(description='LH056 event-record read (no download count).')
    ap.add_argument('--closure', action='store_true', help='the one re-read at the closure gate')
    a = ap.parse_args()
    for _, url, *_ in PLAN:
        if 'simple' in url:
            continue  # planned only for the gate's logged answer; refused by robots.txt on 18 November
        assert not any(f in url for f in FORBIDDEN), 'refused: ' + url
    label = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%MZ')
    out = ROOT / 'data' / (('closure-' if a.closure else 'prebrief-') + label)
    assert not out.exists(), 'label already held; not overwritten'
    out.mkdir(parents=True)
    gate = RobotsGate(UA)
    rows, made = [], 0
    for name, url, method, body, headers in PLAN:
        if made >= MAX_REQUESTS:
            sys.exit('ceiling of %d requests reached' % MAX_REQUESTS)
        row, requested = fetch(gate, name, url, method, body, headers, out)
        made += int(requested)
        rows.append(row)
        print(json.dumps({k: row.get(k) for k in ('name', 'status', 'bytes', 'emails_withheld')}), flush=True)
    fields = ['name', 'url', 'method', 'request_body', 'utc_start', 'status', 'content_type', 'last_modified',
              'bytes', 'sha256', 'emails_withheld', 'file', 'robots']
    with open(out / 'fetchlog.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(out)


if __name__ == '__main__':
    main()
