#!/usr/bin/env python3
"""R-0026, stage A: compare the reviewer's blind classes (r0026_blind.csv) with the writer's final classes
(data/job_classes.csv), per job and per resulting pair class, and recompute every pair class from the job table
as a check of the pair rule. Run from the repository root: python3 studies/LH017/review/r0026_blind_compare.py
> studies/LH017/review/r0026_blind_compare.txt. Reads only; writes nothing to data/."""
import csv
import sys
from collections import Counter, defaultdict

csv.field_size_limit(10 ** 9)
D = 'studies/LH017/data/'
sample = list(csv.DictReader(open(D + 'review_sample.csv')))
mine = {r['job_key']: r for r in csv.DictReader(open('studies/LH017/review/r0026_blind.csv'))}
jobs = list(csv.DictReader(open(D + 'job_classes.csv')))
jc = {r['job_key']: r for r in jobs}
pc = {r['pair_id']: r for r in csv.DictReader(open(D + 'pair_classes.csv'))}

# The reviewer's resolution of each disagreement, by the brief's rules (see notes/R-0026.md, Stage A).
RESOLUTION = {
    'github.com/galaxyproject/galaxy@bbac30d66bac:.github/workflows/tool_form_harness.yaml#test~1':
        ('writer stands (class 6), sub-label wrong',
         'common_startup.sh, the level read, runs `${PIP_CMD} install -r requirements.txt -r dev-requirements.txt`; '
         'PIP_CMD is assigned once literally and once from a command substitution, so by the letter the deciding '
         'value is one the rules cannot substitute: class 6 stands, but its reason is "build argument", not the '
         'depth-2 source; by the question\'s own test every branch reads T (pinned-requirements.txt through the '
         'root requirements.txt include, and dev-requirements.txt). Not counted as wrong. No pair effect: P163 '
         'reads the pin and the timed lock through other jobs.'),
    'github.com/phenobarbital/ai-parrot@dd4c70085cf5:.github/workflows/ci.yml#test-tools~2':
        ('reviewer right (class 1), script wrong',
         '`uv sync --package ai-parrot-tools` with no uv.lock resolves the workspace afresh; ai-parrot-tools '
         'depends on the workspace member ai-parrot, whose manifest packages/ai-parrot/pyproject.toml is in T '
         'and pins urllib3==2.6.3 in [project] dependencies; the script took the root pyproject.toml as the '
         'manifest and never followed --package to the member. The brief\'s rules do not name --package, so '
         'the case falls to the question\'s own test and to an amendment. Counted as wrong. Pair effect: P327 '
         'becomes "reads the pin" (its other jobs are `uv sync --package ai-parrot`, the T manifest\'s own '
         'project, and class 5 jobs).'),
    'github.com/asozialesnetzwerk/an-website@7a5038611dad:.github/workflows/deploy.yml#test-zipapp~2':
        ('reviewer right (class 4), script wrong',
         'the step runs `grep "^pytest-" pip-constraints.txt | xargs pip install -c pip-constraints.txt html5lib '
         'pytest time-machine`: pip runs, so it is an install step; pip-constraints.txt, not in T, pins '
         'pillow==12.1.1, so class 4 (another pinned file), as the writer judged the same construct in '
         'github-pages (`pip install -c pip-constraints.txt coverage`). The script\'s command splitter does not '
         'look past `xargs` and saw no installer ("no Python install"). Counted as wrong. No pair effect: P051 '
         'reads the pin through test-distribution.'),
    'github.com/asozialesnetzwerk/an-website@d0ff5122f7de:.github/workflows/deploy.yml#build-source-tarball~1':
        ('reviewer right (class 2), writer wrong',
         '`pip install --no-deps .` installs the project and no dependency, so no version of aiohttp is taken '
         'from any file; the judgement read the manifest (setup.py reads pip-requirements.txt) and did not weigh '
         '--no-deps, which the script itself treats as installing no requirement elsewhere (ci.py, project()). '
         'Class 2 (lock unused) by the letter of the sub-labels. Counted as wrong. No pair effect: P050 reads '
         'the pin through test-distribution.'),
}


def pair_class(classes, locks):
    """The brief's pair rule and lock rule from a list of job classes and, for class 1 jobs, whether a T lock decided."""
    if not classes:
        return 'no CI', ''
    if 1 in classes:
        mixed = any(c in (2, 3, 4) for c in classes)
        pcl = 'reads the pin' + (' (mixed)' if mixed else '')
    elif 6 in classes:
        pcl = 'undetermined'
    elif any(c in (2, 3, 4) for c in classes):
        pcl = 'does not read the pin'
    else:
        pcl = "nothing of the project's requirements"
    if any(l for l in locks):
        lock = 'reads the timed lock'
    elif 6 in classes and not any(c in (1, 2, 3, 4) for c in classes):
        lock = 'undetermined'
    elif 6 in classes:
        lock = 'undetermined'
    elif any(c in (1, 2, 3, 4) for c in classes):
        lock = 'does not'
    else:
        lock = 'outside'
    return pcl, lock


print('R-0026 stage A: blind classes against the writer\'s final classes\n')
agree = Counter()
n = Counter()
diffs = []
for s in sample:
    k = s['job_key']
    w = jc[k]
    m = mine[k]
    g = s['group']
    n[g] += 1
    same_class = int(m['class']) == int(w['final_class'])
    same_sub = (m['sub_label'] or '') == (w['final_sub'] or '') or (int(m['class']) == 1 and (m['sub_label'] in ('', 'may re-lock')))
    same_lock = (m['T_lock'] or 'no') == (w['T_lock'] or 'no')
    agree[g, 'class'] += same_class
    agree[g, 'class+sub'] += same_class and same_sub
    agree[g, 'class+sub+lock'] += same_class and same_sub and same_lock
    if not (same_class and same_sub and same_lock):
        diffs.append((s, w, m, same_class))
for g in ('script-decided', 'judged'):
    print(f'{g}: class agreement {agree[g, "class"]}/{n[g]}; class and sub-label {agree[g, "class+sub"]}/{n[g]}; '
          f'with T_lock {agree[g, "class+sub+lock"]}/{n[g]}')
print()
print('Disagreements (class, or sub-label, or T_lock):')
wrong = Counter()
for s, w, m, same_class in diffs:
    k = s['job_key']
    print(f'- [{s["group"]}] {s["pair_id"]} {k}')
    print(f'    reviewer: class {m["class"]} / {m["sub_label"] or "-"} / T_lock {m["T_lock"] or "-"}')
    print(f'    writer:   class {w["final_class"]} / {w["final_sub"] or "-"} / T_lock {w["T_lock"]} (decided by {w["decided_by"]})')
    print(f'    writer\'s reason: {(w["judge_reason"] or w["script_reason"] or "-")[:200]}')
    print(f'    reviewer\'s reason: {m["reason"][:400]}')
    if k in RESOLUTION:
        verdict, why = RESOLUTION[k]
        print(f'    resolution: {verdict}. {why}')
        if 'wrong' in verdict and 'stands' not in verdict:
            wrong[s['group']] += 1
    elif not same_class:
        print('    resolution: (unresolved)')
    else:
        print('    resolution: sub-label difference only; the brief ranks class 6 reasons in no order.')
print()
print(f'Wrong after resolution: script-decided {wrong["script-decided"]} of 20 (threshold: more than 2 corrects the script); '
      f'judged {wrong["judged"]} of 20 (threshold: more than 2 that change a pair class triggers re-judging).')

# Per resulting pair class: substitute the reviewer's classes for the sampled jobs.
print('\nPer resulting pair class (reviewer\'s classes substituted for the sampled jobs, writer\'s for the rest):')
by_pair = defaultdict(list)
for r in jobs:
    by_pair[r['pair_id']].append(r)
sampled_pairs = sorted({s['pair_id'] for s in sample})
pair_agree = 0
pair_changes = []
for p in sampled_pairs:
    rows = by_pair[p]
    wc = [int(r['final_class']) for r in rows]
    wl = [int(r['final_class']) == 1 and r['T_lock'] == 'yes' for r in rows]
    rc = [int(mine[r['job_key']]['class']) if r['job_key'] in mine else int(r['final_class']) for r in rows]
    rl = [(c == 1 and ((mine[r['job_key']]['T_lock'] == 'yes') if r['job_key'] in mine else r['T_lock'] == 'yes'))
          for c, r in zip(rc, rows)]
    wp = pair_class(wc, wl)
    rp = pair_class(rc, rl)
    rec = pc[p]
    recorded = (rec['pair_class'] + (' (mixed)' if rec['pair_sub'] == 'mixed' else ''), rec['lock_class'])
    has_lock = rec['pin_class'] in ('lockfile', 'both')
    same = wp[0] == rp[0] and (not has_lock or wp[1] == rp[1])
    pair_agree += same
    flag = '' if same else '  <<< pair class would change'
    print(f'  {p} {rec["repo"]} {rec["library"]} ({rec["pin_class"]}): writer {wp[0]}' +
          (f', lock {wp[1]}' if has_lock else '') + f'; reviewer {rp[0]}' + (f', lock {rp[1]}' if has_lock else '') + flag)
    if wp != (recorded[0], recorded[1] if has_lock else wp[1]) and (wp[0] != recorded[0] or (has_lock and wp[1] != recorded[1])):
        print(f'     NOTE recorded pair_classes.csv says {recorded}, recomputed from job_classes.csv {wp}')
    if not same:
        pair_changes.append(p)
print(f'Pair-class agreement: {pair_agree}/{len(sampled_pairs)} sampled pairs; changed: {pair_changes or "none"}')

# Check of the pair rule over every pair: recompute from job_classes.csv and compare with pair_classes.csv.
print('\nPair rule check over all pairs (recomputed from job_classes.csv against pair_classes.csv):')
bad = 0
for p, rec in pc.items():
    rows = by_pair.get(p, [])
    wc = [int(r['final_class']) for r in rows]
    wl = [int(r['final_class']) == 1 and r['T_lock'] == 'yes' for r in rows]
    wp = pair_class(wc, wl)
    want_class = rec['pair_class'] + (' (mixed)' if rec['pair_sub'] == 'mixed' else '')
    has_lock = rec['pin_class'] in ('lockfile', 'both')
    want_lock = rec['lock_class'] if has_lock else ''
    got_lock = wp[1] if has_lock else ''
    if not has_lock:
        got_lock = ''
    # pairs with no CI or nothing of the requirements are "outside" for the lock
    if has_lock and wp[0] == "nothing of the project's requirements":
        got_lock = 'outside'
    if has_lock and wp[0] == 'no CI':
        got_lock = ''
    if want_class != wp[0] or want_lock != got_lock:
        bad += 1
        if bad <= 10:
            print(f'  MISMATCH {p}: recorded ({want_class}, {want_lock}) recomputed ({wp[0]}, {got_lock}) classes={wc}')
print(f'  mismatches: {bad} of {len(pc)} pairs')
print('  pair classes recorded:', dict(Counter(r['pair_class'] for r in pc.values())))
