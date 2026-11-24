"""R-0128: independent reproduction of LH034 version 1.0's consequential figures.

Written by the evidence reviewer from the brief and the retained files only; it does
not import or copy studies/LH034/scripts/record_v1.py or tabulate.py.
Run from the repository root:  python3 -I notes/R-0128-lh034-v1-evidence/reproduce.py
"""
import gzip, json, glob, hashlib, os, re, statistics
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, 'studies/LH034/data')
PLAIN = re.compile(r'v(\d+)\.(\d+)\.(\d+)')

def pct(num, den):
    """Round once, half up, from the exact counts."""
    return float((Decimal(num) * 100 / Decimal(den)).quantize(Decimal('0.1'), ROUND_HALF_UP))

# ---- day files: earliest read holding each day (read dirs sort by time in their names)
reads = sorted(glob.glob(os.path.join(D, 'read-*')))
first = {}
copies = {}
for r in reads:
    for f in sorted(glob.glob(os.path.join(r, 'day-*.raw.gz'))):
        ds = os.path.basename(f)[4:12]
        day = date(int(ds[:4]), int(ds[4:6]), int(ds[6:]))
        copies.setdefault(day, []).append(f)
        first.setdefault(day, f)
data = {d: json.loads(gzip.open(f).read()) for d, f in first.items()}
print('days held', len(data), min(data), max(data))

# ---- release list read 5 November (derived file)
rel = json.load(open(os.path.join(D, 'read-2026-11-05T1414Z/dist-index.derived.json')))['extracted']['releases']
listed = [v for v, _, _ in rel]
listed_set = set(listed)
reldate = {v: dt for v, dt, _ in rel}

def line_of(v):
    m = re.match(r'v(\d+)\.', v)
    return int(m.group(1)) if m else None

def line_order(line):  # newest first, list order
    return [v for v in listed if line_of(v) == line]

def semver(v):
    m = PLAIN.fullmatch(v)
    return tuple(int(x) for x in m.groups()) if m else None

def counts(day, line, fix, rule):
    """(at_or_above, denominator, unlisted_above) for one line and day."""
    order = line_order(line)
    fi = order.index(fix)
    above = set(order[:fi + 1])
    num = den = unl = 0
    for v, n in data[day]['version'].items():
        if line_of(v) != line:
            continue
        if v in listed_set:
            den += n
            if v in above:
                num += n
        elif rule == 'amended' and semver(v) and semver(v) > semver(fix):
            num += n; den += n; unl += n
    return num, den, unl

OCT0 = date(2026, 10, 21)
FIX = {22: 'v22.23.4', 24: 'v24.22.1', 26: 'v26.12.1'}
out = {}

# ---- measure 1
print('\nMeasure 1 (per cent, rounded once from counts)')
m1 = {}
for rule in ('as_written', 'amended'):
    for L, fix in FIX.items():
        s = []
        for k in range(31):
            n, d, _ = counts(OCT0 + timedelta(k), L, fix, rule)
            s.append((n, d))
        exact = [n / d for n, d in s]
        r1 = [pct(n, d) for n, d in s]
        m1[(rule, L)] = exact
        half = next(k for k in range(31) if exact[k] >= 0.5)
        below_after = [k for k in range(half + 1, 31) if exact[k] < 0.5]
        S7 = statistics.mean(exact[5:8]) * 100; S30 = statistics.mean(exact[28:31]) * 100
        print(f' {rule:10s} {L}: ' + ' '.join(f'{x:5.1f}' for x in r1))
        print(f'   first half day {half}; below half after {below_after}; d1 {r1[1]} d2 {r1[2]} d7 {r1[7]} d14 {r1[14]} d30 {r1[30]}; 1-d30 {round(100 - r1[30], 1)} (from counts {pct(s[30][1]-s[30][0], s[30][1])}); d30 line count {s[30][1]}')
        print(f'   d13-20 [{min(r1[13:21])}, {max(r1[13:21])}]; d21-30 [{min(r1[21:31])}, {max(r1[21:31])}]; S7 {S7:.2f} S30 {S30:.2f} L {(S30 - S7) / S30:.4f}')
        out[(rule, L)] = dict(S7=S7, S30=S30, L=(S30 - S7) / S30)

# unlisted share of line on day 30 (amended denominator)
print('\nUnlisted plain keys above fix, share of line (amended)')
for L, fix in FIX.items():
    for k in (21, 22, 25, 28, 29, 30):
        n, d, u = counts(OCT0 + timedelta(k), L, fix, 'amended')
        keys = {v: c for v, c in data[OCT0 + timedelta(k)]['version'].items() if line_of(v) == L and v not in listed_set}
        print(f'  line {L} day {k}: unlisted keys {keys}; share {pct(u, d)}')
# any other unlisted key in fixed lines, days 0-30
other = set()
for k in range(31):
    for v in data[OCT0 + timedelta(k)]['version']:
        if line_of(v) in FIX and v not in listed_set and not (semver(v) and semver(v) > semver(FIX[line_of(v)])):
            other.add(v)
print('  other unlisted keys in fixed lines days 0-30:', sorted(other))
print('  first day each unlisted in-line key appears:', {v: min(k for k in range(31) if v in data[OCT0 + timedelta(k)]['version']) for v in ('v22.23.5', 'v24.22.3', 'v26.13.1')})

# ---- tests A and B
php = json.load(open(os.path.join(ROOT, 'studies/LH033/data/record_v1.json')))['amendment2']['php']
phpmed = statistics.median(v['L'] for v in php.values())
print(f'\nPHP median L {phpmed:.5f}')
for rule in ('as_written', 'amended'):
    Ls = [out[(rule, L)]['L'] for L in FIX]
    gap = min(out[(rule, 24)]['S30'], out[(rule, 26)]['S30']) - out[(rule, 22)]['S30']
    print(f' {rule}: median L {statistics.median(Ls):.4f}, A holds {statistics.median(Ls) < phpmed}; B gap {gap:.2f} holds {gap > 5}')

# ---- measure 2
print('\nMeasure 2')
def m2(day):
    v = data[day]['version']
    attr = sum(n for k, n in v.items() if k != 'unknown')
    unf = sum(n for k, n in v.items() if k != 'unknown' and line_of(k) not in FIX)
    by = lambda L: sum(n for k, n in v.items() if line_of(k) == L)
    nov = data[day]['total'] - attr
    return attr, unf, by(20), by(25), by(27), nov, data[day]['total']
rows = {}
for k in range(-28, 31):
    day = OCT0 + timedelta(k)
    if day in data:
        rows[k] = m2(day)
sep = [k for k in rows if OCT0 + timedelta(k) <= date(2026, 9, 30)]
def rng(ks, i):
    vals = [pct(rows[k][i], rows[k][0]) for k in ks]
    return min(vals), max(vals)
print('  Sep 23-30 unfixed', rng(sep, 1), 'days -7..-1', rng(range(-7, 0), 1), 'days 8-30', rng(range(8, 31), 1), 'days 0-7', rng(range(0, 8), 1))
print('  day 0,2,7,14,30 unfixed', [pct(rows[k][1], rows[k][0]) for k in (0, 2, 7, 14, 30)])
print('  line20 days 0-30', rng(range(31), 2), 'day30', pct(rows[30][2], rows[30][0]), '| line25 days 0-30', rng(range(31), 3), 'day30', pct(rows[30][3], rows[30][0]))
l27 = [round(rows[k][4] / rows[k][0] * 100, 2) for k in range(31)]
print('  line27 per day 0-30', l27, '; day 9 unfixed', pct(rows[9][1], rows[9][0]), '; days 10-30 range', min(l27[10:]), max(l27[10:]))
print('  max no-version share of total Sep23..d30', max(rows[k][5] / rows[k][6] * 100 for k in rows), '%; day30 total', rows[30][6], 'attributed', rows[30][0])
wk = {k: rows[k][6] for k in range(31)}
we = [wk[k] for k in range(31) if (OCT0 + timedelta(k)).weekday() >= 5]
wd = [wk[k] for k in range(31) if (OCT0 + timedelta(k)).weekday() < 5]
print(f'  weekend totals {min(we)/1e6:.1f}-{max(we)/1e6:.1f} M; weekday {min(wd)/1e6:.1f}-{max(wd)/1e6:.1f} M')
print('  sep days held', sorted(OCT0 + timedelta(k) for k in sep)[0], len(sep))

# ---- measure 3, day 30
print('\nMeasure 3, day 30')
d30 = OCT0 + timedelta(30)
for rule in ('as_written', 'amended'):
    for L, fix in FIX.items():
        order = line_order(L); fi = order.index(fix)
        g = {'at': 0, '1': 0, '2-4': 0, '5+': 0}; per = {}
        for v, n in data[d30]['version'].items():
            if line_of(v) != L:
                continue
            if v in listed_set:
                behind = order.index(v) - fi
                key = 'at' if behind <= 0 else '1' if behind == 1 else '2-4' if behind <= 4 else '5+'
                g[key] += n
                if behind > 0:
                    per[v] = (behind, n)
            elif rule == 'amended' and semver(v) and semver(v) > semver(fix):
                g['at'] += n
        tot = sum(g.values())
        big = max(per.items(), key=lambda x: x[1][1])
        print(f'  {rule:10s} {L}: total {tot}; ' + ', '.join(f'{k} {pct(x, tot)}' for k, x in g.items()) + f'; largest below {big[0]} {big[1][0]} behind {pct(big[1][1], tot)}')

# ---- measure 4, July
print('\nMeasure 4 (July)')
JUL0 = date(2026, 7, 28)
FIXJ = {22: 'v22.23.2', 24: 'v24.18.1', 26: 'v26.5.1'}
print('  list dates of July fixes', {v: reldate[v] for v in FIXJ.values()})
for L, fix in FIXJ.items():
    order = line_order(L); fi = order.index(fix); above = set(order[:fi + 1])
    s = []
    for k in range(31):
        v = data[JUL0 + timedelta(k)]['version']
        unl = [x for x in v if line_of(x) == L and x not in listed_set]
        assert not unl, unl
        num = sum(n for x, n in v.items() if x in above); den = sum(n for x, n in v.items() if line_of(x) == L and x in listed_set)
        s.append((num, den))
    ex = [n / d for n, d in s]
    half = next(k for k in range(31) if ex[k] >= 0.5)
    print(f'  {L}: first half {half}; d1 {pct(*s[1])} d2 {pct(*s[2])} d3 {pct(*s[3])} d7 {pct(*s[7])} d8 {pct(*s[8])} d14 {pct(*s[14])} d15 {pct(*s[15])} d30 {pct(*s[30])}; d7 counts {s[7]}')
    later = [(v, reldate[v]) for v in order[:fi] if reldate[v] <= str(JUL0 + timedelta(30))]
    print(f'     later listed releases within July 30 days: {later}')

# ---- comparators
print('\nComparators')
py = json.load(open(os.path.join(ROOT, 'studies/LH033/data/python_side.json')))
php1 = json.load(open(os.path.join(ROOT, 'studies/LH033/data/record_v1.json')))['m1_summary']
for k in (1, 2, 7, 14, 30):
    pv = [py['four_security_fixes'][p][str(k)] * 100 for p in py['four_security_fixes']]
    ph = [php1[b][f'day{k}'] for b in php1]
    print(f'  day {k}: python4 {min(pv):.1f}-{max(pv):.1f} (exact {min(pv):.4f}-{max(pv):.4f}); median37 {py["median_of_project_medians_37"][str(k)]["median"]}; php {min(ph)}-{max(ph)}')
    for rule in ('as_written', 'amended'):
        pl = []
        for L in FIX:
            x = m1[(rule, L)][k] * 100
            a = 'below' if x < min(pv) else 'above' if x > max(pv) else 'within'
            b = 'below' if x < min(ph) else 'above' if x > max(ph) else 'within'
            pl.append(f'{L}:{a}/{b}')
        print(f'     {rule}: ' + ' '.join(pl))

# ---- reread of days 0-7
print('\nRe-read of days 0-7')
for k in range(8):
    day = OCT0 + timedelta(k)
    c = copies[day]
    b = [gzip.open(f).read() for f in c]
    print(f'  day {k}: copies {len(c)} {[os.path.basename(os.path.dirname(f)) for f in c]}; identical {all(x == b[0] for x in b)}; sha {hashlib.sha256(b[0]).hexdigest()[:16]}')
# read-log sha check for every first copy
bad = []
for r in reads:
    log = json.load(open(os.path.join(r, 'read_log.json')))
    for e in log:
        if e.get('file', '').startswith('day-'):
            raw = gzip.open(os.path.join(r, e['file'])).read()
            if hashlib.sha256(raw).hexdigest() != e['sha256'] or len(raw) != e['bytes']:
                bad.append((r, e['file']))
print('  read-log sha/bytes mismatches over all day files:', bad)

# ---- supplementary checks (added after the first pass)
print('\nSupplementary')
print('  unfixed share, 1 to 13 October (days -20 to -8):', rng(range(-20, -7), 1), '; days held', sum(1 for k in range(-20, -7) if k in rows))
print('  unfixed share days 8, 9, 10 and the same without line 27:',
      [(k, pct(rows[k][1], rows[k][0]), pct(rows[k][1] - rows[k][4], rows[k][0])) for k in (8, 9, 10)])
for rule in ('amended', 'as_written'):
    g = min(out[(rule, 24)]['S30'], out[(rule, 26)]['S30']) - out[(rule, 22)]['S30']
    print(f'  test B gap {rule}, unrounded S30s: {g:.4f}')
# list order within fixed lines agrees with semver
for L in FIX:
    o = line_order(L)
    print(f'  line {L}: list order == semver order descending: {o == sorted(o, key=semver, reverse=True)}')
# as-written line 22: listed at-or-above vs listed below the fix, day 20 and day 30 (counts)
for L, fix in FIX.items():
    for k in (20, 30):
        n, d, _ = counts(OCT0 + timedelta(k), L, fix, 'as_written')
        print(f'  line {L} day {k}: listed at/above {n}, listed below {d - n}')

# ---- Python median of 37 project medians, unrounded, from LH011's retained table
import csv
share = {}
for row in csv.DictReader(open(os.path.join(ROOT, 'studies/LH011/data/analysis/release_days.csv'))):
    if row['status'] == 'known' and int(row['day']) in (1, 2, 7, 14, 30):
        share[(row['project'], row['version'], int(row['day']))] = float(row['share_at_or_newer'])
projs = sorted({p for p, _, _ in share})
for k in (1, 2, 7, 14, 30):
    pm = [statistics.median(v) for p in projs if (v := [s for (q, ver, dd), s in share.items() if q == p and dd == k])]
    print(f'  Python median of {len(pm)} project medians, day {k}: {statistics.median(pm) * 100:.4f} per cent')
