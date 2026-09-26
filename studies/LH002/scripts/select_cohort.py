#!/usr/bin/env python3
"""LH002 cohort selection. Uses deps.dev metadata only: the dependents list of
PyPI mcp 1.27.0, each dependent's SOURCE_REPO link and its first PyPI release
date. Falls back to PyPI's JSON metadata for the repository link when deps.dev has
none. Eligible: a GitHub repository other than the library's, one entry per
repository, and a first PyPI release before the window start. Reads no
dependent's commit, tag or in-window release activity.

Usage: python3 select_cohort.py <scratch_dir>
Writes <scratch_dir>/raw/depsdev/* and <scratch_dir>/cohort_selection.json
"""
import hashlib, json, os, sys, time, urllib.request, urllib.parse

S = sys.argv[1]
RAW = os.path.join(S, 'raw', 'depsdev')
os.makedirs(RAW, exist_ok=True)
LIB, LIBVER = 'mcp', '1.27.0'
LIBREPO = 'github.com/modelcontextprotocol/python-sdk'
WINDOW_START = '2026-03-26T00:00:00Z'
PREVER = '1.26.0'  # the release current at window start

def get(url, path):
    if not os.path.exists(path):
        with urllib.request.urlopen(url, timeout=60) as r:
            open(path, 'wb').write(r.read())
        time.sleep(0.2)
    return json.load(open(path))

q = urllib.parse.quote

def repo_of(name, ver):
    v = get(f'https://api.deps.dev/v3/systems/pypi/packages/{q(name, safe="")}/versions/{q(ver, safe="")}',
            os.path.join(RAW, f'ver-{name}-{ver}.json'))
    for rp in v.get('relatedProjects', []):
        if rp['relationType'] == 'SOURCE_REPO' and rp['projectKey']['id'].startswith('github.com/'):
            return rp['projectKey']['id'].lower(), 'deps.dev relation'
    for l in v.get('links', []):
        u = l['url'].lower().rstrip('/')
        if 'github.com/' in u and l['label'] in ('SOURCE_REPO', 'HOMEPAGE'):
            parts = u.split('github.com/')[1].split('/')
            if len(parts) >= 2 and parts[1]:
                return 'github.com/' + parts[0] + '/' + parts[1].removesuffix('.git'), 'deps.dev link'
    # fallback: PyPI's own metadata for the same version
    pj = get(f'https://pypi.org/pypi/{q(name, safe="")}/{q(ver, safe="")}/json',
             os.path.join(RAW, f'pypi-{name}-{ver}.json'))
    urls = list((pj['info'].get('project_urls') or {}).items()) + [('home_page', pj['info'].get('home_page') or '')]
    urls.sort(key=lambda kv: 0 if kv[0].lower() in ('source', 'repository', 'source code', 'code', 'github') else 1)
    for _, u in urls:
        u = (u or '').lower().rstrip('/')
        if 'github.com/' in u:
            parts = u.split('github.com/')[1].split('/')
            if len(parts) >= 2 and parts[1]:
                return 'github.com/' + parts[0] + '/' + parts[1].removesuffix('.git'), 'PyPI project_urls'
    return None, None

def frame(libver, seen):
    dep = get(f'https://deps.dev/_/s/pypi/p/{LIB}/v/{libver}/dependents',
              os.path.join(RAW, f'web-dependents-{libver}.json'))
    rows = []
    for d in dep['directSample']:
        name, ver = d['package']['name'], d['version']
        repo, via = repo_of(name, ver)
        p = get(f'https://api.deps.dev/v3/systems/pypi/packages/{q(name, safe="")}',
                os.path.join(RAW, f'pkg-{name}.json'))
        first = min((x['publishedAt'] for x in p['versions'] if x.get('publishedAt')), default=None)
        rows.append(dict(frame=f'{LIB} {libver}', package=name, version=ver, repo=repo, repo_via=via,
                         first_release=first, hash=hashlib.sha256(name.lower().encode()).hexdigest()))
    eligible = []
    for r in sorted(rows, key=lambda r: r['hash']):
        why = ('no GitHub repo' if r['repo'] is None else 'library repo' if r['repo'] == LIBREPO
               else 'duplicate repo' if r['repo'] in seen
               else 'first PyPI release not before window start' if not (r['first_release'] and r['first_release'] < WINDOW_START)
               else None)
        if why:
            r['excluded'] = why; continue
        seen.add(r['repo']); eligible.append(r)
    counts = {k: dep[k] for k in ('totalCount', 'directCount', 'indirectCount')}
    return rows, eligible, counts

seen = set()
# Slots 1 to 8: direct dependents of the in-window release, in SHA-256 order of package name.
rows_a, elig_a, counts_a = frame(LIBVER, seen)
chosen = elig_a[:8]
for r in chosen: r['slot'] = 'A: in-window release frame, hash order'
# Slot 9 (if slots 1 to 8 did not fill, the remaining slots up to 9 in total dependents):
# the oldest by first PyPI release among the in-window frame's remainder; then, to guarantee an
# older and possibly quieter contrast whatever frame A yields, slots up to 9 dependents are
# filled from the pre-window release's (1.26.0) direct dependents, oldest first release first.
rest_a = sorted(elig_a[8:], key=lambda r: r['first_release'])
for r in rest_a[:1]:
    r['slot'] = 'A: oldest first release'; chosen.append(r)
rows_b, elig_b, counts_b = frame(PREVER, seen)
for r in sorted(elig_b, key=lambda r: r['first_release']):
    if len(chosen) >= 9: break
    r['slot'] = 'B: pre-window release frame, oldest first release'; chosen.append(r)
out = dict(library=dict(package=LIB, version=LIBVER, repo=LIBREPO), window_start=WINDOW_START,
           frame_counts={LIBVER: counts_a, PREVER: counts_b},
           rows=rows_a + rows_b, chosen=chosen)
json.dump(out, open(os.path.join(S, 'cohort_selection.json'), 'w'), indent=1)
for r in rows_a + rows_b:
    if r.get('slot') or r['frame'].endswith(LIBVER):
        print(f"{r['frame']:10} {r['package']:26} {r['repo'] or '-':52} {str(r['repo_via']):18} first={str(r['first_release'])[:10]} {r.get('slot', r.get('excluded',''))}")
print('frame B excluded reasons:', {k: sum(1 for r in rows_b if r.get('excluded') == k) for k in set(r.get('excluded') for r in rows_b)})
print('counts', counts_a, counts_b)
