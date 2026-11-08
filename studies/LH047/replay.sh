#!/bin/sh
# LH047 part C, offline replay: rebuilds the request table, the robots.txt index, the verdicts
# and the tables from files in the repository. Makes no network request. Run from the repository root:
#   sh studies/LH047/replay.sh
# The transcript extraction (scripts/transcript_requests.py) and the current robots.txt re-reads
# (scripts/fetch.py robots-current ...) are not replayed: the transcripts live outside the
# repository, and a re-read would be a new request. Their outputs are kept under data/.
set -e
python3 -I studies/LH047/scripts/robots9309.py
python3 -I studies/LH047/scripts/normalise_logs.py
python3 -I studies/LH047/scripts/robots_index.py
python3 -I studies/LH047/scripts/audit.py
python3 -I studies/LH047/scripts/tabulate.py > /dev/null
echo "tables: studies/LH047/data/audit/tables.md; summary: studies/LH047/data/audit/summary.json"
