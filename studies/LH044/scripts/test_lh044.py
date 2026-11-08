#!/usr/bin/env python3
"""Offline checks for LH044's collector and classifier. Makes no network request.

  1. Re-classifies every retained baseline response (data/read-2026-11-08T1920Z) in memory and
     compares with the committed classes.csv.
  2. Exercises fetch_robots (amendment 3) against canned responses: same-site and cross-site
     redirects, relative Locations, the five-redirect limit, the per-host cap, and a final hop
     answered by this container's own policy. The first hop of each case is a retained baseline
     robots.txt redirect where one exists.
  3. A few RFC 9309 matching cases.
  4 to 6. Amendment 4: the robots.txt read limit, echoed addresses, refresh-to-captcha pages.
  7. Amendment 5 (the keeper's rule, scripts/robots_rules.py): the eight baseline probes the
     evidence review named would not have been sent, under any provider setting; no other baseline
     probe would have been withheld and none allowed that protocol 0.1 refused; measure 4 reads the
     same on every baseline file with either matcher; and an offline read (fetch replaced by the
     retained responses) withholds the probe and records the provider and the deciding group.

Usage: python3 -I studies/LH044/scripts/test_lh044.py
"""
from pathlib import Path
import csv
import io
import json
import sys
import tempfile
import contextlib

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import collect  # noqa: E402
from classify import parse_robots, robots_allowed  # noqa: E402

BASE = collect.ROOT / 'data' / 'read-2026-11-08T1920Z'
fails = []


def check(name, cond):
    print(('ok   ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)


# 1. classifier on the retained baseline, in a temporary copy so nothing in the repository changes
committed = {r['id']: (r['class'], r['detail']) for r in csv.DictReader(open(BASE / 'classes.csv'))}
with tempfile.TemporaryDirectory() as tmp:
    fake_root = Path(tmp)
    (fake_root / 'data').mkdir()
    import shutil
    work = fake_root / 'data' / BASE.name   # same label, so the baseline's classifier (0.2) applies
    shutil.copytree(BASE, work, ignore=shutil.ignore_patterns('classes.csv', 'robots.csv', 'summary.json'))
    old = collect.ROOT
    collect.ROOT = fake_root
    with contextlib.redirect_stdout(io.StringIO()):
        collect.do_classify(BASE.name[len('read-'):])
    collect.ROOT = old
    again = {r['id']: (r['class'], r['detail']) for r in csv.DictReader(open(work / 'classes.csv'))}
check('baseline reclassified offline matches committed classes.csv (%d services)' % len(committed),
      again == committed)


# 2. fetch_robots against canned responses
def resp(url, status, headers=None, body=b'', error=None):
    return {'url': url, 'status': status, 'headers': headers or [], 'body': body, 'error': error,
            'error_detail': '', 'truncated': False, 'sha256': '', 'elapsed_ms': 0, 'ua': '', 'accept': '',
            'utc': '2026-11-15T00:00:00Z', 'encoding': ''}


class FakeRec:
    def __init__(self, table):
        self.table, self.n, self.host_counts, self.log, self.v03 = table, 0, {}, [], True

    def get(self, sid, kind, url, ua, accept, cap=65536):
        self.caps = getattr(self, 'caps', []) + [cap]
        self.n += 1
        h = (collect.urlsplit(url).hostname or '').lower()
        self.host_counts[h] = self.host_counts.get(h, 0) + 1
        r = dict(self.table[url])
        r['n'] = self.n
        self.log.append((kind, url))
        return r


def retained_first_hop(sid):
    meta = json.load(open(BASE / 'services.json'))
    s = next(x for x in meta['services'] if x['id'] == sid)
    r = collect._load_resp(BASE, s['robots_n'])
    log = {x['n']: x for x in csv.DictReader(open(BASE / 'readlog.csv'))}
    url = log[str(s['robots_n'])]['url']
    return url, resp(url, r['status'], r['headers'], r['body'])


ROBOTS_OK = b'User-agent: *\nDisallow: /private\n'

# same-site, absolute Location (retained: wikimedia.org -> www.wikimedia.org//robots.txt)
u0, r0 = retained_first_hop('D02')
loc = collect.header(r0, 'location')
t = {u0: r0, collect.urljoin(u0, loc): resp(collect.urljoin(u0, loc), 200, [], ROBOTS_OK)}
rec = FakeRec(t)
final, chain, cut = collect.fetch_robots(rec, 'D02', u0)
st, groups, pcls, _ = collect.robots_outcome(final)
check('D02 retained redirect followed once to a parsed robots.txt', len(chain) == 2 and st == 'parsed' and not cut)
check('rules of the final robots.txt apply to the probe host',
      collect.obey(groups, 'https://wikimedia.org/api/x', None).allowed and
      not collect.obey(groups, 'https://wikimedia.org/private/x', None).allowed)
check('hops logged with their own kind', [k for k, _ in rec.log] == ['robots', 'robots-redirect-1'])

# relative Location (retained: docs.rs -> /-/static/.../robots.txt)
u0, r0 = retained_first_hop('D14')
nxt = collect.urljoin(u0, collect.header(r0, 'location'))
rec = FakeRec({u0: r0, nxt: resp(nxt, 200, [], ROBOTS_OK)})
final, chain, cut = collect.fetch_robots(rec, 'D14', u0)
check('D14 relative Location resolved against the robots.txt URL', nxt.startswith('https://docs.rs/') and
      collect.robots_outcome(final)[0] == 'parsed')

# cross-site onto github.com, answered by this container's own policy (retained: hackage)
u0, r0 = retained_first_hop('R13')
nxt = collect.urljoin(u0, collect.header(r0, 'location'))
policy = b'{"message":"GitHub access to this repository is not enabled for this session."}'
rec = FakeRec({u0: r0, nxt: resp(nxt, 403, [('Content-Type', 'application/json')], policy)})
final, chain, cut = collect.fetch_robots(rec, 'R13', u0)
st, _, pcls, det = collect.robots_outcome(final)
check('R13 cross-site hop to a container refusal is robots_unreachable, so no probe',
      st == 'unreachable' and pcls == 'robots_unreachable')

# five-redirect limit: six requests, chain ends on a redirect -> robots_redirect, no probe
t = {}
for k in range(7):
    url = 'https://loop.example/r%d' % k if k else 'https://loop.example/robots.txt'
    t[url] = resp(url, 301, [('Location', '/r%d' % (k + 1))])
rec = FakeRec(t)
final, chain, cut = collect.fetch_robots(rec, 'X', 'https://loop.example/robots.txt')
check('at most five redirects followed (six requests)', len(chain) == 6)
check('a chain still redirecting after five hops reads as robots_redirect',
      collect.robots_outcome(final)[2] == 'robots_redirect')

# per-host cap: a host already at HOST_CAP gets no further request
rec = FakeRec({'https://full.example/robots.txt': resp('https://full.example/robots.txt', 200, [], ROBOTS_OK)})
rec.host_counts['full.example'] = collect.HOST_CAP
final, chain, cut = collect.fetch_robots(rec, 'X', 'https://full.example/robots.txt')
check('host cap stops the robots.txt request', chain == [] and cut == 'host_cap')
check('host cap stops a probe', collect.host_full(rec, 'https://full.example/x'))
check('one service uses at most HOST_CAP requests on one host (6 robots + 1 probe)',
      collect.ROBOTS_MAX_REDIRECTS + 2 == collect.HOST_CAP)

# 3. RFC 9309 matching
g = parse_robots('User-agent: *\nDisallow: /*?\nAllow: /a$\n\nUser-agent: Lighthouse-research\nDisallow: /p\n')
check('own product-token group replaces *', robots_allowed(g, 'Lighthouse-research', 'https://x/q?1')
      and not robots_allowed(g, 'Lighthouse-research', 'https://x/p/1'))
check('wildcard honoured for others', not robots_allowed(g, 'Other', 'https://x/q?1'))

# 4. Amendment 4 (1): robots.txt read limit and cut-off last lines
from classify import complete_lines, classify  # noqa: E402
log = {x['n']: x for x in csv.DictReader(open(BASE / 'readlog.csv'))}
meta = json.load(open(BASE / 'services.json'))
svc = {x['id']: x for x in meta['services']}
n = svc['R12']['robots_n']
cran = collect._load_resp(BASE, n)
cran.update({'error': None, 'url': log[str(n)]['url'], 'truncated': log[str(n)]['truncated']})
check('CRAN robots.txt was cut at the baseline (64 KiB)', log[str(n)]['truncated'] == 'True')
check('baseline (0.2) still reads CRAN as parsed', collect.robots_outcome(cran, '0.2')[0] == 'parsed')
st, _, pcls, det = collect.robots_outcome(cran, '0.3')
check('from read 1 a robots.txt cut at the limit is robots_unreachable, so no probe', pcls == 'robots_unreachable')
text = cran['body'].decode('utf-8', 'replace')
probe = svc['R12']['url']
check('the cut-off fragment alone disallowed the probe',
      not robots_allowed(parse_robots(text), 'Lighthouse-research', probe))
check('complete lines only: the fragment is never applied',
      robots_allowed(parse_robots(complete_lines(text, True)), 'Lighthouse-research', probe)
      and not complete_lines(text, True).rstrip('\n').endswith('/web/pac'))
check('an uncut file is kept whole', complete_lines('a\nb', False) == 'a\nb')
rec = FakeRec({'https://c.example/robots.txt': resp('https://c.example/robots.txt', 200, [], b'')})
collect.fetch_robots(rec, 'X', 'https://c.example/robots.txt')
check('robots.txt requested with a 512 KiB cap from read 1', rec.caps == [512 * 1024] and collect.ROBOTS_CAP >= 500 * 1024)

# 5. Amendment 4 (2): echoed addresses and route
echoes = []
for k, x in log.items():
    r = collect._load_resp(BASE, k)
    echoes += [(x['service'], x['route'], w, nm, a) for w, nm, a in collect.scan_echoes(r['headers'], r['body'])]
names = {e[3] for e in echoes}
check('x-client-ip and x-ratelimit-ip echoes found in the baseline', {'x-client-ip', 'x-ratelimit-ip'} <= names)
check('body echo found on the plain-HTTP route (P04)', any(e[0] == 'P04' and e[2] == 'body' and e[1] == 'direct-http' for e in echoes))
check('echoes on the proxied route are all in 160.79.104.0/21',
      all(e[4].startswith('160.79.10') and 104 <= int(e[4].split('.')[2]) <= 111 for e in echoes if e[1] == 'egress-proxy'))
syn = collect.scan_echoes([('X-Forwarded-For', '203.0.113.7, 10.0.0.1'), ('Server', 'nginx')],
                          b'<p>Your IP address is 198.51.100.9</p><p>version 1.2.3.4.5</p>')
check('synthetic echoes: forwarded-for header and a body phrase',
      ('header', 'x-forwarded-for', '203.0.113.7') in syn and any(a == '198.51.100.9' for _, _, a in syn))
check('a version string is not an address', not any(a.startswith('1.2.3') for _, _, a in syn))
rows = list(csv.DictReader(open(BASE / 'classes.csv')))
check('classes.csv records each service\'s route', 'route' in rows[0] and all(r['route'] for r in rows))

# 6. Amendment 4 (3): refresh-to-captcha pages (P04), post hoc
p4 = collect._load_resp(BASE, svc['P04']['probe_n'])
check('P04 probe: 0.2 open_unconfirmed, 0.3 challenge',
      classify(p4['status'], None, p4['headers'], p4['body'], 'api', '<Identify>', version='0.2')[0] == 'open_unconfirmed'
      and classify(p4['status'], None, p4['headers'], p4['body'], 'api', '<Identify>', version='0.3') == ('challenge', 'captcha-refresh'))
n = svc['P04']['robots_n']
p4r = collect._load_resp(BASE, n)
p4r.update({'error': None, 'url': log[str(n)]['url'], 'truncated': log[str(n)]['truncated']})
check('P04 robots.txt: 0.2 parsed (a probe followed), 0.3 wall_at_robots (no probe)',
      collect.robots_outcome(p4r, '0.2')[0] == 'parsed' and collect.robots_outcome(p4r, '0.3')[2] == 'wall_at_robots')
check('a page that only mentions a captcha is not a challenge',
      classify(200, None, [], b'<html><p>Our forms use a captcha.</p>hello</html>', 'page', 'hello', version='0.3')[0] == 'open')

# 7. Amendment 5: the keeper's rule (scripts/robots_rules.py), provider from LIGHTHOUSE_PROVIDER
import robots_rules  # noqa: E402  (collect put scripts/ on the path)
EIGHT = ['D15', 'Q07', 'F06', 'F07', 'R06', 'R07', 'D11', 'P18']
withheld = {p: set() for p in ('anthropic', 'openai', None)}
looser, m4_diff = [], []
for sid, s in svc.items():
    if not s['robots_n'] or s['robots_state'] != 'parsed':
        continue
    n = s['robots_n']
    rr = collect._load_resp(BASE, n)
    rr.update({'error': None, 'url': log[str(n)]['url'], 'truncated': log[str(n)]['truncated']})
    st, g, _, _ = collect.robots_outcome(rr, '0.3')
    if st != 'parsed':
        continue       # CRAN (R12), cut at 64 KiB: robots_unreachable from read 1 whatever the rule
    old_g = parse_robots(rr['body'].decode('utf-8', 'replace'))
    old_ok = robots_allowed(old_g, 'Lighthouse-research', s['url'])
    for p in withheld:
        ok = collect.obey(g, s['url'], p).allowed
        if s['probe_n'] and old_ok and not ok:
            withheld[p].add(sid)
        if ok and not old_ok:
            looser.append((sid, p))
    root = '%s://%s/' % (collect.urlsplit(s['url']).scheme, collect.urlsplit(s['url']).netloc)
    from classify import AI_TOKENS  # noqa: E402
    for t in AI_TOKENS + ['*']:
        if robots_allowed(old_g, t, root) != robots_rules.token_allowed(g, t, root):
            m4_diff.append((sid, t))
for p, ids in withheld.items():
    check('provider %s: the baseline probes withheld under amendment 5 are exactly the eight %s'
          % (p or 'unknown (all)', ','.join(EIGHT)), ids == set(EIGHT))
check('every one of the eight was sent at the baseline', all(svc[x]['probe_n'] for x in EIGHT))
check('no baseline robots.txt allows under amendment 5 a probe protocol 0.1 refused', looser == [])
check('measure 4 reads the same on every parsed baseline file with either matcher', m4_diff == [])
for sid in EIGHT:
    n = svc[sid]['robots_n']
    rr = collect._load_resp(BASE, n)
    rr.update({'error': None, 'url': log[str(n)]['url'], 'truncated': log[str(n)]['truncated']})
    d = collect.obey(collect.robots_outcome(rr, '0.3')[1], svc[sid]['url'], 'anthropic')
    check('%s %s withheld as anthropic, decided by %s (%s, line %s)' % (sid, svc[sid]['host'], d.decided_by,
          d.rule, d.line), not d.allowed and d.decided_by in robots_rules.load_tokens()['anthropic'])

# an offline read through do_read itself: fetch replaced by the retained responses, no network
import lh044lib  # noqa: E402
by_url = {}
for k, x in log.items():
    r = collect._load_resp(BASE, k)
    by_url[x['url']] = dict(resp(x['url'], r['status'], r['headers'], r['body']), sha256=x['sha256'])
asked = []


def fake_fetch(url, ua=None, accept=None, cap=None):
    asked.append(url)
    return dict(by_url[url])


for prov in ('anthropic', None):
    with tempfile.TemporaryDirectory() as tmp:
        fake_root = Path(tmp)
        (fake_root / 'data').mkdir()
        saved = (collect.ROOT, collect.fetch, collect.PAUSE, collect.load_panel)
        panel = [dict(r, stratum='named') for r in csv.DictReader(open(collect.ROOT / 'panel' / 'named.csv'))
                 if r['id'] in ('D15', 'D01')]
        collect.ROOT, collect.fetch, collect.PAUSE = fake_root, fake_fetch, 0
        collect.load_panel = lambda: panel
        asked.clear()
        with contextlib.redirect_stdout(io.StringIO()):
            collect.do_read('2026-11-15T0000Z', prov)
        collect.ROOT, collect.fetch, collect.PAUSE, collect.load_panel = saved
        meta = json.load(open(fake_root / 'data' / 'read-2026-11-15T0000Z' / 'services.json'))
        d15 = next(x for x in meta['services'] if x['id'] == 'D15')
        rob = {r['id']: r for r in csv.DictReader(open(fake_root / 'data' / 'read-2026-11-15T0000Z' / 'robots.csv'))}
        summ = json.load(open(fake_root / 'data' / 'read-2026-11-15T0000Z' / 'summary.json'))
        check('offline read, provider %s: D15 gets its robots.txt only, recorded robots_disallowed by an Anthropic '
              'token, provider recorded' % (prov or 'all'),
              d15['pre_class'] == 'robots_disallowed' and not d15['probe_n'] and 'by ClaudeBot' in d15['pre_detail']
              and svc['D15']['url'] not in asked and meta['provider'] == (prov or 'all')
              and summ['provider'] == (prov or 'all'))
        check('offline read, provider %s: robots.csv carries the obeyed decision' % (prov or 'all'),
              rob['D15']['obeyed_probe_allowed'] == 'False' and rob['D15']['obeyed_decided_by'] == 'ClaudeBot')

print('\n%d failed' % len(fails))
sys.exit(1 if fails else 0)
