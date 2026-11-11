#!/usr/bin/env python3
"""Static closed-disclosure proofs. Not a browser, keyboard or human test.
Requires WeasyPrint70 and PyMuPDF. Original pilot proofs remain in git.
"""
import base64,re,sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from weasyprint import HTML
from weasyprint.urls import URLFetcher
import fitz
ROOT=Path(__file__).resolve().parents[2];SITE=ROOT/'site/_site';OUT=ROOT/'notes/knowledge-lineage/proofs'
sys.path.insert(0,str(ROOT/'scripts'))
from chart_style import THEMES
class LocalOnly(URLFetcher):
 def fetch(self,url,headers=None):
  p=urlparse(url)
  if p.scheme=='file' and not Path(p.path).resolve().is_relative_to(SITE):raise ValueError('Outside built site')
  return super().fetch(url,headers)
class ClosedDetails(HTMLParser):
 """Print engines do not close native details; model only their default visibility."""
 def __init__(self):super().__init__(convert_charrefs=False);self.out=[];self.stack=[];self.skipping=0
 def handle_starttag(self,t,attrs):
  if self.skipping:
   if t=='details':self.skipping+=1
   return
  if t=='details':self.stack.append('open' not in dict(attrs))
  self.out.append(self.get_starttag_text())
 def handle_endtag(self,t):
  if self.skipping:
   if t=='details':
    self.skipping-=1
    if not self.skipping:self.out.append('</details>');self.stack.pop()
   return
  self.out.append(f'</{t}>')
  if t=='summary' and self.stack and self.stack[-1]:self.skipping=1
  if t=='details' and self.stack:self.stack.pop()
 def handle_data(self,s):
  if not self.skipping:self.out.append(s)
 def handle_entityref(self,s):
  if not self.skipping:self.out.append('&'+s+';')
 def handle_charref(self,s):
  if not self.skipping:self.out.append('&#'+s+';')
 def handle_decl(self,s):self.out.append('<!'+s+'>')
fetcher=LocalOnly(allowed_protocols={'file','data'});OUT.mkdir(exist_ok=True)
for name,route,widths in [('overview','',[390,1100]),('trails','trails/',[390])]:
 raw=(SITE/'map/knowledge-lineage'/route/'index.html').read_text()
 raw=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',raw)
 parser=ClosedDetails();parser.feed(raw);raw=''.join(parser.out)
 raw=re.sub(r'((?:href|src)=["\'])/([^"\']*)',lambda m:m[1]+(SITE/m[2]).as_uri(),raw)
 for width in widths:
  for theme in ['light','dark']:
   proof=raw
   for image in ['finding.svg','history-mobile.svg','history-wide.svg']:
    svg=(ROOT/'notes/knowledge-lineage'/image).read_text()
    for key,value in THEMES[theme].items():svg=svg.replace(f'var(--{key})',value)
    data='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    proof=proof.replace((SITE/'notes/knowledge-lineage'/image).as_uri(),data)
   proof=re.sub(r'<svg\b[\s\S]*?</svg>',lambda m:__import__('functools').reduce(lambda text,kv:text.replace(f'var(--{kv[0]})',kv[1]),THEMES[theme].items(),m[0]),proof)
   mobile=''' .knowledge-territories {grid-template-columns:1fr} .knowledge-phone-drawing {display:block} .knowledge-wide-drawing {display:none} .knowledge-record-list {grid-template-columns:1fr} .knowledge-overview h1 {font-size:2.8rem} .lineage-choices {grid-template-columns:1fr;display:grid} .lineage-choices a {min-height:0} .lineage-clocks {grid-template-columns:1fr} ''' if width==390 else ''
   themeCss=':root {'+';'.join(f'--{key}:{val}' for key,val in THEMES[theme].items())+';--rule:'+THEMES[theme]['grid']+';--accent:'+THEMES[theme]['teal']+';--tint:'+('#1c2124' if theme=='dark' else '#f3efe6')+'}'
   css=f'@page {{size:{width}px 11000px;margin:0}} body {{background:var(--bg);color:var(--ink)}} a {{color:var(--accent)}} .lineage-page h1 {{font-size:43px}} .lineage-choices {{display:grid}} '+themeCss+mobile
   if name=='overview':css+='main {max-width:1180px}'
   proof=proof.replace('</body>',f'<style>{css}</style></body>')
   doc=HTML(string=proof,base_url=SITE.as_uri()+'/',url_fetcher=fetcher).render()
   pdf=fitz.open(stream=doc.write_pdf(),filetype='pdf');page=pdf[0]
   blocks=page.get_text('blocks');bottom=min(page.rect.height,max(b[3] for b in blocks)+20)
   page.get_pixmap(matrix=fitz.Matrix(4/3,4/3),clip=fitz.Rect(0,0,page.rect.width,bottom)).save(OUT/f'{name}-{width}-{theme}.png')
   print(f'{name} {width}px {theme}: {len(doc.pages)} static page(s), closed disclosures')
