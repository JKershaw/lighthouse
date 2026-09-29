#!/bin/sh
# LH014 offline replay, on the model of studies/LH011/replay.sh. No network, no key. Python 3 with the
# `packaging` library (PEP 440; 24.0 was used).
#   sh studies/LH014/replay.sh           regenerate into a temporary directory and compare with data/
#   sh studies/LH014/replay.sh --write   also rewrite data/analysis/ and uptake.svg in place
# 1 checks brief.md against snapshot_sha256.txt, and amendments.md's first amendment (the text before
# any "## Amendment 2") against the SHA-256 posted on issue #16 and committed at 514f4bd; 2 reruns the
# frame (frame.py --list, then frame.py) from the retained reads; 3 reruns analyse.py; 4 redraws the
# figure; 5 checks the read log against the brief's ceilings and the cut. Exits non-zero on any
# difference.
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PYTHON:-python3}
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0
same() {  # same <generated> <retained> <label>
  if cmp -s "$1" "$2"; then echo "   same  $3"
  elif [ "${WRITE:-}" = 1 ]; then cp "$1" "$2"; echo "   changed, rewritten: $3"
  else echo "   DIFF  $3"; fail=1; fi
}
[ "${1:-}" = "--write" ] && WRITE=1

echo "1. snapshots: brief.md and amendment 1"
"$PY" - "$HERE" <<'PYEOF' || fail=1
import hashlib, sys, os
h = sys.argv[1]
brief = hashlib.sha256(open(os.path.join(h, 'brief.md'), 'rb').read()).hexdigest()
snap = open(os.path.join(h, 'snapshot_sha256.txt')).read().split()[0]
text = open(os.path.join(h, 'amendments.md'), 'rb').read()
first = text.split(b'\n## Amendment 2')[0]
a1 = hashlib.sha256(first).hexdigest()
ok = brief == snap and a1 == 'ccb7a3460c9574ea933e869462d43ff99e168bd86c0860392559648d2020f7fa'
print(f'   brief.md {"matches" if brief == snap else "DIFFERS from"} the snapshot; amendment 1 '
      f'{"matches" if a1.startswith("ccb7a346") else "DIFFERS from"} ccb7a346...')
sys.exit(0 if ok else 1)
PYEOF

echo "2. frame: frame.py --list and frame.py from the ranking, the PyPI reads and the installer names"
mkdir -p "$TMP/frame"
(cd "$HERE/scripts" && LH014_OUT="$TMP/frame" "$PY" frame.py --list > /dev/null && LH014_OUT="$TMP/frame" "$PY" frame.py > /dev/null) \
  || { echo "frame.py failed"; exit 1; }
for f in frame frame_checks drawn releases releases_first_excluded project_order overlap mirror_installers ranking_comparison; do
  same "$TMP/frame/$f.csv" "$HERE/data/$f.csv" "data/$f.csv"
done

echo "3. analysis: analyse.py over data/daily_totals.csv, counts/, mirror/ and ci/"
mkdir -p "$TMP/analysis"
(cd "$HERE/scripts" && LH014_OUT="$TMP/analysis" "$PY" analyse.py > /dev/null) || { echo "analyse.py failed"; exit 1; }
for p in "$TMP"/analysis/*.csv; do f=$(basename "$p"); same "$p" "$HERE/data/analysis/$f" "data/analysis/$f"; done
for p in "$HERE"/data/analysis/*.csv; do f=$(basename "$p"); [ -e "$TMP/analysis/$f" ] || { echo "   MISSING  data/analysis/$f"; fail=1; }; done

echo "4. figure: draw_figure.py"
(cd "$HERE/scripts" && LH014_OUT="$TMP/analysis" "$PY" draw_figure.py "$TMP/uptake.svg" > /dev/null) || { echo "draw_figure.py failed"; exit 1; }
same "$TMP/uptake.svg" "$HERE/uptake.svg" "uptake.svg"

echo "5. reads: against the brief's ceilings, and no date after 27 September 2026 in any query"
"$PY" - "$HERE/data/read_log.csv" <<'PYEOF' || fail=1
import csv, re, sys
rows = list(csv.DictReader(open(sys.argv[1])))
ck = [r for r in rows if r['source'].startswith('ClickPy')]
n = sum(int(r['read_rows'] or 0) for r in ck)
top = max(int(r['read_rows'] or 0) for r in ck)
py = sum(r['source'].startswith('PyPI JSON') for r in rows)
docs = sum(r['source'].startswith('Documentation') for r in rows)
late = [r['label'] for r in ck if any(d > '2026-09-27' for d in re.findall(r"'(\d{4}-\d{2}-\d{2})'", r['query']))]
bad = [r['label'] for r in ck if not r['http_status'].startswith('200') or '(exception' in r['http_status']]
print(f'   ClickPy {len(ck)} queries of 800, {n:,} rows read of 60,000,000,000 (largest single query {top:,}); '
      f'PyPI JSON {py} of 400; documentation {docs} of 5; queries naming a later day {len(late)}; failed queries {len(bad)}')
sys.exit(0 if len(ck) <= 800 and n <= 60_000_000_000 and top < 1_000_000_000 and py <= 400 and docs <= 5 and not late else 1)
PYEOF

if [ $fail -ne 0 ]; then echo "REPLAY FAILED"; exit 1; fi
echo "REPLAY PASSED"
