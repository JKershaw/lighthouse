from pathlib import Path
import re, json
import tinycss2, fitz
from weasyprint import HTML,URLFetcher
default_url_fetcher=URLFetcher()
r=Path(__file__).resolve().parents[2];out=r.parent/'lighthouse-publish-qa';out.mkdir(exist_ok=True)
site=r/'site/_site';h=(site/'essays/it-was-only-a-test/index.html').read_text()
css=(r/'site/assets/fonts.css').read_text().replace('url("fonts/','url("'+(site/'assets/fonts').as_uri()+'/')+'\n'+(r/'site/assets/site.css').read_text()
def flatten(s,width,dark):
 result=[]
 for rule in tinycss2.parse_stylesheet(s,skip_comments=True,skip_whitespace=True):
  if rule.type=='at-rule' and rule.lower_at_keyword=='media':
   q=tinycss2.serialize(rule.prelude);ok='print' not in q
   for op,num in re.findall(r'(min|max)-width:\s*([0-9]+)px',q):ok &= width>=int(num) if op=='min' else width<=int(num)
   if 'prefers-color-scheme' in q:ok &= ('dark' in q)==dark
   if ok: result.append(flatten(tinycss2.serialize(rule.content),width,dark))
  else:result.append(tinycss2.serialize([rule]))
 return '\n'.join(result)
def fetch(url):
 if url.startswith('file:///') and not url.startswith(site.as_uri()):url=(site/url[len('file:///'):]).as_uri()
 return default_url_fetcher(url)
fetch._fail_on_errors=False
for width,dark in [(390,False),(390,True),(1280,False)]:
 name=f'{width}-'+('dark' if dark else 'light')
 doc=re.sub(r'<link[^>]+rel="stylesheet"[^>]*>','',h)
 # Match the native script's initial collapsed-note state at these widths.
 doc=doc.replace('class="side-note-toggle"','class="side-note-toggle"').replace('aria-expanded="true"','aria-expanded="false"')
 doc=re.sub(r'(class="side-note-toggle"[^>]*?) hidden>',r'\1>',doc)
 doc=doc.replace('class="side-note-body"','hidden class="side-note-body"')
 extra=f'@page{{size:{width}px 1100px;margin:0}}html,body{{width:{width}px}} .skip{{display:none}}'
 doc=doc.replace('</head>','<style>'+flatten(css,width,dark)+extra+'</style></head>')
 pdf=HTML(string=doc,base_url=str(site),url_fetcher=fetch,media_type='screen').write_pdf()
 d=fitz.open(stream=pdf,filetype='pdf')
 selected=[0]+[i for i,p in enumerate(d) if 'TWO ORGANISATIONS, DIFFERENT CLOCKS' in p.get_text() or 'A HYPOTHESIS TO TEST' in p.get_text()]
 for i in selected:d[i].get_pixmap(matrix=fitz.Matrix(1,1)).save(out/f'{name}-{i+1}.png')
 print(name,len(d),'pages',selected)
