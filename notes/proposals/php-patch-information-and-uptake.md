# Following the PHP fix from notice to use: source feasibility audit

**21 October 2026, preliminary design note, not a fixed protocol or a study result.** Writer: Codex, GPT-6 Sol in ChatGPT Work Mode; model spend unknown. Read alongside LH018 and LH019. This note records source access and prior knowledge before selecting a further cohort. A later study must fix its own question, frame, clock, ceiling and stopping rule before reading its outcomes.

## Why another question exists

LH018 records vendor fix statements and four version-specific images; LH019 records that four same-variant moving image tags already pointed to the fixed manifests at their first observation. Neither traces **how people learned of the fix**, the build and publishing process between source and registry, or whether consumers rebuilt, pulled or ran anything. These are different events with different public traces. The freshest opportunity is a contemporaneous account of the official image pipeline and a small, preselected downstream CI cohort, not a claimed internet-wide protection rate.

## Measurement audit

| Boundary | Public record to inspect | Can establish | Cannot establish / access caveat |
| --- | --- | --- | --- |
| Upstream announcement | php.net releases; php/php-src advisories and their timestamps | Published advisory and named fixed versions | Who saw or acted on it; precise availability from a date-only announcement |
| Information in a maintainer community | A preselected set of official issue/PR threads and vendor notices, including `docker-library/php` issue #1693 and PR #1694 | A public message, reply, decision, or source change at its recorded time | Total readership, private coordination, why a person acted, or a representative spread rate; comments and reactions are engagement, not installations |
| Packaging change | `docker-library/php` PR #1694, commit, review, checks; `docker-library/official-images` PR #22541 | Proposal, review, merge and test records in two distinct repositories | That the Docker Hub image has been published at merge time |
| Publisher CI and release | Public GitHub Actions run/job metadata, `docker-library/meta` source/build records, official-images manifest, registry digest | A job was queued, started, completed or failed; source moved through the publisher's staged build pipeline; final registry manifest was observed | A green source PR check is not a production registry push; some logs may require sign-in and all retained logs need a byte ceiling |
| Distributor publication | Debian and Ubuntu tracker and advisory (LH018), then architecture-specific build and package-index records if accessible | Vendor statement, build status, index availability, each with its own clock | Installed host count; a fixed tracker status alone need not prove a binary is in the index at an observed instant |
| Consumer CI | A cohort of public repositories selected *before* inspecting their reactions; Dockerfile/base-image reference, workflow at pinned commits, run metadata, logged image digest when available, published derived image | Source instruction, observed CI run and, if the log actually exposes it, a resolved input digest or output image | That a workflow ran from its mere presence, that a run pulled fresh layers, or that a built image was deployed |
| Public uptake proxy | A repeated sample of selected public consumer repos' pinned base digests and published derived image manifests | How many *in that defined sample* changed a pin or published a new derived artifact during the window | All PHP hosts or deployments. Search-index coverage, survivor bias, caches, private CI and variant differences remain |
| Pulls and running use | Docker Hub repository-level aggregate counter; possible publisher analytics; voluntary operator telemetry | The aggregate counter counts requests for the repository; publisher-only analytics can distinguish tag/digest, checks and downloads by period | Anonymous public tag-level use or an internet-wide protected fraction. Pulls include version checks and are not runs; publisher analytics require appropriate organisation access |

The public official-image pipeline has a specific intermediate record: after the image source PR, a separate official-images PR is reviewed and tested on amd64; `docker-library/meta` records sources and builds; staging images, architecture repositories and finally `library/php` indexes are published in separate steps. This is an unusually clear opportunity to compare **communication, CI and registry clocks** without collapsing them into one event. At this audit, the PHP packaging PR was merged, an official-images PR and a successful test rerun were visible, and the LH018/LH019 registry observations already exist. Their precise event times and causal linkage still need a retained, replayable collection. The official-images run page exposed job names, status and a rerun but asked for sign-in to view logs on the anonymous page. These observations are prior knowledge for any future brief, not unseen outcomes.

Docker's analytics documentation says organisation members can export weekly or monthly CSVs. It lists raw pull actions by tag/digest, including version checks, and warns that inferred use cases are classifications of client signals. No publisher access has been established for `library/php`, and the public `pull_count` belongs to the repository rather than a protected-versus-unprotected population. Do not divide either by estimated PHP websites.

## Suggested bounded next study

First, retain one **publisher-chain case** for the four fixed PHP versions: upstream advisory; the two Docker packaging PRs and their commit/review/check events; a small set of named official-image jobs and meta records; first observed registry digests from LH018/LH019. Keep event timestamps at their source precision and retrieval times separate. Precommit the source list and what counts as “information”, “CI test”, “published image” and missing. One can describe the chain and intervals only where endpoints are independently timestamped. The known PRs make this a retrospective selected case, with no statistical claim about typical delay.

Second, if the public CI evidence is useful, fix a small downstream **consumer cohort** by a reproducible rule before looking at whether its repositories updated. Freeze repository IDs and base references at an as-of commit, include negative and inaccessible cases, and follow for a declared window. Classify separately: advisory mention, base reference edit, CI run, resolved base digest in logs, derived image publication. Count per repository as well as per event, and explicitly report unknowns. Never treat a workflow file or CI badge as an executed deployment. The selection source, search date, search-index lag, architecture and repository survival belong in the result.

Do not open a general “uptake” study until a defensible denominator and an observable installation or run boundary are named. An opt-in operator cohort could supply that boundary with consent and known coverage; public GitHub and Docker alone do not. LH013 remains Lighthouse's standing baseline question and can proceed independently.

## Primary sources read for this audit

All accessed on 21 October 2026 UTC. Search snippets were only leads; these pages were opened.

- https://github.com/docker-library/php/issues/1693, https://github.com/docker-library/php/pull/1694 and https://github.com/docker-library/php/actions (public issue, packaging PR and CI listing).
- https://github.com/docker-library/official-images/pull/22541 and https://github.com/docker-library/official-images/actions/runs/39617280912 (official-images PR and one test rerun; anonymous page requested sign-in for logs).
- https://github.com/docker-library/faq#an-images-source-changed-in-git-now-what (publisher's declared lifecycle from source commit through staging and image indexes).
- https://docs.github.com/en/rest/actions/workflow-runs and https://docs.github.com/en/rest/actions/workflow-jobs (run and job metadata interfaces; access must be checked for each repository and log).
- https://docs.docker.com/docker-hub/repos/manage/trusted-content/insights-analytics/ and https://docs.docker.com/reference/api/hub/latest/schemas/repository_info/ (owner analytics and repository aggregate counter).
- Local `studies/LH018/` and `studies/LH019/` (retained source lists, responses and first snapshots, pending GitHub publication).

The Debian build and Ubuntu package-index routes have **not** yet passed a live access and schema check in this audit. A search result for package pages can lag the current security-pocket contents; a source-facing preflight must precede a protocol relying on them. No public consumer repository cohort was selected or read here.
