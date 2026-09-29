#!/usr/bin/env python3
"""R-0020, stage 2: inference checks on LH014 from the retained files only. No network. Python 3 with
`packaging`. Writes r0020_inference.txt beside this script. Every reading here is post hoc, made by the
reader-and-inference review after the record and the pieces were written; none is a test.

Groups: the top fifty (studies/LH011/data: releases.csv, counts/), band A and band B (studies/LH014/data).
Shares are recomputed from the counts files exactly as the studies' analyse.py do (at-or-newer share on
day d: downloads of the release or any higher version in the counts' numerator set over the project's
total that day), and checked against the retained release_outcomes.csv before anything else is read.

Questions:
 1. Horizon: per project, do most releases reach half by day 30, against within two days? If the
    30-day figure climbs a lot, "size, not speed" is the weaker reading.
 2. Ceiling: for releases that replaced a version at least 14 days old and in the numerator set, the
    share of "the replaced version or newer" on the day before day 0 (E, the newest-or-newer share the
    library already ran at) beside the new release's day-2 and day-30 shares. If S30 ~ E, the gradient
    in the pace is a gradient in what already floated to the newest version, not in uptake.
 3. Top fifty against each band: a percentile interval of the difference in the two-day project share,
    resampling both groups (10,000 draws; a description, since the brief fixed no such test).
 4. Rank against the project median day-1 share: Spearman's rho within each band and across all three
    groups, with a permutation p-value.
 5. Single-release projects inside the "every release" and "no release" groups.
 6. Mirrors: the largest project-median mirror share of a release's own downloads, and projects over
    1 and 2 per cent.
 7. Point-in-time horizons: the same "most releases at half" read on single days (2, 7, 14, 30) rather
    than as a maximum over days, with the day-30 group differences, and the projects that are "no"
    within two days but "yes" by day 30 (added after 1 showed the maximum-over-days figure climbing)."""
import csv, datetime, glob, os, random, statistics
from collections import defaultdict
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LH014 = os.path.join(ROOT, 'studies', 'LH014', 'data')
LH011 = os.path.join(ROOT, 'studies', 'LH011', 'data')
CUT, D, ONE = datetime.date(2026, 9, 27), datetime.date.fromisoformat, datetime.timedelta(days=1)
out = []
say = lambda *a: out.append(' '.join(str(x) for x in a))


def rd(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def load_counts(data):
    c = {}
    for f in sorted(glob.glob(os.path.join(data, 'counts', '*.csv'))):
        rows = defaultdict(lambda: defaultdict(int))
        for r in rd(f):
            rows[r['date']][r['v']] += int(r['downloads'])
        c[os.path.basename(f)[:-4]] = rows
    return c


def share(counts, p, day, pred):
    """(share, status) of the versions satisfying pred over the project's total on `day`."""
    if day > CUT:
        return None, 'after cut'
    row = counts[p].get(str(day))
    if not row:
        return None, 'no row'
    tot = sum(row.values())
    if tot == 0:
        return None, 'no downloads'
    return sum(n for v, n in row.items() if v != '~other' and pred(Version(v))) / tot, 'known'


groups = {}
for name, data, band in (('top fifty', LH011, None), ('band A', LH014, 'A'), ('band B', LH014, 'B')):
    rel = [r for r in rd(os.path.join(data, 'releases.csv')) if band is None or r['band'] == band]
    counts = load_counts(data)
    firstq = defaultdict(lambda: None)
    for r in rel:
        v = Version(r['version'])
        if firstq[r['project']] is None or v < firstq[r['project']]:
            firstq[r['project']] = v
    recs = []
    for r in rel:
        p, v0 = r['project'], Version(r['version'])
        d0 = D(r['day0'])
        s = {}
        for k in (-1, 0, 1, 2, 30):
            s[k] = share(counts, p, d0 + k * ONE, lambda v, v0=v0: v >= v0)
        reached2 = ('yes' if any(s[k][0] is not None and s[k][0] >= .5 for k in (1, 2))
                    else 'unknown' if any(s[k][0] is None for k in (1, 2)) else 'no')
        dth, last_known = '', -1
        for k in range(31):
            sh, st = share(counts, p, d0 + k * ONE, lambda v, v0=v0: v >= v0)
            if st == 'known':
                last_known = k
                if sh >= .5:
                    dth = k
                    break
        reached30 = 'yes' if dth != '' else ('no' if last_known == 30 else 'unknown')
        rv = Version(r['replaced_version'])
        old_age = (D(r['day0']) - D(r['replaced_first_upload_utc'][:10])).days
        eve = None
        if rv >= firstq[p] and old_age >= 14:
            eve = share(counts, p, d0 - ONE, lambda v, rv=rv: v >= rv)[0]
        recs.append(dict(project=p, version=r['version'], s1=s[1][0], s2=s[2][0], s30=s[30][0], reached2=reached2,
                         reached30=reached30, days_to_half=dth, eve=eve, old_age=old_age))
    groups[name] = dict(recs=recs, data=data, band=band)

# ---- self-check against the retained outcomes -------------------------------------------------------------
for name, g in groups.items():
    ro = rd(os.path.join(g['data'], 'analysis', 'release_outcomes.csv'))
    if g['band']:
        ro = [x for x in ro if x['band'] == g['band']]
    by = {(x['project'], x['version']): x for x in ro}
    bad = 0
    for r in g['recs']:
        x = by[(r['project'], r['version'])]
        for mine, theirs in ((r['s1'], x['share_day1']), (r['s2'], x['share_day2']),
                             (r['s30'], x.get('share_day30')) if 'share_day30' in x else (None, None)):
            if theirs is None:
                continue
            a = '' if mine is None else f'{mine:.6f}'
            if a != theirs:
                bad += 1
        if r['reached2'] != x['reached_half_within_two_days']:
            bad += 1
        if str(r['days_to_half']) != x['days_to_half']:
            bad += 1
    say(f'self-check, {name}: {len(g["recs"])} releases recomputed from counts/; disagreements with '
        f'release_outcomes.csv: {bad}')
say('')


def projmed(recs, key, cond=lambda r: True):
    per = defaultdict(list)
    for r in recs:
        if cond(r) and r[key] is not None and r[key] != '':
            per[r['project']].append(r[key])
    return {p: statistics.median(v) for p, v in per.items()}


def q3(xs):
    xs = sorted(xs)
    q = statistics.quantiles(xs, n=4, method='inclusive')
    return f'{q[0]*100:.1f} | {statistics.median(xs)*100:.1f} | {q[2]*100:.1f}'


def most(recs, key):
    """project -> 'yes'/'no' by 'most releases with a known outcome', or absent when none known."""
    per = defaultdict(list)
    for r in recs:
        if r[key] != 'unknown':
            per[r['project']].append(r[key] == 'yes')
    return {p: 2 * sum(v) > len(v) for p, v in per.items()}


# ---- 1. horizon ---------------------------------------------------------------------------------------------
say('1. HORIZON: projects whose releases mostly reached half within two days, and by day 30')
flags = {}
for name, g in groups.items():
    m2, m30 = most(g['recs'], 'reached2'), most(g['recs'], 'reached30')
    both = [p for p in m2 if p in m30]
    flip = sum(1 for p in both if not m2[p] and m30[p])
    n30 = len(m30)
    say(f'  {name}: two days {sum(m2.values())}/{len(m2)} = {100*sum(m2.values())/len(m2):.1f}%; '
        f'by day 30 {sum(m30.values())}/{n30} = {100*sum(m30.values())/n30:.1f}% '
        f'({flip} projects "no" at two days become "yes" by day 30; {len(m2) - n30} lose a known outcome at day 30)')
    r2 = [r for r in g['recs'] if r['reached2'] != 'unknown']
    r30 = [r for r in g['recs'] if r['reached30'] != 'unknown']
    say(f'    pooled releases: within two days {sum(r["reached2"] == "yes" for r in r2)}/{len(r2)}; '
        f'by day 30 {sum(r["reached30"] == "yes" for r in r30)}/{len(r30)}')
    flags[name] = [1 if v else 0 for v in m2.values()]
say('')

say('   project medians of the at-or-newer share, per group (lower quartile | median | upper quartile, %)')
for name, g in groups.items():
    for k, lab in (('s1', 'day 1'), ('s2', 'day 2'), ('s30', 'day 30')):
        pm = projmed(g['recs'], k)
        say(f'  {name}, {lab}: {q3(list(pm.values()))}  (projects {len(pm)})')
    ratio = projmed([dict(project=r['project'], ratio=r['s2'] / r['s30']) for r in g['recs']
                     if r['s2'] is not None and r['s30']], 'ratio')
    say(f'  {name}, day-2 share as a fraction of day-30 share: {q3(list(ratio.values()))}')
say('')

# ---- 2. ceiling --------------------------------------------------------------------------------------------
say('2. CEILING: releases whose replaced version was at least 14 days old and in the numerator set.')
say('   E = share of "the replaced version or newer" on the day before day 0; S2, S30 = the new release\'s')
say('   at-or-newer shares on days 2 and 30. Project medians (lower quartile | median | upper quartile, %).')
for name, g in groups.items():
    rs = [r for r in g['recs'] if r['eve'] is not None]
    say(f'  {name}: {len(rs)} of {len(g["recs"])} releases qualify, in {len({r["project"] for r in rs})} projects')
    e = projmed(rs, 'eve')
    say(f'    E:   {q3(list(e.values()))}')
    say(f'    S2:  {q3(list(projmed(rs, "s2").values()))}')
    s30 = [r for r in rs if r['s30'] is not None]
    say(f'    S30: {q3(list(projmed(s30, "s30").values()))}  (releases with day 30 read: {len(s30)})')
    d2 = projmed([dict(project=r['project'], d=r['s2'] - r['eve']) for r in rs if r['s2'] is not None], 'd')
    d30 = projmed([dict(project=r['project'], d=r['s30'] - r['eve']) for r in s30], 'd')
    say(f'    S2 - E, points:  {q3(list(d2.values()))}')
    say(f'    S30 - E, points: {q3(list(d30.values()))}')
    within = sum(1 for r in s30 if abs(r['s30'] - r['eve']) <= .10)
    say(f'    releases with S30 within 10 points of E: {within}/{len(s30)} = {100*within/len(s30):.0f}%')
    low = [r for r in rs if r['eve'] < .5]
    say(f'    releases with E below one half: {len(low)}/{len(rs)}; of them, reached half within two days: '
        f'{sum(r["reached2"] == "yes" for r in low)}, by day 30: {sum(r["reached30"] == "yes" for r in low)}')
    high = [r for r in rs if r['eve'] >= .5]
    say(f'    releases with E at or above one half: {len(high)}; of them, reached half within two days: '
        f'{sum(r["reached2"] == "yes" for r in high)}, by day 30: {sum(r["reached30"] == "yes" for r in high)}')
    # per project: does the project's median E sit on the same side of one half as its two-day outcome?
    m2 = most(g['recs'], 'reached2')
    agree = sum(1 for p, v in e.items() if p in m2 and (v >= .5) == m2[p])
    say(f'    projects whose median E is on the same side of one half as their two-day outcome: {agree}/{len([p for p in e if p in m2])}')
say('')

# ---- 3. group differences ----------------------------------------------------------------------------------
say('3. DIFFERENCE IN THE TWO-DAY PROJECT SHARE, resampling both groups (10,000 draws, seed 20260929; post hoc)')
rng = random.Random(20260929)
B = 10000


def boot(a, b):
    diffs = []
    for _ in range(B):
        sa = sum(rng.choice(a) for _ in a) / len(a)
        sb = sum(rng.choice(b) for _ in b) / len(b)
        diffs.append(sa - sb)
    diffs.sort()
    pc = lambda p: diffs[min(len(diffs) - 1, int(p * (len(diffs) - 1)))]
    return sum(a) / len(a) - sum(b) / len(b), pc(.025), pc(.975), sum(1 for d in diffs if d <= 0) / B


for x, y in (('top fifty', 'band A'), ('top fifty', 'band B'), ('band A', 'band B')):
    d, lo, hi, p0 = boot(flags[x], flags[y])
    say(f'  {x} minus {y}: {100*d:.1f} points, interval {100*lo:.1f} to {100*hi:.1f}; resamples at or below zero: {100*p0:.1f}%')
say('')

# ---- 4. rank against the day-1 share ------------------------------------------------------------------------
say('4. RANK AGAINST THE PROJECT MEDIAN DAY-1 SHARE (Spearman rho; permutation p, 10,000 draws; post hoc)')
frame = rd(os.path.join(LH014, 'frame.csv'))
pos = {r['project']: int(r['position']) for r in frame if r['position']}
drawn = rd(os.path.join(LH014, 'drawn.csv'))
pos.update({r['project']: int(r['position']) for r in drawn})


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    rk = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            rk[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return rk


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** .5
    return num / den


def perm_p(x, y, rho):
    y = list(y)
    n = 0
    for _ in range(B):
        rng.shuffle(y)
        if abs(spearman(x, y)) >= abs(rho):
            n += 1
    return n / B


allx, ally = [], []
for name, g in groups.items():
    pm = projmed(g['recs'], 's1')
    x = [pos[p] for p in pm]
    y = [pm[p] for p in pm]
    allx += x
    ally += y
    rho = spearman(x, y)
    say(f'  within {name}: rho = {rho:+.2f} (n = {len(x)}, positions {min(x)} to {max(x)}), p = {perm_p(x, y, rho):.3f}')
rho = spearman(allx, ally)
say(f'  across all three groups: rho = {rho:+.2f} (n = {len(allx)}), p = {perm_p(allx, ally, rho):.3f}')
say('')

# ---- 5. single-release projects ---------------------------------------------------------------------------
say('5. SINGLE-RELEASE PROJECTS inside the "every release reached half" and "no release" groups')
for name, g in groups.items():
    per = defaultdict(list)
    for r in g['recs']:
        if r['reached2'] != 'unknown':
            per[r['project']].append(r['reached2'] == 'yes')
    every = [p for p, v in per.items() if all(v)]
    none = [p for p, v in per.items() if not any(v)]
    one = {p for p, v in per.items() if len(v) == 1}
    say(f'  {name}: every {len(every)} (single-release {len([p for p in every if p in one])}); '
        f'none {len(none)} (single-release {len([p for p in none if p in one])}); '
        f'projects with one release {len(one)} of {len(per)}; with three or more, all-or-nothing '
        f'{sum(1 for p, v in per.items() if len(v) >= 3 and (all(v) or not any(v)))}/{sum(1 for v in per.values() if len(v) >= 3)}')
say('')

# ---- 6. mirrors --------------------------------------------------------------------------------------------
say("6. MIRRORS: project-median share of a release's own downloads on days 0 and 1 made by the three named tools")
po = rd(os.path.join(LH014, 'analysis', 'project_outcomes.csv'))
for b in 'AB':
    xs = [(p['project'], float(p['median_mirror_share_of_own_days01'])) for p in po
          if p['band'] == b and p['median_mirror_share_of_own_days01'] != '']
    xs.sort(key=lambda t: -t[1])
    say(f'  band {b}: largest {xs[0][0]} {100*xs[0][1]:.2f}%; over 1%: {sum(1 for _, v in xs if v > .01)}; over 2%: '
        f'{sum(1 for _, v in xs if v > .02)}; of {len(xs)} projects')

# ---- 7. point-in-time horizons and the flipped projects ------------------------------------------------
say('')
say('7. POINT-IN-TIME: projects whose releases mostly had an at-or-newer share of at least one half ON day d')
say('   (the two-day measure is a maximum over days 1 and 2; "by day 30" a maximum over days 0 to 30; these are single days)')
pit = {}
for name, g in groups.items():
    data, band = g['data'], g['band']
    counts = load_counts(data)
    rel = [r for r in rd(os.path.join(data, 'releases.csv')) if band is None or r['band'] == band]
    line = []
    for k in (2, 7, 14, 30):
        per = defaultdict(list)
        for r in rel:
            sh, st = share(counts, r['project'], D(r['day0']) + k * ONE, lambda v, v0=Version(r['version']): v >= v0)
            if st == 'known':
                per[r['project']].append(sh >= .5)
        m = {p: 2 * sum(v) > len(v) for p, v in per.items()}
        pit[(name, k)] = [1 if v else 0 for v in m.values()]
        line.append(f'day {k}: {sum(m.values())}/{len(m)} = {100*sum(m.values())/len(m):.0f}%')
    say(f'  {name}: ' + '; '.join(line))
say('   differences at day 30 (single day), resampling both groups:')
for x, y in (('top fifty', 'band A'), ('top fifty', 'band B'), ('band A', 'band B')):
    d, lo, hi, p0 = boot(pit[(x, 30)], pit[(y, 30)])
    say(f'    {x} minus {y}: {100*d:.1f} points, interval {100*lo:.1f} to {100*hi:.1f}; resamples at or below zero: {100*p0:.1f}%')
say('')
say('   the projects "no" within two days and "yes" by day 30 (median over their releases of the day-1, day-2 and')
say('   day-30 shares, %; median days to half among releases reaching it; releases):')
for name, g in groups.items():
    m2, m30 = most(g['recs'], 'reached2'), most(g['recs'], 'reached30')
    for p in sorted(p for p in m2 if p in m30 and not m2[p] and m30[p]):
        rs = [r for r in g['recs'] if r['project'] == p]
        f = lambda k: statistics.median([r[k] for r in rs if r[k] is not None]) * 100 if any(r[k] is not None for r in rs) else float('nan')
        dth = statistics.median([r['days_to_half'] for r in rs if r['days_to_half'] != ''])
        say(f'    {name}, {p}: day 1 {f("s1"):.0f}, day 2 {f("s2"):.0f}, day 30 {f("s30"):.0f}; days to half {dth:g}; releases {len(rs)}')

with open(os.path.join(HERE, 'r0020_inference.txt'), 'w') as f:
    f.write('\n'.join(out) + '\n')
print('\n'.join(out))
