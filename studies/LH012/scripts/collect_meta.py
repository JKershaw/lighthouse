#!/usr/bin/env python3
"""LH012 phase 1: the reads that touch no outcome, made before the brief is fixed.
M00 to M04 are ClickPy reads of the server's version and limits, the `pypi` database's table
definitions and column types, and the first and last day held; the phase gate in common.py refuses
anything that could return a download count. P001 to P500 are PyPI JSON reads of the projects in
LH010's top 500 (data retained there, ClickPy's August 2026 totals, read 27 September 2026); V reads
are PyPI JSON reads of single versions of dependents (the versions that were newest during the read
week). Writes data/clickpy_server.csv, clickpy_schema.csv, clickpy_columns.csv, clickpy_coverage.csv,
clickpy_last_day_by_table.csv, versions.csv, files.csv.gz, top500_screen.csv, requirements.csv and
dependent_versions.csv.

Adapted from studies/LH011/scripts/collect_frame.py. What changed: no monthly totals are read (the
top 500 is LH010's, reused); the schema read drops total_rows and covers every per-day table; the
coverage read covers the per-day tables as well as pypi_downloads_max_min; PyPI's JSON is kept per
file (Requires-Python, name, type, tags, yanked, upload time) and per version for the 37 projects,
and each top-500 project's declared requirements are parsed with the `packaging` library.
Usage: python3 collect_meta.py clickpy | pypi | week"""
import csv, gzip, json, os, sys
from packaging.version import Version, InvalidVersion
from packaging.requirements import Requirement, InvalidRequirement
from packaging.utils import canonicalize_name, parse_wheel_filename, InvalidWheelFilename
from common import clickhouse, get_json, write_csv, read_csv, DATA, SCRATCH

ROOT = os.path.dirname(os.path.dirname(DATA))
P37 = sorted({r['project'] for r in csv.DictReader(open(os.path.join(ROOT, 'LH011', 'data', 'releases.csv')))})
TOP500 = list(csv.DictReader(open(os.path.join(ROOT, 'LH010', 'data', 'top500.csv'))))
RAW = os.path.join(SCRATCH, 'pypi_json')
TABLES = ['pypi', 'pypi_downloads_per_day', 'pypi_downloads_per_day_by_version',
          'pypi_downloads_per_day_by_version_by_python', 'pypi_downloads_per_day_by_version_by_system',
          'pypi_downloads_per_day_by_version_by_installer_by_type', 'pypi_downloads_per_day_by_version_by_file_type',
          'pypi_downloads_per_day_by_version_by_country', 'pypi_downloads_per_day_by_installer',
          'pypi_downloads_max_min', 'pypi_raw']
# The read week, fixed in the brief after M03 and M04 were read: the last full Monday to Sunday
# held for all 37 projects in every per-day table.
WEEK = ('2026-09-21', '2026-09-27')


def q(names):
    return ','.join("'%s'" % n for n in names)


def stage_clickpy():
    clickhouse('M00 server and limits', "SELECT version() AS server_version, timezone() AS tz, "
               "getSetting('max_result_rows') AS max_result_rows, getSetting('max_rows_to_read') AS max_rows_to_read, "
               "getSetting('max_bytes_to_read') AS max_bytes_to_read, getSetting('max_execution_time') AS max_execution_time, "
               "getSetting('result_overflow_mode') AS result_overflow_mode, getSetting('read_overflow_mode') AS read_overflow_mode",
               'clickpy_server.csv')
    clickhouse('M01 schema', "SELECT name, engine, sorting_key, primary_key, partition_key, create_table_query "
               "FROM system.tables WHERE database = 'pypi' ORDER BY name", 'clickpy_schema.csv')
    clickhouse('M02 columns', "SELECT table, position, name, type, default_kind, default_expression, comment, "
               f"is_in_sorting_key, is_in_primary_key FROM system.columns WHERE database = 'pypi' AND table IN ({q(TABLES)}) "
               "ORDER BY table, position", 'clickpy_columns.csv')
    names = sorted(set(P37) | {r['project'] for r in TOP500})
    clickhouse('M03 coverage (first and last day held, top 500)', "SELECT project, min(min_date) AS first_day, "
               f"max(max_date) AS last_day FROM pypi.pypi_downloads_max_min WHERE project IN ({q(names)}) "
               "GROUP BY project ORDER BY project", 'clickpy_coverage.csv')
    out = []
    for i, t in enumerate(TABLES[1:6], 1):
        rows = clickhouse(f'M04.{i} last day held in {t}', f"SELECT project, min(date) AS first_day, max(date) AS last_day "
                          f"FROM pypi.{t} WHERE project IN ({q(P37)}) AND date >= '2025-09-01' GROUP BY project ORDER BY project")
        out += [dict(table=t, **r) for r in rows]
    write_csv('clickpy_last_day_by_table.csv', out)


def pre(v):
    try:
        x = Version(v)
        return x.is_prerelease or x.is_devrelease, 'ok'
    except InvalidVersion:
        return '', 'invalid'


def platform_family(tag):
    for fam in ('manylinux', 'musllinux', 'macosx', 'win', 'linux', 'any', 'ios', 'android', 'emscripten', 'pyodide'):
        if tag.startswith(fam):
            return fam
    return 'other'


def stage_pypi():
    os.makedirs(RAW, exist_ok=True)
    screen, reqs, vrows, frows, dvers = [], [], [], [], []
    for i, r in enumerate(TOP500, 1):
        name = r['project']
        path = os.path.join(RAW, name + '.json')
        if os.path.exists(path):
            d, status = json.load(open(path)), '200 (scratch copy of this session\'s read)'
        else:
            status, d = get_json('PyPI JSON API', f'P{i:03d} {name}', f'https://pypi.org/pypi/{name}/json',
                                 'versions.csv' if name in P37 else 'top500_screen.csv')
            if d is not None:
                json.dump(d, open(path, 'w'))
        if d is None:
            screen.append(dict(rank=r['rank'], project=name, latest_version='', latest_requires_python='',
                               n_requirements='', names_one_of_37='', status='HTTP ' + status))
            continue
        info = d['info']
        rd = info.get('requires_dist') or []
        hits = parse_reqs(name, info['version'], 'latest at read', rd, reqs)
        screen.append(dict(rank=r['rank'], project=name, latest_version=info['version'],
                           latest_requires_python=info.get('requires_python') or '', n_requirements=len(rd),
                           names_one_of_37=' '.join(sorted(hits)), status='200'))
        for v, files in d['releases'].items():
            ups = sorted(f['upload_time_iso_8601'] for f in files)
            is_pre, parse = pre(v)
            base = dict(project=name, version=v, first_upload_utc=ups[0] if ups else '',
                        is_prerelease=is_pre, parse=parse, n_files=len(files),
                        all_yanked=bool(files) and all(f.get('yanked') for f in files))
            if name in P37:
                rp = sorted({(f.get('requires_python') or '') for f in files})
                py, abi, plat = set(), set(), set()
                for f in files:
                    frows.append(dict(project=name, version=v, filename=f['filename'], packagetype=f['packagetype'],
                                      python_version=f.get('python_version') or '', requires_python=f.get('requires_python') or '',
                                      yanked=bool(f.get('yanked')), upload_time_utc=f['upload_time_iso_8601'], size=f.get('size', '')))
                    if f['packagetype'] == 'bdist_wheel':
                        try:
                            _, _, _, tags = parse_wheel_filename(f['filename'])
                            for t in tags:
                                py.add(t.interpreter); abi.add(t.abi); plat.add(platform_family(t.platform))
                        except InvalidWheelFilename:
                            py.add('unparsed')
                vrows.append(dict(base, last_upload_utc=ups[-1] if ups else '',
                                  any_yanked=any(f.get('yanked') for f in files),
                                  requires_python=' | '.join(rp),
                                  has_sdist=any(f['packagetype'] == 'sdist' for f in files),
                                  n_wheels=sum(f['packagetype'] == 'bdist_wheel' for f in files),
                                  wheel_interpreters=' '.join(sorted(py)), wheel_abis=' '.join(sorted(abi)),
                                  wheel_platforms=' '.join(sorted(plat))))
            if hits or name in P37:
                dvers.append(base)
    write_csv('top500_screen.csv', screen)
    write_csv('requirements.csv', reqs)
    write_csv('versions.csv', vrows)
    write_csv('dependent_versions.csv', dvers)
    with gzip.open(os.path.join(DATA, 'files.csv.gz'), 'wt', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(frows[0].keys()), lineterminator='\n')
        w.writeheader()
        w.writerows(frows)


def parse_reqs(dependent, version, which, rd, out):
    hits = set()
    for s in rd:
        try:
            req = Requirement(s)
        except InvalidRequirement:
            out.append(dict(dependent=dependent, dependent_version=version, which=which, requirement=s,
                            name='', specifier='', marker='', extra_only='', one_of_37='', parse='invalid'))
            continue
        n = canonicalize_name(req.name)
        m = str(req.marker) if req.marker else ''
        if n in P37:
            hits.add(n)
            out.append(dict(dependent=dependent, dependent_version=version, which=which, requirement=s, name=n,
                            specifier=str(req.specifier), marker=m, extra_only='extra ==' in m, one_of_37=True, parse='ok'))
    return hits


def newest_during_week(versions):
    """Every non-pre-release version, not wholly yanked now, that was the highest by PEP 440 at some
    moment of the read week: the highest uploaded before the week, and each one uploaded during it
    that was higher than every version uploaded before it."""
    start, end = WEEK[0] + 'T00:00:00', WEEK[1] + 'T23:59:59.999999'
    ok = [(Version(v['version']), v['first_upload_utc'], v['version']) for v in versions
          if v['parse'] == 'ok' and v['is_prerelease'] in ('False', False) and v['all_yanked'] in ('False', False)
          and v['first_upload_utc']]
    before = [x for x in ok if x[1] < start]
    cur = max(before)[0] if before else None
    out = [str(max(before)[2])] if before else []
    for x in sorted((x for x in ok if start <= x[1] <= end), key=lambda x: x[1]):
        if cur is None or x[0] > cur:
            cur = x[0]
            out.append(x[2])
    return out


def stage_week():
    """V reads: each dependent version that was newest during the read week and is not the latest
    at read (whose requirements the project JSON already gave)."""
    screen = {r['project']: r for r in read_csv('top500_screen.csv')}
    reqs = read_csv('requirements.csv')
    dv = {}
    for v in read_csv('dependent_versions.csv'):
        dv.setdefault(v['project'], []).append(v)
    deps = sorted({r['dependent'] for r in reqs if r['one_of_37'] == 'True'} | set(P37))
    rows, i = [], 0
    for dep in deps:
        wk = newest_during_week(dv.get(dep, []))
        for v in wk:
            rows.append(dict(dependent=dep, version=v, latest_at_read=v == screen[dep]['latest_version']))
            if v == screen[dep]['latest_version']:
                continue
            i += 1
            status, d = get_json('PyPI JSON API', f'V{i:03d} {dep} {v}', f'https://pypi.org/pypi/{dep}/{v}/json', 'requirements.csv')
            if d is None:
                reqs.append(dict(dependent=dep, dependent_version=v, which='newest during the read week', requirement='',
                                 name='', specifier='', marker='', extra_only='', one_of_37='', parse='HTTP ' + status))
                continue
            parse_reqs(dep, v, 'newest during the read week', d['info'].get('requires_dist') or [], reqs)
    write_csv('requirements.csv', reqs)
    write_csv('week_versions.csv', rows)


if __name__ == '__main__':
    {'clickpy': stage_clickpy, 'pypi': stage_pypi, 'week': stage_week}[sys.argv[1]]()
