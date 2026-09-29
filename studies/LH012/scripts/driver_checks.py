#!/usr/bin/env python3
"""LH012: a check made by the driving session while writing the piece, after every count was read
(post hoc, one description). "Older" in the record means a version numbered below the reference release
R, not one uploaded before it. This prints, per project, the share of its older downloads over the read
week that are of versions first uploaded after R was, such as a patch to an earlier line, so that the
piece does not call every older download "a month out of date"; and, a second description, where
boto3's Python 3.9 downloads sit against the last boto3 that admits 3.9. Offline, from data/week/versions/,
data/versions.csv and data/reference.csv. Usage: python3 driver_checks.py > data/driver/driver_checks.txt"""
import csv, os
from packaging.version import Version, InvalidVersion
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(HERE, 'data')
up = {(r['project'], r['version']): r['first_upload_utc'] for r in csv.DictReader(open(os.path.join(D, 'versions.csv')))}
ref = {r['project']: r for r in csv.DictReader(open(os.path.join(D, 'reference.csv')))}
print('project, older downloads, of which versions uploaded after R (share), largest such version')
rows = []
for p in sorted(ref):
    R, Rt = Version(ref[p]['R']), ref[p]['R_first_upload_utc']
    older = after = 0
    by = {}
    for r in csv.DictReader(open(os.path.join(D, 'week', 'versions', p + '.csv'))):
        v, n = r['version'], int(r['n'])
        if (p, v) not in up:
            continue  # unlisted: "other" in the record
        try:
            V = Version(v)
        except InvalidVersion:
            continue
        if V.is_prerelease or V.is_devrelease or V >= R:
            continue
        older += n
        if up[(p, v)] > Rt:
            after += n
            by[v] = by.get(v, 0) + n
    top = max(by.items(), key=lambda x: x[1]) if by else ('', 0)
    rows.append((p, older, after))
    print(f'{p}, {older}, {after} ({after / older if older else 0:.3f}), {top[0]} {top[1]}')
a = [r for r in rows if r[1] and r[2] / r[1] > 0.01]
print(f'projects with more than 1 per cent of older downloads on versions uploaded after R: {len(a)}: ' +
      ', '.join(f'{p} {x / o:.3f}' for p, o, x in a))

# Second description, same session, also post hoc: where boto3's Python 3.9 downloads over the read week
# sit against 1.42.97, the highest boto3 whose Requires-Python admits 3.9 (data/python_admission.csv).
from packaging.version import Version as _V
edge, below, at, above = _V('1.42.97'), 0, 0, 0
for r in csv.DictReader(open(os.path.join(D, 'week', 'python', 'boto3.csv'))):
    if r['python_minor'] != '3.9':
        continue
    try:
        v = _V(r['version'])
    except InvalidVersion:
        continue
    n = int(r['n'])
    below, at, above = below + n * (v < edge), at + n * (v == edge), above + n * (v > edge)
t = below + at + above
print(f'boto3, Python 3.9, 21 to 27 September 2026: {t} downloads; below 1.42.97 {below} ({below / t:.3f}), '
      f'at it {at} ({at / t:.3f}), above it {above} ({above / t:.4f})')
