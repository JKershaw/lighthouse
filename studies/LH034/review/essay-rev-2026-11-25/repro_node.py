"""R-0141: reproduce the Node.js figures new or changed in the essay's 1.1 draft
from the retained daily summaries and the derived 5 November release list
(not from record_v1.json), then compare with LH034's record_v1.json.
Run from the repository root:
python3 -I studies/LH034/review/essay-rev-2026-11-25/repro_node.py"""
import gzip, json, os, re, datetime, statistics
D = 'studies/LH034/data'
reads = sorted(r for r in os.listdir(D) if r.startswith('read-'))
days = {}
for r in reads:  # earliest read holding each day file
    for f in sorted(os.listdir(os.path.join(D, r))):
        m = re.match(r'day-(\d{8})\.raw\.gz$', f)
        if m and m.group(1) not in days:
            days[m.group(1)] = json.loads(gzip.open(os.path.join(D, r, f)).read())
rel = json.load(open(os.path.join(D, 'read-2026-11-05T1414Z', 'dist-index.derived.json')))['extracted']['releases']
listed = {v for v, _, _ in rel}
FIX = {'22': (22, 23, 4), '24': (24, 22, 1), '26': (26, 12, 1)}
def parse(v):
    m = re.match(r'^v(\d+)\.(\d+)\.(\d+)$', v)
    return tuple(map(int, m.groups())) if m else None
day0 = datetime.date(2026, 10, 21)
def key(n): return (day0 + datetime.timedelta(n)).strftime('%Y%m%d')
def unfixed(n):
    vs = days[key(n)]['version']
    att = sum(c for v, c in vs.items() if v != 'unknown')
    out = sum(c for v, c in vs.items() if v != 'unknown' and v.lstrip('v').split('.')[0] not in FIX)
    return 100 * out / att
def share(n, line, amended):
    vs = days[key(n)]['version']; fx = FIX[line]; num = den = 0
    for v, c in vs.items():
        if not v.startswith('v' + line + '.'):
            continue
        p = parse(v)
        if v in listed:
            den += c; num += c if (p and p >= fx) else 0
        elif amended and p and p > fx:
            den += c; num += c
    return 100 * num / den
u = [round(unfixed(n), 1) for n in range(-7, 8)]
print('Unfixed share days -7..7:', u, 'range', min(u), max(u))
print('Unfixed share day 30:', round(unfixed(30), 1))
we, wd = [], []
for n in range(0, 31):
    dt = day0 + datetime.timedelta(n); t = days[key(n)]['total']
    (we if dt.weekday() >= 5 else wd).append(t)
print('Days 0-30 weekend range (M):', round(min(we)/1e6, 1), round(max(we)/1e6, 1), ' weekday range (M):', round(min(wd)/1e6, 1), round(max(wd)/1e6, 1))
allwe = [d['total'] for k, d in days.items() if k >= '20260923' and datetime.datetime.strptime(k, '%Y%m%d').weekday() >= 5]
allwd = [d['total'] for k, d in days.items() if k >= '20260923' and datetime.datetime.strptime(k, '%Y%m%d').weekday() < 5]
print('23 Sep to 20 Nov: max weekend', max(allwe), 'min weekday', min(allwd), 'every weekend below every weekday:', max(allwe) < min(allwd))
for amended in (True, False):
    lab = 'amended' if amended else 'as written'
    d30 = {l: round(share(30, l, amended), 1) for l in FIX}
    S7 = {l: statistics.mean(share(n, l, amended) for n in (5, 6, 7)) for l in FIX}
    S30 = {l: statistics.mean(share(n, l, amended) for n in (28, 29, 30)) for l in FIX}
    L = {l: (S30[l] - S7[l]) / S30[l] for l in FIX}
    print(f'{lab}: day 30 {d30}; S30 {dict((l, round(S30[l], 2)) for l in FIX)}; L {dict((l, round(L[l], 3)) for l in FIX)}; median L {round(statistics.median(L.values()), 3)}; test B gap {round(min(S30["24"], S30["26"]) - S30["22"], 2)}')
rec = json.load(open(os.path.join(D, 'record_v1.json')))
print('record measure_2.summary day30_unfixed_pct, weekend, weekday:', rec['measure_2']['summary']['day30_unfixed_pct'], rec['measure_2']['summary']['weekend_totals_days_0_to_30_millions'], rec['measure_2']['summary']['weekday_totals_days_0_to_30_millions'])
# Unrounded extremes behind the Correction notice's "rounds to 12 to 17"
ur = [(n, unfixed(n)) for n in range(-7, 8)]
lo, hi = min(ur, key=lambda x: x[1]), max(ur, key=lambda x: x[1])
print(f'Unrounded unfixed share days -7..7: min {lo[1]:.3f} (day {lo[0]}), max {hi[1]:.3f} (day {hi[0]}); whole numbers {round(lo[1])} to {round(hi[1])}')
