import sys, json, urllib.request, urllib.error
from urllib.parse import urlsplit
from collections import Counter, defaultdict
sys.path.insert(0, 'scripts'); import robots_rules as rr
UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
TRAIN = ['ClaudeBot', 'anthropic-ai', 'GPTBot', 'Google-Extended', 'CCBot', 'Applebot-Extended', 'meta-externalagent', 'Bytespider', 'cohere-training-data-crawler']
kept = json.load(open(sys.argv[1])); cache = {}
def groups(u):
    p = urlsplit(u); h = p.hostname
    if h not in cache:
        try:
            r = urllib.request.urlopen(urllib.request.Request(f"{p.scheme}://{h}/robots.txt", headers={"User-Agent": UA}), timeout=20)
            cache[h] = (r.status, rr.parse(r.read(512*1024).decode('utf-8', 'replace')))
        except urllib.error.HTTPError as e: cache[h] = (e.code, None)
        except Exception as e: cache[h] = (type(e).__name__, None)
    return cache[h]
cls = Counter(); byhost = defaultdict(Counter); size = Counter()
for o in kept:
    st, g = groups(o['url'])
    if g is None: c = 'no rules readable (%s)' % st
    else:
        named_train = [t for t in TRAIN if rr._rules_naming(g, t)[0] and not rr.token_allowed(g, t, o['url'])]
        star = rr.token_allowed(g, '*', o['url'])
        user = rr.token_allowed(g, 'Claude-User', o['url'])
        if named_train and star: c = 'A: AI-training token named and refused; * allows'
        elif named_train: c = 'A+: AI-training token named and refused; * refuses too'
        elif not star: c = 'B: * refuses all bots (no AI token named)'
        else: c = 'C: allowed for training tokens'
    o['cls'] = c; cls[c] += 1; byhost[c][o['host']] += 1; size[c] += o['size']
json.dump(kept, open(sys.argv[2], 'w'))
for c, n in cls.most_common(): print(n, 'bodies,', round(size[c]/1e6, 1), 'MB |', c)
print()
for c in byhost:
    if not c.startswith('C'): print(c, '->', dict(byhost[c].most_common()))
