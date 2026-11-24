"""Resolution of R-0130 (24 Nov 2026), by the driving session's subagent. Offline; reads retained bodies only.
Extends r0130_check.py: states each premise of the post hoc d(9 Nov) argument and checks it against the reads.
A. Each read's stated window, balance (per-version sum == point total), 13.3.0 value.
B. For days 10..16, the package daily total at every read holding it, and the first read holding it.
C. The argument, step by step, with which reads each step rests on. (post hoc; outside the protocol)"""
import gzip, json, glob, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
reads = sorted(glob.glob(os.path.join(base, 'read-*')))
def load(r, n): return json.loads(gzip.open(os.path.join(r, n + '.raw.gz')).read())
rows = []
for r in reads:
    lab = os.path.basename(r)[5:]
    v = load(r, 'versions')['downloads']; pb = load(r, 'point_before'); pa = load(r, 'point_after')
    d = {x['day']: x['downloads'] for x in load(r, 'range')['downloads']}
    rows.append((lab, pb, pa, v, d))
print('A. read | window | point before/after agree | per-version sum | point | balanced | 13.3.0')
for lab, pb, pa, v, d in rows:
    agree = (pb['start'], pb['end'], pb['downloads']) == (pa['start'], pa['end'], pa['downloads'])
    s = sum(v.values())
    print(f'  {lab} | {pb["start"]}..{pb["end"]} | {agree} | {s} | {pb["downloads"]} | {s == pb["downloads"]} | {v.get("13.3.0", "no key")}')
print('B. package daily totals, days 10..16 Nov, at each read holding the day (own-date answers set aside)')
for i in range(10, 17):
    day = '2026-11-%02d' % i
    held = [(lab, d[day]) for lab, pb, pa, v, d in rows if day in d and lab[:10] != day]
    print(f'  {day}: first held at {held[0][0]}; values {sorted(set(x for _, x in held))} over {len(held)} reads')
byend = {pb['end']: (lab, v, pb, sum(v.values()) == pb['downloads']) for lab, pb, pa, v, d in rows}
l12, v12, p12, b12 = byend['2026-11-12']; l16, v16, p16, b16 = byend['2026-11-16']
print('C. the post hoc argument')
print(f'  1. W(12 Nov) = 6..12 Nov, read {l12}, balanced {b12}, 13.3.0 = {v12.get("13.3.0")}: d9+d10+d11+d12 = 202 as tabled then.')
print(f'  2. W(16 Nov) = 10..16 Nov, read {l16}, balanced {b16}, 13.3.0 key present {"13.3.0" in v16}:')
print('     premise: in a balanced window the per-version table covers the same fetches as the package totals (the clock rule\'s premise);')
print('     so as tabled at 17 Nov, npm attributes no fetch on 10..16 Nov to 13.3.0.')
print('  3. Days 10..12 Nov had the same package totals at 17 Nov as at 13 Nov (B), so no counted fetch was removed from them between.')
print('  4. If x of the 202 at step 1 fell on 10..12 Nov, by 17 Nov those x are still in the package totals (3) but not on 13.3.0 (2),')
print('     and W(16) still balances, so they would have to sit under another version key: re-attribution with every total unchanged.')
print('  5. Otherwise x = 0, so d10 = d11 = d12 = 0 and d9 = 202 (d13..d15 = 0 already, from held windows under the brief).')
print('  6. Days 16 Nov and 17..23 Nov: no read before their first holding read existed, so a fetch npm dropped from both tables')
print('     before that read leaves no trace; for these days the two explanations of an absent key stay apart only by post hoc reading.')
print('  Scope: the argument concerns fetches npm counted; it says nothing of requests npm never counted.')
