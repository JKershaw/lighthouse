#!/usr/bin/env python3
"""R-0021 stage B: what moved between LH015 record 0.1 (commit 2eb774f) and 0.2.

Reads the 0.1 class tables out of git history (read-only) into the scratchpad,
compares every build's class and every pair's class with the current tables,
and prints the moves with the reason each one is expected to have (the blind
check's three errors, the wheel rule, amendment 7, amendment 2 as written).
Also prints the frame facts the piece rests on. Output is kept as
r0021_corrections.txt.
"""
import csv
import io
import os
import subprocess
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
DATA = os.path.join(HERE, '..', 'data')
OLD = '2eb774f'


def old(name):
    txt = subprocess.run(['git', 'show', f'{OLD}:studies/LH015/data/{name}'], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return list(csv.DictReader(io.StringIO(txt)))


def cur(name):
    with open(os.path.join(DATA, name), newline='') as fh:
        return list(csv.DictReader(fh))


def main():
    o = {r['build_id']: r for r in old('recipe_classes.csv')}
    n = {r['build_id']: r for r in cur('recipe_classes.csv')}
    print('builds: 0.1 %d, 0.2 %d, same ids: %s' % (len(o), len(n), set(o) == set(n)))
    moved = [(b, o[b], n[b]) for b in sorted(o) if o[b]['class'] != n[b]['class']]
    print('builds whose class changed: %d, at snapshots %d' % (len(moved), sum(r['role'] == 'snapshot' for _, r, _ in moved)))
    for b, a, c in moved:
        print('  %-11s %-8s %s %-26s -> %s %-22s decided_by %s -> %s | %s' % (
            b, a['role'], a['class'], a['sub'][:26], c['class'], c['sub'][:22], a['decided_by'], c['decided_by'],
            (c['reason'] or c['judge_reason'])[:90]))
    subonly = [b for b in o if o[b]['class'] == n[b]['class'] and (o[b]['sub'], o[b]['flags']) != (n[b]['sub'], n[b]['flags'])]
    print('builds whose sub-label or flags changed with the same class: %d' % len(subonly))
    for b in subonly[:20]:
        print('  %-11s %s [%s] -> %s [%s]' % (b, o[b]['sub'], o[b]['flags'], n[b]['sub'], n[b]['flags']))
    dec = [b for b in o if o[b]['decided_by'] != n[b]['decided_by']]
    print('builds that moved between script and writer pools: %s' % dec)
    print('0.2 decided_by at snapshots:', Counter(r['decided_by'] for r in n.values() if r['role'] == 'snapshot'))
    print('0.2 decided_by all:', Counter(r['decided_by'] for r in n.values()))

    po = {r['pair_id']: r for r in old('pair_classes.csv')}
    pn = {r['pair_id']: r for r in cur('pair_classes.csv')}
    for col in ('pair_class', 'head_class', 'mixed', 'main_class', 'r3_only', 'reads_T_lock', 'relock_class'):
        ch = [(p, po[p][col], pn[p][col]) for p in sorted(po) if po[p][col] != pn[p][col]]
        print('pairs whose %s changed: %d' % (col, len(ch)))
        for p, a, b in ch:
            print('   %s %s: %s -> %s' % (p, pn[p]['repo'], a, b))

    # frame facts the piece rests on
    fr = cur('frame.csv')
    libs = sorted({r['library'] for r in fr})
    print('\nframe: %d pairs, %d repositories, %d libraries, %d events' % (
        len(fr), len({r['repo'] for r in fr}), len(libs), len({(r['library'], r['threshold']) for r in fr})))
    print('libraries:', ' '.join(libs))
    rel = sorted(r['release_time'] for r in fr)
    snap = sorted(r['snapshot_time'] for r in fr)
    print('release_time range: %s .. %s' % (rel[0], rel[-1]))
    print('snapshot_time range: %s .. %s' % (snap[0], snap[-1]))
    for r in fr:
        if 'bbot' in r['repo']:
            print('bbot row:', {k: r[k] for k in ('pair_id', 'repo', 'library', 'threshold', 'pair_fix', 'event_kind', 'release_time',
                                                  'advisory_time', 'source_study', 'snapshot_commit', 'snapshot_time', 'pin_class',
                                                  'timed_files', 'outcome', 'lag_release_days')})
            print('   pair class:', pn[r['pair_id']]['pair_class'], '| classes:', pn[r['pair_id']]['classes'])
            for b, rr in n.items():
                if rr['pair_id'] == r['pair_id']:
                    print('   build', b, rr['role'], rr['path'], rr['class'], rr['sub'], '|', rr['reason'][:100])


if __name__ == '__main__':
    main()
