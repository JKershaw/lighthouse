#!/usr/bin/env python3
"""LH061: decide, per document read, whether its body may be kept, and write the derived record otherwise.

Written 25 November 2026 for the queue row LH061-search-read. The brief keeps a body only where the
document states a licence that allows redistribution or states that it is in the public domain, and
then only through save_body (keep_decision: robots.txt and the page's own reservation). Every other
document read gets a derived file through write_derived: URL, read time, status, SHA-256 of the bytes
received, the facts the study uses and short attributed quotations. The facts come from a JSON spec
the reading agent wrote after reading (argument --spec), one entry per document id, with
"licence_allows_keeping": true only where the document's own text states such a licence.

Reads the bytes fetch.py left in the working folder (--work) and updates the body_kept column of
studies/LH061/fetchlog.csv. Nothing downloaded is executed.

Usage: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH061/keep.py --work <dir> --spec <facts.json>
"""
import argparse, csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from lh_fetch import save_body, write_derived  # noqa: E402

LOG = os.path.join(HERE, "fetchlog.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--spec", required=True)
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    os.makedirs(os.path.join(HERE, "derived"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "bodies"), exist_ok=True)
    decided = {}
    for did, ent in spec.items():
        meta = json.load(open(os.path.join(a.work, did + ".meta.json")))
        body = open(os.path.join(a.work, did + ".bin"), "rb").read()
        kept, why = False, "no licence allowing redistribution, and no public-domain statement, found in the document read"
        if ent.get("licence_allows_keeping") and body[:5] == b"%PDF-":
            # Added 25 November 2026 after the first run kept A07's PDF: its compressed streams held author
            # email addresses that redact_bytes cannot reach, so no PDF body is kept (AGENTS.md: emails withheld).
            why = ("the licence (" + ent.get("licence_statement", "") + ") and keep_decision allowed keeping, but a PDF's "
                   "compressed streams can hold email addresses that redact_bytes cannot reach, so the body is not kept")
        elif ent.get("licence_allows_keeping"):
            ext = ".html"
            kept, why = save_body(os.path.join(HERE, "bodies", did + ext), body, meta["final_url"],
                                  meta.get("headers"), access="oneoff")
            why = ("yes: " if kept else "") + str(why) + "; licence: " + ent.get("licence_statement", "")
        common = dict(read_utc=meta["read_utc"], final_url=meta["final_url"], http_status=meta["status"],
                      content_type=meta["content_type"], bytes=meta["bytes"], sha256=meta["sha256"],
                      used_for="LH061 search-and-read row, 25 November 2026: inclusion decision and claims (claims.csv)")
        if kept:
            with open(os.path.join(HERE, "derived", did + ".json"), "w", encoding="utf-8") as f:
                json.dump({"url": meta["url"], **common, "body_kept": why, "extracted": ent["facts"]}, f,
                          indent=1, ensure_ascii=False)
                f.write("\n")
            decided[did] = why
        else:
            write_derived(os.path.join(HERE, "derived", did + ".json"), meta["url"], why, ent["facts"], **common)
            decided[did] = "no: " + why
        print(did, decided[did][:160])
    rows = list(csv.DictReader(open(LOG)))
    for r in rows:
        if r["id"] in decided and r["outcome"] == "ok":
            r["body_kept"] = decided[r["id"]][:300]
    with open(LOG, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
