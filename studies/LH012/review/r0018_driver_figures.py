#!/usr/bin/env python3
"""The figures the driving session used in the prose of the piece's version 1.1 and the record's version 0.3 when
resolving the reader-and-inference review (notes/R-0018.md), from the retained files, offline. Nothing here is new
analysis: it reads data/week/python/, data/versions.csv, data/analysis/firstday_releases.csv and bounds.csv.
Output: review/r0018_driver_figures.txt."""
import csv, os, statistics
from collections import defaultdict
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
out = []


def profile(project, minor):
    d = defaultdict(int)
    for r in csv.DictReader(open(os.path.join(DATA, 'week', 'python', project + '.csv'))):
        if r['python_minor'] == minor:
            d[r['version']] += int(r['n'])
    return d


# 1. boto3 on Python 3.9 below its edge 1.42.97
d = profile('boto3', '3.9')
vs = sorted(d, key=Version, reverse=True)
below = [v for v in vs if Version(v) < Version('1.42.97')]
first50 = [(v, d[v]) for v in below[:50]]
inside = [x for x in first50 if 882_000 <= x[1] <= 906_000]
out.append(f"1. boto3, Python 3.9, 21 to 27 September 2026: 1.42.97 (the edge) {d['1.42.97']:,}; of the 50 versions below it, "
           f"{len(inside)} between 882,000 and 906,000 (range {min(n for _, n in inside):,} to {max(n for _, n in inside):,}); outside: "
           + ', '.join(f'{v} {n:,}' for v, n in first50 if not 882_000 <= n <= 906_000)
           + f"; median of the first 100 below the edge {statistics.median(d[v] for v in below[:100]):,.0f}")
# 2. aiobotocore on Python 3.9: the ten versions below its edge 3.5.0
a = profile('aiobotocore', '3.9')
av = [v for v in sorted(a, key=Version, reverse=True) if Version(v) < Version('3.5.0')][:10]
out.append(f"2. aiobotocore, Python 3.9: 3.5.0 (the edge) {a['3.5.0']:,}; the nine versions below it, {av[0]} to {av[8]}: "
           f"{min(a[v] for v in av[:9]):,} to {max(a[v] for v in av[:9]):,}; the tenth, {av[9]}: {a[av[9]]:,}")
# 3. grpcio-status on Python 3.9: the yanked version inside the plateau
g = profile('grpcio-status', '3.9')
yanked = {r['version'] for r in csv.DictReader(open(os.path.join(DATA, 'versions.csv')))
          if r['project'] == 'grpcio-status' and r['all_yanked'] == 'True'}
gv = [v for v in sorted(g, key=Version, reverse=True) if not Version(v).is_prerelease]
i = gv.index('1.80.0')
out.append('3. grpcio-status, Python 3.9, from its edge 1.80.0 down: '
           + ', '.join(f"{v} {g[v]:,}{' (yanked)' if v in yanked else ''}" for v in gv[i:i + 6])
           + f"; yanked versions of the project: {', '.join(sorted(yanked, key=Version))}")
# 4. the brief's secondary first-day descriptor for boto3 and aiobotocore
rel = defaultdict(list)
for r in csv.DictReader(open(os.path.join(DATA, 'analysis', 'firstday_releases.csv'))):
    if r['ratio_s2_s30'] and r['s2'] and r['s30']:
        rel[r['project']].append((float(r['s2']), float(r['s30']), float(r['ratio_s2_s30'])))
for p in ('boto3', 'aiobotocore'):
    x = rel[p]
    out.append(f"4. {p}: {len(x)} releases; median day-2 share {100 * statistics.median(a for a, _, _ in x):.1f}, "
               f"median day-30 share {100 * statistics.median(b for _, b, _ in x):.1f}, median ratio {statistics.median(c for _, _, c in x):.2f}")
meds = sorted((statistics.median(c for _, _, c in x), p) for p, x in rel.items())
out.append('   median over projects of the median ratio: %.2f; projects under 0.75: %s'
           % (statistics.median(m for m, _ in meds), ', '.join(f'{p} {m:.2f}' for m, p in meds if m < 0.75)))
# 5. holds by the dependent's current versions (bounds.csv)
for r in csv.DictReader(open(os.path.join(DATA, 'analysis', 'bounds.csv'))):
    if r['class'] == 'accounts for most':
        out.append(f"5. {r['project']}: held by current versions of the largest dependent {100 * float(r['largest_held_by_current_versions']):.1f} per cent; "
                   f"by all dependents' current versions {100 * float(r['sum_held_by_current_versions']):.1f}; by their older versions {100 * float(r['sum_held_by_older_versions']):.1f}")
open(os.path.join(HERE, 'r0018_driver_figures.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
