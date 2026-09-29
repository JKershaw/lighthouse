#!/usr/bin/env python3
"""LH014: offline analysis of the retained query results. No network. Python 3 with the `packaging`
library (PEP 440; 24.0 used).

Reads data/drawn.csv, releases.csv, pypi_versions.csv, daily_totals.csv, counts/, mirror/ and ci/, and
writes into $LH014_OUT (default data/analysis/): gaps.csv, release_days.csv, release_outcomes.csv,
mirror_releases.csv, ci_releases.csv, project_outcomes.csv (every per-project measure, CI and mirror
medians included), checks.csv and summary.csv.

The rules are the brief's (snapshot 31c19166...) and amendment 1's (ccb7a346...):
- at-or-newer share on day d: downloads that day of the release or any higher non-pre-release version
  PyPI lists, over all the project's downloads that day, both from the by-version table; own share
  likewise; reached half within two days: at least 0.5 on day 1 or day 2, unknown when neither reaches
  it and either is unknown; days to half: first day 0 to 30 at 0.5 or more;
- a day after 2026-09-27 is not read; a gap is a day with no row for a project that has rows on the
  days either side, or a day whose total over the 160 drawn projects (per-day table) is below half the
  median of the days read from d-3 to d+3; every measure on a gap, a censored day or a day with no
  downloads is unknown;
- settling (LH012): delta = share on day 30 minus share on day 2, in points; a release settles when
  |delta| <= 10; a project settles when more than half of its releases with a known delta do;
  descriptors: day-2 to day-30 ratio, and delta from day 1;
- a project's outcome: most (more than half) of its releases with a known outcome reached half;
  conventions: LH011's (as a rule >= 3/4, not as a rule < 1/2, for some projects between) and LH012's
  (holds as a rule >= 3/4, holds for some projects 1/2 to 3/4, fails < 1/2);
- CI share: pip and uv downloads flagged true over all pip and uv downloads, days 0 to 2 pooled, new
  minus replaced in points; unknown when either side has no pip or uv download, when a day is a gap, or
  (amendment 1, case 1) when the CI read has no row on a day the by-version table shows the release
  downloaded; installer names are matched exactly, so 'pip' followed by U+200B is flag not known;
- M1: at-or-newer share on days 0 to 2 from the installer table over all installers and without the
  mirror class, and the difference in points; M2: the mirror class's downloads of the release's own
  version on days 0 and 1, and their share of its own downloads, from the same table;
- intervals: percentile, linear interpolation, 10,000 resamples of a band's projects with a known
  measure, one random.Random(20260929) drawn in the order A primary, B primary, A settling, B settling,
  A CI, B CI, then the same six without the overlap projects.

Adapted from studies/LH011/scripts/analyse.py. What changed: two bands summarised separately; LH012's
settling test, convention and descriptors added; the gap rule's total is over the 160 drawn projects;
every day is cut at 27 September; the mirror readings M1 and M2 and the check of the installer table
against the by-version table are new, and the pypistats cross-check is dropped; the CI reads are one
file per project and carry amendment 1's gap rule; every band result is also computed without the
overlap projects; the kind-of-release breakdown is dropped (brief: no subgroup)."""
import csv, datetime, glob, os, random, statistics
from collections import defaultdict
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
OUT = os.environ.get('LH014_OUT', os.path.join(DATA, 'analysis'))
os.makedirs(OUT, exist_ok=True)
LAST, D, ONE = datetime.date(2026, 9, 27), datetime.date.fromisoformat, datetime.timedelta(days=1)
SEED, B = 20260929, 10000
KNOWN_FLAG = ('pip', 'uv')


def rd(path):
    with open(os.path.join(DATA, path) if not os.path.isabs(path) else path, newline='') as f:
        return list(csv.DictReader(f))


def fmt(x):
    return f'{x:.6f}' if isinstance(x, float) else x


def wr(name, rows, fields=None):
    fields = fields or (list(rows[0].keys()) if rows else ['empty'])
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k, '')) for k in fields})


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


med = lambda xs: statistics.median(xs) if xs else ''
drawn = rd('drawn.csv')
band_of = {d['project']: d['band'] for d in drawn}
overlap = {d['project'] for d in drawn if d['in_overlap_set'] == 'True'}
releases = rd('releases.csv')
nonpre = defaultdict(list)
for v in rd('pypi_versions.csv'):
    if v['parse'] == 'ok' and v['is_prerelease'] == 'False':
        nonpre[v['project']].append(v['version'])

# ---- gaps -----------------------------------------------------------------------------------------
totals = defaultdict(int)
for r in rd('daily_totals.csv'):
    totals[(r['project'], r['date'])] += int(r['downloads'])
alld = defaultdict(int)
for (p, d), n in totals.items():
    alld[d] += n
days = sorted(alld)
gaps, gap_rows = set(), []
for i, d in enumerate(days):
    m = statistics.median([alld[x] for x in days[max(0, i - 3): i + 4]])
    if alld[d] < 0.5 * m:
        gaps.add(('*', d))
        gap_rows.append(dict(project='*all drawn*', date=d, rule='total below half the median of d-3..d+3'))


def load(sub, key):
    out = {}
    for f in sorted(glob.glob(os.path.join(DATA, sub, '*.csv'))):
        c = defaultdict(lambda: defaultdict(int))
        for r in rd(f):
            c[r['date']][key(r)] += int(r['downloads'])
        out[os.path.basename(f)[:-4]] = c
    return out


counts = load('counts', lambda r: r['v'])
mirror = load('mirror', lambda r: (r['v'], r['installer_class']))
ci = load('ci', lambda r: (r['version'], r['installer'], r['ci']))
for p, c in counts.items():
    d, end = D(min(c)), D(max(c))
    while d <= end:
        if str(d) not in c and str(d - ONE) in c and str(d + ONE) in c:
            gaps.add((p, str(d)))
            gap_rows.append(dict(project=p, date=str(d), rule='no row with rows either side'))
        d += ONE
wr('gaps.csv', gap_rows, ['project', 'date', 'rule'])
is_gap = lambda p, ds: ('*', ds) in gaps or (p, ds) in gaps

# ---- shares, outcomes, settling and mirrors per release ---------------------------------------------------
day_rows, outcomes, mrows = [], [], []
for r in releases:
    p, v0 = r['project'], r['version']
    newer = {v for v in nonpre[p] if Version(v) >= Version(v0)}
    d0, sh = D(r['day0']), {}
    for k in range(31):
        d = d0 + k * ONE
        ds = str(d)
        tot = aon = own = ''
        if d > LAST:
            st = 'not read (after the cut)'
        elif is_gap(p, ds):
            st = 'gap'
        else:
            row = counts[p].get(ds, {})
            tot = sum(row.values())
            aon = sum(n for v, n in row.items() if v in newer)
            own = row.get(v0, 0)
            st = 'known' if tot > 0 else 'no downloads'
        sh[k] = aon / tot if st == 'known' else None
        day_rows.append(dict(band=r['band'], project=p, version=v0, day=k, date=ds, status=st, total=tot, at_or_newer=aon,
                             own=own, share_at_or_newer=sh[k] if sh[k] is not None else '',
                             share_own=own / tot if st == 'known' else ''))
    s1, s2, s30 = sh[1], sh[2], sh[30]
    reached = ('yes' if (s1 is not None and s1 >= .5) or (s2 is not None and s2 >= .5)
               else 'unknown' if s1 is None or s2 is None else 'no')
    dth = next((k for k in range(31) if sh[k] is not None and sh[k] >= .5), '')
    delta = (s30 - s2) * 100 if s2 is not None and s30 is not None else None
    outcomes.append(dict(band=r['band'], project=p, version=v0, day0=r['day0'], hours_left_in_day0=r['hours_left_in_day0'],
                         ci_subsample=r['ci_subsample'], share_day0=sh[0] if sh[0] is not None else '',
                         share_day1=s1 if s1 is not None else '', share_day2=s2 if s2 is not None else '',
                         share_day30=s30 if s30 is not None else '', reached_half_within_two_days=reached, days_to_half=dth,
                         delta_pp=delta if delta is not None else '', settles=(abs(delta) <= 10) if delta is not None else '',
                         ratio_day2_to_day30=(s2 / s30) if delta is not None and s30 > 0 else '',
                         delta_from_day1_pp=(s30 - s1) * 100 if s1 is not None and s30 is not None else ''))
    m = {}   # M1 and M2 from the installer table
    for k in range(3):
        d = d0 + k * ONE
        ds = str(d)
        row = mirror.get(p, {}).get(ds, {}) if d <= LAST and not is_gap(p, ds) else {}
        ta, tw = sum(row.values()), sum(n for (v, c), n in row.items() if c == '~not mirror')
        aa = sum(n for (v, c), n in row.items() if v in newer)
        aw = sum(n for (v, c), n in row.items() if v in newer and c == '~not mirror')
        m[k] = dict(all=aa / ta if ta else None, wo=aw / tw if tw else None, own=sum(n for (v, c), n in row.items() if v == v0),
                    mown=sum(n for (v, c), n in row.items() if v == v0 and c != '~not mirror'), tot=ta)
    reach = lambda key: ('yes' if any(m[k][key] is not None and m[k][key] >= .5 for k in (1, 2))
                         else 'unknown' if any(m[k][key] is None for k in (1, 2)) else 'no')
    own01 = m[0]['own'] + m[1]['own']
    mrows.append(dict(band=r['band'], project=p, version=v0, **{f'share_all_day{k}': m[k]['all'] if m[k]['all'] is not None else '' for k in range(3)},
                      **{f'share_without_mirrors_day{k}': m[k]['wo'] if m[k]['wo'] is not None else '' for k in range(3)},
                      **{f'diff_pp_day{k}': (m[k]['all'] - m[k]['wo']) * 100 if m[k]['all'] is not None and m[k]['wo'] is not None else '' for k in range(3)},
                      reached_all=reach('all'), reached_without_mirrors=reach('wo'),
                      mirror_own_day0=m[0]['mown'], mirror_own_day1=m[1]['mown'], own_day0=m[0]['own'], own_day1=m[1]['own'],
                      mirror_share_of_own_days01=(m[0]['mown'] + m[1]['mown']) / own01 if own01 else '',
                      installer_table_total_day0=m[0]['tot'], installer_table_total_day1=m[1]['tot'], installer_table_total_day2=m[2]['tot']))
wr('release_days.csv', day_rows)
wr('release_outcomes.csv', outcomes)
wr('mirror_releases.csv', mrows)

# ---- CI per subsample release --------------------------------------------------------------------------
ci_rows = []
for r in releases:
    if r['ci_subsample'] != 'True':
        continue
    p, new, old, d0 = r['project'], r['version'], r['replaced_version'], D(r['day0'])
    a, gapdays = defaultdict(int), 0
    for k in range(3):
        ds = str(d0 + k * ONE)
        row = ci.get(p, {}).get(ds, {})
        cells = {key: n for key, n in row.items() if key[0] in (new, old)}
        if is_gap(p, ds) or (not cells and counts[p].get(ds, {}).get(new, 0) > 0):
            gapdays += 1
        for (v, inst, flag), n in cells.items():
            side = 'new' if v == new else 'old'
            known = inst in KNOWN_FLAG and flag in ('true', 'false')
            a[f'{side}_{"known" if known else "unknown"}'] += n
            if known and flag == 'true':
                a[f'{side}_true'] += n
    ns = a['new_true'] / a['new_known'] if a['new_known'] else None
    os_ = a['old_true'] / a['old_known'] if a['old_known'] else None
    diff = (ns - os_) * 100 if ns is not None and os_ is not None and not gapdays else None
    ci_rows.append(dict(band=r['band'], project=p, version=new, replaced_version=old, day0=r['day0'], new_pip_uv=a['new_known'],
                        new_ci_true=a['new_true'], new_flag_not_known=a['new_unknown'], old_pip_uv=a['old_known'],
                        old_ci_true=a['old_true'], old_flag_not_known=a['old_unknown'], gap_days=gapdays,
                        new_ci_share=ns if ns is not None else '', old_ci_share=os_ if os_ is not None else '',
                        diff_pp=diff if diff is not None else ''))
wr('ci_releases.csv', ci_rows)

# ---- per project -------------------------------------------------------------------------------------------
proj = []
for dr in drawn:
    p = dr['project']
    rs = [x for x in outcomes if x['project'] == p]
    kn = [x for x in rs if x['reached_half_within_two_days'] != 'unknown']
    yes = sum(1 for x in kn if x['reached_half_within_two_days'] == 'yes')
    ks = [x for x in rs if x['delta_pp'] != '']
    st = sum(1 for x in ks if x['settles'])
    mr = [x for x in mrows if x['project'] == p]
    most = lambda key: (lambda kk: ('yes' if 2 * sum(1 for x in kk if x[key] == 'yes') > len(kk) else 'no') if kk else 'no outcome')(
        [x for x in mr if x[key] != 'unknown'])
    cd = [x['diff_pp'] for x in ci_rows if x['project'] == p and x['diff_pp'] != '']
    proj.append(dict(band=dr['band'], draw_order=dr['draw_order'], project=p, in_overlap_set=dr['in_overlap_set'],
                     releases=len(rs), known=len(kn), reached=yes,
                     most_reached=('yes' if 2 * yes > len(kn) else 'no') if kn else 'no outcome',
                     median_day1_share=med([x['share_day1'] for x in rs if x['share_day1'] != '']),
                     median_days_to_half=med([x['days_to_half'] for x in rs if x['days_to_half'] != '']),
                     releases_not_at_half_by_day_30=sum(1 for x in rs if x['days_to_half'] == ''),
                     delta_known=len(ks), settle=st, settles=('yes' if 2 * st > len(ks) else 'no') if ks else 'no outcome',
                     median_delta_pp=med([x['delta_pp'] for x in ks]),
                     median_ratio_day2_to_day30=med([x['ratio_day2_to_day30'] for x in ks if x['ratio_day2_to_day30'] != '']),
                     median_delta_from_day1_pp=med([x['delta_from_day1_pp'] for x in rs if x['delta_from_day1_pp'] != '']),
                     ci_releases=len(cd), median_ci_diff_pp=med(cd),
                     most_reached_installer_table=most('reached_all'), most_reached_without_mirrors=most('reached_without_mirrors'),
                     **{f'median_mirror_diff_pp_day{k}': med([x[f'diff_pp_day{k}'] for x in mr if x[f'diff_pp_day{k}'] != '']) for k in range(3)},
                     median_mirror_share_of_own_days01=med([x['mirror_share_of_own_days01'] for x in mr if x['mirror_share_of_own_days01'] != '']),
                     median_mirror_own_days01=med([x['mirror_own_day0'] + x['mirror_own_day1'] for x in mr])))
wr('project_outcomes.csv', proj)

# ---- across projects, per band, in the brief's order of random draws --------------------------------------
rng = random.Random(SEED)


def share_ci(flags):
    boots = [sum(rng.choice(flags) for _ in flags) / len(flags) for _ in range(B)]
    return pct(boots, .025), pct(boots, .975)


def median_ci(vals):
    boots = [statistics.median([rng.choice(vals) for _ in vals]) for _ in range(B)]
    return pct(boots, .025), pct(boots, .975)


summary = []
S = lambda band, fig, val: summary.append(dict(band=band, figure=fig, value=val))
for label, keep in (('', lambda p: True), (' (without the overlap projects)', lambda p: p['project'] not in overlap)):
    sel = {b: [p for p in proj if p['band'] == b and keep(p)] for b in 'AB'}
    for b in 'AB':
        kp = [p for p in sel[b] if p['most_reached'] != 'no outcome']
        f = [1 if p['most_reached'] == 'yes' else 0 for p in kp]
        s = sum(f) / len(f)
        lo, hi = share_ci(f)
        S(b, 'primary: projects with a known outcome' + label, len(kp))
        S(b, 'primary: projects whose releases mostly reached half within two days' + label, sum(f))
        S(b, 'primary: share' + label, s)
        S(b, 'primary: 95% interval low' + label, lo)
        S(b, 'primary: 95% interval high' + label, hi)
        S(b, 'primary: convention' + label, 'as a rule' if s >= .75 else 'not as a rule' if s < .5 else 'for some projects')
    for b in 'AB':
        kp = [p for p in sel[b] if p['settles'] != 'no outcome']
        f = [1 if p['settles'] == 'yes' else 0 for p in kp]
        s = sum(f) / len(f)
        lo, hi = share_ci(f)
        S(b, 'settling: projects with a known delta' + label, len(kp))
        S(b, 'settling: projects that settle' + label, sum(f))
        S(b, 'settling: share' + label, s)
        S(b, 'settling: 95% interval low' + label, lo)
        S(b, 'settling: 95% interval high' + label, hi)
        S(b, 'settling: convention' + label, 'holds as a rule' if s >= .75 else 'fails' if s < .5 else 'holds for some projects')
    for b in 'AB':
        pm = [p['median_ci_diff_pp'] for p in sel[b] if p['median_ci_diff_pp'] != '']
        lo, hi = median_ci(pm)
        S(b, 'CI: projects with a known difference' + label, len(pm))
        S(b, 'CI: median of project median differences, pp' + label, statistics.median(pm))
        S(b, 'CI: 95% interval low' + label, lo)
        S(b, 'CI: 95% interval high' + label, hi)
        S(b, 'CI: projects whose median difference is below zero' + label, sum(1 for x in pm if x < 0))

for b in 'AB':   # descriptions, no random draws
    ps = [p for p in proj if p['band'] == b and p['releases']]
    rs = [x for x in outcomes if x['band'] == b]
    kr = [x for x in rs if x['reached_half_within_two_days'] != 'unknown']
    q1, q2, q3 = quart([p['median_day1_share'] for p in ps if p['median_day1_share'] != ''])
    S(b, 'drawn projects', sum(1 for p in proj if p['band'] == b))
    S(b, 'projects with a qualifying release', len(ps))
    S(b, 'releases', len(rs))
    S(b, 'project median day-1 share: lower quartile', q1)
    S(b, 'project median day-1 share: median', q2)
    S(b, 'project median day-1 share: upper quartile', q3)
    S(b, 'projects where every release reached half', sum(1 for p in ps if p['known'] and p['reached'] == p['known']))
    S(b, 'projects where no release reached half', sum(1 for p in ps if p['known'] and p['reached'] == 0))
    S(b, 'pooled: releases with a known outcome', len(kr))
    S(b, 'pooled: releases that reached half within two days', sum(1 for x in kr if x['reached_half_within_two_days'] == 'yes'))
    S(b, 'pooled: releases reaching half by day 30', sum(1 for x in rs if x['days_to_half'] != ''))
    S(b, 'pooled: median days to half among them', med([x['days_to_half'] for x in rs if x['days_to_half'] != '']))
    S(b, 'projects with no release at half by day 30', sum(1 for p in ps if p['releases_not_at_half_by_day_30'] == p['releases']))
    ks = [x for x in rs if x['delta_pp'] != '']
    S(b, 'pooled: releases with a known delta', len(ks))
    S(b, 'pooled: releases that settle', sum(1 for x in ks if x['settles']))
    S(b, 'settling: median of project median delta, pp', med([p['median_delta_pp'] for p in ps if p['median_delta_pp'] != '']))
    S(b, 'settling: median of project median day-2 to day-30 ratio', med([p['median_ratio_day2_to_day30'] for p in ps if p['median_ratio_day2_to_day30'] != '']))
    S(b, 'settling: median of project median delta from day 1, pp', med([p['median_delta_from_day1_pp'] for p in ps if p['median_delta_from_day1_pp'] != '']))
    cr = [x for x in ci_rows if x['band'] == b]
    kn = sum(x['new_pip_uv'] + x['old_pip_uv'] for x in cr)
    un = sum(x['new_flag_not_known'] + x['old_flag_not_known'] for x in cr)
    S(b, 'CI: subsample releases', len(cr))
    S(b, 'CI: releases with a known difference', sum(1 for x in cr if x['diff_pp'] != ''))
    S(b, 'CI: releases with a CI gap day', sum(1 for x in cr if x['gap_days']))
    S(b, 'CI: share of subsample downloads whose flag is not known', un / (kn + un) if kn + un else '')
    S(b, 'CI: median of project median new-release shares', med([med([x['new_ci_share'] for x in cr if x['project'] == p['project'] and x['diff_pp'] != '']) for p in ps if any(x['project'] == p['project'] and x['diff_pp'] != '' for x in cr)]))
    S(b, 'CI: median of project median replaced-release shares', med([med([x['old_ci_share'] for x in cr if x['project'] == p['project'] and x['diff_pp'] != '']) for p in ps if any(x['project'] == p['project'] and x['diff_pp'] != '' for x in cr)]))
    for k in range(3):
        q = quart([p[f'median_mirror_diff_pp_day{k}'] for p in ps if p[f'median_mirror_diff_pp_day{k}'] != ''])
        S(b, f'M1: day {k} difference with and without mirrors, pp: lower quartile, median, upper quartile of project medians', ' | '.join(f'{v:.3f}' for v in q))
    ch = [p['project'] for p in ps if p['most_reached_installer_table'] != p['most_reached_without_mirrors']]
    S(b, 'M1: projects whose "most releases reached half" changes without mirrors', len(ch))
    S(b, 'M1: those projects', '; '.join(ch))
    q = quart([p['median_mirror_share_of_own_days01'] for p in ps if p['median_mirror_share_of_own_days01'] != ''])
    S(b, "M2: mirrors' share of a release's own downloads, days 0 and 1: lower quartile, median, upper quartile of project medians", ' | '.join(f'{v:.4f}' for v in q))
    q = quart([p['median_mirror_own_days01'] for p in ps])
    S(b, "M2: mirrors' downloads of a release on days 0 and 1: lower quartile, median, upper quartile of project medians", ' | '.join(f'{v:g}' for v in q))
    mr = [x for x in mrows if x['band'] == b]
    o01 = sum(x['own_day0'] + x['own_day1'] for x in mr)
    S(b, "M2: pooled mirror share of releases' own downloads, days 0 and 1", sum(x['mirror_own_day0'] + x['mirror_own_day1'] for x in mr) / o01 if o01 else '')
    S(b, 'LH012 dependents: releases with day 0 from 22 to 31 August', sum(1 for x in rs if x['project'] in {d['project'] for d in drawn if d['lh012_dependent'] == 'True'} and '2026-08-22' <= x['day0'] <= '2026-08-31'))
S('', 'gap days (all drawn projects)', sum(1 for g in gaps if g[0] == '*'))
S('', 'gap days (project, no row)', sum(1 for g in gaps if g[0] != '*'))

# ---- ClickPy's two-table checks --------------------------------------------------------------------------
checks = []
for name, pairs in (('per-day table against by-version table, project-days read in both',
                     [(totals[(p, d)], sum(c.values())) for p, cc in counts.items() for d, c in cc.items() if (p, d) in totals]),
                    ('installer table against by-version table, release days 0 to 2',
                     [(sum(mm.values()), sum(counts[p].get(d, {}).values())) for p, md in mirror.items() for d, mm in md.items() if d in counts[p]])):
    diff = [abs(a - b) / a for a, b in pairs if a and a != b]
    checks.append(dict(check=name, compared=len(pairs), identical=sum(1 for a, b in pairs if a == b),
                       differing=len(diff), over_5_percent=sum(1 for x in diff if x > .05),
                       largest_relative_difference=max(diff) if diff else 0.0))
wr('checks.csv', checks)
wr('summary.csv', summary, ['band', 'figure', 'value'])
for s in summary:
    if not s['figure'].startswith('M1: those'):
        print(f"{s['band'] or '-'} | {s['figure']}: {fmt(s['value'])}")
for c in checks:
    print(c)
