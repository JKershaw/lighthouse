"""R-0138: independent reproduction of the PHP figures the revised week-one piece uses,
from LH033's retained Censys bodies. Written fresh for this review. Run: python3 -I <this file>"""
import gzip, json
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
D = Path('studies/LH033/data')
def snap(read):
    return json.loads(gzip.decompress((D / read / 'censys.raw.gz').read_bytes()))['snapshot']
S = snap('read-2026-11-21T1414Z')
D0 = date(2026, 10, 21)
bh = {(r['day'], r['branch']): (r['patched'], r['targets']) for r in S['branch_history']}
day = lambda n: str(D0 + timedelta(n))
B = ['8.2', '8.3', '8.4', '8.5']
print('== patched share by branch')
for n in [1, 2, 7, 14, 30]:
    print(n, ' '.join(f'{b} {100*bh[(day(n),b)][0]/bh[(day(n),b)][1]:.1f}' for b in B))
print('first day at half:', {b: next(n for n in range(31) if bh[(day(n), b)][0] / bh[(day(n), b)][1] >= .5) for b in B})
older_below = all(max(bh[(day(n), b)][0]/bh[(day(n), b)][1] for b in B[:2]) < min(bh[(day(n), b)][0]/bh[(day(n), b)][1] for b in B[2:]) for n in range(1, 31))
print('older two below newer two every day 1..30:', older_below)
print('== counts')
for b in B:
    p7, t7 = bh[(day(7), b)]; p14, t14 = bh[(day(14), b)]; p30, t30 = bh[(day(30), b)]
    print(b, 'patched d7->14', p14 - p7, 'd14->30', p30 - p14, 'branch d14->30', t30 - t14)
print('== unfixed tail (affected_nofix over affected+affected_nofix+patched)')
h = defaultdict(dict)
for r in S['history']: h[r['day']][r['status']] = r['targets']
for n in [0, 7, 14, 30]:
    x = h[day(n)]; ver = x['affected'] + x['affected_nofix'] + x['patched']
    print(n, x['affected_nofix'], ver, f"{100*x['affected_nofix']/ver:.1f}%", 'no-version share of all', f"{100*x['unknown']/(ver+x['unknown']):.1f}%")
print('== 8.3.8 in branch_versions (snapshot)')
bv = defaultdict(int); tot83 = 0
for r in S['branch_versions']:
    if r['branch'] == '8.3':
        tot83 += r['targets']
        if r['version'] == '8.3.8': bv['8.3.8'] += r['targets']
print('8.3.8', bv['8.3.8'], 'of', tot83, f"{100*bv['8.3.8']/tot83:.1f}%")
print('== five or more behind, 8.2 and 8.3 (share of not-at-or-above)')
FIX = {'8.2': 35, '8.3': 36}
for b, fx in FIX.items():
    rows = [(r['version'], r['targets']) for r in S['branch_versions'] if r['branch'] == b]
    tot = sum(t for _, t in rows); below = five = 0
    for v, t in rows:
        try: p = int(v.split('.')[2])
        except Exception: continue
        if p < fx:
            below += t
            if fx - p >= 5: five += t
    print(b, f'below {100*below/tot:.1f}% five+ {100*five/tot:.1f}%  five+ as share of below {100*five/below:.0f}%')
print('== check day 7 against the earliest read holding it')
for rd in ['read-2026-10-29T0635Z', 'read-2026-10-30T0635Z']:
    E = snap(rd); e = {(r['day'], r['branch']): (r['patched'], r['targets']) for r in E['branch_history']}
    if (day(7), '8.3') in e: print(rd, all(e[(day(7), b)] == bh[(day(7), b)] for b in B))
