"""LH041 figure: maintainer clusters reached, hour by hour, in six worm waves.

    python3 -I studies/LH041/scripts/draw_figure.py 2026-11-08T1910Z

Reads data/<read>/tables/posthoc/clusters.csv and waves.csv (the post hoc view:
versions whose registry time is inside the wave's window; window joins only
among waves of the record's ecosystem) and writes studies/LH041/figure-reach.svg.
The SVG carries its own light and dark themes (scripts/chart_style.py).
"""
import csv, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from chart_style import svg_open  # noqa: E402
from html import escape  # noqa: E402

read = sys.argv[1]
T = os.path.join(HERE, "..", "data", read, "tables", "posthoc")
cl = [r for r in csv.DictReader(open(os.path.join(T, "clusters.csv"))) if r["scope"] == "indicator+window"]
wv = {r["wave"]: r for r in csv.DictReader(open(os.path.join(T, "waves.csv"))) if r["scope"] == "indicator+window"}

PANELS = [("W01", "Shai-Hulud, Sep 2025"), ("W02", "Shai-Hulud 2.0, Nov 2025"), ("W06", "TanStack wave, May 2026"),
          ("W07", "AntV wave, May 2026"), ("W08", "Miasma, Jun 2026"), ("W11", "ChainDrop, Aug 2026")]
XMAX = {"W01": 72, "W02": 16, "W06": 32, "W07": 168, "W08": 96, "W11": 56}
TICKS = {"W01": [0, 24, 48, 72], "W02": [0, 4, 8, 12, 16], "W06": [0, 8, 16, 24, 32], "W07": [0, 48, 96, 144],
         "W08": [0, 24, 48, 72, 96], "W11": [0, 12, 24, 36, 48]}
YMAX = {"W01": 20, "W02": 90, "W06": 15, "W07": 5, "W08": 10, "W11": 15}
YT = {"W01": [0, 10, 20], "W02": [0, 30, 60, 90], "W06": [0, 5, 10, 15], "W07": [0, 5], "W08": [0, 5, 10], "W11": [0, 5, 10, 15]}

W_, H_ = 720, 790
pw, ph = 300, 150
x0s = [70, 410]
y0s = [125, 345, 565]
out = [svg_open(W_, H_, "Maintainer clusters reached after each wave's first malicious publish",
                "Six small step charts, one per worm wave. Each shows how many groups of packages sharing a current npm "
                "maintainer had published a malicious version, counting up from the wave's first publish by the "
                "registry's clock. Shai-Hulud 2.0 reached 88 clusters in under 15 hours; ChainDrop 13 of its 14 in under 4 "
                "hours; Shai-Hulud 17 in 71 hours; the TanStack wave 13 in 30 hours; Miasma 8 in 87 hours; the AntV "
                "wave stayed mostly in one cluster of 316 packages, with 2 others. Post hoc view, record 0.3; a group is not a victim, an account or a step of the worm. "
                "Source: OSV malicious-package records and npm registry metadata read 8 November 2026.")]
out.append(f'<rect width="{W_}" height="{H_}" fill="var(--bg)"/>')
out.append('<text class="head" x="24" y="34">How many maintainer groups had a malicious version, hour by hour</text>')
out.append('<text class="sub" x="24" y="56">Groups of packages sharing a current npm maintainer, with a malicious version, from the</text>')
out.append('<text class="sub" x="24" y="74">wave\'s first malicious publish (registry clock). Each panel has its own scales.</text>')

for k, (wid, title) in enumerate(PANELS):
    x0 = x0s[k % 2]
    y0 = y0s[k // 2]
    xm = XMAX[wid]
    pts = sorted(float(r["hours_after_wave_first"]) for r in cl if r["wave"] == wid)
    w = wv[wid]

    def X(h):
        return x0 + pw * min(h, xm) / xm

    def Y(n):
        return y0 + ph - ph * n / YMAX[wid]

    out.append(f'<text class="nm" x="{x0}" y="{y0 - 12}">{escape(title)}</text>')
    for yv in YT[wid]:
        out.append(f'<line class="grid" x1="{x0}" x2="{x0 + pw}" y1="{Y(yv):.1f}" y2="{Y(yv):.1f}"/>')
        if True:
            out.append(f'<text class="ax" x="{x0 - 8}" y="{Y(yv) + 4:.1f}" text-anchor="end">{yv}</text>')
    out.append(f'<line class="axis" x1="{x0}" x2="{x0 + pw}" y1="{Y(0):.1f}" y2="{Y(0):.1f}"/>')
    for t in TICKS[wid]:
        out.append(f'<line class="axis" x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{Y(0):.1f}" y2="{Y(0) + 4:.1f}"/>')
        out.append(f'<text class="ax" x="{X(t):.1f}" y="{Y(0) + 17:.1f}" text-anchor="middle">{t}</text>')
    out.append(f'<text class="ax" x="{x0 + pw}" y="{Y(0) + 32:.1f}" text-anchor="end">hours after first publish</text>')
    d = f"M{X(0):.1f},{Y(0):.1f}"
    n = 0
    for h in pts:
        n += 1
        d += f" H{X(h):.1f} V{Y(n):.1f}"
    end_h = pts[-1] if pts else 0
    d += f" H{X(min(xm, end_h)):.1f}"
    out.append(f'<path d="{d}" fill="none" stroke="var(--teal)" stroke-width="2.5"/>')
    lab = f'{n} clusters, last new at {float(w["hours_to_last_new_cluster"]):.1f} h'
    if wid == "W07":
        lab = f'{n} clusters; one holds {w["largest_cluster_packages"]} packages'
    lx, ly, anc = (x0 + 8, y0 + 14, "start") if wid == "W08" else (x0 + pw, y0 + ph - 30, "end")
    out.append(f'<text class="ann" x="{lx}" y="{ly}" text-anchor="{anc}">{escape(lab)}</text>')
    out.append(f'<text class="ann" x="{lx}" y="{ly + 16}" text-anchor="{anc}">{w["npm_packages"]} npm packages, {w["versions"]} versions</text>')

out.append(f'<text class="note" x="24" y="{H_ - 22}">Post hoc view: versions outside each wave\'s window left out. A group is packages sharing a maintainer today, not a</text>')
out.append(f'<text class="note" x="24" y="{H_ - 7}">victim or a worm step; a later group does not show that no person published. OSV and npm registry, read 8 Nov 2026.</text>')
out.append("</svg>")
open(os.path.join(HERE, "..", "figure-reach.svg"), "w").write("\n".join(out) + "\n")
print("wrote figure-reach.svg")
