#!/usr/bin/env python3
"""Offline integrity and status check for LH027's one bounded request."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
record = json.loads((root / 'data/read-2026-10-22.json').read_text())
body = (root / 'data/notice-2026-10-22.html').read_bytes()
assert len(body) == record['byte_count'] == 919
assert hashlib.sha256(body).hexdigest() == record['sha256']
assert record['status'] == 403
assert record['url'] == record['final_url']
print('LH027 retained response: HTTP 403, 919 bytes, hash verified; notice unavailable')
