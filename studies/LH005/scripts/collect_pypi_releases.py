#!/usr/bin/env python3
"""LH005: release upload times for mcp and lean-lsp-mcp from PyPI's own JSON API, because ClickPy's
copy of the metadata table (pypi.projects) holds no row for the current mcp project (see LH005.md).
Usage: python3 collect_pypi_releases.py   (writes data/pypi_release_files.csv)"""
from common import get_json, write_csv

rows = []
for pkg in ('mcp', 'lean-lsp-mcp'):
    status, d = get_json('PyPI JSON API', f'R {pkg}', f'https://pypi.org/pypi/{pkg}/json', 'pypi_release_files.csv')
    for version, files in d['releases'].items():
        for f in files:
            rows.append({'project': pkg, 'version': version, 'filename': f['filename'],
                         'packagetype': f['packagetype'], 'upload_time_utc': f['upload_time_iso_8601'],
                         'yanked': f['yanked']})
rows.sort(key=lambda r: (r['project'], r['upload_time_utc'], r['filename']))
write_csv('pypi_release_files.csv', rows)
