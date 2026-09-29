#!/usr/bin/env python3
"""Replay review X3 (notes/replay-X3.md): calculations over LH012's retained files, offline, no network.
Written after the record and its tables were read, so every reading here is post hoc.
Usage: python3 studies/LH012/review/replay_x3.py > studies/LH012/review/replay_x3.txt"""
import csv, os, statistics, datetime as dt
from collections import defaultdict
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
DAYS = [f'2026-09-{d}' for d in range(21, 28)]
WEEK_END = '2026-09-27T23:59:59.999999'


def rd(*p):
    return list(csv.DictReader(open(os.path.join(DATA, *p))))


_VC = {}


def V(s):
    if s not in _VC:
        try:
            _VC[s] = Version(s)
        except InvalidVersion:
            _VC[s] = None
    return _VC[s]


REF = {r['project']: r for r in rd('reference.csv')}
P37 = sorted(REF)
VERS = defaultdict(dict)
for v in rd('versions.csv'):
    VERS[v['project']][v['version']] = v


def usable(v):
    return v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and v['first_upload_utc']


def admits_minor(rp, m):
    if not rp.strip():
        return True
    try:
        s = SpecifierSet(rp)
    except InvalidSpecifier:
        return None
    return any(s.contains(Version(f'{m}.{k}'), prereleases=True) for k in range(31))


def version_admits(row, m):
    vals = [admits_minor(x, m) for x in row['requires_python'].split(' | ')] if row['requires_python'] else [True]
    return any(v is True for v in vals)


_EX = {}


def excluded(p, m):
    """As analyse.py: no usable version at or above R uploaded by the week's end admits minor m."""
    if (p, m) not in _EX:
        R = V(REF[p]['R'])
        ge = [v for s, v in VERS[p].items() if usable(v) and V(s) and V(s) >= R and v['first_upload_utc'] <= WEEK_END]
        _EX[(p, m)] = not any(version_admits(v, m) for v in ge)
    return _EX[(p, m)]


def is_older(p, s):
    v = V(s)
    if s not in VERS[p] or v is None:
        return False
    return v < V(REF[p]['R'])


def spread(counts):
    """n versions, versions for 50 and 80 per cent, top share."""
    srt = sorted(counts.values(), reverse=True)
    tot = sum(srt)
    out = {}
    for q in (0.5, 0.8):
        cum, k = 0, 0
        for x in srt:
            if cum >= q * tot:
                break
            cum += x
            k += 1
        out[q] = k
    return len(srt), out[0.5], out[0.8], (srt[0] / tot if tot else None)


def age_days(p, s, on='2026-09-24'):
    return (dt.date.fromisoformat(on) - dt.date.fromisoformat(VERS[p][s]['first_upload_utc'][:10])).days


def wmedian(pairs):
    pairs = sorted(pairs)
    half, acc = sum(n for _, n in pairs) / 2, 0
    for a, n in pairs:
        acc += n
        if acc >= half:
            return a


print('Replay X3: post hoc calculations over LH012\'s retained files (read week 21 to 27 September 2026)')
print()

# ---------------------------------------------------------------- A. boto3's Python 3.9 older downloads: one population?
print('A. Version spread of older downloads by Python class (W sums from data/week/python/)')
print('   A cell of the log\'s fields (Python 3.9, pip, Linux, glibc, no CI flag) is not a population; the number of')
print('   versions its fetches sit on says whether it could be one. Ages are days from first upload to 24 September.')
for p in ('boto3', 'botocore', 'aiobotocore', 'numpy', 'pandas'):
    cls = {'excluded': defaultdict(int), 'admitted': defaultdict(int), '3.9': defaultdict(int)}
    for r in rd('week', 'python', p + '.csv'):
        if not is_older(p, r['version']):
            continue
        n, m = int(r['n']), r['python_minor']
        if not m:
            continue
        key = 'excluded' if excluded(p, m) else 'admitted'
        cls[key][r['version']] += n
        if m == '3.9':
            cls['3.9'][r['version']] += n
    for key in ('3.9', 'excluded', 'admitted'):
        c = cls[key]
        if not c:
            continue
        nv, n50, n80, top = spread(c)
        tot = sum(c.values())
        med_age = wmedian([(age_days(p, v), n) for v, n in c.items()])
        over_year = sum(n for v, n in c.items() if age_days(p, v) > 365) / tot
        print(f'   {p} older from {key} Pythons: {tot:,} fetches on {nv} versions; versions for half {n50}, for 80 per cent {n80}; '
              f'largest version {top * 100:.1f} per cent; median age {med_age} days; over a year old {over_year * 100:.1f} per cent')
        if key == '3.9' and p == 'boto3':
            top10 = sorted(c.items(), key=lambda x: -x[1])[:10]
            print('      ten largest: ' + '; '.join(f'{v} ({VERS[p][v]["first_upload_utc"][:10]}) {n / tot * 100:.1f}' for v, n in top10))
            byyear = defaultdict(int)
            for v, n in c.items():
                byyear[VERS[p][v]['first_upload_utc'][:4]] += n
            print('      by year of the version\'s upload: ' + ', '.join(f'{y} {n / tot * 100:.1f}' for y, n in sorted(byyear.items())))
print()

# ---------------------------------------------------------------- B. Do the Python and the bounds explanation overlap for botocore and s3transfer?
print('B. botocore and s3transfer: the boto3 hold and the excluded-Python fetches are largely the same fetches')
edge = {'boto3': V('1.42.97'), 'botocore': V('1.42.97'), 's3transfer': V('0.16.1')}
for p in ('boto3', 'botocore', 's3transfer'):
    ex = adm = nr = 0
    ex_le = adm_le = adm_1_43 = 0
    for r in rd('week', 'python', p + '.csv'):
        if not is_older(p, r['version']):
            continue
        n, m, v = int(r['n']), r['python_minor'], V(r['version'])
        if not m:
            nr += n
        elif excluded(p, m):
            ex += n
            ex_le += n * (v <= edge[p])
        else:
            adm += n
            adm_le += n * (v <= edge[p])
    older = ex + adm + nr
    print(f'   {p}: older {older:,}; from excluded Pythons {ex / older * 100:.1f} per cent, admitted {adm / older * 100:.1f}, none {nr / older * 100:.1f}; '
          f'of the admitted-Python older fetches, at or below the last version for Python 3.9 ({edge[p]}) {adm_le / adm * 100:.1f} per cent, '
          f'above it (released May to August 2026) {(adm - adm_le) / adm * 100:.1f}')
print('   Reading: boto3 versions below 1.43 (the ones the record says hold botocore and s3transfer) are the versions the Python 3.9')
print('   population fetches; the share of botocore\'s and s3transfer\'s older fetches that come from excluded Pythons is what P already counts.')
print()

# ---------------------------------------------------------------- C. First-day test: the sign of the drift
print('C. The first-day test: sign and size of delta (day 30 minus day 2, points), 355 releases')
fr = [r for r in rd('analysis', 'firstday_releases.csv') if r['delta_points']]
d = [float(r['delta_points']) for r in fr]
pos = sum(1 for x in d if x > 0)
print(f'   releases {len(d)}; delta > 0 for {pos} ({pos / len(d) * 100:.1f} per cent); median {statistics.median(d):.1f}; '
      f'quartiles {statistics.quantiles(d, n=4)[0]:.1f} and {statistics.quantiles(d, n=4)[2]:.1f}; '
      f'within 5 points {sum(1 for x in d if abs(x) <= 5)}; within 10 {sum(1 for x in d if abs(x) <= 10)}; above +10 {sum(1 for x in d if x > 10)}; below -10 {sum(1 for x in d if x < -10)}')
byp = defaultdict(list)
for r in fr:
    byp[r['project']].append(float(r['delta_points']))
meds = {p: statistics.median(v) for p, v in byp.items()}
print(f'   projects {len(meds)}; median delta > 0 in {sum(1 for m in meds.values() if m > 0)}; between 0 and +10 in '
      f'{sum(1 for m in meds.values() if 0 < m <= 10)}; median of project medians {statistics.median(meds.values()):.1f}')
b = byp['boto3']
print(f'   boto3: {len(b)} releases, median delta {statistics.median(b):.1f}; above +10 {sum(1 for x in b if x > 10)}, within 10 {sum(1 for x in b if abs(x) <= 10)}, '
      f'delta > 0 {sum(1 for x in b if x > 0)}; botocore median {statistics.median(byp["botocore"]):.1f}, above +10 {sum(1 for x in byp["botocore"] if x > 10)}')
rat = [float(r['ratio_s2_s30']) for r in fr if r['ratio_s2_s30']]
print(f'   day-2 share over day-30 share: median {statistics.median(rat):.2f} (a release whose share still grows has a ratio below 1)')
print('   Reading: the ten-point band passes releases whose share keeps climbing through the month; "settles" is true within the')
print('   band the brief fixed, and the climb is what LH008 saw as pins moving over weeks.')
print()

# ---------------------------------------------------------------- D. Pooled shares without boto3
print('D. The pooled older share and what boto3 does to it')
wk = {r['project']: r for r in rd('analysis', 'week.csv')}
tot = sum(int(r['total']) for r in wk.values())
old = sum(int(r['older']) for r in wk.values())
fam = ('boto3', 'botocore', 's3transfer', 'aiobotocore')
tot_nb = tot - int(wk['boto3']['total'])
old_nb = old - int(wk['boto3']['older'])
tot_nf = tot - sum(int(wk[p]['total']) for p in fam)
old_nf = old - sum(int(wk[p]['older']) for p in fam)
print(f'   all 37: {old / tot * 100:.1f} per cent of {tot:,}; boto3 is {int(wk["boto3"]["total"]) / tot * 100:.1f} per cent of all fetches and '
      f'{int(wk["boto3"]["older"]) / old * 100:.1f} per cent of all older fetches')
print(f'   without boto3: {old_nb / tot_nb * 100:.1f} per cent; without the boto3 family (boto3, botocore, s3transfer, aiobotocore): {old_nf / tot_nf * 100:.1f}')
py = {r['project']: r for r in rd('analysis', 'python.csv')}
ex_all = sum(int(r['older_excluded_python']) for r in py.values())
ex_nb = ex_all - int(py['boto3']['older_excluded_python'])
old2 = sum(int(r['older_W2']) for r in py.values())
print(f'   pooled P lower: {ex_all / old2 * 100:.1f} per cent; without boto3 {ex_nb / (old2 - int(py["boto3"]["older_W2"])) * 100:.1f}')
print()

# ---------------------------------------------------------------- E. Weekday and weekend
print('E. Older and at-or-newer downloads by day of the week (data/week/versions/): does the older part dip at the weekend?')
for p in ('boto3', 'botocore', 'requests', 'certifi', 'pydantic-core'):
    per = defaultdict(lambda: [0, 0])
    for r in rd('week', 'versions', p + '.csv'):
        k = 0 if is_older(p, r['version']) else 1
        per[r['date']][k] += int(r['n'])
    wd = [per[d] for d in DAYS[:5]]
    we = [per[d] for d in DAYS[5:]]
    o_wd, o_we = statistics.mean(x[0] for x in wd), statistics.mean(x[0] for x in we)
    n_wd, n_we = statistics.mean(x[1] for x in wd), statistics.mean(x[1] for x in we)
    print(f'   {p}: older per weekday {o_wd / 1e6:.1f}M, per weekend day {o_we / 1e6:.1f}M (ratio {o_we / o_wd:.2f}); '
          f'at-or-newer {n_wd / 1e6:.1f}M and {n_we / 1e6:.1f}M (ratio {n_we / n_wd:.2f})')
print()

# ---------------------------------------------------------------- F. Ages of older downloads from admitted Pythons, all 37
print('F. Older downloads from Pythons a newer version admits: how old are the versions they sit on? (fetch-weighted median age, days;')
print('   share of those fetches on versions over a year old; share on versions uploaded within 90 days before R, the ordinary lag)')
rows = []
for p in P37:
    Rt = REF[p]['R_first_upload_utc']
    R90 = (dt.datetime.fromisoformat(Rt[:19]) - dt.timedelta(days=90)).isoformat()
    pairs, recent, tot = [], 0, 0
    for r in rd('week', 'python', p + '.csv'):
        if not is_older(p, r['version']):
            continue
        m, n = r['python_minor'], int(r['n'])
        if not m or excluded(p, m):
            continue
        pairs.append((age_days(p, r['version']), n))
        tot += n
        if VERS[p][r['version']]['first_upload_utc'] >= R90:
            recent += n
    over = sum(n for a, n in pairs if a > 365) / tot
    rows.append((p, wmedian(pairs), over, recent / tot))
rows.sort(key=lambda x: -x[1])
for p, med, over, rec in rows:
    print(f'   {p}: median age {med}; over a year {over * 100:.0f} per cent; within 90 days before R {rec * 100:.0f} per cent')
print(f'   median over projects: age {statistics.median(x[1] for x in rows)} days; over a year {statistics.median(x[2] for x in rows) * 100:.0f} per cent; '
      f'within 90 days before R {statistics.median(x[3] for x in rows) * 100:.0f} per cent')
print()

# ---------------------------------------------------------------- G. awscli's exact pins on botocore, read but not counted
print('G. awscli pins botocore exactly, its older versions were read (as a dependent of urllib3), but it is not among botocore\'s')
print('   or s3transfer\'s identified dependents: the dependents rule screens on the latest version and the versions newest during W,')
print('   and awscli 1.46.1 (latest at read) names only urllib3 among the 37 (data/top500_screen.csv, data/pairs.csv).')
req2 = defaultdict(dict)
for r in rd('requirements_phase2.csv'):
    if r['dependent'] == 'awscli' and r['parse'] == 'ok' and r['name'] in ('botocore', 's3transfer'):
        req2[r['dependent_version']][r['name']] = r['specifier']
mix = defaultdict(int)
for r in rd('deps', 'versions', 'awscli.csv'):
    mix[r['version']] += int(r['n'])
tot = sum(mix.values())
Rb = V(REF['botocore']['R'])
held_b = sum(n for v, n in mix.items() if v in req2 and 'botocore' in req2[v] and req2[v]['botocore'].startswith('==')
             and V(req2[v]['botocore'][2:]) and V(req2[v]['botocore'][2:]) < Rb)
unread = sum(n for v, n in mix.items() if v not in req2 and v != '1.46.1')
older_botocore = int(wk['botocore']['older'])
older_s3 = int(wk['s3transfer']['older'])
print(f'   awscli W fetches {tot:,} (1.46.1 alone {mix["1.46.1"]:,}); versions read with a botocore pin {len(req2)}: '
      + ', '.join(f'{v} {req2[v].get("botocore", "")}' for v in sorted(req2, key=lambda s: V(s) or Version("0"))))
print(f'   fetches at read versions pinning botocore below R {held_b:,}: {held_b / tot * 100:.1f} per cent of awscli\'s fetches, '
      f'{held_b / older_botocore * 100:.1f} per cent of botocore\'s older fetches, at a fetch ratio of {tot / int(wk["botocore"]["total"]):.2f} '
      f'(an exact pin brings exactly that botocore version, so this is the unstrained kind of hold); unread awscli versions {unread:,} fetches')
print(f'   the same versions\' ranges on s3transfer would hold about the same fetches against s3transfer\'s {older_s3:,} older fetches ({held_b / older_s3 * 100:.1f} per cent)')
print()
print('done')
