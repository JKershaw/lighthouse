#!/usr/bin/env python3
"""LH040 tabulator: the brief's measures (studies/LH040/brief.md, protocol 0.1 with its amendment of
9 November 2026), computed from retained data only. No network request is made.

Written at the checkpoint (schedule row LH040-checkpoint), 10 November 2026, after read 1
(data/read-2026-11-09T1432Z/) had been collected but before its counts were tabulated. The writer
looked at the raw files to learn their shape (columns, duplicate dates, category values) and saw
1.107.0's day-0 row and the March rows while doing so; every choice marked CHOICE below was made
after that look, and is therefore made after some outcomes were seen. None changes the brief's
question, comparison set, measures, pre-set reading or missing-evidence rules.

Inputs:
  data/pre-brief-2026-11-08T1414Z/pypi_project_json.raw   L1, upload times (for h(R))
  data/read-<label>/Q1..Q7 *.raw, pypistats_overall.raw, readlog.csv

Outputs (tables/, overwritten on each run):
  daily_totals.csv, m1_day0.csv, m2_tail.csv, m2_tail_by_installer.csv, m2_tail_by_file_type.csv,
  m3_index.csv, m4_displaced.csv, m5_installer.csv, m5_installer_by_name.csv, m5_system.csv,
  m5_ci.csv, m6_march.csv,
  m7_depsdev.csv, checks.json, summary.txt

Replay: python3 -I studies/LH040/scripts/tabulate.py --read 2026-11-09T1432Z
"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median
import argparse
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
L1 = ROOT / 'data' / 'pre-brief-2026-11-08T1414Z' / 'pypi_project_json.raw'
OUT = ROOT / 'tables'

CASE = '1.107.0'
CASE_DAY0 = '2026-10-21'
# Brief, "Population and unit": the 17 comparison releases, fixed before any count.
COMPARISON = ['1.103.2', '1.104.0', '1.104.1', '1.104.2', '1.105.0', '1.105.1', '1.106.0', '1.106.1',
              '1.106.2', '1.106.3', '1.106.4', '1.106.5', '1.106.6', '1.108.0', '1.108.1', '1.108.2',
              '1.108.3']
DISPLACED = '1.106.2'
# Brief, "Clocks": upload 11:39:51 UTC (maintainers' report, R1, R2); primary end 13:23, with 13:20
# (Datadog, R8) and 12:47 (Aikido, R7) as alternatives.
CASE_UPLOAD = datetime(2026, 10, 21, 11, 39, 51, tzinfo=timezone.utc)
ENDS = {'13:23': datetime(2026, 10, 21, 13, 23, tzinfo=timezone.utc),
        '13:20': datetime(2026, 10, 21, 13, 20, tzinfo=timezone.utc),
        '12:47': datetime(2026, 10, 21, 12, 47, tzinfo=timezone.utc)}
PRIMARY = '13:23'
MARCH = ['1.82.7', '1.82.8']
MARCH_DAY0 = '2026-03-24'
MARCH_PYPI = 119000          # R5: "downloaded over 119k times"
STEPSECURITY = 49000         # R9: "about 49,000 times"
# CHOICE (measure 5): the brief names "pip, uv, poetry, pdm, bandersnatch and other mirror tools named
# by ClickPy, other names, none". Mirror tools are read as the names that mirror or proxy an index
# for others: bandersnatch, devpi, Nexus, Artifactory, z3c.pypimirror and pep381client. Every
# installer is also tabulated by its own name, so the grouping can be undone.
MIRRORS = {'bandersnatch', 'devpi', 'Nexus', 'Artifactory', 'z3c.pypimirror', 'pep381client'}
NAMED = ['pip', 'uv', 'poetry', 'pdm']
CI_KNOWN = {'pip', 'uv'}    # LH011's rule: the flag is read only for pip and uv


def group_installer(name):
    if name == '':
        return 'none'
    if name in NAMED:
        return name
    if name in MIRRORS:
        return 'mirror tools'
    return 'other names'


def final_key(v):
    """PEP 440 order for final releases N.N.N (all litellm finals in scope are of this form)."""
    return tuple(int(x) for x in v.split('.'))


def is_final(v):
    return all(p.isdigit() for p in v.split('.'))


def read_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))


def write_csv(name, rows, fields):
    with open(OUT / name, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in fields})


def r6(x):
    return '' if x is None else round(x, 6)


def uploads():
    """First upload time of every final release in L1, plus 1.107.0 (absent from L1) at 11:39:51."""
    d = json.loads(L1.read_bytes())
    up = {}
    for v, files in d['releases'].items():
        if files and is_final(v):
            up[v] = min(datetime.fromisoformat(f['upload_time_iso_8601'].replace('Z', '+00:00'))
                        for f in files)
    assert CASE not in up
    up[CASE] = CASE_UPLOAD
    return up


def hours_newest(rel, up, end):
    """h(R): hours of R's day 0 during which R was the highest final release on PyPI (brief, Clocks).
    1.107.0 is treated as on PyPI from CASE_UPLOAD to `end` and absent after; so 1.106.2 gets its two
    spells. CHOICE: the alternative end applies to 1.106.2's second spell too, so each window end is
    one consistent timeline for all 18 releases."""
    day0 = up[rel].replace(hour=0, minute=0, second=0, microsecond=0)
    day1 = day0 + timedelta(days=1)
    events = sorted(set([day0, day1] + [t for t in list(up.values()) + [end] if day0 < t < day1]))

    def highest_at(t):
        live = [v for v, u in up.items() if u <= t and not (v == CASE and t >= end)]
        return max(live, key=final_key)

    total = 0.0
    for a, b in zip(events, events[1:]):
        if highest_at(a) == rel:
            total += (b - a).total_seconds()
    return total / 3600


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--read', default='2026-11-09T1432Z')
    a = ap.parse_args()
    rd = ROOT / 'data' / ('read-' + a.read)
    OUT.mkdir(exist_ok=True)
    log = {r['name']: r for r in read_csv(rd / 'readlog.csv')}
    # Each retained body is checked against the SHA-256 its read logged.
    hashes = {n: hashlib.sha256((rd / (n + '.raw')).read_bytes()).hexdigest() == r['sha256']
              for n, r in log.items() if r['size'] not in ('', '0')}
    assert all(hashes.values()), hashes

    # ---- Daily totals. CHOICE: ClickPy's pypi_downloads_per_day returned more than one row for some
    # dates (unmerged parts of a summing table); Q1 did not sum, so rows for a date are summed here.
    tot_rows = defaultdict(list)
    for r in read_csv(rd / 'Q1_daily_totals.raw'):
        tot_rows[r['date']].append(int(r['count']))
    total = {d: sum(v) for d, v in tot_rows.items()}
    days = sorted(total)
    last_day = days[-1]

    # Gap rule (brief, Missing evidence; LH011's rule): no total, or total below half the median of
    # the seven days d-3..d+3, d included. CHOICE: at the ends of the series, the days held within
    # d-3..d+3 are used; a day with no total inside the series is a gap by the first clause.
    def all_days(start, end):
        s, e = datetime.fromisoformat(start), datetime.fromisoformat(end)
        return [(s + timedelta(days=i)).date().isoformat() for i in range((e - s).days + 1)]

    gap = {}
    for d in all_days(days[0], last_day):
        if d not in total:
            gap[d] = True
            continue
        dt = datetime.fromisoformat(d)
        around = [total[x] for x in ((dt + timedelta(days=k)).date().isoformat() for k in range(-3, 4))
                  if x in total]
        gap[d] = total[d] < 0.5 * median(around)

    ps = json.loads((rd / 'pypistats_overall.raw').read_bytes())
    pmap = {(x['category'], x['date']): x['downloads'] for x in ps['data']}
    trows, nbad, nchk = [], 0, 0
    for d in all_days(days[0], last_day):
        w, wo = pmap.get(('with_mirrors', d)), pmap.get(('without_mirrors', d))
        c = total.get(d)
        diff = (c / w - 1) if (c is not None and w) else None
        if '2026-10-14' <= d <= '2026-11-04':
            nchk += 1
            if diff is None or abs(diff) > 0.05:
                nbad += 1
        trows.append(dict(date=d, clickpy_total=c, clickpy_rows=len(tot_rows.get(d, [])),
                          pypistats_with_mirrors=w, pypistats_without_mirrors=wo,
                          clickpy_over_with_mirrors_minus_1=r6(diff), gap=gap.get(d, True)))
    write_csv('daily_totals.csv', trows, ['date', 'clickpy_total', 'clickpy_rows', 'pypistats_with_mirrors',
                                          'pypistats_without_mirrors', 'clickpy_over_with_mirrors_minus_1', 'gap'])

    # ---- Per-version daily counts.
    q2 = defaultdict(int)
    for r in read_csv(rd / 'Q2_daily_by_version_oct_nov.raw'):
        q2[(r['date'], r['version'])] += int(r['count'])
    up = uploads()
    day0 = {v: up[v].date().isoformat() for v in COMPARISON + [CASE]}
    assert day0[CASE] == CASE_DAY0

    def count0(v, d):
        """Brief, Missing evidence: on a non-gap day, no row is zero for a comparison release and
        'no record' (None) for 1.107.0."""
        if gap.get(d, True):
            return None, 'gap'
        if (d, v) in q2:
            return q2[(d, v)], 'row'
        return (None, 'no record') if v == CASE else (0, 'no row, zero')

    # ---- Measure 1.
    c0, c0_status = count0(CASE, CASE_DAY0)
    ft = defaultdict(int)
    ft_all = defaultdict(lambda: defaultdict(int))
    for r in read_csv(rd / 'Q7_file_type.raw'):
        ft_all[(r['date'], r['version'])][r['type']] += int(r['count'])
    ft = ft_all[(CASE_DAY0, CASE)]
    s0 = (c0 / total[CASE_DAY0]) if c0 is not None else None
    m1 = [dict(item='C0, fetches of 1.107.0 on 2026-10-21 (Q2)', value=c0),
          dict(item='status', value=c0_status),
          dict(item='of which bdist_wheel (Q7)', value=ft.get('bdist_wheel')),
          dict(item='of which sdist (Q7)', value=ft.get('sdist')),
          dict(item='Q7 sum', value=sum(ft.values())),
          dict(item='litellm total on 2026-10-21 (Q1, rows summed)', value=total[CASE_DAY0]),
          dict(item='S0, share of the day', value=r6(s0)),
          dict(item='StepSecurity (R9) "about 49,000"', value=STEPSECURITY),
          dict(item='C0 minus 49,000', value=(c0 - STEPSECURITY) if c0 is not None else None)]
    write_csv('m1_day0.csv', m1, ['item', 'value'])

    # ---- Measure 2, the tail to date: days 22 October to the last day held.
    q4 = defaultdict(lambda: defaultdict(int))
    for r in read_csv(rd / 'Q4_installer.raw'):
        q4[(r['date'], r['version'])][r['installer']] += int(r['count'])
    tail, tail_inst, tail_ft = [], defaultdict(int), defaultdict(int)
    tail_sum, tail_unknown_days = 0, []
    for d in all_days('2026-10-22', last_day):
        c, st = count0(CASE, d)
        inst = q4.get((d, CASE), {})
        ftd = ft_all.get((d, CASE), {})
        tail.append(dict(date=d, day=(datetime.fromisoformat(d) - datetime.fromisoformat(CASE_DAY0)).days,
                         count=c, status=st, litellm_total=total.get(d), gap=gap.get(d, True),
                         installer_sum=sum(inst.values()) if inst else '', file_type_sum=sum(ftd.values()) if ftd else ''))
        if c is None:
            tail_unknown_days.append(d)
        else:
            tail_sum += c
            for k, n in inst.items():
                tail_inst[k] += n
            for k, n in ftd.items():
                tail_ft[k] += n
    write_csv('m2_tail.csv', tail, ['date', 'day', 'count', 'status', 'litellm_total', 'gap',
                                    'installer_sum', 'file_type_sum'])
    write_csv('m2_tail_by_installer.csv',
              [dict(installer=k or '(none)', group=group_installer(k), count=n, share=r6(n / sum(tail_inst.values())))
               for k, n in sorted(tail_inst.items(), key=lambda x: -x[1])], ['installer', 'group', 'count', 'share'])
    write_csv('m2_tail_by_file_type.csv', [dict(type=k, count=n) for k, n in sorted(tail_ft.items())], ['type', 'count'])

    # ---- Measure 3.
    rels = COMPARISON + [CASE]
    m3, idx = [], {e: {} for e in ENDS}
    for v in rels:
        d = day0[v]
        c, st = count0(v, d)
        share = (c / total[d]) if c is not None else None
        row = dict(release=v, role='case' if v == CASE else 'comparison', upload_utc=up[v].isoformat(),
                   day0=d, count_day0=c, status=st, litellm_total_day0=total.get(d), S0=r6(share))
        for e, end in ENDS.items():
            h = (end - CASE_UPLOAD).total_seconds() / 3600 if v == CASE else hours_newest(v, up, end)
            i = share / (h / 24) if (share is not None and h > 0) else None
            row['h_' + e] = round(h, 4)
            row['I_' + e] = r6(i)
            idx[e][v] = i
        m3.append(row)
    summ3 = {}
    for e in ENDS:
        comp = [idx[e][v] for v in COMPARISON if idx[e][v] is not None]
        ci = idx[e][CASE]
        known = [(v, idx[e][v]) for v in rels if idx[e][v] is not None]
        rank = 1 + sum(1 for v, i in known if i > ci) if ci is not None else None
        summ3[e] = dict(n_comparison_known=len(comp), comparison_min=min(comp), comparison_max=max(comp),
                        comparison_median=median(comp), case_I=ci,
                        case_rank_of_known=rank, n_known=len(known),
                        ratio_to_median=(ci / median(comp)) if ci is not None else None,
                        within_range=(min(comp) <= ci <= max(comp)) if ci is not None else None,
                        above=(ci > max(comp)) if ci is not None else None,
                        below=(ci < min(comp)) if ci is not None else None)
        for row in m3:
            row['rank_' + e] = 1 + sum(1 for v, i in known if idx[e][row['release']] is not None
                                       and i > idx[e][row['release']])
    flags = [summ3[e] for e in ENDS]
    if any(s['case_I'] is None for s in flags) or min(s['n_comparison_known'] for s in flags) < 10:
        reading = 'none (fewer than ten known comparison shares, or the case unknown): reported as a list'
    elif all(s['within_range'] for s in flags):
        reading = 'travelled as an ordinary newest release did in its first hours'
    elif all(s['above'] for s in flags):
        reading = 'faster'
    elif all(s['below'] for s in flags):
        reading = 'slower'
    else:
        reading = "depends on the window's end"
    f3 = ['release', 'role', 'upload_utc', 'day0', 'count_day0', 'status', 'litellm_total_day0', 'S0']
    for e in ENDS:
        f3 += ['h_' + e, 'I_' + e, 'rank_' + e]
    write_csv('m3_index.csv', m3, f3)

    # ---- Measure 4 (tabulated; the brief schedules its reading for the record, after read 2).
    m4 = []
    for d in ['2026-10-20', '2026-10-21', '2026-10-22', '2026-10-23']:
        m4.append({'date': d, 'litellm_total': total.get(d), 'gap': gap.get(d, True),
                   '1.106.1': q2.get((d, '1.106.1'), 0), '1.106.2': q2.get((d, '1.106.2'), 0),
                   '1.107.0': q2.get((d, CASE))})
    write_csv('m4_displaced.csv', m4, ['date', 'litellm_total', 'gap', '1.106.1', '1.106.2', '1.107.0'])

    # ---- Measure 5: installer, system and CI shares on day 0.
    q5 = defaultdict(lambda: defaultdict(int))
    for r in read_csv(rd / 'Q5_system.raw'):
        q5[(r['date'], r['version'])][r['system']] += int(r['count'])
    q6 = defaultdict(lambda: defaultdict(int))
    for r in read_csv(rd / 'Q6_ci.raw'):
        q6[(r['date'], r['version'])][(r['installer'], r['ci'])] += int(r['count'])

    def shares(table, keyfn):
        out = {}
        for v in rels:
            cell = table.get((day0[v], v), {})
            n = sum(cell.values())
            g = defaultdict(int)
            for k, c in cell.items():
                g[keyfn(k)] += c
            out[v] = (n, {k: c / n for k, c in g.items()} if n else {}, dict(g))
        return out

    def share_table(name, sh, label):
        cats = sorted({k for v in rels for k in sh[v][1]})
        rows = []
        for k in cats:
            comp = [sh[v][1].get(k, 0.0) for v in COMPARISON if sh[v][0]]
            rows.append({label: k if k != '' else '(none)', 'case_count': sh[CASE][2].get(k, 0),
                         'case_share': r6(sh[CASE][1].get(k, 0.0)) if sh[CASE][0] else '',
                         'comparison_median': r6(median(comp)), 'comparison_min': r6(min(comp)),
                         'comparison_max': r6(max(comp)), 'n_comparison': len(comp),
                         'case_rank_high_of_18': 1 + sum(1 for x in comp if x > sh[CASE][1].get(k, 0.0))})
        write_csv(name, rows, [label, 'case_count', 'case_share', 'comparison_median', 'comparison_min',
                               'comparison_max', 'n_comparison', 'case_rank_high_of_18'])
        return rows

    inst_g = share_table('m5_installer.csv', shares(q4, group_installer), 'installer_group')
    inst_n = share_table('m5_installer_by_name.csv', shares(q4, lambda k: k), 'installer')
    sys_rows = share_table('m5_system.csv', shares(q5, lambda k: k), 'system')
    ci_rows = []
    for v in rels:
        cell = q6.get((day0[v], v), {})
        known = sum(c for (i, f), c in cell.items() if i in CI_KNOWN and f in ('true', 'false'))
        true = sum(c for (i, f), c in cell.items() if i in CI_KNOWN and f == 'true')
        allc = sum(cell.values())
        ci_rows.append(dict(release=v, day0=day0[v], q6_total=allc, pip_uv=known, pip_uv_ci_true=true,
                            ci_share=r6(true / known) if known else '', flag_not_known=allc - known,
                            flag_not_known_share=r6((allc - known) / allc) if allc else ''))
    comp_ci = [float(r['ci_share']) for r in ci_rows if r['release'] in COMPARISON and r['ci_share'] != '']
    case_ci = next(r for r in ci_rows if r['release'] == CASE)
    write_csv('m5_ci.csv', ci_rows, ['release', 'day0', 'q6_total', 'pip_uv', 'pip_uv_ci_true', 'ci_share',
                                     'flag_not_known', 'flag_not_known_share'])

    # ---- Measure 6: March calibration, 24 March to 30 April (the brief's March read window).
    q3 = defaultdict(int)
    for r in read_csv(rd / 'Q3_daily_by_version_march.raw'):
        q3[(r['date'], r['version'])] += int(r['count'])
    m6, m6_sum, m6_unknown = [], 0, []
    for d in all_days(MARCH_DAY0, '2026-04-30'):
        row = {'date': d, 'litellm_total': total.get(d), 'gap': gap.get(d, True)}
        s = 0
        for v in MARCH:
            if gap.get(d, True):
                row[v] = ''
            else:
                row[v] = q3.get((d, v), 'no record')
                s += q3.get((d, v), 0)
        if gap.get(d, True):
            m6_unknown.append(d)
        else:
            m6_sum += s
        m6.append(row)
    write_csv('m6_march.csv', m6, ['date', 'litellm_total', 'gap'] + MARCH)
    m6_day0 = sum(q3.get((MARCH_DAY0, v), 0) for v in MARCH)
    m6_pass = (MARCH_PYPI / 2 <= m6_sum <= MARCH_PYPI * 2)

    # ---- Measure 7: deps.dev.
    m7 = [dict(name=n, url=r['url'], utc_start=r['utc_start'], status=r['status'], size=r['size'])
          for n, r in log.items() if n.startswith('depsdev')]
    write_csv('m7_depsdev.csv', m7, ['name', 'url', 'utc_start', 'status', 'size'])

    # ---- Inconclusive checks (brief, "What would leave it inconclusive").
    checks = dict(read=a.read, last_day_held=last_day, bodies_match_logged_sha256=hashes,
                  case_row_on_day0=c0 is not None, day0_gap=gap[CASE_DAY0],
                  march_within_factor_two=m6_pass,
                  pypistats_days_checked=nchk, pypistats_days_over_5pc=nbad,
                  pypistats_rule_fails=nbad > nchk / 5,
                  comparison_known_day0=summ3[PRIMARY]['n_comparison_known'],
                  gap_days=[d for d, g in gap.items() if g],
                  measure3=summ3, measure3_reading=reading,
                  queries={n: r['status'] for n, r in log.items()})
    (OUT / 'checks.json').write_text(json.dumps(checks, indent=1, default=str) + '\n')

    # ---- Text summary.
    L = []
    p = L.append
    p('LH040 tabulation of read %s (last day held %s). Counts are fetches logged by PyPI as ClickPy holds them.' % (a.read, last_day))
    p('Retained bodies match their logged SHA-256: %s' % all(hashes.values()))
    p('Gap days in Q1 span: %s' % ([d for d, g in gap.items() if g] or 'none'))
    p('pypistats check, 14 Oct to 4 Nov: %d of %d days differ by more than 5%% (rule fails if more than a fifth).' % (nbad, nchk))
    p('')
    p('Measure 1. C0 = %s fetches of 1.107.0 on 2026-10-21 (%s); wheel %s, sdist %s; litellm total %s; S0 = %.4f.'
      % (c0, c0_status, ft.get('bdist_wheel'), ft.get('sdist'), total[CASE_DAY0], s0))
    p('  StepSecurity (R9): about 49,000; C0 minus 49,000 = %+d.' % (c0 - STEPSECURITY))
    p('')
    p('Measure 2, tail to date (22 Oct to %s): %d fetches over %d days; unknown days: %s.'
      % (last_day, tail_sum, len(tail), tail_unknown_days or 'none'))
    p('  by day: ' + ', '.join('%s:%s' % (r['date'][5:], r['count']) for r in tail))
    p('  by installer: ' + ', '.join('%s %d' % (k or '(none)', n) for k, n in sorted(tail_inst.items(), key=lambda x: -x[1])))
    p('  by file type: ' + ', '.join('%s %d' % kv for kv in sorted(tail_ft.items())))
    p('')
    p('Measure 3, I(R) = S0(R) / (h(R)/24):')
    for row in m3:
        p('  %-8s day0 %s count %8s S0 %.5f  h %s  I %s' % (
            row['release'], row['day0'], row['count_day0'], row['S0'],
            '/'.join('%.2f' % row['h_' + e] for e in ENDS), '/'.join('%.4f' % row['I_' + e] for e in ENDS)))
    for e, s in summ3.items():
        p('  end %s: case I %.4f, comparison range %.4f to %.4f, median %.4f, ratio %.2f, rank %d of %d'
          % (e, s['case_I'], s['comparison_min'], s['comparison_max'], s['comparison_median'],
             s['ratio_to_median'], s['case_rank_of_known'], s['n_known']))
    p('  pre-set reading: ' + reading)
    p('')
    p('Measure 4 (tabulated only; read in the record after read 2):')
    for r in m4:
        p('  %s 1.106.1 %s 1.106.2 %s 1.107.0 %s' % (r['date'], r['1.106.1'], r['1.106.2'], r['1.107.0']))
    p('')
    p('Measure 5, day-0 shares (case; comparison median, min to max):')
    for rows, lab in ((inst_g, 'installer_group'), (sys_rows, 'system')):
        for r in rows:
            p('  %-14s %-12s %s; %s, %s to %s' % (lab.split('_')[0], r[lab], r['case_share'], r['comparison_median'],
                                                r['comparison_min'], r['comparison_max']))
    p('  CI share (pip and uv only): case %s (%d of %d; flag not known %d of %d); comparison median %.4f, %.4f to %.4f'
      % (case_ci['ci_share'], case_ci['pip_uv_ci_true'], case_ci['pip_uv'], case_ci['flag_not_known'],
         case_ci['q6_total'], median(comp_ci), min(comp_ci), max(comp_ci)))
    p('')
    p('Measure 6: 1.82.7 and 1.82.8, 24 Mar to 30 Apr: %d fetches (day 0: %d); unknown days: %s; PyPI "over 119k"; within a factor of two: %s.'
      % (m6_sum, m6_day0, m6_unknown or 'none', m6_pass))
    p('')
    p('Measure 7: deps.dev: ' + '; '.join('%s %s' % (r['name'], r['status'][:60]) for r in m7))
    (OUT / 'summary.txt').write_text('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
