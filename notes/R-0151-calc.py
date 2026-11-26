#!/usr/bin/env python3
"""R-0151: independent reproduction of LH051 record 1.0 measures 2 to 7 from the retained CSVs.

Written by the evidence reviewer of 26 November 2026, without reusing studies/LH051/scripts/tabulate.py.
Reads only studies/LH051/data/hours.csv and studies/LH051/data/counts.csv (aggregate counts, no identifier);
fetches nothing. The gap flag is recomputed from the per-file Push/Create/Delete totals and checked against the
collector's own gap_hour column. Replay from the repository root:

    python3 -I notes/R-0151-calc.py > notes/R-0151-calc-output.txt
"""
import csv
import hashlib
import statistics
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'studies' / 'LH051' / 'data'


def key(h):
    d, hh = h.rsplit('-', 1)
    return datetime.strptime(d, '%Y-%m-%d') + timedelta(hours=int(hh))


def name(t):
    return f'{t:%Y-%m-%d}-{t.hour}'


def hours_between(a, b):
    t, out = key(a), []
    while t <= key(b):
        out.append(name(t))
        t += timedelta(hours=1)
    return out


for f in ('hours.csv', 'counts.csv'):
    print(f'sha256 {f}: {hashlib.sha256((D / f).read_bytes()).hexdigest()}')

rows = list(csv.DictReader(open(D / 'hours.csv', newline='')))
held = {}
for r in rows:
    if r['http_status'] == '200' and r['gzip_ok'] == '1':
        held[r['hour']] = r
first, last = '2026-11-09-0', max(held, key=key)
rng = hours_between(first, last)
print(f'range {first}..{last}: {len(rng)} hours; held {len(held)}; rows {len(rows)}; '
      f'missing {[h for h in rng if h not in held]}')
print(f'json errors >0: {sum(1 for r in rows if r["json_errors"] not in ("", "0"))}')
gap = {h: all(int(held[h][t]) == 0 for t in ('PushEvent', 'CreateEvent', 'DeleteEvent')) for h in held}
mism = [h for h in held if gap[h] != (held[h]['gap_hour'] == '1')]
print(f'gap hours (recomputed): {sum(gap.values())}; disagreements with collector flag: {mism}')
byread = defaultdict(int)
for h in held:
    byread[held[h]['read']] += 1
print('hours by read:', dict(sorted(byread.items())))
print('bytes total:', sum(int(held[h]['bytes']) for h in held))
pr = {h: int(held[h]['PullRequestEvent']) for h in held}
mn = min(pr, key=pr.get)
print(f'PullRequestEvent per hour: min {pr[mn]} at {mn}; max {max(pr.values())}; '
      f'min within first 181 hours {min(pr[h] for h in hours_between(first, "2026-11-16-12"))}')
# runs of gap hours
runs, cur = [], None
for h in rng:
    if gap[h]:
        cur = [h, h] if cur is None else [cur[0], h]
    elif cur:
        runs.append(cur)
        cur = None
if cur:
    runs.append(cur)
longest = max(runs, key=lambda r: len(hours_between(*r)))
print(f'gap runs: {len(runs)}; longest {longest[0]}..{longest[1]} ({len(hours_between(*longest))} hours)')

# counts: cell lookup; None = unknown
cells = defaultdict(int)
for r in csv.DictReader(open(D / 'counts.csv', newline='')):
    assert r['hour'] in held, r['hour']
    cells[(r['hour'], r['marker'], r['event_type'], r['action'])] += int(r['events'])
    if r['marker'] == 'M1' and r['event_type'] == 'PullRequestEvent' and r['action'] == 'opened':
        assert r['distinct_repos'] == r['events'], r['hour']
print('check: every M1 opened cell has distinct_repos == events: ok')
UNK = ('PushEvent', 'CreateEvent', 'DeleteEvent')


def c(h, m, t, a=None):
    if t in UNK and gap[h]:
        return None
    return sum(v for (hh, mm, tt, aa), v in cells.items() if hh == h and mm == m and tt == t and (a is None or aa == a))


def tot(m, t, a=None, hs=None):
    return sum(v for (hh, mm, tt, aa), v in cells.items()
               if mm == m and tt == t and (a is None or aa == a) and (hs is None or hh in hs))


print('\n== M1 totals over all held hours (counts.csv rows; Push/Create/Delete rows exist only in non-gap hours)')
for t, a in [('PullRequestEvent', 'opened'), ('PullRequestEvent', 'closed'), ('PullRequestEvent', 'reopened'),
             ('PullRequestEvent', 'other'), ('PullRequestReviewEvent', 'created'),
             ('PullRequestReviewEvent', 'updated'), ('CreateEvent', None), ('DeleteEvent', None), ('PushEvent', None)]:
    print(f'  {t} {a or "all"}: {tot("M1", t, a)}')
assert all(not gap[hh] for (hh, mm, tt, aa) in cells if tt in UNK), 'a Push/Create/Delete row in a gap hour'
rv = sorted({hh for (hh, mm, tt, aa) in cells if mm == 'M1' and tt == 'PullRequestReviewEvent'}, key=key)
print(f'  M1 review hours: {rv[0]}..{rv[-1]}')
op = {h: c(h, 'M1', 'PullRequestEvent', 'opened') for h in rng}
ophs = [h for h in rng if op[h]]
print(f'  M1 opened hours: {ophs[0]}..{ophs[-1]}; top two {sorted(op.items(), key=lambda x: -x[1])[:2]}')
late = defaultdict(lambda: defaultdict(int))
for (hh, mm, tt, aa), v in cells.items():
    if mm == 'M1' and key(hh) >= key('2026-11-13-0'):
        late[hh[:10]][f'{tt} {aa}'.strip()] += v
print('  M1 by day from 13 November:', {d: dict(x) for d, x in sorted(late.items())})

print('\n== Measure 2: onset')
onset = next(h for h in rng if any(v for (hh, mm, tt, aa), v in cells.items() if hh == h and mm == 'M1'))
print(f'  onset {onset}; M1 events in it {sum(v for (hh, mm, tt, aa), v in cells.items() if hh == onset and mm == "M1")}')
vs = '2026-11-10-12'
print(f'  vendor start hour {vs}: held {vs in held}; gap {gap[vs]}; M1 PR {c(vs, "M1", "PullRequestEvent")}; '
      f'M1 RV {c(vs, "M1", "PullRequestReviewEvent")}')
before = hours_between(first, name(key(onset) - timedelta(hours=1)))
print(f'  hours before onset {len(before)}; gap among them {sum(gap[h] for h in before)}')

print('\n== Measure 3: probe coverage')
for v, a, b, n, more in (('Aikido E4', '2026-11-10-12', '2026-11-11-14', 61839, False),
                         ('StepSecurity E1', '2026-11-10-0', '2026-11-12-7', 63000, True)):
    hs = hours_between(a, b)
    s = sum(op[h] for h in hs)
    sh = 100 * s / n
    reading = 'most' if sh >= 50 else 'a minority' if sh >= 10 else 'a small fraction'
    print(f'  {v}: {a}..{b} {len(hs)} hours, held {sum(h in held for h in hs)}, gap {sum(gap[h] for h in hs)}; '
          f'opened {s}; /{n} = {sh:.4f}% {"(upper estimate)" if more else ""} -> {reading}; '
          f'in non-gap hours {sum(op[h] for h in hs if not gap[h])}')

print('\n== Measure 4: internal completeness, onset..2026-11-12-23')
hs = hours_between(onset, '2026-11-12-23')
ng = [h for h in hs if not gap[h]]
print(f'  hours {len(hs)}; non-gap {len(ng)}: {ng}')
print(f'  per non-gap hour (create, opened): {[(h, c(h, "M1", "CreateEvent"), op[h]) for h in ng if c(h, "M1", "CreateEvent") or op[h]]}')
print(f'  sums: create {sum(c(h, "M1", "CreateEvent") for h in ng)}; opened {sum(op[h] for h in ng)}; '
      f'opened in gap hours {sum(op[h] for h in hs if gap[h])} ({len(hs) - len(ng)} gap hours)')

print('\n== Measure 5: cleanup by UTC day (complete days only)')
co = cc = 0
day = key('2026-11-10-0')
gaps_10_25 = 0
while day <= key(last):
    hs = hours_between(name(day), name(day + timedelta(hours=23)))
    hh = [h for h in hs if h in held]
    o = sum(op[h] for h in hh)
    cl = sum(c(h, 'M1', 'PullRequestEvent', 'closed') for h in hh)
    ro = sum(c(h, 'M1', 'PullRequestEvent', 'reopened') for h in hh)
    ot = sum(c(h, 'M1', 'PullRequestEvent', 'other') for h in hh)
    de = sum(c(h, 'M1', 'DeleteEvent') for h in hh if not gap[h])
    g = sum(gap[h] for h in hh)
    if len(hh) == 24:
        co += o
        cc += cl
        gaps_10_25 += g
        print(f'  {day:%d %b} held {len(hh)} gap {g:>2} opened {o:>3} closed {cl} reopened {ro} other {ot} '
              f'delete {de} cum {cc}/{co} = {100 * cc / co:.2f}%')
    else:
        print(f'  {day:%d %b} incomplete: held {len(hh)} gap {g}; opened {o} closed {cl} other {ot} delete {de}')
    day += timedelta(days=1)
print(f'  complete days 10..25 Nov: hours {16 * 24}, gap {gaps_10_25}; M1 deletions total {tot("M1", "DeleteEvent")}')
print(f'  vendors: 100-90 = 10%; 100-92 = 8% no longer open by their searches')

print('\n== Measure 6: M2 and M3 by type, baseline vs after (unknown hours left out)')
periods = (('baseline', hours_between(first, '2026-11-10-11')), ('after', hours_between('2026-11-10-12', last)))
for m in ('M2', 'M3'):
    for t in ('PullRequestEvent', 'PullRequestReviewEvent', 'CreateEvent', 'DeleteEvent', 'PushEvent'):
        parts = []
        for p, hs in periods:
            vals = [x for x in (c(h, m, t) for h in hs) if x is not None]
            parts.append(f'{p}: known {len(vals)}, total {sum(vals)}, median {statistics.median(vals):g}, '
                         f'range {min(vals)}..{max(vals)}')
        print(f'  {m} {t}: ' + '; '.join(parts))
burst = hours_between('2026-11-12-2', '2026-11-12-5')
for t in ('CreateEvent', 'DeleteEvent', 'PushEvent'):
    print(f'  M2 {t} in 12 Nov 02:00-05:59: {tot("M2", t, hs=set(burst))} of {tot("M2", t)}')

print('\n== Measure 7: M1 PullRequestEvent in gap and other hours from onset')
for a, b in ((onset, last), (onset, '2026-11-12-23'), ('2026-11-13-0', last)):
    hs = hours_between(a, b)
    for lab, sel in (('gap', [h for h in hs if gap[h]]), ('other', [h for h in hs if not gap[h]])):
        by = {x: sum(c(h, 'M1', 'PullRequestEvent', x) for h in sel) for x in ('opened', 'closed', 'reopened', 'other')}
        print(f'  {a}..{b} {lab}: {len(sel)} hours, M1 PR {sum(by.values())} {by}')

print('\n== Since the checkpoint (hours 2026-11-16-13..last)')
new = hours_between('2026-11-16-13', last)
print(f'  hours {len(new)}, gap {sum(gap[h] for h in new)}')
d = defaultdict(int)
for (hh, mm, tt, aa), v in cells.items():
    if mm == 'M1' and hh in set(new):
        d[f'{tt} {aa}'.strip()] += v
print('  M1 in them:', dict(d))
