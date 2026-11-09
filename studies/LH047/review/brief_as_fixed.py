"""LH047 review (R-0065 resolution): the headline count under the brief as fixed, and what the 172 are.

Reads studies/LH047/data/audit/requests-judged.csv and studies/LH047/data/robots-index.csv only;
makes no network request. Run from the repository root:
    python3 -I studies/LH047/review/brief_as_fixed.py > studies/LH047/review/brief_as_fixed.out

Written by the driving session's resolution subagent on 9 November 2026, after every figure was seen.

1. Under the brief as fixed (section 5, R8), a User-Agent fails identification only if it claims to be a
   browser. The essay reader review's `Mozilla/5.0 (compatible; research-reader/1.0)` has the shape of
   LH044's `Mozilla/5.0 (compatible; Lighthouse-research/1.0; ...)`, which the audit judged compliant, and
   the brief has no class for a name that is neither Lighthouse's nor a tool's default. The audit's
   "does not comply" for it was made after it was seen (Method 5d). Here those 61 are set aside as
   unclassified, and the overall counts are recomputed.
2. What the 172 are: response status, practice (who sent them), Crawl-delay with and without robots.txt
   reads, and where each verdict's robots.txt came from.
"""
import csv
import collections

J = "studies/LH047/data/audit/requests-judged.csv"
IDX = "studies/LH047/data/robots-index.csv"
rows = list(csv.DictReader(open(J, newline="")))


def fails(r, k):
    return r[k].startswith("does not comply")


def show(title, counter):
    print(title)
    for k, v in counter.most_common():
        print(f"  {v:5d}  {k}")


A = [r for r in rows if r["overall_A"] == "does not comply"]
print(f"requests: {len(rows)}; overall reading A does not comply: {len(A)}")
show("R8 verdicts, all requests:", collections.Counter(r["R8"] for r in rows))

print("\n## 1. Under the brief as fixed (the post hoc R8 class set aside)")
for col, r1 in (("overall_A", "R1"), ("overall_B", "R2"), ("overall_B_agent", "R2_agent")):
    bad = [r for r in rows if r[col] == "does not comply"]
    only8 = [r for r in bad if fails(r, "R8") and not any(fails(r, k) for k in (r1, "R4", "R5", "R6", "R7"))]
    print(f"{col}: {len(bad)} do not comply; {len(only8)} of them fail on R8 alone; "
          f"under the brief as fixed {len(bad) - len(only8)}")
r8 = [r for r in rows if fails(r, "R8")]
print(f"R8 fails: {len(r8)}; of them also failing R1: {sum(fails(r, 'R1') for r in r8)}")
show("R8 fails by who and source:", collections.Counter((r["who"], r["source"]) for r in r8))
only8A = [r for r in A if fails(r, "R8") and not any(fails(r, k) for k in ("R1", "R4", "R5", "R6", "R7"))]
show("the R8-only requests' R1 verdict:", collections.Counter(r["R1"] for r in only8A))
fixed = [r for r in A if r not in only8A]
print(f"brief as fixed, reading A: {len(fixed)}")

print("\n## 2. What the 172 are")
show("status, all 172:", collections.Counter(r["status"] or "(none recorded)" for r in A))
show("status, the 113:", collections.Counter(r["status"] or "(none recorded)" for r in fixed))
py = [r for r in A if r["host"] == "pypi.org"]
show(f"pypi.org requests among the 172 ({len(py)}), status:", collections.Counter(r["status"] for r in py))
show("pypi.org requests by who:", collections.Counter(r["who"] for r in py))
lh041 = [r for r in A if r["who"] == "LH041"]
rr = [r for r in A if fails(r, "R8")]
both = {id(r) for r in lh041} | {id(r) for r in rr}
print(f"LH041's collector: {len(lh041)}; the essay reader review's User-Agent: {len(rr)} "
      f"({sum(r['source'] == 'log' for r in rr)} logged, {sum(r['source'] == 'transcript' for r in rr)} ad hoc); "
      f"the two practices together: {len(both)} of {len(A)}")
show("the 172 by who:", collections.Counter(r["who"] for r in A))
show("the 113 by who:", collections.Counter(r["who"] for r in fixed))
rules = collections.Counter()
for r in fixed:
    rules[" + ".join(k for k in ("R1", "R4", "R5", "R6", "R7", "R8") if fails(r, k))] += 1
show("the 113 by failing rule(s):", rules)
r5 = [r for r in A if fails(r, "R5")]
print(f"Crawl-delay (R5) fails: {len(r5)}; still failing when robots.txt reads are not counted as requests: "
      f"{sum(fails(r, 'R5_excl_robots') for r in r5)}")
show("robots.txt provenance, the 172:", collections.Counter(r["robots_prov"] for r in A))
show("robots.txt provenance, the 113:", collections.Counter(r["robots_prov"] for r in fixed))

idx = [x for x in csv.DictReader(open(IDX, newline="")) if x["file"] == "studies/LH044/data/read-2026-11-08T1920Z/0031.b"]
print("\nPyPI robots.txt copy deciding the pypi.org verdicts:",
      collections.Counter(r["robots_file"] for r in py).most_common(1), "read at", [x["utc"] for x in idx])
print("first LH041 pypi.org request:", min(r["utc"] for r in py if r["who"] == "LH041"))
print("other pypi.org requests:", sorted(r["utc"] for r in py if r["who"] != "LH041"))

addB = [r for r in rows if r["overall_B"] == "does not comply" and r["overall_A"] != "does not comply"]
show(f"\nreading B adds {len(addB)}; their robots.txt provenance:", collections.Counter(r["robots_prov"] for r in addB))
