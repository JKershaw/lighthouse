#!/usr/bin/env python3
"""Per-entry table for one LH030 read. Applies the brief's written rule that a tracker's 404, or a record API's
explicit empty answer, is "no record" rather than unavailable (written after the baseline was seen; it encodes the
brief's text and changes no class), joins the hand decisions on IV kept in hand_iv.json, and prints one row per entry.
Usage: tabulate.py <read directory>"""
from pathlib import Path
import json
import sys

read_dir = Path(sys.argv[1])
log = {r['name']: r for r in json.loads((read_dir / 'read_log.json').read_text())}
classes = json.loads((read_dir / 'classes.json').read_text())
hand = json.loads((read_dir / 'hand_iv.json').read_text()) if (read_dir / 'hand_iv.json').exists() else {}


def no_record(row):
    if row.get('group') != 'records' or 'file' not in row:
        return False
    body = (read_dir / row['file']).read_text(encoding='utf-8', errors='replace')
    if row.get('status') == 404:
        return True
    try:
        data = json.loads(body)
    except ValueError:
        return False
    return data.get('totalResults') == 0 or data.get('error') == 'CVE_RECORD_DNE'


entries = {}
for c in classes:
    row = log[c['name']]
    state = 'no record' if no_record(row) else c['access']
    e = entries.setdefault((c['group'], c['source']), {'urls': 0, 'states': [], 'I': False, 'II': False, 'III': False, 'V': set(), 'IV': 'n/a'})
    e['urls'] += 1
    e['states'].append(f"{c['name']}:{row.get('status')}:{state}")
    if state == 'read':
        e['I'] |= bool(c['I']); e['II'] |= c['II_yes']; e['III'] |= c['III_yes']; e['V'] |= set(c['V'])
        if c['IV_yes']:
            e['IV'] = hand.get(c['name'], 'snippets await a hand reading')
        elif e['IV'] == 'n/a':
            e['IV'] = 'none'
for (group, source), e in entries.items():
    print(json.dumps({'group': group, 'entry': source, 'states': e['states'], 'I': e['I'], 'II': e['II'], 'III': e['III'],
                      'IV': e['IV'], 'V': sorted(e['V'])}))
