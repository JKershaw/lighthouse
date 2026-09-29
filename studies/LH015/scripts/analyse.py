"""LH015 phase 3: pair classes, the blind sample, and every measure on one set of resamples (brief, "Measures").

Reads data/frame.csv, frame_files.csv, pairs_read.csv, recipes.csv, recipe_classes.csv and pypi.csv; writes
data/review_sample.csv first (before any measure), then pair_classes.csv, not_read.csv, measures.csv, described.csv,
sensitivities.csv, s1_fresh_build.csv, s2_head.csv, s3_moves.csv and s4_mechanisms.csv. Offline and deterministic.
"""
import hashlib
import re
import operator
import os
import random
import statistics
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa: E402,F401
from packaging.specifiers import SpecifierSet, InvalidSpecifier  # noqa: E402

SEED, B_N, SALT = 20260929, 10000, 'LH015-review-20260929:'
NINE = {'agentcrew', 'serena', 'mcp-snowflake-server', 'browser-use', 'seclab-taskflow-agent', 'cognirepo', 'mistral-vibe',
        'prosuite-mcp', 'relay-shell'}


def pct(xs, p):
    """LH011's percentile, linear interpolation."""
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def label(x):
    return '' if x is None else 'as a rule' if x >= 0.75 else 'for some pairs' if x >= 0.5 else 'not as a rule'


def pair_class(classes):
    """The brief's pair rule from the classes of all builds (strings '1' to '6')."""
    cs = [str(c) for c in classes]
    if not cs:
        return 'no recipe'
    if all(c == '5' for c in cs):
        return 'nothing of the project\'s requirements'
    if any(c in ('2', '3', '4') for c in cs):
        return 'not from the pinned file'
    if any(c == '1' for c in cs) and all(c in ('1', '5') for c in cs):
        return 'from the pinned file'
    return 'undetermined'


def main():
    fr = read_csv('frame.csv')
    fmap = {r['pair_id']: r for r in fr}
    pr = {r['pair_id']: r for r in read_csv('pairs_read.csv')}
    builds = [b for b in read_csv('recipe_classes.csv')]
    pending = [b['build_id'] for b in builds if b['class'] == 'to judge']
    if pending:
        sys.exit(f'{len(pending)} builds still to judge, e.g. {pending[:5]}')
    rec = {r['build_id']: r for r in read_csv('recipes.csv')}
    lines = defaultdict(list)
    for r in read_csv('recipe_lines.csv'):
        lines[(r['repo'], r['commit'], r['path'])].append(r)

    # ---------------------------------------------------------------- blind sample, before any measure
    def key(b):
        return hashlib.sha256((SALT + b['pair_id'] + ':' + b['commit'] + ':' + b['path']).encode()).hexdigest()
    order = sorted(builds, key=lambda b: (key(b), b['build_id']))
    # the pools as they stood when the sample was drawn (version 0.1): judged = a judgement made before the blind check
    before = {r['build_id'] for r in read_csv('judgements.csv') if r.get('made', '') != 'after the blind check (R-0021)'}
    samp = [b for b in order if b['build_id'] not in before][:30] + [b for b in order if b['build_id'] in before][:30]
    rows = []
    for b in samp:
        f, r = fmap[b['pair_id']], rec[b['build_id']]
        keep = set(r['final_path'].split()) | {'-1'}
        txt = ' ⏎ '.join(f"{x['op']} {x['text']}" if x['part'] == '0' else x['text']
                               for x in lines[(f['repo'], b['commit'], b['path'])] if x['stage'] in keep)
        rows.append({'order_hash': key(b)[:16], 'group': 'script-decided' if b['build_id'] not in before else 'judged',
                     'build_id': b['build_id'], 'pair_id': b['pair_id'], 'repo': f['repo'], 'role': b['role'],
                     'commit': b['commit'], 'path': b['path'], 'target': b['target'], 'context': b['context'],
                     'context_how': r['context_how'], 'ignore_file': r['ignore_file'], 'build_args': r['build_args'],
                     'library': f['library'], 'T': r['T_paths'], 'pin_class': f['pin_class'], 'recipe_lines': txt[:30000]})
    write_csv('review_sample.csv', rows, list(rows[0].keys()) if rows else ['build_id'])

    # ---------------------------------------------------------------- pair classes
    by_pair = defaultdict(lambda: {'snapshot': [], 'head': []})
    for b in builds:
        by_pair[b['pair_id']][b['role']].append(b)
    out, read_ids, not_read = [], [], []
    for f in fr:
        pid, p = f['pair_id'], pr.get(f['pair_id'], {})
        st = p.get('status', 'not read: no row')
        row = {'pair_id': pid, 'repo': f['repo'], 'library': f['library'], 'threshold': f['threshold'], 'pin_class': f['pin_class'],
               'source_study': f['source_study'], 'status': st, 'outcome': f['outcome'], 'lag_release_days': f['lag_release_days']}
        if st != 'read' or p.get('snapshot_status_snapshot'):
            row['status'] = st if st != 'read' else 'not read: tree unreadable'
            not_read.append(row)
            out.append(row)
            continue
        read_ids.append(pid)
        sb, hb = by_pair[pid]['snapshot'], by_pair[pid]['head']
        n_prim = int(p.get('snapshot_n_primary') or 0)
        row.update({'keeps_recipe': 'yes' if n_prim else 'no', 'n_primary': n_prim, 'n_builds': len(sb),
                    'n_nonprimary': p.get('snapshot_n_nonprimary', ''), 'n_default_name': p.get('snapshot_n_default_name', ''),
                    'other_defs': p.get('snapshot_other_defs', ''),
                    'pair_class': pair_class([b['class'] for b in sb]) if n_prim else 'no recipe',
                    'mixed': 'yes' if n_prim and any(b['class'] == '1' for b in sb) and
                    any(b['class'] in ('2', '3', '4') for b in sb) else 'no',
                    'classes': ' '.join(sorted(b['class'] for b in sb)),
                    'head_keeps_recipe': 'yes' if int(p.get('head_n_primary') or 0) else ('no' if p.get('head_n_primary') else ''),
                    'head_class': (pair_class([b['class'] for b in hb]) if int(p.get('head_n_primary') or 0) else 'no recipe')
                    if p.get('head_n_primary') not in (None, '') else 'unknown',
                    'head_same_as_27sep': p.get('head_same_as_27sep', '')})
        # main recipe: fewest directories, default name first, then byte order
        if sb:
            main_path = sorted({b['path'] for b in sb}, key=lambda x: (x.split('#')[0].count('/'),
                               0 if x.split('#')[0].rsplit('/', 1)[-1].lower() == 'dockerfile' else
                               1 if x.split('#')[0].rsplit('/', 1)[-1].lower() == 'containerfile' else 2, x.encode()))[0]
            row['main_class'] = pair_class([b['class'] for b in sb if b['path'] == main_path])
            dflt = [b for b in sb if b['path'].split('#')[0].rsplit('/', 1)[-1].lower() in ('dockerfile', 'containerfile')]
            row['r2_class'] = pair_class([b['class'] for b in dflt]) if dflt else 'no recipe'
            row['relock_class'] = pair_class(['2' if 'may re-lock' in b['flags'] and b['class'] == '1' else b['class'] for b in sb])
            kept = [b for b in sb if 'at start only' not in b['flags']]
            row['nostart_class'] = pair_class([b['class'] for b in kept]) if kept else 'no recipe'
            r3 = [b for b in sb if b['class'] in ('2', '3', '4')]
            row['r3_only'] = 'yes' if r3 and all((b['class'] == '2' and b['sub'] == 'other file' and b['names_L'] == 'no') or
                                                 (b['class'] == '3' and b.get('pypi', '') == 'not listed') for b in r3) else 'no'
            row['reads_T_lock'] = 'yes' if any(b['class'] == '1' and b['T_lock'] == 'yes' for b in sb) else 'no'
        else:
            row.update({'main_class': row['pair_class'], 'r2_class': row['pair_class'], 'relock_class': row['pair_class'],
                        'nostart_class': row['pair_class'], 'r3_only': 'no', 'reads_T_lock': 'no'})
        row['r1_keeps'] = 'yes' if n_prim or int(p.get('snapshot_n_nonprimary') or 0) else 'no'
        row['r2_keeps'] = 'yes' if int(p.get('snapshot_n_default_name') or 0) else 'no'
        row['nine'] = 'yes' if f['repo'].rsplit('/', 1)[-1].lower() in NINE else 'no'
        out.append(row)
    fields = ['pair_id', 'repo', 'library', 'threshold', 'pin_class', 'source_study', 'status', 'keeps_recipe', 'n_primary',
              'n_builds', 'n_nonprimary', 'n_default_name', 'other_defs', 'pair_class', 'mixed', 'classes', 'main_class', 'r2_class',
              'relock_class', 'nostart_class', 'r3_only', 'reads_T_lock', 'r1_keeps', 'r2_keeps', 'nine', 'head_keeps_recipe',
              'head_class', 'head_same_as_27sep', 'outcome', 'lag_release_days']
    write_csv('pair_classes.csv', out, fields)
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
        D, N = sum(den), sum(num)
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
            res.append({'measure': name, 'view': view, 'num': N if view == 'pairs' else round(sum(a), 3),
                        'den': D if view == 'pairs' else sum(b), 'n_repos': sum(rh), 'share': rnd(pt), 'lo': rnd(lo),
                        'hi': rnd(hi), 'skipped': skipped})
        return res

    def diff(fa, pa, fb, pb, name):
        A, Bv = vec(fa, pa), vec(fb, pb)
        pt = (sum(A[0]) / sum(A[1]) - sum(Bv[0]) / sum(Bv[1])) if sum(A[1]) and sum(Bv[1]) else None
        xs, skipped = [], 0
        for c in counts:
            da, db = sum(map(operator.mul, c, A[1])), sum(map(operator.mul, c, Bv[1]))
            if not da or not db:
                skipped += 1
                continue
            xs.append(sum(map(operator.mul, c, A[0])) / da - sum(map(operator.mul, c, Bv[0])) / db)
        return {'measure': name, 'view': 'pairs', 'num': '', 'den': f'{sum(A[1])} and {sum(Bv[1])}', 'share': rnd(pt),
                'lo': rnd(pct(xs, 0.025)) if xs else '', 'hi': rnd(pct(xs, 0.975)) if xs else '', 'skipped': skipped}

    DEC = ('from the pinned file', 'not from the pinned file')

    def p2(col='pair_class', und=None):
        def f(r):
            c = r[col]
            if c == 'undetermined' and und:
                c = und
            if c not in DEC:
                return None
            return 1 if c == DEC[0] else 0
        return f

    keeps = [p for p in read_ids if P[p]['keeps_recipe'] == 'yes']
    measures = []
    measures += boot(lambda r: 1 if r['keeps_recipe'] == 'yes' else 0, name='P1 keeps a recipe')
    measures += boot(p2(), name='P2 from the pinned file, all')
    for pc in ('lockfile', 'exact pin', 'both'):
        measures += boot(p2(), [p for p in read_ids if P[p]['pin_class'] == pc], name=f'P2 from the pinned file, {pc}')
    n_und = sum(1 for p in keeps if P[p]['pair_class'] == 'undetermined')
    for m in measures:
        m['label'] = label(m['share'] if m['share'] != '' else None)
        if m['lo'] != '' and label(m['lo']) != label(m['hi']):
            m['note'] = 'interval spans a label boundary'
        if m['measure'].startswith('P2') and m['view'] == 'pairs':
            small = (m['den'] < 40 or m['n_repos'] < 25) if m['measure'].endswith('all') else (m['den'] < 20 or m['n_repos'] < 12)
            if small:
                m['label'] = ''
                m['note'] = (m.get('note', '') + '; too few pairs or repositories for a label').strip('; ')
    if len(read_ids) < 313:
        for m in measures:
            m['note'] = (m.get('note', '') + '; inconclusive for the frame (fewer than 313 pairs read)').strip('; ')

    # ---------------------------------------------------------------- described, not tested
    desc = []
    ex = [p for p in read_ids if P[p]['pin_class'] == 'exact pin']
    lk = [p for p in read_ids if P[p]['pin_class'] == 'lockfile']
    lkb = [p for p in read_ids if P[p]['pin_class'] in ('lockfile', 'both')]
    desc.append(diff(p2(), ex, p2(), lk, 'P2 exact pin minus lockfile'))
    desc.append(diff(p2(), ex, p2(), lkb, 'P2 exact pin minus lockfile and both'))
    for nm, fn in (('nothing of the project\'s requirements', lambda r: r['pair_class'] == nm),):
        pass
    for c in ('nothing of the project\'s requirements', 'undetermined'):
        desc += boot(lambda r, c=c: 1 if r['pair_class'] == c else 0, keeps, f'share of pairs with a recipe: {c}', False)
    desc += boot(lambda r: 1 if r['mixed'] == 'yes' else 0, keeps, 'share of pairs with a recipe: mixed', False)
    desc += boot(lambda r: (1 if r['reads_T_lock'] == 'yes' else 0) if r['pair_class'] in DEC else None, lkb,
                 'pairs with a lockfile (lockfile or both), decided: some build reads the timed lockfile', False)
    desc += boot(lambda r: 1 if r['pair_class'] == 'not from the pinned file' else 0, read_ids,
                 'pairs read whose recipe would not take the pinned file', False)
    nf = [p for p in read_ids if P[p]['pair_class'] == 'not from the pinned file']
    snaps = [b for b in builds if b['role'] == 'snapshot']
    for k in ('2', '3', '4'):
        desc.append({'measure': f'pairs "not from the pinned file" with a class {k} build', 'view': 'pairs',
                     'num': sum(1 for p in nf if k in P[p]['classes'].split()), 'den': len(nf)})
    for s in ('lock unused', 'lock absent', 'other file', 'upgrade', 'inline'):
        desc.append({'measure': f'class 2 builds at snapshots, sub-label {s}', 'view': 'builds',
                     'num': sum(1 for b in snaps if b['class'] == '2' and b['sub'] == s), 'den': sum(b['class'] == '2' for b in snaps)})
    write_csv('described.csv', desc, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'skipped'])

    # ---------------------------------------------------------------- sensitivities
    sens = []
    sens += boot(lambda r: 1 if r['r1_keeps'] == 'yes' else 0, name='R1 P1, recipes in excluded directories counted')
    sens += boot(lambda r: 1 if r['r2_keeps'] == 'yes' else 0, name='R2 P1, only files named Dockerfile or Containerfile')
    sens += boot(p2('r2_class'), name='R2 P2, only files named Dockerfile or Containerfile')
    sens += boot(p2('main_class'), name='P2, main recipe alone')
    sens += boot(lambda r: 1 if r['keeps_recipe'] == 'yes' else 0, [p for p in read_ids if P[p]['nine'] == 'no'],
                 'P1 without the nine repositories LH006 or LH007 read')
    sens += boot(p2(), [p for p in read_ids if P[p]['nine'] == 'no'], 'P2 without the nine repositories LH006 or LH007 read')
    sens += boot(p2('relock_class'), name='P2, "may re-lock" builds counted as class 2')
    sens += boot(p2('nostart_class'), name='P2, recipes whose only install is at start dropped')
    sens += boot(p2(und='from the pinned file'), name='P2, undetermined counted as from the pinned file')
    sens += boot(p2(und='not from the pinned file'), name='P2, undetermined counted as not from the pinned file')
    sens += boot(lambda r: None if r['r3_only'] == 'yes' else p2()(r), name='R3 P2, builds that do not show L set aside')
    for pc in ('lockfile', 'exact pin', 'both'):
        pp = [p for p in read_ids if P[p]['pin_class'] == pc]
        sens += boot(lambda r: None if r['r3_only'] == 'yes' else p2()(r), pp, f'R3 P2, {pc}', False)
        for u in DEC:
            sens += boot(p2(und=u), pp, f'P2, {pc}, undetermined counted as {u}')
    for m in sens:
        m['label'] = label(m['share'] if m['share'] != '' else None)
    # brief: undetermined above one fifth of pairs with a recipe -> P2's label stands only if both undetermined bounds carry it
    und_share = n_und / len(keeps) if keeps else 0
    for m in measures:
        m['label_as_computed'] = m['label']
        if m['measure'].startswith('P2') and m['label'] and und_share > 0.2:
            pc = m['measure'].split(', ', 1)[1]
            names = [f'P2, undetermined counted as {u}' if pc == 'all' else f'P2, {pc}, undetermined counted as {u}' for u in DEC]
            bounds = [x for x in sens if x['measure'] in names and x['view'] == m['view']]
            if len(bounds) < 2 or any(x['label'] != m['label'] for x in bounds):
                m['label'] = ''
                m['note'] = (m.get('note', '') + f'; label withheld: undetermined pairs are {und_share:.3f} of pairs with a recipe and '
                             f'the bounds read {" / ".join(x["label"] for x in bounds)}').strip('; ')
    write_csv('measures.csv', measures, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'label', 'label_as_computed',
                                         'note', 'skipped'])
    write_csv('sensitivities.csv', sens, ['measure', 'view', 'num', 'den', 'n_repos', 'share', 'lo', 'hi', 'label', 'skipped'])

    # ---------------------------------------------------------------- S1 to S4
    s1 = []
    for pid in nf:
        f = fmap[pid]
        fix = V(f['pair_fix'] or f['threshold'])
        verdicts = []
        for b in by_pair[pid]['snapshot']:
            if b['class'] == '2':
                specs = [x.strip() for x in b['spec'].split('|') if x.strip()] if b['names_L'] == 'yes' else []
            elif b['class'] == '3':
                specs = [b['pypi_spec']] if b.get('pypi') in ('published pin', 'published range') else []
            else:
                continue
            verdicts.append(admits(specs, fix))
        det = [v for v in verdicts if v in ('admits', 'excludes')]
        s1.append({'pair_id': pid, 'library': f['library'], 'pair_fix': f['pair_fix'], 'builds': ' '.join(verdicts),
                   'reading': 'not determined' if not det else det[0] if len(set(det)) == 1 else 'differs by build'})
    write_csv('s1_fresh_build.csv', s1, ['pair_id', 'library', 'pair_fix', 'builds', 'reading'])
    s2 = Counter((P[p]['pair_class'], P[p]['head_class']) for p in read_ids)
    write_csv('s2_head.csv', [{'snapshot_class': a, 'head_class': b, 'pairs': c} for (a, b), c in sorted(s2.items())],
              ['snapshot_class', 'head_class', 'pairs'])
    s3 = []
    for c in ('no recipe', 'nothing of the project\'s requirements', 'from the pinned file', 'not from the pinned file',
              'undetermined'):
        ps = [P[p] for p in read_ids if P[p]['pair_class'] == c]
        lags = sorted(float(r['lag_release_days']) for r in ps if r['outcome'] == 'moved' and r['lag_release_days'])
        q = statistics.quantiles(lags, n=4, method='inclusive') if len(lags) >= 2 else [None] * 3
        s3.append({'pair_class': c, 'pairs': len(ps), 'moved': sum(r['outcome'] == 'moved' for r in ps),
                   'censored': sum(r['outcome'].startswith('censored') for r in ps),
                   'removed': sum(r['outcome'].startswith('removed') for r in ps),
                   'lag_q1': rnd(q[0]), 'lag_median': rnd(statistics.median(lags)) if lags else '', 'lag_q3': rnd(q[2])})
    write_csv('s3_moves.csv', s3, ['pair_class', 'pairs', 'moved', 'censored', 'removed', 'lag_q1', 'lag_median', 'lag_q3'])
    s4 = []
    fams = [('pip -r, -c or sync of a file', r':-[rc] |includes|pip-sync|keeps the pins'), ('pip install of a project directory', r':project '),
            ('uv sync, run, export or lock', r'uv (sync|run|export|lock)'), ('Poetry', r'poetry '), ('Pipenv', r'pipenv '), ('PDM', r'pdm '),
            ('own package from the index', r'own package'), ('conda family', r'conda|mamba'), ('other named packages', r'named package')]
    for nm, rx in fams:
        s4.append({'item': 'snapshot builds whose steps include (from the effects column)', 'value': nm,
                   'count': sum(1 for b in snaps if re.search(rx, b['effects']))})
    s4 += [{'item': 'recipes per pair keeping one', 'value': k, 'count': v}
           for k, v in sorted(Counter(P[p]['n_primary'] for p in keeps).items())]
    rset = {(b['pair_id'].split('-')[0], b['commit'], b['path']) for b in snaps}
    recs = {(fmap[pid]['repo'], c, pth) for pid, c, pth in rset}
    s4 += [{'item': 'distinct snapshot recipes by depth', 'value': k, 'count': v}
           for k, v in sorted(Counter(x[2].split('#')[0].count('/') for x in recs).items())]
    forms = {}
    for b in snaps:
        forms[(fmap[b['pair_id']]['repo'], b['commit'], b['path'])] = rec[b['build_id']]['name_form']
    s4 += [{'item': 'distinct snapshot recipes by name form', 'value': k, 'count': v} for k, v in sorted(Counter(forms.values()).items())]
    s4.append({'item': 'distinct snapshot recipes that are templates', 'value': '',
               'count': len({(fmap[b['pair_id']]['repo'], b['commit'], b['path']) for b in snaps if rec[b['build_id']]['template'] == 'yes'})})
    s4.append({'item': 'snapshot builds with an install at start', 'value': 'at start (also)',
               'count': sum('at start' in b['flags'].split(';') for b in snaps)})
    s4.append({'item': 'snapshot builds with an install at start', 'value': 'at start only',
               'count': sum('at start only' in b['flags'] for b in snaps)})
    s4.append({'item': 'snapshot builds flagged may re-lock', 'value': '', 'count': sum('may re-lock' in b['flags'] for b in snaps)})
    s4.append({'item': 'pairs read with another build definition', 'value': '', 'count': sum(1 for p in read_ids if P[p]['other_defs'])})
    s4.append({'item': 'pairs read whose only recipes lie in excluded directories', 'value': '',
               'count': sum(1 for p in read_ids if P[p]['keeps_recipe'] == 'no' and P[p]['r1_keeps'] == 'yes')})
    s4 += [{'item': 'snapshot builds by class and sub-label', 'value': f"{k[0]} {k[1]}".strip(), 'count': v}
           for k, v in sorted(Counter((b['class'], b['sub']) for b in snaps).items())]
    s4 += [{'item': 'snapshot builds decided by', 'value': k, 'count': v} for k, v in sorted(Counter(b['decided_by'] for b in snaps).items())]
    write_csv('s4_mechanisms.csv', s4, ['item', 'value', 'count'])
    pcs = Counter(P[p]['pair_class'] for p in read_ids)
    print(f'pairs read {len(read_ids)} of {len(fr)} in {n} repositories; pair classes {dict(pcs)}')
    for m in measures:
        if m['view'] == 'pairs':
            print(f"{m['measure']}: {m['num']}/{m['den']} = {m['share']} [{m['lo']}, {m['hi']}] {m['label']} {m.get('note', '')}")


def admits(specs, fix):
    if not specs or fix is None:
        return 'not determined'
    res = set()
    for s in specs:
        s = s.strip()
        if s in ('any', ''):
            res.add('admits')
            continue
        if ';' in s or s.startswith('poetry:') or s == '?':
            res.add('not determined')
            continue
        try:
            res.add('admits' if SpecifierSet(s).contains(fix, prereleases=True) else 'excludes')
        except InvalidSpecifier:
            res.add('not determined')
    if res == {'admits'} or res == {'excludes'}:
        return res.pop()
    return 'not determined' if 'not determined' in res else 'differs'


def rnd(x):
    return '' if x is None else round(x, 4)


if __name__ == '__main__':
    main()
