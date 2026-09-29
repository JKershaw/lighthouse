#!/usr/bin/env python3
"""LH014 phase 3: every download count, read after amendment 1 was snapshotted (commit 514f4bd), with
LH014_PHASE=3. common.py refuses any query that could read a day after 2026-09-27, adds
read_overflow_mode = 'throw' to every query, and treats one that reports reading a per-query limit as
failed. Projects are read in data/project_order.csv's order (A1, B1, A2 and so on), and the steps run
in the brief's order (Stopping condition):

  G01  daily totals of the 160 drawn projects, pypi_downloads_per_day, 25 March to 27 September 2026,
       split by date under 10,000 rows (the gap rule; the check against the by-version table)
  V..  per project with a qualifying release: daily downloads by version, pypi_downloads_per_day_by_version,
       from seven days before its first day 0 to 30 days after its last or 27 September, with every version
       outside the numerator set (non-pre-release versions PyPI lists at or above the project's earliest
       qualifying release) folded server-side into '~other' (data/counts/<project>.csv)
  M..  per project with a qualifying release: the installer table on each release's days 0 to 2, by date,
       version (numerator set, else '~other') and installer, every installer outside the mirror class
       (amendment 1: Artifactory, bandersnatch, devpi; z3c.pypimirror, absent, is kept in the rule)
       folded into '~not mirror' (data/mirror/<project>.csv)
  C..  per project with a CI-subsample release: pypi.pypi on each subsample release's days 0 to 2 for the
       release and the one it replaced, by date, version, installer and flag, in one query per project
       (data/ci/<project>.csv)

Adapted from studies/LH011/scripts/collect_counts.py. What changed: 160 projects in two bands read in an
alternating order; every date stops at the cut; the mirror reads (M) are new; the CI reads are batched
per project with (date, version) pairs instead of one query per release; pypistats is not read; a part
that fails a limit is halved and read again. A project whose file exists is skipped, so a run that
stops can be resumed. Usage: LH014_PHASE=3 python3 collect_counts.py [G|V|M|C ...]   (default: all four)"""
import datetime, os, sys
from packaging.version import Version
import common
from common import clickhouse, read_csv, write_csv, DATA

if common.PHASE in ('1', '2'):
    raise SystemExit('counts are read in phase 3 only: set LH014_PHASE=3')
CUT, D, ONE = datetime.date(2026, 9, 27), datetime.date.fromisoformat, datetime.timedelta(days=1)
MCLASS = "if(lower(installer) IN ('bandersnatch','z3c.pypimirror','artifactory','devpi'), installer, '~not mirror')"
steps = sys.argv[1:] or ['G', 'V', 'M', 'C']
q = lambda xs: ','.join("'%s'" % x for x in xs)
order = read_csv('project_order.csv')
releases = read_csv('releases.csv')
versions = read_csv('pypi_versions.csv')
for sub in ('counts', 'mirror', 'ci'):
    os.makedirs(os.path.join(DATA, sub), exist_ok=True)


def nset(p, rel):
    lo = min(Version(r['version']) for r in rel)
    return [v for v in versions if v['project'] == p and v['parse'] == 'ok' and v['is_prerelease'] == 'False'
            and Version(v['version']) >= lo]


def split(items, weight, cap=8000):
    """Consecutive runs of items whose summed weight stays under cap."""
    out, cur, est = [], [], 0
    for it in items:
        w = weight(it)
        if cur and est + w > cap:
            out.append(cur)
            cur, est = [], 0
        cur.append(it)
        est += w
    return out + ([cur] if cur else [])


def run(label, sql_for, parts):
    rows, stack, k = [], list(parts), 0
    while stack:
        part = stack.pop(0)
        k += 1
        try:
            rows += clickhouse(f'{label} {k}', sql_for(part))
        except SystemExit as e:
            if len(part) == 1 or 'ceiling' in str(e):
                raise
            print(f'{label} {k}: {str(e)[:100]}; halving')
            stack[0:0] = [part[:len(part) // 2], part[len(part) // 2:]]
    return rows


if 'G' in steps and not os.path.exists(os.path.join(DATA, 'daily_totals.csv')):
    names = [o['project'] for o in order]
    days = [D('2026-03-25') + k * ONE for k in range((CUT - D('2026-03-25')).days + 1)]
    rows = run('G01 daily totals', lambda part: f"SELECT project, date, sum(count) AS downloads FROM pypi.pypi_downloads_per_day "
               f"WHERE project IN ({q(names)}) AND date BETWEEN '{part[0]}' AND '{part[-1]}' GROUP BY project, date",
               split(days, lambda d: len(names)))
    rows.sort(key=lambda r: (r['project'], r['date']))
    write_csv('daily_totals.csv', rows, ['project', 'date', 'downloads'])
    print('G: rows', len(rows))

for step in ('V', 'M', 'C'):
    if step not in steps:
        continue
    done = 0
    for o in order:
        p = o['project']
        rel = [r for r in releases if r['project'] == p]
        out = {'V': f'counts/{p}.csv', 'M': f'mirror/{p}.csv', 'C': f'ci/{p}.csv'}[step]
        if not rel or os.path.exists(os.path.join(DATA, out)):
            continue
        ns = nset(p, rel)
        vs = q(v['version'] for v in ns)
        up = lambda d: 1 + sum(1 for v in ns if D(v['first_upload_utc'][:10]) <= d)
        lab = f'{step}{int(o["read_order"]):03d} {p}'
        if step == 'V':
            a = D(min(r['day0'] for r in rel)) - 7 * ONE
            b = min(D(max(r['day0'] for r in rel)) + 30 * ONE, CUT)
            days = [a + k * ONE for k in range((b - a).days + 1)]
            rows = run(lab, lambda part: f"SELECT date, if(version IN ({vs}), version, '~other') AS v, sum(count) AS downloads "
                       f"FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' AND date BETWEEN '{part[0]}' "
                       f"AND '{part[-1]}' GROUP BY date, v ORDER BY date, v", split(days, up))
            fields = ['date', 'v', 'downloads']
        elif step == 'M':
            days = sorted(d for d in {D(r['day0']) + k * ONE for r in rel for k in range(3)} if d <= CUT)
            rows = run(lab, lambda part: f"SELECT date, if(version IN ({vs}), version, '~other') AS v, {MCLASS} AS installer_class, "
                       f"sum(count) AS downloads FROM pypi.pypi_downloads_per_day_by_version_by_installer_by_type WHERE project = '{p}' "
                       f"AND date IN ({q(str(d) for d in part)}) GROUP BY date, v, installer_class ORDER BY date, v, installer_class",
                       split(days, lambda d: 4 * up(d)))
            fields = ['date', 'v', 'installer_class', 'downloads']
        else:
            sub = [r for r in rel if r['ci_subsample'] == 'True']

            def sql(part):
                prs = sorted({(str(D(r['day0']) + k * ONE), v) for r in part for k in range(3)
                              for v in (r['version'], r['replaced_version'])})
                tup = ','.join(f"(toDate('{d}'), '{v}')" for d, v in prs)
                return (f"SELECT date, version, installer, toString(ci) AS ci, count() AS downloads FROM pypi.pypi "
                        f"WHERE project = '{p}' AND date IN ({q(sorted({d for d, _ in prs}))}) AND (date, version) IN ({tup}) "
                        f"GROUP BY date, version, installer, ci ORDER BY date, version, installer, ci")
            rows = run(lab, sql, [sub])
            rows = list({(r['date'], r['version'], r['installer'], r['ci']): r for r in rows}.values())
            rows.sort(key=lambda r: (r['date'], r['version'], r['installer'], r['ci']))
            fields = ['date', 'version', 'installer', 'ci', 'downloads']
        write_csv(out, rows, fields)
        done += 1
    print(f'{step}: projects read {done}')
q_, r_, p_, d_ = common.spent()
print(f'reads so far: ClickPy {q_} queries, {r_:,} rows read; PyPI {p_}; documentation {d_}')
