#!/usr/bin/env python3
"""LH042 evidence review: check sources.md's read time, status and URL for each
retained body against the collector's read logs. Usage: python3 -I studies/LH042/review/sources_check.py"""
import csv, pathlib, re
H = pathlib.Path(__file__).resolve().parent.parent
log = {}
for rl in (H / "data").glob("*/readlog.csv"):
    for r in csv.DictReader(open(rl)):
        log[f"{rl.parent.name}/{int(r['n']):03d}"] = r
bad = n = 0
for line in open(H / "sources.md"):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 6 or cells[0] not in log:
        continue
    n += 1
    r = log[cells[0]]
    url_ok = r["url"] in line
    t_ok = r["start_utc"] in line
    s_ok = (str(r["http_status"]) in cells) or (not r["http_status"])
    if not (url_ok and t_ok and s_ok):
        bad += 1
        print("DIFF", cells[0], "url" if not url_ok else "", "time" if not t_ok else "", "status" if not s_ok else "", "|", r["start_utc"], r["http_status"])
print(f"sources.md rows matched to read logs: {n}; rows differing: {bad}; read-log entries: {len(log)}")
