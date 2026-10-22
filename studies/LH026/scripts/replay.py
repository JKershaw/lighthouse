#!/usr/bin/env python3
"""Recompute exact base and derivative layer-prefix readings from retained bytes."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/snapshot-2026-10-22'
DRUPAL = ROOT.parent / 'LH023/data/snapshot-2026-10-22'
rows = list(csv.DictReader((OUT / 'read_log.csv').open()))
assert len(rows) <= 4
for row in rows:
    if row['key'] == 'auth':
        assert not row['sha256'] and not (OUT / 'auth.raw').exists()
        continue
    body = (OUT / (row['key'] + '.raw')).read_bytes()
    assert len(body) == int(row['bytes'])
    assert hashlib.sha256(body).hexdigest() == row['sha256']
    assert row['status'] == '200' and not row['error']

hub = json.loads((OUT / 'hubtag.raw').read_text())
platform = next(x for x in hub['images'] if x.get('os') == 'linux' and x.get('architecture') == 'amd64')
base_manifest_bytes = (OUT / 'manifest.raw').read_bytes()
assert hashlib.sha256(base_manifest_bytes).hexdigest() == platform['digest'].split(':')[1]
base_manifest = json.loads(base_manifest_bytes)
base_config_bytes = (OUT / 'config.raw').read_bytes()
assert hashlib.sha256(base_config_bytes).hexdigest() == base_manifest['config']['digest'].split(':')[1]
base_config = json.loads(base_config_bytes)

prior = list(csv.DictReader((DRUPAL / 'read_log.csv').open()))
for name in ('derived_tag', 'manifest', 'config'):
    r = next(x for x in prior if x['key'] == name)
    body = (DRUPAL / (name + '.raw')).read_bytes()
    assert hashlib.sha256(body).hexdigest() == r['sha256']
    assert len(body) == int(r['bytes'])
tag = json.loads((DRUPAL / 'derived_tag.raw').read_text())
derived_platform = next(x for x in tag['images'] if x.get('os') == 'linux' and x.get('architecture') == 'amd64')
derived_manifest_bytes = (DRUPAL / 'manifest.raw').read_bytes()
assert hashlib.sha256(derived_manifest_bytes).hexdigest() == derived_platform['digest'].split(':')[1]
derived_manifest = json.loads(derived_manifest_bytes)
derived_config_bytes = (DRUPAL / 'config.raw').read_bytes()
assert hashlib.sha256(derived_config_bytes).hexdigest() == derived_manifest['config']['digest'].split(':')[1]
derived_config = json.loads(derived_config_bytes)

def compare(base, derived):
    mismatch = next((i for i, (a, b) in enumerate(zip(base, derived)) if a != b), None)
    return dict(base_layers=len(base), derived_layers=len(derived),
                is_full_prefix=len(derived) >= len(base) and mismatch is None,
                first_mismatch_index=mismatch)


uncompressed = compare(base_config['rootfs']['diff_ids'], derived_config['rootfs']['diff_ids'])
compressed = compare([x['digest'] for x in base_manifest['layers']],
                     [x['digest'] for x in derived_manifest['layers']])
versions = [[x for x in config['config']['Env'] if x.startswith('PHP_VERSION=')]
            for config in (base_config, derived_config)]
result = dict(base_platform_digest=platform['digest'], derived_platform_digest=derived_platform['digest'],
              uncompressed_diff_ids=uncompressed, compressed_layer_digests=compressed,
              base_php_version=versions[0], derived_php_version=versions[1],
              base_read_utc=rows[0]['utc'], derivative_read_utc=prior[0]['utc'])
(ROOT / 'data/result-2026-10-22.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
