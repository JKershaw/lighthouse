#!/usr/bin/env python3
"""LH042 evidence review: re-read a few publishers' pages live, once each.
Honest User-Agent, robots.txt read first through scripts/robots_gate.py (from the robots sweep
of 9 November 2026; a disallowed URL, or one whose robots.txt cannot be read, is not fetched), two
seconds apart, no cookies, keys or email. Every saved body has IPv4 addresses replaced
and email addresses withheld (scripts/redact_emails.py) before it is written; the log
keeps the hash of the bytes as received.
From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md; the record of the
LH042 evidence review's live read, not run again): the gate is scripts/lh_fetch.py's own (check, then
lh_fetch's urlopen, which asks the same cached gate, so the rule and the robots.txt reads are unchanged),
and the body, after the IPv4 replacement, is saved only through lh_fetch's save_body; where it may not be
kept no NNN.body is written and readlog.csv gains a body_kept column ("no: <reason>"), added only when
some body was not kept. A kept body is written under the same name with the same bytes as before.
Usage: python3 -I studies/LH042/review/live_fetch.py studies/LH042/review/live_urls.txt studies/LH042/review/live

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH042/review/live_fetch.py`."""
import csv, datetime as dt, hashlib, pathlib, re, ssl, sys, time
import urllib.error, urllib.parse, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts"))
from redact_emails import redact_bytes
from lh_fetch import check, urlopen, save_body, UA  # robots.txt rule (8 November 2026), one keep path (21 November)
IPV4 = re.compile(rb"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
urls = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
ctx = ssl.create_default_context(); robots = {}; log = []
for n, u in enumerate(urls, 1):
    t = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ok, info = check(u)
    why = "%s (group %s, rule %s)" % (info.get("reason"), info.get("decided_by", ""), info.get("rule", ""))
    row = dict(n=n, url=u, start_utc=t, robots="", status="", bytes="", sha256_received="", ipv4_replaced="", emails_withheld="", error="")
    if not ok:
        row["robots"] = "not fetched: " + why; log.append(row); continue
    row["robots"] = why
    body = b""
    try:
        with urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "*/*"}), timeout=60, context=ctx) as r:
            body = r.read(); row["status"] = r.status; final, hdrs = r.geturl() or u, r.headers
    except urllib.error.HTTPError as e:
        body = e.read() or b""; row["status"] = e.code; final, hdrs = e.geturl() or u, e.headers
    except Exception as e:
        row["error"] = f"{type(e).__name__}: {e}"[:200]; final, hdrs = u, None
    row["bytes"] = len(body); row["sha256_received"] = hashlib.sha256(body).hexdigest() if body else ""
    s, k = IPV4.subn(b"x.x.x.x", body); s, m = redact_bytes(s)
    row["ipv4_replaced"] = k; row["emails_withheld"] = m
    kept, why = save_body(out / f"{n:03d}.body", s, final, hdrs)
    if not kept:
        row["body_kept"] = "no: " + why
    log.append(row); time.sleep(2)
with open(out / "readlog.csv", "w", newline="") as f:
    fields = [k for k in log[0] if k != "body_kept"] + (["body_kept"] if any("body_kept" in r for r in log) else [])
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(log)
for r in log:
    print(r["n"], r["start_utc"], r["robots"], r["status"], r["bytes"], r["url"], r["error"])
