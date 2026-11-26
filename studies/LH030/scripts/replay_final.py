#!/usr/bin/env python3
"""Replay for LH030's final record (version 1.0), written after every read had been seen.
For each retained read directory that has a classes.json, copies the directory to a temporary place, reruns the
fixed classifier there (so the retained classes.json is never overwritten), checks that the rerun's classes.json is
byte for byte the retained one, runs tabulate.py on the retained directory, and then prints, per panel entry, each
read at which its tabulated state or classes changed. It changes no class and adds no rule: retirement (VI) and the
IV decisions are hand readings kept in each read's hand_iv.json and in the record, not computed here.
Usage: python3 -I studies/LH030/scripts/replay_final.py"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / 'data'


def tabulate(read_dir):
    out = subprocess.run([sys.executable, '-I', str(HERE / 'tabulate.py'), str(read_dir)], capture_output=True, text=True, check=True).stdout
    rows = {}
    for line in out.splitlines():
        r = json.loads(line)
        states = sorted({s.split(':', 2)[2] for s in r['states']})
        statuses = [s.split(':', 2)[1] for s in r['states']]
        iv = r['IV'].split(':', 1)[0]
        rows[r['entry']] = (r['group'], '/'.join(states), '/'.join(statuses), r['I'], r['II'], r['III'], iv, bool(r['V']))
    return rows


reads = sorted(d for d in DATA.glob('read-*') if (d / 'classes.json').exists())
skipped = sorted(d.name for d in DATA.glob('read-*') if not (d / 'classes.json').exists())
print(f'{len(reads)} read directories with classes.json; skipped (no classes.json): {", ".join(skipped) or "none"}')
mismatch = 0
with tempfile.TemporaryDirectory() as tmp:
    for d in reads:
        copy = Path(tmp) / d.name
        shutil.copytree(d, copy)
        subprocess.run([sys.executable, '-I', str(HERE / 'classify.py'), str(copy)], capture_output=True, check=True)
        same = (copy / 'classes.json').read_bytes() == (d / 'classes.json').read_bytes()
        mismatch += not same
        print(f'{d.name}: rerun classes.json {"identical to retained" if same else "DIFFERS from retained"}')
print(f'classifier replay mismatches: {mismatch}')
print()
print('Per entry: read label, access state (HTTP status), I, II, III, IV hand decision, V; printed at the first read and at each change.')
history = {}
order = []
for d in reads:
    for entry, row in tabulate(d).items():
        if entry not in history:
            order.append(entry)
            history[entry] = []
        if not history[entry] or history[entry][-1][1] != row:
            history[entry].append((d.name[5:], row))
for entry in order:
    group = history[entry][0][1][0]
    print(f'{entry} ({group})')
    for label, (g, state, status, i, ii, iii, iv, v) in history[entry]:
        print(f'  {label}: {state} ({status}); I={i} II={ii} III={iii} IV={iv} V={v}')
print()
print('Readable entries per read (an entry counts as readable when at least one of its URLs was read in full or answered "no record"; the PHP reference is not counted):')
for d in reads:
    rows = tabulate(d)
    counted = {e: r for e, r in rows.items() if r[0] != 'reference'}
    readable = [e for e, r in counted.items() if 'read' in r[1].split('/') or 'no record' in r[1].split('/')]
    unread = sorted(set(counted) - set(readable))
    print(f'  {d.name[5:]}: {len(readable)} of {len(counted)}; not readable: {", ".join(unread)}')
