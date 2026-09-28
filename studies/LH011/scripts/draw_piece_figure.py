#!/usr/bin/env python3
"""LH011: draw articles/two-days-for-most.svg, the piece's figure, from data/analysis/release_days.csv
and project_outcomes.csv (offline, no library). One line per project with a qualifying release: for
each day 0 to 30 after release, the median over that project's releases of the at-or-newer share
(censored days, after 27 September 2026, left out of the median). Blue: most of the project's
releases reached half within two days; orange: most did not. A few lines are named at their right
end, greedily, so that names do not collide.

It also prints, for the caller and the review, each project's median day-1 and day-30 shares and
how many projects' day-30 median lies within ten points of their day-1 median: a reading of the
record's own table, not a figure the record states.
Usage: python3 draw_piece_figure.py [out.svg]   (default: articles/two-days-for-most.svg)
The printed reading is kept as data/piece_figure_reading.txt:
  python3 studies/LH011/scripts/draw_piece_figure.py > studies/LH011/data/piece_figure_reading.txt"""
import csv, os, sys, statistics
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(STUDY))
A = os.environ.get('LH011_OUT', os.path.join(STUDY, 'data', 'analysis'))
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'articles', 'two-days-for-most.svg')

proj = {r['project']: r for r in csv.DictReader(open(os.path.join(A, 'project_outcomes.csv'))) if r['releases'] != '0'}
by = defaultdict(lambda: defaultdict(list))
for r in csv.DictReader(open(os.path.join(A, 'release_days.csv'))):
    if r['status'] == 'known' and r['share_at_or_newer']:
        by[r['project']][int(r['day'])].append(float(r['share_at_or_newer']))
series = {p: [(d, statistics.median(by[p][d])) for d in range(31) if by[p].get(d)] for p in proj}
yes = [p for p in proj if proj[p]['most_reached'] == 'yes']
no = [p for p in proj if proj[p]['most_reached'] == 'no']

# the printed reading
print('project, group, releases, median day-1 share, median day-30 share (releases with day 30 held)')
close = 0
for p in sorted(proj, key=lambda p: -dict(series[p]).get(1, 0)):
    s = dict(series[p])
    d30 = s.get(30)
    print(f'{p}, {proj[p]["most_reached"]}, {proj[p]["releases"]}, {s[1] * 100:.1f}, '
          + (f'{d30 * 100:.1f}' if d30 is not None else 'not held'))
    if d30 is not None and abs(d30 - s[1]) <= 0.10:
        close += 1
print(f'projects whose median day-30 share is within 10 points of their median day-1 share: {close} of '
      f'{sum(1 for p in proj if dict(series[p]).get(30) is not None)} with day 30 held')

W, H = 720, 560
X0, X1, Y0, Y1 = 60, 560, 150, 470   # plot box: Y0 top (100%), Y1 bottom (0%)
x = lambda d: X0 + (X1 - X0) * d / 30
y = lambda v: Y1 - (Y1 - Y0) * v
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">')
o.append('<title id="t">Share of each library\'s downloads at a new release or later, day by day for thirty days after release, '
         '37 of the most downloaded Python libraries, releases of April to August 2026</title>')
low = sorted(no, key=lambda p: dict(series[p])[1])
o.append('<desc id="d">A line chart with one line for each of 37 Python libraries. The horizontal axis is days since a '
         'release, from 0 to 30; the vertical axis is the share of that day\'s downloads of the library that were the new '
         'release or a later one, the median over the library\'s releases, from 0 to 100 per cent, with a dashed line at half. '
         f'Every line starts lower on the day of release than the day after, rises on that next day, and then runs nearly flat for the rest of the month. '
         f'{len(yes)} lines, in blue, are libraries where most releases reached half within two days; they sit between about '
         '49 and 85 per cent from day 1 onwards. '
         f'{len(no)} lines, in orange, are libraries where none did; they sit between about 2 and 37 per cent all month: '
         + ', '.join(f'{p} {dict(series[p])[1] * 100:.0f}' for p in low)
         + ' per cent on day 1. ClickPy\'s copy of the Python Package Index download log, read 28 September 2026.</desc>')
o.append('''<style>
svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --band:#efeee9; --a:#2a78d6; --b:#eb6834; }
@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; --grid:#383835; --band:#2a2a27; --a:#3987e5; --b:#d95926; } }
text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }
.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }
.ann { font-size: 12px; fill: var(--ink2); } .ax { font-size: 12px; fill: var(--muted); } .nm { font-size: 11px; fill: var(--ink2); }
.note { font-size: 11.5px; fill: var(--muted); }
</style>''')
o.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
o.append('<text x="16" y="30" class="head">The day after a release set its share for the month</text>')
o.append('<text x="16" y="51" class="sub">Share of each library\'s daily downloads that were the new release or a later one,</text>')
o.append('<text x="16" y="68" class="sub">median over the library\'s releases, by days since release. One line per library.</text>')
# legend
o.append(f'<line x1="16" y1="96" x2="40" y2="96" stroke="var(--a)" stroke-width="2.5"/>'
         f'<text x="48" y="100" class="ann">most releases reached half within two days ({len(yes)} libraries)</text>')
o.append(f'<line x1="16" y1="118" x2="40" y2="118" stroke="var(--b)" stroke-width="2.5" stroke-dasharray="6 3"/>'
         f'<text x="48" y="122" class="ann">none did ({len(no)} libraries)</text>')
# days 1 and 2 band, grid, axes
o.append(f'<rect x="{x(0.5):.1f}" y="{Y0}" width="{x(2.5) - x(0.5):.1f}" height="{Y1 - Y0}" fill="var(--band)"/>')
o.append(f'<text x="{x(1.5):.1f}" y="{Y0 - 6}" class="ax" text-anchor="middle">days 1 and 2</text>')
for v in (0, 0.25, 0.5, 0.75, 1):
    if v == 0.5:
        o.append(f'<line x1="{X0}" y1="{y(v):.1f}" x2="{X1}" y2="{y(v):.1f}" stroke="var(--ink2)" stroke-width="1" stroke-dasharray="4 3"/>')
    else:
        o.append(f'<line x1="{X0}" y1="{y(v):.1f}" x2="{X1}" y2="{y(v):.1f}" stroke="var(--grid)" stroke-width="1"/>')
    o.append(f'<text x="{X0 - 8}" y="{y(v) + 4:.1f}" class="ax" text-anchor="end">{int(v * 100)}%</text>')
o.append(f'<text x="{X1 - 4}" y="{y(0.5) + 14:.1f}" text-anchor="end" class="ann">half</text>')
for d in (0, 1, 2, 7, 14, 21, 30):
    o.append(f'<line x1="{x(d):.1f}" y1="{Y1}" x2="{x(d):.1f}" y2="{Y1 + 4}" stroke="var(--muted)" stroke-width="1"/>')
    o.append(f'<text x="{x(d):.1f}" y="{Y1 + 18}" class="ax" text-anchor="middle">{d}</text>')
o.append(f'<text x="{(X0 + X1) / 2:.0f}" y="{Y1 + 36}" class="ax" text-anchor="middle">days since the release (day 0 is the day of upload, in UTC)</text>')


def path(p):
    return 'M' + ' L'.join(f'{x(d):.1f},{y(v):.1f}' for d, v in series[p])


for group, col, dash in ((yes, 'var(--a)', ''), (no, 'var(--b)', ' stroke-dasharray="6 3"')):
    for p in sorted(group):
        s = dict(series[p])
        tip = (f'{p}: {proj[p]["releases"]} releases, {proj[p]["reached"]} reached half within two days; '
               f'median share {s[1] * 100:.0f}% on day 1' + (f', {s[30] * 100:.0f}% on day 30' if 30 in s else ''))
        o.append(f'<path d="{path(p)}" fill="none" stroke="{col}" stroke-width="1.6" stroke-linejoin="round" opacity="0.85"{dash}>'
                 f'<title>{tip}</title></path>')

# names at the right end, greedy by priority: a name whose line ends within 4 px of a placed name joins
# it; otherwise it is placed only if at least 13 px from every placed name
prio = ['boto3', 'aiobotocore', 'numpy', 'botocore', 'litellm', 's3transfer', 'pandas', 'protobuf', 'grpcio-status',
        'requests', 'packaging', 'certifi', 'urllib3', 'pydantic', 'starlette', 'cryptography']
placed = []   # [y, [names]]
for p in prio:
    if p not in series:
        continue
    d, v = series[p][-1]
    yy = y(v) + 4
    near = [q for q in placed if abs(yy - q[0]) < 4]
    if near:
        near[0][1].append(p)
    elif all(abs(yy - q[0]) >= 13 for q in placed):
        placed.append([yy, [p]])
for yy, names in placed:
    o.append(f'<text x="{X1 + 8}" y="{yy:.1f}" class="nm">{", ".join(names)}</text>')

o.append(f'<text x="16" y="{H - 30}" class="note">37 of the 50 most downloaded Python projects in August 2026, 424 releases uploaded April to August 2026.</text>')
o.append(f'<text x="16" y="{H - 13}" class="note">ClickPy&#8217;s public copy of the Python Package Index download log, read 28 September 2026; no day after 27 September.</text>')
o.append('</svg>')
open(out, 'w').write('\n'.join(o) + '\n')
print('wrote', out, file=sys.stderr)
