#!/usr/bin/env python3
"""LH049 tabulator: measures 1 to 7 of studies/LH049/brief.md (protocol 0.1), as written, from the retained reads.

Usage (offline; no network request, no key, standard-library Python 3):
  python3 -I studies/LH049/scripts/tabulate.py            prints the tables as text
  python3 -I studies/LH049/scripts/tabulate.py --json     prints the same results as JSON

Written at the checkpoint of 17 November 2026, after the counts were seen. It implements the brief's rules and
changes none of them. Where the brief can be read more than one way, the reading taken is commented here
("READING:") and listed under "Method" and "Limits" in LH049.md.

Extended on 24 November 2026 for record version 1.0, after the weekly read, changing no rule: measure 2 now reports
V(23 Nov) from the held window ending 23 November (the brief's tail), and four descriptive lines were added (each
read's package daily totals summed over its stated window beside the point total; each per-version answer's key
count against the registry's listed versions; the package's daily totals 17 to 23 November; 13.3.0's time entry).

Rules implemented, by the brief's section:
  Clocks       A read's per-version window W(t) is held only if point_before and point_after both answered 200,
               state the same start, end and total, end - start = 6 days, and the per-version totals of the
               versions answer sum to that total. Otherwise that read's window is unknown.
  Day counts   V(t) is 13.3.0's total in the held window ending t. d(t) = 0 for t before 9 November.
               d(9) = V(9); d(t) = V(t) - V(t-1) for 10..15; d(16) = V(16) - V(15) + d(9).
               If W(9) is not held, d(9) is bounded: at most V of the earliest window held, at least
               V(15) - V(16). A difference that needs a window not held, or a window with no 13.3.0 key, is
               unknown. Sums that can still be formed are reported as sums.
  Missing      200 per-version answer without key 13.3.0: "no record", not zero. Unknown is never no.
  Measures     1 day-0 count and S0; 2 d(10..16) and their sum (V(23) waits for the weekly read);
               3 I = S0 / (75.1/1440); 4 the package's 9 November beside the median and range of 2..16
               November; 5 comparison release, only if one qualifies; 6 Socket's "order of ten" (4 to 31);
               7 registry and OSV state at each read.
"""
from datetime import date, timedelta
from hashlib import sha256
from pathlib import Path
import gzip
import json
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
CASE = '13.3.0'
DAY0 = date(2026, 11, 9)
MINUTES = 75.1                       # brief: 00:09:50.630 to 01:24:58 UTC (Socket's end, as reported)
SOCKET_RANGE = (4, 31)               # brief, measure 6
TABULATOR = '17 November 2026, extended 24 November 2026'
COMPARISON_FROM, COMPARISON_TO = '2026-11-10T00:00', '2026-11-16T23:59'


def d(s):
    return date.fromisoformat(s)


def body(read_dir, name):
    return json.loads(gzip.decompress((read_dir / (name + '.raw.gz')).read_bytes()))


def final_release(v):
    return '-' not in v


def vkey(v):
    return tuple(int(x) for x in v.split('.'))


def load_reads():
    reads = []
    for read_dir in sorted(DATA.glob('read-*')):
        log = {r['name']: r for r in json.loads((read_dir / 'read_log.json').read_text())}
        r = {'label': read_dir.name[len('read-'):], 'dir': read_dir, 'log': log, 'hash_checks': []}
        for name, row in log.items():
            ok200 = row.get('status') == 200 and row.get('file')
            r[name + '_ok'] = bool(ok200)
            if ok200:
                raw = gzip.decompress((read_dir / row['file']).read_bytes())
                # The log hashes the bytes received; a body with emails withheld cannot match by design.
                if row.get('emails_withheld', 0) == 0:
                    r['hash_checks'].append((name, sha256(raw).hexdigest() == row['sha256']))
        reads.append(r)
    return reads


def window_check(r):
    """The Clocks rule for one read. Returns (t or None, reasons failed, details)."""
    fails, det = [], {}
    if not (r['point_before_ok'] and r['point_after_ok'] and r['versions_ok']):
        return None, ['a point or versions request did not answer 200'], det
    pb, pa = body(r['dir'], 'point_before'), body(r['dir'], 'point_after')
    vs = body(r['dir'], 'versions')['downloads']
    det = {'before': (pb['start'], pb['end'], pb['downloads']), 'after': (pa['start'], pa['end'], pa['downloads']),
           'versions_sum': sum(vs.values()), 'versions_n': len(vs), 'case_key': CASE in vs,
           'case_value': vs.get(CASE)}
    if (pb['start'], pb['end'], pb['downloads']) != (pa['start'], pa['end'], pa['downloads']):
        fails.append('points disagree')
    if d(pb['end']) - d(pb['start']) != timedelta(days=6):
        fails.append('stated window is not seven days')
    if sum(vs.values()) != pb['downloads']:
        fails.append('per-version sum %d != point total %d (difference %+d)'
                     % (sum(vs.values()), pb['downloads'], sum(vs.values()) - pb['downloads']))
    return (None if fails else d(pb['end'])), fails, det


def main():
    as_json = '--json' in sys.argv
    reads = load_reads()
    out = {'reads': [], 'checks': {}}

    # ---- Clocks: which windows are held, and V(t) for 13.3.0
    V = {}             # t -> int (held, key present) or 'no record' (held, key absent)
    raw_case = {}      # t (stated end, held or not) -> 13.3.0 value as answered, for the record's observation only
    for r in reads:
        t, fails, det = window_check(r)
        if det:
            raw_case[det['before'][1]] = det['case_value'] if det['case_key'] else 'no record'
        if t is not None:
            if t in V:
                sys.exit('two held windows end on %s; the brief gives no rule for this' % t)
            V[t] = det['case_value'] if det['case_key'] else 'no record'
        out['reads'].append({'label': r['label'], 'stated_window': det.get('before', [None, None])[:2],
                             'point_total': det.get('before', [None, None, None])[2],
                             'versions_sum': det.get('versions_sum'), 'held': t is not None,
                             'window_end_t': str(t) if t else None, 'fails': fails,
                             'case_13_3_0': (det['case_value'] if det.get('case_key') else 'no record') if det else None,
                             'hash_checks_ok': all(ok for _, ok in r['hash_checks']),
                             'hash_checks_n': len(r['hash_checks'])})

    def Vn(t):
        """V(t) as a number: 0 before day 0 (brief), the held value, or None (unknown or no record)."""
        if t < DAY0:
            return 0
        v = V.get(t)
        return v if isinstance(v, int) else None

    def dd(t):
        """d(t) by the brief's formulas; None where it needs a window not held or with no record."""
        if t < DAY0:
            return 0
        if t == DAY0:
            return Vn(DAY0)
        a, b = Vn(t), Vn(t - timedelta(days=1))
        if a is None or b is None:
            return None
        if t <= DAY0 + timedelta(days=6):            # 10..15 November: d(t-7) = 0
            return a - b
        if t == DAY0 + timedelta(days=7):            # 16 November
            d9 = dd(DAY0)
            return None if d9 is None else a - b + d9
        return None                                  # beyond 16 November the brief gives d only via the weekly read

    days = [DAY0 + timedelta(days=k) for k in range(8)]          # 9..16 November
    dcounts = {str(t): dd(t) for t in days}

    # d(9) exact, or the brief's bound
    d9 = dcounts[str(DAY0)]
    held_ends = sorted(t for t, v in V.items() if isinstance(v, int))
    if d9 is not None:
        d9_desc = {'exact': d9}
    else:
        # READING: "if the window ending 9 November is never read" is taken to cover a read whose window the
        # Clocks rule leaves unknown, since the missing-evidence rules make such a window unknown with every
        # difference that uses it. "The earliest window held" is the earliest held window with a 13.3.0 value.
        upper = V[held_ends[0]] if held_ends else None
        v15, v16 = Vn(date(2026, 11, 15)), Vn(date(2026, 11, 16))
        lower = (v15 - v16) if (v15 is not None and v16 is not None) else None
        d9_desc = {'exact': None, 'upper': upper, 'upper_from_window_ending': str(held_ends[0]) if held_ends else None,
                   'lower': lower,
                   'lower_note': None if lower is not None else
                   'V(15 Nov) - V(16 Nov) cannot be formed: W(16 Nov) %s' %
                   ('has no record of 13.3.0' if V.get(date(2026, 11, 16)) == 'no record' else 'is not held')}

    # Sums that can still be formed (brief: "the sums that can still be formed are reported as sums").
    # A held V(t) with t in 12..15 equals d(t-6..t) restricted to days >= 9 November, since d = 0 before.
    sums = []
    for t in held_ends:
        if t <= DAY0 + timedelta(days=6):
            first = max(DAY0, t - timedelta(days=6))
            sums.append({'days': '%s to %s' % (first, t), 'sum': V[t], 'from': 'V(%s)' % t})

    # ---- request 4: the package's daily totals, from every read's range answer
    by_day = {}
    for r in reads:
        if not r.get('range_ok'):
            continue
        rng = body(r['dir'], 'range')
        read_date = r['label'][:10]
        for row in rng['downloads']:
            by_day.setdefault(row['day'], []).append((r['label'], row['downloads'], row['day'] == read_date))
    # READING: a read's answer for its own UTC date is the day not yet loaded (E7) and is set aside; for every
    # other day the newest read's value is used, and any disagreement between reads is reported.
    pkg, pkg_disagree = {}, {}
    for day, vals in sorted(by_day.items()):
        loaded = [(lab, n) for lab, n, own in vals if not own]
        if not loaded:
            continue
        pkg[day] = loaded[-1][1]
        if len({n for _, n in loaded}) > 1:
            pkg_disagree[day] = loaded

    p9 = pkg.get(str(DAY0))
    # brief: a day answered as zero for the whole package when the per-version window shows fetches is unknown
    if p9 == 0:
        p9 = None

    # ---- measure 1 and 3
    def share(x):
        return None if (x is None or not p9) else x / p9
    frac = MINUTES / 1440
    m1 = {'d9': d9_desc, 'package_9_nov': p9}
    if d9 is not None:
        m1['S0'] = share(d9)
        m3 = {'I': share(d9) / frac}
    else:
        m1['S0_upper'] = share(d9_desc['upper'])
        m1['S0_lower'] = share(d9_desc['lower'])
        m3 = {'I_upper': None if m1['S0_upper'] is None else m1['S0_upper'] / frac,
              'I_lower': None if m1['S0_lower'] is None else m1['S0_lower'] / frac}
    m3['minutes_share'] = frac

    # ---- measure 2
    after = {k: v for k, v in dcounts.items() if k != str(DAY0)}
    m2 = {'d': after, 'sum_10_to_16': sum(after.values()) if all(v is not None for v in after.values()) else None,
          'any_day_above_zero': any(v for v in after.values() if v is not None) or None,
          'V_23_nov': V.get(date(2026, 11, 23), 'not held')}
    if m2['any_day_above_zero'] is None and all(v is not None for v in after.values()):
        m2['any_day_above_zero'] = False

    # ---- measure 4: other days 2..16 November that the reads hold
    other = {k: v for k, v in pkg.items() if '2026-11-02' <= k <= '2026-11-16' and k != str(DAY0)}
    vals = list(other.values())
    m4 = {'package_9_nov': p9, 'other_days_n': len(vals), 'median': statistics.median(vals) if vals else None,
          'min': min(vals) if vals else None, 'max': max(vals) if vals else None, 'd9': d9_desc,
          'other_days': other}

    # ---- measure 5: a comparison release qualifies?
    qualifying = set()
    for r in reads:
        if not r.get('packument_ok'):
            continue
        for v, ts in body(r['dir'], 'packument').get('time', {}).items():
            if v in ('created', 'modified', CASE) or not final_release(v):
                continue
            try:
                if vkey(v) > (13, 2, 0) and COMPARISON_FROM <= ts[:16] <= COMPARISON_TO:
                    qualifying.add((v, ts))
            except ValueError:
                continue
    m5 = {'qualifying': sorted(qualifying), 'made': bool(qualifying)}
    if qualifying:
        m5['note'] = 'a release qualified; this tabulator does not yet derive d0(R): extend before use'

    # ---- measure 6
    lo, hi = SOCKET_RANGE
    if d9 is not None:
        m6 = {'reading': 'consistent' if lo <= d9 <= hi else 'not consistent', 'difference_from_ten': d9 - 10}
    else:
        u, l_ = d9_desc['upper'], d9_desc['lower']
        floor = l_ if l_ is not None else 0     # counts cannot be negative; the brief's own lower bound is noted
        if u is not None and lo <= floor and u <= hi:
            m6 = {'reading': 'consistent (whole bound inside 4 to 31)'}
        elif u is not None and (u < lo or floor > hi):
            m6 = {'reading': 'not consistent (whole bound outside 4 to 31)'}
        else:
            m6 = {'reading': 'not made: the bound on d(9 Nov) is not wholly inside or outside 4 to 31',
                  'bound_used': [floor, u], 'brief_lower_formed': l_ is not None}

    # ---- measure 7: registry and OSV at each read
    m7, prev_versions = [], None
    for r in reads:
        row = {'label': r['label']}
        if r.get('packument_ok'):
            p = body(r['dir'], 'packument')
            t = p.get('time', {})
            listed = set(p.get('versions', {}))
            row.update(listed=CASE in listed, time_kept=CASE in t, time=t.get(CASE), latest=p.get('dist-tags', {}).get('latest'),
                       deprecated=sorted(v for v, x in p.get('versions', {}).items() if x.get('deprecated')),
                       unpublished='unpublished' in t, modified=t.get('modified'), n_listed=len(listed),
                       new_since_last=sorted(listed - prev_versions) if prev_versions is not None else None,
                       gone_since_last=sorted(prev_versions - listed) if prev_versions is not None else None)
            prev_versions = listed
        else:
            row['registry'] = 'unavailable'
        if r.get('osv_ok'):
            vulns = body(r['dir'], 'osv').get('vulns', [])
            row['osv'] = [{'id': x['id'], 'aliases': x.get('aliases'), 'modified': x.get('modified'),
                           'withdrawn': x.get('withdrawn'),
                           'sources': sorted(s.get('source', '') for s in
                                             x.get('database_specific', {}).get('malicious-packages-origins', []))}
                          for x in vulns]
        else:
            row['osv'] = 'unavailable'
        m7.append(row)

    # ---- descriptive lines added 24 November 2026 (no measure uses them)
    extra = []
    for r in reads:
        e = {'label': r['label']}
        if r['point_before_ok'] and r.get('range_ok'):
            pb = body(r['dir'], 'point_before')
            e['range_sum_over_stated_window'] = sum(row['downloads'] for row in body(r['dir'], 'range')['downloads']
                                                    if pb['start'] <= row['day'] <= pb['end'])
            e['point_total'] = pb['downloads']
        if r['versions_ok'] and r.get('packument_ok'):
            vs = body(r['dir'], 'versions')['downloads']
            listed = set(body(r['dir'], 'packument').get('versions', {}))
            e.update(keys=len(vs), zero_values=sum(1 for x in vs.values() if x == 0), min_value=min(vs.values()),
                     listed=len(listed), listed_without_key=len(listed - set(vs)),
                     keys_not_listed=sorted(set(vs) - listed))
        extra.append(e)
    late = {k: v for k, v in pkg.items() if '2026-11-17' <= k <= '2026-11-23'}
    late_desc = {'n': len(late), 'min': min(late.values()) if late else None,
                 'max': max(late.values()) if late else None, 'sum': sum(late.values()) if late else None}

    out.update(extra_per_read=extra, package_daily_17_to_23=late_desc)
    out.update(V={str(k): v for k, v in sorted(V.items())}, raw_case_by_stated_end=raw_case, d=dcounts,
               sums_formed=sums, package_daily=pkg, package_daily_disagreements=pkg_disagree,
               m1=m1, m2=m2, m3=m3, m4=m4, m5=m5, m6=m6, m7=m7)

    if as_json:
        print(json.dumps(out, indent=1, default=str))
        return

    P = print
    P('LH049 tabulation (brief protocol 0.1; tabulator %s), %d retained reads' % (TABULATOR, len(reads)))
    P('\nClocks: windows held')
    for r in out['reads']:
        P('  %-16s stated %s..%s point %s per-version sum %s  13.3.0 %s  %s  bodies hash-checked %d ok=%s'
          % (r['label'], r['stated_window'][0], r['stated_window'][1], r['point_total'], r['versions_sum'],
             r['case_13_3_0'], 'HELD W(%s)' % r['window_end_t'] if r['held'] else 'UNKNOWN: ' + '; '.join(r['fails']),
             r['hash_checks_n'], r['hash_checks_ok']))
    P('\nV(t), held windows only: ' + ', '.join('%s=%s' % (k, v) for k, v in out['V'].items()))
    P('\nDay counts d(t): ' + ', '.join('%s=%s' % (k[5:], 'unknown' if v is None else v) for k, v in dcounts.items()))
    P('Sums still formed: ' + ('; '.join('d(%s) = %s [%s]' % (s['days'], s['sum'], s['from']) for s in sums) or 'none'))
    P('\nMeasure 1: d(9 Nov) %s; package total 9 Nov = %s' % (json.dumps(d9_desc), p9))
    P('  S0 ' + ('= %.4f' % m1['S0'] if 'S0' in m1 else 'upper %s, lower %s' % (
        'unknown' if m1['S0_upper'] is None else '%.4f' % m1['S0_upper'],
        'unknown' if m1['S0_lower'] is None else '%.4f' % m1['S0_lower'])))
    P('Measure 2: d(10..16) = %s; sum %s; any day above zero: %s; V(23 Nov) = %s'
      % (', '.join('%s=%s' % (k[5:], 'unknown' if v is None else v) for k, v in after.items()),
         'unknown' if m2['sum_10_to_16'] is None else m2['sum_10_to_16'],
         'unknown' if m2['any_day_above_zero'] is None else m2['any_day_above_zero'], m2['V_23_nov']))
    P('Measure 3: minutes share %.5f; I %s' % (frac, 'I' in m3 and '%.3f' % m3['I'] or 'upper %s, lower %s' % (
        'unknown' if m3['I_upper'] is None else '%.3f' % m3['I_upper'],
        'unknown' if m3['I_lower'] is None else '%.3f' % m3['I_lower'])))
    P('Measure 4: package 9 Nov %s; other days 2..16 Nov held: n=%d, median %s, range %s to %s'
      % (p9, m4['other_days_n'], m4['median'], m4['min'], m4['max']))
    P('  daily totals: ' + ', '.join('%s=%s' % (k[5:], v) for k, v in pkg.items()))
    P('  disagreements between reads on a loaded day: %s' % (pkg_disagree or 'none'))
    P('  package daily totals 17..23 Nov (description, not a measure): n=%s, min %s, max %s, sum %s'
      % (late_desc['n'], late_desc['min'], late_desc['max'], late_desc['sum']))
    P('Measure 5: qualifying comparison releases: %s -> %s' % (m5['qualifying'] or 'none', 'made' if m5['made'] else 'not made'))
    P('Measure 6: %s' % json.dumps(m6))
    P('Measure 7:')
    for row in m7:
        P('  %s listed=%s time_kept=%s time=%s latest=%s deprecated=%s unpublished=%s modified=%s n_listed=%s new=%s gone=%s'
          % (row['label'], row.get('listed'), row.get('time_kept'), row.get('time'), row.get('latest'), row.get('deprecated'),
             row.get('unpublished'), row.get('modified'), row.get('n_listed'), row.get('new_since_last'),
             row.get('gone_since_last')))
        for o in row['osv'] if isinstance(row['osv'], list) else []:
            P('      osv %s %s modified %s withdrawn %s sources %s' % (o['id'], o['aliases'], o['modified'],
                                                                     o['withdrawn'], o['sources']))
    P('\nOutside the protocol (observation only, not used by any measure): 13.3.0 as answered in every '
      'per-version window by stated end: ' + ', '.join('%s=%s' % (k[5:], v) for k, v in sorted(raw_case.items())))
    P('\nDescriptive checks (added 24 November 2026; no measure uses them):')
    for e in extra:
        P('  %s package daily totals summed over the stated window %s, point total %s; per-version keys %s '
          '(zero values %s, smallest %s); registry lists %s, listed without a key %s; keys not listed %s'
          % (e['label'], e.get('range_sum_over_stated_window'), e.get('point_total'), e.get('keys'),
             e.get('zero_values'), e.get('min_value'), e.get('listed'), e.get('listed_without_key'),
             e.get('keys_not_listed')))


if __name__ == '__main__':
    main()
