#!/usr/bin/env python3
"""Offline verification of retained LH028 responses."""
from hashlib import sha256
from pathlib import Path
import argparse
import json

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--snapshot', required=True)
args = parser.parse_args()
rows = json.loads((root / 'data' / ('snapshot-' + args.snapshot) / 'read_log.json').read_text())
assert len(rows) == 3
for row in rows:
    if 'file' not in row:
        print(row['source'], row.get('error', 'unavailable'))
        continue
    body = (root / row['file']).read_bytes()
    assert len(body) == row['bytes'] <= 1024 * 1024
    assert sha256(body).hexdigest() == row['sha256']
    print(row['source'], row['status'], row['bytes'], 'bytes verified')
