#!/usr/bin/env python3
"""R-0026, stage B: independent recomputation of LH017's primary shares from data/pairs.csv, one bootstrap interval
recomputed with a different implementation (numpy is not assumed; plain Python, seed 26 rather than the study's),
the one-fifth rule per measure frame, and the effect on P2 and P3 of the two pair classes the review found wrong
(P327 ai-parrot: reads the pin, not "does not read"; P277 and P278 chain-gang: undetermined, not "does not read").
Run from the repository root: python3 studies/LH017/review/r0026_checks.py > studies/LH017/review/r0026_checks.txt."""
import csv
import random
from collections import defaultdict

D = 'studies/LH017/data/'
P = [r for r in csv.DictReader(open(D + 'pairs.csv')) if r['status'] == 'read']
M = {r['measure'] + '|' + r['view']: r for r in csv.DictReader(open(D + 'measures.csv'))}


def label(s):
    return 'as a rule' if s >= 0.75 else ('for some pairs' if s >= 0.5 else 'not as a rule')


def pct(xs, q):
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def share(pairs, num, den):
    n = sum(1 for p in pairs if den(p) and num(p))
    d = sum(1 for p in pairs if den(p))
    return n, d


def boot(pairs, num, den, B=4000, seed=26):
    by = defaultdict(list)
    for p in pairs:
        by[p['repo']].append(p)
    repos = sorted(by)
    rnd = random.Random(seed)
    out = []
    for _ in range(B):
        n = d = 0
        for _ in range(len(repos)):
            for p in by[repos[rnd.randrange(len(repos))]]:
                if den(p):
                    d += 1
                    n += bool(num(p))
        if d:
            out.append(n / d)
    return pct(out, 0.025), pct(out, 0.975)


def report(name, pairs, num, den, key=None, interval=True):
    n, d = share(pairs, num, den)
    s = n / d if d else float('nan')
    line = f'{name}: {n} of {d} = {100 * s:.1f} per cent, {label(s)}'
    if interval:
        lo, hi = boot(pairs, num, den)
        line += f'; interval (reviewer, 4,000 resamples, seed 26) {100 * lo:.1f} to {100 * hi:.1f}'
    if key and key in M:
        m = M[key]
        line += f' | record: {m["num"]} of {m["den"]} = {100 * float(m["share"]):.1f} ({100 * float(m["lo"]):.1f} to {100 * float(m["hi"]):.1f}) {m["label"] or "no label"}'
    print(line)


decided = lambda p: p['pair_class'] in ('reads the pin', 'does not read the pin')
reads = lambda p: p['pair_class'] == 'reads the pin'
frame2 = lambda p: p['pair_class'] in ('reads the pin', 'does not read the pin', 'undetermined')
lock = lambda p: p['pin_class'] in ('lockfile', 'both')
ldec = lambda p: lock(p) and p['lock_class'] in ('reads the timed lock', 'does not')
lreads = lambda p: p['lock_class'] == 'reads the timed lock'
lframe = lambda p: lock(p) and p['lock_class'] in ('reads the timed lock', 'does not', 'undetermined')

print('Primary shares recomputed from pairs.csv (pairs view), beside measures.csv:')
report('P1 keeps CI', P, lambda p: p['keeps_ci'] == 'yes', lambda p: True, 'P1 keeps CI|pairs')
report('P2 all', P, reads, decided, 'P2 reads the pin, all|pairs')
for cls in ('lockfile', 'exact pin', 'both'):
    report(f'P2 {cls}', P, reads, lambda p, c=cls: decided(p) and p['pin_class'] == c, f'P2 reads the pin, {cls}|pairs', interval=False)
report('P3', P, lreads, ldec, 'P3 reads the timed lock, pairs with a timed lockfile|pairs')
print()
print('One-fifth rule (undetermined share of each measure frame):')
for name, fr, cond in [('P2 all', frame2, lambda p: True)] + [(f'P2 {c}', frame2, lambda p, c=c: p['pin_class'] == c) for c in ('lockfile', 'exact pin', 'both')] + [('P3', lframe, lambda p: True)]:
    u = sum(1 for p in P if fr(p) and cond(p) and (p['pair_class'] == 'undetermined' if name.startswith('P2') else p['lock_class'] == 'undetermined'))
    d = sum(1 for p in P if fr(p) and cond(p))
    print(f'  {name}: {u} of {d} = {100 * u / d:.1f} per cent {"(label withheld unless both bounds agree)" if u / d > 0.2 else ""}')
print()
print('Keeps-CI check: keeps_ci yes', sum(1 for p in P if p['keeps_ci'] == 'yes'), '; other CI only', sum(1 for p in P if p['other_ci_only'] == 'yes'))
print()
print('Effect of the review\'s corrections (point estimates; labels by the brief\'s convention):')
fixed = []
for p in P:
    q = dict(p)
    if p['pair_id'] == 'P327':
        q['pair_class'] = 'reads the pin'      # uv sync --package <member> installs the T manifest's project (11 jobs)
    if p['pair_id'] in ('P277', 'P278'):
        q['pair_class'] = 'undetermined'       # the wheel maturin-action built is installed with --find-links, origin untraced
    fixed.append(q)
report('P2 all, corrected', fixed, reads, decided, interval=False)
report('P2 exact pin, corrected', fixed, reads, lambda p: decided(p) and p['pin_class'] == 'exact pin', interval=False)
print('  does not read the pin, corrected:', sum(1 for p in fixed if p['pair_class'] == 'does not read the pin'), '(was 11)')
print('  undetermined, corrected:', sum(1 for p in fixed if p['pair_class'] == 'undetermined'), '(was 48)')
u = sum(1 for p in fixed if frame2(p) and p['pair_class'] == 'undetermined')
d = sum(1 for p in fixed if frame2(p))
print(f'  one-fifth rule, P2 all, corrected: {u} of {d} = {100 * u / d:.1f} per cent')
print('  P3 is unchanged: neither pair has a timed lockfile.')
print()
print('Job-level counts touched by the three classifier defects (from the review\'s reads of ci_lines.csv):')
print('  xargs <installer> unrecognised: 34 job rows (an-website at six snapshots, one homeassistant-ai/ha-mcp job), classed 5 "no Python install" where an install step runs; no pair class changes')
print('  uv sync --package <member> not followed to the member manifest: 14 job rows (ai-parrot 11 in P327, sagewai/platform 3 already class 1 by the lock); P327 changes')
print('  --find-links to a wheel built in the job read as an index install: 5 class 3 rows (chain-gang: P277 one job, P278 four variants); both pairs change')
