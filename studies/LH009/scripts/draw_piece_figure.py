"""Draws articles/fixes-that-said-so.svg, the piece's figure, from data/lags.csv.

For each window (from the release, stopping at the advisory where it came first; and from the advisory)
and each class, the rate of first moves to the fix per 100 repositories still waiting per day, split by
who made the move. The rates are computed here from lags.csv as analyse.py computes them, and checked
against data/hazard_by_class.csv before anything is drawn. No network.
"""
import csv, os
from datetime import datetime, timedelta
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DATA = os.path.join(ROOT, 'studies/LH009/data')
OUT = os.path.join(ROOT, 'articles/fixes-that-said-so.svg')
L = list(csv.DictReader(open(os.path.join(DATA, 'lags.csv'))))
HZ = [r for r in csv.DictReader(open(os.path.join(DATA, 'hazard_by_class.csv'))) if r['grouping'] == 'class']
D = timedelta(days=1)
def t(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))

WINDOWS = [  # (label, section, start, end, name in hazard_by_class.csv)
    ('days 0 to 2', 'r', lambda r, a: r, lambda r, a: min(r + 2 * D, a), 'release +0 to +2 days, or to the advisory where it came first'),
    ('days 2 to 7', 'r', lambda r, a: r + 2 * D, lambda r, a: min(r + 7 * D, a), 'release +2 to +7 days, stopping at the advisory'),
    ('days 7 to 30', 'r', lambda r, a: r + 7 * D, lambda r, a: min(r + 30 * D, a), 'release +7 to +30 days, stopping at the advisory'),
    ('days 0 to 2', 'a', lambda r, a: a, lambda r, a: a + 2 * D, 'advisory +0 to +2 days'),
    ('days 2 to 7', 'a', lambda r, a: a + 2 * D, lambda r, a: a + 7 * D, 'advisory +2 to +7 days'),
    ('days 7 to 30', 'a', lambda r, a: a + 7 * D, lambda r, a: a + 30 * D, 'advisory +7 to +30 days'),
]
AUTH = ['bot', "person merging a bot's branch", 'person']

def window(cls, s, e):
    moves = {k: 0 for k in AUTH}; days = 0.0
    for r in L:
        if r['cls'] != cls: continue
        rel, adv = t(r['release_time']), t(r['advisory_time'])
        a, b = s(rel, adv), e(rel, adv)
        if b <= a: continue
        stop = t(r['committer_time']) if r['committer_time'] else t(r['end_of_observation'])
        hi = min(b, stop)
        if hi > a: days += (hi - a) / D
        if r['outcome'] == 'moved' and a <= stop < b: moves[r['authorship']] += 1
    return moves, days

rows = []
for lab, sec, s, e, name in WINDOWS:
    for cls in ('announced', 'silent'):
        mv, days = window(cls, s, e)
        n = sum(mv.values()); rate = 100 * n / days
        ref = [h for h in HZ if h['cls'] == cls and h['window'] == name][0]
        assert int(ref['moves']) == n and abs(float(ref['repo_days_at_risk']) - days) < 0.06 and abs(float(ref['moves_per_100_repo_days']) - rate) < 0.006, (cls, name, n, days, rate, ref)
        rows.append((lab, sec, cls, mv, days, n, rate))
        print(sec, lab, cls, n, round(days, 1), round(rate, 2), mv)
pairs = {c: sum(1 for r in L if r['cls'] == c) for c in ('announced', 'silent')}
libs = {c: len({r['library'] for r in L if r['cls'] == c}) for c in ('announced', 'silent')}
assert pairs == {'announced': 152, 'silent': 105} and libs == {'announced': 7, 'silent': 7}, (pairs, libs)

W = 720; X0 = 196; XMAX = 6.0; X1 = 560
def x(v): return X0 + (X1 - X0) * v / XMAX
BH = 15; BG = 4; GG = 16
o = []
top = 176
H = top + 6 * (2 * BH + BG + GG) + 2 * 34 + 150
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">')
o.append('<title id="t">How fast pinned software moved to security fixes whose notes said so and to silent ones, before and after the advisory, fourteen Python libraries, April to September 2026</title>')
desc = ('Horizontal bars in two sections. The first counts days from the fixed release and stops at the advisory where it came first; the second counts days from the advisory. '
        'In each of three windows, days 0 to 2, 2 to 7 and 7 to 30, one bar is for fixes whose own release notes said they fixed a security flaw and one for fixes whose notes, where we could read them, did not. '
        'Each bar is the number of first moves to the fix per 100 repositories still waiting, per day, split by who made the move: a bot, a person merging a bot\'s branch, or a person. ')
parts = []
for lab, sec, cls, mv, days, n, rate in rows:
    parts.append(f"{'after the advisory' if sec == 'a' else 'after the release'}, {lab}, {'said so' if cls == 'announced' else 'silent'}: {rate:.1f} on {n} moves ({mv['bot']} by bots, {mv[AUTH[1]]} merged from a bot, {mv['person']} by people)")
desc += '; '.join(parts) + '. '
desc += ('Before the advisory, the two classes ran at about the same pace in the first two days and from day 7 to day 30; in days 2 to 7 fixes that said so drew moves at about twice the pace, mostly made by people. '
         '257 repository and library pairs, 152 on seven libraries and 105 on seven, one fixed release per library, released 31 March to 23 July 2026, histories read to 27 September 2026.')
o.append(f'<desc id="d">{desc}</desc>')
o.append('''<style>
svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --band:#efeee9; --bot:#2a78d6; --mrg:#9cc3ef; --per:#8a8984; }
@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; --grid:#383835; --band:#2a2a27; --bot:#4b93ea; --mrg:#2c5a8f; --per:#9f9d95; } }
text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }
.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }
.lab { font-size: 14px; font-weight: 600; } .note { font-size: 11.5px; fill: var(--muted); }
.ann { font-size: 12px; fill: var(--ink2); } .ax { font-size: 12px; fill: var(--muted); } .cls { font-size: 12px; fill: var(--ink2); }
.val { font-size: 12px; fill: var(--ink); }
</style>''')
o.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
o.append('<text x="16" y="30" class="head">Before the advisory, fixes that said so drew pins faster, in days 2 to 7</text>')
o.append('<text x="16" y="51" class="sub">First moves to the fix per 100 repositories still waiting, per day, by whether the release\'s own</text>')
o.append('<text x="16" y="68" class="sub">notes said it fixed a security flaw, and by who made the move.</text>')
ly = 98
o.append(f'<rect x="16" y="{ly-10}" width="12" height="12" rx="2" fill="var(--bot)"/><text x="34" y="{ly}" class="ann">a bot wrote it</text>')
o.append(f'<rect x="140" y="{ly-10}" width="12" height="12" rx="2" fill="var(--mrg)" stroke="var(--bot)" stroke-width="1.2"/><text x="158" y="{ly}" class="ann">a person merged a bot\'s branch</text>')
o.append(f'<rect x="366" y="{ly-10}" width="12" height="12" rx="2" fill="var(--per)"/><text x="384" y="{ly}" class="ann">a person</text>')
o.append(f'<text x="16" y="{ly+22}" class="ann"><tspan font-weight="600">said so</tspan>: the changelog, tag message or package description said, at the release, that it fixed a security flaw.</text>')
o.append(f'<text x="16" y="{ly+40}" class="ann"><tspan font-weight="600">silent</tspan>: none of them did, in what we could read.</text>')
# axis
y = top
ends = []
for i, (lab, sec, cls, mv, days, n, rate) in enumerate(rows):
    if i % 6 == 0:
        head = 'Before the advisory, counting days from the release' if sec == 'r' else 'After the advisory, counting days from it'
        o.append(f'<text x="16" y="{y}" class="lab">{head}</text>')
        y += 14
        sec_top = y
    if i % 2 == 0:
        o.append(f'<text x="16" y="{y+BH+BG/2+4:.0f}" class="ann">{lab}</text>')
    o.append(f'<text x="{X0-10}" y="{y+BH-3.5:.1f}" class="cls" text-anchor="end">{"said so" if cls == "announced" else "silent"}</text>')
    cx = X0
    for k, col in zip(AUTH, ['var(--bot)', 'var(--mrg)', 'var(--per)']):
        if not mv[k]: continue
        wv = (x(100 * mv[k] / days) - X0)
        tip = f"{'said so' if cls == 'announced' else 'silent'}, {lab} after the {'release' if sec == 'r' else 'advisory'}: {mv[k]} of {n} moves {'by bots' if k == 'bot' else ('merged from a bot' if k != 'person' else 'by people')}"
        stroke = ' stroke="var(--bot)" stroke-width="1.2"' if k == AUTH[1] else ''
        o.append(f'<rect x="{cx:.1f}" y="{y}" width="{max(wv-2,1):.1f}" height="{BH}" rx="2" fill="{col}"{stroke}><title>{tip}</title></rect>')
        cx += wv
    o.append(f'<text x="{max(cx,X0)+6:.1f}" y="{y+BH-3.5:.1f}" class="val">{rate:.1f}<tspan class="note"> · {n} move{"s" if n != 1 else ""}</tspan></text>')
    y += BH + (BG if i % 2 == 0 else GG)
    if i % 6 == 5:
        for v in range(0, 7):
            o.append(f'<line x1="{x(v):.1f}" y1="{sec_top-4}" x2="{x(v):.1f}" y2="{y-GG+4}" stroke="var(--grid)" stroke-width="1"/>')
            o.append(f'<text x="{x(v):.1f}" y="{y-GG+18}" class="ax" text-anchor="middle">{v}</text>')
        y += 34
# move the grid lines behind the bars
grid = [s for s in o if s.startswith('<line')]
o = [s for s in o if not s.startswith('<line')]
bg_index = [i for i, s in enumerate(o) if s.startswith('<rect width=')][0]
o[bg_index + 1:bg_index + 1] = grid
fy = y - 6
for k, line in enumerate([
    '257 pairs of a repository and a library it pinned or locked at an affected version when the fix came out:',
    '152 on seven libraries whose fix said so and 105 on seven whose fix did not (two more libraries had no',
    'pinned dependents to follow), from the dependents Open Source Insights lists, sampled by a rule fixed in',
    'advance. One fixed release per library, released 31 March to 23 July 2026. Windows from the release stop at',
    'the advisory where it came first. A move is a commit changing what a project asks for, not an installation.',
    'Git histories, the Python Package Index, OSV and Open Source Insights read on 27 September 2026.']):
    o.append(f'<text x="16" y="{fy+16*k}" class="note">{line}</text>')
o.append('</svg>')
H2 = fy + 16 * 5 + 18
o[0] = o[0].replace(f'viewBox="0 0 {W} {H}" width="{W}" height="{H}"', f'viewBox="0 0 {W} {H2}" width="{W}" height="{H2}"')
o = [s.replace(f'<rect width="{W}" height="{H}"', f'<rect width="{W}" height="{H2}"') for s in o]
open(OUT, 'w').write('\n'.join(o) + '\n')
print('wrote', OUT, H2)
