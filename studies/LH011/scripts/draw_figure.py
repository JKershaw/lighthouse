#!/usr/bin/env python3
"""LH011: draw uptake.svg from data/analysis/ (offline). One row per project with a qualifying
release: a thin line spans its releases' day-1 at-or-newer shares, the mark is their median; a
blue circle means most of its releases reached half within two days, an orange square that they did
not. Adapted from studies/LH005/scripts/draw_figure.py: what changed is the whole drawing (a dot
plot of projects in place of one release's daily shares); like it, plain SVG with no library.
Usage: python3 draw_figure.py [out.svg]   (default: studies/LH011/uptake.svg)"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
A = os.environ.get('LH011_OUT', os.path.join(STUDY, 'data', 'analysis'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STUDY, 'uptake.svg')
proj = [r for r in csv.DictReader(open(os.path.join(A, 'project_outcomes.csv'))) if r['releases'] != '0']
rel = list(csv.DictReader(open(os.path.join(A, 'release_outcomes.csv'))))
for p in proj:
    s = [float(r['share_day1']) for r in rel if r['project'] == p['project'] and r['share_day1']]
    p['lo'], p['hi'], p['med'] = min(s), max(s), float(p['median_day1_share'])
proj.sort(key=lambda p: (p['med'], p['project']))

W, L, R, T, RH = 760, 190, 30, 58, 17
H = T + RH * len(proj) + 58
x = lambda v: L + v * (W - L - R)
e = []
e.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
         'aria-label="Median share of each project\'s downloads at a new release or newer on the day after release">')
e.append('<style>svg{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--grid:#e4e3de;--a:#2a78d6;--b:#eb6834}'
         '@media (prefers-color-scheme: dark){svg{--bg:#1a1a19;--ink:#ffffff;--ink2:#c3c2b7;--grid:#3a3936;--a:#3987e5;--b:#d95926}}'
         'text{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:var(--ink2)}.t{fill:var(--ink);font-weight:600}</style>')
e.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
e.append(f'<text class="t" x="{L}" y="22">Day-1 share of downloads at the new release or newer, by project</text>')
# legend
e.append(f'<circle cx="{L + 6}" cy="40" r="5" fill="var(--a)"/><text x="{L + 16}" y="44">most releases reached half within two days</text>')
e.append(f'<rect x="{L + 300}" y="35" width="10" height="10" rx="2" fill="var(--b)"/><text x="{L + 316}" y="44">most did not</text>')
for v in (0, 0.25, 0.5, 0.75, 1):
    dash = ' stroke-dasharray="4 3"' if v == 0.5 else ''
    col = 'var(--ink2)' if v == 0.5 else 'var(--grid)'
    e.append(f'<line x1="{x(v):.1f}" y1="{T - 6}" x2="{x(v):.1f}" y2="{T + RH * len(proj)}" stroke="{col}" stroke-width="1"{dash}/>')
    e.append(f'<text x="{x(v):.1f}" y="{T + RH * len(proj) + 16}" text-anchor="middle">{int(v * 100)}%</text>')
for i, p in enumerate(proj):
    y = T + RH * i + RH / 2
    ok = p['most_reached'] == 'yes'
    col = 'var(--a)' if ok else 'var(--b)'
    e.append(f'<text x="{L - 10}" y="{y + 4:.1f}" text-anchor="end">{p["project"]} ({p["releases"]})</text>')
    e.append(f'<line x1="{x(p["lo"]):.1f}" y1="{y:.1f}" x2="{x(p["hi"]):.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="2" stroke-linecap="round" opacity="0.55"/>')
    tip = (f'<title>{p["project"]}: {p["releases"]} releases, {p["reached"]} reached half within two days; '
           f'median day-1 share {p["med"] * 100:.1f}% (range {p["lo"] * 100:.1f} to {p["hi"] * 100:.1f})</title>')
    if ok:
        e.append(f'<circle cx="{x(p["med"]):.1f}" cy="{y:.1f}" r="5" fill="{col}" stroke="var(--bg)" stroke-width="2">{tip}</circle>')
    else:
        e.append(f'<rect x="{x(p["med"]) - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" rx="2" fill="{col}" stroke="var(--bg)" stroke-width="2">{tip}</rect>')
e.append(f'<text x="{L}" y="{H - 26}">Mark: median over the project\'s releases; line: their range; releases in brackets.</text>')
e.append(f'<text x="{L}" y="{H - 10}">ClickPy by-version table, April to August 2026 releases, read 28 September 2026.</text>')
e.append('</svg>')
open(out, 'w').write('\n'.join(e) + '\n')
print('wrote', out)
