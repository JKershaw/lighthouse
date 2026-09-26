# LH002 study brief

**study:** LH002
**edition:** 0.1
**date opened:** 2026-09-26, written before any repository history, event file or archive visit was collected
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), from the ticket Harbour issued as LH002 (kind `research`) and the design in programme.md
**grounded at:** repository commit ac2e974

## Question

The observer's question, from the ticket: when something changes in this neighbourhood, where does the change appear next? The programme's form of it: what can public activity reveal about change and dependency in a small software neighbourhood, and where does it fail to reveal running activity? The ticket adds the question it is meant to settle: whether propagation can be read from public records at all.

## Scope

- **Ecosystem:** PyPI, the Python package index. Chosen by the dispatch because Open Source Insights resolves it [S11], most of its projects are on GitHub, its manifests are readable text, and much of the AI tooling Lighthouse watches is published there.
- **Library:** `mcp`, the Model Context Protocol Python SDK, source repository https://github.com/modelcontextprotocol/python-sdk. Chosen before any dependent's activity was read, by this rule: an AI agent tooling library on PyPI, hosted on GitHub, resolved by Open Source Insights, whose release history before 28 June 2026 (ninety days before today) holds a release with no other release within twenty-eight days on either side, so that a twenty-eight-day window can hold exactly one. Four candidates were compared on their own release dates only (`mcp`, `tiktoken`, `instructor`, `safetensors`, from api.deps.dev read 2026-09-26). `mcp` 1.27.0 qualifies: the previous release, 1.26.0, was published on 24 January 2026 and the next, 1.27.1, on 8 May 2026. `tiktoken` 0.13.0 also qualified; `mcp` was preferred because agent tooling is closer to what the charter watches.
- **Window:** 2026-03-26T00:00:00Z to 2026-04-22T23:59:59Z, twenty-eight UTC days. Fixed by the release: Open Source Insights gives `mcp` 1.27.0's publication time as 2026-04-02T14:48:07Z, so the window opens seven whole days before the release day, the release falls on day 8, and twenty days follow it, leaving room for later changes in dependents. The window ends 157 days before 26 September 2026. It contains no other `mcp` release.
- **Observation:** of the public record of a past window, collected on 26 September 2026, not of live activity.

## Selection rule

Recorded here as run, in scripts/select_cohort.py, which reads Open Source Insights metadata only and no dependent's commits, tags or in-window releases.

1. **Frame A, the in-window release's dependents.** The direct dependents of `mcp` 1.27.0 as Open Source Insights lists them. The documented API returns only counts (v3alpha `:dependents`: 36 in all, 34 direct, 2 indirect); the list comes from the site's own JSON endpoint behind its dependents page, https://deps.dev/_/s/pypi/p/mcp/v/1.27.0/dependents, which is undocumented. Both read 2026-09-26. The definition of a version's dependents (whether it counts every dependent version or each dependent package's latest) is not stated in the documentation read (https://docs.deps.dev/faq/, 2026-09-26).
2. **Repository link.** The GitHub repository named by the dependent version's SOURCE_REPO relation in Open Source Insights, or a GitHub link in its metadata; failing that, a GitHub URL in PyPI's own metadata for the same version (https://pypi.org/pypi/NAME/VERSION/json). No repository is found by searching names.
3. **Eligible.** A GitHub repository other than the library's own; one entry per repository; and a first PyPI release, by Open Source Insights' publication dates, before the window opens, so that the project existed during the window.
4. **Slots 1 to 8.** Eligible members of frame A in ascending order of the SHA-256 digest of the package name.
5. **Slot 9 onwards, up to nine dependents.** First the oldest remaining member of frame A by first PyPI release; then, if slots remain, members of **frame B**, the direct dependents of `mcp` 1.26.0 (the release current when the window opens; 118 in all, 95 direct, 23 indirect), under the same eligibility, oldest first PyPI release first. This guarantees older projects in the cohort whatever frame A yields, and puts in a contrast group that Open Source Insights resolves to the release before the window rather than the one in it.

**Revisions made before this brief, and before any activity was read.** The first run admitted dependents first published after the window and took no repository link from PyPI; it would have put repositories that did not exist in the window into the cohort. The eligibility condition in step 3 and the PyPI fallback in step 2 were added, and the frame B slots in step 5 were added when frame A yielded only seven eligible dependents, all of which are therefore in the cohort. The PyPI fallback found no link for any package: none of the ten frame A versions without a link in Open Source Insights declares one on PyPI either.

**Frame A outcome (34 direct dependents):** 10 with no repository link in either registry, 17 first published on PyPI on or after 26 March 2026, 7 eligible and chosen. **Frame B outcome (95 direct dependents):** 31 with no repository link, 18 first published on or after the window start, 5 duplicates of a repository already counted, 41 eligible, 2 chosen as the oldest.

**Selection bias, stated in advance.** Frame A holds packages whose published metadata Open Source Insights resolves to the in-window release, so it is selected on having taken up that release at some point. The study can therefore test whether the public record connects an uptake to the release, but it cannot estimate how often dependents take up a release. Frame B is the partial contrast.

## Cohort

Fixed at this point. Any later change is a protocol amendment recorded in LH002.md.

| id | repository (public URL) | PyPI package | role | frame | first PyPI release |
| --- | --- | --- | --- | --- | --- |
| R00 | https://github.com/modelcontextprotocol/python-sdk | mcp | library | | 2024-11-20 (version 0.9.1) |
| R01 | https://github.com/saigontechnology/agentcrew | agentcrew-ai | dependent | A, slot 1 | 2025-06-23 |
| R02 | https://github.com/robertwhiffin/ai-slide-generator | databricks-tellr-app | dependent | A, slot 2 | 2026-01-19 |
| R03 | https://github.com/ooo0ooo/lean-lsp-mcp | lean-lsp-mcp | dependent | A, slot 3 | 2025-03-31 |
| R04 | https://github.com/paulieb89/pyp6xer-mcp | pyp6xer-mcp | dependent | A, slot 4 | 2025-12-08 |
| R05 | https://github.com/oraios/serena | serena-agent | dependent | A, slot 5 | 2025-07-21 |
| R06 | https://github.com/eddmpython/dartlab | dartlab | dependent | A, slot 6 | 2026-03-06 |
| R07 | https://github.com/mistralai/mistral-vibe | mistral-vibe | dependent | A, slot 7 | 2025-11-17 |
| R08 | https://github.com/drakkar-software/octobot | octobot | dependent, older | B, oldest | 2019-01-16 |
| R09 | https://github.com/jesse-ai/jesse | jesse | dependent, older | B, second oldest | 2020-04-06 |

Repository URLs are published because the ticket requires them for reproduction and because they name projects; several namespaces are personal accounts. That is the one identifier of a person this record carries, and it is the project's own public address, not an attribution of any commit. Open Source Insights gives repository keys in lower case; GitHub resolves them case-insensitively. First release dates are the earliest publication time in Open Source Insights' version list for each package.

## Sources and access

| source | used for | access | recheck at commencement |
| --- | --- | --- | --- |
| Git history over HTTPS from github.com | commits, tags, manifests at window start and end, additions and deletions | anonymous public clones, `--filter=blob:none`, into scratch | at collection |
| Open Source Insights, api.deps.dev and the deps.dev site endpoint [S11] | the frames, versions and publication times, each dependent's resolved dependencies, the typed dependency map | anonymous, no key | read 2026-09-26, answered |
| GH Archive [S5] | one hour of events: the hour holding the release, 2026-04-02 14:00 to 14:59 UTC, file https://data.gharchive.org/2026-04-02-14.json.gz; count cohort events, record size, estimate the window's cost | anonymous download | server answered 2026-09-26 |
| Software Heritage API [S10] | origin lookup for all ten; visit history for one repository, the library's, to test whether the window's history can be had without the live forge | anonymous, rate-limited | API root answered 2026-09-26 |
| PyPI JSON API | repository link fallback in selection only; dependents' in-window PyPI releases come from Open Source Insights' publication dates | anonymous | read 2026-09-26 |
| GitHub REST API, unauthenticated | fork and archived flags and GitHub Releases, if its anonymous limit allows; otherwise recorded as not retrieved | anonymous, 60 requests an hour | at collection |

No credential from the environment is read or used.

## Readings, per repository and UTC day

Commits (deduplicated by hash across every fetched branch and tag, placed by committer time, with author time kept); active days; additions and deletions separately, with lockfiles and vendored paths shown separately rather than silently dropped; tags and GitHub Releases; PyPI releases of the dependent package; dependency changes in manifests (`pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`, `Pipfile`) and, separately, changes in the locked `mcp` version in lockfiles; the `mcp` requirement and locked version at window start and end; authors in three classes, identified bot (a name or address ending in `[bot]`, or dependabot, renovate, github-actions, pre-commit-ci and similar service accounts), identified human account (a non-bot author whose address is a GitHub noreply address, which ties the commit to a GitHub account), and unknown (every other author). No AI authorship is attributed from style or volume; a commit trailer that names an AI tool is counted as a trailer, not as authorship. Totals and rates per observed repository-day; a repository-day before a repository's first commit, or otherwise without retrievable history, is missing, not zero.

## Inclusion rules

Forks: each repository's fork flag is recorded; a fork would be kept and marked, not replaced. Vendored content (paths under `vendor/`, `_vendor/`, `third_party/`, `vendored/`) and generated files (lockfiles such as `uv.lock`, `poetry.lock`, `Pipfile.lock`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) are counted in their own columns. Merge commits count as commits and contribute no line counts. Repeated observations: the same commit reachable from several branches counts once; a commit in GH Archive and in git is one change seen twice.

## Identity and retention

Contributor names and addresses stay in scratch space outside the repository and are deleted with it. The record publishes counts, the three classes and pseudonyms (`H01`, `B01` and so on, assigned per study by first appearance). No contributor name, handle or address is written under studies/LH002/.

## Resource ceiling

About ten dollars of this subagent's spend at list rates. One GH Archive hour, not the window. One repository's Software Heritage visit history. Clones without file contents, blobs fetched only for manifests and line counts.

## Stopping condition

Close when the window has been read for every retrievable cohort repository, the two maps are drawn, candidate propagation links have been tested against the ordinary explanations, and the coverage review is written: either a pattern shown with its evidence, or the records shown unable to connect the events. If retrieval fails for most of the cohort, close with a feasibility result and a source assessment.

## Intended output

LH002.md (version 0.1), cohort.md, the time map and dependency map as SVG, data/ with per-repository-day CSV tables, and scripts/ with the scripts run.
