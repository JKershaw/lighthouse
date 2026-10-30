#!/usr/bin/env python3
"""Evidence review R-0043: find every quotation in the version 1.3 additions and report which
retained source text holds it verbatim (after normalising curly quotes and whitespace).
Run from the repository root: python3 -I notes/php-leads-2026-10-30/review/quotes.py"""
import json, re, subprocess
from pathlib import Path

R = Path('notes/php-leads-2026-10-30/review')
def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return re.sub(r'\s+', ' ', s)
sources = {p.stem: norm(p.read_text()) for p in R.glob('*.txt') if p.stem != 'hashes'}
feed = json.loads(Path('studies/LH031/data/read-2026-10-30T0634Z/feed.raw').read_bytes())
sources['cisa-feed'] = norm(json.dumps(feed, ensure_ascii=False))
sources['cisa-webfetch(model rendering)'] = norm(Path('studies/LH031/data/criteria-2026-10-30T1148Z/webfetch.md').read_text())
diff = subprocess.run(['git', 'diff', '-U0', 'f5b6315', '--', 'articles', 'README.md', 'investigations', 'programme.md'],
                      capture_output=True, text=True).stdout
added = '\n'.join(l[1:] for l in diff.splitlines() if l.startswith('+') and not l.startswith('+++'))
for q in sorted(set(re.findall(r'"([^"]{3,})"', norm(added)))):
    hits = [k for k, v in sources.items() if q in v]
    print(('OK   ' if hits else 'MISS ') + repr(q) + '  ' + ', '.join(hits))
