#!/usr/bin/env python3
"""LH013: the frame, from metadata only (no download count), offline. Reads data/versions.csv (PyPI as read
on 2 November 2026) and LH012's data/reference.csv (R0) and data/versions.csv (PyPI as LH012 read it on
29 September 2026). Writes, under data/frame/ (or $LH013_OUT/frame):
  reference.csv          per project: R0 (LH012's, held fixed); R1 and R2, each week's own reference release
                         by LH012's rule (highest non-pre-release, not wholly yanked, first uploaded on or before
                         28 August 2026 for W1 and 4 September 2026 for W2); the versions at or above R0
                         uploaded since LH012's read
  classes.csv            per project and version listed by PyPI: its class at R0, R1 and R2 (older, at_or_newer,
                         other); a version ClickPy holds that PyPI does not list is "other" (brief, measure 1)
  python_admission.csv   per project, reference (R0, R1, R2), week and Python minor: whether a usable version at or
                         above the reference, uploaded by the end of each day of the week, admits the minor; whether
                         that changed within the week; and the edge, the highest usable version below the reference
                         that admits the minor (brief, measure 2: admission recomputed for each day)
  metadata_changes.csv   versions uploaded before 29 September 2026 whose yanking or Requires-Python differs from
                         LH012's read
Rules as LH012's frame.py and analyse.py: usable = parses, not a pre- or dev-release, not wholly yanked, has an
upload time; a version admits a minor when any of its files' Requires-Python admits some X.Y.0 to X.Y.30.
Usage: python3 frame.py"""
import csv, os, datetime as dt
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
LH012 = os.path.join(os.path.dirname(STUDY), 'LH012', 'data')
OUT = os.path.join(os.environ.get('LH013_OUT', DATA), 'frame')
os.makedirs(OUT, exist_ok=True)
MINORS = ['2.7'] + ['3.%d' % i for i in range(4, 16)]
WEEKS = {'W1': '2026-09-28', 'W2': '2026-10-05'}
CUT = {'W1': '2026-08-28T23:59:59.999999', 'W2': '2026-09-04T23:59:59.999999'}
LH012_READ = '2026-09-29T06:19:00'


def rd(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def wr(name, rows, fields):
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})


def V(s):
    try:
        return Version(s)
    except InvalidVersion:
        return None


def usable(v):
    return v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and v['first_upload_utc']


def admits_minor(rp, m):
    if not rp.strip():
        return True
    try:
        s = SpecifierSet(rp)
    except InvalidSpecifier:
        return None
    return any(s.contains(Version(f'{m}.{k}'), prereleases=True) for k in range(31))


def version_admits(row, m):
    vals = [admits_minor(x, m) for x in row['requires_python'].split(' | ')] if row['requires_python'] else [True]
    if any(v is True for v in vals):
        return True
    return None if any(v is None for v in vals) else False


VERS = {}
for v in rd(os.path.join(DATA, 'versions.csv')):
    VERS.setdefault(v['project'], {})[v['version']] = v
OLD = {}
for v in rd(os.path.join(LH012, 'versions.csv')):
    OLD.setdefault(v['project'], {})[v['version']] = v
REF0 = {r['project']: r for r in rd(os.path.join(LH012, 'reference.csv'))}
P37 = sorted(REF0)


def cls(v, R):
    """older, at_or_newer or other, for a version PyPI lists, against reference R (LH012's vclass, with its
    'unlisted' and unparsable versions in 'other', as the brief's measure 1 says)."""
    x = V(v['version'])
    if v['parse'] != 'ok' or x is None:
        return 'other'
    if x < R:
        return 'older'
    return 'other' if (x.is_prerelease or x.is_devrelease) else 'at_or_newer'


ref_rows, cls_rows, adm_rows, chg = [], [], [], []
for p in P37:
    vs = VERS[p]
    R0 = Version(REF0[p]['R'])
    assert REF0[p]['R'] in vs and usable(vs[REF0[p]['R']]), p
    Rw = {}
    for w, cut in CUT.items():
        ok = [v for v in vs.values() if usable(v) and v['first_upload_utc'] <= cut]
        Rw[w] = max(ok, key=lambda v: Version(v['version']))['version']
    new_ge = sorted((k for k, v in vs.items() if usable(v) and Version(k) >= R0 and v['first_upload_utc'] > LH012_READ), key=Version)
    ref_rows.append(dict(project=p, R0=str(REF0[p]['R']), R1=Rw['W1'], R2=Rw['W2'],
                         R0_differs_from_R1=str(Version(Rw['W1']) != R0), R0_differs_from_R2=str(Version(Rw['W2']) != R0),
                         n_listed_versions=len(vs), usable_ge_R0_uploaded_after_lh012_read=' '.join(new_ge)))
    for k, v in sorted(vs.items()):
        cls_rows.append(dict(project=p, version=k, R0=cls(v, R0), R1=cls(v, Version(Rw['W1'])), R2=cls(v, Version(Rw['W2']))))
    for refname, R in (('R0', R0), ('R1', Version(Rw['W1'])), ('R2', Version(Rw['W2']))):
        below = sorted((Version(k) for k, v in vs.items() if usable(v) and Version(k) < R), reverse=True)
        for w, first in WEEKS.items():
            if refname == 'R1' and w != 'W1' or refname == 'R2' and w != 'W2':
                continue
            days = [str(dt.date.fromisoformat(first) + dt.timedelta(days=i)) for i in range(7)]
            for m in MINORS:
                per_day = []
                for d in days:
                    end = d + 'T23:59:59.999999'
                    a = [version_admits(v, m) for k, v in vs.items() if usable(v) and Version(k) >= R and v['first_upload_utc'] <= end]
                    per_day.append(True if any(x is True for x in a) else (None if any(x is None for x in a) else False))
                edge = next((str(x) for x in below if version_admits(vs[str(x)] if str(x) in vs else next(v for k, v in vs.items() if Version(k) == x), m) is True), '')
                adm_rows.append(dict(project=p, reference=refname, R=str(R), week=w, python_minor=m,
                                     admitted_by_week_end=per_day[-1], admitted_each_day=' '.join(str(x) for x in per_day),
                                     changes_within_week=str(len(set(per_day)) > 1), edge_below_R=edge))
    for k, v in vs.items():
        o = OLD.get(p, {}).get(k)
        if o is None:
            if v['first_upload_utc'] and v['first_upload_utc'] < LH012_READ:
                chg.append(dict(project=p, version=k, what='listed now, not in LH012\'s read', lh012='', now=v['first_upload_utc']))
            continue
        for f in ('all_yanked', 'any_yanked', 'requires_python'):
            if o[f] != v[f]:
                chg.append(dict(project=p, version=k, what=f, lh012=o[f], now=v[f]))
    for k in OLD.get(p, {}):
        if k not in vs:
            chg.append(dict(project=p, version=k, what='in LH012\'s read, not listed now', lh012='listed', now=''))
wr('reference.csv', ref_rows, list(ref_rows[0].keys()))
wr('classes.csv', cls_rows, ['project', 'version', 'R0', 'R1', 'R2'])
wr('python_admission.csv', adm_rows, list(adm_rows[0].keys()))
wr('metadata_changes.csv', chg, ['project', 'version', 'what', 'lh012', 'now'])
ch = [r for r in adm_rows if r['changes_within_week'] == 'True']
print('admission changing within a week:', len(ch), [(r['project'], r['reference'], r['week'], r['python_minor'], r['admitted_each_day']) for r in ch])
print('R1 != R0:', sum(r['R0_differs_from_R1'] == 'True' for r in ref_rows), '; R2 != R0:', sum(r['R0_differs_from_R2'] == 'True' for r in ref_rows))
print('metadata changes since LH012\'s read:', len(chg))
