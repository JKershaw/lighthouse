"""Recheck of LH047 record 0.3's revised figures (R-0067). Reads only the judged table.
Run: python3 -I studies/LH047/review/recheck/recheck.py"""
import csv, collections, pathlib
here = pathlib.Path(__file__).resolve().parents[2]
rows = list(csv.DictReader(open(here / "data/audit/requests-judged.csv", newline="")))
C = collections.Counter
print("requests:", len(rows))
ts = sorted(r["utc"] for r in rows if r["utc"])
print("utc min/max:", ts[0], ts[-1], "missing utc:", sum(1 for r in rows if not r["utc"]))
print("by source:", dict(C(r["source"] for r in rows)))
dnc = lambda v: v.startswith("does not")
# robots.txt verdict column for each reading: R1 (reading A), R2 (all seven Anthropic tokens), R2_agent (agent tokens only)
for col, rob in (("overall_A", "R1"), ("overall_B", "R2"), ("overall_B_agent", "R2_agent")):
    fails = [r for r in rows if dnc(r[col])]
    def others(r):
        return [k for k in (rob, "R4", "R5", "R6", "R7") if dnc(r[k])]
    r8only = [r for r in fails if dnc(r["R8"]) and not others(r)]
    print(col, "fails", len(fails), "R8-only", len(r8only), "without them", len(fails) - len(r8only))
    print("  overall values:", dict(C(r[col] for r in rows)))
A = [r for r in rows if dnc(r["overall_A"])]
print("R8 fails total:", sum(dnc(r["R8"]) for r in rows), "R8 and R1:", sum(dnc(r["R8"]) and dnc(r["R1"]) for r in rows))
print("status of 172:", dict(C(r["status"] for r in A)))
py = [r for r in A if r["host"] == "pypi.org"]
print("pypi in 172:", len(py), dict(C(r["status"] for r in py)), dict(C(r["who"] for r in py)))
print("pypi json urls:", sum("/json" in r["url"] for r in py))
lh041 = [r for r in A if r["who"] == "LH041"]
ua = [r for r in A if dnc(r["R8"])]
print("LH041 in 172:", len(lh041), "R8 fails in 172:", len(ua), "union:", len({id(r) for r in lh041} | {id(r) for r in ua}))
print("LH041 robots_first:", dict(C(r["robots_first"] for r in lh041)))
print("provenance, all:", dict(C(r["robots_prov"] for r in rows)))
print("provenance, 172:", dict(C(r["robots_prov"] for r in A)))
cur = [r for r in A if r["robots_prov"].startswith("current")]
print("current re-read among 172, by rule failing:", [(r["host"], [k for k in ('R1','R4','R5','R8') if dnc(r[k])]) for r in cur])
print("R5 fails:", sum(dnc(r["R5"]) for r in rows), "R5 excl robots:", dict(C(r["R5_excl_robots"] for r in rows if dnc(r["R5"]))))
print("R4 fails:", sum(dnc(r["R4"]) for r in rows), "R1 fails:", sum(dnc(r["R1"]) for r in rows), "R1 unknown:", sum(r["R1"].startswith("unknown") for r in rows))

# When was the deciding robots.txt copy read, relative to each of the 172 requests?
idx = {}
for r in csv.DictReader(open(here / "data/robots-index.csv", newline="")):
    idx.setdefault(r["file"], []).append(r["utc"])
when = C()
for r in A:
    f = r["robots_file"]
    if r["robots_prov"].startswith("current"):
        when["current re-read, 20:40 to 20:43"] += 1
    elif f in idx:
        t = min(idx[f])
        when[("copy read before request" if t <= r["utc"] else "copy read after request") + " (" + r["robots_prov"] + ")"] += 1
    else:
        when["no indexed copy: " + r["robots_prov"]] += 1
print("deciding robots.txt copy vs request time, the 172:")
for k, v in sorted(when.items()): print(f"  {v:4d}  {k}")

# The 65 verdicts among the 172 whose deciding copy was read after the request: how many are R8-only, and the largest gap
from datetime import datetime
P = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
after, gaps = [], []
for r in A:
    f = r["robots_file"]
    if r["robots_prov"].startswith("current"):
        after.append(r)
    elif r["robots_prov"].startswith("retained") and f in idx and min(idx[f]) > r["utc"]:
        after.append(r); gaps.append((P(min(idx[f])) - P(r["utc"])).total_seconds() / 60)
r8only = lambda r: dnc(r["R8"]) and not any(dnc(r[k]) for k in ("R1", "R4", "R5", "R6", "R7"))
print("read after the request:", len(after), "of them R8-only (post hoc):", sum(r8only(r) for r in after),
      "; retained copies read after: largest gap %.1f min" % max(gaps))
print("  failing on a robots.txt-decided rule (R1/R4/R5):", [(r["host"], r["robots_prov"][:20]) for r in after if not r8only(r)])
