#!/usr/bin/env python3
"""Checks of finer Findings sentences, written AFTER the record was opened (so a check, not an independent
reproduction). Reuses the reproduction's share function by importing reproduce_lh011 with its output
redirected to a scratch directory. Prints: per-project median day-30 share for the eleven, how many
releases reached half by day 30, how many on day 0, litellm's releases that reached half and their day."""
import os, statistics, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], tempfile.mkdtemp()]
import reproduce_lh011 as R   # noqa: runs the reproduction into the temp dir
ONE = R.ONE
rows = []
for r in R.releases:
    s30 = R.share(r['project'], r['V'], r['day0'] + 30 * ONE)
    rows.append((r['project'], r['version'], r['s1'], s30, r['days_to_half']))
eleven = [p for p, v in R.proj.items() if v['cls'] == 'none reached']
print("eleven projects: median day-1 share -> median day-30 share (releases whose day 30 is held)")
for p in sorted(eleven, key=lambda p: float(R.proj[p]['median_day1_share'])):
    d1 = [s1 for pp, _, s1, _, _ in rows if pp == p and s1 is not None]
    d30 = [s30 for pp, _, _, s30, _ in rows if pp == p and s30 is not None]
    print(f"  {p:18s} {100*statistics.median(d1):5.1f} -> {100*statistics.median(d30):5.1f}  (n {len(d1)}, day-30 held {len(d30)})")
reached = [(p, v, d) for p, v, _, _, d in rows if isinstance(d, int)]
print("releases reaching half within 30 days:", len(reached), "; on day 0:", sum(1 for _, _, d in reached if d == 0),
      "; median day:", statistics.median(d for _, _, d in reached))
lit = [(v, d) for p, v, d in reached if p == 'litellm']
print("litellm releases reaching half:", len(lit), lit, "median day", statistics.median(d for _, d in lit) if lit else None)
print("day 0 of each litellm release that reached, and the day it reached:")
for r in R.releases:
    if r['project'] == 'litellm' and isinstance(r['days_to_half'], int):
        print("  ", r['version'], r['day0'], "reached on", r['day0'] + r['days_to_half'] * ONE)
print("projects none of whose releases reached half by day 30:", sum(1 for p in eleven if not any(pp == p for pp, _, _ in reached)))

# the piece's opening example (articles/two-days-for-most.md): requests 2.34.0 and pandas 3.0.3, released 11 May 2026
for p, v in (('requests', '2.34.0'), ('pandas', '3.0.3')):
    r = next(r for r in R.releases if r['project'] == p and r['version'] == v)
    d1 = r['day0'] + ONE
    rows1 = R.counts[p][d1.isoformat()]
    num = sum(n for vv, n in rows1.items() if vv != '~other' and R.Version(vv) >= r['V'])
    print(f"{p} {v}: day 0 {r['day0']}, day 1 at-or-newer {num:,} of {sum(rows1.values()):,} = {100*num/sum(rows1.values()):.1f} per cent; day 30 {100*R.share(p, r['V'], r['day0'] + 30*ONE):.1f} per cent")
