#!/usr/bin/env python3
"""LH011: derive the releases, the CI subsample and the project order from data/projects.csv and
data/pypi_versions.csv, offline. No network.

Rules, from the brief: a qualifying release is a version that is not a pre-release or development
release (PEP 440), whose first file was uploaded between 2026-04-01T00:00:00Z and
2026-08-31T23:59:59Z, and which at that moment was higher than every earlier-uploaded non-pre-release
version. Its replaced release is the newest non-pre-release version immediately before its upload.
Kind is the first differing component of the release tuple against the replaced release (0 major,
1 minor, 2 or later patch; a difference only in epoch is 'epoch', only in post-release 'post').
'Released again within seven days' means another version became the newest within 168 hours of this
one's first upload (any date, so August releases see September). The CI subsample is the first
qualifying release uploaded in each calendar month, April to August. Projects are ordered by the
SHA-256 of their names. Versions that do not parse as PEP 440 take no part in any comparison.

New for LH011 (LH005 had one release and needed no frame).
Usage: python3 frame.py   (writes data/releases.csv and data/project_order.csv)"""
import hashlib
from packaging.version import Version
from common import read_csv, write_csv

START, END = '2026-04-01T00:00:00', '2026-08-31T23:59:59'
projects = [r['project'] for r in read_csv('projects.csv') if r['status'] == 'selected']
versions = read_csv('pypi_versions.csv')


def kind(new, old):
    if old is None:
        return 'first'
    if new.epoch != old.epoch:
        return 'epoch'
    a, b = list(new.release), list(old.release)
    n = max(len(a), len(b))
    a += [0] * (n - len(a)); b += [0] * (n - len(b))
    for i in range(n):
        if a[i] != b[i]:
            return ['major', 'minor'][i] if i < 2 else 'patch'
    return 'post'


out, order = [], []
for p in projects:
    vs = [r for r in versions if r['project'] == p and r['parse'] == 'ok' and r['is_prerelease'] == 'False']
    vs.sort(key=lambda r: (r['first_upload_utc'], Version(r['version'])))
    newest, chain = None, []   # chain: versions that became the newest when uploaded, in upload order
    for r in vs:
        v = Version(r['version'])
        if newest is None or v > Version(newest['version']):
            chain.append((r, newest))
            newest = r
    seen_month = set()
    for i, (r, prev) in enumerate(chain):
        t = r['first_upload_utc'][:19]
        if not (START <= t <= END):
            continue
        nxt = chain[i + 1][0] if i + 1 < len(chain) else None
        month = t[:7]
        ci = month not in seen_month
        seen_month.add(month)
        # hours between this upload and the next newest upload
        from datetime import datetime
        f = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
        gap_h = round((f(nxt['first_upload_utc']) - f(r['first_upload_utc'])).total_seconds() / 3600, 2) if nxt else ''
        day0 = f(r['first_upload_utc'])
        hours_left = round(24 - (day0.hour + day0.minute / 60 + day0.second / 3600), 2)
        out.append(dict(project=p, version=r['version'], first_upload_utc=r['first_upload_utc'], day0=t[:10],
                        hours_left_in_day0=hours_left, replaced_version=prev['version'] if prev else '',
                        replaced_first_upload_utc=prev['first_upload_utc'] if prev else '',
                        kind=kind(Version(r['version']), Version(prev['version']) if prev else None),
                        next_newest_version=nxt['version'] if nxt else '',
                        hours_to_next_newest=gap_h,
                        released_again_within_7d=(gap_h != '' and gap_h <= 168),
                        yanked=r['any_yanked'], ci_subsample=ci))
    order.append(dict(sha256_order=0, project=p, sha256=hashlib.sha256(p.encode()).hexdigest(),
                      n_releases=sum(1 for o in out if o['project'] == p),
                      n_ci_subsample=sum(1 for o in out if o['project'] == p and o['ci_subsample'])))
order.sort(key=lambda o: o['sha256'])
for i, o in enumerate(order, 1):
    o['sha256_order'] = i
write_csv('project_order.csv', order)
write_csv('releases.csv', out)
print(len(out), 'releases;', sum(o['ci_subsample'] for o in out), 'in the CI subsample;',
      sum(1 for o in order if o['n_releases']), 'projects with at least one release')
