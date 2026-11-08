#!/usr/bin/env python3
"""LH042: build the dated table, the series list and the figure from data/counts.csv.

Usage: python3 -I studies/LH042/scripts/build.py
Writes data/table.md, data/series.csv, data/series_changes.txt and figure.svg.
No count is typed here: every value comes from counts.csv, whose quotations
check_quotes.py verifies against the retained bodies.
"""
import csv
import datetime as dt
import pathlib
import sys
from collections import defaultdict
from html import escape

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT.parent.parent / "scripts"))
from chart_style import svg_open, series_stroke  # noqa: E402

CLASSES = {
    "1": "Ollama API endpoints",
    "1-2": "LLM endpoints as one publisher's category (Ollama and other inference servers together)",
    "2": "Other self-hosted inference servers",
    "3": "AI application front-ends and builders",
    "4": "OpenClaw-family agent control panels",
    "5": "Other agent runtimes' panels",
    "6": "MCP servers",
    "7": "Publisher-defined aggregates",
    "8": "Devices a small self-replicating model could use",
}
ORDER = ["1", "1-2", "2", "3", "4", "5", "6", "7", "8"]

rows = list(csv.DictReader(open(ROOT / "data" / "counts.csv")))


def sort_date(r):
    d = r["date_end"]
    return d + "-15" if len(d) == 7 else d


def fmt(r):
    q = r["qualifier"]
    n = f"{int(r['count']):,}"
    return f"{q} {n}" if q else n


# The dated table
out = ["# LH042 dated table (built by scripts/build.py from data/counts.csv; do not edit by hand)", "",
       "Every row is a publisher's own count, admitted under the brief. Rows of different series are never joined. "
       "Date is the scan date or window end where the source gives one; the basis column says which clock it is.", ""]
for c in ORDER:
    rs = sorted([r for r in rows if r["cls"] == c], key=sort_date)
    out.append(f"## Class {c}: {CLASSES[c]}")
    out.append("")
    if not rs:
        out.append("No admitted count.")
        out.append("")
        continue
    out.append("| id | date | count | unit | product | publisher | method | kind | series | date basis | source |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rs:
        date = r["date_end"] if r["date_start"] == r["date_end"] else f"{r['date_start']} to {r['date_end']}"
        cells = [r["id"], date, fmt(r), r["unit"], r["product"], r["publisher"], r["method"], r["kind"],
                 r["series"], r["date_basis"], r["source"]]
        out.append("| " + " | ".join(x.replace("|", "/") for x in cells) + " |")
    out.append("")
(ROOT / "data" / "table.md").write_text("\n".join(out) + "\n")

# Series
by = defaultdict(list)
for r in rows:
    by[r["series"]].append(r)
srows = []
changes = []
for s in sorted(by, key=lambda x: int(x[1:])):
    rs = sorted(by[s], key=sort_date)
    first, last = rs[0], rs[-1]
    dates = sorted({r["date_end"] for r in rs})
    srows.append(dict(series=s, cls=first["cls"], product=first["product"], publisher=first["publisher"],
                      method=first["method"], kind=first["kind"], unit=first["unit"], n_counts=len(rs),
                      n_dates=len(dates), first_date=first["date_end"], first=fmt(first),
                      last_date=last["date_end"], last=fmt(last)))
    if len(dates) >= 2:
        a, b = int(first["count"]), int(last["count"])
        lo = min(int(r["count"]) for r in rs)
        hi = max(int(r["count"]) for r in rs)
        changes.append(f"{s} ({first['publisher']}; {first['product']}; {first['kind']}, {first['unit']}): "
                       f"{len(dates)} dates, {first['date_end']} {a:,} to {last['date_end']} {b:,}, "
                       f"change {b - a:+,} ({(b - a) / a * 100:+.1f}%); lowest {lo:,}, highest {hi:,}; "
                       f"steps up {sum(1 for x, y in zip(rs, rs[1:]) if int(y['count']) > int(x['count']))}, "
                       f"down {sum(1 for x, y in zip(rs, rs[1:]) if int(y['count']) < int(x['count']))}")
with open(ROOT / "data" / "series.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(srows[0].keys()))
    w.writeheader()
    w.writerows(srows)
n_multi = sum(1 for s in srows if s["n_dates"] >= 2)
summary = [f"admitted counts: {len(rows)}", f"series: {len(srows)}", f"series with two or more dates: {n_multi}",
           "counts by class: " + ", ".join(f"{c}={sum(1 for r in rows if r['cls'] == c)}" for c in ORDER),
           "publishers: " + str(len({r['publisher'].split(' (')[0] for r in rows})), ""] + changes
(ROOT / "data" / "series_changes.txt").write_text("\n".join(summary) + "\n")
print("\n".join(summary))


# Figure: small multiples, one per comparable series group, each its own axis from zero
def d2f(d):
    if len(d) == 7:
        d += "-15"
    t = dt.date.fromisoformat(d)
    return t.toordinal()


panels = [
    ("OpenClaw-family panels", "OpenA2A index: Shodan, sum of its OpenClaw queries", ["S42"], "line"),
    ("LLM endpoints", "OpenA2A index: Shodan, its LLM-endpoint category", ["S43"], "line"),
    ("MCP servers", "OpenA2A index: Shodan, its MCP category", ["S44"], "line"),
    ("Ollama endpoints, 2025 to 2026", "Xu et al.: own daily IPv4 sweep; four days the paper states", ["S01"], "points"),
]
W, H = 720, 650
pw, ph = 255, 165
lefts = [78, 428]
tops = [138, 392]
svg = [svg_open(W, H, "Published counts of exposed AI services, by method",
                "Four small charts, each its own series and axis, never joined. OpenA2A's monthly Shodan index, March to "
                "November 2026: OpenClaw-family gateways 242,379 on 14 March, 267,172 on 11 April, lowest 153,638 on "
                "26 June, 205,872 on 1 November; LLM endpoints between 5,126 and 47,369; MCP servers rising from 889 "
                "to 2,734. Xu and co-authors' own daily sweep of Ollama's port: 10,473 IPs on 14 February 2025, "
                "16,821 on 25 April 2025, about 11,500 in July 2025 and 16,059 on 13 February 2026. A Shodan index "
                "count is what Shodan's crawlers indexed, not a verified host. Source: LH042 data/counts.csv.")]
svg.append('<rect width="100%" height="100%" fill="var(--bg)"/>')
svg.append('<text class="head" x="24" y="32">Published counts of exposed AI services, by method</text>')
svg.append('<text class="sub" x="24" y="54">Each chart is one publisher\'s series with its own axis from zero. Series are never joined.</text>')
svg.append('<text class="sub" x="24" y="72">Unreviewed working figure, LH042 version 0.1; counts as published, read 8 November 2026.</text>')
for i, (title, sub, series, mode) in enumerate(panels):
    x0 = lefts[i % 2]
    y0 = tops[i // 2]
    pts = sorted([r for r in rows if r["series"] in series], key=sort_date)
    xs = [d2f(r["date_end"]) for r in pts]
    ys = [int(r["count"]) for r in pts]
    xmin, xmax = min(xs), max(xs)
    span = max(1, xmax - xmin)
    ymax = max(ys) * 1.12
    ymax = int(ymax)
    mag = 10 ** (len(str(ymax)) - 1)
    top = ((ymax // mag) + 1) * mag
    if top / ymax > 1.6:
        top = ((ymax // (mag // 2)) + 1) * (mag // 2)

    def X(v):
        return x0 + (v - xmin) / span * pw

    def Y(v):
        return y0 + ph - v / top * ph

    svg.append(f'<text class="sec" x="{x0 - 46}" y="{y0 - 32}">{escape(title)}</text>')
    svg.append(f'<text class="note" x="{x0 - 46}" y="{y0 - 16}">{escape(sub)}</text>')
    for k in range(0, 3):
        v = top * k / 2
        svg.append(f'<line class="grid" x1="{x0}" x2="{x0 + pw}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>')
        svg.append(f'<text class="ax" x="{x0 - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{int(v):,}</text>')
    svg.append(f'<line class="axis" x1="{x0}" x2="{x0 + pw}" y1="{y0 + ph}" y2="{y0 + ph}"/>')
    for r, xv in ((pts[0], xs[0]), (pts[-1], xs[-1])):
        d = dt.date.fromordinal(xv)
        lab = d.strftime("%-d %b %Y") if r["date_precision"] == "day" else d.strftime("%b %Y")
        anchor = "start" if xv == xs[0] else "end"
        svg.append(f'<text class="ax" x="{X(xv):.1f}" y="{y0 + ph + 16}" text-anchor="{anchor}">{lab}</text>')
    colour = series_stroke(i)
    if mode == "line":
        path = " ".join(f"{'M' if j == 0 else 'L'}{X(a):.1f},{Y(b):.1f}" for j, (a, b) in enumerate(zip(xs, ys)))
        svg.append(f'<path d="{path}" fill="none" {colour} stroke-linejoin="round"/>')
    for a, b in zip(xs, ys):
        svg.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="4" fill="var(--bg)" stroke="var(--{colour.split("var(--")[1].split(")")[0]})" stroke-width="2.5"/>')
    labelled = set(range(len(ys))) if mode == "points" else {0, len(ys) - 1, ys.index(max(ys)), ys.index(min(ys))}
    for j in sorted(labelled):
        a, b = xs[j], ys[j]
        anchor = "start" if j == 0 else ("end" if j == len(ys) - 1 else "middle")
        if j == 0:
            dy = 18 if len(ys) > 1 and ys[1] > b else -10
        elif j == len(ys) - 1:
            dy = 18 if ys[j - 1] > b else -10
        else:
            dy = 18 if b == min(ys) else -10
        q = "about " if pts[j]["qualifier"] else ""
        svg.append(f'<text class="nm" x="{X(a):.1f}" y="{Y(b) + dy:.1f}" text-anchor="{anchor}">{q}{b:,}</text>')
svg.append('<text class="note" x="24" y="616">OpenA2A plots the latest sweep each month; sweeps within one month can differ by more than months do.</text>')
svg.append('<text class="note" x="24" y="634">Exposure is not compromise. Counts are the publishers\' claims; Lighthouse scanned nothing.</text>')
svg.append("</svg>")
(ROOT / "figure.svg").write_text("\n".join(svg) + "\n")
