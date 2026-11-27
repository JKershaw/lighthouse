#!/usr/bin/env python3
"""LH062 evidence review (R-0162), 27 November 2026: reproduce tally.py and the record's figures.
Reads only retained files. Run: python3 -I studies/LH062/review/check.py  (output in check-output.txt)"""
import csv, os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(H)
out = subprocess.run([sys.executable, "-I", os.path.join(S, "tally.py")], capture_output=True, text=True).stdout
print("tally.py output identical to tally-output.txt:", out == open(os.path.join(S, "tally-output.txt")).read())
c = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(S, "claims.csv")))}
print("A07 exposed day14/day0 %.1f%%, day172/day0 %.1f%%; valid day14/day0 %.1f%%, day172/day0 %.1f%%" % (
    100*706/1405, 100*1019/1405, 100*865/1175, 100*660/1175))
print("A07 fall in valid by day 14: %.1f%% (authors: about 26%%); fall in exposed: %.1f%% (authors: 50%%)" % (
    100*(1175-865)/1175, 100*(1405-706)/1405))
print("A07 day-0 counts as share of 1,748: exposed %.1f%%, valid %.1f%%" % (100*1405/1748, 100*1175/1748))
print("A07 delivered 1,668 / 2,435 entities = %.1f%%; 1,668/(1,668+767) = %.1f%%" % (100*1668/2435, 100*1668/(1668+767)))
print("B1 36,293/36,425 = %.2f%%; 18,332/110,993 = %.2f%%; 36,425/110,993 = %.1f%%" % (
    100*36293/36425, 100*18332/110993, 100*36425/110993))
units = {}
for k, r in c.items():
    units.setdefault(r["doc"].split()[0], set()).add(r["unit"])
print("unit labels by document:", {k: sorted(v) for k, v in units.items()})
print("A07 unit labels differ within one document:", len(units["A07"]) > 1)
