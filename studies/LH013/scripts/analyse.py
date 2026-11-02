#!/usr/bin/env python3
"""LH013: every table and figure the record cites, offline, from the files retained in data/ and LH012's retained
W0 files. Writes data/analysis/ (or $LH013_OUT/analysis) and prints data/analysis/results.txt.
The measures, tests and conventions are the brief's (brief.md, SHA-256 on issue #15) with amendments 1 to 4.
Code reused from LH012, named where used: scripts/analyse.py (classes, admission, P and its classes, the bootstrap),
review/r0018_walkshare.py (measure 4, unchanged), review/r0018_staircase.py (blocks of twenty),
scripts/post_hoc.py and scripts/driver_checks.py (the boto3 tests), review/r0025_walk_dip.py (amendment 2).
Usage: python3 analyse.py"""
import csv, os, random, re, statistics
from collections import defaultdict
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, 'data')
L12 = os.path.join(os.path.dirname(STUDY), 'LH012', 'data')
OUT = os.path.join(os.environ.get('LH013_OUT', DATA), 'analysis')
os.makedirs(OUT, exist_ok=True)
SEED, NBOOT = 20260929, 10000
WEEKS = ('W1', 'W2')
WEEK_END = {'W0': '2026-09-27T23:59:59.999999', 'W1': '2026-10-04T23:59:59.999999', 'W2': '2026-10-11T23:59:59.999999'}
LINES = []


def say(*a):
    LINES.append(' '.join(str(x) for x in a))


def rd(*p):
    with open(os.path.join(*p), newline='') as f:
        return list(csv.DictReader(f))


def fmt(x):
    return f'{x:.6f}' if isinstance(x, float) else ('' if x is None else x)


def wr(name, rows, fields=None):
    fields = fields or list(rows[0].keys())
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k, '')) for k in fields})


def pct(x, d=1):
    return 'unknown' if x is None else f'{100 * x:.{d}f}'


def share(a, b):
    return a / b if b else None


_VC = {}


def V(s):
    if s not in _VC:
        try:
            _VC[s] = Version(s)
        except InvalidVersion:
            _VC[s] = None
    return _VC[s]


def boot(values, stat, seed=SEED, n=NBOOT):
    """LH012's percentile interval over resamples of projects with replacement."""
    rnd = random.Random(seed)
    out = sorted(stat([values[rnd.randrange(len(values))] for _ in values]) for _ in range(n))
    return out[int(0.025 * n)], out[int(0.975 * n) - 1]


# ---------------------------------------------------------------- frame
REF = {r['project']: r for r in rd(DATA, 'frame', 'reference.csv')}
P37 = sorted(REF)
CLS = defaultdict(dict)
for r in rd(DATA, 'frame', 'classes.csv'):
    CLS[r['project']][r['version']] = r
VERS = defaultdict(dict)
for v in rd(DATA, 'versions.csv'):
    VERS[v['project']][v['version']] = v
W0OK = {r['project']: r['confirmed'] == 'True' for r in rd(os.path.join(os.environ.get('LH013_OUT', DATA), 'analysis'), 'w0_check.csv')}
GAPS = defaultdict(set)
for g in rd(os.path.join(os.environ.get('LH013_OUT', DATA), 'analysis'), 'gaps.csv'):
    GAPS[g['project']].add(g['date'])
L12WEEK = {r['project']: r for r in rd(L12, 'analysis', 'week.csv')}
L12PY = {r['project']: r for r in rd(L12, 'analysis', 'python.csv')}
L12REF = {r['project']: r for r in rd(L12, 'reference.csv')}
assert all(L12REF[p]['R'] == REF[p]['R0'] for p in P37)


def vclass(p, v, ref='R0'):
    c = CLS[p].get(v)
    return c[ref] if c else 'other'  # a version PyPI does not list is "other" (brief, measure 1)


def usable(v):
    return v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and v['first_upload_utc']


def admits_minor(rp, m):
    if not rp.strip():
        return True
    try:
        s = SpecifierSet(rp)
    except InvalidSpecifier:
        return None
    return any(s.contains(Version(f'{m}.{k}'), prereleases=True) for k in range(31))


def version_admits(row, m):
    vals = [admits_minor(x, m) for x in row['requires_python'].split(' | ')] if row['requires_python'] else [True]
    if any(v is True for v in vals):
        return True
    return None if any(v is None for v in vals) else False


_EX, _ED = {}, {}


def excluded(p, m, R, end):
    """LH012's rule: no usable version at or above R, uploaded by `end`, admits minor m (amendment 4: constant within
    each week, so the week's end stands for each of its days)."""
    k = (p, m, R, end)
    if k not in _EX:
        Rv = Version(R)
        ge = [v for s, v in VERS[p].items() if usable(v) and Version(s) >= Rv and v['first_upload_utc'] <= end]
        _EX[k] = not any(version_admits(v, m) is True for v in ge)
    return _EX[k]


def edge(p, m, R):
    k = (p, m, R)
    if k not in _ED:
        Rv = Version(R)
        below = sorted(Version(s) for s, v in VERS[p].items() if usable(v) and Version(s) < Rv and version_admits(v, m) is True)
        _ED[k] = str(below[-1]) if below else ''
    return _ED[k]


def pyminor(s):
    return s if re.fullmatch(r'\d+\.\d+', s or '') else ''


def classify(lo, hi):
    """LH012's convention."""
    if lo is None or hi is None:
        return 'unknown'
    if lo > 0.5:
        return 'accounts for most'
    if hi < 0.1:
        return 'accounts for little'
    if hi < 0.5:
        return 'cannot be the main reason'
    return 'undetermined'


def coarse(c):
    return 'cannot be the main reason' if c == 'accounts for little' else c


# ---------------------------------------------------------------- the counts
VSUM = {w: defaultdict(lambda: defaultdict(int)) for w in ('W0',) + WEEKS}
PSUM = {w: defaultdict(list) for w in ('W0',) + WEEKS}
for p in P37:
    for r in rd(L12, 'week', 'versions', p + '.csv'):
        VSUM['W0'][p][r['version']] += int(r['n'])
    for r in rd(L12, 'week', 'python', p + '.csv'):
        PSUM['W0'][p].append((r['version'], r['python_minor'], int(r['n'])))
    for r in rd(DATA, 'counts', 'versions', p + '.csv'):
        VSUM[r['week']][p][r['version']] += int(r['n'])
    for r in rd(DATA, 'counts', 'python', p + '.csv'):
        PSUM[r['week']][p].append((r['version'], r['python_minor'], int(r['n'])))


def older_share(p, w, ref):
    c = defaultdict(int)
    for v, n in VSUM[w][p].items():
        c[vclass(p, v, ref)] += n
    tot = sum(c.values())
    return dict(total=tot, older=c['older'], at_or_newer=c['at_or_newer'], other=c['other'], O=share(c['older'], tot))


def python_measure(p, w, ref, R, vtotal):
    ex = nr = adm = at_edge = tot = 0
    per_minor = defaultdict(int)
    for v, m0, n in PSUM[w][p]:
        tot += n
        if vclass(p, v, ref) != 'older':
            continue
        m = pyminor(m0)
        if not m:
            nr += n
        elif excluded(p, m, R, WEEK_END[w]):
            ex += n
            per_minor[m] += n
            if v == edge(p, m, R):
                at_edge += n
        else:
            adm += n
    older = ex + nr + adm
    diff = (tot - vtotal) / vtotal if vtotal else None
    return dict(older_bypython=older, older_excluded=ex, older_not_reported=nr, older_admitted=adm,
                P_lower=share(ex, older), P_upper=share(ex + nr, older), edge_share=share(at_edge, ex),
                excluded_minors=' '.join(f'{m}:{v}' for m, v in sorted(per_minor.items())), bypython_total=tot,
                bypython_vs_versions=diff, table_check='ok' if diff is not None and abs(diff) <= 0.02 else 'tables differ by more than 2 per cent')


# ---------------------------------------------------------------- 1 and 2: O and P at R0, W0 (recomputed) to W2
o_rows, p_rows = [], []
O, P = defaultdict(dict), defaultdict(dict)
for p in P37:
    for w in ('W0',) + WEEKS:
        o = older_share(p, w, 'R0')
        known = len(GAPS[p] & set()) <= 2 if w == 'W0' else len([d for d in GAPS[p] if (d <= '2026-10-04') == (w == 'W1')]) <= 2
        o.update(project=p, week=w, R=REF[p]['R0'], gap_days=0 if w == 'W0' else len([d for d in GAPS[p] if (d <= '2026-10-04') == (w == 'W1')]),
                 known=str(known and (W0OK.get(p, False) if w == 'W0' else True)))
        O[p][w] = o
        o_rows.append(o)
        q = python_measure(p, w, 'R0', REF[p]['R0'], o['total'])
        q.update(project=p, week=w)
        P[p][w] = q
        p_rows.append(q)
# LH012's rule: P is described only when more than a third of projects have more than a third of older downloads
# with no Python reported, or (per project) when the two tables differ by more than 2 per cent
for w in ('W0',) + WEEKS:
    heavy = sum(1 for p in P37 if P[p][w]['older_bypython'] and P[p][w]['older_not_reported'] / P[p][w]['older_bypython'] > 1 / 3)
    for p in P37:
        q = P[p][w]
        q['class'] = 'description only' if (heavy > len(P37) / 3 or q['table_check'] != 'ok') else classify(q['P_lower'], q['P_upper'])
# W0 recomputed here must equal LH012's retained tables
w0_same_O = all(abs(O[p]['W0']['O'] - float(L12WEEK[p]['O'])) < 1e-6 and O[p]['W0']['total'] == int(L12WEEK[p]['total']) for p in P37)
w0_same_P = all(P[p]['W0']['class'] == L12PY[p]['class'] and abs(P[p]['W0']['P_lower'] - float(L12PY[p]['P_lower'])) < 1e-6
                and abs(P[p]['W0']['P_upper'] - float(L12PY[p]['P_upper'])) < 1e-6 for p in P37)

hold_rows = []
for p in P37:
    o0, o1, o2 = (O[p][w]['O'] for w in ('W0', 'W1', 'W2'))
    o_known = all(O[p][w]['known'] == 'True' for w in ('W0', 'W1', 'W2')) and W0OK.get(p, False)
    o_hold = (abs(o1 - o0) <= 0.05 and abs(o2 - o0) <= 0.05) if o_known else None
    cl = [P[p][w]['class'] for w in ('W0', 'W1', 'W2')]
    p_known = o_known and all(c not in ('description only', 'unknown') for c in cl)
    p_hold = (len({coarse(c) for c in cl}) == 1) if p_known else None
    hold_rows.append(dict(project=p, O_W0=o0, O_W1=o1, O_W2=o2, dO_W1=o1 - o0, dO_W2=o2 - o0, O_known=str(o_known),
                          O_holds='' if o_hold is None else str(o_hold),
                          P_class_W0=cl[0], P_class_W1=cl[1], P_class_W2=cl[2],
                          P_lower_W0=P[p]['W0']['P_lower'], P_upper_W0=P[p]['W0']['P_upper'],
                          P_lower_W1=P[p]['W1']['P_lower'], P_upper_W1=P[p]['W1']['P_upper'],
                          P_lower_W2=P[p]['W2']['P_lower'], P_upper_W2=P[p]['W2']['P_upper'],
                          P_known=str(p_known), P_holds='' if p_hold is None else str(p_hold)))
wr('older.csv', o_rows, ['project', 'week', 'R', 'gap_days', 'known', 'total', 'older', 'at_or_newer', 'other', 'O'])
wr('python.csv', p_rows, ['project', 'week', 'older_bypython', 'older_excluded', 'older_not_reported', 'older_admitted', 'P_lower',
                          'P_upper', 'class', 'edge_share', 'excluded_minors', 'bypython_total', 'bypython_vs_versions', 'table_check'])

# ---------------------------------------------------------------- 3: cells (C, C5), CI flag by class (amendment 3)
cell_rows = []
C = defaultdict(dict)


def half_count(sizes, total):
    acc = 0
    for i, s in enumerate(sizes[:1000], 1):
        acc += s
        if acc >= total / 2:
            return str(i)
    return 'more than 1,000'


for p in P37:
    for w in WEEKS:
        path = os.path.join(DATA, 'counts', 'pass', f'{p}_{w}.csv')
        if not os.path.exists(path):
            C[p][w] = None
            continue
        r = rd(path)[0]
        tot = int(r['total'])
        vt = O[p][w]['total']
        diff = (tot - vt) / vt if vt else None
        row = dict(project=p, week=w, pass_total=tot, versions_total=vt, pass_vs_versions=diff,
                   pass_check='ok' if diff is not None and abs(diff) <= 0.02 else 'tables differ by more than 2 per cent')
        for k, base, den in (('c6', 'C', tot), ('c5', 'C5', tot), ('older_c6', 'olderC', int(r['older'])), ('older_c5', 'olderC5', int(r['older']))):
            sizes = [int(x) for x in r[k + '_top'].split()] if r[k + '_top'] else []
            assert sizes == sorted(sizes, reverse=True)
            row[base] = share(sizes[0], den) if sizes else None
            row[base + '_cell'] = r[k + '_key']
            row[base + '_cells'] = int(r[k + '_cells'])
            row[base + '_half'] = half_count(sizes, den) if sizes else ''
        for c in ('older', 'at_or_newer', 'other'):
            n = int(r[c])
            row[c] = n
            for f in ('true', 'false', 'unknown'):
                row[f'{c}_ci_{f}'] = int(r[f'{c}_ci_{f}'])
            row[f'{c}_ci_true_share'] = share(int(r[f'{c}_ci_true']), n)
        row['ci_true_older_minus_newer'] = (row['older_ci_true_share'] - row['at_or_newer_ci_true_share']
                                            if row['older_ci_true_share'] is not None and row['at_or_newer_ci_true_share'] is not None else None)
        C[p][w] = row
        cell_rows.append(row)
wr('cells.csv', cell_rows)
for h in hold_rows:
    p = h['project']
    a, b = C[p].get('W1'), C[p].get('W2')
    for base in ('C', 'C5'):
        known = bool(a and b and a['pass_check'] == 'ok' and b['pass_check'] == 'ok')
        h[f'{base}_W1'], h[f'{base}_W2'] = (a or {}).get(base), (b or {}).get(base)
        h[f'{base}_cell_W1'], h[f'{base}_cell_W2'] = (a or {}).get(base + '_cell'), (b or {}).get(base + '_cell')
        h[f'{base}_known'] = str(known)
        h[f'{base}_holds'] = str(abs(b[base] - a[base]) <= 0.05 and a[base + '_cell'] == b[base + '_cell']) if known else ''
wr('holds.csv', hold_rows)

# ---------------------------------------------------------------- across projects
say('LH013 results (analyse.py). Shares in per cent; intervals are percentile intervals over 10,000 resamples of projects, seed 20260929.')
say('')
say(f'Checks: W0 recomputed from LH012\'s retained files equals LH012\'s week.csv (O, total): {w0_same_O}; python.csv (P, class): {w0_same_P}')
say(f'W0 baseline check (W0 totals read again): {sum(W0OK.values())} of 37 confirmed within 2 per cent')
say(f'Gap days in W1 and W2: {sum(len(g) for g in GAPS.values())}')
for w in WEEKS:
    bad = [p for p in P37 if P[p][w]['table_check'] != 'ok']
    badc = [p for p in P37 if C[p].get(w) is None or C[p][w]['pass_check'] != 'ok']
    mx = max(abs(P[p][w]['bypython_vs_versions']) for p in P37)
    mxc = max((abs(C[p][w]['pass_vs_versions']) for p in P37 if C[p].get(w)), default=None)
    say(f'{w}: by-Python table against per-version table, largest difference {100 * mx:.4f} per cent, projects over 2 per cent: {bad or "none"}; '
        f'pypi.pypi pass against per-version table, largest difference {"unknown" if mxc is None else f"{100 * mxc:.4f}"} per cent, projects over 2 per cent or unread: {badc or "none"}')
say('')


def label(k, n):
    return 'as a rule' if k >= 0.75 * n else ('for most projects' if k > 0.5 * n else 'for some projects')


summ = []
for meas in ('O', 'P', 'C', 'C5'):
    vals = [h[f'{meas}_holds'] == 'True' for h in hold_rows if h[f'{meas}_known'] == 'True']
    n, k = len(vals), sum(vals)
    lo, hi = boot([1.0 if v else 0.0 for v in vals], lambda s: sum(s) / len(s)) if n else (None, None)
    summ.append(dict(measure=meas, known=n, hold=k, share=share(k, n), ci_low=lo, ci_high=hi, label=label(k, n) if n else ''))
    say(f'{meas} holds: {k} of {n} projects with a known outcome ({pct(share(k, n))} per cent, interval {pct(lo)} to {pct(hi)}): "{label(k, n)}"')
wr('summary.csv', summ)
say('')
for meas in ('O', 'P'):
    no = [h['project'] for h in hold_rows if h[f'{meas}_holds'] == 'False']
    say(f'{meas} does not hold for: {", ".join(no) or "none"}')
for meas in ('C', 'C5'):
    no = [f"{h['project']} ({pct(h[meas + '_W1'])} to {pct(h[meas + '_W2'])}{'' if h[meas + '_cell_W1'] == h[meas + '_cell_W2'] else ', cell changed'})" for h in hold_rows if h[f'{meas}_holds'] == 'False']
    say(f'{meas} does not hold for: {", ".join(no) or "none"}')
say('')
for w in ('W0',) + WEEKS:
    os_ = [O[p][w]['O'] for p in P37]
    med = statistics.median(os_)
    lo, hi = boot(os_, statistics.median)
    pooled = sum(O[p][w]['older'] for p in P37) / sum(O[p][w]['total'] for p in P37)
    pl = [P[p][w]['P_lower'] for p in P37]
    pu = [P[p][w]['P_upper'] for p in P37]
    pooled_lo = sum(P[p][w]['older_excluded'] for p in P37) / sum(P[p][w]['older_bypython'] for p in P37)
    pooled_hi = sum(P[p][w]['older_excluded'] + P[p][w]['older_not_reported'] for p in P37) / sum(P[p][w]['older_bypython'] for p in P37)
    cls = defaultdict(list)
    for p in P37:
        cls[P[p][w]['class']].append(p)
    say(f'{w}: median O {pct(med)} (interval {pct(lo)} to {pct(hi)}), range {pct(min(os_))} to {pct(max(os_))}, pooled {pct(pooled)}; '
        f'median P {pct(statistics.median(pl))} to {pct(statistics.median(pu))}, pooled {pct(pooled_lo)} to {pct(pooled_hi)}')
    for c in ('accounts for most', 'undetermined', 'cannot be the main reason', 'accounts for little', 'description only'):
        if cls[c]:
            say(f'      P {c}: {len(cls[c])}: {", ".join(cls[c]) if len(cls[c]) <= 8 else ""}')
dO = [h['dO_W1'] for h in hold_rows] + [h['dO_W2'] for h in hold_rows]
say(f'Change in O from W0, over the 74 project-weeks: median {100 * statistics.median(dO):+.2f} points, largest absolute {100 * max(abs(x) for x in dO):.2f} points')
say('')
for w in WEEKS:
    rows = [C[p][w] for p in P37 if C[p].get(w)]
    for base in ('C', 'C5', 'olderC', 'olderC5'):
        v = [r[base] for r in rows if r[base] is not None]
        lo, hi = boot(v, statistics.median)
        halves = [r[base + '_half'] for r in rows]
        num = sorted(int(x) for x in halves if x.isdigit())
        say(f'{w} {base}: median {pct(statistics.median(v))} (interval {pct(lo)} to {pct(hi)}), range {pct(min(v))} to {pct(max(v))}; '
            f'cells carrying half: median {statistics.median(num) if len(num) == len(halves) else "see cells.csv"}, '
            f'range {num[0]} to {"more than 1,000" if len(num) < len(halves) else num[-1]}, more than 1,000 for {len(halves) - len(num)}')
    top = sorted(rows, key=lambda r: -r['C'])[:6]
    say(f'{w} largest C: ' + '; '.join(f"{r['project']} {pct(r['C'])} ({r['C_cell']})" for r in top))
    top = sorted(rows, key=lambda r: -r['C5'])[:6]
    say(f'{w} largest C5: ' + '; '.join(f"{r['project']} {pct(r['C5'])} ({r['C5_cell']})" for r in top))
say('')
say('Amendment 3: share of downloads flagged ci=true, older and at-or-newer (at R0), per project-week; "other" apart')
for w in WEEKS:
    rows = [C[p][w] for p in P37 if C[p].get(w)]
    d = [r['ci_true_older_minus_newer'] for r in rows if r['ci_true_older_minus_newer'] is not None]
    lo, hi = boot(d, statistics.median)
    say(f'   {w}: median older {pct(statistics.median(r["older_ci_true_share"] for r in rows if r["older_ci_true_share"] is not None))}, '
        f'median at-or-newer {pct(statistics.median(r["at_or_newer_ci_true_share"] for r in rows if r["at_or_newer_ci_true_share"] is not None))}; '
        f'difference older minus at-or-newer: median {100 * statistics.median(d):+.1f} points (interval {100 * lo:+.1f} to {100 * hi:+.1f}), '
        f'older higher for {sum(x > 0 for x in d)} of {len(d)}; ci unknown: {sum(r["older_ci_unknown"] + r["at_or_newer_ci_unknown"] + r["other_ci_unknown"] for r in rows):,} downloads')
say('')

# ---------------------------------------------------------------- the tests of LH012's post hoc readings
tests = []
say('Tests of LH012\'s post hoc readings (brief, "Tests and conventions")')
res = {}
for w in ('W0',) + WEEKS:
    b3 = PSUM[w]['boto3']
    bc = PSUM[w]['botocore']
    t3 = sum(n for _, m, n in b3 if m == '3.9'); ta = sum(n for _, _, n in b3)
    c3 = sum(n for _, m, n in bc if m == '3.9'); ca = sum(n for _, _, n in bc)
    e = Version('1.42.97')
    below = sum(n for v, m, n in b3 if m == '3.9' and V(v) is not None and V(v) < e)
    at = sum(n for v, m, n in b3 if m == '3.9' and V(v) is not None and V(v) == e)
    res[w] = dict(share39=t3 / ta, ratio39=t3 / c3, ratio_all=ta / ca, below=below / t3, at=at / t3, n39=t3, total=ta)
    say(f'   {w}: boto3 Python 3.9 {t3:,} of {ta:,} ({pct(t3 / ta)} per cent); boto3 over botocore on 3.9 {t3 / c3:.2f}, all Pythons {ta / ca:.2f} '
        f'(twice: {2 * ta / ca:.2f}); of the 3.9 downloads below 1.42.97 {pct(below / t3)} per cent, at it {pct(at / t3)}')
t1 = all(res[w]['share39'] > 0.5 for w in WEEKS)
t2 = all(res[w]['ratio39'] >= 2 * res[w]['ratio_all'] for w in WEEKS)
t3_ = all(res[w]['below'] > 0.75 for w in WEEKS)
say(f'   test 1, boto3\'s 3.9 share above one half in W1 and W2: {"holds" if t1 else "does not hold"}')
say(f'   test 2, the 3.9 ratio at least twice the all-Python ratio in W1 and W2: {"holds" if t2 else "does not hold"}')
say(f'   test 3, more than three quarters of boto3\'s 3.9 downloads below 1.42.97 in W1 and W2: {"holds" if t3_ else "does not hold"}')
tests += [dict(test='boto3 3.9 share above one half, W1 and W2', result=str(t1)), dict(test='3.9 ratio at least twice all-Python ratio, W1 and W2', result=str(t2)),
          dict(test='boto3 3.9 more than three quarters below 1.42.97, W1 and W2', result=str(t3_))]


# ---------------------------------------------------------------- 4: version profiles, r0018_walkshare.py's definitions
def decompose(seq):
    """r0018_walkshare.py, unchanged."""
    n = [k for _, k in seq]
    med = [statistics.median(n[max(0, i - 4):i + 5]) for i in range(len(n))]
    plateau = sum(min(x, 1.5 * mm) for x, mm in zip(n, med)) - min(n[0], 1.5 * med[0])
    body = n[1:101]
    rel = [abs(y - x) / x for x, y in zip(body, body[1:]) if x]
    return sum(n), plateau, statistics.median(rel) if rel else float('nan')


def Vfinal(s):
    v = V(s)
    return None if v is None or v.is_prerelease else v


ADM12 = {(r['project'], r['python_minor']): r for r in rd(L12, 'python_admission.csv')}
MINORS12 = sorted({m for (_, m) in ADM12}, key=lambda m: tuple(int(x) for x in m.split('.')))


def adm(p, m, w):
    """As r0018_walkshare.py's ADM row: for W0, LH012's python_admission.csv; for W1 and W2, the same at R0 by the
    week's end (amendment 4), on the same minors as LH012's file."""
    if w == 'W0':
        return ADM12.get((p, m))
    if (p, m) not in ADM12:
        return None
    return dict(any_ge_R_admits=str(not excluded(p, m, REF[p]['R0'], WEEK_END[w])), edge_below_R=edge(p, m, REF[p]['R0']))


def profiles(p, w):
    R = Version(REF[p]['R0'])
    by = defaultdict(lambda: defaultdict(int))
    for v0, m, n in PSUM[w][p]:
        v = Vfinal(v0)
        if v is not None and v < R:
            by[m][v] += n
    out = {}
    for m, c in by.items():
        a = adm(p, m, w)
        if a is None:
            continue
        seq = sorted(c.items(), key=lambda kv: kv[0], reverse=True)
        if a['any_ge_R_admits'] == 'False' and a['edge_below_R']:
            e = Version(a['edge_below_R'])
            seq = [kv for kv in seq if kv[0] <= e]
        out[m] = seq
    return out


walk_rows, prof_rows = [], []
WALK = defaultdict(dict)
for w in ('W0',) + WEEKS:
    tot_clear = tot_older = 0
    for p in P37:
        clear = prob = 0.0
        names = []
        for m, seq in profiles(p, w).items():
            if len(seq) < 12 or sum(k for _, k in seq) < 1_000_000:
                continue
            t, pl, fl = decompose(seq)
            prof_rows.append(dict(project=p, week=w, python_minor=m, start=str(seq[0][0]), versions=len(seq), older_downloads=t,
                                  flatness=fl, walk_shaped=str(fl < 0.05), plateau_mass=pl))
            if fl < 0.05:
                clear += pl
                names.append(m)
        older = P[p][w]['older_bypython']
        WALK[p][w] = clear / older if older else None
        tot_clear += clear
        tot_older += older
        walk_rows.append(dict(project=p, week=w, older_bypython=older, walk_mass=clear, walk_share=share(clear, older),
                              walk_minors=' '.join(sorted(names, key=lambda m: tuple(int(x) for x in m.split('.'))))))
    WALK['_pooled'][w] = tot_clear / tot_older
wr('profiles.csv', prof_rows)
wr('walk.csv', walk_rows)
fl = {w: next(r['flatness'] for r in prof_rows if r['project'] == 'boto3' and r['week'] == w and r['python_minor'] == '3.9') for w in ('W0',) + WEEKS}
st = {w: next(r['start'] for r in prof_rows if r['project'] == 'boto3' and r['week'] == w and r['python_minor'] == '3.9') for w in ('W0',) + WEEKS}
t4 = all(fl[w] < 0.05 for w in WEEKS)
say(f'   test 4 (the walk), boto3\'s Python 3.9 profile below 1.42.97 walk-shaped in W1 and W2: {"holds" if t4 else "does not hold"}; '
    f'flatness W0 {fl["W0"]:.4f}, W1 {fl["W1"]:.4f}, W2 {fl["W2"]:.4f} (start {st["W0"]}, {st["W1"]}, {st["W2"]})')
tests.append(dict(test='boto3 3.9 profile below 1.42.97 walk-shaped, W1 and W2', result=str(t4)))
wr('tests.csv', tests)
say('')
say('Measure 4, described: walk-shaped share of older downloads (r0018_walkshare.py definitions; W0 recomputed from LH012\'s files, record 17.1 pooled)')
say(f'   pooled: W0 {pct(WALK["_pooled"]["W0"])}, W1 {pct(WALK["_pooled"]["W1"])}, W2 {pct(WALK["_pooled"]["W2"])}')
for p in P37:
    if any((WALK[p][w] or 0) > 0.005 for w in ('W0',) + WEEKS):
        say(f'   {p:<16} W0 {pct(WALK[p]["W0"]):>5}  W1 {pct(WALK[p]["W1"]):>5}  W2 {pct(WALK[p]["W2"]):>5}   minors W1: '
            + next(r['walk_minors'] for r in walk_rows if r['project'] == p and r['week'] == 'W1')
            + '; W2: ' + next(r['walk_minors'] for r in walk_rows if r['project'] == p and r['week'] == 'W2'))
for w in ('W0',) + WEEKS:
    say(f'   {w}: median over projects {pct(statistics.median(WALK[p][w] or 0 for p in P37))}; projects over a tenth: {sum((WALK[p][w] or 0) > 0.1 for p in P37)}')
say('')
say('boto3 on Python 3.9 below 1.42.97: median count per block of twenty versions from the edge down (r0018_staircase.py\'s blocks), and 1.42.87 over the mean of 1.42.86 and 1.42.88 (amendment 2)')
stair = []
for w in ('W0',) + WEEKS:
    seq = profiles('boto3', w)['3.9']
    n = [k for _, k in seq]
    blocks = [statistics.median(n[i:i + 20]) for i in range(0, min(len(n), 1200), 20)]
    c = dict((str(v), k) for v, k in seq)
    dip = c.get('1.42.87', 0) / ((c.get('1.42.86', 0) + c.get('1.42.88', 0)) / 2)
    say(f'   {w}: edge {seq[0][0]} {seq[0][1]:,}; blocks: ' + ', '.join(f'{int(b):,}' for b in blocks[:40]))
    say(f'       1.42.86 {c.get("1.42.86", 0):,}, 1.42.87 {c.get("1.42.87", 0):,}, 1.42.88 {c.get("1.42.88", 0):,}; ratio {dip:.2f}')
    for i, b in enumerate(blocks):
        stair.append(dict(week=w, block=i + 1, first_depth=20 * i + 1, median_count=b))
    stair.append(dict(week=w, block='dip', first_depth='', median_count=dip))
wr('boto3_py39_blocks.csv', stair)
say('')

# ---------------------------------------------------------------- 5: secondary, O and P at each week's own reference
sec = []
for p in P37:
    for w, ref in (('W1', 'R1'), ('W2', 'R2')):
        o = older_share(p, w, ref)
        q = python_measure(p, w, ref, REF[p][ref], o['total'])
        sec.append(dict(project=p, week=w, R=REF[p][ref], R_differs_from_R0=REF[p][f'R0_differs_from_{ref}'], O=o['O'], P_lower=q['P_lower'],
                        P_upper=q['P_upper'], class_=classify(q['P_lower'], q['P_upper']) if q['table_check'] == 'ok' else 'description only',
                        O_at_R0=O[p][w]['O']))
wr('secondary.csv', sec)
say('Secondary, described: O and P at each week\'s own reference release (R1 for W1, R2 for W2)')
for w in WEEKS:
    s = [r for r in sec if r['week'] == w]
    ch = [r for r in s if r['R_differs_from_R0'] == 'True']
    say(f'   {w}: median O {pct(statistics.median(r["O"] for r in s))} (at R0 {pct(statistics.median(r["O_at_R0"] for r in s))}); '
        f'{len(ch)} projects with a different reference, O at own R minus O at R0: ' + ', '.join(f'{r["project"]} {100 * (r["O"] - r["O_at_R0"]):+.1f}' for r in ch))
    say(f'      P classes: ' + ', '.join(f'{k} {v}' for k, v in sorted(defaultdict(int, {c: sum(1 for r in s if r["class_"] == c) for c in {r["class_"] for r in s}}).items())))

open(os.path.join(OUT, 'results.txt'), 'w').write('\n'.join(LINES) + '\n')
print('\n'.join(LINES))
