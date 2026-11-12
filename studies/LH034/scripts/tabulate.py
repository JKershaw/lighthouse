#!/usr/bin/env python3
"""Tabulate LH034 offline from every read held: measures 1, 2 and 4 (brief.md, Measures).

Usage: tabulate.py. Writes data/tables.json and prints it. A day's value is from the earliest read holding it.
Release order and dates come from the latest read's dist/index.json. Measure 3 is taken only once day 30 is held.
The version table's 'unknown' key is counted with the requests that have no version, not as a line.
Amendment of 12 November 2026 (post hoc, brief.md): measure 1 is also given with in-line plain release
strings (vMAJOR.MINOR.PATCH) that the kept release list does not hold but that sort above the line's fixed
release by semantic version counted as at or above the fix; the series as written (unlisted dropped) is kept
beside it under its original key, for every day.
"""
from datetime import date
from pathlib import Path
import gzip
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DAYS = (1, 2, 7, 14, 30)
EVENTS = {'2026-10': (date(2026, 10, 21), {'22': 'v22.23.4', '24': 'v24.22.1', '26': 'v26.12.1'}),
          '2026-07': (date(2026, 7, 28), {'22': 'v22.23.2', '24': 'v24.18.1', '26': 'v26.5.1'})}
reads = sorted((ROOT / 'data').glob('read-*'))
# The newest read that holds the release list (amendment of 9 November 2026: nodejs.org's robots.txt
# disallows /dist/, so reads from 9 November do not fetch it; versions released after that list are
# outside `order` and are counted separately as unlisted, never silently as old).
index_read = [r for r in reads if (r / 'dist-index.raw.gz').exists()][-1]
index = json.loads(gzip.decompress((index_read / 'dist-index.raw.gz').read_bytes()))
order = {r['version']: n for n, r in enumerate(reversed(index))}  # higher is later
days = {}
for read in reads:
    for f in sorted(read.glob('day-*.raw.gz')):
        d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
        days.setdefault(d, (read.name, json.loads(gzip.decompress(f.read_bytes()))))


def line(v):
    return v[1:].split('.')[0]


PLAIN = re.compile(r'v(\d+)\.(\d+)\.(\d+)')


def semver(v):
    m = PLAIN.fullmatch(v)
    return tuple(int(x) for x in m.groups()) if m else None


def share_at_or_newer(versions, ln, fixed, unlisted_above=False):
    """As written: listed versions only. With unlisted_above (amendment of 12 November 2026), an unlisted
    plain release string in the line that sorts above `fixed` by semantic version is added as at or above;
    any other unlisted string (not plain, or not above the fix) stays out, as before."""
    in_line = {v: n for v, n in versions.items() if line(v) == ln and v in order}
    total = sum(in_line.values())
    newer = sum(n for v, n in in_line.items() if order[v] >= order[fixed])
    added = {}
    if unlisted_above:
        added = {v: n for v, n in versions.items() if line(v) == ln and v not in order
                 and semver(v) is not None and semver(v) > semver(fixed)}
        total += sum(added.values())
        newer += sum(added.values())
    return total, newer, (round(newer / total, 4) if total else None), added


tables = {'reads': [r.name for r in reads], 'days_held': [str(d) for d in sorted(days)], 'release_list_from': index_read.name}
tables['unlisted_versions_by_day'] = {}
for d, (rname, summary) in sorted(days.items()):
    vs = summary.get('version', {}) if isinstance(summary, dict) else {}
    unl = {v: n for v, n in vs.items() if v.startswith('v') and v not in order}
    if unl:
        tables['unlisted_versions_by_day'][str(d)] = unl
def mean_share(v, ks):
    xs = [v[k]['share'] for k in ks if k in v and v[k]['share'] is not None]
    return round(sum(xs) / len(xs), 4) if len(xs) == len(ks) else None


def measure(day0, fixed, unlisted_above=False):
    m = {}
    for d, (src, s) in sorted(days.items()):
        k = (d - day0).days
        if 0 <= k <= 30:
            for ln, fv in fixed.items():
                total, newer, sh, added = share_at_or_newer(s['version'], ln, fv, unlisted_above)
                row = {'day': str(d), 'line_downloads': total, 'at_or_newer': newer, 'share': sh, 'read': src}
                if unlisted_above:
                    row['unlisted_counted_at_or_above'] = added
                m.setdefault(ln, {})[k] = row
    return {'day0': str(day0), 'fixed': fixed, 'by_line': m,
            'first_day_at_half': {ln: next((k for k, x in sorted(v.items()) if x['share'] is not None and x['share'] >= 0.5), None) for ln, v in m.items()},
            'summary_days': {ln: {k: v[k]['share'] for k in DAYS if k in v} for ln, v in m.items()},
            # amendment 1 (30 October): S7 = mean of days 5 to 7, S30 = mean of days 28 to 30; None until all held
            'S7_S30': {ln: {'S7': mean_share(v, (5, 6, 7)), 'S30': mean_share(v, (28, 29, 30))} for ln, v in m.items()}}


for key, (day0, fixed) in EVENTS.items():
    tables[f'measure_{"1" if key == "2026-10" else "4"}_{key}'] = measure(day0, fixed)
# Amendment of 12 November 2026 (post hoc): measure 1 with unlisted in-line versions above the fix counted
# as at or above. The key above stays the measure as written; both are reported for every day.
m1, m1a = tables['measure_1_2026-10'], measure(*EVENTS['2026-10'], unlisted_above=True)
tables['measure_1_2026-10_amended_unlisted_above'] = m1a
tables['measure_1_rules_compared'] = {
    ln: {'days_identical': [k for k in sorted(v) if v[k]['share'] == m1a['by_line'][ln][k]['share']
                            and v[k]['line_downloads'] == m1a['by_line'][ln][k]['line_downloads']],
         'days_differing': {k: {'as_written': v[k]['share'], 'amended': m1a['by_line'][ln][k]['share']}
                            for k in sorted(v) if v[k]['share'] != m1a['by_line'][ln][k]['share']
                            or v[k]['line_downloads'] != m1a['by_line'][ln][k]['line_downloads']}}
    for ln, v in m1['by_line'].items()}
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
print('measure 1, rules compared:', json.dumps(tables['measure_1_rules_compared'], indent=1))
print('measure 2, from day -3:', json.dumps({d: {k: x[k] for k in ('unfixed_share', 'line_20_share', 'line_25_share', 'no_version_share_of_total')} for d, x in m2.items() if d >= '2026-10-18'}, indent=1))
