#!/usr/bin/env python3
"""LH008 step 1b: the full OSV records of the five advisories named in brief.md's first amendment, for
their affected ranges and aliases. Writes data/event_advisory_ranges.csv."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import jget, write_csv

IDS = ['GHSA-qccp-gfcp-xxvc', 'GHSA-mf9v-mfxr-j63j', 'GHSA-537c-gmf6-5ccf', 'GHSA-xgmm-8j9v-c9wx', 'GHSA-wqp7-x3pw-xc5r']
rows = []
for i in IDS:
    j = jget('OSV API', 'OSV vuln ' + i, 'https://api.osv.dev/v1/vulns/' + i)
    for a in j['affected']:
        rows.append(dict(id=i, published=j['published'], modified=j['modified'], package=a['package']['name'],
                         ranges=json.dumps([r['events'] for r in a.get('ranges', [])]), aliases=' '.join(j.get('aliases', [])),
                         summary=j.get('summary', '')[:160]))
write_csv('event_advisory_ranges.csv', rows)
