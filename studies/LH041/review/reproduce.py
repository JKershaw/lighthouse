"""LH041 evidence review (R-0057): an independent re-derivation of the record's
important figures from the retained read, written by the reviewer without
reusing tabulate.py's code. Reads only studies/LH041/data/<read>/ and the
protocol's indicator lists in scripts/waves.py (the fixed input, read as data).

    python3 -I studies/LH041/review/reproduce.py [read]   > studies/LH041/review/reproduce-output.txt

Nothing from any malicious-package record is run; records and packument
extracts are parsed as JSON text.
"""
import ast, collections, gzip, json, os, re, statistics, sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
READ = sys.argv[1] if len(sys.argv) > 1 else "2026-11-08T1910Z"
D = os.path.join(ROOT, "data", READ)

# --- protocol, read from waves.py as a literal (not imported) -------------
src = open(os.path.join(ROOT, "scripts", "waves.py")).read()
tree = ast.parse(src)
LINEAGE, WAVES = None, []
for node in tree.body:
    if isinstance(node, ast.Assign) and node.targets[0].id == "LINEAGE":
        LINEAGE = ast.literal_eval(node.value)
    if isinstance(node, ast.Assign) and node.targets[0].id == "WAVES":
        for call in node.value.elts:
            WAVES.append({k.arg: ast.literal_eval(k.value) for k in call.keywords})
WV = {w["id"]: w for w in WAVES}

def P(t):  # parse an ISO time to aware UTC, tolerating nanoseconds
    if not t:
        return None
    m = re.match(r"(\d{4}-\d\d-\d\d)(?:T(\d\d:\d\d:\d\d)(?:\.(\d+))?)?(Z|[+-]\d\d:\d\d)?$", t)
    if not m:
        raise ValueError(t)
    base = m.group(1) + "T" + (m.group(2) or "00:00:00")
    frac = (m.group(3) or "0")[:6].ljust(6, "0")
    return datetime.strptime(base + "." + frac, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)

def window(wid):
    a, b = WV[wid]["window"]
    return P(a), P(b) + timedelta(days=1)

def inwin(wid, t):
    a, b = window(wid)
    return a <= t < b

def defang(s):
    s = s.lower()
    for x, y in (("[.]", "."), ("(.)", "."), ("[dot]", "."), ("(dot)", "."), ("hxxp", "http"), ("[:]", ":")):
        s = s.replace(x, y)
    return s

# --- data -------------------------------------------------------------------
sel = [json.loads(l) for l in gzip.open(os.path.join(D, "osv-selected.jsonl.gz"), "rt")]
npm = {}
for l in gzip.open(os.path.join(D, "npm-extract.jsonl.gz"), "rt"):
    r = json.loads(l); npm[r["package"]] = r
pypi = {}
for l in gzip.open(os.path.join(D, "pypi-extract.jsonl.gz"), "rt"):
    r = json.loads(l); pypi[(r["package"], r["version"])] = r

print("== selection")
print("selected records:", len(sel), collections.Counter(s["ecosystem"] for s in sel))

recs = []
mismatch = 0
for s in sel:
    raw = s["raw"]; r = json.loads(raw)
    t = defang(raw)
    lin = [m for m in LINEAGE if re.search(m, t)]
    spec = {w["id"] for w in WAVES if any(re.search(m, t) for m in w["specific"])}
    shar = {w["id"] for w in WAVES if any(re.search(m, t) for m in w["shared"])}
    seed = None
    pkg = ((r.get("affected") or [{}])[0].get("package") or {}).get("name", "")
    for w in WAVES:
        for sd in w["seeds"]:
            if (sd.endswith("/") and pkg.lower().startswith(sd.lower())) or pkg.lower() == sd.lower():
                seed = w["id"]
    # does my match agree with the collector's stored match?
    if spec != set(s["match"]["specific"]) or shar != set(s["match"]["shared"]) or bool(lin) != bool(s["match"]["lineage"]):
        mismatch += 1
    if not (lin or spec or shar or seed):
        print("  record selected but my matcher finds nothing:", r["id"])
    vers = sorted({v for a in r.get("affected") or [] for v in a.get("versions") or []})
    eco = s["ecosystem"]
    rt = {}
    for v in vers:
        if eco == "npm":
            tt = ((npm.get(pkg) or {}).get("time") or {}).get(v)
            rt[v] = P(tt) if tt else None
        else:
            ups = [u for u in (pypi.get((pkg, v)) or {}).get("uploads") or [] if u]
            rt[v] = P(min(ups)) if ups else None
    recs.append(dict(id=r["id"], eco=eco, pkg=pkg, vers=vers, rt=rt, spec=spec, shar=shar, lin=bool(lin), seed=seed,
                     withdrawn=bool(r.get("withdrawn")), pub=P(r.get("published")),
                     raw=raw))
print("records where my matcher disagrees with the stored match:", mismatch)
print("withdrawn:", [x["id"] for x in recs if x["withdrawn"]])

def assign(x, posthoc):
    if len(x["spec"]) == 1:
        return next(iter(x["spec"])), "indicator"
    if len(x["spec"]) > 1:
        return None, "ambiguous " + "+".join(sorted(x["spec"]))
    if x["shar"] or x["lin"]:
        cand = sorted(x["shar"]) if x["shar"] else sorted(WV)
        if posthoc:
            cand = [w for w in cand if x["eco"] in WV[w]["eco"]]
        known = [t for t in x["rt"].values() if t]
        d = min(known) if known else x["pub"]
        hit = [w for w in cand if d and inwin(w, d)]
        if len(hit) == 1:
            return hit[0], "window"
        return None, ("window-overlap " + "+".join(hit)) if hit else "lineage, unassigned"
    return None, "seed only"

live = [x for x in recs if not x["withdrawn"]]
for posthoc in (False, True):
    print("\n== joins,", "post hoc view" if posthoc else "brief's view")
    for x in live:
        x["wave"], x["join"] = assign(x, posthoc)
    c = collections.Counter(x["join"] for x in live)
    for k, v in sorted(c.items()):
        print(" ", k, v)

def clusters(rs, wid, posthoc):
    """Union packages that share any hashed current maintainer. Returns list of
    (first in-scope registry time, packages) per cluster, earliest first, and counts."""
    pk_first, pk_m = {}, {}
    nopk = notime = placeholder = 0
    pkgs = sorted({x["pkg"] for x in rs if x["eco"] == "npm"})
    for p in pkgs:
        ts = [t for x in rs if x["pkg"] == p and x["eco"] == "npm" for v, t in x["rt"].items()
              if t and (not posthoc or inwin(wid, t))]
        e = npm.get(p) or {}
        ms = set(m for m in e.get("maintainers_h") or [] if m)
        lst = e.get("versions_listed") or []
        ph = bool(lst) and all(v.endswith("-security") for v in lst)
        if e.get("status") != 200:
            nopk += 1
        if ph:
            placeholder += 1
        if not ts:
            notime += 1
        if ms and ts and not ph:
            pk_first[p] = min(ts); pk_m[p] = ms
    # connected components via BFS on the package-maintainer graph
    by_m = collections.defaultdict(set)
    for p, ms in pk_m.items():
        for m in ms:
            by_m[m].add(p)
    seen, comps = set(), []
    for p in pk_m:
        if p in seen:
            continue
        stack, comp = [p], set()
        while stack:
            q = stack.pop()
            if q in comp:
                continue
            comp.add(q)
            for m in pk_m[q]:
                stack.extend(by_m[m] - comp)
        seen |= comp
        comps.append((min(pk_first[q] for q in comp), sorted(comp)))
    comps.sort()
    return comps, dict(npm_packages=len(pkgs), no_packument=nopk, no_time=notime, placeholder=placeholder,
                       known_both=len(pk_m))

def report(wid, posthoc, indicator_only=False):
    rs = [x for x in live if x["wave"] == wid and (not indicator_only or x["join"] == "indicator")]
    vers = [(x["pkg"], v, t) for x in rs for v, t in x["rt"].items()]
    if posthoc:
        vers_in = [(p, v, t) for p, v, t in vers if t is None or inwin(wid, t)]
    else:
        vers_in = vers
    known = sorted(t for _, _, t in vers_in if t)
    comps, cnt = clusters(rs, wid, posthoc)
    out = dict(wave=wid, view="posthoc" if posthoc else "brief", scope="indicator" if indicator_only else "indicator+window",
               records=len(rs), packages=len({(x["eco"], x["pkg"]) for x in rs}),
               versions=len(vers_in), registry_dated=len(known),
               first=known[0].strftime("%Y-%m-%d %H:%M:%S") if known else "",
               last=known[-1].strftime("%Y-%m-%d %H:%M:%S") if known else "",
               span_h=round((known[-1] - known[0]).total_seconds() / 3600, 2) if known else "",
               clusters=len(comps), **cnt)
    if comps:
        t0 = comps[0][0]
        later = [c for c in comps[1:] if c[0] > t0]
        out["first_cluster_packages"] = len(comps[0][1])
        out["later_clusters"] = len(later)
        out["packages_in_later_clusters"] = sum(len(c[1]) for c in later)
        out["largest_cluster"] = max(len(c[1]) for c in comps)
        out["hours_to_each_new_cluster"] = [round((c[0] - t0).total_seconds() / 3600, 2) for c in later]
        out["cluster_sizes_in_order"] = [len(c[1]) for c in comps]
        if later:
            hs = sorted((c[0] - t0).total_seconds() / 3600 for c in later)
            out["median_new_cluster_h_lower"] = round(hs[(len(hs) - 1) // 2], 2)
            out["median_new_cluster_h_statistics"] = round(statistics.median(hs), 2)
    return out, rs, comps

print("\n== per wave")
keep = {}
for posthoc in (False, True):
    for x in live:
        x["wave"], x["join"] = assign(x, posthoc)
    for wid in WV:
        for ind in (True, False):
            o, rs, comps = report(wid, posthoc, ind)
            if o["records"]:
                h = o.pop("hours_to_each_new_cluster", None)
                print(json.dumps(o))
                keep[(wid, posthoc, ind)] = (o, rs, comps, h)

# --- headline checks --------------------------------------------------------
print("\n== headline checks")
o, rs, comps, h = keep[("W02", True, False)]
print("W02 post hoc: clusters", o["clusters"], "later", o.get("later_clusters"), "span h", o["span_h"],
      "first", o["first"], "last", o["last"], "median new cluster h", o.get("median_new_cluster_h_lower"))
o, rs, comps, h = keep[("W11", True, True)]
print("W11 post hoc, indicator only: records", o["records"], "packages", o["packages"], "versions in window", o["versions"],
      "registry-dated", o["registry_dated"], "first", o["first"], "last", o["last"], "span h", o["span_h"],
      "clusters", o["clusters"], "first cluster packages", o["first_cluster_packages"],
      "later clusters", o["later_clusters"], "packages in later clusters", o["packages_in_later_clusters"],
      "no packument", o["no_packument"], "hours to each new cluster", h)
o, rs, comps, h = keep[("W07", True, False)]
print("W07 post hoc: clusters", o["clusters"], "sizes", o["cluster_sizes_in_order"], "hours", h)

# W07: how many distinct hashed maintainers hold the big cluster together, and
# how many distinct hashed publishers do the surviving version documents show?
print("\n== reading clusters as accounts (hashes only; no name is recovered)")
for wid in ("W01", "W02", "W06", "W07", "W08", "W11"):
    key = (wid, True, False)
    if key not in keep:
        continue
    o, rs, comps, h = key and keep[key]
    big = comps[0][1] if comps else []
    msets = [set(npm[p].get("maintainers_h") or []) for p in big]
    allm = set().union(*msets) if msets else set()
    common = set.intersection(*msets) if msets else set()
    m_count = collections.Counter(m for s in msets for m in s)
    top = m_count.most_common(1)[0][1] if m_count else 0
    pubs = collections.Counter()
    docs = 0
    for x in rs:
        d = (npm.get(x["pkg"]) or {}).get("record_version_docs") or {}
        for v, dd in d.items():
            docs += 1
            pubs[dd.get("npmUser_h")] += 1
    # clusters with a single maintainer hash
    singles = sum(1 for c in comps if len(set().union(*[set(npm[p].get("maintainers_h") or []) for p in c[1]])) == 1)
    print(wid, "first cluster: packages", len(big), "distinct maintainer hashes", len(allm),
          "hashes on every package", len(common), "most packages held by one hash", top,
          "| clusters with one maintainer hash", singles, "of", len(comps),
          "| surviving record-version documents", docs, "distinct publishers", len(pubs))

# --- residue share ----------------------------------------------------------
import csv
idx = list(csv.DictReader(gzip.open(os.path.join(D, "osv-mal-index.csv.gz"), "rt")))
n_npm_since = sum(1 for r in idx if r["ecosystem"] == "npm" and r["published"] >= "2025-09-01")
print("\n== residue")
print("MAL records in index:", collections.Counter(r["ecosystem"] for r in idx), "npm published since 2025-09-01:", n_npm_since)
for posthoc in (False, True):
    for x in live:
        x["wave"], x["join"] = assign(x, posthoc)
    tot_r = tot_v = 0
    for wid in WV:
        if (wid, posthoc, False) in keep:
            o = keep[(wid, posthoc, False)][0]
            tot_r += o["records"]; tot_v += o["versions"]
    print("posthoc" if posthoc else "brief", "records assigned", tot_r, "versions", tot_v,
          "share of npm since Sept 2025 (records/163,919-type denominator): %.2f%%" % (100 * tot_r / n_npm_since))
