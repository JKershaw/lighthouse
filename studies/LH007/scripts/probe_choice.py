#!/usr/bin/env python3
"""LH007 step 0: the reads behind the choice of library and release (brief.md, 'Choice').
Reads only PyPI's release list and Open Source Insights' dependents counts; no tag list,
manifest, configuration or layer. Writes data/choice_reads.csv."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, write_csv

LIBS = [a for a in sys.argv[1:] if not a.startswith('--')] or ['mcp']
rows = []
for lib in LIBS:
    r = http('PyPI JSON API', f'PyPI {lib}', f'https://pypi.org/pypi/{lib}/json')
    rel = r.json()['releases']
    vs = []
    for v, files in rel.items():
        if not files: continue
        t = min(f['upload_time_iso_8601'] for f in files)
        if t >= '2026-05-01':
            vs.append((t, v))
    for t, v in sorted(vs):
        rows.append(dict(library=lib, version=v, first_upload_utc=t))
        print(lib, v, t)
write_csv('choice_releases.csv', rows)

# The dependents counts that informed the choice were read at 21:15:50 UTC with this code (run inline
# then; the counts are in data/read_log.csv's labels and in LH007.md). Pass --counts to repeat it.
if '--counts' in sys.argv:
    for v in ['1.28.0', '1.28.1', '1.27.2', '1.29.0']:
        j = http('Open Source Insights', f'deps.dev dependents mcp {v} (counts, for the choice)',
                 f'https://deps.dev/_/s/pypi/p/mcp/v/{v}/dependents').json()
        print(v, {k: j.get(k) for k in ('totalCount', 'directCount', 'indirectCount')})
