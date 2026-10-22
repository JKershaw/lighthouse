# LH021: What can public PHP consumer image repositories show of a rebuild?

**Protocol 0.1, fixed 21 October 2026 UTC before inspecting the three selected repositories' files and runs.** Writer: Codex, GPT-6 Sol in ChatGPT Work Mode; model spend unknown. This is a source-feasibility and first *post-release* snapshot, not a representative sample or uptake estimate.

## Question and prior knowledge

Can a reproducible, small public consumer-image cohort expose an instruction to use the official PHP base, an actual GitHub Actions run, and a published derivative artifact, as distinct boundaries? This first run tests the first two boundaries. No registry derived-image read or earlier source revision is in scope, so it cannot yet identify a patch response or changed base image.

LH018 through LH020 already observed the official PHP release, source PR, publisher CI and four image manifests. A source search before this protocol identified three public application image repositories by name: `docker-library/wordpress`, `docker-library/drupal`, `nextcloud/docker`. The search also exposed a *different*, excluded Nextcloud all-in-one Dockerfile apparently using an older PHP version. That snippet is prior knowledge and cannot be a surprise result or grounds for selecting the cohort. None of the selected three repositories' current Dockerfiles or workflow outcomes was inspected for this protocol.

## Fixed cohort and observation rule

Take those exact three repositories without replacement, even if a source is empty, archived or inaccessible. They are a purposive set of public PHP application image publishers, not a random draw of PHP hosts. For each, read the repository and default branch commit, then its recursive tree at that SHA. Select at most four lexicographically first paths whose basename begins `Dockerfile` (including templates), and at most two lexicographically first `.github/workflows/*.yml` or `.yaml` paths. Retrieve those blobs by immutable SHA. Also read the ten most recent GitHub Actions runs in the repository at the collection time; record their head SHAs and times without assuming one executed the selected snapshot's instructions. This path cap samples repository files and can miss the actual production recipe or workflow. Do not replace selected paths after seeing their contents.

Classify a selected Dockerfile's *literal* `FROM php:<tag>` line as a source reference. An ARG, templated `FROM`, an image from another registry, or a missing file is unresolved for this simple reader, not negative evidence of PHP use. A workflow file shows a potential CI path; a run record shows that one workflow ran, with no proof it built that image unless a commit and job are linked. Report the pinned head SHA, source fields and retrieval time. Do not call a newly seen run a response to the security advisory, a successful run a deployment, or a moving base tag a fixed installed PHP binary. A later study needs a pre-event commit or retained image digest and a follow-up window to test a *change*.

## Ceiling and stop

At most 36 public unauthenticated GitHub API calls and 12 MiB retained bodies, 2 MiB per response, with the API rate remaining at least five. Retain full bounded bytes, status, URL, observation time and SHA-256, including failures. If a tree is truncated or a selected file is inaccessible, classify the affected result unknown. Stop after one snapshot per repository or at a binding ceiling. No CI logs, secrets, external image layers or third-party contact. The collector refuses to overwrite its run. Outputs are raw evidence, a read log, offline replay and a short feasibility record. A later prospective check needs a separately labelled run and its own stop rule.
