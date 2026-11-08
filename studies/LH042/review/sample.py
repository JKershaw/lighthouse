#!/usr/bin/env python3
"""LH042 evidence review: draw a fixed random sample of admitted counts to check by hand.
Seed fixed before the draw (20261108). Usage: python3 -I studies/LH042/review/sample.py"""
import csv, pathlib, random
D = pathlib.Path(__file__).resolve().parent.parent / "data"
ids = [r["id"] for r in csv.DictReader(open(D / "counts.csv")) if r["status"] == "admitted"]
rng = random.Random(20261108)
s = sorted(rng.sample(ids, 24))
print(len(ids), "admitted;", "sample of", len(s), ":", " ".join(s))
