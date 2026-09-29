#!/usr/bin/env python3
"""LH014 phase 1: ClickPy's server, the `demo` user's settings, and the `pypi` database's table
definitions and columns, read before the brief was fixed and before any download count. Every query
reads the `system` database only (the phase gate in common.py refuses anything else). The tables'
row totals (system.tables.total_rows) are not read, since `pypi.pypi` holds one row per download.

Adapted from studies/LH011/scripts/collect_frame.py (F00 to F02). What changed: the settings are read
from system.settings (every setting changed from its default for this user) as well as by name; the
schema read leaves out total_rows; the columns of every table of the `pypi` database are kept.
S04 and the two documentation pages (D01, D02) were first run inline, at 12:30:29 to 12:30:56 UTC
on 29 September 2026, after S00 showed the `demo` user's read_overflow_mode to be 'break'; this file
keeps them with the texts and URLs used. The pages are saved to scratch space only.
Writes data/clickpy_server.csv, clickpy_settings.csv, clickpy_schema.csv, clickpy_columns.csv and
clickpy_overflow_setting.csv.
Usage: python3 collect_schema.py [--docs]"""
import os, sys
from common import clickhouse, get_text, SCRATCH

clickhouse('S00 server and limits', "SELECT version() AS server_version, timezone() AS tz, "
           "getSetting('max_result_rows') AS max_result_rows, getSetting('result_overflow_mode') AS result_overflow_mode, "
           "getSetting('max_rows_to_read') AS max_rows_to_read, getSetting('max_bytes_to_read') AS max_bytes_to_read, "
           "getSetting('read_overflow_mode') AS read_overflow_mode, getSetting('max_execution_time') AS max_execution_time, "
           "getSetting('readonly') AS readonly", 'clickpy_server.csv')
clickhouse('S01 changed settings', "SELECT name, value, type FROM system.settings WHERE changed ORDER BY name",
           'clickpy_settings.csv')
clickhouse('S02 schema', "SELECT name, engine, sorting_key, primary_key, create_table_query "
           "FROM system.tables WHERE database = 'pypi' ORDER BY name", 'clickpy_schema.csv')
clickhouse('S03 columns', "SELECT table, position, name, type FROM system.columns WHERE database = 'pypi' "
           "ORDER BY table, position", 'clickpy_columns.csv')
clickhouse('S04 can a query set read_overflow_mode to throw', "SELECT getSetting('read_overflow_mode') AS read_overflow_mode, "
           "getSetting('max_rows_to_read') AS max_rows_to_read SETTINGS read_overflow_mode = 'throw'",
           'clickpy_overflow_setting.csv')
if '--docs' in sys.argv:
    get_text('D01 ClickHouse query complexity settings', 'https://clickhouse.com/docs/operations/settings/query-complexity',
             os.path.join(SCRATCH, 'ch_query_complexity.html'))
    get_text('D02 pypistats FAQ', 'https://pypistats.org/faqs', os.path.join(SCRATCH, 'pypistats_faqs.html'))
