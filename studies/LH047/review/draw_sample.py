"""LH047 evidence review (R-0063): draw a sample of R1/R2 verdicts to re-derive by hand.

The seed is fixed here before any draw. Strata, from data/audit/requests-judged.csv:
  A  R1 "does not comply"                                  draw 6
  B  R1 "complies" but R2 "does not comply" (reading B)     draw 6
  C  R1 "complies" and R2 "complies", excluding robots.txt
     reads: one request from each of 14 robots.txt copies drawn at random
     (so the sample is not swamped by the 2,199 npm requests that share one copy)
  D  R1 "unknown"                                           draw 2
For each drawn request it prints the URL, the copy used and every group in that copy that
names `*`, Lighthouse-research or one of the seven Anthropic tokens, with its rules, so the
verdict can be re-derived by reading. The reviewer's own verdicts are written by hand into
review/sample-verdicts.csv; compare_sample.py compares them with the audit's.
Run from the repository root: python3 -I studies/LH047/review/draw_sample.py
"""
import csv, os, random
from urllib.parse import urlsplit

SEED = 63047
ROOT = os.getcwd()
J = os.path.join(ROOT, 'studies/LH047/data/audit/requests-judged.csv')
OUT = os.path.join(ROOT, 'studies/LH047/review/sample-drawn.csv')
rng = random.Random(SEED)
rows = list(csv.DictReader(open(J, newline='')))
for i, r in enumerate(rows):
    r['row'] = str(i + 2)  # line number in the CSV, header = 1
A = [r for r in rows if r['R1'] == 'does not comply']
B = [r for r in rows if r['R1'] == 'complies' and r['R2'] == 'does not comply']
Cpool = [r for r in rows if r['R1'] == 'complies' and r['R2'] == 'complies' and r['use'] != 'robots' and r['robots_file']]
D = [r for r in rows if r['R1'] == 'unknown']
sample = [('A', r) for r in rng.sample(A, 6)] + [('B', r) for r in rng.sample(B, 6)]
files = sorted({r['robots_file'] for r in Cpool})
for f in rng.sample(files, 14):
    sample.append(('C', rng.choice([r for r in Cpool if r['robots_file'] == f])))
sample += [('D', r) for r in rng.sample(D, 2)]
WANT = {'*', 'lighthouse-research', 'anthropic-ai', 'claudebot', 'claude-web', 'claude-user', 'claude-searchbot', 'claude-code', 'claude-agent'}
with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['n', 'stratum', 'row', 'who', 'url', 'robots_file', 'robots_status', 'robots_prov', 'audit_R1', 'audit_R1_rule', 'audit_R2', 'audit_R2_tokens'])
    for n, (s, r) in enumerate(sample, 1):
        w.writerow([n, s, r['row'], r['who'], r['url'], r['robots_file'], r['robots_status'], r['robots_prov'], r['R1'], r['R1_rule'], r['R2'], r['R2_tokens']])
for n, (s, r) in enumerate(sample, 1):
    u = urlsplit(r['url'])
    print('=' * 100)
    print('#%d stratum %s  row %s  %s  %s' % (n, s, r['row'], r['who'], r['utc']))
    print('URL :', r['url'])
    print('path:', (u.path or '/') + ('?' + u.query if u.query else ''))
    print('copy:', r['robots_file'], r['robots_status'], '|', r['robots_prov'])
    if r['robots_file'] and r['robots_status'].startswith('2'):
        lines = open(os.path.join(ROOT, r['robots_file']), 'rb').read().decode('utf-8', 'replace').splitlines()
        # print raw lines of groups whose user-agent run includes a wanted token
        keep, run_agents, in_agents, out = False, [], False, []
        for ln in lines:
            s2 = ln.split('#')[0].strip()
            k = s2.split(':', 1)[0].strip().lower() if ':' in s2 else ''
            if k == 'user-agent':
                if not in_agents:
                    run_agents = []
                in_agents = True
                run_agents.append(s2.split(':', 1)[1].strip().lower())
                keep = bool(set(run_agents) & WANT)
                if keep:
                    out.append(ln)
            elif k in ('allow', 'disallow', 'crawl-delay', 'content-signal', 'content-usage'):
                in_agents = False
                if keep:
                    out.append(ln)
        print('\n'.join('    ' + x for x in out[:80]) + ('\n    ...(%d more lines)' % (len(out) - 80) if len(out) > 80 else ''))
