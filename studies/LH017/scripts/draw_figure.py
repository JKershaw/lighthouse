#!/usr/bin/env python3
"""LH017: draw ci.svg from data/pairs.csv and job_classes.csv and LH015's data/pair_classes.csv and recipe_classes.csv
(offline). Two groups of two bars, container recipes (LH015) above CI workflows (this study): whether some build installs
the library's version from the pinned file, and, for pairs with a timed lockfile, from the lockfile itself. Each bar is
the pairs where that kind of build installs the project's requirements or could not be decided: reads it (blue), reads
the lockfile only through a command that may re-lock (blue, striped; lockfile group only), does not (orange), could not
be decided (grey, hatched). Counts are labelled where a segment is wide enough; every segment carries a native tooltip.
Colour tokens, marks and plain SVG follow studies/LH015/scripts/draw_figure.py, whose blue and orange pair was checked
with the dataviz skill's validate_palette.js (light on #fcfcfb, dark on #1a1a19).
Usage: python3 draw_figure.py [out.svg]   (default: studies/LH017/ci.svg)"""
import csv
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
D = os.path.join(STUDY, 'data')
L15 = os.path.join(os.path.dirname(STUDY), 'LH015', 'data')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(STUDY, 'ci.svg')

P = [r for r in csv.DictReader(open(os.path.join(D, 'pairs.csv'))) if r['status'] == 'read']
jc = defaultdict(list)
for r in csv.DictReader(open(os.path.join(D, 'job_classes.csv'))):
    jc[r['pair_id']].append(r)
l15 = {r['pair_id']: r for r in csv.DictReader(open(os.path.join(L15, 'pair_classes.csv')))}
l15b = defaultdict(list)
for r in csv.DictReader(open(os.path.join(L15, 'recipe_classes.csv'))):
    if r['role'] == 'snapshot':
        l15b[r['pair_id']].append(r)
LOCK = ('lockfile', 'both')

# container recipes (LH015)
rp = {'reads': sum(1 for r in l15.values() if r['pair_class'] == 'from the pinned file'),
      'not': sum(1 for r in l15.values() if r['pair_class'] == 'not from the pinned file'),
      'und': sum(1 for r in l15.values() if r['pair_class'] == 'undetermined')}
rl_dec = [p for p, r in l15.items() if r['pin_class'] in LOCK and r['pair_class'] in ('from the pinned file', 'not from the pinned file')]
rl_reads = [p for p in rl_dec if l15[p]['reads_T_lock'] == 'yes']
rl_relock = [p for p in rl_reads if all('may re-lock' in b['flags'] for b in l15b[p] if b['class'] == '1' and b['T_lock'] == 'yes')]
rl = {'reads': len(rl_reads) - len(rl_relock), 'relock': len(rl_relock), 'not': len(rl_dec) - len(rl_reads),
      'und': sum(1 for r in l15.values() if r['pin_class'] in LOCK and r['pair_class'] == 'undetermined')}
# CI workflows (this study)
cp = {'reads': sum(1 for r in P if r['pair_class'] == 'reads the pin'),
      'not': sum(1 for r in P if r['pair_class'] == 'does not read the pin'),
      'und': sum(1 for r in P if r['pair_class'] == 'undetermined')}
cl_reads = [r['pair_id'] for r in P if r['lock_class'] == 'reads the timed lock']
cl_relock = [p for p in cl_reads if all('may re-lock' in j['flags'] for j in jc[p] if j['final_class'] == '1' and j['T_lock'] == 'yes')]
cl = {'reads': len(cl_reads) - len(cl_relock), 'relock': len(cl_relock),
      'not': sum(1 for r in P if r['lock_class'] == 'does not'), 'und': sum(1 for r in P if r['lock_class'] == 'undetermined')}

SEG = [('reads', 'fa', 'installs from it'), ('relock', 'fr', 'only through a command that may re-lock'),
       ('not', 'fb', 'does not install from it'), ('und', 'fu', 'could not be decided')]
GROUPS = [('Some build installs the version from the pin or lockfile', [('Container recipes', rp), ('CI workflows', cp)]),
          ('Some build installs it from the lockfile itself (projects with a timed lockfile)',
           [('Container recipes', rl), ('CI workflows', cl)])]

W, L, R = 720, 150, 24
bw = W - L - R
BH, RH = 24, 40
esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;').replace("'", '&#39;')
y0 = 146
H = y0 + 2 * (30 + 2 * RH) + 56
e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     'aria-label="For 469 moments when a Python project pinned or locked a widely used library, whether its container '
     'recipes and its CI workflows install the library from the pinned file, and from the lockfile itself, with the '
     'cases that could not be decided">']
e.append('<style>svg{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--a:#2a78d6;--b:#eb6834;--u:#a9a8a2;--n:#d6d5cf;--on:#ffffff}'
         '@media (prefers-color-scheme: dark){svg{--bg:#1a1a19;--ink:#ffffff;--ink2:#c3c2b7;--a:#3987e5;--b:#d95926;'
         '--u:#6f6e69;--n:#4a4945;--on:#ffffff}}'
         'text{font:12px system-ui,-apple-system,Segoe UI,sans-serif;fill:var(--ink2)}.t{fill:var(--ink);font-weight:600}'
         '.s{font-size:11px}.v{fill:var(--on);font-size:11px;font-weight:600}.d{fill:var(--ink);font-size:11px;font-weight:600}'
         '.fa{fill:var(--a)}.fr{fill:url(#stripe)}.fb{fill:var(--b)}.fu{fill:url(#hatch)}</style>')
e.append('<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="6" height="6" fill="var(--n)"/><rect width="2.2" height="6" fill="var(--u)"/></pattern>'
         '<pattern id="stripe" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(135)">'
         '<rect width="6" height="6" fill="var(--a)"/><rect width="1.8" height="6" fill="var(--bg)"/></pattern></defs>')
e.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
e.append('<text x="16" y="24" class="t">Whether a pinned project\'s own builds install what its pin or lockfile names</text>')
e.append('<text x="16" y="42" class="s">469 moments, from 2025 to 2026, when one of 332 Python projects held an older version of a library in a pin or</text>')
e.append('<text x="16" y="58" class="s">lockfile as a new release came out; each kind of build\'s instructions read at the project\'s last commit before it</text>')
for j, (key, cls, label) in enumerate(SEG):
    lx = (16, 136, 402, 562)[j]
    e.append(f'<rect x="{lx}" y="{84 - 9}" width="11" height="11" rx="2" class="{cls}"/>')
    e.append(f'<text x="{lx + 16}" y="84" class="s">{esc(label)}</text>')
e.append('<text x="16" y="106" class="s">Each bar counts the moments at which the project\'s builds of that kind install its requirements, or at which</text>')
e.append('<text x="16" y="122" class="s">the rules could not decide; a project appears once for each moment.</text>')
y = y0
for gname, rows in GROUPS:
    e.append(f'<text x="16" y="{y + 12}" class="t">{esc(gname)}</text>')
    y += 24
    for name, c in rows:
        n = sum(c.values())
        e.append(f'<text x="16" y="{y + BH / 2 + 1}" class="t">{esc(name)}</text>')
        e.append(f'<text x="16" y="{y + BH / 2 + 15}" class="s">{n} moments</text>')
        x = L
        for key, cls, label in SEG:
            k = c.get(key, 0)
            if not k:
                continue
            w = bw * k / n
            gap = 2 if x > L else 0
            e.append(f'<rect x="{x + gap:.1f}" y="{y}" width="{max(w - gap, 0.5):.1f}" height="{BH}" rx="3" class="{cls}">'
                     f'<title>{esc(name)}: {esc(label)}, {k} of {n} ({100 * k / n:.1f} per cent)</title></rect>')
            if w >= 22:
                lab_cls = 'v' if key in ('reads', 'not', 'relock') else 'd'
                if key == 'relock':
                    lw = 8 + 7 * len(str(k))
                    e.append(f'<rect x="{x + w / 2 + gap / 2 - lw / 2:.1f}" y="{y + 5}" width="{lw}" height="{BH - 10}" rx="3" class="fa"/>')
                e.append(f'<text x="{x + w / 2 + gap / 2:.1f}" y="{y + BH / 2 + 4}" text-anchor="middle" class="{lab_cls}">{k}</text>')
            x += w
        y += RH
    y += 6
e.append(f'<text x="16" y="{H - 30}" class="s">A recipe is not a build and a workflow is not a run: nothing here shows which builds ran, how often or with what cache.</text>')
e.append(f'<text x="16" y="{H - 14}" class="s">Container recipes read on 29 September 2026, CI workflows on 30 September 2026, from the projects\' public repositories.</text>')
e.append('</svg>')
open(out, 'w').write('\n'.join(e) + '\n')
print(out, {'recipes pin': rp, 'CI pin': cp, 'recipes lock': rl, 'CI lock': cl})
