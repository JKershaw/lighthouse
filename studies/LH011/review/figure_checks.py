#!/usr/bin/env python3
"""R-0014: checks of the piece figure's alt text and caption against release_days.csv: the range of
each group's project medians over days 0 to 30, and the CI installer total. Output: figure_checks.txt."""
import csv, os, statistics
from collections import defaultdict
STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(STUDY, 'data', 'analysis')
po = {r['project']: r for r in csv.DictReader(open(os.path.join(A, 'project_outcomes.csv'))) if r['releases'] != '0'}
sh = defaultdict(lambda: defaultdict(list))
for r in csv.DictReader(open(os.path.join(A, 'release_days.csv'))):
    if r['status'] == 'known' and r['share_at_or_newer']:
        sh[r['project']][int(r['day'])].append(float(r['share_at_or_newer']))
med = {p: {d: statistics.median(v) for d, v in sh[p].items()} for p in po}
for g in ('yes', 'no'):
    ps = [p for p in po if po[p]['most_reached'] == g]
    d0 = [(p, round(med[p][0] * 100, 1)) for p in ps]
    lo = min((med[p][d], p, d) for p in ps for d in range(1, 31))
    hi = max((med[p][d], p, d) for p in ps for d in range(1, 31))
    print(f'group {g}: {len(ps)} projects; day-0 medians from {min(x[1] for x in d0)} to {max(x[1] for x in d0)} (highest: {sorted(d0, key=lambda x: -x[1])[:3]})')
    print(f'   over days 1 to 30, lowest project median {lo[0]*100:.1f} ({lo[1]}, day {lo[2]}), highest {hi[0]*100:.1f} ({hi[1]}, day {hi[2]})')
rows = list(csv.DictReader(open(os.path.join(A, 'ci_installers.csv'))))
print('CI installer downloads total', sum(int(r['downloads']) for r in rows), 'flag known share', sum(float(r['share']) for r in rows if r['flag_known'] == 'True'))
