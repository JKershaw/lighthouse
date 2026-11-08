#!/bin/sh
# LH046 replay. Offline: recompute every derived figure and the figure from the retained counts.
#   sh studies/LH046/replay.sh            (from the repository root)
# Online (refetches about 450 files, about 17 GB; files may have changed since 8 November 2026,
# so compare sha256 in data/hours.csv): python3 -I studies/LH046/scripts/collect.py <new data dir>
set -e
python3 -I studies/LH046/scripts/analyse.py studies/LH046/data > /dev/null
python3 -I studies/LH046/scripts/figure.py studies/LH046/data studies/LH046/figure.svg
echo "wrote studies/LH046/data/files.csv, studies/LH046/data/results.txt, studies/LH046/figure.svg"
