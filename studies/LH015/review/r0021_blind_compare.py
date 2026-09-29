#!/usr/bin/env python3
"""R-0021 stage A: compare the reviewer's blind classes with the writer's.

Reads review/r0021_blind.csv (the reviewer's classes, written before any of
the writer's classes were opened), data/recipe_classes.csv, data/judgements.csv,
data/recipes.csv and data/pair_classes.csv. For every disagreement it
recomputes the pair's class under the brief's pair rule with the reviewer's
class substituted, and says whether the pair's class would change. Output goes
to stdout; the record keeps it as r0021_blind_compare.txt.

Run: python3 studies/LH015/review/r0021_blind_compare.py > studies/LH015/review/r0021_blind_compare.txt
"""
import csv
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')


def load(path):
    with open(path, newline='') as fh:
        return list(csv.DictReader(fh))


def pair_class(classes):
    """The brief's pair rule over the classes of all builds of a pair's primary recipes."""
    cs = [int(c) for c in classes]
    if not cs:
        return 'no recipe'
    if all(c == 5 for c in cs):
        return "nothing of the project's requirements"
    if any(c in (2, 3, 4) for c in cs):
        return 'not from the pinned file' + (' (mixed)' if any(c == 1 for c in cs) else '')
    if any(c == 1 for c in cs) and all(c in (1, 5) for c in cs):
        return 'from the pinned file'
    return 'undetermined'


def main():
    mine = {r['build_id']: r for r in load(os.path.join(HERE, 'r0021_blind.csv'))}
    writer = {r['build_id']: r for r in load(os.path.join(DATA, 'recipe_classes.csv'))}
    judged = {r['build_id']: r for r in load(os.path.join(DATA, 'judgements.csv'))}
    recipes = {r['build_id']: r for r in load(os.path.join(DATA, 'recipes.csv'))}
    pairs = {r['pair_id']: r for r in load(os.path.join(DATA, 'pair_classes.csv'))}

    # builds of primary recipes per (pair, role), for the pair rule
    by_pair_role = defaultdict(list)
    for bid, r in writer.items():
        if recipes[bid]['primary'] == 'yes':
            by_pair_role[(r['pair_id'], r['role'])].append(bid)

    # check the writer's stored pair classes are reproduced by pair_class() at snapshots
    mism = 0
    for pid, p in pairs.items():
        if p['status'] != 'read' or p['keeps_recipe'] != 'yes':
            continue
        got = pair_class([writer[b]['class'] for b in by_pair_role[(pid, 'snapshot')]])
        want = p['pair_class'] + (' (mixed)' if p['mixed'] == 'yes' else '')
        if got != want:
            mism += 1
            print('pair rule mismatch', pid, got, '!=', want)
    print('pair rule reproduced for snapshots; mismatches:', mism)

    print()
    print('== per build (group | build | role | writer class/sub [flags] | reviewer class/sub | agree)')
    agree = Counter()
    total = Counter()
    by_pc = defaultdict(lambda: [0, 0])
    disagreements = []
    for bid in sorted(mine, key=lambda b: (mine[b]['group'] != 'script-decided', b)):
        m, w = mine[bid], writer[bid]
        g = m['group']
        assert (w['decided_by'] == 'script') == (g == 'script-decided'), bid
        same = m['reviewer_class'] == w['class']
        total[g] += 1
        agree[g] += same
        p = pairs[w['pair_id']]
        pc = p['pair_class'] if w['role'] == 'snapshot' else 'head: ' + p['head_class']
        by_pc[pc][0] += same
        by_pc[pc][1] += 1
        wsub = w['sub'] + (' [' + w['flags'] + ']' if w['flags'] else '')
        print('%-14s %-10s %-8s | W %s %-28s | R %s %-28s | %s' % (
            g, bid, w['role'], w['class'], wsub[:28], m['reviewer_class'], m['reviewer_sublabel'][:28],
            'agree' if same else 'DISAGREE'))
        if not same:
            disagreements.append(bid)

    print()
    print('== agreement per half')
    for g in ('script-decided', 'judged'):
        print('  %-15s %d of %d' % (g, agree[g], total[g]))
    print('  %-15s %d of %d' % ('all', sum(agree.values()), sum(total.values())))
    print()
    print("== agreement per resulting pair class (the writer's pair class of the build's pair at its role)")
    for pc, (a, n) in sorted(by_pc.items()):
        print('  %-45s %d of %d' % (pc, a, n))

    print()
    print('== disagreements: would the pair class change with the reviewer classes substituted?')
    changes = Counter()
    for bid in disagreements:
        m, w = mine[bid], writer[bid]
        pid, role = w['pair_id'], w['role']
        builds = by_pair_role[(pid, role)]
        before = pair_class([writer[b]['class'] for b in builds])
        # substitute every reviewer class of this pair and role that disagrees (they stand or fall together)
        after = pair_class([mine[b]['reviewer_class'] if b in mine else writer[b]['class'] for b in builds])
        changed = before != after
        changes[(m['group'], changed)] += 1
        print('- %s (%s, %s, %s): writer %s %s [%s] -> reviewer %s %s' % (
            bid, m['group'], role, pid, w['class'], w['sub'], w['flags'], m['reviewer_class'], m['reviewer_sublabel']))
        print('    writer reason : %s' % (w['reason'] or judged.get(bid, {}).get('reason', ''))[:300])
        if bid in judged and judged[bid]['reason'] != w['reason']:
            print('    judge reason  : %s' % judged[bid]['reason'][:300])
        print('    reviewer reason: %s' % m['reviewer_reason'][:300])
        print('    other builds of this pair and role: %s' % ' '.join(
            '%s=%s' % (b, writer[b]['class']) for b in builds if b != bid))
        print('    pair class %s: %s -> %s  (%s)' % (role, before, after, 'CHANGES' if changed else 'unchanged'))
    print()
    print('== counts of disagreements by half and whether the pair class changes (before resolution)')
    for (g, ch), n in sorted(changes.items()):
        print('  %-15s %-10s %d' % (g, 'changes' if ch else 'unchanged', n))


if __name__ == '__main__':
    main()
