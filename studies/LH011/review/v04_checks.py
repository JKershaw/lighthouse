#!/usr/bin/env python3
"""LH011 version 0.4: the two checks behind the correction of 29 September 2026, late evening.

Both problems were found by a replay of the reader-and-inference review in LH016
(studies/LH016/review/replay-X2/ and replay-X3/) and first checked there by that session's
driving session; this script repeats the checks on LH011's own retained table, so the record
keeps them. Offline, standard library only. Reads data/analysis/release_days.csv (or
LH011_OUT, as replay.sh sets it). Both are readings made after every count was read.

1. litellm's releases that reached half within 30 days: the day each first did so, and on how
   many of its later days within 30 it was still at half; with litellm's daily total and the
   downloads at 1.83.1 or newer around the day they share.
2. What a month adds after the first days: for each release whose day 30 is held, the
   at-or-newer share on day 30 minus that on day 1 and on day 2, in points; how many rose and
   by how much, by release and by project; and the day-1 share as a fraction of the day-30 share.

Usage: python3 studies/LH011/review/v04_checks.py > studies/LH011/review/v04_checks.txt"""
import csv, os, statistics as st
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
A = os.environ.get('LH011_OUT', os.path.join(STUDY, 'data', 'analysis'))
rows = [r for r in csv.DictReader(open(os.path.join(A, 'release_days.csv')))
        if r['status'] == 'known' and r['share_at_or_newer']]


def q(v):
    a, b, c = st.quantiles(v, n=4)
    return f'median {b:.2f}, quartiles {a:.2f} and {c:.2f}'


print('1. litellm: releases at half of its downloads, at that version or newer, on some day 1 to 30')
lit = defaultdict(dict)
for r in rows:
    if r['project'] == 'litellm':
        lit[r['version']][int(r['day'])] = r
out = []
for v, d in lit.items():
    at = [k for k in sorted(d) if 1 <= k <= 30 and float(d[k]['share_at_or_newer']) >= 0.5]
    if at:
        later = [k for k in sorted(d) if at[0] < k <= 30]
        still = sum(float(d[k]['share_at_or_newer']) >= 0.5 for k in later)
        out.append((d[0]['date'], v, at[0], d[at[0]]['date'], float(d[at[0]]['share_at_or_newer']), still, len(later)))
print('released, version, first day at half, its date, share that day, later days at half of later days read')
for o in sorted(out):
    print(f'{o[0]} {o[1]} day {o[2]} {o[3]} {o[4] * 100:.1f} {o[5]} of {o[6]}')
print(f'{len(out)} of {len(lit)} releases; first dates at half: {sorted(set(o[3] for o in out))}; '
      f'median first day {st.median(o[2] for o in out)}')
print('litellm around that day: date, total downloads, at 1.83.1 or newer, share, older than 1.83.1')
for day in range(25, 31):
    r = lit['1.83.1'].get(day)
    if r:
        t, n = int(r['total']), int(r['at_or_newer'])
        print(f'{r["date"]} {t:,} {n:,} {n / t * 100:.1f} {t - n:,}')

print()
print('2. What a month adds after the first days (at-or-newer share, points)')
rel = defaultdict(dict)
for r in rows:
    rel[(r['project'], r['version'])][int(r['day'])] = float(r['share_at_or_newer'])
for a in (1, 2):
    pairs = {k: (d[30] - d[a]) * 100 for k, d in rel.items() if 30 in d and a in d}
    v = list(pairs.values())
    print(f'day 30 minus day {a}: {len(v)} releases with both days held; higher on day 30 {sum(x > 0 for x in v)}, '
          f'lower {sum(x < 0 for x in v)}; {q(v)}; more than +10 {sum(x > 10 for x in v)}, below -10 {sum(x < -10 for x in v)}')
    bp = defaultdict(list)
    for (p, _), x in pairs.items():
        bp[p].append(x)
    m = [st.median(x) for x in bp.values()]
    print(f'   by project, the median over its releases: {len(m)} projects, above zero {sum(x > 0 for x in m)}, '
          f'median of project medians {st.median(m):.2f}')
    rest = [x for (p, _), x in pairs.items() if p not in ('boto3', 'botocore', 'litellm')]
    print(f'   without boto3, botocore and litellm: {len(rest)} releases, higher {sum(x > 0 for x in rest)}, median {st.median(rest):.2f}')
    rat = [d[a] / d[30] for d in rel.values() if 30 in d and a in d and d[30] > 0]
    print(f'   the day-{a} share as a fraction of the day-30 share: median {st.median(rat):.3f}')
days = defaultdict(lambda: defaultdict(list))
for (p, _), d in rel.items():
    for k, s in d.items():
        days[p][k].append(s)
diff = {p: (st.median(days[p][30]) - st.median(days[p][1])) * 100 for p in days if days[p].get(30)}
print(f'the chart\'s reading, each project\'s median share on day 30 minus its median on day 1: {len(diff)} projects, '
      f'above zero {sum(x > 0 for x in diff.values())}, median {st.median(diff.values()):.2f}; below zero: '
      + ', '.join(f'{p} {x:+.1f}' for p, x in sorted(diff.items(), key=lambda t: t[1]) if x < 0))
