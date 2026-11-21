# Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
# (notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH050/data/2026-11-19T1417Z/collector.py`.
import csv, hashlib, json, os, sys, time, urllib.request, urllib.error, datetime, socket
REPO = "/home/user/lighthouse"
sys.path.insert(0, os.path.join(REPO, "scripts"))
os.environ["LIGHTHOUSE_PROVIDER"] = "anthropic"
import lh_fetch
from lh_fetch import UA, NotFetched
from redact_emails import redact_bytes
label = sys.argv[1]
base = os.path.join(REPO, "studies/LH050/data", label)
os.makedirs(base + "/bodies", exist_ok=True); os.makedirs(base + "/robots", exist_ok=True)
names = {"PA-S24":"S24_techcentral","PA-S25":"S25_eweek","PA-S26":"S26_assemblymag","PA-S27":"S27_tnw",
         "PA-S16":"S16_unoda","PA-S15":"S15_ungeneva","PA-S11":"S11_icrc_faq","PA-S13":"S13_jsp936"}
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
log = open(base + "/fetch_log.jsonl", "a")
for row in csv.DictReader(open(os.path.join(REPO, "studies/LH050/panel.csv"))):
    sid, url, nm = row["source_id"], row["url"], names[row["source_id"]]
    ok, info = lh_fetch.check(url)
    info["checked_at"] = now()
    rref = "studies/LH050/data/%s/robots/%s.json" % (label, nm)
    json.dump(info, open(os.path.join(REPO, rref), "w"))
    rec = {"panel_id": row["panel_id"], "source_id": sid, "url": url, "robots_ref": rref, "provider": "anthropic"}
    if not ok:
        rec.update(observed_at=now(), access="unavailable", note="robots: " + info.get("reason", ""))
        log.write(json.dumps(rec) + "\n"); log.flush(); print(rec); continue
    attempts = 0
    while True:
        attempts += 1
        rec["observed_at"] = now()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            r = lh_fetch.urlopen(req, timeout=40, check_redirects=True)
            body = r.read(); status = r.status; final = r.geturl(); ctype = r.headers.get("Content-Type", "")
            red, n = redact_bytes(body)
            ext = ".pdf" if "pdf" in ctype else ".html"
            rp = "studies/LH050/data/%s/bodies/%s%s" % (label, nm, ext)
            # saved only through lh_fetch's save_body (the keeper, 21 November 2026); this collector is the record
            # of its read and is not run again; a kept body is unchanged
            kept, why = lh_fetch.save_body(os.path.join(REPO, rp), body, final or url, r.headers)
            rec.update(status=status, final_url=final, content_type=ctype, received_bytes=len(body),
                       received_sha256=hashlib.sha256(body).hexdigest(), emails_redacted=n,
                       retained_sha256=hashlib.sha256(red).hexdigest() if kept else "", retained_path=rp if kept else "",
                       access="readable")
            if not kept:
                rec["body_kept"] = "no: " + why
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
