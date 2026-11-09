"""R-0063: an independent re-implementation of R1 and R2 (written by the reviewer without
reusing robots9309.py), run over every request in requests-judged.csv whose robots.txt copy
was parsed (2xx, not truncated, not answered by the container), to compare verdicts.
Run from the repository root: python3 -I studies/LH047/review/crosscheck_r1r2.py"""
import csv, os, re
from urllib.parse import urlsplit, unquote

ROOT = os.getcwd()
J = os.path.join(ROOT, 'studies/LH047/data/audit/requests-judged.csv')
ANTH = ['anthropic-ai', 'claudebot', 'claude-web', 'claude-user', 'claude-searchbot', 'claude-code', 'claude-agent']


def groups(text):
    out, agents, rules, prev = [], None, None, None
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        m = re.match(r'([A-Za-z-]+)\s*:\s*(.*)$', line)
        if not m:
            continue
        k, v = m.group(1).lower(), m.group(2).strip()
        if k == 'user-agent':
            if prev != 'ua':
                agents, rules = [], []
                out.append((agents, rules))
            agents.append(v.lower())
            prev = 'ua'
        elif k in ('allow', 'disallow') and agents is not None:
            rules.append((k, v))
            prev = 'rule'
    return out


def norm(s):
    # decode percent-escapes of unreserved characters only
    return re.sub(r'%([0-9A-Fa-f]{2})', lambda m: chr(int(m.group(1), 16)) if re.match(r'[A-Za-z0-9._~-]', chr(int(m.group(1), 16))) else '%' + m.group(1).upper(), s)


def matches(pat, path):
    pat, path = norm(pat), norm(path)
    end = pat.endswith('$')
    if end:
        pat = pat[:-1]
    parts = pat.split('*')
    rx = '^' + '.*'.join(map(re.escape, parts)) + ('$' if end else '')
    return re.search(rx, path, re.S) is not None


def allowed(gs, path):
    best_len, best_allow = -1, True
    for _, rules in gs:
        for k, p in rules:
            if not p or not matches(p, path):
                continue
            L = len(p)
            if L > best_len or (L == best_len and k == 'allow'):
                best_len, best_allow = L, (k == 'allow')
    return best_allow


diff, n = [], 0
for r in csv.DictReader(open(J, newline='')):
    if r['R1'] not in ('complies', 'does not comply') or not r['robots_status'].startswith('2') or not r['robots_file']:
        continue
    u = urlsplit(r['url'])
    path = (u.path or '/') + ('?' + u.query if u.query else '')
    if u.path == '/robots.txt':
        continue
    n += 1
    g = groups(open(os.path.join(ROOT, r['robots_file']), 'rb').read().decode('utf-8', 'replace'))
    own = [x for x in g if 'lighthouse-research' in x[0]] or [x for x in g if '*' in x[0]]
    r1 = 'complies' if allowed(own, path) else 'does not comply'
    bad = [t for t in ANTH if [x for x in g if t in x[0]] and not allowed([x for x in g if t in x[0]], path)]
    mine_tokens = set(bad)
    theirs = set(x.lower() for x in r['R2_tokens'].split())
    if r1 != r['R1'] or mine_tokens != theirs:
        diff.append((r['who'], r['url'][:90], r['R1'], r1, sorted(theirs), sorted(mine_tokens)))
print('requests compared (parsed 2xx copies, not robots.txt reads):', n)
print('differences:', len(diff))
for d in diff:
    print('  ', d)
