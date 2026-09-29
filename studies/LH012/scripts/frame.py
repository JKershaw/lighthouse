#!/usr/bin/env python3
"""LH012: the frame, from metadata only (no download count), offline over data/ and LH011's retained
releases. Writes data/reference.csv (each project's reference release R and the versions at or above
it held during the read week), data/python_admission.csv (for each project and Python minor, whether
any version at or above R admits it by Requires-Python, and the highest version below R that does),
data/pairs.csv (each top-500 dependent's requirement on one of the 37, in the versions newest during
the read week or latest at read, classified by whether it can hold the project below R) and
data/releases_nov_mar.csv (the secondary question's releases, by LH011's rule).
New for LH012; the release rule is LH011's scripts/frame.py rule, rewritten here.
Usage: python3 frame.py"""
import csv, os
from packaging.version import Version
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.markers import Marker
from common import read_csv, write_csv, DATA

CUTOFF = '2026-08-21T23:59:59.999999'   # R: highest non-pre-release uploaded on or before this
WEEK_END = '2026-09-27T23:59:59.999999'
NM = ('2025-11-01T00:00:00', '2026-03-31T23:59:59.999999')
MINORS = ['2.7'] + ['3.%d' % i for i in range(5, 16)]
ROOT = os.path.dirname(os.path.dirname(DATA))
P37 = sorted({r['project'] for r in csv.DictReader(open(os.path.join(ROOT, 'LH011', 'data', 'releases.csv')))})


def usable(v):
    return v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and v['first_upload_utc']


def admits_minor(rp, minor):
    """Requires-Python admits some patch release of the minor (X.Y.0 to X.Y.30); a blank admits all."""
    if not rp.strip():
        return True
    try:
        s = SpecifierSet(rp)
    except InvalidSpecifier:
        return None
    return any(s.contains(Version(f'{minor}.{k}'), prereleases=True) for k in range(31))


def version_admits(row, minor):
    """A version admits a minor when any of its files' Requires-Python does (pip reads it per file)."""
    vals = [admits_minor(x, minor) for x in row['requires_python'].split(' | ')] if row['requires_python'] else [True]
    if any(v is True for v in vals):
        return True
    return None if any(v is None for v in vals) else False


vers = {}
for v in read_csv('versions.csv'):
    vers.setdefault(v['project'], []).append(v)

ref, adm = [], []
for p in P37:
    ok = [v for v in vers[p] if usable(v)]
    before = [v for v in ok if v['first_upload_utc'] <= CUTOFF]
    R = max(before, key=lambda v: Version(v['version']))
    rv = Version(R['version'])
    ge = sorted((v for v in ok if Version(v['version']) >= rv and v['first_upload_utc'] <= WEEK_END),
                key=lambda v: Version(v['version']))
    ref.append(dict(project=p, R=R['version'], R_first_upload_utc=R['first_upload_utc'],
                    R_requires_python=R['requires_python'], n_versions_ge_R_by_week_end=len(ge),
                    newest_by_week_end=ge[-1]['version'], versions_ge_R=' '.join(v['version'] for v in ge)))
    below = sorted((v for v in ok if Version(v['version']) < rv), key=lambda v: Version(v['version']))
    for m in MINORS:
        a = [version_admits(v, m) for v in ge]
        edge = [v for v in below if version_admits(v, m)]
        adm.append(dict(project=p, python_minor=m, R_admits=version_admits(R, m),
                        any_ge_R_admits=True if any(x is True for x in a) else (None if any(x is None for x in a) else False),
                        edge_below_R=edge[-1]['version'] if edge else ''))
write_csv('reference.csv', ref)
write_csv('python_admission.csv', adm)

# Pairs: each non-self requirement on one of the 37, in the versions read (latest at read, and every
# version newest during the read week).
refd = {r['project']: r for r in ref}
geR = {r['project']: [Version(x) for x in r['versions_ge_R'].split()] for r in ref}
pairs = []
for r in read_csv('requirements.csv'):
    if r['one_of_37'] != 'True' or r['dependent'] == r['name']:
        continue
    D = r['name']
    s = SpecifierSet(r['specifier'])
    ops = {x.operator for x in s}
    upper = bool(ops & {'<', '<=', '==', '===', '~='})
    admits_ge = any(s.contains(v, prereleases=True) for v in geR[D])
    m = r['marker']
    pairs.append(dict(dependent=r['dependent'], dependent_version=r['dependent_version'], which=r['which'], project=D,
                      specifier=r['specifier'], marker=m, extra_only=r['extra_only'],
                      marker_has_python='python_version' in m or 'python_full_version' in m,
                      marker_has_platform=any(k in m for k in ('sys_platform', 'platform_', 'os_name', 'implementation')),
                      has_upper_bound=upper, admits_a_version_ge_R=admits_ge, R=refd[D]['R']))
write_csv('pairs.csv', pairs)

# Secondary question: releases of November 2025 to March 2026 by LH011's rule (not a pre-release,
# first uploaded in the window, higher than every earlier-uploaded non-pre-release version).
nm = []
for p in P37:
    seq = sorted((v for v in vers[p] if v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['first_upload_utc']),
                 key=lambda v: v['first_upload_utc'])
    top = None
    for v in seq:
        x = Version(v['version'])
        if top is None or x > top:
            if NM[0] <= v['first_upload_utc'] <= NM[1]:
                nm.append(dict(project=p, version=v['version'], first_upload_utc=v['first_upload_utc'],
                               day0=v['first_upload_utc'][:10], replaced_version=str(top), yanked_all_files=v['all_yanked']))
            top = x
write_csv('releases_nov_mar.csv', nm)
print('R cut-off', CUTOFF, '; releases Nov-Mar', len(nm), 'in', len({r['project'] for r in nm}), 'projects')
