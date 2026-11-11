"""LH041, brief Amendment 2, analysis 3 (post hoc; written 11 November 2026, before
read 2's collection): whether the cluster counts hold under other groupings.

    python3 -I studies/LH041/scripts/groupings.py --read <read label> [--out DIR]

Reads only retained files under data/<read>/ (osv-selected.jsonl.gz,
npm-extract.jsonl.gz, pypi-extract.jsonl.gz) and writes
data/<read>/tables/amendment2/groupings.csv (or DIR/groupings.csv), and prints
the same table. Post hoc: the amendment was conceived after read 1's counts,
clusters and timings were seen; anything quoted from this output is labelled so.

What it does. For both views (the brief's, and the post hoc view of
scripts/tabulate.py --posthoc) and both scopes (indicator joins; indicator and
window joins), for every wave, it recomputes clusters, reach after the seed and
the brief's reading rule under three groupings:
  brief  packages linked when their current npm maintainer lists share a hash
         (the brief's maintainer clusters; this is the baseline and must
         reproduce data/<read>/tables[/posthoc]/waves.csv, which the script
         checks and reports);
  (a)    packages linked when they share a current maintainer hash or an npm
         scope (the part of a name before "/", for names beginning "@");
         unscoped packages link by maintainer only;
  (b)    the brief's maintainer clusters, with any maintainer hash dropped before
         linking if it is on more than 10 per cent of that wave's npm packages
         with known maintainers.
A wave's count "holds" under an alternative if its reading under the brief's
rule (spread across clusters, one further cluster, stayed in one cluster, or
unknown) is the same as under the brief's grouping. Numbers are reported either
way. 2 alternatives x 2 views per wave, each scope shown.

Reuse. Record assignment and the per-wave cluster computation mirror
scripts/tabulate.py line for line (its helpers ts, iso, hours, in_window and UF
are imported from it); only the linking step differs between groupings.

Rules fixed here where the amendment leaves a choice (fixed before read 2 and
not chosen by looking at any alternative's result on read 1):
  R1 Eligibility is the brief's under every grouping: a package enters the
     clusters only if it has a current maintainer list, is not a registry
     placeholder (sole versions ending "-security") and has a registry-dated
     malicious version in the wave. A scoped package with unknown maintainers
     does not enter under (a) by its scope. So the known share, and the
     reading rule's "unknown" below one half, are the same under all three;
     only the links differ.
  R2 (b)'s denominator is the wave's npm packages (in that view and scope) with
     known maintainers: a current maintainer list and not a placeholder,
     whether or not a version has a registry time, as the brief defines
     "maintainers unknown". A hash is dropped if the number of those packages
     listing it is strictly greater than 0.10 x the denominator. The rule
     applies at every wave size as written: in a wave of fewer than ten such
     packages, any hash on two or more of them is on more than 10 per cent and
     is dropped (so is a hash on the only package of a one-package wave,
     which changes nothing).
  R3 Under (b) a package all of whose hashes are dropped stays eligible (its
     maintainers are known) and forms a cluster of its own unless it links
     through a hash that was kept.
  R4 Scopes compare as written in the package name, case-sensitively.
Re-identification: the script uses only salted maintainer hashes, scopes and
package names already kept. It never prints a hash, never resolves one, and
names no maintainer, account or repository; for (b) it prints only how many
hashes were dropped.
"""
import argparse, collections, csv, gzip, json, os, sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import waves  # noqa: E402
from tabulate import ts, iso, hours, in_window, UF  # noqa: E402  (same helpers as the published tables)

W = {w["id"]: w for w in waves.WAVES}
GROUPINGS = ("brief", "a", "b")


def shown(path):
    """Path as printed: relative to the repository, or a placeholder for an --out outside it."""
    root = os.path.realpath(os.path.join(HERE, "..", "..", ".."))
    path = os.path.realpath(path)
    return os.path.relpath(path, root) if path.startswith(root + os.sep) else "<--out directory>/" + os.path.basename(path)


def load(d):
    npm = {}
    for l in gzip.open(os.path.join(d, "npm-extract.jsonl.gz"), "rt"):
        r = json.loads(l)
        npm[r["package"]] = r
    pypi = {}
    for l in gzip.open(os.path.join(d, "pypi-extract.jsonl.gz"), "rt"):
        r = json.loads(l)
        pypi[(r["package"], r["version"])] = r
    return npm, pypi


def assign(d, npm, pypi, posthoc):
    """Mirror of tabulate.py's '# ---- assign records' block (fields used here only)."""
    def reg_time(eco, pkg, v):
        if eco == "npm":
            t = (npm.get(pkg) or {}).get("time") or {}
            return ts(t.get(v)) if t.get(v) else None
        r = pypi.get((pkg, v)) or {}
        up = [u for u in r.get("uploads") or [] if u]
        return ts(min(up)) if up else None

    rows = []
    for l in gzip.open(os.path.join(d, "osv-selected.jsonl.gz"), "rt"):
        r = json.loads(l)
        rec = json.loads(r["raw"])
        if rec.get("withdrawn"):
            continue
        eco = r["ecosystem"]
        aff = rec.get("affected") or [{}]
        pkg = aff[0].get("package", {}).get("name", "")
        vers = sorted({v for x in aff for v in x.get("versions", [])})
        ranges = any(x.get("ranges") for x in aff)
        rt = {v: reg_time(eco, pkg, v) for v in vers}
        known = [t for t in rt.values() if t]
        pub = ts(rec.get("published"))
        date = min(known) if known else pub
        m = r["match"]
        spec = sorted(m["specific"])
        if len(spec) == 1:
            wave, join = spec[0], "indicator"
        elif len(spec) > 1:
            wave, join = "", "ambiguous"
        elif m["shared"] or m["lineage"]:
            cands = sorted(m["shared"]) if m["shared"] else sorted(W)
            if posthoc:
                cands = [w for w in cands if eco in W[w]["eco"]]
            hit = [w for w in cands if date and in_window(w, date)]
            if len(hit) == 1:
                wave, join = hit[0], "window"
            else:
                wave, join = "", "unassigned"
        else:
            wave, join = "", "seed-only"
        rows.append(dict(id=rec["id"], eco=eco, pkg=pkg, vers=vers, ranges=ranges, rt=rt, wave=wave, join=join))
    return rows


def wave_records(rows, wid, scope, posthoc):
    """Mirror of tabulate.py's per-wave selection, including the post hoc version filter."""
    rs = [x for x in rows if x["wave"] == wid and (x["join"] == "indicator" or scope == "indicator+window")]
    if posthoc:
        rs = [dict(x, vers=[v for v in x["vers"] if not x["rt"][v] or in_window(wid, x["rt"][v])]) for x in rs]
        rs = [x for x in rs if x["vers"] or x["ranges"]]
    return rs


def clusters(rs, npm, grouping):
    """tabulate.py's cluster block, with the linking step chosen by `grouping`."""
    pk = sorted({(x["eco"], x["pkg"]) for x in rs})
    npm_pk = [p for e, p in pk if e == "npm"]
    pfirst, pmaint, known_m = {}, {}, []
    for p in npm_pk:
        ts_p = [x["rt"][v] for x in rs if x["pkg"] == p and x["eco"] == "npm" for v in x["vers"] if x["rt"][v]]
        ex = npm.get(p) or {}
        ms = [m for m in ex.get("maintainers_h") or [] if m]
        lst = ex.get("versions_listed") or []
        is_ph = bool(lst) and all(v.endswith("-security") for v in lst)
        if ms and not is_ph:
            known_m.append((p, ms))
        if ms and not is_ph and ts_p:
            pfirst[p] = min(ts_p)
            pmaint[p] = ms
    dropped = set()
    if grouping == "b" and known_m:  # R2
        cnt = collections.Counter(m for _, ms in known_m for m in set(ms))
        dropped = {m for m, c in cnt.items() if c > 0.10 * len(known_m)}
    uf = UF()
    unlinked = 0
    for p, ms in pmaint.items():
        uf.f("p:" + p)
        keep = [m for m in ms if m not in dropped]
        if grouping == "b" and not keep:
            unlinked += 1  # R3
        for mm in keep:
            uf.u("p:" + p, "m:" + mm)
        if grouping == "a" and p.startswith("@") and "/" in p:
            uf.u("p:" + p, "s:" + p.split("/", 1)[0])
    cl = collections.defaultdict(list)
    for p in pfirst:
        cl[uf.f("p:" + p)].append(p)
    cfirst = sorted((min(pfirst[p] for p in ps), len(ps)) for ps in cl.values())
    share = len(pfirst) / len(npm_pk) if npm_pk else 0
    if cfirst:
        seed_t = cfirst[0][0]
        later = [c for c in cfirst[1:] if c[0] > seed_t]
        reach = len(later)
        t_last = hours(seed_t, later[-1][0]) if later else 0
        largest = max(c[1] for c in cfirst)
    else:
        reach, t_last, largest = "", "", ""
    reading = ("unknown" if (not npm_pk or share < 0.5) else
               "spread across clusters" if (reach and reach >= 2) else
               "one further cluster" if reach == 1 else "stayed in one cluster")
    return dict(npm_packages=len(npm_pk), known_maintainers=len(known_m), known_both=len(pfirst),
                known_share=round(share, 3) if npm_pk else "", clusters=len(cfirst), reach=reach,
                hours_to_last_new_cluster=t_last, largest=largest, reading=reading,
                hashes_dropped=len(dropped), packages_all_hashes_dropped=unlinked)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True)
    ap.add_argument("--out", help="output directory (default data/<read>/tables/amendment2)")
    a = ap.parse_args()
    d = os.path.join(HERE, "..", "data", a.read)
    out = a.out or os.path.join(d, "tables", "amendment2")
    os.makedirs(out, exist_ok=True)
    npm, pypi = load(d)

    table, mism, checked = [], [], 0
    for view in ("brief", "posthoc"):
        rows = assign(d, npm, pypi, view == "posthoc")
        pub = {}
        pf = os.path.join(d, "tables", *(["posthoc"] if view == "posthoc" else []), "waves.csv")
        if os.path.exists(pf):
            pub = {(r["wave"], r["scope"]): r for r in csv.DictReader(open(pf))}
        for wid in W:
            for scope in ("indicator", "indicator+window"):
                if scope == "indicator+window" and not any(x["wave"] == wid for x in rows):
                    continue  # tabulate.py writes no indicator+window row for a wave with no record
                rs = wave_records(rows, wid, scope, view == "posthoc")
                g = {k: clusters(rs, npm, k) for k in GROUPINGS}
                b = g["brief"]
                row = dict(view=view, wave=wid, scope=scope, npm_packages=b["npm_packages"],
                           npm_known_maintainers=b["known_maintainers"], npm_known_both=b["known_both"],
                           known_share=b["known_share"])
                for k in GROUPINGS:
                    for f in ("clusters", "reach", "hours_to_last_new_cluster", "largest", "reading"):
                        row[f"{k}_{f}"] = g[k][f]
                row["a_holds"] = int(g["a"]["reading"] == b["reading"])
                row["b_holds"] = int(g["b"]["reading"] == b["reading"])
                row["b_hashes_dropped"] = g["b"]["hashes_dropped"]
                row["b_packages_all_hashes_dropped"] = g["b"]["packages_all_hashes_dropped"]
                table.append(row)
                p = pub.get((wid, scope))
                if p is not None:
                    checked += 1
                    want = (p["npm_packages"], p["npm_known_both"], str(p["clusters"]), str(p["reach_after_seed"]),
                            p["reading"])
                    got = (str(b["npm_packages"]), str(b["known_both"]), str(b["clusters"]), str(b["reach"]),
                           b["reading"])
                    if want != got:
                        mism.append((view, wid, scope, want, got))
                elif pub:
                    mism.append((view, wid, scope, "no published row", "row computed"))

    with open(os.path.join(out, "groupings.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        w.writeheader()
        w.writerows(table)

    print(f"LH041 Amendment 2, analysis 3 (post hoc), read {a.read}; written to {shown(os.path.join(out, 'groupings.csv'))}")
    print("Groupings: brief = shared maintainer hash; a = shared hash or npm scope; "
          "b = shared hash after dropping hashes on >10% of the wave's npm packages with known maintainers.")
    if checked:
        print(f"Baseline check against the published tables: {checked} wave rows compared "
              f"(npm packages, known both, clusters, reach, reading); mismatches: {len(mism)}")
        for m in mism:
            print("  MISMATCH", m)
    else:
        print("Baseline check: no published tables found for this read (run scripts/tabulate.py first).")
    cols = ["view", "wave", "scope", "npm_packages", "known_share",
            "brief_clusters", "brief_reach", "brief_reading",
            "a_clusters", "a_reach", "a_reading", "a_holds",
            "b_clusters", "b_reach", "b_reading", "b_holds", "b_hashes_dropped", "b_packages_all_hashes_dropped"]
    print(",".join(cols))
    for r in table:
        print(",".join(str(r[c]) for c in cols))


if __name__ == "__main__":
    main()
