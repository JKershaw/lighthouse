#!/bin/sh
# LH047 re-audit of ISO week 2026-W47, offline replay. Run from the repository root:
#   sh studies/LH047/data/reaudit-2026-W47/replay.sh
# Needs the git objects of the population commit and of the later check commit (a clone with history
# back to 12 November 2026; in a shallow clone run `git fetch --shallow-since=2026-11-12 origin main` first).
# Makes no network request: the current robots.txt re-reads of 23 November 2026 (made once with
#   LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH047/scripts/fetch.py ../reaudit-2026-W47/robots-current \
#       studies/LH047/data/reaudit-2026-W47/needs-current.txt
# ) are kept in robots-current/ and are not repeated.
set -e
P=e74c302bb255f9d8c3ed7eee653f20a3f2dbf6ed   # last commit on main at or before 2026-11-22T23:59:59Z
L=f5aed200cce7a4b7de1f3e312525a9f5bd683fde   # main when the re-audit began (23 November 2026), for logs committed later
W=studies/LH047/data/reaudit-2026-W47/code
python3 -I $W/find_logs.py $P $L
python3 -I $W/classify.py
python3 -I $W/handcode.py $P
python3 -I $W/normalise.py $P $L
python3 -I $W/needs.py
python3 -I $W/audit.py $P
python3 -I $W/tabulate.py > /dev/null
echo "tables: studies/LH047/data/reaudit-2026-W47/tables.md; summary: studies/LH047/data/reaudit-2026-W47/summary.json"
