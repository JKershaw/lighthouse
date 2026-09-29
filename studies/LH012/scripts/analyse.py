#!/usr/bin/env python3
"""LH012: every table the record cites, offline, from the retained files in data/ (and LH008's and
LH011's retained files for the "two ways" table). Writes data/analysis/ (or $LH012_OUT).
New for LH012. The measures, classes and conventions are the brief's (brief.md, snapshot of
29 September 2026) with amendments 1 and 2; readings where the brief left a choice are named in
the docstrings below and in amendments.md.
Usage: python3 analyse.py"""
import csv, gzip, os, random, re, statistics, datetime as dt
from collections import defaultdict
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.markers import Marker
from packaging.tags import parse_tag

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, 'data')
ROOT = os.path.dirname(STUDY)
OUT = os.path.join(os.environ.get('LH012_OUT', DATA), 'analysis') if not os.environ.get('LH012_OUT') else os.environ['LH012_OUT']
os.makedirs(OUT, exist_ok=True)
DAYS = [f'2026-09-{d}' for d in range(21, 28)]
WEEK_END = '2026-09-27T23:59:59.999999'
SEED, NBOOT = 20260929, 10000
MINORS_KNOWN = ['2.7'] + ['3.%d' % i for i in range(4, 16)]


def rd(*p):
    with open(os.path.join(*p)) as f:
        return list(csv.DictReader(f))


def wr(name, rows, fields=None):
    fields = fields or (list(rows[0].keys()) if rows else ['empty'])
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(r.get(k, '')) for k in fields})


def fmt(x):
    if isinstance(x, float):
        return f'{x:.6f}'
    return x


_VC = {}


def V(s):
    if s not in _VC:
        try:
            _VC[s] = Version(s)
        except InvalidVersion:
            _VC[s] = None
    return _VC[s]


_SS = {}


def SS(spec):
    if spec not in _SS:
        _SS[spec] = SpecifierSet(spec)
    return _SS[spec]


# ---------------------------------------------------------------- metadata
REF = {r['project']: r for r in rd(DATA, 'reference.csv')}
P37 = sorted(REF)
VERS = defaultdict(dict)
for v in rd(DATA, 'versions.csv'):
    VERS[v['project']][v['version']] = v
DVERS = defaultdict(dict)
for v in rd(DATA, 'dependent_versions.csv'):
    DVERS[v['project']][v['version']] = v
TOP = {r['project']: int(r['rank']) for r in rd(ROOT, 'LH010', 'data', 'top500.csv')}
TOPD = {r['project']: int(r['downloads']) for r in rd(ROOT, 'LH010', 'data', 'top500.csv')}


def usable(v):
    return v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and v['first_upload_utc']


AVAIL = {}


def avail(p, end):
    """Usable versions of one of the 37 uploaded by `end`, as Versions."""
    if (p, end) not in AVAIL:
        AVAIL[(p, end)] = [Version(k) for k, v in VERS[p].items() if usable(v) and v['first_upload_utc'] <= end]
    return AVAIL[(p, end)]


VC = {}


def vclass(p, s):
    if (p, s) not in VC:
        VC[(p, s)] = _vclass(p, s)
    return VC[(p, s)]


def _vclass(p, s):
    """older, at_or_newer, other (pre-release at or above R) or unlisted."""
    if s not in VERS[p]:
        return 'unlisted'
    x = V(s)
    if x is None:
        return 'unlisted'
    R = Version(REF[p]['R'])
    if x < R:
        return 'older'
    return 'other' if (x.is_prerelease or x.is_devrelease) else 'at_or_newer'


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


EXCL_CACHE = {}


def excluded(p, m):
    """True when no usable version at or above R, uploaded by the end of W, admits minor m (amendment 1:
    constant over W)."""
    k = (p, m)
    if k not in EXCL_CACHE:
        R = Version(REF[p]['R'])
        ge = [v for s, v in VERS[p].items() if usable(v) and Version(s) >= R and v['first_upload_utc'] <= WEEK_END]
        EXCL_CACHE[k] = not any(version_admits(v, m) is True for v in ge)
    return EXCL_CACHE[k]


EDGE = {}


def edge(p, m):
    if (p, m) not in EDGE:
        EDGE[(p, m)] = _edge(p, m)
    return EDGE[(p, m)]


def _edge(p, m):
    R = Version(REF[p]['R'])
    below = sorted((Version(s) for s, v in VERS[p].items() if usable(v) and Version(s) < R and version_admits(v, m) is True))
    return str(below[-1]) if below else ''


def pyminor(s):
    return s if re.fullmatch(r'\d+\.\d+', s or '') else ''


def boot(values, stat, seed=SEED, n=NBOOT):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        s = [values[rnd.randrange(len(values))] for _ in values]
        out.append(stat(s))
    out.sort()
    return out[int(0.025 * n)], out[int(0.975 * n) - 1]


def share(a, b):
    return a / b if b else None


# ---------------------------------------------------------------- gap rule on W (and for the first day)
tot37 = defaultdict(int)
proj_days = defaultdict(dict)
for i in (1, 2, 3):
    for r in rd(DATA, 'firstday', f'daily_totals_{i}.csv'):
        tot37[r['date']] += int(r['n'])
        proj_days[r['project']][r['date']] = int(r['n'])
alldates = sorted(tot37)


def is_gap(p, d):
    day = dt.date.fromisoformat(d)
    around = [str(day + dt.timedelta(days=k)) for k in range(-3, 4)]
    vals = [tot37[x] for x in around if x in tot37]
    if d in tot37 and vals and tot37[d] < 0.5 * statistics.median(vals):
        return True
    prev, nxt = str(day - dt.timedelta(days=1)), str(day + dt.timedelta(days=1))
    if d not in proj_days[p] and prev in proj_days[p] and nxt in proj_days[p]:
        return True
    return False


gaps = [dict(project=p, date=d) for p in P37 for d in DAYS if is_gap(p, d)]
wr('gaps_week.csv', gaps, ['project', 'date'])
GAPDAYS = defaultdict(set)
for g in gaps:
    GAPDAYS[g['project']].add(g['date'])

# ---------------------------------------------------------------- per project on W: older share and more
W1 = {}
for p in P37:
    W1[p] = [dict(date=r['date'], version=r['version'], n=int(r['n'])) for r in rd(DATA, 'week', 'versions', p + '.csv')
             if r['date'] not in GAPDAYS[p]]


NEWEST = {}


def newest_on(p, d):
    if (p, d) not in NEWEST:
        NEWEST[(p, d)] = str(max(avail(p, d + 'T23:59:59.999999')))
    return NEWEST[(p, d)]


week_rows = []
OLDER_W1, TOTAL_W1, OLDER_MIX = {}, {}, {}
for p in P37:
    c = defaultdict(int)
    mix = defaultdict(int)
    newest = 0
    for r in W1[p]:
        k = vclass(p, r['version'])
        c[k] += r['n']
        if k == 'older':
            mix[r['version']] += r['n']
        if r['version'] == newest_on(p, r['date']):
            newest += r['n']
    tot = sum(c.values())
    OLDER_W1[p], TOTAL_W1[p], OLDER_MIX[p] = c['older'], tot, mix
    srt = sorted(mix.values(), reverse=True)
    cum, n80 = 0, 0
    for x in srt:
        if cum >= 0.8 * c['older']:
            break
        cum += x
        n80 += 1
    ages = []
    for r in W1[p]:
        if vclass(p, r['version']) == 'older':
            up = VERS[p][r['version']]['first_upload_utc'][:10]
            ages.append(((dt.date.fromisoformat(r['date']) - dt.date.fromisoformat(up)).days, r['n']))
    ages.sort()
    half, acc, med = sum(n for _, n in ages) / 2, 0, None
    for a, n in ages:
        acc += n
        if acc >= half:
            med = a
            break
    over_year = sum(n for a, n in ages if a > 365)
    week_rows.append(dict(project=p, R=REF[p]['R'], R_first_upload=REF[p]['R_first_upload_utc'][:10],
                          gap_days=len(GAPDAYS[p]), total=tot, older=c['older'], at_or_newer=c['at_or_newer'],
                          other=c['other'], unlisted=c['unlisted'], O=share(c['older'], tot),
                          at_or_newer_share=share(c['at_or_newer'], tot), newest_on_day_share=share(newest, tot),
                          older_versions_downloaded=len(mix), n80_older_versions=n80,
                          median_age_older_days=med, share_older_over_365_days=share(over_year, c['older'])))

# ---------------------------------------------------------------- P: Python exclusion
W2 = {p: rd(DATA, 'week', 'python', p + '.csv') for p in P37}
py_rows, py_detail = [], []
P_EST = {}
for p in P37:
    ex = nr = adm = at_edge = 0
    tot2 = 0
    per_minor = defaultdict(lambda: [0, 0])
    for r in W2[p]:
        n = int(r['n'])
        tot2 += n
        if vclass(p, r['version']) != 'older':
            continue
        m = pyminor(r['python_minor'])
        if not m:
            nr += n
        elif excluded(p, m):
            ex += n
            per_minor[m][0] += n
            if r['version'] == edge(p, m):
                at_edge += n
                per_minor[m][1] += n
        else:
            adm += n
    older = ex + nr + adm
    plo, phi = share(ex, older), share(ex + nr, older)
    P_EST[p] = (plo, phi)
    diff = (tot2 - TOTAL_W1[p]) / TOTAL_W1[p] if TOTAL_W1[p] else None
    py_rows.append(dict(project=p, older_W2=older, older_excluded_python=ex, older_python_not_reported=nr,
                        older_admitted_python=adm, P_lower=plo, P_upper=phi, edge_share=share(at_edge, ex),
                        excluded_minors_with_older=' '.join(f'{m}:{v[0]}' for m, v in sorted(per_minor.items())),
                        W2_total=tot2, W1_total=TOTAL_W1[p], W2_vs_W1=diff,
                        W2_check='description only (tables differ by more than 2 per cent)' if diff is not None and abs(diff) > 0.02 else 'ok'))


def classify(lo, hi):
    if lo is None or hi is None:
        return 'unknown'
    if lo > 0.5:
        return 'accounts for most'
    if hi < 0.1:
        return 'accounts for little'
    if hi < 0.5:
        return 'cannot be the main reason'
    return 'undetermined'


nr_heavy = sum(1 for r in py_rows if r['older_W2'] and r['older_python_not_reported'] / r['older_W2'] > 1 / 3)
P_DESCRIPTIVE = nr_heavy > len(P37) / 3
for r in py_rows:
    r['class'] = 'description only' if (P_DESCRIPTIVE or r['W2_check'] != 'ok') else classify(r['P_lower'], r['P_upper'])
wr('python.csv', py_rows)

# ---------------------------------------------------------------- requirements
REQ = defaultdict(list)       # (dependent, version) -> rows naming one of the 37
READ = set()
for r in rd(DATA, 'requirements.csv'):
    if r['parse'] == 'ok' and r['one_of_37'] == 'True':
        REQ[(r['dependent'], r['dependent_version'])].append(dict(name=r['name'], specifier=r['specifier'], marker=r['marker']))
    READ.add((r['dependent'], r['dependent_version']))
for r in rd(DATA, 'top500_screen.csv'):
    if r['status'] == '200':
        READ.add((r['project'], r['latest_version']))
for r in rd(DATA, 'week_versions.csv'):
    READ.add((r['dependent'], r['version']))
p2 = os.path.join(DATA, 'requirements_phase2.csv')
for r in (rd(p2) if os.path.exists(p2) else []):
    if r['parse'] == 'ok':
        REQ[(r['dependent'], r['dependent_version'])].append(dict(name=r['name'], specifier=r['specifier'], marker=r['marker']))
p2r = os.path.join(DATA, 'dependent_reads.csv')
for r in (rd(p2r) if os.path.exists(p2r) else []):
    if r['status'] == '200':
        READ.add((r['dependent'], r['version']))
# phase 1 kept only rows naming one of the 37, with duplicates for the two readings of a version
for k in REQ:
    seen, uniq = set(), []
    for x in REQ[k]:
        t = (x['name'], x['specifier'], x['marker'])
        if t not in seen:
            seen.add(t)
            uniq.append(x)
    REQ[k] = uniq
WEEKV = defaultdict(set)
for r in rd(DATA, 'week_versions.csv'):
    WEEKV[r['dependent']].add(r['version'])

PAIRS = rd(DATA, 'pairs.csv')
DEPS_OF = defaultdict(set)
for r in PAIRS:
    DEPS_OF[r['project']].add(r['dependent'])


def mix_by_day(x):
    path = os.path.join(DATA, 'week', 'versions', x + '.csv') if x in REF else os.path.join(DATA, 'deps', 'versions', x + '.csv')
    if not os.path.exists(path):
        return None
    return [dict(date=r['date'], version=r['version'], n=int(r['n'])) for r in rd(path)]


def py_mix(x):
    path = os.path.join(DATA, 'week', 'python', x + '.csv') if x in REF else os.path.join(DATA, 'deps', 'python', x + '.csv')
    if not os.path.exists(path):
        return None
    m = defaultdict(lambda: defaultdict(int))
    for r in rd(path):
        m[r['version']][pyminor(r['python_minor'])] += int(r['n'])
    return m


PLATFORM_KEYS = ('sys_platform', 'platform_', 'os_name', 'implementation', 'platform_python_implementation')


_SH = {}


def spec_holds(D, spec, day_end):
    """The specifier admits no usable version of D at or above R(D) uploaded by day_end."""
    k = (D, spec, day_end)
    if k not in _SH:
        R = V(REF[D]['R'])
        s = SS(spec)
        _SH[k] = not any(s.contains(v) for v in avail(D, day_end) if v >= R)
    return _SH[k]


def ge_requirements(D, Y, day_end):
    """For each available version of D at or above R, its unconditioned specifier on Y (None if it has
    no requirement on Y; 'unread' if its requirements were not read)."""
    R = Version(REF[D]['R'])
    out = []
    for v in avail(D, day_end):
        if v < R:
            continue
        key = (D, str(v))
        if key not in READ:
            out.append('unread')
            continue
        rows = [x for x in REQ[key] if x['name'] == Y and not x['marker']]
        out.append(rows[0]['specifier'] if rows else None)
    return out


def one_step_holds(D, reqs_of_x, day_end):
    """x holds D through another of the 37, Y (brief: one step)."""
    for x in reqs_of_x:
        Y = x['name']
        if Y == D or x['marker'] or Y not in REF:
            continue
        if (D, Y, day_end) not in _GR:
            _GR[(D, Y, day_end)] = ge_requirements(D, Y, day_end)
        specs = _GR[(D, Y, day_end)]
        if not specs or any(s is None or s == 'unread' for s in specs):
            continue
        adm_x = admitted_set(Y, x['specifier'])
        if all(not (adm_x & admitted_set(Y, s)) for s in specs):
            return Y
    return None


_ADM = {}
_GR = {}


def admitted_set(Y, spec):
    if (Y, spec) not in _ADM:
        s = SS(spec)
        _ADM[(Y, spec)] = frozenset(k for k, v in VERS[Y].items() if v['parse'] == 'ok' and v['is_prerelease'] == 'False' and s.contains(V(k)))
    return _ADM[(Y, spec)]


HS = {}


def hold_status(X, xv, D, day_end, pym):
    k = (X, xv, D, day_end)
    if k not in HS:
        HS[k] = _hold_status(X, xv, D, day_end, pym)
    return HS[k]


def _hold_status(X, xv, D, day_end, pym):
    """Fractions of x's downloads that hold D: returns (held, unknown, extra_unknown, via) where held and
    unknown are fractions of x's downloads (Python markers split by x's Python mix)."""
    key = (X, xv)
    if key not in READ:
        return 0.0, 1.0, 0.0, 'unread'
    rows = [r for r in REQ[key] if r['name'] == D]
    via = ''
    held = unk = ext = 0.0
    if rows:
        extra = [r for r in rows if 'extra' in r['marker']]
        plat = [r for r in rows if 'extra' not in r['marker'] and any(k in r['marker'] for k in PLATFORM_KEYS)]
        pyr = [r for r in rows if r not in extra and r not in plat and r['marker']]
        plain = [r for r in rows if not r['marker']]
        if any(spec_holds(D, r['specifier'], day_end) for r in plain):
            return 1.0, 0.0, 0.0, 'direct'
        if pyr:
            dist = pym.get(xv) if pym else None
            if not dist:
                unk = 1.0
            else:
                t = sum(dist.values())
                for m, n in dist.items():
                    if not m:
                        unk += n / t
                        continue
                    env = {'python_version': m, 'python_full_version': m + '.0', 'extra': ''}
                    if any(Marker(r['marker']).evaluate(env) and spec_holds(D, r['specifier'], day_end) for r in pyr):
                        held += n / t
                via = 'python marker'
        if plat and any(spec_holds(D, r['specifier'], day_end) for r in plat):
            unk = max(unk, 1.0 - held)
            via = via or 'platform marker'
        if extra and any(spec_holds(D, r['specifier'], day_end) for r in extra):
            ext = 1.0 - held - unk
            via = via or 'extra'
        if held or unk or ext:
            return held, unk, ext, via or 'direct'
    Y = one_step_holds(D, REQ[key], day_end)
    if Y:
        return 1.0, 0.0, 0.0, 'one step via ' + Y
    return 0.0, 0.0, 0.0, ''


MIX = {}
PYM = {}


def get_mix(x):
    if x not in MIX:
        MIX[x] = mix_by_day(x)
        PYM[x] = py_mix(x)
    return MIX[x], PYM[x]


bound_rows, dep_rows = [], []
HELD_BY = {}
for D in P37:
    olderD = OLDER_W1[D]
    per_x = []
    for X in sorted(DEPS_OF[D]):
        mix, pym = get_mix(X)
        if mix is None:
            per_x.append(dict(project=D, dependent=X, status='no version mix read'))
            continue
        totX = held_cur = held_old = unk = ext = 0.0
        vias = set()
        admitted = set()
        for r in mix:
            if r['date'] in GAPDAYS[D]:
                continue
            h, u, e, via = hold_status(X, r['version'], D, r['date'] + 'T23:59:59.999999', pym)
            totX += r['n']
            if h:
                if r['version'] in WEEKV[X]:
                    held_cur += h * r['n']
                else:
                    held_old += h * r['n']
                vias.add(via)
                for q in REQ[(X, r['version'])]:
                    if q['name'] == D and 'extra' not in q['marker']:
                        admitted |= admitted_set(D, q['specifier'])
                    elif via.startswith('one step') and q['name'] == via.split()[-1]:
                        pass
            unk += u * r['n']
            ext += e * r['n']
        per_x.append(dict(project=D, dependent=X, rank=TOP.get(X, ''), X_week_fetches=int(totX),
                          fetch_ratio_X_to_D=share(totX, TOTAL_W1[D]), held_by_current_versions=int(held_cur),
                          held_by_older_versions=int(held_old), unknown=int(unk), extra_unknown=int(ext),
                          via=' '.join(sorted(vias)), status='read',
                          _admitted=admitted))
    known = [x for x in per_x if x['status'] == 'read']
    lo_x = max(known, key=lambda x: x['held_by_current_versions'] + x['held_by_older_versions'], default=None)
    lo = (lo_x['held_by_current_versions'] + lo_x['held_by_older_versions']) if lo_x else 0
    hi = sum(x['held_by_current_versions'] + x['held_by_older_versions'] + x['unknown'] + x['extra_unknown'] for x in known)
    missing = [x['dependent'] for x in per_x if x['status'] != 'read']
    Blo, Bhi = (min(1.0, lo / olderD), min(1.0, hi / olderD)) if olderD else (None, None)
    guard = None
    if lo_x and olderD and not any(v.startswith('one step') for v in lo_x['via'].split(' ') if v) and 'one step' not in lo_x['via']:
        at_adm = sum(n for v, n in OLDER_MIX[D].items() if v in lo_x['_admitted'])
        guard = at_adm / olderD
    cls = classify(Blo, Bhi)
    note = ''
    if cls == 'accounts for most' and not (guard is not None and guard > 0.5):
        cls = 'undetermined'
        note = (f"guard failed: {lo_x['dependent']} fetch ratio {lo_x['fetch_ratio_X_to_D']:.2f}" if guard is not None
                else f"guard not computable for a one-step hold by {lo_x['dependent']}")
    if missing and cls in ('cannot be the main reason', 'accounts for little'):
        note += (' ' if note else '') + 'dependents without a mix: ' + ' '.join(missing)
    cur = max((x['held_by_current_versions'] for x in known), default=0)
    bound_rows.append(dict(project=D, older_fetches=olderD, dependents=len(per_x), B_lower=Blo, B_upper=Bhi,
                           lower_from=lo_x['dependent'] if lo_x and lo else '',
                           lower_fetch_ratio=lo_x['fetch_ratio_X_to_D'] if lo_x and lo else '',
                           largest_held_by_current_versions=share(cur, olderD),
                           sum_held_by_current_versions=share(sum(x['held_by_current_versions'] for x in known), olderD),
                           sum_held_by_older_versions=share(sum(x['held_by_older_versions'] for x in known), olderD),
                           sum_unknown_unread_or_marker=share(sum(x['unknown'] for x in known), olderD),
                           sum_extra_unknown=share(sum(x['extra_unknown'] for x in known), olderD),
                           guard_share_at_admitted=guard, class_=cls, note=note))
    for x in per_x:
        x.pop('_admitted', None)
        dep_rows.append(x)
for r in bound_rows:
    r['class'] = r.pop('class_')
wr('bounds.csv', bound_rows)
wr('bounds_by_dependent.csv', dep_rows, ['project', 'dependent', 'rank', 'status', 'X_week_fetches', 'fetch_ratio_X_to_D',
                                         'held_by_current_versions', 'held_by_older_versions', 'unknown', 'extra_unknown', 'via'])
B_EST = {r['project']: (r['B_lower'], r['B_upper']) for r in bound_rows}

# ---------------------------------------------------------------- tightly coupled pairs: F, Z, O(D)
WK = {(r['dependent'], r['version']) for r in rd(DATA, 'week_versions.csv')}


def tight_pairs():
    vers = defaultdict(list)
    for v in rd(DATA, 'versions.csv'):
        if usable(v) and v['first_upload_utc'] <= WEEK_END:
            vers[v['project']].append(Version(v['version']))
    out = {}
    for r in PAIRS:
        if r['extra_only'] == 'True' or (r['dependent'], r['dependent_version']) not in WK or r['has_upper_bound'] != 'True':
            continue
        n = sum(SpecifierSet(r['specifier']).contains(v) for v in vers[r['project']])
        k = (r['dependent'], r['project'])
        out[k] = min(out.get(k, 99), n)
    return sorted(k for k, n in out.items() if n <= 10 and TOPD[k[0]] >= 0.1 * TOPD[k[1]])


def newest_period_end(X, xv):
    """The last moment xv was X's newest: the first upload of the next higher usable version after it,
    or its own upload when it never was newest, or the end of W when it still was."""
    vv = DVERS[X] if X not in REF else VERS[X]
    me = vv.get(xv)
    if not me or not me['first_upload_utc']:
        return None
    x = V(xv)
    up = me['first_upload_utc']
    later_higher = [v['first_upload_utc'] for k, v in vv.items() if v['parse'] == 'ok' and v['is_prerelease'] == 'False'
                    and v['all_yanked'] == 'False' and v['first_upload_utc'] and V(k) and V(k) > x]
    earlier_higher = [t for t in later_higher if t <= up]
    if earlier_higher:
        return up  # never newest: resolved at its own upload (amendment 3)
    return min(later_higher) if later_higher and min(later_higher) <= WEEK_END else WEEK_END


tight_rows = []
CAND = {}
for X, D in tight_pairs():
    mix, pym = get_mix(X)
    totX = sum(r['n'] for r in mix if r['date'] not in GAPDAYS[D])
    olderD = OLDER_W1[D]
    Fh = Fu = Zh = Zu = 0.0
    exact = True
    pred = defaultdict(float)
    covered = 0.0
    for r in mix:
        if r['date'] in GAPDAYS[D]:
            continue
        key = (X, r['version'])
        rows = [q for q in REQ[key] if q['name'] == D and 'extra' not in q['marker']]
        if key not in READ:
            Fu += r['n']
            Zu += r['n']
            continue
        covered += r['n']
        h, u, e, via = hold_status(X, r['version'], D, r['date'] + 'T23:59:59.999999', pym)
        if via.startswith('one step'):
            h = 0.0  # the number test is about X's own bound on D
        Fh += h * r['n']
        Fu += u * r['n']
        t = newest_period_end(X, r['version'])
        plain = [q for q in rows if not q['marker']]
        if t is None or not plain:
            if not rows:
                pass  # no requirement on D: resolves to D's newest, not older
            else:
                Zu += r['n']
            exact = False
            continue
        ck = (D, plain[0]['specifier'], t)
        if ck not in CAND:
            s = SS(plain[0]['specifier'])
            CAND[ck] = sorted(v for v in avail(D, t) if s.contains(v))
        cand = CAND[ck]
        if not cand:
            Zu += r['n']
        elif cand[-1] < Version(REF[D]['R']):
            Zh += r['n']
        spec = plain[0]['specifier']
        if spec.startswith('==') and ',' not in spec and '*' not in spec:
            pred[spec[2:]] += r['n']
        else:
            exact = False
    F = (Fh / totX, (Fh + Fu) / totX) if totX else (None, None)
    Z = (Zh / totX, (Zh + Zu) / totX) if totX else (None, None)

    def reading(lo, hi):
        if lo is None:
            return 'unknown'
        if lo * totX >= 0.5 * olderD:
            return 'accounts for at least half'
        if hi * totX < 0.5 * olderD:
            return 'does not'
        return 'undetermined'
    tvd = ''
    if exact and pred:
        allD = defaultdict(int)
        for r in W1[D]:
            allD[r['version']] += r['n']
        tp, to = sum(pred.values()), sum(allD.values())
        keys = set(pred) | set(allD)
        tvd = 0.5 * sum(abs(pred.get(k, 0) / tp - allD.get(k, 0) / to) for k in keys)
    tight_rows.append(dict(X=X, D=D, X_week_fetches=int(totX), D_week_fetches=TOTAL_W1[D], ratio_X_to_D=share(totX, TOTAL_W1[D]),
                           X_fetches_covered=share(covered, totX), F_lower=F[0], F_upper=F[1], Z_lower=Z[0], Z_upper=Z[1],
                           O_D=share(olderD, TOTAL_W1[D]), D_older_fetches=olderD,
                           fresh_predicted_older_fetches_lower=int(F[0] * totX) if totX else '',
                           fresh_predicted_older_fetches_upper=int(F[1] * totX) if totX else '',
                           frozen_predicted_older_fetches_lower=int(Z[0] * totX) if totX else '',
                           frozen_predicted_older_fetches_upper=int(Z[1] * totX) if totX else '',
                           F_reading=reading(*F), Z_reading=reading(*Z), exact_pin_tvd=tvd))
wr('tight_pairs.csv', tight_rows)

# ---------------------------------------------------------------- frozen-list descriptors and the trace
bound_edges = defaultdict(set)
for D in P37:
    for X in DEPS_OF[D]:
        mix, pym = get_mix(X)
        if not mix:
            continue
        tot = defaultdict(int)
        for r in mix:
            tot[r['version']] += r['n']
        T = sum(tot.values())
        for xv, n in tot.items():
            if T and n / T < 0.001:
                continue
            h, u, e, via = hold_status(X, xv, D, WEEK_END, pym)
            if not h or via.startswith('one step'):
                continue
            for q in REQ[(X, xv)]:
                if q['name'] == D and 'extra' not in q['marker']:
                    ck = (D, q['specifier'], WEEK_END)
                    if ck not in CAND:
                        s = SS(q['specifier'])
                        CAND[ck] = sorted(v for v in avail(D, WEEK_END) if s.contains(v))
                    c = CAND[ck]
                    if c:
                        bound_edges[D].add(str(c[-1]))

frozen_rows = []
for p in P37:
    ps = rd(DATA, 'week', 'pass', p + '.csv')
    agg = defaultdict(int)
    for r in ps:
        if r['date'] in GAPDAYS[p]:
            continue
        agg[(r['cls'], r['installer'], r['ci'], r['system'], r['libc_lib'], r['type'])] += int(r['n'])
    out = dict(project=p)
    for cls in ('older', 'at_or_newer'):
        t = sum(n for k, n in agg.items() if k[0] == cls)
        pu = sum(n for k, n in agg.items() if k[0] == cls and k[1] in ('pip', 'uv'))
        ci = sum(n for k, n in agg.items() if k[0] == cls and k[1] in ('pip', 'uv') and k[2] == 'true')
        out[f'{cls}_total'] = t
        out[f'{cls}_ci_share_pip_uv'] = share(ci, pu)
        out[f'{cls}_unknown_flag_values'] = sum(n for k, n in agg.items() if k[0] == cls and k[2] == 'unknown')
        for inst in ('pip', 'uv', 'poetry', 'pdm', 'requests', ''):
            out[f'{cls}_installer_{inst or "none"}'] = share(sum(n for k, n in agg.items() if k[0] == cls and k[1] == inst), t)
        out[f'{cls}_installer_other'] = share(sum(n for k, n in agg.items() if k[0] == cls and k[1] not in ('pip', 'uv', 'poetry', 'pdm', 'requests', '')), t)
        for sysn in ('Linux', 'Windows', 'Darwin', ''):
            out[f'{cls}_system_{sysn or "none"}'] = share(sum(n for k, n in agg.items() if k[0] == cls and k[3] == sysn), t)
        lp = sum(n for k, n in agg.items() if k[0] == cls and k[1] == 'pip' and k[3] == 'Linux')
        out[f'{cls}_pip_linux_glibc'] = share(sum(n for k, n in agg.items() if k[0] == cls and k[1] == 'pip' and k[3] == 'Linux' and k[4] == 'glibc'), lp)
        lu = sum(n for k, n in agg.items() if k[0] == cls and k[1] == 'uv' and k[3] == 'Linux')
        out[f'{cls}_uv_linux_musl'] = share(sum(n for k, n in agg.items() if k[0] == cls and k[1] == 'uv' and k[3] == 'Linux' and k[4] == 'musl'), lu)
        out[f'{cls}_sdist'] = share(sum(n for k, n in agg.items() if k[0] == cls and k[5] == 'sdist'), t)
    a, b = out['older_ci_share_pip_uv'], out['at_or_newer_ci_share_pip_uv']
    out['ci_difference_points'] = (a - b) * 100 if a is not None and b is not None else None
    out['pass_total_vs_W1'] = share(sum(agg.values()) - TOTAL_W1[p], TOTAL_W1[p])
    # off-edge share of older downloads (W2), with E(p) for excluded Pythons only (amendment 3)
    off = on = 0
    for r in W2[p]:
        if vclass(p, r['version']) != 'older':
            continue
        n = int(r['n'])
        m = pyminor(r['python_minor'])
        at = (m and excluded(p, m) and r['version'] == edge(p, m)) or r['version'] in bound_edges[p]
        if at:
            on += n
        else:
            off += n
    out['older_off_edge_share'] = share(off, off + on)
    out['bound_edges'] = len(bound_edges[p])
    out['shows_frozen_list_trace'] = bool(out['older_off_edge_share'] is not None and out['older_off_edge_share'] > 0.5
                                          and out['ci_difference_points'] is not None and out['ci_difference_points'] > 0)
    frozen_rows.append(out)
wr('frozen.csv', frozen_rows)

# ---------------------------------------------------------------- residual
res_rows = []
for w in week_rows:
    p = w['project']
    plo, phi = P_EST[p]
    blo, bhi = B_EST[p]
    O = w['O']
    if None in (plo, phi, blo, bhi, O):
        res_rows.append(dict(project=p, O=O))
        continue
    acc_hi, acc_lo = min(1.0, phi + bhi), max(plo, blo)
    res_rows.append(dict(project=p, O=O, accounted_lower=acc_lo, accounted_upper=acc_hi,
                         residual_share_of_downloads_lower=O * (1 - acc_hi), residual_share_of_downloads_upper=O * (1 - acc_lo),
                         residual_share_of_older_lower=1 - acc_hi, residual_share_of_older_upper=1 - acc_lo))
wr('residual.csv', res_rows)

# ---------------------------------------------------------------- files (secondary)
PLAT_RE = re.compile(r'^(manylinux|musllinux)_(\d+)_(\d+)_(.+)$')
LEGACY = {'manylinux1': (2, 5), 'manylinux2010': (2, 12), 'manylinux2014': (2, 17)}


def plat_key(tag):
    """(family, arch, floor) for a platform tag; floor is a tuple, or None."""
    for leg, fl in LEGACY.items():
        if tag.startswith(leg + '_'):
            return 'manylinux', tag[len(leg) + 1:], fl
    m = PLAT_RE.match(tag)
    if m:
        return m.group(1), m.group(4), (int(m.group(2)), int(m.group(3)))
    m = re.match(r'^macosx_(\d+)_(\d+)_(.+)$', tag)
    if m:
        return 'macosx', m.group(3), (int(m.group(1)), int(m.group(2)))
    if tag.startswith('win'):
        return 'win', tag, None
    return tag, '', None


def interp_ok(interp, abi, m):
    """Does a wheel with this interpreter and ABI tag install on Python minor m (CPython assumed)?"""
    mm = m.replace('.', '')
    for it in interp.split('.'):
        if it in ('py3', 'py2.py3', 'py' + mm[0]) or it == 'py' + mm:
            return True
        if it == 'cp' + mm:
            return True
        if abi == 'abi3' and it.startswith('cp3') and Version(it[2] + '.' + it[3:]) <= Version(m):
            return True
    return False


file_rows = []
fdir = os.path.join(DATA, 'week', 'files')
for p in sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []:
    p = p[:-4]
    R = Version(REF[p]['R'])
    ge_wheels = []
    with gzip.open(os.path.join(DATA, 'files.csv.gz'), 'rt') as f:
        for r in csv.DictReader(f):
            if r['project'] == p and r['packagetype'] == 'bdist_wheel' and V(r['version']) and V(r['version']) >= R \
                    and usable(VERS[p][r['version']]) and r['upload_time_utc'] <= WEEK_END:
                parts = r['filename'][:-4].split('-')
                ge_wheels.append((parts[-3], parts[-2], parts[-1]))
    c = defaultdict(int)
    for r in rd(fdir, p + '.csv'):
        n = int(r['n'])
        if r['plat'] in ('(not a wheel)', '(no file name)'):
            c[r['plat']] += n
            continue
        m = pyminor(r['python_minor'])
        if not m:
            c['python not reported'] += n
            continue
        okw = False
        for plat in r['plat'].split('.'):
            fam, arch, floor = plat_key(plat)
            for gi, ga, gp in ge_wheels:
                if not interp_ok(gi, ga, m):
                    continue
                for g in gp.split('.'):
                    gf, garch, gfl = plat_key(g)
                    if g == 'any' or (gf == fam and garch == arch and (gfl is None or floor is None or gfl <= floor)):
                        okw = True
                        break
                if okw:
                    break
            if okw:
                break
        c['wheel available at or above R' if okw else 'wheel-excluded'] += n
    t = sum(c.values())
    file_rows.append(dict(project=p, older_downloads=t, **{k: share(v, t) for k, v in sorted(c.items())}))
wr('files.csv', file_rows, ['project', 'older_downloads', 'wheel-excluded', 'wheel available at or above R', '(not a wheel)',
                            '(no file name)', 'python not reported'])

# ---------------------------------------------------------------- across projects
def summary_block(name, rows, lo_k, hi_k, cls_k):
    known = [r for r in rows if r.get(cls_k) not in (None, 'unknown', 'description only')]
    out = []
    for cls in ('accounts for most', 'undetermined', 'cannot be the main reason', 'accounts for little'):
        members = [r['project'] for r in known if r[cls_k] == cls]
        if cls == 'cannot be the main reason':
            members_all = [r['project'] for r in known if r[cls_k] in ('cannot be the main reason', 'accounts for little')]
        else:
            members_all = members
        flags = [1 if r['project'] in members_all else 0 for r in known]
        ci = boot(flags, lambda s: sum(s) / len(s)) if flags else ('', '')
        out.append(dict(explanation=name, class_=cls + (' (including accounts for little)' if cls == 'cannot be the main reason' else ''),
                        projects=len(members_all), of_known=len(known), share=share(len(members_all), len(known)),
                        ci_low=ci[0], ci_high=ci[1], list=' '.join(sorted(members_all))))
    for k in (lo_k, hi_k):
        vals = [r[k] for r in known if r[k] is not None]
        med = statistics.median(vals) if vals else None
        ci = boot(vals, statistics.median) if vals else ('', '')
        out.append(dict(explanation=name, class_=f'median of project {k}', projects='', of_known=len(vals), share=med,
                        ci_low=ci[0], ci_high=ci[1], list=''))
    for r in out:
        r['class'] = r.pop('class_')
    return out


summ = summary_block('Python exclusion (P)', py_rows, 'P_lower', 'P_upper', 'class') + \
    summary_block('identified bounds (B)', bound_rows, 'B_lower', 'B_upper', 'class')
tot_older = sum(r['older_W2'] for r in py_rows)
pooled = [dict(explanation='pooled', class_='P lower, all 37 projects\' older downloads', share=share(sum(r['older_excluded_python'] for r in py_rows), tot_older)),
          dict(explanation='pooled', class_='P upper', share=share(sum(r['older_excluded_python'] + r['older_python_not_reported'] for r in py_rows), tot_older)),
          dict(explanation='pooled', class_='older share O of all 37 projects\' downloads', share=share(sum(OLDER_W1.values()), sum(TOTAL_W1.values())))]
for r in pooled:
    r['class'] = r.pop('class_')
trace = [r['project'] for r in frozen_rows if r['shows_frozen_list_trace']]
summ.append(dict(explanation='frozen-list trace (described)', **{'class': 'shows the trace'}, projects=len(trace), of_known=len(frozen_rows),
                 share=share(len(trace), len(frozen_rows)), list=' '.join(trace)))
vals = [r['O'] for r in week_rows]
ci = boot(vals, statistics.median)
summ.append(dict(explanation='older share O', **{'class': 'median of projects'}, of_known=len(vals), share=statistics.median(vals), ci_low=ci[0], ci_high=ci[1]))
wr('summary.csv', summ + pooled, ['explanation', 'class', 'projects', 'of_known', 'share', 'ci_low', 'ci_high', 'list'])
wr('week.csv', week_rows)

# ---------------------------------------------------------------- the first day, November to March
nm = rd(DATA, 'releases_nov_mar.csv')
fd_rows = []
for p in P37:
    rel = [r for r in nm if r['project'] == p]
    if not rel:
        continue
    cnt = defaultdict(dict)
    for r in rd(DATA, 'firstday', 'counts', p + '.csv'):
        cnt[r['date']][r['v']] = int(r['n'])
    for r in rel:
        x = Version(r['version'])
        s = {}
        for k in (1, 2, 30):
            d = str(dt.date.fromisoformat(r['day0']) + dt.timedelta(days=k))
            if is_gap(p, d) or d not in cnt:
                s[k] = None
                continue
            tot = sum(cnt[d].values())
            num = sum(n for v, n in cnt[d].items() if v != '~other' and V(v) and V(v) >= x and not V(v).is_prerelease)
            s[k] = num / tot if tot else None
        delta = (s[30] - s[2]) * 100 if s[2] is not None and s[30] is not None else None
        fd_rows.append(dict(project=p, version=r['version'], day0=r['day0'], yanked=r['yanked_all_files'],
                            s1=s[1], s2=s[2], s30=s[30], delta_points=delta,
                            settled='' if delta is None else abs(delta) <= 10,
                            ratio_s2_s30=share(s[2], s[30]) if s[2] is not None and s[30] else None,
                            delta_from_day1_points=(s[30] - s[1]) * 100 if s[1] is not None and s[30] is not None else None))
wr('firstday_releases.csv', fd_rows)


def project_settle(rows):
    out = []
    for p in sorted({r['project'] for r in rows}):
        k = [r for r in rows if r['project'] == p and r['settled'] != '']
        if not k:
            continue
        n = sum(1 for r in k if r['settled'])
        out.append(dict(project=p, releases_known=len(k), settled=n, project_settles=n > len(k) / 2,
                        median_delta_points=statistics.median(r['delta_points'] for r in k)))
    return out


fdp = project_settle(fd_rows)
wr('firstday_projects.csv', fdp)
flags = [1 if r['project_settles'] else 0 for r in fdp]
ci = boot(flags, lambda s: sum(s) / len(s)) if flags else ('', '')
sh = share(sum(flags), len(flags))
verdict = 'inconclusive' if len(flags) < 20 else ('holds as a rule' if sh >= 0.75 else ('holds for some projects' if sh >= 0.5 else 'fails'))
# the same measure on LH011's April to August releases (data already read; not a test)
lh = defaultdict(dict)
for r in rd(ROOT, 'LH011', 'data', 'analysis', 'release_days.csv'):
    if r['status'] == 'known' and r['day'] in ('1', '2', '30'):
        lh[(r['project'], r['version'])][int(r['day'])] = float(r['share_at_or_newer'])
lh_rows = []
for (p, v), s in sorted(lh.items()):
    if 2 in s and 30 in s:
        d = (s[30] - s[2]) * 100
        lh_rows.append(dict(project=p, version=v, delta_points=d, settled=abs(d) <= 10))
lhp = project_settle(lh_rows)
wr('firstday_lh011_projects.csv', lhp)
pooled_rel = [r for r in fd_rows if r['settled'] != '']
wr('firstday_summary.csv', [
    dict(set='November 2025 to March 2026 (the test)', projects_known=len(flags), projects_settle=sum(flags), share=sh,
         ci_low=ci[0], ci_high=ci[1], reading=verdict, releases_known=len(pooled_rel),
         releases_settled=sum(1 for r in pooled_rel if r['settled'])),
    dict(set='April to August 2026, LH011 releases (already read; not a test)', projects_known=len(lhp),
         projects_settle=sum(1 for r in lhp if r['project_settles']), share=share(sum(1 for r in lhp if r['project_settles']), len(lhp)),
         reading='description', releases_known=len(lh_rows), releases_settled=sum(1 for r in lh_rows if r['settled']))])

# ---------------------------------------------------------------- the same releases read two ways
LH8 = os.path.join(ROOT, 'LH008', 'data')
ev = [r for r in rd(LH8, 'events.csv') if r['chosen'] == 'yes']
lags = [r for r in rd(LH8, 'lags.csv') if r['kind'] == 'fix']
rel_day = {}
for r in rd(ROOT, 'LH011', 'data', 'analysis', 'release_days.csv'):
    if r['status'] == 'known':
        rel_day[(r['project'], r['version'], int(r['day']))] = float(r['share_at_or_newer'])
tw = []
for e in ev:
    lib, v = e['library'], e['fixed_release']
    pairs = [r for r in lags if r['library'] == lib]
    for d in range(1, 31):
        moved = sum(1 for r in pairs if r['outcome'] == 'moved' and r['lag_release_days'] and float(r['lag_release_days']) <= d)
        tw.append(dict(library=lib, fixed_release=v, day=d, pinned_pairs=len(pairs), moved_by_day=moved,
                       moved_share=share(moved, len(pairs)), download_share_at_or_newer=rel_day.get((lib, v, d), '')))
wr('two_ways.csv', tw)
print('analysis written to', OUT)
