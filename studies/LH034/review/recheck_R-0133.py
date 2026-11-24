#!/usr/bin/env python3
"""R-0133 recheck of LH034 v1.1 (fresh agent, 24 November 2026). Post hoc, descriptive.
Written independently of resolution_R-0131.py and R-0131_counts.py: reads each day file (earliest read
holding it) and the 5 November list, classes keys per line as at/above the fix (amended rule: listed
plain key >= fix, or unlisted plain key > fix) or below it (listed < fix), and reproduces the late-rise
split (one-sided, as in v1.1, and a symmetric average of the two orders), the fall in below-fix downloads
from days 5-7 to 28-30, and the ranges v1.1's Findings quote. Standard library only.
Usage: python3 -I studies/LH034/review/recheck_R-0133.py > studies/LH034/review/recheck_R-0133.txt"""
import gzip, json, re
from datetime import date, timedelta
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data'
L = json.loads((DATA / 'read-2026-11-05T1414Z' / 'dist-index.derived.json').read_text())['extracted']
vi = L['fields'].index('version'); LISTED = {r[vi] for r in L['releases']}
DAY = {}
for rd in sorted(DATA.glob('read-*')):          # read dirs sort by time, so first seen = earliest read
    for f in sorted(rd.glob('day-*.raw.gz')):
        s = f.name[4:12]; d = date(int(s[:4]), int(s[4:6]), int(s[6:8]))
        if d not in DAY: DAY[d] = json.loads(gzip.decompress(f.read_bytes()))['version']
D0 = date(2026, 10, 21)
FIX = {22: (22, 23, 4), 24: (24, 22, 1), 26: (26, 12, 1)}
PLAIN = re.compile(r'v(\d+)\.(\d+)\.(\d+)$')
def cls(n):
    vt = DAY[D0 + timedelta(days=n)]; out = {}
    att = sum(c for k, c in vt.items() if k != 'unknown')
    for ln, fx in FIX.items():
        A = B = W = 0   # W = listed at/above only (rule as written numerator)
        for k, c in vt.items():
            m = PLAIN.match(k)
            if not m or int(m.group(1)) != ln: continue
            v = tuple(int(x) for x in m.groups())
            if k in LISTED:
                if v >= fx: A += c; W += c
                else: B += c
            elif v > fx: A += c
        out[ln] = (A, B, W)
    return out, att
C = {n: cls(n) for n in range(0, 31)}
def mean(ns, ln, i): return sum(C[n][0][ln][i] for n in ns) / len(ns)
def split(w1, w2, title):
    print(f'\n## {title}')
    for ln in FIX:
        A1, B1, A2, B2 = mean(w1, ln, 0), mean(w1, ln, 1), mean(w2, ln, 0), mean(w2, ln, 1)
        s = lambda a, b: a / (a + b)
        tot = s(A2, B2) - s(A1, B1)
        a1 = s(A2, B1) - s(A1, B1); b1 = s(A1, B2) - s(A1, B1)          # one-sided, earlier other side
        a2 = s(A2, B2) - s(A1, B2); b2 = s(A2, B2) - s(A2, B1)          # one-sided, later other side
        print(f'L{ln}: A {A1:,.0f}->{A2:,.0f} ({100*(A2/A1-1):+.1f}%), B {B1:,.0f}->{B2:,.0f} ({100*(B2/B1-1):+.1f}%), '
              f'share {100*s(A1,B1):.2f}->{100*s(A2,B2):.2f} ({100*tot:+.2f} pts); '
              f'from A {100*a1:+.2f}, from B {100*b1:+.2f} (other side held early); '
              f'symmetric A {100*(a1+a2)/2:+.2f}, B {100*(b1+b2)/2:+.2f}; A part of rise {100*(a1+a2)/2/tot:.0f}%')
print('# R-0133 recheck, post hoc and descriptive; amended rule')
split(range(13, 21), range(21, 31), 'Days 13-20 vs 21-30')
split([16, 19, 20], [28, 29, 30], 'Weekdays 16,19,20 vs 28,29,30')
split([5, 6, 7], [28, 29, 30], 'Days 5-7 vs 28-30')
print('\n## Below-fix ranges')
wd = lambda n: (D0 + timedelta(days=n)).weekday() < 5
for ln in FIX:
    b = lambda ns: (min(C[n][0][ln][1] for n in ns), max(C[n][0][ln][1] for n in ns))
    print(f'L{ln}: days 5-7 {b([5,6,7])}; weekdays 12-30 {b([n for n in range(12,31) if wd(n)])}; all days 12-30 {b(range(12,31))}; '
          f'weekdays 8-11 {b([n for n in range(8,12) if wd(n)])}')
    print(f'      below / attributed, days 13-20: {min(100*C[n][0][ln][1]/C[n][1] for n in range(13,21)):.2f}-{max(100*C[n][0][ln][1]/C[n][1] for n in range(13,21)):.2f}; '
          f'days 21-30: {min(100*C[n][0][ln][1]/C[n][1] for n in range(21,31)):.2f}-{max(100*C[n][0][ln][1]/C[n][1] for n in range(21,31)):.2f}')
    print(f'      Tue 13,20,27 below: {[C[n][0][ln][1] for n in (13,20,27)]}; Fri 16,23,30: {[C[n][0][ln][1] for n in (16,23,30)]}')
    print(f'      day 20 listed at/above {C[20][0][ln][2]:,} below {C[20][0][ln][1]:,}; day 30 listed at/above {C[30][0][ln][2]:,} below {C[30][0][ln][1]:,}')
print('\n## Amended share by day, and all-attributed total, days 12-30')
for n in range(12, 31):
    print(n, (D0+timedelta(days=n)).strftime('%a'), ' '.join(f'L{ln} {100*C[n][0][ln][0]/(C[n][0][ln][0]+C[n][0][ln][1]):.1f}' for ln in FIX), f'att {C[n][1]:,}')
