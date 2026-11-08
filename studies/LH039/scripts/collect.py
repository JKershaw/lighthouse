#!/usr/bin/env python3
"""Daily read for LH039 (WordPress core CVE-2026-119977), under brief.md (0.1 from 8 November 2026).

One GET per URL, bodies kept as fetched under data/raw-<label>/ with readlog.csv
(url, UTC start, status, content type, size, SHA-256). Skips a label already held.
Usage: python3 studies/LH039/scripts/collect.py --read 2026-11-08T1415Z
"""
import argparse, csv, datetime, hashlib, os, sys, urllib.request

URLS = [
    ("stats-1", "https://api.wordpress.org/stats/wordpress/1.0/"),
    ("stats-2", "https://api.wordpress.org/stats/php/1.0/"),
    ("stats-3", "https://api.wordpress.org/stats/mysql/1.0/"),
    ("stats-4", "https://api.wordpress.org/stats/locale/1.0/"),
    ("meta-1", "https://api.wordpress.org/core/version-check/1.7/"),
    ("meta-4", "https://api.wordpress.org/core/stable-check/1.0/"),
    ("cand-2", "https://wordpress.org/download/counter/"),
    ("cand-3", "https://w3techs.com/technologies/details/cm-wordpress"),
    ("cand-4", "https://w3techs.com/technologies/details/cm-wordpress/7"),
    ("cand-5", "https://packagist.org/packages/roots/wordpress/stats.json"),
    ("cand-6", "https://packagist.org/packages/johnpbloch/wordpress-core/stats.json"),
    # Added by brief 0.1 (8 November 2026): W3Techs's patch-level pages and monthly
    # history for the three branches with the most sites among those offered a fix,
    # and WordPress.org's per-branch download counters.
    ("w3-71", "https://w3techs.com/technologies/details/cm-wordpress/7.1"),
    ("w3-70", "https://w3techs.com/technologies/details/cm-wordpress/7.0"),
    ("w3-69", "https://w3techs.com/technologies/details/cm-wordpress/6.9"),
    ("w3h-71", "https://w3techs.com/technologies/history_details/cm-wordpress/7.1"),
    ("w3h-70", "https://w3techs.com/technologies/history_details/cm-wordpress/7.0"),
    ("w3h-69", "https://w3techs.com/technologies/history_details/cm-wordpress/6.9"),
    ("dl-71", "https://wordpress.org/wp-json/wporg/v1/core-downloads/7.1"),
    ("dl-70", "https://wordpress.org/wp-json/wporg/v1/core-downloads/7.0"),
    ("dl-69", "https://wordpress.org/wp-json/wporg/v1/core-downloads/6.9"),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--read", required=True, help="UTC label YYYY-MM-DDTHHMMZ, the minute the collector starts")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(here, "..", "data", "raw-" + a.read)
    if os.path.exists(d):
        print("already held:", d); return
    os.makedirs(d)
    with open(os.path.join(d, "readlog.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["name", "url", "utc_start", "status", "content_type", "size", "sha256"])
        for name, url in URLS:
            t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            req = urllib.request.Request(url, headers={"User-Agent": "Lighthouse-research/1.0"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    body = r.read(4 << 20); status = r.status; ct = r.headers.get("Content-Type", "")
            except Exception as e:
                body = str(e).encode(); status = getattr(e, "code", "error"); ct = ""
            open(os.path.join(d, name + ".body"), "wb").write(body)
            w.writerow([name, url, t, status, ct, len(body), hashlib.sha256(body).hexdigest()])
            print(name, status, len(body))

if __name__ == "__main__":
    sys.exit(main())
