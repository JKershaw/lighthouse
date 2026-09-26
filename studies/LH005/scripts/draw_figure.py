#!/usr/bin/env python3
"""LH005: draws uptake.svg from data/mcp_daily_by_version_share.csv and the LH002 moves.
Usage: python3 draw_figure.py"""
import datetime, os
from common import read_csv, STUDY

rows = read_csv('mcp_daily_by_version_share.csv')
D0 = datetime.date.fromisoformat(rows[0]['date'])
N = len(rows)
W, H = 1000, 580
L, R, T, B = 64, 170, 92, 360          # plot box: x from L to W-R, y from T to B
PW, PH = W - L - R, B - T


def x_at(t):
    """t: datetime (UTC). Day d's data point sits at the middle of the day."""
    days = (t - datetime.datetime.combine(D0, datetime.time())).total_seconds() / 86400
    return L + PW * days / N


def x_day(i):
    return L + PW * (i + 0.5) / N


def y(v):
    return B - PH * v


dt = lambda s: datetime.datetime.fromisoformat(s)
SERIES = [('share_1.27.0', '1.27.0', '--s1'), ('share_1.26.0', '1.26.0', '--s2'),
          ('other', 'every other version', '--s3')]
for r in rows:
    r['other'] = str(1 - float(r['share_1.27.0']) - float(r['share_1.26.0']))

MOVES = [  # LH002 data/propagation_candidates.csv and data/pypi_releases_in_window.csv
    ('2026-04-04T16:20', 'R04 first GitHub commit, lockfile holds 1.27.0'),
    ('2026-04-08T18:26', 'R03 lean-lsp-mcp pins mcp==1.27.0; its 0.26.0 22 min later'),
    ('2026-04-13T13:57', 'R06 dartlab lockfile to 1.27.0'),
    ('2026-04-14T00:09', 'R04 pyp6xer-mcp adds mcp==1.27.0'),
    ('2026-04-22T23:02', 'R02 ai-slide-generator adds mcp, lock 1.27.0'),
]
REL = dt('2026-04-02T14:48')

o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     'aria-labelledby="t d">',
     '<title id="t">Share of mcp daily downloads by version, 19 March to 29 April 2026</title>',
     '<desc id="d">Lines for mcp 1.27.0, 1.26.0 and every other version, as shares of each UTC day\'s downloads '
     'in ClickPy\'s copy of the PyPI download table, with the LH002 window shaded and the dependents\' moves marked.</desc>',
     '<style>',
     'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e4e3df; --win:#f0efec; '
     '--s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --acc:#0b0b0b; }',
     '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781; '
     '--grid:#383835; --win:#2a2a28; --s1:#3987e5; --s2:#d95926; --s3:#199e70; --acc:#ffffff; } }',
     'text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink); }',
     '.t2 { fill: var(--ink2); } .mu { fill: var(--muted); }',
     '</style>',
     f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
     '<text x="16" y="30" font-size="17" font-weight="600">What was downloaded: mcp versions as a share of each day\'s downloads</text>',
     '<text x="16" y="52" font-size="12.5" class="t2">All installers, UTC days, 19 March to 29 April 2026. ClickPy (ClickHouse\'s copy of PyPI\'s BigQuery download table), read 26 September 2026.</text>',
     '<text x="16" y="70" font-size="12.5" class="t2">Denominator: every download of any mcp version that day, 3.6 to 11.7 million a day.</text>']
# LH002 window shading
wx0 = x_at(dt('2026-03-26T00:00')); wx1 = x_at(dt('2026-04-23T00:00'))
o.append(f'<rect x="{wx0:.1f}" y="{T}" width="{wx1 - wx0:.1f}" height="{PH}" fill="var(--win)"/>')
o.append(f'<text x="{wx0 + 4:.1f}" y="{T + 14}" font-size="11" class="mu">LH002 window, 26 Mar to 22 Apr</text>')
# grid and y axis
for v in (0, .25, .5, .75, 1):
    o.append(f'<line x1="{L}" y1="{y(v):.1f}" x2="{W - R}" y2="{y(v):.1f}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<text x="{L - 8}" y="{y(v) + 4:.1f}" font-size="11" text-anchor="end" class="mu">{int(v * 100)}%</text>')
# x axis: Mondays
for i, r in enumerate(rows):
    d = datetime.date.fromisoformat(r['date'])
    if d.weekday() == 0:
        xx = L + PW * i / N
        o.append(f'<line x1="{xx:.1f}" y1="{B}" x2="{xx:.1f}" y2="{B + 5}" stroke="var(--muted)"/>')
        o.append(f'<text x="{xx:.1f}" y="{B + 18}" font-size="11" text-anchor="middle" class="mu">Mon {d.day} {d.strftime("%b")}</text>')
# release line
rx = x_at(REL)
o.append(f'<line x1="{rx:.1f}" y1="{T - 6}" x2="{rx:.1f}" y2="{B}" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="4 3"/>')
o.append(f'<text x="{rx + 4:.1f}" y="{T - 10}" font-size="11.5" font-weight="600">mcp 1.27.0 on PyPI, 2 Apr 14:48 UTC</text>')
# series
for key, label, var in SERIES:
    pts = ' '.join(f'{x_day(i):.1f},{y(float(r[key])):.1f}' for i, r in enumerate(rows))
    o.append(f'<polyline points="{pts}" fill="none" stroke="var({var})" stroke-width="2" stroke-linejoin="round"/>')
    for i, r in enumerate(rows):
        n = r['1.27.0'] if key == 'share_1.27.0' else r['1.26.0'] if key == 'share_1.26.0' else \
            str(int(r['all_versions']) - int(r['1.27.0']) - int(r['1.26.0']))
        o.append(f'<circle cx="{x_day(i):.1f}" cy="{y(float(r[key])):.1f}" r="7" fill="transparent">'
                 f'<title>{r["date"]} ({r["weekday"]}): {label} {float(r[key]) * 100:.1f}%, {int(n):,} of {int(r["all_versions"]):,}</title></circle>')
    last = rows[-1]
    o.append(f'<text x="{W - R + 8}" y="{y(float(last[key])) + 4:.1f}" font-size="12" font-weight="600" class="t2">'
             f'<tspan fill="var({var})">●</tspan> {label}</text>')
# moves, on a strip below the axis
sy = B + 44
o.append(f'<text x="16" y="{sy - 8}" font-size="12" font-weight="600">LH002 moves</text>')
o.append(f'<line x1="{L}" y1="{sy}" x2="{W - R}" y2="{sy}" stroke="var(--grid)"/>')
for k, (t, lab) in enumerate(MOVES):
    mx = x_at(dt(t))
    ly = sy + 22 + 20 * k
    o.append(f'<line x1="{mx:.1f}" y1="{T}" x2="{mx:.1f}" y2="{B}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="1 3"/>')
    o.append(f'<circle cx="{mx:.1f}" cy="{sy}" r="5" fill="var(--acc)"/>')
    o.append(f'<line x1="{mx:.1f}" y1="{sy}" x2="{mx:.1f}" y2="{ly - 4}" stroke="var(--muted)" stroke-width="1"/>')
    anchor = 'end' if mx > L + PW * 0.6 else 'start'
    tx = mx - 6 if anchor == 'end' else mx + 6
    o.append(f'<text x="{tx:.1f}" y="{ly}" font-size="11.5" text-anchor="{anchor}" class="t2">'
             f'{datetime.datetime.fromisoformat(t).strftime("%d %b %H:%M")} {lab}</text>')
o.append(f'<text x="16" y="{H - 28}" font-size="11" class="mu">Moves from studies/LH002/data/propagation_candidates.csv (commit times, UTC).</text>')
o.append(f'<text x="16" y="{H - 12}" font-size="11" class="mu">Shares from studies/LH005/data/mcp_daily_by_version_share.csv. Hover a point for the count.</text>')
o.append('</svg>')
open(os.path.join(STUDY, 'uptake.svg'), 'w').write('\n'.join(o) + '\n')
print('wrote uptake.svg')
