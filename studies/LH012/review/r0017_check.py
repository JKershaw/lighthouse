"""Checks made by the release review of the corrected piece (version 1.1) and record (version 0.3), notes/R-0017.md.

No figure changed in that round, so nothing is recomputed from the raw counts; this recounts, from the retained
analysis tables, the classes and figures the reworded sentences rest on, and the short form's length.
Run from the repository root: python3 studies/LH012/review/r0017_check.py
"""
import csv
import re
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[3]
analysis = root / "studies/LH012/data/analysis"

python = list(csv.DictReader(open(analysis / "python.csv")))
bounds = list(csv.DictReader(open(analysis / "bounds.csv")))
week = {r["project"]: r for r in csv.DictReader(open(analysis / "week.csv"))}

print("A. Python exclusion, P: classes from python.csv")
pc = Counter(r["class"] for r in python)
print("  ", dict(pc))
print("   fewer than half (cannot, incl. little):", pc["cannot be the main reason"] + pc["accounts for little"])
for r in python:
    if r["class"] == "accounts for most":
        print(f"   {r['project']}: P {float(r['P_lower'])*100:.1f} to {float(r['P_upper'])*100:.1f}, edge share {float(r['edge_share'])*100:.1f}")
edges = sorted(float(r["edge_share"]) for r in python)
print(f"   median edge share over 37: {100*(edges[18]):.1f}")

print("B. Identified bounds, B: classes from bounds.csv")
bc = Counter(r["class"] for r in bounds)
print("  ", dict(bc))
print("   cannot (incl. little):", bc["cannot be the main reason"] + bc["accounts for little"])
for r in bounds:
    if r["class"] == "accounts for most":
        print(f"   {r['project']}: B {float(r['B_lower'])*100:.1f} to {float(r['B_upper'])*100:.1f}, from {r['lower_from']} at {float(r['lower_fetch_ratio']):.2f} times, held by current versions {float(r['largest_held_by_current_versions'])*100:.1f}, guard {float(r['guard_share_at_admitted'])*100:.1f}")
und = [r for r in bounds if r["class"] == "undetermined"]
print("   undetermined with upper at one:", sum(1 for r in und if float(r["B_upper"]) >= 0.999999), "of", len(und),
      "; smallest upper among them:", min(float(r["B_upper"]) for r in und))

print("C. 'most downloads of boto3 cannot have brought a download of either' (one-to-one bound)")
b3 = int(week["boto3"]["total"])
for p in ("botocore", "s3transfer"):
    t = int(week[p]["total"])
    print(f"   {p}: {t:,} of boto3's {b3:,} at most, {100*t/b3:.1f} per cent; boto3 over {p} {b3/t:.2f}")

print("D. 'for most of the others' (the 30 outside P-most and B-most)")
pm = {r["project"] for r in python if r["class"] == "accounts for most"}
bm = {r["project"] for r in bounds if r["class"] == "accounts for most"}
others = [r["project"] for r in python if r["project"] not in pm | bm]
pcl = {r["project"]: r["class"] for r in python}
bcl = {r["project"]: r["class"] for r in bounds}
p_cannot = [p for p in others if pcl[p] in ("cannot be the main reason", "accounts for little")]
b_und = [p for p in others if bcl[p] == "undetermined"]
both = [p for p in others if p in p_cannot and p in b_und]
print(f"   others {len(others)}; P fewer than half {len(p_cannot)}; B undetermined {len(b_und)}; both {len(both)}")

print("E. The short form's length (articles/short/old-versions-new-pythons.md)")
lines = open(root / "articles/short/old-versions-new-pythons.md").read().split("\n")
i = next(k for k, l in enumerate(lines) if l.startswith("# "))
j = next(k for k, l in enumerate(lines) if l.strip() == "---")
body = lines[i + 1:j]


def wc(ls):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", "\n".join(ls))
    return len(s.split())


k = next(m for m, l in enumerate(body) if l.startswith("*29 September"))
print("   words after the title, before the colophon:", wc(body))
print("   the same without the Correction notice:", wc([l for l in body if not l.startswith("> **Correction")]))
print("   words after the byline:", wc(body[k + 1:]))
