"""LH017 phase 3: the blind sample, then every measure on one set of resamples (brief, "Measures, conventions and
intervals").

Reads data/frame.csv, pairs_read.csv, pair_classes.csv, job_classes.csv, jobs.csv, ci_lines.csv, doc_classes.csv,
judgements.csv and pypi.csv, and LH015's data/pair_classes.csv and recipe_classes.csv (hashes checked); writes
data/review_sample.csv first (before any measure), then pairs.csv, not_read.csv, measures.csv, described.csv,
beside_lh015.csv, sensitivities.csv, s1_mechanisms.csv, s2_log.csv, s3_triggers.csv, s4_container.csv, s5_docs.csv and
s6_moves.csv. Offline and deterministic.
"""
import hashlib
import json
import operator
import os
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F401

SEED, B_N, SALT = 20260930, 10000, 'LH017-review-20260930:'
LH015 = os.path.join(os.path.dirname(STUDY), 'LH015', 'data')
LH015_HASH = {'pair_classes.csv': 'a120c24f5f6f5c640256d4d66ae7ff547cc070f5b9abad75a2cb1c9942eae5d5',
              'recipe_classes.csv': '54d1c7459d87d90ff5bf6b204347632e311c799fa4374dbed49c2755f30cefb0'}
DEC = ('reads the pin', 'does not read the pin')
LDEC = ('reads the timed lock', 'does not')
FLAG_TOOLS = {'pip', 'uv', 'uv pip', 'pipx', 'pip-sync', 'pip-compile', 'piptools', 'pipenv', 'setup.py', 'conda', 'mamba',
              'micromamba', 'tox', 'nox', 'hatch', 'make', 'gmake', 'just', 'call', 'source', 'uvx'}


def pct(xs, p):
    """LH011's percentile, linear interpolation."""
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def rnd(x, k=4):
    return '' if x is None else round(x, k)


def label(x):
    return '' if x is None or x == '' else 'as a rule' if x >= 0.75 else 'for some pairs' if x >= 0.5 else 'not as a rule'


def lh015(name):
    p = os.path.join(LH015, name)
    got = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if got != LH015_HASH[name]:
        sys.exit(f'LH015 {name}: SHA-256 {got} is not the brief\'s {LH015_HASH[name]}')
    return read_csv(name, LH015)


def pair_class_of(classes):
    if not classes:
        return 'no CI'
    if any(c == 1 for c in classes):
        return 'reads the pin'
    if any(c == 6 for c in classes):
        return 'undetermined'
    if any(c in (2, 3, 4) for c in classes):
        return 'does not read the pin'
    return "nothing of the project's requirements"


def lh015_rule(classes):
    """LH015's pair rule applied to CI jobs: from the pinned file only when every other job is class 1 or 5."""
    if not classes:
        return 'no CI'
    if all(c == 5 for c in classes):
        return "nothing of the project's requirements"
    if any(c in (2, 3, 4) for c in classes):
        return 'does not read the pin'
    if any(c == 1 for c in classes):
        return 'reads the pin'
    return 'undetermined'


def lock_of(rows):
    if any(r['c'] == 1 and r['T_lock'] == 'yes' for r in rows):
        return 'reads the timed lock'
    if any(r['c'] == 6 for r in rows):
        return 'undetermined'
    if any(r['c'] in (1, 2, 3, 4) for r in rows):
        return 'does not'
    return 'outside'


def cache_on(c):
    """An installer cache restored as written: setup-python's cache input, setup-uv's enable-cache unless false (its
    default, "auto", is on for GitHub's runners by its README), or an actions/cache step whose path holds an installer
    cache (brief, S2)."""
    parts = [p.strip() for p in (c or '').split('|') if p.strip()]
    return any(not (p.startswith('setup-uv:') and p.split(':', 1)[1].strip().lower() == 'false') for p in parts)


def routine(j):
    t = set((j['triggers'] or '').split())
    if j['system'] == 'gitlab':
        return True
    if t & {'push', 'pull_request'}:
        return True
    return j.get('inputs_from') == 'call' and bool(set((j.get('caller_triggers') or '').split()) & {'push', 'pull_request'})


def main():
    fr = read_csv('frame.csv')
    fmap = {r['pair_id']: r for r in fr}
    ff = defaultdict(list)
    for r in read_csv('frame_files.csv'):
        ff[r['pair_id']].append(r)
    pr = {r['pair_id']: r for r in read_csv('pairs_read.csv')}
    jc = read_csv('job_classes.csv')
    jobs = {r['job_key']: r for r in read_csv('jobs.csv')}
    pending = [r for r in jc if r['decided_by'] == 'not judged' and r['script_class'] == 'to judge']
    # the writer judges every "to judge" job that could change a pair's class or its reading for the lock (brief, 3)
    by_pair_jobs = defaultdict(list)
    for r in jc:
        by_pair_jobs[r['pair_id']].append(r)
    must = []
    for r in pending:
        rows = by_pair_jobs[r['pair_id']]
        has1 = any(x['final_class'] == '1' for x in rows)
        haslock = any(x['final_class'] == '1' and x['T_lock'] == 'yes' for x in rows)
        lockpair = fmap[r['pair_id']]['pin_class'] in ('lockfile', 'both')
        if not has1 or (lockpair and not haslock):
            must.append(r)
    if must:
        sys.exit(f'{len(must)} jobs still to judge, e.g. {[(m["pair_id"], m["job_key"]) for m in must[:5]]}')

    # ---------------------------------------------------------------- blind sample, before any measure
    lines = defaultdict(list)
    for r in read_csv('ci_lines.csv'):
        lines[r['job_key']].append(r)

    def key(r):
        j = jobs[r['job_key']]
        return hashlib.sha256((SALT + r['pair_id'] + ':' + j['file'] + ':' + j['job'] + ':' + j['variant']).encode()).hexdigest()
    order = sorted(jc, key=lambda r: (key(r), r['job_key']))
    samp = [r for r in order if r['decided_by'] == 'script'][:20] + [r for r in order if r['decided_by'] == 'judged'][:20]
    rows = []
    for r in samp:
        f, j = fmap[r['pair_id']], jobs[r['job_key']]
        txt = []
        cur = None
        for x in lines[r['job_key']]:
            tag = f"[{x['seq']}{'.' + x['sub'] if x['sub'] else ''}]"
            if x['field'] == 'step':
                if x['part'] == '0':
                    txt.append(tag + ' ' + x['text'])
                else:
                    txt[-1] += x['text']
            else:
                if x['part'] == '0':
                    txt.append(tag + ' run> ' + x['text'])
                else:
                    txt[-1] += x['text']
        rows.append({'order_hash': key(r)[:16], 'group': 'script-decided' if r['decided_by'] == 'script' else 'judged',
                     'pair_id': r['pair_id'], 'repo': f['repo'], 'commit': j['commit'], 'file': j['file'], 'job': j['job'],
                     'variant': j['variant'], 'values': j['values'], 'system': j['system'], 'library': f['library'],
                     'T': ' | '.join(f"{x['path']} ({x['pin_class']} {x['versions']})" for x in ff[r['pair_id']]),
                     'pin_class': f['pin_class'], 'own_package': f['package'], 'job_key': r['job_key'],
                     'stored_steps': ' ⏎ '.join(txt)[:30000]})
    # drawn once, before any measure and before the blind check (07:37 UTC, 30 September 2026); kept as drawn thereafter,
    # like judgements.csv, so corrections made after the check do not redraw it (the record says how a redraw would differ)
    if not os.path.exists(os.path.join(DATA, 'review_sample.csv')):
        write_csv('review_sample.csv', rows, list(rows[0].keys()) if rows else ['pair_id'])
    drawn = {(r['pair_id'], r['job_key']) for r in read_csv('review_sample.csv')}
    redraw = {(r['pair_id'], r['job_key']) for r in rows}
    open(os.path.join(DATA, 'review_sample_redraw.txt'), 'w').write(
        f'jobs a redraw by the same rule on the current pools would give that the drawn sample lacks: {len(redraw - drawn)} of {len(redraw)}\n')

    # ---------------------------------------------------------------- pairs
    l15 = {r['pair_id']: r for r in lh015('pair_classes.csv')}
    l15b = defaultdict(list)
    for b in lh015('recipe_classes.csv'):
        if b.get('role', 'snapshot') == 'snapshot':
            l15b[b['pair_id']].append(b)
    out, read_ids, not_read = [], [], []
    for f in fr:
        pid = f['pair_id']
        p = pr.get(pid, {})
        st = p.get('status', 'not read: no row')
        row = {'pair_id': pid, 'repo': f['repo'], 'library': f['library'], 'threshold': f['threshold'], 'pin_class': f['pin_class'],
               'source_study': f['source_study'], 'status': st, 'outcome': f['outcome'], 'lag_release_days': f['lag_release_days']}
        if st != 'read':
            not_read.append(row)
            out.append(row)
            continue
        read_ids.append(pid)
        rs = [{'c': int(r['final_class']), 'sub': r['final_sub'], 'T_lock': r['T_lock'], 'job_key': r['job_key'],
               'flags': r['flags'], 'routine': routine(jobs[r['job_key']]), 'by': r['decided_by']} for r in by_pair_jobs[pid]]
        cls = [r['c'] for r in rs]
        pc = pair_class_of(cls)
        n_other = int(p.get('other_ci_files') or 0)
        l = l15.get(pid, {})
        lock_unused = any(b['class'] == '2' and b.get('sub') == 'lock unused' for b in l15b.get(pid, []))
        row.update({
            'keeps_ci': 'yes' if rs else 'no', 'other_ci_only': 'yes' if not rs and n_other else 'no', 'jobs': len(rs),
            'pair_class': pc, 'mixed': 'yes' if pc == 'reads the pin' and any(c in (2, 3, 4) for c in cls) else 'no',
            'lock_class': lock_of(rs) if f['pin_class'] in ('lockfile', 'both') and rs else '',
            'classes': ' '.join(str(c) for c in sorted(cls)),
            'routine_class': pair_class_of([r['c'] for r in rs if r['routine']]),
            'routine_lock': lock_of([r for r in rs if r['routine']]) if f['pin_class'] in ('lockfile', 'both') and
            any(r['routine'] for r in rs) else '',
            'lh015_rule_class': lh015_rule(cls),
            'relock_class': pair_class_of([2 if (r['c'] == 1 and 'may re-lock' in r['flags']) else r['c'] for r in rs]),
            'relock_lock': lock_of([{**r, 'c': 2 if (r['c'] == 1 and 'may re-lock' in r['flags']) else r['c']} for r in rs])
            if f['pin_class'] in ('lockfile', 'both') and rs else '',
            'conditional_only': 'yes' if pc == 'reads the pin' and all('class rests on a conditional step' in r['flags']
                                                                         for r in rs if r['c'] == 1) else 'no',
            'later_unread': 'yes' if any(r['c'] == 1 and 'later step not read' in r['flags'] for r in rs) else 'no',
            'lh015_class': l.get('pair_class', ''), 'lh015_reads_T_lock': l.get('reads_T_lock', ''),
            'lh015_lock_unused': 'yes' if lock_unused else 'no',
            'judged_jobs': sum(1 for r in rs if r['by'] == 'judged'), 'not_judged_jobs': sum(1 for r in rs if r['by'] == 'not judged'),
        })
        out.append(row)
    fields = list(out[[i for i, r in enumerate(out) if r['status'] == 'read'][0]].keys())
    write_csv('pairs.csv', out, fields)
    write_csv('not_read.csv', not_read, ['pair_id', 'repo', 'library', 'threshold', 'pin_class', 'source_study', 'status'])

    # ---------------------------------------------------------------- resamples of repositories read
    P = {r['pair_id']: r for r in out if r['pair_id'] in read_ids}
    repos = []
    for pid in read_ids:
        if P[pid]['repo'] not in repos:
            repos.append(P[pid]['repo'])
    ri = {r: i for i, r in enumerate(repos)}
    n = len(repos)
    rng = random.Random(SEED)
    counts = []
    for _ in range(B_N):
        c = [0] * n
        for _ in range(n):
            c[rng.randrange(n)] += 1
        counts.append(c)

    def vec(fn, pids):
        num, den, pn = [0] * n, [0] * n, defaultdict(list)
        for pid in pids:
            v = fn(P[pid])
            if v is None:
                continue
            i = ri[P[pid]['repo']]
            num[i] += v
            den[i] += 1
            pn[i].append(v)
        rv = [sum(pn[i]) / len(pn[i]) if pn[i] else 0 for i in range(n)]
        rh = [1 if pn[i] else 0 for i in range(n)]
        return num, den, rv, rh

    def boot(fn, pids=None, name='', view_repo=True):
        pids = pids if pids is not None else read_ids
        num, den, rv, rh = vec(fn, pids)
        res = []
        for view, a, b in (('pairs', num, den), ('repositories', rv, rh)):
            if view == 'repositories' and not view_repo:
                continue
            pt = sum(a) / sum(b) if sum(b) else None
            xs, skipped = [], 0
            for c in counts:
                d = sum(map(operator.mul, c, b))
                if not d:
                    skipped += 1
                    continue
                xs.append(sum(map(operator.mul, c, a)) / d)
            lo, hi = (pct(xs, 0.025), pct(xs, 0.975)) if xs else (None, None)
            res.append({'measure': name, 'view': view, 'num': sum(num) if view == 'pairs' else round(sum(a), 3),
                        'den': sum(den) if view == 'pairs' else sum(b), 'n_repos': sum(rh), 'share': rnd(pt), 'lo': rnd(lo),
                        'hi': rnd(hi), 'skipped': skipped})
        return res

    def p2(col='pair_class', und=None):
        def f(r):
            c = r[col]
            if c == 'undetermined' and und:
                c = und
            if c not in DEC:
                return None
            return 1 if c == DEC[0] else 0
        return f

    def p3(col='lock_class', und=None):
        def f(r):
            c = r[col]
            if c == 'undetermined' and und:
                c = und
            if c not in LDEC:
                return None
            return 1 if c == LDEC[0] else 0
        return f

    by_pc = {pc: [p for p in read_ids if P[p]['pin_class'] == pc] for pc in ('lockfile', 'exact pin', 'both')}
    lkb = [p for p in read_ids if P[p]['pin_class'] in ('lockfile', 'both')]
    measures = []
    measures += boot(lambda r: 1 if r['keeps_ci'] == 'yes' else 0, name='P1 keeps CI')
    measures += boot(p2(), name='P2 reads the pin, all')
    for pc, pp in by_pc.items():
        measures += boot(p2(), pp, name=f'P2 reads the pin, {pc}')
    measures += boot(p3(), lkb, name='P3 reads the timed lock, pairs with a timed lockfile')

    # ---------------------------------------------------------------- sensitivities
    sens = []
    sens += boot(lambda r: 1 if r['keeps_ci'] == 'yes' or r['other_ci_only'] == 'yes' else 0,
                 name='P1, other CI only counted as keeping CI')
    for u in DEC:
        sens += boot(p2(und=u), name=f'P2, undetermined counted as {u}')
        for pc, pp in by_pc.items():
            sens += boot(p2(und=u), pp, name=f'P2, {pc}, undetermined counted as {u}')
    for u in LDEC:
        sens += boot(p3(und=u), lkb, name=f'P3, undetermined counted as {u}')
    sens += boot(p2('routine_class'), name='P2, routine jobs only')
    for pc, pp in by_pc.items():
        sens += boot(p2('routine_class'), pp, name=f'P2, routine jobs only, {pc}')
    sens += boot(p3('routine_lock'), lkb, name='P3, routine jobs only')
    sens += boot(p2('lh015_rule_class'), name='P2, LH015\'s pair rule')
    for pc, pp in by_pc.items():
        sens += boot(p2('lh015_rule_class'), pp, name=f'P2, LH015\'s pair rule, {pc}')
    sens += boot(p2('relock_class'), name='P2, "may re-lock" jobs counted as class 2')
    sens += boot(p3('relock_lock'), lkb, name='P3, "may re-lock" jobs counted as class 2')
    for m in sens:
        m['label'] = label(m['share'])

    # labels: small denominators, the undetermined share, the frame
    ci = [p for p in read_ids if P[p]['keeps_ci'] == 'yes']
    inst = [p for p in ci if P[p]['pair_class'] in DEC + ('undetermined',)]
    und_p2 = sum(1 for p in inst if P[p]['pair_class'] == 'undetermined') / len(inst) if inst else 0
    inst3 = [p for p in lkb if P[p]['lock_class'] in LDEC + ('undetermined',)]
    und_p3 = sum(1 for p in inst3 if P[p]['lock_class'] == 'undetermined') / len(inst3) if inst3 else 0
    for m in measures:
        m['label'] = label(m['share'])
        if m['lo'] != '' and label(m['lo']) != label(m['hi']):
            m['note'] = 'interval spans a label boundary'
        if m['view'] != 'pairs':
            continue
        if m['measure'].startswith(('P2', 'P3')):
            small = (m['den'] < 40 or m['n_repos'] < 25) if m['measure'] == 'P2 reads the pin, all' else \
                (m['den'] < 20 or m['n_repos'] < 12)
            if small:
                m['label'] = ''
                m['note'] = (m.get('note', '') + '; too few pairs or repositories for a label').strip('; ')
    def und_share_p2(pc):
        fr_ = [p for p in inst if pc == 'all' or P[p]['pin_class'] == pc]
        return sum(1 for p in fr_ if P[p]['pair_class'] == 'undetermined') / len(fr_) if fr_ else 0
    for m in measures:
        m['label_as_computed'] = m['label']
        if not m['label'] or not m['measure'].startswith(('P2', 'P3')):
            continue
        if m['measure'].startswith('P2'):
            pc = m['measure'].split(', ', 1)[1]
            share = und_share_p2(pc)     # the undetermined share of this measure's own frame (brief)
            names = [f'P2, undetermined counted as {u}' if pc == 'all' else f'P2, {pc}, undetermined counted as {u}' for u in DEC]
        else:
            share = und_p3
            names = [f'P3, undetermined counted as {u}' for u in LDEC]
        if share > 0.2:
            bounds = [x for x in sens if x['measure'] in names and x['view'] == m['view']]
            if len(bounds) < 2 or any(x['label'] != m['label'] for x in bounds):
                m['label'] = ''
                m['note'] = (m.get('note', '') + f'; label withheld: undetermined pairs are {share:.3f} of the measure\'s frame and '
                             f'the bounds read {" / ".join(x["label"] for x in bounds)}').strip('; ')
    if len(read_ids) < 313:
        for m in measures:
            m['note'] = (m.get('note', '') + '; inconclusive for the frame (fewer than 313 pairs read)').strip('; ')
    write_csv('measures.csv', measures, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'label',
                                         'label_as_computed', 'note', 'skipped'])
    write_csv('sensitivities.csv', sens, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'label', 'skipped'])

    # ---------------------------------------------------------------- described, not tested
    desc = []
    desc.append({'measure': 'undetermined share of pairs whose CI installs the project\'s requirements or is undetermined (P2 frame)',
                 'view': 'pairs', 'num': sum(1 for p in inst if P[p]['pair_class'] == 'undetermined'), 'den': len(inst),
                 'share': rnd(und_p2)})
    for pc in ('lockfile', 'exact pin', 'both'):
        fr_ = [p for p in inst if P[p]['pin_class'] == pc]
        desc.append({'measure': f'undetermined share of the P2 frame, {pc}', 'view': 'pairs',
                     'num': sum(1 for p in fr_ if P[p]['pair_class'] == 'undetermined'), 'den': len(fr_),
                     'share': rnd(sum(1 for p in fr_ if P[p]['pair_class'] == 'undetermined') / len(fr_) if fr_ else None)})
    desc.append({'measure': 'undetermined share of pairs with a timed lockfile in P3\'s frame', 'view': 'pairs',
                 'num': sum(1 for p in inst3 if P[p]['lock_class'] == 'undetermined'), 'den': len(inst3), 'share': rnd(und_p3)})
    for c in ("nothing of the project's requirements", 'undetermined', 'reads the pin', 'does not read the pin'):
        desc += boot(lambda r, c=c: 1 if r['pair_class'] == c else 0, ci, f'share of pairs with CI: {c}', False)
    desc += boot(lambda r: 1 if r['mixed'] == 'yes' else 0, [p for p in ci if P[p]['pair_class'] == 'reads the pin'],
                 'share of pairs that read the pin: mixed (another job class 2 to 4)', False)
    desc += boot(lambda r: 1 if r['conditional_only'] == 'yes' else 0, [p for p in ci if P[p]['pair_class'] == 'reads the pin'],
                 'share of pairs that read the pin: only through steps under a condition', False)
    desc += boot(lambda r: 1 if r['later_unread'] == 'yes' else 0, [p for p in ci if P[p]['pair_class'] == 'reads the pin'],
                 'share of pairs that read the pin: a class 1 job with a later step not read', False)
    lockpairs = [p for p in lkb if P[p]['lock_class']]
    desc.append({'measure': 'pairs with a timed lockfile and CI, by reading for the lock', 'view': 'pairs',
                 'num': json.dumps(Counter(P[p]['lock_class'] for p in lockpairs), sort_keys=True), 'den': len(lockpairs)})
    # either and neither: a container build (LH015 class 1) or a CI job reads the pin
    def either(r):
        return 1 if (r['lh015_class'] == 'from the pinned file' or r['pair_class'] == 'reads the pin') else 0

    def neither(r):
        rec_no = r['lh015_class'] in ('not from the pinned file', "nothing of the project's requirements", 'no recipe')
        ci_no = r['pair_class'] in ('does not read the pin', "nothing of the project's requirements", 'no CI')
        rec_yes = r['lh015_class'] == 'from the pinned file'
        ci_yes = r['pair_class'] == 'reads the pin'
        if rec_yes or ci_yes:
            return 0
        if rec_no and ci_no:
            return 1
        return None
    desc += boot(either, read_ids, 'pairs read where a container build (LH015) or a CI job installs from the pinned file', False)
    desc += boot(neither, read_ids, 'pairs read, decided in both: neither recipe nor CI reads the pin', False)
    und_either = sum(1 for p in read_ids if neither(P[p]) is None)
    desc.append({'measure': 'pairs read not decided for "neither" (a recipe or CI undetermined, neither reading the pin)',
                 'view': 'pairs', 'num': und_either, 'den': len(read_ids)})
    dn = [p for p in read_ids if P[p]['pair_class'] == 'does not read the pin']
    jmap = defaultdict(list)
    for r in jc:
        jmap[r['pair_id']].append(r)
    for k in ('2', '3', '4'):
        desc.append({'measure': f'pairs that do not read the pin with a class {k} job', 'view': 'pairs',
                     'num': sum(1 for p in dn if any(r['final_class'] == k for r in jmap[p])), 'den': len(dn)})
    for s in ('upgrade', 'lock absent', 'lock unused', 'other file', 'inline'):
        desc.append({'measure': f'pairs that do not read the pin with a class 2 job, sub-label {s}', 'view': 'pairs',
                     'num': sum(1 for p in dn if any(r['final_class'] == '2' and r['final_sub'] == s for r in jmap[p])), 'den': len(dn)})
    # per job and per workflow
    readset = set(read_ids)
    djobs = [r for r in jc if r['pair_id'] in readset and r['final_class'] in ('1', '2', '3', '4', '5')]
    desc.append({'measure': 'decided jobs (pair and job) that are class 1', 'view': 'jobs',
                 'num': sum(1 for r in djobs if r['final_class'] == '1'), 'den': len(djobs)})
    inst_jobs = [r for r in djobs if r['final_class'] in ('1', '2', '3', '4')]
    desc.append({'measure': 'decided jobs that install the project\'s requirements (class 1 to 4) and are class 1', 'view': 'jobs',
                 'num': sum(1 for r in inst_jobs if r['final_class'] == '1'), 'den': len(inst_jobs)})
    wf = defaultdict(list)
    for r in jc:
        if r['pair_id'] in readset:
            wf[(r['pair_id'], r['file'])].append(r['final_class'])
    wf_dec = {k: v for k, v in wf.items() if '1' in v or all(c in ('2', '3', '4', '5') for c in v)}
    desc.append({'measure': 'workflows (pair and file) with a class 1 job, among workflows decided', 'view': 'workflows',
                 'num': sum(1 for v in wf_dec.values() if '1' in v), 'den': len(wf_dec)})
    desc.append({'measure': 'jobs per pair with CI (median, max)', 'view': 'pairs',
                 'num': statistics.median([P[p]['jobs'] for p in ci]) if ci else '', 'den': max([P[p]['jobs'] for p in ci]) if ci else ''})
    write_csv('described.csv', desc, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'skipped'])

    # ---------------------------------------------------------------- beside LH015, pair by pair
    beside = []
    for lc in ('from the pinned file', 'not from the pinned file', 'undetermined', "nothing of the project's requirements",
               'no recipe'):
        ps = [p for p in read_ids if P[p]['lh015_class'] == lc]
        row = {'lh015_class': lc, 'pairs': len(ps)}
        for c in ('reads the pin', 'does not read the pin', "nothing of the project's requirements", 'undetermined', 'no CI'):
            row[c] = sum(1 for p in ps if P[p]['pair_class'] == c)
        lk = [p for p in ps if P[p]['lock_class'] in LDEC]
        row['lock pairs decided'] = len(lk)
        row['CI reads the timed lock'] = sum(1 for p in lk if P[p]['lock_class'] == 'reads the timed lock')
        beside.append(row)
    lu = [p for p in read_ids if P[p]['lh015_lock_unused'] == 'yes']
    row = {'lh015_class': 'a recipe build left a timed lock unused (lock unused)', 'pairs': len(lu)}
    for c in ('reads the pin', 'does not read the pin', "nothing of the project's requirements", 'undetermined', 'no CI'):
        row[c] = sum(1 for p in lu if P[p]['pair_class'] == c)
    lk = [p for p in lu if P[p]['lock_class'] in LDEC]
    row['lock pairs decided'] = len(lk)
    row['CI reads the timed lock'] = sum(1 for p in lk if P[p]['lock_class'] == 'reads the timed lock')
    beside.append(row)
    both = [p for p in lkb if P[p]['lock_class'] in LDEC and P[p]['lh015_class'] in ('from the pinned file', 'not from the pinned file')]
    for a in ('yes', 'no'):
        for b in LDEC:
            beside.append({'lh015_class': f'2x2: container build reads the timed lock = {a}; CI = {b}',
                           'pairs': sum(1 for p in both if P[p]['lh015_reads_T_lock'] == a and P[p]['lock_class'] == b)})
    write_csv('beside_lh015.csv', beside, ['lh015_class', 'pairs', 'reads the pin', 'does not read the pin',
                                           "nothing of the project's requirements", 'undetermined', 'no CI', 'lock pairs decided',
                                           'CI reads the timed lock'])
    extra = []
    nf = [p for p in read_ids if P[p]['lh015_class'] == 'not from the pinned file']
    extra += boot(p2(), nf, 'P2 among LH015\'s pairs "not from the pinned file"', False)
    extra += boot(p3(), [p for p in nf if P[p]['pin_class'] in ('lockfile', 'both')],
                  'P3 among LH015\'s pairs "not from the pinned file" with a timed lockfile', False)
    extra += boot(p2(), lu, 'P2 among pairs whose recipe left a timed lock unused', False)
    extra += boot(p3(), lu, 'P3 among pairs whose recipe left a timed lock unused', False)
    extra += boot(p3(), [p for p in lkb if P[p]['lh015_reads_T_lock'] == 'no' and
                         P[p]['lh015_class'] in ('from the pinned file', 'not from the pinned file')],
                  'P3 among lockfile pairs whose decided recipes read no timed lock', False)
    extra += boot(p2(), [p for p in read_ids if P[p]['lh015_class'] == 'no recipe'], 'P2 among pairs with no recipe', False)
    write_csv('beside_lh015_shares.csv', extra, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'skipped'])

    # ---------------------------------------------------------------- S1 to S6
    s1 = Counter()
    for r in jc:
        if r['pair_id'] not in readset or r['final_class'] not in ('1', '2') or r['decided_by'] != 'script':
            continue
        for t in set((r['T_tools'] if r['final_class'] == '1' else r['tools']).split()):
            s1[(r['final_class'], t)] += 1
    s1rows = [{'class': a, 'tool': b, 'jobs': c} for (a, b), c in sorted(s1.items(), key=lambda x: (-x[1], x[0]))]
    fl = Counter()
    for r in jc:
        if r['pair_id'] in readset and r['final_class'] == '1':
            for x in r['flags'].split('; '):
                if x:
                    fl[x] += 1
    s1rows += [{'class': '1', 'tool': 'flag: ' + k, 'jobs': v} for k, v in sorted(fl.items())]
    s1rows += [{'class': 'all', 'tool': 'decided by: ' + k, 'jobs': v} for k, v in
               sorted(Counter(r['decided_by'] for r in jc if r['pair_id'] in readset).items())]
    write_csv('s1_mechanisms.csv', s1rows, ['class', 'tool', 'jobs'])
    s2 = []
    for p in read_ids:
        if P[p]['pair_class'] != 'reads the pin':
            continue
        ones = [r for r in jmap[p] if r['final_class'] == '1']
        tools = {t for r in ones for t in r['T_tools'].split()}
        flagged = any(t in FLAG_TOOLS for t in tools)
        caches = [cache_on(jobs[r['job_key']]['cache']) for r in ones]
        s2.append({'pair_id': p, 'pin_class': P[p]['pin_class'], 'T_tools': ' '.join(sorted(tools)),
                   'a pip or uv install reads the pin': 'yes' if flagged else ('no' if tools else 'unknown'),
                   'every class 1 job restores an installer cache as written': 'yes' if caches and all(caches) else 'no',
                   'some class 1 job has no cache setting': 'yes' if any(not c for c in caches) else 'no'})
    write_csv('s2_log.csv', s2, list(s2[0].keys()) if s2 else ['pair_id'])
    s3 = []
    for p in read_ids:
        if P[p]['pair_class'] != 'reads the pin':
            continue
        ones = [jobs[r['job_key']] for r in jmap[p] if r['final_class'] == '1']
        s3.append({'pair_id': p, 'routine': 'yes' if any(routine(j) for j in ones) else 'no',
                   'gitlab': 'yes' if any(j['system'] == 'gitlab' for j in ones) else 'no',
                   'triggers': ' '.join(sorted({t for j in ones for t in (j['triggers'] + ' ' + j.get('caller_triggers', '')).split()}))})
    write_csv('s3_triggers.csv', s3, ['pair_id', 'routine', 'gitlab', 'triggers'])
    s4 = Counter()
    for p in read_ids:
        cb = any(r['container_build'] == 'yes' for r in jmap[p])
        s4[(('CI builds a container' if cb else 'no container build in CI'), P[p]['lh015_class'])] += 1
    write_csv('s4_container.csv', [{'ci': a, 'lh015_class': b, 'pairs': c} for (a, b), c in sorted(s4.items())],
              ['ci', 'lh015_class', 'pairs'])
    dc = defaultdict(set)
    for r in read_csv('doc_classes.csv'):
        dc[r['pair_id']].add(r['class'])
    s5 = []
    for p in read_ids:
        cs = dc.get(p, set())
        s5.append({'pair_id': p, 'pin_class': P[p]['pin_class'], 'documented': 'yes' if cs else 'no',
                   'classes': ' '.join(sorted(cs)), 'a documented command reads the pin': 'yes' if '1' in cs else 'no',
                   'own package from the index documented': 'yes' if '3' in cs else 'no'})
    write_csv('s5_docs.csv', s5, list(s5[0].keys()))
    s6 = []
    for c in ('reads the pin', 'does not read the pin', "nothing of the project's requirements", 'undetermined', 'no CI'):
        ps = [P[p] for p in read_ids if P[p]['pair_class'] == c]
        lags = sorted(float(r['lag_release_days']) for r in ps if r['outcome'] == 'moved' and r['lag_release_days'])
        q = statistics.quantiles(lags, n=4, method='inclusive') if len(lags) >= 2 else [None] * 3
        s6.append({'pair_class': c, 'pairs': len(ps), 'moved': sum(r['outcome'] == 'moved' for r in ps),
                   'censored': sum(r['outcome'].startswith('censored') for r in ps),
                   'removed': sum(r['outcome'] not in ('moved',) and not r['outcome'].startswith('censored') for r in ps),
                   'lag_q1': rnd(q[0], 1), 'lag_median': rnd(q[1], 1), 'lag_q3': rnd(q[2], 1)})
    write_csv('s6_moves.csv', s6, ['pair_class', 'pairs', 'moved', 'censored', 'removed', 'lag_q1', 'lag_median', 'lag_q3'])
    for m in measures:
        print(m['measure'], m['view'], m['num'], m['den'], m['share'], m['lo'], m['hi'], m['label'], m.get('note', ''))


if __name__ == '__main__':
    main()
