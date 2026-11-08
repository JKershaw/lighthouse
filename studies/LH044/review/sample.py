#!/usr/bin/env python3
"""Evidence review (R-0059): draw the reviewer's random sample of 30 of LH044's 161 services for
a manual reading of their retained baseline responses, and print, for each, the classes.csv entry
and the paths of the kept robots.txt and probe responses. The seed is fixed here, before any
sampled response was opened. Usage: python3 -I studies/LH044/review/sample.py
"""
import csv, hashlib, json, random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data' / 'read-2026-11-08T1920Z'
svc = {s['id']: s for s in json.load(open(D / 'services.json'))['services']}
cls = {r['id']: r for r in csv.DictReader(open(D / 'classes.csv'))}
ids = sorted(cls)
seed = int(hashlib.sha256(b'R-0059 LH044 reviewer sample, 8 November 2026').hexdigest(), 16)
pick = sorted(random.Random(seed).sample(ids, 30))
for i in pick:
    s, c = svc[i], cls[i]
    print(i, c['host'], c['surface'], 'class=%s' % c['class'], 'status=%s' % c['status'],
          'robots_n=%s' % s['robots_n'], 'probe_n=%s' % s['probe_n'], 'marker=%r' % s['marker'])
