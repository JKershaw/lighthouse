#!/usr/bin/env python3
"""Evidence review (R-0059): for each service whose kept robots.txt was parsed at the baseline,
show which rule decided the probe for the token Lighthouse-research, which group applied, and
whether the kept robots.txt was truncated at the 64 KiB cap. Offline: reads only retained files.
Usage: python3 -I studies/LH044/review/robots_check.py
"""
import csv, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from classify import parse_robots, _rules_for, _pat_match, _norm_path, robots_allowed
D = ROOT / 'data' / 'read-2026-11-08T1920Z'
log = {r['n']: r for r in csv.DictReader(open(D / 'readlog.csv'))}
svc = json.load(open(D / 'services.json'))['services']
for s in svc:
    if s['robots_state'] != 'parsed':
        continue
    n = str(s['robots_n'])
    body = (D / ('%04d.b' % int(n))).read_bytes().decode('utf-8', 'replace')
    g = parse_robots(body)
    tok = 'lighthouse-research'
    own_group = any(tok in a for a, _ in g)
    path = _norm_path(s['url'])
    best = None
    for allow, pat in _rules_for(g, 'Lighthouse-research'):
        if pat and _pat_match(pat, path):
            if best is None or len(pat) > len(best[1]) or (len(pat) == len(best[1]) and allow):
                best = (allow, pat)
    ok = robots_allowed(g, 'Lighthouse-research', s['url'])
    trunc = log[n]['truncated']
    last = body.rstrip('\n').rsplit('\n', 1)[-1] if trunc == 'True' else ''
    print('%s %-32s allowed=%-5s group=%-9s truncated=%-5s rule=%s%s' % (
        s['id'], s['host'], ok, 'own' if own_group else '*', trunc,
        ('Allow ' if best and best[0] else 'Disallow ' if best else '(none)') + (best[1] if best else ''),
        ('   last kept line: %r' % last[:60]) if last else ''))
