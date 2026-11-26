"""LH061 tally: counts of claims by class, setting, vendor and data, per part and
per document, and counts of reads from the fetch log. Reads only claims.csv and
fetchlog.csv in the study directory. No figure is combined across parts.

Run from the repository root:
    python3 -I studies/LH061/scripts/tally.py studies/LH061 > studies/LH061/scripts/tally-output.txt
"""
import csv
import sys
from collections import Counter, OrderedDict
from pathlib import Path

CLASSES = ["measured outcome", "self-reported", "modelled", "asserted"]


def data_label(value):
    v = value.strip().lower()
    for key in ("yes", "partly", "no", "not applicable"):
        if v.startswith(key):
            return key
    return "other: " + value


def main(study):
    study = Path(study)
    with open(study / "claims.csv", newline="", encoding="utf-8") as f:
        claims = list(csv.DictReader(f))
    with open(study / "fetchlog.csv", newline="", encoding="utf-8") as f:
        fetches = list(csv.DictReader(f))

    print("LH061 tally, from claims.csv and fetchlog.csv")
    print("claims in file:", len(claims))
    for part in ("A", "B"):
        rows = [r for r in claims if r["part"] == part]
        print()
        print(f"== Part {part}: {len(rows)} claims")
        cls = Counter(r["class"] for r in rows)
        print("by class:", ", ".join(f"{c} {cls.get(c, 0)}" for c in CLASSES))
        unknown = set(cls) - set(CLASSES)
        if unknown:
            print("UNKNOWN CLASSES:", unknown)
        print("by setting:", dict(Counter(r["setting"] for r in rows)))
        print("vendor yes:", sum(r["vendor"] == "yes" for r in rows))
        print("data public:", dict(Counter(data_label(r["data_public"]) for r in rows)))
        meas = [r for r in rows if r["class"] == "measured outcome"]
        print(f"measured claims: {len(meas)}; of these vendor {sum(r['vendor']=='yes' for r in meas)},"
              f" laboratory {sum(r['setting']=='laboratory' for r in meas)},"
              f" field {sum(r['setting']=='field' for r in meas)},"
              f" exercise {sum(r['setting']=='exercise' for r in meas)}")
        print("measured claims, data public:", dict(Counter(data_label(r["data_public"]) for r in meas)))
        docs = OrderedDict()
        for r in rows:
            docs.setdefault(r["document"], Counter())[r["class"]] += 1
        print("per document (class counts; documents are not pooled):")
        for d, c in docs.items():
            print(f"  {d}: total {sum(c.values())}; " + ", ".join(f"{k} {c.get(k, 0)}" for k in CLASSES))
        if part == "A":
            print("per claim, direction as recorded:")
            for r in rows:
                print(f"  {r['claim_id']}: {r['class']} | {r['setting']} | vendor {r['vendor']} | {r['direction']}")

    print()
    print("== Fetch log")
    for kind in ("document", "locator"):
        rows = [r for r in fetches if r["kind"] == kind]
        requested = [r for r in rows if r["status"].strip()]
        refused = [r for r in rows if r["outcome"].startswith("robots refusal (not requested)")]
        print(f"{kind}: {len(rows)} rows; requests with a status {len(requested)};"
              f" refused before any request {len(refused)}; other {len(rows)-len(requested)-len(refused)}")
        print("  status counts:", dict(Counter(r["status"] or "(none)" for r in rows)))
        for part in ("A", "B"):
            pr = [r for r in requested if r["part"] == part]
            ok = sum(r["status"] == "200" for r in pr)
            print(f"  part {part}: requests {len(pr)}, HTTP 200 {ok}, other status {len(pr)-ok},"
                  f" refused {sum(r['part']==part for r in refused)}")
    docs = [r for r in fetches if r["kind"] == "document"]
    walls = [r for r in docs if r["status"].strip() and r["status"] != "200"]
    refused = [r for r in docs if r["outcome"].startswith("robots refusal")]
    print(f"document GETs used: {sum(1 for r in docs if r['status'].strip())} of 20;"
          f" unused {20 - sum(1 for r in docs if r['status'].strip())}")
    print(f"walls among document GETs (non-200): {len(walls)} ({', '.join(r['id'] for r in walls)})")
    print(f"robots refusals of documents, no GET: {len(refused)} ({', '.join(r['id'] for r in refused)})")
    print(f"walls plus refusals: {len(walls) + len(refused)}; brief's threshold: more than 6")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "studies/LH061")
