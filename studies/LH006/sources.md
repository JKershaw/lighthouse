# LH006 source assessment

What a public container registry records of an installation, read before and alongside the images in LH006.md. Every statement names the page or reading it came from and when (UTC, 26 September 2026). A statement this study inferred rather than read says so. Pages are numbered D1 to D8 here; readings of the registries themselves are in data/read_log.csv, one row per request.

## Pages read

| id | page | publisher; date the page gives | read (UTC) |
| --- | --- | --- | --- |
| D1 | https://docs.docker.com/docker-hub/usage/ | Docker; no date recorded | 18:26:15 |
| D2 | https://docs.docker.com/docker-hub/usage/pulls/ | Docker; no date recorded | 18:26:15 |
| D3 | https://docs.docker.com/reference/api/hub/latest/ | Docker; the page renders its reference with scripts, and only the endpoint list was legible in the fetched text | 18:26:50 |
| D4 | https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry | GitHub; no date recorded | 18:26:16 |
| D5 | https://docs.github.com/en/rest/packages/packages | GitHub; no date recorded | 18:26:50 |
| D6 | https://docs.quay.io/api/ | Red Hat Quay; no date recorded | 18:26:18 |
| D7 | https://pkg.go.dev/github.com/opencontainers/image-spec/specs-go/v1 | Go package documentation of the OCI image specification's Go types, module v1.1.1, published 24 February 2025 (page) | 18:27:34 |
| D8 | https://docs.docker.com/reference/api/registry/latest/ | Docker; fetched, not used: its text is rendered by scripts | 18:26:17 |

The HEAD at 18:37:46 that first showed the hourly limit was made with curl before the scripts' logging began, so it is recorded in brief.md and LH006.md and not in data/read_log.csv.

Not read: the OCI image and distribution specifications in their own repositories. github.com answered 403 for https://github.com/opencontainers/image-spec/blob/main/annotations.md (18:26:17), as it has for earlier studies through this session's proxy. A copy of the same file on raw.githubusercontent.com answered 200 and was deleted unread, following LH005's practice of leaving to the driver whether that host counts as routing around the refusal. The driver's decision, recorded here on 26 September 2026: raw.githubusercontent.com is a host the session's proxy allows, serving public files, so reading it is not routing around a refusal of github.com's pages, and later studies may read it; this study's findings do not depend on it, since D7 carries the same definitions. In the repository's source list, Docker Hub is S24 and GitHub's container registry S25. https://specs.opencontainers.org/ answered 200 but serves the specifications' text by script from GitHub, so nothing legible came back (18:26:28, 18:26:51). The OCI field definitions below are therefore from D7, the specification's Go types and their comments, which is the specification in code rather than in prose.

## What an image is, as records

- **Tag.** A name in a repository that points at one manifest or index digest at a time. The distribution API's tag list (`/v2/<name>/tags/list`) returns names only, with no time and no digest (observation: every tag list read here, data/tags_registry.csv).
- **Image index.** A list of per-platform manifests by digest. Every multi-platform image read here also lists entries with platform `unknown/unknown`, which are build attestations attached by the build tool (observation of the platform field; what they hold was not read).
- **Manifest.** The configuration blob's digest and the ordered list of layer digests with sizes and media types.
- **Configuration blob.** JSON with `created` ("the combined date and time at which the image was created", D7), `history` (one entry per build step, each with `created`, `created_by`, "the command which created the layer", and `empty_layer`, D7), and the build's labels. Labels this study reads: `org.opencontainers.image.created` ("the date and time on which the image was built"), `org.opencontainers.image.revision` ("the source control revision identifier for the packaged software"), `org.opencontainers.image.version` ("the version of the packaged software") and `org.opencontainers.image.source` ("the URL to get source code for building the image") (D7). GitHub recommends the `source` label so that an image can be connected to a repository (D4). Labels are written by whoever builds the image; nothing checks them against the source (inference; no page read says otherwise).
- **Layer.** A compressed tar archive of the files a build step added, changed or removed. A Python environment installed in the image appears in some layer as a `site-packages` directory, with one `<name>-<version>.dist-info` directory per installed distribution, holding the installer's own record of what it installed. This is the reading this study relies on: it is written by the installer at build time, not by the project describing itself (interpretation of how pip and uv install, not read in their documentation for this study).

What none of these records holds: whether, where, when or how often an image was run. A registry sees manifest and blob requests; a request is a download of an image, not a start of a container, and a container can be started many times from one download (inference from how a container runtime caches images; not read in a runtime's documentation for this study).

## Docker Hub

- **Access.** Anonymous: "Unauthenticated Users 100 per IPv4 address or IPv6 /64 subnet" per six hours (D2, D1). "A pull for a normal image makes one pull for a single manifest"; "A pull for a multi-arch image will count as one pull for each different architecture"; version checks "do not count towards usage pricing"; the rate-limit headers "are returned on both GET and HEAD requests. Using GET emulates a real pull and counts towards the limit. Using HEAD won't." (D2). A separate abuse limit applies "to all requests to Hub properties including web pages, APIs, and image pulls ... in the order of thousands of requests per minute" (D1). Blob requests are not described as pulls on the pages read (D1, D2: silence, not a statement).
- **As served here.** Every HEAD this session made returned `ratelimit-limit: 100;w=3600`, one hundred per hour rather than per six hours, and `docker-ratelimit-source` named one of several proxy egress addresses (160.79.106.23, .129, .132, .133, .137, .138 and .139 between 18:37 and 19:03). `ratelimit-remaining` was 8 at 18:37:46 and 18 at 18:40:19; it was 0 from 18:43:57, when HEAD itself began to answer 429, until at least 18:55:26; and it was 91 at 19:02:22 (observation; data/read_log.csv holds the statuses, and the remaining counts are quoted from the scripts' output). The allowance is shared with everything else leaving through the same address, so how much of it a study behind a shared proxy can spend is not in its own hands (interpretation).
- **Tag records (hub API).** `https://hub.docker.com/v2/namespaces/<ns>/repositories/<repo>/tags` returns, per current tag: `last_updated`, `tag_last_pushed`, `tag_last_pulled`, `tag_status` (active or inactive), the digest the tag points at now, its media type, and per-platform `images` with each platform manifest's digest, size, `last_pushed` and `last_pulled` (observation, data/tags_hub.csv; D3 lists the endpoint). These are metadata reads, not pulls. The per-tag `images` endpoint (`.../tags/<tag>/images`) also lists each layer's digest, size and build instruction (observation of one response at 18:37:46; not used to fetch layers, brief.md amendment point 1).
- **Repository records.** `pull_count` for the repository (data/context_reads.csv). By D2 a pull is a manifest request, so the count is of downloads of image descriptions, not of runs, and it counts every client, including scanners and mirrors (interpretation).
- **What is kept when a tag moves.** The tag API lists only where each tag points now. It has no field for earlier digests of the same tag (observation of every field returned). An earlier build survives in the listing only if another tag still points at it: a project that tags every build with a version or a commit identifier as well as `latest` leaves every build listed; a project that pushes only a moving tag leaves no listed trace of the builds it replaced (derived from data/tags_hub.csv; see LH006.md, Findings). Whether Docker Hub still serves a replaced, untagged manifest by digest could not be tested, because no public record read gives such a digest.
- **Last pulled.** `tag_last_pulled` gives one time per tag. Of keboola/mcp-server's 730 tags, 612 were last pulled on 17 August 2026, and 255 of daltonnyx/agentcrew's 387 on the same day (derived, data/tags_hub.csv). A single client pulling every tag on one day fits a mirror, scanner or archive sweep better than use (interpretation). A last-pulled time says when some client last asked, not that anyone ran it.

## GitHub's container registry (ghcr.io)

- **Access.** "You can also access public container images anonymously" (D4). No anonymous rate limit is stated on D4. Anonymous tokens come from `https://ghcr.io/token`. For `ashlesh-t/cognirepo`, which a project workflow names, the token endpoint answered 401 at 18:36:57 (observation); what that means (private, never pushed, or deleted) the response does not say.
- **Tag list.** Names only, current tags only (observation, data/tags_registry.csv).
- **Version history.** GitHub's REST API lists "package versions", including untagged ones, with times; it needs a token: "To access package metadata, your token must include the read:packages scope" (D5), and api.github.com answers 403 through this session's proxy (driver's check, 18:24). Not read. So for ghcr.io this study sees only the builds that still carry a tag.
- **Referrers.** The OCI referrers endpoint answered 404 `MANIFEST_UNKNOWN` for a serena index at 18:49:56 (data/context_reads.csv). Nothing attached to a digest is listed through it.
- **Configuration and layers.** Served anonymously for every serena image read (data/read_log.csv).

## quay.io

- Read-only calls on public repositories need no token; other calls need an OAuth token (D6). Quay's tag API keeps tag history, but no image in the selection lives on quay.io, so it was not read. The only quay.io references found were manylinux build containers in mistral-vibe's release workflow, which are tools for building wheels, not images of the project.

## What each record reaches

| record | release | download | installation | run |
| --- | --- | --- | --- | --- |
| tag list (names) | no | no | no | no |
| hub tag record (pushed, pulled times, digests) | no | a last pull time per tag; a pull count per repository | the time an installation was published | no |
| configuration (created, labels, history) | the source revision, if the builder labels it | no | the build time and the commands that installed | no |
| layer `site-packages/*.dist-info` | no | no | the versions the installer put in the image | no |
| a lockfile or requirements file inside the image | no | no | what was meant to be installed; weaker than dist-info | no |

## Distortions

| distortion | effect on an image as a record of installation | visible in the records read? |
| --- | --- | --- |
| Moving tags (`latest`, `main`, `stable`, `staging`) | the tag's history is overwritten; the builds it pointed at before are not listed | only when another tag keeps the same digest |
| Deleted tags and images | a build removed from the registry leaves no trace in the anonymous API | no |
| Labels written by the builder | a wrong or missing `created`, `revision` or `version` label goes unchecked | partly: `created` in the configuration can be compared with the hub's push time |
| Reproducible-build timestamps | a build that sets `SOURCE_DATE_EPOCH` records a fixed `created` time, not the build time (inference from the practice; not seen in the images read) | by comparing `created` with the push time |
| Images built from an open range rather than a lockfile | the installed version depends on the day of the build, not on the project's pin | yes: dist-info against the project's lock at the same commit |
| Several Python environments in one image | a system `site-packages` and a virtual environment can hold different versions | only if every layer is read; this study stops at the first `mcp` seen, top down |
| Pulls by scanners, mirrors and archives | a pull count or last-pulled time rises without anyone using the image | not separable in the records read |
