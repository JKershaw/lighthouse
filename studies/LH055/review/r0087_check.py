#!/usr/bin/env python3
"""Independent reproduction for review R-0087 of LH055 round 1 (record 0.1, commit cb6fab5).

Written by the reviewer without reusing r1_tables.py. Offline, standard library only.
Replay from the repository root:
  python3 -I studies/LH055/review/r0087_check.py > studies/LH055/review/r0087_check_output.txt
"""
import csv, gzip, hashlib, json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data", "baseline-2026-11-17T2030Z")

def lines(sid):
    return open(os.path.join(D, "text", sid + ".txt"), encoding="utf-8").read().split("\n")

def squash(s):
    return " ".join(s.split())

print("== A. fetch log: bytes, hashes, timings")
log = [json.loads(l) for l in open(os.path.join(D, "fetch_log.jsonl"))]
tot = 0
for r in log:
    tot += r["received_bytes"]
    line = f"{r['id']} status {r['status']} bytes {r['received_bytes']} start {r['started']} finish {r['finished']}"
    if "retained_body" in r:
        raw = gzip.open(os.path.join(D, r["retained_body"])).read()
        h = hashlib.sha256(raw).hexdigest()
        line += f" | retained-body sha256 {'= retained_sha256' if h == r['retained_sha256'] else 'MISMATCH'}"
        line += f" | received==retained hash: {r['received_sha256'] == r['retained_sha256']}"
        line += f" | retained bytes {len(raw)}"
    print(line)
print(f"sum of received_bytes over all 7 GETs (incl. the 429 body): {tot:,}")
print(f"sum over the six 200 responses only: {sum(r['received_bytes'] for r in log if r['status'] == 200):,}")
print(f"robots decision files: {len(os.listdir(os.path.join(D, 'robots')))}")

print("\n== B. claims.csv passages and locators (independent check, exact substring after whitespace squash)")
claims = list(csv.DictReader(open(os.path.join(ROOT, "claims.csv"), encoding="utf-8")))
probs = 0
for c in claims:
    m = re.fullmatch(r"text/(S\d\d)\.txt lines (\d+)(?:-(\d+))?", c["passage_locator"])
    sid, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
    assert sid == c["source_id"]
    seg = squash(" ".join(lines(sid)[a-1:b]))
    if squash(c["passage"]) not in seg:
        probs += 1
        print("NOT FOUND", c["claim_id"])
    # also: is the passage unique in the whole text? (locator ambiguity)
    whole = squash(" ".join(lines(sid)))
    n = whole.count(squash(c["passage"]))
    if n != 1:
        print(f"note: {c['claim_id']} passage occurs {n} times in {sid}")
print(f"{len(claims)} claims; {probs} passages not found at their locators")
ids = [c["claim_id"] for c in claims]
print(f"unique ids: {len(set(ids))}; first {min(ids)}; last {max(ids)}")
print("by source:", dict(sorted(Counter(c["source_id"] for c in claims).items())))
bc = Counter(b.strip() for c in claims for b in c["basis"].split(";"))
print("basis labels:", dict(bc.most_common()))

print("\n== C. links.csv tallies")
links = list(csv.DictReader(open(os.path.join(ROOT, "links.csv"), encoding="utf-8")))
print("rows:", len(links))
def tally(rows):
    t = Counter(r["status"] for r in rows)
    return {k.split()[0]: t.get(k, 0) for k in ["supported by the stated evidence", "claimed without sufficient disclosed support", "contradicted", "unknown"]}
print("all:", tally(links))
print("ARTEX incl. unread S05 (exclude S06):", tally([r for r in links if r["source_id"] != "S06"]))
print("ARTEX read (S01-S04, S07):", tally([r for r in links if r["source_id"] in ("S01", "S02", "S03", "S04", "S07")]))
print("S02 only:", tally([r for r in links if r["source_id"] == "S02"]))
print("S06 only:", tally([r for r in links if r["source_id"] == "S06"]))
idset = {c["claim_id"]: c["source_id"] for c in claims}
bad = [(r["source_id"], r["link_id"], x) for r in links for x in re.split(r";\s*", r["claim_ids"]) if x and idset.get(x) != r["source_id"]]
print("link claim-id problems:", bad)

print("\n== D. Censys figures, read from the text")
s4 = squash(" ".join(lines("S04")))
for pat in [r"As of November \d, 2026, Censys observed [\d,]+ hosts", r"As of November \d, 2026, this matches [\d,]+ hosts",
            r"About \d+ sit in two blocks", r"roughly \d+ distinct-looking", r"\d+ ARTEX hosts \([\d.]+%\)",
            r"PEG Tech \(AS54600\): \d+ hosts", r"Yancy Limited \(AS138415\): \d+ hosts", r"about \d+% of hosts",
            r"\d+ ARTEX hosts also run self-hosted LLM gateway or reseller software, mainly CLIProxyAPI \(\d+\) and New API \(\d+\)",
            r"\(([\d,]+) endpoints\)", r"Between November 3 and November 5, \d+ closed and \d+ new", r"Censys observed \d+ open directories"]:
    print(" ", re.findall(pat, s4))
peg, yan, tot_h = 493, 157, 1465
print(f"  493+157={peg+yan}; 1465-650={tot_h-650}; 650/1465={650/1465:.4f}; 155/1465={155/1465:.4f}; 43-(19+18)={43-37}")
ctry = re.search(r"Top countries(.*?)Console language", s4).group(1)
nums = [int(x.replace(",", "")) for x in re.findall(r"(\d[\d,]*)", ctry)]
print(f"  country figures {nums}, sum {sum(nums)}")

print("\n== E. SANS channel arithmetic")
s6 = squash(" ".join(lines("S06")))
print(" ", re.findall(r"roughly \d+ upstream endpoints", s6), re.findall(r"disabled the \d+ that failed", s6), re.findall(r"approximately \d+ KB", s6))
print(f"  379-341={379-341} (derived; 'roughly 379' so the remainder is approximate); share failed {341/379:.3f}")

print("\n== F. IOC date ranges")
s2 = lines("S02")
for camp in ("Campaign 1", "Campaign 2"):
    rows = [re.search(r"(\d{4}-\d\d-\d\d) (\d{4}-\d\d-\d\d) " + camp + r"$", l) for l in s2]
    rows = [r.groups() for r in rows if r]
    print(f"  Amazon {camp}: {len(rows)} rows; first-seen min {min(r[0] for r in rows)}; last-seen max {max(r[1] for r in rows)}")
s3 = lines("S03")
rows = [re.search(r"(\d{4}-\d\d-\d\d)Active as of (\d{4}-\d\d-\d\d)", l) for l in s3]
rows = [r.groups() for r in rows if r]
print(f"  Microsoft: {len(rows)} rows; first seen {min(r[0] for r in rows)} to {max(r[0] for r in rows)}; active as of {set(r[1] for r in rows)}")

print("\n== G. FBI notes and console-count citation")
s1 = lines("S01")
start = next(i for i, l in enumerate(s1) if l.strip() == "Notes")
end = next(i for i, l in enumerate(s1) if "Reporting Notice" in l)
notes = [l for l in s1[start:end] if re.match(r"^\d+\. ", l.strip())]
print(f"  numbered notes in the Notes section: {len(notes)}; any line naming Amazon in the FLASH: {any('Amazon' in l for l in s1)}")
print("  1,600 sentence:", squash(" ".join(s1[33:36])))
print("  StepSecurity console counts:", re.findall(r"(Unit 42|Censys|BadByte|SOCRadar): ([\d,]+) hosts", squash(' '.join(lines('S07')))))

print("\n== H. Amazon caveat, exact")
for i, l in enumerate(s2, 1):
    for key in ("cannot verify", "could not be confirmed", "agents’ own descriptions", "succeeded where", "moderate confidence that ARTEX"):
        if key in l:
            j = l.find(key)
            print(f"  S02 line {i}: ...{l[max(0, j-160):j+120]}...")

print("\n== I. Passages bearing on 'every source that speaks to control' and 'agents spreading themselves'")
s7 = lines("S07")
for i, l in enumerate(s7, 1):
    for key in ("escaped", "decided by itself", "runaway", "A person only steers", "told the agents"):
        if key in l:
            j = l.find(key)
            print(f"  S07 line {i}: ...{l[max(0, j-120):j+100]}...")
