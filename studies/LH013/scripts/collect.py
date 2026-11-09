#!/usr/bin/env python3
"""LH013 collection. Every read is logged in data/read_log.csv by common.py. Stages, in the brief's order:
  eligibility  E1 LH012's coverage query (first and last day held per table and project, the five per-day
               tables of studies/LH012/data/clickpy_last_day_by_table.csv), which returns no count; E2 the
               parts of those tables and of pypi.pypi that hold 12 October 2026 (partition, part name, its
               first and last day and its modification time, no row count), to see whether the source can say
               when that day was first held
  days         L1 the days held per project over W1 and W2 (project and date only, pypi_downloads_per_day)
  meta         PyPI's JSON API for the 37 projects (raw bodies kept in data/pypi/)
  --- the stages below read counts and run only with LH013_PHASE=counts ---
  w0check      B1 W0 daily totals by project from pypi_downloads_per_day_by_version, for the baseline check
  totals       N1 daily totals by project, 25 September to 14 October 2026, for LH011's gap rule
  versions     V  per project, W1 and W2 sums by version (pypi_downloads_per_day_by_version)
  python       Y  per project, W1 and W2 sums by version and Python minor (..._by_version_by_python), split by
               Python minor where a result would pass 10,000 rows
  pass         C  per project and week, one pass of pypi.pypi computing, server side, the totals by class and CI
               flag (amendment 3), and the sizes of the 1,001 largest cells of the six fields and of the five (and
               of the same over older downloads only), with each largest cell's values
Usage: [LH013_PHASE=counts] python3 collect.py <stage> [project ...]"""
import csv, json, os, sys, datetime as dt
import common
from common import clickhouse, get_json, write_csv, read_csv, DATA

ROOT = os.path.dirname(os.path.dirname(DATA))
P37 = sorted({r['project'] for r in read_csv(os.path.join(ROOT, 'LH011', 'data', 'releases.csv'))})
assert len(P37) == 37
TABLES = ['pypi_downloads_per_day', 'pypi_downloads_per_day_by_version',
          'pypi_downloads_per_day_by_version_by_python', 'pypi_downloads_per_day_by_version_by_system',
          'pypi_downloads_per_day_by_version_by_installer_by_type']
WEEKS = {'W1': ('2026-09-28', '2026-10-04'), 'W2': ('2026-10-05', '2026-10-11')}
W0 = ('2026-09-21', '2026-09-27')


def ql(xs):
    return ','.join("'" + x.replace("'", "''") + "'" for x in xs)


def stage_eligibility():
    out = []
    for i, t in enumerate(TABLES, 1):
        rows = clickhouse('eligibility', f'E1.{i} last day held in {t}',
                          f"SELECT project, min(date) AS first_day, max(date) AS last_day FROM pypi.{t} "
                          f"WHERE project IN ({ql(P37)}) AND date >= '2025-09-01' GROUP BY project ORDER BY project")
        if rows is None:
            raise SystemExit('coverage query failed')
        out += [dict(table=t, **r) for r in rows]
    write_csv(os.path.join(DATA, 'eligibility', 'clickpy_last_day_by_table.csv'), out, ['table', 'project', 'first_day', 'last_day'])
    held = {(r['table'], r['project']): r['last_day'] for r in out}
    missing = [(t, p) for t in TABLES for p in P37 if (t, p) not in held]
    latest = min(held.values()) if held else ''
    met = not missing and all(v >= '2026-10-12' for v in held.values())
    print(json.dumps(dict(condition_met=met, pairs=len(held), missing=missing,
                          earliest_last_day=latest, latest_last_day=max(held.values()) if held else '')))
    rows = clickhouse('eligibility', 'E2 parts holding 12 October 2026',
                      "SELECT table, partition, name, min_date, max_date, modification_time, active FROM system.parts "
                      f"WHERE database = 'pypi' AND table IN ({ql(['pypi'] + TABLES)}) "
                      "AND min_date <= '2026-10-12' AND max_date >= '2026-10-12' ORDER BY table, modification_time",
                      'eligibility/parts_holding_2026-10-12.csv')
    print('parts rows:', None if rows is None else len(rows))


def stage_days():
    a, b = WEEKS['W1'][0], WEEKS['W2'][1]
    rows = clickhouse('days', 'L1 days held per project, W1 and W2',
                      f"SELECT DISTINCT project, date FROM pypi.pypi_downloads_per_day WHERE project IN ({ql(P37)}) "
                      f"AND date >= '{a}' AND date <= '{b}' ORDER BY project, date", 'days/days_held.csv')
    have = {(r['project'], r['date']) for r in rows}
    days = [str(dt.date(2026, 9, 28) + dt.timedelta(days=i)) for i in range(14)]
    missing = [dict(project=p, date=d) for p in P37 for d in days if (p, d) not in have]
    write_csv(os.path.join(DATA, 'days', 'days_not_held.csv'), missing, ['project', 'date'])
    print('project-days held', len(have), 'of', 37 * 14, '; not held', len(missing))


def stage_meta():
    os.makedirs(os.path.join(DATA, 'pypi'), exist_ok=True)
    for i, p in enumerate(P37, 1):
        path = os.path.join(DATA, 'pypi', p + '.json')
        if os.path.exists(path):
            continue
        status, d, body = get_json('meta', f'J{i:02d} {p}', f'https://pypi.org/pypi/{p}/json', f'pypi/{p}.json')
        if d is None:
            print('   HTTP', status, p)
            continue
        with open(path, 'w') as f:
            f.write(body)


def stage_docs():
    """The brief's fixed documentation read (Resource ceiling): the package index's own statement of what its
    download table counts, and the log parser that fills it, read before any count. Saved under data/docs/."""
    import hashlib
    pages = [('D1 PyPI BigQuery datasets page', 'https://docs.pypi.org/api/bigquery/', 'bigquery.html'),
             ('D2 linehaul log parser', 'https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/linehaul/events/parser.py', 'linehaul_parser.py.txt')]
    os.makedirs(os.path.join(DATA, 'docs'), exist_ok=True)
    for label, url, fn in pages:
        t = common.now()
        status, body, _ = common.curl(url)  # robots.txt-gated: status "not fetched: ..." when not allowed
        sha = hashlib.sha256(body.encode()).hexdigest()  # of the text received; email addresses are withheld from the kept file
        if not status.startswith('not fetched'):
            with open(os.path.join(DATA, 'docs', fn), 'w') as f:
                f.write(common.redact_bytes(body.encode())[0].decode())
        common.log(dict(read_utc=t, source='Documentation', stage='docs', label=label, endpoint=url, http_status=status,
                        read_bytes=len(body.encode()), output='docs/' + fn if not status.startswith('not fetched') else '',
                        note='sha256 ' + sha))
        print(label, status, len(body))


if __name__ == '__main__':
    stage = sys.argv[1]
    if stage in ("w0check", 'totals', 'versions', 'python', 'pass'):
        import collect_counts
        collect_counts.run(stage, sys.argv[2:])
    else:
        globals()['stage_' + stage]()

