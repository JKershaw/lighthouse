"""Independent reproduction of LH040 record 1.0's figures (R-0134). Written from the brief and the raw
files, without tabulate.py. Reads only retained files; no network. Run:
python3 -I notes/R-0134-lh040-v1-evidence/reproduce.py > notes/R-0134-lh040-v1-evidence/output.txt
"""
import csv, hashlib, json, os, statistics, sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from packaging.version import Version

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'studies', 'LH040', 'data')
R1, R2 = os.path.join(ROOT, 'read-2026-11-09T1432Z'), os.path.join(ROOT, 'read-2026-11-23T1433Z')
CASE, D0 = '1.107.0', '2026-10-21'
COMP = {'1.103.2': '2026-10-01', '1.104.0': '2026-10-03', '1.104.1': '2026-10-07', '1.104.2': '2026-10-08',
        '1.105.0': '2026-10-11', '1.105.1': '2026-10-14', '1.106.0': '2026-10-18', '1.106.1': '2026-10-20',
        '1.106.2': '2026-10-21', '1.106.3': '2026-10-24', '1.106.4': '2026-10-25', '1.106.5': '2026-10-27',
        '1.106.6': '2026-10-28', '1.108.0': '2026-11-04', '1.108.1': '2026-11-05', '1.108.2': '2026-11-06',
        '1.108.3': '2026-11-07'}
ALL = dict(COMP, **{CASE: D0})
MIRRORS = {'bandersnatch', 'devpi', 'Nexus', 'Artifactory', 'z3c.pypimirror', 'pep381client'}

def p(*a): print(*a)

def rows(d, name):
    with open(os.path.join(d, name), newline='') as f:
        return list(csv.DictReader(f))

def hashcheck(d):
    log = rows(d, 'readlog.csv'); ok = 0
    for r in log:
        fn = os.path.join(d, r['name'] + '.raw')
        if os.path.exists(fn):
            h = hashlib.sha256(open(fn, 'rb').read()).hexdigest()
            assert h == r['sha256'], fn
            ok += 1
    return ok, [(r['name'], r['status'][:60]) for r in log if not r['status'].startswith('200')]

def load(d):
    tot = defaultdict(int); nrows = defaultdict(int)
    for r in rows(d, 'Q1_daily_totals.raw'):
        tot[r['date']] += int(r['count']); nrows[r['date']] += 1
    ver = {}
    for r in rows(d, 'Q2_daily_by_version_oct_nov.raw'):
        ver[(r['date'], r['version'])] = ver.get((r['date'], r['version']), 0) + int(r['count'])
    mar = {(r['date'], r['version']): int(r['count']) for r in rows(d, 'Q3_daily_by_version_march.raw')}
    ins = {(r['date'], r['version'], r['installer']): int(r['count']) for r in rows(d, 'Q4_installer.raw')}
    sysm = {(r['date'], r['version'], r['system']): int(r['count']) for r in rows(d, 'Q5_system.raw')}
    ci = {(r['date'], r['version'], r['installer'], r['ci']): int(r['count']) for r in rows(d, 'Q6_ci.raw')}
    ft = {(r['date'], r['version'], r['type']): int(r['count']) for r in rows(d, 'Q7_file_type.raw')}
    ps = {(x['category'], x['date']): x['downloads'] for x in json.load(open(os.path.join(d, 'pypistats_overall.raw')))['data']}
    return dict(tot=tot, nrows=nrows, ver=ver, mar=mar, ins=ins, sys=sysm, ci=ci, ft=ft, ps=ps)

def gaps(tot):
    ds = sorted(tot); g = {}
    for i, d in enumerate(ds):
        dd = date.fromisoformat(d)
        win = [tot[x.isoformat()] for x in (dd + timedelta(k) for k in range(-3, 4)) if x.isoformat() in tot]
        g[d] = tot[d] < 0.5 * statistics.median(win)
    # also days missing entirely between first and last
    first, last = date.fromisoformat(ds[0]), date.fromisoformat(ds[-1])
    missing = [(first + timedelta(k)).isoformat() for k in range((last - first).days + 1)
               if (first + timedelta(k)).isoformat() not in tot]
    return g, missing

p('== Hash checks')
for d in (R1, R2):
    ok, bad = hashcheck(d); p(os.path.basename(d), 'bodies matching logged SHA-256:', ok, '; non-200:', bad)

A, B = load(R1), load(R2)
p('\n== Daily totals and gaps (read 2)')
g, missing = gaps(B['tot'])
p('days', min(B['tot']), 'to', max(B['tot']), 'n =', len(B['tot']), '; missing dates:', missing, '; gap days:', [d for d, v in g.items() if v])
p('dates with >1 row:', {d: n for d, n in B['nrows'].items() if n > 1})
p('read 1 dates with >1 row:', {d: n for d, n in A['nrows'].items() if n > 1})
for d in sorted(B['nrows']):
    if B['nrows'][d] > 1:
        p('  ', d, 'sum', B['tot'][d], 'pypistats with', B['ps'].get(('with_mirrors', d)))
for d in ('2026-11-05', '2026-11-08'):
    p('  ', d, 'read1', A['tot'][d], A['nrows'][d], 'rows; read2', B['tot'][d], B['nrows'][d], 'rows')

p('\n== Measure 1')
C0 = B['ver'][(D0, CASE)]; T0 = B['tot'][D0]
p('C0', C0, 'read1', A['ver'][(D0, CASE)], '; litellm total', T0, 'read1', A['tot'][D0], '; S0 = %.4f%%' % (100 * C0 / T0))
p('file types day 0:', {k[2]: v for k, v in B['ft'].items() if k[0] == D0 and k[1] == CASE})
p('C0 - 49000 =', C0 - 49000)
p('pypistats 21 Oct with/without:', B['ps'].get(('with_mirrors', D0)), B['ps'].get(('without_mirrors', D0)))

p('\n== pypistats agreement')
def agree(lo, hi):
    out = []; d = date.fromisoformat(lo)
    while d <= date.fromisoformat(hi):
        k = d.isoformat(); w = B['ps'].get(('with_mirrors', k))
        if w is not None and k in B['tot']:
            out.append((k, B['tot'][k] / w - 1))
        d += timedelta(1)
    big = [x for x in out if abs(x[1]) > 0.05]
    mx = max(out, key=lambda x: abs(x[1]))
    p(lo, 'to', hi, ': days compared', len(out), '; >5%:', len(big), '; largest', mx[0], '%+.2f%%' % (100 * mx[1]))
agree('2026-10-14', '2026-11-04'); agree('2026-11-05', '2026-11-22')
p('pypistats dates', min(k[1] for k in B['ps']), max(k[1] for k in B['ps']))

p('\n== Timeline and measure 3')
L1 = json.load(open(os.path.join(ROOT, 'pre-brief-2026-11-08T1414Z', 'pypi_project_json.derived.json')))['extracted']
up = {}
for v, t in L1['first_upload_time_iso_8601'].items():
    if t is None: continue
    V = Version(v)
    if V.is_prerelease or V.is_postrelease or V.is_devrelease: continue
    up[v] = datetime.fromisoformat(t.replace('Z', '+00:00'))
def dt(s): return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
CASE_UP = dt('2026-10-21T11:39:51')
# check comparison set from L1
lo, hi = dt('2026-10-01T00:00:00'), dt('2026-11-08T00:00:00')
order = sorted(up, key=lambda v: up[v]); best = None; qual = []
for v in order:
    if best is None or Version(v) > Version(best):
        if lo <= up[v] < hi: qual.append(v)
        best = v
p('qualifying releases from L1:', qual, 'n =', len(qual), '; equals brief set:', sorted(qual, key=Version) == sorted(COMP, key=Version))
p('day 0 agrees with collector:', all(up[v].date().isoformat() == COMP[v] for v in COMP))
for v in ('1.106.2', '1.106.3', '1.108.1'): p('  upload', v, up[v].isoformat())

def hours(end):
    events = [(up[v], 'add', v) for v in up] + [(CASE_UP, 'add', CASE), (dt('2026-10-21T' + end + ':00'), 'del', CASE)]
    events.sort(key=lambda e: e[0])
    h = {}
    for R, d0 in ALL.items():
        s, e = dt(d0 + 'T00:00:00'), dt(d0 + 'T00:00:00') + timedelta(1)
        present = set(); total = 0.0; cur = s
        def top(): return max(present, key=Version) if present else None
        for t, kind, v in events:
            if t >= e: break
            if t > s:
                a = max(cur, s)
                if t > a and top() == R: total += (t - a).total_seconds()
                cur = t
            if kind == 'add': present.add(v)
            else: present.discard(v)
        a = max(cur, s)
        if top() == R: total += (e - a).total_seconds()
        h[R] = total / 3600
    return h

for end, who in (('13:23', 'maintainers'), ('13:20', 'Datadog'), ('12:47', 'Aikido')):
    h = hours(end)
    I = {R: (B['ver'][(ALL[R], R)] / B['tot'][ALL[R]]) / (h[R] / 24) for R in ALL}
    comp = [I[R] for R in COMP]; med = statistics.median(comp)
    rank = 1 + sum(1 for R in ALL if I[R] > I[CASE])
    inside = min(comp) <= I[CASE] <= max(comp)
    p('end %s (%s): h(1.107.0)=%.4f I=%.4f; comp min %.4f median %.4f max %.4f; ratio %.3f; rank %d of 18; inside=%s'
      % (end, who, h[CASE], I[CASE], min(comp), med, max(comp), I[CASE] / med, rank, inside))
    p('   ', ', '.join('%s %.3f (h %.2f)' % (R, I[R], h[R]) for R in sorted(COMP, key=Version)))
    p('   below 1.107.0:', [R for R in COMP if I[R] < I[CASE]], '; 1.106.2 h %.2f' % h['1.106.2'])
    if end == '13:23':
        short = sorted([R for R in COMP if h[R] < 2], key=Version)
        p('   h<2:', short, 'uploads', [up[R].strftime('%H:%M') for R in short], 'I range %.3f-%.3f' % (min(I[R] for R in short), max(I[R] for R in short)))

p('\n== Measure 2 (read 2)')
days = [(date(2026, 10, 22) + timedelta(k)).isoformat() for k in range(32)]
seq = []
for d in days:
    v = B['ver'].get((d, CASE)); seq.append(v)
    if v is None: p('  no row', d, 'day', (date.fromisoformat(d) - date(2026, 10, 21)).days, 'total held', d in B['tot'], 'gap', g.get(d))
p('by day:', seq)
d30 = [x for x in seq[:30] if x is not None]
p('days 1-30 with record', len(d30), 'sum', sum(d30), '; to 22 Nov sum', sum(x for x in seq if x is not None), '; first 18 days', sum(x for x in seq[:18] if x is not None))
p('read 1 tail to 8 Nov:', sum(A['ver'].get((d, CASE), 0) for d in days[:18]))
insum = defaultdict(int); ftsum = defaultdict(int)
for (d, v, i), c in B['ins'].items():
    if v == CASE and '2026-10-22' <= d <= '2026-11-20': insum[i] += c
for (d, v, t), c in B['ft'].items():
    if v == CASE and '2026-10-22' <= d <= '2026-11-20': ftsum[t] += c
tot_i = sum(insum.values())
p('installers days 1-30:', {k or '(none)': (c, round(100 * c / tot_i, 1)) for k, c in sorted(insum.items(), key=lambda x: -x[1])}, 'sum', tot_i)
p('file types days 1-30:', dict(ftsum))
p('pip after day 0 any day:', sum(c for (d, v, i), c in B['ins'].items() if v == CASE and d > D0 and i == 'pip'))

p('\n== Measure 4')
for d in ('2026-10-20', '2026-10-21', '2026-10-22', '2026-10-23'):
    p(d, [B['ver'].get((d, v)) for v in ('1.106.1', '1.106.2', '1.107.0')])

p('\n== Measure 5')
def cat(i):
    if i in ('pip', 'uv', 'poetry', 'pdm'): return i
    if i == '': return 'none'
    if i in MIRRORS: return 'mirror'
    return 'other'
shares = defaultdict(dict); counts = defaultdict(dict)
for R, d0 in ALL.items():
    n = B['ver'][(d0, R)]
    c = defaultdict(int)
    for (d, v, i), x in B['ins'].items():
        if d == d0 and v == R: c[cat(i)] += x
    s = defaultdict(int)
    for (d, v, sy), x in B['sys'].items():
        if d == d0 and v == R: s['sys:' + (sy or 'none')] += x
    allc = dict(c); allc.update(s)
    for k, x in allc.items(): shares[k][R] = x / n; counts[k][R] = x
    p('  %s installer sum %d system sum %d day0 %d' % (R, sum(c.values()), sum(s.values()), n)) if R == CASE else None
p('1.107.0 named installers day 0:', {i: x for (d, v, i), x in B['ins'].items() if d == D0 and v == CASE})
for k in sorted(shares):
    comp = [shares[k].get(R, 0.0) for R in COMP]
    cs = shares[k].get(CASE, 0.0)
    out = 'ABOVE' if cs > max(comp) else ('BELOW' if cs < min(comp) else '')
    p('%-14s case %6d %.3f%% | median %.3f%% range %.3f%%-%.3f%% %s' % (k, counts[k].get(CASE, 0), 100 * cs,
      100 * statistics.median(comp), 100 * min(comp), 100 * max(comp), out))
def cishare(R):
    d0 = ALL[R]; t = f = 0
    for (d, v, i, c), x in B['ci'].items():
        if d == d0 and v == R and i in ('pip', 'uv'):
            t += x; f += x if c == 'true' else 0
    allx = sum(x for (d, v, i, c), x in B['ci'].items() if d == d0 and v == R)
    return f, t, allx
f, t, allx = cishare(CASE)
cc = [cishare(R) for R in COMP]; cs = [a / b for a, b, _ in cc]
p('CI: 1.107.0 %d of %d = %.2f%%; not known %d of %d (%.2f%%); comp median %.2f%% range %.2f%%-%.2f%%'
  % (f, t, 100 * f / t, allx - t, allx, 100 * (allx - t) / allx, 100 * statistics.median(cs), 100 * min(cs), 100 * max(cs)))

p('\n== Measure 6')
m = {d: v for d, v in B['mar'].items()}
d24 = {v: m.get(('2026-03-24', v)) for v in ('1.82.7', '1.82.8')}
s = sum(c for (d, v), c in m.items() if v in ('1.82.7', '1.82.8') and '2026-03-24' <= d <= '2026-04-30')
p('24 March', d24, 'together', sum(d24.values()), '; 24 Mar-30 Apr', s, '; ratio to 119000 %.3f' % (s / 119000),
  '; dates with rows', sorted({d for (d, v) in m if v in ('1.82.7', '1.82.8')}))
p('gap days in 24 Mar-30 Apr:', [d for d, v in g.items() if v and '2026-03-24' <= d <= '2026-04-30'])

p('\n== Re-read comparison (cells both reads hold, dates to 2026-11-08)')
for key in ('tot', 'ver', 'ins', 'sys', 'ci', 'ft', 'mar'):
    a, b = A[key], B[key]
    def dd(k): return k if isinstance(k, str) else k[0]
    common = [k for k in a if k in b and dd(k) <= '2026-11-08']
    diff = [k for k in common if a[k] != b[k]]
    only_a = [k for k in a if k not in b and dd(k) <= '2026-11-08']
    d21 = [k for k in common if dd(k) == D0]
    p('%-4s common %d, differ %d, only in read 1 %d, on 21 Oct %d' % (key, len(common), len(diff), len(only_a), len(d21)))
