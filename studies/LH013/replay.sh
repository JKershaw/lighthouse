#!/bin/sh
# LH013 offline replay, as studies/LH012/replay.sh. No network, no key. Python 3 with `packaging` (24.0 was used).
#   sh studies/LH013/replay.sh     regenerate into a temporary directory and compare byte for byte with data/ and the figure
# Exits non-zero if a hash does not verify, any output differs, or the reads pass a ceiling.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0

echo "1. hashes: the brief against issue #15's snapshot, and the files hashed before any count (data/pre_counts_sha256.txt)"
# The robots-sweep amendment of 9 November 2026 (appended to brief.md) changed brief.md, by appending it, and
# scripts/collect.py, common.py and preflight.py, after the counts; their pre-count versions are at commit 4c9b77c^.
# So the brief is verified up to that amendment, and those three scripts are listed, not verified (fixed 19 November 2026).
want=$(grep '  studies/LH013/brief.md$' "$HERE/snapshot_sha256.txt" | cut -d' ' -f1)
got=$("$PY" -c "import hashlib,sys; s=open(sys.argv[1],'rb').read(); i=s.find(b'\n- **Amendment, 9 November 2026'); print(hashlib.sha256(s if i < 0 else s[:i]).hexdigest())" "$HERE/brief.md")
[ "$want" = "$got" ] && echo "   brief.md verifies (text before the amendment of 9 November 2026)" || { echo "   brief.md DOES NOT VERIFY"; fail=1; }
AMENDED='scripts/collect.py|scripts/common.py|scripts/preflight.py'
(cd "$HERE" && grep -v '^#' data/pre_counts_sha256.txt | grep -Ev "  ($AMENDED)\$" | sha256sum -c -) > "$TMP/sha.log" 2>&1 && echo "   $(grep -c ': OK' "$TMP/sha.log") pre-count files verify; collect.py, common.py and preflight.py changed by the 9 November amendment, not verified" || { echo "   PRE-COUNT FILES DO NOT VERIFY"; cat "$TMP/sha.log"; fail=1; }

echo "2. frame, gap rule and baseline check: frame.py, gaps.py, w0check.py"
mkdir -p "$TMP/out/analysis"
LH013_OUT="$TMP/out" "$PY" "$HERE/scripts/frame.py" > /dev/null || { echo "frame.py failed"; exit 1; }
LH013_OUT="$TMP/out" "$PY" "$HERE/scripts/gaps.py" > /dev/null || { echo "gaps.py failed"; exit 1; }
LH013_OUT="$TMP/out" "$PY" "$HERE/scripts/w0check.py" > /dev/null || { echo "w0check.py failed"; exit 1; }
for f in frame/reference.csv frame/classes.csv frame/python_admission.csv frame/metadata_changes.csv analysis/gaps.csv analysis/w0_check.csv; do
  if cmp -s "$TMP/out/$f" "$HERE/data/$f"; then echo "   same  data/$f"; else echo "   DIFF  data/$f"; fail=1; fi
done

echo "3. analysis: analyse.py"
LH013_OUT="$TMP/out" "$PY" "$HERE/scripts/analyse.py" > /dev/null || { echo "analyse.py failed"; exit 1; }
for p in "$HERE"/data/analysis/*; do
  f=$(basename "$p")
  if cmp -s "$TMP/out/analysis/$f" "$p"; then echo "   same  data/analysis/$f"; else echo "   DIFF  data/analysis/$f"; fail=1; fi
done

echo "4. readings made after the counts (post hoc) and the figure: post_hoc.py, draw_figure.py"
"$PY" "$HERE/scripts/post_hoc.py" > "$TMP/post_hoc_reading.txt" || { echo "post_hoc.py failed"; exit 1; }
cmp -s "$TMP/post_hoc_reading.txt" "$HERE/data/post_hoc_reading.txt" && echo "   same  data/post_hoc_reading.txt" || { echo "   DIFF  data/post_hoc_reading.txt"; fail=1; }
LH013_OUT="$TMP/out" "$PY" "$HERE/scripts/draw_figure.py" "$TMP/fig.svg" || { echo "draw_figure.py failed"; exit 1; }
cmp -s "$TMP/fig.svg" "$HERE/older_three_weeks.svg" && echo "   same  older_three_weeks.svg" || { echo "   DIFF  older_three_weeks.svg"; fail=1; }

echo "5. reads against the brief's ceilings (300 ClickPy queries, 30 billion rows, 300 PyPI JSON requests, 5 page reads)"
"$PY" - "$HERE/data/read_log.csv" <<'PYEOF'
import csv, sys
rows = list(csv.DictReader(open(sys.argv[1])))
ck = [r for r in rows if r['source'].startswith('ClickPy')]
n = sum(int(r['read_rows'] or 0) for r in ck)
pj = sum(r['source'] == 'PyPI JSON API' for r in rows)
pg = sum(r['source'] == 'Documentation' for r in rows)
print(f"   ClickPy queries {len(ck)}, rows read {n:,}; PyPI JSON {pj}; page reads {pg}")
sys.exit(0 if len(ck) <= 300 and n <= 30_000_000_000 and pj <= 300 and pg <= 5 else 1)
PYEOF
[ $? -eq 0 ] || fail=1
[ $fail -eq 0 ] && echo "replay passed" || echo "replay FAILED"
exit $fail
