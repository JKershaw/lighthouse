"""R-0098: fresh recheck of the resolution of R-0082 in commit d8a7d8d (LH047 paper draft).
Recomputes, from retained primary data and with its own small robots.txt evaluator
(independent of studies/LH047/scripts/robots9309.py), each figure the resolution wrote.
Offline. Run from the repository root:
    python3 -I studies/LH047/review/paper/recheck_r0098.py > studies/LH047/review/paper/recheck_r0098.out
"""
import csv, json, re, collections
from urllib.parse import urlsplit, unquote

R = list(csv.DictReader(open('studies/LH047/data/audit/requests-judged.csv')))
NC = 'does not comply'
C = collections.Counter
TOK = json.load(open('scripts/robots_tokens.json'))
ANTH = [t['token'] for t in TOK['anthropic']]
KIND = {t['token']: t['kind'] for t in TOK['anthropic']}
AGENT = [t for t in ANTH if KIND[t] in ('user-triggered fetcher', 'user-directed hosted browser', 'harness (Claude Code)')]
print('Anthropic tokens in scripts/robots_tokens.json:', ANTH)
print('agent/user-triggered tokens (by kind):', AGENT)


# --- a minimal RFC 9309 evaluator, written for this recheck ---
def parse(text):
    groups, cur, last_ua = [], None, False
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k, v = k.strip().lower(), v.strip()
        if k == 'user-agent':
            if cur is None or not last_ua:
                cur = {'ua': [], 'rules': []}
                groups.append(cur)
            cur['ua'].append(v.lower())
            last_ua = True
        elif k in ('allow', 'disallow'):
            last_ua = False
            if cur is not None:
                cur['rules'].append((k, v))
        else:
            last_ua = False
    return groups


def pat_re(p):
    end = p.endswith('$')
    if end:
        p = p[:-1]
    return re.compile('^' + '.*'.join(re.escape(unquote(x)) for x in p.split('*')) + ('$' if end else ''))


def allowed(groups, path):
    best = None  # (length, is_allow)
    for g in groups:
        for k, v in g['rules']:
            if k == 'disallow' and v == '':
                continue
            if pat_re(v).match(unquote(path)):
                cand = (len(v), k == 'allow')
                if best is None or cand > best:
                    best = cand
    return True if best is None else best[1]


def disallowing_tokens(robots_file, url):
    text = open(robots_file, 'rb').read().decode('utf-8', 'replace')
    gs = parse(text)
    u = urlsplit(url)
    path = (u.path or '/') + ('?' + u.query if u.query else '')
    out = []
    for t in ANTH:
        named = [g for g in gs if t.lower() in g['ua']]
        if named and not allowed(named, path):
            out.append(t)
    return out


print('\n== 1. The 19 requests the keeper rule adds (overall_B breaks, overall_A does not) ==')
added = [r for r in R if r['overall_B'] == NC and r['overall_A'] != NC]
print('n =', len(added))
mism = 0
names_cb = only_cb = not_agent = cb_sole_dependency = 0
for r in added:
    mine = disallowing_tokens(r['robots_file'], r['url'])
    theirs = r['R2_tokens'].split()
    if sorted(mine) != sorted(theirs):
        mism += 1
    names_cb += 'ClaudeBot' in mine
    only_cb += mine == ['ClaudeBot']
    agent_hit = [t for t in mine if t in AGENT]
    not_agent += not agent_hit
    print(' %s %s %-40s mine=%s agent=%s' % (r['utc'], r['who'][:22].ljust(22), r['host'], ' '.join(mine), ' '.join(agent_hit) or '-'))
print('my evaluator vs audit R2_tokens mismatches:', mism)
print('disallowed by a group naming ClaudeBot:', names_cb, 'of', len(added))
print('NOT disallowed by any group naming an agent/user-triggered token (Claude-User, Claude-Agent, Claude-Code):', not_agent)
print('  cross-check with overall_B_agent complies among the 19:', sum(r['overall_B_agent'] != NC for r in added))
print('disallowed ONLY by the ClaudeBot group (no other Anthropic token, crawler or agent):', only_cb)
print('disallowed by a group naming another Anthropic CRAWLER/older token (Claude-SearchBot, Claude-Web, anthropic-ai) but no agent token:',
      sum(1 for r in added if not [t for t in disallowing_tokens(r['robots_file'], r['url']) if t in AGENT]
          and [t for t in disallowing_tokens(r['robots_file'], r['url']) if t != 'ClaudeBot']))

print('\n== 2. Unanswered among the 172 ==')
A = [r for r in R if r['overall_A'] == NC]
print('172 =', len(A), '; reached:', dict(C(r['reached'] for r in A)))
nr = [r for r in A if r['reached'] == 'status not recorded']
for r in nr:
    print(' status not recorded:', r['who'], r['url'], r['utc'], r['log'])
log = list(csv.DictReader(open('studies/LH042/data/dash-2026-11-08T1909Z/readlog.csv')))
for x in log:
    if 'shadowserver' in x['url']:
        print(' LH042 readlog row:', x['n'], x['url'], x['start_utc'], 'robots=%r status=%r bytes=%r error=%r' % (x['robots'], x['http_status'], x['bytes'], x['error']))
print(' In fetch.py as committed at 0916f1d (in force at 19:09), an unreadable robots.txt returns ok=True and the error column')
print(' is written only by the page request\'s own exception handler, so this row is the page request getting a reset.')
noans = [r for r in A if r['reached'].startswith('no (no answer)')] + nr
print('no answer on primary logs:', len(noans), '(4 marked no answer + 1 status-not-recorded shown above to be a reset)')
unreach = [r for r in A if r['R1_rule'].startswith('robots.txt unreachable at the time')]
print('the five to unreachable-robots sites:', len(unreach), sorted({r['host'] for r in unreach}),
      '; all in no-answer set:', all(r in noans for r in unreach))
print('refused by the container (an answer, from our own container, not the site):', sum(r['reached'].startswith('no (refused') for r in A))

print('\n== 3. PyPI ==')
p = [r for r in R if r['host'] == 'pypi.org' and r['R1'] == NC]
print('PyPI R1 breaches:', len(p), 'status:', dict(C(r['status'] for r in p)))
for r in p:
    if r['status'] == '200':
        print(' the 200:', r['utc'], r['who'], r['url'])

print('\n== 4. The 12 "other" robots.txt-rule requests ==')
fixed = [r for r in A if any(r[k].startswith(NC) for k in ('R1', 'R4', 'R5', 'R6'))]
r1 = [r for r in fixed if r['R1'] == NC]
coll = [r for r in r1 if r['host'] == 'pypi.org' and r['who'] == 'LH041']
other = [r for r in r1 if r not in coll]
print('113 =', len(fixed), '; R1 among them', len(r1), '; the collector\'s PyPI requests', len(coll),
      '; other R1 (the figure\'s light blue)', len(other), '=', sum(r['host'] == 'pypi.org' for r in other), 'PyPI from reviewers/drafting +',
      sum(r['host'] != 'pypi.org' for r in other), 'elsewhere')
print('of the', len(other), 'robots.txt unreachable:', sum(r['R1_rule'].startswith('robots.txt unreachable') for r in other))
for r in other:
    print(' ', r['who'], r['host'], r['status'] or '-', r['R1_rule'][:60])

print('\n== 5. Week and deadline (brief amendment 2, schedule rows) ==')
b = open('studies/LH047/brief.md').read()
print('amendment 2 names "Monday 16 November 2026" .. "Sunday 22 November 2026":',
      'Monday 16 November 2026' in b and 'Sunday 22 November 2026' in b)
for row in csv.reader(open('schedule/due.csv')):
    if row and row[0] in ('LH047-reread', 'LH047-reread-record', 'LH047-week-amendment'):
        print(' due.csv', row[0], 'earliest', row[3] or '-', 'deadline', row[4] or '-')
