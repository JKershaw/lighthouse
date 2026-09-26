#!/usr/bin/env python3
"""LH007 step 1: the frame and the screening of brief.md's sampling rule. Reads no image, tag list
or registry.

Frame: the direct dependents Open Source Insights lists for mcp 1.27.2, 1.28.0 and 1.28.1, ordered by
SHA-256 of the PEP 503 normalised name (data/frame.csv, written before any clone). Screening, for the
first 120 in that order, as LH006: the repository by LH002's rule; PyPI's JSON for the listed and the
latest version; a blobless clone and, at the default branch head and at its last commit at or before
2026-07-14T21:37:16Z, only the files the brief names. Writes data/candidate_frame.csv and
data/candidate_hits.csv. Qualification is decided in classify_candidates.py.

Usage: LH007_SCRATCH=<dir> python3 select_candidates.py [frame|screen]
"""
import hashlib, os, re, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, write_csv, read_csv, git, SCRATCH, now, log

PERIOD_END = '2026-07-14T21:37:16Z'
VERSIONS = ['1.27.2', '1.28.0', '1.28.1']
N_SCREEN = 120
q = lambda s: urllib.parse.quote(s, safe='')
TERMS = re.compile(r'docker\s+pull|docker\s+run|podman\s+(pull|run)|ghcr\.io|docker\.io/|hub\.docker\.com|quay\.io|'
                   r'registry\.gitlab\.com|public\.ecr\.aws|\.azurecr\.io|gcr\.io|pkg\.dev|build-push-action|docker\s+push|'
                   r'org\.opencontainers\.image|"registryType"\s*:\s*"oci"|registry_type|^\s*image\s*:|^\s*images\s*:|--push', re.I)


def norm(n):
    return re.sub(r'[-_.]+', '-', n).lower()


def jget(label, url):
    r = http('Open Source Insights' if 'deps.dev' in url else 'PyPI JSON API', label, url)
    return r.json() if r.status_code == 200 else None


def frame():
    fr = {}
    counts = []
    for v in VERSIONS:
        d = jget(f'deps.dev dependents mcp {v}', f'https://deps.dev/_/s/pypi/p/mcp/v/{v}/dependents')
        c = jget(f'deps.dev v3 dependents count mcp {v}',
                 f'https://api.deps.dev/v3alpha/systems/pypi/packages/mcp/versions/{v}:dependents')
        counts.append(dict(version=v, total=d['totalCount'], direct=d['directCount'], indirect=d['indirectCount'],
                           direct_listed=len(d['directSample']),
                           v3alpha=str(c) if c else 'not served', read_utc=now()))
        for i, e in enumerate(d['directSample']):
            n = norm(e['package']['name'])
            x = fr.setdefault(n, dict(package=e['package']['name'], norm=n, sha256=hashlib.sha256(n.encode()).hexdigest(),
                                      **{f'in_{w}': '' for w in VERSIONS}, listed_version=''))
            x[f'in_{v}'] = e['version']
            x['listed_version'] = x['listed_version'] or e['version']
            x[f'pos_{v}'] = i
    rows = sorted(fr.values(), key=lambda r: r['sha256'])
    for i, r in enumerate(rows, 1):
        r['hash_rank'] = i
        r['screened'] = 'yes' if i <= N_SCREEN else 'no (beyond the screening limit)'
    write_csv('frame.csv', rows, ['hash_rank', 'package', 'norm', 'sha256'] + [f'in_{v}' for v in VERSIONS] +
              ['listed_version', 'screened'])
    write_csv('frame_counts.csv', counts)
    print(counts, len(rows))


def repo_from_version(name, ver):
    v = jget(f'deps.dev version {name} {ver}',
             f'https://api.deps.dev/v3/systems/pypi/packages/{q(name)}/versions/{q(ver)}') or {}
    for rp in v.get('relatedProjects', []):
        if rp['relationType'] == 'SOURCE_REPO':
            return rp['projectKey']['id'].lower(), 'deps.dev relation'
    for l in v.get('links', []):
        u = l['url'].lower().rstrip('/')
        for host in ('github.com/', 'gitlab.com/'):
            if host in u and l['label'] in ('SOURCE_REPO', 'HOMEPAGE'):
                parts = u.split(host)[1].split('/')
                if len(parts) >= 2 and parts[1]:
                    return host + parts[0] + '/' + parts[1].removesuffix('.git'), 'deps.dev link'
    return None, None


def repo_from_pypi(pj):
    urls = list((pj['info'].get('project_urls') or {}).items()) + [('home_page', pj['info'].get('home_page') or '')]
    urls.sort(key=lambda kv: 0 if kv[0].lower() in ('source', 'repository', 'source code', 'code', 'github') else 1)
    for _, u in urls:
        u = (u or '').lower().rstrip('/')
        for host in ('github.com/', 'gitlab.com/'):
            if host in u:
                parts = u.split(host)[1].split('/')
                if len(parts) >= 2 and parts[1]:
                    return host + parts[0] + '/' + parts[1].removesuffix('.git'), 'PyPI project_urls'
    return None, None


def wanted(path):
    b = path.rsplit('/', 1)[-1]
    depth = path.count('/')
    return (re.match(r'(?i)^(docker|container)file', b) or b.lower().endswith('.dockerfile')
            or re.match(r'(?i)^(docker-)?compose.*\.ya?ml$', b)
            or (path.startswith('.github/workflows/') and b.endswith(('.yml', '.yaml')))
            or b == '.gitlab-ci.yml'
            or (b.lower().startswith('readme') and depth <= 2)
            or (depth == 0 and b.lower().endswith('.md'))
            or (b in ('server.json', 'smithery.yaml') and depth <= 2))


def scan_text(text, where, hits, pkg, path):
    for i, line in enumerate(text.splitlines(), 1):
        if TERMS.search(line):
            hits.append(dict(package=pkg, where=where, file=path, line=i, text=line.strip()[:240]))


def screen_one(e):
    pkg, hits = e['package'], []
    latest = jget(f'PyPI latest {pkg}', f'https://pypi.org/pypi/{q(pkg)}/json')
    e['latest_version'] = latest['info']['version'] if latest else ''
    listed = jget(f'PyPI {pkg} {e["listed_version"]}', f'https://pypi.org/pypi/{q(pkg)}/{q(e["listed_version"])}/json')
    r, via = repo_from_version(pkg, e['listed_version'])
    if not r and listed:
        r, via = repo_from_pypi(listed)
    if not r and latest:
        r, via = repo_from_pypi(latest)
    e['repo'], e['repo_via'] = r or '', via or ''
    for tag, pj in (('pypi listed', listed), ('pypi latest', latest)):
        if pj:
            scan_text(pj['info'].get('description') or '', tag, hits, pkg, 'description')
            scan_text('\n'.join(f'{k}: {v}' for k, v in (pj['info'].get('project_urls') or {}).items()),
                      tag, hits, pkg, 'project_urls')
    e.update(head_commit='', head_date='', period_end_commit='', period_end_date='', files_head=0,
             files_period_end=0, dockerfile_head='', dockerfile_period_end='', clone='')
    if e['repo']:
        d = os.path.join(SCRATCH, 'repos', e['repo'].replace('/', '__'))
        url = 'https://' + e['repo'] + '.git'
        t = now()
        if not os.path.exists(d):
            try:
                git(['-c', 'credential.helper=', '-c', 'core.askPass=true', 'clone', '-q', '--filter=blob:none',
                     '--no-checkout', url, d])
                st = 'cloned'
            except Exception as ex:
                st = 'failed: ' + str(ex)[:200].replace('\n', ' ')
        else:
            st = 'already cloned'
        log(read_utc=t, source='git over HTTPS', label=f'clone {pkg}', method='git clone --filter=blob:none',
            endpoint=url, http_status='', bytes='', note=st)
        e['clone'] = st.split(':')[0]
        if e['clone'] != 'failed' and os.path.exists(d):
            try:
                head = git(['rev-parse', 'HEAD'], cwd=d).strip()
                pend = git(['rev-list', '-1', f'--before={PERIOD_END}', 'HEAD'], cwd=d).strip()
            except Exception:
                head, pend = '', ''
            for label, c in (('head', head), ('period_end', pend)):
                if not c:
                    continue
                e[f'{label}_commit'] = c[:10]
                e[f'{label}_date'] = git(['show', '-s', '--format=%cI', c], cwd=d).strip()
                paths = [p for p in git(['ls-tree', '-r', '--name-only', c], cwd=d).splitlines() if wanted(p)][:300]
                e[f'files_{label}'] = len(paths)
                e[f'dockerfile_{label}'] = ';'.join(p for p in paths if re.match(r'(?i)^(docker|container)file', p.rsplit('/', 1)[-1]) or p.lower().endswith('.dockerfile'))[:500]
                for p in paths:
                    try:
                        txt = git(['show', f'{c}:{p}'], cwd=d)
                    except Exception:
                        continue
                    scan_text(txt, f'git {label} {c[:10]}', hits, pkg, p)
    print(e['hash_rank'], pkg, e['repo'], e.get('clone'), bool(e.get('dockerfile_head')), len(hits), flush=True)
    return e, hits


def screen():
    os.makedirs(os.path.join(SCRATCH, 'repos'), exist_ok=True)
    fr = [r for r in read_csv('frame.csv') if r['screened'] == 'yes']
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(screen_one, fr))
    rows = [r for r, _ in res]
    hits = [h for _, hs in res for h in hs]
    write_csv('candidate_frame.csv', rows, ['hash_rank', 'package', 'listed_version', 'latest_version', 'in_1.27.2',
                                            'in_1.28.0', 'in_1.28.1', 'repo', 'repo_via', 'clone', 'head_commit',
                                            'head_date', 'period_end_commit', 'period_end_date', 'files_head',
                                            'files_period_end', 'dockerfile_head', 'dockerfile_period_end'])
    write_csv('candidate_hits.csv', hits, ['package', 'where', 'file', 'line', 'text'])


if __name__ == '__main__':
    {'frame': frame, 'screen': screen}[sys.argv[1]]()
