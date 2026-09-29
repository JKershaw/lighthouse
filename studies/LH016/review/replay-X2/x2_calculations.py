#!/usr/bin/env python3
"""Replay X2 (notes/replay-X2.md), stage 2: calculations the record does not report, from the retained
files only (data/counts/*.csv, data/releases.csv, data/pypi_versions.csv, data/projects.csv,
data/analysis/project_outcomes.csv). No network. Standard library plus `packaging`.

1. Thinning of the pre-April population: for each project, the share of its daily downloads that fell
   in '~other' (every version older than the project's first qualifying release, plus pre-releases
   and versions PyPI does not list) on day 1 after its first release and at the end of its retained
   window, and for the eleven plateau projects by 30-day step. This is the pace of the population
   that does not take a release, over five months rather than thirty days.
2. Age mix of a full month's downloads (the last 28 days each project's file holds): versions at most
   30 days old, versions 31 days to the first qualifying release, and older ('~other').
3. boto3 against botocore, month by month: downloads of versions at most 30 days old and of older
   versions, and their ratios; the August totals of the four AWS libraries and their named dependents.
4. The share of projects under other units: the four AWS libraries as one unit; protobuf and
   grpcio-status as one.
5. Pre-release versions uploaded in the window per project (they fall into '~other').
Output: x2_calculations.txt beside it.  Run: python3 studies/LH011/review/x2_calculations.py"""
import csv, datetime, glob, os, statistics
from collections import defaultdict
from packaging.version import Version

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'x2_calculations.txt')
D = datetime.date.fromisoformat
ONE = datetime.timedelta(days=1)
lines = []
say = lines.append


def rd(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


releases = rd('releases.csv')
versions = rd('pypi_versions.csv')
po = {r['project']: r for r in rd('analysis/project_outcomes.csv') if r['releases'] != '0'}
upload = {(v['project'], v['version']): D(v['first_upload_utc'][:10]) for v in versions}
first_day0 = {}
for r in releases:
    p = r['project']
    first_day0[p] = min(first_day0.get(p, D(r['day0'])), D(r['day0']))
counts = {}
for f in sorted(glob.glob(os.path.join(DATA, 'counts', '*.csv'))):
    p = os.path.basename(f)[:-4]
    c = defaultdict(dict)
    with open(f) as fh:
        for r in csv.DictReader(fh):
            c[r['date']][r['v']] = c[r['date']].get(r['v'], 0) + int(r['downloads'])
    counts[p] = c
yes = sorted(p for p in po if po[p]['most_reached'] == 'yes')
no = sorted(p for p in po if po[p]['most_reached'] == 'no')


def other_share(p, d):
    row = counts[p].get(str(d))
    if not row:
        return None
    tot = sum(row.values())
    return row.get('~other', 0) / tot if tot else None


def mean_share(p, days):
    xs = [other_share(p, d) for d in days]
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


# ---- 1. thinning of the pre-April population -----------------------------------------------------
say('1. Share of each project\'s daily downloads on versions older than its first qualifying release ("~other";')
say('   pre-releases and unlisted versions are in it too), on day 1 after that release and over the last seven')
say('   days the project\'s file holds (30 days after its last release, or 27 September). Days = days from the')
say('   first release\'s day 0 to the last day held.')
say(f'   {"project":<20}{"group":<6}{"first day0":<12}{"last day":<12}{"days":>5}{"day-1 other":>13}{"last-7d other":>15}{"change":>9}')
thin = {}
for grp, ps in (('yes', yes), ('no', no)):
    for p in ps:
        d0 = first_day0[p]
        last = D(max(counts[p]))
        a = other_share(p, d0 + ONE)
        b = mean_share(p, [last - k * ONE for k in range(7)])
        thin[p] = (a, b, (last - d0).days)
        say(f'   {p:<20}{grp:<6}{str(d0):<12}{str(last):<12}{(last - d0).days:>5}{a * 100:>12.1f}%{b * 100:>14.1f}%{(b - a) * 100:>+8.1f}')
for grp, ps in (('26 that reached half', yes), ('eleven that did not', no)):
    ch = [thin[p][1] - thin[p][0] for p in ps]
    say(f'   {grp}: median change in the ~other share from day 1 to the last week, {statistics.median(ch) * 100:+.1f} points '
        f'(range {min(ch) * 100:+.1f} to {max(ch) * 100:+.1f}); median days spanned {statistics.median(thin[p][2] for p in ps):.0f}')
say('')
say('   The eleven by 30-day step from the first release (~other share, 7-day mean centred on the step, per cent):')
say(f'   {"project":<16}' + ''.join(f'{"d" + str(k):>8}' for k in (1, 30, 60, 90, 120, 150, 179)))
for p in sorted(no, key=lambda p: first_day0[p]):
    d0 = first_day0[p]
    cells = []
    for k in (1, 30, 60, 90, 120, 150, 179):
        if k == 1:
            v = other_share(p, d0 + ONE)
        else:
            v = mean_share(p, [d0 + (k + j) * ONE for j in range(-3, 4)])
        cells.append(f'{v * 100:>8.1f}' if v is not None else f'{"-":>8}')
    say(f'   {p:<16}' + ''.join(cells))
say('')

# ---- 2. age mix over the last 28 days held --------------------------------------------------------
say('2. Age mix of downloads over the last 28 days each project\'s file holds: versions at most 30 days old on the')
say('   day of download, versions 31 days old to the first qualifying release (April to August), and older')
say('   ("~other", uploaded before April or pre-release). Per cent of the 28 days\' downloads.')
say(f'   {"project":<20}{"group":<6}{"window end":<12}{"<=30d":>8}{"31d-Apr":>9}{"pre-Apr":>9}{"downloads/day":>15}')
mix = {}
for grp, ps in (('yes', yes), (' no', no)):
    for p in ps:
        last = D(max(counts[p]))
        fresh = mid = other = 0
        for k in range(28):
            d = last - k * ONE
            row = counts[p].get(str(d), {})
            for v, n in row.items():
                if v == '~other':
                    other += n
                elif (d - upload[(p, v)]).days <= 30:
                    fresh += n
                else:
                    mid += n
        tot = fresh + mid + other
        mix[p] = (fresh / tot, mid / tot, other / tot, tot / 28)
        say(f'   {p:<20}{grp.strip():<6}{str(last):<12}{fresh / tot * 100:>7.1f}%{mid / tot * 100:>8.1f}%{other / tot * 100:>8.1f}%{tot / 28:>15,.0f}')
say('')

# ---- 3. boto3 against botocore --------------------------------------------------------------------
say('3. boto3 against botocore (and s3transfer, aiobotocore): downloads of versions at most 30 days old and of')
say('   older versions, by calendar month, in millions a day. boto3 requires botocore, so a fresh install of')
say('   boto3 into an empty environment fetches both.')
months = [(2026, m) for m in (5, 6, 7, 8, 9)]
fam = ['boto3', 'botocore', 's3transfer', 'aiobotocore']
say(f'   {"month":<10}' + ''.join(f'{p + " fresh":>18}{p + " old":>16}' for p in fam))
famtab = {}
for (y, m) in months:
    cells = []
    for p in fam:
        fresh = old = days = 0
        d = datetime.date(y, m, 1)
        while d.month == m:
            row = counts[p].get(str(d))
            if row:
                days += 1
                for v, n in row.items():
                    if v != '~other' and (d - upload[(p, v)]).days <= 30:
                        fresh += n
                    else:
                        old += n
            d += ONE
        famtab[(p, m)] = (fresh / days / 1e6 if days else None, old / days / 1e6 if days else None, days)
        cells.append(f'{famtab[(p, m)][0]:>18.1f}{famtab[(p, m)][1]:>16.1f}' if days else f'{"-":>18}{"-":>16}')
    say(f'   {y}-{m:02d}  ' + ''.join(cells))
for m in (5, 6, 7, 8):
    b, c = famtab[('boto3', m)], famtab[('botocore', m)]
    say(f'   {2026}-{m:02d}: boto3 fresh / botocore fresh = {b[0] / c[0]:.2f}; boto3 old / botocore old = {b[1] / c[1]:.2f}; '
        f'boto3 total / botocore total = {(b[0] + b[1]) / (c[0] + c[1]):.2f}')
aug = {r['project']: int(r['downloads_2026_08']) for r in rd('projects.csv')}
top = {r['project']: int(r['downloads']) for r in rd('clickpy_top_projects_2026_08.csv')}
say(f'   August 2026 totals (millions): boto3 {aug["boto3"] / 1e6:,.0f}, botocore {aug["botocore"] / 1e6:,.0f}, '
    f's3transfer {aug["s3transfer"] / 1e6:,.0f}, aiobotocore {aug["aiobotocore"] / 1e6:,.0f}, jmespath {aug["jmespath"] / 1e6:,.0f}, '
    f's3fs (rank 59, depends on aiobotocore) {top["s3fs"] / 1e6:,.0f}; protobuf {aug["protobuf"] / 1e6:,.0f}, '
    f'grpcio-status {aug["grpcio-status"] / 1e6:,.0f}, googleapis-common-protos {top["googleapis-common-protos"] / 1e6:,.0f}, '
    f'google-auth {top["google-auth"] / 1e6:,.0f}; fsspec {aug["fsspec"] / 1e6:,.0f}')
say('')

# ---- 4. the share of projects under other units ---------------------------------------------------
say('4. The share of projects where most releases reached half within two days, under other units:')
n_yes, n_all = len(yes), len(po)
say(f'   brief\'s unit (each project once): {n_yes} of {n_all} = {n_yes / n_all * 100:.1f}%')
aws = ['boto3', 'botocore', 's3transfer', 'aiobotocore']
say(f'   the four AWS libraries as one unit (all four did not reach): {n_yes} of {n_all - 3} = {n_yes / (n_all - 3) * 100:.1f}%')
say(f'   and protobuf with grpcio-status as one unit too: {n_yes} of {n_all - 4} = {n_yes / (n_all - 4) * 100:.1f}%')
say('   The brief\'s convention: "as a rule" at 75 per cent or more.')
say('')

# ---- 5. pre-releases in the window ----------------------------------------------------------------
say('5. Pre-release versions uploaded 1 April to 31 August 2026 (they are folded into "~other"), by project:')
pre = defaultdict(int)
for v in versions:
    if v['is_prerelease'] == 'True' and '2026-04-01' <= v['first_upload_utc'][:10] <= '2026-08-31':
        pre[v['project']] += 1
say('   ' + ', '.join(f'{p} {n}' for p, n in sorted(pre.items(), key=lambda kv: -kv[1])) if pre else '   none')
say('   (a pre-release is installed only when asked for, so its downloads are ordinarily small; the retained counts cannot show them)')

say('')

# ---- 6. weekly series for the three whose ~other share moved most --------------------------------
say('6. Weekly ~other share (7-day means, weeks starting Monday) for botocore, boto3 and litellm, to date the steps:')
wk = defaultdict(lambda: defaultdict(list))
for p in ('botocore', 'boto3', 'litellm'):
    for ds in sorted(counts[p]):
        d = D(ds)
        if d < first_day0[p]:
            continue
        v = other_share(p, d)
        if v is not None:
            wk[p][d - datetime.timedelta(days=d.weekday())].append(v)
weeks = sorted(set(w for p in wk for w in wk[p]))
say(f'   {"week of":<12}' + ''.join(f'{p:>10}' for p in ('botocore', 'boto3', 'litellm')))
for w in weeks:
    say(f'   {str(w):<12}' + ''.join(f'{statistics.mean(wk[p][w]) * 100:>9.1f}%' if wk[p].get(w) else f'{"-":>10}' for p in ('botocore', 'boto3', 'litellm')))

say('')

# ---- 7. litellm's volume over the window, and which of its releases reached half ------------------
say('7. litellm: mean daily downloads by month, split into "~other" (older than 1.83.1, or pre-release) and the')
say('   numerator versions; and the six releases that reached half, with their day 0 and days to half.')
say(f'   {"month":<10}{"days":>5}{"total/day":>14}{"~other/day":>14}{"numerator/day":>16}{"~other share":>14}')
for (y, m) in [(2026, m) for m in (4, 5, 6, 7, 8, 9)]:
    tot = oth = days = 0
    d = datetime.date(y, m, 1)
    while d.month == m:
        row = counts['litellm'].get(str(d))
        if row and d >= first_day0['litellm']:
            days += 1
            tot += sum(row.values())
            oth += row.get('~other', 0)
        d += ONE
    if days:
        say(f'   {y}-{m:02d}  {days:>5}{tot / days:>14,.0f}{oth / days:>14,.0f}{(tot - oth) / days:>16,.0f}{oth / tot * 100:>13.1f}%')
ro = [r for r in rd('analysis/release_outcomes.csv') if r['project'] == 'litellm' and r['days_to_half'] != '']
say('   releases reaching half: ' + '; '.join(f'{r["version"]} (day 0 {r["day0"]}) on day {r["days_to_half"]}' for r in ro))
say('   crossing dates: ' + ', '.join(sorted({str(D(r['day0']) + int(r['days_to_half']) * ONE) for r in ro})))
say('   litellm ~other share by day, 27 April to 6 May: ' + ', '.join(
    f'{d.day:02d}/{d.month:02d} {other_share("litellm", d) * 100:.1f}' for d in (datetime.date(2026, 4, 27) + k * ONE for k in range(10))))
say('   the same for the other daily releasers and their 30-day totals: boto3 and botocore mean daily downloads by month')
for p in ('boto3', 'botocore'):
    cells = []
    for m in (4, 5, 6, 7, 8, 9):
        tot = days = 0
        d = datetime.date(2026, m, 1)
        while d.month == m:
            row = counts[p].get(str(d))
            if row and d >= first_day0[p]:
                days += 1
                tot += sum(row.values())
            d += ONE
        cells.append(f'{m:02d}: {tot / days / 1e6:.1f}M' if days else f'{m:02d}: -')
    say(f'   {p}: ' + ', '.join(cells))

with open(OUT, 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('\n'.join(lines))
