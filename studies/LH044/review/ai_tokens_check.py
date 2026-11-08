#!/usr/bin/env python3
"""Evidence review (R-0059): cross-check robots.csv's named-AI-crawler columns against the raw
user-agent lines of each kept, parsed robots.txt. For each file, lists the AI tokens the study
counts as disallowed at '/', and any user-agent line that names one of the 17 tokens (by
case-insensitive substring) whose token robots.csv nonetheless counts as allowed, for reading.
Offline. Usage: python3 -I studies/LH044/review/ai_tokens_check.py
"""
import csv, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data' / 'read-2026-11-08T1920Z'
svc = {s['id']: s for s in json.load(open(D / 'services.json'))['services']}
rows = list(csv.DictReader(open(D / 'robots.csv')))
toks = [k for k in rows[0] if k not in ('id', 'host', 'lighthouse_probe_allowed', 'star_root_allowed', 'star_probe_allowed')]
for r in rows:
    body = (D / ('%04d.b' % int(svc[r['id']]['robots_n']))).read_text('utf-8', 'replace')
    uas = [l.split(':', 1)[1].split('#')[0].strip() for l in body.splitlines() if l.lower().startswith('user-agent')]
    blocked = [t for t in toks if r[t] == 'False']
    named_but_allowed = sorted({t for t in toks for u in uas if t.lower() in u.lower() and r[t] == 'True'})
    if blocked or named_but_allowed:
        print('%s %-28s star_root=%s blocked=%d %s' % (r['id'], r['host'], r['star_root_allowed'], len(blocked),
              ('NAMED-BUT-ALLOWED=%s' % named_but_allowed) if named_but_allowed else ''))

# Which probes were sent to hosts whose robots.txt disallows, at the probe path, an Anthropic
# agent or crawler token (the four in measure 4, plus Claude-Code, which some files name)?
import sys
sys.path.insert(0, str(ROOT / 'scripts'))
from classify import parse_robots, robots_allowed
cls = {r['id']: r for r in csv.DictReader(open(D / 'classes.csv'))}
ANTH = ['ClaudeBot', 'Claude-User', 'Claude-SearchBot', 'anthropic-ai', 'Claude-Code']
print('\nprobes sent where the kept robots.txt disallows an Anthropic token at the probe path:')
for r in rows:
    s = svc[r['id']]
    if not s['probe_n']:
        continue
    g = parse_robots((D / ('%04d.b' % int(s['robots_n']))).read_text('utf-8', 'replace'))
    no = [t for t in ANTH if not robots_allowed(g, t, s['url'])]
    if no:
        print('   %s %-24s class=%-16s disallowed for %s' % (r['id'], r['host'], cls[r['id']]['class'], no))
