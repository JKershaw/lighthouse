"""R-0056: compare the reviewer's re-read counts (review/out/counts.csv) with LH046's data/hours.csv and minutes.csv,
and score the unread hours against the predictions written before they were fetched.
Usage (from the repository root): python3 -I studies/LH046/review/scripts/compare.py > studies/LH046/review/out/compare.txt"""
import csv, json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "..", "..", "data"); O = os.path.join(HERE, "..", "out")
TYPES = ["PushEvent", "CreateEvent", "DeleteEvent", "PullRequestEvent", "PullRequestReviewEvent",
         "PullRequestReviewCommentEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent", "ForkEvent",
         "ReleaseEvent", "MemberEvent", "PublicEvent", "GollumEvent", "CommitCommentEvent", "DiscussionEvent"]
study = {}
for r in csv.DictReader(open(os.path.join(D, "hours.csv"), newline="")):
    if r["set"] != "reread":
        study.setdefault(r["label"], r)
smin = collections.defaultdict(lambda: [0] * 60)
for r in csv.DictReader(open(os.path.join(D, "minutes.csv"), newline="")):
    if r["set"] != "reread":
        smin[r["label"]][int(r["minute"])] = int(r["push_events"])
mine = list(csv.DictReader(open(os.path.join(O, "counts.csv"), newline="")))
same = diff = 0
print("== Re-read files against data/hours.csv (sha256, bytes, events, all 16 types, other types, push keys, ref types, minute profile)")
for r in mine:
    if r["kind"] == "unread":
        continue
    s = study[r["label"]]
    checks = {"sha256": r["sha256"] == s["sha256"], "bytes": r["bytes"] == s["bytes"], "events": r["events"] == s["events"],
              "types": all(r[t] == s[t] for t in TYPES),
              "other": json.loads(r["other_types"]) == json.loads(s["other_types"]),
              "create_ref": json.loads(r["create_ref_types"]) == json.loads(s["create_ref_types"]),
              "push_minutes": [int(x) for x in r["push_by_minute"].split()] == smin[r["label"]],
              "minutes_with_events": r["minutes_with_events"] == s["minutes_with_events"]}
    ok = all(checks.values()); same += ok; diff += not ok
    bad = [k for k, v in checks.items() if not v]
    print(f"  {r['label']:>14} ({r['kind']}): {'all match' if ok else 'DIFFER: ' + ', '.join(bad)}; sha256 {r['sha256'][:16]}; events {r['events']}; PushEvent {r['PushEvent']}; read {r['utc_read']}")
print(f"  {same} match on every field, {diff} differ")
print("\n== Unread hours (not in LH046's sample), against predictions written before fetching")
pred = {}
for line in open(os.path.join(O, "predictions.txt")):
    if "-> predict" in line:
        pred[line.split(":")[0]] = line.rsplit(" ", 1)[1].strip()
tally = collections.Counter()
for r in mine:
    if r["kind"] != "unread":
        continue
    p = int(r["PushEvent"]); c = int(r["CreateEvent"]); d = int(r["DeleteEvent"])
    got = "none" if p == 0 else "pushes"
    hit = pred[r["label"]] == "either" or pred[r["label"]] == got
    tally[(pred[r["label"]], got)] += 1
    together = (p == 0) == (c == 0) == (d == 0)
    ctrl = sum(int(r[k]) for k in ("PullRequestEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent"))
    part = ""
    if p:
        pm = [int(x) for x in r["push_by_minute"].split()]
        run = best = 0
        for x in pm:
            run = run + 1 if x == 0 else 0; best = max(best, run)
        part = f"; push minutes {r['minutes_with_push']}, first {r['first_push_minute']}, last {r['last_push_minute']}, longest run without {best}"
    print(f"  {r['label']:>14}: predicted {pred[r['label']]:6} got {got:6} {'ok' if hit else 'MISS'}; events {r['events']}, push {p}, create {c}, delete {d}, control {ctrl}; three together: {together}; minutes with events {r['minutes_with_events']}; empty {r['events']=='0'}{part}")
print("  tally (predicted, got):", dict(tally))
print("\n== Payload shape in every re-read file")
keys = collections.Counter(); refs = collections.Counter(); commits = 0
for r in mine:
    for k, v in json.loads(r["push_payload_keys"]).items(): keys[k] += v
    for k, v in json.loads(r["create_ref_types"]).items(): refs[k] += v
    commits += int(r["push_with_commits"])
print("  PushEvent key sets:", dict(keys), "; with commits:", commits, "; CreateEvent ref_type:", dict(refs))
print("  outside-hour events:", sum(int(r["outside_hour"]) for r in mine), "; JSON errors:", sum(int(r["json_errors"]) for r in mine),
      "; HTTP statuses:", dict(collections.Counter(r["http_status"] for r in mine)), "; bytes received:", sum(int(r["bytes"]) for r in mine))
