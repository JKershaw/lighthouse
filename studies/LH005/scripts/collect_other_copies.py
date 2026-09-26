#!/usr/bin/env python3
"""LH005: reads of the two other public derivatives of PyPI's BigQuery download table.
pypistats.org (PSF-hosted, about 180 days kept, no version breakdown) and pepy.tech's anonymous
/api/v2 path (per-version daily counts for the last three months only). No key is used; the
documented pepy host api.pepy.tech requires one and is only probed for its status.
Usage: python3 collect_other_copies.py   (writes data/pypistats_*.csv, data/pepy_*.csv)"""
from common import get_json, write_csv

# pypistats: the overall series, with and without mirrors, and two segmentations
for pkg in ('mcp', 'lean-lsp-mcp'):
    status, d = get_json('pypistats.org', f'P overall {pkg}', f'https://pypistats.org/api/packages/{pkg}/overall',
                         f'pypistats_{pkg}_overall.csv')
    if d:
        rows = sorted(({'date': r['date'], 'category': r['category'], 'downloads': r['downloads']}
                       for r in d['data']), key=lambda r: (r['date'], r['category']))
        write_csv(f'pypistats_{pkg}_overall.csv', rows)
for seg in ('system', 'python_minor'):
    status, d = get_json('pypistats.org', f'P {seg} mcp', f'https://pypistats.org/api/packages/mcp/{seg}',
                         f'pypistats_mcp_{seg}.csv')
    if d:
        rows = sorted(({'date': r['date'], 'category': r['category'], 'downloads': r['downloads']}
                       for r in d['data']), key=lambda r: (r['date'], r['category']))
        write_csv(f'pypistats_mcp_{seg}.csv', rows)
# pypistats has no version or installer endpoint in its documentation; probe once to record that
for probe in ('version', 'installer'):
    get_json('pypistats.org', f'P probe {probe}', f'https://pypistats.org/api/packages/mcp/{probe}')

# pepy.tech: the anonymous path on the site's own host, then the documented host without a key
for pkg in ('mcp', 'lean-lsp-mcp'):
    status, d = get_json('pepy.tech', f'E v2 {pkg}', f'https://pepy.tech/api/v2/projects/{pkg}',
                         f'pepy_{pkg}_daily_by_version.csv')
    if d:
        rows = [{'date': day, 'version': v, 'downloads': n}
                for day, per in sorted(d['downloads'].items()) for v, n in sorted(per.items())]
        write_csv(f'pepy_{pkg}_daily_by_version.csv', rows)
        write_csv(f'pepy_{pkg}_total.csv', [{'project': pkg, 'total_downloads': d['total_downloads'],
                                            'first_day': min(d['downloads']), 'last_day': max(d['downloads'])}])
get_json('pepy.tech', 'E documented host without key', 'https://api.pepy.tech/api/v2/projects/mcp')
