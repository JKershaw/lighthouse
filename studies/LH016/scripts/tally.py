"""LH016: tally the coded changes by the brief's measures M1 to M7.

Reads data/changes.csv (primary frame, rounds P1 to P6), data/changes_secondary.csv
(round S), data/costs.csv, data/post_hoc_readings.csv, data/research_steps.csv and,
if present, data/blind_compare.txt. Writes data/tally.txt.

Written by the driving session before any coded row was read, and run only
after the second coder's sample was drawn (scripts/draw_sample.py).

Run from studies/LH016: python3 scripts/tally.py
"""
import csv
import os
from collections import Counter, defaultdict

STEPS = ["K", "E", "B", "R1", "R2", "RC", "D"]
TIERS = ["A", "B", "C", "N"]


def rows(path):
    if not os.path.exists(path):
        return []
    return list(csv.DictReader(open(path, newline="")))


def norm(r):
    for k in ("step", "tier", "type", "direction", "improved", "post_release", "post_hoc", "round"):
        r[k] = (r.get(k) or "").strip()
    r["tier"] = r["tier"].upper()
    r["step"] = r["step"].upper()
    r["type"] = r["type"].lower()
    r["direction"] = r["direction"].lower()
    r["improved"] = r["improved"].lower()
    r["post_release"] = r["post_release"].lower()
    r["post_hoc"] = r["post_hoc"].lower()
    try:
        r["surface_edits_n"] = int(r.get("surface_edits") or 0)
    except ValueError:
        r["surface_edits_n"] = 0
    r["passed"] = [s.strip().upper() for s in (r.get("passed_by") or "").replace(",", ";").split(";") if s.strip()]
    r["also"] = [s.strip().upper() for s in (r.get("also_raised") or "").replace(",", ";").split(";") if s.strip()]
    return r


prim = [norm(r) for r in rows("data/changes.csv") if (r.get("round") or "").startswith("P")]
sec_all = [norm(r) for r in rows("data/changes_secondary.csv")]
# Amendment 1: a secondary row whose change lies inside a primary window is
# counted in the primary frame only, so that M4 does not count it twice.
sec = [r for r in sec_all if "also in the primary frame" not in (r.get("comment") or "").lower()]
costs = rows("data/costs.csv")
hoc = rows("data/post_hoc_readings.csv")
steps_r = rows("data/research_steps.csv")

out = []
p = out.append

p(f"Primary frame: {len(prim)} changes in {len(set(r['round'] for r in prim))} rounds")
p(f"Secondary frame: {len(sec_all)} rows, {len(sec_all) - len(sec)} of them inside a primary window and counted there only (amendment 1)")
p("Tier over all steps: " + ", ".join(f"{t} {sum(r['tier'] == t for r in prim)}" for t in TIERS)
  + f", blank or other {sum(r['tier'] not in TIERS for r in prim)}")
p("")

# M1: by step and tier
p("M1. Changes by step (first raised) and tier; A-tier surface edits")
p("step  " + "  ".join(f"{t:>3}" for t in TIERS) + "  A-edits  rounds with the step")
seen_steps = [s for s in STEPS if any(r["step"] == s for r in prim)] + \
    sorted({r["step"] for r in prim} - set(STEPS))
for s in seen_steps:
    rs = [r for r in prim if r["step"] == s]
    edits = sum(r["surface_edits_n"] for r in rs if r["tier"] == "A")
    rounds = sorted({r["round"] for r in rs})
    p(f"{s:<5} " + "  ".join(f"{sum(r['tier'] == t for r in rs):>3}" for t in TIERS)
      + f"  {edits:>7}  {', '.join(rounds)}")
p("")
p("M1. A and B changes by step, type and direction")
for s in seen_steps:
    rs = [r for r in prim if r["step"] == s and r["tier"] in ("A", "B")]
    if not rs:
        continue
    p(f"{s}: types {dict(Counter(r['type'] for r in rs).most_common())}; "
      f"directions {dict(Counter(r['direction'] for r in rs).most_common())}; "
      f"improved {dict(Counter(r['improved'] for r in rs).most_common())}")
p("")
p("A and B changes by round and step")
for rd in sorted({r["round"] for r in prim}):
    rs = [r for r in prim if r["round"] == rd]
    by = Counter((r["step"], r["tier"]) for r in rs if r["tier"] in ("A", "B", "C"))
    p(f"{rd}: " + "; ".join(f"{s} {t} {n}" for (s, t), n in sorted(by.items())))
p("")

# M2: A-tier changes to text an earlier step had passed
p("M2. A-tier changes altering text an earlier step in the round had read and passed")
for s in seen_steps:
    rs = [r for r in prim if r["step"] == s and r["tier"] == "A"]
    if not rs:
        continue
    passed = [r for r in rs if r["passed"]]
    who = Counter(x for r in passed for x in r["passed"])
    p(f"{s}: {len(passed)} of {len(rs)}; passed by {dict(who.most_common())}")
also = Counter(x for r in prim if r["tier"] in ("A", "B") for x in r["also"])
p(f"'also raised' by a later step, A and B changes: {dict(also.most_common())}")
p("")

# M3: cost per A-tier change
p("M3. Recorded cost and A-tier changes by step, primary frame (list rates, estimates)")
cost_by = defaultdict(float)
cost_rounds = defaultdict(set)
for c in costs:
    if c["round"].startswith("P") and c["step"] in STEPS and c["cost_usd"]:
        cost_by[c["step"]] += float(c["cost_usd"])
        cost_rounds[c["step"]].add(c["round"])
for s in seen_steps:
    a = sum(1 for r in prim if r["step"] == s and r["tier"] == "A")
    ab = sum(1 for r in prim if r["step"] == s and r["tier"] in ("A", "B", "C"))
    cst = cost_by.get(s)
    if cst:
        per = f"{cst / a:.2f} per A change" if a else "no A change"
        p(f"{s}: ${cst:.2f} over {', '.join(sorted(cost_rounds[s]))}; A {a}, A/B/C {ab}; {per}")
    else:
        p(f"{s}: no separable model cost recorded; A {a}, A/B/C {ab}")
# The reader review as one step, over the rounds it ran
rr_rounds = sorted(cost_rounds["R1"] | cost_rounds["R2"] | cost_rounds["RC"])
rr_cost = cost_by["R1"] + cost_by["R2"] + cost_by["RC"]
rr_a = sum(1 for r in prim if r["step"] in ("R1", "R2", "RC") and r["tier"] == "A")
rr_abc = sum(1 for r in prim if r["step"] in ("R1", "R2", "RC") and r["tier"] in ("A", "B", "C"))
if rr_cost:
    p(f"reader review (R1, R2 and RC together): ${rr_cost:.2f} over {', '.join(rr_rounds)}; A {rr_a}, A/B/C {rr_abc}"
      + (f"; {rr_cost / rr_a:.2f} per A change" if rr_a else ""))
# E only in the rounds where the reader review also ran, for a like-for-like view
e_same = sum(float(c["cost_usd"]) for c in costs if c["step"] == "E" and c["round"] in rr_rounds and c["cost_usd"])
e_same_a = sum(1 for r in prim if r["step"] == "E" and r["round"] in rr_rounds and r["tier"] == "A")
p(f"E in the reader review's rounds only ({', '.join(rr_rounds)}): ${e_same:.2f}; A {e_same_a}")
p("")

# By round, for the rounds with a reader review
p("A-tier changes by round and step, with each round's recorded review cost")
for rd in sorted({r["round"] for r in prim}):
    a_by = Counter(r["step"] for r in prim if r["round"] == rd and r["tier"] == "A")
    cst = {c["step"]: float(c["cost_usd"]) for c in costs if c["round"] == rd and c["step"] in STEPS and c["cost_usd"]}
    p(f"{rd}: A by step {dict(a_by)}; review cost by step {cst}")
p("")

# M4: escapes
p("M4. Escapes: A-tier changes after a piece's release")
esc = [r for r in prim + sec if r["post_release"] == "yes" and r["tier"] == "A"]
p(f"A-tier post-release changes: {len(esc)} (primary {sum(r in prim for r in esc)}, secondary {sum(r in sec for r in esc)})")
later_ev = [r for r in esc if (r.get("comment") or "").strip().lower().startswith("later evidence")]
corr = [r for r in esc if r not in later_ev]
p(f"  of which 'later evidence' notices {len(later_ev)}, other changes {len(corr)}")
p(f"  other changes by step: {dict(Counter(r['step'] for r in corr).most_common())}")
p(f"  other changes by type: {dict(Counter(r['type'] for r in corr).most_common())}")
p(f"  passed before release by: {dict(Counter(x for r in corr for x in r['passed']).most_common())}")
p(f"  later evidence by step: {dict(Counter(r['step'] for r in later_ev).most_common())}")
p("  the other changes, one line each:")
for r in corr:
    p(f"   {r['id']} {r['round']} {r['step']} {r['type']}/{r['direction']}: {(r.get('after') or '')[:110]}")
p("")

# M5
p("M5. Readings made after the counts")
p(f"{len(hoc)} readings; introduced by {dict(Counter((h.get('introduced_by') or '').split(' (')[0].split(',')[0].strip() for h in hoc).most_common())}")
p(f"tested later: {dict(Counter((h.get('tested_later') or '').strip().lower() for h in hoc).most_common())}; "
  f"results: {dict(Counter((h.get('result') or '').strip().lower() for h in hoc).most_common())}")
prim_hoc = [r for r in prim if r["post_hoc"] == "yes"]
p(f"primary-frame changes flagged post hoc: {len(prim_hoc)}, by step {dict(Counter(r['step'] for r in prim_hoc).most_common())}")
p("")

# M6
p("M6. Reversals and changes that moved away from the evidence")
rev = [r for r in prim + sec if r["improved"] == "no" or "revers" in (r.get("comment") or "").lower()
       or "undo" in (r.get("comment") or "").lower() or "undone" in (r.get("comment") or "").lower()]
p(f"{len(rev)} rows")
for r in rev:
    p(f"   {r['id']} {r['step']} improved={r['improved']}: {(r.get('comment') or '')[:150]}")
p("")

# M7
p("M7. Research steps")
p(f"{len(steps_r)} rows; by kind {dict(Counter((s.get('kind') or '').strip() for s in steps_r))}; "
  f"touched an outcome {dict(Counter((s.get('touched_outcome') or '').strip().lower() for s in steps_r))}")
for kind in ("P", "Lit"):
    ks = [s for s in steps_r if (s.get("kind") or "").strip() == kind]
    p(f"{kind}: {dict(Counter((s.get('touched_outcome') or '').strip().lower() for s in ks))}")
p("")

if os.path.exists("data/blind_compare.txt"):
    p("M8. Second coder (data/blind_compare.txt)")
    out.extend("   " + l for l in open("data/blind_compare.txt").read().splitlines()[:6])

text = "\n".join(out)
open("data/tally.txt", "w").write(text + "\n")
print(text)
