#!/bin/sh
# LH012 offline replay, as studies/LH011/replay.sh. No network, no key. Python 3 with the `packaging`
# library (24.0 was used).
#   sh studies/LH012/replay.sh           regenerate into a temporary directory and compare with data/
#   sh studies/LH012/replay.sh --write   also rewrite data/analysis/ and the figure in place
# Exits non-zero if the snapshot does not verify, if any table differs, or if the reads pass a ceiling.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0

echo "1. snapshot: the brief and phase 1 files against the hashes posted on issue #14 (06:35 UTC, 29 September 2026)"
# sources.md may grow after the snapshot: its part before "## Added after the snapshot" is what was hashed
(cd "$HERE" && grep -v ' sources.md$' data/snapshot_sha256.txt | sha256sum -c -) > "$TMP/sha.log" 2>&1 && echo "   all $(grep -c ': OK' "$TMP/sha.log") files other than sources.md verify" || { echo "   SNAPSHOT DOES NOT VERIFY"; cat "$TMP/sha.log"; fail=1; }
"$PY" - "$HERE/sources.md" "$HERE/data/snapshot_sha256.txt" <<'PYEOF' || fail=1
import hashlib, sys
s = open(sys.argv[1], 'rb').read()
i = s.find(b'\n## Added after the snapshot')
want = [l.split()[0] for l in open(sys.argv[2]) if l.strip().endswith(' sources.md')][0]
ok = hashlib.sha256(s[:i] if i >= 0 else s).hexdigest() == want
print('   sources.md, the part before its phase 2 section:', 'verifies' if ok else 'DOES NOT VERIFY')
sys.exit(0 if ok else 1)
PYEOF

echo "2. frame: frame.py from versions.csv, requirements.csv and LH011's releases"
LH012_OUT="$TMP/frame" "$PY" "$HERE/scripts/frame.py" > "$TMP/frame.log" || { echo "frame.py failed"; cat "$TMP/frame.log"; exit 1; }
for f in reference python_admission pairs releases_nov_mar; do
  if cmp -s "$TMP/frame/$f.csv" "$HERE/data/$f.csv"; then echo "   same  data/$f.csv"; else echo "   DIFF  data/$f.csv"; fail=1; fi
done

echo "3. analysis: analyse.py over data/week, data/deps, data/firstday and the requirements"
LH012_OUT="$TMP/analysis" "$PY" "$HERE/scripts/analyse.py" > "$TMP/analyse.log" || { echo "analyse.py failed"; cat "$TMP/analyse.log"; exit 1; }
for p in "$TMP"/analysis/*.csv; do
  f=$(basename "$p")
  if cmp -s "$p" "$HERE/data/analysis/$f"; then echo "   same  data/analysis/$f"
  elif [ "${1:-}" = "--write" ]; then cp "$p" "$HERE/data/analysis/$f"; echo "   changed, rewritten: data/analysis/$f"
  else echo "   DIFF  data/analysis/$f"; fail=1; fi
done
for p in "$HERE"/data/analysis/*.csv; do
  f=$(basename "$p"); [ -e "$TMP/analysis/$f" ] || { echo "   MISSING  data/analysis/$f"; fail=1; }
done

echo "4. figure: draw_figure.py"
LH012_OUT="$TMP/analysis" "$PY" "$HERE/scripts/draw_figure.py" "$TMP/older.svg" > /dev/null || { echo "draw_figure.py failed"; exit 1; }
if cmp -s "$TMP/older.svg" "$HERE/older.svg"; then echo "   same  older.svg"; elif [ "${1:-}" = "--write" ]; then cp "$TMP/older.svg" "$HERE/older.svg"; echo "   changed, rewritten: older.svg"; else echo "   DIFF  older.svg"; fail=1; fi

echo "5. reads: both logs against the brief's ceilings (900 queries, 40 billion rows, 5,000 PyPI requests, 30 page reads)"
"$PY" - "$HERE/data/read_log.csv" "$HERE/data/read_log_phase2.csv" <<'PYEOF'
import csv, sys
rows = [r for f in sys.argv[1:] for r in csv.DictReader(open(f))]
ck = [r for r in rows if r['source'].startswith('ClickPy')]
n = sum(int(r['read_rows'] or 0) for r in ck)
pj = sum(r['source'] == 'PyPI JSON API' for r in rows)
pages = sum(r['source'] == 'Documentation and literature' for r in rows) + 2  # two web searches, not logged
print(f"   ClickPy queries {len(ck)}, rows read {n:,}; PyPI JSON {pj}; source archives "
      f"{sum(r['source'].startswith('PyPI source') for r in rows)}; page reads and searches {pages}")
sys.exit(0 if len(ck) <= 900 and n <= 40_000_000_000 and pj <= 5000 and pages <= 30 else 1)
PYEOF
[ $? -eq 0 ] || fail=1

echo "6. readings made after the counts (post hoc): post_hoc.py"
"$PY" "$HERE/scripts/post_hoc.py" > "$TMP/post_hoc_reading.txt" || { echo "post_hoc.py failed"; exit 1; }
if cmp -s "$TMP/post_hoc_reading.txt" "$HERE/data/post_hoc_reading.txt"; then echo "   same  data/post_hoc_reading.txt"; else echo "   DIFF  data/post_hoc_reading.txt"; fail=1; fi

echo "7. the piece's figure and the writer's checks (added by the driving session; the checks are post hoc): draw_piece_figure.py, driver_checks.py"
LH012_OUT="$TMP/analysis" "$PY" "$HERE/scripts/draw_piece_figure.py" "$TMP/piece.svg" > /dev/null || { echo "draw_piece_figure.py failed"; exit 1; }
if cmp -s "$TMP/piece.svg" "$HERE/../../articles/old-versions-new-pythons.svg"; then echo "   same  articles/old-versions-new-pythons.svg"; else echo "   DIFF  articles/old-versions-new-pythons.svg"; fail=1; fi
"$PY" "$HERE/scripts/driver_checks.py" > "$TMP/driver_checks.txt" || { echo "driver_checks.py failed"; exit 1; }
if cmp -s "$TMP/driver_checks.txt" "$HERE/data/driver/driver_checks.txt"; then echo "   same  data/driver/driver_checks.txt"; else echo "   DIFF  data/driver/driver_checks.txt"; fail=1; fi

echo "8. the check behind version 0.4 (post hoc): review/v04_checks.py"
"$PY" "$HERE/review/v04_checks.py" > "$TMP/v04_checks.txt" || { echo "v04_checks.py failed"; exit 1; }
if cmp -s "$TMP/v04_checks.txt" "$HERE/review/v04_checks.txt"; then echo "   same  review/v04_checks.txt"; else echo "   DIFF  review/v04_checks.txt"; fail=1; fi

[ $fail -eq 0 ] && echo "replay passed" || echo "replay FAILED"
exit $fail
