"""LH012 phase 2: points common.py's logger at data/read_log_phase2.csv, sets the phase to 2 and sets
each ceiling to the brief's less what phase 1 used (amendment 1). common.py itself is unchanged, so
its snapshot hash still verifies. Import this module instead of common in phase 2 scripts."""
import csv, os
import common
from common import *  # noqa: F401,F403

PHASE1_LOG = common.LOG
common.LOG = os.path.join(common.DATA, 'read_log_phase2.csv')
common.PHASE = '2'
_p1 = list(csv.DictReader(open(PHASE1_LOG)))
_q1 = sum(r['source'].startswith('ClickPy') for r in _p1)
_r1 = sum(int(r['read_rows'] or 0) for r in _p1 if r['source'].startswith('ClickPy'))
_j1 = sum(r['source'].startswith('PyPI JSON') for r in _p1)
common.MAX_QUERIES = 900 - _q1
common.MAX_ROWS_READ = 40_000_000_000 - _r1
common.MAX_PYPI = 5000 - _j1
clickhouse, get_json, write_csv, read_csv = common.clickhouse, common.get_json, common.write_csv, common.read_csv
DATA, SCRATCH = common.DATA, common.SCRATCH
