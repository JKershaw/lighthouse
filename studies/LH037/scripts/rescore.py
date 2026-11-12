#!/usr/bin/env python3
"""Re-score LH037's held bodies offline under the old and the amended mention rules (amendment of 12 November 2026).

Post hoc: written after the 12 November read showed the old rule scoring D-Link's listing 0. Fetches nothing and
writes nothing; it reads each read's logs and gzipped bodies under data/ and prints, per read:
- whether the old rule recomputed on the held body gives the count the log recorded (held bodies have had email
  addresses withheld, so a difference there would come from that, and is printed);
- every body the old rule did not flag (no CVE id exactly, no whole-word PHP) that the amended rule flags;
- every body with a whole-word PHP count of 0 and an amended php count above 0, flagged or not by a CVE id.

Usage: python3 -I studies/LH037/scripts/rescore.py
"""
from pathlib import Path
import gzip, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mentions import counts, flagged_old, flagged_new  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CVES = json.loads((ROOT / 'panel.json').read_text())['cves']

for read in sorted((ROOT / 'data').glob('read-*')):
    rows = []
    for log in ('read_log.json', 'found_log.json'):
        if (read / log).exists():
            rows += [(log, row) for row in json.loads((read / log).read_text())]
    held = mismatch = 0
    missed, php_only = [], []
    absent = []
    for log, row in rows:
        path = read / row['file'] if row.get('file') else None
        if not path or not path.exists():
            absent.append(row['name'])
            continue
        held += 1
        m = counts(gzip.decompress(path.read_bytes()), CVES)
        logged = row.get('mentions', {})
        if any(logged.get(k) != m[k] for k in CVES + ['PHP']):
            mismatch += 1
            print('  recount differs from log:', row['name'], {k: (logged.get(k), m[k]) for k in CVES + ['PHP']})
        short = {'PHP': m['PHP'], 'php_prefix': m['php_prefix'],
                 'cve_exact': sum(m[c] for c in CVES), 'cve_any_case': sum(m['cve_any_case'].values())}
        if not flagged_old(m, CVES) and flagged_new(m, CVES):
            missed.append((log, row['vendor'], row['name'], short))
        if m['PHP'] == 0 and m['php_prefix'] > 0:
            php_only.append((log, row['vendor'], row['name'], short))
    print(f'{read.name}: {len(rows)} log rows, {held} bodies held, {len(absent)} not held'
          f'{" (" + ", ".join(absent) + ")" if absent else ""}; old-rule recount differs from log for {mismatch}')
    print(f'  flagged by the amended rule only (old rule: nothing): {len(missed)}')
    for item in missed:
        print('   ', *item)
    print(f'  whole-word PHP 0 but amended php count > 0: {len(php_only)}')
    for item in php_only:
        print('   ', *item)
