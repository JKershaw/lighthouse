#!/usr/bin/env python3
"""LH042: extract the "Recent sweeps" table of OpenA2A's Exposure Prevalence Index.

Usage: python3 -I studies/LH042/scripts/extract_index.py data/<label> [<n>]
Reads data/<label>/<n>.body (default 001), finds the table rows (sweep date,
total, MCP, LLM, OpenClaw, A2A; a month with several sweeps also lists their
count and range) and the "As of" date, and appends one row per sweep to
data/index_reads.csv with the read label, so a row the publisher restates later
is kept beside its earlier reading rather than overwritten.
"""
import csv, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from totext import text_of
OUT = HERE.parent / "data" / "index_reads.csv"


def main(d, n="001"):
    d = pathlib.Path(d)
    if not d.is_absolute():
        d = HERE.parent / d
    t = re.sub(r"\s+", " ", text_of((d / f"{n}.body").read_bytes()))
    asof = re.search(r"As of ([A-Z][a-z]+ \d{1,2}, 20\d\d)", t)
    seg = t.split("Recent sweeps", 1)[1].split("Top countries", 1)[0]
    rows = []
    for chunk in re.split(r"(?=\b20\d\d-\d\d-\d\d\b)", seg):
        m = re.match(r"(20\d\d-\d\d-\d\d)\s+(.*)", chunk.strip())
        if not m:
            continue
        date, rest = m.group(1), m.group(2)
        multi = re.match(r"(\d+) sweeps · latest plotted\s+(.*)", rest)
        nsw, lo, hi = "1", "", ""
        if multi:
            nsw, rest = multi.group(1), multi.group(2)
        nums = re.findall(r"\d{1,3}(?:,\d{3})*", rest)
        if multi:
            plotted, lo, hi, nums = nums[0], nums[1], nums[2], nums[3:]
            total = plotted
        else:
            total, nums = nums[0], nums[1:]
        mcp, llm, oc, a2a = (nums + [""] * 4)[:4]
        rows.append(dict(read=d.name, as_of=asof.group(1) if asof else "", sweep=date, sweeps_in_month=nsw,
                         range_low=lo, range_high=hi, total=total, mcp=mcp, llm=llm, openclaw=oc, a2a=a2a))
    new = not OUT.exists()
    with open(OUT, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main(*sys.argv[1:])
