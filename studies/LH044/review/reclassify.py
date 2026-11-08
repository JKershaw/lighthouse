#!/usr/bin/env python3
"""Evidence review (R-0059): re-derive LH044's baseline classes offline from the retained files.

(a) Re-runs the study's own classifier, version 0.2 (scripts/classify.py at HEAD), over every
    service's kept robots.txt and probe response, by the same steps as collect.py's do_classify,
    and compares with data/read-2026-11-08T1920Z/classes.csv.
(b) Does the same with version 0.1 (classify.py as committed with the draw, 1789e54, read from
    git), to test the checkpoint's statement that only the GitHub and readthedocs classes changed.
(c) Scans every kept response that the classifier did not call a wall for wall-like text the
    signature lists do not cover, for the reviewer's own reading.
No network; nothing in the study's data directory is written.
Usage: python3 -I studies/LH044/review/reclassify.py
"""
import csv, importlib.util, json, re, subprocess, sys, types
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data' / 'read-2026-11-08T1920Z'
REPO = ROOT.parents[1]


def load_module(name, source):
    m = types.ModuleType(name)
    exec(compile(source, name, 'exec'), m.__dict__)
    return m


v02 = load_module('classify_v02', (ROOT / 'scripts' / 'classify.py').read_text())
v01 = load_module('classify_v01', subprocess.check_output(
    ['git', '-C', str(REPO), 'show', '1789e54:studies/LH044/scripts/classify.py'], text=True))

log = {r['n']: r for r in csv.DictReader(open(D / 'readlog.csv'))}
svc = json.load(open(D / 'services.json'))['services']
kept = {r['id']: r for r in csv.DictReader(open(D / 'classes.csv'))}


def resp(n):
    lines = (D / ('%04d.h' % int(n))).read_text().splitlines()
    st = lines[0].split(' ', 1)[1] if lines else 'None'
    hdrs = [tuple(x.split(': ', 1)) if ': ' in x else (x, '') for x in lines[1:] if x]
    return {'status': None if st == 'None' else int(st), 'headers': hdrs,
            'body': (D / ('%04d.b' % int(n))).read_bytes(), 'error': log[str(n)]['error'] or None,
            'url': log[str(n)]['url']}


def robots_class(C, r):
    if r['error']:
        return 'robots_unreachable', r['error'], None
    c, d = C.classify(r['status'], None, r['headers'], r['body'], 'file', '', r['url'])
    if c == 'unread_proxy':
        return 'robots_unreachable', d, None
    if c in ('challenge', 'rate_limited'):
        return 'wall_at_robots', c + ':' + d, None
    if 200 <= r['status'] < 300:
        return '', '', C.parse_robots(r['body'].decode('utf-8', 'replace'))
    if 300 <= r['status'] < 400:
        return 'robots_redirect', '', None
    if 400 <= r['status'] < 500:
        return '', '', []
    return 'robots_unreachable', str(r['status']), None


def derive(C):
    out = {}
    for s in svc:
        r = resp(s['robots_n'])
        cls, det, groups = robots_class(C, r)
        if not cls:
            if not C.robots_allowed(groups, 'Lighthouse-research', s['url']):
                cls = 'robots_disallowed'
            elif s['probe_n']:
                p = resp(s['probe_n'])
                cls, det = C.classify(p['status'] or 0, p['error'], p['headers'], p['body'],
                                      s['surface'], s['marker'], s['url'])
            else:
                cls = 'unprobed'
        out[s['id']] = cls
    return out


for name, C in (('0.2', v02), ('0.1', v01)):
    got = derive(C)
    diffs = [(i, kept[i]['class'], got[i]) for i in kept if kept[i]['class'] != got[i]]
    print('classifier %s: %d services, %d differ from classes.csv' % (name, len(got), len(diffs)))
    for d in diffs:
        print('   %s classes.csv=%s re-derived=%s' % d)

print('\n(c) kept responses not called walls that carry wall-like text:')
PAT = re.compile(r'(?i)captcha|challenge|verify (?:that )?you are (?:a )?human|are you a robot|just a moment|'
                 r'making sure you|anubis|go-away|access denied|blocked|http-equiv="?refresh|rate.?limit|'
                 r'too many requests|bot protection|unusual traffic')
for s in svc:
    for kind in ('robots_n', 'probe_n'):
        n = s[kind]
        if not n:
            continue
        if kind == 'robots_n' and kept[s['id']]['class'] == 'wall_at_robots':
            continue
        if kind == 'probe_n' and kept[s['id']]['wall'] == 'yes':
            continue
        r = resp(n)
        text = r['body'].decode('utf-8', 'replace')
        if r['status'] and 200 <= r['status'] < 300 and kind == 'robots_n' and 'user-agent' in text.lower():
            continue  # a parsed robots.txt mentioning these words in a rule path is not a page
        hits = sorted(set(m.group(0).lower() for m in PAT.finditer(text[:65536])))
        if hits:
            print('   %s %s n=%s status=%s class=%s hits=%s' % (s['id'], kind[:-2], n, r['status'],
                                                              kept[s['id']]['class'], hits[:8]))

print('\n(d) 2xx probes whose challenge or captcha signature was overridden by the marker:')
for s in svc:
    if not s['probe_n']:
        continue
    p = resp(s['probe_n'])
    if not (p['status'] and 200 <= p['status'] < 300):
        continue
    text = p['body'].decode('utf-8', 'replace')
    v = v02._match(v02.CHALLENGE_SIGS, p['headers'], text) or v02._match(v02.CAPTCHA_SIGS, p['headers'], text)
    if v and s['marker'] and s['marker'] in text:
        print('   %s %s signature=%s marker=%r class=%s' % (s['id'], s['host'], v, s['marker'], kept[s['id']]['class']))
