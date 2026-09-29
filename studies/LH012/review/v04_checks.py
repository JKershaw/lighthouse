#!/usr/bin/env python3
"""LH012 version 0.4: the check behind the correction of 29 September 2026, late evening.

Found by a replay of the reader-and-inference review in LH016 (studies/LH016/review/replay-X3/,
its problem 2) and first checked there by that session's driving session; this script repeats
the check on LH012's own retained table so the record keeps it. A reading made after the counts.
Offline, standard library only.

Does a new version's share keep rising after day 2? For each of the 355 November to March
releases, delta_points is its at-or-newer share on day 30 minus that on day 2, in points
(data/analysis/firstday_releases.csv, as analyse.py writes it). Counts by release, by project,
and without the three projects that release on most working days.

Usage: python3 studies/LH012/review/v04_checks.py > studies/LH012/review/v04_checks.txt"""
import csv, os, statistics as st
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
rows = list(csv.DictReader(open(os.path.join(STUDY, 'data', 'analysis', 'firstday_releases.csv'))))


def q(v):
    a, b, c = st.quantiles(v, n=4)
    return f'median {b:.2f}, quartiles {a:.2f} and {c:.2f}'


d = [float(r['delta_points']) for r in rows]
print(f'releases {len(d)}; higher on day 30 than on day 2: {sum(x > 0 for x in d)}; lower: {sum(x < 0 for x in d)}')
print(f'day 30 minus day 2, points: {q(d)}; more than +10: {sum(x > 10 for x in d)}; below -10: {sum(x < -10 for x in d)}')
settled = [float(r['delta_points']) for r in rows if r['settled'] == 'True']
print(f'among the releases that settled (|delta| at most ten points): {len(settled)}, higher on day 30 {sum(x > 0 for x in settled)}, {q(settled)}')
rat = [float(r['ratio_s2_s30']) for r in rows if r['ratio_s2_s30'] not in ('', 'nan')]
print(f'the day-2 share as a fraction of the day-30 share, by release: median {st.median(rat):.3f}')
bp = defaultdict(list)
for r in rows:
    bp[r['project']].append(float(r['delta_points']))
m = {p: st.median(v) for p, v in bp.items()}
print(f'by project, the median over its releases: {len(m)} projects, above zero {sum(x > 0 for x in m.values())}, '
      f'median of project medians {st.median(m.values()):.2f}; not above zero: '
      + ', '.join(f'{p} {x:+.2f}' for p, x in m.items() if x <= 0))
print('the three projects that release on most working days: '
      + '; '.join(f'{p} {len(bp[p])} releases, median {m[p]:.2f}' for p in ('boto3', 'botocore', 'litellm')))
rest = [float(r['delta_points']) for r in rows if r['project'] not in ('boto3', 'botocore', 'litellm')]
print(f'without them: {len(rest)} releases, higher on day 30 {sum(x > 0 for x in rest)}, {q(rest)}')
