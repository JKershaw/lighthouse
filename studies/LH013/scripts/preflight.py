#!/usr/bin/env python3
"""Read LH013 coverage and date presence only; never request download counts."""
import csv
import hashlib
import io
import json
import subprocess
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
    response = subprocess.run(['curl', '--max-time', '90', '-sS', '-D', str(OUT / (label + '.headers')),
                               '-w', '\nHTTP %{http_code}', 'https://sql-clickhouse.clickhouse.com/?user=demo',
                               '--data-binary', '@-'], input=(sql + ' FORMAT CSVWithNames').encode(),
                              capture_output=True, timeout=100)
    body, _, status = response.stdout.rpartition(b'\nHTTP ')
    (OUT / (label + '.csv')).write_bytes(body)
    log.append(dict(label=label, observed_at_utc=start, query=sql, status=status.decode(errors='replace'),
                    bytes=len(body), sha256=hashlib.sha256(body).hexdigest(), stderr=response.stderr.decode()))
    if response.returncode or status != b'200':
        raise RuntimeError(f'{label}: {status!r} {response.stderr[:200]!r}')
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
