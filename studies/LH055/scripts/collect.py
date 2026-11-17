#!/usr/bin/env python3
"""LH055 collector: one robots-gated content GET per URL, retained under the brief's rules.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH055/scripts/collect.py <label> <id=url>...

For each id=url: ask scripts/robots_gate.py; if allowed, make exactly one GET (redirects followed by
urllib, no retry); keep the received-body sha256 and length; withhold email addresses, IPv4
addresses, key-shaped strings and defanged indicators from the retained body and text; write
data/<label>/bodies/<id>.raw.gz, data/<label>/text/<id>.txt, data/<label>/robots/<id>.json and one
line per URL in data/<label>/fetch_log.jsonl. A wall (403, challenge, error) is logged, not retried.
Nothing fetched is executed. Text is extracted with pdftotext for PDFs and scripts/reader_view.py's
parser for HTML.
"""
import datetime, gzip, hashlib, json, os, re, subprocess, sys, tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from lh_fetch import UA, NotFetched, check, urlopen  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402
from reader_view import View  # noqa: E402

PATTERNS = [
    (re.compile(rb"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b"), b"[ipv4 withheld]"),
    (re.compile(rb"\b(?:sk|pk|rk)-[A-Za-z0-9_\-]{16,}"), b"[key withheld]"),
    (re.compile(rb"\bAKIA[0-9A-Z]{16}\b"), b"[key withheld]"),
    (re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}"), b"[key withheld]"),
    (re.compile(rb"\bAIza[0-9A-Za-z_\-]{30,}"), b"[key withheld]"),
    (re.compile(rb"hxxps?://\S+", re.I), b"[defanged indicator withheld]"),
    (re.compile(rb"\b[\w\-]+(?:\[\.\][\w\-]+)+\b"), b"[defanged indicator withheld]"),
]


def withhold(b):
    b, n_email = redact_bytes(b)
    counts = {"email": n_email}
    for pat, rep in PATTERNS:
        b, n = pat.subn(rep, b)
        counts[rep.decode()] = counts.get(rep.decode(), 0) + n
    return b, counts


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def to_text(body, ctype):
    if "pdf" in (ctype or "") or body[:5] == b"%PDF-":
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "in.pdf")
            open(p, "wb").write(body)
            r = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, timeout=120)
            return r.stdout.decode("utf-8", "replace")
    v = View()
    v.feed(body.decode("utf-8", "replace"))
    v.flush()
    return "\n".join(v.out)


def main(label, pairs):
    out = os.path.join(ROOT, "studies", "LH055", "data", label)
    for sub in ("bodies", "text", "robots"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    log = open(os.path.join(out, "fetch_log.jsonl"), "a")
    for pair in pairs:
        sid, url = pair.split("=", 1)
        rec = {"id": sid, "requested_url": url, "provider": os.environ.get("LIGHTHOUSE_PROVIDER", ""),
               "user_agent": UA, "started": now()}
        ok, info = check(url)
        json.dump(info, open(os.path.join(out, "robots", sid + ".json"), "w"), indent=1, sort_keys=True)
        rec["robots_ok"] = ok
        rec["robots_ref"] = "robots/%s.json" % sid
        if not ok:
            rec.update(outcome="not_fetched_robots", finished=now())
            log.write(json.dumps(rec) + "\n"); log.flush()
            print(sid, "not fetched (robots)", info.get("reason"))
            continue
        body, status, final, ctype, headers = b"", None, url, "", {}
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=60) as r:
                status, final, ctype = r.status, r.geturl(), r.headers.get("Content-Type", "")
                headers = {k: r.headers.get(k) for k in ("Last-Modified", "ETag", "Date", "Content-Length")}
                body = r.read()
            rec["outcome"] = "received"
        except HTTPError as e:
            status, ctype = e.code, e.headers.get("Content-Type", "") if e.headers else ""
            body = e.read() if hasattr(e, "read") else b""
            rec["outcome"] = "http_error"
        except (URLError, NotFetched, OSError) as e:
            rec["outcome"] = "network_error"
            rec["error"] = str(e)[:300]
        rec.update(status=status, final_url=final, content_type=ctype, headers=headers,
                   received_bytes=len(body), received_sha256=hashlib.sha256(body).hexdigest() if body else "")
        if rec["outcome"] == "received":
            kept, counts = withhold(body)
            gzip.open(os.path.join(out, "bodies", sid + ".raw.gz"), "wb").write(kept)
            text = to_text(body, ctype)
            ktext, tcounts = withhold(text.encode("utf-8"))
            open(os.path.join(out, "text", sid + ".txt"), "wb").write(ktext)
            rec.update(retained_body="bodies/%s.raw.gz" % sid, retained_text="text/%s.txt" % sid,
                       retained_sha256=hashlib.sha256(kept).hexdigest(), withheld_body=counts,
                       withheld_text=tcounts, text_chars=len(ktext))
        rec["finished"] = now()
        log.write(json.dumps(rec) + "\n"); log.flush()
        print(sid, rec["outcome"], status, final, ctype, len(body))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
