#!/usr/bin/env python3
"""Read LH013 coverage and date presence only; never request download counts.

The record of the preflight of 22 October 2026; it refuses to run again once its directory exists. From
21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) each query goes through
scripts/lh_fetch.py's urlopen (before, the curl command, after the same robots.txt gate; urlopen asks the
same cached gate), the response's header block is written as <label>.headers as curl -D wrote it, and the
CSV body is saved only through lh_fetch's save_body; where it may not be kept no .csv is written and the
log row gets body_kept "no: <reason>". The status logged is the HTTP code as text, '000' where no response
came, 'not fetched' where robots.txt refused a redirect (each redirect is checked, check_redirects=True; curl
-L followed them unchecked); stderr holds the exception or the refusal where there was one.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH013/scripts/preflight.py`."""
import csv
import hashlib
import io
import json
import urllib.error
import urllib.request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, check as robots_check, NotFetched, UA, save_body  # noqa: E402  robots.txt gate (8 November 2026); one keep path (21 November)
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'LH013' / 'data' / 'preflight-2026-10-22'
OUT.mkdir(parents=True, exist_ok=False)
projects = sorted({r['project'] for r in csv.DictReader((ROOT / 'LH011/data/releases.csv').open())})
names = ','.join("'" + p.replace("'", "''") + "'" for p in projects)
tables = ('pypi_downloads_per_day', 'pypi_downloads_per_day_by_version',
          'pypi_downloads_per_day_by_version_by_python',
          'pypi_downloads_per_day_by_version_by_system',
          'pypi_downloads_per_day_by_version_by_installer_by_type')
log = []


def query(label, sql):
    assert 'count(' not in sql.lower() and 'sum(' not in sql.lower()
    start = datetime.now(timezone.utc).isoformat(timespec='seconds')
    endpoint = 'https://sql-clickhouse.clickhouse.com/?user=demo'
    ok, info = robots_check(endpoint)  # the robots.txt gate (the keeper, 8 November 2026)
    if not ok:  # not requested: a missing reading, never a negative
        why = 'not fetched: %s (robots %s, status %s, group %s, rule %s)' % (info.get('reason'), info.get('robots_url'),
              info.get('robots_status'), info.get('decided_by', ''), info.get('rule', ''))
        log.append(dict(label=label, observed_at_utc=start, query=sql, status=why, bytes=0, sha256='', stderr=''))
        raise RuntimeError(f'{label}: {why}')
    req = urllib.request.Request(endpoint, data=(sql + ' FORMAT CSVWithNames').encode(), headers={'User-Agent': UA})
    body, status, stderr, final, hdrs = b'', b'000', '', endpoint, None
    try:
        try:
            resp = urlopen(req, timeout=90, check_redirects=True)
        except urllib.error.HTTPError as e:
            resp = e
        with resp:
            body, status, final, hdrs = resp.read(), str(resp.status).encode(), resp.geturl() or endpoint, resp.headers
        (OUT / (label + '.headers')).write_text('HTTP/1.1 %s %s\r\n%s\r\n' % (  # the response's header block, not its body
            resp.status, getattr(resp, 'reason', ''), ''.join('%s: %s\r\n' % kv for kv in hdrs.items())))
    except NotFetched as e:  # a redirect robots.txt refuses: not requested
        status = b'not fetched'
        stderr = str(e)
    except Exception as e:
        stderr = '%s: %s' % (type(e).__name__, e)
    # no response (an error or a refused redirect): nothing to keep, no file
    kept, why = save_body(OUT / (label + '.csv'), body, final, hdrs) if hdrs is not None else (True, '')
    row = dict(label=label, observed_at_utc=start, query=sql, status=status.decode(errors='replace'),
               bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), stderr=stderr)
    if not kept:
        row['body_kept'] = 'no: ' + why
    log.append(row)
    if stderr or status != b'200':
        raise RuntimeError(f'{label}: {status!r} {stderr[:200]!r}')
    return list(csv.DictReader(io.StringIO(body.decode())))


try:
    covered = {}
    for table in tables:
        sql = (f'SELECT project, min(date) AS first_day, max(date) AS last_day FROM pypi.{table} '
               f"WHERE project IN ({names}) AND date >= '2025-09-01' GROUP BY project ORDER BY project")
        rows = query('coverage_' + table, sql)
        covered[table] = {r['project']: r['last_day'] for r in rows}
    eligible = all(covered[t].get(p, '') >= '2026-10-12' for t in tables for p in projects)
    if eligible:
        sql = (f'SELECT DISTINCT project, date FROM pypi.pypi_downloads_per_day '
               f"WHERE project IN ({names}) AND date >= '2026-09-28' AND date <= '2026-10-11' "
               'ORDER BY project, date')
        dates = query('week_dates', sql)
        present = {(r['project'], r['date']) for r in dates}
        from datetime import date, timedelta
        days = [str(date(2026, 9, 28) + timedelta(days=i)) for i in range(14)]
        missing = [{'project': p, 'date': d} for p in projects for d in days if (p, d) not in present]
        (OUT / 'missing_dates.json').write_text(json.dumps(missing, indent=2) + '\n')
    print(json.dumps({'eligible': eligible, 'projects': len(projects), 'latest_by_table':
                      {t: sorted(set(covered[t].values())) for t in tables},
                      'missing_week_dates': len(missing) if eligible else None}))
finally:
    (OUT / 'read_log.json').write_text(json.dumps(log, indent=2) + '\n')
