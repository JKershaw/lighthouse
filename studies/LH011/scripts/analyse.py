#!/usr/bin/env python3
"""LH011: offline analysis of the retained query results. No network. Standard-library Python 3 and
the `packaging` library (PEP 440 comparison).

Reads data/releases.csv, data/pypi_versions.csv, data/project_order.csv, data/daily_totals_*.csv,
data/counts/*.csv, data/ci/*.csv and data/pypistats/*.csv; writes, into $LH011_OUT (default
data/analysis/): gaps.csv, release_days.csv, release_outcomes.csv, project_outcomes.csv,
ci_releases.csv, ci_projects.csv, ci_installers.csv, described.csv, crosscheck_pypistats.csv and summary.csv.

Every rule is the brief's and amendment 1's: at-or-newer share = downloads that day of the release or
any higher non-pre-release version (PEP 440, versions listed by PyPI's JSON) over all the project's
downloads that day, both from pypi_downloads_per_day_by_version; reached half within two days = the
share is at least 0.5 on day 1 or day 2, unknown when neither reaches it and either is unknown; days
to half = first day 0 to 30 at 0.5 or more; a gap is a day with no row for a project that has rows on
the days either side, or a day whose total over the 50 projects is below half the median of days d-3
to d+3; CI share = pip and uv downloads flagged 'true' over all pip and uv downloads, days 0 to 2
pooled, new release minus replaced release in percentage points; projects are the unit, and
intervals are percentile intervals over 10,000 resamples of projects, seed 20260927.

Adapted from studies/LH005/scripts/analyse.py. What changed: LH005 described one release; this
computes the same share (numerator and denominator from the by-version table) for 424 releases, adds
the at-or-newer numerator, the gap rule, per-project aggregation, the project-resampled intervals,
the CI share restricted to installers whose flag rule was read, and the pypistats cross-check."""
import csv, datetime, glob, os, random, statistics
from collections import defaultdict
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
OUT = os.environ.get('LH011_OUT', os.path.join(DATA, 'analysis'))
os.makedirs(OUT, exist_ok=True)
LAST = datetime.date(2026, 9, 27)
D = datetime.date.fromisoformat
ONE = datetime.timedelta(days=1)
SEED, B = 20260927, 10000
KNOWN_FLAG = ('pip', 'uv')


def rd(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def wr(name, rows, fields=None):
    fields = fields or (list(rows[0].keys()) if rows else ['empty'])
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k, '')) for k in fields})


def fmt(x):
    if isinstance(x, float):
        return f'{x:.6f}'
    return x


def quart(xs):
    xs = sorted(xs)
    if not xs:
        return ('', '', '')
    q = statistics.quantiles(xs, n=4, method='inclusive') if len(xs) > 1 else [xs[0]] * 3
    return (q[0], statistics.median(xs), q[2])


def pct(xs, p):
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


releases = rd(os.path.join(DATA, 'releases.csv'))
order = rd(os.path.join(DATA, 'project_order.csv'))
versions = rd(os.path.join(DATA, 'pypi_versions.csv'))
nonpre = defaultdict(list)
for v in versions:
    if v['is_prerelease'] == 'False':
        nonpre[v['project']].append(v['version'])

# ---- gaps ---------------------------------------------------------------------------------------
totals = defaultdict(int)          # (project, date) -> downloads, pypi_downloads_per_day
for f in sorted(glob.glob(os.path.join(DATA, 'daily_totals_*.csv'))):
    for r in rd(f):
        totals[(r['project'], r['date'])] += int(r['downloads'])
all50 = defaultdict(int)
for (p, d), n in totals.items():
    all50[d] += n
days = sorted(all50)
gaps, gap_rows = set(), []   # (project or '*', date)
for i, d in enumerate(days):
    around = [all50[x] for x in days[max(0, i - 3): i + 4]]
    med = statistics.median(around)
    if all50[d] < 0.5 * med:
        gaps.add(('*', d))
        gap_rows.append(dict(project='*all 50*', date=d, rule='total below half the median of d-3..d+3',
                             value=all50[d], median=med))

counts = {}   # project -> {date: {v: n}}
for f in sorted(glob.glob(os.path.join(DATA, 'counts', '*.csv'))):
    p = os.path.basename(f)[:-4]
    c = defaultdict(dict)
    for r in rd(f):
        c[r['date']][r['v']] = c[r['date']].get(r['v'], 0) + int(r['downloads'])
    counts[p] = c
    ds = sorted(c)
    d, end = D(ds[0]), D(ds[-1])
    while d <= end:
        if str(d) not in c and str(d - ONE) in c and str(d + ONE) in c:
            gaps.add((p, str(d)))
            gap_rows.append(dict(project=p, date=str(d), rule='no row with rows either side', value='', median=''))
        d += ONE
wr('gaps.csv', gap_rows, ['project', 'date', 'rule', 'value', 'median'])


def is_gap(p, d):
    return ('*', d) in gaps or (p, d) in gaps


# ---- shares by release and day ------------------------------------------------------------------
day_rows, outcomes = [], []
for r in releases:
    p, rv = r['project'], Version(r['version'])
    newer = {v for v in nonpre[p] if Version(v) >= rv}
    c, d0 = counts[p], D(r['day0'])
    shares = {}
    for k in range(31):
        d = d0 + k * ONE
        ds = str(d)
        if d > LAST:
            status, tot, aon, own = 'censored (after last day held)', '', '', ''
        elif is_gap(p, ds):
            status, tot, aon, own = 'gap', '', '', ''
        else:
            row = c.get(ds, {})
            tot = sum(row.values())
            aon = sum(n for v, n in row.items() if v in newer)
            own = row.get(r['version'], 0)
            status = 'known' if tot > 0 else 'no downloads'
        sa = aon / tot if status == 'known' else None
        so = own / tot if status == 'known' else None
        shares[k] = sa
        day_rows.append(dict(project=p, version=r['version'], day=k, date=ds, status=status, total=tot,
                             at_or_newer=aon, own=own, share_at_or_newer=sa if sa is not None else '',
                             share_own=so if so is not None else ''))
    s1, s2 = shares[1], shares[2]
    if (s1 is not None and s1 >= 0.5) or (s2 is not None and s2 >= 0.5):
        reached = 'yes'
    elif s1 is None or s2 is None:
        reached = 'unknown'
    else:
        reached = 'no'
    dth, note = '', ''
    for k in range(31):
        if shares[k] is not None and shares[k] >= 0.5:
            dth = k
            if any(shares[j] is None for j in range(k)):
                note = 'an unknown day precedes it'
            break
    if dth == '':
        last_known = max([k for k in range(31) if shares[k] is not None], default='')
        note = f'not reached by day {last_known}' if last_known != '' else 'no known day'
    own_rows = [x for x in day_rows[-31:]]
    outcomes.append(dict(project=p, version=r['version'], day0=r['day0'], hours_left_in_day0=r['hours_left_in_day0'],
                         kind=r['kind'], released_again_within_7d=r['released_again_within_7d'], yanked=r['yanked'],
                         ci_subsample=r['ci_subsample'],
                         share_day0=shares[0] if shares[0] is not None else '',
                         share_day1=s1 if s1 is not None else '', share_day2=s2 if s2 is not None else '',
                         own_share_day1=own_rows[1]['share_own'], own_share_day2=own_rows[2]['share_own'],
                         reached_half_within_two_days=reached, days_to_half=dth, days_to_half_note=note))
wr('release_days.csv', day_rows)
wr('release_outcomes.csv', outcomes)

# ---- per project and across projects -----------------------------------------------------------
rng = random.Random(SEED)
proj_rows = []
for o in order:
    p = o['project']
    rs = [x for x in outcomes if x['project'] == p]
    known = [x for x in rs if x['reached_half_within_two_days'] != 'unknown']
    yes = sum(1 for x in known if x['reached_half_within_two_days'] == 'yes')
    d1 = [x['share_day1'] for x in rs if x['share_day1'] != '']
    dth = [x['days_to_half'] for x in rs if x['days_to_half'] != '']
    proj_rows.append(dict(sha256_order=o['sha256_order'], project=p, releases=len(rs), known=len(known), reached=yes,
                          share_reached=yes / len(known) if known else '',
                          most_reached=('yes' if yes * 2 > len(known) else 'no') if known else 'no outcome',
                          median_day1_share=statistics.median(d1) if d1 else '',
                          median_days_to_half_among_reaching=statistics.median(dth) if dth else '',
                          releases_not_reaching_half_by_day_30=sum(1 for x in rs if x['days_to_half'] == '')))
wr('project_outcomes.csv', proj_rows)
kp = [x for x in proj_rows if x['most_reached'] != 'no outcome']
flags = [1 if x['most_reached'] == 'yes' else 0 for x in kp]
share_proj = sum(flags) / len(flags)
boots = sorted(sum(rng.choice(flags) for _ in flags) / len(flags) for _ in range(B))
meds = [x['median_day1_share'] for x in kp if x['median_day1_share'] != '']
convention = ('as a rule' if share_proj >= 0.75 else 'not as a rule' if share_proj < 0.5 else 'for some projects')
kr = [x for x in outcomes if x['reached_half_within_two_days'] != 'unknown']
summary = [
    ('projects in frame', len(order)), ('projects with a qualifying release', sum(1 for x in proj_rows if x['releases'])),
    ('projects with a known outcome', len(kp)), ('projects where most releases reached half within two days', sum(flags)),
    ('share of projects', share_proj), ('share of projects, 95% interval low', pct(boots, 0.025)),
    ('share of projects, 95% interval high', pct(boots, 0.975)), ('reporting convention', convention),
    ('project median day-1 share: lower quartile', quart(meds)[0]), ('project median day-1 share: median', quart(meds)[1]),
    ('project median day-1 share: upper quartile', quart(meds)[2]),
    ('releases', len(outcomes)), ('releases with a known outcome', len(kr)),
    ('releases reaching half within two days (pooled)', sum(1 for x in kr if x['reached_half_within_two_days'] == 'yes')),
    ('pooled share of releases', sum(1 for x in kr if x['reached_half_within_two_days'] == 'yes') / len(kr)),
    ('releases with unknown outcome', len(outcomes) - len(kr)),
    ('gap days (all 50)', sum(1 for g in gaps if g[0] == '*')), ('gap days (project, no row)', sum(1 for g in gaps if g[0] != '*')),
]

# ---- CI ----------------------------------------------------------------------------------------
ci_rows = []
pooled, by_inst = defaultdict(int), defaultdict(int)
for r in releases:
    if r['ci_subsample'] != 'True':
        continue
    p = r['project']
    rows = rd(os.path.join(DATA, 'ci', f'{p}_{r["version"]}.csv'))
    a = defaultdict(int)
    for x in rows:
        side = 'new' if x['version'] == r['version'] else 'old'
        known = x['installer'] in KNOWN_FLAG and x['ci'] in ('true', 'false')
        key = f'{side}_{"known" if known else "unknown"}' + ('_true' if known and x['ci'] == 'true' else '')
        a[key] += int(x['downloads'])
        if x['ci'] == 'unknown':
            a['ci_value_unknown'] += int(x['downloads'])
        pooled['known' if known else 'unknown'] += int(x['downloads'])
        by_inst[x['installer'] or '(none recorded)'] += int(x['downloads'])
    gapdays = [k for k in range(3) if is_gap(p, str(D(r['day0']) + k * ONE))]
    nk, ok = a['new_known'] + a['new_known_true'], a['old_known'] + a['old_known_true']
    ns = a['new_known_true'] / nk if nk else None
    os_ = a['old_known_true'] / ok if ok else None
    diff = (ns - os_) * 100 if ns is not None and os_ is not None and not gapdays else None
    ci_rows.append(dict(project=p, version=r['version'], replaced_version=r['replaced_version'], day0=r['day0'],
                        kind=r['kind'], released_again_within_7d=r['released_again_within_7d'],
                        new_pip_uv=nk, new_pip_uv_ci_true=a['new_known_true'], new_flag_not_known=a['new_unknown'],
                        old_pip_uv=ok, old_pip_uv_ci_true=a['old_known_true'], old_flag_not_known=a['old_unknown'],
                        ci_value_unknown=a['ci_value_unknown'], gap_days=len(gapdays),
                        new_ci_share=ns if ns is not None else '', old_ci_share=os_ if os_ is not None else '',
                        diff_pp=diff if diff is not None else ''))
wr('ci_releases.csv', ci_rows)
tot_inst = sum(by_inst.values())
wr('ci_installers.csv', [dict(installer=k, downloads=v, share=v / tot_inst, flag_known=k in KNOWN_FLAG)
                         for k, v in sorted(by_inst.items(), key=lambda kv: -kv[1])])
ci_proj = []
for o in order:
    ds = [x['diff_pp'] for x in ci_rows if x['project'] == o['project'] and x['diff_pp'] != '']
    if ds:
        mine = [x for x in ci_rows if x['project'] == o['project'] and x['diff_pp'] != '']
        ci_proj.append(dict(project=o['project'], releases=len(ds), median_diff_pp=statistics.median(ds),
                            median_new_ci_share=statistics.median(x['new_ci_share'] for x in mine),
                            median_old_ci_share=statistics.median(x['old_ci_share'] for x in mine),
                            releases_new_below_old=sum(1 for d in ds if d < 0)))
wr('ci_projects.csv', ci_proj)
pm = [x['median_diff_pp'] for x in ci_proj]
cb = sorted(statistics.median([rng.choice(pm) for _ in pm]) for _ in range(B))
alld = [x['diff_pp'] for x in ci_rows if x['diff_pp'] != '']
summary += [
    ('CI: releases in subsample', len(ci_rows)), ('CI: releases with a known difference', len(alld)),
    ('CI: projects with a known difference', len(pm)),
    ('CI: median of project medians, pp', statistics.median(pm)),
    ('CI: median of project medians, 95% interval low', pct(cb, 0.025)),
    ('CI: median of project medians, 95% interval high', pct(cb, 0.975)),
    ('CI: projects whose median difference is below zero', sum(1 for d in pm if d < 0)),
    ('CI: median of project median new-release CI shares', statistics.median(x['median_new_ci_share'] for x in ci_proj)),
    ('CI: median of project median replaced-release CI shares', statistics.median(x['median_old_ci_share'] for x in ci_proj)),
    ('CI: pooled over releases, median difference pp', statistics.median(alld)),
    ('CI: releases with new share below old', sum(1 for d in alld if d < 0)),
    ('CI: downloads read (new and replaced, days 0-2)', pooled['known'] + pooled['unknown']),
    ('CI: share from installers whose flag is not known', pooled['unknown'] / (pooled['known'] + pooled['unknown'])),
    ('CI: downloads with the value unknown', sum(x['ci_value_unknown'] for x in ci_rows)),
    ('CI: pooled new-release CI share (pip, uv)', sum(x['new_pip_uv_ci_true'] for x in ci_rows) / sum(x['new_pip_uv'] for x in ci_rows)),
    ('CI: pooled replaced-release CI share (pip, uv)', sum(x['old_pip_uv_ci_true'] for x in ci_rows) / sum(x['old_pip_uv'] for x in ci_rows)),
]

# ---- described, not tested ----------------------------------------------------------------------
desc = []
cimap = {(x['project'], x['version']): x['diff_pp'] for x in ci_rows}
for dim in ('kind', 'released_again_within_7d'):
    for val in sorted({x[dim] for x in outcomes}):
        rs = [x for x in outcomes if x[dim] == val]
        kn = [x for x in rs if x['reached_half_within_two_days'] != 'unknown']
        d1 = [x['share_day1'] for x in rs if x['share_day1'] != '']
        cd = [cimap[(x['project'], x['version'])] for x in rs if cimap.get((x['project'], x['version']), '') != '']
        desc.append(dict(dimension=dim, value=val, releases=len(rs), projects=len({x['project'] for x in rs}),
                         known=len(kn), reached=sum(1 for x in kn if x['reached_half_within_two_days'] == 'yes'),
                         share_reached=(sum(1 for x in kn if x['reached_half_within_two_days'] == 'yes') / len(kn)) if kn else '',
                         median_day1_share=statistics.median(d1) if d1 else '',
                         ci_releases=len(cd), median_ci_diff_pp=statistics.median(cd) if cd else ''))
wr('described.csv', desc)

# ---- cross-check against pypistats "with mirrors" ------------------------------------------------
xc = []
for f in sorted(glob.glob(os.path.join(DATA, 'pypistats', '*_overall.csv'))):
    p = os.path.basename(f)[:-len('_overall.csv')]
    ps = {r['date']: int(r['downloads']) for r in rd(f) if r['category'] == 'with_mirrors'}
    first = min(D(x['day0']) for x in releases if x['project'] == p)
    for k in (1, 2, 3):
        d = str(first + k * ONE)
        cp = totals.get((p, d))
        pv = ps.get(d)
        bv = sum(counts[p].get(d, {}).values())
        xc.append(dict(project=p, date=d, clickpy_per_day=cp if cp is not None else '', clickpy_by_version=bv,
                       pypistats_with_mirrors=pv if pv is not None else '',
                       rel_diff=(cp - pv) / pv if cp is not None and pv else '',
                       over_5pct=(abs(cp - pv) / pv > 0.05) if cp is not None and pv else 'not held'))
wr('crosscheck_pypistats.csv', xc)
held = [x for x in xc if x['over_5pct'] != 'not held']
summary += [('cross-check days held by both', len(held)),
            ('cross-check days differing by more than 5%', sum(1 for x in held if x['over_5pct'] is True)),
            ('cross-check largest absolute relative difference', max(abs(x['rel_diff']) for x in held) if held else '')]
# the two ClickPy tables' daily totals, compared wherever both were read (a check on the denominator)
agree = [(totals[(p, d)], sum(c.values())) for p in counts for d, c in counts[p].items() if (p, d) in totals]
summary += [('per-day vs by-version table: project-days compared', len(agree)),
            ('per-day vs by-version table: project-days differing', sum(1 for a, b in agree if a != b)),
            ('per-day vs by-version table: largest relative difference', max(abs(a - b) / a for a, b in agree))]
summary += [('releases reaching half by day 30 (pooled)', sum(1 for x in outcomes if x['days_to_half'] != '')),
            ('releases reaching half: median days to half', statistics.median(x['days_to_half'] for x in outcomes if x['days_to_half'] != '')),
            ('projects with no release reaching half by day 30', sum(1 for x in proj_rows if x['releases'] and x['releases_not_reaching_half_by_day_30'] == x['releases']))]
wr('summary.csv', [dict(figure=k, value=v) for k, v in summary], ['figure', 'value'])
for k, v in summary:
    print(f'{k}: {fmt(v)}')
