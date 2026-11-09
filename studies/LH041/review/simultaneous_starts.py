"""LH041, resolution of R-0061 (post hoc, written after the counts and after the
reader review pointed at the clusters table). For each wave in the post hoc view,
how many maintainer clusters after the first began publishing in the same second
as, or within 60 seconds of, the cluster that began just before them? Reads only
the retained table; prints counts.
    python3 -I studies/LH041/review/simultaneous_starts.py > studies/LH041/review/simultaneous_starts-output.txt
Scopes: indicator joins for W02 and W11 (the headline counts), indicator+window
for the others. Two thresholds (0 s and 60 s) chosen after the table was seen.
"""
import csv, os
from datetime import datetime
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "..", "data", "2026-11-08T1910Z", "tables", "posthoc", "clusters.csv")
SCOPE = {"W02": "indicator", "W11": "indicator"}
rows = {}
for r in csv.DictReader(open(T)):
    if r["scope"] != SCOPE.get(r["wave"], "indicator+window"):
        continue
    rows.setdefault(r["wave"], []).append(datetime.strptime(r["cluster_first_publish"], "%Y-%m-%dT%H:%M:%SZ"))
print("wave,scope,clusters,after_first,same_second_as_previous,within_60s_of_previous,"
      "within_60s_of_wave_first,starts_more_than_60s_after_previous")
for w in sorted(rows):
    ts = sorted(rows[w])
    gaps = [(b - a).total_seconds() for a, b in zip(ts, ts[1:])]
    same = sum(1 for g in gaps if g == 0)
    w60 = sum(1 for g in gaps if g <= 60)
    first60 = sum(1 for t in ts[1:] if (t - ts[0]).total_seconds() <= 60)
    print(f"{w},{SCOPE.get(w, 'indicator+window')},{len(ts)},{len(ts)-1},{same},{w60},{first60},{len(gaps)-w60}")
