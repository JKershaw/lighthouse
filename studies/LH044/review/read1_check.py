"""LH044 read 1 evidence review (R-0072): reproduce the checkpoint's consequential counts from the
kept files, independently of scripts/compare_reads.py, and run the review's checks.

Offline; makes no request. From the repository root:
    python3 -I studies/LH044/review/read1_check.py > studies/LH044/review/read1_check-output.txt
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

D = Path(__file__).resolve().parent.parent / 'data'
A = D / 'read-2026-11-08T1920Z'
B = D / 'read-2026-11-15T1413Z'
WALL = {'challenge', 'login', 'rate_limited', 'refused', 'api_closed', 'wall_at_robots'}
UNK = {'unreachable', 'unread_proxy', 'robots_unreachable', 'robots_redirect',
       'not_probed_host_cap', 'skipped_retry_after',
       'review:unread_no_probe'}  # last: the review's label for P31 read as not a wall (section 8)


def rows(p):
    return list(csv.DictReader(open(p, encoding='utf-8')))


ca = {r['id']: r for r in rows(A / 'classes.csv')}
cb = {r['id']: r for r in rows(B / 'classes.csv')}
log = rows(B / 'readlog.csv')


def tab(cls, override=None):
    override = override or {}
    out = {}
    for s in ('named', 'drawn'):
        t = Counter()
        for i, r in cls.items():
            if r['stratum'] != s:
                continue
            c = override.get(i, r['class'])
            if c == 'robots_disallowed':
                t['robots_disallowed'] += 1
            elif c in UNK:
                t['unknown'] += 1
                t[c] += 1
            elif c == 'wall_at_robots':
                t['wall_at_robots'] += 1
            else:
                t['probe_answered'] += 1
                if c == 'unread_proxy':
                    raise SystemExit('unexpected')
            if c in WALL:
                t['walled'] += 1
        t['state_read'] = t['probe_answered'] + t['wall_at_robots']
        out[s] = dict(sorted(t.items()))
    return out


print('== 1. Measure 1/2 table, read 1, from classes.csv (independent count)')
for s, t in tab(cb).items():
    print(' ', s, t)
print('   baseline:')
for s, t in tab(ca).items():
    print(' ', s, t)

print('\n== 2. Closings and openings (open <-> walled, both known), with route at each read')
for i in sorted(cb):
    x, y = ca[i]['class'], cb[i]['class']
    if (x == 'open' and y in WALL) or (x in WALL and y == 'open'):
        print('  %s %s %s: %s (%s) -> %s (%s)' % (i, cb[i]['stratum'], cb[i]['host'], x, ca[i]['route'], y,
                                                  cb[i]['route']))

print('\n== 3. Requests (measure 8)')
kinds = Counter('robots' if r['kind'] == 'robots' else ('redirect' if r['kind'].startswith('robots-redirect')
                else r['kind']) for r in log)
print('  total', len(log), dict(kinds))
print('  routes', dict(Counter(r['route'] for r in log)))
strat = {i: cb[i]['stratum'] for i in cb}
bystr = defaultdict(Counter)
for r in log:
    bystr[strat[r['service']]][r['route']] += 1
print('  by stratum', {k: dict(v) for k, v in bystr.items()})
host = Counter(r['url'].split('/')[2] for r in log)
print('  max requests to one host', max(host.values()), [h for h, n in host.items() if n == max(host.values())][:5])
print('  bytes in readlog', sum(int(r['bytes'] or 0) for r in log))

print('\n== 4. The egress rule: every echo kept, by read and route')
for lab, d in (('baseline', A), ('read 1', B)):
    for r in rows(d / 'echoes.csv'):
        print('  %s %s %s %s %s' % (lab, r['service'], r['route'], r['name'], r['address']))
p04 = (B / '0179.b').read_text()
print('  read 1 P04 robots body (not caught by the collector):', p04[p04.find('y='):p04.find('"></meta>')])
for f in sorted((B / 'rdap').glob('*.json')):
    j = json.load(open(f))
    reg = [x[3] for e in j['entities'] for x in e['vcardArray'][1] if x[0] == 'fn']
    print('  RDAP %s: %s %s-%s %s registrant %s' % (f.stem, j['handle'], j['startAddress'], j['endAddress'],
                                                    j['name'], reg))

print('\n== 5. PubMed (A11): headers at both reads')
for lab, d, ns in (('baseline', A, ('0128', '0129')), ('read 1', B, ('0132', '0133'))):
    for n in ns:
        h = (d / (n + '.h')).read_text().splitlines()
        keep = [x for x in h if x.split(':')[0].lower() in ('http 200', 'http 403', 'server', 'via', 'alt-svc', 'date')
                or x.startswith('HTTP')]
        print('  %s %s %s' % (lab, n, keep))
print('  read 1 body:', (B / '0133.b').read_text())
print('  container policy refusal for comparison (0004.h):', (B / '0004.h').read_text().splitlines())

print('\n== 6. Imunify360: every kept body naming it, and the robots.txt answer before each probe')
for f in sorted(B.glob('*.b')):
    t = f.read_bytes()
    if b'Imunify360' in t:
        n = int(f.stem)
        r = log[n - 1]
        print('  %s %s %s %s %s' % (f.stem, r['service'], r['kind'], r['status'], r['route']))
for f in sorted(list(A.glob('*.b')) + list(B.glob('*.b'))):
    t = f.read_bytes()
    if b'wsidchk' in t or b'One moment, please' in t:
        n = int(f.stem)
        rl = rows(f.parent / 'readlog.csv')[n - 1]
        print('  JS challenge page (title "One moment, please...", wsidchk form):', f.parent.name, f.stem,
              rl['service'], rl['kind'], rl['status'], rl['content_type'], rl['bytes'],
              'robots_state=' + (cb if f.parent == B else ca)[rl['service']]['robots_state'])

print('\n== 7. robots.txt parsed at read 1 whose governing answer was an HTML page')
rob = {r['id']: r for r in rows(B / 'robots.csv')}
last = {}
for r in log:
    if r['kind'].startswith('robots'):
        last[r['service']] = r
for i in sorted(rob):
    r = last[i]
    b = (B / ('%04d.b' % int(r['n']))).read_bytes()[:300].lower()
    if b'<html' in b or b'<!doctype' in b:
        print('  %s %s n=%s %s %s bytes' % (i, cb[i]['host'], r['n'], r['status'], r['bytes']))
print('  parsed files: %d; excluding the two challenge pages: %d' % (len(rob), len(rob) - 2))
roba = {r['id'] for r in rows(A / 'robots.csv')}
both = set(rob) & roba
print('  parsed at both reads: %d; excluding P38 (challenge page at read 1): %d' % (len(both), len(both - {'P38'})))
ut = rows(B / 'usage_token.csv')
print('  usage token named: %d, mentioned: %d, of %d rows' % (
    sum(r['usage_token_named'] == 'True' for r in ut), sum(r['usage_token_mentioned'] == 'True' for r in ut), len(ut)))

print('\n== 8. P31 (contact-form captcha): what a non-wall reading does to the drawn row')
t = tab(cb, {'P31': 'review:unread_no_probe'})['drawn']
print('  P31 as not a wall (no probe was sent, so its state is unread):', t)
print('  -> walled %d of %d read' % (t['walled'], t['state_read']))
body = (B / '0225.b').read_text(encoding='utf-8', errors='replace')
k = body.find('g-recaptcha')
print('  widget context:', body[k - 160:k + 40].replace('\n', ' '))
print('  form:', body[body.find('<form action="https://elpub.ru'):][:120])

print('\n== 9. Hackage (R13): the chain and the governing file')
for r in log:
    if r['service'] == 'R13':
        print('  %s %s %s %s %s' % (r['n'], r['kind'], r['status'], r['url'][:95], r['bytes']))
t51 = (B / '0051.b').read_text()
print('  sha256 of kept 0051.b', hashlib.sha256(t51.encode()).hexdigest(), 'readlog', log[50]['sha256'])
print('  user-agent lines', sum(1 for x in t51.splitlines() if x.lower().startswith('user-agent')),
      '| "*" group:', any(x.strip().lower() == 'user-agent: *' for x in t51.splitlines()),
      '| __usage_ai-training present:', '__usage_ai-training' in t51)
print('  classes.csv R13:', cb['R13']['class'], cb['R13']['detail'])
