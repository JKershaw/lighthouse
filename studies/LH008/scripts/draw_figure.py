#!/usr/bin/env python3
"""LH008: rates.svg, the rate at which kept repositories moved their pin or lock, in moves per 100
repository-days at risk, in windows measured from three reference times: the fixed release (fix
frames), the advisory (fix frames) and the comparison release (comparison frames). Each bar spans its
window on a shared days axis; its height is the rate. From data/hazard.csv. No network access.
Palette as LH007's figure (validated with the dataviz skill's validator, light and dark)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, STUDY

H_ = read_csv('hazard.csv')


def rate(prefix):
    return [(h, float(h['moves_per_100_repo_days'])) for h in H_ if h['window'].startswith(prefix)]


PANELS = [
    ('From the fixed release (fix frames, 102 repositories)', 's1',
     [((0, 2), 'release +0 to +2'), ((2, 7), 'release +2 to +7 days, or to the advisory'), ((7, 24), 'release +7 days to the advisory')]),
    ('From the advisory (the same 102 repositories)', 's2',
     [((-7, 0), 'advisory -7 to +0'), ((0, 2), 'advisory +0 to +2'), ((2, 7), 'advisory +2 to +7'), ((7, 30), 'advisory +7 to +30')]),
    ('From the comparison release, no advisory named it (91 repositories)', 's3',
     [((0, 2), 'release +0 to +2'), ((2, 7), 'release +2 to +7'), ((7, 30), 'release +7 to +30')]),
]
KIND = {0: 'fix', 1: 'fix', 2: 'comparison'}
W, L, R, T = 900, 70, 24, 84
PH, GAP = 120, 46
X0, X1, YMAX = -7, 30, 6
x = lambda d: L + (d - X0) / (X1 - X0) * (W - L - R)
Hh = T + len(PANELS) * (PH + GAP) + 66
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" width="{W}" height="{Hh}" role="img" aria-labelledby="t d">',
     '<title id="t">How fast pins moved after a fixed release, after its advisory, and after a release no advisory named</title>',
     '<desc id="d">Moves per 100 repository-days at risk, by window. In the two days after the fixed release the rate was 4.1, '
     'from day two to day seven, or to the advisory where it came first, 1.5; in the two days after the advisory 5.1 and in days two to seven after it 4.3, against 1.3 to 1.7 in the weeks '
     'between and after; after a comparison release no advisory named, 2.8 in the first two days and 0.6 from day seven to thirty. '
     'The values are in data/hazard.csv.</desc>',
     '<style>',
     'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e4e3df; '
     '--s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; }',
     '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781; '
     '--grid:#383835; --s1:#3987e5; --s2:#d95926; --s3:#199e70; } }',
     'text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink); }',
     '.t2 { fill: var(--ink2); } .mu { fill: var(--muted); }',
     '</style>',
     f'<rect width="{W}" height="{Hh}" fill="var(--bg)"/>',
     '<text x="16" y="28" font-size="17" font-weight="600">Pins moved faster after a fix and its advisory than after a release no advisory named</text>',
     '<text x="16" y="50" font-size="13" class="t2">Moves per 100 repository-days at risk, by window, in days from each reference time. Four libraries; pooled.</text>']
for i, (title, c, wins) in enumerate(PANELS):
    top = T + i * (PH + GAP)
    base = top + PH
    y = lambda v: base - v / YMAX * (PH - 18)
    o.append(f'<text x="{L}" y="{top+2}" font-size="13" font-weight="600">{title}</text>')
    for v in (0, 2, 4, 6):
        o.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{W-R}" y2="{y(v):.1f}" stroke="var(--grid)" stroke-width="1"/>')
        o.append(f'<text x="{L-8}" y="{y(v)+4:.1f}" font-size="11" text-anchor="end" class="t2">{v}</text>')
    o.append(f'<line x1="{x(0):.1f}" y1="{top+8}" x2="{x(0):.1f}" y2="{base}" stroke="var(--ink)" stroke-width="1.5"/>')
    for (a, b), prefix in wins:
        hs = [h for h in H_ if h['kind'] == KIND[i] and h['window'].startswith(prefix)]
        if not hs:
            continue
        h = hs[0]
        v = float(h['moves_per_100_repo_days'])
        x0, x1 = x(a) + 1, x(b) - 1
        o.append(f'<path d="M{x0:.1f},{base} V{y(v)+4:.1f} q0,-4 4,-4 H{x1-4:.1f} q4,0 4,4 V{base} Z" fill="var(--{c})">'
                 f'<title>{h["window"]}: {h["moves"]} moves in {h["repo_days_at_risk"]} repository-days, {v} per 100</title></path>')
        o.append(f'<text x="{(x0+x1)/2:.1f}" y="{y(v)-6:.1f}" font-size="12" text-anchor="middle">{v:.1f}</text>')
    for d in (-7, 0, 2, 7, 14, 21, 30):
        o.append(f'<text x="{x(d):.1f}" y="{base+15}" font-size="11" text-anchor="middle" class="t2">{d:+d}</text>')
    if i == 0:
        o.append(f'<text x="{W-R}" y="{top+30}" font-size="11" text-anchor="end" class="mu">+2 to +7 stops at the advisory where it came first (urllib3 +3.9, cryptography +5.9); from +7 to the advisory: pyjwt and starlette only</text>')
    if i == 1:
        o.append(f'<text x="{W-R}" y="{top+2}" font-size="11" text-anchor="end" class="mu">-7 to 0 includes the release days for urllib3 and cryptography</text>')
o.append(f'<text x="16" y="{Hh-44}" font-size="11" class="mu">Repositories of Open Source Insights dependents of urllib3, cryptography, pyjwt and starlette that pinned or locked the release</text>')
o.append(f'<text x="16" y="{Hh-28}" font-size="11" class="mu">before; a move is the first default-branch commit taking the pin to the fix (or comparison release) or later. Git, PyPI and OSV</text>')
o.append(f'<text x="16" y="{Hh-12}" font-size="11" class="mu">read 27 September 2026. Source: Lighthouse LH008, data/hazard.csv.</text>')
o.append('</svg>')
open(os.path.join(STUDY, 'rates.svg'), 'w').write('\n'.join(o) + '\n')
print('written')
