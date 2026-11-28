"""R-0174: compare the visible article text of the three Phantom reports whose bodies are retained
(TechCentral, eWeek, The Next Web) across the reads of 13, 19 and 26 November 2026.
Run: python3 -I notes/R-0174-lh050-reader-evidence/reread_compare.py"""
import re, html, hashlib, json
D = 'studies/LH050/data/'
reads = {'13': D+'2026-11-13T1454Z/bodies/', '19': D+'2026-11-19T1417Z/bodies/', '26': D+'2026-11-26T1414Z/bodies/'}
pages = {'TechCentral': ('S24_techcentral.html', 'In the future, the battlefield', 'reducing the perceived risks and consequences'),
         'eWeek': ('S25_eweek.html', 'A San Francisco startup with ties', 'strengthening US manufacturing.'),
         'TNW': ('S27_tnw.html', 'Foundation Future Industries, a San Francisco startup', 'Whether they need to look human to fight is the question')}
def text(p):
    s = open(p, encoding='utf-8', errors='replace').read()
    meta = sorted(set(re.findall(r'"(datePublished|dateModified)"\s*:\s*"([^"]+)"', s)))
    s = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?s)<!--.*?-->', ' ', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s); s = html.unescape(s); s = re.sub(r'\s+', ' ', s)
    return s, meta
for name, (fn, start, end) in pages.items():
    out = []
    for d, base in reads.items():
        s, meta = text(base+fn)
        i = s.find(start); j = s.find(end, i)
        body = s[i:j+len(end)] if i >= 0 and j >= 0 else None
        h = hashlib.sha256(body.encode()).hexdigest()[:16] if body else 'NOT FOUND'
        out.append((d, h, len(body) if body else 0, meta[:4]))
    print(name)
    for o in out: print('   ', o)
    print('    same article text across reads:', len({o[1] for o in out}) == 1)
for d in ('13', '19', '26'):
    p = {'13': D+'2026-11-13T1454Z/bodies/S26_assemblymag.derived.json', '19': D+'2026-11-19T1417Z/bodies/S26_assemblymag.derived.json', '26': D+'2026-11-26T1414Z/bodies/S26_assemblymag.derived.json'}[d]
    j = json.load(open(p))
    print('Assembly', d, 'article_text_sha256:', j.get('extracted', {}).get('article_text_sha256', 'not recorded'))
