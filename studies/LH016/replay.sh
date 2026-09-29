#!/bin/sh
# LH016 replay: recompute every figure in the record from the retained tables,
# offline, and compare with the committed outputs. Run from the repository root:
#   bash studies/LH016/replay.sh
set -e
cd "$(dirname "$0")"
tmp=$(mktemp -d)
cp data/tally.txt data/blind_compare.txt data/origin_check.txt "$tmp"/
python3 scripts/draw_sample.py
git diff --quiet -- data/blind_input.csv data/blind_key.csv && echo "sample: unchanged (seed 16)"
python3 scripts/compare_blind.py > /dev/null
python3 scripts/tally.py > /dev/null
python3 scripts/post_hoc_origin.py > /dev/null
for f in tally.txt blind_compare.txt origin_check.txt; do
  if cmp -s "data/$f" "$tmp/$f"; then echo "$f: reproduced"; else echo "$f: DIFFERS"; fi
done
cd ../..
python3 studies/LH016/review/replay-X2/driver_check_litellm.py | cmp -s - studies/LH016/review/replay-X2/driver_check_litellm.txt && echo "driver_check_litellm.txt: reproduced"
python3 studies/LH016/review/replay-X3/driver_check_drift.py | cmp -s - studies/LH016/review/replay-X3/driver_check_drift.txt && echo "driver_check_drift.txt: reproduced"
rm -r "$tmp"
