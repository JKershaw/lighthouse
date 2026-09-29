#!/usr/bin/env python3
"""R-0018, section H: the shape of the count-by-version profile of older downloads, from the retained W sums by
version and Python minor (data/week/python/<project>.csv). Offline; no count is re-read.

Why: an installer that backtracks through versions during a resolve fetches the newest admitted version first and
then successively older ones until one fits, so the count at each version is the number of resolves that went at
least that deep: a staircase that never rises as the version gets older. Environments rebuilt from lists frozen at
many dates leave a jagged profile, since some versions were current on days more lists were frozen. So, for each
project and Python minor, versions are ordered from the highest admitted version downwards and the share of
adjacent pairs where the older version has at most the count of the newer one is reported, with the profile's
first values. Output: review/r0018_staircase.txt."""
import csv, os, re, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
OUT = os.path.join(HERE, 'r0018_staircase.txt')
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


def profile(p, m, top=12, depth=None):
    R = Version(REF[p]['R'])
    a = ADM.get((p, m))
    excluded = a is not None and a['any_ge_R_admits'] == 'False'
    edge = Version(a['edge_below_R']) if excluded and a['edge_below_R'] else None
    c = defaultdict(int)
    for r in rd(DATA, 'week', 'python', p + '.csv'):
        if r['python_minor'] == m:
            v = V(r['version'])
            if v is not None and v < R:
                c[v] += int(r['n'])
    if not c:
        say(f'   {p} on {m}: no older downloads'); return
    seq = sorted(c.items(), key=lambda kv: kv[0], reverse=True)  # newest first
    if excluded and edge is not None:
        seq = [kv for kv in seq if kv[0] <= edge]  # the walk starts at the edge on an excluded Python
    if depth:
        seq = seq[:depth]
    n = [k for _, k in seq]
    tot = sum(n)
    pairs = list(zip(n, n[1:]))
    down = sum(1 for x, y in pairs if y <= x)
    strict_up = sum(1 for x, y in pairs if y > 1.05 * x)
    head = ', '.join(f'{str(v)}:{k:,}' for v, k in seq[:top])
    say(f'   {p} on {m} ({"excluded" if excluded else "admitted"}; start {seq[0][0]}): {len(seq)} versions, {tot:,} downloads;'
        f' non-rising pairs {down}/{len(pairs)} = {100 * down / len(pairs):.0f} per cent; rises above 5 per cent: {strict_up}')
    say(f'      from the top: {head}')
    # the walk in blocks of twenty versions from the top: median count per block
    blocks = [statistics.median(n[i:i + 20]) for i in range(0, min(len(n), 600), 20)]
    say('      median count per block of 20 versions, from the top: ' + ', '.join(f'{int(b):,}' for b in blocks[:25]))


say('H. Count-by-version profiles of older downloads, newest first (data/week/python/*.csv)')
say('   A backtracking resolve leaves a staircase that never rises with depth; frozen lists leave a jagged profile.')
say('')
for p, m in (('boto3', '3.9'), ('boto3', '3.8'), ('boto3', '3.7'), ('boto3', '3.10'), ('boto3', '3.12'),
             ('botocore', '3.9'), ('botocore', '3.12'), ('s3transfer', '3.9'),
             ('aiobotocore', '3.9'), ('aiobotocore', '3.12'), ('fsspec', '3.9'), ('fsspec', '3.12'),
             ('numpy', '3.9'), ('numpy', '3.11'), ('pandas', '3.9'), ('pandas', '3.10'), ('urllib3', '3.9'), ('requests', '3.9'),
             ('certifi', '3.12'), ('requests', '3.12'), ('typing-extensions', '3.12'), ('pytest', '3.12'), ('cryptography', '3.12')):
    profile(p, m)
    say('')
say('   Note: on an excluded Python the walk is taken from the edge, the highest version below R that admits it; on an admitted')
say('   Python a fresh resolve lands at or above R, so older versions there are reached only by a constraint or a list.')
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
