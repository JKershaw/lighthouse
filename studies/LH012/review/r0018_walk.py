#!/usr/bin/env python3
"""R-0018, section I: how much of each count-by-version profile is a plateau (the same count at version after
version), how flat it is, and whether it continues above R on an admitted Python. Offline, from
data/week/python/<project>.csv and data/reference.csv; no count is re-read.

Decomposition, per project and Python minor, over the versions ordered newest first: the running median of the
counts over a window of nine versions is the plateau; what a version carries above 1.5 times that median is a
spike (a version fetched for itself: a pin, a list, a fresh install at an edge); the rest is plateau mass.
Flatness is the median absolute relative change between adjacent versions among the first 100 versions below
the start, so a walk that fetches each of them once per resolve gives a value near zero and lists give a large
one. Output: review/r0018_walk.txt."""
import csv, os, re, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
OUT = os.path.join(HERE, 'r0018_walk.txt')
try:
    from packaging.version import Version, InvalidVersion
except ImportError:
    class InvalidVersion(Exception):
        pass

    class Version:
        def __init__(self, s):
            if not re.match(r'^\d+(\.\d+)*$', s):
                raise InvalidVersion(s)
            self.k = tuple(int(x) for x in s.split('.')); self.is_prerelease = False

        def __lt__(self, o): return self.k < o.k
        def __le__(self, o): return self.k <= o.k
        def __ge__(self, o): return self.k >= o.k
        def __gt__(self, o): return self.k > o.k
        def __eq__(self, o): return self.k == o.k
        def __hash__(self): return hash(self.k)


def V(s):
    try:
        v = Version(s)
        return None if v.is_prerelease else v
    except InvalidVersion:
        return None


def rd(*p):
    with open(os.path.join(*p), newline='') as f:
        return list(csv.DictReader(f))


REF = {r['project']: r for r in rd(DATA, 'reference.csv')}
ADM = {(r['project'], r['python_minor']): r for r in rd(DATA, 'python_admission.csv')}
lines = []


def say(*a):
    lines.append(' '.join(str(x) for x in a))


def counts(p, m, below_R=True):
    R = Version(REF[p]['R'])
    c = defaultdict(int)
    for r in rd(DATA, 'week', 'python', p + '.csv'):
        if r['python_minor'] == m:
            v = V(r['version'])
            if v is not None and (v < R or not below_R):
                c[v] += int(r['n'])
    return sorted(c.items(), key=lambda kv: kv[0], reverse=True)


def decompose(seq, start_index=0):
    n = [k for _, k in seq]
    med = []
    for i in range(len(n)):
        w = n[max(0, i - 4):i + 5]
        med.append(statistics.median(w))
    plateau = sum(min(x, 1.5 * mm) for x, mm in zip(n, med))
    spike = sum(n) - plateau
    body = n[start_index + 1:start_index + 101]
    rel = [abs(y - x) / x for x, y in zip(body, body[1:]) if x]
    flat = statistics.median(rel) if rel else float('nan')
    return sum(n), plateau, spike, flat


say('I. Plateau against spike mass in the count-by-version profiles of older downloads (data/week/python/*.csv)')
say('   plateau: what versions carry up to 1.5 times the running median of their nine neighbours; spike: the rest.')
say('   flatness: median |relative change| between adjacent versions over the first 100 versions below the start.')
say('')
say(f'   {"project":<18}{"Python":>7}{"class":>10}{"start":>12}{"older dl":>14}{"start version":>14}{"plateau":>9}{"spike":>7}{"flatness":>10}')
tot_plateau_excl = 0
rows = []
for p in sorted(REF):
    for m in ('2.7', '3.6', '3.7', '3.8', '3.9', '3.10', '3.11', '3.12', '3.13'):
        a = ADM.get((p, m))
        if a is None:
            continue
        excluded = a['any_ge_R_admits'] == 'False'
        seq = counts(p, m)
        if excluded and a['edge_below_R']:
            e = Version(a['edge_below_R'])
            seq = [kv for kv in seq if kv[0] <= e]
        if len(seq) < 12 or sum(k for _, k in seq) < 1_000_000:
            continue
        t, pl, sp, fl = decompose(seq)
        start_share = seq[0][1] / t
        rows.append((p, m, 'excluded' if excluded else 'admitted', str(seq[0][0]), t, start_share, (pl - min(seq[0][1], 1.5 * statistics.median([k for _, k in seq[:9]]))) / t, sp / t, fl))
for p, m, cl, st, t, ss, pl, sp, fl in sorted(rows, key=lambda r: r[8]):
    say(f'   {p:<18}{m:>7}{cl:>10}{st:>12}{t:>14,}{100 * ss:>13.1f}%{100 * pl:>8.1f}%{100 * sp:>6.1f}%{fl:>10.3f}')
say('')
say('   (start version: the share at the edge on an excluded Python, or at the highest version below R on an admitted one;')
say('    plateau here excludes the start version; the three columns need not sum to 100 where the start is itself a spike)')
say('')

# the boto3 family in detail: implied walk depth and mass
say('J. boto3 on Python 3.9: the walk in numbers')
seq = counts('boto3', '3.9')
e = Version(ADM[('boto3', '3.9')]['edge_below_R'])
seq = [kv for kv in seq if kv[0] <= e]
n = [k for _, k in seq]
T = sum(n)
say(f'   downloads at the edge 1.42.97: {n[0]:,}; below it: {T - n[0]:,}')
for d in (1, 10, 50, 100, 200, 300, 500, 700, 1000, 1500, 2000):
    if d < len(n):
        say(f'   count at depth {d:>4} below the edge (version {seq[d][0]}): {n[d]:>10,}   cumulative below the edge to here: {sum(n[1:d + 1]):>13,}')
# fit: the number of resolves reaching each depth is the count there; total wheels fetched per week by the walk = sum
say(f'   if each count is the number of resolves reaching that depth, the walk fetched {T - n[0]:,} wheels in the week,')
say(f'   from about {n[1]:,} resolves that went at least one version deep ({n[1] / 7:,.0f} a day) and about {n[500]:,} that went 500 deep ({n[500] / 7:,.0f} a day).')
say('')

# above R on admitted Pythons: does the plateau continue through the at-or-newer versions?
say('K. boto3 on admitted Pythons, all versions newest first, to see whether the plateau continues above R (1.43.78)')
for m in ('3.10', '3.11', '3.12'):
    seq = counts('boto3', m, below_R=False)
    say(f'   Python {m}: ' + ', '.join(f'{v}:{k:,}' for v, k in seq[:36]))
say('')
say('L. botocore on Python 3.9, the same, from the edge')
seq = counts('botocore', '3.9')
e = Version(ADM[('botocore', '3.9')]['edge_below_R'])
seq = [kv for kv in seq if kv[0] <= e]
n = [k for _, k in seq]
for d in (0, 1, 10, 50, 100, 110, 120, 200, 500, 1000):
    if d < len(n):
        say(f'   depth {d:>4} ({seq[d][0]}): {n[d]:>12,}')
say('')
say('M. The share of all 37 projects\' older downloads that is plateau mass on excluded Pythons, and boto3\'s part of it')
pl_all = 0; pl_boto = 0; older_all = 0
for p in sorted(REF):
    for r in rd(DATA, 'python.csv') if False else []:
        pass
pyr = {r['project']: r for r in rd(os.path.join(DATA, 'analysis'), 'python.csv')}
older_all = sum(int(r['older_W2']) for r in pyr.values())
for p, m, cl, st, t, ss, pl, sp, fl in rows:
    if cl == 'excluded':
        pl_all += pl * t
        if p == 'boto3':
            pl_boto += pl * t
say(f'   pooled older downloads {older_all:,}; plateau mass below the edges on excluded Pythons {pl_all:,} ({100 * pl_all / older_all:.1f} per cent), '
    f'of which boto3 {pl_boto:,} ({100 * pl_boto / older_all:.1f} per cent of pooled older downloads)')
say('   (projects and minors with under a million older downloads, or under 12 versions, are left out of this sum)')
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
