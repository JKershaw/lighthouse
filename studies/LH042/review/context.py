#!/usr/bin/env python3
"""LH042 evidence review: print each chosen count's row and the retained body's text
around its quotation, for reading by hand. Independent of check_quotes.py except for
the shared HTML-to-text helper (scripts/totext.py).
Usage: python3 -I studies/LH042/review/context.py C01 C02 ... [--width N]"""
import csv, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from totext import text_of
D = HERE.parent / "data"
args = [a for a in sys.argv[1:] if not a.startswith("--")]
W = 500
for a in sys.argv[1:]:
    if a.startswith("--width="):
        W = int(a.split("=")[1])
def norm(s):
    for a, b in [("’","'"),("‘","'"),("“",'"'),("”",'"'),("–","-"),("—","-"),("∼","~")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()
rows = {r["id"]: r for r in csv.DictReader(open(D / "counts.csv"))}
for i in args:
    r = rows[i]
    t = norm(text_of((D / (r["source"] + ".body")).read_bytes()))
    q = norm(r["quote"])
    k = t.find(q)
    print("=" * 100)
    for f in ["id","publisher","product","method","kind","unit","count","qualifier","date_start","date_end","date_basis","published","source","series","note"]:
        print(f"{f}: {r[f]}")
    print("QUOTE:", r["quote"])
    print("found at", k, "occurrences", t.count(q))
    if k >= 0:
        print("CONTEXT:", t[max(0, k - W): k + len(q) + W])
