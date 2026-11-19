"""R-0100 reader-and-inference review of the LH047 paper draft: checks of figures the piece states.

Reads studies/LH047/data/audit/requests-judged.csv and studies/LH047/data/robots-index.csv only;
no network request. Run from the repository root:
    python3 -I studies/LH047/review/paper/reader_checks.py > studies/LH047/review/paper/reader_checks.out
Written 19 November 2026 by the reader-and-inference reviewer (Claude Code, Opus 5.5), after every figure was seen.
"""
import csv, collections, datetime as dt, re

rows = list(csv.DictReader(open("studies/LH047/data/audit/requests-judged.csv", newline="")))
idx = list(csv.DictReader(open("studies/LH047/data/robots-index.csv", newline="")))
fails = lambda r, k: r[k].startswith("does not comply")
A = [r for r in rows if r["overall_A"] == "does not comply"]
only8 = [r for r in A if fails(r, "R8") and not any(fails(r, k) for k in ("R1", "R4", "R5", "R6", "R7"))]
F = [r for r in A if r not in only8]
print("172:", len(A), " 113:", len(F))

# 1. Reading B's extra 19: which tokens' groups catch them
B = [r for r in rows if r["overall_B"] == "does not comply" and r["overall_A"] != "does not comply"]
print("\n1. reading B adds:", len(B))
for r in B:
    print("  ", r["who"], r["host"], "| R2_tokens:", r["R2_tokens"], "| R2_agent:", r["R2_agent"])
print("  all mention ClaudeBot:", all("claudebot" in r["R2_tokens"].lower() for r in B))
print("  agent-token reading catches", sum(r["overall_B_agent"] == "does not comply" for r in B), "of them")

# 2. Provenance of the robots.txt copy and its lag after the request, the 172
print("\n2. robots_prov, the 172:")
idx_by_file = {}
print("   robots-index columns:", list(idx[0].keys()))
for i in idx:
    for k in ("path", "file", "robots_file"):
        if k in i:
            idx_by_file[i[k]] = i
def parse(t):
    try:
        return dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
    except Exception:
        return None
tcol = [c for c in idx[0] if "utc" in c.lower() or "time" in c.lower()]
print("   index time columns:", tcol)
after = []
for r in A:
    i = idx_by_file.get(r["robots_file"]) or idx_by_file.get(r["robots_file"].replace("studies/LH047/", ""))
    lag = None
    if i and tcol:
        a, b = parse(r["utc"]), parse(i[tcol[0]])
        if a and b:
            lag = (b - a).total_seconds() / 60
    r["_lag"] = lag
c = collections.Counter()
for r in A:
    lag = r["_lag"]
    k = (r["robots_prov"], "after request" if (lag is not None and lag > 0) else ("before/at" if lag is not None else "no time"))
    c[k] += 1
for k, v in c.most_common():
    print(f"   {v:4d} {k}")
cur = [r for r in A if r["robots_prov"].startswith("current")]
aft = [r for r in A if not r["robots_prov"].startswith("current") and r["_lag"] is not None and r["_lag"] > 0]
print("   current re-read:", len(cur), "; earlier copy kept after the request:", len(aft),
      "; max lag min:", max((r["_lag"] for r in aft), default=None))
print("   of these", len(cur) + len(aft), ", among the reviewer's R8-only 59:",
      sum(r in only8 for r in cur + aft))

# 3. Decomposition of the 113 by what the rule rests on
print("\n3. the 113 by component:")
comp = collections.Counter()
for r in F:
    if r["host"] == "pypi.org":
        k = "PyPI documented JSON interface (R1)"
    elif fails(r, "R5") and not fails(r, "R1") and not fails(r, "R4") and r["R5_excl_robots"].startswith("complies"):
        k = "Crawl-delay only because robots.txt read counted (R5)"
    elif fails(r, "R5"):
        k = "Crawl-delay page to page (R5)"
    elif fails(r, "R4"):
        k = "use=reference, pages kept (R4)"
    elif fails(r, "R1"):
        k = "other robots.txt (R1): " + r["host"]
    else:
        k = "other"
    comp[k] += 1
for k, v in sorted(comp.items(), key=lambda x: -x[1]):
    print(f"   {v:4d} {k}")
print("   R5_excl_robots values among R5 fails:", collections.Counter(r["R5_excl_robots"] for r in F if fails(r, "R5")))

# 4. The 85: status and the PyPI URLs' shape
py = [r for r in F if r["host"] == "pypi.org" and r["who"] == "LH041"]
print("\n4. LH041 pypi:", len(py), collections.Counter(r["status"] for r in py))
print("   first/last utc:", min(r["utc"] for r in py), max(r["utc"] for r in py))
print("   sample urls:", [r["url"] for r in py[:5]])
print("   robots copy:", collections.Counter(r["robots_file"] for r in py), collections.Counter(r["R1_rule"] for r in py))
