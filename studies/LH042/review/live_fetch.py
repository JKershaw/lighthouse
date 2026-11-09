#!/usr/bin/env python3
"""LH042 evidence review: re-read a few publishers' pages live, once each.
Honest User-Agent, robots.txt read first through scripts/robots_gate.py (from the robots sweep
of 9 November 2026; a disallowed URL, or one whose robots.txt cannot be read, is not fetched), two
seconds apart, no cookies, keys or email. Every saved body has IPv4 addresses replaced
and email addresses withheld (scripts/redact_emails.py) before it is written; the log
keeps the hash of the bytes as received.
Usage: python3 -I studies/LH042/review/live_fetch.py studies/LH042/review/live_urls.txt studies/LH042/review/live"""
import csv, datetime as dt, hashlib, pathlib, re, ssl, sys, time
import urllib.error, urllib.parse, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts"))
from redact_emails import redact_bytes
from robots_gate import RobotsGate  # the keeper's robots.txt rule, 8 November 2026
UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"
GATE = RobotsGate(UA)
IPV4 = re.compile(rb"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
urls = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
ctx = ssl.create_default_context(); robots = {}; log = []
for n, u in enumerate(urls, 1):
    t = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ok, info = GATE.check(u)
    why = "%s (group %s, rule %s)" % (info.get("reason"), info.get("decided_by", ""), info.get("rule", ""))
    row = dict(n=n, url=u, start_utc=t, robots="", status="", bytes="", sha256_received="", ipv4_replaced="", emails_withheld="", error="")
    if not ok:
        row["robots"] = "not fetched: " + why; log.append(row); continue
    row["robots"] = why
    body = b""
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*"}), timeout=60, context=ctx) as r:
            body = r.read(); row["status"] = r.status
    except urllib.error.HTTPError as e:
        body = e.read() or b""; row["status"] = e.code
    except Exception as e:
        row["error"] = f"{type(e).__name__}: {e}"[:200]
    row["bytes"] = len(body); row["sha256_received"] = hashlib.sha256(body).hexdigest() if body else ""
    s, k = IPV4.subn(b"x.x.x.x", body); s, m = redact_bytes(s)
    row["ipv4_replaced"] = k; row["emails_withheld"] = m
    (out / f"{n:03d}.body").write_bytes(s)
    log.append(row); time.sleep(2)
with open(out / "readlog.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(log[0])); w.writeheader(); w.writerows(log)
for r in log:
    print(r["n"], r["start_utc"], r["robots"], r["status"], r["bytes"], r["url"], r["error"])
