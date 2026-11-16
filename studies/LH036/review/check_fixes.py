#!/usr/bin/env python3
"""LH036 interim evidence review: fixes (measure 4) and pages (measure 5) recomputed from the raw read bodies,
independently of tabulate.py (SUSE and Debian parsed from the HTML table rows, not from extracted text lines).
Usage: python3 -I studies/LH036/review/check_fixes.py"""
from pathlib import Path
from html import unescape
from hashlib import sha256
import gzip, json, re
D = Path(__file__).resolve().parents[1] / 'data'
reads = sorted(p for p in D.glob('read-*') if p.is_dir())
MAIN = {'kernel-default', 'kernel-source', 'kernel-rt', 'kernel-64kb'}
def raw(r, n):
    log = {x['name']: x for x in json.loads((r / 'read_log.json').read_text())}
    x = log.get(n)
    if not x or x.get('status') != 200 or not x.get('file'): return None, x
    return gzip.decompress((r / x['file']).read_bytes()).decode('utf-8', 'replace'), x
def cells(tr): return [unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in re.findall(r'(?s)<t[dh][^>]*>(.*?)</t[dh]>', tr)]

print('== Debian')
for r in reads:
    t, _ = raw(r, 'debian')
    tabs = re.findall(r'(?s)<table>(.*?)</table>', t)
    tab = next(x for x in tabs if 'Source Package' in x)
    rows = [cells(tr) for tr in re.findall(r'(?s)<tr>(.*?)</tr>', tab)][1:]
    tab2 = next(x for x in tabs if 'Fixed Version' in x)
    rows2 = [cells(tr) for tr in re.findall(r'(?s)<tr>(.*?)</tr>', tab2)][1:]
    print(r.name, [(c[0].replace(' (PTS)', ''), c[1], c[2], c[3]) for c in rows])
    print('   fixed-version table:', rows2)

print('\n== Ubuntu (linux package)')
for r in reads:
    u = json.loads(raw(r, 'ubuntu')[0])
    lin = next(p for p in u['packages'] if p['name'] == 'linux')
    notes = [(n.get('id'), n.get('published')) for n in u.get('notices', []) if isinstance(n, dict)]
    print(r.name, 'priority', u.get('priority'), {s['release_codename']: (s['status'], s.get('description', '')) for s in lin['statuses']})
    print('   notices', len(notes), (min(n[1] for n in notes), max(n[1] for n in notes)) if notes else '')

print('\n== Red Hat')
prev_aff = None
for r in reads:
    j = json.loads(raw(r, 'redhat')[0])
    ar = j.get('affected_release', [])
    ps = j.get('package_state', [])
    prods = {a['product_name'] for a in ar}
    advs = {a.get('advisory') for a in ar}
    aff = sorted((p['product_name'], p['package_name']) for p in ps if p['fix_state'] == 'Affected')
    print(r.name, 'products with fixed release', len(prods), 'advisories', len(advs), 'fixed rows', len(ar), 'rows Affected', len(aff), 'dates', sorted({a.get('release_date', '')[:10] for a in ar}))
    if prev_aff is not None and set(prev_aff) - set(aff): print('   left Affected:', sorted(set(prev_aff) - set(aff)))
    prev_aff = aff
    if r == reads[-1]:
        print('   Affected now:', aff, 'Not affected:', sorted({p['product_name'] for p in ps if p['fix_state'] == 'Not affected'}))
        for a in sorted(ar, key=lambda a: (a.get('release_date'), a['product_name'])):
            print('   ', a.get('release_date', '')[:10], a.get('advisory'), a['product_name'], '|', a.get('package'))

print('\n== SUSE (main kernel packages: %s)' % sorted(MAIN))
prev_rel = None
for r in reads:
    t, _ = raw(r, 'suse')
    overall = re.search(r'Overall state of this security issue:\s*([^<]+)<', t).group(1).strip()
    sec = t[t.index('Status of this issue by product and package'):]
    sec = sec[:sec.index('</table>')]
    rows = [c for c in (cells(tr) for tr in re.findall(r'(?s)<tr>(.*?)</tr>', sec)) if len(c) == 3 and c[0] != 'Product(s)']
    st = {}
    for p, pkg, s in rows:
        if pkg in MAIN: st.setdefault(p, set()).add(s)
        else: st.setdefault(p, set())
    allp = {p for p, _, _ in rows}
    cls = {'rel': set(), 'onlyAff': set(), 'onlyIP': set(), 'NA': set(), 'other': set()}
    mixed = 0
    for p in allp:
        s = st.get(p, set())
        if 'Released' in s:
            cls['rel'].add(p); mixed += bool(s - {'Released'})
        elif s == {'Affected'}: cls['onlyAff'].add(p)
        elif s == {'In progress'}: cls['onlyIP'].add(p)
        elif s == {'Not affected'}: cls['NA'].add(p)
        else: cls['other'].add(p)
    print(r.name, 'overall', overall, 'page rows', len(rows), 'products', len(allp), {k: len(v) for k, v in cls.items()}, 'released-and-other', mixed,
          'other:', {p: sorted(st.get(p, set())) for p in cls['other']})
    if prev_rel is not None:
        print('   newly released:', sorted(cls['rel'] - prev_rel), ' lost released:', sorted(prev_rel - cls['rel']))
    prev_rel = cls['rel']
    if r == reads[-1]: print('   only Affected now:', sorted(cls['onlyAff']))

print('\n== Pages (measure 5)')
def text_of(h):
    h = re.sub(r'(?s)<(script|style).*?</\1>', '', h)
    return [l.strip() for l in re.sub(r'[ \t\r]+', ' ', unescape(re.sub(r'<[^>]+>', '\n', h))).split('\n') if l.strip()]
for n in ('anthropic', 'almalinux', 'kernel_announcement'):
    prev = None
    for r in reads:
        t, x = raw(r, n)
        if t is None:
            print(n, r.name, 'no body', (x or {}).get('status'), (x or {}).get('robots', {}).get('reason') if x else 'not in log'); continue
        tx = text_of(t)
        dm = re.search(r'"dateModified"\s*:\s*"([^"]+)"', t)
        print(n, r.name, 'bytes sha', x['sha256'][:12], 'text sha', sha256('\n'.join(tx).encode()).hexdigest()[:12], 'dateModified', dm.group(1) if dm else None,
              'challenge' if 'not a bot' in t[:2000] else '', 'title', (re.search(r'(?s)<title>(.*?)</title>', t) or [None, None])[1])
        if prev and prev != tx:
            import difflib
            dl = [l for l in difflib.unified_diff(prev, tx, lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---'))]
            print('   text diff (%d lines):' % len(dl), dl[:12])
        prev = tx
