#!/usr/bin/env python3
"""Pre-brief reads for LH045: fetch named URLs once each and keep them raw.

Bodies go to <outdir>/<name>.raw, with readlog.csv appended (name, url, UTC start,
status, content type, size, SHA-256). A name already held is skipped, so a rerun
fetches nothing twice. These reads establish what each source publishes, its terms
and its robots.txt; they are not the study's captures (scripts/collect.py).
Usage: python3 -I probe.py <outdir> name=url [name=url ...]
"""
import csv, datetime, hashlib, os, sys, time, urllib.request

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
            if os.path.exists(path):
                print("held", name); continue
            t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read(16 << 20); status = r.status; ct = r.headers.get("Content-Type", "")
            except urllib.error.HTTPError as e:
                body = e.read() or str(e).encode(); status = e.code; ct = e.headers.get("Content-Type", "")
            except Exception as e:
                body = repr(e).encode(); status = "error"; ct = ""
            open(path, "wb").write(body)
            w.writerow([name, url, t, status, ct, len(body), hashlib.sha256(body).hexdigest()])
            f.flush()
            print(name, status, ct, len(body))
            time.sleep(1)

if __name__ == "__main__":
    main()
