"""R-0138: independent reproduction of the Node.js figures the revised piece uses,
from LH034's retained daily summaries and the release list kept on 5 November.
Written fresh for this review (not a copy of record_v1.py). Run: python3 -I <this file>"""
import gzip, json, re
from datetime import date, timedelta
from pathlib import Path
D = Path('studies/LH034/data')
rel = json.loads((D / 'read-2026-11-05T1414Z' / 'dist-index.derived.json').read_text())['extracted']['releases']
listed = [r[0] for r in rel]
listed_set = set(listed)
days = {}
for rd in sorted(p for p in D.iterdir() if p.name.startswith('read-')):
    for f in sorted(rd.glob('day-*.raw.gz')):
        d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
        if d not in days:
            days[d] = json.loads(gzip.decompress(f.read_bytes()))
D0 = date(2026, 10, 21)
PLAIN = re.compile(r'^v(\d+)\.(\d+)\.(\d+)$')
FIX = {22: (22, 23, 4), 24: (24, 22, 1), 26: (26, 12, 1)}
def tup(v):
    m = PLAIN.match(v); return tuple(map(int, m.groups())) if m else None
def line_of(v):
    m = re.match(r'^v(\d+)\.', v); return int(m.group(1)) if m else None
def split(ver, L, rule):
    above = below = 0
    for v, n in ver.items():
        if v == 'unknown' or line_of(v) != L: continue
        t = tup(v)
        if v in listed_set:
            if t is None: continue
            if t >= FIX[L]: above += n
            else: below += n
        elif rule == 'amended' and t is not None and t > FIX[L]:
            above += n
    return above, below
def share(d, L, rule):
    a, b = split(days[d]['version'], L, rule); return 100 * a / (a + b), a, b
dn = lambda n: D0 + timedelta(n)
print('== measure 1, selected days')
for n in [1, 2, 3, 4, 7, 14, 30]:
    print(n, ' '.join(f"L{L} written {share(dn(n),L,'written')[0]:.1f} amended {share(dn(n),L,'amended')[0]:.1f}" for L in FIX))
print('first day >= 50 (both rules agree before day 21):', {L: next(n for n in range(31) if share(dn(n), L, 'amended')[0] >= 50) for L in FIX})
print('days below half after first, line 22 amended:', [n for n in range(3, 31) if share(dn(n), 22, 'amended')[0] < 50])
print('== new versions share of line, day 30 (amended denominator)')
for L, v in [(22, 'v22.23.5'), (24, 'v24.22.3'), (26, 'v26.13.1')]:
    s, a, b = share(dn(30), L, 'amended'); n = days[dn(30)]['version'][v]
    print(v, n, f'{100*n/(a+b):.1f}%')
print('first day each appears:', {v: min(d for d in days if days[d]['version'].get(v)) for v in ['v22.23.5', 'v24.22.3', 'v26.13.1']})
print('== late rise: means days 13-20 vs 21-30, amended')
for L in FIX:
    A1 = sum(split(days[dn(n)]['version'], L, 'amended')[0] for n in range(13, 21)) / 8
    B1 = sum(split(days[dn(n)]['version'], L, 'amended')[1] for n in range(13, 21)) / 8
    A2 = sum(split(days[dn(n)]['version'], L, 'amended')[0] for n in range(21, 31)) / 10
    B2 = sum(split(days[dn(n)]['version'], L, 'amended')[1] for n in range(21, 31)) / 10
    print(L, f'above {100*(A2/A1-1):+.1f}%  below {100*(B2/B1-1):+.1f}%  share of means {100*A1/(A1+B1):.1f} -> {100*A2/(A2+B2):.1f}')
    r1 = [share(dn(n), L, 'amended')[0] for n in range(13, 21)]; r2 = [share(dn(n), L, 'amended')[0] for n in range(21, 31)]
    print('   daily ranges', f'{min(r1):.1f}-{max(r1):.1f}', f'{min(r2):.1f}-{max(r2):.1f}')
print('== line 22 below-fix counts')
print('days 5-7:', [split(days[dn(n)]['version'], 22, 'amended')[1] for n in (5, 6, 7)])
wk = [n for n in range(12, 31) if dn(n).weekday() < 5]
bw = [split(days[dn(n)]['version'], 22, 'amended')[1] for n in wk]
print('weekdays 12-30 min/max:', min(bw), max(bw), 'n days', len(wk))
print('== line 22 distance behind on day 30 (amended)')
order22 = [v for v in listed if line_of(v) == 22 and tup(v)]
fixi = order22.index('v22.23.4')
ver = days[dn(30)]['version']; a, b = split(ver, 22, 'amended'); tot = a + b
five = sum(n for v, n in ver.items() if v in listed_set and line_of(v) == 22 and tup(v) and tup(v) < FIX[22] and order22.index(v) - fixi >= 5)
print(f'below {100*b/tot:.1f}%, five or more behind {100*five/tot:.1f}%')
print('== unfixed tail (lines other than 22/24/26), share of version-attributed downloads')
def tail(d):
    ver = days[d]['version']; att = sum(n for v, n in ver.items() if v != 'unknown' and line_of(v) is not None)
    att2 = sum(n for v, n in ver.items() if v != 'unknown')
    unf = sum(n for v, n in ver.items() if v != 'unknown' and line_of(v) is not None and line_of(v) not in FIX)
    return 100 * unf / att, att, att2
for n in range(-7, 8):
    t, att, att2 = tail(dn(n)); print(n, dn(n), f'{t:.2f}', att == att2)
vals = [round(tail(dn(n))[0], 1) for n in range(-7, 8)]
print('days -7..7 range', min(vals), max(vals), '; day 30', round(tail(dn(30))[0], 1))
print('days 0..7 range', min(vals[7:]), max(vals[7:]))
print('== July (measure 4) first day at half, line 22, 24')
J0 = date(2026, 7, 28); JF = {22: (22, 23, 2), 24: (24, 18, 1), 26: (26, 5, 1)}
for L in (22, 24):
    for n in range(31):
        ver = days[J0 + timedelta(n)]['version']
        a = sum(c for v, c in ver.items() if line_of(v) == L and v in listed_set and tup(v) and tup(v) >= JF[L])
        b = sum(c for v, c in ver.items() if line_of(v) == L and v in listed_set and tup(v) and tup(v) < JF[L])
        if a / (a + b) >= .5: print(L, 'July first day at half', n); break
