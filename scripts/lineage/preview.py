#!/usr/bin/env python3
"""Pack the built pilot as one inspectable HTML file. No JavaScript or network assets."""
from pathlib import Path
import re
import base64
ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'site/_site'
html=(SITE/'map/knowledge-lineage/index.html').read_text()
html=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',html)
fontcss=(ROOT/'site/assets/fonts.css').read_text()
fontcss=re.sub(r'url\("([^\"]+)"\)',lambda m:'url("data:font/woff2;base64,'+base64.b64encode((ROOT/'site/assets'/m[1]).read_bytes()).decode()+'")',fontcss)
for filename,content in [('fonts.css',fontcss),('site.css',(ROOT/'site/assets/site.css').read_text()),('lineage.css',(ROOT/'site/assets/lineage.css').read_text())]:
    html=html.replace(f'<link rel="stylesheet" href="/assets/{filename}">',f'<style>{content}</style>')
html=re.sub(r'<link rel="(?:manifest|icon|apple-touch-icon|alternate)"[^>]*>','',html)
svg=(ROOT/'notes/knowledge-lineage/finding.svg').read_bytes()
html=html.replace('src="/notes/knowledge-lineage/finding.svg"','src="data:image/svg+xml;base64,'+base64.b64encode(svg).decode()+'"')
branch='https://github.com/JKershaw/lighthouse/blob/pilot/knowledge-lineage/'
def target(m):
    route=m[1]
    if route.startswith('/notes/knowledge-lineage/'):
        name=route[len('/notes/knowledge-lineage/'):].rstrip('/')
        return 'href="'+branch+'notes/knowledge-lineage/'+(name if '.' in name else name+'.md')+'"'
    if route=='/map/knowledge-lineage/data.json':return 'href="'+branch+'notes/knowledge-lineage/graph.json"'
    return 'href="https://lighthouse.harbour.cat'+route+'"'
html=re.sub(r'href="(/[^\"]*)"',target,html)
html=html.replace('</head>','<!-- Embedded fonts retain their SIL Open Font Licenses in the repository at site/assets/fonts/. -->\n</head>')
(ROOT/'notes/knowledge-lineage/preview.html').write_text(html)
assert not re.search(r'(?:src|href)="/',html)
assert '<script' not in html
print('Wrote self-contained preview with evidence links; no network-loaded assets.')
