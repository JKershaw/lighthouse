#!/usr/bin/env python3
"""Independent reproduction of LH011's pace result from the retained data and the brief alone.

Written 8 November 2026 by a fresh agent (Fable 5.1) that had read studies/LH011/brief.md (with
amendment 1), sources.md, replay.sh, the data files' headers and the scripts' docstrings, and had not
read LH011.md, data/analysis/, review/ or the pieces. Written without running or reading the body of
studies/LH011/scripts/analyse.py or frame.py.

Reads, from studies/LH011/data/: projects.csv, pypi_versions.csv, counts/*.csv, daily_totals_*.csv,
and releases.csv only to compare the frame I derive with the one amendment 1 committed before any
count was read. Writes into the output directory given as the first argument (default: ../output):
  frame_diff.txt         my frame against data/releases.csv
  release_outcomes.csv   per release: day 0, shares on days 0 to 2, reached-half class, days to half
  project_outcomes.csv   per project: releases, known, reached, share, class, median day-1 share
  summary.txt            the headline figures and the bootstrap interval

Rules, as the brief and amendment 1 fix them:
- Qualifying release: not a PEP 440 pre-release or dev release; first file uploaded in
  [2026-04-01T00:00:00Z, 2026-08-31T23:59:59Z]; higher than every earlier-uploaded non-pre-release
  version. Yanked versions kept.
- Day 0 = UTC day of first upload; days 1 and 2 the next two UTC days.
- At-or-newer share on day d = downloads that day of the release or any higher non-pre-release
  version listed by PyPI's JSON, over all the project's downloads that day (all rows, '~other'
  included), both from pypi_downloads_per_day_by_version (the counts files).
- Gap: a day with no row for the project in pypi_downloads_per_day although both neighbours have one;
  or a day whose total over the 50 projects is below half the median of days d-3 to d+3. A measure
  on a gap day is unknown.
- Reached half within two days: share >= 0.5 on day 1 or day 2; unknown if neither reaches it and
  either is unknown; else no.
- Days to half: first day 0..30 (or to the last day held, 2026-09-27) with share >= 0.5.
- Per project: share of releases with a known outcome that reached half; "most" = more than half;
  a project has a known outcome when at least one release does. Across projects: how many had most
  reach half, median and quartiles of the projects' median day-1 shares, and a project-resampled
  95 per cent percentile interval, 10,000 resamples, seed 20260927.
Standard library plus `packaging` for PEP 440.
"""
import csv, datetime, glob, os, random, statistics, sys
from collections import defaultdict
from packaging.version import Version, InvalidVersion

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(ROOT, 'studies', 'LH011', 'data')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'output')
os.makedirs(OUT, exist_ok=True)

D = datetime.date.fromisoformat
ONE = datetime.timedelta(days=1)
LAST_HELD = D('2026-09-27')
WIN_START = datetime.datetime(2026, 4, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
WIN_END = datetime.datetime(2026, 8, 31, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc)


def read(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def ts(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))


# ---------------------------------------------------------------- 1. the frame
projects = [r['project'] for r in read(os.path.join(DATA, 'projects.csv')) if r['status'] == 'selected']
assert len(projects) == 50, len(projects)

versions = defaultdict(list)   # project -> [(Version, version string, first upload datetime, yanked)]
unparsed = 0
for r in read(os.path.join(DATA, 'pypi_versions.csv')):
    if r['project'] not in projects:
        continue
    try:
        v = Version(r['version'])
    except InvalidVersion:
        unparsed += 1
        continue
    if v.is_prerelease or v.is_devrelease:     # PEP 440 pre-release or development release
        continue
    versions[r['project']].append((v, r['version'], ts(r['first_upload_utc']), r['any_yanked'] == 'True'))

releases = []      # dicts
for p in projects:
    vs = sorted(versions[p], key=lambda t: t[2])    # by first upload
    newest = None   # (Version, string, upload)
    for v, s, up, yanked in vs:
        if newest is None or v > newest[0]:
            if WIN_START <= up <= WIN_END:
                releases.append(dict(project=p, version=s, V=v, upload=up, day0=up.date(),
                                     replaced=newest[1] if newest else '', yanked=yanked))
            newest = (v, s, up)
releases.sort(key=lambda r: (r['project'], r['upload']))

# compare with the frame amendment 1 committed before any count was read
theirs = read(os.path.join(DATA, 'releases.csv'))
mine_keys = {(r['project'], r['version']) for r in releases}
their_keys = {(r['project'], r['version']) for r in theirs}
their_by = {(r['project'], r['version']): r for r in theirs}
frame_lines = [f"my qualifying releases: {len(releases)} in {len({r['project'] for r in releases})} projects; "
               f"data/releases.csv: {len(theirs)} in {len({r['project'] for r in theirs})} projects",
               f"only mine: {sorted(mine_keys - their_keys)}", f"only theirs: {sorted(their_keys - mine_keys)}",
               f"versions that did not parse as PEP 440 (skipped): {unparsed}"]
mismatch = []
for r in releases:
    t = their_by.get((r['project'], r['version']))
    if t and (t['day0'] != r['day0'].isoformat() or t['replaced_version'] != r['replaced']):
        mismatch.append((r['project'], r['version'], r['day0'].isoformat(), t['day0'], r['replaced'], t['replaced_version']))
frame_lines.append(f"day0/replaced mismatches among shared releases: {mismatch}")
with open(os.path.join(OUT, 'frame_diff.txt'), 'w') as f:
    f.write('\n'.join(frame_lines) + '\n')
print('\n'.join(frame_lines))

# ---------------------------------------------------------------- 2. the counts
counts = {}   # project -> date -> {version: downloads}
for p in projects:
    path = os.path.join(DATA, 'counts', f'{p}.csv')
    if not os.path.exists(path):
        continue
    byday = defaultdict(dict)
    with open(path, newline='') as f:
        for row in csv.reader(f):
            if not row or row[0] == 'date':      # header, possibly repeated where a query was split
                continue
            d, v, n = row[0], row[1], int(row[2])
            byday[d][v] = byday[d].get(v, 0) + n   # a split query could repeat a (date, v) pair; summing is the safe reading
    counts[p] = byday

# daily totals for the gap rule (pypi_downloads_per_day over the 50 projects)
totals = defaultdict(dict)    # project -> date -> downloads
for path in sorted(glob.glob(os.path.join(DATA, 'daily_totals_*.csv'))):
    for r in read(path):
        totals[r['project']][r['date']] = int(r['downloads'])
all_days = sorted({d for p in totals for d in totals[p]}, key=D)
sum50 = {d: sum(totals[p].get(d, 0) for p in projects) for d in all_days}


def is_gap(p, day):
    """The brief's two clauses. Clause 1: no row for the project on a day whose two neighbours have rows.
    Clause 2: the 50-project total is below half the median of days d-3..d+3 (d included)."""
    s = day.isoformat()
    before, after = (day - ONE).isoformat(), (day + ONE).isoformat()
    if s not in totals[p] and before in totals[p] and after in totals[p]:
        return True, 'no row'
    window = [sum50[(day + k * ONE).isoformat()] for k in range(-3, 4) if (day + k * ONE).isoformat() in sum50]
    if s in sum50 and window and sum50[s] < 0.5 * statistics.median(window):
        return True, 'low total'
    return False, ''


def share(p, release_V, day):
    """At-or-newer share on a day, or None when unknown (gap, no rows, or day beyond the last held)."""
    if day > LAST_HELD:
        return None
    gap, _ = is_gap(p, day)
    if gap:
        return None
    rows = counts.get(p, {}).get(day.isoformat())
    if not rows:
        return None
    denom = sum(rows.values())
    if denom == 0:
        return None
    num = 0
    for v, n in rows.items():
        if v == '~other':
            continue
        try:
            if Version(v) >= release_V and not Version(v).is_prerelease:
                num += n
        except InvalidVersion:
            pass
    return num / denom


# a version in the numerator must be one PyPI lists (reading 2); every explicit row in the counts is
# a version in some release's numerator set, so the string match above suffices, but check it:
listed = {p: {s for _, s, _, _ in versions[p]} for p in projects}
stray = {(p, v) for p in counts for d in counts[p] for v in counts[p][d] if v != '~other' and v not in listed[p]}
print('explicit count versions not in PyPI\'s non-pre-release list:', sorted(stray)[:20], len(stray))

# ---------------------------------------------------------------- 3. per release
out_rows = []
for r in releases:
    p, V, d0 = r['project'], r['V'], r['day0']
    s = [share(p, V, d0 + k * ONE) for k in range(0, 31)]
    s1, s2 = s[1], s[2]
    if (s1 is not None and s1 >= 0.5) or (s2 is not None and s2 >= 0.5):
        reached = 'yes'
    elif s1 is None or s2 is None:
        reached = 'unknown'
    else:
        reached = 'no'
    days_to_half = ''
    for k in range(31):
        if s[k] is not None and s[k] >= 0.5:
            days_to_half = k
            break
    if days_to_half == '':
        last_read = max((k for k in range(31) if s[k] is not None), default=None)
        days_to_half = 'not by day 30' if (d0 + 30 * ONE) <= LAST_HELD else f'not by last day held (day {last_read})'
    r.update(s0=s[0], s1=s1, s2=s2, reached=reached, days_to_half=days_to_half)
    out_rows.append(dict(project=p, version=r['version'], day0=d0.isoformat(), replaced=r['replaced'], yanked=r['yanked'],
                         share_day0='' if s[0] is None else f'{s[0]:.4f}', share_day1='' if s1 is None else f'{s1:.4f}',
                         share_day2='' if s2 is None else f'{s2:.4f}', reached_half_within_2d=reached, days_to_half=days_to_half))
with open(os.path.join(OUT, 'release_outcomes.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
    w.writeheader(); w.writerows(out_rows)

# ---------------------------------------------------------------- 4. per project
proj = {}
for p in sorted({r['project'] for r in releases}):
    rs = [r for r in releases if r['project'] == p]
    known = [r for r in rs if r['reached'] != 'unknown']
    yes = [r for r in known if r['reached'] == 'yes']
    d1 = [r['s1'] for r in rs if r['s1'] is not None]
    cls = 'no known outcome'
    frac = None
    if known:
        frac = len(yes) / len(known)
        cls = 'most reached' if frac > 0.5 else ('none reached' if len(yes) == 0 else 'some, not most')
    proj[p] = dict(project=p, releases=len(rs), known=len(known), reached=len(yes), unknown=len(rs) - len(known),
                   share_reached='' if frac is None else f'{frac:.3f}', cls=cls,
                   median_day1_share='' if not d1 else f'{statistics.median(d1):.4f}',
                   n_not_by_30=sum(1 for r in rs if str(r['days_to_half']).startswith('not by day 30')),
                   n_censored=sum(1 for r in rs if str(r['days_to_half']).startswith('not by last')))
with open(os.path.join(OUT, 'project_outcomes.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(next(iter(proj.values())).keys()))
    w.writeheader(); w.writerows(proj.values())

# ---------------------------------------------------------------- 5. summary and bootstrap
known_projects = [v for v in proj.values() if v['known'] > 0]
most = [v for v in known_projects if v['cls'] == 'most reached']
none = [v for v in known_projects if v['cls'] == 'none reached']
some = [v for v in known_projects if v['cls'] == 'some, not most']
pooled_known = sum(v['known'] for v in known_projects)
pooled_yes = sum(v['reached'] for v in known_projects)
pooled_unknown = sum(v['unknown'] for v in proj.values())
medians = sorted(float(v['median_day1_share']) for v in proj.values() if v['median_day1_share'] != '')
q = statistics.quantiles(medians, n=4, method='inclusive') if len(medians) >= 2 else []

rng = random.Random(20260927)
flags = [1 if v['cls'] == 'most reached' else 0 for v in known_projects]
boots = []
for _ in range(10000):
    sample = rng.choices(flags, k=len(flags))
    boots.append(sum(sample) / len(sample))
boots.sort()
lo, hi = boots[int(0.025 * len(boots))], boots[int(0.975 * len(boots)) - 1]
# a second convention, in case the original used nearest-rank percentiles differently
lo2 = statistics.quantiles(boots, n=40, method='inclusive')[0]
hi2 = statistics.quantiles(boots, n=40, method='inclusive')[-1]
# the same bootstrap for the median of project medians
rng2 = random.Random(20260927)
mb = sorted(statistics.median(rng2.choices(medians, k=len(medians))) for _ in range(10000))

frac_most = len(most) / len(known_projects)
convention = 'as a rule' if frac_most >= 0.75 else ('not as a rule' if frac_most < 0.5 else 'for some projects')
lines = [
    f"qualifying releases: {len(releases)}; projects that released: {len(proj)}; projects with a known outcome: {len(known_projects)}",
    f"projects where most releases reached half within two days: {len(most)} of {len(known_projects)} ({frac_most:.3f}) -> '{convention}'",
    f"projects where no release reached half within two days: {len(none)}",
    f"projects where some but not most reached: {len(some)}: {[v['project'] for v in some]}",
    f"project-resampled 95% interval for the share of projects (10,000 resamples, seed 20260927, random.choices): "
    f"{lo:.3f} to {hi:.3f} (index convention) / {lo2:.3f} to {hi2:.3f} (inclusive quantiles)",
    f"pooled over releases: {pooled_yes} of {pooled_known} known reached half within two days ({pooled_yes / pooled_known:.3f}); unknown: {pooled_unknown}",
    f"projects' median day-1 at-or-newer share: median {statistics.median(medians):.3f}, quartiles {q[0]:.3f} and {q[2]:.3f} (n={len(medians)})",
    f"bootstrap of that median: {mb[int(0.025 * len(mb))]:.3f} to {mb[int(0.975 * len(mb)) - 1]:.3f}",
    f"releases not at half by day 30: {sum(v['n_not_by_30'] for v in proj.values())}; censored at the last day held: {sum(v['n_censored'] for v in proj.values())}",
    "",
    "projects where most reached: " + ', '.join(f"{v['project']} {v['reached']}/{v['known']}" for v in most),
    "projects where none reached: " + ', '.join(f"{v['project']} 0/{v['known']}" for v in none),
    "",
    "gap days found (project, day, clause) among the days used:",
]
gaps_seen = set()
for r in releases:
    for k in range(31):
        day = r['day0'] + k * ONE
        if day <= LAST_HELD:
            g, why = is_gap(r['project'], day)
            if g:
                gaps_seen.add((r['project'], day.isoformat(), why))
lines.append('  ' + (str(sorted(gaps_seen)) if gaps_seen else 'none'))
with open(os.path.join(OUT, 'summary.txt'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('\n'.join(lines))
