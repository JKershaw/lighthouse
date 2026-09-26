#!/usr/bin/env python3
"""LH005: draws the reader-facing figure for the piece, articles/what-a-download-shows.svg.

Bars: the share of each UTC day's mcp downloads that were 1.27.0, 26 March to 22 April 2026,
from data/mcp_daily_by_version_share.csv (ClickPy by-version table, read 26 September 2026).
Marks: the days LH002's dependents were seen taking up 1.27.0, from
studies/LH002/data/propagation_candidates.csv (commit times, UTC), as draw_figure.py uses them.
No internal names or ids appear in the drawing.
Usage: python3 draw_piece_figure.py"""
import datetime, os
from common import read_csv, STUDY

OUT = os.path.join(STUDY, '..', '..', 'articles', 'what-a-download-shows.svg')
FIRST, LAST = '2026-03-26', '2026-04-22'
rows = [r for r in read_csv('mcp_daily_by_version_share.csv') if FIRST <= r['date'] <= LAST]
N = len(rows)
D0 = datetime.date.fromisoformat(FIRST)

W = 600
L, R = 52, 20                   # plot box x from L to W - R
T, B = 104, 318                 # plot box y from T to B
PW, PH = W - L - R, B - T
SLOT = PW / N
REL = datetime.datetime(2026, 4, 2, 14, 48)

# (commit time UTC, label). From studies/LH002/data/propagation_candidates.csv.
MOVES = [
    ('2026-04-04T16:20', '4 Apr', 'already held by a project new to GitHub'),
    ('2026-04-08T18:26', '8 Apr', 'first exact pin; own release follows'),
    ('2026-04-13T13:57', '13 Apr', "a busy project's lockfile"),
    ('2026-04-14T00:09', '14 Apr', 'a second exact pin'),
    ('2026-04-22T23:02', '22 Apr', 'a first-time user'),
]


def x_time(t):
    days = (t - datetime.datetime.combine(D0, datetime.time())).total_seconds() / 86400
    return L + SLOT * days


def y(v):
    return B - PH * v


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace("'", '&#39;')


MOVE_Y0 = B + 74
ROW = 24
H = MOVE_Y0 + ROW * len(MOVES) + 44

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
     '<title id="t">How much of each day\'s downloads of mcp were the new version, 26 March to 22 April 2026</title>',
     '<desc id="d">A bar for each day from 26 March to 22 April 2026 shows the share of that day\'s downloads of the '
     'Python library mcp that were its new version, 1.27.0, published on 2 April at 14:48 UTC. The share is 22 per cent '
     'on the day of release, 48 per cent the next day, 51 per cent the day after, and between 45 and 71 per cent on every '
     'day to 22 April. Beneath, the days on which four of nine neighbouring projects that depend on the library were seen '
     'taking it up: 4, 8, 13, 14 and 22 April. The downloads reach about half before the first of those days.</desc>',
     '<style>',
     'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --bar:#2a78d6; --acc:#0b0b0b; }',
     '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; '
     '--grid:#383835; --bar:#3987e5; --acc:#ffffff; } }',
     'text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }',
     '.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }',
     '.ax { font-size: 12px; fill: var(--muted); } .lab { font-size: 13px; fill: var(--ink2); }',
     '.strong { font-size: 13px; font-weight: 600; } .note { font-size: 12px; fill: var(--muted); }',
     '</style>',
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     '<text class="head" x="16" y="30">The new version, as a share of each day\'s downloads</text>',
     '<text class="sub" x="16" y="52">mcp 1.27.0, UTC days, 26 March to 22 April 2026</text>']

# grid and y axis
for v in (0, .25, .5, .75, 1):
    o.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{W - R}" y2="{y(v):.1f}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<text class="ax" x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{int(v * 100)}%</text>')

# bars, with a hover title carrying the count
for i, r in enumerate(rows):
    s = float(r['share_1.27.0'])
    if s <= 0:
        continue
    bx = L + SLOT * i + 2
    bw = SLOT - 4
    top = y(s)
    o.append(f'<path d="M{bx:.1f},{B} V{top + 3:.1f} Q{bx:.1f},{top:.1f} {bx + 3:.1f},{top:.1f} H{bx + bw - 3:.1f} '
             f'Q{bx + bw:.1f},{top:.1f} {bx + bw:.1f},{top + 3:.1f} V{B} Z" fill="var(--bar)">'
             f'<title>{r["date"]}: {s * 100:.1f}%, {int(r["1.27.0"]):,} of {int(r["all_versions"]):,} downloads</title></path>')

# direct labels on three bars
by_date = {r['date']: (i, r) for i, r in enumerate(rows)}
i, r = by_date['2026-04-12']
o.append(f'<text class="strong" x="{L + SLOT * (i + 0.5):.1f}" y="{y(float(r["share_1.27.0"])) - 8:.1f}" '
         f'text-anchor="middle">peak: {float(r["share_1.27.0"]) * 100:.0f}%</text>')
i, r = by_date['2026-04-03']   # the day after release: label in the empty space left of the release line
ty = y(float(r['share_1.27.0']))
bx = L + SLOT * i + 2
o.append(f'<line x1="{L + SLOT * 6:.1f}" y1="{ty:.1f}" x2="{bx - 2:.1f}" y2="{ty:.1f}" stroke="var(--muted)" stroke-width="1"/>')
o.append(f'<text class="strong" x="{L + SLOT * 6 - 4:.1f}" y="{ty + 4:.1f}" text-anchor="end">'
         f'next day: {float(r["share_1.27.0"]) * 100:.0f}%</text>')

# release line
rx = x_time(REL)
o.append(f'<line x1="{rx:.1f}" y1="{T - 22}" x2="{rx:.1f}" y2="{B}" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="4 3"/>')
o.append(f'<text class="strong" x="{rx + 6:.1f}" y="{T - 12}">released 2 Apr, 14:48 UTC</text>')

# x axis: every Thursday from 26 March, plus the last day
for i, r in enumerate(rows):
    d = datetime.date.fromisoformat(r['date'])
    if i % 7 == 0 or i == N - 1:
        cx = L + SLOT * (i + 0.5)
        o.append(f'<line x1="{cx:.1f}" y1="{B}" x2="{cx:.1f}" y2="{B + 5}" stroke="var(--muted)"/>')
        anchor = 'end' if i == N - 1 else 'middle'
        tx = cx + SLOT / 2 if i == N - 1 else cx
        o.append(f'<text class="ax" x="{tx:.1f}" y="{B + 20}" text-anchor="{anchor}">{d.day} {d.strftime("%b")}</text>')

# the neighbours' moves: one row each, the dot at its time on the same axis as the bars
o.append(f'<text class="strong" x="16" y="{B + 50}">When four of nine neighbouring projects took it up</text>')
for k, (t, day, lab) in enumerate(MOVES):
    mx = x_time(datetime.datetime.fromisoformat(t))
    ry = MOVE_Y0 + ROW * k
    o.append(f'<line x1="{L}" y1="{ry}" x2="{W - R}" y2="{ry}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<circle cx="{mx:.1f}" cy="{ry}" r="5" fill="var(--acc)"/>')
    text = f'<tspan font-weight="600" fill="var(--ink)">{day}</tspan> {esc(lab)}'
    if mx > W / 2:
        o.append(f'<text class="lab" x="{mx - 10:.1f}" y="{ry + 4.5}" text-anchor="end">{text}</text>')
    else:
        o.append(f'<text class="lab" x="{mx + 10:.1f}" y="{ry + 4.5}">{text}</text>')

o.append(f'<text class="note" x="16" y="{H - 30}">Downloads: PyPI\'s public download log, in ClickHouse\'s copy, read 26 September 2026.</text>')
o.append(f'<text class="note" x="16" y="{H - 13}">Projects: their public histories, read the same day. The other five did not take it up.</text>')
o.append('</svg>')

with open(OUT, 'w') as f:
    f.write('\n'.join(o) + '\n')
print('wrote', os.path.normpath(OUT))
