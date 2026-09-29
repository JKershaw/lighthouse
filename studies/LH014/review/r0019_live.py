#!/usr/bin/env python3
"""Release review R-0019: eight project-days re-read live from ClickPy's public SQL service (user `demo`,
anonymously) and compared with LH014's retained counts. Every query names only days on or before
2026-09-27 and sets read_overflow_mode = 'throw'. Output: studies/LH014/review/r0019_live.txt.
The reads: pillow 12.3.0 on its days 1 and 30 and sentry-sdk 2.64.0 on its days 1 and 30 (the piece's
opening figures), one band B release day each for astropy and djlint, pillow's per-day total on 2 July, and
the mirror classes' downloads of pillow 12.3.0 on its days 0 and 1 (a first run folded 12.2.0 into '~other' where the study kept it, so its cells differed only by that fold; the sums agreed)."""
import csv, datetime, io, os, sys, urllib.parse, urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), 'data')
URL = 'https://sql-clickhouse.clickhouse.com/?user=demo'
CUT = '2026-09-27'
D = datetime.date.fromisoformat
ONE = datetime.timedelta(days=1)


def run(sql):
    assert "read_overflow_mode = 'throw'" in sql
    import re
    assert all(d <= CUT for d in re.findall(r"'(\d{4}-\d{2}-\d{2})'", sql)), 'a query named a day after the cut'
    req = urllib.request.Request(URL, data=sql.encode(), headers={'Content-Type': 'text/plain'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read().decode()
        rows = list(csv.DictReader(io.StringIO(body)))
        return rows, resp.headers.get('X-ClickHouse-Summary', '')


def rd(*p):
    with open(os.path.join(*p), newline='') as f:
        return list(csv.DictReader(f))


counts = defaultdict(lambda: defaultdict(dict))
rels = {(r['project'], r['version']): r for r in rd(DATA, 'releases.csv')}
picks = [('pillow', '12.3.0', 1), ('pillow', '12.3.0', 30), ('sentry-sdk', '2.64.0', 1), ('sentry-sdk', '2.64.0', 30)]
for p in ('astropy', 'djlint'):
    r = next(x for x in rd(DATA, 'releases.csv') if x['project'] == p)
    picks.append((p, r['version'], 1 if p == 'astropy' else 2))
print(f'read at {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} UTC from {URL}')
ok = True
for p, v, k in picks:
    day = str(D(rels[p, v]['day0']) + k * ONE)
    ret = {r['v']: int(r['downloads']) for r in rd(DATA, 'counts', f'{p}.csv') if r['date'] == day}
    kept = [w for w in ret if w != '~other']
    sql = (f"SELECT date, if(version IN ({','.join(repr(w) for w in kept)}), version, '~other') AS v, sum(count) AS downloads "
           f"FROM pypi.pypi_downloads_per_day_by_version WHERE project = '{p}' AND date = '{day}' GROUP BY date, v ORDER BY v "
           f"SETTINGS read_overflow_mode = 'throw' FORMAT CSVWithNames")
    rows, summ = run(sql)
    live = {r['v']: int(r['downloads']) for r in rows}
    same = live == ret
    ok &= same
    tot = sum(live.values())
    own = live.get(v, 0)
    print(f'{"same" if same else "DIFF"}  {p} {v} day {k} ({day}): live total {tot:,}, own {own:,} ({100 * own / tot:.1f} per cent), '
          f'{len(live)} rows; retained total {sum(ret.values()):,}, own {ret.get(v, 0):,}' + ('' if same else f'\n      live {live}\n      retained {ret}'))
# per-day table
rows, _ = run("SELECT sum(count) AS downloads FROM pypi.pypi_downloads_per_day WHERE project = 'pillow' AND date = '2026-07-02' SETTINGS read_overflow_mode = 'throw' FORMAT CSVWithNames")
live = int(rows[0]['downloads'])
ret = next(int(r['downloads']) for r in rd(DATA, 'daily_totals.csv') if r['project'] == 'pillow' and r['date'] == '2026-07-02')
ok &= live == ret
print(f'{"same" if live == ret else "DIFF"}  pillow per-day total 2026-07-02: live {live:,}, retained {ret:,}')
# mirror classes, pillow 12.3.0 days 0 and 1
kept = sorted({r['v'] for r in rd(DATA, 'mirror', 'pillow.csv') if r['date'] in ('2026-07-01', '2026-07-02') and r['v'] != '~other'})
sql = (f"SELECT date, if(version IN ({','.join(repr(w) for w in kept)}), version, '~other') AS v, if(lower(installer) IN ('bandersnatch','z3c.pypimirror','artifactory','devpi'), installer, '~not mirror') AS installer_class, "
       f"sum(count) AS downloads FROM pypi.pypi_downloads_per_day_by_version_by_installer_by_type WHERE project = 'pillow' AND date IN ('2026-07-01','2026-07-02') "
       f"GROUP BY date, v, installer_class ORDER BY date, v, installer_class SETTINGS read_overflow_mode = 'throw' FORMAT CSVWithNames")
rows, _ = run(sql)
live = {(r['date'], r['v'], r['installer_class']): int(r['downloads']) for r in rows}
ret = {(r['date'], r['v'], r['installer_class']): int(r['downloads']) for r in rd(DATA, 'mirror', 'pillow.csv') if r['date'] in ('2026-07-01', '2026-07-02')}
same = live == ret
ok &= same
mir = {d: sum(n for (dd, w, c), n in live.items() if dd == d and w == '12.3.0' and c != '~not mirror') for d in ('2026-07-01', '2026-07-02')}
print(f'{"same" if same else "DIFF"}  pillow 12.3.0 mirror-class downloads: {mir} (live, {len(live)} cells); retained {len(ret)} cells'
      + ('' if same else f'\n      live {live}\n      retained {ret}'))
print('ALL MATCH' if ok else 'SOME DIFFER')
