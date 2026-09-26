#!/usr/bin/env python3
"""LH007 step 2: the qualification decision for every screened package in data/candidate_frame.csv,
made by reading data/candidate_hits.csv, data/candidate_images.csv and, where a line needed context,
the named file in the clone (named in the reason). Decisions were made before any registry was read.
Writes data/candidates.csv and data/sample.csv (the qualifying image repositories in hash order, up to
24, one row per image repository). No network access."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import read_csv, write_csv

SAMPLE_MAX = 24
REPUBLISH = 'a republish of another project under a prefixed name; the image named is that project\'s, not published by this package'
# package: (qualifies, image repository, where named, reason)
D = {
    'langflow-base': ('yes', 'ghcr.io/langflow-ai/langflow', 'repository', '.github/workflows/docker-build-v2.yml pushes ghcr.io/langflow-ai/langflow (and docker.io/langflowai/langflow) from the repository that builds langflow-base; ghcr.io copy read (brief: prefer ghcr.io)'),
    'langflow-base-nightly': ('yes', 'ghcr.io/langflow-ai/langflow-nightly', 'repository', 'the same repository\'s workflows push ghcr.io/langflow-ai/langflow-nightly (and docker.io/langflowai/langflow-nightly) from the nightly builds; ghcr.io copy read'),
    'browser-use': ('yes', 'ghcr.io/browser-use/browser-use', 'repository', '.github/workflows/docker.yml, build-push-action with images ghcr.io/browser-use/browser-use (present at both commits)'),
    'aurite': ('yes', 'docker.io/aurite/aurite-agents', 'repository', '.github/workflows/docker-publish.yml pushes REGISTRY docker.io, IMAGE_NAME aurite/aurite-agents'),
    'cognirepo': ('yes', 'ghcr.io/ashlesh-t/cognirepo', 'repository', '.github/workflows/docker.yml pushes ghcr.io/${{ github.repository }} (LH006 found this package answering 401 at ghcr.io/token)'),
    'mcp-pinot-server': ('yes', 'ghcr.io/startreedata/mcp-pinot', 'repository', '.github/workflows/release.yml pushes ghcr.io/${{ github.repository }}:<version> and says "Docker image published to ghcr.io/..."'),
    'mcp-standards-server': ('yes', 'ghcr.io/williamzujkowski/mcp-standards-server', 'repository', '.github/workflows/release.yml pushes ghcr.io/williamzujkowski/mcp-standards-server'),
    'jesse': ('yes', 'docker.io/salehmir/jesse', 'repository and PyPI description', '.github/workflows/docker-publish.yml pushes salehmir/jesse on v* tags; README and PyPI link hub.docker.com/r/salehmir/jesse (as LH006)'),
    'seclab-taskflow-agent': ('yes', 'ghcr.io/githubsecuritylab/seclab-taskflow-agent', 'repository and PyPI description', 'README and PyPI description run ghcr.io/githubsecuritylab/seclab-taskflow-agent; release.yml attests the oci image'),
    'cloudsmith-cli': ('yes', 'docker.io/cloudsmith/cloudsmith-cli', 'repository', '.github/workflows/release.yml at the period-end commit pushes cloudsmith/cloudsmith-cli (Docker Hub) and docker.cloudsmith.io; the head commit moves image publishing into variables'),
    'better-telegram-mcp': ('yes', 'ghcr.io/n24q02m/better-telegram-mcp', 'repository', '.github/workflows/cd.yml pushes ghcr.io/n24q02m/better-telegram-mcp; server.json names an OCI package'),
    'hybrid-groups': ('yes', 'ghcr.io/gradion-ai/hybrid-groups', 'repository', '.github/workflows/docker.yml pushes ghcr.io/gradion-ai/hybrid-groups'),
    'chemgraph': ('yes', 'ghcr.io/argonne-lcf/chemgraph', 'repository', '.github/workflows/ghcr-publish.yml pushes ghcr.io/${owner}/chemgraph'),
    'modulector-sdk': ('yes', 'docker.io/omicsdatascience/modulector', 'repository', '.github/workflows/prod-env-wf.yml pushes omicsdatascience/modulector; the image is built from the repository whose root project requires mcp==1.27.2 (sdk/ holds the SDK package); image of the repository, not of the SDK distribution alone'),
    'mcp-atlassian': ('yes', 'ghcr.io/sooperset/mcp-atlassian', 'PyPI description', 'no repository link in Open Source Insights or PyPI; the description gives docker pull ghcr.io/sooperset/mcp-atlassian:latest, published by the same author as the package'),
    'mcp-proxy-for-aws-cli': ('yes', 'public.ecr.aws/mcp-proxy-for-aws/mcp-proxy-for-aws', 'repository', '.github/workflows/ecr-publish-on-release.yml pushes to public ECR alias mcp-proxy-for-aws; the Dockerfile runs pip install mcp-proxy-for-aws-cli, the package itself'),
    'alation-ai-agent-mcp': ('yes', 'ghcr.io/alation/alation-ai-agent-sdk/alation-mcp-server', 'repository', '.github/workflows/build-docker-image.yml pushes ghcr.io/alation/alation-ai-agent-sdk/alation-mcp-server'),
    'intsig-mcp-atlassian': ('yes', 'registry.intsig.net/confluence-mcp/confluence-mcp', 'PyPI description', 'the description gives docker pull registry.intsig.net/confluence-mcp/confluence-mcp:latest, a registry of the package author\'s organisation'),
    'mcp-mesh': ('yes', 'ghcr.io/dhyansraj/mcp-mesh/python-runtime', 'repository', '.github/workflows/release.yml pushes python-runtime images (packaging/docker/python-runtime.Dockerfile, pip install mcp-mesh==VERSION with a constraints file) to mcpmesh/ on Docker Hub and ghcr.io/dhyansraj/mcp-mesh/; ghcr.io copy read. Its registry and typescript-runtime images do not install the Python package'),
    'serena-agent': ('yes', 'ghcr.io/oraios/serena', 'repository', '.github/workflows/docker.yml pushes ghcr.io/${{ github.repository }} (as LH006)'),
    'openroad-mcp': ('yes', 'ghcr.io/the-openroad-project/openroad-mcp', 'repository', '.github/workflows/docker-publish.yml pushes ghcr.io/the-openroad-project/openroad-mcp; server.json names an OCI package'),
    'aurapro-webui': ('yes', 'ghcr.io/aurapro-official/aurapro-webui', 'repository', '.github/workflows/docker.yaml pushes ghcr.io/${GITHUB_REPOSITORY,,}'),
    # not qualifying, with reasons
    'aevrin-scanner-core': ('no', '', 'repository', 'docker run of a sandbox container built locally; no published image named'),
    'aurapro-ui': ('no', '', 'PyPI description', 'names ghcr.io/open-webui/open-webui, the image of the project it is derived from, not one it publishes'),
    'gfg-mcp-atlassian': ('no', '', 'PyPI description', 'names ghcr.io/sooperset/mcp-atlassian, the upstream project\'s image, not one it publishes'),
    'iflow-mcp-kaluso-nolodjska-ai-team-mcp': ('no', '', 'repository', REPUBLISH),
    'iflow-mcp-pdfmathtranslate-pdf2zh': ('no', '', 'repository', REPUBLISH),
    'iflow-mcp-topoteretes-cognee-mcp': ('no', '', 'PyPI description', REPUBLISH),
    'iflow-mcp-mcp-server-twelve-data': ('no', '', 'PyPI description', 'docker run of a locally built tag; no published image named'),
    'async-hermes-agent': ('no', '', 'repository', 'a fork whose workflow at the period-end commit names nousresearch/hermes-agent, the upstream image'),
    'elasticsearch-mcp-server-es9': ('no', '', 'PyPI description', 'names ghcr.io/cr7258/elasticsearch-mcp-server, the image of the sibling distribution elasticsearch-mcp-server; no repository or author in the metadata ties this distribution to it'),
    'elasticsearch-mcp-server-es7': ('no', '', 'PyPI description', 'as elasticsearch-mcp-server-es9'),
    'mcpm': ('no', '', 'repository', 'the only pushing workflow (frp.yml) publishes frpc and frps tunnel images, which do not install mcpm'),
    'mcp-behaviour-guard': ('no', '', 'repository', 'ci.yml builds with push: false; no published image named'),
    'secure-mcp-gateway': ('no', '', 'repository', 'workflows push to a private Amazon ECR with account credentials; README runs locally built images; no public image named'),
    'aimeat-crewai': ('no', '', 'repository', 'service images (postgres, openhands) only'),
    'quellgeist': ('no', '', 'repository', 'a comment about a third-party action image and an ollama service image only'),
    'phpipam-mcp-server': ('no', '', 'repository', 'compose file names a locally built tag; no published image named'),
    'mcp-instana': ('no', '', 'PyPI description', 'docker run of a locally built tag; no published image named'),
    'mcp-quickbooks': ('no', '', 'PyPI description', 'docker run of a locally built tag; no published image named'),
    'azurefunctions-agents-runtime': ('no', '', 'PyPI description', 'an azurite storage emulator container only'),
    'lean-lsp-mcp': ('no', '', 'repository', 'Dockerfile, no published image named (as LH006)'),
}


def main():
    frame = read_csv('candidate_frame.csv')
    hits = collections.Counter(h['package'] for h in read_csv('candidate_hits.csv'))
    out = []
    for f in frame:
        p = f['package']
        if p in D:
            q, img, where, why = D[p]
        elif f['clone'] == 'failed':
            q, img, where, why = 'no', '', '', 'repository could not be cloned (' + f['repo'] + '); PyPI metadata names no image'
        elif not f['repo']:
            q, img, where, why = 'no', '', 'PyPI description', 'no repository link in Open Source Insights or PyPI; PyPI metadata names no image'
        else:
            q, img, where, why = 'no', '', '', ('Dockerfile, no published image named: ' + f['dockerfile_head'][:120]) if f['dockerfile_head'] else 'no image reference in the files read or in PyPI metadata'
        out.append(dict(hash_rank=f['hash_rank'], package=p, in_127_2=f['in_1.27.2'], in_128_0=f['in_1.28.0'],
                        in_128_1=f['in_1.28.1'], repo=f['repo'], clone=f['clone'],
                        dockerfile_at_head='yes' if f['dockerfile_head'] else 'no',
                        dockerfile_at_period_end='yes' if f['dockerfile_period_end'] else 'no',
                        matching_lines=hits.get(p, 0), qualifies=q, image_repository=img, named_in=where, reason=why))
    write_csv('candidates.csv', out)
    seen, sample = set(), []
    for o in sorted(out, key=lambda o: int(o['hash_rank'])):
        if o['qualifies'] == 'yes' and o['image_repository'] not in seen:
            seen.add(o['image_repository'])
            host, name = o['image_repository'].split('/', 1)
            sample.append(dict(sample_rank=len(sample) + 1, hash_rank=o['hash_rank'], package=o['package'], repo=o['repo'],
                               registry=host, image=name, sampled='yes' if len(sample) < SAMPLE_MAX else 'no (beyond 24)'))
    write_csv('sample.csv', sample)
    print(collections.Counter(o['qualifies'] for o in out), collections.Counter(s['registry'] for s in sample), len(sample))


if __name__ == '__main__':
    main()
