"""R-0063: R1 under the rule as it now stands (scripts/robots_rules.py with provider 'anthropic',
tokens from scripts/robots_tokens.json as committed), for every request whose copy was parsed,
compared with the audit's R2 (reading B). Reads only retained copies; makes no request.
Run from the repository root: python3 -I studies/LH047/review/rule_now.py"""
import csv, os, sys
from urllib.parse import urlsplit
sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))
import robots_rules as RR  # noqa: E402
J = os.path.join(os.getcwd(), 'studies/LH047/data/audit/requests-judged.csv')
rows = list(csv.DictReader(open(J, newline='')))
diff = []
now_bad = 0
for r in rows:
    if r['R2'] == 'unknown':
        now_bad += any(r[k].startswith('does not comply') for k in ('R4', 'R5', 'R6', 'R7', 'R8'))
        continue
    u = urlsplit(r['url'])
    if u.path == '/robots.txt' or r['R1_rule'].startswith(('robots.txt unreachable', 'robots.txt 4', 'robots.txt itself')) or not r['robots_file'] or not r['robots_status'].startswith('2'):
        now = r['R1']  # no parsed file: the keeper's rule and R1 agree (unreachable = disallow, 4xx = allow)
    else:
        body = open(os.path.join(os.getcwd(), r['robots_file']), 'rb').read().decode('utf-8', 'replace')
        d = RR.decide(body, (u.path or '/') + ('?' + u.query if u.query else ''), 'anthropic')
        now = 'complies' if d.allowed else 'does not comply'
    others = [r[k] for k in ('R4', 'R5', 'R6', 'R7', 'R8')]
    overall = 'does not comply' if now == 'does not comply' or any(v.startswith('does not comply') for v in others) else 'other'
    now_bad += overall == 'does not comply'
    if (now == 'does not comply') != (r['R2'] == 'does not comply'):
        diff.append((r['who'], r['url'][:80], 'R2=' + r['R2'], 'rule now=' + now))
print('requests that do not comply overall under the rule as it now stands:', now_bad)
print('requests where the rule as it now stands and reading B (R2) differ on robots.txt:', len(diff))
for d in diff:
    print('  ', d)
# list requests that fail overall under reading B but not under the rule as it now stands
for r in rows:
    if r['overall_B'] == 'does not comply' and r['R2'] == 'does not comply' and not any(r[k].startswith('does not comply') for k in ('R4', 'R5', 'R6', 'R7', 'R8')):
        u = urlsplit(r['url'])
        if r['robots_file'] and r['robots_status'].startswith('2') and u.path != '/robots.txt':
            body = open(os.path.join(os.getcwd(), r['robots_file']), 'rb').read().decode('utf-8', 'replace')
            d = RR.decide(body, (u.path or '/') + ('?' + u.query if u.query else ''), 'anthropic')
            if d.allowed:
                print('  B fails, rule now allows:', r['who'], r['url'][:80], d.decided_by, d.rule)
