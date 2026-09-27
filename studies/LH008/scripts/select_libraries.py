#!/usr/bin/env python3
"""LH008 step 1: the libraries, their events and comparison releases, by brief.md's rules. Reads no
dependent and no repository.
Writes data/top200.csv (ClickPy, August 2026), data/osv_advisories.csv (every OSV record against each of
the 200), data/qualifying_advisories.csv, data/events.csv (the chosen libraries: fixed release, release
before it, advisory, comparison release and the release before that) and data/releases_<lib>.csv."""
import csv, io, os, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from packaging.version import Version, InvalidVersion
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, jget, write_csv, ts, iso, norm

W0, W1 = ts('2026-03-27T00:00:00Z'), ts('2026-08-27T23:59:59Z')
N_TOP, N_LIB = 200, 4
q = lambda s: urllib.parse.quote(s, safe='')


def top200():
    Q = ("SELECT project, sum(count) AS downloads FROM pypi.pypi_downloads_per_month WHERE month = '2026-08-01' "
         f"GROUP BY project ORDER BY downloads DESC LIMIT {N_TOP} FORMAT CSVWithNames")
    r = http('ClickPy (ClickHouse public demo)', 'top 200 projects August 2026',
             'https://sql-clickhouse.clickhouse.com/?user=demo', method='POST', data=Q.encode(), note=Q)
    rows = list(csv.DictReader(io.StringIO(r.text)))
    for i, x in enumerate(rows, 1):
        x['rank'] = i
    write_csv('top200.csv', rows, ['rank', 'project', 'downloads'])
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


def ranges_for(v, pkg):
    out = []
    for a in v.get('affected', []):
        if norm(a.get('package', {}).get('name', '')) != norm(pkg) or a.get('package', {}).get('ecosystem') != 'PyPI':
            continue
        for rg in a.get('ranges', []):
            if rg.get('type') == 'ECOSYSTEM':
                out.append(rg.get('events', []))
    return out


def fixed_versions(v, pkg):
    return [e['fixed'] for evs in ranges_for(v, pkg) for e in evs if 'fixed' in e]


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
    top = top200()
    with ThreadPoolExecutor(8) as ex:
        allv = list(ex.map(lambda t: (t, osv(t['project'])), top))
    arows, qual = [], []
    for t, vs in allv:
        for v in vs:
            ds = v.get('database_specific') or {}
            arows.append(dict(project=t['project'], rank=t['rank'], id=v['id'], aliases=' '.join(v.get('aliases', [])),
                              severity=ds.get('severity', ''), published=v.get('published', ''),
                              modified=v.get('modified', ''), withdrawn=v.get('withdrawn', ''),
                              github_reviewed_at=ds.get('github_reviewed_at', ''),
                              nvd_published_at=ds.get('nvd_published_at', ''),
                              fixed=' '.join(fixed_versions(v, t['project'])), summary=(v.get('summary') or '')[:200]))
    write_csv('osv_advisories.csv', arows)
    for a in arows:
        if not a['id'].startswith('GHSA-') or a['severity'] not in ('HIGH', 'CRITICAL') or a['withdrawn']:
            continue
        if not (W0 <= ts(a['published']) <= W1) or not a['fixed']:
            continue
        qual.append(a)
    rel = {}
    for p in sorted({a['project'] for a in qual}):
        rel[p] = releases(p)
    for a in qual:
        fx = max(a['fixed'].split(), key=lambda s: V(s) or Version('0'))
        a['fixed_release'] = fx
        up = rel[a['project']].get(fx)
        a['fixed_uploaded'] = up or ''
        a['qualifies'] = 'yes' if up and ts(up).date() <= (ts(a['published']).date() - __import__('datetime').timedelta(days=1)) else (
            'no: fixed release not on PyPI' if not up else 'no: fixed release not a calendar day before the advisory')
    write_csv('qualifying_advisories.csv', qual, ['project', 'rank', 'id', 'aliases', 'severity', 'published',
                                                  'github_reviewed_at', 'nvd_published_at', 'fixed', 'fixed_release',
                                                  'fixed_uploaded', 'qualifies', 'summary'])
    events = []
    for p in sorted({a['project'] for a in qual if a['qualifies'] == 'yes'}, key=lambda p: int([t['rank'] for t in top if t['project'] == p][0])):
        qs = sorted([a for a in qual if a['project'] == p and a['qualifies'] == 'yes'], key=lambda a: ts(a['published']))
        first = qs[0]
        fx = first['fixed_release']
        grp = [a for a in qs if a['fixed_release'] == fx]
        R = rel[p]
        stable = sorted([v for v in R if not V(v).is_prerelease and not V(v).is_devrelease], key=V)
        before = lambda x: max([v for v in stable if V(v) < V(x) and ts(R[v]) < ts(R[x])], key=V, default='')
        rb = before(fx)
        patch = lambda x, y: V(x).release[:2] == V(y).release[:2]
        kind = 'patch' if rb and patch(fx, rb) else 'minor or major'
        all_fixed = {f for a in arows if a['project'] == p for f in a['fixed'].split()}
        cands = []
        for v in stable:
            if ts(R[v]) > ts(R[fx]) - __import__('datetime').timedelta(days=30) or v in all_fixed:
                continue
            b = before(v)
            if not b:
                continue
            if ('patch' if patch(v, b) else 'minor or major') != kind:
                continue
            cands.append(v)
        comp = max(cands, key=lambda v: ts(R[v]), default='')
        events.append(dict(library=p, rank=[t['rank'] for t in top if t['project'] == p][0], advisory=first['id'],
                           other_advisories_same_fix=' '.join(a['id'] for a in grp[1:]), severity=first['severity'],
                           advisory_published=first['published'], github_reviewed_at=first['github_reviewed_at'],
                           nvd_published_at=first['nvd_published_at'], fixed_release=fx, fixed_uploaded=R[fx],
                           release_before_fix=rb, release_before_fix_uploaded=R.get(rb, ''), kind=kind,
                           comparison_release=comp, comparison_uploaded=R.get(comp, ''),
                           release_before_comparison=before(comp) if comp else '',
                           release_before_comparison_uploaded=R.get(before(comp), '') if comp else '',
                           chosen='yes' if len([e for e in events if e['chosen'] == 'yes']) < N_LIB else 'no (beyond four)'))
    write_csv('events.csv', events)
    for e in events:
        if e['chosen'] == 'yes':
            R = rel[e['library']]
            write_csv(f'releases_{norm(e["library"])}.csv', [dict(version=v, uploaded=R[v]) for v in sorted(R, key=lambda v: ts(R[v]))])
    for e in events:
        print(e['rank'], e['library'], e['advisory'], e['severity'], e['advisory_published'], 'fix', e['fixed_release'],
              e['fixed_uploaded'], 'before', e['release_before_fix'], '| comp', e['comparison_release'],
              e['comparison_uploaded'], 'before', e['release_before_comparison'], e['chosen'])
    print(len(arows), 'OSV records;', len(qual), 'HIGH/CRITICAL GHSA in window with a fix;',
          sum(a['qualifies'] == 'yes' for a in qual), 'qualify')


if __name__ == '__main__':
    main()
