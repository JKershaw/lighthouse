#!/usr/bin/env python3
"""LH036 interim evidence review: detail checks from the raw bodies (read statuses, first-shown products,
SUSE products with no main kernel package, reference containers, AlmaLinux text changes).
Usage: python3 -I studies/LH036/review/check_details.py"""
from pathlib import Path
from html import unescape
import gzip, json, re, difflib
D = Path(__file__).resolve().parents[1] / 'data'
reads = sorted(p for p in D.glob('read-*') if p.is_dir())
MAIN = {'kernel-default', 'kernel-source', 'kernel-rt', 'kernel-64kb'}
def raw(r, n):
    log = {x['name']: x for x in json.loads((r / 'read_log.json').read_text())}
    x = log.get(n)
    if not x or x.get('status') != 200 or not x.get('file'): return None
    return gzip.decompress((r / x['file']).read_bytes()).decode('utf-8', 'replace')
def cells(tr): return [unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in re.findall(r'(?s)<t[dh][^>]*>(.*?)</t[dh]>', tr)]
print('== read statuses (non-200 or short bodies)')
for r in reads:
    for x in json.loads((r / 'read_log.json').read_text()):
        if x.get('status') != 200 or (x.get('bytes') or 0) < 200:
            print(r.name, x['name'], x.get('status'), x.get('bytes'), (x.get('robots') or {}).get('reason'), x.get('error'))
    print(r.name, 'entries', len(json.loads((r / 'read_log.json').read_text())))
print('\n== CVE record: which container carries each oss-security reference')
for r in (reads[0], reads[2]):
    c = json.loads(raw(r, 'cve_org'))
    for k, refs in [('cna', c['containers']['cna'].get('references', []))] + [('adp:' + a['providerMetadata'].get('shortName', ''), a.get('references', [])) for a in c['containers'].get('adp', [])]:
        print(r.name, k, [x['url'] for x in refs if 'openwall' in x['url']])
print('\n== Red Hat products first shown with a fixed release, by read')
seen = set()
for r in reads:
    ar = json.loads(raw(r, 'redhat')).get('affected_release', [])
    now = {a['product_name'] for a in ar}
    print(r.name, sorted(now - seen)); seen |= now
print('\n== SUSE products new to the page, and products with no main kernel package (their packages)')
seen = None
for r in reads:
    t = raw(r, 'suse'); sec = t[t.index('Status of this issue by product and package'):]; sec = sec[:sec.index('</table>')]
    rows = [c for c in (cells(tr) for tr in re.findall(r'(?s)<tr>(.*?)</tr>', sec)) if len(c) == 3 and c[0] != 'Product(s)']
    prods = {p for p, _, _ in rows}
    if seen is not None: print(r.name, 'new to page:', sorted(prods - seen), 'gone:', sorted(seen - prods))
    seen = prods
    if r in (reads[0], reads[-1]):
        nomain = {p: sorted({(pk, s) for q, pk, s in rows if q == p}) for p in prods if not any(q == p and pk in MAIN for q, pk, s in rows)}
        print(r.name, 'products', len(prods), 'with a main kernel package', len(prods) - len(nomain), 'without', len(nomain))
        for p, v in sorted(nomain.items()): print('   ', p, v[:4], '...' if len(v) > 4 else '')
print('\n== AlmaLinux text changes after 2 November, full')
def text_of(h):
    h = re.sub(r'(?s)<(script|style).*?</\1>', '', h)
    return [l.strip() for l in re.sub(r'[ \t\r]+', ' ', unescape(re.sub(r'<[^>]+>', '\n', h))).split('\n') if l.strip()]
prev = None
for r in reads:
    tx = text_of(raw(r, 'almalinux'))
    if prev is not None and r.name > 'read-2026-11-02':
        dl = [l for l in difflib.unified_diff(prev, tx, lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---'))]
        print(r.name, sorted(set(dl)))
    if r.name.startswith('read-2026-11-02'):
        i = next(k for k, l in enumerate(tx) if l.startswith('Update:'))
        print('2 Nov update text:', tx[i:i + 14])
    prev = tx
print('\n== SUSE live-patch rows (kernel-livepatch*, kgraft-patch*) by state, per read, and rows turning Released')
prev = None
for r in reads:
    t = raw(r, 'suse'); sec = t[t.index('Status of this issue by product and package'):]; sec = sec[:sec.index('</table>')]
    rows = [c for c in (cells(tr) for tr in re.findall(r'(?s)<tr>(.*?)</tr>', sec)) if len(c) == 3 and c[1].startswith(('kernel-livepatch', 'kgraft-patch'))]
    st = {}
    for p, pk, s in rows: st[s] = st.get(s, 0) + 1
    cur = {(p, pk): s for p, pk, s in rows}
    turned = sum(1 for k, s in cur.items() if s == 'Released' and prev is not None and prev.get(k) not in (None, 'Released'))
    new_rel = sum(1 for k, s in cur.items() if s == 'Released' and prev is not None and k not in prev)
    print(r.name, 'rows', len(rows), st, 'turned Released from another state', turned, 'new rows already Released', new_rel)
    prev = cur
