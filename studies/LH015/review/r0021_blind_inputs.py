#!/usr/bin/env python3
"""R-0021 stage A helper: print the stored inputs of one sampled build.

Reads only the tables the review brief allows before the blind classes are
written: data/review_sample.csv, recipes.csv, recipe_lines.csv, aux_lines.csv,
tree_paths.csv, frame_files.csv and pypi.csv. It never opens the writer's
classes (recipe_classes.csv, judgements.csv, pair_classes.csv) or results.

Usage: r0021_blind_inputs.py BUILD_ID [--aux-grep REGEX] [--no-lines]
       r0021_blind_inputs.py --aux-count BUILD_ID
"""
import csv
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data')
FORBIDDEN = {'recipe_classes.csv', 'judgements.csv', 'pair_classes.csv',
             'measures.csv', 'described.csv', 'sensitivities.csv'}


def load(name):
    assert name not in FORBIDDEN and not name.startswith('s'), name
    with open(os.path.join(DATA, name), newline='') as fh:
        return list(csv.DictReader(fh))


def main(argv):
    aux_grep = None
    show_lines = True
    count_only = False
    args = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--aux-grep':
            aux_grep = re.compile(argv[i + 1])
            i += 2
            continue
        if a == '--no-lines':
            show_lines = False
        elif a == '--aux-count':
            count_only = True
        else:
            args.append(a)
        i += 1
    build_id = args[0]
    sample = {r['build_id']: r for r in load('review_sample.csv')}
    s = sample[build_id]
    rec = {r['build_id']: r for r in load('recipes.csv')}[build_id]
    repo, commit, path = s['repo'], s['commit'], s['path']
    print('### BUILD', build_id, s['group'], s['role'], repo, commit, path)
    print('target=%r context=%r how=%r candidates=%r ignore=%r args=%r' % (
        s['target'], s['context'], s['context_how'], rec['context_candidates'],
        s['ignore_file'], s['build_args']))
    print('name_form=%s depth=%s template=%s readable=%s stages=%s final_path=%r own_names=%r note=%r' % (
        rec['name_form'], rec['depth'], rec['template'], rec['readable'],
        rec['stages'], rec['final_path'], rec['own_names'], rec['note']))
    print('L=%s pin_class=%s T=%s' % (s['library'], s['pin_class'], s['T']))
    ff = [r for r in load('frame_files.csv') if r['pair_id'] == s['pair_id']]
    for r in ff:
        print('  T file: %s depth=%s pin=%s versions=%s (snapshot %s)' % (
            r['path'], r['depth'], r['pin_class'], r['versions'], r['snapshot_commit']))
    py = [r for r in load('pypi.csv') if r['build_id'] == build_id]
    for r in py:
        print('  pypi:', r)
    if count_only:
        aux = [r for r in load('aux_lines.csv') if r['repo'] == repo and r['commit'] == commit]
        c = defaultdict(int)
        for r in aux:
            c[r['path']] += 1
        for p, n in sorted(c.items()):
            print('  aux %4d %s' % (n, p))
        return
    if show_lines:
        print('--- recipe lines (stage n op part | text), all stored stages')
        for r in load('recipe_lines.csv'):
            if r['repo'] == repo and r['commit'] == commit and r['path'] == path:
                print('%s %4s %-10s %s | %s' % (r['stage'], r['n'], r['op'], r['part'], r['text']))
    print('--- aux lines at this commit')
    for r in load('aux_lines.csv'):
        if r['repo'] == repo and r['commit'] == commit:
            if aux_grep and not aux_grep.search(r['path']):
                continue
            print('%s:%s | %s' % (r['path'], r['line'], r['text']))
    print('--- tree queries at this commit')
    for r in load('tree_paths.csv'):
        if r['repo'] == repo and r['commit'] == commit:
            print('%s %s -> %s' % (r['query'], r['path'], r['result']))


if __name__ == '__main__':
    main(sys.argv[1:])
