"""LH041 evidence review (R-0057), second pass: the record's smaller figures
(clocks, out-of-window versions, seeds, lineage records, indicator strings,
PyPI statuses), recomputed from the retained read. Imports reproduce.py's
loaded state by running it as a module would be heavy, so it re-loads simply.

    python3 -I studies/LH041/review/checks2.py > studies/LH041/review/checks2-output.txt
"""
import collections, csv, gzip, io, json, os, re, statistics, sys, contextlib
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):  # load reproduce.py's state quietly
    g = {"__file__": os.path.join(HERE, "reproduce.py"), "__name__": "lh041_review"}
    exec(open(os.path.join(HERE, "reproduce.py")).read(), g)
live, WV, P, inwin, assign, npm, pypi, D, keep, defang, WAVES = (g[k] for k in
    ("live", "WV", "P", "inwin", "assign", "npm", "pypi", "D", "keep", "defang", "WAVES"))

def setview(posthoc):
    for x in live:
        x["wave"], x["join"] = assign(x, posthoc)

print("== PyPI release reads")
print(collections.Counter(r["status"] for r in pypi.values()), "reads:", len(pypi))

print("\n== indicator strings: records containing each W02 and W11 specific indicator")
for wid in ("W02", "W11", "W07", "W06", "W03", "W12", "W13"):
    for m in WV[wid]["specific"]:
        n = sum(1 for x in live if re.search(m, defang(x["raw"])))
        if n:
            print(wid, repr(m), n)

setview(False)
print("\n== versions with a registry time outside their wave's window (brief's view)")
for wid in ("W02", "W11", "W06"):
    ts = sorted(t for x in live if x["wave"] == wid for t in x["rt"].values() if t and not inwin(wid, t))
    print(wid, len(ts), collections.Counter(t.strftime("%Y-%m") for t in ts))

print("\n== ambiguous W02+W10 records")
for x in live:
    if x["join"].startswith("ambiguous"):
        r = json.loads(x["raw"])
        print(x["id"], x["pkg"].split("/")[0], "published", r.get("published"), "modified", r.get("modified"))

print("\n== lineage, unassigned (brief's view): by date month and marker")
lu = [x for x in live if x["join"] == "lineage, unassigned"]
def d(x):
    k = [t for t in x["rt"].values() if t]
    return min(k) if k else x["pub"]
print(len(lu), collections.Counter((x["eco"], d(x).strftime("%Y-%m")) for x in lu))
mk = collections.Counter()
for x in lu:
    t = defang(x["raw"])
    if d(x).strftime("%Y-%m") == "2026-03":
        mk[("canisterworm" in t, "teampcp" in t)] += 1
print("March 2026 records: (names canisterworm, names teampcp) ->", dict(mk))

print("\n== clocks (post hoc view)")
setview(True)
for wid in ("W01", "W02", "W06", "W07", "W08", "W11", "W12", "W13"):
    rs = [x for x in live if x["wave"] == wid]
    vs = [(t, x) for x in rs for t in x["rt"].values() if t and inwin(wid, t)]
    if not vs:
        continue
    first = min(t for t, _ in vs)
    osv_first = min(x["pub"] for x in rs)
    r_all = [json.loads(x["raw"]) for x in rs]
    imps = []
    bare = 0
    for r in r_all:
        if re.match(r"^\d{4}-\d\d-\d\dT00:00:00Z$", r.get("published", "")):
            bare += 1
        for o in (r.get("database_specific") or {}).get("malicious-packages-origins") or []:
            if o.get("import_time"):
                imps.append(P(o["import_time"]))
    lags = [(x["pub"] - t).total_seconds() / 3600 for t, x in vs]
    print(wid, "first registry", first, "| first OSV published - first registry (h) %.2f" % ((osv_first - first).total_seconds() / 3600),
          "| median version lag (h) %.2f" % statistics.median(lags),
          "| first import - first registry (h) %.2f" % ((min(imps) - first).total_seconds() / 3600) if imps else "",
          "| records with bare-date published", bare, "of", len(rs))

print("\n== W03 earliest OSV published among its records")
for posthoc in (False, True):
    setview(posthoc)
    print(min((x["pub"], x["id"]) for x in live if x["wave"] == "W03"))

print("\n== W08 hours to each new cluster (post hoc)")
o, rs, comps, h = keep[("W08", True, False)]
print(h)
o, rs, comps, h = keep[("W06", True, False)]
print("W06", h)
o, rs, comps, h = keep[("W01", True, False)]
print("W01", h)

print("\n== seeds: MAL records in the full index, and how the selected copies were classed (brief's view)")
setview(False)
idx = list(csv.DictReader(gzip.open(os.path.join(D, "osv-mal-index.csv.gz"), "rt")))
byid = {x["id"]: x for x in live}
for w in WAVES:
    for s in w["seeds"]:
        sl = s.lower()
        hit = [r for r in idx if (r["package"].lower().startswith(sl) if sl.endswith("/") else r["package"].lower() == sl)]
        cls = collections.Counter((byid[r["id"]]["wave"] or byid[r["id"]]["join"]) if r["id"] in byid else "not selected/withdrawn" for r in hit)
        print(w["id"], s, len(hit), dict(cls))
print("tensorlake-prefixed packages in the full MAL index:", sorted({r["package"] for r in idx if r["package"].lower().startswith("tensorlake") or r["package"].lower().startswith("@tensorlake")}))

print("\n== ChainDrop: math_init.js and Math_Symbol.js")
setview(True)
rs = [x for x in live if x["wave"] == "W11" and x["join"] == "indicator"]
print("records", len(rs), "naming math_init.js", sum(1 for x in rs if re.search(r"math_init\.js", x["raw"], re.I)),
      "naming math_symbol.js", sum(1 for x in rs if re.search(r"math_symbol\.js", x["raw"], re.I)))

print("\n== origins of ChainDrop's indicator records (reporting feeds)")
c = collections.Counter()
for x in rs:
    r = json.loads(x["raw"])
    c[";".join(sorted({o.get("source", "") for o in (r.get("database_specific") or {}).get("malicious-packages-origins") or []}))] += 1
print(c)
