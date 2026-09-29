"""LH016: the driving session's check of replay X2's problem 3, on LH011's
retained table. When did litellm's releases that reached half of its
downloads within 30 days first do so? Reads
studies/LH011/data/analysis/release_days.csv as LH011 kept it.

Run from the repository root:
python3 studies/LH016/review/replay-X2/driver_check_litellm.py
"""
import csv
from collections import defaultdict

rows = [r for r in csv.DictReader(open("studies/LH011/data/analysis/release_days.csv"))
        if r["project"] == "litellm" and r["status"] == "known"]
by_version = defaultdict(list)
for r in rows:
    by_version[r["version"]].append(r)
found = []
for v, rs in by_version.items():
    rs.sort(key=lambda r: int(r["day"]))
    days = [r for r in rs if 1 <= int(r["day"]) <= 30 and float(r["share_at_or_newer"]) >= 0.5]
    if days:
        after = [r for r in rs if int(r["day"]) > int(days[0]["day"]) and int(r["day"]) <= 30]
        still = sum(float(r["share_at_or_newer"]) >= 0.5 for r in after)
        found.append((rs[0]["date"], v, int(days[0]["day"]), days[0]["date"],
                      float(days[0]["share_at_or_newer"]), still, len(after)))
found.sort()
print("released, version, first day at half, its date, share that day, later days at half of later days read")
for f in found:
    print(f"{f[0]} {f[1]} day {f[2]} {f[3]} {f[4]:.3f} {f[5]} of {f[6]}")
print(f"{len(found)} releases; first dates at half: {sorted(set(f[3] for f in found))}")
