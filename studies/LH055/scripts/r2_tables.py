#!/usr/bin/env python3
"""LH055 round 2 checks and tables, offline, standard library only.

Usage (from the repository root):
  python3 -I studies/LH055/scripts/r2_tables.py > studies/LH055/scripts/r2_tables_output.txt

1. Recompute the SHA-256 of each round 2 retained body and compare it with the fetch log, or, where
   redactions.json has an entry, check the fetch log against its 'before' hash and the file against
   its 'after' hashes (body and text).
2. Check that every round 2 passage in claims.csv (sources S08 to S14) occurs verbatim (whitespace
   normalised) in the retained text within the stated line range, carries no withheld marker, and
   that every claim has a campaign.
3. Check that every claim id cited in links_r2.csv exists, belongs to that source, and that each
   row has a campaign; no duplicate source/link rows.
4. Count round 2 link statuses by source, by link, and by whether they bear on Amazon's Campaign 1.
5. Absence and provenance checks the record relies on, and clock arithmetic.
6. Budget counts against the brief's round 2 and pilot limits.
"""
import csv, datetime, gzip, hashlib, json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
LABEL = "round2-2026-11-17T2124Z"
DATA = os.path.join(STUDY, "data", LABEL)
BASE = os.path.join(STUDY, "data", "baseline-2026-11-17T2030Z")
R2 = {"S08", "S09", "S10", "S11", "S12", "S13", "S14"}
FILE = {"S08": "R01", "S09": "R02", "S10": "R03", "S11": "R04", "S12": "R05", "S13": "R06", "S14": "R07"}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def text(path):
    return open(path, encoding="utf-8").read()


def main():
    ok = True
    red = json.load(open(os.path.join(DATA, "redactions.json")))
    _p2 = os.path.join(DATA, "withholding_pass2.json")
    PASS2 = json.load(open(_p2)) if os.path.exists(_p2) else {}
    print("== 1. round 2 retained hashes")
    log = [json.loads(l) for l in open(os.path.join(DATA, "fetch_log.jsonl"))]
    for r in log:
        if "retained_body" not in r:
            print(f"{r['id']}: no body retained (outcome {r['outcome']}, status {r['status']})")
            continue
        body = gzip.open(os.path.join(DATA, r["retained_body"])).read()
        p2 = PASS2.get(r["id"], {})  # second withholding pass, scripts/withhold_pass2.py
        if r["id"] in red:
            e = red[r["id"]]
            t = open(os.path.join(DATA, r["retained_text"]), "rb").read()
            if p2:
                same = (r["retained_sha256"] == e["body_sha256_before"] and e["body_sha256_after"] == p2["body"]["sha256_before"]
                        and sha(body) == p2["body"]["sha256_after"] and e["text_sha256_after"] == p2["text"]["sha256_before"]
                        and sha(t) == p2["text"]["sha256_after"])
            else:
                same = (r["retained_sha256"] == e["body_sha256_before"] and sha(body) == e["body_sha256_after"]
                        and sha(t) == e["text_sha256_after"])
            print(f"{r['id']}: {'match' if same else 'DIFFERS'} (fetch log = redactions 'before'; body and text = 'after'; personal details withheld after collection)")
        elif p2.get("body"):
            same = r["retained_sha256"] == p2["body"]["sha256_before"] and sha(body) == p2["body"]["sha256_after"]
            print(f"{r['id']}: {'match' if same else 'DIFFERS'}")
        else:
            same = sha(body) == r["retained_sha256"]
            print(f"{r['id']}: {'match' if same else 'DIFFERS'}")
        ok &= same

    print("\n== 2. round 2 claim passages in retained text")
    claims = list(csv.DictReader(open(os.path.join(STUDY, "claims.csv"))))
    ids = {c["claim_id"]: c["source_id"] for c in claims}
    r2 = [c for c in claims if c["source_id"] in R2]
    bad = 0
    for c in r2:
        m = re.match(re.escape(LABEL) + r"/text/(R\d+)\.txt lines (\d+)(?:-(\d+))?$", c["passage_locator"])
        if not m or m.group(1) != FILE[c["source_id"]]:
            print(f"{c['claim_id']}: bad locator {c['passage_locator']}")
            bad += 1
            continue
        a, b = int(m.group(2)), int(m.group(3) or m.group(2))
        lines = text(os.path.join(DATA, "text", m.group(1) + ".txt")).split("\n")
        if norm(c["passage"]) not in norm(" ".join(lines[a - 1:b])):
            print(f"{c['claim_id']}: passage NOT found at {c['passage_locator']}")
            bad += 1
        if "withheld" in c["passage"]:
            print(f"{c['claim_id']}: passage contains a withheld marker")
            bad += 1
        if not c["campaign"].strip():
            print(f"{c['claim_id']}: no campaign")
            bad += 1
    nums = sorted(int(c["claim_id"][-3:]) for c in r2)
    print(f"{len(r2)} round 2 claims checked (C{nums[0]} to C{nums[-1]}); {bad} problems; claims.csv holds {len(claims)} rows in all")
    print("round 2 claims by source: " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(c['source_id'] for c in r2).items())))
    basis = Counter(b for c in r2 for b in c["basis"].split("; "))
    print("round 2 basis labels (a claim may carry several):")
    for k, v in basis.most_common():
        print(f"  {v:3d}  {k}")
    ok &= bad == 0

    print("\n== 3. links_r2.csv references")
    links = list(csv.DictReader(open(os.path.join(STUDY, "links_r2.csv"))))
    bad = 0
    for l in links:
        if not l["campaign"].strip() or not l["bears_on_amazon_campaign1"].strip():
            print(f"{l['source_id']} {l['link_id']}: campaign or Campaign 1 field empty")
            bad += 1
        for cid in [x.strip() for x in l["claim_ids"].split(";") if x.strip()]:
            if cid not in ids:
                print(f"{l['source_id']} {l['link_id']}: unknown claim {cid}")
                bad += 1
            elif ids[cid] != l["source_id"]:
                print(f"{l['source_id']} {l['link_id']}: claim {cid} belongs to {ids[cid]}")
                bad += 1
    dup = [p for p, n in Counter((l["source_id"], l["link_id"]) for l in links).items() if n > 1]
    if dup:
        print("duplicate source/link rows:", dup)
        bad += len(dup)
    r1 = list(csv.DictReader(open(os.path.join(STUDY, "links.csv"))))
    print(f"{len(links)} round 2 link rows checked; {bad} problems; round 1 links.csv still holds {len(r1)} rows")
    ok &= bad == 0

    print("\n== 4. round 2 link statuses (counts of this record's codings, not of events)")
    statuses = ["supported by the stated evidence", "claimed without sufficient disclosed support", "contradicted", "unknown"]
    short = {s: s.split()[0] for s in statuses}
    order = ["L1", "L2", "L3", "L4", "L5", "L6"]
    grid = defaultdict(dict)
    for l in links:
        grid[l["source_id"]][l["link_id"]] = short[l["status"]]
    print("source  " + "  ".join(f"{k:>9}" for k in order))
    for s in sorted(grid):
        print(f"{s:6}  " + "  ".join(f"{grid[s].get(k, '-'):>9}" for k in order))
    cnt = Counter(l["status"] for l in links)
    print("all round 2 rows: " + "; ".join(f"{short[s]} {cnt.get(s, 0)}" for s in statuses) + f" (of {len(links)})")
    for label, keep in [("rows bearing on Amazon's Campaign 1 (repetition only)", lambda l: l["bears_on_amazon_campaign1"].startswith("repetition")),
                        ("rows from other campaigns or design readings", lambda l: not l["bears_on_amazon_campaign1"].startswith("repetition"))]:
        c2 = Counter(l["status"] for l in links if keep(l))
        print(f"{label}: " + "; ".join(f"{short[s]} {c2.get(s, 0)}" for s in statuses) + f" (of {sum(c2.values())})")
    print("supported or contradicted codings bearing on Campaign 1: "
          + str(sum(1 for l in links if l["status"] in statuses[0::2] and not l["bears_on_amazon_campaign1"].startswith("no"))))
    print("round 1 Amazon (S02) codings, unchanged: " + "; ".join(f"{l['link_id']} {short[l['status']]}" for l in r1 if l["source_id"] == "S02"))

    print("\n== 5. absence, provenance and clocks")
    checks = []
    r04 = text(os.path.join(DATA, "text", "R04.txt")).lower()
    for term in ["self-sustain", "stolen key", "inference", "gateway", "loop"]:
        checks.append((f"Equixly (R04) text lacks '{term}'", term not in r04))
    r06 = text(os.path.join(DATA, "text", "R06.txt")).lower()
    for term in ["amazon", "madpot", "self-sustain", "inference", "gateway"]:
        checks.append((f"Talos (R06) text lacks '{term}'", term not in r06))
    s02t = norm(text(os.path.join(BASE, "text", "S02.txt")))
    s02b = gzip.open(os.path.join(BASE, "bodies", "S02.raw.gz")).read().decode("utf-8", "replace")
    checks.append(("The Stack's quoted 'Each call shipped' is absent from Amazon's text and body", "shipped" not in s02t and "shipped" not in s02b))
    r02 = text(os.path.join(DATA, "text", "R02.txt")).lower()
    for term in ["gateway", "llm/pool", "key pool"]:
        checks.append((f"GitGuardian (R02) text lacks '{term}'", term not in r02))
    r03 = text(os.path.join(DATA, "text", "R03.txt"))
    checks.append(("CrowdStrike (R03) text lacks 'bought' and 'purchas'", "bought" not in r03.lower() and "purchas" not in r03.lower()))
    r07 = text(os.path.join(DATA, "text", "R07.txt")).lower()
    for term in ["bedrock", "sagemaker", "invokemodel"]:
        checks.append((f"Datadog (R07) text lacks '{term}'", term not in r07))
    for name, res in checks:
        print(f"{'yes' if res else 'NO '}  {name}")
        ok &= res
    amazon = datetime.datetime.fromisoformat("2026-11-13T13:26:42-07:00")
    talos = datetime.datetime.fromisoformat("2026-11-13T20:57:13+00:00")
    ms_mod = datetime.datetime.fromisoformat("2026-11-10T00:47:23+00:00")
    print(f"Amazon post published {amazon.astimezone(datetime.timezone.utc).isoformat()}; Talos published {talos.isoformat()}, {(talos - amazon).total_seconds() / 60:.1f} minutes later")
    print(f"Microsoft 5 November report last modified {ms_mod.isoformat()}, {(amazon - ms_mod).total_seconds() / 86400:.2f} days before Amazon's post")

    print("\n== 6. budget")
    q = len(re.findall(r"^## Q\d+", text(os.path.join(DATA, "searches", "queries.md")), re.M))
    q1 = len(re.findall(r"^## Q\d+", text(os.path.join(BASE, "searches", "queries.md")), re.M))
    print(f"round 2 queries: {q} of 4; pilot queries: {q + q1} of 10")
    n = len({r["id"] for r in log})
    nb = len({json.loads(l)["id"] for l in open(os.path.join(BASE, "fetch_log.jsonl"))})
    print(f"round 2 documents requested: {n} of 8 (all received); pilot distinct documents requested: {n + nb} of 24 (baseline {nb}, of which 6 retained)")
    print(f"round 2 bytes received: {sum(r['received_bytes'] for r in log):,}; content GETs: {len(log)}; first start {min(r['started'] for r in log)}, last finish {max(r['finished'] for r in log)}")
    print("\nall checks passed" if ok else "\nSOME CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
