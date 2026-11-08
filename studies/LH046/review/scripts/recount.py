"""R-0056: recompute LH046's headline figures from data/hours.csv with the reviewer's own code (no import of analyse.py).
Usage (from the repository root): python3 -I studies/LH046/review/scripts/recount.py > studies/LH046/review/out/recount.txt"""
import csv, json, os, statistics as st, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "..", "data", "hours.csv"), newline="")))
first = {}
for r in rows:
    if r["set"] != "reread":
        first.setdefault(r["label"], r)
I = lambda r, k: int(r[k] or 0)
def when(l):
    d, h = l.rsplit("-", 1); return dt.datetime.fromisoformat(d) + dt.timedelta(hours=int(h))
CUT = dt.datetime(2026, 10, 15)
panel = [r for r in first.values() if r["set"] == "panel"]
print("distinct files:", len(first), "; rows incl. re-reads:", len(rows), "; panel:", len(panel))
print("HTTP statuses (first reads):", sorted({r["http_status"] for r in first.values()}))
pre = [r for r in panel if when(r["label"]) < CUT]; post = [r for r in panel if when(r["label"]) >= CUT]
for name, g in (("1 Sep-14 Oct", pre), ("15 Oct-7 Nov", post)):
    z = [r for r in g if I(r, "PushEvent") == 0]
    print(f"panel {name}: no PushEvent {len(z)}/{len(g)} = {100*len(z)/len(g):.1f}%")
    for h in (0, 6, 12, 18):
        gh = [r for r in g if r["label"].endswith(f"-{h}")]
        print(f"   hour {h:2d}: {sum(I(r,'PushEvent')==0 for r in gh)}/{len(gh)}")
print("panel overall no push:", sum(I(r, "PushEvent") == 0 for r in panel), "/", len(panel))
for m in ("2026-09", "2026-10", "2026-11"):
    g = [r for r in panel if r["label"].startswith(m)]
    print("  month", m, sum(I(r, "PushEvent") == 0 for r in g), "/", len(g))
# together
mixed = [r["label"] for r in first.values() if len({I(r, k) == 0 for k in ("PushEvent", "CreateEvent", "DeleteEvent")}) > 1]
print("files where Push/Create/Delete are not all present or all absent:", mixed)
# CreateEvent ref types
tot, tot_all, other = 0, 0, {}
for r in first.values():
    cr = json.loads(r["create_ref_types"] or "{}")
    for k, v in cr.items():
        tot_all += v
        if k == "branch": tot += v
        else: other[k] = other.get(k, 0) + v
print("CreateEvents in first reads:", sum(I(r, "CreateEvent") for r in first.values()), "; by ref_type branch:", tot, "other:", other)
print("CreateEvents incl. re-reads:", sum(I(r, "CreateEvent") for r in rows))
pk = {}
for r in first.values():
    if I(r, "PushEvent"):
        k = tuple(sorted(json.loads(r["push_payload_keys"]).items()))
        keys = tuple(sorted(json.loads(r["push_payload_keys"]).keys()))
        allsame = len(set(json.loads(r["push_payload_keys"]).values())) == 1 and list(json.loads(r["push_payload_keys"]).values())[0] == I(r, "PushEvent")
        pk.setdefault((keys, allsame), 0); pk[(keys, allsame)] += 1
print("push payload key sets (keys, every push carries each):", pk, "; push_with_commits total:", sum(I(r, "push_with_commits") for r in first.values()))
print("min minutes_with_events over first reads:", min(I(r, "minutes_with_events") for r in first.values()))
print("events outside hour:", sum(I(r, "outside_hour") for r in first.values()), "; json errors:", sum(I(r, "json_errors") for r in first.values()), "; empty:", [r["label"] for r in first.values() if I(r, "events") == 0])
# references
print("\nReference hours (12:00 on 1st and 15th, Jan-Aug) and LH002's hour:")
CTRL = ["PullRequestEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent"]
for r in sorted((r for r in first.values() if r["set"] == "reference"), key=lambda r: when(r["label"])):
    print(f"  {r['label']:>14}: events {I(r,'events'):>7} push {I(r,'PushEvent'):>7} create {I(r,'CreateEvent'):>6} delete {I(r,'DeleteEvent'):>5} PR {I(r,'PullRequestEvent'):>6} issues {I(r,'IssuesEvent'):>5} comments {I(r,'IssueCommentEvent'):>5} stars {I(r,'WatchEvent'):>5} control {sum(I(r,k) for k in CTRL):>6} push share {I(r,'PushEvent')/I(r,'events'):.3f}")
refs16 = [r for r in first.values() if r["set"] == "reference" and r["label"] != "2026-04-02-14"]
print("reference median control:", st.median(sum(I(r, k) for k in CTRL) for r in refs16), "; median push:", st.median(I(r, "PushEvent") for r in refs16), "; median events:", st.median(I(r, "events") for r in refs16))
# finding 6/7
def summ(g, k):
    v = [I(r, k) if k != "control" else sum(I(r, c) for c in CTRL) for r in g]
    return f"n={len(v)} median {st.median(v):,.0f} range {min(v):,}-{max(v):,}" if v else "n=0"
for name, g in (("1 Sep-14 Oct", pre), ("15 Oct-7 Nov", post)):
    z = [r for r in g if I(r, "PushEvent") == 0]; p = [r for r in g if I(r, "PushEvent")]
    print(f"\n{name}: no-push files events {summ(z,'events')}; control {summ(z,'control')}")
    print(f"{name}: push files PushEvent {summ(p,'PushEvent')}; events {summ(p,'events')}; control {summ(p,'control')}")
    refc = st.median(sum(I(r, k) for k in CTRL) for r in refs16)
    print(f"{name}: control/ref-median ratio, no-push median {st.median(sum(I(r,k) for k in CTRL)/refc for r in z):.2f}, push median {st.median(sum(I(r,k) for k in CTRL)/refc for r in p):.2f}")
need = ["PullRequestEvent", "PullRequestReviewEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent", "ForkEvent", "ReleaseEvent", "MemberEvent", "GollumEvent"]
zp = [r for r in panel if I(r, "PushEvent") == 0]
lack = {k: [r["label"] for r in zp if I(r, k) == 0] for k in need}
print("\npanel no-push files lacking a type:", {k: v for k, v in lack.items() if v} or "none")
big = sorted(zp, key=lambda r: -I(r, "events"))[:5]
print("largest no-push panel files:", [(r["label"], I(r, "events"), sum(I(r, k) for k in CTRL)) for r in big])
# runs over panel + latest
seq = sorted((r for r in first.values() if r["set"] in ("panel", "latest") or (r["label"].rsplit("-",1)[1] in ("0","6","12","18") and when(r["label"]) >= dt.datetime(2026,9,1))), key=lambda r: when(r["label"]))
runs, cur = [], []
for r in seq:
    if I(r, "PushEvent") == 0: cur.append(r["label"])
    elif cur: runs.append(cur); cur = []
if cur: runs.append(cur)
print("\nruns of panel/latest files without pushes:", [(c[0], c[-1], len(c)) for c in runs])
# Last-Modified
offs = []
for r in first.values():
    lm = dt.datetime.strptime(r["last_modified"], "%a, %d %b %Y %H:%M:%S GMT")
    offs.append(((lm - when(r["label"]) - dt.timedelta(hours=1)).total_seconds() / 60, r["label"]))
print("Last-Modified minus end of hour, minutes: min", min(offs), "max", max(offs))
# partial push hours
pph = [r for r in first.values() if I(r, "PushEvent") and I(r, "longest_zero_push_run_min") >= 5]
print("files with pushes and a >=5 minute run without:", len(pph))
