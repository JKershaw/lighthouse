#!/usr/bin/env python3
"""R-0036: what changed between the last read without the PHP entries and the
first read with them, what the feed says about the basis for any entry, and
the weekday of 21 October 2026 (the short form's "Wednesday").
Usage: python3 -I studies/LH031/review/r0036_check.py"""
import json, pathlib, re, datetime
ROOT = pathlib.Path(__file__).resolve().parents[3]
D = ROOT / "studies/LH031/data"
before = json.loads((D / "read-2026-10-26T1830Z/feed.raw").read_bytes())
after = json.loads((D / "read-2026-10-27T0633Z/feed.raw").read_bytes())
ib = {v["cveID"]: v for v in before["vulnerabilities"]}
ia = {v["cveID"]: v for v in after["vulnerabilities"]}
print("before", before["catalogVersion"], before["count"], len(ib))
print("after ", after["catalogVersion"], after["count"], len(ia))
print("added:", sorted(set(ia) - set(ib)))
print("removed:", sorted(set(ib) - set(ia)))
changed = [k for k in set(ia) & set(ib) if ia[k] != ib[k]]
print("entries present in both but changed:", sorted(changed))
text = (D / "read-2026-10-27T0633Z/feed.raw").read_text("utf-8")
for w in ("honeypot", "attempt", "in the wild", "observed", "evidence", "criteria", "successful"):
    print(f"occurrences of {w!r} anywhere in the feed:", len(re.findall(re.escape(w), text, re.I)))
php = [ia[k] for k in ("CVE-2026-109618", "CVE-2026-109619")]
for v in php:
    urls = re.findall(r"https?://\S+", v["notes"])
    print(v["cveID"], "notes URLs:", [u.rstrip(" ;") for u in urls])
oct26 = [v for v in after["vulnerabilities"] if v["dateAdded"].startswith("2026-10")]
print("entries dated October 2026:", len(oct26),
      "with forensicTriage Yes:", sum(v.get("forensicTriage") == "Yes" for v in oct26))
ft = sum(v.get("forensicTriage") == "Yes" for v in after["vulnerabilities"])
print("all entries with forensicTriage Yes:", ft, "of", len(ia))
print("21 October 2026 is a", datetime.date(2026, 10, 21).strftime("%A"))
