#!/usr/bin/env python3
"""LH055 horizon-lead intake read under the one-off rule (27 November 2026, Watch read).

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH055/scripts/intake_oneoff.py <label> <id=url>

Same as collect.py (one robots-gated GET, no retry, the same withholding, text extraction and log
fields), except that robots.txt is read with access='oneoff' (the keeper, 21 November 2026: a one-off,
targeted read) and each redirect is gated too. The body is kept only through lh_fetch.save_body; where
keep_decision says no, the text is held for this run only (text/<id>.txt.withheld-local) and the log
carries body_kept "no: <reason>". Exactly two arguments after the label are refused, so a stray flag
cannot become a label or a URL.
"""
import hashlib, json, os, sys
from urllib.error import HTTPError, URLError
from urllib.request import Request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from collect import ROOT, withhold, to_text, now  # noqa: E402
from lh_fetch import UA, NotFetched, check, urlopen, save_body  # noqa: E402

ACCESS = "oneoff"


def main(label, pair):
    if label.startswith("-") or "=" not in pair:
        sys.exit("usage: intake_oneoff.py <label> <id=url>")
    out = os.path.join(ROOT, "studies", "LH055", "data", label)
    for sub in ("bodies", "text", "robots"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    sid, url = pair.split("=", 1)
    rec = {"id": sid, "requested_url": url, "provider": os.environ.get("LIGHTHOUSE_PROVIDER", ""),
           "user_agent": UA, "access": ACCESS, "started": now()}
    ok, info = check(url, ACCESS)
    json.dump(info, open(os.path.join(out, "robots", sid + ".json"), "w"), indent=1, sort_keys=True)
    rec.update(robots_ok=ok, robots_ref="robots/%s.json" % sid)
    log = open(os.path.join(out, "fetch_log.jsonl"), "a")
    if not ok:
        rec.update(outcome="not_fetched_robots", finished=now())
        log.write(json.dumps(rec) + "\n")
        print(sid, "not fetched (robots)", info.get("reason"))
        return
    body, status, final, ctype, headers, resp_headers = b"", None, url, "", {}, None
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=60, check_redirects=True, access=ACCESS) as r:
            status, final, ctype = r.status, r.geturl(), r.headers.get("Content-Type", "")
            headers = {k: r.headers.get(k) for k in ("Last-Modified", "ETag", "Date", "Content-Length")}
            resp_headers = r.headers
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
        ktext, tcounts = withhold(to_text(body, ctype).encode("utf-8"))
        ok_keep, why = save_body(os.path.join(out, "bodies", sid + ".raw.gz"), kept, final or url, resp_headers, access=ACCESS)
        if ok_keep:
            open(os.path.join(out, "text", sid + ".txt"), "wb").write(ktext)
            rec.update(retained_body="bodies/%s.raw.gz" % sid, retained_text="text/%s.txt" % sid,
                       retained_sha256=hashlib.sha256(kept).hexdigest(), withheld_body=counts,
                       withheld_text=tcounts, text_chars=len(ktext))
        else:
            open(os.path.join(out, "text", sid + ".txt.withheld-local"), "wb").write(ktext)
            rec.update(body_kept="no: " + why, text_sha256=hashlib.sha256(ktext).hexdigest(), text_chars=len(ktext),
                       local_text="text/%s.txt.withheld-local (this run only; not retained)" % sid)
    rec["finished"] = now()
    log.write(json.dumps(rec) + "\n")
    print(sid, rec["outcome"], status, final, ctype, len(body), rec.get("body_kept", "kept"))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: intake_oneoff.py <label> <id=url>")
    main(sys.argv[1], sys.argv[2])
