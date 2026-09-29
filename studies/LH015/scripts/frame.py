"""LH015 frame: the distinct repository and event pairs of LH008's, LH009's and LH010's retained tables.

Offline. Reads only studies/LH008, LH009 and LH010 data/ (lags.csv, moves.csv, snapshot_files.csv, screen.csv,
and LH010's reused_moves.csv) and writes data/frame.csv, data/frame_files.csv and data/frame_counts.csv here.
No network, no clone, no recipe. The rule is brief.md's (Population and unit).

1. Every row of the three lags.csv tables is mapped to one moves.csv row: LH008's by (frame, repo); LH009's and
   LH010's reused rows (source LH008 or LH009) to the source study's '<library>:fix' frame and repo; LH010's own
   rows by (frame, repo). A row that does not map stops the script.
2. A pair is (repository lower-cased, library, threshold release), the threshold being the release whose upload
   time set the snapshot. Rows with the same key are one pair; the earliest study's moves row (LH008, then LH009,
   then LH010) gives its frame, package, snapshot commit and pinned files; the others are listed in also_in.
   A duplicate whose snapshot commit differs stops the script.
3. The pair's timed files are its rows in that study's snapshot_files.csv, joined on (frame, package). Every one
   is checked to hold a version below the pair's fix (LH010's pair_fix where given, else the threshold), by
   PEP 440 order; the check is reported, not used to drop anything.
4. Pin class: 'lockfile' if every timed file is a lockfile, 'exact pin' if every one is an exact pin, else 'both'.
"""
import csv
import hashlib
import os
import sys
from collections import Counter, defaultdict

from packaging.version import InvalidVersion, Version

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
STUDIES = os.path.dirname(STUDY)
OUT = os.environ.get('LH015_OUT', os.path.join(STUDY, 'data'))
ORDER = ['LH008', 'LH009', 'LH010']


def rd(study, name):
    with open(os.path.join(STUDIES, study, 'data', name), newline='') as f:
        return list(csv.DictReader(f))


def wr(name, rows, fields):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})


def V(s):
    try:
        return Version(s)
    except (InvalidVersion, TypeError):
        return None


def main():
    moves = {s: rd(s, 'moves.csv') for s in ORDER}
    lags = {s: rd(s, 'lags.csv') for s in ORDER}
    idx = {(s, r['frame'], r['repo']): r for s in ORDER for r in moves[s]}
    screen = {(s, r['frame'], r['package']): r for s in ORDER for r in rd(s, 'screen.csv')}
    sfiles = defaultdict(list)
    for s in ORDER:
        for x in rd(s, 'snapshot_files.csv'):
            sfiles[(s, x['frame'], x['package'])].append(x)

    # 1. map every lags row to a moves row
    mapped = []  # (lags study, moves key, lags row)
    for r in lags['LH008']:
        mapped.append(('LH008', ('LH008', r['frame'], r['repo']), r))
    for r in lags['LH009']:
        mapped.append(('LH009', (r['source'], r['library'] + ':fix', r['repo']), r))
    for r in lags['LH010']:
        k = ('LH010', r['frame'], r['repo']) if r['source'] == 'LH010' else (r['source'], r['library'] + ':fix', r['repo'])
        mapped.append(('LH010', k, r))
    bad = [(s, k) for s, k, _ in mapped if k not in idx]
    if bad:
        sys.exit(f'unmapped lags rows: {bad[:5]}')
    # LH010's reused_moves.csv names its rows with LH010's frames; match them to LH008's and LH009's by pair key
    earlier = {(r['repo'].lower(), r['library'], r['threshold']): r for s in ('LH008', 'LH009') for r in moves[s]}
    for r in rd('LH010', 'reused_moves.csv'):
        src = earlier.get((r['repo'].lower(), r['library'], r['threshold']))
        if src is None or src['snapshot_commit'] != r['snapshot_commit']:
            sys.exit(f"LH010 reused row differs from its source: {r['frame']} {r['repo']}")

    # 2. distinct pairs
    by_key = defaultdict(list)
    for lag_study, k, lagrow in mapped:
        m = idx[k]
        key = (m['repo'].lower(), m['library'], m['threshold'])
        by_key[key].append((k, lag_study, lagrow))
    pairs, files_out = [], []
    for key, rows in by_key.items():
        ks = sorted({k for k, _, _ in rows}, key=lambda k: ORDER.index(k[0]))
        k0 = ks[0]
        m = idx[k0]
        snaps = {idx[k]['snapshot_commit'] for k in ks}
        if len(snaps) > 1:
            sys.exit(f'duplicate pair with differing snapshots: {key} {snaps}')
        sc = screen.get(k0) or screen.get((k0[0], k0[1], m['package'])) or {}
        fix = m.get('pair_fix') or m['threshold']
        tf = sfiles[(k0[0], k0[1], m['package'])]
        if not tf:
            sys.exit(f'pair without pinned files: {key}')
        below = all(any(V(v) and V(fix) and V(v) < V(fix) for v in x['versions'].split(',')) for x in tf)
        classes = {x['pin_class'] for x in tf}
        pin = 'lockfile' if classes == {'lockfile'} else 'exact pin' if classes == {'exact pin'} else 'both'
        lag_first = sorted(rows, key=lambda t: ORDER.index(t[1]))[0][2]
        pairs.append(dict(
            repo=m['repo'], library=m['library'], threshold=m['threshold'], pair_fix=fix,
            event_kind=m['kind'], release_time=m['release_time'], advisory_time=m.get('advisory_time', ''),
            source_study=k0[0], frame=k0[1], package=m['package'], shared_by=lag_first.get('shared_by', ''),
            also_in=' '.join(f'{k[0]}:{k[1]}' for k in ks[1:]),
            lags_tables=' '.join(sorted({t[1] for t in rows}, key=ORDER.index)),
            default_branch=m['default_branch'], snapshot_commit=m['snapshot_commit'],
            snapshot_time=sc.get('snapshot_time', ''), head_commit_27sep=m.get('head_commit', ''),
            n_timed=len(tf), pin_class=pin, timed_all_below_fix='yes' if below else 'no',
            timed_files='; '.join(f"{x['path']} [{x['pin_class']}] {x['versions']}" for x in sorted(tf, key=lambda x: x['path'])),
            outcome=m['outcome'], lag_release_days=lag_first.get('lag_release_days', ''),
        ))
    pairs.sort(key=lambda p: (p['repo'].lower(), p['release_time'], p['library']))
    for i, p in enumerate(pairs, 1):
        p['pair_id'] = f'P{i:03d}'
        k0 = (p['source_study'], p['frame'], p['repo'])
        for x in sorted(sfiles[(p['source_study'], p['frame'], p['package'])], key=lambda x: x['path']):
            files_out.append(dict(pair_id=p['pair_id'], repo=p['repo'], snapshot_commit=p['snapshot_commit'],
                                  path=x['path'], depth=x['path'].count('/'), pin_class=x['pin_class'], versions=x['versions']))
    fields = ['pair_id', 'repo', 'library', 'threshold', 'pair_fix', 'event_kind', 'release_time', 'advisory_time',
              'source_study', 'frame', 'package', 'shared_by', 'also_in', 'lags_tables', 'default_branch',
              'snapshot_commit', 'snapshot_time', 'head_commit_27sep', 'n_timed', 'pin_class', 'timed_all_below_fix',
              'timed_files', 'outcome', 'lag_release_days']
    wr('frame.csv', pairs, fields)
    wr('frame_files.csv', files_out, ['pair_id', 'repo', 'snapshot_commit', 'path', 'depth', 'pin_class', 'versions'])

    repos = Counter(p['repo'].lower() for p in pairs)
    events = {(p['library'], p['threshold']) for p in pairs}
    c = [('lags rows, LH008 / LH009 / LH010', ' / '.join(str(len(lags[s])) for s in ORDER)),
         ('moves rows, LH008 / LH009 / LH010', ' / '.join(str(len(moves[s])) for s in ORDER)),
         ('distinct pairs', len(pairs)),
         ('pairs read by two studies (same snapshot)', sum(1 for p in pairs if p['also_in'])),
         ('distinct repositories', len(repos)),
         ('distinct events (library, threshold)', len(events)),
         ('repositories by number of pairs', ' '.join(f'{n}:{k}' for n, k in sorted(Counter(repos.values()).items()))),
         ('pin class: lockfile / exact pin / both', ' / '.join(str(sum(1 for p in pairs if p['pin_class'] == c)) for c in ('lockfile', 'exact pin', 'both'))),
         ('pairs whose every timed file holds a version below the fix', sum(1 for p in pairs if p['timed_all_below_fix'] == 'yes')),
         ('timed files', len(files_out)),
         ('timed files by depth 0 / 1 / 2 / 3', ' / '.join(str(sum(1 for x in files_out if x['depth'] == d)) for d in range(4))),
         ('pairs with every timed file at the root', sum(1 for p in pairs if all('/' not in f.split(' [')[0] for f in p['timed_files'].split('; ')))),
         ('repository hosts', ' '.join(f'{h}:{n}' for h, n in sorted(Counter(r.split('/')[0] for r in repos).items()))),
         ('sha256 of frame.csv', hashlib.sha256(open(os.path.join(OUT, 'frame.csv'), 'rb').read()).hexdigest())]
    wr('frame_counts.csv', [dict(measure=a, value=b) for a, b in c], ['measure', 'value'])
    for a, b in c:
        print(f'{a}: {b}')


if __name__ == '__main__':
    main()
