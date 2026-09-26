# LH006 study brief

**study:** LH006
**edition:** 0.1
**date opened:** 2026-09-26, about 18:30 UTC, written after reading the registries' documentation and before any candidate was searched or any tag list, manifest, configuration or layer was read
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driver session for issue #6 (LH006), from the design in programme.md
**grounded at:** repository commit 2c63cac

## Question

Is there a public record of what was installed, past the download? A public container image is a packaged environment published to be run. Its layers hold the files installed in it, including each Python package's installed metadata (a `<name>-<version>.dist-info` directory in `site-packages`), and its configuration holds the time it was built and, often, the commit it was built from. LH005 found that PyPI's download log stops at the file. This study asks whether the published images of LH002's neighbourhood show which version of `mcp` was installed in them, when, and how that compares with the release (1.27.0, published 2026-04-02T14:48:07Z), the downloads LH005 read and the dependents' moves LH002 read.

## Scope

- **Frame.** LH002's ten repositories (studies/LH002/cohort.md, R00 to R09) and the direct dependents of `mcp` 1.27.0 that Open Source Insights lists (frame A, 34 in LH002's read of 26 September 2026), read again from the same endpoint, https://deps.dev/_/s/pypi/p/mcp/v/1.27.0/dependents. If today's list differs from the 34 LH002 counted, both are recorded and the union is searched. Seven of frame A are LH002 cohort members, so the frame is at most 37 packages.
- **Period.** LH002's window, 2026-03-26T00:00:00Z to 2026-04-22T23:59:59Z, and the month after, to 2026-05-22T23:59:59Z. The nearest image outside the period on each side is also read, to bracket it.
- **Observation.** Of registry records and image contents as they stand on 26 September 2026, four to six months after the builds. Not of anything that ran.

## Interpretation boundary

An image records an installation made to be run. It is not a run: nothing in a registry says whether, where or how often an image was started. A pull count, where a registry shows one, counts manifest requests, not runs. A tag is a movable name: the same tag can be rebuilt and pointed at a new digest, and the registry may or may not keep the earlier one. The record says, for each image, which of release, download, installation and run a reading reaches; which tags were rebuilt under the same name; and whether the earlier digest is still listed or served.

## Access and cost decision, per registry

Documentation read before this brief (pages and read times in sources.md):

- **Docker Hub** (registry-1.docker.io, with anonymous tokens from auth.docker.io; metadata from hub.docker.com's v2 API). Anonymous pulls are limited to "100 per IPv4 address or IPv6 /64 subnet" per six hours. "A pull for a normal image makes one pull for a single manifest"; "A pull for a multi-arch image will count as one pull for each different architecture". The rate-limit headers "are returned on both GET and HEAD requests. Using GET emulates a real pull and counts towards the limit. Using HEAD won't." Version checks "do not count towards usage pricing". A separate abuse limit of "thousands of requests per minute" applies to all requests. **Decision:** read Docker Hub anonymously. Tag metadata comes from the hub API (no pull counted, by the documentation). Digests come from HEAD requests on manifests (not counted). A manifest GET is made only for a tag or digest this study will read further, one platform (linux/amd64) per image, and each is counted against a budget of 60 manifest GETs per six hours, leaving headroom because the proxy's address may be shared. Before the first GET and every twenty after, a HEAD reads `ratelimit-remaining`; reads stop if it is below 10. Blob GETs (configuration and layers) are not described as pulls in the pages read; this is recorded as the documentation's silence, not as a finding.
- **GitHub's container registry** (ghcr.io, anonymous tokens from ghcr.io/token). The documentation says public images can be accessed anonymously and states no anonymous pull limit on the page read. Version history (every digest ever pushed, with times) is served only by the GitHub REST API, which requires a token with `read:packages` for package metadata, and which answers 403 through this session's proxy in any case. **Decision:** read ghcr.io anonymously through the registry API only: tag list, manifests, configuration and layer blobs. The REST API is not read, and nothing routes around the 403.
- **quay.io.** Its API is public for read-only calls on public repositories and keeps tag history. **Decision:** read only if a qualifying image lives there.
- **Other registries** (for example registry.gitlab.com, public.ecr.aws, Azure or Google registries): read anonymously through the OCI distribution API if a qualifying image names one, and recorded as refused if it asks for credentials.
- **The Docker daemon is not used.** No image is pulled whole. Every read is a plain HTTPS request made by Python or curl, logged with its time in data/read_log.csv.

**Reading a layer without the whole image.** An OCI or Docker layer is a gzip (or zstd) compressed tar archive, served whole by digest; a gzip stream has no index, so a byte range from its middle cannot be decompressed on its own. The study therefore streams a layer from its start, decompresses and walks the tar entries as they arrive, and closes the connection as soon as it has seen an entry under `site-packages/mcp-<version>.dist-info/`. Layers are chosen from the configuration's history: the layers whose recorded command installs Python packages or copies a virtual environment (for example `uv sync`, `pip install`, `COPY --from=builder /app/.venv`) are read first, largest-numbered first; base image layers (the Python runtime and the operating system) are read only if nothing is found above them. If the image holds no installed `mcp` metadata but holds a lockfile or requirements file (for example `uv.lock`), its pinned `mcp` version is recorded and labelled as weaker: a lockfile in an image says what was to be installed, not what was.

## Selection rule, fixed before any image contents are read

For each package in the frame:

1. **Repository.** The repository LH002's rule resolves (Open Source Insights' SOURCE_REPO relation or link, then PyPI's project URLs), for the version the frame lists.
2. **Package metadata.** PyPI's JSON for the version the frame lists and for the latest version on 26 September 2026: the description and project URLs, searched for `docker pull`, `docker run`, `ghcr.io/`, `docker.io/`, `hub.docker.com/r/`, `quay.io/`, `registry.gitlab.com/` and OCI package entries.
3. **Repository files.** A blobless clone over HTTPS (`git clone --filter=blob:none --no-checkout`), then at two commits, the default branch's head on 26 September 2026 and its last commit at or before 2026-05-22T23:59:59Z, only these files are fetched and searched: any file named `Dockerfile*`, `Containerfile*` or `*.dockerfile`; compose files; `.github/workflows/*.yml` and `*.yaml`; `.gitlab-ci.yml`; `README*` and other `*.md` files at the root; `server.json` and `smithery.yaml` (the MCP registry's and Smithery's manifests, which can name an OCI image). The same search terms as step 2, plus `docker/build-push-action`, `docker push`, `org.opencontainers.image.source`.
4. **An image qualifies** if the repository or package metadata names a published image at a registry: a workflow that builds and pushes to a named image; a pull or run command for a registry image not built locally in the same instructions; an OCI entry in `server.json`; or an image named in PyPI's metadata. A Dockerfile alone, for a user to build, does not qualify, and is recorded as "Dockerfile, no published image named". An image that is named but does not answer on its registry is recorded as "named, not found".
5. **No other route in.** Docker Hub or ghcr.io are not searched by name to find images for the selection; that would select on a different population (images whose name mentions a word, published by anyone). One Docker Hub search count for the word "mcp" is read, as context for how large that other population is, and no content from it is read.

Every candidate, with why it qualified or did not, goes in data/candidates.csv.

## Readings, for each qualifying image repository

1. The tag list from the registry's distribution API, and on Docker Hub the hub API's tag records (`last_updated`, `last_pushed`, `tag_last_pulled`, digest and per-platform images).
2. For each tag whose push or build time falls in the period, and the nearest outside it on each side: its current digest (HEAD), its manifest or index, the linux/amd64 manifest, the configuration blob (`created`, `history`, labels such as `org.opencontainers.image.created`, `.revision`, `.version`, `.source`).
3. The installed `mcp` version, read from the layers as above, and the image's own package version where it is found on the way. At most 30 tags per image repository: if more fall in the period, version-named tags first, then the first and last of the rest by time, and the rule applied is recorded.
4. What the registry keeps when a tag moves: whether any earlier digest is listed (tag records, signature or attestation tags named after a digest, referrers) and whether an earlier digest known from any such listing is still served.
5. Set beside the release time, LH005's daily download shares (studies/LH005/data/mcp_daily_by_version_share.csv) and LH002's dependents' moves (studies/LH002/data/propagation_candidates.csv): which images held 1.27.0, when built, the lag from release, and whether an image's move came before or after the project's own pin in git.

## Resource ceiling

About eight dollars of this subagent's own spend at list rates. Network: at most 3 GB of compressed layer bytes in all and 800 MB per image repository, counted by the scripts, which stop a layer read at the dist-info or at the cap; Docker Hub manifest GETs within the budget above; documentation pages fetched once each. Layers are held only in the scratch directory outside the repository and deleted at the end; none is committed. No account, key or credential; only the anonymous tokens the registries' token endpoints hand to any caller, whose values are never written to the repository.

## Stopping condition

Close when every qualifying image repository's tags in the period (within the per-repository cap) have been read, or when a registry refuses and the refusal is recorded, or at the ceiling. If no image or very few qualify, that is the finding: the record is then chiefly a source assessment, with a statement of how thin the published-image population is for this neighbourhood.

## Intended output

LH006.md (version 0.1), sources.md (the registries as records of installed state), data/ with candidates.csv, the tag and image tables, read_log.csv, and scripts/ that reproduce them. One SVG figure only if the data earns it.

## Amendment, 2026-09-26 about 18:45 UTC, after the tag lists and before any Docker Hub manifest or any layer was read

Four things found while listing tags change how the plan above is carried out; none changes the question, the frame or the selection rule.

1. **Docker Hub's anonymous limit, as served, is hourly and shared.** A HEAD on a manifest at 18:37:46 UTC returned `ratelimit-limit: 100;w=3600` and `ratelimit-remaining: 8;w=3600`, with `docker-ratelimit-source` naming the proxy's egress address; at 18:40:19 another egress address had 18 remaining. The documentation says 100 per six hours (sources.md). This session shares the address with other traffic, so most of the documented allowance is not this study's to spend. The budget above is therefore replaced: this study makes at most 30 Docker Hub manifest GETs in all, only while `ratelimit-remaining` is 10 or more, and each is the linux/amd64 manifest fetched by the digest the hub API already lists (no index GET). The layer digests that the hub API's per-tag `images` endpoint lists are not used to fetch blobs without a manifest GET, because that would read images while leaving out the request Docker meters; every image whose layers are read has had its counted manifest GET.
2. **Priority order for Docker Hub images**, since not every image in the period can be read: first, for each image repository, the last image pushed before the release (2026-04-02T14:48:07Z), the first after it, the last in LH002's window and the last in the period; then the nearest image outside the period on each side and the first in the period; then, between any two read images whose `mcp` versions differ, the image midway between them in push order, repeated while the budget lasts. The plan, with each image's priority and reason, is data/layer_plan.csv. ghcr.io images are all read, in time order, within the byte cap.
3. **Layer reading stops at the first `mcp` dist-info seen**, reading layers from the top of the image down, and does not read layers whose history line is a base-image step (operating system or Python runtime) with no Python package installation in it. An image with no `mcp` in its upper layers is recorded as "not found in layers read", not as "no mcp installed".
4. **cognirepo's image cannot be read.** ghcr.io/token answered 401 at 18:36:57 UTC for `ashlesh-t/cognirepo`, which is what it does for a package that is private or does not exist. It stays in the record as named, not readable anonymously; nothing else is tried.
