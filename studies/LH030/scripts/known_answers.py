#!/usr/bin/env python3
"""Run the fixed classifier on bodies retained before LH030, whose classes are already known:
pre-instruction pages of 22 October (LH024) as negatives; PHP's 23 October page (LH029), Cloudflare's
23 October 16:06 UTC revision (LH028) and SOCRadar's 23 October page (discovery pass) as positives."""
from pathlib import Path
import csv
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from classify import classify  # noqa: E402

cases = []
for r in csv.DictReader(open(REPO / 'studies/LH024/data/snapshot-2026-10-22/read_log.csv')):
    if r['raw_retained'] == 'True' and r['key'] not in ('php_1',):
        cases.append(('notices', 'neg22oct_' + r['key'], REPO / 'studies/LH024/data/snapshot-2026-10-22' / (r['key'] + '.raw'), int(r['status'] or 0)))
cases += [('reference', 'pos_php_23oct', REPO / 'studies/LH029/data/snapshot-2026-10-23/archive.raw', 200),
          ('notices', 'pos_cloudflare_23oct', REPO / 'studies/LH028/data/snapshot-2026-10-23T1600Z/cloudflare.raw', 200),
          ('notices', 'pos_socradar_23oct', REPO / 'notes/php-discovery-2026-10-23/pages/socradar.raw', 200)]
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    rows = []
    for group, name, path, status in cases:
        (tmp / (name + '.raw')).write_bytes(path.read_bytes())
        rows.append({'group': group, 'source': name, 'name': name, 'status': status, 'bytes': path.stat().st_size,
                     'content_type': 'text/html', 'file': name + '.raw', 'sha256': ''})
    (tmp / 'read_log.json').write_text(json.dumps(rows))
    for result in classify(tmp):
        print(json.dumps({k: result.get(k) for k in ('name', 'access', 'I', 'II_yes', 'III_yes', 'IV_yes', 'V')}))
        if result.get('IV_yes'):
            for snippet in result['IV'][:3]:
                print('   IV snippet:', snippet[:260])
