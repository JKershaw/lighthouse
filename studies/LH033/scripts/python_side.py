#!/usr/bin/env python3
"""LH033's Python comparators, from LH011's and LH008's retained tables only (brief.md, Measures).

Writes data/python_side.json and prints it. No Python download or repository is read afresh.
"""
from pathlib import Path
from statistics import median
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
STUDIES = ROOT.parent
DAYS = (1, 2, 7, 14, 30)
FIXES = {('urllib3', '2.7.0'), ('cryptography', '48.0.1'), ('pyjwt', '2.13.0'), ('starlette', '1.1.0')}

share = {}
for r in csv.DictReader(open(STUDIES / 'LH011/data/analysis/release_days.csv')):
    if r['status'] == 'known' and int(r['day']) in DAYS:
        share[(r['project'], r['version'], int(r['day']))] = float(r['share_at_or_newer'])

out = {'four_security_fixes': {}, 'median_of_project_medians_37': {}}
for project, version in sorted(FIXES):
    out['four_security_fixes'][f'{project} {version}'] = {d: share.get((project, version, d)) for d in DAYS}
releases = {(p, v) for p, v, _ in share}
projects = sorted({p for p, _ in releases})
for d in DAYS:
    per_project = [median(vals) for p in projects
                   if (vals := [share[(p, v, d)] for q, v in releases if q == p and (p, v, d) in share])]
    out['median_of_project_medians_37'][d] = {'median': round(median(per_project), 4), 'projects': len(per_project)}

moved = {7: 0, 30: 0}
pairs = 0
for r in csv.DictReader(open(STUDIES / 'LH008/data/lags.csv')):
    if not r['frame'].endswith(':fix'):
        continue
    pairs += 1
    if r['outcome'] == 'moved' and r['lag_release_days']:
        for d in moved:
            moved[d] += float(r['lag_release_days']) <= d
out['lh008_fix_pairs_moved_within'] = {'pairs': pairs, **{f'{d} days': n for d, n in moved.items()},
                                        'clock': 'committer time after release, as LH008 data/lags.csv'}
(ROOT / 'data' / 'python_side.json').write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1))
