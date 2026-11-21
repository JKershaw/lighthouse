#!/usr/bin/env python3
"""LH042: check that every quotation in data/counts.csv and data/relayed.csv is in
its retained body (after converting HTML to text and collapsing whitespace and
quote marks), and that each admitted count's figure appears in its quotation.
For a body not kept (withheld for use=reference, amendment of 9 November 2026, or under the keeper's
decision of 21 November 2026), the check reads this run's local copy while it exists and copies each
quotation it finds there into the record's extract (.withheld.json, "quotes", at most 2,000 characters
in all, as the brief's amendment sets), so a later run, after the local copy is gone, still finds it:
a real quotation is never reported missing only because its body was not kept.
Usage: python3 -I studies/LH042/scripts/check_quotes.py"""
import csv, json, pathlib, re, sys
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
    """The retained body's text; for a body withheld for use=reference (amendment of 9 November
    2026), this run's local copy if present, else the quotations kept in its .withheld.json."""
    if src not in cache:
        body = DATA / (src + ".body")
        rec = DATA / (src + ".withheld.json")
        local = pathlib.Path(str(body) + ".withheld-local")
        if rec.exists() and not local.exists():
            cache[src] = norm(" | ".join(str(v) for v in json.loads(rec.read_text()).get("extract", {}).values()))
        else:
            cache[src] = norm(text_of((local if local.exists() else body).read_bytes()))
    return cache[src]

QUOTE_CAP = 2000


def keep_quote(src, quote):
    """Copy a quotation found in this run's local copy into the record's extract, once, within the cap.
    True when the quotation is safe for later runs (copied, already there, or its body is kept);
    False when copying it would pass the cap, which the check then reports as a problem."""
    rec_p = DATA / (src + ".withheld.json")
    local = pathlib.Path(str(DATA / (src + ".body")) + ".withheld-local")
    if not (rec_p.exists() and local.exists()):
        return True
    rec = json.loads(rec_p.read_text())
    ext = rec.setdefault("extract", {})
    quotes = ext.setdefault("quotes", [])
    if quote in quotes:
        return True
    if sum(len(q) for q in quotes) + len(quote) > QUOTE_CAP:
        return False  # over the cap: reported as a problem now, while the page is still to hand
    quotes.append(quote)
    rec_p.write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n")
    return True


bad = 0
for fname in ["counts.csv", "relayed.csv"]:
    p = DATA / fname
    if not p.exists():
        continue
    for r in csv.DictReader(open(p)):
        if not r.get("source") or not r.get("quote"):
            continue
        ok = norm(r["quote"]) in body_text(r["source"])
        capped = ok and not keep_quote(r["source"], r["quote"])
        fig = True
        if fname == "counts.csv":
            c = int(r["count"])
            forms = {f"{c:,}", str(c)}
            if c % 100 == 0:
                forms |= {f"{c/1000:g}K", f"{c/1000:g}k"}
            if c >= 1_000_000:
                forms.add(f"{c/1_000_000:g} million")
            fig = any(x in r["quote"] for x in forms)
        status = ("QUOTE NOT FOUND" if not ok else "FIGURE NOT IN QUOTE" if not fig
                  else f"QUOTE OVER THE {QUOTE_CAP}-CHARACTER CAP FOR A BODY NOT KEPT: shorten it" if capped else "ok")
        if status != "ok":
            bad += 1
        print(f"{fname}\t{r['id']}\t{status}")
print("problems:", bad)
sys.exit(1 if bad else 0)
