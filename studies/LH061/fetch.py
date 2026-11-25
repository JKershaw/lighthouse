#!/usr/bin/env python3
"""LH061: one gated one-off GET of a document or locator page (brief, "How fetches are made and what is kept").

Written 25 November 2026 for the queue row LH061-search-read. Each call makes at most one request for one
URL (plus one retry only on a timeout, a connection error or HTTP 500, 502 or 504, as the brief allows),
through scripts/lh_fetch.py with access='oneoff' and check_redirects=True. A URL robots.txt refuses is not
requested and is logged "robots refusal" (no GET used). Every attempt goes in studies/LH061/fetchlog.csv.

Nothing is kept in the repository by this script except the log line. The bytes received and a text
extraction (pdftotext reading from stdin for a PDF; tags stripped for HTML) go to a working folder outside
the repository (argument --work, the session's scratchpad), only so that the reading agent can read the
document; that folder is deleted at the end of the session. Whether a body may be kept is decided later,
per document, by keep.py through save_body (keep_decision) and the document's own licence statement, and
otherwise write_derived. No code from any download is run; pdftotext only parses the bytes as a PDF.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH061/fetch.py --work <dir> --kind document|locator
         --id <id> --part A|B --url <url>
"""
import argparse, csv, datetime, hashlib, html, json, os, re, socket, subprocess, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from lh_fetch import urlopen, UA, NotFetched  # noqa: E402

LOG = os.path.join(HERE, "fetchlog.csv")
FIELDS = ["utc", "id", "kind", "part", "url", "attempt", "final_url", "status", "content_type", "bytes",
          "sha256", "outcome", "body_kept", "note"]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(row):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in FIELDS})


def strip_html(b):
    t = b.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>|</tr>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(re.sub(r"[ \t]+", " ", t))


def links(b, base):
    t = b.decode("utf-8", "replace")
    out = []
    for href, txt in re.findall(r'(?is)<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', t):
        txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", txt))).strip()
        out.append((urllib.request.urljoin(base, html.unescape(href)), txt[:160]))
    return out


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(req, timeout=90, check_redirects=True, access="oneoff") as r:
        return r.status, r.geturl() or url, dict(r.headers), r.read(64 << 20)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--kind", choices=["document", "locator"], required=True)
    ap.add_argument("--id", required=True)
    ap.add_argument("--part", choices=["A", "B"], required=True)
    ap.add_argument("--url", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    base = dict(id=a.id, kind=a.kind, part=a.part, url=a.url)
    for attempt in (1, 2):
        t = now()
        try:
            status, final, hdrs, body = get(a.url)
        except NotFetched as e:
            log({**base, "utc": t, "attempt": attempt, "outcome": "robots refusal (not requested)",
                 "body_kept": "no: not requested", "note": str(e)[:300]})
            print("ROBOTS REFUSAL", e); return
        except urllib.error.HTTPError as e:
            body = e.read(); status = e.code; final = e.geturl() or a.url; hdrs = dict(e.headers)
            if status in (500, 502, 504) and attempt == 1:
                log({**base, "utc": t, "attempt": attempt, "final_url": final, "status": status,
                     "outcome": "error, retried", "body_kept": "no: error"}); time.sleep(5); continue
        except (socket.timeout, TimeoutError, urllib.error.URLError, ConnectionError) as e:
            if attempt == 1:
                log({**base, "utc": t, "attempt": attempt, "outcome": "error, retried", "body_kept": "no: error",
                     "note": repr(e)[:300]}); time.sleep(5); continue
            log({**base, "utc": t, "attempt": attempt, "outcome": "error", "body_kept": "no: error",
                 "note": repr(e)[:300]}); print("ERROR", e); return
        sha = hashlib.sha256(body).hexdigest()
        ct = hdrs.get("Content-Type", hdrs.get("content-type", ""))
        outcome = "ok" if status == 200 else "wall (HTTP %s)" % status
        stem = os.path.join(a.work, a.id)
        with open(stem + ".bin", "wb") as f:
            f.write(body)
        json.dump({"url": a.url, "final_url": final, "read_utc": t, "status": status, "content_type": ct,
                   "bytes": len(body), "sha256": sha, "headers": hdrs}, open(stem + ".meta.json", "w"), indent=1)
        is_pdf = body[:5] == b"%PDF-" or "pdf" in ct.lower()
        if is_pdf:
            p = subprocess.run(["pdftotext", "-layout", "-", "-"], input=body, capture_output=True, timeout=300)
            text = p.stdout.decode("utf-8", "replace")
        else:
            text = strip_html(body)
            if a.kind == "locator":
                with open(stem + ".links.txt", "w") as f:
                    for u, x in links(body, final):
                        f.write("%s\t%s\n" % (u, x))
        with open(stem + ".txt", "w") as f:
            f.write(text)
        log({**base, "utc": t, "attempt": attempt, "final_url": final, "status": status, "content_type": ct,
             "bytes": len(body), "sha256": sha, "outcome": outcome,
             "body_kept": "pending (keep.py)" if a.kind == "document" else "no: locator, no body kept",
             "note": "text extracted for reading outside the repository; %d characters" % len(text)})
        print(status, ct, len(body), "pdf" if is_pdf else "html", len(text), "chars", final)
        return


if __name__ == "__main__":
    main()
