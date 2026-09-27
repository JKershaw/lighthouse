#!/bin/sh
# LH010 offline replay (REPLAY.md). No network, no key, standard-library Python 3.
#   sh studies/LH010/replay.sh           check: regenerate into a temporary directory and compare with data/
#   sh studies/LH010/replay.sh --write   also rewrite data/reanalysis/ in place (after a deliberate change)
# Exits non-zero if any table differs or any check fails.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0

echo "1. baseline: analyse.py into $TMP/baseline, compared byte for byte with data/"
LH010_OUT="$TMP/baseline" "$PY" "$HERE/scripts/analyse.py" > "$TMP/analyse.log" || { echo "analyse.py failed"; cat "$TMP/analyse.log"; exit 1; }
for f in lags summary_by_event summary_by_class hazard_by_class library_rates library_unit by_authorship within_library; do
  if cmp -s "$TMP/baseline/$f.csv" "$HERE/data/$f.csv"; then echo "   same  data/$f.csv"; else echo "   DIFF  data/$f.csv"; fail=1; fi
done

echo "   and classes.py, reuse.py and summarise_reads.py, the other offline steps, into $TMP/offline"
LH010_OUT="$TMP/offline" "$PY" "$HERE/scripts/classes.py" > "$TMP/classes.log" || { echo "classes.py failed"; cat "$TMP/classes.log"; exit 1; }
LH010_OUT="$TMP/offline" "$PY" "$HERE/scripts/reuse.py" > "$TMP/reuse.log" || { echo "reuse.py failed"; cat "$TMP/reuse.log"; exit 1; }
LH010_OUT="$TMP/offline" "$PY" "$HERE/scripts/summarise_reads.py" > "$TMP/reads.log" || { echo "summarise_reads.py failed"; exit 1; }
for f in fix_classes reused_screen reused_moves read_summary; do
  if cmp -s "$TMP/offline/$f.csv" "$HERE/data/$f.csv"; then echo "   same  data/$f.csv"; else echo "   DIFF  data/$f.csv"; fail=1; fi
done

echo "2. reanalysis: reanalyse.py into $TMP/reanalysis, compared with data/reanalysis/"
"$PY" "$HERE/scripts/reanalyse.py" --out "$TMP/reanalysis" > "$TMP/reanalyse.log" || { echo "reanalyse.py failed"; cat "$TMP/reanalyse.log"; exit 1; }
for p in "$TMP"/reanalysis/*.csv; do
  f=$(basename "$p")
  if cmp -s "$p" "$HERE/data/reanalysis/$f"; then echo "   same  data/reanalysis/$f"
  elif [ "${1:-}" = "--write" ]; then echo "   new or changed, rewritten: data/reanalysis/$f"
  else echo "   DIFF  data/reanalysis/$f"; fail=1; fi
done
for p in "$HERE"/data/reanalysis/*.csv; do  # a committed table the script no longer writes is a difference too
  f=$(basename "$p")
  [ -e "$TMP/reanalysis/$f" ] || { echo "   MISSING  data/reanalysis/$f was not regenerated"; fail=1; }
done
if [ "${1:-}" = "--write" ]; then
  mkdir -p "$HERE/data/reanalysis" && cp "$TMP"/reanalysis/*.csv "$HERE/data/reanalysis/" && echo "   written to data/reanalysis/"
fi

echo "3. checks: python3 -m unittest (scripts/test_reanalyse.py)"
"$PY" -m unittest discover -s "$HERE/scripts" -p 'test_*.py' || fail=1

if [ $fail -ne 0 ]; then echo "REPLAY FAILED"; exit 1; fi
echo "REPLAY PASSED"
