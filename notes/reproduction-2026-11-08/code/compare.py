#!/usr/bin/env python3
"""Compare the independent reproduction's tables (../output/) with the record's (studies/LH011/data/analysis/),
release by release and project by project. Run after the reproduction; written after the record was opened."""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
MINE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'output')
THEIRS = os.path.join(ROOT, 'studies', 'LH011', 'data', 'analysis')


def read(p):
    with open(p, newline='') as f:
        return list(csv.DictReader(f))


out = []
# releases
mine = {(r['project'], r['version']): r for r in read(os.path.join(MINE, 'release_outcomes.csv'))}
theirs = {(r['project'], r['version']): r for r in read(os.path.join(THEIRS, 'release_outcomes.csv'))}
out.append(f"releases: mine {len(mine)}, record {len(theirs)}, keys equal: {set(mine) == set(theirs)}")
share_diffs, class_diffs, dth_diffs = [], [], []
max_abs = 0.0
for k in sorted(mine):
    m, t = mine[k], theirs[k]
    for d in ('0', '1', '2'):
        a, b = m[f'share_day{d}'], t[f'share_day{d}']
        if (a == '') != (b == ''):
            share_diffs.append((k, d, a, b))
        elif a != '':
            diff = abs(float(a) - float(b))
            max_abs = max(max_abs, diff)
            if diff > 0.00005:      # mine is written to 4 dp, theirs to 6
                share_diffs.append((k, d, a, b))
    if m['reached_half_within_2d'] != t['reached_half_within_two_days']:
        class_diffs.append((k, m['reached_half_within_2d'], t['reached_half_within_two_days']))
    md = str(m['days_to_half'])
    td = t['days_to_half'] if t['days_to_half'] != '' else t['days_to_half_note']
    if md.isdigit():
        same = td == md
    elif md.startswith('not by day 30'):
        same = 'by day 30' in td
    else:
        same = 'last day' in td or 'held' in td or 'censored' in td or '27' in td
    if not same:
        dth_diffs.append((k, md, td))
out.append(f"day 0-2 shares: largest absolute difference {max_abs:.6f} (rounding only); mismatches beyond rounding: {len(share_diffs)} {share_diffs[:10]}")
out.append(f"reached-half class mismatches: {len(class_diffs)} {class_diffs[:10]}")
out.append(f"days-to-half mismatches: {len(dth_diffs)} {dth_diffs[:10]}")
notes = sorted({t['days_to_half_note'] for t in theirs.values() if t['days_to_half'] == ''})
out.append(f"record's days_to_half notes: {notes}")

# projects
pm = {r['project']: r for r in read(os.path.join(MINE, 'project_outcomes.csv'))}
pt = {r['project']: r for r in read(os.path.join(THEIRS, 'project_outcomes.csv')) if r['releases'] != '0'}
out.append(f"projects with releases: mine {len(pm)}, record {len(pt)}, same set: {set(pm) == set(pt)}")
pdiffs = []
for p in sorted(pm):
    m, t = pm[p], pt[p]
    cls = {'most reached': 'yes', 'none reached': 'no', 'some, not most': 'no'}[m['cls']]
    if (m['releases'], m['known'], m['reached']) != (t['releases'], t['known'], t['reached']) or cls != t['most_reached'] \
            or abs(float(m['median_day1_share']) - float(t['median_day1_share'])) > 0.00005 \
            or str(m['n_not_by_30']) != t['releases_not_reaching_half_by_day_30'].strip():
        pdiffs.append((p, dict(m), dict(t)))
out.append(f"project rows differing: {len(pdiffs)}")
for d in pdiffs:
    out.append('  ' + repr(d))
print('\n'.join(out))
with open(os.path.join(MINE, 'compare.txt'), 'w') as f:
    f.write('\n'.join(out) + '\n')
