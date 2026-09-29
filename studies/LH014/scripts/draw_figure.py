#!/usr/bin/env python3
"""LH014: draw uptake.svg from data/analysis/ and LH011's retained analysis (offline). Top panel: for
the top fifty (LH011's 37 projects with a release) and the two bands, the share of projects whose
releases mostly reached half of downloads within two days, with its 95 per cent interval and the
brief's one-half and three-quarter lines. Bottom panel: each project's median day-1 at-or-newer share,
a blue circle where most of its releases reached half within two days and an orange square where they
did not, stacked where values are close. Adapted from studies/LH011/scripts/draw_figure.py: what
changed is the layout (three groups in two panels in place of one row per project); the colour
tokens, marks and plain SVG are LH011's.
Usage: python3 draw_figure.py [out.svg]   (default: studies/LH014/uptake.svg)"""
import csv, os, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(STUDY))
A = os.environ.get('LH014_OUT', os.path.join(STUDY, 'data', 'analysis'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STUDY, 'uptake.svg')
rd = lambda p: list(csv.DictReader(open(p)))
summ = {(r['band'], r['figure']): r['value'] for r in rd(os.path.join(A, 'summary.csv'))}
lh011 = [r for r in rd(os.path.join(ROOT, 'studies', 'LH011', 'data', 'analysis', 'project_outcomes.csv')) if r['releases'] != '0']
lh011s = {r['figure']: r['value'] for r in rd(os.path.join(ROOT, 'studies', 'LH011', 'data', 'analysis', 'summary.csv'))}
mine = rd(os.path.join(A, 'project_outcomes.csv'))
groups = [('Top fifty', '37 released (every project)',
           [(r['project'], float(r['median_day1_share']), r['most_reached'] == 'yes') for r in lh011],
           (int(lh011s['projects where most releases reached half within two days']), int(lh011s['projects with a known outcome']),
            float(lh011s['share of projects']), float(lh011s['share of projects, 95% interval low']), float(lh011s['share of projects, 95% interval high'])))]
for b, name, sub in (('A', 'Positions 51 to 500', '80 drawn, 52 released'), ('B', 'Positions 501 to 5,000', '80 drawn, 35 released')):
    g = lambda f: summ[(b, f)]
    groups.append((name, sub, [(r['project'], float(r['median_day1_share']), r['most_reached'] == 'yes')
                               for r in mine if r['band'] == b and r['median_day1_share'] != ''],
                   (int(g('primary: projects whose releases mostly reached half within two days')), int(g('primary: projects with a known outcome')),
                    float(g('primary: share')), float(g('primary: 95% interval low')), float(g('primary: 95% interval high')))))

W, L, R = 720, 205, 80
x = lambda v: L + v * (W - L - R)
e = []
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;')
# bottom panel geometry: symmetric stacks in bins of 2.5 points
stacks = []
for _, _, pts, _ in groups:
    bins, pos = defaultdict(int), []
    for name, v, ok in sorted(pts, key=lambda t: t[1]):
        k = min(int(v * 40), 39)
        i = bins[k]
        bins[k] += 1
        pos.append((name, v, ok, (i + 1) // 2 * (1 if i % 2 else -1)))
    stacks.append((pos, max(bins.values())))
T1, RH1 = 70, 34
T2 = T1 + RH1 * 3 + 64
heights = [max(40, (m // 2 + 1) * 11 * 2) for _, m in stacks]
H = T2 + sum(heights) + 70
e.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         'aria-label="Share of projects whose new releases mostly reached half of downloads within two days, for the top fifty '
         'Python projects and two bands below them, and each project\'s median day-1 share">')
e.append('<style>svg{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--grid:#e4e3de;--a:#2a78d6;--b:#eb6834}'
         '@media (prefers-color-scheme: dark){svg{--bg:#1a1a19;--ink:#ffffff;--ink2:#c3c2b7;--grid:#3a3936;--a:#3987e5;--b:#d95926}}'
         'text{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:var(--ink2)}.t{fill:var(--ink);font-weight:600}'
         '.s{font-size:11px}</style>')
e.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
e.append(f'<text class="t" x="16" y="24">Below the top fifty, fewer projects&#8217; new releases reach half of downloads within two days</text>')
e.append(f'<text x="16" y="{T1 - 22}">Share of projects whose releases mostly reached half of downloads on day 1 or 2, with 95% interval</text>')
for v, lab in ((0.5, 'one half'), (0.75, 'three quarters')):
    e.append(f'<line x1="{x(v):.1f}" y1="{T1 - 8}" x2="{x(v):.1f}" y2="{T1 + RH1 * 3 - 8}" stroke="var(--ink2)" stroke-width="1" stroke-dasharray="4 3"/>')
    e.append(f'<text class="s" x="{x(v):.1f}" y="{T1 + RH1 * 3 + 6}" text-anchor="middle">{lab}</text>')
for v in (0, 0.25, 1):
    e.append(f'<line x1="{x(v):.1f}" y1="{T1 - 8}" x2="{x(v):.1f}" y2="{T1 + RH1 * 3 - 8}" stroke="var(--grid)" stroke-width="1"/>')
for i, (name, sub, pts, (k, n, s, lo, hi)) in enumerate(groups):
    y = T1 + RH1 * i + 8
    e.append(f'<text class="t" x="{L - 12}" y="{y}" text-anchor="end">{name}</text>')
    e.append(f'<text class="s" x="{L - 12}" y="{y + 14}" text-anchor="end">{sub}</text>')
    e.append(f'<line x1="{x(lo):.1f}" y1="{y + 2}" x2="{x(hi):.1f}" y2="{y + 2}" stroke="var(--ink)" stroke-width="2" stroke-linecap="round"/>')
    e.append(f'<circle cx="{x(s):.1f}" cy="{y + 2}" r="5.5" fill="var(--ink)" stroke="var(--bg)" stroke-width="2">'
             f'<title>{name}: {k} of {n} projects ({s * 100:.1f}%; interval {lo * 100:.1f} to {hi * 100:.1f})</title></circle>')
    e.append(f'<text x="{x(1) + 10:.1f}" y="{y + 6}">{k} of {n}</text>')
e.append(f'<text x="16" y="{T2 - 26}">Each project\'s median day-1 share of downloads at the new release or newer</text>')
e.append(f'<circle cx="22" cy="{T2 - 8}" r="5" fill="var(--a)"/><text class="s" x="32" y="{T2 - 4}">most releases reached half within two days</text>')
e.append(f'<rect x="292" y="{T2 - 13}" width="10" height="10" rx="2" fill="var(--b)"/><text class="s" x="308" y="{T2 - 4}">most did not</text>')
y0 = T2 + 6
bottom = y0 + sum(heights)
for v in (0, 0.25, 0.5, 0.75, 1):
    dash = ' stroke-dasharray="4 3"' if v == 0.5 else ''
    e.append(f'<line x1="{x(v):.1f}" y1="{y0}" x2="{x(v):.1f}" y2="{bottom}" stroke="{"var(--ink2)" if v == 0.5 else "var(--grid)"}" stroke-width="1"{dash}/>')
    e.append(f'<text x="{x(v):.1f}" y="{bottom + 16}" text-anchor="middle">{int(v * 100)}%</text>')
for (name, sub, pts, _), (pos, m), h in zip(groups, stacks, heights):
    cy = y0 + h / 2
    e.append(f'<text class="t" x="{L - 12}" y="{cy + 4:.1f}" text-anchor="end">{name}</text>')
    for pname, v, ok, off in pos:
        yy = cy + off * 11
        col = 'var(--a)' if ok else 'var(--b)'
        tip = f'<title>{esc(pname)}: median day-1 share {v * 100:.1f}%</title>'
        if ok:
            e.append(f'<circle cx="{x(v):.1f}" cy="{yy:.1f}" r="4.5" fill="{col}" stroke="var(--bg)" stroke-width="1.5">{tip}</circle>')
        else:
            e.append(f'<rect x="{x(v) - 4.5:.1f}" y="{yy - 4.5:.1f}" width="9" height="9" rx="2" fill="{col}" stroke="var(--bg)" stroke-width="1.5">{tip}</rect>')
    y0 += h
e.append(f'<text class="s" x="16" y="{H - 30}">Releases that became the newest version, April to August 2026; ClickPy downloads by version to 27 September 2026.</text>')
e.append(f'<text class="s" x="16" y="{H - 14}">Top fifty read on 28 September 2026; the bands, 80 projects drawn at random from each, on 29 September.</text>')
e.append('</svg>')
open(out, 'w').write('\n'.join(e) + '\n')
print('wrote', out)
