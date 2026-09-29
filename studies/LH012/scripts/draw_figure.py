#!/usr/bin/env python3
"""LH012: the record's figure, from data/analysis/python.csv and week.csv (or $LH012_OUT). For each of the
37 projects, its downloads over 21 to 27 September 2026 split into: older versions fetched from a Python
that no version at or above R admits; older versions with no Python reported; older versions from a
Python that a newer version admits; and the rest (R or newer, and the few pre-releases and unlisted
versions). New for LH012. Usage: python3 draw_figure.py [output.svg]"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.environ.get('LH012_OUT') or os.path.join(os.path.dirname(HERE), 'data', 'analysis')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), 'older.svg')
py = {r['project']: r for r in csv.DictReader(open(os.path.join(A, 'python.csv')))}
wk = {r['project']: r for r in csv.DictReader(open(os.path.join(A, 'week.csv')))}
rows = []
for p, r in py.items():
    t = float(r['W2_total'])
    ex, nr, ad = (float(r[k]) / t for k in ('older_excluded_python', 'older_python_not_reported', 'older_admitted_python'))
    rows.append((p, ex, nr, ad, float(wk[p]['O'])))
rows.sort(key=lambda x: (-x[4], x[0]))
W, left, right, top, rh = 720, 128, 16, 80, 13
bw = W - left - right
H = top + rh * len(rows) + 40
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     'aria-label="Share of each project\'s downloads on older versions, by whether the Python excludes newer releases">',
     '<style>',
     ':root{--bg:#ffffff;--ink:#1f2328;--muted:#59636e;--ex:#b4462b;--nr:#c9b8a6;--ad:#3d6fb6;--rest:#e6e9ee;--grid:#d0d7de}',
     '@media (prefers-color-scheme: dark){:root{--bg:#0d1117;--ink:#e6edf3;--muted:#9198a1;--ex:#e0714f;--nr:#6e6258;--ad:#6f9fe0;--rest:#30363d;--grid:#3d444d}}',
     'text{font-family:system-ui,-apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:var(--ink)}',
     '.m{fill:var(--muted);font-size:10px}.l{font-size:10.5px}',
     '</style>',
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     '<text x="16" y="20" font-size="13" font-weight="600">Downloads on older versions, by the Python that fetched them</text>',
     '<text x="16" y="36" class="m">Each bar is one project\'s downloads over 21 to 27 September 2026; older means below the release of 21 August or earlier.</text>']
for j, (lab, var) in enumerate((('older version, fetched from a Python that every newer release excludes', 'ex'), ('older version, no Python reported', 'nr'),
                               ('older version, fetched from a Python that a newer release admits', 'ad'), ('that release or newer', 'rest'))):
    lx, ly = (16 if j % 2 == 0 else 400), 46 + 13 * (j // 2)
    s.append(f'<rect x="{lx}" y="{ly}" width="10" height="8" fill="var(--{var})"/><text x="{lx + 14}" y="{ly + 8}" class="m">{lab}</text>')
for i, (p, ex, nr, ad, O) in enumerate(rows):
    y = top + i * rh
    s.append(f'<text x="{left - 6}" y="{y + 9.5}" text-anchor="end" class="l">{p}</text>')
    x = left
    for v, var in ((ex, 'ex'), (nr, 'nr'), (ad, 'ad'), (max(0.0, 1 - ex - nr - ad), 'rest')):
        w = v * bw
        s.append(f'<rect x="{x:.2f}" y="{y + 1.5}" width="{w:.2f}" height="{rh - 3}" fill="var(--{var})"/>')
        x += w
for k in range(0, 101, 25):
    x = left + bw * k / 100
    s.append(f'<line x1="{x:.1f}" y1="{top - 2}" x2="{x:.1f}" y2="{top + rh * len(rows)}" stroke="var(--grid)" stroke-width="0.6"/>')
    s.append(f'<text x="{x:.1f}" y="{top + rh * len(rows) + 13}" text-anchor="middle" class="m">{k}%</text>')
s.append(f'<text x="{left}" y="{H - 8}" class="m">ClickPy, per-version and per-Python downloads, read 29 September 2026; Requires-Python from PyPI.</text>')
s.append('</svg>')
open(out, 'w').write('\n'.join(s) + '\n')
print(out)
