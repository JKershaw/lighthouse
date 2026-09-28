#!/usr/bin/env python3
"""R-0014: anonymous re-reads of a few of LH011's counts from ClickPy (user demo, POST, as
scripts/common.py does) and of a few upload times from PyPI's JSON API, compared with the retained
files. At most 15 ClickPy queries; every read is printed with its time. No key or credential.
Output: requery.txt beside it. Run: python3 studies/LH011/review/requery.py"""
import csv, os, json, subprocess, datetime, io
from collections import defaultdict
STUDY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(STUDY, 'data')
CH = 'https://sql-clickhouse.clickhouse.com/?user=demo'
n_queries = 0

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def curl(url, data=None):
    cmd = ['curl', '-sS', '-w', '\n%{http_code}', url]
    if data is not None:
        cmd += ['--data-binary', '@-']
    p = subprocess.run(cmd, input=(data or '').encode(), capture_output=True, timeout=120)
    out = p.stdout.decode('utf-8', 'replace')
    body, _, status = out.rpartition('\n')
    return status, body

def ch(label, sql):
    global n_queries
    n_queries += 1
    assert n_queries <= 15
    t = now()
    status, body = curl(CH, sql + ' FORMAT CSVWithNames')
    rows = list(csv.DictReader(io.StringIO(body))) if status == '200' else []
    print(f'[Q{n_queries} {t}] {label}: HTTP {status}, {len(rows)} rows\n    {" ".join(sql.split())}')
    return rows

rel = {(r['project'], r['version']): r for r in csv.DictReader(open(os.path.join(D, 'releases.csv')))}
def retained_counts(p, date):
    out = {}
    for r in csv.DictReader(open(os.path.join(D, 'counts', p + '.csv'))):
        if r['date'] == date:
            out[r['v']] = int(r['downloads'])
    return out

# 1. day-1 counts by version for four releases: two plateau (numpy, boto3), two fast (requests, pandas is the
# piece's slow example; certifi fast). Compare named versions and the '~other' fold and the total.
checks = [('numpy', '2.4.5'), ('boto3', '1.42.81'), ('requests', '2.34.0'), ('pandas', '3.0.3'), ('certifi', None)]
for p, v in checks:
    if v is None:
        v = min((k[1] for k in rel if k[0] == p), key=lambda x: rel[(p, x)]['day0'])
    r = rel[(p, v)]
    day1 = (datetime.date.fromisoformat(r['day0']) + datetime.timedelta(days=1)).isoformat()
    rows = ch(f'{p} {v} day 1 ({day1}) by version',
              f"SELECT version, sum(count) AS downloads FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' AND date = '{day1}' GROUP BY version")
    live = {x['version']: int(x['downloads']) for x in rows}
    kept = retained_counts(p, day1)
    named = {k: c for k, c in kept.items() if k != '~other'}
    live_named_sum = sum(live.get(k, 0) for k in named)
    print(f'    retained: total {sum(kept.values()):,}, named versions {len(named)} summing {sum(named.values()):,}, ~other {kept.get("~other", 0):,}')
    print(f'    live:     total {sum(live.values()):,}, same named versions summing {live_named_sum:,}, rest {sum(live.values()) - live_named_sum:,}')
    mism = [(k, named[k], live.get(k)) for k in named if live.get(k) != named[k]]
    print(f'    named versions differing: {mism if mism else "none"}; own {v}: retained {named.get(v)}, live {live.get(v)}')
    share_live = sum(live.get(k, 0) for k in named) / sum(live.values())
    print(f'    at-or-newer share day 1: retained {sum(named.values())/sum(kept.values()):.4f}, live {share_live:.4f}')

# 2. daily totals from the per-day table for the same project-days
rows = ch('per-day totals for the same project-days',
          "SELECT project, date, sum(count) AS downloads FROM pypi.pypi_downloads_per_day WHERE (project, date) IN (('numpy','2026-05-16'),('boto3','2026-04-02'),('requests','2026-05-12'),('pandas','2026-05-12')) GROUP BY project, date")
tot = {}
for f in ('daily_totals_a.csv', 'daily_totals_b.csv'):
    for r in csv.DictReader(open(os.path.join(D, f))):
        tot[(r['project'], r['date'])] = int(r['downloads'])
for x in rows:
    k = (x['project'], x['date'])
    print(f'    {k}: live {int(x["downloads"]):,}, retained {tot.get(k):,}')

# 3. CI reads for one fast (pathspec) and one plateau (aiobotocore) subsample release, days 0 to 2
for p, v in (('pathspec', None), ('aiobotocore', '3.4.0')):
    if v is None:
        v = next(k[1] for k in rel if k[0] == p and rel[k]['ci_subsample'] == 'True')
    r = rel[(p, v)]; ov = r['replaced_version']
    d0 = datetime.date.fromisoformat(r['day0']); d2 = (d0 + datetime.timedelta(days=2)).isoformat()
    rows = ch(f'CI read {p} {v} against {ov}, days 0 to 2',
              f"SELECT date, version, installer, ci, count() AS downloads FROM pypi.pypi WHERE project = '{p}' AND date BETWEEN '{d0}' AND '{d2}' AND version IN ('{v}', '{ov}') GROUP BY date, version, installer, ci")
    live = defaultdict(int); kept = defaultdict(int)
    for x in rows:
        live[(x['version'], x['installer'], x['ci'])] += int(x['downloads'])
    for x in csv.DictReader(open(os.path.join(D, 'ci', f'{p}_{v}.csv'))):
        kept[(x['version'], x['installer'], x['ci'])] += int(x['downloads'])
    def share(agg, ver):
        t = sum(c for (a, i, f), c in agg.items() if a == ver and i in ('pip', 'uv'))
        y = sum(c for (a, i, f), c in agg.items() if a == ver and i in ('pip', 'uv') and f == 'true')
        return y / t if t else None
    print(f'    rows: retained {len(kept)}, live {len(live)}; cells differing: {sum(1 for k in set(kept) | set(live) if kept.get(k, 0) != live.get(k, 0))}')
    print(f'    pip+uv CI share new: retained {share(kept, v):.4f}, live {share(live, v):.4f}; old: retained {share(kept, ov):.4f}, live {share(live, ov):.4f}')
    print(f'    total downloads: retained {sum(kept.values()):,}, live {sum(live.values()):,}')

# 4. PyPI JSON upload times
print('PyPI JSON API, earliest file upload_time_iso_8601 against data/releases.csv first_upload_utc:')
for p, v in (('requests', '2.34.0'), ('pandas', '3.0.3'), ('numpy', '2.4.5'), ('boto3', '1.42.81')):
    t = now()
    status, body = curl(f'https://pypi.org/pypi/{p}/{v}/json')
    j = json.loads(body)
    earliest = min(f['upload_time_iso_8601'] for f in j['urls'])
    print(f'    [{t}] {p} {v}: HTTP {status}, earliest file {earliest}, retained {rel[(p, v)]["first_upload_utc"]}, match {earliest == rel[(p, v)]["first_upload_utc"]}, yanked {any(f["yanked"] for f in j["urls"])}')
print('ClickPy queries used:', n_queries)
