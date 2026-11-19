"""LH013 installer brief, Stage A (studies/LH013/installer-brief.md): ClickPy, anonymous, no account.

A1: boto3's rows on D (17 November 2026) and how many have a file name ending .metadata, split by
python_minor 3.9 or other and by installer name. A2: boto3's total for D from pypi_downloads_per_day.
Two queries, inside the brief's ceiling of five. Every request goes through common.py (robots.txt gate,
overflow settings, read_log.csv). Writes data/installer/stage_a_A1.csv and stage_a_A2.csv.

Usage: LIGHTHOUSE_PROVIDER=anthropic LH013_PHASE=counts python3 scripts/installer_stage_a.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import clickhouse  # noqa: E402

D = '2026-11-17'
a1 = clickhouse('installer-A', 'A1', f"""
SELECT if(python_minor = '3.9', '3.9', 'other') AS py, installer, count() AS rows,
       countIf(endsWith(filename, '.metadata')) AS metadata_rows
FROM pypi.pypi WHERE project = 'boto3' AND date = '{D}'
GROUP BY py, installer ORDER BY rows DESC""", output='installer/stage_a_A1.csv',
    note='installer brief Stage A, A1')
a2 = clickhouse('installer-A', 'A2', f"""
SELECT date, project, sum(count) AS total
FROM pypi.pypi_downloads_per_day WHERE project = 'boto3' AND date = '{D}'
GROUP BY date, project""", output='installer/stage_a_A2.csv', note='installer brief Stage A, A2')
for name, rows in (('A1', a1), ('A2', a2)):
    print(name, 'failed' if rows is None else f'{len(rows)} rows')
    for r in (rows or [])[:20]:
        print('  ', r)
