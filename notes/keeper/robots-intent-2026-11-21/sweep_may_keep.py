#!/usr/bin/env python3
"""Sweep for kept bodies that the keeper's rule of 21 November 2026 says may not be kept
(notes/keeper/2026-11-21-robots-intent.md, point 2).

Finds every read log under studies/ and notes/ (a .csv, .json or .jsonl file with "log" in its name,
including CSV logs without a header row), ties each logged URL to a kept body file in the same folder,
and asks scripts/robots_gate.py's RobotsGate(UA).may_keep(url), which reads each host's robots.txt once.
A body already replaced by a <stem>.derived.json, and Lighthouse's own "not fetched" notes, are skipped.
Files in a log's folder that no logged URL ties to are counted by study.

Usage, from the repository root: LIGHTHOUSE_PROVIDER=anthropic python3 -I notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py OUT.json
Network: one GET of robots.txt per host, nothing else.
"""
import csv, json, os, sys
from collections import Counter, defaultdict
from urllib.parse import urlsplit

ROOT = os.getcwd()
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import robots_gate, robots_rules  # noqa: E402

UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
csv.field_size_limit(10 ** 9)
SKIP_DIRS = ('.git', 'harbour/.session', 'node_modules')
NOT_BODY = ('.derived.json', '.md', '.py', '.sh', '.svg', '.png')
NAME_KEYS = ('name', 'source', 'id', 'key')
FILE_KEYS = ('file', 'body_file', 'saved', 'saved_as', 'path', 'body', 'raw', 'out', 'filename')


def logs():
    for top in ('studies', 'notes'):
        for root, ds, fs in os.walk(top):
            if any(s in root for s in SKIP_DIRS):
                ds[:] = []; continue
            for f in fs:
                if 'log' in f.lower() and f.endswith(('.csv', '.json', '.jsonl')):
                    yield os.path.join(root, f)


def records(p):
    try:
        if p.endswith('.csv'):
            rows = list(csv.reader(open(p, newline='', errors='replace')))
            if not rows:
                return []
            if any(c.startswith('http') for c in rows[0]):  # no header row: positional
                return [{'_cols': r} for r in rows]
            return [dict(zip(rows[0], r)) for r in rows[1:]]
        if p.endswith('.jsonl'):
            return [json.loads(l) for l in open(p) if l.strip()]
        d = json.load(open(p))
    except Exception:
        return []
    if isinstance(d, list):
        return [x for x in d if isinstance(x, dict)]
    if isinstance(d, dict):
        for k in ('requests', 'reads', 'fetches', 'entries', 'log', 'items', 'sources'):
            if isinstance(d.get(k), list):
                return [x for x in d[k] if isinstance(x, dict)]
        return [d]
    return []


def url_of(r):
    if '_cols' in r:
        return next((c for c in r['_cols'] if c.startswith('http') and not c.endswith('/robots.txt')), None)
    for k, v in r.items():
        if isinstance(v, str) and v.startswith('http') and 'url' in str(k).lower() and 'robots' not in str(k).lower() \
                and not v.endswith('/robots.txt'):
            return v
    return None


def is_body(d, f):
    p = os.path.join(d, f)
    return os.path.isfile(p) and os.path.getsize(p) > 0 and not f.endswith(NOT_BODY) and 'log' not in f.lower()


def stem_of(fp):
    for ext in ('.raw.gz', '.body', '.raw', '.html', '.json', '.txt', '.gz', '.xml', '.csv', '.pdf'):
        if fp.endswith(ext):
            return fp[:-len(ext)]
    return fp


def main():
    out = sys.argv[1]
    allrecs = [(p, r) for p in logs() for r in records(p)]
    # url -> names used for it in headed logs, to tie positional (headerless) rows to files
    names_for = defaultdict(set)
    for p, r in allrecs:
        if '_cols' not in r:
            u = url_of(r)
            for k in NAME_KEYS:
                if u and isinstance(r.get(k), str) and r[k]:
                    names_for[u].add(r[k])
    tied, seen = [], set()
    log_dirs = set()
    for p, r in allrecs:
        d = os.path.dirname(p); log_dirs.add(d)
        u = url_of(r)
        if not u:
            continue
        files = os.listdir(d)
        cand = []
        for k in FILE_KEYS:
            v = r.get(k)
            if isinstance(v, str) and v and len(v) < 300:
                cand.append(os.path.basename(v))
        names = [r[k] for k in NAME_KEYS if isinstance(r.get(k), str) and r[k]] or sorted(names_for.get(u, ()))
        for n in names:
            cand += [f for f in files if f.split('.')[0] == n or stem_of(f) == n or f == n]
        for c in cand:
            if c in files and is_body(d, c):
                fp = os.path.join(d, c)
                if fp not in seen:
                    seen.add(fp); tied.append((fp, u))
                break
    gate = robots_gate.RobotsGate(UA)
    res, notkeep = [], []
    for fp, u in sorted(tied):
        stem = stem_of(fp)
        if os.path.exists(stem + '.derived.json'):
            continue
        with open(fp, 'rb') as fh:
            head = fh.read(64)
        if head.startswith(b'not fetched'):
            continue
        keep, why = gate.may_keep(u)
        row = {'file': fp, 'url': u, 'host': urlsplit(u).hostname, 'may_keep': keep, 'reason': why}
        rec = gate.cache.get('%s://%s/robots.txt' % (urlsplit(u).scheme, urlsplit(u).netloc), {})
        row['robots_status'] = rec.get('status')
        if not keep and why == 'not fetched' and isinstance(rec.get('status'), int) and rec.get('status') < 400:
            # the gate's recurring rule refuses the fetch, so it gives no keeping answer: ask the keeping rule itself
            k2, w2 = robots_rules.may_keep(rec['body'], u, rec.get('truncated', False))
            row.update(keep_rule=k2, keep_rule_reason=w2)
        res.append(row)
    untied = Counter()
    for d in log_dirs:
        for f in os.listdir(d):
            fp = os.path.join(d, f)
            if is_body(d, f) and fp not in seen and not os.path.exists(stem_of(fp) + '.derived.json'):
                untied[fp.split('/')[1] if fp.startswith('studies/') else 'notes'] += 1
    bad = [r for r in res if not r['may_keep'] and (r.get('keep_rule') is not True)]
    json.dump({'checked': len(res), 'refused_or_unknown': bad, 'all': res, 'untied_by_study': dict(sorted(untied.items())),
               'robots': {k: {'status': v.get('status'), 'sha256': v.get('sha256'), 'error': v.get('error')}
                          for k, v in gate.cache.items()}}, open(out, 'w'), indent=1)
    print('bodies tied and checked:', len(res), '| hosts:', len(gate.cache))
    print('may_keep False:', Counter(r['reason'] for r in res if not r['may_keep']))
    print('of which the keeping rule itself allows (recurring fetch refused only):',
          sum(1 for r in res if r.get('keep_rule') is True))
    print('refused or unknown (listed in output):', len(bad), Counter(r['host'] for r in bad))
    print('untied files by study:', dict(sorted(untied.items())))


if __name__ == '__main__':
    main()
