#!/usr/bin/env python3
"""Packagist per-version daily downloads for LH039 (brief.md, measure 3).

Packagist keeps the daily history, so this runs at each checkpoint, not daily.
For both Composer packages of WordPress core and every release of branches 7.1,
7.0 and 6.9, one GET of stats/<version>.json?average=daily&from=2026-10-14, kept
under data/packagist-<label>/ with readlog.csv. Skips a label already held.
From 21 November 2026 (the keeper's decision, notes/keeper/2026-11-21-robots-intent.md) a body is saved
only through scripts/lh_fetch.py's save_body; where it may not be kept, no <name>.json is written and
<name>.derived.json (write_derived) holds the read's metadata, body_kept "no: <reason>" and the daily
series; tabulate.py's measure 3 then stops ("readings unavailable") rather than drop the release.
Usage: python3 studies/LH039/scripts/packagist.py --read 2026-11-14T1415Z

Moved onto the shared fetch path (lh_fetch urlopen and save_body) on 21 November 2026 under the keeper's decision
(notes/keeper/2026-11-21-robots-intent.md); the evidence was collected by the earlier version, `git show 7523007:studies/LH039/scripts/packagist.py`.
"""
import argparse, csv, datetime, hashlib, json, os, sys, time, urllib.request
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', '..', 'scripts'))
from lh_fetch import urlopen, redacted, UA, save_body, write_derived  # noqa: E402  robots.txt gate (the keeper, 8 November 2026)

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
                fetched = False
                try:
                    with urlopen(req, timeout=60) as r:
                        body = r.read(4 << 20); status = r.status; ct = r.headers.get("Content-Type", "")
                        final, hdrs, fetched = r.geturl() or url, r.headers, True
                except Exception as e:
                    body = str(e).encode(); status = getattr(e, "code", "error"); ct = ""
                sha = hashlib.sha256(body).hexdigest()
                note = ""
                if not fetched:  # Lighthouse's own note of the failure, not a page body
                    open(os.path.join(d, name + ".json"), "wb").write(redacted(body))
                else:
                    kept, why = save_body(os.path.join(d, name + ".json"), body, final, hdrs)
                    if not kept:
                        try:
                            j = json.loads(body)
                            ext = {"labels": j["labels"], "values": j["values"]}
                        except Exception as e:
                            ext = {"extract_error": type(e).__name__}
                        write_derived(os.path.join(d, name + ".derived.json"), url, why, ext, read_utc=t,
                                      http_status=status, content_type=ct, bytes=len(body), sha256=sha)
                        note = "  body_kept: no: " + why
                w.writerow([name, url, t, status, ct, len(body), sha])
                print(name, status, len(body), note); time.sleep(0.5)

if __name__ == "__main__":
    sys.exit(main())
