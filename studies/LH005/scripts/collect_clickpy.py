#!/usr/bin/env python3
"""LH005: every ClickPy read, in the order run. ClickPy is ClickHouse's public copy of PyPI's
BigQuery download table (sources.md in this directory). The demo user is anonymous; results are
capped by the server at 10,000 rows, so each query is filtered to named projects and dates.
Usage: python3 collect_clickpy.py   (writes data/clickpy_*.csv and appends to data/read_log.csv)"""
from common import clickhouse

MCP = "'mcp'"
COHORT = ("'mcp','agentcrew-ai','databricks-tellr-app','lean-lsp-mcp','pyp6xer-mcp','serena-agent',"
          "'dartlab','mistral-vibe','octobot','jesse'")
WINDOW_MARGIN = "date BETWEEN '2026-03-19' AND '2026-04-29'"   # LH002 window plus seven days either side
CONTRAST = "date BETWEEN '2026-01-17' AND '2026-02-27'"        # 1.26.0: seven days before its release day, 34 after
PEPY_OVERLAP = "date BETWEEN '2026-06-27' AND '2026-09-25'"    # the days pepy's anonymous API holds
VCLASS = ("multiIf(version = '1.27.0', '1.27.0', version = '1.26.0', '1.26.0', version = '1.25.0', '1.25.0', "
          "version = '1.26.1', '1.26.1', 'other')")

# C01 what the database holds: every table's engine, row count and definition
clickhouse('C01 schema', """
SELECT name, engine, total_rows, create_table_query FROM system.tables WHERE database = 'pypi' ORDER BY name
""", 'clickpy_schema.csv')

# C02 first and last day held for each cohort package
clickhouse('C02 coverage', f"""
SELECT project, min(min_date) AS first_day, max(max_date) AS last_day
FROM pypi.pypi_downloads_max_min WHERE project IN ({COHORT}) GROUP BY project ORDER BY project
""", 'clickpy_coverage.csv')

# C03 release upload times from ClickPy's copy of PyPI's metadata table, for the packages read by version
clickhouse('C03 uploads', """
SELECT name AS project, version, min(upload_time) AS first_upload_utc, groupUniqArray(packagetype) AS file_types
FROM pypi.projects WHERE name IN ('mcp', 'lean-lsp-mcp') GROUP BY name, version ORDER BY name, first_upload_utc
""", 'clickpy_uploads.csv')

# C04 mcp daily totals, from the release before the window to the last day held
clickhouse('C04 mcp daily totals', f"""
SELECT date, count AS downloads FROM (SELECT date, sum(count) AS count FROM pypi.pypi_downloads_per_day
WHERE project = {MCP} AND date BETWEEN '2026-01-17' AND '2026-09-25' GROUP BY date) ORDER BY date
""", 'clickpy_mcp_daily_total.csv')

# C05 mcp daily downloads by version, in three periods (the server returns at most 10,000 rows)
for label, period, out in (('C05a', WINDOW_MARGIN, 'clickpy_mcp_daily_by_version_window.csv'),
                           ('C05b', CONTRAST, 'clickpy_mcp_daily_by_version_contrast.csv'),
                           ('C05c', PEPY_OVERLAP, 'clickpy_mcp_daily_by_version_pepy_overlap.csv')):
    clickhouse(f'{label} mcp by version', f"""
    SELECT date, version, sum(count) AS downloads FROM pypi.pypi_downloads_per_day_by_version
    WHERE project = {MCP} AND {period} GROUP BY date, version ORDER BY date, version
    """, out)

# C06 mcp daily downloads by version class, installer name and file type
for label, period, out in (('C06a', WINDOW_MARGIN, 'clickpy_mcp_daily_by_installer_window.csv'),
                           ('C06b', CONTRAST, 'clickpy_mcp_daily_by_installer_contrast.csv')):
    clickhouse(f'{label} mcp by installer and type', f"""
    SELECT date, {VCLASS} AS version_class, installer, type, sum(count) AS downloads
    FROM pypi.pypi_downloads_per_day_by_version_by_installer_by_type
    WHERE project = {MCP} AND {period} GROUP BY date, version_class, installer, type
    ORDER BY date, version_class, installer, type
    """, out)

# C07 mcp from the per-download table: the CI flag, which no aggregate table carries
clickhouse('C07 mcp by ci flag', f"""
SELECT date, {VCLASS} AS version_class, installer, toString(ci) AS ci, count() AS downloads
FROM pypi.pypi WHERE project = {MCP} AND {WINDOW_MARGIN}
GROUP BY date, version_class, installer, ci ORDER BY date, version_class, installer, ci
""", 'clickpy_mcp_daily_by_ci_window.csv')

# C08 the CI flag in the contrast period, to see whether the field was populated then
clickhouse('C08 mcp ci flag contrast', f"""
SELECT date, {VCLASS} AS version_class, toString(ci) AS ci, count() AS downloads
FROM pypi.pypi WHERE project = {MCP} AND {CONTRAST}
GROUP BY date, version_class, ci ORDER BY date, version_class, ci
""", 'clickpy_mcp_daily_by_ci_contrast.csv')

# C09 lean-lsp-mcp, the exact-pin dependent (LH002's R03), per download: version, installer, type, CI flag
clickhouse('C09 lean-lsp-mcp', """
SELECT date, version, installer, type, toString(ci) AS ci, count() AS downloads
FROM pypi.pypi WHERE project = 'lean-lsp-mcp' AND date BETWEEN '2026-03-19' AND '2026-05-10'
GROUP BY date, version, installer, type, ci ORDER BY date, version, installer, type, ci
""", 'clickpy_lean_lsp_mcp_window.csv')

# C10 the other cohort packages' daily totals in the window, for scale only
clickhouse('C10 cohort daily totals', f"""
SELECT date, project, sum(count) AS downloads FROM pypi.pypi_downloads_per_day
WHERE project IN ({COHORT}) AND {WINDOW_MARGIN} GROUP BY date, project ORDER BY project, date
""", 'clickpy_cohort_daily_total.csv')

# C11 file type from the table whose sorting key includes it. In the installer table above, `type` is
# outside the SummingMergeTree key (project, version, date, installer), so merged rows keep one
# arbitrary file type; that table is used for installers only.
clickhouse('C11 mcp by file type', f"""
SELECT date, {VCLASS} AS version_class, type, sum(count) AS downloads
FROM pypi.pypi_downloads_per_day_by_version_by_file_type
WHERE project = {MCP} AND {WINDOW_MARGIN} GROUP BY date, version_class, type ORDER BY date, version_class, type
""", 'clickpy_mcp_daily_by_file_type_window.csv')

# C12 downloads recorded under the name mcp before the current project's first file (PyPI JSON API: 2024-11-20)
clickhouse('C12 mcp before 2024-11-20', """
SELECT toYear(date) AS year, sum(count) AS downloads, min(date) AS first_day, max(date) AS last_day
FROM pypi.pypi_downloads_per_day WHERE project = 'mcp' AND date < '2024-11-20' GROUP BY year ORDER BY year
""", 'clickpy_mcp_before_current_project.csv')
