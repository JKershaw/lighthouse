#!/usr/bin/env python3
"""Static HTML render proofs only. This is not a browser or accessibility test.
Requires WeasyPrint and PyMuPDF; PYTHONPATH may point to a scratch install.
"""
import re
from pathlib import Path
import base64
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts"))
from chart_style import THEMES
from urllib.parse import urlparse
from weasyprint import HTML, CSS
from weasyprint.urls import URLFetcher
import fitz

ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'site/_site'
OUT=ROOT/'notes/knowledge-lineage/proofs'
OUT.mkdir(exist_ok=True)
html=(SITE/'map/knowledge-lineage/index.html').read_text()
# Do not make network requests while rendering retained local pages.
class LocalOnly(URLFetcher):
    def fetch(self, url, headers=None):
        parsed=urlparse(url)
        if parsed.scheme=='file' and not Path(parsed.path).resolve().is_relative_to(SITE):
            raise ValueError('Outside built site')
        return super().fetch(url,headers)
local_only=LocalOnly(allowed_protocols={'file','data'})
html=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',html)
html=re.sub(r'((?:href|src)=["\'])/([^"\']*)',lambda m:m[1]+(SITE/m[2]).as_uri(),html)
for width,theme in [(390,'light'),(390,'dark'),(1000,'light'),(1000,'dark')]:
    # Only retain the introduction and finding trail in proofs; exact built text and CSS.
    end=html.index('<section id="topic"')
    proof=html[:end]+'</article></main></body></html>'
    mobile=''' .lineage-choices {grid-template-columns:1fr !important} .lineage-choices a {min-height:0} .lineage-clocks {grid-template-columns:1fr} .lineage-card {padding:.95rem} .lineage-steps {padding-left:1rem} .lineage-step {padding-left:1rem} ''' if width==390 else ''
    dark=':root {--bg:#15191b;--ink:#e6e2d9;--muted:#aaa498;--rule:#2f3538;--accent:#8ec4d4;--tint:#1c2124;--essay:#e0a650}' if theme=='dark' else ''
    css=f'''@page {{size:{width}px 6500px; margin:0}} body {{background:var(--bg)}} .lineage-choices {{display:grid !important}} .lineage-step {{break-inside:auto}} {mobile} {dark}'''
    css += ' .lineage-page h1 {font-size:43px} body {color:var(--ink)} a {color:var(--accent)}'
    proof=proof.replace('</body>',f'<style>{css}</style></body>')
    # WeasyPrint's SVG renderer does not resolve the SVG's custom properties.
    # Resolve the same shared palette explicitly for this static proof only.
    svg=(ROOT/'notes/knowledge-lineage/finding.svg').read_text()
    for key,value in THEMES[theme].items():svg=svg.replace(f'var(--{key})',value)
    data='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    proof=proof.replace((SITE/'notes/knowledge-lineage/finding.svg').as_uri(),data)
    doc=HTML(string=proof,base_url=SITE.as_uri()+'/',url_fetcher=local_only).render()
    pdf=doc.write_pdf()
    rendered=fitz.open(stream=pdf,filetype='pdf')
    page=rendered[0]
    # Crop to the last text, so a long paper size does not leave empty background.
    bounds=page.get_text('blocks')
    bottom=min(page.rect.height,max(b[3] for b in bounds)+20)
    page.get_pixmap(matrix=fitz.Matrix(1.333333,1.333333),clip=fitz.Rect(0,0,page.rect.width,bottom)).save(OUT/f'finding-{width}-{theme}.png')
    # PDFs are intermediate only; the user-facing proofs are PNGs.
    print(f'{width}px {theme}: {len(doc.pages)} static proof page(s)')

# Render the related topic at phone width too, with the same actual template text.
for theme in ['light','dark']:
    topic=re.search(r'<section id="topic"[\s\S]*?</section>',html).group()
    proof=html[:html.index('<section id="finding"')]+topic+'</article></main></body></html>'
    dark=':root {--bg:#15191b;--ink:#e6e2d9;--muted:#aaa498;--rule:#2f3538;--accent:#8ec4d4;--tint:#1c2124;--essay:#e0a650}' if theme=='dark' else ''
    css=f'@page {{size:390px 6500px;margin:0}} body {{background:var(--bg);color:var(--ink)}} a {{color:var(--accent)}} .lineage-page h1 {{font-size:43px}} .lineage-choices {{display:grid;grid-template-columns:1fr}} .lineage-choices a {{min-height:0}} .lineage-clocks {{grid-template-columns:1fr}} .lineage-card {{padding:.95rem}} {dark}'
    proof=proof.replace('</body>',f'<style>{css}</style></body>')
    doc=HTML(string=proof,base_url=SITE.as_uri()+'/',url_fetcher=local_only).render()
    page=fitz.open(stream=doc.write_pdf(),filetype='pdf')[0]
    bottom=min(page.rect.height,max(b[3] for b in page.get_text('blocks'))+20)
    page.get_pixmap(matrix=fitz.Matrix(1.333333,1.333333),clip=fitz.Rect(0,0,page.rect.width,bottom)).save(OUT/f'topic-390-{theme}.png')
    print(f'390px {theme}: topic static proof')
