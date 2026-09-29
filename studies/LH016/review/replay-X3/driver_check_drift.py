"""LH016: the driving session's check of replay X3's problem 2, on LH012's
retained first-day table. Does a new version's share keep rising from day 2
to day 30? Reads studies/LH012/data/analysis/firstday_releases.csv (355
releases, November 2025 to March 2026, as LH012 kept them).

Run from the repository root:
python3 studies/LH016/review/replay-X3/driver_check_drift.py
"""
import csv
import statistics as st
from collections import defaultdict

rows = list(csv.DictReader(open("studies/LH012/data/analysis/firstday_releases.csv")))
d = [float(r["delta_points"]) for r in rows]
print(f"releases {len(d)}; day-30 share above day-2 share: {sum(x > 0 for x in d)}")
print(f"median day-30 minus day-2, points: {st.median(d):.2f}; quartiles "
      + ", ".join(f"{q:.2f}" for q in st.quantiles(d, n=4)))
print(f"above +10 points: {sum(x > 10 for x in d)}; below -10 points: {sum(x < -10 for x in d)}")
rat = [float(r["ratio_s2_s30"]) for r in rows if r["ratio_s2_s30"] not in ("", "nan")]
print(f"median day-2 share as a fraction of day-30: {st.median(rat):.3f}")
bp = defaultdict(list)
for r in rows:
    bp[r["project"]].append(float(r["delta_points"]))
meds = [st.median(v) for v in bp.values()]
print(f"projects {len(bp)}; median of project medians, points: {st.median(meds):.2f}; "
      f"projects whose median is above zero: {sum(m > 0 for m in meds)}")
