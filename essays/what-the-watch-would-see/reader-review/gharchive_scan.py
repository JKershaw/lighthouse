"""Count events and PushEvents in GH Archive hourly files read from stdin, one hour per call.
Usage: curl -s https://data.gharchive.org/<YYYY-MM-DD-H>.json.gz | python3 -I gharchive_scan.py <label>
Prints: label,events,push_events,create_events (read as data only; nothing is kept)."""
import gzip, json, sys
ev = push = create = 0
with gzip.open(sys.stdin.buffer, "rt", encoding="utf-8") as f:
    for line in f:
        t = json.loads(line).get("type"); ev += 1
        push += t == "PushEvent"; create += t == "CreateEvent"
print(f"{sys.argv[1]},{ev},{push},{create}")
