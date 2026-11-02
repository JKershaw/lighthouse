"""LH013 count stages, run only with LH013_PHASE=counts, after the eligibility check, the days-held listing,
the PyPI metadata read and amendment 4 (all before any count of W1 or W2). Called from collect.py.
Writes under data/counts/. A query that fails (an HTTP error, an exception in the body, or a limit, which
SETTINGS make throw) is logged and split as stated per stage; nothing is retried silently."""
import csv, os
import common
from common import clickhouse, write_csv, read_csv, DATA

ROOT = os.path.dirname(os.path.dirname(DATA))
P37 = sorted({r['project'] for r in read_csv(os.path.join(ROOT, 'LH011', 'data', 'releases.csv'))})
OUT = os.path.join(DATA, 'counts')
WK = "if(date <= '2026-10-04', 'W1', 'W2')"
MINOR_GROUPS = [('a', ['', '2.7', '3.4', '3.5', '3.6']), ('b', ['3.7', '3.8', '3.9', '3.10']), ('c', ['3.11', '3.12', '3.13']),
                ('d', ['3.14', '3.15'])]


def ql(xs):
    return ','.join("'" + x.replace("'", "''") + "'" for x in xs)


def classes():
    c = {}
    for r in read_csv(os.path.join(DATA, 'frame', 'classes.csv')):
        c.setdefault(r['project'], {}).setdefault(r['R0'], []).append(r['version'])
    return c


def gap_days():
    path = os.path.join(DATA, 'analysis', 'gaps.csv')
    return {} if not os.path.exists(path) else {(r['project'], r['date']) for r in read_csv(path)}


def stage_w0check(_):
    if PHASE_CHECK():
        clickhouse('w0check', 'B1 W0 daily totals by project, per-version table',
                   f"SELECT project, date, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version WHERE project IN ({ql(P37)}) "
                   "AND date BETWEEN '2026-09-21' AND '2026-09-27' GROUP BY project, date ORDER BY project, date", 'counts/w0_daily_totals.csv')


def stage_totals(_):
    clickhouse('totals', 'N1 daily totals by project, 25 September to 14 October 2026 (gap rule)',
               f"SELECT project, date, sum(count) AS n FROM pypi.pypi_downloads_per_day WHERE project IN ({ql(P37)}) "
               "AND date BETWEEN '2026-09-25' AND '2026-10-14' GROUP BY project, date ORDER BY project, date", 'counts/daily_totals.csv')


def stage_versions(projects):
    gaps = gap_days()
    for p in projects or P37:
        path = os.path.join(OUT, 'versions', p + '.csv')
        if os.path.exists(path):
            continue
        skip = sorted(d for (q, d) in gaps if q == p)
        cond = f" AND date NOT IN ({ql(skip)})" if skip else ''
        rows = clickhouse('versions', f'V {p} W1 and W2 sums by version' + (f' without gap days {skip}' if skip else ''),
                          f"SELECT {WK} AS week, version, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version "
                          f"WHERE project = '{p}' AND date BETWEEN '2026-09-28' AND '2026-10-11'{cond} GROUP BY week, version ORDER BY week, version")
        if rows is None:
            rows = []
            for w, (a, b) in (('W1', ('2026-09-28', '2026-10-04')), ('W2', ('2026-10-05', '2026-10-11'))):
                r = clickhouse('versions', f'V {p} {w} sums by version (split)',
                               f"SELECT '{w}' AS week, version, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version "
                               f"WHERE project = '{p}' AND date BETWEEN '{a}' AND '{b}'{cond} GROUP BY week, version ORDER BY version")
                if r is None:
                    raise SystemExit(f'V {p} {w}: could not be read')
                rows += r
        write_csv(path, rows, ['week', 'version', 'n'])


def stage_python(projects):
    gaps = gap_days()
    for p in projects or P37:
        path = os.path.join(OUT, 'python', p + '.csv')
        if os.path.exists(path):
            continue
        skip = sorted(d for (q, d) in gaps if q == p)
        cond = f" AND date NOT IN ({ql(skip)})" if skip else ''
        base = (f"SELECT {WK} AS week, version, python_minor, sum(count) AS n FROM pypi.pypi_downloads_per_day_by_version_by_python "
                f"WHERE project = '{p}' AND date BETWEEN '2026-09-28' AND '2026-10-11'{cond}")
        rows = clickhouse('python', f'Y {p} W1 and W2 sums by version and Python', base + " GROUP BY week, version, python_minor ORDER BY week, version, python_minor")
        if rows is None:
            rows = []
            named = [m for _, g in MINOR_GROUPS for m in g]
            for w, (a, b) in (('W1', ('2026-09-28', '2026-10-04')), ('W2', ('2026-10-05', '2026-10-11'))):
                for g, ms in MINOR_GROUPS + [('rest', None)]:
                    c = f"python_minor IN ({ql(ms)})" if ms else f"python_minor NOT IN ({ql(named)})"
                    r = clickhouse('python', f'Y {p} {w} minors {g} (split)',
                                   base.replace("date BETWEEN '2026-09-28' AND '2026-10-11'", f"date BETWEEN '{a}' AND '{b}' AND {c}")
                                   + " GROUP BY week, version, python_minor ORDER BY version, python_minor")
                    if r is None:
                        raise SystemExit(f'Y {p} {w} {g}: could not be read')
                    rows += r
        write_csv(path, rows, ['week', 'version', 'python_minor', 'n'])


K6 = "concat(python_minor, '|', installer, '|', system, '|', libc_lib, '|', ci, '|', country_code)"
K5 = "concat(python_minor, '|', installer, '|', system, '|', libc_lib, '|', ci)"


def cell_sql(p, a, b, ge, older, cond=''):
    def arr(m, name):
        return (f"tupleElement({m}, 1)[indexOf(tupleElement({m}, 2), arrayMax(tupleElement({m}, 2)))] AS {name}_key, "
                f"length(tupleElement({m}, 1)) AS {name}_cells, "
                f"arrayStringConcat(arrayMap(x -> toString(x), arraySlice(arrayReverseSort(tupleElement({m}, 2)), 1, 1001)), ' ') AS {name}_top")
    ci = ', '.join(f"sumIf(n, cls = '{c}' AND ci = '{f}') AS {c}_ci_{f}" for c in ('older', 'at_or_newer', 'other')
                   for f in ('true', 'false', 'unknown'))
    return (f"SELECT total, older, at_or_newer, other, {', '.join(f'{c}_ci_{f}' for c in ('older', 'at_or_newer', 'other') for f in ('true', 'false', 'unknown'))}, "
            f"{arr('m6', 'c6')}, {arr('m5', 'c5')}, {arr('o6', 'older_c6')}, {arr('o5', 'older_c5')} FROM ("
            f"SELECT sum(n) AS total, sumIf(n, cls = 'older') AS older, sumIf(n, cls = 'at_or_newer') AS at_or_newer, "
            f"sumIf(n, cls = 'other') AS other, {ci}, sumMap([{K6}], [n]) AS m6, sumMap([{K5}], [n]) AS m5, "
            f"sumMapIf([{K6}], [n], cls = 'older') AS o6, sumMapIf([{K5}], [n], cls = 'older') AS o5 FROM ("
            f"SELECT multiIf(version IN ({ql(ge)}), 'at_or_newer', version IN ({ql(older)}), 'older', 'other') AS cls, python_minor, "
            f"installer, system, tupleElement(libc, 'lib') AS libc_lib, toString(ci) AS ci, country_code, count() AS n "
            f"FROM pypi.pypi WHERE project = '{p}' AND date BETWEEN '{a}' AND '{b}'{cond} "
            f"GROUP BY cls, python_minor, installer, system, libc_lib, ci, country_code))")


def stage_pass(projects):
    cl = classes()
    gaps = gap_days()
    for p in projects or P37:
        ge, older = cl[p].get('at_or_newer', []), cl[p].get('older', [])
        for w, (a, b) in (('W1', ('2026-09-28', '2026-10-04')), ('W2', ('2026-10-05', '2026-10-11'))):
            path = os.path.join(OUT, 'pass', f'{p}_{w}.csv')
            if os.path.exists(path):
                continue
            skip = sorted(d for (q, d) in gaps if q == p and a <= d <= b)
            cond = f" AND date NOT IN ({ql(skip)})" if skip else ''
            rows = clickhouse('pass', f'C {p} {w} cells' + (f' without gap days {skip}' if skip else ''), cell_sql(p, a, b, ge, older, cond), f'counts/pass/{p}_{w}.csv')
            if rows is None:
                print(f'   C {p} {w}: failed; left unread for now')


def PHASE_CHECK():
    if common.PHASE != 'counts':
        raise SystemExit('count stages run only with LH013_PHASE=counts')
    return True


def run(stage, projects):
    PHASE_CHECK()
    os.makedirs(OUT, exist_ok=True)
    globals()['stage_' + stage](projects)
