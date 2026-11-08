#!/usr/bin/env python3
"""LH042: check that every quotation in data/counts.csv and data/relayed.csv is in
its retained body (after converting HTML to text and collapsing whitespace and
quote marks), and that each admitted count's figure appears in its quotation.
Usage: python3 -I studies/LH042/scripts/check_quotes.py"""
import csv, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from totext import text_of
DATA = HERE.parent / "data"

def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("∼", "~")
    return re.sub(r"\s+", " ", s).strip()

cache = {}
def body_text(src):
    if src not in cache:
        cache[src] = norm(text_of((DATA / (src + ".body")).read_bytes()))
    return cache[src]

bad = 0
for fname in ["counts.csv", "relayed.csv"]:
    p = DATA / fname
    if not p.exists():
        continue
    for r in csv.DictReader(open(p)):
        if not r.get("source") or not r.get("quote"):
            continue
        ok = norm(r["quote"]) in body_text(r["source"])
        fig = True
        if fname == "counts.csv":
            c = int(r["count"])
            forms = {f"{c:,}", str(c)}
            if c % 100 == 0:
                forms |= {f"{c/1000:g}K", f"{c/1000:g}k"}
            if c >= 1_000_000:
                forms.add(f"{c/1_000_000:g} million")
            fig = any(x in r["quote"] for x in forms)
        status = "ok" if ok and fig else ("QUOTE NOT FOUND" if not ok else "FIGURE NOT IN QUOTE")
        if status != "ok":
            bad += 1
        print(f"{fname}\t{r['id']}\t{status}")
print("problems:", bad)
sys.exit(1 if bad else 0)
