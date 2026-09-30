#!/bin/sh
# LH017 replay, offline: the frame's hashes, the rules' tests, the classification from the stored records, and every
# measure; each output is compared byte for byte with the committed one. judgements.csv and review_sample.csv (drawn
# before the blind check and kept as drawn) are inputs.
set -e
cd "$(dirname "$0")"
S=scripts
OUT=$(mktemp -d)
python3 $S/frame.py > /dev/null
python3 $S/test_classify.py | tail -n 1
for f in job_classes.csv doc_classes.csv pair_classes.csv file_facts.csv review_sample_redraw.txt pairs.csv not_read.csv measures.csv described.csv \
         beside_lh015.csv beside_lh015_shares.csv sensitivities.csv s1_mechanisms.csv s2_log.csv s3_triggers.csv \
         s4_container.csv s5_docs.csv s6_moves.csv; do
  cp data/$f "$OUT/$f"
done
python3 $S/classify.py > /dev/null
python3 $S/analyse.py > /dev/null
bad=0
for f in "$OUT"/*; do
  b=$(basename "$f")
  if cmp -s "$f" "data/$b"; then echo "same: $b"; else echo "DIFFERS: $b"; bad=1; fi
done
echo "brief SHA-256: $(sha256sum brief.md | cut -d' ' -f1) (posted on issue #19: fc17c66e91cbe32832c775545999e9fb108268f1693ee9d2f05cf5a5ee9cbf53)"
python3 - <<'PY'
import csv
rows = list(csv.DictReader(open('data/read_log.csv')))
clones = sum(1 for r in rows if r['method'].startswith('git clone'))
shows = sum(1 for r in rows if r['method'] == 'git show')
gets = sum(1 for r in rows if r['method'] == 'GET' and 'pypi.org/pypi/' in r['endpoint'] and 'hatch-pip-compile' not in r['endpoint'])
size = sum(int(r['bytes'] or 0) for r in rows if r['method'].startswith('git clone'))
print(f'ceilings: {clones} clone attempts (664), {size / 1e9:.2f} GB cloned (8 GB), {shows} git show reads (20,000), {gets} PyPI requests (60)')
PY
exit $bad
