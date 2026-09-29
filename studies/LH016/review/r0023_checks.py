"""R-0023: the evidence reviewer's independent recount of LH016's figures.

Recomputes, with its own code and without importing the study's scripts,
the counts the record's Answer and Findings rest on (from data/changes.csv,
data/changes_secondary.csv, data/costs.csv, data/blind_codes.csv,
data/blind_key.csv, data/post_hoc_readings.csv, data/research_steps.csv and
data/origin_check.txt), and the two driver checks of the replays' findings
(from LH011's and LH012's retained tables). Writes r0023_checks.txt.

Run from the repository root:
python3 studies/LH016/review/r0023_checks.py
"""
import csv
import statistics as st
from collections import Counter, defaultdict

D = "studies/LH016/data/"
out = []
p = out.append


def rows(path):
    return list(csv.DictReader(open(path, newline="")))


prim = rows(D + "changes.csv")
sec = rows(D + "changes_secondary.csv")
costs = rows(D + "costs.csv")

# --- 1. The primary frame's counts (Answer; Findings 1 to 4)
p("1. Primary frame")
p(f"rows {len(prim)}; by round {dict(sorted(Counter(r['round'] for r in prim).items()))}")
p(f"tiers {dict(Counter(r['tier'] for r in prim))}")
A = [r for r in prim if r["tier"] == "A"]
p(f"A-tier {len(A)}; surface edits over A rows {sum(int(r['surface_edits']) for r in A)}")
by_step = defaultdict(Counter)
for r in prim:
    by_step[r["step"]][r["tier"]] += 1
for s in ["K", "E", "B", "R1", "R2", "RC", "D"]:
    if by_step[s]:
        p(f"  {s}: " + ", ".join(f"{t} {by_step[s][t]}" for t in "ABCN"))
MEANING = {"unit", "cause", "new reading"}
p("A-tier types by step, and the group unit/cause/new reading (a grouping the record says was made after the counts):")
for s in ["K", "E", "B", "R2", "RC", "D"]:
    rs = [r for r in A if r["step"] == s]
    tc = Counter(r["type"] or "(none)" for r in rs)
    p(f"  {s}: {dict(tc.most_common())}; group {sum(1 for r in rs if r['type'] in MEANING)} of {len(rs)}; "
      f"certainty+figure {tc['certainty'] + tc['figure']}")


def passed(r):
    return [x.strip() for x in r["passed_by"].replace(",", ";").split(";") if x.strip()]


for s in ["K", "R2", "RC", "E", "D", "B"]:
    rs = [r for r in A if r["step"] == s]
    any_e = sum(1 for r in rs if any(x.startswith("E") for x in passed(r)))
    any_p = sum(1 for r in rs if passed(r))
    r1 = sum(1 for r in rs if "R1" in passed(r))
    p(f"  M2 {s}: {any_p} of {len(rs)} altered text an earlier step passed; passed by an evidence review (E, E(R-0016) or E(R-0017)) {any_e}; by R1 {r1}")
pre = [r for r in A if r["round"] in ("P5", "P6")]
p(f"before release in P5 and P6: {len(pre)} A-tier changes {dict(Counter(r['step'] for r in pre).most_common())}")
p(f"improved over A rows by step: " + "; ".join(f"{s} {dict(Counter(r['improved'] for r in A if r['step'] == s))}" for s in ["K", "E", "B", "R2", "RC", "D"]))
cdec = [r for r in prim if r["tier"] == "C"]
p(f"tier C by step and direction: {dict(Counter((r['step'], r['direction']) for r in cdec))}")
p("")

# --- 2. Cost per A-tier change (Finding 6)
p("2. Costs (list rates, from data/costs.csv)")
cost = defaultdict(float)
for c in costs:
    if c["round"].startswith("P") and c["cost_usd"]:
        cost[c["step"]] += float(c["cost_usd"])
nA = Counter(r["step"] for r in A)
for s in ["E", "B", "R1", "R2", "RC"]:
    p(f"  {s}: ${cost[s]:.2f}; A {nA[s]}; per A change {cost[s] / nA[s] if nA[s] else float('nan'):.2f}")
rr = cost["R1"] + cost["R2"] + cost["RC"]
p(f"  reader review together: ${rr:.2f}; A {nA['R2'] + nA['RC']}; per A change {rr / (nA['R2'] + nA['RC']):.2f}")
e456 = sum(float(c["cost_usd"]) for c in costs if c["step"] == "E" and c["round"] in ("P4", "P5", "P6"))
a456 = sum(1 for r in A if r["step"] == "E" and r["round"] in ("P4", "P5", "P6"))
p(f"  E in P4 to P6: ${e456:.2f}; A {a456}; per A change {e456 / a456:.2f}")
for rd, st_ in [("P1", "LH011"), ("P3", "LH012"), ("P5", "LH014"), ("P6", "LH015")]:
    res = sum(float(c["cost_usd"]) for c in costs if c["round"] == rd and c["step"] in ("research", "writing") and c["cost_usd"])
    chk = sum(float(c["cost_usd"]) for c in costs if c["round"] == rd and c["step"] in ("E", "B", "R1", "R2", "RC") and c["cost_usd"])
    p(f"  {rd} {st_}: research and writing ${res:.2f}; checks before first release ${chk:.2f}")
p("  replay runs X1 to X3: no row in costs.csv; the record's $3.59, $4.98, $4.82 have no retained source")
p("")

# --- 3. Escapes (Finding 7)
p("3. After release")
sec_kept = [r for r in sec if "also in the primary frame" not in r["comment"].lower()]
esc = [r for r in prim + sec_kept if r["post_release"] == "yes" and r["tier"] == "A"]
later = [r for r in esc if r["comment"].lower().startswith("later evidence")]
corr = [r for r in esc if r not in later]
p(f"A-tier changes after release {len(esc)} (primary {sum(r in prim for r in esc)}, secondary {sum(r in sec_kept for r in esc)}); later evidence {len(later)}; corrections {len(corr)}")
p(f"corrections by step {dict(Counter(r['step'] for r in corr).most_common())}")
k_sec = [r for r in corr if r["step"] == "K" and r["id"].startswith("S")]
p(f"the keeper's corrections in the secondary frame ({len(k_sec)}), by main surface: "
  f"{dict(Counter(r['surfaces'].split(';')[0].split(' (')[0].strip() for r in k_sec))}")
p("")

# --- 4. Origin of the corrected text (Finding 5), read from data/origin_check.txt
p("4. Origin of the text the recheck and the evidence review corrected (data/origin_check.txt)")
oc = {}
for line in open(D + "origin_check.txt"):
    parts = line.split()
    if len(parts) > 3 and parts[0][0] == "P" and "-" in parts[0]:
        oc[parts[0]] = "written" if "written during" in line else ("added" if " added:" in line else "starting")
for s in ["RC", "E", "R2", "K", "D", "B"]:
    ids = [r["id"] for r in A if r["step"] == s]
    p(f"  {s}: {dict(Counter(oc.get(i, '?') for i in ids))}; written: {[i for i in ids if oc.get(i) == 'written']}")
p2e = [r["id"] for r in A if r["step"] == "E" and r["round"] == "P2"]
p(f"  E in P2 (LH011's revision): {len(p2e)} A rows, written during the round {sum(oc.get(i) == 'written' for i in p2e)}")
p("")

# --- 5. Second coder (Finding 11), kappa recomputed
p("5. Second coder")
first = {r["id"]: r for r in prim}
key = {r["sample_no"]: r["id"] for r in rows(D + "blind_key.csv")}
second = {r["sample_no"]: r for r in rows(D + "blind_codes.csv")}


def kappa(pairs):
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return po, (po - pe) / (1 - pe)


tiers = [(first[key[n]]["tier"], second[n]["tier"].strip().upper()) for n in key]
mat = [(a != "N", b != "N") for a, b in tiers]
types = [(first[key[n]]["type"].lower(), second[n]["type"].strip().lower()) for n in key
         if first[key[n]]["tier"] != "N" and second[n]["tier"].strip().upper() != "N"]
dirs = [(first[key[n]]["direction"].lower(), second[n]["direction"].strip().lower()) for n in key
        if first[key[n]]["tier"] != "N" and second[n]["tier"].strip().upper() != "N"]
p(f"  sample {len(tiers)}; first coder's tiers {dict(Counter(a for a, _ in tiers))}")
p(f"  material: agreement {kappa(mat)[0]:.3f}, kappa {kappa(mat)[1]:.3f}; tier: agreement {kappa(tiers)[0]:.3f}, kappa {kappa(tiers)[1]:.3f}")
p(f"  type agreement {sum(a == b for a, b in types)} of {len(types)}; direction {sum(a == b for a, b in dirs)} of {len(dirs)}")
p("")

# --- 6. Post hoc readings and research steps (Findings 8 and 10)
p("6. Post hoc readings and research steps")
hoc = rows(D + "post_hoc_readings.csv")
p(f"  readings {len(hoc)}; tested_later {dict(Counter(h['tested_later'] for h in hoc))}")
none = [h for h in hoc if h["tested_later"] == "no"]
p(f"  no test: {len(none)}, from stage 2: {sum('stage 2' in h['introduced_by'] for h in none)}, from the driving session after the keeper's reading: {sum('after the keeper' in h['introduced_by'] for h in none)}")
p(f"  introduced by stage 2 {sum('stage 2' in h['introduced_by'] for h in hoc)}; by research writers {sum('research writer' in h['introduced_by'] or 'writing agent' in h['introduced_by'] for h in hoc)}; by the driving session {sum(h['introduced_by'].startswith('the driving session') for h in hoc)}")
steps = rows(D + "research_steps.csv")
lit = [s for s in steps if s["kind"] == "Lit"]
p(f"  literature checks {len(lit)}; recorded a design change {sum(not s['effect'].startswith('none') for s in lit)}; recorded none {sum(s['effect'].startswith('none') for s in lit)} ({[s['id'] for s in lit if s['effect'].startswith('none')]})")
p(f"  brief conventions (P) {sum(s['kind'] == 'P' for s in steps)}")
p("")

# --- 7. Replay X2's litellm finding, recounted from LH011's retained table
p("7. litellm's releases that reached half within 30 days (studies/LH011/data/analysis/release_days.csv)")
rd = [r for r in rows("studies/LH011/data/analysis/release_days.csv") if r["project"] == "litellm"]
p(f"  litellm rows {len(rd)}; versions {len(set(r['version'] for r in rd))}; statuses {dict(Counter(r['status'] for r in rd))}")
byv = defaultdict(dict)
for r in rd:
    byv[r["version"]][int(r["day"])] = (r["date"], float(r["share_at_or_newer"]))
firsts = []
for v, days in byv.items():
    hit = [d for d in sorted(days) if 1 <= d <= 30 and days[d][1] >= 0.5]
    if hit:
        d0 = hit[0]
        later = [d for d in sorted(days) if d0 < d <= 30]
        held = [d for d in later if days[d][1] >= 0.5]
        firsts.append((v, d0, days[d0][0], len(held), len(later)))
        p(f"  {v}: first at half on day {d0} ({days[d0][0]}), share {days[d0][1]:.3f}; at half on {len(held)} of {len(later)} later days read (to day 30)")
p(f"  releases reaching half within 30 days: {len(firsts)}; median first day {st.median([f[1] for f in firsts])}; distinct dates {sorted(set(f[2] for f in firsts))}")
p(f"  releases at half on day 1 or 2: {sum(1 for f in firsts if f[1] <= 2)}")
p("")

# --- 8. Replay X3's drift finding, recounted from LH012's retained table
p("8. The rise after day 2 (studies/LH012/data/analysis/firstday_releases.csv)")
fr = rows("studies/LH012/data/analysis/firstday_releases.csv")
own = [(float(r["s30"]) - float(r["s2"])) * 100 for r in fr]
tab = [float(r["delta_points"]) for r in fr]
p(f"  releases {len(fr)}; delta_points equals (s30 - s2) x 100 within 0.01 for all rows: {all(abs(a - b) < 0.01 for a, b in zip(own, tab))}")
p(f"  day-30 share above day-2 share: {sum(x > 0 for x in own)}; median rise {st.median(own):.2f} points; quartiles {[round(q, 2) for q in st.quantiles(own, n=4)]}")
p(f"  above +10: {sum(x > 10 for x in own)}; below -10: {sum(x < -10 for x in own)}; settled (|delta| <= 10) {sum(abs(x) <= 10 for x in own)}")
bp = defaultdict(list)
for r, x in zip(fr, own):
    bp[r["project"]].append(x)
meds = {k: st.median(v) for k, v in bp.items()}
p(f"  projects {len(bp)}; median of project medians {st.median(meds.values()):.2f}; projects with median above zero {sum(m > 0 for m in meds.values())}; the one at or below: {[k for k, m in meds.items() if m <= 0]}")
rat = [float(r["ratio_s2_s30"]) for r in fr if r["ratio_s2_s30"] not in ("", "nan")]
p(f"  median day-2 share as a fraction of day-30: {st.median(rat):.3f}")
p("  note: s2 and s30 are the at-or-newer shares (LH012's definition), so the rise is the share of downloads moving to the release or a later one, not a later release displacing this one")

p("")

# --- 9. Two sensitivities the reviewer added
p("9. Reviewer's sensitivities")
WIDER = MEANING | {"scope", "limit"}
p("  the record's group (unit, cause, new reading) widened by scope and limit, A-tier changes by step:")
for s in ["K", "E", "B", "R2", "RC", "D"]:
    rs = [r for r in A if r["step"] == s]
    p(f"    {s}: {sum(1 for r in rs if r['type'] in WIDER)} of {len(rs)}")
rc8 = [r for r in A if r["step"] == "RC" and oc.get(r["id"]) == "written"]
p(f"  the recheck's 8 changes to text written during the round, by type: {dict(Counter(r['type'] for r in rc8))}")
import subprocess


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


p("  P6-29's short-form sentence ('more than a quarter of the recipes could not be decided'): commits that introduced its words")
p("    " + git("log", "--format=%h %ci %s", "-S", "more than a quarter of the recipes could not be decided",
               "--", "articles/short/recipes-follow-the-pin.md").replace("\n", "\n    ")[:400])
p("    (c488d2a is the window after the blind check, 3ca1804..c488d2a, credited to B or D; the resolution's window is 92d2013..ab2b12c)")
draft = git("show", "9523003:investigations/software-updates.md")
i = draft.find("39 of 50")
p("  P5-20: the draft's sentence at 9523003 (the round's first commit): '..." + draft[max(0, i - 60):i + 80].replace("\n", " ") + "...'")
p("    so the ambiguity the recheck fixed was in the draft; stage 2 reworded the sentence without removing it")

text = "\n".join(out)
open("studies/LH016/review/r0023_checks.txt", "w").write(text + "\n")
print(text)
