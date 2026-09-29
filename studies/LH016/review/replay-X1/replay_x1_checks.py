#!/usr/bin/env python3
"""Replay X1 (stage two): checks on LH011 made from the retained analysis tables and frame files only
(data/analysis/release_days.csv, release_outcomes.csv, project_outcomes.csv, ci_releases.csv,
ci_projects.csv; data/releases.csv; data/projects.csv). Offline, standard library. Output:
replay_x1_checks.txt beside it. Run from anywhere: python3 studies/LH011/review/replay_x1_checks.py

What it asks, in order:
 1. the piece's opening figures for requests 2.34.0 and pandas 3.0.3 (day 1 and day 30);
 2. a recount of the headline (26 of 37 projects, 127 of 424 releases);
 3. whether "a new release was half" also holds by the release's OWN share, not at-or-newer;
 4. speed against level: each project's median share on days 1, 2, 7, 14 and 30, the drift from
    day 1 to day 30, and the older-version mass left at day 30, by group (most reached / none did);
 5. weekend against weekday: at-or-newer share and total downloads on days 3 to 30, by group, as a
    look at whether the plateau traffic is weekday (build) traffic;
 6. the CI figures; 7. the yanked pandas 3.0.4; 8. boto3 against botocore monthly totals;
 9. how many projects would count as reaching the threshold within two days if the threshold were not half."""
import csv, os, statistics, datetime
from collections import defaultdict

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
A = os.path.join(DATA, 'analysis')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'replay_x1_checks.txt')
lines = []
def say(s=''):
    lines.append(s)
def rd(p):
    return list(csv.DictReader(open(p)))
def med(xs):
    return statistics.median(xs) if xs else float('nan')
def q(xs, p):
    xs = sorted(xs); k = (len(xs) - 1) * p; lo = int(k); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)

days = rd(os.path.join(A, 'release_days.csv'))
outc = rd(os.path.join(A, 'release_outcomes.csv'))
proj = {r['project']: r for r in rd(os.path.join(A, 'project_outcomes.csv')) if r['releases'] != '0'}
rel = {(r['project'], r['version']): r for r in rd(os.path.join(DATA, 'releases.csv'))}
group = {p: ('yes' if proj[p]['most_reached'] == 'yes' else 'no') for p in proj}

# ---- 1. opening anecdote ---------------------------------------------------------------------------
say('1. The opening figures (from release_days.csv and releases.csv)')
for p, v in (('requests', '2.34.0'), ('pandas', '3.0.3')):
    r = rel[(p, v)]
    say(f'  {p} {v}: uploaded {r["first_upload_utc"][:16]}Z, replaced {r["replaced_version"]}, next newest {r["next_newest_version"]} after {r["hours_to_next_newest"]} h')
    for d in (0, 1, 2, 30):
        x = next(z for z in days if z['project'] == p and z['version'] == v and z['day'] == str(d))
        say(f'    day {d} ({x["date"]}): total {int(x["total"]):,}; at-or-newer {int(x["at_or_newer"]):,} = {100*float(x["share_at_or_newer"]):.1f}%; own {int(x["own"]):,} = {100*float(x["share_own"]):.1f}%')
say()

# ---- 2. recount ------------------------------------------------------------------------------------
say('2. Recount of the headline')
yes_p = [p for p in proj if group[p] == 'yes']; no_p = [p for p in proj if group[p] == 'no']
say(f'  projects with releases {len(proj)}; most releases reached half within two days: {len(yes_p)}; none/most not: {len(no_p)}')
say(f'  releases {len(outc)}; reached half within two days {sum(o["reached_half_within_two_days"] == "yes" for o in outc)}; unknown {sum(o["reached_half_within_two_days"] == "unknown" for o in outc)}')
say(f'  projects where NO release reached half within two days: {sum(1 for p in proj if proj[p]["reached"] == "0")}; every release did: {sum(1 for p in proj if proj[p]["reached"] == proj[p]["releases"])}')
say()

# ---- 3. own share ----------------------------------------------------------------------------------
say('3. Would the headline hold by the release\'s OWN share (not "this release or any later one")?')
own_reached = {}
for o in outc:
    s1 = float(o['own_share_day1']) if o['own_share_day1'] else None
    s2 = float(o['own_share_day2']) if o['own_share_day2'] else None
    own_reached[(o['project'], o['version'])] = ((s1 is not None and s1 >= 0.5) or (s2 is not None and s2 >= 0.5))
aon_yes = [o for o in outc if o['reached_half_within_two_days'] == 'yes']
say(f'  releases reaching half at-or-newer: {len(aon_yes)}; of these also by own share: {sum(own_reached[(o["project"], o["version"])] for o in aon_yes)}')
say(f'  releases reaching half by own share in all: {sum(own_reached.values())}')
own_proj_yes = 0
changed = []
for p in proj:
    rs = [o for o in outc if o['project'] == p]
    k = sum(own_reached[(p, o['version'])] for o in rs)
    most = k * 2 > len(rs)
    own_proj_yes += most
    if (group[p] == 'yes') != most:
        changed.append(f'{p} ({k} of {len(rs)} by own share)')
say(f'  projects where most releases reached half by own share: {own_proj_yes} of {len(proj)} (at-or-newer: {len(yes_p)}); projects that change group: {", ".join(changed) or "none"}')
# where the two measures differ, how soon the next release came
diff_rel = [o for o in aon_yes if not own_reached[(o['project'], o['version'])]]
say(f'  releases that reach half only at-or-newer: {len(diff_rel)}; hours to the next newest version among them: ' +
    ', '.join(f'{o["project"]} {o["version"]} {rel[(o["project"], o["version"])]["hours_to_next_newest"]}h' for o in diff_rel))
say()

# ---- 4. speed against level -------------------------------------------------------------------------
say('4. Speed against level: project medians of the at-or-newer share by day (releases with that day known), per cent')
by = defaultdict(lambda: defaultdict(list))
for z in days:
    if z['status'] == 'known' and z['share_at_or_newer']:
        by[z['project']][int(z['day'])].append(float(z['share_at_or_newer']))
M = {p: {d: 100 * med(by[p][d]) for d in range(31) if by[p].get(d)} for p in proj}
say(f'  {"project":20s} {"grp":3s} {"d1":>6s} {"d2":>6s} {"d7":>6s} {"d14":>6s} {"d30":>6s} {"d30-d1":>7s} {"d1/d30":>7s} {"older@30":>8s}')
drift = defaultdict(list); frac = defaultdict(list); left = defaultdict(list); step2 = defaultdict(list)
for p in sorted(proj, key=lambda p: (group[p] != 'yes', -M[p][1])):
    m = M[p]
    if 30 not in m:
        continue
    dr = m[30] - m[1]; fr = m[1] / m[30] if m[30] else float('nan')
    drift[group[p]].append(dr); frac[group[p]].append(fr); left[group[p]].append(100 - m[30]); step2[group[p]].append(m[2] - m[1])
    say(f'  {p:20s} {group[p]:3s} {m[1]:6.1f} {m[2]:6.1f} {m[7]:6.1f} {m[14]:6.1f} {m[30]:6.1f} {dr:+7.1f} {fr:7.2f} {100 - m[30]:8.1f}')
for g in ('yes', 'no'):
    say(f'  group {g}: n={len(drift[g])}; drift d30-d1 median {med(drift[g]):+.1f} pts (quartiles {q(drift[g], .25):+.1f} to {q(drift[g], .75):+.1f}, range {min(drift[g]):+.1f} to {max(drift[g]):+.1f});'
        f' d2-d1 median {med(step2[g]):+.1f}; share of the day-30 level already held on day 1: median {med(frac[g]):.2f} (range {min(frac[g]):.2f} to {max(frac[g]):.2f});'
        f' older-version share at day 30: median {med(left[g]):.0f}% (range {min(left[g]):.0f} to {max(left[g]):.0f})')
say(f'  projects rising more than 5 points from day 1 to day 30: yes-group {sum(d > 5 for d in drift["yes"])} of {len(drift["yes"])}, no-group {sum(d > 5 for d in drift["no"])} of {len(drift["no"])}')
# per release, no-group: drift distribution
nr = []
for o in outc:
    if group[o['project']] == 'no':
        s = {int(z['day']): float(z['share_at_or_newer']) for z in days if z['project'] == o['project'] and z['version'] == o['version'] and z['status'] == 'known' and z['share_at_or_newer']}
        if 1 in s and 30 in s:
            nr.append(100 * (s[30] - s[1]))
say(f'  no-group releases with day 30 held: {len(nr)}; per-release drift d30-d1: median {med(nr):+.1f} pts, quartiles {q(nr, .25):+.1f} to {q(nr, .75):+.1f}, max {max(nr):+.1f}')
say()

# ---- 5. weekend against weekday ----------------------------------------------------------------------
say('5. Weekend against weekday, days 3 to 30 of each release (UTC dates): per project, median over releases of')
say('   (median weekend at-or-newer share) - (median weekday share), points; and median weekend/weekday total downloads')
wk = defaultdict(list); vol = defaultdict(list)
per = defaultdict(lambda: defaultdict(lambda: {'we': [], 'wd': [], 'tv_we': [], 'tv_wd': []}))
for z in days:
    if z['status'] != 'known' or not z['share_at_or_newer'] or not (3 <= int(z['day']) <= 30):
        continue
    wd = datetime.date.fromisoformat(z['date']).weekday() >= 5
    e = per[z['project']][z['version']]
    e['we' if wd else 'wd'].append(float(z['share_at_or_newer']))
    e['tv_we' if wd else 'tv_wd'].append(int(z['total']))
rows5 = []
for p in proj:
    ds, vs = [], []
    for v, e in per[p].items():
        if e['we'] and e['wd']:
            ds.append(100 * (med(e['we']) - med(e['wd']))); vs.append(med(e['tv_we']) / med(e['tv_wd']))
    if ds:
        rows5.append((p, group[p], med(ds), med(vs))); wk[group[p]].append(med(ds)); vol[group[p]].append(med(vs))
for p, g, d, v in sorted(rows5, key=lambda r: (r[1] != 'yes', -r[2])):
    say(f'  {p:20s} {g:3s} share weekend-weekday {d:+6.1f} pts; downloads weekend/weekday {v:.2f}')
for g in ('yes', 'no'):
    say(f'  group {g}: share difference median {med(wk[g]):+.1f} pts (range {min(wk[g]):+.1f} to {max(wk[g]):+.1f}); weekend/weekday downloads median {med(vol[g]):.2f} (range {min(vol[g]):.2f} to {max(vol[g]):.2f})')
say()

# ---- 6. CI ----------------------------------------------------------------------------------------
say('6. CI figures (ci_releases.csv, ci_projects.csv)')
ci = rd(os.path.join(A, 'ci_releases.csv')); cp = rd(os.path.join(A, 'ci_projects.csv'))
dd = [float(r['diff_pp']) for r in ci if r['diff_pp']]
pm = [float(r['median_diff_pp']) for r in cp]
say(f'  releases {len(ci)}, known differences {len(dd)}, new below old {sum(d < 0 for d in dd)}; median of project medians {med(pm):.1f} pts; projects below zero {sum(d < 0 for d in pm)} of {len(pm)}')
say(f'  median project new share {100*med([float(r["median_new_ci_share"]) for r in cp]):.1f}%, replaced {100*med([float(r["median_old_ci_share"]) for r in cp]):.1f}%')
for r in cp:
    if r['project'] in ('boto3', 'botocore', 'litellm'):
        say(f'  {r["project"]}: median diff {float(r["median_diff_pp"]):+.2f}, new {100*float(r["median_new_ci_share"]):.1f}% vs old {100*float(r["median_old_ci_share"]):.1f}%, releases new below old {r["releases_new_below_old"]} of {r["releases"]}')
say('  CI share of the REPLACED release, no-group projects (a look at whether the plateau traffic is flagged more): ' +
    ', '.join(f'{r["project"]} {100*float(r["median_old_ci_share"]):.0f}%' for r in cp if group.get(r['project']) == 'no'))
say('  yes-group median of replaced-release CI share: ' + f'{100*med([float(r["median_old_ci_share"]) for r in cp if group.get(r["project"]) == "yes"]):.1f}%; no-group: {100*med([float(r["median_old_ci_share"]) for r in cp if group.get(r["project"]) == "no"]):.1f}%')
say()

# ---- 7. yanked pandas 3.0.4 -------------------------------------------------------------------------
say('7. pandas 3.0.4 (yanked): at-or-newer share by day')
say('  ' + ', '.join(f'd{z["day"]} {100*float(z["share_at_or_newer"]):.1f}%' for z in days if z['project'] == 'pandas' and z['version'] == '3.0.4' and z['status'] == 'known' and int(z['day']) <= 6))
say()

# ---- 8. boto3 vs botocore ---------------------------------------------------------------------------
say('8. Monthly totals, August 2026 (projects.csv): boto3 against the botocore it requires, and s3transfer')
pr = {r['project']: int(r['downloads_2026_08']) for r in rd(os.path.join(DATA, 'projects.csv'))}
say(f'  boto3 {pr["boto3"]:,}; botocore {pr["botocore"]:,} (ratio {pr["boto3"]/pr["botocore"]:.2f}); s3transfer {pr["s3transfer"]:,}; aiobotocore {pr["aiobotocore"]:,}')
say()
say('9. The half threshold: projects whose median day-1 at-or-newer share is at or above a threshold (37 projects)')
d1 = {p: M[p][1] for p in proj}
for t in (50, 40, 30, 25, 20, 10):
    n = sum(1 for p in proj if d1[p] >= t)
    say(f'  threshold {t:2d}%: {n} of 37 = {100*n/37:.0f}% ({"as a rule" if n/37 >= .75 else "not as a rule" if n/37 < .5 else "for some"} by the brief\'s convention)')
say('  the five mixed projects (most, not all, releases reached half) and their median day-1 shares: ' +
    ', '.join(f'{p} {d1[p]:.1f}' for p in proj if proj[p]['most_reached'] == 'yes' and proj[p]['reached'] != proj[p]['releases']))
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
