#!/usr/bin/env python3
"""LH034 with LH033: draw the week-one piece's figure, frozen at the reads it uses (offline, no library).

Top panel, downloads: the at-or-newer share of each fixed Node.js line's daily nodejs.org downloads (LH034, days 0 to 7),
beside the range of LH008's four Python security fixes' at-or-newer download shares and the median over LH011's 37 projects.
Bottom panel, services seen from outside: Censys's patched share of version-reporting PHP services in each fixed branch
(LH033, read of 29 October 2026, days 0 to 7). Two panels, each with its own unit, so that a request share and a
service share never sit on one scale.
Usage: python3 draw_piece_figure.py [out.svg]   (default: articles/a-week-after-two-fixes.svg)
"""
from collections import defaultdict
from html import escape
from pathlib import Path
import csv
import json
import statistics
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from chart_style import css, DASHES

PHP_READ = ROOT / 'studies/LH033/data/read-2026-10-29T0635Z/tables.json'
NODE = ROOT / 'studies/LH034/data/tables.json'
out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'articles/a-week-after-two-fixes.svg'
LAST = 7

php = {b: [s[str(d)]['patched'] / s[str(d)]['targets'] for d in range(LAST + 1)]  # unrounded, so labels round once
       for b, s in json.loads(PHP_READ.read_text())['m1_patched_share_by_branch'].items()}
node = {l: [s[str(d)]['at_or_newer'] / s[str(d)]['line_downloads'] for d in range(LAST + 1)]
        for l, s in json.loads(NODE.read_text())['measure_1_2026-10']['by_line'].items()}

FIXES = {('urllib3', '2.7.0'), ('cryptography', '48.0.1'), ('pyjwt', '2.13.0'), ('starlette', '1.1.0')}
fix = defaultdict(dict)
proj = defaultdict(lambda: defaultdict(list))
for r in csv.DictReader(open(ROOT / 'studies/LH011/data/analysis/release_days.csv')):
    if r['status'] != 'known' or not r['share_at_or_newer']:
        continue
    d, v = int(r['day']), float(r['share_at_or_newer'])
    if d > LAST:
        continue
    proj[r['project']][d].append(v)
    if (r['project'], r['version']) in FIXES:
        fix[(r['project'], r['version'])][d] = v
days = range(LAST + 1)
lo = [min(f[d] for f in fix.values()) for d in days]
hi = [max(f[d] for f in fix.values()) for d in days]
med = [statistics.median(statistics.median(p[d]) for p in proj.values() if p.get(d)) for d in days]

W, H = 720, 800
X0, X1 = 60, 520
PH = 210                                 # panel plot height
P1, P2 = 150, 470                        # top of each plot area
x = lambda d: X0 + (X1 - X0) * d / LAST
y = lambda top, v: top + PH - PH * v
pct = lambda v: f'{v * 100:.1f}%'

def fmt_range(vals):
    return f'{min(vals) * 100:.1f} to {max(vals) * 100:.1f} per cent'

desc = ('Two line charts, one above the other, each with its own unit, by day since the releases of 21 October 2026 (day 0) '
        'to day 7, 28 October. The top chart is downloads: the share of each fixed Node.js line\'s daily downloads from nodejs.org '
        f'that were the fixed release or newer. Line 22 went from {pct(node["22"][1])} on day 1 to {pct(node["22"][7])} on day 7, '
        f'line 24 from {pct(node["24"][1])} to {pct(node["24"][7])}, and line 26 from {pct(node["26"][1])} to {pct(node["26"][7])}, '
        f'after {pct(node["26"][2])} on day 2. Behind them, a band shows the range of four Python security fixes\' share of their '
        f'library\'s daily downloads, {fmt_range([lo[1], hi[1]])} on day 1 and {fmt_range([lo[7], hi[7]])} on day 7, and a dashed '
        f'line the median over 37 Python libraries, {pct(med[1])} on day 1 and {pct(med[7])} on day 7; those releases date from '
        'April to August 2026. The bottom chart is services seen from outside: the share of internet-facing PHP services reporting '
        'a version in each fixed branch that Censys counts as patched. On day 7: ' +
        ', '.join(f'{b} {pct(s[7])}' for b, s in sorted(php.items(), key=lambda kv: -kv[1][7])) +
        f'; on day 1 they were {fmt_range([s[1] for s in php.values()])}. A dashed line marks half in each chart. '
        'Downloads are requests, not machines; Censys\'s patched shares are floors, because distributions that backport a fix '
        'keep the old version number and a service counts only after a rescan. Sources: nodejs.org download summaries and '
        'Censys ARC\'s PHP2Shell dashboard, read by Lighthouse to 29 and 30 October 2026; ClickPy\'s copy of the Python Package '
        'Index download log, read 28 September 2026.')

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
     '<title id="t">A week after the PHP and Node.js fixes of 21 October 2026: Node.js downloads beside Python downloads, '
     'and PHP services counted from outside</title>',
     f'<desc id="d">{escape(desc)}</desc>', css(),
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     '<text x="16" y="30" class="head">A week after the fixes of 21 October 2026</text>',
     '<text x="16" y="51" class="sub">Two kinds of count, drawn apart: requests to download servers, and services seen from outside.</text>',
     '<text x="16" y="68" class="sub">Each panel has its own unit. Day 0 is the release day (UTC), a part day.</text>']

def axes(top, unit_label):
    for v in (0, 0.25, 0.5, 0.75, 1):
        style = 'stroke="var(--muted)" stroke-dasharray="4 3"' if v == 0.5 else 'stroke="var(--grid)"'
        o.append(f'<line x1="{X0}" y1="{y(top, v):.1f}" x2="{X1}" y2="{y(top, v):.1f}" {style} stroke-width="1"/>')
        o.append(f'<text x="{X0 - 8}" y="{y(top, v) + 4:.1f}" class="ax" text-anchor="end">{int(v * 100)}%</text>')
    for d in days:
        o.append(f'<line x1="{x(d):.1f}" y1="{top + PH}" x2="{x(d):.1f}" y2="{top + PH + 4}" stroke="var(--muted)" stroke-width="1"/>')
        o.append(f'<text x="{x(d):.1f}" y="{top + PH + 18}" class="ax" text-anchor="middle">{d}</text>')
    o.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{top + PH + 34}" class="ax" text-anchor="middle">days since the release</text>')
    o.append(f'<text x="{X0}" y="{top - 12}" class="ann">{unit_label}</text>')

def labels(top, items):
    """items: (value at day 7, text, colour); keep 15 px apart in the right margin."""
    rows = sorted([[y(top, v) + 4, text, colour, y(top, v)] for v, text, colour in items])
    for i in range(1, len(rows)):
        rows[i][0] = max(rows[i][0], rows[i - 1][0] + 15)
    for yy, text, colour, ey in rows:
        o.append(f'<path d="M{X1 + 5:.1f},{ey:.1f} L{X1 + 11:.1f},{yy - 4:.1f}" fill="none" stroke="var(--{colour})"/>')
        o.append(f'<text x="{X1 + 14}" y="{yy:.1f}" class="nm">{text}</text>')

# Top panel: downloads
o.append(f'<text x="16" y="{P1 - 40}" class="sec">Downloads: share of a day\'s downloads at the fixed release or newer</text>')
axes(P1, 'Node.js (nodejs.org) and Python (PyPI): requests in a day, not machines')
band = ' L'.join(f'{x(d):.1f},{y(P1, hi[d]):.1f}' for d in days) + ' L' + ' L'.join(f'{x(d):.1f},{y(P1, lo[d]):.1f}' for d in reversed(days))
o.append(f'<path d="M{band} Z" fill="var(--amber)" fill-opacity="0.12" stroke="var(--amber)" stroke-width="1.2">'
         f'<title>Four Python security fixes: {pct(lo[1])} to {pct(hi[1])} on day 1, {pct(lo[7])} to {pct(hi[7])} on day 7</title></path>')
o.append('<path d="M' + ' L'.join(f'{x(d):.1f},{y(P1, med[d]):.1f}' for d in days) + '" fill="none" stroke="var(--amber)" '
         f'stroke-width="2" stroke-dasharray="5 3"><title>Median over 37 Python libraries: {pct(med[1])} on day 1, {pct(med[7])} on day 7</title></path>')
items = [(hi[7], 'Python fixes, range', 'amber'), (med[7] - 0.0001, 'Python, median', 'amber')]
for i, (line, s) in enumerate(sorted(node.items())):
    o.append('<path d="M' + ' L'.join(f'{x(d):.1f},{y(P1, v):.1f}' for d, v in enumerate(s)) + '" fill="none" stroke="var(--purple)" '
             f'stroke-width="2.2" stroke-linejoin="round"' + (f' stroke-dasharray="{DASHES[i]}"' if DASHES[i] else '') + '/>')
    for d, v in enumerate(s):
        o.append(f'<circle cx="{x(d):.1f}" cy="{y(P1, v):.1f}" r="3.5" fill="var(--purple)" stroke="var(--bg)" stroke-width="1.5">'
                 f'<title>Node.js {line}, day {d}: {pct(v)} of the line\'s downloads at or above the fix</title></circle>')
    items.append((s[7], f'Node.js {line}  {pct(s[7])}', 'purple'))
labels(P1, items)

# Bottom panel: services
o.append(f'<text x="16" y="{P2 - 40}" class="sec">Services seen from outside: share Censys counts as patched</text>')
axes(P2, 'PHP: internet-facing services reporting a version, as last scanned; a floor on protection')
items = []
for i, (b, s) in enumerate(sorted(php.items())):
    o.append('<path d="M' + ' L'.join(f'{x(d):.1f},{y(P2, v):.1f}' for d, v in enumerate(s)) + '" fill="none" stroke="var(--teal)" '
             f'stroke-width="2.2" stroke-linejoin="round"' + (f' stroke-dasharray="{DASHES[i]}"' if DASHES[i] else '') + '/>')
    for d, v in enumerate(s):
        o.append(f'<circle cx="{x(d):.1f}" cy="{y(P2, v):.1f}" r="3.5" fill="var(--teal)" stroke="var(--bg)" stroke-width="1.5">'
                 f'<title>PHP {b}, day {d}: {pct(v)} of version-reporting services counted patched</title></circle>')
    items.append((s[7], f'PHP {b}  {pct(s[7])}', 'teal'))
labels(P2, items)

notes = ['Python: four security fixes (urllib3, cryptography, pyjwt, starlette) and 37 libraries\' releases, April to August 2026.',
         'Censys counts a service patched only after a rescan sees a fixed version; distributions that backport keep the old number.',
         'Sources: nodejs.org download summaries; Censys ARC PHP2Shell (read 29 Oct 2026); ClickPy (read 28 Sept 2026).']
for i, line in enumerate(notes):
    o.append(f'<text x="16" y="{H - 52 + i * 16}" class="note">{escape(line)}</text>')
o.append('</svg>')
out.write_text('\n'.join(o) + '\n')
print('wrote', out, file=sys.stderr)
