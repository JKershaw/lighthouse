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
after rounds 1 to 5, whose bodies were redacted in place afterwards), error. robots.txt is read once per host and a disallowed URL is not
fetched. The client names itself honestly and sends no cookies, keys or email.
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
import urllib.robotparser

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "scripts"))
from redact_emails import redact_bytes  # noqa: E402

UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"
HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE.parent / "data"
IPV4 = re.compile(rb"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")


def now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def robots_ok(url, cache, ctx):
    p = urllib.parse.urlsplit(url)
    root = f"{p.scheme}://{p.netloc}"
    if root not in cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            req = urllib.request.Request(root + "/robots.txt", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                rp.parse(r.read().decode("utf-8", "replace").splitlines())
            cache[root] = ("read", rp)
        except urllib.error.HTTPError as e:
            # 4xx: no robots file, everything allowed (the convention); 5xx: unknown, fetch anyway and say so
            cache[root] = (f"robots {e.code}", None)
        except Exception as e:  # unreachable robots.txt
            cache[root] = (f"robots unreadable ({type(e).__name__})", None)
    state, rp = cache[root]
    if rp is None:
        return True, state
    return rp.can_fetch(UA, url), ("allowed" if rp.can_fetch(UA, url) else "disallowed")


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
            row["error"] = "not fetched: robots.txt disallows"
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
