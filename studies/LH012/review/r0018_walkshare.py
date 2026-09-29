#!/usr/bin/env python3
"""R-0018, section N: how much of each project's older downloads is walk-shaped, from the same decomposition as
r0018_walk.py (plateau mass on profiles whose flatness is under 0.05, "clear", and under 0.2, "probable"), as a
share of the project's older downloads in data/analysis/python.csv. Offline. Output: review/r0018_walkshare.txt."""
import csv, os, re, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
OUT = os.path.join(HERE, 'r0018_walkshare.txt')
from packaging.version import Version, InvalidVersion


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
PY = {r['project']: r for r in rd(DATA, 'analysis', 'python.csv')}
lines = []


def say(*a):
    lines.append(' '.join(str(x) for x in a))


def decompose(seq):
    n = [k for _, k in seq]
    med = [statistics.median(n[max(0, i - 4):i + 5]) for i in range(len(n))]
    plateau = sum(min(x, 1.5 * mm) for x, mm in zip(n, med)) - min(n[0], 1.5 * med[0])  # without the start version
    body = n[1:101]
    rel = [abs(y - x) / x for x, y in zip(body, body[1:]) if x]
    return sum(n), plateau, statistics.median(rel) if rel else float('nan')


say('N. Walk-shaped mass per project: plateau mass (without the start version) on profiles with flatness under 0.05 (clear)')
say('   and under 0.2 (probable), as a share of the project\'s older downloads (python.csv older_W2); minors with at least')
say('   a million older downloads and twelve versions below the start; both excluded and admitted Pythons.')
say('')
say(f'   {"project":<18}{"older downloads":>16}{"clear walk":>12}{"probable":>10}   minors with a clear walk (flatness)')
tot_clear = tot_prob = tot_older = 0
out = []
for p in sorted(REF):
    R = Version(REF[p]['R'])
    by = defaultdict(lambda: defaultdict(int))
    for r in rd(DATA, 'week', 'python', p + '.csv'):
        v = V(r['version'])
        if v is not None and v < R:
            by[r['python_minor']][v] += int(r['n'])
    clear = prob = 0.0
    names = []
    for m, c in by.items():
        a = ADM.get((p, m))
        if a is None:
            continue
        seq = sorted(c.items(), key=lambda kv: kv[0], reverse=True)
        if a['any_ge_R_admits'] == 'False' and a['edge_below_R']:
            e = Version(a['edge_below_R'])
            seq = [kv for kv in seq if kv[0] <= e]
        if len(seq) < 12 or sum(k for _, k in seq) < 1_000_000:
            continue
        t, pl, fl = decompose(seq)
        if fl < 0.05:
            clear += pl; prob += pl; names.append(f'{m} ({fl:.3f})')
        elif fl < 0.2:
            prob += pl
    older = int(PY[p]['older_W2'])
    tot_older += older; tot_clear += clear; tot_prob += prob
    out.append((p, older, clear / older, prob / older, ', '.join(sorted(names, key=lambda s: float(s.split('(')[1][:-1])))))
for p, older, c, pr, names in sorted(out, key=lambda x: -x[2]):
    if pr > 0.005:
        say(f'   {p:<18}{older:>16,}{100 * c:>11.1f}%{100 * pr:>9.1f}%   {names}')
say(f'   pooled over the 37: older downloads {tot_older:,}; clear walk {tot_clear:,.0f} ({100 * tot_clear / tot_older:.1f} per cent); probable {tot_prob:,.0f} ({100 * tot_prob / tot_older:.1f} per cent)')
say('   the pooled older share O with the clear walk set aside: '
    + f'{100 * (tot_older - tot_clear) / (sum(int(r["W2_total"]) for r in PY.values()) - tot_clear):.1f} per cent (record: 45.6)')
med = statistics.median(x[2] for x in out)
say(f'   median over projects of the clear-walk share: {100 * med:.1f} per cent; projects with a clear walk over a tenth of older downloads: {sum(1 for x in out if x[2] > 0.1)}')
open(OUT, 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
