#!/usr/bin/env python3
"""LH011: the frame, read before any per-version download count (brief, "Stopping condition").
F00 to F03 are ClickPy reads of the server's limits, the database's table definitions and the
August 2026 project totals (summed over versions, so no per-version count is read); P01 to P50 are
PyPI JSON reads of each selected project's release files. F00 to F03 were first run inline, in this
order, on 28 September 2026 from 19:53 UTC with these exact texts; this file keeps them.
Writes data/clickpy_server.csv, clickpy_schema.csv, clickpy_columns.csv,
clickpy_top_projects_2026_08.csv, projects.csv and pypi_versions.csv.

Adapted from studies/LH005/scripts/collect_pypi_releases.py and collect_clickpy.py (C01). What
changed: the project list comes from ClickPy's monthly table with the brief's tooling exclusions; the
schema read keeps sorting and primary keys; PyPI release files are reduced to one row per version
(first and last upload, file count, file types, whether any file is yanked) for fifty projects;
the pre-release test uses the `packaging` library's PEP 440 parser.
Usage: python3 collect_frame.py [--skip-clickpy]"""
import sys
from packaging.version import Version, InvalidVersion
from common import clickhouse, get_json, write_csv, read_csv

TOOLING = ['pip', 'setuptools', 'wheel', 'uv', 'virtualenv', 'pipenv', 'pipx', 'poetry', 'poetry-core',
           'pdm', 'pdm-backend', 'hatchling', 'flit-core', 'build', 'setuptools-scm', 'scikit-build-core',
           'maturin']

if '--skip-clickpy' not in sys.argv:
    clickhouse('F00 server and limits', "SELECT version() AS server_version, timezone() AS tz, "
               "getSetting('max_result_rows') AS max_result_rows, getSetting('max_rows_to_read') AS max_rows_to_read, "
               "getSetting('max_bytes_to_read') AS max_bytes_to_read, getSetting('max_execution_time') AS max_execution_time",
               'clickpy_server.csv')
    clickhouse('F01 schema', "SELECT name, engine, total_rows, sorting_key, primary_key, create_table_query "
               "FROM system.tables WHERE database = 'pypi' ORDER BY name", 'clickpy_schema.csv')
    clickhouse('F02 month column', "SELECT name, type FROM system.columns WHERE database='pypi' AND table IN "
               "('pypi_downloads_per_month','pypi_downloads_per_day_by_version','pypi','pypi_downloads_per_day') "
               "ORDER BY table, position", 'clickpy_columns.csv')
    clickhouse('F03 top projects August 2026', "SELECT project, sum(count) AS downloads FROM pypi.pypi_downloads_per_month "
               "WHERE month = '2026-08-01' GROUP BY project ORDER BY downloads DESC, project LIMIT 80",
               'clickpy_top_projects_2026_08.csv')

top = read_csv('clickpy_top_projects_2026_08.csv')
projects, removed = [], []
for rank, r in enumerate(top, 1):
    if r['project'] in TOOLING:
        removed.append(dict(rank=rank, project=r['project'], downloads_2026_08=r['downloads'], status='removed: tooling'))
    elif len(projects) < 50:
        projects.append(dict(rank=rank, project=r['project'], downloads_2026_08=r['downloads'], status='selected'))
write_csv('projects.csv', sorted(projects + removed, key=lambda x: x['rank']))
if '--skip-clickpy' not in sys.argv:
    lst = ','.join("'%s'" % p['project'] for p in projects)
    clickhouse('F04 coverage', f"SELECT project, min(min_date) AS first_day, max(max_date) AS last_day "
               f"FROM pypi.pypi_downloads_max_min WHERE project IN ({lst}) GROUP BY project ORDER BY project",
               'clickpy_coverage.csv')

rows = []
for i, p in enumerate(projects, 1):
    name = p['project']
    status, d = get_json('PyPI JSON API', f'P{i:02d} {name}', f'https://pypi.org/pypi/{name}/json', 'pypi_versions.csv')
    if d is None:
        rows.append(dict(project=name, version='', first_upload_utc='', last_upload_utc='', n_files=0,
                         file_types='', any_yanked='', is_prerelease='', parse='HTTP ' + status))
        continue
    for version, files in d['releases'].items():
        if not files:
            continue
        try:
            v = Version(version)
            pre, parse = (v.is_prerelease or v.is_devrelease), 'ok'
        except InvalidVersion:
            pre, parse = '', 'invalid PEP 440'
        times = sorted(f['upload_time_iso_8601'] for f in files)
        rows.append(dict(project=name, version=version, first_upload_utc=times[0], last_upload_utc=times[-1],
                         n_files=len(files), file_types='|'.join(sorted({f['packagetype'] for f in files})),
                         any_yanked=any(f['yanked'] for f in files), is_prerelease=pre, parse=parse))
rows.sort(key=lambda r: (r['project'], r['first_upload_utc'], r['version']))
write_csv('pypi_versions.csv', rows)
