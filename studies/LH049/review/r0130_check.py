"""R-0130 reader-review check (24 Nov 2026). Offline; reads retained bodies only.
1. Where the +210 per-version excess sits (which version keys).
2. Whether package daily totals for 10-16 Nov were stable across reads.
3. The implication of a balanced W(16 Nov) with no 13.3.0 key for d(10..12) and so d(9)."""
import gzip, json, glob, os, sys
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
reads = sorted(glob.glob(os.path.join(base, 'read-*')))
def load(r, n): return json.loads(gzip.open(os.path.join(r, n + '.raw.gz')).read())
V, P, D = {}, {}, {}
for r in reads:
    lab = os.path.basename(r)[5:]
    V[lab] = load(r, 'versions')['downloads']
    p = load(r, 'point_before'); P[lab] = (p['start'], p['end'], p['downloads'])
    D[lab] = {x['day']: x['downloads'] for x in load(r, 'range')['downloads']}
labs = list(V)
print('1. per-version change between consecutive daily reads, versions whose change differs from 13.3.0 pattern')
for a, b in zip(labs, labs[1:8]):
    va, vb = V[a], V[b]
    # window shift: W(b) - W(a) = day_new - day_dropped per version
    dp = P[b][2] - P[a][2]
    dv = sum(vb.values()) - sum(va.values())
    big = sorted(((vb.get(k, 0) - va.get(k, 0), k) for k in set(va) | set(vb)), key=lambda t: abs(t[0]), reverse=True)[:4]
    print(f'  {a}->{b}: point change {dp:+d}, per-version sum change {dv:+d}, gap change {dv-dp:+d}; largest key changes {big}')
print('2. package daily totals for 9-16 Nov at each read that held them')
for day in ['2026-11-%02d' % i for i in range(9, 17)]:
    vals = [(l[:10], D[l][day]) for l in labs if day in D[l] and l[:10] != day]
    print(f'  {day}: {sorted(set(v for _, v in vals))} over {len(vals)} reads')
w16 = '2026-11-17T1415Z'
print('3. W(16 Nov):', P[w16], 'per-version sum', sum(V[w16].values()), '13.3.0 key present:', '13.3.0' in V[w16])
s = sum(D[w16]['2026-11-%02d' % i] for i in range(10, 17))
print('   package daily totals 10..16 summed at that read', s)
print('   W(12 Nov) 13.3.0 =', V['2026-11-13T1452Z'].get('13.3.0'), '= d9+d10+d11+d12')
print('   If per-version and package tables count the same fetches in a balanced window (the clock rule\'s premise),')
print('   13.3.0 has 0 counted fetches in 10..16 Nov as tabled at 17 Nov; days 10..15 had the same package totals at')
print('   every earlier read, so no counted fetch was later removed from them; hence d10=d11=d12=0 and d9=202,')
print('   unless npm re-attributed 13.3.0 fetches to another version key without changing any total. (post hoc)')
