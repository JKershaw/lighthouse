# LH008 study brief

**study:** LH008
**edition:** 0.1
**date opened:** 2026-09-27, about 07:20 UTC, written after reading only the list of ClickPy's tables (one request, 07:17 UTC, in data/read_log.csv) and before any list of popular projects, any OSV advisory, any release time, any dependents list or any repository was read for this study. The libraries, releases and comparison releases that the rules below select are therefore not known to this brief; they are recorded in the first amendment, which is written after they are read and before any dependent is read
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driver session for issue #9 (LH008), from the design in programme.md
**grounded at:** repository commit a8a34e5

## Question

When software built on a widely used Python library pins or locks it, what moves the pin: a new release, or a security advisory fixed by one? LH007 saw, in one library (`mcp`) and one sample, more first pins on a release move in the day after a high-severity advisory than in the four weeks after the release itself, four of six in changes Dependabot wrote. This study asks the same of several libraries, with the release and the advisory on different days, and sets it against a release that no advisory followed.

## Choice of libraries (rule fixed before anything below it is read)

1. **Widely used.** The 200 projects with the most downloads in August 2026 in ClickPy's copy of PyPI's download log [S21] (table `pypi.pypi_downloads_per_month`, month 2026-08-01, summed over versions), read once.
2. **Advisory.** For each of the 200, OSV's records [S26] from `https://api.osv.dev/v1/query` with the package name and ecosystem PyPI. An advisory qualifies if it is a GitHub advisory record (id beginning `GHSA-`), its `database_specific.severity` is `HIGH` or `CRITICAL` (GitHub's own severity label as OSV carries it; CVSS vectors are not recomputed, and records from other databases without that field, such as `PYSEC-` records alone, are not considered), and its OSV `published` time falls between 2026-03-27T00:00:00Z and 2026-08-27T23:59:59Z. Withdrawn records are excluded.
3. **The fix already released.** The advisory's **fixed release** is the highest `fixed` version among its ECOSYSTEM ranges for the package. Its release time is the earliest upload time of any of its files in PyPI's JSON [L1 in this study's sources.md]. The advisory qualifies only if the fixed release's UTC calendar date is at least one day before the UTC calendar date of the advisory's OSV `published` time, so the release and the advisory fall on different days.
4. **One event per library.** Where a library has several qualifying advisories, they are grouped by fixed release; the library's event is the fixed release whose earliest qualifying advisory is the earliest in the window (the longest follow-up), and the event's **advisory time** is that earliest qualifying advisory's OSV `published` time. Every other advisory against the library in OSV, of any severity, is listed in data/ with its times, so a reader can see what else was published near the event.
5. **Up to four libraries**, taken in descending order of August 2026 downloads among those with a qualifying event. Four is set by the budget: each library needs two frames of dependents below.
6. **The advisory time used is OSV's `published` field of the GHSA record**, which is the publication time GitHub's advisory database gives (GitHub's advisory pages and API were refused to anonymous requests through this environment in LH007 and are not read). Where the record carries `database_specific.github_reviewed_at` or `nvd_published_at`, both are recorded, and the analysis reports whether using the review time instead changes any share.

## Comparison release (rule fixed before it is read)

For each chosen library, the **comparison release** is the most recent release, not a pre-release, that (a) was uploaded at least 30 days before the event's fixed release, (b) is of the same kind as the fixed release (a patch if the fixed release changes only the third component relative to the release before it; otherwise a minor or major release), and (c) is not a `fixed` version in any OSV advisory against the library, of any severity or database. Its lags are measured from its own upload time, as the fixed release's are; because a later release and the advisory follow it, the comparison is made on the shares within 1, 2, 7 and 30 days, and moves that come after the next advisory against the library are marked.

## Frame and sampling (fixed before any dependent is read)

- **Frames.** For each library, two frames: the direct dependents that Open Source Insights lists at `https://deps.dev/_/s/pypi/p/<library>/v/<version>/dependents` [L2] for (i) the **release before the fix**, the highest non-pre-release version below the fixed release and uploaded before it, and (ii) the **release before the comparison release**, defined the same way. The endpoint's `directSample` holds at most 100 entries; the direct count it gives and the number listed are recorded, and the entries not listed are the frame's unread part.
- **Order.** Each frame's packages, by normalised name (PEP 503), in ascending order of the SHA-256 of that name.
- **Number.** In that order, up to **60 packages per frame** are screened (all of them if the frame is smaller). A package in both of a library's frames is screened once for each. The screening order is written to data/frame.csv before any repository is cloned.
- **Repository**, as LH007 found it (LH002's rule): Open Source Insights' SOURCE_REPO relation or link for the listed version from `api.deps.dev/v3`, then PyPI's project URLs; github.com and gitlab.com only. A blobless clone without checkout, over HTTPS, held in /tmp/lh008, outside the repository; history from 2025-09-01 at the earliest where the clone is shallow.
- **Default branch** is the branch the clone's HEAD names. Only first-parent commits on it are read.

## Classification of the pin (for each screened repository)

At the **snapshot commit**, the last first-parent commit on the default branch at or before the relevant release time (the fixed release for the fix frame, the comparison release for the comparison frame), the following files are read, at most three directories deep, skipping paths containing `test`, `example` or `docs`:

- **lockfile:** `uv.lock`, `poetry.lock`, `pdm.lock`, `Pipfile.lock`, and a requirements file (`requirements*.txt` or a `.txt` under a `requirements/` directory) whose text says it was generated by pip-compile or `uv pip compile` (or by `uv export`, `pdm export` or `poetry export`). The held version is the version locked for the library; if a lockfile locks it more than once (for example for different Python versions), the lowest is used.
- **exact pin:** a requirement naming exactly one version for the library (`==X` or `===X` without a wildcard, or a bare Poetry version `"X"`) in `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile`, or a hand-written requirements file.
- Anything else (a range, a bare name, no mention) is **not pinned** and the repository is not kept.

A repository is **kept** for the fix frame if some pinning or locking file at the snapshot holds a version that OSV lists as affected by the event's advisory (the ranges' `introduced` and `fixed` events decide); for the comparison frame, a version below the comparison release. The **release time** for a kept repository is the upload time of the `fixed` version of the advisory range that contains the held version (normally the fixed release; an older release line's own fix where the repository is on that line). If a repository holds the library in several files, all are followed.

## The move and its authorship

- **The move** is the first first-parent commit on the default branch after the snapshot at which some file that held an affected version (comparison frame: a version below the comparison release) holds a version no longer affected and not lower than before (comparison frame: the comparison release or later), or stops mentioning the library while another followed file holds such a version. Removing the library entirely is recorded as a removal, not a move. Commits are read in order up to the head as cloned; a repository whose followed files have not moved by then is **censored** at the clone time and counted, not dropped. A repository whose followed files hold more than 400 first-parent commits after the snapshot is read to its first move or to its 400th commit and marked.
- **Times:** the commit's committer time (for a merge or a squash made on GitHub, close to when it reached the default branch; git does not record pushes) and its author time. Lags are taken from the committer time: from the release time, and (fix frame) from the advisory time.
- **Authorship class**, from git alone, since the GitHub API is refused for these repositories in this environment:
  - **bot:** the moving commit's author name or e-mail marks a bot (`[bot]`, or a known automation name such as dependabot, renovate, pre-commit-ci, github-actions, snyk, pyup, mergify, or a name ending in `bot`), whoever committed it; a merge whose author is a bot is also a bot.
  - **person merging a bot's branch:** a merge commit, authored by a person, whose message names a branch of a bot (for example `from owner/dependabot/pip/...`, `renovate/...`) or whose second parent is authored by a bot.
  - **person:** anything else.
  - The bot's name, whether the message (or, for a merge, the merged branch's tip message) says `security`, `vulnerab`, or names a GHSA, CVE or PYSEC identifier (recorded as the bot's or the person's word), and any `Co-authored-by` trailer naming a bot or an AI system are recorded.
  - What this cannot distinguish: a squash or rebase merge by a person of a bot's pull request usually shows the bot as author, so it falls in **bot**; a person's commit that copies a bot's text, or a bot account a project runs itself under a person-like name, is misread; pull-request bodies and labels, where Dependabot marks a security update, are not read.

## Analysis

For each library and frame, and pooled: the kept repositories, the moves and the censored; the distribution of lags from the release (days; median and quartiles among movers) and, for the fix frame, from the advisory; the share of kept repositories that moved within 1 and 2 days (0 to 24 and 0 to 48 hours) after the release and after the advisory, and the share that moved before the advisory; the same by authorship class. The comparison frames give the same shares from release. With the samples this small, shares are given as counts over the kept, and no significance test is run. A move before the advisory but after the release is a move on the release; a move after the advisory is not evidence that the advisory caused it (interpretation; the link is timing, as in LH007). ClickPy's daily shares by version may be set beside the moves for context; optional.

## Interpretation boundary

As the programme says: a commit that moves a pin is a request, not an installation, and not a run. A bot's commit shows that the project runs a bot, not what it was configured to do or whether its security mode fired; a message calling it a security update is the bot's word. Nothing here says whether any project was exposed to an advisory, and no project is named as vulnerable; projects are named only where a reader needs to check a row, as LH007 did. A dependent listed by Open Source Insights is a published package; its repository is the project's development record, not its deployments.

## Resource ceiling

About nine dollars of this subagent's own model spend at list rates. Network: clones and fetched blobs held in /tmp/lh008, at most **3 GB** on disk, checked before each clone; screening stops there and the unscreened remainder is stated. At most 4 libraries, 8 frames, 480 screened packages. All reads anonymous and logged in data/read_log.csv; git's on-demand blob fetches are counted by clone, not by request. No account, key or credential.

## Stopping condition

Close when every frame's first 60 packages (or the whole frame) have been screened and every kept repository has been read to its move or to the head, or at the ceiling, with the unread part stated. If access fails so that the sample cannot be read, the record is a source assessment. The question, the library rule, the frames and the sampling rule are not changed after any dependent is read; a change to how the plan is carried out is made by a dated amendment below.

## Intended output

LH008.md (version 0.1), sources.md, data/ with every table and read_log.csv, scripts/ that reproduce them, and one SVG figure only if the data earns it.

## Amendment 1, 2026-09-27 about 07:22 UTC, after the libraries were chosen and before any dependent was read

**What was read** (data/read_log.csv, 07:17:14 to 07:20:54 UTC): ClickPy's August 2026 download totals (data/top200.csv); OSV's records for each of the 200 projects, 948 in all (data/osv_advisories.csv); PyPI's release lists for the 16 projects with a HIGH or CRITICAL GHSA record published in the window and a fix; and the five OSV records named below by id.

**Applied** (observation; data/qualifying_advisories.csv, data/events.csv). 68 GHSA records rated HIGH or CRITICAL were published in the window with a fixed version, against 16 of the 200 projects, and in every one of the 68 the fixed release was on PyPI at least a calendar day before the advisory. The four chosen, in download order:

| library (August rank) | advisory (OSV `published`, UTC) | fixed release (first upload, UTC) | release before the fix | comparison release (upload) | release before it |
| --- | --- | --- | --- | --- | --- |
| urllib3 (6) | GHSA-qccp-gfcp-xxvc, HIGH, 2026-05-11 14:51:20 (and GHSA-mf9v-mfxr-j63j, HIGH, 25 seconds later, same fix) | 2.7.0, 2026-05-07 16:13:17 | 2.6.3 | 2.4.0, 2025-04-10 15:23:37 | 2.3.0 |
| cryptography (10) | GHSA-537c-gmf6-5ccf, HIGH, 2026-06-15 20:12:27 | 48.0.1, 2026-06-09 22:30:53 | 48.0.0 | 46.0.4, 2026-01-28 00:23:07 | 46.0.3 |
| pyjwt (45) | GHSA-xgmm-8j9v-c9wx, HIGH, 2026-06-15 19:28:06 | 2.13.0, 2026-05-21 19:54:35 | 2.12.1 | 2.11.0, 2026-01-30 19:59:54 | 2.10.1 |
| starlette (46) | GHSA-wqp7-x3pw-xc5r, HIGH, 2026-06-15 20:16:30 | 1.1.0, 2026-05-23 16:55:39 | 1.0.1 | 1.0.0, 2026-03-22 18:29:45 | 0.52.1 |

Each advisory's OSV range runs from an early version (`0`, `0.5.0` or `1.23`) to the fix, so every version below the fixed release is affected and the kept rule reduces to "holds a version below the fixed release". `github_reviewed_at` equals `published` in all four, so the review-time sensitivity in the brief is empty.

**Other public records near the events**, which the brief's rule does not choose but a reader needs (observation, data/osv_advisories.csv): for pyjwt, five PYSEC records naming 2.13.0 (or 2.12.1) as fixed, derived from CVEs that NVD published on 2026-05-28 16:16 UTC, 7 days after the release and 18 days before the GHSA record; for urllib3, PYSEC records two days after the GHSA; for starlette, a MODERATE GHSA fixed in 1.0.1 (the release before the fix; its PYSEC record 22 May, GHSA 4 June), a MODERATE GHSA for 1.1.0 published 25 seconds before the HIGH one, a PYSEC record for 1.1.0 on 17 June, and a HIGH GHSA fixed in 1.3.1 23 minutes later the same evening; for cryptography, two HIGH GHSA records on 3 August fixed in 49.0.0 and 50.0.0. Three of the four chosen advisories were published within 52 minutes of each other on the evening of 15 June 2026 (19:28 to 20:16 UTC). Because pyjwt has a public CVE and PYSEC record a week after the release, the analysis reports pyjwt's lags from both the GHSA time (the brief's advisory time) and the NVD time, and says which moves fall between them.

**Comparison releases and later advisories** (observation). The next advisory against the library after each comparison release: urllib3 2.4.0, 69 days (GHSA, MODERATE, 18 June 2025, fixed in 2.5.0); cryptography 46.0.4, 13 days (GHSA-r6ph-v2qm-q3c2, HIGH, 10 February 2026, fixed in 46.0.5); pyjwt 2.11.0, 42 days (GHSA-752w-5fwx-jx9f, HIGH, 13 March 2026, fixed in 2.12.0); starlette 1.0.0, 61 days (PYSEC-2026-161, 22 May 2026, fixed in 1.0.1). So cryptography's 30-day comparison share includes 17 days after an advisory; moves after the next advisory are marked as the brief says.

**Two changes to how the plan is carried out**, neither changing the question, the libraries, the frames or the sampling rule:

1. **Clones are not shallow.** The comparison snapshot for urllib3 is April 2025, before the brief's "2025-09-01 at the earliest", and a shallow clone cannot find the last commit before a date if the repository made none between the cut and that date. Clones are blobless over the full history of commits and trees, as in LH007, within the 3 GB ceiling.
2. **A sensitivity on the release line.** Since every version below the fix is affected, repositories holding an older line (for example urllib3 1.26) are kept, and their move needs a new major version. Each kept row records the held version, and the analysis also reports the subset that held exactly the release before the fix (comparison: the release before the comparison release).

## Amendment 2, 2026-09-27 about 07:27 UTC, after the screening and before any commit after a snapshot was read

The screening (data/screen.csv, data/snapshot_files.csv) found three things that change how the plan is carried out; none changes the question, the libraries, the frames or the sampling rule.

1. **The unit is the repository.** Several packages in one frame share a repository (eight docassemble packages, six grimoirelab ones). The brief counts repositories, so within a frame each repository is counted once, with the package that comes first in hash order; the others are recorded as sharing it. A repository kept in both of a library's frames is counted in each.
2. **Which paths are skipped.** "Paths containing `test`, `example` or `docs`" is applied to directory names (`tests/`, `testing/`, `examples/`, `docs/` and the like), not to any substring, so that a directory such as `contrib/latest/` is not skipped by accident; a root file such as `requirements-test.txt` is read, since the project keeps it.
3. **What the frames are.** Open Source Insights' lists for an older version are dominated by packages that pin it, since a dependent whose range admits later versions is listed against a later one (interpretation from the counts: 201 of the 436 screened packages pin or lock the library below the threshold). The frame is therefore a frame of pinners by construction, which is what the question needs, and not a sample of all dependents.

## Amendment 3, 2026-09-27 about 07:50 UTC, after the moves were read

Two corrections, neither changing a rule. (1) Amendment 1 says three of the advisories were published "within 52 minutes"; they were published within 48 minutes (19:28:06 to 20:16:30 UTC), as data/events.csv shows. (2) The first reading of the moves (07:27 to 07:39 UTC) classified a merge of a person's branch named `fix/snyk-high-severity-deps` as a merge of a bot's branch, because the pattern for a bot's branch let the owner part of `from owner/branch` run across a slash. The pattern was narrowed to the brief's meaning (the branch itself must be a bot's), and the moves were read again from the same clones (07:45 to 07:47 UTC); only that repository's class changed. The first reading's table is not kept.
