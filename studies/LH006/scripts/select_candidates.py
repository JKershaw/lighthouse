#!/usr/bin/env python3
"""LH006 step 1: apply the selection rule in brief.md. Reads no image, tag list or registry.

Frame: LH002's ten repositories and the direct dependents of PyPI mcp 1.27.0 listed by Open Source
Insights' dependents endpoint (read again now). For each package: the repository LH002's rule
resolves; PyPI's JSON for the listed and the latest version; a blobless clone of the repository and,
at the default branch head and at its last commit at or before 2026-05-22T23:59:59Z, only the files
named in the brief. Writes data/candidate_frame.csv (the frame) and data/candidate_hits.csv (every
matching line). Qualification is decided in classify_candidates.py from these two files.

Usage: LH006_SCRATCH=<dir> python3 select_candidates.py
"""
import os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import http, write_csv, git, SCRATCH, now, log

PERIOD_END = '2026-05-22T23:59:59Z'
LH002 = [  # id, package, repository, as fixed in studies/LH002/cohort.md
    ('R00', 'mcp', 'github.com/modelcontextprotocol/python-sdk'),
    ('R01', 'agentcrew-ai', 'github.com/saigontechnology/agentcrew'),
    ('R02', 'databricks-tellr-app', 'github.com/robertwhiffin/ai-slide-generator'),
    ('R03', 'lean-lsp-mcp', 'github.com/ooo0ooo/lean-lsp-mcp'),
    ('R04', 'pyp6xer-mcp', 'github.com/paulieb89/pyp6xer-mcp'),
    ('R05', 'serena-agent', 'github.com/oraios/serena'),
    ('R06', 'dartlab', 'github.com/eddmpython/dartlab'),
    ('R07', 'mistral-vibe', 'github.com/mistralai/mistral-vibe'),
    ('R08', 'octobot', 'github.com/drakkar-software/octobot'),
    ('R09', 'jesse', 'github.com/jesse-ai/jesse'),
]
q = lambda s: urllib.parse.quote(s, safe='')
TERMS = re.compile(r'docker\s+pull|docker\s+run|podman\s+(pull|run)|ghcr\.io|docker\.io/|hub\.docker\.com|quay\.io|'
                   r'registry\.gitlab\.com|public\.ecr\.aws|\.azurecr\.io|gcr\.io|pkg\.dev|build-push-action|docker\s+push|'
                   r'org\.opencontainers\.image|"registryType"\s*:\s*"oci"|registry_type|^\s*image\s*:', re.I)


def jget(label, url):
    r = http('Open Source Insights' if 'deps.dev' in url else 'PyPI JSON API', label, url)
    return r.json() if r.status_code == 200 else None


def repo_from_version(name, ver):
    """LH002's rule (studies/LH002/scripts/select_cohort.py), extended to any forge host."""
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


def main():
    os.makedirs(os.path.join(SCRATCH, 'repos'), exist_ok=True)
    dep = jget('deps.dev dependents mcp 1.27.0', 'https://deps.dev/_/s/pypi/p/mcp/v/1.27.0/dependents')
    print('counts', {k: dep[k] for k in ('totalCount', 'directCount', 'indirectCount')})
    frame = {}
    for d in dep['directSample']:
        frame[d['package']['name']] = dict(package=d['package']['name'], listed_version=d['version'],
                                           in_lh002='', in_frame_a='yes', repo='', repo_via='')
    for rid, pkg, repo in LH002:
        e = frame.setdefault(pkg, dict(package=pkg, listed_version='', in_frame_a='no', repo='', repo_via=''))
        e.update(in_lh002=rid, repo=repo, repo_via='LH002 cohort.md')
    hits, rows = [], []
    for pkg, e in frame.items():
        latest = jget(f'PyPI latest {pkg}', f'https://pypi.org/pypi/{q(pkg)}/json')
        e['latest_version'] = latest['info']['version'] if latest else ''
        listed = None
        if e['listed_version']:
            listed = jget(f'PyPI {pkg} {e["listed_version"]}', f'https://pypi.org/pypi/{q(pkg)}/{q(e["listed_version"])}/json')
        if not e['repo'] and e['listed_version']:
            r, via = repo_from_version(pkg, e['listed_version'])
            if not r and listed:
                r, via = repo_from_pypi(listed)
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
                    git(['clone', '-q', '--filter=blob:none', '--no-checkout', url, d])
                    st = 'cloned'
                except RuntimeError as ex:
                    st = 'failed: ' + str(ex)[:200].replace('\n', ' ')
            else:
                st = 'already cloned'
            log(read_utc=t, source='git over HTTPS', label=f'clone {pkg}', method='git clone --filter=blob:none',
                endpoint=url, http_status='', bytes='', note=st)
            e['clone'] = st.split(':')[0]
            if os.path.exists(os.path.join(d, '.git')) or os.path.exists(os.path.join(d, 'HEAD')):
                head = git(['rev-parse', 'HEAD'], cwd=d).strip()
                pend = git(['rev-list', '-1', f'--before={PERIOD_END}', 'HEAD'], cwd=d).strip()
                for label, c in (('head', head), ('period_end', pend)):
                    if not c:
                        continue
                    e[f'{label}_commit' if label == 'period_end' else 'head_commit'] = c[:10]
                    e[f'{label}_date'] = git(['show', '-s', '--format=%cI', c], cwd=d).strip()
                    paths = [p for p in git(['ls-tree', '-r', '--name-only', c], cwd=d).splitlines() if wanted(p)][:300]
                    e[f'files_{label}'] = len(paths)
                    e[f'dockerfile_{label}'] = ';'.join(p for p in paths if re.match(r'(?i)^(docker|container)file', p.rsplit('/', 1)[-1]) or p.lower().endswith('.dockerfile'))
                    for p in paths:
                        try:
                            txt = git(['show', f'{c}:{p}'], cwd=d)
                        except RuntimeError:
                            continue
                        scan_text(txt, f'git {label} {c[:10]}', hits, pkg, p)
        rows.append(e)
        print(pkg, e['repo'], e.get('clone'), e.get('dockerfile_head'))
    write_csv('candidate_frame.csv', rows, ['package', 'in_lh002', 'in_frame_a', 'listed_version', 'latest_version',
                                            'repo', 'repo_via', 'clone', 'head_commit', 'head_date', 'period_end_commit',
                                            'period_end_date', 'files_head', 'files_period_end', 'dockerfile_head',
                                            'dockerfile_period_end'])
    write_csv('candidate_hits.csv', hits, ['package', 'where', 'file', 'line', 'text'])


if __name__ == '__main__':
    main()
