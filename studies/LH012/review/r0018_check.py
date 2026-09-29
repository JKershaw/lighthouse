#!/usr/bin/env python3
"""R-0018 (the reader-and-inference review of the LH012 piece, version 1.1): checks made from the study's
retained files only, offline. No count is re-read from any source. Each section says what it computes and
which claim of the piece or the record it bears on. Output: review/r0018_check.txt.

Sections:
  A  boto3's Python 3.9 downloads over 21 to 27 September 2026, by version: how concentrated they are
     (data/week/python/boto3.csv, data/versions.csv). Bears on the piece's closing paragraph and on LH013.
  B  The first-day test read with the brief's secondary descriptor, the ratio of the day-2 to the day-30
     share (data/analysis/firstday_releases.csv). Bears on "a new version's share settles within two days".
  C  pandas: the secondary wheel measure broken down by whether the Python is excluded and by the platform
     tag of the older wheel (data/week/files/pandas.csv, data/files.csv.gz), replicating analyse.py's rule.
     Bears on whether the wheel measure adds to P for pandas.
  D  The title's claim, per project and pooled (data/analysis/python.csv).
  E  The four projects where identified bounds "account for most": holds by the dependent's current versions
     against its older versions (data/analysis/bounds.csv).
  F  The CI-flag half of the frozen-list trace: the size of the differences (data/analysis/frozen.csv).
  G  Weekday against weekend: older and at-or-newer downloads by day of week (data/week/versions/*.csv),
     a description for the next step's design, not a test.
"""
import csv, gzip, os, re, statistics, datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
DATA = os.path.join(S, 'data')
A = os.path.join(DATA, 'analysis')
OUT = os.path.join(HERE, 'r0018_check.txt')
try:
    from packaging.version import Version, InvalidVersion
except ImportError:  # a minimal stand-in for PEP 440 ordering of plain versions
    class InvalidVersion(Exception):
        pass

    class Version:
        def __init__(self, s):
            m = re.match(r'^(\d+(?:\.\d+)*)$', s)
            if not m:
                raise InvalidVersion(s)
            self.k = tuple(int(x) for x in s.split('.'))
            self.is_prerelease = False

        def __lt__(self, o): return self.k < o.k
        def __le__(self, o): return self.k <= o.k
        def __ge__(self, o): return self.k >= o.k
        def __eq__(self, o): return self.k == o.k


def V(s):
    try:
        return Version(s)
    except InvalidVersion:
        return None


def rd(*p):
    with open(os.path.join(*p), newline='') as f:
        return list(csv.DictReader(f))


lines = []


def say(*a):
    lines.append(' '.join(str(x) for x in a))


def pct(x):
    return f'{100 * x:.1f}'


# ---------------------------------------------------------------- A: boto3 on Python 3.9, by version
say('A. boto3, Python 3.9, 21 to 27 September 2026: downloads by version (data/week/python/boto3.csv)')
up = {r['version']: r['first_upload_utc'][:10] for r in rd(DATA, 'versions.csv') if r['project'] == 'boto3'}
py = defaultdict(int)
for r in rd(DATA, 'week', 'python', 'boto3.csv'):
    if r['python_minor'] == '3.9':
        py[r['version']] += int(r['n'])
tot = sum(py.values())
say(f'   total {tot:,} over {len(py)} versions')
ranked = sorted(py.items(), key=lambda kv: -kv[1])
say('   the ten largest versions (share of the 3.9 downloads; first upload):')
for v, n in ranked[:10]:
    say(f'     {v:>10} {pct(n / tot):>6} %  uploaded {up.get(v, "?")}')
cum, k50, k80, k95 = 0, None, None, None
for i, (v, n) in enumerate(ranked, 1):
    cum += n
    if k50 is None and cum >= 0.5 * tot: k50 = i
    if k80 is None and cum >= 0.8 * tot: k80 = i
    if k95 is None and cum >= 0.95 * tot: k95 = i
say(f'   versions needed for half: {k50}; for 80 per cent: {k80}; for 95 per cent: {k95}')
say(f'   largest single version: {pct(ranked[0][1] / tot)} per cent; ten largest together: {pct(sum(n for _, n in ranked[:10]) / tot)} per cent')
# by the year and quarter of the version's first upload
byq = defaultdict(int)
for v, n in py.items():
    d = up.get(v)
    byq[(d[:4] + ' Q' + str((int(d[5:7]) - 1) // 3 + 1)) if d else 'unknown'] += n
say('   by the quarter the version was first uploaded (share of the 3.9 downloads):')
for q in sorted(byq):
    if byq[q] / tot >= 0.005:
        say(f'     {q}: {pct(byq[q] / tot)} %')
say('   share of the 3.9 downloads at versions uploaded before 2026: ' + pct(sum(n for v, n in py.items() if up.get(v, '9') < '2026') / tot) + ' per cent')
say('   Reading: a spread over hundreds of versions is what many lists frozen at many dates would leave; one pinned fleet')
say('   would leave one or a few versions. The log still cannot say how many machines make it.')
say('')

# ---------------------------------------------------------------- B: the first-day test read with the ratio
say('B. The first-day test read with the brief\'s secondary descriptor, the day-2 to day-30 ratio (firstday_releases.csv)')
fr = [r for r in rd(A, 'firstday_releases.csv') if r['settled'] != '']
fp = {r['project']: r for r in rd(A, 'firstday_projects.csv')}
say(f'   {len(fr)} releases with a known delta; {sum(1 for r in fr if r["settled"] == "True")} settled')
settled = [r for r in fr if r['settled'] == 'True']
rat = [float(r['ratio_s2_s30']) for r in settled if r['ratio_s2_s30']]
say(f'   among settled releases: median day-2 share {pct(statistics.median(float(r["s2"]) for r in settled))} per cent, '
    f'median day-30 share {pct(statistics.median(float(r["s30"]) for r in settled))} per cent, median ratio s2/s30 {statistics.median(rat):.2f}')
say(f'   settled releases whose day-30 share is at most 20 per cent: {sum(1 for r in settled if float(r["s30"]) <= 0.2)} of {len(settled)}'
    f' ({sum(1 for r in settled if float(r["s30"]) <= 0.2 and r["project"] in ("boto3", "botocore"))} of them boto3 or botocore)')
say(f'   settled releases whose day-2 share is below three quarters of the day-30 share (grew by more than a third after day 2): '
    f'{sum(1 for x in rat if x < 0.75)} of {len(rat)}')
say('   per project, among releases with a known delta: median s2, median s30, median ratio, and the record\'s verdict')
rows = []
for p in sorted(fp):
    k = [r for r in fr if r['project'] == p]
    s2 = statistics.median(float(r['s2']) for r in k)
    s30 = statistics.median(float(r['s30']) for r in k)
    ratio = statistics.median(float(r['ratio_s2_s30']) for r in k if r['ratio_s2_s30'])
    rows.append((p, len(k), s2, s30, ratio, fp[p]['project_settles'], float(fp[p]['median_delta_points'])))
for p, n, s2, s30, ratio, settles, md in sorted(rows, key=lambda x: x[4]):
    flag = '  <- share grew by more than a third after day 2' if ratio < 0.75 and settles == 'True' else ''
    say(f'     {p:<18} n={n:<3} s2 {pct(s2):>5}  s30 {pct(s30):>5}  ratio {ratio:.2f}  delta {md:+5.1f}  settles={settles}{flag}')
grew = [p for p, n, s2, s30, ratio, settles, md in rows if settles == 'True' and ratio < 0.75]
say(f'   projects counted as settling whose median ratio is below 0.75: {len(grew)} of 28: {", ".join(grew)}')
say('   Reading: the ten-point band is absolute, so a share that is small on both days settles however much it grows in')
say('   proportion; the record reports delta only, though the brief fixed the ratio as a secondary descriptor.')
say('')

# ---------------------------------------------------------------- C: pandas, the wheel measure broken down
say('C. pandas: the secondary wheel measure by Python exclusion and by the older wheel\'s platform tag (replicating analyse.py)')
PLAT_RE = re.compile(r'^(manylinux|musllinux)_(\d+)_(\d+)_(.+)$')
LEGACY = {'manylinux1': (2, 5), 'manylinux2010': (2, 12), 'manylinux2014': (2, 17)}


def plat_key(tag):
    for leg, fl in LEGACY.items():
        if tag.startswith(leg + '_'):
            return 'manylinux', tag[len(leg) + 1:], fl
    m = PLAT_RE.match(tag)
    if m:
        return m.group(1), m.group(4), (int(m.group(2)), int(m.group(3)))
    m = re.match(r'^macosx_(\d+)_(\d+)_(.+)$', tag)
    if m:
        return 'macosx', m.group(3), (int(m.group(1)), int(m.group(2)))
    if tag.startswith('win'):
        return 'win', tag, None
    return tag, '', None


def interp_ok(interp, abi, m):
    mm = m.replace('.', '')
    for it in interp.split('.'):
        if it in ('py3', 'py2.py3', 'py' + mm[0]) or it == 'py' + mm:
            return True
        if it == 'cp' + mm:
            return True
        if abi == 'abi3' and it.startswith('cp3') and Version(it[2] + '.' + it[3:]) <= Version(m):
            return True
    return False


adm = {(r['project'], r['python_minor']): r['any_ge_R_admits'] == 'True' for r in rd(DATA, 'python_admission.csv')}
ref = {r['project']: r for r in rd(DATA, 'reference.csv')}
for p in ('pandas', 'numpy'):
    R = Version(ref[p]['R'])
    ge = []
    with gzip.open(os.path.join(DATA, 'files.csv.gz'), 'rt') as f:
        for r in csv.DictReader(f):
            if r['project'] == p and r['packagetype'] == 'bdist_wheel' and V(r['version']) and V(r['version']) >= R and r['yanked'] != 'True':
                parts = r['filename'][:-4].split('-')
                ge.append((parts[-3], parts[-2], parts[-1]))
    floors = sorted({plat_key(g)[2] for _, _, gp in ge for g in gp.split('.') if plat_key(g)[0] == 'manylinux'})
    say(f'   {p}: R {ref[p]["R"]}, manylinux floors of wheels at or above R: {floors}')
    c = defaultdict(int)
    tot = 0
    for r in rd(DATA, 'week', 'files', p + '.csv'):
        n = int(r['n']); tot += n
        if r['plat'] in ('(not a wheel)', '(no file name)') or not r['python_minor']:
            c[('other', r['plat'] if r['plat'].startswith('(') else 'python not reported', '')] += n
            continue
        m = r['python_minor']
        okw = False
        for plat in r['plat'].split('.'):
            fam, arch, floor = plat_key(plat)
            for gi, ga, gp in ge:
                if not interp_ok(gi, ga, m):
                    continue
                for g in gp.split('.'):
                    gf, garch, gfl = plat_key(g)
                    if g == 'any' or (gf == fam and garch == arch and (gfl is None or floor is None or gfl <= floor)):
                        okw = True; break
                if okw: break
            if okw: break
        excl = 'Python excluded' if not adm.get((p, m), False) else 'Python admitted'
        if okw:
            c[('wheel available', excl, '')] += n
        else:
            fam, arch, floor = plat_key(r['plat'].split('.')[0])
            key = fam + ('_' + '_'.join(map(str, floor)) if floor else '') + '_' + arch
            c[('wheel-excluded', excl, key)] += n
    wx = sum(n for k, n in c.items() if k[0] == 'wheel-excluded')
    say(f'     older downloads {tot:,}; wheel-excluded {pct(wx / tot)} per cent (record: files.csv), of which')
    for excl in ('Python excluded', 'Python admitted'):
        part = sum(n for k, n in c.items() if k[0] == 'wheel-excluded' and k[1] == excl)
        say(f'       from a {excl.lower()} Python: {pct(part / tot)} per cent of older downloads')
    say('     the wheel-excluded downloads from admitted Pythons, by the older wheel\'s tag (share of older downloads):')
    for k, n in sorted(((k, n) for k, n in c.items() if k[0] == 'wheel-excluded' and k[1] == 'Python admitted'), key=lambda kv: -kv[1])[:8]:
        say(f'       {k[2]:<40} {pct(n / tot):>5} %')
say('   Reading: an older manylinux_2_17 wheel fetched by an admitted Python is "wheel-excluded" only because R\'s wheels carry a')
say('   higher floor; the older wheel\'s floor is a lower bound on the machine\'s glibc, not its value, so this part does not show')
say('   machines that could not take the newer wheel. The wheel measure therefore adds nothing firm to P for pandas.')
say('')

# ---------------------------------------------------------------- D: the title
say('D. The title, "Most downloads of old versions come from Pythons a newer version supports" (python.csv)')
pyr = rd(A, 'python.csv')
n_blue = sum(1 for r in pyr if int(r['older_admitted_python']) > int(r['older_W2']) / 2)
say(f'   projects where downloads from admitted Pythons alone are more than half of older downloads: {n_blue} of 37')
say('   the other five: ' + ', '.join(f"{r['project']} ({pct(int(r['older_admitted_python']) / int(r['older_W2']))} %)" for r in pyr if int(r['older_admitted_python']) <= int(r['older_W2']) / 2))
T = sum(int(r['older_W2']) for r in pyr)
say(f'   pooled over all 37 projects\' older downloads: from admitted Pythons {pct(sum(int(r["older_admitted_python"]) for r in pyr) / T)} per cent, '
    f'from excluded {pct(sum(int(r["older_excluded_python"]) for r in pyr) / T)}, not reported {pct(sum(int(r["older_python_not_reported"]) for r in pyr) / T)}')
say(f'   boto3\'s share of the pooled older downloads: {pct(int(next(r for r in pyr if r["project"] == "boto3")["older_W2"]) / T)} per cent')
say('')

# ---------------------------------------------------------------- E: the four B "accounts for most"
say('E. Identified bounds, the four "accounts for most": held by the dependent\'s current versions against its older versions (bounds.csv)')
for r in rd(A, 'bounds.csv'):
    if r['class'] == 'accounts for most':
        say(f'   {r["project"]:<14} lower from {r["lower_from"]:<9} fetch ratio {float(r["lower_fetch_ratio"]):.2f}  '
            f'held by current versions {pct(float(r["largest_held_by_current_versions"])):>5} %  by older versions {pct(float(r["sum_held_by_older_versions"])):>6} % of older fetches (uncapped)')
say('   Reading: only pydantic-core is held by its dependent\'s current versions; for fsspec, botocore and s3transfer the hold is by')
say('   older versions of s3fs and boto3, whose own older fetches are what the study could not explain.')
say('')

# ---------------------------------------------------------------- F: the CI half of the trace
say('F. The CI-flag difference, older minus at-or-newer, in points (frozen.csv)')
fz = rd(A, 'frozen.csv')
pos = sorted(((float(r['ci_difference_points']), r['project']) for r in fz if float(r['ci_difference_points']) > 0), reverse=True)
neg = sorted(((float(r['ci_difference_points']), r['project']) for r in fz if float(r['ci_difference_points']) <= 0))
say('   positive (' + str(len(pos)) + '): ' + ', '.join(f'{p} {d:+.1f}' for d, p in pos))
say('   negative (' + str(len(neg)) + '): ' + ', '.join(f'{p} {d:+.1f}' for d, p in neg))
say(f'   median of the absolute differences: {statistics.median(abs(float(r["ci_difference_points"])) for r in fz):.1f} points; '
    f'differences within 3 points either way: {sum(1 for r in fz if abs(float(r["ci_difference_points"])) <= 3)} of 37')
tr = [r['project'] for r in fz if r['shows_frozen_list_trace'] == 'True']
say(f'   the 18 that show the trace, smallest CI difference: {min(float(r["ci_difference_points"]) for r in fz if r["shows_frozen_list_trace"] == "True"):+.1f} points')
say('   Reading: the split is two-sided and mostly large, not noise about zero; the record\'s median of +1.6 sits between the two groups.')
say('')

# ---------------------------------------------------------------- G: weekday against weekend
say('G. Weekday against weekend, 21 to 27 September 2026 (week/versions/*.csv): the ratio of a weekend day\'s mean to a weekday\'s mean,')
say('   for older and for at-or-newer downloads, and the older share on weekdays and at the weekend (description only)')
wk = {r['project']: r for r in rd(A, 'week.csv')}
res = []
for p in sorted(wk):
    R = Version(wk[p]['R'])
    ge_set = set(wk[p]['R'].split()) if False else None
    old = defaultdict(int); new = defaultdict(int)
    for r in rd(DATA, 'week', 'versions', p + '.csv'):
        v = V(r['version'])
        if v is None:
            continue
        d = dt.date.fromisoformat(r['date'])
        (old if v < R else new)[d.weekday() >= 5] += int(r['n'])
    o_wd, o_we = old[False] / 5, old[True] / 2
    n_wd, n_we = new[False] / 5, new[True] / 2
    res.append((p, o_we / o_wd if o_wd else float('nan'), n_we / n_wd if n_wd else float('nan'),
                old[False] / (old[False] + new[False]), old[True] / (old[True] + new[True])))
say('   ' + f'{"project":<18} {"older we/wd":>11} {"newer we/wd":>11} {"O weekday":>10} {"O weekend":>10}')
for p, ro, rn, owd, owe in res:
    say('   ' + f'{p:<18} {ro:>11.2f} {rn:>11.2f} {pct(owd):>9} % {pct(owe):>9} %')
say(f'   median weekend-to-weekday ratio: older {statistics.median(x[1] for x in res):.2f}, at-or-newer {statistics.median(x[2] for x in res):.2f}; '
    f'projects where older downloads fall less at the weekend than newer ones do: {sum(1 for x in res if x[1] > x[2])} of 37')
say('   Reading: builds and people rest at weekends; a fetch that goes on regardless is a daemon, a schedule or a scanner. The log')
say('   cannot name it, but the weekend ratio is a cheap descriptor of it that LH013 could carry, since it reads the same table.')

open(OUT, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
