#!/usr/bin/env python3
"""LH042 evidence review: compare the live re-reads with the record's retained reads.
For each live URL: was the page byte-identical to the record's read (hash as received)?
If not, is every counts.csv quotation from that page still in the live text?
Usage: python3 -I studies/LH042/review/live_compare.py"""
import csv, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
D = HERE.parent / "data"
sys.path.insert(0, str(HERE.parent / "scripts"))
from totext import text_of
def norm(s):
    for a, b in [("’","'"),("‘","'"),("“",'"'),("”",'"'),("–","-"),("—","-"),("∼","~")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()
orig = {}
for rl in D.glob("*/readlog.csv"):
    for r in csv.DictReader(open(rl)):
        orig[r["url"]] = (rl.parent.name + "/" + f"{int(r['n']):03d}", r["sha256_as_fetched"])
counts = list(csv.DictReader(open(D / "counts.csv")))
for r in csv.DictReader(open(HERE / "live" / "readlog.csv")):
    src, h = orig[r["url"]]
    same = h == r["sha256_received"]
    qs = [c for c in counts if c["source"] == src]
    t = norm(text_of((HERE / "live" / f"{int(r['n']):03d}.body").read_bytes())) if r["status"] == "200" else ""
    found = [c["id"] for c in qs if norm(c["quote"]) in t]
    missing = [c["id"] for c in qs if norm(c["quote"]) not in t]
    print(f"live {int(r['n']):03d} = record {src}: status {r['status']}; byte-identical to record read: {same}; "
          f"quotations from this page: {len(qs)}; found live: {len(found)}; missing live: {missing or 'none'}")
