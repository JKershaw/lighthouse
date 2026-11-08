"""LH046 figure: events and PushEvents in each panel file, 1 September to 7 November 2026, from retained counts.

Usage (from the repository root):  python3 -I studies/LH046/scripts/figure.py studies/LH046/data studies/LH046/figure.svg
"""
import csv, datetime as dt, os, statistics as st, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from chart_style import svg_open, series_stroke

D, OUT = sys.argv[1], sys.argv[2]
rows = [r for r in csv.DictReader(open(os.path.join(D, "hours.csv"), newline=""))]
panel = [r for r in rows if r["set"] == "panel" and r["http_status"] == "200"]
refs = [r for r in rows if r["set"] == "reference" and r["http_status"] == "200" and r["label"] != "2026-04-02-14"]
ref_med = st.median(int(r["events"]) for r in refs) if refs else None
ref_push = st.median(int(r["PushEvent"]) for r in refs) if refs else None


def when(r):
    d, h = r["label"].rsplit("-", 1)
    return dt.datetime.fromisoformat(d) + dt.timedelta(hours=int(h))


panel.sort(key=when)
T0, T1 = dt.datetime(2026, 9, 1), dt.datetime(2026, 11, 8)
W, H = 720, 500
L, R, TOP, BOT = 64, 24, 112, 370
STRIP = 412
ymax = 170000


def x(t): return L + (W - L - R) * (t - T0).total_seconds() / (T1 - T0).total_seconds()
def y(v): return BOT - (BOT - TOP) * min(v, ymax) / ymax


zero = [r for r in panel if int(r["PushEvent"]) == 0]
desc = (f"Line chart of the number of events in each of {len(panel)} GH Archive hourly files read at 00, 06, 12 and 18 UTC "
        f"each day from 1 September to 7 November 2026, with a second line for PushEvents. "
        f"{len(zero)} files held no PushEvent; they are marked as ticks in a strip below the chart. "
        + (f"The median of 16 reference files from January to August 2026 (hour 12) was {ref_med:,.0f} events and {ref_push:,.0f} PushEvents. " if refs else "")
        + "Counts are what the files held when read on 8 November 2026; they are not GitHub's own activity.")
s = [svg_open(W, H, "GH Archive hourly files: events and pushes per file, 1 September to 7 November 2026", desc)]
s.append(f'<rect width="{W}" height="{H}" fill="var(--bg)"/>')
before = [r for r in zero if r["label"] < "2026-10-15"]
s.append(f'<text class="head" x="{L - 48}" y="28">GH Archive\'s hourly files often held no pushes, September to November 2026</text>')
s.append(f'<text class="sub" x="{L - 48}" y="48">Events in each file read at 00, 06, 12 and 18 UTC, 1 September to 7 November 2026 ({len(panel)} files).</text>')
s.append(f'<text class="sub" x="{L - 48}" y="66">No PushEvent in {len(before)} of {sum(r["label"] < "2026-10-15" for r in panel)} files before 15 October and {len(zero) - len(before)} of {sum(r["label"] >= "2026-10-15" for r in panel)} from 15 October.</text>')
for v in range(0, ymax + 1, 20000):
    s.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
    s.append(f'<text class="ax" x="{L - 6}" y="{y(v) + 4:.1f}" text-anchor="end">{v // 1000}k</text>')
s.append(f'<line class="axis" x1="{L}" x2="{W - R}" y1="{BOT}" y2="{BOT}"/>')
for m in (dt.datetime(2026, 9, 1), dt.datetime(2026, 9, 15), dt.datetime(2026, 10, 1), dt.datetime(2026, 10, 15),
          dt.datetime(2026, 11, 1)):
    s.append(f'<line class="axis" x1="{x(m):.1f}" x2="{x(m):.1f}" y1="{BOT}" y2="{BOT + 5}"/>')
    s.append(f'<text class="ax" x="{x(m):.1f}" y="{BOT + 18}" text-anchor="middle">{m.day} {m.strftime("%b")}</text>')
if ref_med:
    s.append(f'<line x1="{L}" x2="{W - R}" y1="{y(ref_med):.1f}" y2="{y(ref_med):.1f}" stroke="var(--neutral)" stroke-width="1.5" stroke-dasharray="4 4"/>')
    s.append(f'<text class="ann" x="{W - R}" y="{y(ref_med) - 6:.1f}" text-anchor="end">Jan to Aug reference median, {ref_med / 1000:.0f}k events</text>')
for i, key in enumerate(("events", "PushEvent")):
    pts = " ".join(f"{x(when(r)):.1f},{y(int(r[key])):.1f}" for r in panel)
    stroke = series_stroke(i).replace('stroke-width="2.5"', 'stroke-width="1.5"')
    s.append(f'<polyline fill="none" {stroke} stroke-linejoin="round" points="{pts}"/>')
s.append(f'<text class="nm" x="{L + 6}" y="{TOP - 12}" style="fill:var(--teal)">All events (solid)</text>')
s.append(f'<text class="nm" x="{L + 150}" y="{TOP - 12}" style="fill:var(--amber)">PushEvents (dashed)</text>')
m15 = x(dt.datetime(2026, 10, 15))
s.append(f'<line x1="{m15:.1f}" x2="{m15:.1f}" y1="{y(ref_med) + 6 if ref_med else TOP:.1f}" y2="{BOT}" stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="2 3"/>')
# strip of files with no pushes
s.append(f'<text class="ann" x="{L - 6}" y="{STRIP + 12}" text-anchor="end">none</text>')
s.append(f'<text class="note" x="{L}" y="{STRIP - 6}">Files holding no PushEvent ({len(zero)} of {len(panel)}), one tick each</text>')
s.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{STRIP + 8}" y2="{STRIP + 8}"/>')
for r in zero:
    xx = x(when(r))
    s.append(f'<line x1="{xx:.1f}" x2="{xx:.1f}" y1="{STRIP}" y2="{STRIP + 16}" stroke="var(--amber)" stroke-width="1.5"/>')
s.append(f'<text class="note" x="{L - 48}" y="{H - 30}">Counts are what the files held when read on 8 November 2026, not GitHub\'s own activity.</text>')
s.append(f'<text class="note" x="{L - 48}" y="{H - 14}">Source: data.gharchive.org hourly files; Lighthouse study LH046, version 0.1, unreviewed.</text>')
s.append("</svg>")
open(OUT, "w").write("\n".join(s) + "\n")
print("wrote", OUT, len(panel), "panel files,", len(zero), "without pushes; max events", max(int(r["events"]) for r in panel))
