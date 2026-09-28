#!/usr/bin/env python3
"""R-0014: independent recomputation of LH011's headline figures from the retained frame and count
files (data/releases.csv, data/pypi_versions.csv, data/counts/, data/ci/), without calling
analyse.py. Standard library plus `packaging` for PEP 440. Output: recompute.txt beside it.
Run from anywhere: python3 studies/LH011/review/recompute.py"""
import csv, os, random, statistics, glob
from collections import defaultdict
from packaging.version import Version

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(STUDY, 'data')

rel = list(csv.DictReader(open(os.path.join(D, 'releases.csv'))))
print('releases', len(rel), 'projects', len({r['project'] for r in rel}))
# non-pre-release versions PyPI lists, per project
nonpre = defaultdict(set)
for r in csv.DictReader(open(os.path.join(D, 'pypi_versions.csv'))):
    if r['parse'] == 'ok' and r['is_prerelease'] == 'False':
        nonpre[r['project']].add(r['version'])

counts = {}
for p in {r['project'] for r in rel}:
    by = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(D, 'counts', p + '.csv'))):
        by[r['date']][r['v']] = int(r['downloads'])
    counts[p] = by

import datetime
def dplus(day0, k):
    return (datetime.date.fromisoformat(day0) + datetime.timedelta(days=k)).isoformat()
LAST = '2026-09-27'

share = {}   # (project, version) -> {day: share}
for r in rel:
    p, v = r['project'], r['version']
    vv = Version(v)
    numer = {u for u in nonpre[p] if Version(u) >= vv}
    s = {}
    for k in range(31):
        d = dplus(r['day0'], k)
        if d > LAST:
            break
        row = counts[p].get(d)
        if row is None:
            s[k] = None; continue
        tot = sum(row.values())
        at = sum(c for u, c in row.items() if u in numer)
        s[k] = at / tot if tot else None
    share[(p, v)] = s

reached = {}
for r in rel:
    s = share[(r['project'], r['version'])]
    reached[(r['project'], r['version'])] = (s.get(1) or 0) >= 0.5 or (s.get(2) or 0) >= 0.5
pooled = sum(reached.values())
print('pooled reached half within two days', pooled, 'of', len(rel), f'{pooled/len(rel):.4f}')

byp = defaultdict(list)
for r in rel:
    byp[r['project']].append((r['project'], r['version']))
most = {p: sum(reached[k] for k in ks) * 2 > len(ks) for p, ks in byp.items()}
n_most = sum(most.values())
print('projects where most releases reached half', n_most, 'of', len(most), f'{n_most/len(most):.4f}')
print('all reached:', sum(all(reached[k] for k in ks) for ks in byp.values()),
      'none reached:', sum(not any(reached[k] for k in ks) for ks in byp.values()))

# day-1 medians per project
med1 = {p: statistics.median(share[k][1] for k in ks) for p, ks in byp.items()}
q = statistics.quantiles(list(med1.values()), n=4, method='inclusive')
print('median of project median day-1 shares', f'{statistics.median(med1.values()):.4f}', 'quartiles (inclusive)', [f'{x:.4f}' for x in q])
q2 = statistics.quantiles(list(med1.values()), n=4, method='exclusive')
print('  quartiles (exclusive method)', [f'{x:.4f}' for x in q2])
for p in sorted(med1, key=med1.get):
    if not most[p]:
        print(f'  plateau {p}: median day-1 {med1[p]*100:.2f}, n={len(byp[p])}')

# resample projects, seed per brief
projs = sorted(byp)
rng = random.Random(20260927)
vals = []
for _ in range(10000):
    smp = [rng.choice(projs) for _ in projs]
    vals.append(sum(most[p] for p in smp) / len(smp))
vals.sort()
def pct(a, q):
    # simple percentile: nearest-rank on the sorted list, and also linear interpolation
    i = int(round(q * (len(a) - 1)))
    return a[i]
print('share of projects 95% interval (percentile, my resampler):', f'{pct(vals,0.025):.4f}', f'{pct(vals,0.975):.4f}')

# days to half within 30 and reached by day 30
n30 = 0; days = []
for r in rel:
    s = share[(r['project'], r['version'])]
    first = next((k for k in range(31) if s.get(k) is not None and s[k] >= 0.5), None)
    if first is not None:
        n30 += 1; days.append(first)
print('releases reaching half by day 30 (or last day held)', n30, 'median day', statistics.median(days))
noproj = [p for p, ks in byp.items() if not any(next((k for k in range(31) if share[x].get(k) is not None and share[x][k] >= 0.5), None) is not None for x in ks)]
print('projects with no release reaching half by day 30:', len(noproj), sorted(noproj))

# day-30 medians vs day-1 medians (the piece's 34 of 37)
close = 0; held = 0
for p, ks in byp.items():
    d30 = [share[k][30] for k in ks if share[k].get(30) is not None]
    if d30:
        held += 1
        if abs(statistics.median(d30) - med1[p]) <= 0.10:
            close += 1
    else:
        print('  no day 30 held for', p)
print('projects with day-30 median within 10 points of day-1 median', close, 'of', held)

# CI subsample
ci = {}
cdiff = defaultdict(list); cnew = defaultdict(list); cold = defaultdict(list)
n_below = 0; n_ci = 0
tot_new = [0, 0]; tot_old = [0, 0]
for r in rel:
    if r['ci_subsample'] != 'True':
        continue
    n_ci += 1
    p, v, ov = r['project'], r['version'], r['replaced_version']
    rows = list(csv.DictReader(open(os.path.join(D, 'ci', f'{p}_{v}.csv'))))
    days = {dplus(r['day0'], k) for k in range(3)}
    agg = {v: [0, 0], ov: [0, 0]}
    for x in rows:
        if x['date'] not in days or x['installer'] not in ('pip', 'uv'):
            continue
        if x['version'] not in agg:
            continue
        agg[x['version']][0] += int(x['downloads'])
        if x['ci'] == 'true':
            agg[x['version']][1] += int(x['downloads'])
    sn = agg[v][1] / agg[v][0]; so = agg[ov][1] / agg[ov][0]
    tot_new[0] += agg[v][0]; tot_new[1] += agg[v][1]; tot_old[0] += agg[ov][0]; tot_old[1] += agg[ov][1]
    d = 100 * (sn - so)
    cdiff[p].append(d); cnew[p].append(sn); cold[p].append(so)
    n_below += d < 0
print('CI subsample releases', n_ci, 'new below old', n_below)
pm = {p: statistics.median(x) for p, x in cdiff.items()}
print('CI projects', len(pm), 'projects with median diff below zero', sum(x < 0 for x in pm.values()))
print('median of project median diffs, pp', f'{statistics.median(pm.values()):.4f}')
print('median of project median new CI share', f'{statistics.median(statistics.median(x) for x in cnew.values()):.4f}',
      'old', f'{statistics.median(statistics.median(x) for x in cold.values()):.4f}')
print('pooled new', f'{tot_new[1]/tot_new[0]:.4f}', 'pooled old', f'{tot_old[1]/tot_old[0]:.4f}')
above = [p for p in pm if statistics.median(cnew[p]) > statistics.median(cold[p])]
print('projects whose median new share exceeds median old share (difference of medians):', above)
rng = random.Random(20260927)
vals = []
plist = sorted(pm)
for _ in range(10000):
    smp = [rng.choice(plist) for _ in plist]
    vals.append(statistics.median(pm[p] for p in smp))
vals.sort()
print('CI median of project medians 95% interval (my resampler):', f'{pct(vals,0.025):.4f}', f'{pct(vals,0.975):.4f}')
for p in ('boto3', 'botocore', 'litellm', 'pathspec', 'pydantic-core'):
    print(f'  {p}: median diff {pm[p]:.2f}, median new {statistics.median(cnew[p])*100:.1f}, median old {statistics.median(cold[p])*100:.1f}, diffs {[round(x,2) for x in cdiff[p]]}')

# exact values behind the record's version 0.2 wording
print('day-30 medians of the eleven (4 decimals):', {p: round(statistics.median([share[k][30] for k in ks if share[k].get(30) is not None]) * 100, 4) for p, ks in byp.items() if not most[p]})
print('difference of medians (new minus old, pp) for the daily releasers:', {p: round(100 * (statistics.median(cnew[p]) - statistics.median(cold[p])), 3) for p in ('boto3', 'botocore', 'litellm')})
