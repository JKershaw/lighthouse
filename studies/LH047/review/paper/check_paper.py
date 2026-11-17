"""LH047 paper evidence review (R-0082): recompute every count the draft
articles/drafts/rules-for-robots.md and its short form state, from
studies/LH047/data/audit/requests-judged.csv (itself rebuilt byte-identically by replay.sh).
Run from the repository root: python3 -I studies/LH047/review/paper/check_paper.py"""
import csv, collections
from datetime import datetime
R = list(csv.DictReader(open('studies/LH047/data/audit/requests-judged.csv')))
C = collections.Counter
NC = 'does not comply'
def t(s): return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
print('requests', len(R), C(r['source'] for r in R))
print('window', min(r['utc'] for r in R), max(r['utc'] for r in R))
rules = ['R1', 'R4', 'R5', 'R6', 'R8']
A = [r for r in R if r['overall_A'] == NC]
B = [r for r in R if r['overall_B'] == NC]
rr = [r for r in R if r['ua'] == 'research-reader']
print('research-reader ua class rows', len(rr))
def broke(r, keys): return [k for k in keys if r[k].startswith(NC)]
fixed = [r for r in A if broke(r, ['R1', 'R4', 'R5', 'R6'])]          # rules as fixed (R8 only for browser impostors)
r8only_A = [r for r in A if broke(r, rules) == ['R8']]
print('\n172 =', len(A), '; broke a fixed rule =', len(fixed), '; R8 only =', len(r8only_A))
print('research-reader requests', len(rr), 'of which in the 113:', sum(r in fixed for r in rr))
print('113 by rule (first rule):', C(broke(r, ['R1','R4','R5'])[0] for r in fixed),
      'overlaps:', sum(len(broke(r, ['R1','R4','R5'])) > 1 for r in fixed))
print('113 transcript-only:', sum(r['source']=='transcript' for r in fixed))
# known beforehand: the two dashboard requests
print('\nB =', len(B), '; added by R2 =', len(B) - len(A))
added = [r for r in B if r['overall_A'] != NC]
print('added requests', len(added), 'all research-reader?', sum(r['ua']=='research-reader' for r in added))
tok = C()
for r in added:
    for x in set(r['R2_tokens'].split()): tok[x] += 1
print('tokens over the 19 added:', tok.most_common())
print('added where ClaudeBot is among disallowing tokens:', sum('ClaudeBot' in r['R2_tokens'].split() for r in added))
print('added where only ClaudeBot (plus nothing else):', sum(r['R2_tokens'].split()==['ClaudeBot'] for r in added))
print('added by agent-token reading (B_agent):', sum(r['overall_B_agent']==NC for r in added))
broke_B = lambda r: [k for k in ['R1','R2','R4','R5','R6','R8'] if r[k].startswith(NC)]
r8only_B = [r for r in B if broke_B(r) == ['R8']]
print('B R8-only', len(r8only_B), '-> B minus those =', len(B) - len(r8only_B))
print('113 + 19 =', len(fixed) + len(added))
print('reviewer requests that were R8-only under A but break R2 under B:',
      [(r['host'], r['R2_tokens']) for r in r8only_A if r['R2']==NC])
# PyPI
p = [r for r in R if r['host']=='pypi.org' and r['R1']==NC]
l = [r for r in p if r['who']=='LH041']
print('\nPyPI R1 breaches', len(p), C(r['who'] for r in p), 'status', C(r['status'] for r in p))
print('collector span', min(r['utc'] for r in l), max(r['utc'] for r in l), 'robots_first', C(r['robots_first'] for r in l))
# rest
r1o = [r for r in fixed if r['R1']==NC and r['host']!='pypi.org']
print('\nother R1', len(r1o), [(r['who'], r['host'], r['status'] or '-', r['R1_rule'][:40]) for r in r1o])
r5 = [r for r in R if r['R5'].startswith(NC)]
print('R5', len(r5), 'R5 excl robots', sum(r['R5_excl_robots'].startswith(NC) for r in R), [(r['host'], r['R5_why']) for r in r5 if r['R5_excl_robots'].startswith(NC)])
print('R5 2-second ones:', sum('2 s after' in r['R5_why'] for r in r5))
r4 = [r for r in R if r['R4']==NC]
print('R4', len(r4), [(r['host'], r['kept']) for r in r4])
# status of 172
def st(r): return 'not found' if r['status']=='404' else ('no answer' if r['status']=='' else r['status'])
print('\n172 status', C(st(r) for r in A), 'reached', C(r['reached'] for r in A))
print('113 status', C(st(r) for r in fixed))
print('two habits', len(l) + len(rr))
# provenance of the robots verdict among the 172
prov = C(r['robots_prov'] for r in A)
print('\n172 robots provenance', prov)
rer = [r for r in A if r['robots_prov'].startswith('current re-read')]
aft = [r for r in A if r['robots_prov']=='retained, same study, read after the request']
print('re-read', len(rer), 'after', len(aft))
idx = list(csv.DictReader(open('studies/LH047/data/robots-index.csv')))
def gap(r):
    fs = [x for x in idx if x['file']==r['robots_file']]
    return [(t(x['utc'])-t(r['utc'])).total_seconds()/60 for x in fs]
print('copy-before-request? retained other/same study copies read after request:')
late = []
for r in A:
    if r['robots_prov'].startswith('retained'):
        g = gap(r)
        if g and max(g) > 0: late.append((r, max(g)))
print(' n', len(late), 'max minutes', round(max(g for _, g in late), 1) if late else None)
print(' of re-read+late, in the 59:', sum(r in r8only_A for r in rer) + sum(r in r8only_A for r, _ in late))
reread_times = sorted(x['utc'] for x in idx if x['study'] in ('robots-current', 'LH047') or 'robots-current' in x['file'])
print('robots-current read times', reread_times[:1], reread_times[-1:])
print('\ntranscript-only requests', sum(r['source']=='transcript' for r in R),
      'dashboard pair source', [(r['url'], r['source']) for r in R if '/api/' in r['url'] and r['host']=='declawed.io'])
