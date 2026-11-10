#!/usr/bin/env python3
"""One small directed view, derived from the pilot's finding edges."""
import json
from pathlib import Path
from html import escape
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from chart_style import svg_open
j=json.loads((ROOT/'notes/knowledge-lineage/graph.json').read_text())
t=j['trails'][0]
byid={s['id']:s for s in t['steps']}
parts=[svg_open(360,478,'How a claim changed after review','Four directly linked records. The earlier essay cites METR’s tentative account, shown by a dotted arrow pointing upwards. A later review challenges the earlier essay, and the corrected claim revises it, with solid arrows pointing back to the earlier wording. These are evidence relationships, not a causal or time scale.')]
parts.append('''<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="var(--muted)"/></marker></defs>
<rect width="360" height="478" fill="var(--bg)"/>
<g fill="none" stroke="var(--muted)" stroke-width="1.7" marker-end="url(#arrow)">
<path d="M180 174 L180 88" stroke-dasharray="3 4"/>
<path d="M90 353 L122 247"/>
<path d="M270 353 L238 247"/>
</g>
<text x="191" y="125" class="nm">cites</text><text x="191" y="143" class="ann">Reported</text>
<text x="12" y="294" class="nm">challenges</text><text x="12" y="312" class="ann">Checked</text>
<text x="277" y="294" class="nm">revises</text><text x="277" y="312" class="ann">Checked</text>''')
def box(id,x,y,w,lines,kind):
 s=byid[id]
 # SVG links go straight to retained passages and work when opened separately.
 parts.append(f'<a href="{escape(s["evidence"]["url"],quote=True)}" aria-label="{escape(s["title"],quote=True)}: exact retained passage"><rect x="{x}" y="{y}" width="{w}" height="72" rx="2" fill="var(--bg)" stroke="var(--muted)" stroke-width="1.4"/>')
 parts.append(f'<text x="{x+10}" y="{y+18}" class="ann">{escape(kind)}</text>')
 for n,line in enumerate(lines):parts.append(f'<text x="{x+10}" y="{y+39+n*18}" font-size="14" font-weight="600">{escape(line)}</text>')
 parts.append('</a>')
box('finding-source',30,15,300,['A tentative account of motive'],'Source account')
box('finding-prior',30,175,300,['Earlier wording went further'],'Essay, before correction')
box('finding-review',10,354,160,['Wording','challenged'],'Later review')
box('finding-corrected',190,354,160,['Uncertainty','restored'],'Corrected claim')
parts.append('<text x="12" y="454" class="ann">8 November records, selected retrospectively.</text><text x="12" y="472" class="ann">Arrows name relationships, not measured causes.</text></svg>')
(ROOT/'notes/knowledge-lineage/finding.svg').write_text('\n'.join(parts)+'\n')
