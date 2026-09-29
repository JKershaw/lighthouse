#!/usr/bin/env python3
"""Replay X2 (notes/replay-X2.md), stage 2: four small anonymous reads of ClickPy's aggregated
by-version table (pypi.pypi_downloads_per_day_by_version), as the release review's requery.py did,
to answer two questions the retained counts cannot, because every version outside the numerator
sets was folded into one '~other' row a day:
  Q1, Q2  litellm on 2026-06-04 and 2026-09-15: how much of '~other' is pre-releases (52 were
          uploaded in the window) rather than versions older than 1.83.1.
  Q3, Q4  boto3 and botocore on 2026-08-12: how the downloads of versions more than 30 days old
          spread across versions (a few, as a dependent's bound would make them, or a long tail),
          and by year of upload.
Each query's UTC time, text, HTTP status and rows are logged below; the rows are kept in
x2_requery_data/. No key or credential; the public `demo` user, through the session's proxy, via curl.
Output: x2_requery.txt.  Run: python3 studies/LH011/review/x2_requery.py"""
import csv, datetime, io, os, subprocess
from collections import defaultdict
from packaging.version import Version

HERE = os.path.dirname(os.path.abspath(__file__))
STUDY = os.path.dirname(HERE)
DATA = os.path.join(STUDY, 'data')
RAW = os.path.join(HERE, 'x2_requery_data')
os.makedirs(RAW, exist_ok=True)
URL = 'https://sql-clickhouse.clickhouse.com/?user=demo'
D = datetime.date.fromisoformat
lines = []
say = lines.append

versions = {}
with open(os.path.join(DATA, 'pypi_versions.csv')) as f:
    for v in csv.DictReader(f):
        versions[(v['project'], v['version'])] = v


def query(label, sql, out):
    t = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    sql = ' '.join(sql.split()) + ' FORMAT CSVWithNames'
    p = subprocess.run(['curl', '-sS', '-w', '\n%{http_code}', URL, '--data-binary', '@-'],
                       input=sql.encode(), capture_output=True, timeout=120)
    body, _, status = p.stdout.decode('utf-8', 'replace').rpartition('\n')
    rows = list(csv.DictReader(io.StringIO(body))) if status.strip() == '200' else []
    say(f'[{label} {t}] HTTP {status.strip()}, {len(rows)} rows: {sql}')
    if rows:
        with open(os.path.join(RAW, out), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
            w.writeheader()
            w.writerows(rows)
    else:
        say(f'    body: {body[:300]}')
    return rows


def by_version(project, day):
    return query(f'{project} {day}', f"""SELECT version, sum(count) AS downloads FROM pypi.pypi_downloads_per_day_by_version
        WHERE project = '{project}' AND date = '{day}' GROUP BY version ORDER BY downloads DESC""", f'{project}_{day}.csv')


# ---- litellm: pre-releases against older versions --------------------------------------------------
FIRST = {'litellm': Version('1.83.1')}
for day in ('2026-06-04', '2026-09-15'):
    rows = by_version('litellm', day)
    if not rows:
        continue
    tot = sum(int(r['downloads']) for r in rows)
    cls = defaultdict(int)
    top_pre = []
    for r in rows:
        n = int(r['downloads'])
        try:
            v = Version(r['version'])
        except Exception:
            cls['unparseable'] += n
            continue
        listed = ('litellm', r['version']) in versions
        if v.is_prerelease or v.is_devrelease:
            cls['pre-release'] += n
            top_pre.append((n, r['version']))
        elif not listed:
            cls['not listed by PyPI'] += n
        elif v >= FIRST['litellm']:
            cls['at or above 1.83.1 (numerator versions)'] += n
        else:
            cls['older stable versions'] += n
    say(f'    litellm {day}: total {tot:,}; ' + '; '.join(f'{k} {n / tot * 100:.1f}%' for k, n in sorted(cls.items(), key=lambda kv: -kv[1])))
    top_pre.sort(reverse=True)
    say('    largest pre-releases: ' + ', '.join(f'{v} {n:,}' for n, v in top_pre[:5]))

# ---- boto3 and botocore: spread of the old-version downloads ---------------------------------------
day = '2026-08-12'
for project in ('boto3', 'botocore'):
    rows = by_version(project, day)
    if not rows:
        continue
    d = D(day)
    tot = sum(int(r['downloads']) for r in rows)
    old, unknown_age, fresh = [], 0, 0
    by_year = defaultdict(int)
    for r in rows:
        n = int(r['downloads'])
        v = versions.get((project, r['version']))
        if v is None:
            unknown_age += n
            continue
        up = D(v['first_upload_utc'][:10])
        if (d - up).days <= 30:
            fresh += n
        else:
            old.append((n, r['version'], up))
            by_year[up.year] += n
    old.sort(reverse=True)
    old_tot = sum(n for n, _, _ in old)
    say(f'    {project} {day}: total {tot:,} over {len(rows)} versions; at most 30 days old {fresh / tot * 100:.1f}%; '
        f'older {old_tot / tot * 100:.1f}% over {len(old)} versions; not listed by PyPI {unknown_age / tot * 100:.1f}%')
    cum = 0
    marks = {}
    for i, (n, _, _) in enumerate(old, 1):
        cum += n
        for k in (1, 5, 20, 100):
            if i == k:
                marks[k] = cum / old_tot
        if 'half' not in marks and cum >= old_tot / 2:
            marks['half'] = i
    say('    share of the older downloads held by the top ' + ', '.join(f'{k}: {marks[k] * 100:.1f}%' for k in (1, 5, 20, 100) if k in marks)
        + f'; versions needed for half of them: {marks.get("half")}')
    say('    the ten largest older versions: ' + ', '.join(f'{v} ({up}) {n / old_tot * 100:.1f}%' for n, v, up in old[:10]))
    say('    older downloads by year of upload: ' + ', '.join(f'{y} {n / old_tot * 100:.1f}%' for y, n in sorted(by_year.items())))

with open(os.path.join(HERE, 'x2_requery.txt'), 'w') as f:
    f.write('\n'.join(lines) + '\n')
print('\n'.join(lines))
