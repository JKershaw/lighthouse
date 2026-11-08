#!/usr/bin/env python3
"""Draws traces.svg for essays/what-the-watch-would-see.md. Offline; no data read.
Replay: python3 essays/what-the-watch-would-see/draw_traces.py"""
import sys
from pathlib import Path
from html import escape
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from chart_style import svg_open  # noqa: E402

W, H = 720, 556
TITLE = 'Where a self-copying pattern would leave public traces'
DESC = ('A scenario, not an observation. Six steps of an invented pattern in which agents publish copies of a '
        'package that leads other agents to publish more. Steps with a public record are drawn solid, with the '
        'record and how soon it could register: the registry listing once the release is up (our reading), the '
        'dependency graph within about an hour for popular packages, download logs from streaming to daily, a malware '
        'record only if someone reports it. The public event archive is drawn with a dotted outline: its stated '
        'cadence is hourly, but in a reviewer\'s scan most noon hours from 15 October to 7 November 2026 held no push '
        'events. In the one malware record read, its own clock began eight days after the upload. Two steps are '
        'drawn dashed and hatched because no public instrument we know of records them: the model computing behind each '
        'decision, and another agent reading the package and deciding to act, which is the link that would make '
        'the copies a pattern. Running the copies is in no public record we know of either.')

steps = [
    # (label, layer, public?, record line 1, record line 2)
    ('An agent decides to publish', 'activity', False, 'No public record', 'the model runs at a provider'),
    ('A package appears on a registry', 'residue', True, 'Registry listing: once it is up (our reading)', 'dependency graph: about an hour if popular'),
    ('Other machines fetch it', 'residue', True, 'Download logs: streaming to daily', 'a fetch, not an install; not who'),
    ('Another agent reads it and acts', 'propagation', False, 'No public record', 'the link that makes it a pattern'),
    ('A commit or a new copy is published', 'residue', 'gaps', 'Event archive: stated hourly, with gaps', 'no pushes in 16 of 24 noon hours since 15 Oct'),
    ('Someone reports it as malicious', 'an observer\u2019s record', True, 'Malware records: only if reported', 'one record\u2019s clock began 8 days on'),
]

out = [svg_open(W, H, TITLE, DESC)]
out.append('<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<line x1="0" y1="0" x2="0" y2="8" stroke="var(--grid)" stroke-width="3"/></pattern>'
           '<marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto">'
           '<path d="M0 0L7 4L0 8" fill="none" stroke="var(--muted)" stroke-width="1.5"/></marker></defs>')
out.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
out.append(f'<text class="head" x="24" y="34">{escape(TITLE)}</text>')
out.append('<text class="sub" x="24" y="56">A scenario, not an observation. Solid: a public record. Dotted: a record with gaps. Hatched: none we know of.</text>')
out.append('<text class="ann" x="64" y="88">Step in the pattern</text>')
out.append('<text class="ann" x="404" y="88">What could register it, and how soon</text>')

top, box_h, gap = 100, 56, 14
x0, bw = 64, 310
for i, (label, layer, public, r1, r2) in enumerate(steps):
    y = top + i * (box_h + gap)
    if public == 'gaps':
        out.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="{box_h}" rx="8" fill="var(--bg)" '
                   f'stroke="var(--teal)" stroke-width="2" stroke-dasharray="2 3"/>')
    elif public:
        out.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="{box_h}" rx="8" fill="var(--bg)" '
                   f'stroke="var(--teal)" stroke-width="2"/>')
    else:
        out.append(f'<rect x="{x0}" y="{y}" width="{bw}" height="{box_h}" rx="8" fill="url(#hatch)" '
                   f'stroke="var(--amber)" stroke-width="2" stroke-dasharray="7 4"/>')
    out.append(f'<text class="sec" x="{x0 + 14}" y="{y + 24}">{escape(label)}</text>')
    out.append(f'<text class="ann" x="{x0 + 14}" y="{y + 43}">{escape(layer)}</text>')
    cls = 'nm'
    out.append(f'<text class="{cls}" x="404" y="{y + 24}">{escape(r1)}</text>')
    out.append(f'<text class="ann" x="404" y="{y + 42}">{escape(r2)}</text>')
    out.append(f'<line x1="{x0 + bw}" y1="{y + box_h / 2}" x2="394" y2="{y + box_h / 2}" class="axis" '
               f'stroke-dasharray="2 3"/>')
    if i < len(steps) - 1 and i != 4:
        out.append(f'<path d="M{x0 + 40} {y + box_h + 2}V{y + box_h + gap - 3}" stroke="var(--muted)" '
                   f'stroke-width="1.5" fill="none" marker-end="url(#arr)"/>')

# loop back from step 5 to step 2: the copy is a new package
y2 = top + 1 * (box_h + gap) + box_h / 2
y5 = top + 4 * (box_h + gap) + box_h / 2
out.append(f'<path d="M{x0} {y5}H40V{y2}H{x0 - 4}" stroke="var(--muted)" stroke-width="1.5" fill="none" '
           f'stroke-dasharray="6 4" marker-end="url(#arr)"/>')
out.append(f'<text class="ann" transform="translate(32 {(y2 + y5) / 2}) rotate(-90)" text-anchor="middle">each copy starts the loop again</text>')
# report step hangs off the side: drawn from step 5 with a dotted connector
y6 = top + 5 * (box_h + gap)
out.append(f'<path d="M{x0 + 120} {y5 + box_h / 2 + 2}V{y6 - 3}" stroke="var(--muted)" stroke-width="1.5" '
           f'stroke-dasharray="2 3" fill="none" marker-end="url(#arr)"/>')
out.append(f'<text class="note" x="24" y="{H - 26}">Running the copies is in no public record we know of. Delays: the instruments\u2019 own pages, a reviewer\u2019s</text>')
out.append(f'<text class="note" x="24" y="{H - 10}">scan of the event archive\u2019s noon hours (1 Oct to 7 Nov 2026), and one OSV record (October 2026).</text>')
out.append('</svg>\n')
Path(__file__).with_name('traces.svg').write_text('\n'.join(out))
print('wrote traces.svg')
