"""R-0141: reproduce the PHP figures new or changed in the essay's 1.1 draft
directly from the retained Censys bodies (not from record_v1.json), then
compare with LH033's record_v1.json. Run from the repository root:
python3 -I studies/LH033/review/essay-rev-2026-11-25/repro_php.py"""
import gzip, json, os, datetime, statistics
D = 'studies/LH033/data'
reads = sorted(r for r in os.listdir(D) if r.startswith('read-'))
bh, hist = {}, {}
for r in reads:  # earliest read holding each completed day
    p = os.path.join(D, r, 'censys.raw.gz')
    if not os.path.exists(p):
        continue
    s = json.loads(gzip.open(p).read())['snapshot']
    rdate = r[5:15]  # a day counts only once complete, i.e. before the read's UTC date
    for row in s.get('branch_history', []):
        if row['day'] >= rdate:
            continue
        bh.setdefault((row['day'], row['branch']), (row['patched'], row['targets']))
    for row in s.get('history', []):
        if row['day'] >= rdate:
            continue
        hist.setdefault((row['day'], row['status']), row['targets'])
day0 = datetime.date(2026, 10, 21)
def d(n): return (day0 + datetime.timedelta(n)).isoformat()
B = ['8.2', '8.3', '8.4', '8.5']
share = lambda n, b: 100 * bh[(d(n), b)][0] / bh[(d(n), b)][1]
print('Day-30 patched shares:', {b: round(share(30, b), 1) for b in B})
print('Day 7 -> 14 patched count rise:', {b: bh[(d(14), b)][0] - bh[(d(7), b)][0] for b in B})
print('Day 14 -> 30 patched rise / branch change:', {b: (bh[(d(30), b)][0] - bh[(d(14), b)][0], bh[(d(30), b)][1] - bh[(d(14), b)][1]) for b in B})
print('Share rise day 23 -> 30 (points):', {b: round(share(30, b) - share(23, b), 1) for b in B})
print('Patched count rise day 23 -> 30 as points of day-23 branch:', {b: round(100 * (bh[(d(30), b)][0] - bh[(d(23), b)][0]) / bh[(d(23), b)][1], 1) for b in B})
def tail(n):
    st = {k: hist[(d(n), k)] for k in ['patched', 'affected', 'affected_nofix', 'unknown']}
    versioned = st['patched'] + st['affected'] + st['affected_nofix']
    allt = versioned + st['unknown']
    return st['affected_nofix'], versioned, allt, st['unknown']
for n in (7, 30):
    nf, v, a, u = tail(n)
    print(f'Day {n}: unfixed {nf:,} of {v:,} versioned = {100*nf/v:.1f}%; no version {100*u/a:.2f}% of {a:,}; reporting {100*(a-u)/a:.1f}%')
# 28 October total and unknown share as in that day's earliest read's tables.json
t = json.load(open(os.path.join(D, 'read-2026-10-29T0635Z', 'tables.json')))
print('tables.json keys (read 29 Oct):', list(t)[:12])
# 8.3.8 in the 21 November snapshot
s = json.loads(gzip.open(os.path.join(D, 'read-2026-11-21T1414Z', 'censys.raw.gz')).read())['snapshot']
v83 = [r for r in s['branch_versions'] if r['branch'] == '8.3']
tot = sum(r['targets'] for r in v83)
x = sum(r['targets'] for r in v83 if r['version'] == '8.3.8')
print(f'8.3.8: {x:,} of {tot:,} 8.3 rows = {100*x/tot:.1f}%')
# Test A / B, PHP side
S = lambda b, a, z: statistics.mean(share(n, b) for n in range(a, z + 1))
L = {b: (S(b, 28, 30) - S(b, 5, 7)) / S(b, 28, 30) for b in B}
print('S30:', {b: round(S(b, 28, 30), 2) for b in B}, 'L:', {b: round(L[b], 4) for b in B}, 'median L', round(statistics.median(L.values()), 4))
print('Test B PHP gap:', round(min(S('8.4', 28, 30), S('8.5', 28, 30)) - max(S('8.2', 28, 30), S('8.3', 28, 30)), 2))
rec = json.load(open(os.path.join(D, 'record_v1.json')))
print('record amendment2 (excerpt):', json.dumps(rec['amendment2'])[:600])
