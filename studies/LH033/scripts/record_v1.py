#!/usr/bin/env python3
"""LH033 record version 1.0: every figure the record states, from retained reads and tables only.

Usage: python3 -I studies/LH033/scripts/record_v1.py
Writes studies/LH033/data/record_v1.json and prints it. Reads no source.

- Measures 1 and 2: each completed day 0 to 30 from the EARLIEST read holding it (brief, Reads),
  with every later read compared field for field (revisions listed).
- Measure 3: branch_versions in the read holding day 30 (2026-11-21T1414Z).
- Measure 4: W3Techs details at each read (tables.json of each read) and the monthly points of
  1 October and 1 November 2026 from the history page of the day-30 read.
- Measure 5 and the Python comparators: from the retained tables named in the brief.
- Amendment 2 tests A and B, PHP side here; Node.js side from studies/LH034/data/tables.json
  (measure 1 as written, and the post hoc amended rule of 12 November beside it).
"""
from datetime import date
from pathlib import Path
from statistics import median
import gzip
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DAY0 = date(2026, 10, 21)
FIXED = {'8.2': 35, '8.3': 36, '8.4': 27, '8.5': 12}
D30_READ = 'read-2026-11-21T1414Z'
out = {}

reads = sorted(p for p in DATA.iterdir() if p.name.startswith('read-') and (p / 'censys.raw.gz').exists())


def snap(p):
    return json.loads(gzip.decompress((p / 'censys.raw.gz').read_bytes()))['snapshot']


# Measures 1 and 2, earliest read per completed day, with revisions
bh, hist, revisions = {}, {}, []
for p in reads:
    s, rd = snap(p), date.fromisoformat(p.name[5:15])
    for r in s['branch_history']:
        if date.fromisoformat(r['day']) >= rd or r['branch'] not in FIXED:
            continue
        k, v = (r['branch'], r['day']), (r['patched'], r['targets'])
        if k not in bh:
            bh[k] = (v, p.name)
        elif bh[k][0] != v:
            revisions.append({'branch': k[0], 'day': k[1], 'first': bh[k], 'later': [v, p.name]})
    day_status = {}
    for r in s['history']:
        if date.fromisoformat(r['day']) < rd:
            day_status.setdefault(r['day'], {})[r['status']] = r['targets']
    for d, st in day_status.items():
        if d not in hist:
            hist[d] = (st, p.name)
        elif hist[d][0] != st:
            revisions.append({'history_day': d, 'first': hist[d], 'later': [st, p.name]})
out['reads_used'] = [p.name for p in reads]
out['revisions'] = revisions

m1 = {}
for (b, d), ((pt, tg), rn) in sorted(bh.items()):
    n = (date.fromisoformat(d) - DAY0).days
    if 0 <= n <= 30:
        m1.setdefault(b, {})[n] = {'day': d, 'patched': pt, 'targets': tg, 'share': pt / tg, 'read': rn}
summ = {}
for b, v in m1.items():
    summ[b] = {'days_held': len(v),
               'first_day_at_half': next((n for n in sorted(v) if v[n]['share'] >= 0.5), None),
               **{f'day{n}': round(v[n]['share'] * 100, 1) for n in (1, 2, 7, 14, 30)},
               'not_patched_day30_pct': round((1 - v[30]['share']) * 100, 1),
               'targets_day30': v[30]['targets']}
out['m1_summary'] = summ

m2 = {}
for d, (st, rn) in sorted(hist.items()):
    n = (date.fromisoformat(d) - DAY0).days
    if 0 <= n <= 30:
        ver = st['affected'] + st['affected_nofix'] + st['patched']
        m2[n] = {'day': d, 'nofix': st['affected_nofix'], 'versioned': ver,
                 'nofix_pct_of_versioned': round(st['affected_nofix'] / ver * 100, 1),
                 'unknown_pct_of_all': round(st['unknown'] / (ver + st['unknown']) * 100, 1), 'read': rn}
out['m2_unfixed_tail'] = {n: m2[n] for n in (0, 1, 2, 7, 14, 28, 29, 30)}

# Measure 3, distance behind the fix, on the read holding day 30
s30 = snap(DATA / D30_READ)
out['m3_snapshot_refreshed_at'] = s30['refreshed_at']
m3 = {}
for b, fx in FIXED.items():
    rows = [(int(r['version'].split('.')[2]), r['targets']) for r in s30['branch_versions']
            if r['branch'] == b and r['version'].count('.') == 2 and r['version'].split('.')[2].isdigit()]
    other = [r for r in s30['branch_versions'] if r['branch'] == b and not (
        r['version'].count('.') == 2 and r['version'].split('.')[2].isdigit())]
    tot = sum(t for _, t in rows) + sum(r['targets'] for r in other)
    g = {'at_or_above_fixed': sum(t for p, t in rows if p >= fx),
         'one_behind': sum(t for p, t in rows if p == fx - 1),
         'two_to_four_behind': sum(t for p, t in rows if fx - 4 <= p <= fx - 2),
         'five_or_more_behind': sum(t for p, t in rows if p <= fx - 5),
         'unparsed_version_rows': sum(r['targets'] for r in other)}
    top = sorted(((t, p) for p, t in rows if p < fx), reverse=True)[:3]
    m3[b] = {'version_reporting_in_branch_versions': tot,
             'branch_history_day30_targets': m1[b][30]['targets'],
             **{k: v for k, v in g.items()},
             **{k + '_pct': round(v / tot * 100, 1) for k, v in g.items()},
             'largest_below_fixed': [{'version': f'{b}.{p}', 'targets': t, 'pct': round(t / tot * 100, 1)} for t, p in top],
             'above_fixed_versions': sorted(f'{b}.{p}' for p, t in rows if p > fx)}
out['m3_distance_behind'] = m3

# Measure 4, W3Techs at each read, and monthly points from the day-30 history pages
m4 = {}
for p in sorted(DATA.glob('read-*/tables.json')):
    t = json.loads(p.read_text()).get('m4_w3techs_within_minor')
    if t:
        m4[p.parent.name] = {b: (x['w3techs_date'], x['share_at_or_above_fixed_pct']) for b, x in t.items()}
out['m4_w3techs_by_read'] = m4
monthly = {}
for b, fx in FIXED.items():
    h = json.loads((DATA / D30_READ / f'w3techs-history_details-{b}.derived.json').read_text())['extracted']['history']
    for col in ('1 Oct 2026', '1 Nov 2026'):
        listed = {}
        for label, vals in h['rows']:
            v = label.split()[-1]
            if v.startswith(b + '.') and v.split('.')[2].isdigit() and int(v.split('.')[2]) >= fx and vals.get(col):
                listed[v] = 0.0 if vals[col].startswith('<') else float(vals[col].rstrip('%'))  # '<0.1%' as 0, as measure 4
        monthly.setdefault(b, {})[col] = {'listed_at_or_above_fixed': listed,
                                          'sum_pct': round(sum(listed.values()), 1) if listed else None}
out['m4_w3techs_monthly'] = monthly

# Measure 5 and the Python comparators
out['m5_packagist'] = json.loads((DATA / 'read-2026-10-25T0855Z' / 'tables.json').read_text()).get('m5_packagist_sept_2026')
py = json.loads((DATA / 'python_side.json').read_text())
out['python'] = py

# Amendment 2
def S(series, days):
    return sum(series[n] for n in days) / len(days)


php = {b: {n: v['share'] for n, v in m1[b].items()} for b in FIXED}
php_t = {}
for b, ser in php.items():
    s7, s30 = S(ser, (5, 6, 7)), S(ser, (28, 29, 30))
    php_t[b] = {'S7': round(s7 * 100, 2), 'S30': round(s30 * 100, 2), 'L': round((s30 - s7) / s30, 4),
                'rise_day23_to_30_pts': round((ser[30] - ser[23]) * 100, 2)}
node = json.loads((ROOT.parent / 'LH034/data/tables.json').read_text())
node_t = {}
for rule, key in (('as_written', 'measure_1_2026-10'), ('amended_post_hoc', 'measure_1_2026-10_amended_unlisted_above')):
    node_t[rule] = {}
    for ln, ser in node[key]['by_line'].items():
        sh = {int(n): v['at_or_newer'] / v['line_downloads'] for n, v in ser.items()}
        s7, s30 = S(sh, (5, 6, 7)), S(sh, (28, 29, 30))
        node_t[rule][ln] = {'S7': round(s7 * 100, 2), 'S30': round(s30 * 100, 2), 'L': round((s30 - s7) / s30, 4)}
mphp = median(v['L'] for v in php_t.values())
A = {'php_median_L': mphp,
     'php_branches_rising_ge_1pt_day23_to_30': sum(v['rise_day23_to_30_pts'] >= 1 for v in php_t.values())}
for rule, t in node_t.items():
    mn = median(v['L'] for v in t.values())
    A[rule] = {'node_median_L': mn, 'php_median_L_greater': mphp > mn}
A['php_rise_part_holds'] = A['php_branches_rising_ge_1pt_day23_to_30'] >= 3
older, newer = max(php_t['8.2']['S30'], php_t['8.3']['S30']), min(php_t['8.4']['S30'], php_t['8.5']['S30'])
B = {'php': {'higher_of_8.2_8.3': older, 'lower_of_8.4_8.5': newer, 'gap_pts': round(newer - older, 2),
             'holds': newer - older > 5}}
for rule, t in node_t.items():
    low = min(t['24']['S30'], t['26']['S30'])
    B['node_' + rule] = {'line22': t['22']['S30'], 'lower_of_24_26': low,
                         'gap_pts': round(low - t['22']['S30'], 2), 'holds': low - t['22']['S30'] > 5}
out['amendment2'] = {'php': php_t, 'node': node_t, 'A': A, 'B': B}

(DATA / 'record_v1.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps(out, indent=1, default=str))
