"""R-0125: week-47 verdicts split by whether the collector's code goes through the shared gate.
Reads data/reaudit-2026-W47/requests-judged.csv only. Run: python3 -I studies/LH047/review/r0125/gate_split.py"""
import csv, collections, os
here = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(here, '..', '..', 'data', 'reaudit-2026-W47', 'requests-judged.csv')
rows = [r for r in csv.DictReader(open(p)) if r['counted'] == 'audited']
print('audited', len(rows))
pages = [r for r in rows if r['kind'] == 'page']
print('page requests', len(pages))
t = collections.Counter((r['gated_in_code'], r['R1']) for r in pages)
print('pages by gated_in_code x R1:')
for k in sorted(t): print(' ', k, t[k])
t = collections.Counter((r['gated_in_code'], r['overall_A']) for r in rows)
print('all audited by gated_in_code x overall_A:')
for k in sorted(t): print(' ', k, t[k])
print('failing (overall A) by practice x gated x rule:')
f = collections.Counter()
for r in rows:
    if r['overall_A'] == 'does not comply':
        rules = [x for x in ('R1','R4','R5','R6','R7','R8') if r[x].startswith('does not')]
        f[(r['practice'], r['gated_in_code'], '+'.join(rules))] += 1
for k in sorted(f): print(' ', k, f[k])
print('pypi JSON-path requests:', sum(1 for r in pages if 'pypi.org' in r['host'] and '/json' in r['url']))
print('gate refusals (not sent) by practice:')
g = collections.Counter(r['practice'] for r in csv.DictReader(open(p)) if r['counted'] == 'apart: refused by the gate')
for k in sorted(g): print(' ', k, g[k])
print('pages, gated=no, by practice:')
g = collections.Counter(r['practice'] for r in pages if r['gated_in_code'] == 'no')
for k in sorted(g): print(' ', k, g[k])
print('audited rows by study LH041:', sum(1 for r in rows if r['study'] == 'LH041' or 'LH041' in r['practice']))
print('pypi.org audited rows:', collections.Counter(r['url'].split('pypi.org')[1][:12] for r in rows if r['host'] == 'pypi.org'))
