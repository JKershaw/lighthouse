#!/usr/bin/env python3
"""LH013: LH011's gap rule (as studies/LH012/scripts/analyse.py, is_gap) on W1 and W2, from the daily totals of the
37 projects over 25 September to 14 October 2026 (data/counts/daily_totals.csv). A day is a gap for a project when
the 37's total that day is under half the median of the 37's totals over the seven days centred on it, or when the
project has no row that day but has rows the day before and after. Writes data/analysis/gaps.csv (or under
$LH013_OUT). Usage: python3 gaps.py"""
import csv, os, statistics, datetime as dt
from collections import defaultdict

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
OUT = os.path.join(os.environ.get('LH013_OUT', DATA), 'analysis')
os.makedirs(OUT, exist_ok=True)
tot37, proj = defaultdict(int), defaultdict(dict)
for r in csv.DictReader(open(os.path.join(DATA, 'counts', 'daily_totals.csv'))):
    tot37[r['date']] += int(r['n'])
    proj[r['project']][r['date']] = int(r['n'])
P37 = sorted(proj)
DAYS = [str(dt.date(2026, 9, 28) + dt.timedelta(days=i)) for i in range(14)]


def is_gap(p, d):
    day = dt.date.fromisoformat(d)
    vals = [tot37[x] for x in (str(day + dt.timedelta(days=k)) for k in range(-3, 4)) if x in tot37]
    if d in tot37 and vals and tot37[d] < 0.5 * statistics.median(vals):
        return True
    prev, nxt = str(day - dt.timedelta(days=1)), str(day + dt.timedelta(days=1))
    return d not in proj[p] and prev in proj[p] and nxt in proj[p]


gaps = [dict(project=p, date=d) for p in P37 for d in DAYS if is_gap(p, d)]
with open(os.path.join(OUT, 'gaps.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['project', 'date'], lineterminator='\n')
    w.writeheader()
    w.writerows(gaps)
print('projects', len(P37), '; gap project-days', len(gaps))
