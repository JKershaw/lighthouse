#!/usr/bin/env python3
"""LH062: the tallies and the within-study arithmetic quoted in LH062.md (record 0.1, 27 November 2026).

Reads only retained files in this directory: claims.csv, fetchlog.csv and searches.md. Makes no request.
Counts claims by stream, class, vendor label, notification status, outcome and unit; checks the brief's stop
gate against searches.md and fetchlog.csv; and recomputes, within one study at a time, the shares the record
quotes beside the authors' own counts. Nothing is pooled, averaged or ranked across studies or units.
Each figure used below is asserted to appear verbatim in its claim's figure field, so a change to claims.csv
that removes it stops the script.

Run: python3 -I studies/LH062/tally.py   (output kept in tally-output.txt)
"""
import collections, csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
claims = list(csv.DictReader(open(os.path.join(HERE, "claims.csv"), encoding="utf-8")))
fetch = list(csv.DictReader(open(os.path.join(HERE, "fetchlog.csv"), encoding="utf-8")))
searches = open(os.path.join(HERE, "searches.md"), encoding="utf-8").read()

print("== Claims")
print("total claims:", len(claims))
print("-- by document (from the claim id):", dict(collections.Counter(r["claim_id"].split("-")[1] for r in claims)))
for field in ["stream", "doc", "class", "vendor_label", "prompt", "outcome", "unit", "design"]:
    print(f"-- by {field} (stream, value): count")
    c = collections.Counter((r["stream"], r[field] or "(blank)") for r in claims)
    for (s, v), n in sorted(c.items()):
        print(f"   {s} | {v}: {n}")

print("\n== Unit and outcome groups (stream, unit, outcome family): claim ids")
def fam(o):
    o = o.lower()
    f = []
    if "exposed" in o:
        f.append("still exposed")
    if "valid" in o:
        f.append("still valid")
    return f
groups = collections.defaultdict(list)
for r in claims:
    for f in fam(r["outcome"]):
        groups[(r["stream"], r["unit"], f)].append(r["claim_id"])
for k, v in sorted(groups.items()):
    docs = sorted({x.split("-")[1] for x in v})
    print(f"   {k[0]} | {k[1]} | {k[2]}: {', '.join(v)}  (documents: {', '.join(docs)})")
multi = [k for k, v in groups.items() if len({x.split('-')[1] for x in v}) > 1]
print("groups spanning more than one document:", len(multi), multi)

print("\n== Stop gate (brief, 'Dates, stopping and the stop gate')")
q = re.findall(r"^## (Q[1-6]), (\S+)$", searches, flags=re.M)
print("query entries in searches.md:", len(q), q)
gets = [r for r in fetch if r["kind"] == "document" and r["status"]]
refused = [r for r in fetch if "robots refusal" in r["outcome"]]
walls = [r for r in gets if r["status"] != "200"]
print("document GETs (a status recorded):", len(gets), "of 12; HTTP 200:", sum(r["status"] == "200" for r in gets))
print("walls among GETs (non-200):", len(walls))
print("robots refusals before any request (no GET used):", len(refused))
print("fetchlog rows:", len(fetch), "; candidates in the register: 9 (searches.md)")
print("latest fetchlog utc:", max(r["utc"] for r in fetch), "; any after 2026-12-14:",
      any(r["utc"][:10] > "2026-12-14" for r in fetch))
print("walls plus refusals:", len(walls) + len(refused), "; more than four:", len(walls) + len(refused) > 4)

print("\n== Within-study arithmetic (Lighthouse's, from the authors' counts; one study at a time)")
fig = {r["claim_id"]: r["figure"] for r in claims}
pop = {r["claim_id"]: r["population_n"] for r in claims}
def need(cid, *texts):
    for t in texts:
        assert t in fig[cid] or t in pop[cid], (cid, t)
need("V-A07-3", "1,405", "706")
need("V-A07-4", "1,175", "865")
need("V-A07-5", "706", "1,019", "865", "660")
print("A07, after notification, still exposed (credentials, day 0 = 1,405):")
for d, n in [(14, 706), (172, 1019)]:
    print(f"   day {d}: {n} of 1405 = {100*n/1405:.1f}% of day 0")
print("A07, after notification, still valid as checked (credentials, day 0 = 1,175):")
for d, n in [(14, 865), (172, 660)]:
    print(f"   day {d}: {n} of 1175 = {100*n/1175:.1f}% of day 0")
need("V-B1-1", "36,293", "36,425")
print(f"B1, still valid March 2023: 36293 of 36425 = {100*36293/36425:.2f}%")
need("V-B1-3", "18,332")
print(f"B1, July 2023: 18332 of 110993 analysed = {100*18332/110993:.2f}% (denominator not stated by the authors)")
need("V-B1-2", "83", "4", "3", "9")
print("B1 sample of 100: 83 + 4 + 3 + 9 =", 83 + 4 + 3 + 9, "(one further app recorded separately)")
need("V-A02-1", "81%", "19%")
print("A02: 19% removed and 81% not removed sum to", 19 + 81)
need("W-W6-2", "28.2%", "71.8%")
print("W6: 28.2% + 71.8% =", round(28.2 + 71.8, 1))
