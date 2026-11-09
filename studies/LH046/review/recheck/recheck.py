# Recheck (R-0064) of the figures in LH046's "Later evidence" notices,
# investigation-page lines and record 0.3 opening and Answer, from data/hours.csv.
import csv, collections, pathlib
d = pathlib.Path(__file__).resolve().parents[2] / "data"
rows = list(csv.DictReader(open(d / "hours.csv")))
print("rows", len(rows), "sets", collections.Counter(r["set"] for r in rows))
by = {}
for r in rows: by.setdefault(r["label"], r)
print("distinct files", len(by))
print("all 200:", all(r["http_status"] == "200" for r in by.values()),
      "all non-empty (events>0):", all(int(r["events"]) > 0 for r in by.values()))
dates = sorted(l.rsplit("-", 1)[0] for l in by)
print("date range", dates[0], dates[-1])
panel = [r for r in rows if r["set"] == "panel"]
hrs = collections.Counter(int(r["label"].rsplit("-", 1)[1]) for r in panel)
print("panel files", len(panel), "hours", dict(hrs), "range", min(r["label"] for r in panel), max(r["label"][:10] for r in panel))
def nopush(r): return int(r["PushEvent"]) == 0
early = [r for r in panel if r["label"][:10] <= "2026-10-14"]
late = [r for r in panel if r["label"][:10] >= "2026-10-15"]
for name, s in (("1 Sep-14 Oct", early), ("15 Oct-7 Nov", late), ("all", panel)):
    n = sum(nopush(r) for r in s)
    print(name, n, "of", len(s), f"{n/len(s):.3f}")
same = all((int(r["PushEvent"]) == 0) == (int(r["CreateEvent"]) == 0) == (int(r["DeleteEvent"]) == 0) for r in panel)
print("Push/Create/Delete zero together in panel:", same)
# runs over the panel in time order
seq = sorted(panel, key=lambda r: (r["label"][:10], int(r["label"].rsplit("-", 1)[1])))
runs, cur = [], []
for r in seq:
    if nopush(r): cur.append(r["label"])
    elif cur: runs.append(cur); cur = []
if cur: runs.append(cur)
print("runs", len(runs))
for x in runs: print("  ", x[0], "->", x[-1], len(x))
# other types in no-push files
np_ = [r for r in panel if nopush(r)]
oth = sorted(int(r["events"]) for r in np_)
print("events in no-push panel files: min", oth[0], "median", oth[len(oth)//2], "max", oth[-1])
ctl = ["PullRequestEvent", "IssuesEvent", "IssueCommentEvent", "WatchEvent"]
ref = sorted([r for r in rows if r["set"] == "reference"], key=lambda r: r["label"])
print("reference files", len(ref))
for r in ref:
    e = int(r["events"]); p = int(r["PushEvent"])
    print("  ", r["label"], "events", e, "push", p, f"push share {100*p/e:.1f}%", "control4", sum(int(r[c]) for c in ctl))
