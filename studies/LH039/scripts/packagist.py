#!/usr/bin/env python3
"""Packagist per-version daily downloads for LH039 (brief.md, measure 3).

Packagist keeps the daily history, so this runs at each checkpoint, not daily.
For both Composer packages of WordPress core and every release of branches 7.1,
7.0 and 6.9, one GET of stats/<version>.json?average=daily&from=2026-10-14, kept
under data/packagist-<label>/ with readlog.csv. Skips a label already held.
Usage: python3 studies/LH039/scripts/packagist.py --read 2026-11-14T1415Z
"""
import argparse, csv, datetime, hashlib, os, sys, time, urllib.request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, redacted, UA  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)

PACKAGES = ["roots/wordpress", "johnpbloch/wordpress-core"]
VERSIONS = (["7.1.%d" % i for i in range(0, 5)] + ["7.0.%d" % i for i in range(0, 9)]
            + ["6.9.%d" % i for i in range(0, 12)])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True)
    ap.add_argument("--extra", nargs="*", default=[], help="later releases named by an amendment, e.g. 7.1.5")
    a = ap.parse_args()
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "packagist-" + a.read)
    if os.path.exists(d):
        print("already held:", d); return
    os.makedirs(d)
    with open(os.path.join(d, "readlog.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["name", "url", "utc_start", "status", "content_type", "size", "sha256"])
        for pkg in PACKAGES:
            for v in VERSIONS + a.extra:
                url = "https://packagist.org/packages/%s/stats/%s.json?average=daily&from=2026-10-14" % (pkg, v)
                name = "%s-%s" % (pkg.split("/")[0], v)
                t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                try:
                    with urlopen(req, timeout=60) as r:
                        body = r.read(4 << 20); status = r.status; ct = r.headers.get("Content-Type", "")
                except Exception as e:
                    body = str(e).encode(); status = getattr(e, "code", "error"); ct = ""
                open(os.path.join(d, name + ".json"), "wb").write(redacted(body))
                w.writerow([name, url, t, status, ct, len(body), hashlib.sha256(body).hexdigest()])
                print(name, status, len(body)); time.sleep(0.5)

if __name__ == "__main__":
    sys.exit(main())
