"""r0025_recheck_day1_half: is the day-1 at-or-newer share most of the day-30 share, by release and by project?

Made by the recheck of the correction round of 29 September 2026 (notes/R-0025.md, "Recheck, by a fresh agent"),
to check the piece's sentence "In every library but litellm, whatever share a new version held on the day after
its release was most of what it held a month later" (articles/two-days-for-most.md, version 1.2, "The first day
set most of the month's share"). Reads only the retained daily table; no download count is fetched.

Run from the repository root: python3 studies/LH011/review/r0025_recheck_day1_half.py > studies/LH011/review/r0025_recheck_day1_half.txt
"""
import csv
import statistics
from collections import Counter, defaultdict

TABLE = "studies/LH011/data/analysis/release_days.csv"

shares = defaultdict(dict)
for row in csv.DictReader(open(TABLE)):
    if row["status"] != "known" or row["share_at_or_newer"] == "":
        continue
    shares[(row["project"], row["version"])][int(row["day"])] = float(row["share_at_or_newer"])

held = {key: days for key, days in shares.items() if 1 in days and 30 in days}
under_half = Counter()
per_project = Counter()
day1 = defaultdict(list)
day30 = defaultdict(list)
for (project, version), days in held.items():
    per_project[project] += 1
    day1[project].append(days[1])
    day30[project].append(days[30])
    if days[1] < 0.5 * days[30]:
        under_half[project] += 1

print("1. By release: releases with day 1 and day 30 held: %d; day-1 share under half of day-30 share: %d"
      % (len(held), sum(under_half.values())))
for project, count in under_half.most_common():
    print("   %s: %d of %d" % (project, count, per_project[project]))

print("2. By project, the chart's median lines: median day-1 share over median day-30 share")
below = []
for project in sorted(per_project):
    ratio = statistics.median(day1[project]) / statistics.median(day30[project])
    if ratio < 0.5:
        below.append((project, ratio))
print("   projects: %d; median line on day 1 under half of its day-30 median: %d%s"
      % (len(per_project), len(below), "".join(" (%s %.2f)" % b for b in below)))
