"""r0025_recheck_lh014_rise: the change from day 2 to day 30 in LH014's retained tables, by band.

Made by the recheck of the correction round of 29 September 2026 (notes/R-0025.md, "Recheck, by a fresh agent"),
to check the figures the record's Next gives for LH014 ("project medians of the change of 4.4 and 6.1 points in
its two bands"), which had no kept calculation. A description of data already read, not a test. Reads only
LH014's retained tables; no download count is fetched.

Run from the repository root: python3 studies/LH012/review/r0025_recheck_lh014_rise.py > studies/LH012/review/r0025_recheck_lh014_rise.txt
"""
import csv
import statistics
from collections import defaultdict

RELEASES = "studies/LH014/data/analysis/release_outcomes.csv"
PROJECTS = "studies/LH014/data/analysis/project_outcomes.csv"

releases = list(csv.DictReader(open(RELEASES)))
projects = list(csv.DictReader(open(PROJECTS)))

for band in ("A", "B"):
    rows = [r for r in releases if r["band"] == band and r["share_day30"] != "" and r["share_day2"] != ""]
    delta = [(float(r["share_day30"]) - float(r["share_day2"])) * 100 for r in rows]
    stored = [float(r["delta_pp"]) for r in rows]
    by_project = defaultdict(list)
    for r, d in zip(rows, delta):
        by_project[r["project"]].append(d)
    medians = [statistics.median(v) for v in by_project.values()]
    column = [float(p["median_delta_pp"]) for p in projects if p["band"] == band and p["median_delta_pp"] != ""]
    print("band %s (ranks %s): releases with day 2 and day 30: %d; higher on day 30: %d; lower: %d; median %.2f points"
          % (band, "51 to 500" if band == "A" else "501 to 5,000", len(rows),
             sum(d > 0 for d in delta), sum(d < 0 for d in delta), statistics.median(delta)))
    print("   delta_pp as stored differs from the recomputed change by at most %.5f points" % max(abs(a - b) for a, b in zip(stored, delta)))
    print("   projects with such a release: %d; project medians above zero: %d; median of project medians %.3f points"
          % (len(medians), sum(m > 0 for m in medians), statistics.median(medians)))
    print("   the same from project_outcomes.csv's median_delta_pp: %d projects, median %.3f"
          % (len(column), statistics.median(column)))
