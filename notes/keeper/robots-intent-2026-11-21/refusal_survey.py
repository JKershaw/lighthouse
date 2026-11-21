import sys, urllib.request, urllib.error, json
from urllib.parse import urlsplit
sys.path.insert(0, 'scripts')
import robots_rules as rr
UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
urls = [u.strip() for u in open(sys.argv[1]) if u.strip()]
cache = {}
def robots(host, scheme):
    if host in cache: return cache[host]
    try:
        r = urllib.request.urlopen(urllib.request.Request(f"{scheme}://{host}/robots.txt", headers={"User-Agent": UA}), timeout=20)
        res = (r.status, r.read(512*1024).decode('utf-8', 'replace'))
    except urllib.error.HTTPError as e: res = (e.code, None)
    except Exception as e: res = (type(e).__name__, None)
    cache[host] = res; return res
TOK = ['Claude-User', 'Claude-Agent', 'ClaudeBot', 'Claude-SearchBot', 'anthropic-ai', 'Claude-Web', 'Claude-Code', 'Lighthouse-research']
out = []
for u in urls:
    p = urlsplit(u); st, body = robots(p.hostname, p.scheme or 'https')
    if body is None:
        out.append(dict(url=u, robots=st, cls='robots unreadable')); continue
    g = rr.parse(body)
    view = {t: rr.token_allowed(g, t, u) for t in TOK}
    star = rr.token_allowed(g, '*', u)
    named = [t for t in TOK if rr._rules_naming(g, t)[0]]
    d = rr.decide_groups(g, u, provider='anthropic')
    if d.allowed: cls = 'allowed now'
    elif view['Claude-User']: cls = 'T2: only crawler/other tokens refuse; Claude-User view allows'
    elif 'Claude-User' in named: cls = 'T1: Claude-User named and refused'
    else: cls = "T1: refused under '*' (no AI token named)" if not named else "T1: '*' refuses; AI crawler tokens named, Claude-User not"
    out.append(dict(url=u, robots=st, cls=cls, named=named, star=star, decided_by=d.decided_by, rule=d.rule))
json.dump(out, open(sys.argv[2], 'w'), indent=1)
from collections import Counter
hosts = {}
for o in out: hosts.setdefault(urlsplit(o['url']).hostname, set()).add(o['cls'])
print(Counter(o['cls'] for o in out)); print()
for h, c in sorted(hosts.items()): print(h, '|', '; '.join(sorted(c)))
