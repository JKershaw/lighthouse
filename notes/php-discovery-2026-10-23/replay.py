#!/usr/bin/env python3
"""Verify the discovery pass's retained pages against its read log."""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
for row in json.loads((HERE / 'read_log.json').read_text()):
    body = (HERE / row['file']).read_bytes()
    assert len(body) == row['bytes'] and sha256(body).hexdigest() == row['sha256']
    print(row['source'], row['status'], row['start_utc'], row['bytes'], 'bytes verified')
