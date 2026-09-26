#!/usr/bin/env python3
"""LH007: installed.svg, one row per image repository with an installed mcp read, each image a mark at
its build time in days since mcp 1.28.0 (filled: holds 1.28.x; hollow: an older version; colour: the
image's install class), the project's first pin or lock of 1.28.x (diamond), and the advisory that
1.28.1 fixed. From data/image_timeline.csv and data/pin_movers.csv. No network access."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, STUDY

X0, X1 = -32, 44
ADV = 29.94
W, L, R, T = 900, 190, 24, 96
ROWH = 30
CLS = {'open range': 's1', 'lockfile': 's2', 'exact pin': 's3'}
rows = [r for r in read_csv('image_timeline.csv') if r['mcp_installed'] and r['days_since_release'] != '']
movers = {m['image']: float(m['days_after_release']) for m in read_csv('pin_movers.csv')}
by = collections.defaultdict(list)
for r in rows:
    d = float(r['days_since_release'])
    by[r['image']].append((d, r))
main = lambda img: collections.Counter(r['install_class'] for _, r in by[img]).most_common(1)[0][0]
order = sorted([i for i in by if any(X0 <= d <= X1 for d, _ in by[i])],
               key=lambda i: (list(CLS).index(main(i)) if main(i) in CLS else 9, i))
B = T + ROWH * len(order)
H = B + 108
x = lambda d: L + (d - X0) / (X1 - X0) * (W - L - R)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     'aria-labelledby="t d">',
     '<title id="t">Which images held mcp 1.28 in the weeks around its release, by how they install</title>',
     '<desc id="d">One row per image repository in the LH007 sample with an installed mcp read. Images that resolve an open '
     'range held the new release from 2.6 days after it; images built from a lockfile or exact pin held it only after the '
     'project moved the pin, which for six projects came within 28 hours after a security advisory on 16 July.</desc>',
     '<style>',
     'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e4e3df; --win:#f0efec; '
     '--s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; }',
     '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781; '
     '--grid:#383835; --win:#2a2a28; --s1:#3987e5; --s2:#d95926; --s3:#199e70; } }',
     'text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink); }',
     '.t2 { fill: var(--ink2); } .mu { fill: var(--muted); }',
     '</style>',
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     f'<text x="16" y="28" font-size="17" font-weight="600">Open-range images took mcp 1.28 within days; pinned ones waited for the pin</text>',
     f'<text x="16" y="50" font-size="13" class="t2">Build time of each image read, in days since mcp 1.28.0 (16 June 2026). Filled: holds 1.28.x. Hollow: older.</text>']
o.append(f'<rect x="{x(-28):.1f}" y="{T-14}" width="{x(28)-x(-28):.1f}" height="{B-T+14}" fill="var(--win)"/>')
for d in range(-28, 43, 7):
    o.append(f'<line x1="{x(d):.1f}" y1="{T-14}" x2="{x(d):.1f}" y2="{B}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<text x="{x(d):.1f}" y="{B+18}" font-size="12" text-anchor="middle" class="t2">{d:+d}</text>')
o.append(f'<line x1="{x(0):.1f}" y1="{T-22}" x2="{x(0):.1f}" y2="{B}" stroke="var(--ink)" stroke-width="1.5"/>')
o.append(f'<text x="{x(0)+4:.1f}" y="{T-26}" font-size="12">release</text>')
o.append(f'<line x1="{x(ADV):.1f}" y1="{T-22}" x2="{x(ADV):.1f}" y2="{B}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 3"/>')
o.append(f'<text x="{x(ADV)+4:.1f}" y="{T-26}" font-size="12">advisory, fixed in 1.28.1</text>')
o.append(f'<text x="{x(-28)+4:.1f}" y="{T-2}" font-size="11" class="mu">four weeks either side</text>')
for k, img in enumerate(order):
    cy = T + ROWH * k + ROWH // 2
    o.append(f'<text x="{L-10}" y="{cy+4}" font-size="13" text-anchor="end">{img.split("/")[-1] if "python-runtime" not in img else "mcp-mesh runtime"}</text>')
    o.append(f'<line x1="{L}" y1="{cy}" x2="{W-R}" y2="{cy}" stroke="var(--grid)" stroke-width="1"/>')
    if img in movers and X0 <= movers[img] <= X1:
        mx = x(movers[img])
        o.append(f'<path d="M{mx:.1f},{cy-8} l8,8 l-8,8 l-8,-8 z" fill="none" stroke="var(--ink)" stroke-width="1.5"/>')
    for d, r in sorted(by[img], key=lambda t: t[0]):
        if not X0 <= d <= X1:
            continue
        c = CLS.get(r['install_class'], 'muted')
        if r['holds_new'] == 'yes':
            o.append(f'<circle cx="{x(d):.1f}" cy="{cy}" r="6" fill="var(--{c})" stroke="var(--bg)" stroke-width="1.5"/>')
        else:
            o.append(f'<circle cx="{x(d):.1f}" cy="{cy}" r="5" fill="var(--bg)" stroke="var(--{c})" stroke-width="2.5"/>')
ly = B + 44
o.append(f'<text x="{L}" y="{ly+4}" font-size="12" class="t2">install class:</text>')
lx = L + 90
for name, c in CLS.items():
    o.append(f'<circle cx="{lx}" cy="{ly}" r="6" fill="var(--{c})"/><text x="{lx+11}" y="{ly+4}" font-size="12">{name}</text>')
    lx += 110
o.append(f'<path d="M{lx},{ly-8} l8,8 l-8,8 l-8,-8 z" fill="none" stroke="var(--ink)" stroke-width="1.5"/>'
         f'<text x="{lx+13}" y="{ly+4}" font-size="12">project first pins or locks 1.28.x</text>')
o.append(f'<text x="16" y="{H-28}" font-size="11" class="mu">Sample: {len(order)} image repositories of direct dependents of mcp (Open Source Insights), images built 32 days before</text>')
o.append(f'<text x="16" y="{H-12}" font-size="11" class="mu">to 44 days after the release. Registries, git and the advisory read 26 September 2026. Source: Lighthouse LH007.</text>')
o.append('</svg>')
open(os.path.join(STUDY, 'installed.svg'), 'w').write('\n'.join(o) + '\n')
print(len(order), 'rows;', sum(1 for i in order for d, _ in by[i] if X0 <= d <= X1), 'images drawn')
