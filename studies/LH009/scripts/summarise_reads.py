#!/usr/bin/env python3
"""LH009 (copied from LH008): data/read_summary.csv, requests and bytes by source from data/read_log.csv, with the first and
last read time. Clones' bytes are the size on disk after the study's blob fetches (du), logged at clone time
before any blob was fetched; the on-disk total at the end is added by hand in LH008.md."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv

agg = collections.OrderedDict()
for r in read_csv('read_log.csv'):
    a = agg.setdefault(r['source'], dict(source=r['source'], requests=0, ok=0, bytes=0, first=r['read_utc'], last=r['read_utc']))
    a['requests'] += 1
    a['ok'] += r['http_status'] in ('200',) or r['note'] in ('cloned', 'already cloned')
    a['bytes'] += int(r['bytes'] or 0)
    a['first'], a['last'] = min(a['first'], r['read_utc']), max(a['last'], r['read_utc'])
write_csv('read_summary.csv', list(agg.values()))
for a in agg.values():
    print(a)
