# LH007 sources

Every network request the scripts made is in data/read_log.csv with its UTC time, endpoint, status and bytes (4,389 rows, 21:15:38 to 21:52:06 UTC on 26 September 2026; one, the clone of mcp-atlassian, was added by hand afterwards). Blobs that git fetched on demand from the blobless clones, when a file at a commit was read, are not logged request by request. Signed query strings that registries add when they redirect a blob download were removed from the logged endpoints; no token value was written anywhere. The two documentation pages below were fetched with curl and are not in the log.

## Pages read

| id | page | publisher; date the page gives | read (UTC, 26 September 2026) |
| --- | --- | --- | --- |
| D1 | https://docs.docker.com/docker-hub/usage/ | Docker; no date recorded | 21:16:51 |
| D2 | https://docs.docker.com/docker-hub/usage/pulls/ | Docker; no date recorded | 21:16:52 |

D1 and D2 say what LH006 quoted from them (studies/LH006/sources.md, D1 and D2, read 18:26 the same day): "100 per IPv4 address or IPv6 /64 subnet" per six hours for unauthenticated users, and the rate-limit headers "are returned on both GET and HEAD requests. Using GET emulates a real pull and counts towards the limit. Using HEAD won't." No documentation of public.ecr.aws's or ghcr.io's anonymous limits was read.

## Records read

| id | source | what it gave | observation window of the record | read (UTC) |
| --- | --- | --- | --- | --- |
| S1 | PyPI JSON API, https://pypi.org/pypi/<package>/json and /<version>/json | release times of `mcp` and `fastmcp` (the choice); each screened package's description and project links; `requires_dist` of every release of each sampled package from 1 April to 15 August 2026 | releases as published | 21:15:38 to 21:46:33 |
| S2 | Open Source Insights, https://deps.dev/_/s/pypi/p/mcp/v/<version>/dependents; https://api.deps.dev/v3alpha/systems/pypi/packages/mcp/versions/<version>:dependents; https://api.deps.dev/v3/systems/pypi/packages/<name>/versions/<version> | dependents counts and the listed direct dependents of `mcp` 1.27.2, 1.28.0 and 1.28.1 (the frame); each package's source repository | Open Source Insights' state on the read day; its method for listing dependents was not read | 21:15:50 to 21:21:15 |
| S3 | git over HTTPS (blobless clones of 75 repositories, 12 more refused, and of github.com/sooperset/mcp-atlassian, named by its image's source label) | Dockerfiles, workflows, READMEs at two commits; the Dockerfile and manifests at each image's build commit; every commit touching a manifest or lockfile from 1 April to 15 August | the repositories' histories as served on the read day | clones 21:19:04 to 21:21:15 and 21:36:52; files read from them to about 21:47 |
| S4 | ghcr.io, OCI distribution API with anonymous tokens from ghcr.io/token | tag lists, manifests, configurations and layers of 14 image repositories; 401 for three others | the registry's current tags; no tag history | 21:26:16 to 21:34:52 |
| S5 | Docker Hub: hub.docker.com v2 tag API and registry-1.docker.io with anonymous tokens from auth.docker.io | tag records (push times, digests) of seven repositories; 25 counted manifest GETs; configurations and 12 layer streams; rate-limit headers | current tags, at most the newest 1,000 per repository; no tag history | 21:26:17 to 21:52:06 |
| S6 | public.ecr.aws, OCI distribution API with anonymous tokens | tags, manifests, configurations and layers of mcp-proxy-for-aws; 11 answers of 429 before requests were paced to one every 1.2 seconds | current tags | 21:26:19 to 21:34:42 |
| S7 | registry.intsig.net | 403 to an unauthenticated `/v2/` | | 21:26:20 and 21:32:08 |
| S8 | ClickPy, ClickHouse's public SQL service (https://sql-clickhouse.clickhouse.com/?user=demo), table `pypi.pypi_downloads_per_day_by_version` | daily `mcp` downloads by version, 19 May to 28 July 2026 | ClickHouse's copy of PyPI's download log, which it re-ingests when it finds gaps (LH005, sources.md L4) | 21:49:04 |
| S9 | OSV API, https://api.osv.dev/v1/query, for `mcp` 1.28.0 | GHSA-vj7q-gjh5-988w (aliases CVE-2026-59950, PYSEC-2026-3483), severity HIGH, published 2026-07-16T20:14:34Z, fixed in 1.28.1: "MCP Python SDK: WebSocket server transport does not support Host/Origin validation" | OSV's record, modified 2026-09-10 | 21:49:34 |
| S9a | OSV API, the same endpoint, for `mcp` with no version (queried by the release review, notes/R-0007.md; data/osv_mcp_all.csv) | six GHSA advisories against `mcp`, three of them published on 16 July 2026: GHSA-hvrp-rf83-w775 at 19:56:12Z and GHSA-jpw9-pfvf-9f58 at 19:58:53Z, both fixed in 1.27.2, and GHSA-vj7q-gjh5-988w at 20:14:34Z. GitHub's own advisory pages and API answered 403 to anonymous requests through the session's proxy and were not read | OSV's records as modified to 2026-09-10 | 22:10 |

## Earlier Lighthouse records used

- studies/LH006/LH006.md version 0.2, brief.md and scripts/ (method and code adapted here), at commit 3328692.
- studies/LH005/LH005.md version 0.2 (the ClickPy query form and the read of ClickPy's reliability), at commit 3328692.
