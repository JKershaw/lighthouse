#!/usr/bin/env python3
"""R-0035: the one live read this review was allowed, of CISA's KEV feed.
Records time, status, size and SHA-256, extracts the three CVEs' entries and the
catalogue header, and compares them with LH031's retained 27 October 06:34 UTC
read. The body is written only to the scratchpad directory given as argv[1];
nothing is saved into the repository unless the relevant entries changed.
Usage: python3 -I studies/LH031/review/live_read.py <scratchpad dir>"""
import datetime as dt, hashlib, json, pathlib, ssl, sys, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[3]
URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
CVES = ["CVE-2026-109618", "CVE-2026-109619", "CVE-2026-115560"]
out_dir = pathlib.Path(sys.argv[1])
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
req = urllib.request.Request(URL, headers={"User-Agent": "Lighthouse R-0035 review read (one request)"})
start = dt.datetime.now(dt.timezone.utc)
try:
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        status = r.status; body = r.read(); ctype = r.headers.get("Content-Type")
except urllib.error.HTTPError as e:
    status = e.code; body = e.read(); ctype = e.headers.get("Content-Type")
finish = dt.datetime.now(dt.timezone.utc)
sha = hashlib.sha256(body).hexdigest()
log = {"url": URL, "start_utc": start.isoformat(), "finish_utc": finish.isoformat(), "status": status,
       "bytes": len(body), "sha256": sha, "content_type": ctype}
(out_dir / "live-feed.raw").write_bytes(body)
retained = json.loads((ROOT / "studies/LH031/data/read-2026-10-27T0633Z/feed.raw").read_bytes())
ret_by = {v["cveID"]: v for v in retained["vulnerabilities"]}
extract = {"catalogVersion": None, "dateReleased": None, "count": None, "entries": {}, "same_as_retained": {}}
try:
    feed = json.loads(body)
    by = {v["cveID"]: v for v in feed["vulnerabilities"]}
    extract.update(catalogVersion=feed.get("catalogVersion"), dateReleased=feed.get("dateReleased"), count=feed.get("count"))
    for c in CVES:
        extract["entries"][c] = by.get(c)
        extract["same_as_retained"][c] = by.get(c) == ret_by.get(c)
    extract["retained_catalogVersion"] = retained["catalogVersion"]
    extract["retained_sha256_identical"] = (sha == "653c72ea869cbca7a9198b5e17b97bef516b67494e89bb919a9639d4eedbfa13")
except Exception as e:  # body not the catalogue
    extract["parse_error"] = repr(e)
json.dump({"read_log": log, "extract": extract}, open(ROOT / "studies/LH031/review/live_read_log.json", "w"), indent=2)
print(json.dumps(log, indent=2)); print(json.dumps({k: v for k, v in extract.items() if k != "entries"}, indent=2))
