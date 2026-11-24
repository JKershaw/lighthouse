#!/usr/bin/env python3
"""Resolution of R-0131 (driving session, 24 November 2026). Post hoc, descriptive.
Per fixed line: downloads at or above the fix (listed + the three unlisted plain keys above it, i.e. the
amended rule) and below the fix, as means over day windows, and a split of each amended-share change into
the part from the change in at-or-above downloads and the part from the change in below-fix downloads.
Split: share s = A/(A+B). From window 1 to window 2, 'A only' = A2/(A2+B1) - s1, 'B only' = A1/(A1+B2) - s1,
reported with the interaction remainder. Same rules as scripts/record_v1.py (earliest read per day; list of
5 November; plain vX.Y.Z keys; 'unknown' not a version). Standard library only.
Usage: python3 -I studies/LH034/review/resolution_R-0131.py > studies/LH034/review/resolution_R-0131.txt"""
from datetime import date, timedelta
from pathlib import Path
import gzip, json, re
DATA = Path(__file__).resolve().parents[1] / 'data'
lst = json.loads((DATA / 'read-2026-11-05T1414Z' / 'dist-index.derived.json').read_text())['extracted']
listed = {dict(zip(lst['fields'], r))['version'] for r in lst['releases']}
days = {}
for read in sorted(DATA.glob('read-*')):
    for f in sorted(read.glob('day-*.raw.gz')):
        d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
        days.setdefault(d, json.loads(gzip.decompress(f.read_bytes())))
FIX = {'22': (22, 23, 4), '24': (24, 22, 1), '26': (26, 12, 1)}
P = re.compile(r'v(\d+)\.(\d+)\.(\d+)')
d0 = date(2026, 10, 21)

def counts(n, ln):
    vt = days[d0 + timedelta(n)]['version']; fx = FIX[ln]; a = b = 0
    for k, c in vt.items():
        m = P.fullmatch(k)
        if not m or m.group(1) != ln: continue
        sv = tuple(map(int, m.groups()))
        if k in listed:
            if sv >= fx: a += c
            else: b += c
        elif sv > fx: a += c
    return a, b

def window(ns, ln):
    A = sum(counts(n, ln)[0] for n in ns) / len(ns); B = sum(counts(n, ln)[1] for n in ns) / len(ns)
    return A, B

def split(w1, w2, label):
    print(f'\n## {label}')
    for ln in FIX:
        A1, B1 = window(w1, ln); A2, B2 = window(w2, ln)
        s1, s2 = A1 / (A1 + B1), A2 / (A2 + B2)
        ao = A2 / (A2 + B1) - s1; bo = A1 / (A1 + B2) - s1; rest = (s2 - s1) - ao - bo
        print(f'L{ln}: at/above mean {A1:,.0f} -> {A2:,.0f} ({100*(A2/A1-1):+.1f}%); '
              f'below mean {B1:,.0f} -> {B2:,.0f} ({100*(B2/B1-1):+.1f}%); '
              f'share of means {100*s1:.1f} -> {100*s2:.1f} ({100*(s2-s1):+.1f} pts): '
              f'from at/above change {100*ao:+.1f}, from below change {100*bo:+.1f}, interaction {100*rest:+.1f}')

print('# Post hoc, descriptive; amended rule (at or above = listed at/above + unlisted plain above the fix)')
split(range(13, 21), range(21, 31), 'Days 13 to 20 against days 21 to 30 (all days)')
split([16, 19, 20], [28, 29, 30], 'Weekday triples: days 16, 19, 20 (Fri, Mon, Tue) against 28, 29, 30 (Wed, Thu, Fri)')
split([5, 6, 7], [28, 29, 30], "Amendment 1's windows: days 5 to 7 (S7) against days 28 to 30 (S30)")
print('\n## Same-weekday pairs, below-fix downloads (Tue 3, 10, 17 Nov; Fri 6, 13, 20 Nov)')
for ln in FIX:
    print(f'L{ln}: Tue ' + ', '.join(f'{counts(n, ln)[1]:,}' for n in (13, 20, 27)) +
          '; Fri ' + ', '.join(f'{counts(n, ln)[1]:,}' for n in (16, 23, 30)))
print('\n## Below-fix and at-or-above downloads by day, days 0 to 30 (amended rule), millions')
for n in range(0, 31):
    d = d0 + timedelta(n)
    print(f'{n:>3} {d} {d.strftime("%a")} | ' + ' | '.join(
        f'L{ln}: {counts(n, ln)[0]/1e6:5.2f}M / {counts(n, ln)[1]/1e6:5.2f}M' for ln in FIX))
