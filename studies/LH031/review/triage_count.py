#!/usr/bin/env python3
"""How many catalogue entries dated October 2026 carry forensicTriage "Yes", in the 27 October 06:34 UTC read.

Run from the repository root: python3 -I studies/LH031/review/triage_count.py > studies/LH031/review/triage_count.txt
"""
import json

d = json.load(open('studies/LH031/data/read-2026-10-27T0633Z/feed.raw'))
october = [e for e in d['vulnerabilities'] if e.get('dateAdded', '').startswith('2026-10')]
print('entries dated October 2026:', len(october))
print('of which forensicTriage Yes:', sum(1 for e in october if e.get('forensicTriage') == 'Yes'))
print('values seen:', sorted({e.get('forensicTriage') for e in october}))
