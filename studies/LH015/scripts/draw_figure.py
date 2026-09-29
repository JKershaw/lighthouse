#!/usr/bin/env python3
"""LH015: draw recipes.svg from data/pair_classes.csv (offline). One bar per row (all pairs, then the
three pin classes), each a whole: the pairs whose recipes install from the pinned file (blue), those
whose recipes do not (orange), those the rules could not decide (grey, hatched), those whose recipes
install nothing of the project's Python requirements (pale grey) and those with no recipe (outline).
Counts are labelled where a segment is wide enough; every segment carries a native tooltip.
Colour tokens, marks and plain SVG follow studies/LH014/scripts/draw_figure.py; the blue and orange
pairs were checked with the dataviz skill's validate_palette.js (light on #fcfcfb, dark on #1a1a19).
Usage: python3 draw_figure.py [out.svg]   (default: studies/LH015/recipes.svg)"""
import csv, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
D = os.environ.get('LH015_DATA', os.path.join(STUDY, 'data'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STUDY, 'recipes.svg')
pairs = list(csv.DictReader(open(os.path.join(D, 'pair_classes.csv'))))
pairs = [p for p in pairs if p['status'] == 'read']

CLASSES = [('from the pinned file', 'From the pinned file', 'fa'),
           ('not from the pinned file', 'Not from the pinned file', 'fb'),
           ('undetermined', 'Could not be decided', 'fu'),
           ("nothing of the project's requirements", "Installs none of the project's requirements", 'fn'),
           ('no recipe', 'No container recipe', 'fo')]
ROWS = [('All pairs', None), ('Lockfile only', 'lockfile'), ('Exact pin only', 'exact pin'), ('Lockfile and pin', 'both')]
counts = []
for name, pin in ROWS:
    c = Counter(p['pair_class'] for p in pairs if pin is None or p['pin_class'] == pin)
    unknown = set(c) - {k for k, _, _ in CLASSES}
    assert not unknown, unknown
    counts.append((name, c, sum(c.values())))

W, L, R = 720, 150, 24
T, RH, BH = 132, 46, 26
H = T + RH * len(ROWS) + 58
bw = W - L - R
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace("'", '&#39;')
e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     'aria-label="For 469 moments when a Python project pinned or locked a widely used library, what the '
     'container recipe the project kept at that moment would install: from the pinned file, not from it, '
     'undecided, none of the project\'s requirements, or no recipe, for all pairs and by kind of pin">']
e.append('<style>svg{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--grid:#e4e3de;--a:#2a78d6;--b:#eb6834;'
         '--u:#a9a8a2;--n:#d6d5cf;--o:#ffffff;--ol:#b3b2ac;--on:#ffffff}'
         '@media (prefers-color-scheme: dark){svg{--bg:#1a1a19;--ink:#ffffff;--ink2:#c3c2b7;--grid:#3a3936;'
         '--a:#3987e5;--b:#d95926;--u:#6f6e69;--n:#4a4945;--o:#1a1a19;--ol:#6f6e69;--on:#ffffff}}'
         'text{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:var(--ink2)}.t{fill:var(--ink);font-weight:600}'
         '.s{font-size:11px}.v{fill:var(--on);font-size:11px;font-weight:600}.d{fill:var(--ink);font-size:11px;font-weight:600}'
         '.fa{fill:var(--a)}.fb{fill:var(--b)}.fu{fill:url(#hatch)}.fn{fill:var(--n)}.fo{fill:var(--o);stroke:var(--ol);stroke-width:1}'
         '</style>')
e.append('<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="6" height="6" fill="var(--n)"/><rect width="2.2" height="6" fill="var(--u)"/></pattern></defs>')
e.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
e.append('<text x="16" y="24" class="t">What a pinned project\'s own container recipe would install</text>')
e.append('<text x="16" y="42" class="s">469 moments, from 2025 to 2026, when one of 332 Python projects held an older version of a library in a pin or lockfile</text>')
e.append('<text x="16" y="58" class="s">as a new release came out; the recipe read at the project\'s last commit before the release</text>')
# legend, two rows, marks beside text
for j, (key, label, cls) in enumerate(CLASSES):
    lx, ly = ((16, 212, 408, 16, 330)[j], 84 + 20 * (j // 3))
    e.append(f'<rect x="{lx}" y="{ly - 9}" width="11" height="11" rx="2" class="{cls}"/>')
    e.append(f'<text x="{lx + 16}" y="{ly}" class="s">{esc(label)}</text>')
for i, (name, c, n) in enumerate(counts):
    y = T + i * RH
    e.append(f'<text x="16" y="{y + BH / 2 + 4}" class="t">{esc(name)}</text>')
    e.append(f'<text x="16" y="{y + BH / 2 + 18}" class="s">{n} pairs</text>')
    x = L
    for key, label, cls in CLASSES:
        k = c.get(key, 0)
        if not k:
            continue
        w = bw * k / n
        gap = 2 if x > L else 0
        e.append(f'<rect x="{x + gap:.1f}" y="{y}" width="{max(w - gap, 0.5):.1f}" height="{BH}" rx="3" class="{cls}">'
                 f'<title>{esc(name)}: {esc(label.lower())}, {k} of {n} pairs ({100 * k / n:.1f} per cent)</title></rect>')
        if w >= 20:
            cl = 'v' if key in ('from the pinned file', 'not from the pinned file') else 'd'
            e.append(f'<text x="{x + w / 2 + gap / 2:.1f}" y="{y + BH / 2 + 4}" text-anchor="middle" class="{cl}">{k}</text>')
        x += w
e.append(f'<text x="16" y="{H - 30}" class="s">A recipe is not a build: no image was read. Whether a build installs the library at all was not resolved.</text>')
e.append(f'<text x="16" y="{H - 14}" class="s">Pin class: the kind of file that held the older version. Source: studies/LH015, data/pair_classes.csv.</text>')
e.append('</svg>')
open(out, 'w').write('\n'.join(e) + '\n')
print(out, [(n, dict(c), t) for n, c, t in counts])
