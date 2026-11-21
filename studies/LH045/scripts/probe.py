#!/usr/bin/env python3
"""Pre-brief reads for LH045: fetch named URLs once each and keep them raw.

Bodies go to <outdir>/<name>.raw, with readlog.csv appended (name, url, UTC start,
status, content type, size, SHA-256). A name already held is skipped, so a rerun
fetches nothing twice. These reads establish what each source publishes, its terms
and its robots.txt; they are not the study's captures (scripts/collect.py).
Usage: python3 -I probe.py <outdir> name=url [name=url ...]

From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md; the pre-brief reads
above were made before it): each URL is fetched through scripts/lh_fetch.py's urlopen with access='oneoff'
(before, urllib's urlopen with no robots check), so a URL robots.txt refuses is not requested and its .raw
holds Lighthouse's own note (status "error", as for any failure); a body, also an HTTP error's, is saved only
through lh_fetch's save_body, which withholds email addresses. Where it may not be kept no .raw is written,
and <name>.derived.json (write_derived) records URL, time, status, size, SHA-256 and body_kept
"no: <reason>"; a rerun treats that name as held.

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH045/scripts/probe.py`.
"""
import csv, datetime, hashlib, os, sys, time, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts"))
from lh_fetch import urlopen, save_body, write_derived  # noqa: E402  robots.txt gate and the one keep path (21 November 2026)

UA = "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)"

def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    log = os.path.join(out, "readlog.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["name", "url", "utc_start", "status", "content_type", "size", "sha256"])
        for arg in sys.argv[2:]:
            name, url = arg.split("=", 1)
            path = os.path.join(out, name + ".raw")
            dpath = os.path.join(out, name + ".derived.json")
            if os.path.exists(path) or os.path.exists(dpath):
                print("held", name); continue
            t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            fetched, final, hdrs = True, url, None
            try:
                with urlopen(req, timeout=60, access="oneoff") as r:
                    body = r.read(16 << 20); status = r.status; ct = r.headers.get("Content-Type", "")
                    final, hdrs = r.geturl() or url, r.headers
            except urllib.error.HTTPError as e:
                body = e.read(); status = e.code; ct = e.headers.get("Content-Type", ""); final, hdrs = e.geturl() or url, e.headers
                if not body:
                    body, fetched = str(e).encode(), False
            except Exception as e:
                body = repr(e).encode(); status = "error"; ct = ""; fetched = False
            sha = hashlib.sha256(body).hexdigest()
            note = ""
            if not fetched:  # Lighthouse's own note of the failure or refusal, not a page body
                open(path, "wb").write(body)
            else:
                kept, why = save_body(path, body, final, hdrs)
                if not kept:
                    write_derived(dpath, url, why, {}, read_utc=t, http_status=status, content_type=ct,
                                  bytes=len(body), sha256=sha)
                    note = "body_kept: no: " + why
            w.writerow([name, url, t, status, ct, len(body), sha])
            f.flush()
            print(name, status, ct, len(body), note)
            time.sleep(1)

if __name__ == "__main__":
    main()
