#!/usr/bin/env python3
"""LH011: readings made after every count had been read (post hoc), for record version 0.3.

None of these was fixed in the brief. They describe the retained tables; they test nothing.
Offline, no network, no library beyond the standard one. Reads data/analysis/release_days.csv and
project_outcomes.csv (or LH011_OUT, as replay.sh sets it), and, for the last reading, LH008's retained
data/events.csv and data/lags.csv (reused, and disclosed in the record's header).

1. What a month adds: for each project, the median over its releases of the at-or-newer share on
   day 1 and on day 30 (releases whose day 30 is held), computed as scripts/draw_piece_figure.py
   computes them, and how many projects' day-30 median lies within ten points of the day-1 median.
   The ten-point band was chosen by the writing agent while drawing the piece's chart.
2. What stays on older versions: one minus the day-30 median, by group (whether most of the
   project's releases reached half within two days).
3. How much of the month's share came on day 1: the day-1 median as a share of the day-30 median.
4. The widest gaps between neighbouring projects' median day-1 shares, as project_outcomes.csv
   gives them (the brief's measure).
5. The same releases read two ways: the four security fixes that were LH008's events are LH011
   releases. For each, LH011's at-or-newer share on days 1 and 30, and how many of LH008's pinned
   repository pairs had moved to the fix within 30 days of its release.

Usage: python3 studies/LH011/scripts/post_hoc.py > studies/LH011/data/post_hoc_reading.txt"""
import csv, os, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
A = os.environ.get('LH011_OUT', os.path.join(STUDY, 'data', 'analysis'))
LH008 = os.path.join(os.path.dirname(STUDY), 'LH008', 'data')

proj = {r['project']: r for r in csv.DictReader(open(os.path.join(A, 'project_outcomes.csv'))) if r['releases'] != '0'}
days = defaultdict(lambda: defaultdict(list))
rel_day = {}
for r in csv.DictReader(open(os.path.join(A, 'release_days.csv'))):
    if r['status'] == 'known' and r['share_at_or_newer']:
        s = float(r['share_at_or_newer'])
        days[r['project']][int(r['day'])].append(s)
        rel_day[(r['project'], r['version'], int(r['day']))] = s


def med(p, d):
    v = days[p].get(d)
    return statistics.median(v) if v else None


def pct(x):
    return f'{x * 100:.1f}'


print('1. What a month adds (medians over each project\'s releases of the at-or-newer share)')
print('project, most releases reached half within two days, releases, day 1, day 30, day 30 minus day 1 (points)')
rows = []
for p in sorted(proj, key=lambda p: -med(p, 1)):
    d1, d30 = med(p, 1), med(p, 30)
    rows.append((p, proj[p]['most_reached'], d1, d30))
    print(f'{p}, {proj[p]["most_reached"]}, {proj[p]["releases"]}, {pct(d1)}, '
          + (f'{pct(d30)}, {(d30 - d1) * 100:+.1f}' if d30 is not None else 'not held, '))
held = [r for r in rows if r[3] is not None]
within = [r for r in held if abs(r[3] - r[2]) <= 0.10]
print(f'within ten points of day 1 by day 30: {len(within)} of {len(held)} projects with day 30 held; '
      f'the others: ' + '; '.join(f'{p} {pct(d1)} to {pct(d30)}' for p, g, d1, d30 in held if abs(d30 - d1) > 0.10))

print()
print('2. What stays on older versions: one minus the day-30 median')
for g, name in (('yes', 'most releases reached half'), ('no', 'no release reached half')):
    v = sorted((1 - d30, p) for p, gg, d1, d30 in held if gg == g)
    print(f'{name}: {len(v)} projects, from {pct(v[0][0])} ({v[0][1]}) to {pct(v[-1][0])} ({v[-1][1]}), '
          f'median {pct(statistics.median(x for x, _ in v))}')

print()
print('3. The day-1 median as a share of the day-30 median, projects where no release reached half')
ratios = sorted(((d1 / d30), p) for p, g, d1, d30 in held if g == 'no')
for x, p in ratios:
    print(f'{p}: {x * 100:.0f} per cent')

print()
print('4. Widest gaps between neighbouring projects\' median day-1 shares (project_outcomes.csv)')
s = sorted((float(r['median_day1_share']), p) for p, r in proj.items())
gaps = sorted(((b[0] - a[0], a, b) for a, b in zip(s, s[1:])), reverse=True)[:3]
for gap, a, b in gaps:
    print(f'{gap * 100:.1f} points, from {a[1]} {pct(a[0])} to {b[1]} {pct(b[0])}')

print()
print('5. The same releases read two ways: LH008\'s four fixes, which are LH011 releases')
print('library, fixed release, LH011 at-or-newer share day 1, day 30, LH008 pinned pairs, moved within 30 days of release, moved by the head as cloned')
ev = [r for r in csv.DictReader(open(os.path.join(LH008, 'events.csv'))) if r['chosen'] == 'yes']
lags = [r for r in csv.DictReader(open(os.path.join(LH008, 'lags.csv'))) if r['kind'] == 'fix']
tp = tm = 0
for e in ev:
    lib, v = e['library'], e['fixed_release']
    pairs = [r for r in lags if r['library'] == lib]
    moved30 = sum(1 for r in pairs if r['outcome'] == 'moved' and r['lag_release_days'] and float(r['lag_release_days']) <= 30)
    moved = sum(1 for r in pairs if r['outcome'] == 'moved')
    tp += len(pairs); tm += moved30
    d1, d30 = rel_day.get((lib, v, 1)), rel_day.get((lib, v, 30))
    print(f'{lib}, {v}, {pct(d1) if d1 is not None else "not an LH011 release"}, '
          f'{pct(d30) if d30 is not None else "not held"}, {len(pairs)}, {moved30}, {moved}')
print(f'all four: {tm} of {tp} pinned pairs moved within 30 days of the release')
