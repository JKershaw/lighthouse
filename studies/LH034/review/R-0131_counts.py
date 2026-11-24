#!/usr/bin/env python3
"""R-0131 (reader-and-inference review of LH034 v1.0): absolute downloads per fixed line, days 13 to 30,
split into listed at/above the fix, unlisted plain above the fix (the three November keys), and below the fix.
Asks whether the amended share's rise after day 21 comes from fewer below-fix downloads or from added volume.
Same rules as scripts/record_v1.py (earliest read per day; list of 5 November). Standard library only.
Usage: python3 -I studies/LH034/review/R-0131_counts.py > studies/LH034/review/R-0131_counts.txt"""
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
print('day date  wd | line: listed>=fix  unlisted>fix  below  | below as share of all attributed downloads')
for n in range(13, 31):
    d = d0 + timedelta(n); vt = days[d]['version']
    att = sum(c for k, c in vt.items() if k != 'unknown')
    row = [f'{n:>3} {d} {d.strftime("%a")}']
    for ln, fx in FIX.items():
        a = u = b = 0
        for k, c in vt.items():
            m = P.fullmatch(k)
            if not m or m.group(1) != ln: continue
            sv = tuple(map(int, m.groups()))
            if k in listed:
                if sv >= fx: a += c
                else: b += c
            elif sv > fx: u += c
        row.append(f'L{ln}: {a/1e6:5.2f}M {u/1e6:5.2f}M {b/1e6:5.2f}M ({100*b/att:4.1f}%)')
    print(' | '.join(row))
