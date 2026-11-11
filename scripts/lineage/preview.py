#!/usr/bin/env python3
"""One offline review file with native anchor routes between the three levels."""
from pathlib import Path
import re,base64
ROOT=Path(__file__).resolve().parents[2];SITE=ROOT/'site/_site'
base=SITE/'map/knowledge-lineage'
html=(base/'index.html').read_text()
# Keep one site shell; append the two deeper views so their native fragments work.
parts=[]
for route in ['trails','evidence']:
 body=(base/route/'index.html').read_text();parts.append(re.search(r'<main id="main">([\s\S]*?)</main>',body).group(1))
html=html.replace('</main>','<hr class="preview-divider">'+('<hr class="preview-divider">'.join(parts))+'</main>')
html=re.sub(r'<script\b[^>]*>[\s\S]*?</script>','',html)
fontcss=(ROOT/'site/assets/fonts.css').read_text()
fontcss=re.sub(r'url\("([^\"]+)"\)',lambda m:'url("data:font/woff2;base64,'+base64.b64encode((ROOT/'site/assets'/m[1]).read_bytes()).decode()+'")',fontcss)
for name,css in [('fonts.css',fontcss),('site.css',(ROOT/'site/assets/site.css').read_text()),('lineage.css',(ROOT/'site/assets/lineage.css').read_text())]:html=html.replace(f'<link rel="stylesheet" href="/assets/{name}">',f'<style>{css}</style>')
html=re.sub(r'<link rel="(?:manifest|icon|apple-touch-icon|alternate)"[^>]*>','',html)
for image in ['finding.svg','history-mobile.svg','history-wide.svg']:
 data='data:image/svg+xml;base64,'+base64.b64encode((ROOT/'notes/knowledge-lineage'/image).read_bytes()).decode()
 html=html.replace(f'src="/notes/knowledge-lineage/{image}"',f'src="{data}"')
branch='https://github.com/JKershaw/lighthouse/blob/pilot/knowledge-lineage/'
def target(m):
 route=m[1]
 for suffix,id in [('trails/','trails-page'),('evidence/','evidence-page'),('','overview-page')]:
  start='/map/knowledge-lineage/'+suffix
  if route==start:return f'href="#{id}"'
  if route.startswith(start+'#'):return 'href="'+route[len(start):]+'"'
 if route.startswith('/notes/knowledge-lineage/'):
  name=route[len('/notes/knowledge-lineage/'):].rstrip('/');return 'href="'+branch+'notes/knowledge-lineage/'+(name if '.' in name else name+'.md')+'"'
 if route in ['/map/knowledge-lineage/data.json','/map/knowledge-lineage/overview.json']:return 'href="'+branch+'notes/knowledge-lineage/'+('graph.json' if route.endswith('data.json') else 'overview.json')+'"'
 return 'href="https://lighthouse.harbour.cat'+route+'"'
html=re.sub(r'href="(/[^\"]*)"',target,html)
licenses='\n'.join((ROOT/'site/assets/fonts'/n).read_text() for n in ['source-sans-3-LICENSE.md','source-serif-4-LICENSE.md'])
html=html.replace('</head>','<!-- Embedded font licences:\n'+licenses.replace('--','- -')+'\n--><style>.lineage-page {max-width:760px;margin-inline:auto}.preview-divider {margin:4rem 0;border:0;border-top:1px solid var(--rule)}</style></head>')
html=re.sub(r'at commit <a href="https://github.com/JKershaw/lighthouse/commit/[0-9a-f]+">[0-9a-f]+</a>', 'on <a href="https://github.com/JKershaw/lighthouse/tree/pilot/knowledge-lineage">the working branch</a>', html)
html='\n'.join(line.rstrip() for line in html.splitlines())+'\n'
(ROOT/'notes/knowledge-lineage/preview.html').write_text(html)
assert not re.search(r'(?:src|href)="/',html);assert '<script' not in html
print('Packed overview, trails and evidence into one self-contained preview.')
