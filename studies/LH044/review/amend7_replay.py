#!/usr/bin/env python3
"""LH044 amendment 7 (16 November 2026, post hoc): replay classifier 0.4 on read 1's retained files.

Read 1 (2026-11-15T1413Z) was classified with 0.3 and stays as read. This replays, offline and in
memory, what 0.4 would have made of it, by the collector's own steps: each service's final robots.txt
answer through robots_outcome('0.4'); where that is now a wall, no probe would have followed and the
class is wall_at_robots; otherwise the kept probe is re-classified with 0.4. It then tabulates both
with compare_reads.tally and lists every class that differs, and scans every kept body of the
baseline and read 1 for the new signature. Nothing in data/ is written.

Usage: python3 -I studies/LH044/review/amend7_replay.py
"""
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(HERE))
import collect  # noqa: E402
import compare_reads  # noqa: E402
from classify import classify, CHALLENGE_SIGS_04  # noqa: E402

D = collect.ROOT / 'data' / 'read-2026-11-15T1413Z'
meta = json.load(open(D / 'services.json'))
log = {r['n']: r for r in csv.DictReader(open(D / 'readlog.csv'))}
committed = {r['id']: r for r in csv.DictReader(open(D / 'classes.csv'))}

replayed = {}
for s in meta['services']:
    row = dict(committed[s['id']])
    if s['robots_n'] and s['robots_state'] not in ('host_cap',):
        rl = log[str(s['robots_n'])]
        rr = collect._load_resp(D, s['robots_n'])
        rr.update({'error': rl['error'] or None, 'url': rl['url'], 'truncated': rl['truncated']})
        state, _, pcls, pdet = collect.robots_outcome(rr, '0.4')
        if pcls == 'wall_at_robots' and row['class'] != 'wall_at_robots':
            row['class'], row['detail'] = pcls, pdet + ' (0.4 replay: no probe would follow)'
        elif s['probe_n'] and not pcls:
            pl = log[str(s['probe_n'])]
            pr = collect._load_resp(D, s['probe_n'])
            dv = collect._derived(pr)
            if dv is None:
                row['class'], row['detail'] = classify(pr['status'] or 0, pl['error'] or None, pr['headers'],
                                                       pr['body'], s['surface'], s['marker'], s['url'],
                                                       version='0.4')
    replayed[s['id']] = row

print('== Classes that differ, 0.3 as read -> 0.4 replay ==')
diff = [(k, committed[k]['class'], replayed[k]['class'], replayed[k]['detail'])
        for k in committed if committed[k]['class'] != replayed[k]['class']]
for k, a, b, det in diff:
    print('  %s (%s): %s -> %s  [%s]' % (k, committed[k]['stratum'], a, b, det))
print('  %d differ' % len(diff))

print('\n== Tally (0.4 replay; as read in brackets) ==')
ta, tb = compare_reads.tally(committed), compare_reads.tally(replayed)
keys = ['probe_answered', 'wall_at_robots', 'state_read', 'walled', 'open', 'robots_disallowed', 'unknown']
for st in ('named', 'drawn'):
    print('  %s: ' % st + ', '.join('%s %d (%d)' % (k, tb[st][k], ta[st][k]) for k in keys))
same_walls = all(ta[st]['walled'] == tb[st]['walled'] and ta[st]['state_read'] == tb[st]['state_read']
                 for st in ('named', 'drawn'))
print('  walled and read counts unchanged: %s' % same_walls)

base = {r['id']: r for r in csv.DictReader(open(collect.ROOT / 'data' / 'read-2026-11-08T1920Z' / 'classes.csv'))}
def closings(a, b):
    out = []
    for k in b:
        ca, cb = compare_reads.state(a[k]['class']), compare_reads.state(b[k]['class'])
        if a[k]['class'] == 'open' and cb == 'wall':
            out.append((k, 'closing'))
        if ca == 'wall' and b[k]['class'] == 'open':
            out.append((k, 'opening'))
    return sorted(out)
print('\n== Closings and openings against the baseline ==')
print('  as read:  ', closings(base, committed))
print('  0.4 replay:', closings(base, replayed))

print('\n== Kept bodies matching the 0.4 signature (baseline and read 1) ==')
for lab in ('read-2026-11-08T1920Z', 'read-2026-11-15T1413Z'):
    for b in sorted((collect.ROOT / 'data' / lab).glob('*.b')):
        text = b.read_bytes().decode('utf-8', 'replace')
        hits = [i for i, (_, _, pat) in enumerate(CHALLENGE_SIGS_04) if re.search(pat, text)]
        if hits:
            n = b.stem.lstrip('0')
            lg = list(csv.DictReader(open(b.parent / 'readlog.csv')))
            r = next(x for x in lg if x['n'] == n)
            print('  %s/%s %s %s %s status %s, alternatives %s' % (lab, b.name, r['service'], r['kind'], r['url'],
                                                                   r['status'], hits))
