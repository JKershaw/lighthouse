"""LH016, a reading made after the counts (post hoc): where did the text an A-tier
change corrected come from?

For each A-tier change in the primary frame with a non-empty `before`, the
quoted passage is split into fragments at "...", " / " and line breaks, and
each fragment of 30 characters or more (after collapsing spaces and
dropping Markdown emphasis) is searched for in every surface the change
names, as that surface stood at the round's starting commit. A change whose
fragment is found corrected text the round started with (the draft, or for
P2 and P4 the released piece); one whose fragments are all absent corrected
text written during the round by an earlier step; a change with an empty
`before` (or one the coder marked "(no such passage)") added text. Digits
are masked before the search, so a passage whose figures changed during the
round still counts as the round's starting text. The search is literal, so a fragment the coder
shortened or re-quoted can be missed; data/origin_check.txt lists every
row so that each class can be checked by eye.

Run from studies/LH016: python3 scripts/post_hoc_origin.py
"""
import csv
import re
import subprocess
from collections import Counter

START = {"P1": "1bc6e80", "P2": "a36508d", "P3": "08c505b",
         "P4": "89d4aa7", "P5": "9523003", "P6": "2135c64"}


def clean(s):
    # Digits are masked, so that a passage whose figures a later fix updated
    # (128 of 166 to 129 of 167) still counts as the same passage.
    s = s.replace("*", "").replace("`", "")
    s = re.sub(r"\d", "#", s)
    return re.sub(r"\s+", " ", s).strip()


def at(commit, path):
    try:
        return clean(subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True,
                                    text=True, check=True, cwd="../..").stdout)
    except subprocess.CalledProcessError:
        return ""


rows = [r for r in csv.DictReader(open("data/changes.csv", newline="")) if r["tier"].strip() == "A"]
out, cls = [], Counter()
by_step = {}
for r in rows:
    before = r["before"].strip()
    if not before or before.startswith("(no such"):
        c = "added"
    else:
        frags = [clean(f) for f in re.split(r"\.\.\.|…| / |\n", before)]
        frags = [f for f in frags if len(f) >= 30]
        texts = [at(START[r["round"]], s.strip()) for s in r["surfaces"].split(";") if s.strip()]
        if not frags:
            c = "unchecked (no fragment of 30 characters)"
        elif any(f in t for f in frags for t in texts):
            c = "in the round's starting text"
        else:
            c = "written during the round"
    cls[c] += 1
    by_step.setdefault(r["step"], Counter())[c] += 1
    out.append(f"{r['id']} {r['step']:<2} {c}: {before[:90]}")

summary = [f"A-tier changes: {len(rows)}", "by origin: " + str(dict(cls))]
for s in sorted(by_step):
    summary.append(f"  {s}: {dict(by_step[s])}")
text = "\n".join(summary + [""] + out)
open("data/origin_check.txt", "w").write(text + "\n")
print(text)
