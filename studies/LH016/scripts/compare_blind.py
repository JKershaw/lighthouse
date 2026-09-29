"""LH016: compare the second coder's codes with the first coder's.

Reads data/blind_codes.csv (sample_no, tier, type, direction, as the second
coder wrote them), data/blind_key.csv and data/changes.csv. Reports raw
agreement and Cohen's kappa on material or not (A, B or C against N) and on
the four tiers, agreement on type and direction where both coders call a
change material, and every disagreement. Writes data/blind_compare.txt.

Run from studies/LH016: python3 scripts/compare_blind.py
"""
import csv
from collections import Counter


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


first = {r["id"]: r for r in csv.DictReader(open("data/changes.csv", newline=""))}
key = {r["sample_no"]: r["id"] for r in csv.DictReader(open("data/blind_key.csv", newline=""))}
second = {r["sample_no"]: r for r in csv.DictReader(open("data/blind_codes.csv", newline=""))}

out = []
tiers, material, types, dirs, disagree = [], [], [], [], []
for no in sorted(key, key=int):
    a = first[key[no]]
    b = second.get(no)
    if b is None:
        out.append(f"sample {no} ({key[no]}): not coded by the second coder")
        continue
    ta, tb = a["tier"].strip().upper(), b["tier"].strip().upper()
    tiers.append((ta, tb))
    material.append((ta != "N", tb != "N"))
    if ta != "N" and tb != "N":
        types.append((a["type"].strip().lower(), b["type"].strip().lower()))
        dirs.append((a["direction"].strip().lower(), b["direction"].strip().lower()))
    if ta != tb or (ta != "N" and tb != "N" and a["type"].strip().lower() != b["type"].strip().lower()):
        disagree.append(f"sample {no} ({key[no]}, step {a['step']}): first {ta}/{a['type']}/{a['direction']}, "
                        f"second {tb}/{b['type']}/{b['direction']}")

po, k = kappa(material)
out.append(f"coded by both: {len(tiers)}")
out.append(f"material or not: agreement {po:.3f}, Cohen's kappa {k:.3f}")
po, k = kappa(tiers)
out.append(f"tier (A, B, C, N): agreement {po:.3f}, Cohen's kappa {k:.3f}")
out.append("first coder's tiers: " + str(dict(Counter(a for a, _ in tiers))))
out.append("second coder's tiers: " + str(dict(Counter(b for _, b in tiers))))
if types:
    out.append(f"type, where both call it material: agreement {sum(a == b for a, b in types)} of {len(types)}")
    out.append(f"direction, where both call it material: agreement {sum(a == b for a, b in dirs)} of {len(dirs)}")
out.append("")
out.append("disagreements on tier, or on type where both call it material:")
out.extend(disagree or ["none"])
text = "\n".join(out)
open("data/blind_compare.txt", "w").write(text + "\n")
print(text)
