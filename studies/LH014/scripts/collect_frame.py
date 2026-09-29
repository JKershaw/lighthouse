#!/usr/bin/env python3
"""LH014 phase 2: the frame, read after the brief's snapshot (commit 353f17f) and before any daily,
per-version, installer or CI count, with LH014_PHASE=2: common.py's gate refuses every query that
counts except the August monthly sums, and every query that could read a day after 2026-09-27.

  R01  the ranking: pypi_downloads_per_month, month 2026-08-01, summed per project, ordered by the sum
       descending and the name ascending, first 5,100 rows (data/clickpy_month_2026_08.csv); then
       frame.py --list writes data/frame.csv and frame_checks.csv
  P..  PyPI JSON, walking each band's draw order until 80 projects are served (data/pypi_walk.csv,
       one row per project walked; data/pypi_versions.csv, one row per version of each served project).
       Not served: 404 or 410 on two reads at least a minute apart; any other failure is retried up to
       three times and then recorded as not read (brief, Population and unit, Draw)
  I01  the installer table's distinct installer names for the drawn projects, 25 March to 27 September
       2026, without counts (data/installer_names.csv)
  K01..K03  coverage: first and last day held from 25 March to 27 September 2026 per drawn project in
       pypi_downloads_per_day, pypi_downloads_per_day_by_version and the installer table
       (data/coverage.csv). pypi.pypi is not read here: any read of it scans one row per download, so
       its rows-read statistic would itself be a download count (amendment 1)

Adapted from studies/LH011/scripts/collect_frame.py. What changed: the list is 5,100 rows and is turned
into bands and a salted-hash draw by frame.py; PyPI's JSON is read in the draw's order until 80
projects per band are served, with the brief's not-served rule, and no field of it that describes
downloads is kept; the installer names and the coverage reads are new, and are split into chunks of
projects, halved on failure, so that no query passes the `demo` user's limits. The PyPI reduction to
one row per version adds whether every file is yanked (LH012's column) to LH011's columns.
Usage: LH014_PHASE=2 python3 collect_frame.py [R] [P] [I] [K]   (default: all four, in that order)"""
import os, sys, time
from packaging.version import Version, InvalidVersion
import common
from common import clickhouse, get_json, write_csv, read_csv
import frame

if common.PHASE != '2':
    raise SystemExit('collect_frame.py reads the frame only: run it with LH014_PHASE=2')
steps = sys.argv[1:] or ['R', 'P', 'I', 'K']
q = lambda xs: ','.join("'%s'" % x for x in xs)
WINDOW = "date BETWEEN '2026-03-25' AND '2026-09-27'"


def chunked(label, projects, make_sql, size):
    """Run make_sql over chunks of projects; a chunk that fails a limit is halved and run again."""
    rows, part, stack = [], 0, [projects[k:k + size] for k in range(0, len(projects), size)]
    while stack:
        chunk = stack.pop(0)
        part += 1
        try:
            rows += clickhouse(f'{label} part {part} ({len(chunk)} projects)', make_sql(chunk))
        except SystemExit as e:
            if len(chunk) == 1:
                raise
            print(f'{label} part {part} failed ({str(e)[:120]}); halving')
            h = len(chunk) // 2
            stack[0:0] = [chunk[:h], chunk[h:]]
    return rows


def read_project(band, i, p):
    """(result, statuses, json) for one project, by the brief's not-served rule."""
    url, statuses, first_missing, failures = f'https://pypi.org/pypi/{p}/json', [], None, 0
    while True:
        t = time.time()
        try:
            status, d = get_json('PyPI JSON API', f'P{band}{i:03d} {p}', url, 'pypi_versions.csv')
        except ValueError:          # a 200 whose body is not JSON
            status, d = '200 (not JSON)', None
        statuses.append(status)
        if status == '200' and d is not None and isinstance(d.get('releases'), dict):
            return 'served', statuses, d
        if status in ('404', '410'):
            if first_missing is not None and t - first_missing >= 60:
                return 'not served', statuses, None
            if first_missing is None:
                first_missing = t
            time.sleep(61)
            continue
        failures += 1
        if failures > 3:
            return 'not read', statuses, None
        time.sleep(5)


if 'R' in steps:
    clickhouse('R01 ranking August 2026', "SELECT project, sum(count) AS downloads FROM pypi.pypi_downloads_per_month "
               "WHERE month = '2026-08-01' GROUP BY project ORDER BY downloads DESC, project ASC LIMIT 5100",
               'clickpy_month_2026_08.csv')
    frame.main_list()

if 'P' in steps:
    orders = frame.band_orders(read_csv('frame.csv'))
    walk, versions = [], []
    for band in ('A', 'B'):
        served = 0
        for i, p in enumerate(orders[band], 1):
            if served >= frame.PER_BAND:
                break
            result, statuses, d = read_project(band, i, p)
            info_name = (d.get('info') or {}).get('name', '') if d else ''
            walk.append(dict(band=band, walk_order=i, project=p, sha256=frame.draw_key(p), result=result,
                             http_statuses='|'.join(statuses), info_name=info_name))
            if result != 'served':
                continue
            served += 1
            for version, files in d['releases'].items():
                if not files:
                    continue
                try:
                    v = Version(version)
                    pre, parse = (v.is_prerelease or v.is_devrelease), 'ok'
                except InvalidVersion:
                    pre, parse = '', 'invalid PEP 440'
                times = sorted(f['upload_time_iso_8601'] for f in files)
                versions.append(dict(project=p, version=version, first_upload_utc=times[0], last_upload_utc=times[-1],
                                     n_files=len(files), file_types='|'.join(sorted({f['packagetype'] for f in files})),
                                     any_yanked=any(f.get('yanked') for f in files), all_yanked=all(f.get('yanked') for f in files),
                                     is_prerelease=pre, parse=parse))
        print(f'band {band}: walked {sum(1 for w in walk if w["band"] == band)}, served {served}, '
              f'not served {sum(1 for w in walk if w["band"] == band and w["result"] == "not served")}, '
              f'not read {sum(1 for w in walk if w["band"] == band and w["result"] == "not read")}')
    versions.sort(key=lambda r: (r['project'], r['first_upload_utc'], r['version']))
    write_csv('pypi_walk.csv', walk, ['band', 'walk_order', 'project', 'sha256', 'result', 'http_statuses', 'info_name'])
    write_csv('pypi_versions.csv', versions, ['project', 'version', 'first_upload_utc', 'last_upload_utc', 'n_files',
                                              'file_types', 'any_yanked', 'all_yanked', 'is_prerelease', 'parse'])

if 'I' in steps or 'K' in steps:
    names = [d['project'] for d in read_csv('drawn.csv')]

if 'I' in steps:
    rows = chunked('I01 installer names', names, lambda c: "SELECT DISTINCT installer FROM "
                   f"pypi.pypi_downloads_per_day_by_version_by_installer_by_type WHERE project IN ({q(c)}) AND {WINDOW} "
                   "ORDER BY installer", 20)
    inst = sorted({r['installer'] for r in rows})
    write_csv('installer_names.csv', [dict(installer=x) for x in inst], ['installer'])
    print(len(inst), 'installer names:', inst)

if 'K' in steps:
    cov = []
    for lab, table, size in (('K01', 'pypi_downloads_per_day', 80), ('K02', 'pypi_downloads_per_day_by_version', 40),
                             ('K03', 'pypi_downloads_per_day_by_version_by_installer_by_type', 20)):
        rows = chunked(f'{lab} coverage {table}', names, lambda c: f"SELECT project, min(date) AS first_day, max(date) AS last_day "
                       f"FROM pypi.{table} WHERE project IN ({q(c)}) AND {WINDOW} GROUP BY project ORDER BY project", size)
        got = {r['project']: r for r in rows}
        for p in names:
            g = got.get(p, {})
            cov.append(dict(table=table, project=p, first_day=g.get('first_day', ''), last_day=g.get('last_day', '')))
    write_csv('coverage.csv', cov, ['table', 'project', 'first_day', 'last_day'])
    for table in sorted({c['table'] for c in cov}):
        cs = [c for c in cov if c['table'] == table]
        print(f'{table}: projects {len(cs)}; last day 2026-09-27 for {sum(1 for c in cs if c["last_day"] == "2026-09-27")}; '
              f'no row {sum(1 for c in cs if not c["last_day"])}; first day after 2026-03-25 for '
              f'{sum(1 for c in cs if c["first_day"] and c["first_day"] > "2026-03-25")}')
