#!/usr/bin/env python3
"""LH006: draws the reader's figure, articles/what-an-image-holds.svg, from data/image_timeline.csv,
data/project_mcp_pins_git.csv and data/project_mcp_pins_pypi.csv.

One row per project whose images gave an installed mcp version (jesse's gave none and is left out).
Each tick is one image whose installed mcp was read, at its configured build time, coloured by
whether it held a version older than 1.27.0 or 1.27.0 and later. The line under the ticks is the
version the project named: its git lockfile (agentcrew, serena, mcp-snowflake-server, from the
first lockfile commit in the span read) or, where there is no public repository or no git record,
its published package's exact requirement on PyPI (keboola, octobot). The diamond is the first
point at which that named version is 1.27.0 or later. Usage: python3 draw_piece_figure.py"""
import datetime, os
from common import read_csv, STUDY

OUT = os.path.join(STUDY, '..', '..', 'articles', 'what-an-image-holds.svg')
X0, X1 = datetime.datetime(2026, 3, 19), datetime.datetime(2026, 5, 31)
REL = datetime.datetime(2026, 4, 2, 14, 48)
W = 720
L, R = 200, 24
TOP = 158          # first row centre
ROW = 64
# (image repository, label, note, package, where the named version comes from)
ROWS = [('docker.io/daltonnyx/agentcrew', 'agentcrew', 'image installs from a range', 'agentcrew-ai', 'git'),
        ('ghcr.io/oraios/serena', 'serena', 'image installs from a pin', 'serena-agent', 'git'),
        ('docker.io/keboola/mcp-server', 'keboola mcp-server', 'package pins exactly', 'keboola-mcp-server', 'pypi'),
        ('docker.io/nsphung/mcp-snowflake-server-nsp', 'mcp-snowflake-server', 'image uses its lockfile', 'mcp-snowflake-server-nsp', 'git'),
        ('docker.io/drakkarsoftware/octobot', 'octobot', 'package pins exactly', 'octobot', 'pypi')]


def dt(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(datetime.timezone.utc).replace(tzinfo=None)


def x(t):
    return L + (W - L - R) * (t - X0).total_seconds() / (X1 - X0).total_seconds()


def is_new(v):
    v = v.replace('mcp', '').lstrip('=<>~! ')
    parts = [int(p) for p in v.split('.')[:2]]
    return parts >= [1, 27]


def named_versions(pkg, src, git, pypi):
    """Sorted (time, version) at which the project's named version changed."""
    ev = []
    if src == 'git':
        for r in git:
            if r['package'] == pkg and r['kind'] == 'lock':
                ev.append((dt(r['committed_utc']), r['mcp']))
    else:
        for r in pypi:
            if r['package'] == pkg and r['requires_mcp'].startswith('mcp=='):
                ev.append((dt(r['published_utc']), r['requires_mcp'][5:]))
    ev.sort()
    out = []
    for t, v in ev:
        if not out or out[-1][1] != v:
            out.append((t, v))
    return out


def main():
    tl = read_csv('image_timeline.csv')
    git = read_csv('project_mcp_pins_git.csv')
    pypi = read_csv('project_mcp_pins_pypi.csv')
    H = TOP + ROW * (len(ROWS) - 1) + 70
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
         '<title id="t">Which mcp each published image installed, against what each project named, 19 March to 30 May 2026</title>',
         '<desc id="d">One row for each of five projects. Each tick is one published image of the project, placed at the time it was built '
         'and coloured by the version of the library mcp installed inside it: orange for a version older than 1.27.0, blue for 1.27.0 or later. '
         'The line beneath is the version the project itself named, in its git lockfile or, for keboola and octobot, in its published package, '
         'and the diamond marks when that named version first became 1.27.0. mcp 1.27.0 was released on 2 April. '
         'agentcrew\'s images held 1.27.0 from 8 April, 16 days before its lockfile moved on 24 April. serena\'s images moved on 27 April, three days after its pin. '
         'keboola\'s moved on 17 April, three days before its package release requiring 1.27.0. mcp-snowflake-server\'s held 1.14.0 until 6 May and moved 11 minutes after its pin. '
         'octobot\'s held 1.26.0, and its next image, on 30 July, still did. A sixth project, jesse, is left out: the one image of it read held no mcp.</desc>',
         '<style>',
         'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --old:#eb6834; --new:#2a78d6; }',
         '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; --grid:#383835; --old:#e0703f; --new:#3987e5; } }',
         'text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }',
         '.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }',
         '.lab { font-size: 13.5px; font-weight: 600; } .note { font-size: 12px; fill: var(--muted); }',
         '.ann { font-size: 12px; fill: var(--ink2); } .ax { font-size: 12px; fill: var(--muted); }',
         '</style>',
         f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
         '<text x="16" y="30" class="head">What each image installed, and what its project had named</text>',
         '<text x="16" y="51" class="sub">Each tick is one published image at its build time, coloured by the mcp inside it.</text>',
         '<text x="16" y="69" class="sub">The line beneath is the version the project named in its lockfile or published package.</text>']
    # legend
    ly = 94
    o += [f'<rect x="16" y="{ly-12}" width="4" height="15" rx="1" fill="var(--old)"/>',
          f'<text x="26" y="{ly}" class="ann">older than 1.27.0</text>',
          f'<rect x="146" y="{ly-12}" width="4" height="15" rx="1" fill="var(--new)"/>',
          f'<text x="156" y="{ly}" class="ann">1.27.0 or later</text>',
          f'<path d="M272,{ly-4.5} l6,-6 l6,6 l-6,6 z" fill="var(--ink)"/>',
          f'<text x="290" y="{ly}" class="ann">project first names 1.27.0</text>']
    ytop, ybot = TOP - 34, TOP + ROW * (len(ROWS) - 1) + 26
    # axis grid
    for d in (datetime.datetime(2026, 4, 1), datetime.datetime(2026, 4, 15), datetime.datetime(2026, 5, 1), datetime.datetime(2026, 5, 15)):
        xx = x(d)
        o.append(f'<line x1="{xx:.1f}" y1="{ytop}" x2="{xx:.1f}" y2="{ybot}" stroke="var(--grid)" stroke-width="1"/>')
        o.append(f'<text x="{xx:.1f}" y="{ybot+18}" class="ax" text-anchor="middle">{d.day} {d.strftime("%B")}</text>')
    xr = x(REL)
    o.append(f'<line x1="{xr:.1f}" y1="{ytop-8}" x2="{xr:.1f}" y2="{ybot}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 3"/>')
    o.append(f'<text x="{xr-6:.1f}" y="{ytop-2}" class="ann" text-anchor="end">mcp 1.27.0 released, 2 April</text>')
    firsts = {}
    for i, (img, lab, note, pkg, src) in enumerate(ROWS):
        y = TOP + ROW * i
        o.append(f'<text x="16" y="{y-2}" class="lab">{lab}</text>')
        o.append(f'<text x="16" y="{y+14}" class="note">{note}</text>')
        # the named version, as a line
        ev = named_versions(pkg, src, git, pypi)
        segs = []
        for j, (t, v) in enumerate(ev):
            t1 = ev[j + 1][0] if j + 1 < len(ev) else X1
            a, b = max(t, X0), min(t1, X1)
            if b > a:
                segs.append((a, b, v))
        for a, b, v in segs:
            c = 'var(--new)' if is_new(v) else 'var(--old)'
            o.append(f'<line x1="{x(a):.1f}" y1="{y+12}" x2="{x(b):.1f}" y2="{y+12}" stroke="{c}" stroke-width="3" stroke-opacity="0.55"/>')
        fn = next((t for t, v in ev if is_new(v)), None)
        if fn and X0 <= fn <= X1:
            fx = x(fn)
            o.append(f'<path d="M{fx:.1f},{y+5} l7,7 l-7,7 l-7,-7 z" fill="var(--ink)" stroke="var(--bg)" stroke-width="1.5"/>')
        # images
        imgs = sorted((dt(r['created_utc']), r['mcp_installed']) for r in tl
                      if r['image'] == img and r['mcp_installed'] and X0 <= dt(r['created_utc']) <= X1)
        first_new = next((t for t, v in imgs if is_new(v)), None)
        firsts[pkg] = (first_new, fn)
        for t, v in imgs:
            c = 'var(--new)' if is_new(v) else 'var(--old)'
            o.append(f'<rect x="{x(t)-2:.1f}" y="{y-14}" width="4" height="18" rx="1" fill="{c}" stroke="var(--bg)" stroke-width="0.75"/>')
        # annotations, placed by hand from the same data
        if pkg == 'agentcrew-ai':
            a, b = x(first_new), x(fn)
            o.append(f'<path d="M{a:.1f},{y-19} v-5 H{b:.1f} v5" fill="none" stroke="var(--ink2)" stroke-width="1"/>')
            o.append(f'<text x="{(a+b)/2:.1f}" y="{y-28}" class="ann" text-anchor="middle">16 days ahead of its lockfile</text>')
        elif pkg == 'serena-agent':
            o.append(f'<text x="{x(first_new)-8:.1f}" y="{y-20}" class="ann" text-anchor="end">3 days after its pin</text>')
        elif pkg == 'keboola-mcp-server':
            o.append(f'<text x="{x(first_new)+10:.1f}" y="{y-20}" class="ann">3 days before its package release</text>')
        elif pkg == 'mcp-snowflake-server-nsp':
            o.append(f'<text x="{x(imgs[0][0])-8:.1f}" y="{y-2}" class="ann" text-anchor="end">held 1.14.0 until its pin moved</text>')
            o.append(f'<text x="{x(first_new):.1f}" y="{y-20}" class="ann" text-anchor="middle">11 minutes after its pin</text>')
        elif pkg == 'octobot':
            o.append(f'<text x="{x(datetime.datetime(2026, 4, 12)):.1f}" y="{y-2}" class="ann">next image, 30 July: still 1.26.0 →</text>')
    o.append(f'<text x="16" y="{H-12}" class="note">Registries read 26 September 2026. Build times from each image\'s configuration, UTC.</text>')
    o.append('</svg>')
    with open(OUT, 'w') as f:
        f.write('\n'.join(o) + '\n')
    for k, (a, b) in firsts.items():
        print(k, 'first image with 1.27+:', a, '| first named:', b)


if __name__ == '__main__':
    main()
