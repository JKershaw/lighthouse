#!/usr/bin/env python3
"""Replace LH034's kept copies of nodejs.org/dist/index.json with derived files (the keeper's decision of
21 November 2026, notes/keeper/2026-11-21-robots-intent.md: nodejs.org's robots.txt refuses all bots
under `*` for /dist/).

For each data/read-*/dist-index.raw.gz it writes dist-index.derived.json beside it, holding the URL, read
times, HTTP status, size and SHA-256 from that read's read_log.json, and only what the study uses: the
release list in the file's order, each entry's version, date and security flag (release order and dates
for tabulate.py; dates and security flags for review/R-0039_checks.py and the brief's measure 4).
It never deletes anything. Offline, standard library only.
Usage: python3 -I studies/LH034/scripts/derive_kept.py
"""
import glob, gzip, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
NOTE = ("Body removed on 21 November 2026 under the keeper's decision (notes/keeper/2026-11-21-robots-intent.md): "
        "the site's robots.txt refuses AI-training or archiving crawlers, or all bots, so Lighthouse keeps the "
        "URL, read time, status, SHA-256 of the bytes received and the facts its records use, not the page.")


USED = "Release order and dates (tabulate.py); dates and security flags (review/R-0039_checks.py, measure 4)."


def dist_index_extract(body):
    """The facts the study uses from dist/index.json: each release's version, date and security flag, in order."""
    return {"fields": ["version", "date", "security"],
            "releases": [[r["version"], r["date"], r.get("security")] for r in json.loads(body)]}


def main():
    n = 0
    for d in sorted(glob.glob(os.path.join(DATA, "read-*"))):
        p = os.path.join(d, "dist-index.raw.gz")
        if not os.path.exists(p):
            continue
        row = next(r for r in json.load(open(os.path.join(d, "read_log.json"))) if r.get("source") == "dist-index")
        rec = {"url": row["url"], "read_utc": row.get("start_utc"), "finish_utc": row.get("finish_utc"),
               "http_status": row.get("status"), "bytes": row.get("bytes"), "sha256": row.get("sha256"),
               "robots_class": "B: * refuses all bots (no AI token named)", "body_removed": NOTE,
               "used_for": USED, "extracted": dist_index_extract(gzip.decompress(open(p, "rb").read()))}
        open(os.path.join(d, "dist-index.derived.json"), "w").write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1
    print("derived files written:", n)


if __name__ == "__main__":
    main()
