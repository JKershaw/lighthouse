# LH050-policy-after collector (2026-11-21, label 2026-11-21T1414Z). Adapted from 2026-11-19T1417Z/collector.py: takes a JSON list of
# {"source_id","name","url"} on argv[2] instead of the panel; same robots gate, redaction, one retry for
# connection failures only, no retries around walls.
import hashlib, json, os, sys, time, urllib.request, urllib.error, datetime, socket
REPO = "/home/user/lighthouse"
sys.path.insert(0, os.path.join(REPO, "scripts"))
os.environ["LIGHTHOUSE_PROVIDER"] = "anthropic"
import lh_fetch
from lh_fetch import UA, NotFetched
from redact_emails import redact_bytes
label = sys.argv[1]
items = json.loads(sys.argv[2])
base = os.path.join(REPO, "studies/LH050/data", label)
os.makedirs(base + "/bodies", exist_ok=True); os.makedirs(base + "/robots", exist_ok=True)
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log = open(base + "/fetch_log.jsonl", "a")
for it in items:
    sid, url, nm = it["source_id"], it["url"], it["name"]
    ok, info = lh_fetch.check(url)
    info["checked_at"] = now()
    rref = "studies/LH050/data/%s/robots/%s.json" % (label, nm)
    json.dump(info, open(os.path.join(REPO, rref), "w"))
    rec = {"source_id": sid, "url": url, "robots_ref": rref, "provider": "anthropic"}
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
            open(os.path.join(REPO, rp), "wb").write(red)
            rec.update(status=status, final_url=final, content_type=ctype, received_bytes=len(body),
                       received_sha256=hashlib.sha256(body).hexdigest(), emails_redacted=n,
                       retained_sha256=hashlib.sha256(red).hexdigest(), retained_path=rp, access="readable")
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
    print(json.dumps({k: rec.get(k) for k in ("source_id","observed_at","status","access","received_bytes","emails_redacted","note")}))
    time.sleep(2)
