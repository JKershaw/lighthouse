"""LH041 recheck of the 0.3 resolution of R-0061 (notes/R-0066-lh041-recheck.md).
Independent of review/simultaneous_starts.py: recomputes the clusters-that-began-
together counts in both views, lists the gaps under 60 s with their clock times,
and re-reads the counts the revised opening, Answer, brief amendment 2 and the
two public passages quote. Reads only the retained tables.
    python3 -I studies/LH041/review/recheck/recheck.py > studies/LH041/review/recheck/recheck-output.txt
"""
import csv, json, os
from datetime import datetime
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "2026-11-08T1910Z", "tables")
def load(view, name):
    p = os.path.join(T, *(["posthoc"] if view == "posthoc" else []), name)
    return list(csv.DictReader(open(p)))
ts = lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
for view in ("posthoc", "brief"):
    print(f"== view: {view}")
    cl = load(view, "clusters.csv")
    for wave, scope in (("W02", "indicator"), ("W11", "indicator"), ("W11", "indicator+window"),
                        ("W01", "indicator+window"), ("W06", "indicator+window"),
                        ("W07", "indicator+window"), ("W08", "indicator+window")):
        rows = sorted((ts(r["cluster_first_publish"]), int(r["packages"])) for r in cl
                      if r["wave"] == wave and r["scope"] == scope)
        if not rows:
            print(f"{wave} {scope}: no clusters"); continue
        t = [r[0] for r in rows]
        gaps = [(b - a).total_seconds() for a, b in zip(t, t[1:])]
        close = [(t[i], t[i + 1], g) for i, g in enumerate(gaps) if g <= 60]
        print(f"{wave} {scope}: clusters={len(t)} later={len(t)-1} same_second={sum(g == 0 for g in gaps)} "
              f"within60={len(close)} within60_of_first={sum((x - t[0]).total_seconds() <= 60 for x in t[1:])} "
              f"first={t[0]:%Y-%m-%d %H:%M:%S} last_new={t[-1]:%Y-%m-%d %H:%M:%S} "
              f"hours_to_last_new={(t[-1]-t[0]).total_seconds()/3600:.2f} sizes={[r[1] for r in rows][:5]}...")
        for a, b, g in close:
            print(f"   {a:%H:%M:%S} -> {b:%H:%M:%S}  gap {g:.0f} s")
    w = {(r["wave"], r["scope"]): r for r in load(view, "waves.csv")}
    dated = sorted({k[0] for k, r in w.items() if r["versions_registry_time"] not in ("", "0")})
    print("waves with any registry-dated version:", dated, len(dated))
    for k in (("W02", "indicator"), ("W11", "indicator"), ("W07", "indicator+window")):
        r = w.get(k)
        if r:
            print(k, {f: r[f] for f in ("packages", "npm_packages", "versions", "versions_registry_time",
                  "first_registry", "last_registry", "span_hours", "clusters", "reach_after_seed",
                  "hours_to_last_new_cluster", "largest_cluster_packages", "seed_cluster_packages", "npm_known_both")})
