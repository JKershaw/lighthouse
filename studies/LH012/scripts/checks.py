#!/usr/bin/env python3
"""LH012: checks of a surprising result against a second table, run after the counts were read.
C1 and C2 read boto3's downloads on one day of W (Wednesday 23 September 2026) by Python minor from
the by-Python view and from `pypi.pypi` itself, to check that 3.9 carries most of boto3's older
downloads in both. C3 (post hoc, one description) splits the same day's Python 3.9 downloads of
boto3 by installer, CI flag and system, to say what those fetches are. Writes data/checks/.
New for LH012. Usage: LH012_PHASE=2 python3 checks.py"""
import os
import phase2  # noqa: F401
import common
from common import DATA

D = '2026-09-23'
os.makedirs(os.path.join(DATA, 'checks'), exist_ok=True)
common.clickhouse('C1 boto3 by Python, by-Python view', f"SELECT python_minor, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version_by_python "
                  f"WHERE project = 'boto3' AND date = '{D}' GROUP BY python_minor ORDER BY n DESC", 'checks/boto3_python_view.csv')
common.clickhouse('C2 boto3 by Python, pypi.pypi', f"SELECT python_minor, count() AS n FROM pypi.pypi WHERE project = 'boto3' AND date = '{D}' "
                  "GROUP BY python_minor ORDER BY n DESC", 'checks/boto3_python_pypi.csv')
common.clickhouse('C3 boto3 Python 3.9 by installer, ci, system (post hoc)', f"SELECT installer, ci, system, tupleElement(libc, 'lib') AS libc_lib, count() AS n "
                  f"FROM pypi.pypi WHERE project = 'boto3' AND date = '{D}' AND python_minor = '3.9' GROUP BY installer, ci, system, libc_lib ORDER BY n DESC LIMIT 20",
                  'checks/boto3_py39_installers.csv')
