#!/usr/bin/env python3
"""LH056 outcome read, as fixed in studies/LH056/brief.md (protocol 0.1). Adapted from studies/LH040/scripts/collect.py.
Run only under a schedule row (LH056-read-1, LH056-read-2), after the brief is committed. One read per UTC label;
a label already held is skipped, never overwritten.

Reads, each once: six queries to ClickPy's public SQL as user demo (Q1 to Q6 below, PyPI's download logs as ClickHouse
loads them) and one GET of pypistats.org's daily totals for agent-framework: seven requests, under the gate's ceiling of
LH040's seven queries per read (gate of 18 November 2026, condition 4). Only the package agent-framework is named in any
query (condition 6). Days run from 1 August 2026 (the comparison window) to 1 December 2026 (day 14) at most.

Every request is asked of scripts/robots_gate.py first (the keeper's rule of 8 November 2026; run with
LIGHTHOUSE_PROVIDER=anthropic under Claude Code, or every provider's tokens are obeyed). A URL the gate refuses is logged
"NotFetched", a missing reading and never a negative.

One retry per request, only on a timeout, a connection error, or HTTP 500, 502 or 504 (an error), and never after a
refusal, a challenge or a rate limit (any other 4xx, 503, NotFetched). Both attempts are logged. After each ClickPy query
the rows read by ClickHouse's own count (X-ClickHouse-Summary) are summed; if the sum passes 5 billion, no further query
is sent in this read and the rest are logged "not sent: ceiling". The CI query on pypi.pypi, the only heavy one, is last.

Bodies are kept raw under data/read-<label>/ after scripts/redact_emails.py redact_bytes, with fetchlog.csv (name, url,
method, request_body, attempt, utc_start, utc_finish, status, content_type, bytes, sha256 of the bytes received,
emails_withheld, read_rows, read_bytes, robots). User-Agent carries Lighthouse's robots token. No key, token or credential.

Usage:
  LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH056/scripts/collect.py --read 2026-11-21T1400Z
  python3 -I studies/LH056/scripts/collect.py --read <label> --dry-run   (prints the plan; sends nothing; asks no gate)
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import argparse
import csv
import json
import socket
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))

UA = 'Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)'
ROOT = Path(__file__).resolve().parents[1]
CH = 'https://sql-clickhouse.clickhouse.com/?user=demo&default_format=CSVWithNames'
CEILING_BYTES = 16 * 1024 * 1024
ROWS_CEILING = 5_000_000_000
RETRY_STATUSES = (500, 502, 504)
FORBIDDEN = ('files.pythonhosted.org', 'pypi.org', 'webhook.site', 'github.com', 'deps.dev', 'bigquery')

PROJECT = 'agent-framework'
FIRST_DAY, LAST_DAY = '2026-08-01', '2026-12-01'   # comparison window start; day 14 of the case
CASE = ('1.26.1', '1.26.2')
DAY0_CASE = '2026-11-17'
# Comparison releases (brief, "Population and unit"): every final agent-framework release first uploaded from
# 1 August to 12 November 2026 that was higher by PEP 440 than every final release uploaded before it, with the UTC day
# of its first upload (day 0), from PyPI's project page read at 2026-11-18T13:19:16Z (data/prebrief-2026-11-18T1319Z/).
COMPARISON = {
    '1.14.0': '2026-08-14', '1.15.0': '2026-08-21', '1.16.0': '2026-08-28', '1.17.0': '2026-09-03',
    '1.18.0': '2026-09-10', '1.19.0': '2026-09-18', '1.20.0': '2026-10-02', '1.21.0': '2026-10-08',
    '1.22.0': '2026-10-15', '1.23.0': '2026-10-22', '1.24.0': '2026-10-30', '1.25.0': '2026-11-07',
    '1.26.0': '2026-11-12',
}
PAIRS = dict(COMPARISON, **{v: DAY0_CASE for v in CASE})
PAIR_SQL = ', '.join("(toDate('%s'), '%s')" % (d, v) for v, d in sorted(PAIRS.items()))
DAY0_DATES = ', '.join("toDate('%s')" % d for d in sorted(set(PAIRS.values())))
# Days whose composition is read for every version: each comparison day 0, and 16 November to day 14.
DAY_FILTER = "(date IN (%s) OR date BETWEEN '2026-11-16' AND '%s')" % (DAY0_DATES, LAST_DAY)

QUERIES = [
    # Duplicate rows for one date (unmerged parts, LH040's method choice 1) are summed here, fixed before any count.
    ('Q1_daily_totals',
     "SELECT date, sum(count) AS count FROM pypi.pypi_downloads_per_day WHERE project = '%s' "
     "AND date BETWEEN '%s' AND '%s' GROUP BY date ORDER BY date" % (PROJECT, FIRST_DAY, LAST_DAY)),
    ('Q2_daily_by_version',
     "SELECT date, version, sum(count) AS count FROM pypi.pypi_downloads_per_day_by_version "
     "WHERE project = '%s' AND date BETWEEN '%s' AND '%s' GROUP BY date, version ORDER BY date, version"
     % (PROJECT, FIRST_DAY, LAST_DAY)),
    # Installer by version on the listed days; the package's installer totals per day are the sum over versions.
    ('Q3_installer',
     "SELECT date, version, installer, sum(count) AS count "
     "FROM pypi.pypi_downloads_per_day_by_version_by_installer_by_type WHERE project = '%s' AND %s "
     "GROUP BY date, version, installer ORDER BY date, version, installer" % (PROJECT, DAY_FILTER)),
    # File types from the file-type table only: the installer table's type column keeps an arbitrary value when rows
    # merge (studies/LH005/LH005.md), so it is summed away above.
    ('Q4_file_type',
     "SELECT date, version, type, sum(count) AS count "
     "FROM pypi.pypi_downloads_per_day_by_version_by_file_type WHERE project = '%s' AND %s "
     "GROUP BY date, version, type ORDER BY date, version, type" % (PROJECT, DAY_FILTER)),
    ('Q5_system',
     "SELECT date, version, system, sum(count) AS count "
     "FROM pypi.pypi_downloads_per_day_by_version_by_system WHERE project = '%s' AND %s "
     "GROUP BY date, version, system ORDER BY date, version, system" % (PROJECT, DAY_FILTER)),
    ('Q6_ci',
     "SELECT date, version, installer, ci, count() AS count FROM pypi.pypi WHERE project = '%s' "
     "AND (date, version) IN (%s) GROUP BY date, version, installer, ci ORDER BY date, version, installer, ci"
     % (PROJECT, PAIR_SQL)),
]
GETS = [('pypistats_overall', 'https://pypistats.org/api/packages/%s/overall' % PROJECT)]
MAX_REQUESTS = 7   # first attempts; retries are at most one per request and logged


def brief_committed():
    """The brief is tracked by git and unchanged since the last commit (AGENTS.md: commit before any outcome)."""
    try:
        tracked = subprocess.run(['git', '-C', str(ROOT), 'ls-files', '--error-unmatch', 'brief.md'],
                                 capture_output=True).returncode == 0
        clean = subprocess.run(['git', '-C', str(ROOT), 'diff', '--quiet', 'HEAD', '--', 'brief.md'],
                               capture_output=True).returncode == 0
        return tracked and clean
    except OSError:
        return False


def attempt(gate, name, url, body, out, n):
    from redact_emails import redact_bytes  # noqa: E402  email addresses withheld
    from lh_fetch import save_body  # noqa: E402  what may be kept (the keeper, 21 November 2026)
    row = {'name': name, 'url': url, 'method': 'POST' if body else 'GET', 'request_body': body or '', 'attempt': n,
           'utc_start': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    ok, info = gate.check(url)
    row['robots'] = '%s (%s, group %s, rule %s)' % (info.get('reason'), info.get('robots_url'),
                                                     info.get('decided_by', ''), info.get('rule', ''))
    if not ok:
        row['status'] = 'NotFetched'
        return row, False
    retryable = False
    payload, final, headers = b'', url, None
    try:
        req = Request(url, data=body.encode() if body else None, headers={'User-Agent': UA})
        try:
            resp = urlopen(req, timeout=180)
        except HTTPError as err:
            resp = err
        with resp:
            payload, final, headers = resp.read(CEILING_BYTES + 1), resp.geturl() or url, resp.headers
            summary = resp.headers.get('X-ClickHouse-Summary', '')
            try:
                s = json.loads(summary) if summary else {}
            except ValueError:
                s = {}
            row.update(status=resp.status, content_type=resp.headers.get('Content-Type', ''),
                       read_rows=s.get('read_rows', ''), read_bytes=s.get('read_bytes', ''))
            retryable = resp.status in RETRY_STATUSES
    except (socket.timeout, TimeoutError, URLError, ConnectionError) as err:
        row['status'] = 'error: ' + type(err).__name__ + ': ' + str(err)[:200]
        retryable = True
    except Exception as err:  # recorded, nothing invented, not retried
        row['status'] = 'error: ' + type(err).__name__ + ': ' + str(err)[:200]
    row.update(utc_finish=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), bytes=len(payload),
               sha256=sha256(payload).hexdigest() if payload else '')
    if payload and len(payload) <= CEILING_BYTES:
        kept, why = save_body(out / ('%s.attempt%d.raw' % (name, n)), payload, final, headers)
        if kept:  # the keeper, 21 November 2026: no body kept where robots.txt or the page refuses it
            row.update(file='%s.attempt%d.raw' % (name, n), emails_withheld=redact_bytes(payload)[1])
        else:
            row['body_kept'] = 'no: ' + why
    elif payload:
        row['status'] = str(row.get('status')) + ' (over the 16 MiB ceiling; no body retained)'
    return row, retryable


def plan():
    return [(n, CH, sql) for n, sql in QUERIES] + [(n, url, None) for n, url in GETS]


def main():
    ap = argparse.ArgumentParser(description='LH056 outcome read (studies/LH056/brief.md).')
    ap.add_argument('--read', required=True, help='UTC label, YYYY-MM-DDTHHMMZ')
    ap.add_argument('--dry-run', action='store_true', help='print the requests; send nothing, ask no gate')
    a = ap.parse_args()
    datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
    p = plan()
    assert len(p) <= MAX_REQUESTS
    for name, url, body in p:
        assert not any(f in url for f in FORBIDDEN), 'refused: ' + url
        assert body is None or ("'%s'" % PROJECT in body and body.count("project = '") == 1), 'one package only'
    if a.dry_run:
        for name, url, body in p:
            print(json.dumps({'name': name, 'url': url, 'method': 'POST' if body else 'GET', 'body': body}))
        print(json.dumps({'dry_run': True, 'brief_committed': brief_committed(),
                          'out': str(ROOT / 'data' / ('read-' + a.read))}))
        return
    if not brief_committed():
        sys.exit('brief.md is not committed (or has uncommitted changes): no read before the protocol is fixed')
    import lh_fetch  # noqa: E402  its robots.txt gate (the keeper's rule, 8 November 2026), for fetching and keeping alike
    out = ROOT / 'data' / ('read-' + a.read)
    if out.exists():
        print('label already held; skipped:', out)
        return
    out.mkdir(parents=True)
    gate = lh_fetch  # lh_fetch.check(url): the same gate save_body asks
    rows, rows_read = [], 0
    for name, url, body in p:
        if url == CH and rows_read > ROWS_CEILING:
            rows.append({'name': name, 'url': url, 'status': 'not sent: ceiling of 5 billion rows read passed'})
            continue
        tries = [attempt(gate, name, url, body, out, 1)]
        if tries[0][1]:
            tries.append(attempt(gate, name, url, body, out, 2))   # one retry, on an error or timeout only
        for row, _ in tries:
            rows.append(row)
            try:
                rows_read += int(row.get('read_rows') or 0)
            except ValueError:
                pass
            print(json.dumps({k: row.get(k) for k in ('name', 'attempt', 'status', 'bytes', 'read_rows')}), flush=True)
    fields = ['name', 'url', 'method', 'request_body', 'attempt', 'utc_start', 'utc_finish', 'status', 'content_type',
              'bytes', 'sha256', 'emails_withheld', 'file', 'read_rows', 'read_bytes', 'robots', 'body_kept']
    with open(out / 'fetchlog.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(out)


if __name__ == '__main__':
    main()
