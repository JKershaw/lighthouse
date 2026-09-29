#!/usr/bin/env python3
"""Release review R-0019 (notes/R-0019.md): an independent recount of LH014's tested and quoted figures
from the retained reads alone, written without copying scripts/analyse.py. No network. Python 3 with
`packaging`. Run from anywhere: python3 studies/LH014/review/r0019_check.py > studies/LH014/review/r0019_check.txt

Recounted, from data/releases.csv, pypi_versions.csv, counts/, daily_totals.csv, mirror/, ci/ and drawn.csv:
the four tests (each band's primary share and settling share, with the brief's percentile intervals over
10,000 project resamples from random.Random(20260929) in the brief's order), the descriptors the piece
quotes (median day-1 shares, days to half, projects with no release at half by day 30, mirror counts and
shares, the post hoc reading, the band A figures without the overlap projects), the CI description, the
two-table checks, the opening figures for pillow 12.3.0 and sentry-sdk 2.64.0, and the ranges the piece's
figure description gives. The top fifty's figures are read from studies/LH011/data/analysis/.
Nothing here reads any day after 2026-09-27; the retained files hold none."""
import csv, datetime, os, random, statistics
from collections import defaultdict
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
LH011 = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'LH011', 'data', 'analysis')
CUT = datetime.date(2026, 9, 27)
D = datetime.date.fromisoformat
ONE = datetime.timedelta(days=1)
MIRROR = {'artifactory', 'bandersnatch', 'devpi', 'z3c.pypimirror'}


def rd(*p):
    with open(os.path.join(*p), newline='') as f:
        return list(csv.DictReader(f))


def pct(xs, p):  # percentile with linear interpolation, the brief's (LH011's) convention
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def q(xs):
    xs = sorted(xs)
    if len(xs) < 2:
        return xs[0], xs[0], xs[0]
    a = statistics.quantiles(xs, n=4, method='inclusive')
    return a[0], statistics.median(xs), a[2]


def f1(x):
    return '' if x == '' or x is None else f'{x:.1f}'


# ---- frame ---------------------------------------------------------------------------------------------
drawn = rd(DATA, 'drawn.csv')
order = {d['project']: (d['band'], int(d['draw_order'])) for d in drawn}
overlap = {d['project'] for d in drawn if d['in_overlap_set'] == 'True'}
releases = rd(DATA, 'releases.csv')
listed = defaultdict(list)  # project -> non-pre-release versions PyPI lists, PEP 440 parsed
for v in rd(DATA, 'pypi_versions.csv'):
    if v['parse'] == 'ok' and v['is_prerelease'] == 'False':
        listed[v['project']].append(v['version'])
projects = sorted({r['project'] for r in releases}, key=lambda p: order[p])
print(f'projects with a release: A {sum(order[p][0] == "A" for p in projects)}, B {sum(order[p][0] == "B" for p in projects)}; '
      f'releases: A {sum(r["band"] == "A" for r in releases)}, B {sum(r["band"] == "B" for r in releases)}')

# ---- gap rule, from the per-day table over the 160 drawn projects -----------------------------------------
daily = defaultdict(dict)
for r in rd(DATA, 'daily_totals.csv'):
    daily[r['project']][D(r['date'])] = int(r['downloads'])
tot = defaultdict(int)
for p in daily:
    for d, n in daily[p].items():
        tot[d] += n
low_days = []
for d in sorted(tot):
    around = [tot[d + k * ONE] for k in range(-3, 4) if (d + k * ONE) in tot]
    if tot[d] < statistics.median(around) / 2:
        low_days.append(d)
print(f'per-day table: {len(tot)} days {min(tot)} to {max(tot)}; days below half the local median: {len(low_days)}')

# ---- per-version counts ----------------------------------------------------------------------------------
counts = {}  # project -> date -> version -> downloads
for p in projects:
    c = defaultdict(dict)
    for r in rd(DATA, 'counts', f'{p}.csv'):
        c[D(r['date'])][r['v']] = int(r['downloads'])
    counts[p] = c


def share(p, day, atleast, own):
    """(at-or-newer share, own share, total) on a date, or None when the day is past the cut, has no row,
    has no downloads, or is a gap (no row with rows either side, or a low day over the drawn projects)."""
    if day > CUT:
        return None
    c = counts[p]
    if day not in c:
        return None
    total = sum(c[day].values())
    if total == 0 or day in low_days:
        return None
    return sum(n for v, n in c[day].items() if v in atleast), c[day].get(own, 0), total


rel = []  # per release
for r in releases:
    p, v = r['project'], r['version']
    d0 = D(r['day0'])
    at = {w for w in listed[p] if Version(w) >= Version(v)}
    sh = {}
    for k in (0, 1, 2, 30):
        s = share(p, d0 + k * ONE, at, v)
        sh[k] = None if s is None else s[0] / s[2]
    # days to half: first day 0..30 at or above one half; None when not reached by day 30 or by the cut
    dth = None
    for k in range(31):
        s = share(p, d0 + k * ONE, at, v)
        if s is not None and s[0] / s[2] >= .5:
            dth = k
            break
    if sh[1] is not None and sh[1] >= .5 or sh[2] is not None and sh[2] >= .5:
        reached = True
    elif sh[1] is None or sh[2] is None:
        reached = None
    else:
        reached = False
    delta = None if sh[2] is None or sh[30] is None else (sh[30] - sh[2]) * 100
    rel.append(dict(band=r['band'], project=p, version=v, d0=d0, sh=sh, reached=reached, dth=dth, delta=delta,
                    settles=None if delta is None else abs(delta) <= 10, ci=r['ci_subsample'] == 'True',
                    replaced=r['replaced_version'], at=at))

# ---- per project -----------------------------------------------------------------------------------------
proj = {}
for p in projects:
    rs = [x for x in rel if x['project'] == p]
    kn = [x for x in rs if x['reached'] is not None]
    n_r = sum(x['reached'] for x in kn)
    kd = [x for x in rs if x['delta'] is not None]
    n_s = sum(x['settles'] for x in kd)
    d1 = [x['sh'][1] for x in rs if x['sh'][1] is not None]
    proj[p] = dict(band=order[p][0], n=len(rs), known=len(kn), reached=n_r,
                   most=None if not kn else n_r > len(kn) / 2, every=bool(kn) and n_r == len(kn), none=bool(kn) and n_r == 0,
                   dknown=len(kd), settled=n_s, settles=None if not kd else n_s > len(kd) / 2,
                   md1=statistics.median(d1) if d1 else None,
                   mdelta=statistics.median([x['delta'] for x in kd]) if kd else None,
                   mratio=statistics.median([x['sh'][2] / x['sh'][30] for x in kd if x['sh'][30]]) if kd else None,
                   md1delta=statistics.median([(x['sh'][30] - x['sh'][1]) * 100 for x in kd if x['sh'][1] is not None]) if kd else None,
                   none_by_30=all(x['dth'] is None for x in rs))

rng = random.Random(20260929)


def share_ci(flags):
    boots = [sum(rng.choice(flags) for _ in flags) / len(flags) for _ in range(10000)]
    return pct(boots, .025) * 100, pct(boots, .975) * 100


def median_ci(vals):
    boots = [statistics.median([rng.choice(vals) for _ in vals]) for _ in range(10000)]
    return pct(boots, .025), pct(boots, .975)


def conv(s, settling=False):
    if settling:
        return 'holds as a rule' if s >= .75 else 'fails' if s < .5 else 'holds for some projects'
    return 'as a rule' if s >= .75 else 'not as a rule' if s < .5 else 'for some projects'


def tests(keep, label):
    print(f'\n== the four tests{label}')
    for key, name in (('most', 'primary'), ('settles', 'settling')):
        for b in 'AB':
            ps = [p for p in projects if proj[p]['band'] == b and keep(p) and proj[p][key] is not None]
            flags = [1 if proj[p][key] else 0 for p in ps]
            s = sum(flags) / len(flags)
            lo, hi = share_ci(flags)
            print(f'   {name} {b}: {sum(flags)} of {len(flags)} = {s * 100:.1f} per cent, interval {lo:.1f} to {hi:.1f}: {conv(s, key == "settles")}')
    return ps


tests(lambda p: True, '')

print('\n== descriptors, per band')
for b in 'AB':
    ps = [p for p in projects if proj[p]['band'] == b]
    print(f'   {b}: every release reached half {sum(proj[p]["every"] for p in ps)}, most but not every '
          f'{sum(proj[p]["most"] and not proj[p]["every"] for p in ps)}, none {sum(proj[p]["none"] for p in ps)}, '
          f'mixed with most not {sum(not proj[p]["most"] and not proj[p]["none"] for p in ps)}')
    md1 = [proj[p]['md1'] * 100 for p in ps if proj[p]['md1'] is not None]
    print(f'   {b}: median of project median day-1 shares {f1(q(md1)[1])} (quartiles {f1(q(md1)[0])}, {f1(q(md1)[2])}), over {len(md1)} projects')
    rs = [x for x in rel if x['band'] == b]
    reached30 = [x['dth'] for x in rs if x['dth'] is not None]
    print(f'   {b}: releases at half by day 30 {len(reached30)} of {len(rs)}, median day {statistics.median(reached30)}; '
          f'projects with no release at half by day 30: {sum(proj[p]["none_by_30"] for p in ps)}')
    known = [x for x in rs if x['reached'] is not None]
    print(f'   {b}: pooled {sum(x["reached"] for x in known)} of {len(known)} releases = {100 * sum(x["reached"] for x in known) / len(known):.1f} per cent')
    kd = [x for x in rs if x['delta'] is not None]
    print(f'   {b}: delta known for {len(kd)} releases, {sum(x["settles"] for x in kd)} settled; project medians: delta '
          f'{f1(statistics.median([proj[p]["mdelta"] for p in ps if proj[p]["mdelta"] is not None]))}, ratio day 2 to day 30 '
          f'{statistics.median([proj[p]["mratio"] for p in ps if proj[p]["mratio"] is not None]):.2f}, delta from day 1 '
          f'{f1(statistics.median([proj[p]["md1delta"] for p in ps if proj[p]["md1delta"] is not None]))}')
    print(f'   {b}: did not settle: {", ".join(p for p in ps if proj[p]["settles"] is False)}')

# ---- the opening figures ---------------------------------------------------------------------------------
print('\n== the opening figures')
for p, v in (('pillow', '12.3.0'), ('sentry-sdk', '2.64.0')):
    x = next(r for r in rel if r['project'] == p and r['version'] == v)
    d1 = x['d0'] + ONE
    s1 = share(p, d1, x['at'], v)
    later = sorted(x['at'] - {v}, key=Version)
    print(f'   {p} {v}: day 0 {x["d0"]}; day 1 {d1} total {s1[2]:,}, own {100 * s1[1] / s1[2]:.1f} per cent, at or newer '
          f'{100 * s1[0] / s1[2]:.1f}; day 30 {x["d0"] + 30 * ONE} at or newer {100 * x["sh"][30]:.1f} (later versions listed: {later[:4]})')

# ---- mirrors ---------------------------------------------------------------------------------------------
print('\n== mirrors (M2 counts and shares; M1 outcomes without the mirror class)')
mir = {}
for p in projects:
    m = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # date -> version -> class -> n
    for r in rd(DATA, 'mirror', f'{p}.csv'):
        m[D(r['date'])][r['v']][r['installer_class']] += int(r['downloads'])
    mir[p] = m
inst_check = [0, 0, 0.0]
for x in rel:
    p, v, m = x['project'], x['version'], mir[x['project']]
    own = [m[x['d0'] + k * ONE][v] for k in (0, 1)]
    x['m2n'] = sum(n for day in own for c, n in day.items() if c.lower() in MIRROR)
    x['m2own'] = sum(sum(day.values()) for day in own)
    x['m1'] = {}
    for k in (0, 1, 2):
        day = m[x['d0'] + k * ONE]
        all_n = sum(sum(c.values()) for c in day.values())
        non = sum(n for w in day for c, n in day[w].items() if c.lower() not in MIRROR)
        at_all = sum(sum(day[w].values()) for w in day if w in x['at'])
        at_non = sum(n for w in day if w in x['at'] for c, n in day[w].items() if c.lower() not in MIRROR)
        x['m1'][k] = (at_all / all_n if all_n else None, at_non / non if non else None)
        # the installer table against the by-version table on days 0 to 2
        cd = x['d0'] + k * ONE
        if cd <= CUT and cd in counts[p] and all_n:
            bv = sum(counts[p][cd].values())
            inst_check[0] += 1
            inst_check[1] += all_n == bv
            inst_check[2] = max(inst_check[2], abs(all_n - bv) / bv)
    r_all = any(x['m1'][k][0] is not None and x['m1'][k][0] >= .5 for k in (1, 2))
    r_non = any(x['m1'][k][1] is not None and x['m1'][k][1] >= .5 for k in (1, 2))
    x['m1change'] = r_all != r_non
for b in 'AB':
    ps = [p for p in projects if proj[p]['band'] == b]
    pm_n = [statistics.median([x['m2n'] for x in rel if x['project'] == p]) for p in ps]
    pm_s = [statistics.median([100 * x['m2n'] / x['m2own'] for x in rel if x['project'] == p and x['m2own']]) for p in ps]
    pooled = 100 * sum(x['m2n'] for x in rel if x['band'] == b) / sum(x['m2own'] for x in rel if x['band'] == b)
    changed = set()
    for p in ps:
        rs = [x for x in rel if x['project'] == p]
        a = sum(any(x['m1'][k][0] is not None and x['m1'][k][0] >= .5 for k in (1, 2)) for x in rs)
        n = sum(any(x['m1'][k][1] is not None and x['m1'][k][1] >= .5 for k in (1, 2)) for x in rs)
        if (a > len(rs) / 2) != (n > len(rs) / 2):
            changed.add(p)
    print(f'   {b}: mirror downloads of the release on days 0 and 1, median of project medians {q(pm_n)[1]:.0f} (quartiles {q(pm_n)[0]:.0f}, {q(pm_n)[2]:.0f}); '
          f'share of own downloads {q(pm_s)[1]:.2f} per cent (quartiles {q(pm_s)[0]:.2f}, {q(pm_s)[2]:.2f}), pooled {pooled:.3f}; '
          f'releases whose "reached half" changes without mirrors {sum(x["m1change"] for x in rel if x["band"] == b)}; projects whose outcome changes {len(changed)}')
print(f'   installer table against by-version table on days 0 to 2: {inst_check[0]} release days, {inst_check[1]} identical, largest relative difference {100 * inst_check[2]:.2f} per cent')

# ---- CI, described ---------------------------------------------------------------------------------------
print('\n== the build-server flag (one release a project a month, days 0 to 2, pip and uv)')
ci_rows = {}
for p in projects:
    c = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))  # date -> version -> [pip/uv, pip/uv true, not known]
    for r in rd(DATA, 'ci', f'{p}.csv'):
        cell = c[D(r['date'])][r['version']]
        n = int(r['downloads'])
        if r['installer'] in ('pip', 'uv'):
            cell[0] += n
            cell[1] += n if r['ci'] == 'true' else 0
        else:
            cell[2] += n
    ci_rows[p] = c
ci_d = defaultdict(list)
ci_new, ci_old, nk = defaultdict(list), defaultdict(list), defaultdict(lambda: [0, 0])
for x in rel:
    if not x['ci']:
        continue
    p, c = x['project'], ci_rows[x['project']]
    days = [x['d0'] + k * ONE for k in (0, 1, 2)]
    if any(d in low_days for d in days):
        continue
    # amendment 1, case 1: a day the by-version table holds for the release with no CI row is a gap
    if any(d <= CUT and counts[p].get(d, {}).get(x['version'], 0) > 0 and x['version'] not in c.get(d, {}) for d in days):
        continue
    new = [sum(c[d][x['version']][i] for d in days) for i in range(3)]
    old = [sum(c[d][x['replaced']][i] for d in days) for i in range(3)]
    if new[0] == 0 or old[0] == 0:
        continue
    diff = 100 * (new[1] / new[0] - old[1] / old[0])
    ci_d[p].append(diff)
    ci_new[p].append(100 * new[1] / new[0])
    ci_old[p].append(100 * old[1] / old[0])
    nk[x['band']][0] += new[2] + old[2]
    nk[x['band']][1] += sum(new) + sum(old)
ci_int = {}
for b in 'AB':
    pm = [statistics.median(ci_d[p]) for p in projects if proj[p]['band'] == b and ci_d[p]]
    ci_int[b] = median_ci(pm)
    print(f'   {b}: {sum(len(ci_d[p]) for p in projects if proj[p]["band"] == b)} releases, {len(pm)} projects; median of project medians '
          f'{statistics.median(pm):.1f} points (interval {ci_int[b][0]:.1f} to {ci_int[b][1]:.1f}); below zero {sum(v < 0 for v in pm)}; '
          f'median project median CI share new {statistics.median([statistics.median(ci_new[p]) for p in projects if proj[p]["band"] == b and ci_new[p]]):.1f} '
          f'against replaced {statistics.median([statistics.median(ci_old[p]) for p in projects if proj[p]["band"] == b and ci_old[p]]):.1f}; '
          f'flag not known {100 * nk[b][0] / nk[b][1]:.1f} per cent')

# ---- without the overlap projects (the rng continues in the brief's order) --------------------------------
tests(lambda p: p not in overlap, ' without the overlap projects')
pm = [statistics.median(ci_d[p]) for p in projects if proj[p]['band'] == 'A' and p not in overlap and ci_d[p]]
lo, hi = median_ci(pm)
print(f'   CI A without overlap: median {statistics.median(pm):.1f} (interval {lo:.1f} to {hi:.1f})')

# ---- post hoc reading: without the tools and young projects -----------------------------------------------
post = {'hatch', 'editables', 'identify', 'cfgv', 'nodeenv', 'httpcore2', 'nab-index', 'pydantic-ai-shields'}
print('\n== post hoc: without the tools and young projects')
for b in 'AB':
    ps = [p for p in projects if proj[p]['band'] == b and proj[p]['most'] is not None]
    kept = [p for p in ps if p not in post]
    print(f'   {b}: named projects with a release {[p for p in ps if p in post]} (most reached: {[proj[p]["most"] for p in ps if p in post]}); '
          f'without them {sum(proj[p]["most"] for p in kept)} of {len(kept)} = {100 * sum(proj[p]["most"] for p in kept) / len(kept):.1f} per cent')

# ---- per-day table against by-version table ------------------------------------------------------------
cmp_n = cmp_same = 0
worst = 0.0
for p in projects:
    for d, byv in counts[p].items():
        if d in daily[p] and d <= CUT:
            bv, pd = sum(byv.values()), daily[p][d]
            cmp_n += 1
            cmp_same += bv == pd
            worst = max(worst, abs(bv - pd) / pd if pd else 0)
print(f'\n== per-day table against by-version table: {cmp_n} project-days, {cmp_same} identical, largest relative difference {100 * worst:.2f} per cent')

# ---- the figure's description ---------------------------------------------------------------------------
print('\n== the figure description: median day-1 shares by outcome')
for b in 'AB':
    yes = sorted(100 * proj[p]['md1'] for p in projects if proj[p]['band'] == b and proj[p]['most'])
    no = sorted(100 * proj[p]['md1'] for p in projects if proj[p]['band'] == b and proj[p]['most'] is False)
    print(f'   {b}: {len(yes)} dots from {yes[0]:.1f} to {yes[-1]:.1f}; {len(no)} squares from {no[0]:.1f} to {no[-1]:.1f}, '
          f'above 45: {[f"{v:.1f}" for v in no if v > 45]}')
top = rd(LH011, 'project_outcomes.csv')
k_share = next(k for k in top[0] if 'median_day1' in k)
k_most = next(k for k in top[0] if k.startswith('most'))
yes = sorted(100 * float(r[k_share]) for r in top if r[k_most] == 'yes')
no = sorted(100 * float(r[k_share]) for r in top if r[k_most] == 'no')
print(f'   top fifty ({k_most}, {k_share}): {len(yes)} dots from {yes[0]:.1f} to {yes[-1]:.1f}; {len(no)} squares from {no[0]:.1f} to {no[-1]:.1f}; '
      f'median of project medians {statistics.median(yes + no):.1f}')
for r in rd(LH011, 'summary.csv'):
    if 'interval' in ' '.join(r.values()).lower() and 'primary' in ' '.join(r.values()).lower():
        print('   LH011 summary:', dict(r))
