#!/usr/bin/env python3
"""LH034 record version 1.0: every figure the record states, from retained files only.

Usage: python3 -I studies/LH034/scripts/record_v1.py > studies/LH034/data/record_v1_output.txt
Writes studies/LH034/data/record_v1.json and prints a readable summary. Reads no source; standard library only.

It repeats scripts/tabulate.py's rules (tabulate.py runs on import and rewrites tables.json, so it is not
imported) and checks its measure 1 and 2 figures against data/tables.json:
- each day's value from the EARLIEST read holding it (brief, Reads);
- release order from the newest kept release list, read-2026-11-05T1414Z (amendment of 9 November);
- measure 1 both as written (listed versions only) and under the post hoc amendment of 12 November
  (unlisted plain vMAJOR.MINOR.PATCH keys in a fixed line above its fixed release counted at or above);
- the version table's 'unknown' key counted with requests that have no version.
Measure 3 (day 30), the re-read comparison of days 0 to 7, amendment 1's tests A and B, and the comparators
(studies/LH033/data/python_side.json and studies/LH033/data/record_v1.json) are new here.
"""
from datetime import date, timedelta
from pathlib import Path
from statistics import median
import gzip
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
LH033 = ROOT.parent / 'LH033' / 'data'
SUMMARY_DAYS = (1, 2, 7, 14, 30)
FIXED_LINES = ('22', '24', '26')
EVENTS = {'2026-10': (date(2026, 10, 21), {'22': 'v22.23.4', '24': 'v24.22.1', '26': 'v26.12.1'}),
          '2026-07': (date(2026, 7, 28), {'22': 'v22.23.2', '24': 'v24.18.1', '26': 'v26.5.1'})}
REREAD = 'read-2026-11-22T1416Z'
LIST_READ = 'read-2026-11-05T1414Z'
out = {}

# ---- inputs -------------------------------------------------------------------------------------------
reads = sorted(DATA.glob('read-*'))
lst = json.loads((DATA / LIST_READ / 'dist-index.derived.json').read_text())['extracted']
index = [dict(zip(lst['fields'], r)) for r in lst['releases']]
order = {r['version']: n for n, r in enumerate(reversed(index))}  # higher is later, as tabulate.py
days, copies = {}, {}
for read in reads:
    for f in sorted(read.glob('day-*.raw.gz')):
        d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
        copies.setdefault(d, []).append(f)
        days.setdefault(d, (read.name, json.loads(gzip.decompress(f.read_bytes()))))
out['inputs'] = {'reads': [r.name for r in reads], 'release_list_from': LIST_READ,
                 'release_list_read_utc': json.loads((DATA / LIST_READ / 'dist-index.derived.json').read_text())['read_utc'],
                 'days_held': len(days), 'first_day': str(min(days)), 'last_day': str(max(days))}

PLAIN = re.compile(r'v(\d+)\.(\d+)\.(\d+)')


def line(v):
    return v[1:].split('.')[0]


def semver(v):
    m = PLAIN.fullmatch(v)
    return tuple(int(x) for x in m.groups()) if m else None


def r1(x):
    return None if x is None else round(x * 100, 1)


# Release order within each fixed line, and whether it agrees with semantic version order
line_order = {}
for ln in FIXED_LINES:
    vs = sorted((v for v in order if line(v) == ln), key=lambda v: order[v])
    line_order[ln] = vs
out['release_list_checks'] = {ln: {'listed_in_line': len(vs),
                                   'list_order_matches_semver': [semver(v) for v in vs] == sorted(semver(v) for v in vs),
                                   'fixed_and_neighbours_newest_first': list(reversed(vs))[:8]}
                              for ln, vs in line_order.items()}


def split(versions, ln, fixed):
    """Partition a day's in-line keys: listed at/above, listed below (with list distance), unlisted plain above
    the fix, and other unlisted keys (pre-release, build suffix, or plain at or below the fix)."""
    fi = line_order[ln].index(fixed)
    listed_above, listed_below, unl_above, unl_other = 0, {}, {}, {}
    for v, n in versions.items():
        if not v.startswith('v') or line(v) != ln:
            continue
        if v in order:
            pos = line_order[ln].index(v)
            if pos >= fi:
                listed_above += n
            else:
                listed_below[v] = (fi - pos, n)
        elif semver(v) is not None and semver(v) > semver(fixed):
            unl_above[v] = n
        else:
            unl_other[v] = n
    return listed_above, listed_below, unl_above, unl_other


def share(versions, ln, fixed, amended):
    a, below, ua, _ = split(versions, ln, fixed)
    newer = a + (sum(ua.values()) if amended else 0)
    total = a + sum(n for _, n in below.values()) + (sum(ua.values()) if amended else 0)
    return total, newer, (newer / total if total else None)


# ---- measure 1 (and 4) ----------------------------------------------------------------------------------
def measure(day0, fixed, amended):
    by = {}
    for d, (src, s) in sorted(days.items()):
        k = (d - day0).days
        if 0 <= k <= 30:
            for ln, fv in fixed.items():
                t, n, sh = share(s['version'], ln, fv, amended)
                by.setdefault(ln, {})[k] = {'day': str(d), 'weekday': d.strftime('%a'), 'line_downloads': t,
                                            'at_or_above': n, 'share': sh, 'read': src}
    res = {}
    for ln, v in by.items():
        first = next((k for k in sorted(v) if v[k]['share'] is not None and v[k]['share'] >= 0.5), None)
        res[ln] = {'days_held': len(v),
                   'daily_pct': {k: r1(v[k]['share']) for k in sorted(v)},
                   'daily_line_downloads': {k: v[k]['line_downloads'] for k in sorted(v)},
                   'first_day_at_half': first,
                   'days_below_half_after_first': [k for k in sorted(v) if first is not None and k > first and v[k]['share'] < 0.5],
                   **{f'day{k}_pct': r1(v[k]['share']) for k in SUMMARY_DAYS if k in v},
                   'one_minus_day30_pct': r1(1 - v[30]['share']) if 30 in v else None,
                   'range_days_8_to_30_pct': [r1(min(v[k]['share'] for k in range(8, 31) if k in v)),
                                              r1(max(v[k]['share'] for k in range(8, 31) if k in v))] if 30 in v else None,
                   'range_days_13_to_20_pct': [r1(min(v[k]['share'] for k in range(13, 21) if k in v)),
                                               r1(max(v[k]['share'] for k in range(13, 21) if k in v))] if 20 in v else None,
                   'range_days_21_to_30_pct': [r1(min(v[k]['share'] for k in range(21, 31) if k in v)),
                                               r1(max(v[k]['share'] for k in range(21, 31) if k in v))] if 30 in v else None,
                   '_shares': {k: v[k]['share'] for k in sorted(v)}}
    return res


m1 = {'as_written': measure(*EVENTS['2026-10'], amended=False),
      'amended_post_hoc': measure(*EVENTS['2026-10'], amended=True)}
m4 = measure(*EVENTS['2026-07'], amended=False)
m4_amended = measure(*EVENTS['2026-07'], amended=True)

# Agreement with data/tables.json (written by tabulate.py)
tab = json.loads((DATA / 'tables.json').read_text())
mismatch = []
for rule, key in (('as_written', 'measure_1_2026-10'), ('amended_post_hoc', 'measure_1_2026-10_amended_unlisted_above'),
                  ('m4', 'measure_4_2026-07')):
    mine = m4 if rule == 'm4' else m1[rule]
    for ln, ser in tab[key]['by_line'].items():
        for k, row in ser.items():
            if row['share'] != round(mine[ln]['_shares'][int(k)], 4) or row['line_downloads'] != mine[ln]['daily_line_downloads'][int(k)]:
                mismatch.append([rule, ln, k])
out['check_against_tables_json'] = {'measure_1_and_4_mismatches': mismatch,
                                    'measure_4_rules_identical': all(m4[ln]['_shares'] == m4_amended[ln]['_shares'] for ln in m4)}

rules_differ = {ln: [k for k in range(31) if m1['as_written'][ln]['_shares'][k] != m1['amended_post_hoc'][ln]['_shares'][k]]
                for ln in FIXED_LINES}
out['measure_1'] = {rule: {ln: {k: v for k, v in x.items() if k != '_shares'} for ln, x in r.items()} for rule, r in m1.items()}
out['measure_1_days_rules_differ'] = rules_differ

# Unlisted versions in the fixed lines, days 0 to 30
unl = {}
other_unlisted = {}
for d, (src, s) in sorted(days.items()):
    k = (d - EVENTS['2026-10'][0]).days
    if 0 <= k <= 30:
        for ln, fv in EVENTS['2026-10'][1].items():
            a, below, ua, uo = split(s['version'], ln, fv)
            tot_am = a + sum(n for _, n in below.values()) + sum(ua.values())
            for v, n in ua.items():
                unl.setdefault(v, {})[k] = {'downloads': n, 'pct_of_line_amended': r1(n / tot_am)}
            if uo:
                other_unlisted.setdefault(str(k), {}).update(uo)
out['unlisted_above_fix_by_version'] = unl
out['unlisted_in_fixed_lines_not_plain_or_at_or_below_fix'] = other_unlisted
out['unlisted_outside_fixed_lines_day30'] = {v: n for v, n in days[EVENTS['2026-10'][0] + timedelta(30)][1]['version'].items()
                                            if v.startswith('v') and v not in order and line(v) not in FIXED_LINES}

# ---- measure 2 -------------------------------------------------------------------------------------------
m2 = {}
for d, (src, s) in sorted(days.items()):
    if d >= date(2026, 9, 23):
        v = {x: n for x, n in s['version'].items() if x != 'unknown'}
        att = sum(v.values())
        _unf = sum(n for x, n in v.items() if line(x) not in FIXED_LINES) / att
        m2[str(d)] = {'_unfixed_share': _unf, 'day_n': (d - EVENTS['2026-10'][0]).days, 'weekday': d.strftime('%a'), 'total': s['total'], 'attributed': att,
                      'unfixed_pct': r1(sum(n for x, n in v.items() if line(x) not in FIXED_LINES) / att),
                      'line20_pct': r1(sum(n for x, n in v.items() if line(x) == '20') / att),
                      'line27_pct': round(sum(n for x, n in v.items() if line(x) == '27') / att * 100, 2),
                      'line25_pct': r1(sum(n for x, n in v.items() if line(x) == '25') / att),
                      'no_version_pct_of_total': round((s['total'] - att) / s['total'] * 100, 3)}
for ds, row in m2.items():
    t = tab['measure_2_unfixed_tail'][ds]
    if round(row.pop('_unfixed_share'), 4) != t['unfixed_share']:
        mismatch.append(['m2', ds])


def rng(field, lo, hi):
    xs = [r[field] for r in m2.values() if lo <= r['day_n'] <= hi]
    return [min(xs), max(xs)]


out['measure_2'] = {'daily': m2,
                    'summary': {'late_september_23_to_30_unfixed_pct': rng('unfixed_pct', -28, -21),
                                'days_minus7_to_minus1_unfixed_pct': rng('unfixed_pct', -7, -1),
                                'days_0_to_7_unfixed_pct': rng('unfixed_pct', 0, 7),
                                'days_8_to_30_unfixed_pct': rng('unfixed_pct', 8, 30),
                                **{f'day{k}_unfixed_pct': next(r['unfixed_pct'] for r in m2.values() if r['day_n'] == k) for k in (0, 2, 7, 14, 30)},
                                'days_minus7_to_7_line20_pct': rng('line20_pct', -7, 7),
                                'days_minus7_to_7_line25_pct': rng('line25_pct', -7, 7),
                                'days_0_to_30_line20_pct': rng('line20_pct', 0, 30),
                                'days_0_to_30_line25_pct': rng('line25_pct', 0, 30),
                                'day30_line20_pct': next(r['line20_pct'] for r in m2.values() if r['day_n'] == 30),
                                'days_0_to_30_line27_pct_max': max(r['line27_pct'] for r in m2.values() if 0 <= r['day_n'] <= 30),
                                'day30_line27_pct': next(r['line27_pct'] for r in m2.values() if r['day_n'] == 30),
                                'day30_line25_pct': next(r['line25_pct'] for r in m2.values() if r['day_n'] == 30),
                                'max_no_version_pct_of_total_sep23_to_day30': max(r['no_version_pct_of_total'] for r in m2.values() if r['day_n'] <= 30),
                                'weekend_totals_days_0_to_30_millions': [round(min(r['total'] for r in m2.values() if 0 <= r['day_n'] <= 30 and r['weekday'] in ('Sat', 'Sun')) / 1e6, 1),
                                                                         round(max(r['total'] for r in m2.values() if 0 <= r['day_n'] <= 30 and r['weekday'] in ('Sat', 'Sun')) / 1e6, 1)],
                                'weekday_totals_days_0_to_30_millions': [round(min(r['total'] for r in m2.values() if 0 <= r['day_n'] <= 30 and r['weekday'] not in ('Sat', 'Sun')) / 1e6, 1),
                                                                         round(max(r['total'] for r in m2.values() if 0 <= r['day_n'] <= 30 and r['weekday'] not in ('Sat', 'Sun')) / 1e6, 1)],
                                'day30_total': next(r['total'] for r in m2.values() if r['day_n'] == 30),
                                'day30_attributed': next(r['attributed'] for r in m2.values() if r['day_n'] == 30)}}

# ---- measure 3, day 30 -------------------------------------------------------------------------------------
d30 = EVENTS['2026-10'][0] + timedelta(30)
vers30 = days[d30][1]['version']
m3 = {}
for ln, fv in EVENTS['2026-10'][1].items():
    a, below, ua, uo = split(vers30, ln, fv)
    groups = {'one_behind': sum(n for dist, n in below.values() if dist == 1),
              'two_to_four_behind': sum(n for dist, n in below.values() if 2 <= dist <= 4),
              'five_or_more_behind': sum(n for dist, n in below.values() if dist >= 5)}
    top = sorted(((n, v, dist) for v, (dist, n) in below.items()), reverse=True)[:3]
    res = {'unlisted_above_counted_at_or_above': ua, 'unlisted_excluded': uo,
           'one_behind_version': [v for v, (dist, _) in below.items() if dist == 1],
           'two_to_four_behind_versions': sorted((v for v, (dist, _) in below.items() if 2 <= dist <= 4), key=semver, reverse=True),
           'largest_below': [{'version': v, 'releases_behind': dist, 'downloads': n} for n, v, dist in top]}
    for rule, extra in (('as_written', 0), ('amended_post_hoc', sum(ua.values()))):
        tot = a + extra + sum(groups.values())
        res[rule] = {'line_downloads': tot, 'at_or_above_pct': r1((a + extra) / tot),
                     **{g + '_pct': r1(n / tot) for g, n in groups.items()},
                     'largest_below_pct': [r1(n / tot) for n, _, _ in top]}
    res['counts'] = {'listed_at_or_above': a, **groups}
    m3[ln] = res
out['measure_3_day30'] = m3

# ---- measure 4 ---------------------------------------------------------------------------------------------
out['measure_4_later_listed_releases_within_30_days'] = {
    ln: [[r['version'], r['date']] for r in index if line(r['version']) == ln
         and order[r['version']] > order[fv] and r['date'] <= str(EVENTS['2026-07'][0] + timedelta(30))]
    for ln, fv in EVENTS['2026-07'][1].items()}
out['measure_4'] = {ln: {k: v for k, v in x.items() if k not in ('_shares', 'daily_line_downloads')} for ln, x in m4.items()}
# Post hoc alignment by posting day kept from version 0.1: July's days 2, 3, 8, 15, 31 against October's 1, 2, 7, 14, 30.
# July day 31 (28 August) is outside the retained comparator days (28 July to 27 August), so it is not held.
out['measure_4_posting_day_alignment_post_hoc'] = {ln: {f'oct_day{k}': r1(x['_shares'].get(k + 1)) for k in (1, 2, 7, 14)}
                                                   for ln, x in m4.items()}

# ---- re-read of days 0 to 7 ---------------------------------------------------------------------------------
rr = {}
for f in sorted((DATA / REREAD).glob('day-*.raw.gz')):
    d = date(int(f.name[4:8]), int(f.name[8:10]), int(f.name[10:12]))
    first = copies[d][0]
    b1, b2 = gzip.decompress(first.read_bytes()), gzip.decompress(f.read_bytes())
    j1, j2 = json.loads(b1), json.loads(b2)
    log2 = {r.get('file'): r for r in json.loads((DATA / REREAD / 'read_log.json').read_text())}
    log1 = {r.get('file'): r for r in json.loads((first.parent / 'read_log.json').read_text())}
    rr[str(d)] = {'day_n': (d - EVENTS['2026-10'][0]).days, 'first_copy': first.parent.name,
                  'decompressed_bytes_identical': b1 == b2,
                  'sha256_decompressed_first': hashlib.sha256(b1).hexdigest()[:16],
                  'sha256_decompressed_reread': hashlib.sha256(b2).hexdigest()[:16],
                  'read_log_sha256_equal': log1.get(f.name, {}).get('sha256') == log2.get(f.name, {}).get('sha256'),
                  'total_equal': j1['total'] == j2['total'], 'version_map_equal': j1['version'] == j2['version'],
                  'max_share_difference_points': 0.0 if j1['version'] == j2['version'] else None}
out['reread_days_0_to_7'] = {'by_day': rr, 'all_identical': all(x['decompressed_bytes_identical'] and x['total_equal']
                                                                and x['version_map_equal'] for x in rr.values()),
                             'days_compared': len(rr)}

# ---- amendment 1: tests A and B ------------------------------------------------------------------------------
def S(sh, ks):
    return sum(sh[k] for k in ks) / len(ks)


node = {}
for rule, r in m1.items():
    node[rule] = {}
    for ln in FIXED_LINES:
        s7, s30 = S(r[ln]['_shares'], (5, 6, 7)), S(r[ln]['_shares'], (28, 29, 30))
        node[rule][ln] = {'S7': round(s7 * 100, 2), 'S30': round(s30 * 100, 2), 'L': round((s30 - s7) / s30, 4)}
lh033 = json.loads((LH033 / 'record_v1.json').read_text())
php_med = lh033['amendment2']['A']['php_median_L']
tests = {'php_median_L_from_LH033': php_med, 'php_L_by_branch_from_LH033': {b: v['L'] for b, v in lh033['amendment2']['php'].items()}}
for rule, t in node.items():
    mn = median(v['L'] for v in t.values())
    low = min(t['24']['S30'], t['26']['S30'])
    tests[rule] = {'by_line': t, 'node_median_L': mn,
                   'A_node_median_L_smaller_than_php': mn < php_med,
                   'B_line22_S30': t['22']['S30'], 'B_lower_of_24_26_S30': low,
                   'B_gap_points': round(low - t['22']['S30'], 2), 'B_holds_gap_over_5': low - t['22']['S30'] > 5}
# Agreement with LH033's record, which computed the Node.js side from tables.json
agree = {}
for rule in node:
    for ln, v in node[rule].items():
        agree[f'{rule}_{ln}'] = v == lh033['amendment2']['node'][rule][ln]
tests['agrees_with_LH033_record'] = agree
out['amendment_1_tests'] = tests

# ---- comparators ------------------------------------------------------------------------------------------------
py = json.loads((LH033 / 'python_side.json').read_text())
comp = {}
for k in SUMMARY_DAYS:
    fx = [v[str(k)] for v in py['four_security_fixes'].values()]
    php = [lh033['m1_summary'][b][f'day{k}'] for b in ('8.2', '8.3', '8.4', '8.5')]
    comp[k] = {'node_as_written_pct': {ln: m1['as_written'][ln][f'day{k}_pct'] for ln in FIXED_LINES},
               'node_amended_post_hoc_pct': {ln: m1['amended_post_hoc'][ln][f'day{k}_pct'] for ln in FIXED_LINES},
               'python_four_fixes_range_pct': [r1(min(fx)), r1(max(fx))],
               'python_median_of_37_pct': r1(py['median_of_project_medians_37'][str(k)]['median']),
               'php_censys_range_pct': [min(php), max(php)]}
def place(x, lo_hi):
    return 'below' if x < lo_hi[0] else 'above' if x > lo_hi[1] else 'within'


for k, c in comp.items():
    for rule in ('node_as_written_pct', 'node_amended_post_hoc_pct'):
        c[rule.replace('_pct', '_vs_python_range')] = {ln: place(x, c['python_four_fixes_range_pct']) for ln, x in c[rule].items()}
        c[rule.replace('_pct', '_vs_php_range')] = {ln: place(x, c['php_censys_range_pct']) for ln, x in c[rule].items()}
out['comparators'] = comp
out['check_against_tables_json']['all_mismatches'] = mismatch
# tables.json keeps shares to four decimals; rounding those again to one decimal of a per cent can differ by 0.1
# from rounding the exact share. Every figure in this record is rounded once, from the exact counts.
out['double_rounding_cases'] = {
    'measure_4_line22_day7': {'tables_json_share': tab['measure_4_2026-07']['by_line']['22']['7']['share'],
                              'exact_pct_rounded_once': out['measure_4']['22']['day7_pct']},
    'measure_1_amended_line26_day30': {'tables_json_share': tab['measure_1_2026-10_amended_unlisted_above']['by_line']['26']['30']['share'],
                                       'exact_pct_rounded_once': out['measure_1']['amended_post_hoc']['26']['day30_pct']}}

(DATA / 'record_v1.json').write_text(json.dumps(out, indent=1, default=str) + '\n')

# ---- readable summary --------------------------------------------------------------------------------------------
P = print
P('LH034 record_v1: figures from retained files;', out['inputs']['days_held'], 'days held,', out['inputs']['first_day'], 'to', out['inputs']['last_day'])
P('check against tables.json, mismatches:', mismatch, '| measure 4 identical under both rules:', out['check_against_tables_json']['measure_4_rules_identical'])
P('release list checks:', json.dumps(out['release_list_checks']))
P('\nMeasure 1, share at or above the fix, per cent, days 0 to 30')
for ln in FIXED_LINES:
    for rule in m1:
        P(f' line {ln} {rule:17s}', ' '.join(f'{x:5.1f}' for x in out['measure_1'][rule][ln]['daily_pct'].values()))
for rule in m1:
    for ln in FIXED_LINES:
        x = out['measure_1'][rule][ln]
        P(f' {rule:17s} line {ln}: first day at half {x["first_day_at_half"]}, below half after: {x["days_below_half_after_first"]};',
          ', '.join(f'd{k} {x[f"day{k}_pct"]}' for k in SUMMARY_DAYS), f'; 1 - d30 = {x["one_minus_day30_pct"]}; d8-30 range {x["range_days_8_to_30_pct"]}; d13-20 {x["range_days_13_to_20_pct"]}; d21-30 {x["range_days_21_to_30_pct"]}')
P(' days the rules differ:', rules_differ)
P(' unlisted above fix:', json.dumps({v: {k: x for k, x in d.items() if k in (21, 22, 25, 28, 29, 30)} for v, d in unl.items()}))
P(' other unlisted keys in fixed lines (excluded under both rules):', other_unlisted or 'none')
P(' unlisted outside fixed lines, day 30:', out['unlisted_outside_fixed_lines_day30'])
P('double rounding cases:', json.dumps(out['double_rounding_cases']))
P('\nMeasure 2 summary:', json.dumps(out['measure_2']['summary']))
P('\nMeasure 3, day 30:')
for ln, x in m3.items():
    P(f' line {ln}: one behind {x["one_behind_version"]}, two to four {x["two_to_four_behind_versions"]}, excluded {x["unlisted_excluded"]}')
    for rule in ('as_written', 'amended_post_hoc'):
        P(f'   {rule}: {json.dumps(x[rule])}')
    P('   largest below:', x['largest_below'])
P('\nMeasure 4 (July):')
for ln, x in out['measure_4'].items():
    P(f' line {ln}: first day at half {x["first_day_at_half"]};', ', '.join(f'd{k} {x.get(f"day{k}_pct")}' for k in SUMMARY_DAYS))
P(' later listed releases within July day 30:', out['measure_4_later_listed_releases_within_30_days'])
P(' posting-day alignment (post hoc):', json.dumps(out['measure_4_posting_day_alignment_post_hoc']))
P('\nRe-read of days 0 to 7: all identical =', out['reread_days_0_to_7']['all_identical'])
for d, x in rr.items():
    P(f' {d} (day {x["day_n"]}) vs {x["first_copy"]}: bytes {x["decompressed_bytes_identical"]}, log sha {x["read_log_sha256_equal"]}, total {x["total_equal"]}, versions {x["version_map_equal"]}')
P('\nAmendment 1 tests:')
P(' PHP median L (LH033):', php_med)
for rule in m1:
    t = tests[rule]
    P(f' {rule}: {json.dumps(t["by_line"])}; median L {t["node_median_L"]}; A (Node median L < PHP) {t["A_node_median_L_smaller_than_php"]};'
      f' B gap {t["B_gap_points"]} points, holds {t["B_holds_gap_over_5"]}')
P(' agrees with LH033 record:', agree)
P('\nComparators:')
for k, x in comp.items():
    P(f' day {k}: {json.dumps(x)}')
