#!/usr/bin/env python3
"""LH007 step 4: for every image whose configuration was read (data/image_configs.csv), the commit it
was built from and what that commit says about installing mcp. The commit is the configuration's
org.opencontainers.image.revision label where the clone holds it ('label'), else the default branch's
last first-parent commit at or before the build time ('nearest before build', weaker). At that commit:
the Dockerfile the publishing workflow names, its install lines, and the mcp specifier and locked
version in the project's manifests. Writes data/image_builds.csv. Reads only local blobless clones
(git fetches the few blobs it needs over HTTPS; each clone is logged in read_log.csv by
select_candidates.py, except mcp-atlassian's, cloned from its image's source label and logged here)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv, git, SCRATCH

REPO = {  # image repository: (repository, Dockerfile path used by the publishing workflow)
    'ghcr.io/startreedata/mcp-pinot': ('github.com/startreedata/mcp-pinot', 'Dockerfile'),
    'ghcr.io/n24q02m/better-telegram-mcp': ('github.com/n24q02m/better-telegram-mcp', 'Dockerfile'),
    'ghcr.io/argonne-lcf/chemgraph': ('github.com/argonne-lcf/chemgraph', 'Dockerfile'),
    'ghcr.io/sooperset/mcp-atlassian': ('github.com/sooperset/mcp-atlassian', 'Dockerfile'),
    'public.ecr.aws/mcp-proxy-for-aws/mcp-proxy-for-aws': ('github.com/aws/mcp-proxy-for-aws', 'Dockerfile'),
    'ghcr.io/dhyansraj/mcp-mesh/python-runtime': ('github.com/dhyansraj/mcp-mesh', 'packaging/docker/python-runtime.Dockerfile'),
    'ghcr.io/oraios/serena': ('github.com/oraios/serena', 'Dockerfile'),
    'ghcr.io/the-openroad-project/openroad-mcp': ('github.com/the-openroad-project/openroad-mcp', 'Dockerfile'),
    'ghcr.io/williamzujkowski/mcp-standards-server': ('github.com/williamzujkowski/mcp-standards-server', 'Dockerfile'),
    'ghcr.io/githubsecuritylab/seclab-taskflow-agent': ('github.com/githubsecuritylab/seclab-taskflow-agent', 'docker/Dockerfile'),
    'ghcr.io/gradion-ai/hybrid-groups': ('github.com/gradion-ai/hybrid-groups', 'docker/Dockerfile'),
    'ghcr.io/alation/alation-ai-agent-sdk/alation-mcp-server': ('github.com/alation/alation-ai-agent-sdk', 'python/dist-mcp/Dockerfile'),
    'ghcr.io/aurapro-official/aurapro-webui': ('github.com/aurapro-official/aurapro-webui', 'Dockerfile'),
    'docker.io/langflowai/langflow': ('github.com/langflow-ai/langflow', 'docker/build_and_push.Dockerfile'),
    'docker.io/langflowai/langflow-nightly': ('github.com/langflow-ai/langflow', 'docker/build_and_push.Dockerfile'),
    'docker.io/browseruse/browseruse': ('github.com/browser-use/browser-use', 'Dockerfile'),
    'docker.io/salehmir/jesse': ('github.com/jesse-ai/jesse', 'Dockerfile'),
    'docker.io/cloudsmith/cloudsmith-cli': ('github.com/cloudsmith-io/cloudsmith-cli', 'Dockerfile'),
    'docker.io/omicsdatascience/modulector': ('github.com/omics-datascience/modulector', 'Dockerfile'),
    'docker.io/aurite/aurite-agents': ('github.com/aurite-ai/aurite-agents', 'Dockerfile'),
}
INSTALL = re.compile(r'\b(pip3?|uv|poetry|pdm|pipx)\b.*\b(install|sync|add)\b|COPY .*(uv\.lock|poetry\.lock|requirements|pyproject|constraints|\.venv)|--from=.*(venv|site-packages)', re.I)
MANIFESTS = re.compile(r'^(pyproject\.toml|requirements[^/]*\.txt|backend/requirements\.txt|src/backend/base/pyproject\.toml|python/dist-mcp/pyproject\.toml|packages/[^/]+/pyproject\.toml|src/[^/]+/pyproject\.toml)$')


def mcp_spec(txt):
    m = re.search(r'''(?m)^\s*["']?\bmcp(\[[^\]]*\])?\s*((?:[=<>!~]=?|===)\s*[0-9][^"',;\s\]#]*(?:\s*,\s*[=<>!~]=?\s*[0-9][^"',;\s\]#]*)*)''', txt)
    if m:
        return m.group(2).replace(' ', '')
    return 'unversioned' if re.search(r'''(?m)^\s*["']mcp(\[[^\]]*\])?["']|^\s*mcp\s*$''', txt) else ''


def lock_version(txt):
    m = re.search(r'\[\[package\]\]\s*\nname = "mcp"\s*\nversion = "([^"]+)"', txt)
    return m.group(1) if m else ''


def main():
    rows = []
    cfgs = read_csv('image_configs.csv')
    for c in cfgs:
        img = c['image']
        repo, dfile = REPO.get(img, ('', ''))
        out = dict(image=img, index_digest=c['index_digest'], created=c['created'], label_revision=c['label_revision'],
                   repo=repo, dockerfile=dfile, commit='', commit_basis='', commit_utc='', dockerfile_install_lines='',
                   manifest_specs='', lock_files='', uv_lock_mcp='', poetry_lock_mcp='')
        d = os.path.join(SCRATCH, 'repos', repo.replace('/', '__')) if repo else ''
        if not d or not os.path.exists(d):
            rows.append(out)
            continue
        sha, basis = '', ''
        if c['label_revision']:
            try:
                sha = git(['rev-parse', '--verify', '-q', c['label_revision'] + '^{commit}'], cwd=d).strip()
                basis = 'revision label'
            except RuntimeError:
                sha = ''
        if not sha and c['created']:
            sha = git(['rev-list', '-1', '--first-parent', f'--before={c["created"]}', 'HEAD'], cwd=d).strip()
            basis = 'nearest before build (weaker)'
        if not sha:
            rows.append(out)
            continue
        out.update(commit=sha[:10], commit_basis=basis, commit_utc=git(['show', '-s', '--format=%cI', sha], cwd=d).strip())
        tree = git(['ls-tree', '-r', '--name-only', sha], cwd=d).splitlines()
        if dfile in tree:
            txt = git(['show', f'{sha}:{dfile}'], cwd=d)
            lines = [re.sub(r'\s+', ' ', l.strip()) for l in re.sub(r'\\\n', ' ', txt).splitlines()
                     if INSTALL.search(l) and not l.strip().startswith('#')]
            out['dockerfile_install_lines'] = ' || '.join(lines)[:1200]
        else:
            out['dockerfile_install_lines'] = f'{dfile} absent at this commit'
        specs = []
        for p in tree:
            if MANIFESTS.match(p):
                s = mcp_spec(git(['show', f'{sha}:{p}'], cwd=d))
                if s:
                    specs.append(f'{p}: mcp{s}' if s != 'unversioned' else f'{p}: mcp (no version)')
        out['manifest_specs'] = '; '.join(specs)
        locks = sorted([p for p in tree if p.rsplit('/', 1)[-1] in ('uv.lock', 'poetry.lock', 'pdm.lock') and p.count('/') <= 2],
                       key=lambda p: (p.count('/'), p))  # the root lockfile first
        out['lock_files'] = ';'.join(locks)
        for p in locks:
            v = lock_version(git(['show', f'{sha}:{p}'], cwd=d))
            if v and p.endswith('uv.lock') and not out['uv_lock_mcp']:
                out['uv_lock_mcp'] = f'{p}={v}'
            if v and p.endswith('poetry.lock') and not out['poetry_lock_mcp']:
                out['poetry_lock_mcp'] = f'{p}={v}'
        rows.append(out)
        print(img.split('/')[-1], c['created'][:10], basis[:8], out['manifest_specs'][:80], out['uv_lock_mcp'])
    write_csv('image_builds.csv', rows, list(rows[0].keys()))


if __name__ == '__main__':
    main()
