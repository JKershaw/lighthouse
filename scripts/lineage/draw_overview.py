#!/usr/bin/env python3
"""Two readable layouts of the same selected, evidence-backed inquiry history."""
from pathlib import Path
from html import escape
import json,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from chart_style import svg_open
j=json.loads((ROOT/'notes/knowledge-lineage/overview.json').read_text())['history']
nodes={n['id']:n for n in j['nodes']}
for mobile in [False,True]:
 width,height=(360,1210) if mobile else (1040,610)
 pos={id:(18,18+i*145) for i,id in enumerate(nodes)} if mobile else {'projects':(15,80),'downloads':(275,80),'images':(535,80),'pace':(795,80),'advisory':(535,300),'four':(275,300),'notes':(15,300),'open':(15,510)}
 w,h=(288,112) if mobile else (230,88)
 title='How the software-update inquiry developed'
 desc='Eight selected readings. Projects led to downloads and images, then an advisory hypothesis. Wider samples revised that explanation and left the release-note question unsettled. A branch from downloads tested the two-day pattern in more libraries. Each box links to the current article; the HTML list supplies summaries and evidence. Arrows follow documented steps, not measured causes.'
 parts=[svg_open(width,height,title,desc),f'<rect width="{width}" height="{height}" fill="var(--bg)"/>','<defs><marker id="next" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="var(--muted)"/></marker></defs>']
 def line(d,dashed=False):parts.append(f'<path d="{d}" stroke="var(--muted)" stroke-width="1.8" fill="none" marker-end="url(#next)"'+(' stroke-dasharray="4 4"' if dashed else '')+'/>')
 if mobile:
  for a,b in zip(list(nodes)[:-1],list(nodes)[1:]):
   x,y=pos[a];xb,yb=pos[b];line(f'M{x+w/2} {y+h} V{yb-3}')
  x,y=pos['downloads'];xb,yb=pos['pace'];line(f'M{x+w} {y+h/2} H340 V{yb+h/2} H{xb+w+3}',True)
  parts.append('<text x="18" y="1190" class="ann">Dotted link: the earlier download question.</text>')
 else:
  line('M245 124 H272');line('M505 124 H532');line('M650 168 V297');line('M535 344 H508');line('M275 344 H248');line('M130 388 V507')
  line('M390 80 V20 H910 V77',True)
  line('M245 554 H1032 V210 H910 V171',True)
  parts.append('<text x="650" y="15" text-anchor="middle" class="ann">Test the download pattern more widely</text>')
  parts.append('<text x="666" y="235" class="sec">What moves a pin?</text>')
  parts.append('<text x="650" y="580" class="ann">A later direction change returns to downloads</text>')
 for id,n in nodes.items():
  x,y=pos[id];label=n['status'];font=14 if mobile else 15
  parts.append(f'<a href="https://lighthouse.harbour.cat{escape(n["url"],quote=True)}" aria-label="{escape(n["title"],quote=True)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="var(--bg)" stroke="var(--muted)" stroke-width="1.5"/>')
  for i,t in enumerate(n['lines']):parts.append(f'<text x="{x+12}" y="{y+27+i*21}" font-size="{font}" font-weight="600">{escape(t)}</text>')
  parts.append(f'<text x="{x+12}" y="{y+h-14}" class="ann">{escape(label)}</text></a>')
 parts.append('</svg>')
 markup='\n'.join(parts)+'\n'
 prefix='history-phone' if mobile else 'history-wide'
 markup=markup.replace('chart-title',prefix+'-title').replace('chart-desc',prefix+'-desc').replace('id="next"','id="'+prefix+'-next"').replace('url(#next)','url(#'+prefix+'-next)')
 (ROOT/'notes/knowledge-lineage'/('history-mobile.svg' if mobile else 'history-wide.svg')).write_text(markup)
