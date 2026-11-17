#!/usr/bin/env python3
"""LH055 round 1 checks and tables, offline, standard library only.

Usage (from the repository root):
  python3 -I studies/LH055/scripts/r1_tables.py > studies/LH055/scripts/r1_tables_output.txt

1. Recompute the SHA-256 of each retained body and compare it with the fetch log.
2. Check that every passage in claims.csv occurs verbatim (whitespace normalised) in the
   retained text within the stated line range.
3. Check that every claim id cited in links.csv exists in claims.csv and belongs to that source.
4. Count link statuses by source and by link (descriptive counts of this record's codings).
5. Recompute the few derived figures the record states.
"""
import csv, gzip, hashlib, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, "data", "baseline-2026-11-17T2030Z")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def main():
    ok = True
    print("== 1. retained body hashes against fetch_log.jsonl")
    for line in open(os.path.join(DATA, "fetch_log.jsonl")):
        r = json.loads(line)
        if "retained_body" not in r:
            print(f"{r['id']}: no body retained (outcome {r['outcome']}, status {r['status']})")
            continue
        h = hashlib.sha256(gzip.open(os.path.join(DATA, r["retained_body"])).read()).hexdigest()
        same = h == r["retained_sha256"]
        ok &= same
        print(f"{r['id']}: {'match' if same else 'DIFFERS'}")

    print("\n== 2. claim passages in retained text")
    claims = list(csv.DictReader(open(os.path.join(STUDY, "claims.csv"))))
    texts = {}
    bad = 0
    for c in claims:
        m = re.match(r"text/(S\d+)\.txt lines (\d+)(?:-(\d+))?$", c["passage_locator"])
        if not m or m.group(1) != c["source_id"]:
            print(f"{c['claim_id']}: bad locator {c['passage_locator']}")
            bad += 1
            continue
        sid, a = m.group(1), int(m.group(2))
        b = int(m.group(3) or a)
        if sid not in texts:
            texts[sid] = open(os.path.join(DATA, "text", sid + ".txt"), encoding="utf-8").read().split("\n")
        window = norm(" ".join(texts[sid][a - 1:b]))
        if norm(c["passage"]) not in window:
            print(f"{c['claim_id']}: passage NOT found in {sid} lines {a}-{b}: {c['passage']!r}")
            bad += 1
        if "withheld" in c["passage"]:
            print(f"{c['claim_id']}: passage contains a withheld marker")
            bad += 1
    ok &= bad == 0
    print(f"{len(claims)} claims checked; {bad} problems")
    by_src = Counter(c["source_id"] for c in claims)
    print("claims by source: " + ", ".join(f"{k} {v}" for k, v in sorted(by_src.items())))
    basis = Counter()
    for c in claims:
        for b in c["basis"].split("; "):
            basis[b] += 1
    print("basis labels (a claim may carry several):")
    for k, v in basis.most_common():
        print(f"  {v:3d}  {k}")

    print("\n== 3. links.csv references")
    links = list(csv.DictReader(open(os.path.join(STUDY, "links.csv"))))
    ids = {c["claim_id"]: c["source_id"] for c in claims}
    bad = 0
    for l in links:
        for cid in [x.strip() for x in l["claim_ids"].split(";") if x.strip()]:
            if cid not in ids:
                print(f"{l['source_id']} {l['link_id']}: unknown claim {cid}")
                bad += 1
            elif ids[cid] != l["source_id"]:
                print(f"{l['source_id']} {l['link_id']}: claim {cid} belongs to {ids[cid]}")
                bad += 1
    pairs = Counter((l["source_id"], l["link_id"]) for l in links)
    dup = [p for p, n in pairs.items() if n > 1]
    if dup:
        print("duplicate source/link rows:", dup)
        bad += len(dup)
    ok &= bad == 0
    print(f"{len(links)} link rows checked; {bad} problems")

    print("\n== 4. link statuses (counts of this record's codings, not of events)")
    statuses = ["supported by the stated evidence", "claimed without sufficient disclosed support", "contradicted", "unknown"]
    short = {s: s.split()[0] for s in statuses}
    order = ["L1", "L2", "L3", "L4", "L5", "L6"]
    grid = defaultdict(dict)
    for l in links:
        grid[l["source_id"]][l["link_id"]] = short[l["status"]]
    print("source  " + "  ".join(f"{k:>9}" for k in order))
    for s in sorted(grid):
        print(f"{s:6}  " + "  ".join(f"{grid[s].get(k, '-'):>9}" for k in order))
    for label, keep in [("all 7 sources", lambda s: True),
                        ("ARTEX sources (S01 to S05, S07)", lambda s: s != "S06"),
                        ("ARTEX sources that were read (S01 to S04, S07)", lambda s: s not in ("S05", "S06"))]:
        cnt = Counter(l["status"] for l in links if keep(l["source_id"]))
        print(f"{label}: " + "; ".join(f"{short[s]} {cnt.get(s, 0)}" for s in statuses) + f" (of {sum(cnt.values())} rows)")
    print("by link, over all sources:")
    for k in order:
        cnt = Counter(l["status"] for l in links if l["link_id"] == k)
        print(f"  {k}: " + "; ".join(f"{short[s]} {cnt.get(s, 0)}" for s in statuses))

    print("\n== 5. derived figures")
    print(f"Censys: 1465 - 650 = {1465 - 650} (page says roughly 815)")
    print(f"Censys: 650 / 1465 = {650 / 1465:.3f} (page says about 44%)")
    print(f"Censys: 155 / 1465 = {155 / 1465:.4f} (page says 10.6%)")
    print(f"Censys: 493 + 157 = {493 + 157} (PEG Tech plus Yancy, page says about 650)")
    print(f"Censys: 19 + 18 = {19 + 18} of 43 gateway hosts named by product; {43 - 37} not broken down")
    print(f"Censys: six named countries sum {726 + 387 + 177 + 51 + 38 + 21} of 1,465 hosts (the rest not listed)")
    print(f"SANS: roughly 379 - 341 = {379 - 341} channels left after the agent's test (SANS does not state this)")
    s02 = open(os.path.join(DATA, "text", "S02.txt"), encoding="utf-8").read().split("\n")[114:125]
    for camp in ("Campaign 1", "Campaign 2"):
        rows = [re.findall(r"(\d{4}-\d{2}-\d{2}) (\d{4}-\d{2}-\d{2}) " + camp, l) for l in s02]
        rows = [r[0] for r in rows if r]
        print(f"Amazon {camp} indicators: {len(rows)} rows, first seen {min(a for a, b in rows)}, last seen {max(b for a, b in rows)}")
    s03 = open(os.path.join(DATA, "text", "S03.txt"), encoding="utf-8").read().split("\n")[140:148]
    rows = [re.findall(r"(\d{4}-\d{2}-\d{2})Active as of (\d{4}-\d{2}-\d{2})", l)[0] for l in s03]
    print(f"Microsoft indicators: {len(rows)} rows, first seen {min(a for a, b in rows)} to {max(a for a, b in rows)}, active as of {sorted(set(b for a, b in rows))}")
    print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
