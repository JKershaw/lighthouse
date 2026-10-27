#!/usr/bin/env python3
"""Tabulate LH034 offline from every read held: measures 1, 2 and 4 (brief.md, Measures).

Usage: tabulate.py. Writes data/tables.json and prints it. A day's value is from the earliest read holding it.
Release order and dates come from the latest read's dist/index.json. Measure 3 is taken only once day 30 is held.
The version table's 'unknown' key is counted with the requests that have no version, not as a line.
"""
from datetime import date
from pathlib import Path
import gzip
import json

ROOT = Path(__file__).resolve().parents[1]
DAYS = (1, 2, 7, 14, 30)
EVENTS = {'2026-10': (date(2026, 10, 21), {'22': 'v22.23.4', '24': 'v24.22.1', '26': 'v26.12.1'}),
          '2026-07': (date(2026, 7, 28), {'22': 'v22.23.2', '24': 'v24.18.1', '26': 'v26.5.1'})}
reads = sorted((ROOT / 'data').glob('read-*'))
index = json.loads(gzip.decompress((reads[-1] / 'dist-index.raw.gz').read_bytes()))
order = {r['version']: n for n, r in enumerate(reversed(index))}  # higher is later
days = {}
for read in reads:
    for f in sorted(read.glob('day-*.raw.gz')):
        d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
        days.setdefault(d, (read.name, json.loads(gzip.decompress(f.read_bytes()))))


def line(v):
    return v[1:].split('.')[0]


def share_at_or_newer(versions, ln, fixed):
    in_line = {v: n for v, n in versions.items() if line(v) == ln and v in order}
    total = sum(in_line.values())
    newer = sum(n for v, n in in_line.items() if order[v] >= order[fixed])
    return total, newer, (round(newer / total, 4) if total else None)


tables = {'reads': [r.name for r in reads], 'days_held': [str(d) for d in sorted(days)]}
for key, (day0, fixed) in EVENTS.items():
    m = {}
    for d, (src, s) in sorted(days.items()):
        k = (d - day0).days
        if 0 <= k <= 30:
            for ln, fv in fixed.items():
                total, newer, sh = share_at_or_newer(s['version'], ln, fv)
                m.setdefault(ln, {})[k] = {'day': str(d), 'line_downloads': total, 'at_or_newer': newer, 'share': sh, 'read': src}
    tables[f'measure_{"1" if key == "2026-10" else "4"}_{key}'] = {
        'day0': str(day0), 'fixed': fixed, 'by_line': m,
        'first_day_at_half': {ln: next((k for k, x in sorted(v.items()) if x['share'] is not None and x['share'] >= 0.5), None) for ln, v in m.items()},
        'summary_days': {ln: {k: v[k]['share'] for k in DAYS if k in v} for ln, v in m.items()}}
m2 = {}
for d, (src, s) in sorted(days.items()):
    if d >= date(2026, 9, 23):
        v = {x: n for x, n in s['version'].items() if x != 'unknown'}  # 'unknown' counts as no version
        attributed = sum(v.values())
        unfixed = sum(n for x, n in v.items() if line(x) not in ('22', '24', '26'))
        m2[str(d)] = {'attributed': attributed, 'total': s['total'], 'unfixed_share': round(unfixed / attributed, 4),
                      'line_20_share': round(sum(n for x, n in v.items() if line(x) == '20') / attributed, 4),
                      'line_25_share': round(sum(n for x, n in v.items() if line(x) == '25') / attributed, 4),
                      'no_version_share_of_total': round((s['total'] - attributed) / s['total'], 4), 'read': src}
tables['measure_2_unfixed_tail'] = m2
(ROOT / 'data' / 'tables.json').write_text(json.dumps(tables, indent=1) + '\n')
print(json.dumps({k: v for k, v in tables.items() if k != 'measure_2_unfixed_tail'}, indent=1)[:6000])
print('measure 2, from day -3:', json.dumps({d: {k: x[k] for k in ('unfixed_share', 'line_20_share', 'line_25_share', 'no_version_share_of_total')} for d, x in m2.items() if d >= '2026-10-18'}, indent=1))
