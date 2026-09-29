#!/usr/bin/env python3
"""R-0016: live re-reads for the review of LH012, anonymous, 29 September 2026. ClickPy's public SQL
(user demo) for a sample of the counts the headline rests on, and PyPI's JSON API for a few reference
releases' Requires-Python and pydantic's requirement on pydantic-core. Every ClickPy query is logged with
its time, SQL and the rows ClickHouse reports reading. Compares each figure with the retained files in
data/ and data/analysis/. Usage: python3 requery.py > requery.txt"""
import csv, json, os, subprocess, datetime as dt
from packaging.version import Version, InvalidVersion

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, 'data')
CK = 'https://sql-clickhouse.clickhouse.com/?user=demo'
DAYS = "('2026-09-21','2026-09-22','2026-09-23','2026-09-24','2026-09-25','2026-09-26','2026-09-27')"
LOG = []
TOTAL_ROWS = 0


def ck(label, sql):
    """POST the SQL anonymously; return rows (list of lists) and log time, SQL and read_rows."""
    global TOTAL_ROWS
    t = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    hdr = os.path.join(HERE, '.hdr.tmp')
    out = subprocess.run(['curl', '-sS', '--max-time', '90', '-D', hdr, '-X', 'POST', CK, '--data-binary', sql + ' FORMAT CSV'],
                         capture_output=True, text=True)
    body = out.stdout
    summary = ''
    for line in open(hdr):
        if line.lower().startswith('x-clickhouse-summary:'):
            summary = line.split(':', 1)[1].strip()
    os.remove(hdr)
    read_rows = int(json.loads(summary)['read_rows']) if summary else -1
    TOTAL_ROWS += max(read_rows, 0)
    err = 'Exception' in body or 'Code:' in body[:200]
    LOG.append((t, label, read_rows, err))
    print(f'[{t}] {label}: read_rows {read_rows:,}{"; ERROR IN BODY" if err else ""}\n    {sql}')
    if err:
        print('    body:', body[:300])
        return []
    return list(csv.reader(body.splitlines()))


def pypi(project, version=None):
    url = f'https://pypi.org/pypi/{project}/{version}/json' if version else f'https://pypi.org/pypi/{project}/json'
    t = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    out = subprocess.run(['curl', '-sS', '--max-time', '60', url], capture_output=True, text=True)
    print(f'[{t}] PyPI JSON {url}')
    return json.loads(out.stdout)


def rd(*p):
    return list(csv.DictReader(open(os.path.join(*p))))


def V(s):
    try:
        return Version(s)
    except InvalidVersion:
        return None


def same(a, b):
    return 'agrees' if a == b else f'DIFFERS (retained {b:,})'


print('R-0016 live re-reads, UTC times; retained figures from studies/LH012/data/\n')

# 1. boto3 and botocore over the week by Python minor (the by-Python view, W sums as the record read them)
print('1. boto3 and botocore, 21 to 27 September 2026, by Python minor')
rows = ck('W sums by project and Python minor, boto3 and botocore',
          "SELECT project, python_minor, sum(count) FROM pypi.pypi_downloads_per_day_by_version_by_python "
          f"WHERE project IN ('boto3','botocore') AND date IN {DAYS} GROUP BY project, python_minor")
live = {}
for p, m, n in rows:
    live.setdefault(p, {})[m] = int(n)
for p in ('boto3', 'botocore'):
    ret = {}
    for r in rd(DATA, 'week', 'python', p + '.csv'):
        ret[r['python_minor']] = ret.get(r['python_minor'], 0) + int(r['n'])
    tot_l, tot_r = sum(live[p].values()), sum(ret.values())
    print(f'   {p}: total live {tot_l:,} {same(tot_l, tot_r)}; Python 3.9 live {live[p].get("3.9", 0):,} {same(live[p].get("3.9", 0), ret.get("3.9", 0))}; '
          f'minors differing: {[m for m in set(live[p]) | set(ret) if live[p].get(m, 0) != ret.get(m, 0)]}')
print(f'   boto3 over botocore on Python 3.9: {live["boto3"]["3.9"] / live["botocore"]["3.9"]:.2f}; all Pythons: '
      f'{sum(live["boto3"].values()) / sum(live["botocore"].values()):.2f} (record: 7.51 and 2.94)\n')

# 2. boto3 on 23 September 2026 from pypi.pypi itself, by Python minor, and the Python 3.9 downloads by installer, ci, system, libc
print('2. boto3 on 23 September 2026, from pypi.pypi')
rows = ck('boto3 2026-09-23 by python_minor from pypi.pypi',
          "SELECT python_minor, count() FROM pypi.pypi WHERE project = 'boto3' AND date = '2026-09-23' GROUP BY python_minor")
live = {m: int(n) for m, n in rows}
ret = {r['python_minor']: int(r['n']) for r in rd(DATA, 'checks', 'boto3_python_pypi.csv')}
t = sum(live.values())
print(f'   total {t:,} {same(t, sum(ret.values()))}; Python 3.9 {live.get("3.9", 0):,} {same(live.get("3.9", 0), ret["3.9"])} '
      f'({live.get("3.9", 0) / t * 100:.1f} per cent; record 62.2); every minor equal: {live == ret}')
rows = ck('boto3 2026-09-23 Python 3.9 by installer, ci, system, libc from pypi.pypi',
          "SELECT installer, ci, system, tupleElement(libc, 'lib') AS libc_lib, count() AS n FROM pypi.pypi WHERE project = 'boto3' "
          "AND date = '2026-09-23' AND python_minor = '3.9' GROUP BY installer, ci, system, libc_lib ORDER BY n DESC LIMIT 5")
top = rows[0] if rows else None
ret = rd(DATA, 'checks', 'boto3_py39_installers.csv')[0]
print(f'   largest group live: {top[:4]} {int(top[4]):,} {same(int(top[4]), int(ret["n"]))} '
      f'({int(top[4]) / live["3.9"] * 100:.1f} per cent of the 3.9 downloads; record 99.4)\n')

# 3. boto3's Python 3.9 downloads over the week by version, against 1.42.97 (the driver's second check)
print('3. boto3, Python 3.9, 21 to 27 September 2026, by version, against 1.42.97')
rows = ck('boto3 Python 3.9 W sums by version',
          "SELECT version, sum(count) FROM pypi.pypi_downloads_per_day_by_version_by_python WHERE project = 'boto3' "
          f"AND python_minor = '3.9' AND date IN {DAYS} GROUP BY version")
edge = Version('1.42.97')
below = at = above = 0
for v, n in rows:
    x = V(v)
    if x is None:
        continue
    n = int(n)
    below, at, above = below + n * (x < edge), at + n * (x == edge), above + n * (x > edge)
tt = below + at + above
print(f'   {tt:,} downloads {same(tt, 372822043)}; below 1.42.97 {below / tt * 100:.1f} per cent (record 95.4), at it {at / tt * 100:.1f} (4.6), '
      f'above {above / tt * 100:.2f} (0.01)\n')

# 4. numpy's older downloads by Python minor, classed as excluded, not reported, admitted (P)
print('4. numpy, older downloads over the week by Python minor')
rows = ck('numpy W sums by version and Python minor',
          "SELECT version, python_minor, sum(count) FROM pypi.pypi_downloads_per_day_by_version_by_python WHERE project = 'numpy' "
          f"AND date IN {DAYS} GROUP BY version, python_minor")
R = Version('2.5.2')
adm = {r['python_minor']: r['any_ge_R_admits'] == 'True' for r in rd(DATA, 'python_admission.csv') if r['project'] == 'numpy'}
listed = {r['version'] for r in rd(DATA, 'versions.csv') if r['project'] == 'numpy'}
ex = nr = ad = tot = 0
for v, m, n in rows:
    n = int(n)
    tot += n
    x = V(v)
    if x is None or v not in listed or x >= R:
        continue
    if not m:
        nr += n
    elif not adm.get(m, True):
        ex += n
    else:
        ad += n
older = ex + nr + ad
print(f'   total {tot:,} {same(tot, 190507726)}; older {older:,} {same(older, 139636806)}; excluded {ex:,} {same(ex, 87330440)}; '
      f'not reported {nr:,} {same(nr, 5843987)}; admitted {ad:,} {same(ad, 46462379)}; P {ex / older * 100:.1f} to {(ex + nr) / older * 100:.1f} (record 62.5 to 66.7)\n')

# 5. pydantic-core over the week by version: total, older, 2.46.5
print('5. pydantic-core, 21 to 27 September 2026, by version')
rows = ck('pydantic-core W sums by version',
          f"SELECT version, sum(count) FROM pypi.pypi_downloads_per_day_by_version WHERE project = 'pydantic-core' AND date IN {DAYS} GROUP BY version")
R = Version('2.48.0')
listed = {r['version'] for r in rd(DATA, 'versions.csv') if r['project'] == 'pydantic-core'}
tot = older = v2465 = 0
for v, n in rows:
    n = int(n)
    tot += n
    x = V(v)
    if x is not None and v in listed and x < R:
        older += n
    if v == '2.46.5':
        v2465 = n
print(f'   total {tot:,} {same(tot, 191659060)}; older {older:,} {same(older, 190379025)} ({older / tot * 100:.1f} per cent; record 99.3); '
      f'2.46.5 {v2465:,} {same(v2465, 103371997)} ({v2465 / older * 100:.1f} per cent of older; record 54.3)\n')

# 6. three first-day releases: day 2 and day 30 at-or-newer shares
print('6. three November to March releases, day 2 and day 30 at-or-newer shares')
fd = {(r['project'], r['version']): r for r in rd(DATA, 'analysis', 'firstday_releases.csv')}
picks = [('requests', None), ('numpy', None), ('pydantic-core', None)]
rel = rd(DATA, 'releases_nov_mar.csv')
chosen = []
for p, _ in picks:
    rs = [r for r in rel if r['project'] == p]
    chosen.append(rs[len(rs) // 2])  # the middle release by file order
for r in chosen:
    p, v, d0 = r['project'], r['version'], dt.date.fromisoformat(r['day0'])
    x = Version(v)
    s = {}
    for k in (2, 30):
        d = str(d0 + dt.timedelta(days=k))
        rows = ck(f'{p} {v} day {k} ({d}) by version',
                  f"SELECT version, sum(count) FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' AND date = '{d}' GROUP BY version")
        tot = sum(int(n) for _, n in rows)
        num = sum(int(n) for w, n in rows if V(w) is not None and V(w) >= x and not V(w).is_prerelease)
        s[k] = num / tot
    ret = fd[(p, v)]
    print(f'   {p} {v} (day 0 {d0}): day 2 {s[2] * 100:.2f} (retained {float(ret["s2"]) * 100:.2f}), day 30 {s[30] * 100:.2f} '
          f'(retained {float(ret["s30"]) * 100:.2f}), delta {(s[30] - s[2]) * 100:.2f} points (retained {float(ret["delta_points"]):.2f}), settled {abs(s[30] - s[2]) <= 0.1}')
print()

# 7. PyPI JSON: Requires-Python of reference releases and the Python 3.9 edge; pydantic's requirement on pydantic-core
print('7. PyPI JSON re-reads')
bv = [V(r['version']) for r in rd(DATA, 'versions.csv') if r['project'] == 'boto3' and r['parse'] == 'ok' and r['is_prerelease'] == 'False']
nxt = str(min(x for x in bv if x > Version('1.42.97')))  # the first boto3 above the Python 3.9 edge, as versions.csv lists it
for p, v, want in (('boto3', '1.43.78', '>=3.10'), ('boto3', '1.42.97', '>=3.9'), ('boto3', nxt, '>=3.10'), ('numpy', '2.5.2', '>=3.12'),
                   ('aiobotocore', '3.9.0', '>=3.10'), ('pydantic-core', '2.46.5', None), ('pydantic', '2.13.5', None)):
    j = pypi(p, v)
    rp = sorted({(u.get('requires_python') or '') for u in j['urls']})
    up = min(u['upload_time_iso_8601'] for u in j['urls'])
    line = f'   {p} {v}: Requires-Python {rp}, first upload {up}, yanked {all(u.get("yanked") for u in j["urls"])}'
    if want:
        line += f' ({"agrees" if rp == [want] else "DIFFERS from retained " + want})'
    if p == 'pydantic':
        line += f'; requires_dist on pydantic-core: {[d for d in j["info"]["requires_dist"] if d.startswith("pydantic-core")]}'
    print(line)
j = pypi('boto3')
desc = j['info']['description']
i = desc.find('support for Python 3.9')
print(f'   boto3 project JSON (version {j["info"]["version"]}): ...{desc[max(0, i - 40):i + 60]!r}...')
print(f'\nClickPy queries {len(LOG)}, rows read {TOTAL_ROWS:,}, bodies with an error: {sum(1 for x in LOG if x[3])}')
