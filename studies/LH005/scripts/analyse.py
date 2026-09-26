#!/usr/bin/env python3
"""LH005: every derived table and headline figure, computed from the retained reads in data/.
Usage: python3 analyse.py   (run after the three collect_*.py scripts)"""
import collections, datetime, statistics
from common import read_csv, write_csv

D = datetime.date.fromisoformat
REL = {'1.27.0': D('2026-04-02'), '1.26.0': D('2026-01-24')}   # UTC publication days (PyPI JSON API)
WIN0, WIN1 = D('2026-03-26'), D('2026-04-22')
MIRRORS_PYPISTATS = {'bandersnatch', 'z3c.pypimirror', 'Artifactory', 'devpi'}  # pypistats.org/faqs
figures = []


def fig(name, value, denominator='', basis=''):
    figures.append(dict(figure=name, value=value, denominator=denominator, basis=basis))


def installer_class(name):
    if name == 'uv': return 'uv'
    if name == 'pip': return 'pip'
    if name in ('poetry', 'pdm', 'pipenv', 'hatch'): return 'poetry, pdm and other project managers'
    if name in ('bandersnatch', 'devpi', 'Artifactory', 'Nexus', 'z3c.pypimirror'): return 'mirror or proxy (bandersnatch, devpi, Artifactory, Nexus)'
    if name == 'Bazel': return 'Bazel'
    if name == 'Browser': return 'Browser'
    if name == 'requests': return 'requests'
    if name == '': return 'none recorded'
    return 'other named (Homebrew, OS, setuptools, conda, and a "pip" with an invisible character)'


def pct(a, b):
    return round(100 * a / b, 2) if b else ''


def day_iter(a, b):
    while a <= b:
        yield a
        a += datetime.timedelta(days=1)


# ---------- ClickPy internal consistency and cross-copy agreement ----------
cp_total = {r['date']: int(r['downloads']) for r in read_csv('clickpy_mcp_daily_total.csv')}
by_ver = collections.defaultdict(collections.Counter)
for f in ('clickpy_mcp_daily_by_version_window.csv', 'clickpy_mcp_daily_by_version_contrast.csv',
          'clickpy_mcp_daily_by_version_pepy_overlap.csv'):
    for r in read_csv(f):
        by_ver[r['date']][r['version']] += int(r['downloads'])
inst_win = read_csv('clickpy_mcp_daily_by_installer_window.csv')
inst_con = read_csv('clickpy_mcp_daily_by_installer_contrast.csv')
ci_win = read_csv('clickpy_mcp_daily_by_ci_window.csv')
ci_con = read_csv('clickpy_mcp_daily_by_ci_contrast.csv')
inst_sum, inst_nomirror, inst_nomirror_noname, ci_sum = (collections.Counter() for _ in range(4))
for r in inst_win + inst_con:
    inst_sum[r['date']] += int(r['downloads'])
    if r['installer'] not in MIRRORS_PYPISTATS:
        inst_nomirror[r['date']] += int(r['downloads'])
        if r['installer'] != '':
            inst_nomirror_noname[r['date']] += int(r['downloads'])
for r in ci_win + ci_con:
    ci_sum[r['date']] += int(r['downloads'])
ps = {(r['date'], r['category']): int(r['downloads']) for r in read_csv('pypistats_mcp_overall.csv')}
ps_days = sorted({d for d, _ in ps})
fig('pypistats mcp overall series: first and last day held', f"{ps_days[0]} to {ps_days[-1]}", f'{len(ps_days)} days',
    'pypistats_mcp_overall.csv, read 2026-09-26')

rows = []
for day in sorted(set(cp_total) | set(by_ver)):
    rows.append(dict(date=day, clickpy_per_day_table=cp_total.get(day, ''),
                     clickpy_sum_by_version_table=sum(by_ver[day].values()) if day in by_ver else '',
                     clickpy_sum_installer_table=inst_sum.get(day, ''),
                     clickpy_per_download_table=ci_sum.get(day, ''),
                     clickpy_installer_table_excluding_pypistats_mirror_list=inst_nomirror.get(day, ''),
                     clickpy_installer_table_excluding_mirror_list_and_no_installer=inst_nomirror_noname.get(day, ''),
                     pypistats_with_mirrors=ps.get((day, 'with_mirrors'), ''),
                     pypistats_without_mirrors=ps.get((day, 'without_mirrors'), '')))
write_csv('cross_copy_daily_totals.csv', rows)


def compare(name, pairs, basis):
    pairs = [(a, b) for a, b in pairs if a != '' and b != '']
    if not pairs: return
    diffs = [(a - b) / b for a, b in pairs]
    equal = sum(1 for a, b in pairs if a == b)
    worst = max(pairs, key=lambda p: abs(p[0] - p[1]) / p[1])
    fig(f'{name}: days compared', len(pairs), '', basis)
    fig(f'{name}: days identical', equal, f'{len(pairs)} days', basis)
    fig(f'{name}: median absolute daily difference, per cent', round(100 * statistics.median(abs(x) for x in diffs), 3),
        f'{len(pairs)} days', basis)
    fig(f'{name}: largest absolute daily difference, per cent', round(100 * max(abs(x) for x in diffs), 3),
        f'{worst[0]} against {worst[1]}', basis)
    sa, sb = sum(a for a, _ in pairs), sum(b for _, b in pairs)
    fig(f'{name}: summed over the days compared', f'{sa} against {sb} ({pct(sa - sb, sb)} per cent)', f'{len(pairs)} days', basis)


in_win = [r for r in rows if WIN0 <= D(r['date']) <= WIN1]
compare('ClickPy per-day table against pypistats with mirrors, LH002 window days both hold',
        [(r['clickpy_per_day_table'], r['pypistats_with_mirrors']) for r in in_win], 'cross_copy_daily_totals.csv')
compare('ClickPy per-day table against pypistats with mirrors, every day both hold',
        [(r['clickpy_per_day_table'], r['pypistats_with_mirrors']) for r in rows], 'cross_copy_daily_totals.csv')
compare('ClickPy installer table less pypistats mirror list, against pypistats without mirrors, window and margin days both hold',
        [(r['clickpy_installer_table_excluding_pypistats_mirror_list'], r['pypistats_without_mirrors']) for r in rows
         if D(r['date']) >= D('2026-03-19')], 'cross_copy_daily_totals.csv')
compare('ClickPy installer table less pypistats mirror list and less downloads with no installer name, against pypistats without mirrors',
        [(r['clickpy_installer_table_excluding_mirror_list_and_no_installer'], r['pypistats_without_mirrors']) for r in rows
         if D(r['date']) >= D('2026-03-19')], 'cross_copy_daily_totals.csv')
same = [r for r in rows if r['pypistats_without_mirrors'] != '' and r['clickpy_sum_installer_table'] != ''
        and r['clickpy_sum_installer_table'] == r['pypistats_with_mirrors']]
fig('days on which ClickPy and pypistats agree on the total and ClickPy less mirrors and no-installer rows equals pypistats without mirrors exactly',
    sum(1 for r in same if r['clickpy_installer_table_excluding_mirror_list_and_no_installer'] == r['pypistats_without_mirrors']),
    f'{len(same)} days with identical totals, 29 March to 29 April', 'cross_copy_daily_totals.csv')
compare('ClickPy by-version table against ClickPy per-day table, window and margin',
        [(r['clickpy_sum_by_version_table'], r['clickpy_per_day_table']) for r in rows
         if D('2026-03-19') <= D(r['date']) <= D('2026-04-29')], 'cross_copy_daily_totals.csv')
compare('ClickPy per-download table against ClickPy by-version table, window and margin',
        [(r['clickpy_per_download_table'], r['clickpy_sum_by_version_table']) for r in rows
         if D('2026-03-19') <= D(r['date']) <= D('2026-04-29')], 'cross_copy_daily_totals.csv')
compare('ClickPy installer table against ClickPy by-version table, window and margin',
        [(r['clickpy_sum_installer_table'], r['clickpy_sum_by_version_table']) for r in rows
         if D('2026-03-19') <= D(r['date']) <= D('2026-04-29')], 'cross_copy_daily_totals.csv')
mirror_days = [r for r in rows if r['pypistats_with_mirrors'] != '' and D(r['date']) <= D('2026-09-25')]
mw = sum(r['pypistats_with_mirrors'] for r in mirror_days); mo = sum(r['pypistats_without_mirrors'] for r in mirror_days)
fig('pypistats mcp: mirror downloads (with minus without), share of with-mirrors total', pct(mw - mo, mw),
    f'{mw - mo} of {mw} over {len(mirror_days)} days', 'pypistats_mcp_overall.csv')

# pepy against ClickPy, per version and day, on the days pepy's anonymous API holds
pe = collections.defaultdict(collections.Counter)
for r in read_csv('pepy_mcp_daily_by_version.csv'):
    pe[r['date']][r['version']] += int(r['downloads'])
prow, vd_equal, vd_total = [], 0, 0
for day in sorted(pe):
    c = by_ver.get(day, collections.Counter())
    for v in set(pe[day]) | set(c):
        vd_total += 1
        vd_equal += pe[day][v] == c[v]
    prow.append(dict(date=day, pepy_total=sum(pe[day].values()), clickpy_total=sum(c.values()),
                     pepy_1_28_1=pe[day]['1.28.1'], clickpy_1_28_1=c['1.28.1'],
                     pypistats_with_mirrors=ps.get((day, 'with_mirrors'), '')))
write_csv('cross_copy_pepy_clickpy.csv', prow)
fig('pepy anonymous v2 API for mcp: days held', f"{min(pe)} to {max(pe)}", f'{len(pe)} days', 'pepy_mcp_daily_by_version.csv')
fig('pepy against ClickPy: version-days with identical counts', vd_equal, f'{vd_total} version-days', 'cross_copy_pepy_clickpy.csv')
compare('pepy daily total against ClickPy by-version daily total, days pepy holds',
        [(r['pepy_total'], r['clickpy_total']) for r in prow], 'cross_copy_pepy_clickpy.csv')
compare('pepy daily total against pypistats with mirrors, days pepy holds',
        [(r['pepy_total'], r['pypistats_with_mirrors']) for r in prow], 'cross_copy_pepy_clickpy.csv')

# ---------- The taken side: mcp by version across the window ----------
MAIN = ['1.27.0', '1.26.0', '1.25.0', '1.23.3']
share_rows = []
for day in day_iter(D('2026-03-19'), D('2026-04-29')):
    c = by_ver[day.isoformat()]; t = sum(c.values())
    r = dict(date=day.isoformat(), weekday=day.strftime('%a'), day_after_release=(day - REL['1.27.0']).days, all_versions=t)
    for v in MAIN: r[v] = c[v]
    r['other_versions'] = t - sum(c[v] for v in MAIN)
    for v in MAIN: r[f'share_{v}'] = round(c[v] / t, 4)
    r['share_other'] = round(r['other_versions'] / t, 4)
    share_rows.append(r)
write_csv('mcp_daily_by_version_share.csv', share_rows)

def thresholds(series_name, daily, release, rel_version, first_day, last_day):
    """daily: {date: Counter(version -> downloads)}; first day a version appears and days to shares."""
    out = []
    appear = next((d for d in day_iter(first_day, last_day) if daily[d.isoformat()][rel_version] > 0), None)
    out.append(dict(series=series_name, release=rel_version, measure='first UTC day with any download',
                    date=appear.isoformat() if appear else '', day_after_release=(appear - release).days if appear else '',
                    release_downloads=daily[appear.isoformat()][rel_version] if appear else '',
                    denominator=sum(daily[appear.isoformat()].values()) if appear else '',
                    share_pct=pct(daily[appear.isoformat()][rel_version], sum(daily[appear.isoformat()].values())) if appear else ''))
    for thr in (10, 25, 50):
        hit = None
        for d in day_iter(release, last_day):
            c = daily[d.isoformat()]; t = sum(c.values())
            if t and 100 * c[rel_version] / t >= thr:
                hit = d; break
        c = daily[hit.isoformat()] if hit else collections.Counter()
        out.append(dict(series=series_name, release=rel_version, measure=f'first UTC day with share at or above {thr} per cent',
                        date=hit.isoformat() if hit else 'not reached', day_after_release=(hit - release).days if hit else '',
                        release_downloads=c[rel_version] if hit else '', denominator=sum(c.values()) if hit else '',
                        share_pct=pct(c[rel_version], sum(c.values())) if hit else ''))
    # peak share within the observed span
    best = max(day_iter(release, last_day), key=lambda d: (by := daily[d.isoformat()])[rel_version] / max(1, sum(by.values())))
    c = daily[best.isoformat()]
    out.append(dict(series=series_name, release=rel_version, measure='highest daily share in the span read',
                    date=best.isoformat(), day_after_release=(best - release).days, release_downloads=c[rel_version],
                    denominator=sum(c.values()), share_pct=pct(c[rel_version], sum(c.values()))))
    return out

thr_rows = thresholds('all installers', by_ver, REL['1.27.0'], '1.27.0', D('2026-03-19'), D('2026-04-29'))
thr_rows += thresholds('all installers', by_ver, REL['1.26.0'], '1.26.0', D('2026-01-17'), D('2026-02-27'))

# by installer class, from the installer table
def class_daily(rows_):
    out = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in rows_:
        out[installer_class(r['installer'])][r['date']][r['version_class']] += int(r['downloads'])
    return out
cls_win, cls_con = class_daily(inst_win), class_daily(inst_con)
for cls in sorted(cls_win):
    thr_rows += thresholds(f'installer class: {cls}', cls_win[cls], REL['1.27.0'], '1.27.0', D('2026-03-19'), D('2026-04-29'))
for cls in sorted(cls_con):
    thr_rows += thresholds(f'installer class: {cls}', cls_con[cls], REL['1.26.0'], '1.26.0', D('2026-01-17'), D('2026-02-27'))
# by CI flag, from the per-download table
ci_daily = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for r in ci_win:
    ci_daily[r['ci']][r['date']][r['version_class']] += int(r['downloads'])
for flag in sorted(ci_daily):
    thr_rows += thresholds(f'CI flag: {flag}', ci_daily[flag], REL['1.27.0'], '1.27.0', D('2026-03-19'), D('2026-04-29'))
ci_daily_con = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for r in ci_con:
    ci_daily_con[r['ci']][r['date']][r['version_class']] += int(r['downloads'])
for flag in sorted(ci_daily_con):
    thr_rows += thresholds(f'CI flag: {flag}', ci_daily_con[flag], REL['1.26.0'], '1.26.0', D('2026-01-17'), D('2026-02-27'))
write_csv('uptake_thresholds.csv', thr_rows)

# installer classes and file types, summed over the window days after the release day and over the whole window
def window_sum(rows_, key, first, last):
    agg = collections.defaultdict(collections.Counter)
    for r in rows_:
        if first <= D(r['date']) <= last:
            agg[key(r)]['all'] += int(r['downloads'])
            agg[key(r)][r['version_class']] += int(r['downloads'])
    return agg
after0, after1 = D('2026-04-03'), WIN1   # whole UTC days after the release day, inside the LH002 window
cls_rows = []
ft_win = read_csv('clickpy_mcp_daily_by_file_type_window.csv')
for label, key, src in (('installer class', lambda r: installer_class(r['installer']), inst_win),
                        ('installer name', lambda r: r['installer'] or '(none recorded)', inst_win),
                        ('file type (file-type table)', lambda r: r['type'], ft_win),
                        ('file type as the installer table gives it (unreliable: type is outside that table\'s key)', lambda r: r['type'], inst_win)):
    whole = window_sum(src, key, WIN0, WIN1)
    after = window_sum(src, key, after0, after1)
    tw = sum(v['all'] for v in whole.values()); ta = sum(v['all'] for v in after.values()); t127 = sum(v['1.27.0'] for v in after.values())
    for k in sorted(whole, key=lambda k: -whole[k]['all']):
        cls_rows.append({'grouping': label, 'group': k, 'downloads_whole_window': whole[k]['all'],
                         'share_of_window_pct': pct(whole[k]['all'], tw),
                         'downloads_3_to_22_april': after[k]['all'], '1.27.0_downloads_3_to_22_april': after[k]['1.27.0'],
                         'share_of_group_that_was_1.27.0_pct': pct(after[k]['1.27.0'], after[k]['all']),
                         'share_of_all_1.27.0_downloads_pct': pct(after[k]['1.27.0'], t127),
                         'denominator_window': tw, 'denominator_3_to_22_april': ta, 'denominator_1.27.0': t127})
write_csv('mcp_installer_and_file_type_window.csv', cls_rows)
wtot = sum(r['downloads_whole_window'] for r in cls_rows if r['grouping'] == 'installer class')
fig('mcp downloads in the LH002 window (ClickPy installer table)', wtot, '28 UTC days', 'mcp_installer_and_file_type_window.csv')
for r in cls_rows:
    if r['grouping'] == 'installer class':
        fig(f"window share of mcp downloads, installer class {r['group']}", r['share_of_window_pct'], f"{r['downloads_whole_window']} of {wtot}", 'mcp_installer_and_file_type_window.csv')

# daily by installer class, for the record's table and the weekday test
cls_daily_rows = []
for cls in sorted(cls_win):
    for day in sorted(cls_win[cls]):
        c = cls_win[cls][day]; t = sum(c.values())
        cls_daily_rows.append(dict(date=day, installer_class=cls, all_versions=t, v1_27_0=c['1.27.0'], share_1_27_0_pct=pct(c['1.27.0'], t)))
write_csv('mcp_daily_by_installer_class.csv', cls_daily_rows)

# CI flag, daily
ci_rows = []
for day in day_iter(D('2026-03-19'), D('2026-04-29')):
    ds = day.isoformat()
    r = dict(date=ds, weekday=day.strftime('%a'))
    for flag in ('true', 'false', 'unknown'):
        c = ci_daily.get(flag, {}).get(ds, collections.Counter())
        r[f'ci_{flag}_all'] = sum(c.values()); r[f'ci_{flag}_1.27.0'] = c['1.27.0']
    r['ci_true_share_of_all_pct'] = pct(r['ci_true_all'], r['ci_true_all'] + r['ci_false_all'] + r['ci_unknown_all'])
    r['ci_true_share_of_1.27.0_pct'] = pct(r['ci_true_1.27.0'], r['ci_true_1.27.0'] + r['ci_false_1.27.0'] + r['ci_unknown_1.27.0'])
    ci_rows.append(r)
write_csv('mcp_daily_by_ci_flag.csv', ci_rows)
aw = [r for r in ci_rows if after0 <= D(r['date']) <= after1]
t_true = sum(r['ci_true_1.27.0'] for r in aw); t_all = sum(r['ci_true_1.27.0'] + r['ci_false_1.27.0'] + r['ci_unknown_1.27.0'] for r in aw)
fig('share of mcp 1.27.0 downloads flagged CI, 3 to 22 April', pct(t_true, t_all), f'{t_true} of {t_all}', 'mcp_daily_by_ci_flag.csv')
ww = [r for r in ci_rows if WIN0 <= D(r['date']) <= WIN1]
a_true = sum(r['ci_true_all'] for r in ww); a_all = sum(r['ci_true_all'] + r['ci_false_all'] + r['ci_unknown_all'] for r in ww)
fig('share of all mcp downloads flagged CI, LH002 window', pct(a_true, a_all), f'{a_true} of {a_all}', 'mcp_daily_by_ci_flag.csv')
fig('mcp downloads with CI flag unknown, LH002 window', sum(r['ci_unknown_all'] for r in ww), f'{a_all}', 'mcp_daily_by_ci_flag.csv')
cu = sum(int(r['downloads']) for r in ci_con if r['ci'] == 'unknown'); ct = sum(int(r['downloads']) for r in ci_con)
fig('mcp downloads with CI flag unknown, 17 January to 27 February', cu, f'{ct}', 'clickpy_mcp_daily_by_ci_contrast.csv')

# weekday and weekend: three whole weeks after the release, Monday 6 April to Sunday 26 April
wk = [r for r in share_rows if D('2026-04-06') <= D(r['date']) <= D('2026-04-26')]
def wk_ratio(name, vals):
    wd = [v for d, v in vals if D(d).weekday() < 5]; we = [v for d, v in vals if D(d).weekday() >= 5]
    fig(f'weekend mean over weekday mean, {name}, 6 to 26 April', round(statistics.mean(we) / statistics.mean(wd), 3),
        f'{len(we)} weekend days, {len(wd)} weekdays; means {round(statistics.mean(we))} and {round(statistics.mean(wd))}', 'derived from the daily tables')
wk_ratio('mcp all versions', [(r['date'], r['all_versions']) for r in wk])
wk_ratio('mcp 1.27.0', [(r['date'], r['1.27.0']) for r in wk])
wk_ratio('mcp 1.26.0', [(r['date'], r['1.26.0']) for r in wk])
cir = [r for r in ci_rows if D('2026-04-06') <= D(r['date']) <= D('2026-04-26')]
wk_ratio('mcp 1.27.0 flagged CI', [(r['date'], r['ci_true_1.27.0']) for r in cir])
wk_ratio('mcp 1.27.0 not flagged CI', [(r['date'], r['ci_false_1.27.0']) for r in cir])
for cls in ('uv', 'pip'):
    wk_ratio(f'mcp 1.27.0 by {cls}', [(d, c['1.27.0']) for d, c in cls_win[cls].items() if D('2026-04-06') <= D(d) <= D('2026-04-26')])
    wk_ratio(f'mcp 1.26.0 by {cls}', [(d, c['1.26.0']) for d, c in cls_win[cls].items() if D('2026-04-06') <= D(d) <= D('2026-04-26')])

# ---------- second hop: lean-lsp-mcp ----------
ll = read_csv('clickpy_lean_lsp_mcp_window.csv')
lv = collections.defaultdict(collections.Counter)
for r in ll:
    lv[r['date']][r['version']] += int(r['downloads'])
ll_rows = []
for day in day_iter(D('2026-03-19'), D('2026-05-10')):
    ds = day.isoformat(); c = lv[ds]; m = by_ver.get(ds)
    ll_rows.append(dict(date=ds, weekday=day.strftime('%a'), lean_all_versions=sum(c.values()), lean_0_26_0=c['0.26.0'],
                        lean_0_26_1=c['0.26.1'], lean_0_26_2=c['0.26.2'], lean_0_25_1=c['0.25.1'],
                        mcp_1_27_0=m['1.27.0'] if m else ''))
write_csv('lean_lsp_mcp_daily.csv', ll_rows)
pin = [r for r in ll_rows if D('2026-04-08') <= D(r['date']) <= D('2026-05-03')]
pinned = sum(r['lean_0_26_0'] + r['lean_0_26_1'] for r in pin)
m127 = sum(r['mcp_1_27_0'] for r in pin if r['mcp_1_27_0'] != '')
fig('lean-lsp-mcp 0.26.0 and 0.26.1 downloads, 8 April to 3 May (before 0.26.2)', pinned, '26 UTC days', 'lean_lsp_mcp_daily.csv')
fig('the same, as a share of mcp 1.27.0 downloads over the days ClickPy holds both', pct(pinned, m127) if m127 else '',
    f'{pinned} of {m127} (mcp 1.27.0 over 8 to 29 April only; days after 29 April were not read by version)', 'lean_lsp_mcp_daily.csv')
pin_w = [r for r in ll_rows if D('2026-04-08') <= D(r['date']) <= D('2026-04-29')]
p_w = sum(r['lean_0_26_0'] + r['lean_0_26_1'] for r in pin_w); m_w = sum(r['mcp_1_27_0'] for r in pin_w)
fig('lean-lsp-mcp 0.26.0 and 0.26.1 downloads as a share of mcp 1.27.0 downloads, 8 to 29 April', pct(p_w, m_w), f'{p_w} of {m_w}', 'lean_lsp_mcp_daily.csv')
lc = collections.defaultdict(collections.Counter)
for r in ll:
    if r['version'] in ('0.26.0', '0.26.1'):
        lc['installer'][installer_class(r['installer'])] += int(r['downloads'])
        lc['ci'][r['ci']] += int(r['downloads'])
        lc['type'][r['type']] += int(r['downloads'])
lrows = []
for k in lc:
    tot = sum(lc[k].values())
    for g, n in lc[k].most_common():
        lrows.append(dict(grouping=k, group=g, downloads=n, share_pct=pct(n, tot), denominator=tot))
write_csv('lean_lsp_mcp_0_26_x_breakdown.csv', lrows)

# the other cohort packages, window totals for scale
coh = collections.Counter()
for r in read_csv('clickpy_cohort_daily_total.csv'):
    if WIN0 <= D(r['date']) <= WIN1:
        coh[r['project']] += int(r['downloads'])
write_csv('cohort_window_totals.csv', [dict(project=p, downloads_in_window=n, share_of_mcp_window_pct=pct(n, coh['mcp']))
                                       for p, n in coh.most_common()])

for r in thr_rows:
    if r['series'] in ('all installers', 'installer class: uv', 'installer class: pip', 'CI flag: true', 'CI flag: false'):
        fig(f"{r['series']}, {r['release']}: {r['measure']}", f"{r['date']} (day {r['day_after_release']})",
            f"{r['release_downloads']} of {r['denominator']} ({r['share_pct']} per cent)", 'uptake_thresholds.csv')
write_csv('headline_figures.csv', figures)
print(f'{len(figures)} figures written')

# CI flag by version class, 3 to 22 April (appended; rewrites headline_figures.csv)
vc = collections.defaultdict(collections.Counter)
for r in ci_win:
    if after0 <= D(r['date']) <= after1:
        vc[r['version_class']][r['ci']] += int(r['downloads'])
vrows = []
for v in sorted(vc):
    t = sum(vc[v].values())
    vrows.append(dict(version_class=v, downloads_3_to_22_april=t, flagged_ci=vc[v]['true'], share_flagged_ci_pct=pct(vc[v]['true'], t)))
    fig(f'share of mcp {v} downloads flagged CI, 3 to 22 April', pct(vc[v]['true'], t), f"{vc[v]['true']} of {t}", 'mcp_ci_by_version_class.csv')
allci = sum(vc[v]['true'] for v in vc)
for v in sorted(vc):
    fig(f'share of CI-flagged mcp downloads that were {v}, 3 to 22 April', pct(vc[v]['true'], allci), f"{vc[v]['true']} of {allci}", 'mcp_ci_by_version_class.csv')
write_csv('mcp_ci_by_version_class.csv', vrows)
write_csv('headline_figures.csv', figures)
