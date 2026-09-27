#!/usr/bin/env python3
"""LH009 step 2a: the OSV records of the twelve new events' advisories (LH008's events.csv, not chosen there), for
their affected ranges, and each library's release list from PyPI (first upload of each version). Writes
data/event_advisory_ranges.csv and data/releases_<library>.csv. Copied from LH008's osv_ranges.py and widened."""
import csv, json, os, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jget, write_csv, ts, iso

LH008 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'LH008', 'data')
EV = [e for e in csv.DictReader(open(os.path.join(LH008, 'events.csv'))) if e['chosen'] != 'yes']
rows = []
for e in EV:
    i = e['advisory']
    j = jget('OSV API', 'OSV vuln ' + i, 'https://api.osv.dev/v1/vulns/' + i)
    for a in j['affected']:
        if a['package'].get('ecosystem') != 'PyPI':
            continue
        rows.append(dict(library=e['library'], id=i, published=j['published'], modified=j['modified'], package=a['package']['name'],
                         ranges=json.dumps([r['events'] for r in a.get('ranges', []) if r.get('type') == 'ECOSYSTEM']),
                         aliases=' '.join(j.get('aliases', [])), summary=j.get('summary', '')[:160]))
    pj = jget('PyPI JSON API', 'PyPI ' + e['library'], 'https://pypi.org/pypi/' + urllib.parse.quote(e['library']) + '/json')
    rel = []
    for v, files in pj['releases'].items():
        if files:
            rel.append(dict(version=v, first_upload=iso(min(ts(f['upload_time_iso_8601']) for f in files)), yanked='yes' if all(f.get('yanked') for f in files) else 'no'))
    write_csv(f"releases_{e['library']}.csv", sorted(rel, key=lambda r: r['first_upload']))
write_csv('event_advisory_ranges.csv', rows)
for r in rows:
    print(r['library'], r['id'], r['package'], r['ranges'])
