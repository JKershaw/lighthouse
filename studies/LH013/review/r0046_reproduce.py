#!/usr/bin/env python3
"""R-0046, the evidence review of LH013 0.1: an independent recomputation of the record's main figures from the
retained count files, written by the reviewer without importing or calling the study's scripts (definitions from the
brief, amendment 4 and LH012's brief; where a definition's detail is set by a named reference script, that detail
is followed as stated in the brief). Offline; no network, no key. Python 3 with `packaging`.
Output: review/r0046_reproduce.txt. Compares with data/analysis/*.csv and prints any disagreement."""
import csv, os, re, random, statistics
from collections import defaultdict
from datetime import date, timedelta
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.dirname(HERE)
D = os.path.join(S, 'data')
L12 = os.path.join(os.path.dirname(S), 'LH012', 'data')
out = []


def say(*a):
    out.append(' '.join(str(x) for x in a))


def rd(*p):
    with open(os.path.join(*p), newline='') as f:
        return list(csv.DictReader(f))


def pv(s):
    try:
        return Version(s)
    except InvalidVersion:
        return None


P37 = sorted(r['project'] for r in rd(L12, 'reference.csv'))
R0 = {r['project']: Version(r['R']) for r in rd(L12, 'reference.csv')}
assert len(P37) == 37
LIST = defaultdict(dict)  # PyPI as read 2 November 2026
for r in rd(D, 'versions.csv'):
    LIST[r['project']][r['version']] = r
WEND = {'W0': '2026-09-27T23:59:59.999999Z', 'W1': '2026-10-04T23:59:59.999999Z', 'W2': '2026-10-11T23:59:59.999999Z'}


def klass(p, s):
    if s not in LIST[p]:
        return 'other'
    v = pv(s)
    if v is None:
        return 'other'
    if v < R0[p]:
        return 'older'
    return 'other' if (v.is_prerelease or v.is_devrelease) else 'newer'


def usable(r):
    return r['parse'] == 'ok' and r['is_prerelease'] == 'False' and r['all_yanked'] == 'False' and r['first_upload_utc']


def rp_admits(rp, m):
    parts = rp.split(' | ') if rp else ['']
    for x in parts:
        if not x.strip():
            return True
        try:
            s = SpecifierSet(x)
        except InvalidSpecifier:
            continue
        if any(s.contains(Version(f'{m}.{k}'), prereleases=True) for k in range(31)):
            return True
    return False


_EX = {}


def excluded(p, m, w):
    k = (p, m, w)
    if k not in _EX:
        ge = [r for s, r in LIST[p].items() if usable(r) and pv(s) >= R0[p] and r['first_upload_utc'] <= WEND[w]]
        _EX[k] = not any(rp_admits(r['requires_python'], m) for r in ge)
    return _EX[k]


def edge(p, m):
    below = sorted(pv(s) for s, r in LIST[p].items() if usable(r) and pv(s) < R0[p] and rp_admits(r['requires_python'], m))
    return below[-1] if below else None


def near(a, b, tol):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


# ---------------------------------------------------------------- counts
VER = {}  # (p, w) -> {version: n}
PYC = {}  # (p, w) -> {(version, minor): n}
for p in P37:
    v0 = defaultdict(int)
    for r in rd(L12, 'week', 'versions', p + '.csv'):
        v0[r['version']] += int(r['n'])
    VER[(p, 'W0')] = v0
    p0 = defaultdict(int)
    for r in rd(L12, 'week', 'python', p + '.csv'):
        p0[(r['version'], r['python_minor'])] += int(r['n'])
    PYC[(p, 'W0')] = p0
    for w in ('W1', 'W2'):
        VER[(p, w)] = defaultdict(int)
        PYC[(p, w)] = defaultdict(int)
    for r in rd(D, 'counts', 'versions', p + '.csv'):
        VER[(p, r['week'])][r['version']] += int(r['n'])
    for r in rd(D, 'counts', 'python', p + '.csv'):
        PYC[(p, r['week'])][(r['version'], r['python_minor'])] += int(r['n'])

# ---------------------------------------------------------------- A. W0 check and gap rule
say('A. W0 baseline and gap rule')
lh12w = {r['project']: r for r in rd(L12, 'analysis', 'week.csv')}
now0 = defaultdict(int)
now0d = defaultdict(int)
for r in rd(D, 'counts', 'w0_daily_totals.csv'):
    now0[r['project']] += int(r['n'])
    now0d[(r['project'], r['date'])] += int(r['n'])
old0d = defaultdict(int)
for p in P37:
    for r in rd(L12, 'week', 'versions', p + '.csv'):
        old0d[(p, r['date'])] += int(r['n'])
bad = [p for p in P37 if now0[p] != int(lh12w[p]['total']) or now0[p] != sum(VER[(p, 'W0')].values())]
badd = [k for k in old0d if old0d[k] != now0d.get(k)]
say(f'   W0 totals read again equal to LH012 week.csv and to the sum of LH012 week/versions: {37 - len(bad)} of 37; '
    f'daily totals compared {len(old0d)}, unequal {len(badd)}')
dt = defaultdict(dict)
for r in rd(D, 'counts', 'daily_totals.csv'):
    dt[r['project']][r['date']] = int(r['n'])
days = [date(2026, 9, 28) + timedelta(i) for i in range(14)]
gaps = []
for d in days:
    win = [(d + timedelta(k)).isoformat() for k in range(-3, 4)]
    tot = {x: sum(dt[p].get(x, 0) for p in P37) for x in win}
    if tot[d.isoformat()] < 0.5 * statistics.median(tot.values()):
        gaps.append(('all', d))
    for p in P37:
        if d.isoformat() not in dt[p]:
            gaps.append((p, d))
held = {(r['project'], r['date']) for r in rd(D, 'days', 'days_held.csv')}
say(f'   project-days of W1 and W2 held (days listing): {sum((p, d.isoformat()) in held for p in P37 for d in days)} of 518; '
    f'gap days by LH011\'s rule over the 37: {len(gaps)}')
mins = min(sum(dt[p][d.isoformat()] for p in P37) / statistics.median(
    sum(dt[p][(d + timedelta(k)).isoformat()] for p in P37) for k in range(-3, 4)) for d in days)
say(f'   smallest ratio of a day\'s 37-project total to the median of its seven days: {mins:.3f}')
lastday = {r['last_day'] for r in rd(D, 'eligibility', 'clickpy_last_day_by_table.csv')}
say(f'   eligibility: rows {len(rd(D, "eligibility", "clickpy_last_day_by_table.csv"))}, last days held {sorted(lastday)}')

# ---------------------------------------------------------------- B. O
say('')
say('B. Older share O at R0')
O = {}
TOT = {}
for p in P37:
    for w in ('W0', 'W1', 'W2'):
        c = defaultdict(int)
        for s, n in VER[(p, w)].items():
            c[klass(p, s)] += n
        t = sum(c.values())
        O[(p, w)] = c['older'] / t
        TOT[(p, w)] = t
ref = {(r['project'], r['week']): r for r in rd(D, 'analysis', 'older.csv')}
dis = [(p, w, O[(p, w)], ref[(p, w)]['O']) for p in P37 for w in ('W0', 'W1', 'W2') if not near(O[(p, w)], ref[(p, w)]['O'], 5e-7)]
say(f'   project-weeks recomputed 111; differing from older.csv by more than 5e-7: {len(dis)} {dis[:5]}')
Ohold = {p: abs(O[(p, 'W1')] - O[(p, 'W0')]) <= 0.05 and abs(O[(p, 'W2')] - O[(p, 'W0')]) <= 0.05 for p in P37}
say(f'   O holds: {sum(Ohold.values())} of 37; does not: {", ".join(p for p in P37 if not Ohold[p])}')
for p in P37:
    if not Ohold[p]:
        say(f'      {p}: {100*O[(p,"W0")]:.2f} {100*O[(p,"W1")]:.2f} {100*O[(p,"W2")]:.2f}; changes {100*(O[(p,"W1")]-O[(p,"W0")]):+.2f} {100*(O[(p,"W2")]-O[(p,"W0")]):+.2f}')
for w in ('W0', 'W1', 'W2'):
    xs = [O[(p, w)] for p in P37]
    pooled = sum(O[(p, w)] * TOT[(p, w)] for p in P37) / sum(TOT[(p, w)] for p in P37)
    say(f'   {w}: median {100*statistics.median(xs):.1f}, range {100*min(xs):.1f} to {100*max(xs):.1f}, pooled {100*pooled:.1f}')
ch = [O[(p, w)] - O[(p, 'W0')] for p in P37 for w in ('W1', 'W2')]
say(f'   change from W0 over 74 project-weeks: median {100*statistics.median(ch):.2f}, largest absolute {100*max(map(abs, ch)):.2f}')
say(f'   post hoc reading 3: lower than W0 in W1 {sum(O[(p,"W1")]<O[(p,"W0")] for p in P37)}, in W2 {sum(O[(p,"W2")]<O[(p,"W0")] for p in P37)}, '
    f'both {sum(O[(p,"W1")]<O[(p,"W0")] and O[(p,"W2")]<O[(p,"W0")] for p in P37)}; any change of more than 5 points upward: '
    f'{[p for p in P37 for w in ("W1","W2") if O[(p,w)]-O[(p,"W0")] > 0.05]}')

# ---------------------------------------------------------------- C. P
say('')
say('C. Python exclusion P at R0')


def pclass(lo, hi):
    if lo > 0.5:
        return 'accounts for most'
    if hi < 0.1:
        return 'accounts for little'
    if hi < 0.5:
        return 'cannot be the main reason'
    return 'undetermined'


PL = {}
PCL = {}
BYPY = {}
for p in P37:
    for w in ('W0', 'W1', 'W2'):
        ex = nr = adm = tot = 0
        for (s, m), n in PYC[(p, w)].items():
            tot += n
            if klass(p, s) != 'older':
                continue
            if not re.fullmatch(r'\d+\.\d+', m or ''):
                nr += n
            elif excluded(p, m, w):
                ex += n
            else:
                adm += n
        old = ex + nr + adm
        PL[(p, w)] = (ex / old, (ex + nr) / old)
        PCL[(p, w)] = pclass(*PL[(p, w)])
        BYPY[(p, w)] = tot
refp = {(r['project'], r['week']): r for r in rd(D, 'analysis', 'python.csv')}
dis = [(p, w) for p in P37 for w in ('W0', 'W1', 'W2')
       if not (near(PL[(p, w)][0], refp[(p, w)]['P_lower'], 5e-7) and near(PL[(p, w)][1], refp[(p, w)]['P_upper'], 5e-7)
               and PCL[(p, w)] == refp[(p, w)]['class'])]
say(f'   project-weeks recomputed 111; P or class differing from python.csv: {len(dis)} {dis[:5]}')
lh12p = {r['project']: r['class'] for r in rd(L12, 'analysis', 'python.csv')}
say(f'   W0 classes equal to LH012 python.csv: {sum(PCL[(p,"W0")] == lh12p[p] for p in P37)} of 37')


def broad(c):
    return 'cannot be the main reason' if c == 'accounts for little' else c


Phold = {p: broad(PCL[(p, 'W1')]) == broad(PCL[(p, 'W0')]) == broad(PCL[(p, 'W2')]) for p in P37}
Phold_strict = {p: PCL[(p, 'W1')] == PCL[(p, 'W0')] == PCL[(p, 'W2')] for p in P37}
say(f'   P class holds (accounts for little inside cannot): {sum(Phold.values())} of 37; changed: '
    f'{[(p, PCL[(p,"W0")], PCL[(p,"W1")], PCL[(p,"W2")]) for p in P37 if not Phold[p]]}')
say(f'   (counting accounts for little as its own class it would be {sum(Phold_strict.values())} of 37)')
for w in ('W0', 'W1', 'W2'):
    cnt = defaultdict(list)
    for p in P37:
        cnt[PCL[(p, w)]].append(p)
    say(f'   {w}: ' + '; '.join(f'{k} {len(v)}' + (f' ({", ".join(v)})' if k != 'cannot be the main reason' else '') for k, v in sorted(cnt.items())))
    say(f'      median P {100*statistics.median(PL[(p,w)][0] for p in P37):.1f} to {100*statistics.median(PL[(p,w)][1] for p in P37):.1f}')
for p in ('boto3', 'aiobotocore', 'numpy', 'pandas', 'urllib3'):
    say(f'   {p}: ' + ', '.join(f'{w} {100*PL[(p,w)][0]:.1f} to {100*PL[(p,w)][1]:.1f}' for w in ('W0', 'W1', 'W2')))
WSTART = {'W1': '2026-09-28T00:00:00Z', 'W2': '2026-10-05T00:00:00Z'}
chg = []
for p in P37:
    for w in ('W1', 'W2'):
        for m in ['2.7'] + ['3.%d' % i for i in range(4, 16)]:
            ge0 = [r for s, r in LIST[p].items() if usable(r) and pv(s) >= R0[p] and r['first_upload_utc'] < WSTART[w]]
            if (not any(rp_admits(r['requires_python'], m) for r in ge0)) != excluded(p, m, w):
                chg.append((p, w, m))
say(f'   (project, week, minor) whose exclusion at R0 differs between the week\'s start and end: {len(chg)} {chg}')
dif = max(abs(BYPY[(p, w)] - TOT[(p, w)]) / TOT[(p, w)] for p in P37 for w in ('W1', 'W2'))
say(f'   largest difference of by-Python weekly total from per-version total, W1 and W2: {100*dif:.4f} per cent')

# ---------------------------------------------------------------- D. C and C5
say('')
say('D. Concentration C and C5 from the pass files')
C = {}
for p in P37:
    for w in ('W1', 'W2'):
        r = rd(D, 'counts', 'pass', f'{p}_{w}.csv')[0]
        t = int(r['total'])
        assert int(r['older']) + int(r['at_or_newer']) + int(r['other']) == t
        for k in ('c6', 'c5', 'older_c6', 'older_c5'):
            sizes = [int(x) for x in r[k + '_top'].split()]
            assert sizes == sorted(sizes, reverse=True)
            den = int(r['older']) if k.startswith('older') else t
            acc, half = 0, None
            for i, x in enumerate(sizes[:1000]):
                acc += x
                if acc >= den / 2:
                    half = i + 1
                    break
            C[(p, w, k)] = (sizes[0] / den, r[k + '_key'], half, int(r[k + '_cells']))
        C[(p, w, 'pass_vs_versions')] = (t - TOT[(p, w)]) / TOT[(p, w)]
        C[(p, w, 'ci')] = (int(r['older_ci_true']) / int(r['older']), int(r['at_or_newer_ci_true']) / int(r['at_or_newer']),
                           int(r['older_ci_unknown']) + int(r['at_or_newer_ci_unknown']) + int(r['other_ci_unknown']))
refc = {(r['project'], r['week']): r for r in rd(D, 'analysis', 'cells.csv')}
dis = [(p, w) for p in P37 for w in ('W1', 'W2')
       if not (near(C[(p, w, 'c6')][0], refc[(p, w)]['C'], 5e-7) and C[(p, w, 'c6')][1] == refc[(p, w)]['C_cell']
               and str(C[(p, w, 'c6')][2]) == refc[(p, w)]['C_half'] and near(C[(p, w, 'c5')][0], refc[(p, w)]['C5'], 5e-7)
               and str(C[(p, w, 'c5')][2]) == refc[(p, w)]['C5_half'])]
say(f'   project-weeks 74; differing from cells.csv: {len(dis)} {dis[:5]}')
say(f'   largest |pass total - per-version total| / per-version total: {100*max(abs(C[(p,w,"pass_vs_versions")]) for p in P37 for w in ("W1","W2")):.4f} per cent')
Chold = {}
for k in ('c6', 'c5'):
    Chold[k] = {p: abs(C[(p, 'W2', k)][0] - C[(p, 'W1', k)][0]) <= 0.05 and C[(p, 'W2', k)][1] == C[(p, 'W1', k)][1] for p in P37}
    fails = [p for p in P37 if not Chold[k][p]]
    size_fail = [p for p in P37 if abs(C[(p, 'W2', k)][0] - C[(p, 'W1', k)][0]) > 0.05]
    say(f'   {k} holds: {37-len(fails)} of 37; fails {fails}; of which by size {size_fail}')
    for w in ('W1', 'W2'):
        xs = [C[(p, w, k)][0] for p in P37]
        hs = [C[(p, w, k)][2] for p in P37]
        say(f'      {w}: median {100*statistics.median(xs):.1f}, range {100*min(xs):.1f} to {100*max(xs):.1f}; '
            f'cells carrying half median {statistics.median(hs)}, range {min(hs)} to {max(hs)}')
    for kk in ('older_' + k,):
        say(f'      over older only: median W1 {100*statistics.median(C[(p,"W1",kk)][0] for p in P37):.1f}, W2 {100*statistics.median(C[(p,"W2",kk)][0] for p in P37):.1f}')
us = sum(C[(p, w, 'c6')][1].endswith('|US') for p in P37 for w in ('W1', 'W2'))
say(f'   largest six-field cell with country US: {us} of 74')
for p in ('boto3', 'aiobotocore', 'grpcio-status', 'fsspec', 'botocore', 'certifi'):
    say(f'   {p}: C {100*C[(p,"W1","c6")][0]:.1f} {100*C[(p,"W2","c6")][0]:.1f} ({C[(p,"W1","c6")][1]}); C5 {100*C[(p,"W1","c5")][0]:.1f} {100*C[(p,"W2","c5")][0]:.1f}; '
        f'half {C[(p,"W1","c6")][2]} {C[(p,"W2","c6")][2]}; older C {100*C[(p,"W1","older_c6")][0]:.1f} {100*C[(p,"W2","older_c6")][0]:.1f}')
# second-largest gaps where the largest cell changed
for k in ('c6', 'c5'):
    for p in P37:
        if C[(p, 'W2', k)][1] != C[(p, 'W1', k)][1]:
            g = []
            for w in ('W1', 'W2'):
                r = rd(D, 'counts', 'pass', f'{p}_{w}.csv')[0]
                s = [int(x) for x in r[k + '_top'].split()]
                g.append(100 * (s[0] - s[1]) / int(r['total']))
            say(f'      changed {k} {p}: {C[(p,"W1",k)][1]} -> {C[(p,"W2",k)][1]}; gap between two largest W1 {g[0]:.2f}, W2 {g[1]:.2f} points')
say('   CI flag split (amendment 3):')
for w in ('W1', 'W2'):
    o = [C[(p, w, 'ci')][0] for p in P37]
    n = [C[(p, w, 'ci')][1] for p in P37]
    d = [a - b for a, b in zip(o, n)]
    say(f'      {w}: median older {100*statistics.median(o):.1f}, at-or-newer {100*statistics.median(n):.1f}, difference median {100*statistics.median(d):+.1f}, '
        f'older higher {sum(x > 0 for x in d)} of 37, unknown {sum(C[(p,w,"ci")][2] for p in P37)}; boto3 {100*C[("boto3",w,"ci")][0]:.1f} vs {100*C[("boto3",w,"ci")][1]:.1f}; '
        f'certifi {100*C[("certifi",w,"ci")][0]:.1f} vs {100*C[("certifi",w,"ci")][1]:.1f}')

# ---------------------------------------------------------------- E. intervals (own resampler, two seeds)
say('')
say('E. Project-resampled 95 per cent percentile intervals, 10,000 resamples, reviewer\'s own resampler')


def interval(vals, stat, seed):
    rnd = random.Random(seed)
    k = len(vals)
    st = sorted(stat([vals[int(rnd.random() * k)] for _ in range(k)]) for _ in range(10000))
    return st[249], st[9749]


share = lambda xs: sum(xs) / len(xs)
for name, h in (('O', Ohold), ('P', Phold), ('C', Chold['c6']), ('C5', Chold['c5'])):
    v = [1 if h[p] else 0 for p in P37]
    a = interval(v, share, 1)
    b = interval(v, share, 20261102)
    say(f'   {name} holds {100*share(v):.1f}: seed 1 {100*a[0]:.1f} to {100*a[1]:.1f}; seed 20261102 {100*b[0]:.1f} to {100*b[1]:.1f}')
for w in ('W0', 'W1', 'W2'):
    a = interval([O[(p, w)] for p in P37], statistics.median, 1)
    say(f'   median O {w}: seed 1 {100*a[0]:.1f} to {100*a[1]:.1f}')
for w in ('W1', 'W2'):
    a = interval([C[(p, w, 'c6')][0] for p in P37], statistics.median, 1)
    b = interval([C[(p, w, 'ci')][0] - C[(p, w, 'ci')][1] for p in P37], statistics.median, 1)
    say(f'   median C {w}: seed 1 {100*a[0]:.1f} to {100*a[1]:.1f}; median CI difference older minus at-or-newer {w}: {100*b[0]:+.1f} to {100*b[1]:+.1f}')

# ---------------------------------------------------------------- F. boto3 tests
say('')
say('F. The four tests')
for w in ('W0', 'W1', 'W2'):
    b = PYC[('boto3', w)]
    c = PYC[('botocore', w)]
    t = sum(b.values())
    b39 = sum(n for (s, m), n in b.items() if m == '3.9')
    c39 = sum(n for (s, m), n in c.items() if m == '3.9')
    ct = sum(c.values())
    below = sum(n for (s, m), n in b.items() if m == '3.9' and pv(s) is not None and pv(s) < Version('1.42.97'))
    say(f'   {w}: boto3 3.9 {b39:,} of {t:,} = {100*b39/t:.1f}; ratio on 3.9 {b39/c39:.2f}, all {t/ct:.2f}; below 1.42.97 {100*below/b39:.1f}')
e39 = edge('boto3', '3.9')
say(f'   highest usable boto3 below R0 ({R0["boto3"]}) admitting 3.9: {e39}; boto3 R0 excludes 3.9 in W1 and W2: '
    f'{excluded("boto3","3.9","W1")} {excluded("boto3","3.9","W2")}')


def profile(p, w, m, start):
    c = defaultdict(int)
    for (s, mm), n in PYC[(p, w)].items():
        v = pv(s)
        if mm == m and v is not None and not v.is_prerelease and v < R0[p] and (start is None or v <= start):
            c[v] += n
    return [n for _, n in sorted(c.items(), reverse=True)]


def flat(seq):
    body = seq[1:101]
    rel = [abs(b - a) / a for a, b in zip(body, body[1:]) if a]
    return statistics.median(rel)


def plateau(seq):
    med = [statistics.median(seq[max(0, i - 4):i + 5]) for i in range(len(seq))]
    return sum(min(x, 1.5 * m) for x, m in zip(seq[1:], med[1:]))


for w in ('W0', 'W1', 'W2'):
    seq = profile('boto3', w, '3.9', e39)
    blocks = [statistics.median(seq[1 + 20 * i:21 + 20 * i]) for i in range(len(seq[1:]) // 20)]
    ix = {str(v): n for v, n in zip(sorted({pv(s) for (s, m) in PYC[('boto3', w)] if m == '3.9' and pv(s) is not None and not pv(s).is_prerelease and pv(s) < R0['boto3'] and pv(s) <= e39}, reverse=True), seq)}
    say(f'   {w}: boto3 3.9 flatness {flat(seq):.4f}; versions {len(seq)}; blocks 1, 5, 6, 25, 26, 40: '
        f'{blocks[0]:,.0f} {blocks[4]:,.0f} {blocks[5]:,.0f} {blocks[24]:,.0f} {blocks[25]:,.0f} {blocks[-1]:,.0f}; '
        f'blocks 1 to 5 range {min(blocks[:5]):,.0f} to {max(blocks[:5]):,.0f}, 6 to 25 {min(blocks[5:25]):,.0f} to {max(blocks[5:25]):,.0f}, '
        f'26 on {min(blocks[25:]):,.0f} to {max(blocks[25:]):,.0f}; 1.42.87 ratio {ix["1.42.87"]/((ix["1.42.86"]+ix["1.42.88"])/2):.2f}')

# ---------------------------------------------------------------- G. walk-shaped share, pooled
say('')
say('G. Walk-shaped share of older downloads (measure 4), reviewer\'s implementation')
for w in ('W0', 'W1', 'W2'):
    tot_w = tot_o = 0
    per = {}
    for p in P37:
        minors = {m for (s, m) in PYC[(p, w)] if re.fullmatch(r'\d+\.\d+', m or '')}
        mass = 0
        for m in minors:
            st = edge(p, m) if excluded(p, m, w) else None
            if excluded(p, m, w) and st is None:
                continue
            seq = profile(p, w, m, st)
            if len(seq) < 12 or sum(seq) < 1_000_000:
                continue
            if flat(seq) < 0.05:
                mass += plateau(seq)
        older = sum(n for (s, m), n in PYC[(p, w)].items() if klass(p, s) == 'older')
        per[p] = mass / older
        tot_w += mass
        tot_o += older
    say(f'   {w}: pooled {100*tot_w/tot_o:.1f}; median {100*statistics.median(per.values()):.1f}; boto3 {100*per["boto3"]:.1f}, aiobotocore {100*per["aiobotocore"]:.1f}, '
        f'botocore {100*per["botocore"]:.1f}, anyio {100*per["anyio"]:.1f}, fsspec {100*per["fsspec"]:.1f}, grpcio-status {100*per["grpcio-status"]:.1f}, litellm {100*per["litellm"]:.1f}; over a tenth {sum(x > 0.1 for x in per.values())}')

open(os.path.join(HERE, 'r0046_reproduce.txt'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
