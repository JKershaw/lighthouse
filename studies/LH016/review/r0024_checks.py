#!/usr/bin/env python3
"""R-0024: the evidence review's own reproduction of the figures in the correction round of
29 September 2026, late evening (commit c8d79eb: LH011 record 0.4 and piece 1.2, LH012 record 0.4
and piece 1.2, LH016 record 0.2). Written without reading the round's own scripts for the
arithmetic (studies/LH011/review/v04_checks.py, studies/LH012/review/v04_checks.py and the
LH016 driver checks were read afterwards, to compare); only the retained tables are read:
studies/LH011/data/analysis/release_days.csv and studies/LH012/data/analysis/firstday_releases.csv.
Offline, standard library only. Quartiles are given by two methods, since the round's
scripts use statistics.quantiles (exclusive) and a reader may use another.

Usage: python3 studies/LH016/review/r0024_checks.py > studies/LH016/review/r0024_checks.txt"""
import csv, os, statistics as st
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LH011 = os.path.join(ROOT, 'studies', 'LH011', 'data', 'analysis', 'release_days.csv')
LH012 = os.path.join(ROOT, 'studies', 'LH012', 'data', 'analysis', 'firstday_releases.csv')


def med(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def quart(v):
    ex = st.quantiles(v, n=4, method='exclusive')
    inc = st.quantiles(v, n=4, method='inclusive')
    return f'median {med(v):.2f}; quartiles exclusive {ex[0]:.2f} and {ex[2]:.2f}, inclusive {inc[0]:.2f} and {inc[2]:.2f}'


# ---------------------------------------------------------------- LH011: release_days.csv
rows = list(csv.DictReader(open(LH011)))
known = [r for r in rows if r['status'] == 'known' and r['share_at_or_newer'] != '']
print(f'§1 release_days.csv: {len(rows)} rows, {len(known)} known with a share; days run '
      f'{min(int(r["day"]) for r in rows)} to {max(int(r["day"]) for r in rows)}; '
      f'{len(set((r["project"], r["version"]) for r in rows))} releases of {len(set(r["project"] for r in rows))} projects')

by_rel = defaultdict(dict)   # (project, version) -> day -> row
for r in known:
    by_rel[(r['project'], r['version'])][int(r['day'])] = r

print()
print('§2 litellm: every release whose at-or-newer share was at least 0.5 on any known day 1 to 30')
lit = {k: d for k, d in by_rel.items() if k[0] == 'litellm'}
hits = []
for (p, v), d in sorted(lit.items(), key=lambda kv: kv[1][min(kv[1])]['date']):
    at = [k for k in sorted(d) if 1 <= k <= 30 and float(d[k]['share_at_or_newer']) >= 0.5]
    if at:
        first = at[0]
        later = [k for k in sorted(d) if first < k <= 30]
        later_at = [k for k in later if float(d[k]['share_at_or_newer']) >= 0.5]
        hits.append((v, d[0]['date'], first, d[first]['date'], float(d[first]['share_at_or_newer']), len(later_at), len(later)))
for h in hits:
    print(f'  {h[0]} released {h[1]}: first at half day {h[2]} ({h[3]}), share {h[4]:.3f}; at half on {h[5]} of {h[6]} later days to day 30')
print(f'  {len(hits)} of {len(lit)} litellm releases; dates on which any first reached half: {sorted(set(h[3] for h in hits))}; '
      f'median first day {med([h[2] for h in hits])}; days at half after the first, summed: {sum(h[5] for h in hits)}')
also_day0 = [(v, d[0]['date']) for (p, v), d in lit.items() if 0 in d and float(d[0]['share_at_or_newer']) >= 0.5]
print(f'  litellm releases at half on day 0: {len(also_day0)}')
print('  litellm 1.83.1, days 26 to 30: date, total, at 1.83.1 or newer, share, older')
for k in range(26, 31):
    r = by_rel[('litellm', '1.83.1')].get(k)
    if r:
        t, n = int(r['total']), int(r['at_or_newer'])
        print(f'    day {k} {r["date"]}: {t:,} {n:,} {n / t:.3f} {t - n:,}')
# the same three days as seen from the other five releases: is 1 May the same surge in each?
print('  the share on 2026-05-01 for each of the six, and the day before and after:')
for (p, v), d in sorted(lit.items()):
    if v.startswith('1.83.') and v in [h[0] for h in hits]:
        by_date = {d[k]['date']: (k, float(d[k]['share_at_or_newer'])) for k in d}
        print(f'    {v}: ' + ', '.join(f'{dt} day {by_date[dt][0]} {by_date[dt][1]:.3f}' for dt in ('2026-04-30', '2026-05-01', '2026-05-02') if dt in by_date))

print()
print('§3 day 30 against day 1 and day 2, at-or-newer share, all 37 projects (points = share difference x 100)')
for a in (1, 2):
    pairs = {}
    for k, d in by_rel.items():
        if 30 in d and a in d:
            pairs[k] = (float(d[30]['share_at_or_newer']) - float(d[a]['share_at_or_newer'])) * 100
    v = list(pairs.values())
    print(f'  day 30 minus day {a}: {len(v)} releases; higher on day 30 {sum(x > 0 for x in v)}, equal {sum(x == 0 for x in v)}, lower {sum(x < 0 for x in v)}; '
          f'{quart(v)}; above +10 {sum(x > 10 for x in v)}, below -10 {sum(x < -10 for x in v)}')
    bp = defaultdict(list)
    for (p, _), x in pairs.items():
        bp[p].append(x)
    pm = {p: med(x) for p, x in bp.items()}
    print(f'    by project (median over its releases): {len(pm)} projects, above zero {sum(x > 0 for x in pm.values())}, '
          f'median of project medians {med(list(pm.values())):.2f}; not above zero: '
          + ', '.join(f'{p} {x:+.2f}' for p, x in sorted(pm.items()) if x <= 0))
    rest = [x for (p, _), x in pairs.items() if p not in ('boto3', 'botocore', 'litellm')]
    print(f'    without boto3, botocore and litellm: {len(rest)} releases, higher {sum(x > 0 for x in rest)}, median {med(rest):.2f}')
    ratios = [float(d[a]['share_at_or_newer']) / float(d[30]['share_at_or_newer'])
              for d in by_rel.values() if 30 in d and a in d and float(d[30]['share_at_or_newer']) > 0]
    print(f'    day-{a} share over day-30 share: {len(ratios)} releases, median {med(ratios):.3f}')

# the chart's lines: each project's median share by day over its releases
line = defaultdict(lambda: defaultdict(list))
for (p, _), d in by_rel.items():
    for k, r in d.items():
        line[p][k].append(float(r['share_at_or_newer']))
medline = {p: {k: med(v) for k, v in days.items()} for p, days in line.items()}
d30m1 = {p: (m[30] - m[1]) * 100 for p, m in medline.items() if 30 in m and 1 in m}
print(f'  the chart\'s lines, median on day 30 minus median on day 1: {len(d30m1)} projects, above zero {sum(x > 0 for x in d30m1.values())}, '
      f'median {med(list(d30m1.values())):.2f}; below zero: ' + ', '.join(f'{p} {x:+.1f}' for p, x in sorted(d30m1.items(), key=lambda t: t[1]) if x < 0))
print(f'  ratio of median day-1 to median day-30 line, median over projects: {med([m[1] / m[30] for m in medline.values() if 30 in m and 1 in m]):.3f}')

print()
print('§4 the chart\'s description: where the lines sit')
# a project is "yes" if most of its releases reached half by day 1 or 2 (the record's rule); read from the table
def reached(d):
    return any(k in d and float(d[k]['share_at_or_newer']) >= 0.5 for k in (0, 1, 2))
outcome = defaultdict(list)
for (p, _), d in by_rel.items():
    outcome[p].append(reached(d))
yes = sorted(p for p, o in outcome.items() if sum(o) * 2 > len(o))
no = sorted(p for p in outcome if p not in yes)
print(f'  most releases reached half by day 2: {len(yes)} projects; none did: {len([p for p in no if not any(outcome[p])])}; some but not most: {len([p for p in no if any(outcome[p])])}')
def span(ps, days):
    vals = [medline[p][k] * 100 for p in ps for k in days if k in medline[p]]
    return f'{min(vals):.1f} to {max(vals):.1f}'
print(f'  blue lines (yes), days 1 to 30: {span(yes, range(1, 31))} per cent; orange lines, days 0 to 30: {span(no, range(0, 31))}; orange days 1 to 30: {span(no, range(1, 31))}')
print('  the eleven, median day-1 share, median day-30 share, difference (points), ordered by day 1:')
for p in sorted(no, key=lambda p: medline[p][1]):
    print(f'    {p}: {medline[p][1] * 100:.1f} -> {medline[p][30] * 100:.1f} ({(medline[p][30] - medline[p][1]) * 100:+.1f})')
print('  every line lower on day 0 than day 1: ' + str(all(medline[p][0] < medline[p][1] for p in medline)))
half = [(k, float(d[1]['share_at_or_newer']) / float(d[30]['share_at_or_newer'])) for k, d in by_rel.items() if 30 in d and 1 in d and float(d[30]['share_at_or_newer']) > 0]
print(f'  releases whose day-1 share was less than half of their day-30 share: {sum(r < 0.5 for _, r in half)} of {len(half)}; '
      f'projects whose median line on day 1 is less than half of its day-30 median: '
      + ', '.join(f'{p} {m[1] / m[30]:.2f}' for p, m in sorted(medline.items()) if 30 in m and 1 in m and m[1] / m[30] < 0.5))
print('  the piece\'s opening: requests 2.34.0 and pandas 3.0.3, share on day 1 and day 30:')
for k in (('requests', '2.34.0'), ('pandas', '3.0.3')):
    d = by_rel[k]
    print(f'    {k[0]} {k[1]} (day 0 {d[0]["date"]}): day 1 {float(d[1]["share_at_or_newer"]):.3f}, day 30 {float(d[30]["share_at_or_newer"]):.3f}')

# ---------------------------------------------------------------- LH012: firstday_releases.csv
print()
rows2 = list(csv.DictReader(open(LH012)))
print(f'§5 firstday_releases.csv: {len(rows2)} releases of {len(set(r["project"] for r in rows2))} projects; '
      f'day0 from {min(r["day0"] for r in rows2)} to {max(r["day0"] for r in rows2)}')
delta = [(float(r['s30']) - float(r['s2'])) * 100 for r in rows2]
stated = [float(r['delta_points']) for r in rows2]
print(f'  delta recomputed from the six-decimal s2 and s30 columns differs from delta_points by at most {max(abs(a - b) for a, b in zip(delta, stated)):.5f} points (rounding of the columns); every count below is the same either way')
print(f'  higher on day 30 than day 2: {sum(x > 0 for x in delta)}; lower: {sum(x < 0 for x in delta)}; equal: {sum(x == 0 for x in delta)}')
print(f'  {quart(delta)}; above +10: {sum(x > 10 for x in delta)}; below -10: {sum(x < -10 for x in delta)}; within ten points (|delta| <= 10): {sum(abs(x) <= 10 for x in delta)}')
settled_col = sum(r['settled'] == 'True' for r in rows2)
inband = [x for x in delta if abs(x) <= 10]
print(f'  settled column True: {settled_col}; of those within the band, higher on day 30: {sum(x > 0 for x in inband)}, median {med(inband):.2f}')
ratio = [float(r['s2']) / float(r['s30']) for r in rows2 if float(r['s30']) > 0]
print(f'  s2 / s30, recomputed: {len(ratio)} releases, median {med(ratio):.3f}')
bp = defaultdict(list)
for r, x in zip(rows2, delta):
    bp[r['project']].append(x)
pm = {p: med(v) for p, v in bp.items()}
print(f'  by project: {len(pm)} projects, median above zero for {sum(x > 0 for x in pm.values())}; median of project medians {med(list(pm.values())):.2f}; '
      'not above zero: ' + ', '.join(f'{p} {x:+.2f} ({len(bp[p])} releases)' for p, x in sorted(pm.items()) if x <= 0))
three = ('boto3', 'botocore', 'litellm')
print('  the three daily releasers: ' + '; '.join(f'{p} {len(bp[p])} releases, median {pm[p]:.2f}' for p in three)
      + f'; together {sum(len(bp[p]) for p in three)}')
rest = [x for r, x in zip(rows2, delta) if r['project'] not in three]
print(f'  without them: {len(rest)} releases, higher on day 30 {sum(x > 0 for x in rest)}, {quart(rest)}')
# the settling test itself, unchanged by the round, for completeness
proj_settled = {p: sum(abs(x) <= 10 for x in v) * 2 > len(v) for p, v in bp.items()}
print(f'  the test as the brief defined it: releases within ten points {sum(abs(x) <= 10 for x in delta)} of {len(delta)}; projects where most releases settle '
      f'{sum(proj_settled.values())} of {len(proj_settled)}; not: {", ".join(sorted(p for p, s in proj_settled.items() if not s))}')
