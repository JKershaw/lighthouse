#!/usr/bin/env python3
"""LH013: the record's figure, from data/analysis/holds.csv (or $LH013_OUT/analysis): each project's older share O
in W0, W1 and W2 at its fixed reference release R0, with the brief's band of 5 points either side of W0.
Usage: python3 draw_figure.py <out.svg>"""
import csv, os, sys
STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(os.environ.get('LH013_OUT', os.path.join(STUDY, 'data')), 'analysis')
rows = sorted(csv.DictReader(open(os.path.join(A, 'holds.csv'))), key=lambda r: -float(r['O_W0']))
W, top, rh, left, right = 720, 92, 15, 150, 690
H = top + rh * len(rows) + 46
x = lambda v: left + (right - left) * v
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     'aria-label="Each project\'s share of downloads on versions older than its fixed reference release, in three weeks">',
     '<style>:root{--bg:#fcfcfb;--ink:#0b0b0b;--muted:#52514e;--grid:#e4e3df;--band:#ecebe7;--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a}'
     '@media (prefers-color-scheme: dark){:root{--bg:#1a1a19;--ink:#f0efec;--muted:#c3c2b7;--grid:#383835;--band:#2b2b29;--s1:#3987e5;--s2:#d95926;--s3:#199e70}}'
     'text{font-family:system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:var(--ink)}.m{fill:var(--muted);font-size:10px}.l{font-size:10.5px}</style>',
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     '<text x="16" y="20" font-size="13" font-weight="600">Share of downloads on older versions, three weeks running</text>',
     '<text x="16" y="36" class="m">Each row is one project; older means below its reference release R0, held fixed (the release of 21 August 2026 or earlier).</text>',
     '<text x="16" y="49" class="m">Grey band: within 5 points of 21 to 27 September, the brief\'s test. Projects whose dots leave the band are named in bold.</text>']
lg = [('W0, 21 to 27 Sep', 's1', 'c'), ('W1, 28 Sep to 4 Oct', 's2', 's'), ('W2, 5 to 11 Oct', 's3', 't')]


def mark(kind, cx, cy, col):
    if kind == 'c':
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="var(--{col})" stroke="var(--bg)" stroke-width="1.5"/>'
    if kind == 's':
        return f'<rect x="{cx - 3.6:.1f}" y="{cy - 3.6:.1f}" width="7.2" height="7.2" fill="var(--{col})" stroke="var(--bg)" stroke-width="1.5"/>'
    return f'<path d="M{cx:.1f},{cy - 4.6:.1f} L{cx + 4.4:.1f},{cy + 3.4:.1f} L{cx - 4.4:.1f},{cy + 3.4:.1f} Z" fill="var(--{col})" stroke="var(--bg)" stroke-width="1.5"/>'


for i, (name, col, k) in enumerate(lg):
    o.append(mark(k, 22 + 180 * i, 66, col) + f'<text x="{32 + 180 * i}" y="70" class="l">{name}</text>')
for t in range(0, 101, 20):
    o.append(f'<line x1="{x(t / 100):.1f}" x2="{x(t / 100):.1f}" y1="{top - 8}" y2="{top + rh * len(rows)}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<text x="{x(t / 100):.1f}" y="{top + rh * len(rows) + 14}" class="m" text-anchor="middle">{t}%</text>')
for i, r in enumerate(rows):
    cy = top + rh * i + rh / 2
    o0 = float(r['O_W0'])
    o.append(f'<rect x="{x(max(0, o0 - 0.05)):.1f}" y="{cy - 5.5:.1f}" width="{x(min(1, o0 + 0.05)) - x(max(0, o0 - 0.05)):.1f}" height="11" rx="2" fill="var(--band)"/>')
    bold = ' font-weight="700"' if r['O_holds'] == 'False' else ''
    o.append(f'<text x="{left - 8}" y="{cy + 3.5:.1f}" class="l" text-anchor="end"{bold}>{r["project"]}</text>')
    for (name, col, k), key in zip(lg, ('O_W0', 'O_W1', 'O_W2')):
        o.append(f'<g>{mark(k, x(float(r[key])), cy, col)}<title>{r["project"]}, {name}: {100 * float(r[key]):.1f} per cent</title></g>')
o.append(f'<text x="{(left + right) / 2}" y="{H - 12}" class="m" text-anchor="middle">Share of the week\'s downloads on versions below R0 (ClickPy, read 2 November 2026; W0 as LH012 read it)</text>')
o.append('</svg>')
open(sys.argv[1], 'w').write('\n'.join(o) + '\n')
