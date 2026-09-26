#!/usr/bin/env python3
"""LH006: draws images.svg from data/image_timeline.csv, data/images.csv and
data/project_mcp_pins_git.csv / project_mcp_pins_pypi.csv. One row per image repository; each
image whose layers were read is a mark shaped and coloured by the mcp version found in it; images in
the period that were not read are small grey ticks; the project's first commit pinning or locking
1.27.0 is a black diamond. Usage: python3 draw_figure.py"""
import datetime, os
from common import read_csv, STUDY

X0, X1 = datetime.datetime(2026, 3, 19), datetime.datetime(2026, 5, 30)
W, H = 1000, 490
L, R, T = 190, 30, 140
ROW = 44
REL = datetime.datetime(2026, 4, 2, 14, 48)
WIN = (datetime.datetime(2026, 3, 26), datetime.datetime(2026, 4, 23))
PER_END = datetime.datetime(2026, 5, 23)
REPOS = [('ghcr.io/oraios/serena', 'serena (ghcr.io)', 'serena-agent'),
         ('docker.io/daltonnyx/agentcrew', 'agentcrew', 'agentcrew-ai'),
         ('docker.io/keboola/mcp-server', 'keboola mcp-server', 'keboola-mcp-server'),
         ('docker.io/nsphung/mcp-snowflake-server-nsp', 'mcp-snowflake-server', 'mcp-snowflake-server-nsp'),
         ('docker.io/drakkarsoftware/octobot', 'octobot', 'octobot'),
         ('docker.io/salehmir/jesse', 'jesse', 'jesse')]


def dt(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(datetime.timezone.utc).replace(tzinfo=None)


def x(t):
    return L + (W - L - R) * (t - X0).total_seconds() / (X1 - X0).total_seconds()


def mark(cx, cy, v):
    if v == '1.27.0':
        return f'<circle cx="{cx:.1f}" cy="{cy}" r="6" fill="var(--s1)" stroke="var(--bg)" stroke-width="2"/>'
    if v == '1.26.0':
        return f'<rect x="{cx-5.5:.1f}" y="{cy-5.5}" width="11" height="11" rx="2" fill="var(--s2)" stroke="var(--bg)" stroke-width="2"/>'
    if v:
        return f'<path d="M{cx:.1f},{cy-7} l6.5,11.5 h-13 z" fill="var(--s3)" stroke="var(--bg)" stroke-width="2"/>'
    return f'<circle cx="{cx:.1f}" cy="{cy}" r="5" fill="var(--bg)" stroke="var(--ink2)" stroke-width="2"/>'


def main():
    tl = read_csv('image_timeline.csv')
    imgs = read_csv('images.csv')
    pins = read_csv('project_mcp_pins_git.csv')
    B = T + ROW * len(REPOS)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">',
         '<title id="t">Installed mcp version in published images, 19 March to 30 May 2026</title>',
         '<desc id="d">One row per image repository. Each image whose layers were read is marked by the mcp version its '
         'site-packages records; grey ticks are images tagged in the period that were not read; diamonds are the project\'s '
         'first commit pinning or locking mcp 1.27.0.</desc>',
         '<style>',
         'svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e4e3df; --win:#f0efec; '
         '--s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; }',
         '@media (prefers-color-scheme: dark) { svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781; '
         '--grid:#383835; --win:#2a2a28; --s1:#3987e5; --s2:#d95926; --s3:#199e70; } }',
         'text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink); }',
         '.t2 { fill: var(--ink2); } .mu { fill: var(--muted); }',
         '</style>',
         f'<rect width="{W}" height="{H}" fill="var(--bg)"/>',
         '<text x="16" y="30" font-size="17" font-weight="600">What was installed: the mcp version inside each published image read</text>',
         '<text x="16" y="52" font-size="12.5" class="t2">Build time from each image\'s configuration (Docker Hub push time where the configuration was not read). '
         'Registries read 26 September 2026.</text>']
    # legend
    lx, ly = 16, 80
    for v, lab in (('1.26.0', 'mcp 1.26.0'), ('1.27.0', 'mcp 1.27.0'), ('other', 'another version'), ('', 'no mcp installed')):
        o.append(mark(lx + 7, ly, v if v != 'other' else 'x'))
        o.append(f'<text x="{lx+20}" y="{ly+4.5}" font-size="12.5">{lab}</text>')
        lx += 40 + 7.2 * len(lab)
    lx, ly = 16, 104
    o.append(f'<line x1="{lx+4}" y1="{ly-6}" x2="{lx+4}" y2="{ly+6}" stroke="var(--muted)" stroke-width="2"/>'
             f'<text x="{lx+14}" y="{ly+4.5}" font-size="12.5">image, installed version not read</text>')
    lx += 255
    o.append(f'<path d="M{lx+7},{ly-7} l7,7 l-7,7 l-7,-7 z" fill="var(--ink)"/>'
             f'<text x="{lx+20}" y="{ly+4.5}" font-size="12.5">project pins or locks 1.27.0 in git</text>')
    # window, grid, release
    o.append(f'<rect x="{x(WIN[0]):.1f}" y="{T-14}" width="{x(WIN[1])-x(WIN[0]):.1f}" height="{B-T+14}" fill="var(--win)"/>')
    o.append(f'<text x="{x(WIN[1])-4:.1f}" y="{T-2}" font-size="11.5" text-anchor="end" class="t2">LH002 window</text>')
    d = X0
    while d <= X1:
        if d.day in (1, 8, 15, 22):
            o.append(f'<line x1="{x(d):.1f}" y1="{T-14}" x2="{x(d):.1f}" y2="{B}" stroke="var(--grid)" stroke-width="1"/>')
            o.append(f'<text x="{x(d):.1f}" y="{B+18}" font-size="11.5" text-anchor="middle" class="t2">{d.day} {d.strftime("%b")}</text>')
        d += datetime.timedelta(days=1)
    o.append(f'<line x1="{x(PER_END):.1f}" y1="{T-14}" x2="{x(PER_END):.1f}" y2="{B}" stroke="var(--muted)" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<text x="{x(PER_END)+4:.1f}" y="{T-2}" font-size="11.5" class="t2">period ends</text>')
    o.append(f'<line x1="{x(REL):.1f}" y1="{T-14}" x2="{x(REL):.1f}" y2="{B}" stroke="var(--ink)" stroke-width="1.5"/>')
    o.append(f'<text x="{x(REL)+4:.1f}" y="{B+34}" font-size="11.5">mcp 1.27.0 released, 2 Apr 14:48 UTC</text>')
    for i, (img, lab, pkg) in enumerate(REPOS):
        cy = T + ROW * i + ROW // 2
        o.append(f'<text x="{L-12}" y="{cy+4}" font-size="12.5" text-anchor="end">{lab}</text>')
        o.append(f'<line x1="{L}" y1="{cy}" x2="{W-R}" y2="{cy}" stroke="var(--grid)" stroke-width="1"/>')
        read = {r['tags'] for r in tl if r['image'] == img and (r['mcp_installed'] or r['reading'].startswith('no mcp'))}
        for r in imgs:
            if r['image'] == img and r['position'].startswith(('in ', 'nearest')) and r['tags'] not in read:
                t = r['first_pushed'] or r['created']
                if t and X0 <= dt(t) <= X1:
                    o.append(f'<line x1="{x(dt(t)):.1f}" y1="{cy-6}" x2="{x(dt(t)):.1f}" y2="{cy+6}" stroke="var(--muted)" stroke-width="1.5"/>')
        p = [q for q in pins if q['package'] == pkg and q['mcp'] in ('==1.27.0', '1.27.0')]
        if p and X0 <= dt(p[0]['committed_utc']) <= X1:
            px = x(dt(p[0]['committed_utc']))
            o.append(f'<path d="M{px:.1f},{cy-17} l6,6 l-6,6 l-6,-6 z" fill="var(--ink)"/>')
        last_label = None
        for r in tl:
            if r['image'] == img:
                t = r['created_utc'] or r['pushed_utc']
                if not (t and X0 <= dt(t) <= X1):
                    continue
                if r['mcp_installed'] or r['reading'].startswith('no mcp'):
                    o.append(mark(x(dt(t)), cy, r['mcp_installed']))
                    v = r['mcp_installed']
                    if v and v not in ('1.26.0', '1.27.0') and v != last_label:
                        o.append(f'<text x="{x(dt(t)):.1f}" y="{cy+22}" font-size="11" text-anchor="middle" class="t2">{v}</text>')
                    last_label = v
                else:
                    o.append(f'<line x1="{x(dt(t)):.1f}" y1="{cy-6}" x2="{x(dt(t)):.1f}" y2="{cy+6}" stroke="var(--muted)" stroke-width="1.5"/>')
    o.append(f'<text x="16" y="{H-30}" font-size="11.5" class="mu">Not every image could be read: Docker Hub reads were limited by a shared anonymous allowance and a byte cap (LH006.md, Method).</text>')
    o.append(f'<text x="16" y="{H-13}" font-size="11.5" class="mu">Sources: data/image_timeline.csv (registries and layer contents); data/project_mcp_pins_git.csv (git). octobot\'s next image, 30 July, still held 1.26.0.</text>')
    o.append('</svg>')
    open(os.path.join(STUDY, 'images.svg'), 'w').write('\n'.join(o) + '\n')


if __name__ == '__main__':
    main()
