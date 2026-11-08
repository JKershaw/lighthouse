#!/usr/bin/env python3
"""LH040 outcome read, as fixed in studies/LH040/brief.md (protocol 0.1). Run only under a
schedule row, after the brief is committed. One read per UTC label; a label already held is
skipped, never overwritten.

Reads, each once: ClickPy's public SQL as user demo (queries Q1 to Q7 below), pypistats.org's
daily totals for litellm, and deps.dev's version and dependents endpoints. Bodies are kept raw
under data/read-<label>/ with readlog.csv (name, url, utc_start, status, content_type, size,
sha256, method, request_body, read_rows, read_bytes). ClickHouse's own X-ClickHouse-Summary header
gives rows and bytes read. User-Agent "Lighthouse-research/1.0". No key, token or credential.

Usage: python3 -I studies/LH040/scripts/collect.py --read 2026-11-10T0900Z
"""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import argparse
import csv
import json
import os
import ssl

ROOT = Path(__file__).resolve().parents[1]
UA = 'Lighthouse-research/1.0'
CA = '/root/.ccr/ca-bundle.crt'
CTX = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
CH = 'https://sql-clickhouse.clickhouse.com/?user=demo&default_format=CSVWithNames'
CEILING_BYTES = 16 * 1024 * 1024
MAX_GETS = 20

# Comparison releases (brief, "Population and unit"): each final litellm release first uploaded
# 2026-10-01 to 2026-11-07 that was higher than every earlier-uploaded final release, with the
# UTC day of its first file (day 0). From PyPI's JSON read at 2026-11-08T1414Z.
COMPARISON = {
    '1.103.2': '2026-10-01', '1.104.0': '2026-10-03', '1.104.1': '2026-10-07', '1.104.2': '2026-10-08',
    '1.105.0': '2026-10-11', '1.105.1': '2026-10-14', '1.106.0': '2026-10-18', '1.106.1': '2026-10-20',
    '1.106.2': '2026-10-21', '1.106.3': '2026-10-24', '1.106.4': '2026-10-25', '1.106.5': '2026-10-27',
    '1.106.6': '2026-10-28', '1.108.0': '2026-11-04', '1.108.1': '2026-11-05', '1.108.2': '2026-11-06',
    '1.108.3': '2026-11-07',
}
PAIRS = dict(COMPARISON, **{'1.107.0': '2026-10-21'})
PAIR_SQL = ', '.join("(toDate('%s'), '%s')" % (d, v) for v, d in sorted(PAIRS.items()))
MARCH = "('1.82.6', '1.82.7', '1.82.8', '1.82.9')"

QUERIES = [
    ('Q1_daily_totals',
     "SELECT date, count FROM pypi.pypi_downloads_per_day WHERE project = 'litellm' "
     "AND date >= '2026-03-17' ORDER BY date"),
    ('Q2_daily_by_version_oct_nov',
     "SELECT date, version, sum(count) AS count FROM pypi.pypi_downloads_per_day_by_version "
     "WHERE project = 'litellm' AND date >= '2026-10-01' AND version LIKE '1.10_.%' "
     "GROUP BY date, version ORDER BY date, version"),
    ('Q3_daily_by_version_march',
     "SELECT date, version, sum(count) AS count FROM pypi.pypi_downloads_per_day_by_version "
     "WHERE project = 'litellm' AND date BETWEEN '2026-03-17' AND '2026-04-30' AND version IN " + MARCH + " "
     "GROUP BY date, version ORDER BY date, version"),
    ('Q4_installer',
     "SELECT date, version, installer, sum(count) AS count "
     "FROM pypi.pypi_downloads_per_day_by_version_by_installer_by_type WHERE project = 'litellm' "
     "AND ((date, version) IN (" + PAIR_SQL + ") OR (version = '1.107.0' AND date >= '2026-10-21') "
     "OR (version IN " + MARCH + " AND date BETWEEN '2026-03-24' AND '2026-04-30')) "
     "GROUP BY date, version, installer ORDER BY date, version, installer"),
    # File types from the file-type table: the installer table's type column keeps an arbitrary
    # value when rows merge (studies/LH005/LH005.md), so it is summed away above.
    ('Q7_file_type',
     "SELECT date, version, type, sum(count) AS count "
     "FROM pypi.pypi_downloads_per_day_by_version_by_file_type WHERE project = 'litellm' "
     "AND ((date, version) IN (" + PAIR_SQL + ") OR (version = '1.107.0' AND date >= '2026-10-21') "
     "OR (version IN " + MARCH + " AND date BETWEEN '2026-03-24' AND '2026-04-30')) "
     "GROUP BY date, version, type ORDER BY date, version, type"),
    ('Q5_system',
     "SELECT date, version, system, sum(count) AS count "
     "FROM pypi.pypi_downloads_per_day_by_version_by_system WHERE project = 'litellm' "
     "AND ((date, version) IN (" + PAIR_SQL + ") OR (version = '1.107.0' AND date >= '2026-10-21')) "
     "GROUP BY date, version, system ORDER BY date, version, system"),
    ('Q6_ci',
     "SELECT date, version, installer, ci, count() AS count FROM pypi.pypi WHERE project = 'litellm' "
     "AND (date, version) IN (" + PAIR_SQL + ") GROUP BY date, version, installer, ci "
     "ORDER BY date, version, installer, ci"),
]
GETS = [
    ('pypistats_overall', 'https://pypistats.org/api/packages/litellm/overall'),
    ('depsdev_1.107.0', 'https://api.deps.dev/v3/systems/pypi/packages/litellm/versions/1.107.0'),
    ('depsdev_dependents_1.107.0', 'https://api.deps.dev/v3alpha/systems/pypi/packages/litellm/versions/1.107.0:dependents'),
    ('depsdev_dependents_1.106.2', 'https://api.deps.dev/v3alpha/systems/pypi/packages/litellm/versions/1.106.2:dependents'),
    ('depsdev_dependents_1.106.1', 'https://api.deps.dev/v3alpha/systems/pypi/packages/litellm/versions/1.106.1:dependents'),
    ('depsdev_dependents_1.106.3', 'https://api.deps.dev/v3alpha/systems/pypi/packages/litellm/versions/1.106.3:dependents'),
]


def fetch(name, url, body, out, rows):
    row = {'name': name, 'url': url, 'utc_start': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'method': 'POST' if body else 'GET', 'request_body': body or ''}
    req = Request(url, data=body.encode() if body else None, headers={'User-Agent': UA})
    payload = b''
    try:
        try:
            resp = urlopen(req, timeout=120, context=CTX)
        except HTTPError as err:
            resp = err
        with resp:
            payload = resp.read(CEILING_BYTES + 1)
            summary = resp.headers.get('X-ClickHouse-Summary', '')
            try:
                s = json.loads(summary) if summary else {}
            except ValueError:
                s = {}
            row.update(status=resp.status, content_type=resp.headers.get('Content-Type', ''),
                       read_rows=s.get('read_rows', ''), read_bytes=s.get('read_bytes', ''))
    except Exception as err:
        row.update(status='error: ' + type(err).__name__ + ': ' + str(err)[:200], content_type='')
    row.update(size=len(payload), sha256=sha256(payload).hexdigest() if payload else '')
    if payload:
        (out / (name + '.raw')).write_bytes(payload[:CEILING_BYTES])
    rows.append(row)
    print(json.dumps({k: row.get(k) for k in ('name', 'status', 'size', 'read_rows')}), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read', required=True, help='UTC label, YYYY-MM-DDTHHMMZ')
    a = ap.parse_args()
    datetime.strptime(a.read, '%Y-%m-%dT%H%MZ')
    out = ROOT / 'data' / ('read-' + a.read)
    if out.exists():
        print('label already held; skipped:', out)
        return
    out.mkdir(parents=True)
    rows = []
    for name, sql in QUERIES:
        fetch(name, CH, sql, out, rows)
    assert len(GETS) <= MAX_GETS
    for name, url in GETS:
        fetch(name, url, None, out, rows)
    fields = ['name', 'url', 'utc_start', 'status', 'content_type', 'size', 'sha256', 'method',
              'request_body', 'read_rows', 'read_bytes']
    with open(out / 'readlog.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == '__main__':
    main()
