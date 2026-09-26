#!/usr/bin/env python3
"""LH007 step 7 (optional comparison): the share of each UTC day's mcp downloads that were 1.28.x,
from ClickPy, ClickHouse's public copy of PyPI's download log (user demo, anonymous), as LH005 read it.
Writes data/clickpy_mcp_daily_by_version.csv (raw) and data/clickpy_mcp_daily_share_128.csv."""
import csv, io, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, write_csv

Q = ("SELECT date, version, sum(count) AS downloads FROM pypi.pypi_downloads_per_day_by_version "
     "WHERE project = 'mcp' AND date BETWEEN '2026-05-19' AND '2026-07-28' GROUP BY date, version "
     "ORDER BY date, version FORMAT CSVWithNames")
from common import S, log, now
t = now()
resp = S.post('https://sql-clickhouse.clickhouse.com/?user=demo', data=Q.encode(), timeout=120)
log(read_utc=t, source='ClickPy (ClickHouse public demo)', label='mcp daily by version', method='POST',
    endpoint='https://sql-clickhouse.clickhouse.com/?user=demo', http_status=resp.status_code, bytes=len(resp.content), note=Q)
rows = list(csv.DictReader(io.StringIO(resp.text)))
write_csv('clickpy_mcp_daily_by_version.csv', rows, ['date', 'version', 'downloads'])
tot, new = collections.Counter(), collections.Counter()
for x in rows:
    tot[x['date']] += int(x['downloads'])
    if x['version'].startswith('1.28.'):
        new[x['date']] += int(x['downloads'])
out = [dict(date=d, downloads=tot[d], downloads_128x=new[d], share_128x=round(new[d] / tot[d], 4)) for d in sorted(tot)]
write_csv('clickpy_mcp_daily_share_128.csv', out)
for o in out:
    if o['date'] in ('2026-06-16', '2026-06-17', '2026-06-18', '2026-06-19', '2026-06-23', '2026-06-30', '2026-07-07', '2026-07-14', '2026-07-27'):
        print(o)
