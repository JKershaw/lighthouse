import os, json, csv, glob, sys
from urllib.parse import urlsplit
csv.field_size_limit(10**9)
SKIP = ('./.git', './harbour/.session')
logs = []
for root, ds, fs in os.walk('.'):
    if root.startswith(SKIP): ds[:] = []; continue
    for f in fs:
        if 'log' in f.lower() and f.endswith(('.csv', '.json', '.jsonl')) and not f.startswith(('google-cloud', 'colorlog', 'loguru', 'structlog')):
            logs.append(os.path.join(root, f))
def records(p):
    try:
        if p.endswith('.csv'): return list(csv.DictReader(open(p, newline='', errors='replace')))
        if p.endswith('.jsonl'): return [json.loads(l) for l in open(p) if l.strip()]
        d = json.load(open(p))
    except Exception: return []
    if isinstance(d, list): return [x for x in d if isinstance(x, dict)]
    if isinstance(d, dict):
        for k in ('requests', 'reads', 'fetches', 'entries', 'log', 'items', 'sources'):
            if isinstance(d.get(k), list): return [x for x in d[k] if isinstance(x, dict)]
        return [d]
    return []
out = []; nologurl = 0
for p in logs:
    d = os.path.dirname(p); files = os.listdir(d)
    for r in records(p):
        url = None
        for k, v in r.items():
            if isinstance(v, str) and v.startswith('http') and 'url' in str(k).lower() and 'robots' not in str(k).lower() and not v.endswith('/robots.txt'):
                url = v; break
        if not url: nologurl += 1; continue
        cand = []
        for k in ('file', 'body_file', 'saved', 'saved_as', 'path', 'body', 'raw', 'out', 'filename'):
            v = r.get(k)
            if isinstance(v, str) and v and len(v) < 300: cand.append(os.path.basename(v))
        n = r.get('name') or r.get('id') or r.get('source') or r.get('key')
        if isinstance(n, str) and n:
            cand += [f for f in files if f.split('.')[0] == n]
        hit = [c for c in cand if c in files and os.path.getsize(os.path.join(d, c)) > 0]
        if hit:
            out.append(dict(url=url, host=urlsplit(url).hostname, file=os.path.join(d, hit[0]), size=os.path.getsize(os.path.join(d, hit[0]))))
# dedupe by file
seen = {}; [seen.setdefault(o['file'], o) for o in out]
out = list(seen.values())
json.dump(out, open(sys.argv[1], 'w'))
from collections import Counter
c = Counter(o['host'] for o in out)
print(len(logs), 'logs;', len(out), 'kept bodies matched to a URL;', len(c), 'hosts;', nologurl, 'records without url')
print(c.most_common(80))
