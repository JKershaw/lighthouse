"""R-0132 recheck (24 Nov 2026), written independently of r0130_check.py and resolution_check.py.
Offline; reads retained bodies only. Reproduces the post hoc day-0 inference of LH049 1.1.
Model: at read r, npm tables 13.3.0 fetches per day as c_r(d); package daily totals P_r(d).
Premise (clock rule's own): in a balanced read, sum over versions of per-version counts equals the
package total for the same window, and the per-version table covers the same fetches.
Question 1: which splits (c(9),c(10),c(11),c(12)) of the 202 in W(12 Nov) are compatible with W(16 Nov)?
Question 2: what the reads cannot exclude (drops before the first read holding a day)."""
import gzip, json, glob, os, itertools
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
def load(r, n): return json.loads(gzip.open(os.path.join(r, n + '.raw.gz')).read())
R = {}
for r in sorted(glob.glob(os.path.join(base, 'read-*'))):
    v = load(r, 'versions')['downloads']; p = load(r, 'point_before')
    d = {x['day']: x['downloads'] for x in load(r, 'range')['downloads']}
    R[p['end']] = dict(lab=os.path.basename(r), v=v, p=p, d=d, bal=sum(v.values()) == p['downloads'])
w12, w16 = R['2026-11-12'], R['2026-11-16']
print('W(12):', w12['lab'], w12['p']['start'], w12['p']['end'], 'balanced', w12['bal'], '13.3.0', w12['v'].get('13.3.0'))
print('W(16):', w16['lab'], w16['p']['start'], w16['p']['end'], 'balanced', w16['bal'], '13.3.0', w16['v'].get('13.3.0', 'absent'),
      'sum', sum(w16['v'].values()), 'point', w16['p']['downloads'])
days = ['2026-11-%02d' % i for i in range(10, 13)]
stable = all(w12['d'][x] == w16['d'][x] for x in days)
print('package totals 10..12 Nov at W(12) read vs W(16) read:', [(x[-2:], w12['d'][x], w16['d'][x]) for x in days], 'unchanged', stable)
# Enumerate splits (coarse step 1 on x = c(10)+c(11)+c(12)); c(9) = 202 - x.
# At W(16) read, under the premise with no re-attribution, 13.3.0 fetches on 10..16 as tabled = 0 (absent key, balanced).
# Fetches counted at the W(12) read on 10..12 can leave 13.3.0's key by 17 Nov only by (a) removal from both tables,
# which would lower the package totals for 10..12, or (b) moving to another key with totals unchanged.
ok_no_move = [x for x in range(0, 203) if (x == 0) or (not stable)]
print('x = fetches of the 202 on 10..12 compatible without re-attribution:', ok_no_move, '-> d(9) =', [202 - x for x in ok_no_move])
print('share of package 9 Nov:', round(202 / R['2026-11-09']['d']['2026-11-09'], 4) if '2026-11-09' in R['2026-11-09']['d'] else None)
# Question 2: illustrate the limit. A fetch on day t dropped from both tables before the first read holding t
# leaves every retained body identical; this holds for each of 10..16 Nov and 17..23 Nov alike.
first = {}
for end in sorted(R):
    for day in R[end]['d']:
        if R[end]['lab'][5:15] != day: first.setdefault(day, R[end]['lab'][5:])
print('first read holding each day (a drop before it is invisible):', {k[-5:]: v for k, v in sorted(first.items()) if '2026-11-10' <= k <= '2026-11-23'})
print('Conclusion (post hoc): under the premise, d(9 Nov) = 202 counted fetches unless re-attribution to another key with',
      'totals unchanged; the check does not exclude, for any day 10..23 Nov, fetches dropped from both tables before first tabled.')
