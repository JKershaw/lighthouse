#!/usr/bin/env python3
"""LH007: draws the reader's figure, articles/<slug>.svg, from data/image_timeline.csv and data/pin_movers.csv.

One row per image repository with an installed mcp read and at least one image built between 32 days
before and 44 days after mcp 1.28.0 (the 11 of installed.svg), in two groups by how the images install:
from an open range, or from a lockfile or exact pin (mcp-mesh's runtime and mcp-pinot change class
inside the span and are grouped by how their images installed when they first held 1.28.x). Each tick
is one image at its configured build time, orange if its installed mcp is older than 1.28.0 and blue if
it is 1.28.x. The diamond is the project's first commit pinning or locking 1.28.x (data/pin_movers.csv).
The two vertical lines are the release (2026-06-16T21:37:16Z) and the publication of GHSA-vj7q-gjh5-988w
(2026-07-16T20:14:34Z, data/osv_mcp_1_28_0.csv). No network access. Usage: python3 draw_piece_figure.py"""
import collections, csv, datetime, os

STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(STUDY, 'data')
SLUG = 'what-moves-a-pin'
OUT = os.path.join(STUDY, '..', '..', 'articles', SLUG + '.svg')

REL = datetime.datetime(2026, 6, 16, 21, 37, 16)
ADV = datetime.datetime(2026, 7, 16, 20, 14, 34)
X0, X1 = datetime.datetime(2026, 5, 14), datetime.datetime(2026, 8, 1)
W, L, R = 720, 214, 20
TOP = 176
ROW = 36
GAP = 34

# (image repository, label, note)
OPEN = [('public.ecr.aws/mcp-proxy-for-aws/mcp-proxy-for-aws', 'mcp-proxy-for-aws', 'range; its lockfile unused'),
        ('ghcr.io/dhyansraj/mcp-mesh/python-runtime', 'mcp-mesh runtime', 'range, pinned from 7 July'),
        ('ghcr.io/startreedata/mcp-pinot', 'mcp-pinot', 'range; lockfile from 27 July'),
        ('ghcr.io/argonne-lcf/chemgraph', 'chemgraph', 'range, but held 1.16.0')]
PINNED = [('ghcr.io/n24q02m/better-telegram-mcp', 'better-telegram-mcp', 'lockfile'),
          ('ghcr.io/sooperset/mcp-atlassian', 'mcp-atlassian', 'lockfile'),
          ('ghcr.io/githubsecuritylab/seclab-taskflow-agent', 'seclab-taskflow-agent', 'exact pin'),
          ('ghcr.io/the-openroad-project/openroad-mcp', 'openroad-mcp', 'lockfile'),
          ('ghcr.io/oraios/serena', 'serena', 'exact pin'),
          ('docker.io/browseruse/browseruse', 'browser-use', 'exact pin, unmoved to 15 Aug'),
          ('ghcr.io/gradion-ai/hybrid-groups', 'hybrid-groups', 'lockfile, unmoved to 15 Aug')]


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


def dt(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(datetime.timezone.utc).replace(tzinfo=None)


def x(t):
    return L + (W - L - R) * (t - X0).total_seconds() / (X1 - X0).total_seconds()


def main():
    tl = [r for r in read_csv('image_timeline.csv') if r['mcp_installed']]
    movers = {m['image']: dt(m['when']) for m in read_csv('pin_movers.csv')}
    imgs = collections.defaultdict(list)
    for r in tl:
        t = dt(r['created'])
        if X0 <= t <= X1:
            imgs[r['image']].append((t, r['holds_new'] == 'yes', r['mcp_installed']))
    ys = {}
    y = TOP
    for img, _, _ in OPEN:
        ys[img] = y
        y += ROW
    y += GAP
    for img, _, _ in PINNED:
        ys[img] = y
        y += ROW
    B = y - ROW + 22
    H = B + 96
    n_img = sum(len(v) for k, v in imgs.items() if k in ys)
    desc = ('Eleven rows, one for each image repository of software that depends on the Python library mcp, with published images '
            'built between 14 May and 31 July 2026 whose installed mcp was read. Each tick is one image at its build time, orange if '
            'it installed a version older than 1.28.0 and blue if it installed 1.28.0 or 1.28.1. A diamond marks the project\'s first '
            'commit naming 1.28.0 or later. mcp 1.28.0 was released on 16 June; a security advisory fixed in 1.28.1 was published on '
            '16 July. The top four rows are images that resolve an open version range: three of them turn blue from 19 June, 29 June '
            'and 8 July, before their projects\' own diamonds, and chemgraph\'s stay at 1.16.0. The lower seven are images built from a '
            'lockfile or an exact pin: better-telegram-mcp\'s turn blue on 18 June, just after its bot moved the '
            'lockfile; mcp-atlassian, seclab-taskflow-agent, openroad-mcp and serena have their diamonds within 28 hours after the '
            'advisory, and their images, where one was read afterwards, are blue only after it; browser-use and hybrid-groups have no '
            'diamond by 15 August and their images stay orange. Registries and git read on 26 September 2026.')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
         '<title id="t">Which mcp each published image installed around the 1.28.0 release, by how it installs, 14 May to 31 July 2026</title>',
         f'<desc id="d">{desc}</desc>',
         '<style>',
         'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#6f6e69; --grid:#e4e3df; --band:#f0efec; --old:#eb6834; --new:#2a78d6; }',
         '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#9a9890; --grid:#383835; --band:#262624; --old:#e0703f; --new:#3987e5; } }',
         'text { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; fill: var(--ink); }',
         '.head { font-size: 17px; font-weight: 600; } .sub { font-size: 13px; fill: var(--ink2); }',
         '.lab { font-size: 13px; font-weight: 600; } .note { font-size: 11.5px; fill: var(--muted); }',
         '.grp { font-size: 12px; font-weight: 600; fill: var(--ink2); letter-spacing: 0.02em; }',
         '.ann { font-size: 12px; fill: var(--ink2); } .ax { font-size: 12px; fill: var(--muted); }',
         '</style>',
         f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
         '<text x="16" y="30" class="head">Ranges took the release in days; six of nine pins moved around an advisory</text>',
         '<text x="16" y="51" class="sub">Each tick is one published image at its build time, coloured by the mcp installed inside it.</text>',
         '<text x="16" y="69" class="sub">The diamond is the project\'s first commit naming 1.28.0 or later.</text>']
    o.append('<rect x="16" y="82" width="4" height="15" rx="1" fill="var(--old)"/>')
    o.append('<text x="26" y="94" class="ann">older than 1.28.0</text>')
    o.append('<rect x="146" y="82" width="4" height="15" rx="1" fill="var(--new)"/>')
    o.append('<text x="156" y="94" class="ann">1.28.0 or 1.28.1</text>')
    o.append('<path d="M280,89.5 l6,-6 l6,6 l-6,6 z" fill="var(--ink)"/>')
    o.append('<text x="298" y="94" class="ann">project first names 1.28.x</text>')
    top_line = TOP - 40
    # the 28 hours after the advisory, shaded
    xa, xb = x(ADV), x(ADV + datetime.timedelta(hours=28))
    o.append(f'<rect x="{xa:.1f}" y="{top_line}" width="{xb - xa:.1f}" height="{B - top_line}" fill="var(--band)"/>')
    for d, lab in [(datetime.datetime(2026, 5, 15), '15 May'), (datetime.datetime(2026, 6, 1), '1 June'),
                   (datetime.datetime(2026, 7, 1), '1 July'), (datetime.datetime(2026, 8, 1), '1 Aug')]:
        o.append(f'<line x1="{x(d):.1f}" y1="{top_line}" x2="{x(d):.1f}" y2="{B}" stroke="var(--grid)" stroke-width="1"/>')
        o.append(f'<text x="{x(d):.1f}" y="{B + 18}" class="ax" text-anchor="middle">{lab}</text>')
    o.append(f'<line x1="{x(REL):.1f}" y1="{top_line - 8}" x2="{x(REL):.1f}" y2="{B}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 3"/>')
    o.append(f'<text x="{x(REL) - 6:.1f}" y="{top_line - 12}" class="ann" text-anchor="end">1.28.0 released, 16 June</text>')
    o.append(f'<line x1="{xa:.1f}" y1="{top_line - 8}" x2="{xa:.1f}" y2="{B}" stroke="var(--ink)" stroke-width="1.5"/>')
    o.append(f'<text x="{xa - 6:.1f}" y="{top_line - 26}" class="ann" text-anchor="end">security advisory,</text>')
    o.append(f'<text x="{xa - 6:.1f}" y="{top_line - 12}" class="ann" text-anchor="end">16 July, fixed in 1.28.1</text>')

    def group(rows, head, gy):
        o.append(f'<text x="16" y="{gy}" class="grp">{head}</text>')
        for img, lab, note in rows:
            cy = ys[img]
            o.append(f'<text x="16" y="{cy - 1}" class="lab">{lab}</text>')
            o.append(f'<text x="16" y="{cy + 13}" class="note">{note}</text>')
            o.append(f'<line x1="{L}" y1="{cy + 9}" x2="{W - R}" y2="{cy + 9}" stroke="var(--grid)" stroke-width="1"/>')
            if img in movers and X0 <= movers[img] <= X1:
                mx = x(movers[img])
                o.append(f'<path d="M{mx:.1f},{cy + 3} l6,6 l-6,6 l-6,-6 z" fill="var(--ink)" stroke="var(--bg)" stroke-width="1.5"/>')
            for t, new, _ in sorted(imgs.get(img, [])):
                o.append(f'<rect x="{x(t) - 2:.1f}" y="{cy - 12}" width="4" height="17" rx="1" '
                         f'fill="var(--{"new" if new else "old"})" stroke="var(--bg)" stroke-width="0.75"/>')

    group(OPEN, 'IMAGE RESOLVES AN OPEN RANGE', ys[OPEN[0][0]] - 22)
    group(PINNED, 'IMAGE BUILT FROM A LOCKFILE OR EXACT PIN', ys[PINNED[0][0]] - 22)
    o.append(f'<text x="16" y="{H - 44}" class="note">Sample: {len(ys)} image repositories of software depending directly on mcp, chosen by a rule fixed before any image was read;</text>')
    o.append(f'<text x="16" y="{H - 28}" class="note">{n_img} images built 14 May to 31 July 2026 shown, of 49 read. Shaded: the 28 hours after the advisory. Registries, git and</text>')
    o.append(f'<text x="16" y="{H - 12}" class="note">the advisory read 26 September 2026. Most Docker Hub images in the sample could not be read within our byte budget.</text>')
    o.append('</svg>')
    with open(OUT, 'w') as f:
        f.write('\n'.join(o) + '\n')
    print(len(ys), 'rows;', n_img, 'images drawn;', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
