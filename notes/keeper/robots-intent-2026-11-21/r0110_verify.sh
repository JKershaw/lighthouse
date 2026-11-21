#!/bin/bash
# R-0110: independent re-run of the outputs that records rest on, before and after the removal of kept bodies
# (21 November 2026). Written by the fresh checker; not derived from removal_check.txt's verify.sh.
# A: original scripts on the bodies (worktree at 240e6fb; checkpoint2_extra.py taken from main's 453a50e)
#    against the changed scripts on the derived files (worktree at HEAD).
# B: HEAD's scripts with the removed bodies restored from 240e6fb against HEAD as it is (for scripts that did
#    not exist, or changed for other reasons, at 240e6fb: checkpoint2_extra.py, LH038 timeline/r0105/r0106).
# Usage: bash r0110_verify.sh <empty scratch dir>. Offline; writes only under the scratch dir; removes worktrees.
set -u
R=/home/user/lighthouse; PRE=240e6fb; T=$1
mkdir -p $T/A-pre $T/A-now $T/B-pre $T/B-now
git -C $R worktree add -q --detach $T/wt-pre $PRE
git -C $R worktree add -q --detach $T/wt-now HEAD
git -C $R worktree add -q --detach $T/wt-rest HEAD
git -C $R show 453a50e:studies/LH039/scripts/checkpoint2_extra.py > $T/wt-pre/studies/LH039/scripts/checkpoint2_extra.py
# restore every body deleted since 240e6fb into wt-rest
git -C $R diff --name-only --diff-filter=D $PRE HEAD -- studies > $T/deleted.txt
echo "deleted since $PRE: $(wc -l < $T/deleted.txt)"
(cd $T/wt-pre && tar -cf - -T $T/deleted.txt) | tar -xf - -C $T/wt-rest

runA() {  # $1 tree, $2 out
  cd $1
  for d in studies/LH033/data/read-*; do l=${d#studies/LH033/data/read-}
    python3 -I studies/LH033/scripts/tabulate.py $l > $2/LH033-$l.out 2>&1; echo "rc=$?" >> $2/LH033-$l.out; done
  python3 -I studies/LH034/scripts/tabulate.py > $2/LH034-tab.out 2>&1; cp studies/LH034/data/tables.json $2/LH034-tables.json
  python3 -I studies/LH034/review/R-0039_checks.py 2>&1 | sed -E "s#$1#TREE#g; s#line [0-9]+, in <module>#line N, in <module>#" > $2/LH034-R0039.out
  (cd studies/LH035 && python3 -I scripts/reread_check.py > $2/LH035-reread.out 2>&1; cp data/reads-2026-11-06/quote_check.json $2/LH035-quote_check.json)
  python3 -I studies/LH036/scripts/tabulate.py > $2/LH036-tab.out 2>&1; cp studies/LH036/data/tables.json $2/LH036-tables.json
  PYTHONHASHSEED=0 python3 studies/LH036/review/check_fixes.py > $2/LH036-check_fixes.out 2>&1
  python3 -I studies/LH038/review/r0091_check.py 2>&1 | sed "s#$1#TREE#g" > $2/LH038-r0091.out
  for p in 2026-11-14T1415Z:2026-11-14T1412Z 2026-11-21T1415Z:2026-11-21T1411Z; do
    python3 -I studies/LH039/scripts/tabulate.py --packagist ${p%%:*} --until ${p##*:} --out $2/LH039-${p%%:*} > $2/LH039-${p%%:*}.stdout 2>&1; done
  python3 -I studies/LH039/scripts/checkpoint2_extra.py > $2/LH039-cp2extra.stdout 2>&1; cp studies/LH039/checkpoints/2026-11-21-extra.txt $2/LH039-cp2extra.txt
  python3 -I studies/LH040/scripts/tabulate.py --read 2026-11-09T1432Z > $2/LH040-tab.out 2>&1; cp -r studies/LH040/tables $2/LH040-tables
}
runB() {
  cd $1
  python3 -I studies/LH039/scripts/checkpoint2_extra.py > $2/LH039-cp2extra.stdout 2>&1; cp studies/LH039/checkpoints/2026-11-21-extra.txt $2/LH039-cp2extra.txt
  for s in scripts/timeline.py review/r0105_check.py review/r0106_offsets.py; do
    python3 -I studies/LH038/$s 2>&1 | sed "s#$1#TREE#g" > $2/LH038-$(basename $s .py).out; done
}
runA $T/wt-pre $T/A-pre; runA $T/wt-now $T/A-now
runB $T/wt-rest $T/B-pre; runB $T/wt-now $T/B-now
for x in A B; do cd $T; for f in $(ls $x-pre); do
  if diff -r -q $x-pre/$f $x-now/$f > /dev/null; then echo "$x identical  $f"; else echo "$x DIFFERS    $f"; diff -r $x-pre/$f $x-now/$f | cut -c1-200 | head -8; fi
done; done
# the retained checkpoint files against the HEAD run
for f in 2026-11-21-extra.txt; do cmp -s $T/A-now/LH039-cp2extra.txt $R/studies/LH039/checkpoints/$f && echo "retained $f identical to HEAD run"; done
cmp -s $T/A-now/LH039-2026-11-21T1415Z-tabulation.txt $R/studies/LH039/checkpoints/2026-11-21-tabulation.txt && echo "retained 2026-11-21-tabulation.txt identical to HEAD run"
cmp -s $T/B-now/LH038-timeline.out $R/studies/LH038/scripts/timeline_output.txt && echo "retained timeline_output.txt identical to HEAD run"
for w in wt-pre wt-now wt-rest; do git -C $R worktree remove --force $T/$w; done
git -C $R worktree prune
