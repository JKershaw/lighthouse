#!/usr/bin/env python3
"""The panel's week, 22 to 28 October 2026, from the retained daily reads. Offline.

For each read: per institution, how many selected URLs answered HTTP 200 with a body over 1,000 bytes
(readable), and which retained bodies name CVE-2026-115560. Media entries keep metadata only, so they
are counted for access and not searched.

Usage: python3 studies/LH024/scripts/week.py
"""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
for snap in sorted((ROOT / 'data').glob('snapshot-*')):
    day = snap.name[9:]
    log = list(csv.DictReader(open(snap / 'read_log.csv', newline='')))
    by = {}
    for r in log:
        inst = r['key'].rsplit('_', 1)[0]
        ok = r['status'] == '200' and int(r['bytes_retained'] or 0) > 1000
        names = False
        raw = snap / Path(r['key'] + '.raw')
        if raw.exists():
            names = b'115560' in raw.read_bytes()
        a = by.setdefault(inst, [0, 0, 0])
        a[0] += 1; a[1] += ok; a[2] += names
    print(day, log[0]['observed_at_utc'], f'{len(log)} GETs')
    for inst, (n, ok, names) in sorted(by.items()):
        print(f'  {inst:<18} urls {n}  readable {ok}  name CVE-2026-115560 {names}')
