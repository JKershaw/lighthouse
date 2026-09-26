#!/usr/bin/env python3
"""LH002: Open Source Insights readings for the cohort's packages.

For each package: PyPI releases inside the window (publication times), the
version current at window start and at window end, and the dependency graph
Open Source Insights resolves for each of those versions (typed DIRECT or
INDIRECT, with the requirement on each edge). Also the SOURCE_REPO relation and
its provenance, which types the package-to-repository link.

Usage: python3 collect_depsdev.py <scratch_dir> <study_dir>
"""
import csv, json, os, sys, time, urllib.parse, urllib.request

S, STUDY = sys.argv[1:3]
RAW = os.path.join(S, 'raw', 'depsdev'); os.makedirs(RAW, exist_ok=True)
DATA = os.path.join(STUDY, 'data')
W0, W1 = '2026-03-26T00:00:00Z', '2026-04-23T00:00:00Z'
COHORT = [('R00', 'mcp'), ('R01', 'agentcrew-ai'), ('R02', 'databricks-tellr-app'), ('R03', 'lean-lsp-mcp'),
          ('R04', 'pyp6xer-mcp'), ('R05', 'serena-agent'), ('R06', 'dartlab'), ('R07', 'mistral-vibe'),
          ('R08', 'octobot'), ('R09', 'jesse')]
NAMES = {n: r for r, n in COHORT}
COHORT_REPOS = {'github.com/' + l.split()[1].lower() for l in open(os.path.join(S, 'repos.txt')) if l.strip()}
q = lambda s: urllib.parse.quote(s, safe='')

def get(url, path):
    if not os.path.exists(path):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                open(path, 'wb').write(r.read())
        except urllib.error.HTTPError as e:
            json.dump({'_http_error': e.code}, open(path, 'w'))
        time.sleep(0.2)
    return json.load(open(path))

releases, graph_rows, repo_links, current = [], [], [], {}
for rid, name in COHORT:
    p = get(f'https://api.deps.dev/v3/systems/pypi/packages/{q(name)}', os.path.join(RAW, f'pkg-{name}.json'))
    vs = sorted((v['publishedAt'], v['versionKey']['version']) for v in p['versions'] if v.get('publishedAt'))
    for t, v in vs:
        if W0 <= t < W1:
            releases.append(dict(repo=rid, package=name, version=v, published=t))
    for label, t in (('start', W0), ('end', W1)):
        before = [v for tt, v in vs if tt < t]
        ver = before[-1] if before else None
        current[(rid, label)] = ver
        if not ver:
            graph_rows.append(dict(repo=rid, package=name, at=label, version='', mcp_relation='', mcp_resolved='',
                                   mcp_requirement='', nodes=0, direct=0, cohort_nodes='', error='no version before this time'))
            continue
        vj = get(f'https://api.deps.dev/v3/systems/pypi/packages/{q(name)}/versions/{q(ver)}',
                 os.path.join(RAW, f'ver-{name}-{ver}.json'))
        if label == 'end':
            for rp in vj.get('relatedProjects', []):
                if rp['relationType'] == 'SOURCE_REPO':
                    proj = rp['projectKey']['id']
                    if rid != 'R00' and proj.lower() not in COHORT_REPOS:
                        # a repository outside the cohort: publish host and name, withhold the account
                        parts = proj.split('/')
                        proj = f"{parts[0]}/(account withheld)/{parts[-1]}" if len(parts) >= 3 else proj
                    repo_links.append(dict(repo=rid, package=name, version=ver, project=proj,
                                           provenance=rp['relationProvenance']))
        g = get(f'https://api.deps.dev/v3/systems/pypi/packages/{q(name)}/versions/{q(ver)}:dependencies',
                os.path.join(RAW, f'deps-{name}-{ver}.json'))
        nodes = g.get('nodes', [])
        mcp_idx = [i for i, n in enumerate(nodes) if n['versionKey']['name'] == 'mcp']
        req = ''
        for e in g.get('edges', []):
            if e['toNode'] in mcp_idx and e['fromNode'] == 0:
                req = e.get('requirement', '')
        cohort_nodes = sorted({f"{NAMES[n['versionKey']['name']]}:{n['versionKey']['version']}:{n['relation']}"
                               for n in nodes[1:] if n['versionKey']['name'] in NAMES})
        graph_rows.append(dict(repo=rid, package=name, at=label, version=ver,
                               mcp_relation=nodes[mcp_idx[0]]['relation'] if mcp_idx else '',
                               mcp_resolved=nodes[mcp_idx[0]]['versionKey']['version'] if mcp_idx else '',
                               mcp_requirement=req, nodes=len(nodes),
                               direct=sum(1 for n in nodes if n['relation'] == 'DIRECT'),
                               cohort_nodes=';'.join(cohort_nodes), error=g.get('error', '') or g.get('_http_error', '')))

def write(name, rows):
    with open(os.path.join(DATA, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

write('pypi_releases_in_window.csv', releases)
write('depsdev_graphs_window_start_end.csv', graph_rows)
write('depsdev_source_repo_links.csv', repo_links)
for r in graph_rows: print(r)
print(); [print(r) for r in releases]; print(); [print(r) for r in repo_links]
