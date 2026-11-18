#!/usr/bin/env python3
"""LH055 third withholding pass, text only (18 November 2026, Watch read).

The HTML-to-text extraction joins adjacent table cells with no separator, so an IPv4 address
standing next to a letter or digit in the next cell has no word boundary and escaped the
collector's patterns in the extracted text (the retained body, where cells are tag-separated,
was withheld correctly). This pass withholds any dotted quad not preceded by a digit or dot in
retained text files, using the body's cell boundaries for the cases where a cell's text ends in
a digit, and records SHA-256 before and after in data/<label>/withholding_pass3.json.
Usage: python3 -I studies/LH055/scripts/withhold_pass3_text.py <label>
"""
import glob, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
d = os.path.join(HERE, "..", "data", sys.argv[1])
# Cell boundaries checked against the retained body: the tag cell is "sco-fix2" and the host-count
# cell that follows the address list is "5".
FIXED = [(b"sco-fix238.11.173.1-125", b"sco-fix2[ipv4 withheld]-125"),
         (b"104.168.112.2375AS", b"[ipv4 withheld]5AS")]
PAT = re.compile(rb"(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?!\d)")
sha = lambda b: hashlib.sha256(b).hexdigest()
log = {}
for path in sorted(glob.glob(os.path.join(d, "text", "*.txt"))):
    b = open(path, "rb").read()
    nb, n = b, 0
    for old, new in FIXED:
        n += nb.count(old)
        nb = nb.replace(old, new)
    nb, m = PAT.subn(b"[ipv4 withheld]", nb)
    if n + m:
        open(path, "wb").write(nb)
        log[os.path.basename(path).split(".")[0]] = {"text": {"sha256_before": sha(b), "sha256_after": sha(nb), "withheld": n + m}}
if log:
    json.dump(log, open(os.path.join(d, "withholding_pass3.json"), "w"), indent=1, sort_keys=True)
print(log)
