#!/usr/bin/env python3
"""R-0110 coverage check (fresh checker, 21 November 2026). Offline; reads the repository only.
1. Every body deleted since 240e6fb has a <stem>.derived.json beside it at HEAD, and every derived file has a
   deleted body. 2. Every deleted body's file name and folder are named in its study's data/REMOVED.md (exactly,
   or within a folder range or file-name range that the note states; printed for reading by hand where not exact).
3. No path in remove_list.tsv, nor any deleted path, exists in the working tree.
Usage: python3 -I r0110_coverage.py
"""
import os, re, subprocess
R = "/home/user/lighthouse"; PRE = "240e6fb"
g = lambda *a: subprocess.run(["git", "-C", R] + list(a), capture_output=True, check=True, text=True).stdout.split("\n")
deleted = [f for f in g("diff", "--name-only", "--diff-filter=D", PRE, "HEAD", "--", "studies") if f]
derived = [f for f in g("ls-files", "studies/*.derived.json") if f]
stem = lambda f: re.sub(r"\.(body|raw\.gz|raw|html\.gz|html)$", "", f)
print("deleted since 240e6fb:", len(deleted), "| derived files at HEAD:", len(derived))
print("deleted without derived:", [f for f in deleted if not os.path.exists(os.path.join(R, stem(f) + ".derived.json"))])
ds = {stem(f) for f in deleted}
print("derived without a deleted body:", [f for f in derived if f[: -len(".derived.json")] not in ds])
print("deleted with a non-body extension:", [f for f in deleted if stem(f) == f])
rl = [l.split("\t")[0].lstrip("./") for l in open(R + "/notes/keeper/robots-intent-2026-11-21/remove_list.tsv") if l.strip()]
print("remove_list entries:", len(rl), "| not among deleted:", [f for f in rl if f not in deleted])
print("present in working tree (remove_list or deleted):", [f for f in set(rl) | set(deleted) if os.path.exists(os.path.join(R, f))])
print("deleted beyond remove_list:", sorted(set(deleted) - set(rl)))
for s in sorted({f.split("/")[1] for f in deleted}):
    note = open(f"{R}/studies/{s}/data/REMOVED.md").read()
    fs = [f for f in deleted if f.split("/")[1] == s]
    exact, loose = 0, []
    for f in fs:
        base, folder = f.split("/")[-1], f.split("/")[-2]
        if base in note and folder in note: exact += 1
        else: loose.append(f.split("/data/")[1])
    print(f"{s}: deleted {len(fs)}, base and folder both named in REMOVED.md {exact}, others (read against the note's ranges):")
    for x in loose: print("     ", x)
