#!/usr/bin/env python3
"""LH013: readings made after the counts were seen (post hoc), three of them, offline. None is a test.
1. Where the largest cell changed between W1 and W2, how far apart the two largest cells were in each week.
2. pydantic-core's W2 drop in O: the at-or-newer version that took share, and when it and pydantic 2.14.0 were uploaded.
3. The direction of the change in O from W0, with R0 held fixed.
Usage: python3 post_hoc.py > data/post_hoc_reading.txt"""
import csv, os
from collections import defaultdict
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
rd = lambda *p: list(csv.DictReader(open(os.path.join(D, *p))))
holds = rd('analysis', 'holds.csv')
print('1. Largest cell changed between W1 and W2: the two largest cells as a share of all downloads, in points')
for h in holds:
    for base, k in (('C', 'c6'), ('C5', 'c5')):
        if h[base + '_holds'] == 'False':
            out = []
            for w in ('W1', 'W2'):
                r = rd('counts', 'pass', f"{h['project']}_{w}.csv")[0]
                a, b = [int(x) for x in r[k + '_top'].split()[:2]]
                t = int(r['total'])
                out.append(f'{w} {100 * a / t:.2f} and {100 * b / t:.2f} (gap {100 * (a - b) / t:.2f})')
            print(f"   {base} {h['project']}: {h[base + '_cell_W1']} -> {h[base + '_cell_W2']}; " + '; '.join(out))
print()
up = {(r['project'], r['version']): r['first_upload_utc'] for r in rd('versions.csv')}
c = defaultdict(lambda: defaultdict(int))
for r in rd('counts', 'versions', 'pydantic-core.csv'):
    c[r['week']][r['version']] += int(r['n'])
print('2. pydantic-core, share of each week\'s downloads by version (at least 1 per cent), with first upload (UTC)')
for w in ('W1', 'W2'):
    t = sum(c[w].values())
    print(f'   {w}: ' + '; '.join(f'{v} {100 * n / t:.1f} ({up.get(("pydantic-core", v), "unlisted")[:16]})'
                                for v, n in sorted(c[w].items(), key=lambda x: -x[1]) if n / t >= 0.01))
print(f'   pydantic 2.14.0 first uploaded {up[("pydantic", "2.14.0")][:16]}' if ('pydantic', '2.14.0') in up else '')
print()
d1 = [float(h['dO_W1']) for h in holds]
d2 = [float(h['dO_W2']) for h in holds]
print('3. O at fixed R0, change from W0')
print(f'   lower in W1 than W0: {sum(x < 0 for x in d1)} of 37; lower in W2 than W0: {sum(x < 0 for x in d2)}; lower in W2 than W1: '
      f'{sum(float(h["O_W2"]) < float(h["O_W1"]) for h in holds)}; lower in both weeks: {sum(a < 0 and b < 0 for a, b in zip(d1, d2))}')
