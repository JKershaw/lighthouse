#!/usr/bin/env python3
"""LH013: the brief's check of the baseline. Compares W0's daily totals read again on 2 November 2026 from
pypi_downloads_per_day_by_version (data/counts/w0_daily_totals.csv) with LH012's retained totals (its
data/analysis/week.csv and the daily sums of its data/week/versions/). A project whose W0 total differs by more than
2 per cent has its W0 comparisons reported as unknown. Writes data/analysis/w0_check.csv (or under $LH013_OUT).
This is the code run inline at 15:35 UTC, kept as a script. Usage: python3 w0check.py"""
import csv, os
from collections import defaultdict
STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(os.path.dirname(STUDY), 'LH012', 'data')
OUT = os.path.join(os.environ.get('LH013_OUT', os.path.join(STUDY, 'data')), 'analysis')
os.makedirs(OUT, exist_ok=True)
now = defaultdict(int); nd = {}
for r in csv.DictReader(open(os.path.join(STUDY, 'data', 'counts', 'w0_daily_totals.csv'))):
    now[r['project']] += int(r['n']); nd[(r['project'], r['date'])] = int(r['n'])
old = {r['project']: int(r['total']) for r in csv.DictReader(open(f'{L}/analysis/week.csv'))}
od = defaultdict(int)
for p in old:
    for r in csv.DictReader(open(f'{L}/week/versions/{p}.csv')):
        od[(p, r['date'])] += int(r['n'])
rows = []
for p in sorted(old):
    diff = (now[p] - old[p]) / old[p]
    maxd = max(abs(nd.get(k, 0) - v) / v for k, v in od.items() if k[0] == p)
    rows.append(dict(project=p, lh012_total=old[p], total_now=now[p], difference=f'{diff:.6f}', largest_daily_difference=f'{maxd:.6f}',
                     confirmed=str(abs(diff) <= 0.02)))
w = csv.DictWriter(open(os.path.join(OUT, 'w0_check.csv'), 'w', newline=''), fieldnames=list(rows[0]), lineterminator='\n')
w.writeheader(); w.writerows(rows)
print(sum(r['confirmed'] == 'True' for r in rows), 'of 37 confirmed')
