#!/usr/bin/env python3
"""LH002: draw the time map and the dependency map as SVG from the published tables.
Usage: python3 draw_maps.py <study_dir>"""
import csv, datetime as dt, os, sys
from xml.sax.saxutils import escape as esc
STUDY = sys.argv[1]; D = os.path.join(STUDY, 'data')
UTC = dt.timezone.utc
W0 = dt.datetime(2026, 3, 26, tzinfo=UTC)
REL = dt.datetime(2026, 4, 2, 14, 48, 7, tzinfo=UTC)
def ts(s): return dt.datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(UTC)
rd = lambda n: list(csv.DictReader(open(os.path.join(D, n))))
NAMES = {'R00': 'python-sdk (mcp, library)', 'R01': 'agentcrew', 'R02': 'ai-slide-generator', 'R03': 'lean-lsp-mcp',
         'R04': 'pyp6xer-mcp', 'R05': 'serena', 'R06': 'dartlab', 'R07': 'mistral-vibe', 'R08': 'octobot', 'R09': 'jesse'}
PKG = {'R00': 'mcp', 'R01': 'agentcrew-ai', 'R02': 'databricks-tellr-app', 'R03': 'lean-lsp-mcp', 'R04': 'pyp6xer-mcp',
       'R05': 'serena-agent', 'R06': 'dartlab', 'R07': 'mistral-vibe', 'R08': 'octobot', 'R09': 'jesse'}
STYLE = '''<style>
  svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781; --grid:#e4e3df; --zero:#f0efec;
        --b1:#86b6ef; --b2:#5598e7; --b3:#2a78d6; --b4:#1c5cab; --b5:#104281; --b6:#0d366b; --acc:#eb6834; --blue:#2a78d6; }
  @media (prefers-color-scheme: dark) {
    svg { --bg:#1a1a19; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781; --grid:#383835; --zero:#2a2a28;
          --b1:#184f95; --b2:#1c5cab; --b3:#256abf; --b4:#3987e5; --b5:#6da7ec; --b6:#9ec5f4; --acc:#d95926; --blue:#3987e5; } }
  text { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; fill: var(--ink); }
  .t2 { fill: var(--ink2); } .mu { fill: var(--muted); } .bg { fill: var(--bg); }
</style>'''

# ---------------- time map ----------------
days = rd('repo_day.csv'); deps = rd('manifest_dependency_changes.csv'); cands = rd('propagation_candidates.csv')
rels = rd('pypi_releases_in_window.csv')
W, X0, CW = 1040, 250, 27  # 28 columns of 27 px
LANE, Y0 = 46, 118
H = Y0 + 10 * LANE + 150
BINS = [(1, 2, '--b1'), (3, 5, '--b2'), (6, 10, '--b3'), (11, 25, '--b4'), (26, 50, '--b5'), (51, 10**9, '--b6')]
def fill(n):
    for lo, hi, v in BINS:
        if lo <= n <= hi: return f'var({v})'
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="tm-title tm-desc">',
       STYLE,
       '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
       '<line x1="0" y1="0" x2="0" y2="6" stroke="var(--muted)" stroke-width="1.5"/></pattern></defs>',
       f'<rect class="bg" x="0" y="0" width="{W}" height="{H}"/>',
       '<title id="tm-title">LH002 time map: ten repositories, 26 March to 22 April 2026</title>',
       '<desc id="tm-desc">One lane per repository. Each cell is one UTC day, shaded by commits that day from git. An orange line marks mcp 1.27.0 on PyPI; diamonds mark days with a manifest dependency change; orange dots mark the moment a repository\'s manifest or lockfile first holds mcp 1.27.0.</desc>',
       '<text x="16" y="30" font-size="17" font-weight="600">Time map: commits by day, the library release and dependency changes</text>',
       '<text x="16" y="52" font-size="12.5" class="t2">Ten GitHub repositories (the mcp library and nine PyPI dependents), 26 March to 22 April 2026, UTC days. Git history read 26 September 2026.</text>']
for i in range(28):
    d = (W0 + dt.timedelta(days=i)).date(); x = X0 + i * CW
    if i % 7 == 0 or i == 27:
        out.append(f'<text x="{x + CW/2:.1f}" y="{Y0 - 26}" font-size="11" text-anchor="middle" class="mu">{d.strftime("%d %b")}</text>')
        out.append(f'<line x1="{x}" y1="{Y0 - 18}" x2="{x}" y2="{Y0 + 10*LANE - 6}" stroke="var(--grid)" stroke-width="1"/>')
for li, rid in enumerate(NAMES):
    y = Y0 + li * LANE
    out.append(f'<text x="16" y="{y + 17}" font-size="12.5" font-weight="{600 if rid == "R00" else 400}">{rid} {esc(NAMES[rid])}</text>')
    rows = [r for r in days if r['repo'] == rid]
    tot = sum(int(r['commits'] or 0) for r in rows); obs = sum(1 for r in rows if r['status'] == 'observed')
    out.append(f'<text x="16" y="{y + 33}" font-size="11" class="mu">{tot} commits, {obs} observed days</text>')
    for i, r in enumerate(rows):
        x = X0 + i * CW + 1
        if r['status'] != 'observed':
            out.append(f'<rect x="{x}" y="{y+4}" width="{CW-2}" height="26" rx="4" fill="url(#hatch)"><title>{rid} {r["date"]}: no history on GitHub yet</title></rect>')
            continue
        n = int(r['commits']); md = int(r['manifest_dependency_changes'] or 0)
        tip = f'{rid} {r["date"]}: {n} commits; +{r["additions_other"]}/-{r["deletions_other"]} lines outside lockfiles; {md} manifest dependency changes'
        f = fill(n) if n else 'var(--zero)'
        out.append(f'<rect x="{x}" y="{y+4}" width="{CW-2}" height="26" rx="4" fill="{f}"><title>{esc(tip)}</title></rect>')
        if md:
            cx, cy = x + (CW-2)/2, y + 38
            out.append(f'<path d="M{cx} {cy-5} L{cx+5} {cy} L{cx} {cy+5} L{cx-5} {cy} Z" fill="var(--ink2)"><title>{esc(tip)}</title></path>')
    for c in cands:
        if c['repo'] == rid and c['candidate_link'] != 'no' and '1.27.0' in c['after']:
            t = ts(c['committed_utc']); x = X0 + (t - W0).total_seconds() / 86400 * CW
            tip = f"{rid} {t:%d %b %H:%M} UTC: {c['change']}, now {c['after']}"
            out.append(f'<circle cx="{x:.1f}" cy="{y+17}" r="6" fill="var(--acc)" stroke="var(--bg)" stroke-width="2"><title>{esc(tip)}</title></circle>')
xr = X0 + (REL - W0).total_seconds() / 86400 * CW
out.append(f'<line x1="{xr:.1f}" y1="{Y0 - 14}" x2="{xr:.1f}" y2="{Y0 + 10*LANE - 6}" stroke="var(--acc)" stroke-width="2"/>')
out.append(f'<text x="{xr + 5:.1f}" y="{Y0 - 6}" font-size="11.5" font-weight="600">mcp 1.27.0 on PyPI, 2 Apr 14:48 UTC</text>')
# legend
ly = Y0 + 10 * LANE + 18
out.append(f'<text x="16" y="{ly + 12}" font-size="12" font-weight="600">Commits per day</text>')
lx = 160
for (lo, hi, v), lab in zip(BINS, ['1-2', '3-5', '6-10', '11-25', '26-50', '51+']):
    out.append(f'<rect x="{lx}" y="{ly}" width="22" height="16" rx="4" fill="var({v})"/><text x="{lx+27}" y="{ly+12}" font-size="11.5" class="t2">{lab}</text>')
    lx += 70
out.append(f'<rect x="{lx}" y="{ly}" width="22" height="16" rx="4" fill="var(--zero)"/><text x="{lx+27}" y="{ly+12}" font-size="11.5" class="t2">0</text>')
out.append(f'<rect x="{lx+60}" y="{ly}" width="22" height="16" rx="4" fill="url(#hatch)"/><text x="{lx+87}" y="{ly+12}" font-size="11.5" class="t2">no GitHub history yet</text>')
ly2 = ly + 30
out.append(f'<path d="M22 {ly2+3} L27 {ly2+8} L22 {ly2+13} L17 {ly2+8} Z" fill="var(--ink2)"/><text x="34" y="{ly2+12}" font-size="11.5" class="t2">day with at least one dependency change in a manifest (pyproject, requirements, setup)</text>')
out.append(f'<circle cx="22" cy="{ly2+30}" r="6" fill="var(--acc)"/><text x="34" y="{ly2+34}" font-size="11.5" class="t2">a manifest or lockfile first holds mcp 1.27.0, placed at the commit time</text>')
out.append(f'<line x1="16" y1="{ly2+52}" x2="28" y2="{ly2+52}" stroke="var(--acc)" stroke-width="2"/><text x="34" y="{ly2+56}" font-size="11.5" class="t2">the library release, from the PyPI upload time as Open Source Insights gives it</text>')
out.append(f'<text x="16" y="{H - 12}" font-size="11" class="mu">Commits deduplicated across branches and tags, placed by committer time. Hover a cell for counts. Source: studies/LH002/data/repo_day.csv.</text>')
out.append('</svg>')
open(os.path.join(STUDY, 'time-map.svg'), 'w').write('\n'.join(out))

# ---------------- dependency map ----------------
g = {(r['repo'], r['at']): r for r in rd('depsdev_graphs_window_start_end.csv')}
links = rd('depsdev_source_repo_links.csv')
state = {(r['repo'], r['at']): r for r in rd('mcp_state_window_start_end.csv')}
moved = {c['repo'] for c in cands if c['candidate_link'] != 'no' and '1.27.0' in c['after']}
W2, H2 = 1040, 680
MX, MY = 150, 330
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}" width="{W2}" height="{H2}" role="img" aria-labelledby="dm-title dm-desc">',
       STYLE, f'<rect class="bg" x="0" y="0" width="{W2}" height="{H2}"/>',
       '<title id="dm-title">LH002 dependency map: the cohort as Open Source Insights resolves it</title>',
       '<desc id="dm-desc">The library mcp on the left, the nine dependents on the right. Each line is the dependency Open Source Insights resolves for the dependent\'s PyPI version current at window end, typed by the requirement. No dependent resolves another cohort member.</desc>',
       '<text x="16" y="30" font-size="17" font-weight="600">Dependency map: typed links among the cohort, as Open Source Insights resolves them</text>',
       '<text x="16" y="52" font-size="12.5" class="t2">Each dependent\'s PyPI version current at 22 April 2026. Resolved versions are as the service gave them on 26 September 2026, not as installed in April.</text>']
out.append(f'<rect x="{MX-110}" y="{MY-34}" width="200" height="68" rx="8" fill="none" stroke="var(--ink)" stroke-width="2"/>')
out.append(f'<text x="{MX-10}" y="{MY-8}" font-size="14" font-weight="600" text-anchor="middle">mcp (R00)</text>')
out.append(f'<text x="{MX-10}" y="{MY+10}" font-size="11.5" text-anchor="middle" class="t2">1.27.0 released in window</text>')
out.append(f'<text x="{MX-10}" y="{MY+25}" font-size="11" text-anchor="middle" class="mu">repo link: attested</text>')
NX, top = 560, 100
for i, rid in enumerate([f'R{k:02d}' for k in range(1, 10)]):
    y = top + i * 56
    r = g[(rid, 'end')]
    req, res, err = r['mcp_requirement'], r['mcp_resolved'], r['error']
    if err:
        kind, dash, width, col = 'graph not resolved', '2 4', 1.5, 'var(--muted)'
        lab = 'resolution error in the service'
    elif not req:
        kind, dash, width, col = 'no mcp dependency', '6 5', 1.5, 'var(--muted)'
        lab = f'{r["version"]}: no mcp in resolved graph'
    elif req.startswith('=='):
        kind, dash, width, col = 'exact pin', '', 3, 'var(--blue)'
        lab = f'{r["version"]}: mcp{req}, resolves {res}'
    else:
        kind, dash, width, col = 'lower bound', '', 1.5, 'var(--blue)'
        lab = f'{r["version"]}: mcp{req}, resolves {res}'
    prov = sorted({l['provenance'] for l in links if l['repo'] == rid})
    plab = 'repo link: attested' if 'PYPI_PUBLISH_ATTESTATION' in prov else 'repo link: unverified metadata'
    if rid == 'R04': plab = 'repo link names a GitLab repository'
    d = f'M{NX} {y} C {NX-180} {y}, {MX+260} {MY}, {MX+90} {MY + (i-4)*4}'
    out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else '') +
               f'><title>{esc(f"{rid} {PKG[rid]} {lab} ({kind})")}</title></path>')
    out.append(f'<rect x="{NX}" y="{y-20}" width="200" height="40" rx="6" fill="var(--bg)" stroke="var(--ink2)" stroke-width="1"/>')
    out.append(f'<text x="{NX+10}" y="{y-3}" font-size="12.5" font-weight="600">{rid} {esc(PKG[rid])}</text>')
    out.append(f'<text x="{NX+10}" y="{y+13}" font-size="10.5" class="mu">{esc(plab)}</text>')
    out.append(f'<text x="{NX+212}" y="{y-3}" font-size="11.5" class="t2">{esc(lab)}</text>')
    st = state[(rid, 'end')]
    gl = f"git at window end: {st['mcp_requirements'].split(': ',1)[-1] or 'no mcp'}; lock {st['locked_mcp'].split(': ')[-1] if st['locked_mcp'] else 'none'}"
    out.append(f'<text x="{NX+212}" y="{y+13}" font-size="10.5" class="mu">{esc(gl)}</text>')
    if rid in moved:
        out.append(f'<circle cx="{NX-8}" cy="{y}" r="6" fill="var(--acc)" stroke="var(--bg)" stroke-width="2"><title>{rid}: moved to mcp 1.27.0 inside the window, per git</title></circle>')
ly = top + 9 * 56 + 6
out.append(f'<line x1="16" y1="{ly}" x2="44" y2="{ly}" stroke="var(--blue)" stroke-width="3"/><text x="52" y="{ly+4}" font-size="11.5" class="t2">direct dependency, exact pin (==)</text>')
out.append(f'<line x1="290" y1="{ly}" x2="318" y2="{ly}" stroke="var(--blue)" stroke-width="1.5"/><text x="326" y="{ly+4}" font-size="11.5" class="t2">direct dependency, lower bound (&gt;=)</text>')
out.append(f'<line x1="570" y1="{ly}" x2="598" y2="{ly}" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="6 5"/><text x="606" y="{ly+4}" font-size="11.5" class="t2">no mcp in the window-time version</text>')
out.append(f'<line x1="16" y1="{ly+22}" x2="44" y2="{ly+22}" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="2 4"/><text x="52" y="{ly+26}" font-size="11.5" class="t2">the service could not resolve the graph</text>')
out.append(f'<circle cx="298" cy="{ly+22}" r="6" fill="var(--acc)"/><text x="310" y="{ly+26}" font-size="11.5" class="t2">git shows a move to mcp 1.27.0 inside the window</text>')
out.append(f'<text x="16" y="{ly+48}" font-size="11" class="mu">Seven of nine dependents resolve mcp, each as a direct dependency; no dependent resolves another cohort member. mcp 2.2.0 and 1.30.0 were published on 7 September 2026.</text>')
out.append(f'<text x="16" y="{ly+64}" font-size="11" class="mu">Right-hand grey lines are what git holds at window end. Source: studies/LH002/data/depsdev_graphs_window_start_end.csv and mcp_state_window_start_end.csv.</text>')
out.append('</svg>')
open(os.path.join(STUDY, 'dependency-map.svg'), 'w').write('\n'.join(out))
print('written')
