#!/usr/bin/env python3
"""LH033: draw studies/LH033/figure.svg from the latest read's tables.json and LH011's retained table (offline, no library).

Top: Censys's patched share of version-reporting services in each fixed PHP branch, by day since 21 October 2026
(completed days only), against the range of LH008's four Python security fixes' at-or-newer download shares and the
median over the 37 LH011 projects of their releases' median share, by day since release. Different units, one axis
of shares; the figure says so. Bottom: version-reporting PHP services on the latest completed day, split into patched,
not yet patched in a fixed branch, and on a branch with no fix (Censys's classes).
Usage: python3 draw_figure.py [read label] [out.svg]   (defaults: the latest read holding Censys; studies/LH033/figure.svg)
"""
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
import csv
import json
import statistics
import sys

STUDY = Path(__file__).resolve().parents[1]
reads = sorted(p for p in (STUDY / 'data').glob('read-*') if (p / 'tables.json').exists()
               and 'm1_patched_share_by_branch' in json.loads((p / 'tables.json').read_text()))
read = STUDY / 'data' / ('read-' + sys.argv[1]) if len(sys.argv) > 1 else reads[-1]
out = Path(sys.argv[2]) if len(sys.argv) > 2 else STUDY / 'figure.svg'
t = json.loads((read / 'tables.json').read_text())
m1 = {b: sorted((int(d), v['share']) for d, v in s.items()) for b, s in t['m1_patched_share_by_branch'].items()}
m2 = t['m2_unfixed_tail']
last = max(int(d) for d in m2)
tail = m2[str(last)]
last_date = date(2026, 10, 21) + timedelta(days=last)

FIXES = {('urllib3', '2.7.0'), ('cryptography', '48.0.1'), ('pyjwt', '2.13.0'), ('starlette', '1.1.0')}
fix = defaultdict(dict)
proj = defaultdict(lambda: defaultdict(list))
for r in csv.DictReader(open(STUDY.parent / 'LH011/data/analysis/release_days.csv')):
    if r['status'] != 'known' or not r['share_at_or_newer']:
        continue
    d, v = int(r['day']), float(r['share_at_or_newer'])
    proj[r['project']][d].append(v)
    if (r['project'], r['version']) in FIXES:
        fix[(r['project'], r['version'])][d] = v
days = range(31)
lo = [min(f[d] for f in fix.values()) for d in days]
hi = [max(f[d] for f in fix.values()) for d in days]
med = [statistics.median(statistics.median(p[d]) for p in proj.values() if p.get(d)) for d in days]

W, H = 720, 700
X0, X1, Y0, Y1 = 60, 600, 160, 440
x = lambda d: X0 + (X1 - X0) * d / 30
y = lambda v: Y1 - (Y1 - Y0) * v
pct = lambda v: f'{v * 100:.0f}%'
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">']
o.append('<title id="t">The PHP emergency fix by Censys\'s count of internet-facing services, beside how Python security fixes '
         f'reached downloads, to {last_date.day} October 2026</title>')
ends = ', '.join(f'{b} {s[-1][1] * 100:.1f}%' for b, s in sorted(m1.items(), key=lambda kv: -kv[1][-1][1]))
o.append('<desc id="d">Two charts. The first is a line chart: the horizontal axis is days since release, 0 to 30; the vertical axis '
         'is a share from 0 to 100 per cent, with a dashed line at half. Four blue lines, one per PHP branch, show the share of '
         'version-reporting internet-facing PHP services in that branch that Censys counts as patched, by day since PHP\'s release '
         f'on 21 October 2026. They start near 2 to 4 per cent on day 0, climb steeply on days 1 and 2 and stop at day {last}, '
         f'the last completed day read: {ends}. An orange band shows the range of four Python security fixes\' share of their '
         f'library\'s daily downloads, from {pct(lo[1])} to {pct(hi[1])} on day 1 and {pct(lo[30])} to {pct(hi[30])} on day 30, nearly flat; '
         f'a dashed orange line shows the median over 37 Python libraries, {pct(med[1])} on day 1 and {pct(med[30])} on day 30. The two '
         'measure different things: services as last scanned, and downloads in a day. The second chart is one bar splitting the '
         f'{tail["versioned"] / 1e6:.1f} million PHP services that reported a version on {last_date.day} October: '
         f'{tail["patched"] / 1e6:.1f} million patched, {tail["affected"] / 1e6:.1f} million in fixed branches not yet counted patched, '
         f'and {tail["affected_nofix"] / 1e6:.1f} million on branches PHP did not fix. A further {tail["unknown"] / 1e6:.1f} million '
         'reported no version. Sources: Censys ARC\'s PHP2Shell dashboard, read by Lighthouse; ClickPy\'s copy of the Python '
         'Package Index download log, read 28 September 2026.</desc>')
o.append('''<style>
svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --a:#2a78d6; --b:#eb6834; --wait:#b9b7b0; --hatch:#52514e; }
@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; --grid:#383835; --a:#3987e5; --b:#d95926; --wait:#5c5b56; --hatch:#c3c2b7; } }
text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }
.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }
.ann { font-size: 12px; fill: var(--ink2); } .ax { font-size: 12px; fill: var(--muted); } .nm { font-size: 12px; fill: var(--ink); font-weight: 600; }
.note { font-size: 11.5px; fill: var(--muted); } .sec { font-size: 14px; font-weight: 600; }
</style>''')
o.append('<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="6" height="6" fill="var(--bg)"/><line x1="0" y1="0" x2="0" y2="6" stroke="var(--hatch)" stroke-width="2"/></pattern></defs>')
o.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
span_words = f'{WORDS[last]} day' if last < len(WORDS) else f'{last} day'
o.append(f'<text x="16" y="30" class="head">PHP\'s emergency fix, {span_words}{"s" if last != 1 else ""} in, beside Python fixes\' downloads</text>')
o.append('<text x="16" y="51" class="sub">PHP: share of internet-facing services in each fixed branch that Censys counts as patched.</text>')
o.append('<text x="16" y="68" class="sub">Python: share of a library\'s daily downloads at the fixed release or later. Different units; see below.</text>')
o.append(f'<line x1="16" y1="98" x2="40" y2="98" stroke="var(--a)" stroke-width="2.5"/>'
         f'<text x="48" y="102" class="ann">PHP branch, from 21 October 2026 (Censys); stops at the last completed day read</text>')
o.append(f'<rect x="16" y="113" width="24" height="12" rx="2" fill="var(--b)" opacity="0.28"/>'
         f'<text x="48" y="123" class="ann">range of four Python security fixes, 2026 (urllib3, cryptography, pyjwt, starlette)</text>')
o.append(f'<line x1="16" y1="140" x2="40" y2="140" stroke="var(--b)" stroke-width="2" stroke-dasharray="5 3"/>'
         f'<text x="48" y="144" class="ann">median over 37 of the most downloaded Python libraries\' releases</text>')
for v in (0, 0.25, 0.5, 0.75, 1):
    style = 'stroke="var(--ink2)" stroke-dasharray="4 3"' if v == 0.5 else 'stroke="var(--grid)"'
    o.append(f'<line x1="{X0}" y1="{y(v):.1f}" x2="{X1}" y2="{y(v):.1f}" {style} stroke-width="1"/>')
    o.append(f'<text x="{X0 - 8}" y="{y(v) + 4:.1f}" class="ax" text-anchor="end">{int(v * 100)}%</text>')
o.append(f'<text x="{X1 - 4}" y="{y(0.5) - 6:.1f}" text-anchor="end" class="ann">half</text>')
for d in (0, 1, 2, 3, 7, 14, 21, 30):
    o.append(f'<line x1="{x(d):.1f}" y1="{Y1}" x2="{x(d):.1f}" y2="{Y1 + 4}" stroke="var(--muted)" stroke-width="1"/>')
    o.append(f'<text x="{x(d):.1f}" y="{Y1 + 18}" class="ax" text-anchor="middle">{d}</text>')
o.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{Y1 + 36}" class="ax" text-anchor="middle">days since the release (day 0 is the release day, UTC)</text>')
band = ' L'.join(f'{x(d):.1f},{y(hi[d]):.1f}' for d in days) + ' L' + ' L'.join(f'{x(d):.1f},{y(lo[d]):.1f}' for d in reversed(days))
o.append(f'<path d="M{band} Z" fill="var(--b)" opacity="0.28"><title>Four Python security fixes: {pct(lo[1])} to {pct(hi[1])} '
         f'of downloads on day 1, {pct(lo[30])} to {pct(hi[30])} on day 30</title></path>')
o.append('<path d="M' + ' L'.join(f'{x(d):.1f},{y(med[d]):.1f}' for d in days) + '" fill="none" stroke="var(--b)" stroke-width="2" '
         f'stroke-dasharray="5 3"><title>Median over 37 Python libraries: {pct(med[1])} on day 1, {pct(med[30])} on day 30</title></path>')
labels = []
for b, s in sorted(m1.items()):
    o.append('<path d="M' + ' L'.join(f'{x(d):.1f},{y(v):.1f}' for d, v in s) + '" fill="none" stroke="var(--a)" stroke-width="2" '
             'stroke-linejoin="round"/>')
    for d, v in s:
        o.append(f'<circle cx="{x(d):.1f}" cy="{y(v):.1f}" r="4" fill="var(--a)" stroke="var(--bg)" stroke-width="2">'
                 f'<title>PHP {b}, day {d}: {pct(v)} of version-reporting services counted patched</title></circle>')
    labels.append([y(s[-1][1]) + 4, f'{b}  {s[-1][1] * 100:.1f}%', s[-1][0]])  # one decimal: 49.6 must not read as half
labels.sort()
for i in range(1, len(labels)):   # keep names 14 px apart
    labels[i][0] = max(labels[i][0], labels[i - 1][0] + 14)
for yy, text, d in labels:
    o.append(f'<text x="{x(d) + 10:.1f}" y="{yy:.1f}" class="nm">{text}</text>')
o.append(f'<text x="{x(30) + 6:.1f}" y="{y(hi[30]) - 6:.1f}" class="ann" text-anchor="end">Python, day 30</text>')

BY, BH = 560, 34
o.append(f'<text x="16" y="{BY - 34}" class="sec">PHP services that reported a version, {last_date.day} October 2026: '
         f'{tail["versioned"] / 1e6:.1f} million</text>')
parts = [('patched', tail['patched'], 'var(--a)', 'patched'),
         ('waiting', tail['affected'], 'var(--wait)', 'not yet patched'),
         ('nofix', tail['affected_nofix'], 'url(#hatch)', 'on a branch with no fix (8.1 and older)')]
bx, total, span = 16.0, tail['versioned'], W - 32
for i, (k, n, fill, name) in enumerate(parts):
    w = span * n / total - (2 if i < 2 else 0)
    o.append(f'<rect x="{bx:.1f}" y="{BY - 16}" width="{w:.1f}" height="{BH}" rx="3" fill="{fill}"'
             + (' stroke="var(--hatch)" stroke-width="1"' if k == 'nofix' else '')
             + f'><title>{name}: {n / 1e6:.1f} million ({n / total * 100:.0f}%)</title></rect>')
    o.append(f'<text x="{bx:.1f}" y="{BY + BH + 2}" class="ann">{name}</text>')
    o.append(f'<text x="{bx:.1f}" y="{BY + BH + 18}" class="nm">{n / 1e6:.1f} million, {n / total * 100:.0f}%</text>')
    bx += w + 2
o.append(f'<text x="16" y="{H - 46}" class="note">Not yet patched: in a fixed branch, not yet counted patched. Patched shares are floors, not estimates: distributions</text>')
o.append(f'<text x="16" y="{H - 31}" class="note">that backport the fix keep the old version number, and a rescan must see the change. {tail["unknown"] / 1e6:.1f} million more reported no version.</text>')
o.append(f'<text x="16" y="{H - 13}" class="note">Censys ARC PHP2Shell, read {read.name[5:15]} (LH033); counts services, not machines. ClickPy, read 28 Sept 2026 (LH011).</text>')
o.append('</svg>')
out.write_text('\n'.join(o) + '\n')
print('wrote', out, file=sys.stderr)
