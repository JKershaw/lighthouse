#!/usr/bin/env python3
"""LH050's reusable collector (21 November 2026), made from the read of that day
(data/2026-11-21T1414Z/collector.py, itself adapted from data/2026-11-19T1417Z/collector.py) so that later
reads run one reviewed script rather than a fresh copy. Same behaviour: the robots.txt gate first, one GET
with redirects checked, email addresses withheld, one retry for a connection failure only, never a retry
around a wall.

Usage: LIGHTHOUSE_PROVIDER=<anthropic|openai> python3 -I studies/LH050/scripts/collect.py <UTC label> '<json>'
<json> is a list of {"source_id", "name", "url"}; for the locked panel, the rows of panel.csv with a name each.
Writes data/<label>/bodies/<name>.<html|pdf>, data/<label>/robots/<name>.json and one line per URL in
data/<label>/fetch_log.jsonl.

What may be kept (the keeper's decision of 21 November 2026, notes/keeper/2026-11-21-robots-intent.md): a body
is written through scripts/lh_fetch.py's save_body, which keeps nothing where robots.txt refuses `*`, an
AI-training or archiving crawler, or the page reserves itself. The log line then says body_kept "no: <reason>";
bodies/<name>.derived.json holds the URL, read time, status, hashes and the page title; and the redacted body
is held for this run only in bodies/<name>.<ext>.withheld-local (git ignores it), so the reader can take claims
and short attributed quotes from it. Claims cite that read; the copy is not retained.
"""
import datetime, hashlib, json, os, re, socket, sys, time, urllib.error, urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import lh_fetch  # noqa: E402
from lh_fetch import UA, NotFetched, save_body, write_derived  # noqa: E402
from redact_emails import redact_bytes  # noqa: E402

LOCAL = ".withheld-local"  # as scripts/content_signal.py: git ignores it


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def title_of(body):
    m = re.search(rb"(?is)<title[^>]*>(.*?)</title>", body[:200000])
    return m.group(1).decode("utf-8", "replace").strip()[:300] if m else None


def main(label, items):
    base = os.path.join(REPO, "studies/LH050/data", label)
    os.makedirs(base + "/bodies", exist_ok=True)
    os.makedirs(base + "/robots", exist_ok=True)
    provider = os.environ.get("LIGHTHOUSE_PROVIDER", "") or "all"
    log = open(base + "/fetch_log.jsonl", "a")
    for it in items:
        sid, url, nm = it["source_id"], it["url"], it["name"]
        ok, info = lh_fetch.check(url)
        info["checked_at"] = now()
        rref = "studies/LH050/data/%s/robots/%s.json" % (label, nm)
        json.dump(info, open(os.path.join(REPO, rref), "w"))
        rec = {"source_id": sid, "url": url, "robots_ref": rref, "provider": provider}
        if not ok:
            rec.update(observed_at=now(), access="unavailable", note="robots: " + str(info.get("reason", "")))
            log.write(json.dumps(rec) + "\n"); log.flush(); print(json.dumps(rec)); continue
        attempts = 0
        while True:
            attempts += 1
            rec["observed_at"] = now()
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                r = lh_fetch.urlopen(req, timeout=60, check_redirects=True)
                body = r.read(); status = r.status; final = r.geturl(); ctype = r.headers.get("Content-Type", "")
                red, n = redact_bytes(body)
                ext = ".pdf" if ("pdf" in ctype or body[:5] == b"%PDF-") else ".html"
                rp = "studies/LH050/data/%s/bodies/%s%s" % (label, nm, ext)
                rec.update(status=status, final_url=final, content_type=ctype, received_bytes=len(body),
                           received_sha256=hashlib.sha256(body).hexdigest(), emails_redacted=n,
                           retained_sha256=hashlib.sha256(red).hexdigest(), access="readable")
                kept, why = save_body(os.path.join(REPO, rp), body, final or url, r.headers)
                if kept:
                    rec["retained_path"] = rp
                else:
                    dp = "studies/LH050/data/%s/bodies/%s.derived.json" % (label, nm)
                    rec.update(body_kept="no: " + why, retained_sha256="", derived_path=dp,
                               local_copy=rp + LOCAL + " (this run only; not retained)")
                    open(os.path.join(REPO, rp + LOCAL), "wb").write(red)
                    write_derived(os.path.join(REPO, dp), url, why, {"title": title_of(red)}, final_url=final,
                                  read_utc=rec["observed_at"], http_status=status, content_type=ctype,
                                  bytes_received=len(body), sha256_received=rec["received_sha256"],
                                  used_for="Claims and short quotes taken from this read's run copy cite this read.")
                break
            except urllib.error.HTTPError as e:
                body = e.read() if hasattr(e, "read") else b""
                rec.update(status=e.code, access="unavailable", received_bytes=len(body),
                           received_sha256=hashlib.sha256(body).hexdigest() if body else "",
                           note="HTTP %s; wall or error, not retried" % e.code)
                break
            except NotFetched as e:
                rec.update(access="unavailable", note=str(e)); break
            except (urllib.error.URLError, socket.timeout, ConnectionError, TimeoutError) as e:
                if attempts == 1:
                    rec["first_attempt_error"] = repr(e); time.sleep(5); continue
                rec.update(access="unavailable", note="connection failure after one retry: %r" % (e,)); break
        rec["attempts"] = attempts
        log.write(json.dumps(rec) + "\n"); log.flush()
        print(json.dumps({k: rec.get(k) for k in ("source_id", "observed_at", "status", "access", "received_bytes",
                                                  "emails_redacted", "body_kept", "note")}))
        time.sleep(2)


if __name__ == "__main__":
    main(sys.argv[1], json.loads(sys.argv[2]))
