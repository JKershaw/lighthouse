#!/usr/bin/env python3
"""R-0035: print every context in the retained 27 October feed body where the
feed itself speaks of agencies, binding or who a directive applies to.
Usage: python3 -I studies/LH031/review/feed_context.py"""
import json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[3]
raw = (ROOT / "studies/LH031/data/read-2026-10-27T0633Z/feed.raw").read_bytes()
text = raw.decode("utf-8")
feed = json.loads(raw)
for word in ("binding", "agencies", "agency", "Directive", "federal", "civilian", "must", "required to"):
    for m in re.finditer(re.escape(word), text):
        s, e = max(0, m.start() - 160), min(len(text), m.end() + 160)
        print(f"[{word}] ...{text[s:e]}...")
        print()
# Does any entry define what dueDate means?
hits = [v["cveID"] for v in feed["vulnerabilities"] if "due" in (v.get("requiredAction","")+v.get("notes","")).lower()]
print("entries whose requiredAction or notes contain 'due':", hits[:20], "count", len(hits))
print("distinct requiredAction texts among entries dated 2026-10:", len({v["requiredAction"] for v in feed["vulnerabilities"] if v["dateAdded"].startswith("2026-10")}))
