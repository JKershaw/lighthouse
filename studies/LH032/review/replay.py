#!/usr/bin/env python3
"""Reproduce the pinned baseline repair; no external reads or upstream execution."""
from collections import Counter
from datetime import datetime
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CLONE = Path(sys.argv[1])
PIN = '2fdc314ded280d18868d13d2f33d092a15e5a231'
CORRECTED = ROOT / 'data/read-2026-10-23-baseline-audit'
ORIGINAL = ROOT / 'data/read-2026-10-23T1850Z'
sys.path.insert(0, str(ROOT / 'scripts'))
from verify_inventory import git

with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / 'read'
    subprocess.run([sys.executable, str(ROOT / 'scripts/analyse.py'), str(CLONE), 'replay',
                    '--commit', PIN, '--output', str(out)], check=True, stdout=subprocess.DEVNULL)
    for name in ('entries', 'summary', 'inventory_verification', 'source_entries'):
        assert json.loads((out / (name + '.json')).read_bytes()) == json.loads(
            gzip.decompress((CORRECTED / (name + '.json.gz')).read_bytes())), name
for path in (ORIGINAL / 'list').iterdir():
    source_path = 'LICENSE' if path.name == 'LICENSE' else 'software/' + path.name
    assert path.read_bytes() == git(CLONE, 'show', PIN + ':' + source_path), path.name
advisories = ROOT / 'review/advisory-check-2026-10-23'
reads = json.loads((advisories / 'read_log.json').read_text())
assert len(reads) == 4
for read in reads:
    packed = (advisories / read['file']).read_bytes()
    raw = gzip.decompress(packed)
    assert hashlib.sha256(packed).hexdigest() == read['sha256_gzip']
    assert hashlib.sha256(raw).hexdigest() == read['sha256_retained_response']
    assert len(raw) == read['bytes_retained'] <= 512 * 1024
assert sum(read['bytes_retained'] for read in reads) == 464810
old = json.loads((ORIGINAL / 'entries.json').read_text())
new = json.loads(gzip.decompress((CORRECTED / 'entries.json.gz').read_bytes()))
new_map = {(r['supplier'], r['product']): r for r in new}
changes = []
for row in old:
    corrected = new_map[(row['supplier'], row['product'])]
    changed = {field: {'original': row[field], 'corrected': corrected[field]}
               for field in ('first_listed', 'first_fix_or_not_vuln', 'links_vendor', 'version', 'status_at_head')
               if row[field] != corrected[field]}
    if changed:
        changes.append({'supplier': row['supplier'], 'product': row['product'], 'changed': changed})
bins = Counter()
for row in new:
    h = row['hours_from_php_release_to_that_commit']
    if h is not None:
        bins['before_release' if h < 0 else '0_to_12' if h < 12 else '12_to_24' if h < 24
             else '24_to_36' if h < 36 else '36_to_48' if h < 48 else '48_or_more'] += 1
firsts = Counter(row['first_listed'] for row in new)
report = {'source_commit': PIN, 'all_four_corrected_outputs_replayed': True,
          'original_retained_list_files_match_pinned_source': True,
          'field_difference_counts': dict(Counter(f for r in changes for f in r['changed'])),
          'first_fix_or_not_vuln_bins_hours': dict(bins),
          'largest_surviving_identity_first_listed_batch': firsts.most_common(1),
          'corrected_artifact_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                       for p in sorted(CORRECTED.glob('*.gz'))},
          'differences': changes}
print(json.dumps(report, indent=1))
