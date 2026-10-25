#!/usr/bin/env python3
"""Tabulate one LH033 read offline: measures 1 and 2 from Censys, 4 from W3Techs and 5 from Packagist (brief.md, Measures).

Usage: tabulate.py <read label>, e.g. 2026-10-25T0856Z. Writes data/read-<label>/tables.json and prints it.
Only completed UTC days (before the read's date) enter measures 1 and 2; day 0 is 21 October 2026.
Measure 3 is taken only on the read holding day 30.
"""
from datetime import date
from pathlib import Path
import gzip
import html
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
label = sys.argv[1]
READ = ROOT / 'data' / ('read-' + label)
read_day = date.fromisoformat(label[:10])
DAY0 = date(2026, 10, 21)
FIXED = {'8.2': 35, '8.3': 36, '8.4': 27, '8.5': 12}
tables = {'read': label}


def body(name):
    return gzip.decompress((READ / (name + '.raw.gz')).read_bytes())


if (READ / 'censys.raw.gz').exists():
    snap = json.loads(body('censys'))['snapshot']
    tables['censys_refreshed_at'] = snap['refreshed_at']
    done = lambda day: date.fromisoformat(day) < read_day
    m1 = {}
    for r in snap['branch_history']:
        if done(r['day']):
            m1.setdefault(r['branch'], {})[(date.fromisoformat(r['day']) - DAY0).days] = {
                'day': r['day'], 'patched': r['patched'], 'targets': r['targets'], 'share': round(r['patched'] / r['targets'], 4)}
    tables['m1_patched_share_by_branch'] = {b: dict(sorted(v.items())) for b, v in sorted(m1.items())}
    tables['m1_first_day_at_half'] = {b: next((d for d, x in sorted(v.items()) if x['share'] >= 0.5), None) for b, v in m1.items()}
    by_day = {}
    for r in snap['history']:
        if done(r['day']):
            by_day.setdefault(r['day'], {})[r['status']] = r['targets']
    m2 = {}
    for day, s in sorted(by_day.items()):
        versioned = s['affected'] + s['affected_nofix'] + s['patched']
        m2[(date.fromisoformat(day) - DAY0).days] = {
            'day': day, **s, 'versioned': versioned, 'all': versioned + s['unknown'],
            'nofix_share_of_versioned': round(s['affected_nofix'] / versioned, 4),
            'unknown_share_of_all': round(s['unknown'] / (versioned + s['unknown']), 4)}
    tables['m2_unfixed_tail'] = m2

w3 = {}
for minor, fixed in FIXED.items():
    name = f'w3techs-details-{minor}'
    if not (READ / (name + '.raw.gz')).exists():
        continue
    text = re.sub(r'<script.*?</script>|<style.*?</style>', '', body(name).decode('utf8', 'replace'), flags=re.S)
    text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', text)))
    part = text[text.find('Subversions of PHP ' + minor):]
    part = part[part.find('How to read the diagram'):]
    part = part[part.find('%') + 1:]  # past the worked example
    part = part[:part.find('W3Techs.com,')]
    rows = {int(v): (0.0 if pct is None else float(pct)) for v, pct, lt in
            [(m.group(1), m.group(2), m.group(3)) for m in re.finditer(
                r'Version ' + re.escape(minor) + r'\.(\d+) (?:([\d.]+)%|(less than 0\.1%))', part)]}
    stamp = re.search(r'W3Techs\.com, (\d+ \w+ \d{4})', text)
    w3[minor] = {'w3techs_date': stamp.group(1) if stamp else None, 'fixed_patch': fixed,
                 'share_at_or_above_fixed_pct': round(sum(p for v, p in rows.items() if v >= fixed), 1),
                 'listed_rows': len(rows), 'note': '"less than 0.1%" rows counted as 0'}
if w3:
    tables['m4_w3techs_within_minor'] = w3

pk = READ / 'packagist.json'
if pk.exists():
    monthly = json.loads(pk.read_text())['monthly']
    i = monthly['labels'].index('2026-09')
    month = {v: s[i] for v, s in monthly['values'].items()}
    total = sum(month.values())
    unfixed = sum(n for v, n in month.items() if tuple(map(int, v.split('.'))) <= (8, 1))
    tables['m5_packagist_sept_2026'] = {'installs': total, 'from_8_1_or_older': unfixed,
                                        'share': round(unfixed / total, 4), 'note': 'minor versions as Packagist publishes them'}

(READ / 'tables.json').write_text(json.dumps(tables, indent=1) + '\n')
print(json.dumps(tables, indent=1))
