#!/usr/bin/env python3
"""R-0100: independent reproduction of LH033 record 1.0's figures, from retained files only.

Run from the repository root: python3 -I notes/R-0121-lh033-v1-evidence/reproduce.py
Written by the evidence reviewer (Opus 5.5) on 23 November 2026; does not import record_v1.py.
"""
import csv, gzip, json, re, statistics as st
from datetime import date, timedelta
from pathlib import Path

R = Path('.').resolve()
D = R / 'studies/LH033/data'
DAY0 = date(2026, 10, 21)
FIX = {'8.2': 35, '8.3': 36, '8.4': 27, '8.5': 12}
def pct(x): return round(100 * x, 2)

reads = sorted(x for x in D.glob('read-*') if (x / 'censys.raw.gz').exists())
print('reads with Censys body:', len(reads), [x.name for x in reads])

# earliest read per completed day (day strictly before the read's UTC date)
bh, hs, rev = {}, {}, 0
for rd in reads:
    s = json.load(gzip.open(rd / 'censys.raw.gz'))['snapshot']
    rdate = date.fromisoformat(rd.name[5:15])
    for r in s['branch_history']:
        dd = date.fromisoformat(r['day'])
        if dd >= rdate: continue
        k = (r['branch'], (dd - DAY0).days)
        v = (r['patched'], r['targets'])
        if k in bh and bh[k] != v: rev += 1; print('REVISION', k, bh[k], v, rd.name)
        bh.setdefault(k, v)
    tmp = {}
    for r in s['history']:
        dd = date.fromisoformat(r['day'])
        if dd >= rdate: continue
        tmp.setdefault((dd - DAY0).days, {})[r['status']] = r['targets']
    for n, v in tmp.items():
        if n in hs and hs[n] != v: rev += 1; print('REVISION history', n, rd.name)
        hs.setdefault(n, v)
print('revisions found:', rev)
print('history statuses seen:', sorted({k for v in hs.values() for k in v}))

sh = {b: {n: bh[(b, n)][0] / bh[(b, n)][1] for n in range(0, 31) if (b, n) in bh} for b in FIX}
print('\n== Measure 1 ==')
for b in FIX:
    s = sh[b]
    half = next(n for n in sorted(s) if s[n] >= 0.5)
    print(b, 'days held', len(s), 'day0', pct(s[0]), ' '.join(f'd{n}={pct(s[n])}' for n in (1, 2, 7, 14, 23, 28, 29, 30)),
          'half day', half, 'targets d30', bh[(b, 30)][1], 'not patched d30', pct(1 - s[30]),
          'rise14-30', pct(s[30] - s[14]), 'rise23-30', pct(s[30] - s[23]),
          'share of rise 0-30 by day2', round((s[2] - s[0]) / (s[30] - s[0]), 3))
older_below = all(max(sh['8.2'][n], sh['8.3'][n]) < min(sh['8.4'][n], sh['8.5'][n]) for n in range(1, 31))
print('older both below newer both, every day 1..30:', older_below,
      '; day0:', max(sh['8.2'][0], sh['8.3'][0]) < min(sh['8.4'][0], sh['8.5'][0]))
print('monotone non-decreasing days 0..30 per branch:', {b: all(sh[b][n+1] >= sh[b][n] for n in range(30)) for b in FIX})
print('day 29 change in targets and patched:', {b: (bh[(b,29)][1]-bh[(b,28)][1], bh[(b,29)][0]-bh[(b,28)][0]) for b in FIX})

print('\n== Measure 2 ==')
for n in (0, 1, 2, 7, 14, 28, 29, 30):
    h = hs[n]; ver = h['affected'] + h['affected_nofix'] + h['patched']; allt = ver + h['unknown']
    print(f'day {n}: nofix {h["affected_nofix"]:,} of versioned {ver:,} = {pct(h["affected_nofix"]/ver)}%; unknown {h["unknown"]:,} of {allt:,} = {pct(h["unknown"]/allt)}%')
print('nofix fall day14->30:', hs[14]['affected_nofix'] - hs[30]['affected_nofix'])

print('\n== Measure 3 (read 2026-11-21T1414Z) ==')
snap30 = json.load(gzip.open(D / 'read-2026-11-21T1414Z/censys.raw.gz'))['snapshot']; s30 = snap30
print('refreshed', s30['refreshed_at'])
for b, fx in FIX.items():
    rows = [r for r in s30['branch_versions'] if r['branch'] == b]
    tot = sum(r['targets'] for r in rows)
    g = {'at/above': 0, 'one': 0, '2-4': 0, '5+': 0, 'unparsed': 0}; below = []
    for r in rows:
        m = re.fullmatch(rf'{re.escape(b)}\.(\d+)', r['version'])
        if not m: g['unparsed'] += r['targets']; continue
        p = int(m.group(1)); gap = fx - p
        k = 'at/above' if gap <= 0 else 'one' if gap == 1 else '2-4' if gap <= 4 else '5+'
        g[k] += r['targets']
        if gap > 0: below.append((r['targets'], r['version']))
    below.sort(reverse=True)
    print(b, 'total', tot, 'vs d30 bar', bh[(b, 30)][1], 'diff %', round(100 * (tot - bh[(b, 30)][1]) / bh[(b, 30)][1], 3),
          {k: pct(v / tot) for k, v in g.items()}, 'top below', [(v, t, pct(t / tot)) for t, v in below[:3]])

print('\n== php.net release dates (day-30 read) ==')
for b in FIX:
    j = json.loads(gzip.decompress((D / f'read-2026-11-21T1414Z/phpnet-releases-{b}.raw.gz').read_bytes()))
    def find(v, x=j):
        if isinstance(x, dict):
            if v in x and isinstance(x[v], dict): return x[v].get('date')
            for y in x.values():
                r = find(v, y)
                if r: return r
        return None
    for v in [f'{b}.{FIX[b]-1}', f'{b}.{FIX[b]}', f'{b}.{FIX[b]+1}'] + (['8.3.8'] if b == '8.3' else []):
        print(' ', v, find(v))

print('\n== Measure 4: W3Techs details pages, share within minor at or above fix ==')
for p in sorted(D.glob('read-*/w3techs-details-8.2.derived.json')):
    line = []
    for b, fx in FIX.items():
        e = json.loads((p.parent / f'w3techs-details-{b}.derived.json').read_text())['extracted']
        dg = [x for x in e['diagrams'] if 'subversions' in x['caption']][0]
        tot = 0.0
        for lab, val in dg['rows']:
            m = re.fullmatch(rf'Version {re.escape(b)}\.(\d+)', lab)
            if m and int(m.group(1)) >= fx:
                tot += 0.0 if 'less' in val.lower() or val.startswith('<') else float(val.rstrip('%'))
        line.append(f'{b} {round(tot,1)} ({dg["date"]})')
    print(p.parent.name, '; '.join(line))
print('monthly (day-30 history pages):')
for b, fx in FIX.items():
    h = json.loads((D / f'read-2026-11-21T1414Z/w3techs-history_details-{b}.derived.json').read_text())['extracted']['history']
    for col in ('1 Oct 2026', '1 Nov 2026'):
        cells = {lab: v[col] for lab, v in h['rows'] if re.fullmatch(rf'version {re.escape(b)}\.(\d+)', lab)
                 and int(lab.split('.')[-1]) >= fx and v.get(col)}
        print(' ', b, col, cells, round(sum(0 if c.startswith('<') else float(c.rstrip('%')) for c in cells.values()), 1) if cells else 'not listed')

print('\n== Measure 5: Packagist, September 2026 ==')
pk = json.load(open(D / 'read-2026-10-25T0855Z/packagist.json'))['monthly']
i = pk['labels'].index('2026-09')
tot = sum(v[i] for v in pk['values'].values())
old = sum(v[i] for k, v in pk['values'].items() if tuple(map(int, k.split('.'))) <= (8, 1))
print(f'{old:,} of {tot:,} = {pct(old/tot)}%')

print('\n== Python comparators, recomputed from LH011 release_days.csv and LH008 lags.csv ==')
fixes = {('urllib3', '2.7.0'), ('cryptography', '48.0.1'), ('pyjwt', '2.13.0'), ('starlette', '1.1.0')}
rows = [r for r in csv.DictReader(open(R / 'studies/LH011/data/analysis/release_days.csv')) if r['status'] == 'known']
for d in (1, 2, 7, 14, 30):
    f = {p: float(r['share_at_or_newer']) for r in rows if int(r['day']) == d for p in [(r['project'], r['version'])] if p in fixes}
    byproj = {}
    for r in rows:
        if int(r['day']) == d: byproj.setdefault(r['project'], []).append(float(r['share_at_or_newer']))
    med = st.median(st.median(v) for v in byproj.values())
    print(f'day {d}: fixes {len(f)} range {pct(min(f.values()))} to {pct(max(f.values()))}; median of {len(byproj)} project medians {pct(med)}')
    php = [sh[b][d] for b in FIX]
    print(f'   PHP range {pct(min(php))} to {pct(max(php))}; all PHP below all fixes: {max(php) < min(f.values())}; all above: {min(php) > max(f.values())}')
l8 = [r for r in csv.DictReader(open(R / 'studies/LH008/data/lags.csv')) if r['frame'].endswith(':fix')]
mv = lambda d: sum(1 for r in l8 if r['outcome'] == 'moved' and r['lag_release_days'] and float(r['lag_release_days']) <= d)
print('LH008 fix pairs', len(l8), 'moved within 7', mv(7), 'within 30', mv(30),
      'negative lags', sum(1 for r in l8 if r['lag_release_days'] and float(r['lag_release_days']) < 0))

print('\n== Amendment 2 ==')
S = lambda s, ds: sum(s[n] for n in ds) / len(ds)
Lp = {}
for b in FIX:
    s7, s30 = S(sh[b], (5, 6, 7)), S(sh[b], (28, 29, 30)); Lp[b] = (s30 - s7) / s30
    print(f'PHP {b}: S7 {pct(s7)} S30 {pct(s30)} L {round(Lp[b],4)} rise23-30 {pct(sh[b][30]-sh[b][23])}')
nt = json.load(open(R / 'studies/LH034/data/tables.json'))
S30n = {}
for rule, key in (('as written', 'measure_1_2026-10'), ('amended', 'measure_1_2026-10_amended_unlisted_above')):
    blk = nt[key]; print(rule, 'day0', blk['day0'])
    Ln = {}; S30n[rule] = {}
    for ln, ser in blk['by_line'].items():
        x = {int(n): v['at_or_newer'] / v['line_downloads'] for n, v in ser.items()}
        reads_used = sorted({ser[str(n)]['read'] for n in (5, 6, 7, 28, 29, 30)})
        s7, s30 = S(x, (5, 6, 7)), S(x, (28, 29, 30)); Ln[ln] = (s30 - s7) / s30; S30n[rule][ln] = s30
        print(f'  Node {ln}: S7 {pct(s7)} S30 {pct(s30)} L {round(Ln[ln],4)} reads {reads_used}')
    mp, mn = st.median(Lp.values()), st.median(Ln.values())
    print(f'  Test A: PHP median L {round(mp,4)} > Node median L {round(mn,4)}: {mp > mn}')
    low = min(S30n[rule]['24'], S30n[rule]['26'])
    print(f'  Test B Node: lower of 24/26 {pct(low)} minus 22 {pct(S30n[rule]["22"])} = {pct(low - S30n[rule]["22"])} pts; >5: {low - S30n[rule]["22"] > 0.05}')
s30p = {b: S(sh[b], (28, 29, 30)) for b in FIX}
gap = min(s30p['8.4'], s30p['8.5']) - max(s30p['8.2'], s30p['8.3'])
print(f'Test A rise part: branches up >=1pt d23-30: {sum(sh[b][30]-sh[b][23] >= 0.01 for b in FIX)}')
print(f'Test B PHP: gap {pct(gap)} pts (>5: {gap > 0.05})')

print('\n== Fixed-version boundary in each read (top_versions, top 20 rows only) ==')
for rd in reads:
    s = json.load(gzip.open(rd / 'censys.raw.gz'))['snapshot']
    lo = {}
    for r in s['top_versions']:
        b = '.'.join(r['version'].split('.')[:2])
        if b in FIX and r['status'] == 'patched':
            lo[b] = min(lo.get(b, 99), int(r['version'].split('.')[2]))
    print(rd.name, 'lowest patched patch number per branch', dict(sorted(lo.items())))

print('\n== Per-branch status in the day-30 snapshot (branches): is "unknown" inside measure 1\'s denominator? ==')
for b in FIX:
    st_ = {r['status']: r['targets'] for r in snap30['branches'] if r['branch'] == b}
    print(b, st_, 'affected+patched', st_.get('affected', 0) + st_.get('patched', 0), 'd30 bar', bh[(b, 30)][1])
