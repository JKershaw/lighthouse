#!/usr/bin/env python3
"""R-0015: the reviewer's own recomputation of the five readings made after the counts (record
version 0.3, Findings; data/post_hoc_reading.txt), written without reading scripts/post_hoc.py's
functions and using its own median and rounding. Reads only the retained tables:
data/analysis/release_days.csv, data/analysis/project_outcomes.csv, and LH008's data/events.csv and
data/lags.csv. Offline; standard library only.

    python3 studies/LH011/review/r0015_check.py > studies/LH011/review/r0015_check.txt

It also prints, for every project, the day-1 median as a share of the day-30 median, to test the
piece's sentence that for most of the eleven "the jump came as quickly" as for the rest, and the
rounded figures the piece and short form give (18, 47, 63, 98)."""
import csv, os
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
AN = os.path.join(STUDY, 'data', 'analysis')
LH008 = os.path.join(os.path.dirname(STUDY), 'LH008', 'data')


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def r1(x):  # one decimal, half up, as the record prints
    return Decimal(str(x * 100)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)


def r0(x):  # whole number, half up, as the piece prints
    return Decimal(str(x * 100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)


# --- tables ---
outcomes = {}
with open(os.path.join(AN, 'project_outcomes.csv')) as f:
    for r in csv.DictReader(f):
        if int(r['releases']) > 0:
            outcomes[r['project']] = r
assert len(outcomes) == 37, len(outcomes)

# share by (project, version, day); statuses seen
share = {}
statuses = defaultdict(int)
with open(os.path.join(AN, 'release_days.csv')) as f:
    for r in csv.DictReader(f):
        statuses[r['status']] += 1
        if r['status'] == 'known' and r['share_at_or_newer'] != '':
            share[(r['project'], r['version'], int(r['day']))] = float(r['share_at_or_newer'])
print('release_days.csv statuses:', dict(statuses))

by_pd = defaultdict(list)  # (project, day) -> shares over releases
for (p, v, d), s in share.items():
    by_pd[(p, d)].append(s)

print()
print('1. day-1 and day-30 medians over each project\'s releases, and the ten-point band')
print('project, group, n day 1, n day 30, day 1, day 30, difference, day1/day30')
within = 0
held = 0
rows = {}
for p in sorted(outcomes, key=lambda p: -median(by_pd[(p, 1)])):
    g = outcomes[p]['most_reached']
    d1 = median(by_pd[(p, 1)])
    d30 = median(by_pd[(p, 30)])
    rows[p] = (g, d1, d30)
    if d30 is not None:
        held += 1
        if abs(d30 - d1) <= 0.10:
            within += 1
    print(f'{p}, {g}, {len(by_pd[(p, 1)])}, {len(by_pd[(p, 30)])}, {r1(d1)}, '
          f'{r1(d30) if d30 is not None else "none"}, '
          f'{r1(d30 - d1) if d30 is not None else ""}, '
          f'{r0(d1 / d30) if d30 else ""} per cent')
print(f'within ten points: {within} of {held} projects with day 30 held')
print('outside:', [p for p, (g, d1, d30) in rows.items() if d30 is not None and abs(d30 - d1) > 0.10])

print()
print('2. one minus the day-30 median, by group')
for g in ('yes', 'no'):
    v = sorted((1 - d30, p) for p, (gg, d1, d30) in rows.items() if gg == g and d30 is not None)
    lo, hi = v[0], v[-1]
    print(f'{g}: {len(v)} projects; from {r1(lo[0])} ({lo[1]}) to {r1(hi[0])} ({hi[1]}); '
          f'median {r1(median([x for x, _ in v]))}; whole numbers {r0(lo[0])} to {r0(hi[0])}')

print()
print('3. day-1 median as a share of the day-30 median')
for g in ('no', 'yes'):
    v = sorted((d1 / d30, p) for p, (gg, d1, d30) in rows.items() if gg == g)
    print(f'{g}: ' + '; '.join(f'{p} {r0(x)}' for x, p in v))
    print(f'   range {r0(v[0][0])} to {r0(v[-1][0])} per cent; '
          f'between 70 and 107 inclusive: {sum(1 for x, _ in v if 0.695 <= x < 1.075)} of {len(v)}')

print()
print('4. widest gaps between neighbouring median day-1 shares in project_outcomes.csv')
s = sorted((float(r['median_day1_share']), p) for p, r in outcomes.items())
gaps = sorted(((b[0] - a[0], a[1], a[0], b[1], b[0]) for a, b in zip(s, s[1:])), reverse=True)
for gap, pa, a, pb, b in gaps[:3]:
    print(f'{r1(gap)} points: {pa} {r1(a)} to {pb} {r1(b)}')
print('the gap containing 0.5:', [(pa, r1(a), pb, r1(b)) for gap, pa, a, pb, b in gaps if a < 0.5 <= b])

print()
print('5. LH008\'s chosen fixes that are LH011 releases, and their pinned pairs')
with open(os.path.join(LH008, 'events.csv')) as f:
    events = [r for r in csv.DictReader(f) if r['chosen'] == 'yes']
with open(os.path.join(LH008, 'lags.csv')) as f:
    lags = list(csv.DictReader(f))
print('chosen events:', [(e['library'], e['fixed_release']) for e in events])
print('lags.csv kinds:', dict((k, sum(1 for r in lags if r['kind'] == k)) for k in sorted(set(r['kind'] for r in lags))))
print('lags.csv outcomes (fix rows):', dict((k, sum(1 for r in lags if r['kind'] == 'fix' and r['outcome'] == k))
                                            for k in sorted(set(r['outcome'] for r in lags if r['kind'] == 'fix'))))
tot = tot30 = 0
for e in events:
    lib, v = e['library'], e['fixed_release']
    pairs = [r for r in lags if r['kind'] == 'fix' and r['library'] == lib]
    frames = set(r['frame'] for r in pairs)
    m30 = [r for r in pairs if r['outcome'] == 'moved' and r['lag_release_days'] and float(r['lag_release_days']) <= 30]
    m30_author = [r for r in pairs if r['outcome'] == 'moved' and r['lag_release_days_author_time']
                  and float(r['lag_release_days_author_time']) <= 30]
    moved = [r for r in pairs if r['outcome'] == 'moved']
    d1 = share.get((lib, v, 1)); d30 = share.get((lib, v, 30))
    tot += len(pairs); tot30 += len(m30)
    print(f'{lib} {v}: frames {sorted(frames)}; pairs {len(pairs)}; moved {len(moved)}; '
          f'moved within 30 days by committer time {len(m30)} (by author time {len(m30_author)}); '
          f'LH011 share day 1 {r1(d1) if d1 is not None else "none"}, day 30 {r1(d30) if d30 is not None else "none"}, '
          f'rise {r1(d30 - d1) if d1 is not None and d30 is not None else ""} points')
print(f'all: {tot30} of {tot} pinned pairs moved within 30 days of the release')
