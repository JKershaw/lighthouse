# Essay fact-check reads, 28 November 2026 (row LH050-essay-draft). NOT LH050 collection: one-off reads
# (access='oneoff', the keeper's decision of 21 November 2026) of the commissioning essay's own cited URLs,
# at most eight. Robots check before each request; body kept only through lh_fetch.save_body (keep_decision);
# no retries around walls; one retry only for a connection failure. Writes fetchlog.jsonl (one line per URL)
# and robots/<name>.json. Run once: python3 -I collector.py '<json list of {"name","url"}>'
import hashlib, json, os, sys, time, urllib.request, urllib.error, datetime, socket
REPO = "/home/user/lighthouse"
sys.path.insert(0, os.path.join(REPO, "scripts"))
os.environ["LIGHTHOUSE_PROVIDER"] = "anthropic"
import lh_fetch
from lh_fetch import UA, NotFetched
from redact_emails import redact_bytes
base = os.path.join(REPO, "notes/physical-authority/essay-checks/2026-11-28")
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log = open(os.path.join(base, "fetchlog.jsonl"), "a")
for it in json.loads(sys.argv[1]):
    nm, url = it["name"], it["url"]
    ok, info = lh_fetch.check(url, access='oneoff')
    info["checked_at"] = now()
    json.dump(info, open(os.path.join(base, "robots", nm + ".json"), "w"), indent=1)
    rec = {"name": nm, "url": url, "provider": "anthropic", "access_mode": "oneoff",
           "robots_decision": "%s (%s; group %s; rule %s)" % ("allowed" if ok else "refused", info.get("reason"), info.get("decided_by"), info.get("rule"))}
    if not ok:
        rec.update(utc=now(), http_status=None, bytes=0, sha256="", kept="no: not requested, robots.txt refuses the URL for the one-off read")
        log.write(json.dumps(rec) + "\n"); log.flush(); print(json.dumps(rec)); continue
    attempts = 0
    while True:
        attempts += 1
        rec["utc"] = now()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = lh_fetch.urlopen(req, timeout=60, check_redirects=True, access='oneoff')
            body = r.read(); final = r.geturl(); ctype = r.headers.get("Content-Type", "")
            ext = ".pdf" if body[:5] == b"%PDF-" else ".html"
            path = os.path.join(base, "bodies", nm + ext)
            kept, why = lh_fetch.save_body(path, body, final or url, r.headers, access='oneoff')
            rec.update(http_status=r.status, final_url=final, content_type=ctype, bytes=len(body),
                       sha256=hashlib.sha256(body).hexdigest(), emails_redacted=redact_bytes(body)[1],
                       kept=("yes: " + why + "; bodies/" + nm + ext) if kept else ("no: " + why))
            break
        except urllib.error.HTTPError as e:
            body = e.read() if hasattr(e, "read") else b""
            rec.update(http_status=e.code, bytes=len(body), sha256=hashlib.sha256(body).hexdigest() if body else "",
                       kept="no: HTTP %s, a wall or error; not retried, body not kept" % e.code)
            break
        except NotFetched as e:
            rec.update(http_status=None, bytes=0, sha256="", kept="no: " + str(e)); break
        except (urllib.error.URLError, socket.timeout, ConnectionError, TimeoutError) as e:
            if attempts == 1:
                rec["first_attempt_error"] = repr(e); time.sleep(5); continue
            rec.update(http_status=None, bytes=0, sha256="", kept="no: connection failure after one retry: %r" % (e,)); break
    rec["attempts"] = attempts
    log.write(json.dumps(rec) + "\n"); log.flush(); print(json.dumps(rec))
    time.sleep(2)
