"""R-0174: repeat the piece's word search of the posted final document (S44, CRP.1/Rev.3).
Run: pdftotext studies/LH050/data/2026-11-27T1415Z/bodies/S44_crp1_rev3.pdf - | python3 -I notes/R-0174-lh050-reader-evidence/word_search.py"""
import sys, re, hashlib
raw = sys.stdin.read()
# join words broken by a hyphen at a line end, then collapse whitespace
t = re.sub(r'-\s*\n\s*', '-', raw)
t = re.sub(r'\s+', ' ', t)
print('chars', len(t))
for term in ['human control', 'negotiat', 'legally binding', 'binding', 'human judgement', 'human judgment',
             'meaningful', 'control', 'human', 'prohibit', 'protocol']:
    hits = [m.start() for m in re.finditer(re.escape(term), t, flags=re.I)]
    print(f'{term!r}: {len(hits)}')
    if term in ('negotiat', 'binding', 'human', 'control'):
        for h in hits[:12]:
            print('    ...', t[max(0, h-90):h+90].replace('\n', ' '), '...')
