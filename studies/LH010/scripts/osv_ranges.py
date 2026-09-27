#!/usr/bin/env python3
"""LH010 step 3a: the frames to read and their advisories' affected ranges. Copied from LH009's osv_ranges.py and
changed as follows: the frames are LH010's 43 events (data/events.csv) and the second fix of each library in the
within-library sensitivity (brief.md: a qualifying fix of the other class at least 14 days from the event's, the
nearest in time), rather than LH008's events; the release lists come from data/releases.csv (select_libraries.py)
rather than a new read; a frame's advisory is its fix's earliest qualifying advisory.

Writes data/frame_defs.csv (one row per frame: library, kind, fixed release and upload, release before it,
advisory and time, class, strict class, whether the frame is reused from LH008 or LH009) and
data/event_advisory_ranges.csv (each frame advisory's OSV ECOSYSTEM ranges for each PyPI package it names)."""
import csv, json, os, sys
from packaging.version import Version, InvalidVersion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jget, write_csv, read_csv, ts, norm

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LH008_EV = {(e['library'], e['fixed_release']): e for e in csv.DictReader(open(os.path.join(ROOT, 'LH008', 'data', 'events.csv')))}


def V(s):
    try:
        return Version(s)
    except InvalidVersion:
        return None


C = read_csv('fix_classes.csv')
CL = {(c['library'], c['version']): c for c in C}
REL = {}
for r in read_csv('releases.csv'):
    REL.setdefault(r['library'], {})[r['version']] = r['uploaded']
Q = [a for a in read_csv('qualifying_advisories.csv') if a['qualifies'] == 'yes']


def before(lib, fx):
    R = REL[lib]
    stable = [v for v in R if V(v) and not V(v).is_prerelease and not V(v).is_devrelease]
    return max([v for v in stable if V(v) < V(fx) and ts(R[v]) < ts(R[fx])], key=V, default='')


frames = []
for e in read_csv('events.csv'):
    c = CL[(e['library'], e['fixed_release'])]
    old = LH008_EV.get((e['library'], e['fixed_release']))
    frames.append(dict(frame=f"{norm(e['library'])}:event", library=e['library'], rank=e['rank'], kind='event',
                       fixed_release=e['fixed_release'], fixed_uploaded=e['fixed_uploaded'],
                       release_before_fix=e['release_before_fix'], advisory=e['advisory'], severity=e['severity'],
                       advisory_published=e['advisory_published'], nvd_published_at=e['nvd_published_at'],
                       release_to_advisory_days=e['release_to_advisory_days'], cls=c['class'], strict_class=c['strict_class'],
                       reused=('LH008' if old['chosen'] == 'yes' else 'LH009') if old else 'no'))
for f in list(frames):
    others = [x for x in C if x['library'] == f['library'] and x['event'] == 'no' and x['class'] in ('announced', 'silent')
              and x['class'] != f['cls'] and abs((ts(x['uploaded']) - ts(f['fixed_uploaded'])).total_seconds()) >= 14 * 86400]
    if not others:
        continue
    o = min(others, key=lambda x: abs((ts(x['uploaded']) - ts(f['fixed_uploaded'])).total_seconds()))
    a = min([a for a in Q if a['project'] == f['library'] and a['fixed_release'] == o['version']], key=lambda a: ts(a['published']))
    frames.append(dict(frame=f"{norm(f['library'])}:second", library=f['library'], rank=f['rank'], kind='within-library second fix',
                       fixed_release=o['version'], fixed_uploaded=o['uploaded'], release_before_fix=before(f['library'], o['version']),
                       advisory=a['id'], severity=a['severity'], advisory_published=a['published'], nvd_published_at=a['nvd_published_at'],
                       release_to_advisory_days=o['release_to_advisory_days'], cls=o['class'], strict_class=o['strict_class'], reused='no'))
write_csv('frame_defs.csv', frames)
rows = []
for f in frames:
    j = jget('OSV API', 'OSV vuln ' + f['advisory'], 'https://api.osv.dev/v1/vulns/' + f['advisory'])
    for a in j['affected']:
        if a['package'].get('ecosystem') != 'PyPI':
            continue
        rows.append(dict(frame=f['frame'], library=f['library'], id=f['advisory'], published=j['published'], modified=j['modified'],
                         package=a['package']['name'],
                         ranges=json.dumps([r['events'] for r in a.get('ranges', []) if r.get('type') == 'ECOSYSTEM']),
                         aliases=' '.join(j.get('aliases', [])), summary=j.get('summary', '')[:160]))
write_csv('event_advisory_ranges.csv', rows)
for f in frames:
    rg = [r['ranges'] for r in rows if r['frame'] == f['frame'] and norm(r['package']) == norm(f['library'])]
    print(f['frame'], f['fixed_release'], 'before', f['release_before_fix'], f['cls'], f['reused'], rg[0][:90] if rg else 'NO RANGE')
