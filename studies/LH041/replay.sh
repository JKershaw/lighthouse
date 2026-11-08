#!/bin/sh
# LH041 replay: re-derive every table and the figure from the retained read, offline.
# Run from the repository root. Reads only studies/LH041/data/<read>/.
set -e
READ=${1:-2026-11-08T1910Z}
python3 -I studies/LH041/scripts/tabulate.py --read "$READ" > /dev/null            # pre-set view (brief as written)
python3 -I studies/LH041/scripts/tabulate.py --read "$READ" --posthoc > /dev/null  # post hoc view (labelled in LH041.md)
python3 -I studies/LH041/scripts/draw_figure.py "$READ"
echo "tables in studies/LH041/data/$READ/tables/ and tables/posthoc/"
