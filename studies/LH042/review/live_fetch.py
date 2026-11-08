#!/usr/bin/env python3
"""LH042 evidence review: re-read a few publishers' pages live, once each.
Honest User-Agent, robots.txt read first (a disallowed URL is not fetched), two
seconds apart, no cookies, keys or email. Every saved body has IPv4 addresses replaced
and email addresses withheld (scripts/redact_emails.py) before it is written; the log
keeps the hash of the bytes as received.
Usage: python3 -I studies/LH042/review/live_fetch.py studies/LH042/review/live_urls.txt studies/LH042/review/live"""
import csv, datetime as dt, hashlib, pathlib, re, ssl, sys, time
import urllib.error, urllib.parse, urllib.request, urllib.robotparser
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts"))
from redact_emails import redact_bytes
UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
IPV4 = re.compile(rb"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
urls = [l.split()[0] for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
ctx = ssl.create_default_context(); robots = {}; log = []
for n, u in enumerate(urls, 1):
    t = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    p = urllib.parse.urlsplit(u); root = f"{p.scheme}://{p.netloc}"
    if root not in robots:
        rp = urllib.robotparser.RobotFileParser()
        try:
            with urllib.request.urlopen(urllib.request.Request(root + "/robots.txt", headers={"User-Agent": UA}), timeout=30, context=ctx) as r:
                rp.parse(r.read().decode("utf-8", "replace").splitlines()); robots[root] = rp
        except urllib.error.HTTPError as e:
            robots[root] = None if e.code < 500 else "unknown"
        except Exception:
            robots[root] = "unknown"
    rp = robots[root]
    row = dict(n=n, url=u, start_utc=t, robots="", status="", bytes="", sha256_received="", ipv4_replaced="", emails_withheld="", error="")
    if rp == "unknown":
        row["robots"] = "unreadable; not fetched"; log.append(row); continue
    if rp is not None and not rp.can_fetch(UA, u):
        row["robots"] = "disallowed; not fetched"; log.append(row); continue
    row["robots"] = "allowed" if rp is not None else "no robots.txt (4xx)"
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
