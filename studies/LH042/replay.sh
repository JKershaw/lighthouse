#!/bin/sh
# LH042 offline replay: check every quotation against the retained bodies, then rebuild
# the dated table, the series list and the figure from data/counts.csv. No network.
set -e
cd "$(dirname "$0")/../.."
python3 -I studies/LH042/scripts/check_quotes.py | tail -1
python3 -I studies/LH042/scripts/build.py
python3 scripts/check_chart_style.py > /dev/null && echo "chart palette check passed"
