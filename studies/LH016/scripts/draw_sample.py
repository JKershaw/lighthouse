"""LH016: draw the second coder's sample, as the brief fixes it.

Reads data/changes.csv (the first coder's table), keeps the primary frame's
changes (rounds P1 to P6), sorts them by id, and draws 30 with
random.Random(16) (all of them if there are 30 or fewer). Writes:

  data/blind_input.csv  what the second coder sees: a sample number, the
                        surface, the text before and after, and the record
                        passage the change rests on; nothing else
  data/blind_key.csv    sample number to change id, for compare_blind.py;
                        the second coder is not given this file

Run from studies/LH016: python3 scripts/draw_sample.py
"""
import csv
import random

rows = [r for r in csv.DictReader(open("data/changes.csv", newline=""))
        if r["round"].startswith("P")]
rows.sort(key=lambda r: r["id"])
sample = rows if len(rows) <= 30 else random.Random(16).sample(rows, 30)
sample.sort(key=lambda r: r["id"])
# The order the second coder sees is shuffled with the same seed, so that
# neighbouring changes from one round do not sit together.
order = list(range(len(sample)))
random.Random(16).shuffle(order)

with open("data/blind_input.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sample_no", "surfaces", "before", "after", "evidence"])
    for n, i in enumerate(order, 1):
        r = sample[i]
        w.writerow([n, r["surfaces"], r["before"], r["after"], r["evidence"]])
with open("data/blind_key.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sample_no", "id"])
    for n, i in enumerate(order, 1):
        w.writerow([n, sample[i]["id"]])
print(f"{len(rows)} primary-frame changes; {len(sample)} drawn")
