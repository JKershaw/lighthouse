#!/usr/bin/env python3
"""R-0122 reader review: does the patched share rise because patched counts rise, or because
branch totals (denominators) shrink? Earliest read per completed day, as record_v1.py.
Usage: python3 -I studies/LH033/review/r0122_composition.py"""
from datetime import date
from pathlib import Path
import gzip, json
DATA = Path(__file__).resolve().parents[1] / 'data'
FIXED = ['8.2', '8.3', '8.4', '8.5']
bh, hist = {}, {}
for p in sorted(x for x in DATA.iterdir() if x.name.startswith('read-') and (x/'censys.raw.gz').exists()):
    s = json.loads(gzip.decompress((p/'censys.raw.gz').read_bytes()))['snapshot']
    rd = date.fromisoformat(p.name[5:15])
    for r in s['branch_history']:
        if r['branch'] in FIXED and date.fromisoformat(r['day']) < rd:
            bh.setdefault((r['branch'], r['day']), (r['patched'], r['targets']))
    for r in s['history']:
        if date.fromisoformat(r['day']) < rd:
            hist.setdefault(r['day'], {}).setdefault(r['status'], r['targets'])
days = sorted({d for _, d in bh})
pick = [0, 1, 2, 7, 14, 23, 28, 29, 30]
for b in FIXED:
    print(f'branch {b}: day, patched, targets, unpatched(targets-patched), share%')
    for i in pick:
        pa, t = bh[(b, days[i])]
        print(f'  {i:2d} {pa:>10,} {t:>10,} {t-pa:>10,} {100*pa/t:5.1f}')
    pa0, t0 = bh[(b, days[7])]; pa1, t1 = bh[(b, days[30])]
    print(f'  day7->30: patched {pa1-pa0:+,}  targets {t1-t0:+,}  unpatched {(t1-pa1)-(t0-pa0):+,}')
    print(f'  share at day 30 if targets had stayed at day-7 level: {100*pa1/t0:.1f}%')
print('history statuses, days 0, 7, 14, 30:')
for i in [0, 7, 14, 30]:
    print(' ', i, hist[days[i]])
print('decomposition of share change: (a) from patched-count change at fixed denominator, (b) remainder from denominator change')
for b in FIXED:
    for i, j in [(7, 14), (14, 30), (23, 30)]:
        p0, t0 = bh[(b, days[i])]; p1, t1 = bh[(b, days[j])]
        tot = 100*(p1/t1 - p0/t0); a = 100*(p1 - p0)/t0
        print(f'  {b} day{i}->{j}: share {tot:+5.2f} pts; patched-count part {a:+5.2f}; denominator part {tot-a:+5.2f}; patched {p1-p0:+,} targets {t1-t0:+,}')
