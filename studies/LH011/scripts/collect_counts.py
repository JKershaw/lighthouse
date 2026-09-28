#!/usr/bin/env python3
"""LH011: every download count, read after amendment 1 was committed (f833a4b). Projects are taken in
SHA-256 order of their names (data/project_order.csv); the brief's ceilings are checked before each
ClickPy query by common.clickhouse.

  G01  daily totals of each of the 50 projects, pypi_downloads_per_day (gap rule and cross-check)
  V..  per project: daily downloads by version from pypi_downloads_per_day_by_version, from seven
       days before its first day 0 to 30 days after its last (or the last day held), with every
       version outside the numerator set folded server-side into '~other'; split by date so that no
       result passes 10,000 rows (amendment 1, reading 6)
  C..  per CI-subsample release: pypi.pypi for the project, days 0 to 2 and the release and the one it
       replaced, by date, version, installer and CI flag
  X..  pypistats.org overall series for the five cross-check projects (amendment 1, reading 5)

Adapted from studies/LH005/scripts/collect_clickpy.py (C04, C05, C07) and collect_other_copies.py.
What changed: fifty projects and 424 releases rather than one; the version set per project is built
from PyPI's JSON by PEP 440 rather than named by hand; results are split by date to stay under the
server's row cap; the per-download read is restricted to two versions and three days per release
rather than a whole window; one CSV per project or release under data/counts/ and data/ci/; pepy.tech
is not read. Usage: python3 collect_counts.py [G|V|C|X ...]   (default: all four, in that order)"""
import datetime, os, sys
from packaging.version import Version
from common import clickhouse, get_json, read_csv, write_csv, DATA

LAST = '2026-09-27'   # last day held for all 50 projects (data/clickpy_coverage.csv)
D = datetime.date.fromisoformat
steps = sys.argv[1:] or ['G', 'V', 'C', 'X']
for sub in ('counts', 'ci'):
    os.makedirs(os.path.join(DATA, sub), exist_ok=True)

order = read_csv('project_order.csv')
releases = read_csv('releases.csv')
versions = read_csv('pypi_versions.csv')
selected = [o['project'] for o in order]
q = lambda xs: ','.join("'%s'" % x for x in xs)

if 'G' in steps:
    # 50 projects x about 192 days passes 10,000 rows, so two date halves
    for lab, a, b in (('G01a', '2026-03-20', '2026-06-22'), ('G01b', '2026-06-23', LAST)):
        clickhouse(f'{lab} daily totals', f"""SELECT project, date, sum(count) AS downloads FROM pypi.pypi_downloads_per_day
            WHERE project IN ({q(selected)}) AND date BETWEEN '{a}' AND '{b}' GROUP BY project, date ORDER BY project, date""",
                   f'daily_totals_{lab[-1]}.csv')


def numerator_set(p, rel):
    lo = min(Version(r['version']) for r in rel)
    return sorted((v for v in versions if v['project'] == p and v['is_prerelease'] == 'False'
                   and Version(v['version']) >= lo), key=lambda v: v['first_upload_utc'])


if 'V' in steps:
    for o in order:
        p = o['project']
        rel = [r for r in releases if r['project'] == p]
        if not rel:
            continue
        out = f'counts/{p}.csv'
        if os.path.exists(os.path.join(DATA, out)):
            continue
        nset = numerator_set(p, rel)
        a = D(min(r['day0'] for r in rel)) - datetime.timedelta(days=7)
        b = min(D(max(r['day0'] for r in rel)) + datetime.timedelta(days=30), D(LAST))
        # split [a, b] into chunks whose estimated rows (days x versions already uploaded, plus '~other') stay under 8,000
        chunks, start, est = [], a, 0
        d = a
        while d <= b:
            n = 1 + sum(1 for v in nset if D(v['first_upload_utc'][:10]) <= d)
            if est + n > 8000:
                chunks.append((start, d - datetime.timedelta(days=1)))
                start, est = d, 0
            est += n
            d += datetime.timedelta(days=1)
        chunks.append((start, b))
        rows = []
        for i, (x, y) in enumerate(chunks):
            r = clickhouse(f'V{o["sha256_order"]:>02} {p} {i + 1}/{len(chunks)}', f"""SELECT date,
                if(version IN ({q(v['version'] for v in nset)}), version, '~other') AS v, sum(count) AS downloads
                FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' AND date BETWEEN '{x}' AND '{y}'
                GROUP BY date, v ORDER BY date, v""")
            if len(r) >= 10000:
                raise SystemExit(f'{p}: result reached the row cap; split further')
            rows += r
        write_csv(out, rows, ['date', 'v', 'downloads'])

if 'C' in steps:
    for o in order:
        p = o['project']
        for r in releases:
            if r['project'] != p or r['ci_subsample'] != 'True':
                continue
            out = f'ci/{p}_{r["version"]}.csv'
            if os.path.exists(os.path.join(DATA, out)):
                continue
            d0 = D(r['day0'])
            clickhouse(f'C{o["sha256_order"]:>02} {p} {r["version"]}', f"""SELECT date, version, installer,
                toString(ci) AS ci, count() AS downloads FROM pypi.pypi WHERE project = '{p}'
                AND date BETWEEN '{d0}' AND '{d0 + datetime.timedelta(days=2)}'
                AND version IN ('{r['version']}', '{r['replaced_version']}')
                GROUP BY date, version, installer, ci ORDER BY date, version, installer, ci""", out)

if 'X' in steps:
    xs = [o['project'] for o in order if int(o['n_releases'])][:5]
    for p in xs:
        status, d = get_json('pypistats.org', f'X overall {p}', f'https://pypistats.org/api/packages/{p}/overall',
                             f'pypistats/{p}_overall.csv')
        os.makedirs(os.path.join(DATA, 'pypistats'), exist_ok=True)
        if d:
            write_csv(f'pypistats/{p}_overall.csv', sorted(d['data'], key=lambda x: (x['category'], x['date'])),
                      ['category', 'date', 'downloads'])
