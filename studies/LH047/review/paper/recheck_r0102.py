"""R-0102: fresh recheck of the R-0100 resolution in the LH047 paper draft.

Checks (1) the summary sentence added after R-0100: of the 113 breaches under the brief as fixed,
how many are PyPI JSON-interface requests, how many Crawl-delay breaches exist only because the
robots.txt read counted as a request, whether the two classes overlap, and whether together they
are "most of the 113"; (2) the declined suggestion's reason: the 9 verdicts on robots.txt files
re-read afterwards, when those re-reads happened and how long after their requests.

Reads studies/LH047/data/audit/requests-judged.csv and studies/LH047/data/robots-index.csv only.
No network request. Run from the repository root:
    python3 -I studies/LH047/review/paper/recheck_r0102.py > studies/LH047/review/paper/recheck_r0102.out
Written 19 November 2026 by a fresh rechecker (Claude Code, Opus 5.5), after the figures had been
stated by the draft; it reproduces, it does not set new readings.
"""
import csv, collections, datetime as dt

rows = list(csv.DictReader(open("studies/LH047/data/audit/requests-judged.csv", newline="")))
idx = list(csv.DictReader(open("studies/LH047/data/robots-index.csv", newline="")))
bad = lambda r, k: r[k].startswith("does not comply")
t = lambda s: dt.datetime.fromisoformat(s.replace("Z", "+00:00"))

A = [r for r in rows if r["overall_A"] == "does not comply"]          # 172
post_hoc = [r for r in A if bad(r, "R8") and not any(bad(r, k) for k in ("R1", "R4", "R5", "R6", "R7"))]
F = [r for r in A if r not in post_hoc]                                # 113 as fixed
print("judged rows:", len(rows), "| overall_A breaches:", len(A), "| R8-only (post hoc):", len(post_hoc), "| as fixed:", len(F))

print("\n== 1. The summary's two classes, within the 113 ==")
pypi = [r for r in F if r["host"] == "pypi.org"]
pypi_r1 = [r for r in pypi if bad(r, "R1")]
pypi_json = [r for r in pypi if "/json" in r["url"]]
print("pypi.org requests among the 113:", len(pypi), "| breaking R1:", len(pypi_r1), "| URL contains /json:", len(pypi_json))
print("  pypi statuses:", dict(collections.Counter(r["status"] for r in pypi)))
print("  pypi R1_rule values:", dict(collections.Counter(r["R1_rule"] for r in pypi)))
print("  pypi, who:", dict(collections.Counter(r["who"] for r in pypi)))
print("  pypi breaking any other rule too:", sum(any(bad(r, k) for k in ("R4", "R5", "R6", "R7", "R8")) for r in pypi))
cd = [r for r in F if bad(r, "R5")]
cd_robots_only = [r for r in cd if r["R5_excl_robots"].startswith("complies")]
print("Crawl-delay (R5) breaches among the 113:", len(cd), "| complying once the robots.txt read is excluded:", len(cd_robots_only))
cd_only = [r for r in cd_robots_only if not any(bad(r, k) for k in ("R1", "R4", "R6", "R7", "R8"))]
print("  of those, breaking no other rule (so they count only because of the robots.txt read):", len(cd_only))
for r in cd_robots_only:
    print("   ", r["utc"], r["who"], r["host"], "min_gap", r["host_min_gap"], "| other rules broken:",
          [k for k in ("R1", "R4", "R6", "R7", "R8") if bad(r, k)])
ov = set(map(id, pypi)) & set(map(id, cd_only))
print("overlap PyPI x Crawl-delay-only:", len(ov))
both = len(set(map(id, pypi)) | set(map(id, cd_only)))
print(f"union: {both} of {len(F)} = {both/len(F):.1%}; more than half: {both > len(F)/2}")
print("PyPI alone:", f"{len(pypi)/len(F):.1%}", "| collector's 85 among PyPI:",
      sum(r["who"].startswith("LH041") for r in pypi))
rest = [r for r in F if id(r) not in set(map(id, pypi)) | set(map(id, cd_only))]
print("remaining", len(rest), "by rule:", dict(collections.Counter(
    "+".join(k for k in ("R1", "R4", "R5", "R6", "R7") if bad(r, k)) for r in rest)))

print("\n== 2. The 9 verdicts on current re-reads, and their lag ==")
cur = [r for r in A if r["robots_prov"].startswith("current")]
print("172 with robots_prov 'current re-read':", len(cur), "| among the 113:", sum(r in F for r in cur),
      "| among the post-hoc 59:", sum(r in post_hoc for r in cur))
byfile = {i["file"]: i for i in idx}
lags = []
for r in sorted(cur, key=lambda r: r["utc"]):
    i = byfile.get(r["robots_file"])
    rt = i["utc"] if i else "(not in index)"
    lag = (t(rt) - t(r["utc"])).total_seconds() / 60 if i else None
    lags.append(lag)
    print(f"   req {r['utc']}  reread {rt}  lag {lag if lag is None else round(lag,1)} min  {r['who']} {r['host']}  file {r['robots_file']}")
# file times for all current re-reads in the index (the window the piece states)
cur_files = sorted({r["robots_file"] for r in rows if r["robots_prov"].startswith("current")})
ct = sorted(byfile[f]["utc"] for f in cur_files if f in byfile)
print("current re-read files used anywhere in the audit:", len(cur_files), "| in index:", len(ct),
      "| earliest", ct[0] if ct else None, "| latest", ct[-1] if ct else None)
L = [x for x in lags if x is not None]
print(f"lag over the 9: min {min(L):.1f} min, max {max(L):.1f} min; over 25 min: {sum(x > 25 for x in L)} of {len(L)}")
aft = []
for r in A:
    if r["robots_prov"].startswith("current"):
        continue
    i = byfile.get(r["robots_file"])
    if i and r["utc"]:
        lag = (t(i["utc"]) - t(r["utc"])).total_seconds() / 60
        if lag > 0:
            aft.append(lag)
print(f"copies kept after the request (not current re-reads), among the 172: {len(aft)}, max lag {max(aft):.1f} min")
