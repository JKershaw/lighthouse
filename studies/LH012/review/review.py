#!/usr/bin/env python3
"""R-0016: the review's own recomputation of LH012's headline figures from the retained files in data/,
without calling scripts/analyse.py. Same definitions as the brief (edition 0.1) with amendments 1 to 3,
own code, own bootstrap draws (nearest-rank percentile ends). Prints, beside each figure, what the record
gives. Also: the Python-exclusion set on each day of the week against the week-end table; B for all 37
projects with the guard; the frozen-list trace under amendment 3.1 and under the brief's literal wording;
the wheel-exclusion classes with 'any'-platform wheels set apart; the first-day test; the "two ways" table;
the read log against the record's Method figures. Usage: python3 review.py > review.txt"""
import csv, gzip, math, os, random, re, statistics, datetime as dt
from collections import defaultdict
from packaging.version import Version, InvalidVersion
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.markers import Marker

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, 'data')
ROOT = os.path.dirname(STUDY)
DAYS = [f'2026-09-{d}' for d in range(21, 28)]
WEND = '2026-09-27T23:59:59.999999'


def rd(*p):
    return list(csv.DictReader(open(os.path.join(*p))))


_v = {}


def V(s):
    if s not in _v:
        try:
            _v[s] = Version(s)
        except InvalidVersion:
            _v[s] = None
    return _v[s]


def pct(x, d=1):
    return f'{x * 100:.{d}f}'


def norm(name):
    return re.sub(r'[-_.]+', '-', name).lower()


def boot_ci(vals, stat, seed=20260929, n=10000):
    """Percentile interval over n resamples with replacement; ends by nearest rank."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        out.append(stat([rnd.choice(vals) for _ in vals]))
    out.sort()
    return out[math.ceil(0.025 * n) - 1], out[math.ceil(0.975 * n) - 1]


def mean(s):
    return sum(s) / len(s)


REF = {r['project']: r['R'] for r in rd(DATA, 'reference.csv')}
P37 = sorted(REF)
VERS = defaultdict(dict)
for r in rd(DATA, 'versions.csv'):
    VERS[r['project']][r['version']] = r
DVERS = defaultdict(dict)
for r in rd(DATA, 'dependent_versions.csv'):
    DVERS[r['project']][r['version']] = r
TOPD = {r['project']: int(r['downloads']) for r in rd(ROOT, 'LH010', 'data', 'top500.csv')}


def usable(v):
    return v['parse'] == 'ok' and v['is_prerelease'] == 'False' and v['all_yanked'] == 'False' and bool(v['first_upload_utc'])


def cls(p, s):
    """older (numbered below R), ge (R or a higher final release), other (pre-release above R), unlisted."""
    if s not in VERS[p] or V(s) is None:
        return 'unlisted'
    x, R = V(s), V(REF[p])
    if x < R:
        return 'older'
    return 'other' if (x.is_prerelease or x.is_devrelease) else 'ge'


def admits(rp, m):
    """A version admits minor m when any of its files' Requires-Python (joined by ' | ') contains some m.k, k 0..30; blank admits all."""
    if not rp:
        return True
    for part in rp.split(' | '):
        if not part.strip():
            return True
        try:
            s = SpecifierSet(part)
        except InvalidSpecifier:
            continue
        if any(s.contains(Version(f'{m}.{k}'), prereleases=True) for k in range(31)):
            return True
    return False


def ge_versions(p, end):
    R = V(REF[p])
    return [v for s, v in VERS[p].items() if usable(v) and V(s) is not None and V(s) >= R and v['first_upload_utc'] <= end]


_ex = {}


def excluded(p, m, end=WEND):
    k = (p, m, end)
    if k not in _ex:
        _ex[k] = not any(admits(v['requires_python'], m) for v in ge_versions(p, end))
    return _ex[k]


_edge = {}


def edge(p, m):
    """The highest usable version below R that admits m."""
    if (p, m) not in _edge:
        R = V(REF[p])
        c = [V(s) for s, v in VERS[p].items() if usable(v) and V(s) is not None and V(s) < R and admits(v['requires_python'], m)]
        _edge[(p, m)] = str(max(c)) if c else ''
    return _edge[(p, m)]


MINOR = re.compile(r'\d+\.\d+')

# ------------------------------------------------------------------ gap rule
tot37, pdays = defaultdict(int), defaultdict(dict)
for i in (1, 2, 3):
    for r in rd(DATA, 'firstday', f'daily_totals_{i}.csv'):
        tot37[r['date']] += int(r['n'])
        pdays[r['project']][r['date']] = int(r['n'])


def is_gap(p, d):
    day = dt.date.fromisoformat(d)
    around = [tot37[x] for x in (str(day + dt.timedelta(days=k)) for k in range(-3, 4)) if x in tot37]
    if d in tot37 and around and tot37[d] < 0.5 * statistics.median(around):
        return True
    prev, nxt = str(day - dt.timedelta(days=1)), str(day + dt.timedelta(days=1))
    return d not in pdays[p] and prev in pdays[p] and nxt in pdays[p]


gaps = [(p, d) for p in P37 for d in DAYS if is_gap(p, d)]
print('R-0016 recomputation from studies/LH012/data/, own code\n')
print(f'0. gap days in the read week: {gaps if gaps else "none"} (record: none)\n')

# ------------------------------------------------------------------ A. older share and its descriptors
print('A. Older share O and its descriptors (record: median 37.3 [33.8 to 46.7], pyjwt 20.0 to pydantic-core 99.3, pooled 45.6;')
print('   median 7 older versions for 80 per cent, median fetch-weighted age 298 days, median 42.7 per cent over a year old)')
O, OLDER, TOTAL, MIX = {}, {}, {}, {}
n80s, ages_med, over_year = {}, {}, {}
unl, other = {}, {}
for p in P37:
    c, mix, ages = defaultdict(int), defaultdict(int), []
    for r in rd(DATA, 'week', 'versions', p + '.csv'):
        k, n = cls(p, r['version']), int(r['n'])
        c[k] += n
        if k == 'older':
            mix[r['version']] += n
            up = VERS[p][r['version']]['first_upload_utc'][:10]
            ages.append(((dt.date.fromisoformat(r['date']) - dt.date.fromisoformat(up)).days, n))
    tot = sum(c.values())
    O[p], OLDER[p], TOTAL[p], MIX[p] = c['older'] / tot, c['older'], tot, mix
    unl[p], other[p] = c['unlisted'], c['other']
    acc = k80 = 0
    for x in sorted(mix.values(), reverse=True):
        if acc >= 0.8 * c['older']:
            break
        acc += x
        k80 += 1
    n80s[p] = k80
    ages.sort()
    half, acc = sum(n for _, n in ages) / 2, 0
    for a, n in ages:
        acc += n
        if acc >= half:
            ages_med[p] = a
            break
    over_year[p] = sum(n for a, n in ages if a > 365) / c['older']
vals = [O[p] for p in P37]
lo, hi = boot_ci(vals, statistics.median)
mn, mx = min(P37, key=O.get), max(P37, key=O.get)
print(f'   median O {pct(statistics.median(vals))} [{pct(lo)} to {pct(hi)}]; {mn} {pct(O[mn])} to {mx} {pct(O[mx])}; pooled {pct(sum(OLDER.values()) / sum(TOTAL.values()))}')
print(f'   median older versions for 80 per cent {statistics.median(n80s.values())}; median fetch-weighted age {statistics.median(ages_med.values())} days; '
      f'median share over a year old {pct(statistics.median(over_year.values()))}')
print(f'   unlisted versions, largest: {sorted(unl.items(), key=lambda x: -x[1])[:3]}; pre-releases above R, largest: {sorted(other.items(), key=lambda x: -x[1])[:2]}\n')

# ------------------------------------------------------------------ B. Python exclusion P
print('B. Python exclusion P (record: 3 most [aiobotocore boto3 numpy], 2 undetermined [pandas urllib3], 32 cannot [86.5, 75.7 to 97.3], 8 little;')
print('   median P 12.2 [7.1 to 20.9] lower and 18.0 [12.0 to 27.6] upper; pooled 30.9 to 35.3; median edge share 67.5, boto3 6.7, aiobotocore 0.6)')
W2 = {p: rd(DATA, 'week', 'python', p + '.csv') for p in P37}
PLO, PHI, PCLS, EDGE_SHARE, NR_SHARE = {}, {}, {}, {}, {}
pool_ex = pool_nr = pool_old = 0
W2TOT = {}
for p in P37:
    ex = nr = ad = at = tot2 = 0
    for r in W2[p]:
        n = int(r['n'])
        tot2 += n
        if cls(p, r['version']) != 'older':
            continue
        m = r['python_minor']
        if not MINOR.fullmatch(m or ''):
            nr += n
        elif excluded(p, m):
            ex += n
            at += n * (r['version'] == edge(p, m))
        else:
            ad += n
    older = ex + nr + ad
    W2TOT[p] = tot2
    PLO[p], PHI[p] = ex / older, (ex + nr) / older
    EDGE_SHARE[p], NR_SHARE[p] = (at / ex if ex else None), nr / older
    pool_ex, pool_nr, pool_old = pool_ex + ex, pool_nr + nr, pool_old + older


def classify(lo, hi):
    if lo > 0.5:
        return 'most'
    if hi < 0.1:
        return 'little'
    if hi < 0.5:
        return 'cannot'
    return 'undetermined'


for p in P37:
    PCLS[p] = classify(PLO[p], PHI[p])
groups = defaultdict(list)
for p in P37:
    groups[PCLS[p]].append(p)
cannot_all = sorted(groups['cannot'] + groups['little'])
flags = [1 if p in cannot_all else 0 for p in P37]
lo, hi = boot_ci(flags, mean)
print(f'   most {len(groups["most"])} {groups["most"]}; undetermined {len(groups["undetermined"])} {groups["undetermined"]}; '
      f'cannot (incl. little) {len(cannot_all)} of 37 = {pct(mean(flags))} [{pct(lo)} to {pct(hi)}]; little {len(groups["little"])} {groups["little"]}')
for p in ('boto3', 'aiobotocore', 'numpy', 'pandas', 'urllib3', 'botocore', 's3transfer', 'fsspec', 'litellm'):
    print(f'   {p}: P {pct(PLO[p])} to {pct(PHI[p])} ({PCLS[p]}), edge share {pct(EDGE_SHARE[p])}, no Python {pct(NR_SHARE[p])}')
lo1, hi1 = boot_ci([PLO[p] for p in P37], statistics.median)
lo2, hi2 = boot_ci([PHI[p] for p in P37], statistics.median)
print(f'   median P lower {pct(statistics.median(PLO.values()))} [{pct(lo1)} to {pct(hi1)}], upper {pct(statistics.median(PHI.values()))} [{pct(lo2)} to {pct(hi2)}]; '
      f'pooled {pct(pool_ex / pool_old)} to {pct((pool_ex + pool_nr) / pool_old)}')
print(f'   median edge share {pct(statistics.median(v for v in EDGE_SHARE.values() if v is not None))}; projects with over a third of older downloads without a Python: '
      f'{[p for p in P37 if NR_SHARE[p] > 1 / 3]}; by-Python total differs from per-version total by more than 2 per cent: '
      f'{[p for p in P37 if abs(W2TOT[p] - TOTAL[p]) / TOTAL[p] > 0.02]}')
# the week-end admission table against each day's: any version at or above R uploaded during the week, and whether the excluded set changes
changed = []
for p in P37:
    inweek = [s for s, v in VERS[p].items() if usable(v) and V(s) is not None and V(s) >= V(REF[p]) and '2026-09-21' <= v['first_upload_utc'][:10] <= '2026-09-27']
    minors = {r['python_minor'] for r in W2[p] if MINOR.fullmatch(r['python_minor'] or '')}
    for d in DAYS:
        end = d + 'T23:59:59.999999'
        diff = [m for m in minors if excluded(p, m, end) != excluded(p, m)]
        if diff:
            changed.append((p, d, diff))
    if inweek:
        print(f'   {p}: versions at or above R uploaded during the week: {inweek}')
print(f'   projects and days whose excluded set differs from the week-end table: {changed if changed else "none"} (amendment 1.5 says none)\n')

# ------------------------------------------------------------------ C. requirements and B
print('C. Identified bounds B, all 37, with the guard (record: most 4 [botocore fsspec pydantic-core s3transfer], cannot 7, undetermined 26 [70.3, 54.1 to 83.8];')
print('   pydantic-core 95.8 to 100 from pydantic 1.05 guard 97.6 current 53.2; fsspec 58.5 to 93.4 s3fs 0.53 guard 81.9; botocore 100 boto3 2.94 guard 75.8; s3transfer 100 boto3 3.88 guard 89.5)')
REQ, READ = defaultdict(list), set()
for r in rd(DATA, 'requirements.csv'):
    READ.add((r['dependent'], r['dependent_version']))
    if r['parse'] == 'ok' and r['one_of_37'] == 'True':
        REQ[(r['dependent'], r['dependent_version'])].append((norm(r['name']), r['specifier'], r['marker']))
for r in rd(DATA, 'top500_screen.csv'):
    if r['status'] == '200':
        READ.add((r['project'], r['latest_version']))
for r in rd(DATA, 'week_versions.csv'):
    READ.add((r['dependent'], r['version']))
for r in rd(DATA, 'requirements_phase2.csv'):
    if r['parse'] == 'ok' and norm(r['name']) in REF:
        REQ[(r['dependent'], r['dependent_version'])].append((norm(r['name']), r['specifier'], r['marker']))
for r in rd(DATA, 'dependent_reads.csv'):
    if r['status'] == '200':
        READ.add((r['dependent'], r['version']))
for k in REQ:
    REQ[k] = list(dict.fromkeys(REQ[k]))
PAIRS = rd(DATA, 'pairs.csv')
DEPS = defaultdict(set)
for r in PAIRS:
    DEPS[r['project']].add(r['dependent'])
WEEKV = defaultdict(set)
for r in rd(DATA, 'week_versions.csv'):
    WEEKV[r['dependent']].add(r['version'])

_mix, _pym = {}, {}


def mix(x):
    if x not in _mix:
        path = os.path.join(DATA, 'week' if x in REF else 'deps', 'versions', x + '.csv')
        _mix[x] = [(r['date'], r['version'], int(r['n'])) for r in rd(path)] if os.path.exists(path) else None
        path = os.path.join(DATA, 'week' if x in REF else 'deps', 'python', x + '.csv')
        m = defaultdict(lambda: defaultdict(int))
        if os.path.exists(path):
            for r in rd(path):
                m[r['version']][r['python_minor'] if MINOR.fullmatch(r['python_minor'] or '') else ''] += int(r['n'])
        _pym[x] = m
    return _mix[x], _pym[x]


_avail = {}


def avail(D, end):
    if (D, end) not in _avail:
        _avail[(D, end)] = [V(s) for s, v in VERS[D].items() if usable(v) and V(s) is not None and v['first_upload_utc'] <= end]
    return _avail[(D, end)]


_sh, _ss = {}, {}


def SS(spec):
    if spec not in _ss:
        _ss[spec] = SpecifierSet(spec)
    return _ss[spec]


def holds(D, spec, end):
    """The specifier admits no usable version of D at or above R uploaded by `end`."""
    k = (D, spec, end)
    if k not in _sh:
        R = V(REF[D])
        _sh[k] = not any(SS(spec).contains(v) for v in avail(D, end) if v >= R)
    return _sh[k]


_adm = {}


def admitted(Y, spec):
    if (Y, spec) not in _adm:
        _adm[(Y, spec)] = frozenset(s for s, v in VERS[Y].items() if v['parse'] == 'ok' and v['is_prerelease'] == 'False' and V(s) is not None and SS(spec).contains(V(s)))
    return _adm[(Y, spec)]


PLAT = ('sys_platform', 'platform_', 'os_name', 'implementation')
_ge_req = {}


def one_step(D, reqs, end):
    """x holds D through Y, another of the 37, when x's unconditioned bound on Y admits none of the Y versions
    that any available D at or above R requires (each such D having an unconditioned, read requirement on Y)."""
    for name, spec, marker in reqs:
        if name == D or marker or name not in REF:
            continue
        k = (D, name, end)
        if k not in _ge_req:
            specs = []
            for v in avail(D, end):
                if v < V(REF[D]):
                    continue
                key = (D, str(v))
                if key not in READ:
                    specs = None
                    break
                rows = [q for q in REQ[key] if q[0] == name and not q[2]]
                if not rows:
                    specs = None
                    break
                specs.append(rows[0][1])
            _ge_req[k] = specs
        specs = _ge_req[k]
        if not specs:
            continue
        ax = admitted(name, spec)
        if all(not (ax & admitted(name, s)) for s in specs):
            return name
    return None


_hs = {}


def hold(X, xv, D, end):
    """(held, unknown, extra_unknown, via) as fractions of x's fetches."""
    k = (X, xv, D, end)
    if k in _hs:
        return _hs[k]
    if (X, xv) not in READ:
        _hs[k] = (0.0, 1.0, 0.0, 'unread')
        return _hs[k]
    rows = [q for q in REQ[(X, xv)] if q[0] == D]
    held = unk = ext = 0.0
    via = ''
    extra = [q for q in rows if 'extra' in q[2]]
    plat = [q for q in rows if q not in extra and any(t in q[2] for t in PLAT)]
    pyr = [q for q in rows if q not in extra and q not in plat and q[2]]
    plain = [q for q in rows if not q[2]]
    if any(holds(D, q[1], end) for q in plain):
        _hs[k] = (1.0, 0.0, 0.0, 'direct')
        return _hs[k]
    if pyr:
        dist = mix(X)[1].get(xv)
        if not dist:
            unk = 1.0
        else:
            t = sum(dist.values())
            for m, n in dist.items():
                if not m:
                    unk += n / t
                elif any(Marker(q[2]).evaluate({'python_version': m, 'python_full_version': m + '.0', 'extra': ''}) and holds(D, q[1], end) for q in pyr):
                    held += n / t
        via = 'python marker'
    if plat and any(holds(D, q[1], end) for q in plat):
        unk = max(unk, 1.0 - held)
        via = via or 'platform marker'
    if extra and any(holds(D, q[1], end) for q in extra):
        ext = 1.0 - held - unk
        via = via or 'extra'
    if held or unk or ext:
        _hs[k] = (held, unk, ext, via)
        return _hs[k]
    Y = one_step(D, REQ[(X, xv)], end)
    _hs[k] = (1.0, 0.0, 0.0, 'one step via ' + Y) if Y else (0.0, 0.0, 0.0, '')
    return _hs[k]


BCLS, BLO, BHI, GUARD, LOWX = {}, {}, {}, {}, {}
ONESTEP = defaultdict(int)
for D in P37:
    per = {}
    for X in sorted(DEPS[D]):
        mx, _ = mix(X)
        if mx is None:
            per[X] = None
            continue
        tot = hc = ho = un = ex = 0.0
        adm = set()
        vias = set()
        for d, xv, n in mx:
            h, u, e, via = hold(X, xv, D, d + 'T23:59:59.999999')
            tot += n
            if h:
                if xv in WEEKV[X]:
                    hc += h * n
                else:
                    ho += h * n
                vias.add(via)
                if via.startswith('one step'):
                    ONESTEP[(X, D)] += n
                for name, spec, marker in REQ[(X, xv)]:
                    if name == D and 'extra' not in marker:
                        adm |= admitted(D, spec)
            un += u * n
            ex += e * n
        per[X] = dict(tot=tot, held=hc + ho, hc=hc, ho=ho, un=un, ex=ex, adm=adm, vias=vias)
    known = {x: v for x, v in per.items() if v}
    lx = max(known, key=lambda x: known[x]['held'], default=None)
    lo = known[lx]['held'] if lx else 0.0
    hi = sum(v['held'] + v['un'] + v['ex'] for v in known.values())
    BLO[D], BHI[D] = min(1.0, lo / OLDER[D]), min(1.0, hi / OLDER[D])
    g = None
    if lx and lo and not any(v.startswith('one step') for v in known[lx]['vias']):
        g = sum(n for v, n in MIX[D].items() if v in known[lx]['adm']) / OLDER[D]
    GUARD[D], LOWX[D] = g, (lx, known[lx]['tot'] / TOTAL[D], known[lx]['hc'] / OLDER[D]) if lx and lo else ('', None, 0)
    c = classify(BLO[D], BHI[D])
    if c == 'most' and not (g is not None and g > 0.5):
        c = 'undetermined (guard)'
    BCLS[D] = c
groups = defaultdict(list)
for p in P37:
    groups[BCLS[p]].append(p)
cannot_all = sorted(groups['cannot'] + groups['little'])
und = sorted(groups['undetermined'] + groups['undetermined (guard)'])
lo, hi = boot_ci([1 if p in und else 0 for p in P37], mean)
print(f'   most {len(groups["most"])} {groups["most"]}; cannot (incl. little) {len(cannot_all)} {cannot_all}; undetermined {len(und)} = {pct(len(und) / 37)} [{pct(lo)} to {pct(hi)}]; guard failures {groups["undetermined (guard)"]}')
for p in ('pydantic-core', 'fsspec', 'botocore', 's3transfer', 'boto3', 'aiobotocore', 'urllib3', 'cryptography', 'protobuf'):
    lx, ratio, cur = LOWX[p]
    print(f'   {p}: B {pct(BLO[p])} to {pct(BHI[p])} ({BCLS[p]}); lower from {lx or "-"}' + (f' fetched {ratio:.2f} times {p}; held by its current versions {pct(cur)}; guard {pct(GUARD[p]) if GUARD[p] is not None else "n/a"}' if lx else ''))
print(f'   median B lower {pct(statistics.median(BLO.values()))}, upper {pct(statistics.median(BHI.values()))}; one-step holds by (dependent, project) with their fetches: {dict(ONESTEP) if ONESTEP else "none"}\n')

# ------------------------------------------------------------------ D. the frozen-list trace, two readings of E(p)
print('D. Frozen-list trace (record: 18 projects; median off-edge share 78.3; CI flag more often on older in 20 of 37, median +1.6 points; boto3 6.0 v 32.7, certifi 57.1 v 39.3;')
print('   uv median 59.6 older v 43.2 newer, pip 33.5 v 54.7; certifi uv 68.3 v 28.9; Linux 96.3 v 95.0; sdist 0.1; pip Linux glibc 99.1 v 98.5; uv Linux musl 0.6 v 0.9)')
bedges = defaultdict(set)
for D in P37:
    for X in DEPS[D]:
        mx, _ = mix(X)
        if not mx:
            continue
        tot = defaultdict(int)
        for d, xv, n in mx:
            tot[xv] += n
        T = sum(tot.values())
        for xv, n in tot.items():
            if n / T < 0.001:
                continue
            h, u, e, via = hold(X, xv, D, WEND)
            if not h or via.startswith('one step'):
                continue
            for name, spec, marker in REQ[(X, xv)]:
                if name == D and 'extra' not in marker:
                    c = [v for v in avail(D, WEND) if SS(spec).contains(v)]
                    if c:
                        bedges[D].add(str(max(c)))
trace_a, trace_lit, off_a, off_lit, cidiff = [], [], {}, {}, {}
uv_o, uv_n, pip_o, pip_n, lin_o, lin_n, sd_o, sd_n, gl_o, gl_n, mu_o, mu_n = ({} for _ in range(12))
for p in P37:
    agg = defaultdict(int)
    for r in rd(DATA, 'week', 'pass', p + '.csv'):
        agg[(r['cls'], r['installer'], r['ci'], r['system'], r['libc_lib'], r['type'])] += int(r['n'])
    def sh(cond, base, c):
        b = sum(n for k, n in agg.items() if k[0] == c and base(k))
        return sum(n for k, n in agg.items() if k[0] == c and base(k) and cond(k)) / b if b else None
    ci = {c: sh(lambda k: k[2] == 'true', lambda k: k[1] in ('pip', 'uv'), c) for c in ('older', 'at_or_newer')}
    cidiff[p] = (ci['older'] - ci['at_or_newer']) * 100
    uv_o[p], uv_n[p] = sh(lambda k: k[1] == 'uv', lambda k: True, 'older'), sh(lambda k: k[1] == 'uv', lambda k: True, 'at_or_newer')
    pip_o[p], pip_n[p] = sh(lambda k: k[1] == 'pip', lambda k: True, 'older'), sh(lambda k: k[1] == 'pip', lambda k: True, 'at_or_newer')
    lin_o[p], lin_n[p] = sh(lambda k: k[3] == 'Linux', lambda k: True, 'older'), sh(lambda k: k[3] == 'Linux', lambda k: True, 'at_or_newer')
    sd_o[p], sd_n[p] = sh(lambda k: k[5] == 'sdist', lambda k: True, 'older'), sh(lambda k: k[5] == 'sdist', lambda k: True, 'at_or_newer')
    gl_o[p], gl_n[p] = sh(lambda k: k[4] == 'glibc', lambda k: k[1] == 'pip' and k[3] == 'Linux', 'older'), sh(lambda k: k[4] == 'glibc', lambda k: k[1] == 'pip' and k[3] == 'Linux', 'at_or_newer')
    mu_o[p], mu_n[p] = sh(lambda k: k[4] == 'musl', lambda k: k[1] == 'uv' and k[3] == 'Linux', 'older'), sh(lambda k: k[4] == 'musl', lambda k: k[1] == 'uv' and k[3] == 'Linux', 'at_or_newer')
    on_a = off = on_lit = 0
    for r in W2[p]:
        if cls(p, r['version']) != 'older':
            continue
        n, m, v = int(r['n']), r['python_minor'], r['version']
        m = m if MINOR.fullmatch(m or '') else ''
        at_bound = v in bedges[p]
        at_ex = bool(m) and excluded(p, m) and v == edge(p, m)      # amendment 3.1
        at_any = bool(m) and v == edge(p, m)                        # the brief's wording read literally
        on_a += n * (at_ex or at_bound)
        on_lit += n * (at_any or at_bound)
        off += n
    off_a[p], off_lit[p] = 1 - on_a / off, 1 - on_lit / off
    if off_a[p] > 0.5 and cidiff[p] > 0:
        trace_a.append(p)
    if off_lit[p] > 0.5 and cidiff[p] > 0:
        trace_lit.append(p)
med = lambda d: statistics.median(v for v in d.values() if v is not None)
print(f'   trace (amendment 3.1): {len(trace_a)} {trace_a}')
print(f'   trace (E(p) for every Python): {len(trace_lit)} {trace_lit}; projects that differ: {sorted(set(trace_a) ^ set(trace_lit))}')
print(f'   median off-edge share {pct(med(off_a))} (literal {pct(med(off_lit))}); CI flag more often on older: {sum(1 for v in cidiff.values() if v > 0)} of 37, median {statistics.median(cidiff.values()):+.1f} points')
print(f'   uv median older {pct(med(uv_o))} v newer {pct(med(uv_n))}; pip {pct(med(pip_o))} v {pct(med(pip_n))}; certifi uv {pct(uv_o["certifi"])} v {pct(uv_n["certifi"])}; '
      f'Linux {pct(med(lin_o))} v {pct(med(lin_n))}; sdist {pct(med(sd_o), 2)} v {pct(med(sd_n), 2)}; pip Linux glibc {pct(med(gl_o))} v {pct(med(gl_n))}; uv Linux musl {pct(med(mu_o))} v {pct(med(mu_n))}')
print(f'   CI flag, boto3 {cidiff["boto3"]:+.1f} points, certifi {cidiff["certifi"]:+.1f} points (record: 6.0 v 32.7 and 57.1 v 39.3)\n')

# ------------------------------------------------------------------ E. residual, briefly
print('E. Residual, share of older downloads not accounted for (record: botocore and s3transfer 0; pydantic-core 0 to 4.2; boto3 18.7 to 23.7; annotated-types 67.3 to 90.9; platformdirs 55.2 to 79.1; grpcio-status 52.5 to 84.7)')
for p in ('botocore', 's3transfer', 'pydantic-core', 'boto3', 'annotated-types', 'platformdirs', 'grpcio-status'):
    print(f'   {p}: {pct(1 - min(1.0, PHI[p] + BHI[p]))} to {pct(1 - max(PLO[p], BLO[p]))}')
print()

# ------------------------------------------------------------------ F. files, with 'any' wheels set apart
print('F. Wheel exclusion, secondary (record: numpy 72.0, pandas 67.8, litellm 58.1, aiohttp 33.5, rpds-py 32.6, cffi 25.1, cryptography 8.1, pydantic-core 2.9, charset-normalizer and protobuf 0)')
print('   here: the share the record\'s test calls wheel-excluded, and within it the share of older downloads that were wheels tagged "any" (platform not known, so not testable)')
fdir = os.path.join(DATA, 'week', 'files')
for f in sorted(os.listdir(fdir)):
    p = f[:-4]
    rows = rd(fdir, f)
    tot = sum(int(r['n']) for r in rows)
    anyw = sum(int(r['n']) for r in rows if r['plat'] == 'any')
    nw = sum(int(r['n']) for r in rows if r['plat'] in ('(not a wheel)', '(no file name)'))
    npy = sum(int(r['n']) for r in rows if r['plat'] not in ('(not a wheel)', '(no file name)') and not MINOR.fullmatch(r['python_minor'] or ''))
    ge_any = any(r['project'] == p and r['packagetype'] == 'bdist_wheel' and V(r['version']) and V(r['version']) >= V(REF[p]) and r['filename'].endswith('-any.whl')
                 for r in csv.DictReader(gzip.open(os.path.join(DATA, 'files.csv.gz'), 'rt')))
    print(f'   {p}: older downloads {tot:,}; wheels tagged any {pct(anyw / tot)}; not a wheel {pct(nw / tot)}; Python not reported {pct(npy / tot)}; a wheel tagged any exists at or above R: {ge_any}')
print()

# ------------------------------------------------------------------ G. the first day
print('G. The first-day test (record: 355 releases all known, 257 settled [72.4]; 28 of 32 projects [87.5, 75.0 to 96.9]; aiohttp 1 of 3, litellm 8 of 40, pydantic-core 2 of 5 [median 55.4], starlette 3 of 7; median of medians 3.2; LH011 35 of 37, 374 of 418)')
rel = rd(DATA, 'releases_nov_mar.csv')
per_p = defaultdict(list)
unknown = 0
for r in rel:
    p, x = r['project'], V(r['version'])
    cnt = defaultdict(dict)
    if p not in per_p and not per_p[p]:
        pass
    key = ('cnt', p)
    if key not in _mix:
        c = defaultdict(dict)
        for q in rd(DATA, 'firstday', 'counts', p + '.csv'):
            c[q['date']][q['v']] = int(q['n'])
        _mix[key] = c
    c = _mix[key]
    s = {}
    for k in (2, 30):
        d = str(dt.date.fromisoformat(r['day0']) + dt.timedelta(days=k))
        if is_gap(p, d) or d not in c:
            s[k] = None
            continue
        tot = sum(c[d].values())
        s[k] = sum(n for v, n in c[d].items() if v != '~other' and V(v) and V(v) >= x and not V(v).is_prerelease) / tot
    if s[2] is None or s[30] is None:
        unknown += 1
        continue
    per_p[p].append((s[30] - s[2]) * 100)
settled_rel = sum(1 for p in per_p for d in per_p[p] if abs(d) <= 10)
n_rel = sum(len(v) for v in per_p.values())
proj = {p: (sum(1 for d in v if abs(d) <= 10), len(v), statistics.median(v)) for p, v in per_p.items()}
settles = {p: a > b / 2 for p, (a, b, m) in proj.items()}
flags = [1 if settles[p] else 0 for p in sorted(proj)]
lo, hi = boot_ci(flags, mean)
verdict = 'inconclusive' if len(flags) < 20 else ('holds as a rule' if mean(flags) >= 0.75 else ('for some' if mean(flags) >= 0.5 else 'fails'))
print(f'   releases {n_rel} known ({unknown} unknown), {settled_rel} settled ({pct(settled_rel / n_rel)}); projects {sum(flags)} of {len(flags)} ({pct(mean(flags))} [{pct(lo)} to {pct(hi)}]): {verdict}')
print(f'   not settling: {[(p, proj[p][0], proj[p][1], round(proj[p][2], 1)) for p in sorted(proj) if not settles[p]]}; median of project medians {statistics.median(m for _, _, m in proj.values()):.1f} points')
lh = defaultdict(dict)
for r in rd(ROOT, 'LH011', 'data', 'analysis', 'release_days.csv'):
    if r['status'] == 'known' and r['day'] in ('2', '30'):
        lh[(r['project'], r['version'])][int(r['day'])] = float(r['share_at_or_newer'])
lp = defaultdict(list)
for (p, v), s in lh.items():
    if 2 in s and 30 in s:
        lp[p].append((s[30] - s[2]) * 100)
print(f'   LH011 April to August, same measure: {sum(1 for v in lp.values() if sum(abs(d) <= 10 for d in v) > len(v) / 2)} of {len(lp)} projects, '
      f'{sum(abs(d) <= 10 for v in lp.values() for d in v)} of {sum(len(v) for v in lp.values())} releases\n')

# ------------------------------------------------------------------ H. the same releases read two ways
print('H. Two ways (record: urllib3 13 of 32, 60.8 and 66.3; cryptography 18 of 34, 54.7 and 60.1; pyjwt 15 of 29, 57.6 and 72.3; starlette 4 of 7, 53.8 and 57.3; day 7: 6 of 32 and 5 of 34 moved, shares 58.4 and 55.6)')
LH8 = os.path.join(ROOT, 'LH008', 'data')
ev = [r for r in rd(LH8, 'events.csv') if r['chosen'] == 'yes']
lags = [r for r in rd(LH8, 'lags.csv') if r['kind'] == 'fix']
rday = {}
for r in rd(ROOT, 'LH011', 'data', 'analysis', 'release_days.csv'):
    if r['status'] == 'known':
        rday[(r['project'], r['version'], int(r['day']))] = float(r['share_at_or_newer'])
for e in ev:
    lib, v = e['library'], e['fixed_release']
    pairs = [r for r in lags if r['library'] == lib]
    mv = lambda d: sum(1 for r in pairs if r['outcome'] == 'moved' and r['lag_release_days'] and float(r['lag_release_days']) <= d)
    print(f'   {lib} {v}: {mv(30)} of {len(pairs)} by day 30, {mv(7)} by day 7; shares day 1 {pct(rday[(lib, v, 1)])}, day 7 {pct(rday[(lib, v, 7)])}, day 30 {pct(rday[(lib, v, 30)])}')
print()

# ------------------------------------------------------------------ I. the read log against the Method
print('I. Reads (record: 434 ClickPy queries, 10,227,708,600 rows, 8,595,054,592 from pypi.pypi; about 15 bodies with a streamed error; PyPI JSON 4,472)')
rows = [r for f in ('read_log.csv', 'read_log_phase2.csv') for r in rd(DATA, f)]
ck = [r for r in rows if r['source'].startswith('ClickPy')]
raw = [r for r in ck if re.search(r'FROM\s+pypi\.pypi\b(?!_)', r['query'])]
first_count = min(r['read_utc'] for r in ck if r['read_utc'] > '2026-09-29T06:30')
print(f'   ClickPy {len(ck)} queries, {sum(int(r["read_rows"] or 0) for r in ck):,} rows, {sum(int(r["read_rows"] or 0) for r in raw):,} from pypi.pypi ({len(raw)} queries); '
      f'PyPI JSON {sum(r["source"] == "PyPI JSON API" for r in rows)}; first phase 2 ClickPy read {first_count}; last {max(r["read_utc"] for r in ck)}')
odd = [r for r in ck if r['rows_returned'] in ('5', '10005')]
print(f'   queries whose row count is 5 or 10,005 (an error body or a result cut at the row limit): {len(odd)}; every HTTP status 200: {all(r["http_status"] == "200" for r in rows)}')
print('\ndone')
