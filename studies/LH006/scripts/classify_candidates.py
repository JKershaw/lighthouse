#!/usr/bin/env python3
"""LH006 step 2: the qualification decision for every candidate in data/candidate_frame.csv,
made by reading data/candidate_hits.csv and, where a hit needed context, the named file in the
clone (the file is named in the reason). Decisions were made before any registry was read.
Writes data/candidates.csv. No network access."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv

# package: (qualifies, image repository, where named, reason)
D = {
    'agentcrew-ai': ('yes', 'docker.io/daltonnyx/agentcrew', 'repository',
                     '.github/workflows/docker-build-publish.yml builds linux/amd64 and linux/arm64 and pushes to docker.io/daltonnyx/agentcrew on version tags (present at both commits read)'),
    'serena-agent': ('yes', 'ghcr.io/oraios/serena', 'repository',
                     '.github/workflows/docker.yml pushes ghcr.io/${{ github.repository }} on pushes to main and v* tags (present at both commits read)'),
    'octobot': ('yes', 'docker.io/drakkarsoftware/octobot', 'repository and PyPI description',
                'README and PyPI description give docker run drakkarsoftware/octobot:stable; .github/workflows/main.yml builds and pushes with docker/build-push-action'),
    'jesse': ('yes', 'docker.io/salehmir/jesse', 'repository and PyPI description',
              '.github/workflows/docker-publish.yml pushes IMAGE: salehmir/jesse on v* tags; the workflow was added on 2026-05-30, after the period, and is absent at the period-end commit; README and PyPI description link hub.docker.com/r/salehmir/jesse. LH002 found no mcp requirement in jesse\'s git in the window'),
    'cognirepo': ('yes', 'ghcr.io/ashlesh-t/cognirepo', 'repository',
                  '.github/workflows/docker.yml, added 2026-03-28, pushes ghcr.io/${{ github.repository }} on published releases and on manual dispatch'),
    'mcp-snowflake-server-nsp': ('yes', 'docker.io/nsphung/mcp-snowflake-server-nsp', 'repository and PyPI description',
                                 'README and PyPI description: "The image is published on Docker Hub", docker pull nsphung/mcp-snowflake-server-nsp; publish.yml pushes it; server.json names it as an OCI package'),
    'keboola-mcp-server': ('yes', 'docker.io/keboola/mcp-server', 'PyPI description',
                           'no repository link in Open Source Insights or PyPI; the PyPI description gives docker pull keboola/mcp-server:latest'),
    'hal0ai': ('no', '', 'repository',
               'names published images (ghcr.io/hal0ai/hal0-toolbox-*), but they are model-server runtime toolboxes; their Dockerfiles (packaging/toolbox/*.Dockerfile) do not install the hal0ai package or mcp. Excluded as not an image of the package'),
    'lean-lsp-mcp': ('no', '', 'repository',
                     'Dockerfile, no published image named: the README runs lean-lsp-mcp:containerized, a locally built tag'),
    'pyp6xer-mcp': ('no', '', 'repository', 'Dockerfile, no published image named (the only registry reference is the uv base image)'),
    'uk-legal-mcp': ('no', '', 'repository', 'Dockerfile, no published image named: README and workflow run a locally built uk-legal-mcp tag'),
    'uk-due-diligence-mcp': ('no', '', 'repository', 'Dockerfile, no published image named (the only registry reference is the uv base image)'),
    'uk-business-mcp': ('no', '', 'repository', 'Dockerfile, no published image named'),
    'govuk-mcp': ('no', '', 'repository', 'Dockerfile, no published image named'),
    'audiagentic': ('no', '', 'repository', 'test Dockerfiles only; ci-tests.yml builds with load: true and no push; README runs a local test container'),
    'databricks-tellr-app': ('no', '', 'repository', 'no image of its own; a postgres service image in a test workflow'),
    'mistral-vibe': ('no', '', 'repository', 'no image of its own; manylinux build containers in release workflows'),
    'agentbrain-mcp': ('no', '', '', 'repository named by Open Source Insights could not be cloned (the server asked for credentials: private, renamed or deleted); PyPI metadata names no image'),
}


def main():
    frame = read_csv('candidate_frame.csv')
    hits = collections.Counter(h['package'] for h in read_csv('candidate_hits.csv'))
    out = []
    for f in frame:
        p = f['package']
        if p in D:
            q, img, where, why = D[p]
        elif not f['repo']:
            q, img, where, why = 'no', '', 'PyPI description', 'no repository link in Open Source Insights or PyPI; PyPI metadata names no image'
        else:
            q, img, where, why = 'no', '', '', 'no image reference in the files read or in PyPI metadata' + (
                '; Dockerfile present: ' + f['dockerfile_head'] if f['dockerfile_head'] else '')
        out.append(dict(package=p, lh002_id=f['in_lh002'], in_frame_a=f['in_frame_a'], repo=f['repo'],
                        dockerfile_at_head='yes' if f['dockerfile_head'] else 'no',
                        dockerfile_at_period_end='yes' if f['dockerfile_period_end'] else 'no',
                        matching_lines=hits.get(p, 0), qualifies=q, image_repository=img, named_in=where, reason=why))
    write_csv('candidates.csv', out)
    print(collections.Counter(o['qualifies'] for o in out), sum(1 for o in out if o['dockerfile_at_head'] == 'yes'))


if __name__ == '__main__':
    main()
