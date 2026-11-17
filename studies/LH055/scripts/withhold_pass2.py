#!/usr/bin/env python3
"""LH055 second withholding pass (17 November 2026, driving session).

The collector's defanged-indicator pattern matched the bracketed tail of a defanged IPv4 address
(for example "a.b.c[.]d") and left its first two octets in the retained copies. This pass removes
any "a.b." left directly before a withheld marker, in retained bodies and text, and records the
SHA-256 before and after of each file it changes in data/<label>/withholding_pass2.json. Replays
follow that chain. Usage: python3 -I studies/LH055/scripts/withhold_pass2.py
"""
import glob, gzip, hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
PAT = re.compile(rb"\b\d{1,3}\.\d{1,3}\.(?=\[(?:defanged indicator withheld|ipv4 withheld)\])")
sha = lambda b: hashlib.sha256(b).hexdigest()

for label in sorted(os.listdir(DATA)):
    d = os.path.join(DATA, label)
    log = {}
    for path in sorted(glob.glob(os.path.join(d, "bodies", "*.raw.gz")) + glob.glob(os.path.join(d, "text", "*.txt"))):
        gz = path.endswith(".gz")
        b = gzip.open(path).read() if gz else open(path, "rb").read()
        nb, n = PAT.subn(b"", b)
        if not n:
            continue
        (gzip.open(path, "wb") if gz else open(path, "wb")).write(nb)
        sid = os.path.basename(path).split(".")[0]
        kind = "body" if gz else "text"
        log.setdefault(sid, {})[kind] = {"sha256_before": sha(b), "sha256_after": sha(nb), "prefixes_removed": n}
    if log:
        json.dump(log, open(os.path.join(d, "withholding_pass2.json"), "w"), indent=1, sort_keys=True)
        print(label, {k: {kk: vv["prefixes_removed"] for kk, vv in v.items()} for k, v in log.items()})
