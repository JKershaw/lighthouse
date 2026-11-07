"""Reader review (notes/R-0050-lh035-map-reader.md): what kind of gap each row's
blind-spot reading names, coded by hand by the reviewer from the blind_spot field.
A reviewer's reading, not a test; one dominant kind per row.
Kinds: position = misses what does not reach, cross, answer or get reported to it;
definition = its unit is a proxy for the thing of interest (fetch vs install, PoC vs attack);
access = the fuller data are paid, vetted or private; currency = dated, stale or out of scope by design.
Run from the repository root: python3 studies/LH035/review/gap_kinds.py"""
import json
from collections import Counter
from pathlib import Path
D = Path(__file__).resolve().parent.parent
rows = {r["id"]: r for r in json.loads((D / "data/instruments.json").read_text())["rows"]}
K = {}
for i in "I01 I02 I04 I05 I06 I08 I09 I10 I12 I13 I15 I16 I18 I19 I20 I21 I23 I24 I26 I28 I30 I31 I32 I33 I37 I38 I39 I42 I45 I48".split():
    K[i] = "position"
for i in "I14 I22 I25 I27 I29 I35 I40 I43 I44 I46".split():
    K[i] = "definition"
for i in "I17 I34".split():
    K[i] = "access"
for i in "I03 I11 I36 I41 I47".split():
    K[i] = "currency"
K["I07"] = "blank"
assert set(K) == set(rows), set(rows) ^ set(K)
c = Counter(K.values())
print("rows", len(K), dict(c))
for k in ("definition", "access", "currency"):
    print(k, [(i, rows[i]["name"][:30]) for i in sorted(K) if K[i] == k])
# The seven gaps the full piece lists under "Why it matters", coded the same way.
why = {"routes as seen from most networks": "position", "the IPv6 space": "currency (scan scope chosen)",
       "a free list of which names exist": "access", "most running services without paying": "access",
       "traffic between networks generally": "position", "who downloads software": "definition",
       "the evidence behind exploitation scores": "access"}
print("Why-it-matters gaps:", Counter(v.split()[0] for v in why.values()))
