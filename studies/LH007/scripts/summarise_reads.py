#!/usr/bin/env python3
"""LH007: counts from data/read_log.csv and data/layer_reads.csv for the record. Writes data/read_summary.csv."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv
log = read_csv('read_log.csv')
lr = read_csv('layer_reads.csv')
out = [dict(measure='requests logged', value=len(log)),
       dict(measure='first and last logged read (UTC)', value=f"{min(r['read_utc'] for r in log)} to {max(r['read_utc'] for r in log)}"),
       dict(measure='Docker Hub counted manifest GETs (200)', value=sum(1 for r in log if r['label'].startswith('GET manifest docker.io') and r['http_status'] == '200')),
       dict(measure='Docker Hub rate-limit headers recorded', value=' | '.join(f"{r['read_utc']} {r['note']}" for r in log if r['label'].startswith('ratelimit headers'))),
       dict(measure='layer streams', value=len(lr)),
       dict(measure='compressed layer bytes read', value=sum(int(r['bytes_read'] or 0) for r in lr))]
by = collections.Counter()
for r in lr:
    by[r['image'].split('/')[0]] += int(r['bytes_read'] or 0)
out.append(dict(measure='layer streams by registry', value=' '.join(f"{k}:{v}" for k, v in sorted(collections.Counter(r['image'].split('/')[0] for r in lr).items()))))
for k, v in sorted(by.items()):
    out.append(dict(measure=f'layer bytes read, {k}', value=v))
st = collections.Counter((r['source'], r['http_status']) for r in log)
for (s, c), n in sorted(st.items()):
    out.append(dict(measure=f'requests: {s}, status {c or ("not applicable (git clone)" if s.startswith("git") else "none (connection error, retried)")}', value=n))
out = [o for o in out if o['value'] != '']
write_csv('read_summary.csv', out)
for o in out:
    print(o['measure'], '=', o['value'])
