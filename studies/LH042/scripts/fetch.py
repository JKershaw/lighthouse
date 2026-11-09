#!/usr/bin/env python3
"""LH042 collector: fetch a fixed list of public URLs once each and keep the raw bytes.

Usage (run from anywhere, with python3 -I):
    python3 -I studies/LH042/scripts/fetch.py --label <label> --urls <file>

<file> holds one URL per line; '#' starts a comment. Every saved body has
each IPv4 address replaced by 'x.x.x.x' before it is written (the SHA-256 of
the body as fetched is still logged), so no address of any host, exposed or
not, is retained (the keeper's caution of 8 November 2026). Pages whose
content is a list of exposed hosts are not put in a URL file at all.

Each body is saved as data/<label>/NNN.body with data/<label>/NNN.headers, and
data/<label>/readlog.csv gets one row per URL: n, url, start_utc, robots,
http_status, bytes, sha256_as_fetched, sha256_saved, final_url, content_type,
ipv4_redacted (how many addresses were replaced), emails_redacted
(email addresses withheld with scripts/redact_emails.py, added 8 November 2026
after rounds 1 to 5, whose bodies were redacted in place afterwards), error. robots.txt is read once per host through scripts/robots_gate.py (the keeper's rule
of 8 November 2026; from the robots sweep of 9 November 2026 it replaced urllib.robotparser checked
for this collector's own User-Agent): a URL it disallows, or whose robots.txt answers 5xx or cannot
be read (RFC 9309: complete disallow), is not fetched, and the robots column gives the reason with
the deciding group and rule. The client names itself honestly and sends no cookies, keys or email.

From 9 November 2026 (brief, amendment of that date; scripts/content_signal.py): where the robots.txt
the gate read, or a response header, carries a Content-Signal asking for use=reference or
use=immediate, a 2xx body is not kept: NNN.body holds a placeholder, NNN.withheld.json the sha256
of the bytes received, the signal as read and the page title, and NNN.body.withheld-local the whole
redacted body for this run only (git ignores it), so the brief's extract can be taken from it.
"""
import argparse
import csv
import datetime as dt
import hashlib
import pathlib
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts"))
from redact_emails import redact_bytes  # noqa: E402
from robots_gate import RobotsGate  # noqa: E402  the keeper's robots.txt rule, 8 November 2026
import content_signal  # noqa: E402  use=reference honoured from the next read (amendment, 9 November 2026)

UA = "Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)"  # was "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)" until 9 November 2026
GATE = RobotsGate(UA)
HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data"
IPV4 = re.compile(rb"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def robots_ok(url, cache=None, ctx=None):
    """(allowed, robots column) from scripts/robots_gate.py, which reads each host's robots.txt once per run.
    4xx: no rules. 5xx, unreachable or over 512 KiB: not fetched in this run (until 9 November 2026 this
    collector fetched anyway on a 5xx, saying so; RFC 9309 treats a 5xx as complete disallow)."""
    ok, info = GATE.check(url)
    state = "%s (robots %s, status %s, group %s, rule %s)" % (info.get("reason"), info.get("robots_url"),
                                                            info.get("robots_status"), info.get("decided_by", ""), info.get("rule", ""))
    return ok, state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--urls", required=True)
    ap.add_argument("--pause", type=float, default=2.0)
    a = ap.parse_args()
    out = DATA / a.label
    out.mkdir(parents=True, exist_ok=False)
    ctx = ssl.create_default_context()
    lines = []
    for raw in pathlib.Path(a.urls).read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append((s.split()[0], True))
    cache = {}
    rows = []
    for n, (url, redact) in enumerate(lines, 1):
        start = now()
        ok, rstate = robots_ok(url, cache, ctx)
        row = dict(n=n, url=url, start_utc=start, robots=rstate, http_status="", bytes="",
                   sha256_as_fetched="", sha256_saved="", final_url="", content_type="",
                   ipv4_redacted="", emails_redacted="", error="")
        if not ok:
            row["error"] = "not fetched: " + rstate
            rows.append(row)
            continue
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        body, headers = b"", ""
        try:
            with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
                body = r.read()
                row["http_status"] = r.status
                row["final_url"] = r.geturl()
                row["content_type"] = r.headers.get("Content-Type", "")
                headers = str(r.headers)
        except urllib.error.HTTPError as e:
            body = e.read() or b""
            row["http_status"] = e.code
            row["final_url"] = e.geturl()
            row["content_type"] = e.headers.get("Content-Type", "") if e.headers else ""
            headers = str(e.headers)
        except Exception as e:
            row["error"] = f"{type(e).__name__}: {e}"[:300]
        row["bytes"] = len(body)
        row["sha256_as_fetched"] = hashlib.sha256(body).hexdigest() if body else ""
        saved, nsub = IPV4.subn(b"x.x.x.x", body)
        saved, nmail = redact_bytes(saved)  # the keeper, 8 November 2026: email addresses are withheld
        row["ipv4_redacted"] = nsub
        row["emails_redacted"] = nmail
        row["sha256_saved"] = hashlib.sha256(saved).hexdigest() if saved else ""
        st = row["http_status"]
        sig = {"withhold": False}
        if isinstance(st, int) and 200 <= st < 300:
            # Amendment of 9 November 2026: where the governing robots.txt (as the gate read it, no new
            # request) or a response header carries a Content-Signal asking for use=reference, keep the
            # hash, the headers and a bounded extract, not the body; the whole (redacted) body is held
            # in NNN.body.withheld-local for this run only, which git ignores, for the brief's extract.
            hpairs = [tuple(x.split(": ", 1)) for x in headers.splitlines() if ": " in x]
            sig = content_signal.decide(GATE._robots(url).get("body"), hpairs, GATE.provider)
        if sig["withhold"]:
            content_signal.write_withheld(out / f"{n:03d}.body", saved, {
                "file": f"{n:03d}.body", "by": "studies/LH042/scripts/fetch.py", "url": url,
                "fetched_utc": start, "http_status": st, "headers": f"{n:03d}.headers",
                "sha256_received": row["sha256_as_fetched"], "bytes_received": len(body),
                "content_signal": {"line": sig["signal"], "where": sig["where"],
                                   "as_read": "robots.txt read by scripts/robots_gate.py in this run, sha256 %s"
                                   % GATE._robots(url).get("sha256", "") if sig["where"] == "robots.txt"
                                   else "response header"},
                "extract": {"title": content_signal.title_of(saved)}})
            row["sha256_saved"] = hashlib.sha256((out / f"{n:03d}.body").read_bytes()).hexdigest()
        else:
            (out / f"{n:03d}.body").write_bytes(saved)
        (out / f"{n:03d}.headers").write_text(headers)
        rows.append(row)
        time.sleep(a.pause)
    with open(out / "readlog.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r["n"], r["http_status"], r["bytes"], r["url"], r["error"])


if __name__ == "__main__":
    sys.exit(main())
