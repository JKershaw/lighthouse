#!/usr/bin/env python3
"""LH042 evidence review: reproduce the record's series and derived figures with code
written for the review (it imports nothing from studies/LH042/scripts).

1. Parse OpenA2A's Exposure Prevalence Index table straight from the retained HTML
   (data/round4-2026-11-08/001.body), using the <time dateTime> cells and the
   data-label="..." cells, and compare every value with the hand transcription in
   data/counts.csv (series S42 to S45, S57).
2. Regroup all admitted counts into series by (publisher, method, class, product,
   kind, unit) and compare with the record's series ids: does any record series mix
   methods, kinds, units or publishers, and does any of my groups span two record series?
3. Print the series with two or more dates, with first, last, lowest, highest and
   steps, and the OpenClaw-family figures the record quotes (267,172; 153,638; 205,872).
Usage: python3 -I studies/LH042/review/reproduce.py"""
import csv, pathlib, re
from collections import defaultdict
HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parent / "data"

# 1. the index
raw = (D / "round4-2026-11-08" / "001.body").read_bytes().decode("utf-8")
tb = raw[raw.find("Recent sweeps"):]
tb = tb[:tb.find("</table>")]
idx = {}
for tr in re.findall(r"<tr>(.*?)</tr>", tb, re.S):
    m = re.search(r'<time dateTime="([0-9-]+)"', tr)
    if not m:
        continue
    cells = dict(re.findall(r'data-label="(\w+)"[^>]*>([0-9,]+)', tr))
    idx[m.group(1)] = {k: int(v.replace(",", "")) for k, v in cells.items()}
print("index rows parsed:", len(idx))
for d in sorted(idx):
    print(" ", d, idx[d])

rows = [r for r in csv.DictReader(open(D / "counts.csv")) if r["status"] == "admitted"]
col = {"S42": "OpenClaw", "S43": "LLM", "S44": "MCP", "S45": "Total", "S57": "Total"}
mism = 0; n = 0
for r in rows:
    if r["series"] in col:
        n += 1
        v = idx.get(r["date_end"], {}).get(col[r["series"]])
        if v != int(r["count"]):
            mism += 1
            print("MISMATCH", r["id"], r["series"], r["date_end"], r["count"], v)
print(f"index rows in counts.csv checked: {n}; mismatches: {mism}")
# totals split at OpenA2A's 18 June boundary
for r in rows:
    if r["series"] in ("S45", "S57"):
        side = "before" if r["date_end"] < "2026-06-18" else "after"
        exp = "S45" if side == "before" else "S57"
        if r["series"] != exp:
            print("BOUNDARY WRONG", r["id"], r["date_end"], r["series"])
print("A2A column (not admitted in the record):", [idx[d]["A2A"] for d in sorted(idx)])

# 2. regroup
groups = defaultdict(set)
by_series = defaultdict(list)
for r in rows:
    key = (r["publisher"], r["method"], r["cls"], r["product"], r["kind"], r["unit"])
    groups[key].add(r["series"])
    by_series[r["series"]].append(r)
print("\nmy groups:", len(groups), "record series:", len(by_series))
for k, s in groups.items():
    if len(s) > 1:
        print("one group, several record series:", s, k[:2])
for s, rs in by_series.items():
    for f in ("publisher", "method", "cls", "product", "kind", "unit"):
        vals = {r[f] for r in rs}
        if len(vals) > 1:
            print("record series", s, "varies in", f, vals)
# publishers (top-level organisation, by my own reading of the names)
def org(p):
    p = p.split(" (")[0]
    return p
orgs = sorted({org(r["publisher"]) for r in rows})
print("publishers (name before any parenthesis):", len(orgs))
for o in orgs:
    print("  ", o)

# 3. series with two or more dates
def key(r):
    d = r["date_end"]
    return d + "-15" if len(d) == 7 else d
print()
multi = 0
for s in sorted(by_series, key=lambda x: int(x[1:])):
    rs = sorted(by_series[s], key=key)
    dates = sorted({r["date_end"] for r in rs})
    if len(dates) < 2:
        continue
    multi += 1
    v = [int(r["count"]) for r in rs]
    up = sum(b > a for a, b in zip(v, v[1:])); dn = sum(b < a for a, b in zip(v, v[1:]))
    print(f"{s}: {len(dates)} dates {dates[0]}..{dates[-1]}; values {v}; first {v[0]:,} last {v[-1]:,} "
          f"lowest {min(v):,} ({rs[v.index(min(v))]['date_end']}) highest {max(v):,} ({rs[v.index(max(v))]['date_end']}); up {up} down {dn}")
print("series with two or more dates:", multi)
oc = {d: idx[d]["OpenClaw"] for d in idx}
print("\nOpenClaw-family (index): 2026-04-11 =", f"{oc['2026-04-11']:,}", "; 2026-06-26 =", f"{oc['2026-06-26']:,}",
      "; 2026-11-01 =", f"{oc['2026-11-01']:,}", "; max =", f"{max(oc.values()):,}", "on", max(oc, key=oc.get),
      "; min =", f"{min(oc.values()):,}", "on", min(oc, key=oc.get))
print("record figures 267,172 / 153,638 / 205,872 reproduced:",
      (oc["2026-04-11"], oc["2026-06-26"], oc["2026-11-01"]) == (267172, 153638, 205872))
