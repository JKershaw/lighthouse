#!/usr/bin/env python3
"""LH034 with LH033: draw the month-on revision's figure (offline, no library), days 0 to 30.

Top panel, downloads: the at-or-newer share of each fixed Node.js line's daily nodejs.org downloads (LH034 version
1.1, data/record_v1.json), by the post hoc amended rule on every day and, thinner, by the rule as written from day 20
(the two agree on days 0 to 20); beside the range of LH008's four Python security fixes' at-or-newer download shares
and the median over LH011's 37 projects (LH011's release_days.csv, as python_side.json tabulates them).
Bottom panel, services seen from outside: Censys's patched share of version-reporting PHP services in each fixed
branch (LH033 version 1.2; the day-30 read of 21 November 2026, which holds every day 0 to 30 unrevised).
Two panels, each with its own unit, so that a request share and a service share never sit on one scale.
Usage: python3 -I studies/LH034/scripts/draw_piece_figure_rev.py [out.svg]
       (default: articles/drafts/a-week-after-two-fixes-rev.svg); prints the plotted day 1, 7, 14 and 30 values.
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
from chart_style import css, DASHES  # noqa: E402

PHP_READ = ROOT / 'studies/LH033/data/read-2026-11-21T1414Z/tables.json'
NODE = ROOT / 'studies/LH034/data/record_v1.json'
out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'articles/drafts/a-week-after-two-fixes-rev.svg'
LAST = 30
days = range(LAST + 1)

php = {b: [s[str(d)]['patched'] / s[str(d)]['targets'] for d in days]   # unrounded, so labels round once
       for b, s in json.loads(PHP_READ.read_text())['m1_patched_share_by_branch'].items()}
m1 = json.loads(NODE.read_text())['measure_1']
node_am = {l: [s['daily_pct'][str(d)] / 100 for d in days] for l, s in m1['amended_post_hoc'].items()}
node_aw = {l: [s['daily_pct'][str(d)] / 100 for d in days] for l, s in m1['as_written'].items()}

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
lo = [min(f[d] for f in fix.values()) for d in days]
hi = [max(f[d] for f in fix.values()) for d in days]
med = [statistics.median(statistics.median(p[d]) for p in proj.values() if p.get(d)) for d in days]

pct = lambda v: f'{v * 100:.1f}%'
for d in (1, 7, 14, 30):
    print(f'day {d}: Node amended', {l: pct(s[d]) for l, s in node_am.items()},
          'as written', {l: pct(s[d]) for l, s in node_aw.items()},
          f'| Python fixes {pct(lo[d])} to {pct(hi[d])}, median {pct(med[d])}',
          '| PHP', {b: pct(s[d]) for b, s in sorted(php.items())})

W, H = 720, 860
X0, X1 = 60, 500
PH = 220
P1, P2 = 160, 490
x = lambda d: X0 + (X1 - X0) * d / LAST
y = lambda top, v: top + PH - PH * v


def rng(a, b):
    return f'{a * 100:.1f} to {b * 100:.1f} per cent'


desc = ('Two line charts, one above the other, each with its own unit, by day since the releases of 21 October 2026 (day 0) '
        'to day 30, 20 November. The top chart is downloads: the share of each fixed Node.js line\'s daily downloads from '
        'nodejs.org that were the fixed release or newer. On day 7 line 22 was at ' + pct(node_am['22'][7]) + ', line 24 at '
        + pct(node_am['24'][7]) + ' and line 26 at ' + pct(node_am['26'][7]) + '. On day 30, counting three newer versions '
        'first seen on 11 November (day 21) as fixed, a rule chosen after the counts were seen, they were '
        + pct(node_am['22'][30]) + ', ' + pct(node_am['24'][30]) + ' and ' + pct(node_am['26'][30]) + '; thinner lines from '
        'day 20 show the rule as first written, which leaves those versions out and ends at ' + pct(node_aw['22'][30]) + ', '
        + pct(node_aw['24'][30]) + ' and ' + pct(node_aw['26'][30]) + '. Behind them, a band shows the range of four Python '
        'security fixes\' share of their library\'s daily downloads, ' + rng(lo[7], hi[7]) + ' on day 7 and '
        + rng(lo[30], hi[30]) + ' on day 30, and a dashed line the median over 37 Python libraries, ' + pct(med[30]) +
        ' on day 30; those releases date from April to August 2026. The bottom chart is services seen from outside: the '
        'share of internet-facing PHP services reporting a version in each fixed branch that Censys counts as patched. '
        'On day 7: ' + ', '.join(f'{b} {pct(s[7])}' for b, s in sorted(php.items())) + '; on day 14: '
        + ', '.join(f'{b} {pct(s[14])}' for b, s in sorted(php.items())) + '; on day 30: '
        + ', '.join(f'{b} {pct(s[30])}' for b, s in sorted(php.items())) + '. A dashed line marks half in each chart. '
        'Downloads are requests, not machines; Censys\'s patched shares are floors, because distributions that backport a '
        'fix keep the old version number and a service counts only after a rescan; after day 14 three PHP branches\' '
        'shares rose mostly because fewer services were counted in them. Sources: nodejs.org download summaries and Censys '
        'ARC\'s PHP2Shell dashboard, read by Lighthouse to 22 and 21 November 2026; ClickPy\'s copy of the Python Package '
        'Index download log, read 28 September 2026.')

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
     '<title id="t">A month after the PHP and Node.js fixes of 21 October 2026: Node.js downloads beside Python downloads, '
     'and PHP services counted from outside</title>',
     f'<desc id="d">{escape(desc)}</desc>', css(),
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     '<text x="16" y="30" class="head">A month after the fixes of 21 October 2026</text>',
     '<text x="16" y="51" class="sub">Two kinds of count, drawn apart: requests to download servers, and services seen from outside.</text>',
     '<text x="16" y="68" class="sub">Each panel has its own unit. Day 0 is the release day (UTC), a part day; day 30 is 20 November.</text>']


def axes(top, unit_label):
    for v in (0, 0.25, 0.5, 0.75, 1):
        style = 'stroke="var(--muted)" stroke-dasharray="4 3"' if v == 0.5 else 'stroke="var(--grid)"'
        o.append(f'<line x1="{X0}" y1="{y(top, v):.1f}" x2="{X1}" y2="{y(top, v):.1f}" {style} stroke-width="1"/>')
        o.append(f'<text x="{X0 - 8}" y="{y(top, v) + 4:.1f}" class="ax" text-anchor="end">{int(v * 100)}%</text>')
    for d in (0, 7, 14, 21, 30):
        o.append(f'<line x1="{x(d):.1f}" y1="{top + PH}" x2="{x(d):.1f}" y2="{top + PH + 4}" stroke="var(--muted)" stroke-width="1"/>')
        o.append(f'<text x="{x(d):.1f}" y="{top + PH + 18}" class="ax" text-anchor="middle">{d}</text>')
    o.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{top + PH + 34}" class="ax" text-anchor="middle">days since the release</text>')
    o.append(f'<text x="{X0}" y="{top - 12}" class="ann">{escape(unit_label)}</text>')


def labels(top, items):
    """items: (value at day 30, text, colour); keep 15 px apart in the right margin."""
    rows = sorted([[y(top, v) + 4, text, colour, y(top, v)] for v, text, colour in items])
    for i in range(1, len(rows)):
        rows[i][0] = max(rows[i][0], rows[i - 1][0] + 15)
    for yy, text, colour, ey in rows:
        o.append(f'<path d="M{X1 + 5:.1f},{ey:.1f} L{X1 + 11:.1f},{yy - 4:.1f}" fill="none" stroke="var(--{colour})"/>')
        o.append(f'<text x="{X1 + 14}" y="{yy:.1f}" class="nm">{escape(text)}</text>')


def path(top, vals, start=0):
    return 'M' + ' L'.join(f'{x(d):.1f},{y(top, vals[d]):.1f}' for d in range(start, LAST + 1))


# Top panel: downloads
o.append(f'<text x="16" y="{P1 - 44}" class="sec">Downloads: share of a day\'s downloads at the fixed release or newer</text>')
axes(P1, 'Node.js (nodejs.org) and Python (PyPI): requests in a day, not machines')
o.append(f'<line x1="{x(21):.1f}" y1="{P1}" x2="{x(21):.1f}" y2="{P1 + PH}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="2 3"/>')
o.append(f'<text x="{x(21) - 4:.1f}" y="{P1 + PH - 8}" class="ann" text-anchor="end">11 Nov: three newer Node.js versions appear</text>')
band = ' L'.join(f'{x(d):.1f},{y(P1, hi[d]):.1f}' for d in days) + ' L' + ' L'.join(f'{x(d):.1f},{y(P1, lo[d]):.1f}' for d in reversed(days))
o.append(f'<path d="M{band} Z" fill="var(--amber)" fill-opacity="0.12" stroke="var(--amber)" stroke-width="1.2">'
         f'<title>Four Python security fixes: {pct(lo[7])} to {pct(hi[7])} on day 7, {pct(lo[30])} to {pct(hi[30])} on day 30</title></path>')
o.append(f'<path d="{path(P1, med)}" fill="none" stroke="var(--amber)" stroke-width="2" stroke-dasharray="5 3">'
         f'<title>Median over 37 Python libraries: {pct(med[7])} on day 7, {pct(med[30])} on day 30</title></path>')
items = [(hi[30] + 0.0001, 'Python fixes, range', 'amber'), (med[30], 'Python, median', 'amber')]
for i, line in enumerate(sorted(node_am)):
    dash = f' stroke-dasharray="{DASHES[i]}"' if DASHES[i] else ''
    o.append(f'<path d="{path(P1, node_aw[line], 20)}" fill="none" stroke="var(--neutral)" stroke-width="1.3"{dash}>'
             f'<title>Node.js {line}, rule as first written, days 20 to 30: {pct(node_aw[line][30])} on day 30</title></path>')
    o.append(f'<path d="{path(P1, node_am[line])}" fill="none" stroke="var(--purple)" stroke-width="2.2" stroke-linejoin="round"{dash}>'
             f'<title>Node.js {line}, counting the newer versions as fixed (post hoc): {pct(node_am[line][7])} on day 7, '
             f'{pct(node_am[line][30])} on day 30</title></path>')
    for d in (1, 7, 14, 30):
        o.append(f'<circle cx="{x(d):.1f}" cy="{y(P1, node_am[line][d]):.1f}" r="3.2" fill="var(--purple)" stroke="var(--bg)" stroke-width="1.5">'
                 f'<title>Node.js {line}, day {d}: {pct(node_am[line][d])}</title></circle>')
    items.append((node_am[line][30], f'Node.js {line}  {pct(node_am[line][30])}', 'purple'))
    items.append((node_aw[line][30], f'{line}, as written  {pct(node_aw[line][30])}', 'neutral'))
labels(P1, items)

# Bottom panel: services
o.append(f'<text x="16" y="{P2 - 44}" class="sec">Services seen from outside: share Censys counts as patched</text>')
axes(P2, 'PHP: internet-facing services reporting a version, as last scanned; a floor on protection')
items = []
for i, (b, s) in enumerate(sorted(php.items())):
    dash = f' stroke-dasharray="{DASHES[i]}"' if DASHES[i] else ''
    o.append(f'<path d="{path(P2, s)}" fill="none" stroke="var(--teal)" stroke-width="2.2" stroke-linejoin="round"{dash}/>')
    for d in (1, 7, 14, 30):
        o.append(f'<circle cx="{x(d):.1f}" cy="{y(P2, s[d]):.1f}" r="3.2" fill="var(--teal)" stroke="var(--bg)" stroke-width="1.5">'
                 f'<title>PHP {b}, day {d}: {pct(s[d])} of version-reporting services counted patched</title></circle>')
    items.append((s[30], f'PHP {b}  {pct(s[30])}', 'teal'))
labels(P2, items)

notes = ['Node.js: thick lines count three versions first seen on 11 November as fixed, a rule chosen after the counts were seen;',
         'thin grey lines, from day 20, leave them out, as first written. Python: four security fixes and 37 libraries, April to August 2026.',
         'PHP: after day 14, three branches rose mostly because fewer services were counted in them, not more patched.',
         'Sources: nodejs.org summaries (read to 22 Nov 2026); Censys ARC PHP2Shell (21 Nov 2026); ClickPy (28 Sept 2026).']
for i, line in enumerate(notes):
    o.append(f'<text x="16" y="{H - 74 + i * 16}" class="note">{escape(line)}</text>')
o.append('</svg>')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('\n'.join(o) + '\n')
print('wrote', out, file=sys.stderr)
