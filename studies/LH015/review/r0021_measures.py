#!/usr/bin/env python3
"""R-0021 stage B: the reviewer's own reproduction of LH015's important figures.

Computed from data/pair_classes.csv, data/recipe_classes.csv and data/frame.csv
with code independent of scripts/analyse.py: P1 (pair and repository views),
P2 and its two undetermined bounds overall and by pin class, the pair class
counts (the chart's numbers), the counts behind "not from the pinned file",
R3, S1, the 45 of 90 decided pairs with a lockfile whose build reads it, the
scale bounds 38 and 106 of 469, the main-recipe sensitivity, and a bootstrap
of P1 and P2 with a different seed as a check on the intervals' size (not a
reproduction of the writer's seed). Output is kept as r0021_measures.txt.
"""
import csv
import os
import random
from collections import Counter, defaultdict

from packaging.specifiers import SpecifierSet
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')


def load(name):
    with open(os.path.join(DATA, name), newline='') as fh:
        return list(csv.DictReader(fh))


def pct(xs, p):
    """LH011's percentile: linear interpolation."""
    s = sorted(xs)
    k = (len(s) - 1) * p
    f, c = int(k), min(int(k) + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)


def share(num, den):
    return 100.0 * num / den if den else float('nan')


def main():
    pairs = load('pair_classes.csv')
    builds = load('recipe_classes.csv')
    frame = {r['pair_id']: r for r in load('frame.csv')}
    read = [p for p in pairs if p['status'] == 'read']
    print('pairs read %d of %d; repositories %d' % (len(read), len(pairs), len({p['repo'] for p in read})))

    # P1
    keep = [p for p in read if p['keeps_recipe'] == 'yes']
    print('P1: %d of %d keep a recipe = %.1f%%' % (len(keep), len(read), share(len(keep), len(read))))
    by_repo = defaultdict(list)
    for p in read:
        by_repo[p['repo']].append(p)
    rv = [sum(q['keeps_recipe'] == 'yes' for q in v) / len(v) for v in by_repo.values()]
    print('P1 repository view: %.1f%% over %d repositories; any snapshot %d, every snapshot %d' % (
        100 * sum(rv) / len(rv), len(rv), sum(x > 0 for x in rv), sum(x == 1 for x in rv)))

    # pair classes, overall and by pin class (the chart's numbers)
    order = ['from the pinned file', 'not from the pinned file', 'undetermined', "nothing of the project's requirements", 'no recipe']
    print('pair classes:')
    for pin in ('all', 'lockfile', 'exact pin', 'both'):
        sel = [p for p in read if pin == 'all' or p['pin_class'] == pin]
        c = Counter(p['pair_class'] for p in sel)
        print('  %-10s n=%3d  %s' % (pin, len(sel), '  '.join('%s=%d' % (k[:12], c[k]) for k in order)))
    mixed = sum(p['mixed'] == 'yes' for p in read)
    print('  mixed (a class 1 build beside a class 2 to 4 build): %d' % mixed)

    # P2 and its bounds
    def p2(sel, label):
        f = sum(p['pair_class'] == 'from the pinned file' for p in sel)
        n = sum(p['pair_class'] == 'not from the pinned file' for p in sel)
        u = sum(p['pair_class'] == 'undetermined' for p in sel)
        print('  P2 %-10s %d of %d = %.1f%%; undetermined %d; bounds all-from %.1f%%, all-not %.1f%%' % (
            label, f, f + n, share(f, f + n), u, share(f + u, f + n + u), share(f, f + n + u)))
    print('P2:')
    p2(read, 'all')
    for pin in ('lockfile', 'exact pin', 'both'):
        p2([p for p in read if p['pin_class'] == pin], pin)
    with_recipe = [p for p in read if p['keeps_recipe'] == 'yes']
    und = sum(p['pair_class'] == 'undetermined' for p in with_recipe)
    print('  undetermined among pairs with a recipe: %d of %d = %.1f%% (one fifth = %.1f)' % (
        und, len(with_recipe), share(und, len(with_recipe)), len(with_recipe) / 5))
    # repository view of P2
    rv2 = []
    for v in by_repo.values():
        d = [q for q in v if q['pair_class'] in ('from the pinned file', 'not from the pinned file')]
        if d:
            rv2.append(sum(q['pair_class'] == 'from the pinned file' for q in d) / len(d))
    print('  P2 repository view: %.1f%% over %d repositories' % (100 * sum(rv2) / len(rv2), len(rv2)))
    # main recipe sensitivity
    mf = sum(p['main_class'] == 'from the pinned file' for p in read)
    mn = sum(p['main_class'] == 'not from the pinned file' for p in read)
    print('  P2 main recipe alone: %d of %d = %.1f%%' % (mf, mf + mn, share(mf, mf + mn)))

    # behind "not from the pinned file"
    nf = {p['pair_id']: p for p in read if p['pair_class'] == 'not from the pinned file'}
    snap = [b for b in builds if b['role'] == 'snapshot' and b['pair_id'] in nf]
    has = defaultdict(set)
    for b in snap:
        if b['class'] in ('2', '3', '4'):
            has['class ' + b['class']].add(b['pair_id'])
        if b['class'] == '2':
            has['class 2 ' + b['sub']].add(b['pair_id'])
    print('behind not from the pinned file (%d pairs): %s' % (
        len(nf), '; '.join('%s %d' % (k, len(v)) for k, v in sorted(has.items()))))
    print('  by pin class: %s' % dict(Counter(p['pin_class'] for p in nf.values())))
    # R3
    r3 = [p for p in nf.values() if p['r3_only'] == 'yes']
    f_all = sum(p['pair_class'] == 'from the pinned file' for p in read)
    print('R3: %d of %d not-from pairs rest only on builds that never name L; P2 without them %d of %d = %.1f%%' % (
        len(r3), len(nf), f_all, f_all + len(nf) - len(r3), share(f_all, f_all + len(nf) - len(r3))))
    # scale bounds
    u_all = sum(p['pair_class'] == 'undetermined' for p in read)
    print('scale: not from %d of %d = %.1f%%; with every undetermined pair %d of %d = %.1f%%' % (
        len(nf), len(read), share(len(nf), len(read)), len(nf) + u_all, len(read), share(len(nf) + u_all, len(read))))
    # lockfile pairs whose build reads the timed lock
    dec_lock = [p for p in read if p['pin_class'] in ('lockfile', 'both') and p['pair_class'] in ('from the pinned file', 'not from the pinned file')]
    reads = [p for p in dec_lock if p['reads_T_lock'] == 'yes']
    print('decided pairs with a timed lockfile: %d; a build reads the timed lock itself in %d' % (len(dec_lock), len(reads)))
    noread = [p for p in dec_lock if p['reads_T_lock'] != 'yes']
    print('  the %d without a lock-reading build, by pair class and pin class: %s' % (
        len(noread), dict(Counter((p['pair_class'][:8], p['pin_class']) for p in noread))))
    lu = has.get('class 2 lock unused', set())
    print('  of those, lock unused (class 2 with the timed lock in the context): %d pairs: %s' % (len(lu), ' '.join(sorted(lu))))

    # S1: would a fresh build take the fix?
    print('S1 (reviewer reading of the stored specifiers):')
    s1 = {}
    for pid, p in nf.items():
        fix = Version(frame[pid]['pair_fix'])
        verdicts = []
        for b in snap:
            if b['pair_id'] != pid:
                continue
            specs = []
            if b['class'] == '2' and b['names_L'] == 'yes':
                specs = [s.strip() for s in b['spec'].split('|')]
            elif b['class'] == '3' and b['pypi_spec']:
                specs = [b['pypi_spec']]
            for s in specs:
                if not s or s in ('?', 'any') or s.startswith('poetry:') or ';' in s:
                    verdicts.append('?')
                    continue
                try:
                    verdicts.append('admits' if fix in SpecifierSet(s, prereleases=True) else 'excludes')
                except Exception:
                    verdicts.append('?')
        if 'admits' in verdicts:
            s1[pid] = 'admits'
        elif 'excludes' in verdicts and '?' not in verdicts:
            s1[pid] = 'excludes'
        elif 'excludes' in verdicts:
            s1[pid] = 'excludes or ?'
        else:
            s1[pid] = 'not determined'
    print('  reviewer:', dict(Counter(s1.values())))
    ws1 = {r['pair_id']: r['reading'] for r in load('s1_fresh_build.csv')}
    print('  writer  :', dict(Counter(ws1.values())))
    for pid in sorted(nf):
        if s1[pid].split(' ')[0] != ws1.get(pid, '').split(' ')[0]:
            print('    differs %s: reviewer %s, writer %s' % (pid, s1[pid], ws1.get(pid)))

    # bootstrap check of the intervals' size, a different seed
    repos = sorted(by_repo)
    rng = random.Random(20260930)
    p1s, p2s = [], []
    for _ in range(4000):
        draw = [repos[rng.randrange(len(repos))] for _ in repos]
        ps = [q for r in draw for q in by_repo[r]]
        p1s.append(share(sum(q['keeps_recipe'] == 'yes' for q in ps), len(ps)))
        f = sum(q['pair_class'] == 'from the pinned file' for q in ps)
        n = sum(q['pair_class'] == 'not from the pinned file' for q in ps)
        p2s.append(share(f, f + n))
    print('bootstrap check (4,000 resamples, seed 20260930): P1 %.1f to %.1f; P2 %.1f to %.1f' % (
        pct(p1s, 0.025), pct(p1s, 0.975), pct(p2s, 0.025), pct(p2s, 0.975)))

    # script and writer pools at snapshots
    print('snapshot builds: %d; decided by %s' % (
        sum(b['role'] == 'snapshot' for b in builds), dict(Counter(b['decided_by'] for b in builds if b['role'] == 'snapshot'))))


if __name__ == '__main__':
    main()
