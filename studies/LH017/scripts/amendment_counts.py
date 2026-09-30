"""LH017: how many jobs and pairs each amendment changes (amendments.md).

Run after `LH017_DATA=<dir> LH017_NO_A1=1 python3 collect.py read && ... classify.py` (and the same with LH017_NO_A2=1),
each into its own directory holding copies of frame.csv and frame_files.csv; the reads need the clones, since the
amendments change what the rules ask of the tree. Compares the script's classes there with data/job_classes.csv.

python3 amendment_counts.py <dir with amendment 1 off> <dir with amendment 2 off>   writes data/amendment_counts.txt
"""
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402


def pc(rows):
    cs = [r['script_class'] for r in rows]
    if not cs:
        return 'no CI'
    if '1' in cs:
        return 'reads the pin'
    if '6' in cs or 'to judge' in cs:
        return 'undetermined or to judge'
    if any(c in ('2', '3', '4') for c in cs):
        return 'does not read the pin'
    return "nothing of the project's requirements"


def main():
    main_rows = {(r['pair_id'], r['job_key']): r for r in csv.DictReader(open(os.path.join(DATA, 'job_classes.csv')))}
    out = []
    for name, d in (('amendment 1', sys.argv[1]), ('amendment 2', sys.argv[2])):
        o = {(r['pair_id'], r['job_key']): r for r in csv.DictReader(open(os.path.join(d, 'job_classes.csv')))}
        ch = [(k, o[k]['script_class'], main_rows[k]['script_class']) for k in main_rows
              if k in o and o[k]['script_class'] != main_rows[k]['script_class']]
        out.append(f'{name}: {len(ch)} jobs change the script\'s class, in {len({k[0][0] for k in ch})} pairs and '
                   f'{len({k[0][1].split("@")[0] for k in ch})} repositories; jobs only in one run: '
                   f'{len(set(o) ^ set(main_rows))}')
        for (a, b), n in sorted(collections.Counter((x, y) for _, x, y in ch).items(), key=lambda x: -x[1]):
            out.append(f'  without -> with: class {a} -> {b}: {n}')
        bm, bo = collections.defaultdict(list), collections.defaultdict(list)
        for k, r in main_rows.items():
            bm[k[0]].append(r)
        for k, r in o.items():
            bo[k[0]].append(r)
        for p in sorted(bm):
            if pc(bo[p]) != pc(bm[p]):
                out.append(f'  pair {p}, by the script\'s classes: {pc(bo[p])} -> {pc(bm[p])}')
        out.append('  pairs changed: ' + ' '.join(sorted({k[0][0] for k in ch})))
    open(os.path.join(DATA, 'amendment_counts.txt'), 'w').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
