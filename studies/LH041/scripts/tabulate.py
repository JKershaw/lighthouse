"""LH041 tabulator, written after read 1 to implement the brief's measures as written.

    python3 -I studies/LH041/scripts/tabulate.py --read 2026-11-08T1910Z

Reads only retained files under data/<read>/ and writes data/<read>/tables/.
Nothing here changes the brief's waves, indicators, windows or rules; where the
brief left a detail open, the choice is commented and listed in the record's
Method section.
"""
import argparse, collections, csv, gzip, json, os, re, statistics, sys
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import waves  # noqa: E402

W = {w["id"]: w for w in waves.WAVES}


def ts(s):
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    if "." in s:  # trim nanoseconds
        a, b = s.split(".", 1)
        frac = re.match(r"\d+", b).group(0)[:6]
        s = a + "." + frac + b[len(re.match(r"\d+", b).group(0)):]
    return datetime.fromisoformat(s).astimezone(timezone.utc)


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ") if d else ""


def hours(a, b):
    return round((b - a).total_seconds() / 3600, 2) if a and b else ""


def in_window(wid, d):
    lo, hi = W[wid]["window"]
    lo = datetime.fromisoformat(lo).replace(tzinfo=timezone.utc)
    hi = datetime.fromisoformat(hi).replace(tzinfo=timezone.utc) + timedelta(days=1)  # inclusive end day
    return lo <= d < hi


class UF:
    def __init__(self):
        self.p = {}

    def f(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def u(self, a, b):
        self.p[self.f(a)] = self.f(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True)
    ap.add_argument("--posthoc", action="store_true",
                    help="post hoc view (decided after read 1's counts were seen): window joins only among waves "
                         "whose ecosystems include the record's, and a wave's versions limited to those whose "
                         "registry time falls in its window (versions with no registry time kept in counts only)")
    a = ap.parse_args()
    d = os.path.join(HERE, "..", "data", a.read)
    out = os.path.join(d, "tables", "posthoc") if a.posthoc else os.path.join(d, "tables")
    os.makedirs(out, exist_ok=True)

    npm = {}
    for l in gzip.open(os.path.join(d, "npm-extract.jsonl.gz"), "rt"):
        r = json.loads(l)
        npm[r["package"]] = r
    pypi = {}
    for l in gzip.open(os.path.join(d, "pypi-extract.jsonl.gz"), "rt"):
        r = json.loads(l)
        pypi[(r["package"], r["version"])] = r

    def reg_time(eco, pkg, v):
        if eco == "npm":
            t = (npm.get(pkg) or {}).get("time") or {}
            return ts(t.get(v)) if t.get(v) else None
        r = pypi.get((pkg, v)) or {}
        up = [u for u in r.get("uploads") or [] if u]
        return ts(min(up)) if up else None

    # ---- assign records
    rows = []
    withdrawn = 0
    for l in gzip.open(os.path.join(d, "osv-selected.jsonl.gz"), "rt"):
        r = json.loads(l)
        rec = json.loads(r["raw"])
        if rec.get("withdrawn"):
            withdrawn += 1
            continue
        eco = r["ecosystem"]
        aff = rec.get("affected") or [{}]
        pkg = aff[0].get("package", {}).get("name", "")
        vers = sorted({v for x in aff for v in x.get("versions", [])})
        ranges = any(x.get("ranges") for x in aff)
        origins = (rec.get("database_specific") or {}).get("malicious-packages-origins") or []
        imps = sorted(ts(o["import_time"]) for o in origins if o.get("import_time"))
        rt = {v: reg_time(eco, pkg, v) for v in vers}
        known = [t for t in rt.values() if t]
        pub = ts(rec.get("published"))
        date = min(known) if known else pub
        m = r["match"]
        spec = sorted(m["specific"])
        if len(spec) == 1:
            wave, join = spec[0], "indicator"
        elif len(spec) > 1:
            wave, join = "", "ambiguous:" + "+".join(spec)
        elif m["shared"] or m["lineage"]:
            cands = sorted(m["shared"]) if m["shared"] else sorted(W)
            if a.posthoc:
                cands = [w for w in cands if eco in W[w]["eco"]]
            hit = [w for w in cands if date and in_window(w, date)]
            if len(hit) == 1:
                wave, join = hit[0], "window"
            elif len(hit) > 1:
                wave, join = "", "window-ambiguous:" + "+".join(hit)
            else:
                wave, join = "", "lineage-unassigned"
        else:
            wave, join = "", "seed-only"
        text = rec.get("details", "") or ""
        rows.append(dict(id=rec["id"], eco=eco, pkg=pkg, vers=vers, ranges=ranges, rt=rt, pub=pub,
                         imp=imps[0] if imps else None, date=date, wave=wave, join=join, seed=r["seed"],
                         sources=sorted({o.get("source", "") for o in origins}),
                         math_init=bool(re.search(r"math_init\.js", r["raw"], re.I)),
                         math_symbol=bool(re.search(r"math_symbol\.js", r["raw"], re.I)),
                         details_len=len(text)))

    with open(os.path.join(out, "records.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "ecosystem", "package", "n_versions", "ranges", "versions_with_registry_time",
                    "earliest_registry_time", "osv_published", "first_import", "wave", "join", "seed_wave",
                    "origin_sources"])
        for x in sorted(rows, key=lambda x: (x["wave"], x["join"], x["date"] or datetime.max.replace(tzinfo=timezone.utc))):
            k = [t for t in x["rt"].values() if t]
            w.writerow([x["id"], x["eco"], x["pkg"], len(x["vers"]), int(x["ranges"]), len(k),
                        iso(min(k)) if k else "", iso(x["pub"]), iso(x["imp"]), x["wave"], x["join"],
                        x["seed"] or "", ";".join(x["sources"])])

    joins = collections.Counter(x["join"] if not x["wave"] else x["join"] for x in rows)

    # ---- per wave
    summ = []
    clusters_out = []
    timeline = []
    for wid in W:
        for scope in ("indicator", "indicator+window"):
            rs = [x for x in rows if x["wave"] == wid and (x["join"] == "indicator" or scope == "indicator+window")]
            if not rs and scope == "indicator+window":
                continue
            pk = sorted({(x["eco"], x["pkg"]) for x in rs})
            versions = [(x["eco"], x["pkg"], v, x["rt"][v], x["pub"], x["imp"]) for x in rs for v in x["vers"]]
            outside = sum(1 for *_, t, p, i in versions if t and not in_window(wid, t))
            if a.posthoc:
                versions = [vv for vv in versions if not vv[3] or in_window(wid, vv[3])]
                ok = {(vv[0], vv[1], vv[2]) for vv in versions}
                rs = [dict(x, vers=[v for v in x["vers"] if (x["eco"], x["pkg"], v) in ok]) for x in rs]
                rs = [x for x in rs if x["vers"] or x["ranges"]]
            known = [t for *_, t, p, i in versions if t]
            first = min(known) if known else None
            last = max(known) if known else None
            osv_first = min((x["pub"] for x in rs if x["pub"]), default=None)
            imp_first = min((x["imp"] for x in rs if x["imp"]), default=None)
            lags = [(p - t).total_seconds() / 3600 for *_, t, p, i in versions if t and p]
            # clusters among npm packages
            uf = UF()
            pfirst, pmaint, unknown_m, unknown_t, placeholder, n404 = {}, {}, 0, 0, 0, 0
            npm_pk = [p for e, p in pk if e == "npm"]
            for p in npm_pk:
                ts_p = [x["rt"][v] for x in rs if x["pkg"] == p and x["eco"] == "npm" for v in x["vers"] if x["rt"][v]]
                ex = npm.get(p) or {}
                ms = [m for m in ex.get("maintainers_h") or [] if m]
                lst = ex.get("versions_listed") or []
                if ex.get("status") == 404:
                    n404 += 1
                is_ph = bool(lst) and all(v.endswith("-security") for v in lst)
                if is_ph:
                    placeholder += 1
                if not ms or is_ph:
                    unknown_m += 1
                if not ts_p:
                    unknown_t += 1
                if ms and not is_ph and ts_p:
                    pfirst[p] = min(ts_p)
                    pmaint[p] = ms
                    for mm in ms:
                        uf.u("p:" + p, "m:" + mm)
            cl = collections.defaultdict(list)
            for p in pfirst:
                cl[uf.f("p:" + p)].append(p)
            cfirst = sorted((min(pfirst[p] for p in ps), len(ps), sum(1 for x in rs if x["pkg"] in ps for v in x["vers"]))
                            for ps in cl.values())
            n_known = len(pfirst)
            share = n_known / len(npm_pk) if npm_pk else 0
            if cfirst:
                seed_t = cfirst[0][0]
                later = [c for c in cfirst[1:] if c[0] > seed_t]
                reach = len(later)
                t_last_new = hours(seed_t, later[-1][0]) if later else 0
                t_half = hours(seed_t, later[(len(later) - 1) // 2][0]) if later else ""
                largest = max(c[1] for c in cfirst)
            else:
                reach, t_last_new, t_half, largest = "", "", "", ""
            reading = ("unknown" if (not npm_pk or share < 0.5) else
                       "spread across clusters" if (reach and reach >= 2) else
                       "one further cluster" if reach == 1 else "stayed in one cluster")
            for c in cfirst:
                clusters_out.append([wid, scope, iso(c[0]), hours(cfirst[0][0], c[0]), c[1], c[2]])
            for *_, t, p, i in versions:
                if t:
                    timeline.append([wid, scope, iso(t)])
            summ.append(dict(
                wave=wid, name=W[wid]["name"], scope=scope, records=len(rs),
                packages=len(pk), npm_packages=len(npm_pk), pypi_packages=len(pk) - len(npm_pk),
                versions=len(versions), versions_registry_time_outside_window=outside, ranges_only=sum(1 for x in rs if x["ranges"] and not x["vers"]),
                versions_registry_time=len(known),
                first_registry=iso(first), last_registry=iso(last), span_hours=hours(first, last),
                osv_first_published=iso(osv_first), lag_first_osv_hours=hours(first, osv_first),
                first_import=iso(imp_first),
                median_version_lag_hours=round(statistics.median(lags), 2) if lags else "",
                vendor_clock=W[wid]["vendor_clock"],
                npm_404=n404, npm_placeholder=placeholder, npm_maint_unknown=unknown_m, npm_time_unknown=unknown_t,
                npm_known_both=n_known, known_share=round(share, 3) if npm_pk else "",
                clusters=len(cfirst), reach_after_seed=reach, hours_to_median_new_cluster=t_half,
                hours_to_last_new_cluster=t_last_new, largest_cluster_packages=largest,
                seed_cluster_packages=cfirst[0][1] if cfirst else "",
                reading=reading,
                math_init_records=sum(1 for x in rs if x["math_init"]),
                math_symbol_only_records=sum(1 for x in rs if x["math_symbol"] and not x["math_init"]),
            ))

    with open(os.path.join(out, "waves.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summ[0].keys()))
        w.writeheader()
        w.writerows(summ)
    with open(os.path.join(out, "clusters.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wave", "scope", "cluster_first_publish", "hours_after_wave_first", "packages", "versions"])
        w.writerows(clusters_out)
    with open(os.path.join(out, "timeline.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wave", "scope", "registry_publish"])
        w.writerows(sorted(timeline))

    # ---- seeds: does OSV hold a MAL record for each named seed, and did it join the wave?
    idx = list(csv.DictReader(gzip.open(os.path.join(d, "osv-mal-index.csv.gz"), "rt")))
    seeds = []
    for wid, wv in W.items():
        for s in wv["seeds"]:
            sl = s.lower()
            hit = [r for r in idx if (r["package"].lower().startswith(sl) if sl.endswith("/") else r["package"].lower() == sl)]
            ids = {r["id"] for r in hit}
            joined = [x for x in rows if x["id"] in ids and x["wave"] == wid]
            other = sorted({x["wave"] or x["join"] for x in rows if x["id"] in ids and x["wave"] != wid})
            seeds.append([wid, s, len(hit), len(joined), ";".join(other)])
    with open(os.path.join(out, "seeds.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wave", "seed", "mal_records_for_seed", "joined_this_wave", "other_classes"])
        w.writerows(seeds)

    # ---- cross-wave packages
    by_pkg = collections.defaultdict(set)
    for x in rows:
        if x["wave"]:
            by_pkg[(x["eco"], x["pkg"])].add(x["wave"])
    multi = collections.Counter("+".join(sorted(v)) for v in by_pkg.values() if len(v) > 1)

    # ---- OpenSSF spot check
    spot = []
    selraw = {json.loads(json.loads(l)["raw"])["id"]: json.loads(json.loads(l)["raw"])
              for l in gzip.open(os.path.join(d, "osv-selected.jsonl.gz"), "rt")}
    for l in gzip.open(os.path.join(d, "openssf-spotcheck.jsonl.gz"), "rt"):
        r = json.loads(l)
        o = selraw.get(r["id"]) or {}
        if r.get("status") != 200:
            spot.append([r["id"], r.get("status"), "", ""])
            continue
        try:
            g = json.loads(r["raw"])
        except Exception:
            spot.append([r["id"], 200, "unparsed", ""])
            continue
        vo = sorted({v for x in o.get("affected") or [] for v in x.get("versions", [])})
        vg = sorted({v for x in g.get("affected") or [] for v in x.get("versions", [])})
        to, tg = (o.get("details") or "").strip(), (g.get("details") or "").strip()
        spot.append([r["id"], 200, int(vo == vg), int(to == tg)])
    with open(os.path.join(out, "spotcheck.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "status", "versions_equal", "details_equal"])
        w.writerows(spot)

    # ---- index context
    eco_n = collections.Counter(r["ecosystem"] for r in idx)
    since = collections.Counter(r["ecosystem"] for r in idx if r["published"] >= "2025-09-01")
    report = dict(read=a.read, selected=len(rows) + withdrawn, withdrawn=withdrawn, joins=dict(joins),
                  mal_records_by_ecosystem=dict(eco_n), mal_records_published_since_2025_09_01=dict(since),
                  packages_in_more_than_one_wave=dict(multi),
                  spotcheck=dict(n=len(spot), versions_equal=sum(1 for s in spot if s[2] == 1),
                                 details_equal=sum(1 for s in spot if s[3] == 1)))
    json.dump(report, open(os.path.join(out, "summary.json"), "w"), indent=1, default=str)
    print(json.dumps(report, indent=1, default=str))
    for s in summ:
        print({k: s[k] for k in ("wave", "scope", "records", "packages", "versions", "first_registry", "last_registry",
                                  "span_hours", "lag_first_osv_hours", "clusters", "reach_after_seed", "known_share", "reading")})


if __name__ == "__main__":
    main()
