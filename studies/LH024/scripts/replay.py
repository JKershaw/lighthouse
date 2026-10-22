#!/usr/bin/env python3
"""Offline checks of the LH024 retained first-day panel and primary response bytes."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'data/snapshot-2026-10-22'
panel = {x['id']: x for x in json.loads((ROOT / 'panel.json').read_text())}
selected = {x['id']: x for x in json.loads((ROOT / 'selection-2026-10-22.json').read_text())}
events = {x['id']: x for x in json.loads((ROOT / 'data/events-2026-10-22.json').read_text())}
reads = {x['key']: x for x in csv.DictReader((out / 'read_log.csv').open())}
assert len(panel) == len(selected) == len(events) == 13
assert len(reads) == sum(len(x['urls']) for x in selected.values()) == 17
assert all(len(x['urls']) <= 2 for x in selected.values())
for id_, row in events.items():
    assert all(key in reads and key.startswith(id_ + '_') for key in row['source_keys'])
for key, read in reads.items():
    assert read['url'] in selected[key.rsplit('_', 1)[0]]['urls']
    if read['raw_retained'] == 'True':
        data = (out / (key + '.raw')).read_bytes()
        assert len(data) == int(read['bytes_retained'])
        assert hashlib.sha256(data).hexdigest() == read['sha256_retained']
    else:
        assert not (out / (key + '.raw')).exists()
for key in ('aws_0', 'aws_1', 'google_cloud_0', 'google_cloud_1'):
    assert b'Site Unavailable' in (out / (key + '.raw')).read_bytes()
assert reads['cisa_0']['status'] == '403'
print('verified 13 panel entries, 17 attempts, retained primary hashes and four 200-status access failures')
print('Media hashes record fetched bytes, but cannot be replayed offline because article bodies were not retained.')
