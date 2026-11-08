"""R-0056: before reading the unread hours, write what the study's panel predicts for each (neighbouring panel files).
Usage: python3 -I studies/LH046/review/scripts/predict.py > studies/LH046/review/out/predictions.txt"""
import csv, datetime as dt, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = {r["label"]: r for r in csv.DictReader(open(os.path.join(HERE, "..", "..", "data", "hours.csv"), newline="")) if r["set"] != "reread"}
plan = [r for r in csv.DictReader(open(os.path.join(HERE, "..", "out", "plan.csv"), newline="")) if r["kind"] == "unread"]
print("Written", dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "before any unread hour was fetched.")
print("Rule: an unread hour h lies between panel hours h-3 and h+3; if both neighbours held no PushEvent, predict 'none';")
print("if both held PushEvents, predict 'pushes'; otherwise 'either'.")
for p in plan:
    d, h = p["label"].rsplit("-", 1); h = int(h); day = dt.date.fromisoformat(d)
    def lab(t):
        q = dt.datetime(day.year, day.month, day.day) + dt.timedelta(hours=t)
        return f"{q.date().isoformat()}-{q.hour}"
    a, b = lab(h - 3), lab(h + 3)
    pa, pb = int(rows[a]["PushEvent"]), int(rows[b]["PushEvent"])
    pred = "none" if pa == 0 and pb == 0 else "pushes" if pa and pb else "either"
    print(f"{p['label']}: {a} push {pa}, {b} push {pb} -> predict {pred}")
