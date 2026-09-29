#!/bin/sh
# LH011 offline replay, as studies/LH010/replay.sh. No network, no key. Python 3 with the `packaging`
# library (PEP 440 comparison; 24.0 was used).
#   sh studies/LH011/replay.sh           regenerate into a temporary directory and compare with data/
#   sh studies/LH011/replay.sh --write   also rewrite data/analysis/ and uptake.svg in place
# Step 5 (added with record version 0.3) also reruns the readings made after the counts were read:
# the piece's chart and its printed reading, and scripts/post_hoc.py, which reads LH008's retained
# events and lags as well. Step 6 (record version 0.4) reruns the checks behind that correction.
# Exits non-zero if any table differs.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0

echo "1. frame: frame.py (releases, CI subsample, SHA-256 order) from projects.csv and pypi_versions.csv"
LH011_OUT="$TMP/frame" "$PY" "$HERE/scripts/frame.py" > "$TMP/frame.log" || { echo "frame.py failed"; cat "$TMP/frame.log"; exit 1; }
for f in releases project_order; do
  if cmp -s "$TMP/frame/$f.csv" "$HERE/data/$f.csv"; then echo "   same  data/$f.csv"; else echo "   DIFF  data/$f.csv"; fail=1; fi
done

echo "2. analysis: analyse.py over data/counts, data/ci, data/daily_totals_*, data/pypistats"
LH011_OUT="$TMP/analysis" "$PY" "$HERE/scripts/analyse.py" > "$TMP/analyse.log" || { echo "analyse.py failed"; cat "$TMP/analyse.log"; exit 1; }
for p in "$TMP"/analysis/*.csv; do
  f=$(basename "$p")
  if cmp -s "$p" "$HERE/data/analysis/$f"; then echo "   same  data/analysis/$f"
  elif [ "${1:-}" = "--write" ]; then echo "   changed, rewritten: data/analysis/$f"
  else echo "   DIFF  data/analysis/$f"; fail=1; fi
done
for p in "$HERE"/data/analysis/*.csv; do
  f=$(basename "$p"); [ -e "$TMP/analysis/$f" ] || { echo "   MISSING  data/analysis/$f"; fail=1; }
done

echo "3. figure: draw_figure.py"
LH011_OUT="$TMP/analysis" "$PY" "$HERE/scripts/draw_figure.py" "$TMP/uptake.svg" > /dev/null || { echo "draw_figure.py failed"; exit 1; }
if cmp -s "$TMP/uptake.svg" "$HERE/uptake.svg"; then echo "   same  uptake.svg"; elif [ "${1:-}" = "--write" ]; then echo "   changed, rewritten: uptake.svg"; else echo "   DIFF  uptake.svg"; fail=1; fi

echo "4. reads: queries and rows read against the brief's ceilings (600 queries, 60 billion rows)"
"$PY" - "$HERE/data/read_log.csv" <<'PYEOF'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1])))
ck = [r for r in rows if r['source'].startswith('ClickPy')]
n = sum(int(r['read_rows'] or 0) for r in ck)
print(f"   ClickPy queries {len(ck)}, rows read {n:,}; PyPI JSON {sum(r['source'] == 'PyPI JSON API' for r in rows)}; "
      f"sdists {sum(r['source'] == 'files.pythonhosted.org' for r in rows)}; pypistats {sum(r['source'] == 'pypistats.org' for r in rows)}")
sys.exit(0 if len(ck) <= 600 and n <= 60_000_000_000 else 1)
PYEOF
[ $? -eq 0 ] || fail=1

echo "5. readings made after the counts (post hoc): draw_piece_figure.py and post_hoc.py"
ROOT=$(cd "$HERE/../.." && pwd)
LH011_OUT="$TMP/analysis" "$PY" "$HERE/scripts/draw_piece_figure.py" "$TMP/two-days-for-most.svg" > "$TMP/piece_figure_reading.txt" 2>/dev/null || { echo "draw_piece_figure.py failed"; exit 1; }
LH011_OUT="$TMP/analysis" "$PY" "$HERE/scripts/post_hoc.py" > "$TMP/post_hoc_reading.txt" || { echo "post_hoc.py failed"; exit 1; }
for pair in "piece_figure_reading.txt:$HERE/data/piece_figure_reading.txt" "post_hoc_reading.txt:$HERE/data/post_hoc_reading.txt" "two-days-for-most.svg:$ROOT/articles/two-days-for-most.svg"; do
  f=${pair%%:*}; target=${pair#*:}
  if cmp -s "$TMP/$f" "$target"; then echo "   same  $f"
  elif [ "${1:-}" = "--write" ]; then cp "$TMP/$f" "$target"; echo "   changed, rewritten: $f"
  else echo "   DIFF  $f"; fail=1; fi
done

echo "6. the checks behind version 0.4 (post hoc): review/v04_checks.py"
LH011_OUT="$TMP/analysis" "$PY" "$HERE/review/v04_checks.py" > "$TMP/v04_checks.txt" || { echo "v04_checks.py failed"; exit 1; }
if cmp -s "$TMP/v04_checks.txt" "$HERE/review/v04_checks.txt"; then echo "   same  review/v04_checks.txt"; else echo "   DIFF  review/v04_checks.txt"; fail=1; fi

if [ "${1:-}" = "--write" ]; then cp "$TMP"/analysis/*.csv "$HERE/data/analysis/" && cp "$TMP/uptake.svg" "$HERE/uptake.svg"; fi
if [ $fail -ne 0 ]; then echo "REPLAY FAILED"; exit 1; fi
echo "REPLAY PASSED"
