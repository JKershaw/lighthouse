#!/usr/bin/env python3
"""LH010 step 1: the libraries and their events, by brief.md's rules. Reads no note, dependent or repository.
Copied from LH008's select_libraries.py and changed as LH010's brief says: the 500 most downloaded projects
(not 200); GHSA records of every severity (not HIGH and CRITICAL only), with database_specific.github_reviewed
true; every library with a qualifying advisory has an event (no limit of four) and no comparison release is
chosen; the release lists go to one file.

Writes data/top500.csv (ClickPy, August 2026), data/osv_advisories.csv (every OSV record against each of the
500), data/qualifying_advisories.csv (GHSA, reviewed, in the window, with a fix; whether the fix came a calendar
day earlier), data/events.csv (one per library by LH008's rule 4, in download order) and data/releases.csv
(every release of each library with an event: version and first upload, non-yanked files where any)."""
import csv, datetime, io, os, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from packaging.version import Version, InvalidVersion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, jget, write_csv, ts, iso, norm

W0, W1 = ts('2026-03-27T00:00:00Z'), ts('2026-08-27T23:59:59Z')
N_TOP = 500
q = lambda s: urllib.parse.quote(s, safe='')


def top():
    Q = ("SELECT project, sum(count) AS downloads FROM pypi.pypi_downloads_per_month WHERE month = '2026-08-01' "
         f"GROUP BY project ORDER BY downloads DESC LIMIT {N_TOP} FORMAT CSVWithNames")
    r = http('ClickPy (ClickHouse public demo)', 'top 500 projects August 2026',
             'https://sql-clickhouse.clickhouse.com/?user=demo', method='POST', data=Q.encode(), note=Q)
    rows = list(csv.DictReader(io.StringIO(r.text)))
    for i, x in enumerate(rows, 1):
        x['rank'] = i
    write_csv('top500.csv', rows, ['rank', 'project', 'downloads'])
    return rows


def osv(pkg):
    vulns, token = [], None
    while True:
        body = {'package': {'name': pkg, 'ecosystem': 'PyPI'}}
        if token:
            body['page_token'] = token
        r = http('OSV API', f'OSV query {pkg}', 'https://api.osv.dev/v1/query', method='POST', json_body=body)
        j = r.json() if r.status_code == 200 else {}
        vulns += j.get('vulns', [])
        token = j.get('next_page_token')
        if not token:
            return vulns


def fixed_versions(v, pkg):
    out = []
    for a in v.get('affected', []):
        if norm(a.get('package', {}).get('name', '')) != norm(pkg) or a.get('package', {}).get('ecosystem') != 'PyPI':
            continue
        for rg in a.get('ranges', []):
            if rg.get('type') == 'ECOSYSTEM':
                out += [e['fixed'] for e in rg.get('events', []) if 'fixed' in e]
    return out


def V(s):
    try:
        return Version(s)
    except InvalidVersion:
        return None


def releases(pkg):
    j = jget('PyPI JSON API', f'PyPI {pkg}', f'https://pypi.org/pypi/{q(pkg)}/json')
    out = {}
    for ver, files in (j or {}).get('releases', {}).items():
        files = [f for f in files if not f.get('yanked')] or files
        if files and V(ver):
            out[ver] = min(f['upload_time_iso_8601'] for f in files)
    return out


def main():
    T = top()
    with ThreadPoolExecutor(8) as ex:
        allv = list(ex.map(lambda t: (t, osv(t['project'])), T))
    arows = []
    for t, vs in allv:
        for v in vs:
            ds = v.get('database_specific') or {}
            arows.append(dict(project=t['project'], rank=t['rank'], id=v['id'], aliases=' '.join(v.get('aliases', [])),
                              severity=ds.get('severity', ''), github_reviewed=str(ds.get('github_reviewed', '')),
                              published=v.get('published', ''), modified=v.get('modified', ''),
                              withdrawn=v.get('withdrawn', ''), github_reviewed_at=ds.get('github_reviewed_at', ''),
                              nvd_published_at=ds.get('nvd_published_at', ''),
                              fixed=' '.join(fixed_versions(v, t['project'])), summary=(v.get('summary') or '')[:200]))
    write_csv('osv_advisories.csv', arows)
    qual = [a for a in arows if a['id'].startswith('GHSA-') and a['github_reviewed'] == 'True' and not a['withdrawn']
            and W0 <= ts(a['published']) <= W1 and a['fixed']]
    with ThreadPoolExecutor(8) as ex:
        rel = dict(zip(sorted({a['project'] for a in qual}), ex.map(releases, sorted({a['project'] for a in qual}))))
    for a in qual:
        fx = max(a['fixed'].split(), key=lambda s: V(s) or Version('0'))
        a['fixed_release'] = fx
        up = rel[a['project']].get(fx)
        a['fixed_uploaded'] = up or ''
        a['qualifies'] = 'yes' if up and ts(up).date() <= ts(a['published']).date() - datetime.timedelta(days=1) else (
            'no: fixed release not on PyPI' if not up else 'no: fixed release not a calendar day before the advisory')
    write_csv('qualifying_advisories.csv', qual, ['project', 'rank', 'id', 'aliases', 'severity', 'published',
                                                  'github_reviewed_at', 'nvd_published_at', 'fixed', 'fixed_release',
                                                  'fixed_uploaded', 'qualifies', 'summary'])
    rank = {t['project']: int(t['rank']) for t in T}
    events = []
    for p in sorted({a['project'] for a in qual if a['qualifies'] == 'yes'}, key=lambda p: rank[p]):
        qs = sorted([a for a in qual if a['project'] == p and a['qualifies'] == 'yes'], key=lambda a: ts(a['published']))
        first = qs[0]
        fx = first['fixed_release']
        grp = [a for a in qs if a['fixed_release'] == fx]
        R = rel[p]
        stable = sorted([v for v in R if not V(v).is_prerelease and not V(v).is_devrelease], key=V)
        rb = max([v for v in stable if V(v) < V(fx) and ts(R[v]) < ts(R[fx])], key=V, default='')
        events.append(dict(library=p, rank=rank[p], advisory=first['id'],
                           other_advisories_same_fix=' '.join(a['id'] for a in grp[1:]), severity=first['severity'],
                           advisory_published=first['published'], github_reviewed_at=first['github_reviewed_at'],
                           nvd_published_at=first['nvd_published_at'], fixed_release=fx, fixed_uploaded=R[fx],
                           release_before_fix=rb, release_before_fix_uploaded=R.get(rb, ''),
                           release_to_advisory_days=round((ts(first['published']) - ts(R[fx])).total_seconds() / 86400, 2),
                           qualifying_fixes=' '.join(sorted({a['fixed_release'] for a in qs}, key=V))))
    write_csv('events.csv', events)
    write_csv('releases.csv', [dict(library=p, version=v, uploaded=R[v]) for p, R in rel.items()
                               for v in sorted(R, key=lambda v: ts(R[v]))])
    sev = {}
    for a in qual:
        sev.setdefault(a['severity'] or 'none', [0, 0])[a['qualifies'] == 'yes'] += 1
    print(len(arows), 'OSV records against', len(T), 'projects;', len(qual), 'reviewed GHSA in the window with a fix;',
          sum(a['qualifies'] == 'yes' for a in qual), 'qualify, against', len(events), 'libraries')
    print('by severity [not qualifying, qualifying]:', sev)
    print('distinct qualifying fixes:', len({(a['project'], a['fixed_release']) for a in qual if a['qualifies'] == 'yes'}))
    print('events in the top 200:', sum(e['rank'] <= 200 for e in events))


if __name__ == '__main__':
    main()
