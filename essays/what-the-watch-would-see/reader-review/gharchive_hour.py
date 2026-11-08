"""Tally one GH Archive hour: event types, and what a PushEvent payload carries.
Reads the gzipped file as data only. python3 -I gharchive_hour.py <file.json.gz>"""
import gzip, json, sys, collections
types = collections.Counter(); push_keys = collections.Counter(); n_push = 0; with_commits = 0
create_ref = collections.Counter()
for line in gzip.open(sys.argv[1], "rt", encoding="utf-8"):
    e = json.loads(line); t = e.get("type"); types[t] += 1
    p = e.get("payload") or {}
    if t == "PushEvent":
        n_push += 1; push_keys.update(p.keys())
        if p.get("commits"): with_commits += 1
    if t == "CreateEvent":
        create_ref[p.get("ref_type")] += 1
print("events:", sum(types.values()))
for t, c in types.most_common(): print(f"  {t}: {c}")
print("PushEvent:", n_push, "with a non-empty commits list:", with_commits)
print("PushEvent payload keys (count of events carrying each):", dict(push_keys))
print("CreateEvent ref_type:", dict(create_ref))
