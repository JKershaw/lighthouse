#!/bin/sh
# LH015 replay, offline: frame, classifier tests, classes and measures, compared byte for byte with the retained data;
# the logs checked against the brief's ceilings, and the brief against its committed hash. judgements.csv and pypi.csv are inputs.
set -e
cd "$(dirname "$0")"
echo "df7f7647b73913199c3a8fe8a655e844b14efafeec2b444f9b646c631e879395  brief.md" | sha256sum -c -
T=$(mktemp -d)
LH015_OUT=$T/frame python3 scripts/frame.py > /dev/null
for f in frame.csv frame_files.csv frame_counts.csv; do cmp -s data/$f $T/frame/$f || { echo "DIFFERS: $f"; exit 1; }; done
python3 scripts/test_classify.py | tail -1
mkdir -p $T/data
for f in frame.csv frame_files.csv pairs_read.csv recipes.csv recipe_lines.csv aux_lines.csv tree_paths.csv judgements.csv pypi.csv; do
  cp data/$f $T/data/; done
LH015_DATA=$T/data python3 scripts/classify.py > /dev/null
LH015_DATA=$T/data python3 scripts/analyse.py > /dev/null
for f in recipe_classes.csv review_sample.csv pair_classes.csv not_read.csv measures.csv described.csv sensitivities.csv \
         s1_fresh_build.csv s2_head.csv s3_moves.csv s4_mechanisms.csv; do cmp -s data/$f $T/data/$f || { echo "DIFFERS: $f"; exit 1; }; done
python3 - <<'PY'
import csv
rows = list(csv.DictReader(open('data/read_log.csv')))
clones = sum(r['method'].startswith('git clone') for r in rows)
shows = sum(r['method'] == 'git show' for r in rows)
pypi = sum(r['source'] == 'PyPI JSON API' for r in rows)
last = {}
for r in rows:
    if r['status'] == 'size after reads':
        last[r['repo']] = int(r['bytes'])
total = sum(last.values())
print(f'clone attempts {clones} (ceiling 664); git show reads {shows} (15,000); PyPI requests {pypi} (150); '
      f'clones after reads {total / 1e9:.2f} GB (6 GB at once, 8 GB in all)')
assert clones <= 664 and shows <= 15000 and pypi <= 150 and total <= 6e9
PY
rm -rf $T
echo "replay: all outputs identical"
