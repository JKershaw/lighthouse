#!/usr/bin/env python3
"""LH012 phase 2 collection, run only after the brief's snapshot (issue #14, 06:35 UTC on
29 September 2026), with every read logged in data/read_log_phase2.csv (amendment 1).
Stages, in order:
  week      the 37 projects on W: W1 downloads by day and version; W2 W sums by version and Python
            minor; W3 one grouped pass of pypi.pypi (class, installer, ci, system, libc.lib, type);
            W4 the file-name pass of older downloads for the ten projects with platform wheels
  deps      D1 the dependents' downloads by day and version on W
  pypi      Q the requirements of the 37's versions at or above R, then of each dependent's versions
            in descending order of W downloads (95 per cent or 25 versions, 200 for the X of a
            tightly coupled pair), dependents in LH010 rank order
  markers   D2 W sums by version and Python minor for dependents with a Python marker on one of the 37
  firstday  N1 daily totals of the 37 for the gap rule; N2 per-version downloads on days 1, 2 and 30
            of each November to March release
Writes data/week/, data/deps/, data/firstday/, data/dependent_reads.csv, data/requirements_phase2.csv.
Adapted from studies/LH011/scripts/collect_counts.py. What changed: the tables and grouping are this
brief's; a failed or oversized query is split by day and then by Python minor (amendment 1).
Usage: LH012_PHASE=2 python3 collect.py <stage>"""
import csv, io, json, os, sys
from packaging.version import Version
from packaging.specifiers import SpecifierSet
from packaging.requirements import Requirement, InvalidRequirement
from packaging.utils import canonicalize_name
import common
import phase2  # noqa: F401  (sets the log, phase and ceilings)
from common import read_csv, DATA

W0, W1 = '2026-09-21', '2026-09-27'
DAYS = [f'2026-09-{d}' for d in range(21, 28)]
ROOT = os.path.dirname(os.path.dirname(DATA))
REF = {r['project']: r for r in read_csv('reference.csv')}
P37 = sorted(REF)
AUG = {r['project']: int(r['downloads']) for r in csv.DictReader(open(os.path.join(ROOT, 'LH011', 'data', 'clickpy_top_projects_2026_08.csv')))}
TOP = {r['project']: int(r['rank']) for r in csv.DictReader(open(os.path.join(ROOT, 'LH010', 'data', 'top500.csv')))}
TOPD = {r['project']: int(r['downloads']) for r in csv.DictReader(open(os.path.join(ROOT, 'LH010', 'data', 'top500.csv')))}
BIG = 40_000_000 * 31  # August downloads above which a project's pypi.pypi pass is read day by day
WHEELED = ['aiohttp', 'cffi', 'charset-normalizer', 'cryptography', 'litellm', 'numpy', 'pandas', 'protobuf',
           'pydantic-core', 'rpds-py']


def ql(xs):
    return ','.join("'%s'" % x for x in xs)


def lists(p):
    """(versions at or above R, pre-releases above R) from the metadata."""
    R = Version(REF[p]['R'])
    ge = REF[p]['versions_ge_R'].split()
    oth = []
    for v in VERS[p]:
        if v['parse'] == 'ok' and v['is_prerelease'] == 'True' and Version(v['version']) > R:
            oth.append(v['version'])
    return ge, oth


VERS = {}
for v in read_csv('versions.csv'):
    VERS.setdefault(v['project'], []).append(v)


def run(label, sql, out):
    """Run; on an error (a limit), return None so the caller can split."""
    try:
        rows = common.clickhouse(label, sql)
    except SystemExit as e:
        if 'ceiling' in str(e) or 'refused' in str(e):
            raise
        print('   split after:', str(e)[:160])
        return None
    # ClickHouse can answer HTTP 200 and then stream an exception into the body (for example when the
    # result passes 10,000 rows): such a response is logged as read but treated here as failed.
    if any(isinstance(v, str) and ('__exception__' in v or 'DB::Exception' in v) for r in rows for v in list(r.values()) + list(r.keys())):
        print('   exception in body, split:', label)
        return None
    return rows


def must(r, label):
    if r is None:
        raise SystemExit(f'{label}: could not be read within the limits')
    return r


def save(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields})


def ok(path):
    return os.path.exists(path) and '__exception__' not in open(path).read()


def by_days(label, template, fields, path, days=DAYS, pysplit=False):
    """template has {dates}; tried for the whole list, then day by day, then (if pysplit) by Python halves."""
    if ok(path):
        return None
    rows = run(label, template.format(dates=ql(days)), path)
    if rows is None:
        rows = []
        for d in days:
            r = run(f'{label} {d}', template.format(dates=ql([d])), path)
            if r is None and pysplit:
                r = []
                for half, cond in (('a', "python_minor < '3.11'"), ('b', "python_minor >= '3.11'")):
                    r += must(run(f'{label} {d} {half}', template.format(dates=ql([d])).replace('WHERE ', f'WHERE {cond} AND ', 1), path), label)
            if r is None:
                raise SystemExit(f'{label} {d}: could not be read within the limits')
            rows += r
    save(path, rows, fields)
    return rows


def stage_week():
    for p in P37:
        ge, oth = lists(p)
        by_days(f'W1 {p} by day and version',
                f"SELECT date, version, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' "
                "AND date IN ({dates}) GROUP BY date, version ORDER BY date, version",
                ['date', 'version', 'n'], os.path.join(DATA, 'week', 'versions', p + '.csv'))
        if ok(os.path.join(DATA, 'week', 'python', p + '.csv')) and ok(os.path.join(DATA, 'week', 'pass', p + '.csv')) and (p not in WHEELED or ok(os.path.join(DATA, 'week', 'files', p + '.csv'))):
            continue
        rows = None if ok(os.path.join(DATA, 'week', 'python', p + '.csv')) else run(f'W2 {p} W sums by version and Python',
                   f"SELECT version, python_minor, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version_by_python "
                   f"WHERE project = '{p}' AND date BETWEEN '{W0}' AND '{W1}' GROUP BY version, python_minor ORDER BY version, python_minor", None)
        if rows is None and not ok(os.path.join(DATA, 'week', 'python', p + '.csv')):
            rows = []
            mins = ['', '2.7'] + ['3.%d' % i for i in range(4, 16)]
            conds = [(m or 'none', f"python_minor = '{m}'") for m in mins] + [('rest', f"python_minor NOT IN ({ql(mins)})")]
            for half, cond in conds:
                rows += must(run(f'W2 {p} {half}', f"SELECT version, python_minor, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version_by_python "
                            f"WHERE {cond} AND project = '{p}' AND date BETWEEN '{W0}' AND '{W1}' GROUP BY version, python_minor", None), p)
        if rows is not None:
            save(os.path.join(DATA, 'week', 'python', p + '.csv'), rows, ['version', 'python_minor', 'n'])
        cls = f"multiIf(version IN ({ql(ge)}), 'at_or_newer', version IN ({ql(oth) or ql(['-'])}), 'other', 'older')"
        t = (f"SELECT date, {cls} AS cls, installer, ci, system, tupleElement(libc, 'lib') AS libc_lib, type, count() AS n "
             f"FROM pypi.pypi WHERE project = '{p}' AND date IN ({{dates}}) GROUP BY date, cls, installer, ci, system, libc_lib, type")
        path = os.path.join(DATA, 'week', 'pass', p + '.csv')
        fields = ['date', 'cls', 'installer', 'ci', 'system', 'libc_lib', 'type', 'n']
        if ok(path):
            pass
        elif AUG[p] > BIG:
            rows = []
            for d in DAYS:
                rows += must(run(f'W3 {p} pass {d}', t.format(dates=ql([d])), path), f'W3 {p} {d}')
            save(path, rows, fields)
        else:
            by_days(f'W3 {p} pass', t, fields, path)
        if p in WHEELED:
            # amendment 2: grouped by the downloaded file's wheel tags (parts of its name), not the name itself
            parts = "splitByChar('-', substring(filename, 1, greatest(length(filename) - 4, 0)))"
            whl = "endsWith(filename, '.whl')"
            t = (f"SELECT python_minor, if({whl}, arrayElement({parts}, -3), '') AS interp, if({whl}, arrayElement({parts}, -2), '') AS abi, "
                 f"if({whl}, arrayElement({parts}, -1), if(filename = '', '(no file name)', '(not a wheel)')) AS plat, count() AS n "
                 f"FROM pypi.pypi WHERE project = '{p}' AND date IN ({{dates}}) AND version NOT IN ({ql(ge + oth)}) "
                 "GROUP BY python_minor, interp, abi, plat")
            by_days(f'W4 {p} file tags', t, ['python_minor', 'interp', 'abi', 'plat', 'n'],
                    os.path.join(DATA, 'week', 'files', p + '.csv'), pysplit=True)


def dependents():
    pairs = read_csv('pairs.csv')
    return sorted({r['dependent'] for r in pairs} - set(P37), key=lambda x: TOP[x])


def stage_deps():
    deps = dependents()
    for i in range(0, len(deps), 6):
        grp = deps[i:i + 6]
        if all(ok(os.path.join(DATA, 'deps', 'versions', d + '.csv')) for d in grp):
            continue
        t = (f"SELECT project, date, version, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version WHERE project IN ({ql(grp)}) "
             "AND date IN ({dates}) GROUP BY project, date, version ORDER BY project, date, version")
        rows = run(f'D1 dependents {i // 6 + 1:02d}', t.format(dates=ql(DAYS)), None)
        if rows is None:
            rows = []
            for d in grp:
                r = run(f'D1 dependent {d}', t.replace(f'project IN ({ql(grp)})', f"project IN ('{d}')").format(dates=ql(DAYS)), None)
                if r is None:
                    r = []
                    for day in DAYS:
                        r += must(run(f'D1 dependent {d} {day}', t.replace(f'project IN ({ql(grp)})', f"project IN ('{d}')").format(dates=ql([day])), None), d)
                rows += r
        for d in grp:
            save(os.path.join(DATA, 'deps', 'versions', d + '.csv'), [r for r in rows if r['project'] == d], ['date', 'version', 'n'])


def tight_pairs():
    """The brief's rule (as in phase 1): X's requirement on D outside any extra, in a version of X newest
    during W, with an upper bound, admitting ten or fewer of D's versions released by the end of W, and
    X's August downloads (LH010's top 500) at least a tenth of D's."""
    wk = {(r['dependent'], r['version']) for r in read_csv('week_versions.csv')}
    vers = {}
    for v in read_csv('versions.csv'):
        if v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and v['first_upload_utc'] <= '2026-09-27T23:59:59.999999':
            vers.setdefault(v['project'], []).append(Version(v['version']))
    out = {}
    for r in read_csv('pairs.csv'):
        if r['extra_only'] == 'True' or (r['dependent'], r['dependent_version']) not in wk or r['has_upper_bound'] != 'True':
            continue
        n = sum(SpecifierSet(r['specifier']).contains(v) for v in vers[r['project']])
        k = (r['dependent'], r['project'])
        out[k] = min(out.get(k, 99), n)
    return sorted(k for k, n in out.items() if n <= 10 and TOPD[k[0]] >= 0.1 * TOPD[k[1]])


def wsums(path):
    s = {}
    for r in csv.DictReader(open(path)):
        s[r['version']] = s.get(r['version'], 0) + int(r['n'])
    return s


def parse_all(dep, ver, rd, out):
    for s in rd:
        try:
            req = Requirement(s)
        except InvalidRequirement:
            out.append(dict(dependent=dep, dependent_version=ver, name='', specifier='', marker='', parse='invalid', requirement=s))
            continue
        n = canonicalize_name(req.name)
        if n in REF and n != dep:
            out.append(dict(dependent=dep, dependent_version=ver, name=n, specifier=str(req.specifier),
                            marker=str(req.marker) if req.marker else '', parse='ok', requirement=s))


def stage_pypi():
    reads_path = os.path.join(DATA, 'dependent_reads.csv')
    req_path = os.path.join(DATA, 'requirements_phase2.csv')
    reads = read_csv('dependent_reads.csv') if os.path.exists(reads_path) else []
    reqs = read_csv('requirements_phase2.csv') if os.path.exists(req_path) else []
    done = {(r['dependent'], r['version']) for r in reads}
    # phase 1's reads count as read: the latest at the read and the versions newest during W
    for r in read_csv('top500_screen.csv'):
        done.add((r['project'], r['latest_version']))
    for r in read_csv('week_versions.csv'):
        done.add((r['dependent'], r['version']))
    tx = {x for x, _ in tight_pairs()}
    todo = []
    for p in P37:
        for v in REF[p]['versions_ge_R'].split():
            todo.append((p, v, 'version at or above R'))
    for d in [p for p in P37 if p in {r['dependent'] for r in read_csv('pairs.csv')}] + dependents():
        path = os.path.join(DATA, 'week', 'versions', d + '.csv') if d in REF else os.path.join(DATA, 'deps', 'versions', d + '.csv')
        s = wsums(path)
        tot = sum(s.values())
        cap = 200 if d in tx else 25
        cum = 0
        for i, (v, n) in enumerate(sorted(s.items(), key=lambda x: (-x[1], x[0]))):
            if i >= cap or (tot and cum >= 0.95 * tot):
                break
            cum += n
            todo.append((d, v, f'coverage {i + 1}'))
    k = 0
    try:
        for d, v, why in todo:
            if (d, v) in done:
                continue
            done.add((d, v))
            k += 1
            status, js = common.get_json('PyPI JSON API', f'Q{k:04d} {d} {v}', f'https://pypi.org/pypi/{d}/{v}/json', 'requirements_phase2.csv')
            reads.append(dict(dependent=d, version=v, why=why, status=status))
            if js is not None:
                parse_all(d, v, js['info'].get('requires_dist') or [], reqs)
            if k % 100 == 0:
                save(reads_path, reads, ['dependent', 'version', 'why', 'status'])
                save(req_path, reqs, ['dependent', 'dependent_version', 'name', 'specifier', 'marker', 'parse', 'requirement'])
    finally:
        save(reads_path, reads, ['dependent', 'version', 'why', 'status'])
        save(req_path, reqs, ['dependent', 'dependent_version', 'name', 'specifier', 'marker', 'parse', 'requirement'])


def stage_markers():
    names = set()
    for r in read_csv('requirements.csv') + read_csv('requirements_phase2.csv'):
        m = r['marker']
        if ('python_version' in m or 'python_full_version' in m) and r['dependent'] not in REF:
            names.add(r['dependent'])
    for d in sorted(names, key=lambda x: TOP[x]):
        rows = run(f'D2 {d} W sums by version and Python',
                   f"SELECT version, python_minor, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version_by_python "
                   f"WHERE project = '{d}' AND date BETWEEN '{W0}' AND '{W1}' GROUP BY version, python_minor", None)
        save(os.path.join(DATA, 'deps', 'python', d + '.csv'), must(rows, d), ['version', 'python_minor', 'n'])


def stage_firstday():
    nm = read_csv('releases_nov_mar.csv')
    for i, (a, b) in enumerate((('2025-10-01', '2026-01-31'), ('2026-02-01', '2026-05-31'), ('2026-09-14', '2026-09-28'))):
        rows = run(f'N1 daily totals {i + 1}', f"SELECT project, date, sum(count) AS n FROM pypi.pypi_downloads_per_day "
                   f"WHERE project IN ({ql(P37)}) AND date BETWEEN '{a}' AND '{b}' GROUP BY project, date ORDER BY project, date", None)
        save(os.path.join(DATA, 'firstday', f'daily_totals_{i + 1}.csv'), rows, ['project', 'date', 'n'])
    import datetime as dt
    for p in P37:
        rel = [r for r in nm if r['project'] == p]
        if not rel:
            continue
        first = min(Version(r['version']) for r in rel)
        keep = sorted({v['version'] for v in VERS[p] if v['parse'] == 'ok' and v['is_prerelease'] == 'False' and Version(v['version']) >= first},
                      key=Version)
        dates = sorted({str(dt.date.fromisoformat(r['day0']) + dt.timedelta(days=k)) for r in rel for k in (1, 2, 30)})
        chunk = max(1, 9000 // max(1, len(keep)))
        rows = []
        for j in range(0, len(dates), chunk):
            ds = dates[j:j + chunk]
            r = run(f'N2 {p} {j // chunk + 1}', f"SELECT date, if(version IN ({ql(keep)}), version, '~other') AS v, sum(count) AS n "
                    f"FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' AND date IN ({ql(ds)}) GROUP BY date, v ORDER BY date, v", None)
            if r is None:
                raise SystemExit(f'N2 {p}: split needed')
            rows += r
        save(os.path.join(DATA, 'firstday', 'counts', p + '.csv'), rows, ['date', 'v', 'n'])


if __name__ == '__main__':
    {'week': stage_week, 'deps': stage_deps, 'pypi': stage_pypi, 'markers': stage_markers, 'firstday': stage_firstday}[sys.argv[1]]()
