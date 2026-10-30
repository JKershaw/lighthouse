#!/usr/bin/env python3
"""R-0039: independent recomputation of every figure in the week-one piece (articles/a-week-after-two-fixes.md),
its short form, its figure, and the Answer and Findings of LH033 and LH034, from the retained raw bodies.

Written by the evidence reviewer on 30 October 2026, without importing or reusing the studies' scripts.
Usage: python3 studies/LH034/review/R-0039_checks.py > studies/LH034/review/R-0039_checks.txt
Offline; reads only files in the repository.
"""
from datetime import date, timedelta
from pathlib import Path
from statistics import median
import csv
import gzip
import json
import re

ROOT = Path(__file__).resolve().parents[3]
L33 = ROOT / 'studies/LH033/data'
L34 = ROOT / 'studies/LH034/data'
DAY0 = date(2026, 10, 21)


def raw(p):
    return gzip.decompress(p.read_bytes())


def p1(x):
    return f'{100 * x:.2f}'


def section(t):
    print('\n' + '=' * 8 + ' ' + t)


# ---------------------------------------------------------------- Censys, read of 29 October (the interim cut-off)
section('A. Censys, read-2026-10-29T0635Z only (LH033 brief: interim uses this read for day 7)')
snap = json.loads(raw(L33 / 'read-2026-10-29T0635Z/censys.raw.gz'))['snapshot']
print('refreshed_at', snap['refreshed_at'])
cut = date(2026, 10, 29)
bh = {}
for r in snap['branch_history']:
    d = date.fromisoformat(r['day'])
    if d < cut and r['branch'] in ('8.2', '8.3', '8.4', '8.5'):
        bh.setdefault(r['branch'], {})[(d - DAY0).days] = (r['patched'], r['targets'])
php_share = {}
for b in sorted(bh):
    s = {k: p / t for k, (p, t) in sorted(bh[b].items())}
    php_share[b] = s
    half = next((k for k, v in s.items() if v >= 0.5), None)
    print(f'  {b}: ' + ' '.join(f'd{k}={p1(v)}' for k, v in s.items()) + f' | first day >=50%: {half} | targets d7 {bh[b][7][1]:,}')
    inc = [100 * (s[k] - s[k - 1]) for k in range(3, 8)]
    print(f'      daily rises d3..d7 (points): ' + ', '.join(f'{x:.2f}' for x in inc))
days_in = sorted({k for b in bh for k in bh[b]})
print('  days held:', days_in)
# day-by-day: older two always below newer two from day 1?
print('  older (8.2, 8.3) below newer (8.4, 8.5) on every day 1..7:',
      all(max(php_share['8.2'][k], php_share['8.3'][k]) < min(php_share['8.4'][k], php_share['8.5'][k]) for k in range(1, 8)))

hist = {}
for r in snap['history']:
    d = date.fromisoformat(r['day'])
    if d < cut:
        hist.setdefault((d - DAY0).days, {})[r['status']] = r['targets']
print('  history by day: nofix (M), versioned (M), nofix/versioned, unknown/all, all (M), fixed-branch versioned (affected+patched, M)')
for k, s in sorted(hist.items()):
    ver = s['affected'] + s['affected_nofix'] + s['patched']
    allv = ver + s['unknown']
    print(f'   d{k}: {s["affected_nofix"] / 1e6:.2f}  {ver / 1e6:.2f}  {p1(s["affected_nofix"] / ver)}  {p1(s["unknown"] / allv)}'
          f'  {allv / 1e6:.2f}  {(s["affected"] + s["patched"]) / 1e6:.2f}  unknown {s["unknown"] / 1e6:.2f}')
print('  status keys in history:', sorted({st for s in hist.values() for st in s}))
print('  unknown d2/d1 ratio:', round(hist[2]['unknown'] / hist[1]['unknown'], 2))


def nofix_branches(sn):
    agg = {}
    for r in sn['branches']:
        if r['status'] == 'affected_nofix':
            agg[r['branch']] = agg.get(r['branch'], 0) + r['targets']
    return sorted(agg.items(), key=lambda kv: -kv[1])


print('  snapshot (29 Oct read) unfixed branches, largest first:', [(b, round(n / 1e6, 2)) for b, n in nofix_branches(snap)[:6]])
base = json.loads(raw(L33 / 'read-2026-10-25T0855Z/censys.raw.gz'))['snapshot']
print('  snapshot (25 Oct baseline) unfixed branches, largest first:', [(b, round(n / 1e6, 2)) for b, n in nofix_branches(base)[:6]])
print('  snapshot kpi (29 Oct, current, not a day):', {k: snap['kpi'][k] for k in ('affected_nofix', 'unknown', 'php_targets')})

section('A2. Revisions: every completed day 0..7 identical in every read that holds it?')
reads = sorted(L33.glob('read-*/censys.raw.gz'))
first = {}
diffs = 0
for f in reads:
    rd = date.fromisoformat(f.parent.name[5:15])
    sn = json.loads(raw(f))['snapshot']
    for key, rows in (('bh', sn['branch_history']), ('h', sn['history'])):
        for r in rows:
            if date.fromisoformat(r['day']) < rd and date.fromisoformat(r['day']) <= date(2026, 10, 28):
                k = (key, r['day'], r.get('branch'), r.get('status'))
                v = (r.get('patched'), r['targets'])
                if k in first and first[k] != v:
                    diffs += 1
                    print('   revision', f.parent.name, k, first[k], v)
                first.setdefault(k, v)
print('  reads:', [f.parent.name for f in reads], '| revisions found:', diffs)

# ---------------------------------------------------------------- W3Techs
section('B. W3Techs, share of websites within each minor at or above the fixed patch (from raw HTML)')
FIXED = {'8.2': 35, '8.3': 36, '8.4': 27, '8.5': 12}
for rd in ('read-2026-10-25T0855Z', 'read-2026-10-26T0637Z'):
    out = []
    for m, fx in FIXED.items():
        t = raw(L33 / rd / f'w3techs-details-{m}.raw.gz').decode('utf8', 'replace')
        t = t[t.find('Subversions of PHP ' + m):]
        t = t[t.find('<table class=bars>'):]
        t = t[:t.find('</table></table>') + 1] if '</table></table>' in t else t[:20000]
        rows = re.findall(r'pl-php/' + re.escape(m) + r'\.(\d+)"[^>]*>Version [\d.]+</a>.*?<td>(?:(\d+(?:\.\d+)?)%|less than 0\.1%)', t, re.S)
        seen = {}
        for v, pct in rows:
            seen.setdefault(int(v), float(pct) if pct else 0.0)
        at = sum(p for v, p in seen.items() if v >= fx)
        out.append(f'{m} {at:.1f}% ({len(seen)} rows, fixed .{fx} row: {seen.get(fx)})')
    print(' ', rd, '|', '; '.join(out))

# ---------------------------------------------------------------- Packagist
section('C. Packagist, September 2026 installs from PHP 8.1 or older (packagist.json; raw body not retained, by design)')
pk = json.loads((L33 / 'read-2026-10-25T0855Z/packagist.json').read_text())
mo = pk['monthly']
i = mo['labels'].index('2026-09')
tot = sum(s[i] for s in mo['values'].values())
old = sum(s[i] for v, s in mo['values'].items() if tuple(int(x) for x in v.split('.')) <= (8, 1))
print(f'  monthly: {old / 1e6:.1f} M of {tot / 1e6:.1f} M = {p1(old / tot)}%')
da = pk['daily']
idx = [j for j, l in enumerate(da['labels']) if l.startswith('2026-09')]
dt = sum(s[j] or 0 for s in da['values'].values() for j in idx)
do = sum(s[j] or 0 for v, s in da['values'].items() for j in idx if tuple(int(x) for x in v.split('.')) <= (8, 1))
print(f'  daily series summed over {len(idx)} September days: {do / 1e6:.1f} M of {dt / 1e6:.1f} M = {p1(do / dt)}%')

# ---------------------------------------------------------------- Node.js
section('D. Node.js, from the raw daily summaries (earliest read per day) and dist/index.json')


def vkey(v):
    m = re.match(r'v(\d+)\.(\d+)\.(\d+)$', v)
    return tuple(int(x) for x in m.groups()) if m else None


nread = sorted(L34.glob('read-*'))
day = {}
for rd in nread:
    for f in sorted(rd.glob('day-*.raw.gz')):
        d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
        if d not in day:
            day[d] = (rd.name, json.loads(raw(f)))
idx = json.loads(raw(nread[-1] / 'dist-index.raw.gz'))
inidx = {r['version'] for r in idx}
dates = {r['version']: r['date'] for r in idx}
FIX10 = {'22': (22, 23, 4), '24': (24, 22, 1), '26': (26, 12, 1)}
FIX07 = {'22': (22, 23, 2), '24': (24, 18, 1), '26': (26, 5, 1)}
for ln, fx in FIX10.items():
    newer = sorted((v for v in inidx if vkey(v) and vkey(v)[0] == fx[0] and vkey(v) >= fx), key=vkey)
    print(f'  line {ln}: versions in dist/index.json at or above v{".".join(map(str, fx))}:',
          [(v, dates[v], 'security' if next(r for r in idx if r['version'] == v).get('security') else '') for v in newer])
print('  releases dated after 2026-10-21 in dist/index.json:', [(r['version'], r['date']) for r in idx if r['date'] > '2026-10-21'])


def shares(vers, fixed, only_index=True):
    res = {}
    for ln, fx in fixed.items():
        tot = new = 0
        for v, n in vers.items():
            k = vkey(v)
            if not k or k[0] != fx[0] or (only_index and v not in inidx):
                continue
            tot += n
            new += n if k >= fx else 0
        res[ln] = (new / tot if tot else None, tot)
    return res


node = {}
odd = {}
print('  October: share at or above fix by line (in dist/index.json); [all keys incl. not in index]; line downloads')
for k in range(0, 8):
    d = DAY0 + timedelta(days=k)
    src, s = day[d]
    a = shares(s['version'], FIX10)
    b = shares(s['version'], FIX10, only_index=False)
    node[k] = {ln: a[ln][0] for ln in a}
    for v in s['version']:
        if vkey(v) and vkey(v)[0] in (22, 24, 26) and v not in inidx:
            odd[v] = odd.get(v, 0) + s['version'][v]
    print(f'   d{k} {d} ({src}): ' + '  '.join(f'{ln} {p1(a[ln][0])} [{p1(b[ln][0])}] {a[ln][1] / 1e6:.2f}M' for ln in a)
          + f'  | total {s["total"] / 1e6:.1f}M')
print('  line 22/24/26 keys not in dist/index.json (summed d0..7):', odd)
for ln in FIX10:
    print(f'   line {ln} first day >= 50%: {next(k for k in range(8) if node[k][ln] >= 0.5)};'
          f' days below 50% after that: {[k for k in range(next(k for k in range(8) if node[k][ln] >= 0.5), 8) if node[k][ln] < 0.5]}')
# how much of day 7 is the later releases
s7 = day[DAY0 + timedelta(days=7)][1]['version']
for ln, later in (('24', 'v24.22.2'), ('26', 'v26.13.0')):
    tot = sum(n for v, n in s7.items() if vkey(v) and vkey(v)[0] == int(ln) and v in inidx)
    print(f'   day 7 line {ln}: {later} alone {p1(s7.get(later, 0) / tot)}% of the line; fixed release alone '
          f'{p1(s7.get("v" + ".".join(map(str, FIX10[ln])), 0) / tot)}%')

section('D2. Unfixed lines, line 20, line 25 and no-version share, 23 Sept to 28 Oct')
tail = {}
for d in sorted(day):
    if date(2026, 9, 23) <= d <= date(2026, 10, 28):
        s = day[d][1]
        v = {x: n for x, n in s['version'].items() if x != 'unknown'}
        att = sum(v.values())
        ln = lambda x: x[1:].split('.')[0]
        unf = sum(n for x, n in v.items() if ln(x) not in ('22', '24', '26'))
        tail[d] = (unf / att, sum(n for x, n in v.items() if ln(x) == '20') / att,
                   sum(n for x, n in v.items() if ln(x) == '25') / att, (s['total'] - att) / s['total'], s['total'])
        print(f'   {d} {d.strftime("%a")} unfixed {p1(tail[d][0])}  l20 {p1(tail[d][1])}  l25 {p1(tail[d][2])}  noversion {100 * tail[d][3]:.4f}%  total {tail[d][4] / 1e6:.1f}M')
w = [d for d in tail if date(2026, 10, 14) <= d <= date(2026, 10, 28)]
print('  14-28 Oct unfixed range', p1(min(tail[d][0] for d in w)), 'to', p1(max(tail[d][0] for d in w)),
      '| l20', p1(min(tail[d][1] for d in w)), 'to', p1(max(tail[d][1] for d in w)),
      '| l25', p1(min(tail[d][2] for d in w)), 'to', p1(max(tail[d][2] for d in w)))
sep = [d for d in tail if d <= date(2026, 9, 30)]
print('  23-30 Sept unfixed:', [p1(tail[d][0]) for d in sep])
print('  max no-version share of total, 23 Sept-28 Oct:', f'{100 * max(t[3] for t in tail.values()):.4f}%')
wk = [day[DAY0 + timedelta(days=k)][1]['total'] for k in (1, 2, 5, 6, 7)]
print('  weekend totals (24, 25 Oct) vs mean of weekday days 1,2,5,6,7:',
      [round(day[DAY0 + timedelta(days=k)][1]['total'] / (sum(wk) / len(wk)), 2) for k in (3, 4)])
for ln, fx in FIX10.items():
    lt = lambda k: shares(day[DAY0 + timedelta(days=k)][1]['version'], FIX10)[ln][1]
    print(f'   line {ln} downloads, weekend vs weekday mean: {round((lt(3) + lt(4)) / 2 / (sum(lt(k) for k in (1, 2, 5, 6, 7)) / 5), 2)}')

section('D3. July security release (measure 4): day 0 = 28 July by the brief; posting-aligned is post hoc')
J0 = date(2026, 7, 28)
jul = {}
for k in range(0, 31):
    d = J0 + timedelta(days=k)
    if d in day:
        jul[k] = {ln: v[0] for ln, v in shares(day[d][1]['version'], FIX07).items()}
print('  July days held:', min(jul), 'to', max(jul), len(jul))
for ln in FIX07:
    print(f'   line {ln}: ' + ' '.join(f'd{k}={p1(jul[k][ln])}' for k in (1, 2, 3, 7, 8))
          + f' | first day >=50%: {next((k for k in sorted(jul) if jul[k][ln] >= 0.5), None)}')
print('  October above July on every day 1..7, brief alignment (July day k) and posting alignment (July day k+1):')
for ln in FIX07:
    a = all(node[k][ln] > jul[k][ln] for k in range(1, 8))
    b = all(node[k][ln] > jul[k + 1][ln] for k in range(1, 8))
    print(f'   line {ln}: brief {a}, posting {b}; day 7 Oct {p1(node[7][ln])} vs July d7 {p1(jul[7][ln])} / d8 {p1(jul[8][ln])}')

# ---------------------------------------------------------------- Python comparators, recomputed from LH011 and LH008
section('E. Python comparators from LH011 release_days.csv and LH008 lags.csv')
FIXES = {('urllib3', '2.7.0'), ('cryptography', '48.0.1'), ('pyjwt', '2.13.0'), ('starlette', '1.1.0')}
rows = [r for r in csv.DictReader(open(ROOT / 'studies/LH011/data/analysis/release_days.csv')) if r['status'] == 'known']
py = {}
per = {}
for r in rows:
    d = int(r['day'])
    v = float(r['share_at_or_newer'])
    if (r['project'], r['version']) in FIXES:
        py.setdefault((r['project'], r['version']), {})[d] = v
    per.setdefault(d, {}).setdefault(r['project'], []).append(v)
for f in sorted(py):
    print('  ', f, ' '.join(f'd{d}={p1(py[f][d])}' for d in (1, 2, 7, 14, 30)))
pyr = {}
for d in (1, 2, 7, 14, 30):
    vals = [py[f][d] for f in py]
    mm = median([median(v) for v in per[d].values()])
    pyr[d] = (min(vals), max(vals))
    print(f'   day {d}: four fixes {p1(min(vals))} to {p1(max(vals))}; median of {len(per[d])} project medians {p1(mm)}')
print('   fixes higher on day 30 than day 7:', {f'{p} {v}': py[(p, v)][30] > py[(p, v)][7] for p, v in sorted(py)})
moved = {7: 0, 30: 0}
n = 0
for r in csv.DictReader(open(ROOT / 'studies/LH008/data/lags.csv')):
    if r['frame'].endswith(':fix'):
        n += 1
        if r['outcome'] == 'moved' and r['lag_release_days']:
            for k in moved:
                moved[k] += float(r['lag_release_days']) <= k
print(f'   LH008 fix pairs: {n}; moved within 7 days {moved[7]}, within 30 days {moved[30]}')

# ---------------------------------------------------------------- comparison sentences
section('F. Comparison sentences, day by day')
for k in (1, 2, 7):
    ph = [php_share[b][k] for b in php_share]
    nd = [node[k][l] for l in node[k]]
    lo, hi = pyr[k]
    print(f'  day {k}: PHP {p1(min(ph))}-{p1(max(ph))}; Node {p1(min(nd))}-{p1(max(nd))}; Python {p1(lo)}-{p1(hi)}')
    print(f'    every PHP below every Python: {max(ph) < lo}; Node all below Python: {max(nd) < lo}; Node all above PHP: {min(nd) > max(ph)}')
    print(f'    Node lines below / within / above Python range:', {l: ('below' if node[k][l] < lo else 'above' if node[k][l] > hi else 'within') for l in node[k]})
    print(f'    PHP branches below / within / above Python range:', {b: ('below' if php_share[b][k] < lo else 'above' if php_share[b][k] > hi else 'within') for b in php_share})
print('  PHP 8.5 above every Node line AND above Python max, by day:')
for k in range(0, 8):
    above_node = php_share['8.5'][k] > max(node[k].values())
    print(f'    d{k}: 8.5 {p1(php_share["8.5"][k])} vs Node max {p1(max(node[k].values()))}: above Node {above_node}')
print('  (Python comparators exist only for days 1, 2, 7, 14, 30 in python_side.json; the figure uses LH011 days 0..7)')
