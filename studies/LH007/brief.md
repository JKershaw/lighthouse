# LH007 study brief

**study:** LH007
**edition:** 0.1
**date opened:** 2026-09-26, about 21:18 UTC, written after reading PyPI's release list for `mcp` and `fastmcp`, Open Source Insights' dependents counts for four `mcp` versions and Docker Hub's usage pages (the reads behind the choice below, in data/read_log.csv and sources.md), and before any dependents list was screened or any tag list, manifest, configuration or layer was read
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driver session for issue #8 (LH007), from the design in programme.md
**grounded at:** repository commit 3328692

## Question

When a widely used library releases, how much of the software built on it installs the new version because an installer resolved an open range, and how much waits for a maintainer to move a pin or lockfile? LH005 could infer the two populations only from installer mixes in PyPI's download log; LH006 saw both in six projects' images and found one (agentcrew) whose images held a release sixteen days before its own pin moved, because its Dockerfile installs from an open range. This study takes a sample of the published images of one release's dependents, fixed by a rule before any image is read, classifies each image by how it installs, reads the installed version from its layers, and reports, by class, the share holding the new release by days since the release.

## Choice of library and release

**Rule.** The library is `mcp`, the Model Context Protocol SDK, for continuity with LH002, LH005 and LH006 and because the same download tables (ClickPy) can be set beside the images. The release is the most recent minor or major release of `mcp` (not a pre-release, not a patch) that is at least 28 days old on 26 September 2026 and after which no other minor or major release was published within 28 days, so that images built in the four weeks after it can only hold it (or its patches) or an older version.

**Applied** (observation, PyPI JSON read at 21:15:38 UTC, data/choice_releases.csv): 1.30.0 (7 September) is 19 days old. 1.29.0 and 2.0.0 were published four minutes apart on 28 July, so neither is followed by a clean four weeks and a range without an upper bound would resolve to a new major version; that confound is excluded. **1.28.0, published 2026-06-16T21:37:16Z**, is followed by 1.28.1 (26 June, a patch) and no other minor or major release until 28 July (42 days). Pre-releases 2.0.0a2, a3 and b1 were published inside the period; pip and uv do not select a pre-release unless a specifier names one, so an image holding a 2.0.0 pre-release is recorded as such, not as the new release.

**The new release** means `mcp` 1.28.0 or its patch 1.28.1. An image "holds the new release" if its installed `mcp` is 1.28.x. Images outside the period that hold a later version (1.29 or 2.x) are recorded as later, not as the new release.

`fastmcp` was considered and not chosen: it released 30 versions between May and September 2026, several within days of each other, so no single release has four clean weeks after it.

## Scope

- **Period.** Four weeks either side of the release: 2026-05-19T21:37:16Z to 2026-07-14T21:37:16Z, with the nearest image outside the period on each side. Day 0 is the release instant; "days since release" is build time minus 2026-06-16T21:37:16Z.
- **Frame.** The direct dependents that Open Source Insights lists, at https://deps.dev/_/s/pypi/p/mcp/v/<version>/dependents, for three versions: 1.27.2 (the release before, published 29 May), 1.28.0 and 1.28.1. The dependents of 1.28.x alone are selected on having taken the new release; adding the dependents of 1.27.2 brings in software built on `mcp` just before the release whether or not it later moved. Each package's membership of each list is recorded, and results are reported for each. The endpoint's `directSample` holds at most 100 entries (seen for 1.27.2, 146 direct, and 1.28.1, 122 direct, when the counts were read at 21:15:50); the entries it does not return are the frame's unread part and are stated. The v3 API (`api.deps.dev/v3`) is read for each package's source repository, as in LH002 and LH006.
- **Observation.** Of registry records, image contents, git and PyPI as they stand on 26 September 2026, two and a half to four months after the builds. Not of anything that ran.

## Interpretation boundary

As LH006: an image records an installation made to be run; it is not a run, and nothing in a registry says whether, where or how often it was started. A tag is a movable name and neither registry's anonymous interface keeps what a tag named before, so an image read today may not be the one a tag named then; images that only ever carried a moving tag and were replaced are invisible. A sample of the images of a release's dependents is not the installed population of the library: most installations are never published as images, and projects that publish images are a selected group. The install class is read from the build's own instructions and is the builder's word; where the Dockerfile at the build's commit cannot be tied to the image by a revision label, it is the nearest commit before the build and is labelled weaker.

## Access and cost decision, per registry

Pages read before this brief (sources.md): Docker's usage pages (read again at 21:16:51 UTC; unchanged from LH006's reading: "100 per IPv4 address or IPv6 /64 subnet" per six hours for unauthenticated users; rate-limit headers "are returned on both GET and HEAD requests. Using GET emulates a real pull and counts towards the limit. Using HEAD won't."). LH006 found the limit served as `100;w=3600`, per hour, and nearly exhausted by other traffic on the proxy's shared egress addresses.

- **ghcr.io** (anonymous tokens from ghcr.io/token; OCI distribution API only). No counted allowance was served to LH006. **Decision:** read anonymously, tag list, manifests, configurations and layers. For a repository with more than 300 tags, tags are first narrowed to those whose name dates them to the period plus 14 days either side (a version tag whose git tag or PyPI release falls there, or a commit tag whose commit does), and at most 300 tags per repository have their manifest and configuration read. The GitHub REST API for package versions needs a token and is not read.
- **Docker Hub** (registry-1.docker.io with anonymous tokens from auth.docker.io; tag records from hub.docker.com's v2 API, which is not a pull). **Decision:** tag records and digests from the hub API; HEAD where a digest or the rate-limit headers are all that is needed; a manifest GET only for an image this study will read, and then only the linux/amd64 manifest by the digest the hub API lists (no index GET). **Counted-pull budget: at most 40 manifest GETs in all, and at most 25 in any 60 minutes.** A HEAD reads `ratelimit-remaining` before the first GET and before every tenth after; reading from Docker Hub stops whenever it is below 10, and resumes at most once, no sooner than 60 minutes later. Every limit header seen is recorded.
- **quay.io, registry.gitlab.com and others:** read anonymously through the OCI distribution API if a qualifying image names one; recorded as refused if credentials are asked for.
- **No Docker daemon; no image pulled whole.** Every read is a plain HTTPS request made by the scripts and logged in data/read_log.csv with its time, endpoint, status and bytes.

**Reading a layer** as LH006: stream from the start, gunzip and walk the tar entries as they arrive, close the connection at the first entry under `site-packages/mcp-<version>.dist-info/`, reading layers from the top of the image down and skipping layers whose history line is a base-image step with no Python package installation. An image with no `mcp` in the layers read is "not found in layers read", not "no mcp installed".

## Sampling rule, fixed before any image is read

1. **Hash order.** The frame's packages, by normalised name (PEP 503), are ordered by the SHA-256 of that name, lowest hexadecimal first.
2. **Screening.** In that order, up to 120 packages are screened (all of them if the frame is smaller), with LH006's selection procedure: the repository by LH002's rule (Open Source Insights' SOURCE_REPO relation or link, then PyPI's project URLs); PyPI's JSON for the listed and latest versions, searched for image references; a blobless clone and, at the default branch head and at its last commit at or before 2026-07-14T21:37:16Z, only Dockerfiles, Containerfiles, compose files, CI workflows, root Markdown files and READMEs, `server.json` and `smithery.yaml`, searched for the same terms as LH006. The screening list and its order are written to data/frame.csv before any clone.
3. **Qualification**, as LH006: a package qualifies if its repository or package metadata names a published image of its own at a registry (a workflow that builds and pushes a named image; a pull or run command for a registry image not built locally in the same instructions; an OCI entry in `server.json`; or an image named in PyPI's metadata), and the image installs the package. A Dockerfile alone does not qualify. No registry is searched by name. Every screened package, with the reason, goes in data/candidates.csv, and the decisions are made before any tag list is read.
4. **Sample.** Every qualifying image repository among the screened, up to 24, in hash order. If more than 24 qualify, the first 24 in hash order are taken and the rest are recorded as qualifying but not sampled.

## Readings, for each sampled image repository

1. The tag list, and on Docker Hub the hub API's tag records (push times and digests).
2. **Images to read**, at most 10 per repository, in this priority, each image being a distinct digest dated by Docker Hub's push time or, on ghcr.io, the configuration's `created`: (1) the last image before the release and the first after it; (2) the first and the last image in the period; (3) the images nearest to days +7, +14 and +21 and to day -14; (4) the nearest image outside the period on each side; (5) between two read images of which one holds the new release and the other does not, the image midway between them in time, repeated while the caps allow. On Docker Hub the tiers are taken across repositories in hash order (every repository's tier 1, then every repository's tier 2), so the counted budget is spread; ghcr.io images are read in the same priority without a counted budget.
3. For each image read: its linux/amd64 manifest and configuration (`created`, labels, history lines), and the installed `mcp` version from its layers.
4. **Install class**, from the configuration's history lines and the Dockerfile at the build's commit (the `org.opencontainers.image.revision` label where present, else the last commit on the default branch at or before the build time, labelled weaker):
   - **lockfile:** the step that installs the package consults a lockfile that fixes `mcp` (for example `uv sync` with `uv.lock` present, `poetry install` with `poetry.lock`, a requirements file generated by a lock tool);
   - **exact pin:** no lockfile, and the specifier the installer resolves `mcp` from names one version (`mcp==X`), in the Dockerfile, a requirements file or the package's own metadata;
   - **open range:** no lockfile, and the specifier admits more than one version (for example `mcp>=1.20`, a bare `mcp`, or `pip install <package>` from PyPI whose release requires a range);
   - **unknown:** the instructions read do not show which.
5. **The project's pin at the build time**, from git (the `mcp` specifier in `pyproject.toml` or requirements files and the version locked in `uv.lock` or `poetry.lock`, at the default branch's last commit at or before the build) and, where useful, PyPI's `requires_dist` for the release current at the build.

## Analysis

By install class: the share of images read that hold the new release, in bins of days since the release (the four weeks before; 0 to 7, 7 to 14, 14 to 21 and 21 to 28 days after; and outside the period). For each repository, the first image read holding the new release against the project's first commit pinning or locking it. A list of images whose install class and project pin disagree, in either direction (an image holding a version the project's pin or lock excludes). Where ClickPy's public copy of PyPI's download log can be read anonymously, as LH005 did, the share of each day's `mcp` downloads that were 1.28.x is set beside the images; this comparison is optional.

## Resource ceiling

About eight dollars of this subagent's own model spend at list rates. Network: at most **3 GB** of compressed layer bytes in all and **400 MB per image repository**, counted by the scripts, which stop a layer read at the dist-info or at the cap; the Docker Hub budget above; 120 screened packages; documentation pages fetched once each. Clones and manifests are held in a scratch directory outside the repository; no layer is written to disk and none is committed. No account, key or credential; only the anonymous tokens that registries' token endpoints hand to any caller, held in memory and never written to disk.

## Stopping condition

Close when every sampled repository's images (within the per-repository limit and caps) have been read, or the Docker Hub budget is spent, or a registry refuses and the refusal is recorded, or at the ceiling; the unread part is stated. If access fails so that the sample cannot be read at all, the record is a source assessment. The question, the choice of release and the sampling rule are not changed after any image is read; a change to how the plan is carried out is made by a dated amendment below.

## Intended output

LH007.md (version 0.1), sources.md, data/ with every table and read_log.csv, scripts/ that reproduce them, and one SVG figure only if the data earns it.

## Amendment, 2026-09-26 about 21:27 UTC, after the screening and the tag lists and before any manifest, configuration or layer of a sampled image was read

Four things found in screening and listing change how the plan above is carried out; none changes the question, the release, the frame or the sampling rule.

1. **The frame and the screen.** The three dependents lists hold 199 distinct packages (100 listed of 146 direct for 1.27.2, all 8 for 1.28.0, 100 of 122 for 1.28.1, read at 21:18). The first 120 in hash order were screened; 22 qualify, naming 22 distinct image repositories, all of which are sampled (fewer than 24). The qualification rule is applied as LH006 applied it, with the reading written into data/candidates.csv: an image counts as the package's own when it is built from the package's repository, or named by the package's own metadata, and installs the package or `mcp`; a package that republishes another project under a prefixed name (the `iflow-mcp-` packages), a fork, or a sibling distribution that names another publisher's image does not qualify.
2. **Mirrors.** Where a workflow pushes the same image to ghcr.io and Docker Hub, the ghcr.io copy is read. For three repositories, ghcr.io's token endpoint answered 401 at 21:26 UTC (ghcr.io/langflow-ai/langflow, ghcr.io/langflow-ai/langflow-nightly, ghcr.io/browser-use/browser-use), which is what it answers for a private or absent package; the same workflows push docker.io/langflowai/langflow, docker.io/langflowai/langflow-nightly and docker.io/browseruse/browseruse, and those are read instead, within the Docker Hub budget. cognirepo's ghcr.io token was refused as in LH006, and registry.intsig.net answered 403 to an unauthenticated `/v2/`; both stay in the record as named, not readable anonymously.
3. **Docker Hub's tag API stops at 1,000 tags** (403 on the eleventh page of 100, newest first) for the three large repositories; the 1,000 returned reach back before the period for all three (to 3 October 2025, 2 May 2026 and 16 October 2025), so the period is covered. The limit served at 21:26:45 UTC was `100;w=3600` with 72 remaining (a HEAD on Docker's documented test repository). Seven Docker Hub repositories share the 40-pull budget, so at most about five images each can be read; the tiers are taken across repositories as the brief says.
4. **ghcr.io images are dated by reading every tag.** Every sampled ghcr.io repository has fewer than 300 tags (at most 166), so each tag's digest is read by HEAD and each distinct image's linux/amd64 manifest and configuration are read to date it; the public.ecr.aws repository is read the same way.

## Amendment 2, 2026-09-26 about 21:35 UTC, after the ghcr.io and public.ecr.aws layer reads and before any Docker Hub manifest was read

The plan read the non-Docker Hub images first, since they carry no counted budget. Those reads used 2,471,129,240 of the 3 GB total (three repositories reached the 400 MB cap: chemgraph, aurapro-webui and mcp-mesh's python-runtime), leaving about 0.5 GB for the seven Docker Hub repositories. The caps are not raised. The plan is carried out as follows: Docker Hub images are read in the brief's order within the pull budget; once a byte cap is reached, each remaining planned image still has its linux/amd64 manifest and configuration read (within the pull budget), because the install class and the build time need only those, and it is recorded as "layers not read: byte cap reached before the image". Tier 5 (bisection) is not reached. The consequence, that the installed version is not read for most Docker Hub images, is a limit of this study, not a finding about them.

## Note on times, 2026-09-26 about 21:55 UTC

The clock times in this brief and its amendments were first written from estimates and have been corrected against data/read_log.csv: the brief was opened about 21:18 (it was written before the frame was read at 21:18:52), the first amendment about 21:27 (before the first manifest of a sampled image, read at 21:27:47), and the second at 21:35 (the file was saved at 21:35:40, before the first Docker Hub manifest GET at 21:35:41). The read times quoted inside them were corrected likewise. Nothing else was changed.
