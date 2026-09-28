# LH011 study brief

**Brief, written before any outcome was read, 27 September 2026.**

**study:** LH011
**edition:** 0.1
**date opened:** 2026-09-27, written after reading AGENTS.md and programme.md as revised in the improvement round of 27 September 2026, studies/LH005/ (its brief, record, sources and schema table) and sources.md S20 to S23, and before any query was run or any page of download counts was read for this study. No ClickPy query, PyPI request or pypistats request has been made for LH011.
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), in the improvement round of 27 September 2026, as the worked example of the revised brief convention
**grounded at:** repository commit 497d4ff, with the round's uncommitted changes to AGENTS.md and programme.md
**issue:** #13 (JKershaw/lighthouse), filed by the coordinator; programme.md, Next

What the writer already knows of the outcome, disclosed: LH005's one case, `mcp` 1.27.0, uploaded 2 April 2026 at 14:48 UTC, at 22 per cent of the library's downloads on its upload day, 48 per cent the next and 45 to 71 per cent after, with the CI flag on 10.6 per cent of its downloads against 48.6 per cent of the previous release's; LH007's `mcp` 1.28.x shares of 43 to 62 per cent in June and July 2026; and general knowledge that some of the most downloaded projects (boto3, botocore) release on most working days. No other release's downloads are known to the writer.

## Question

When a new version of one of the most downloaded Python projects is released, does it reach half of the project's downloads within two days as a rule, and how much of its early uptake carries the build-server (CI) flag, compared with the release it replaces?

## Population and unit

- **Projects** (rule fixed now). The 50 projects with the most downloads in August 2026 in ClickPy [S21] (`pypi.pypi_downloads_per_month`, month 2026-08-01, summed over versions), after removing, before the list is read, the packaging and installer tooling whose downloads come mostly from creating environments and isolated builds rather than from dependents: pip, setuptools, wheel, uv, virtualenv, pipenv, pipx, poetry, poetry-core, pdm, pdm-backend, hatchling, flit-core, build, setuptools-scm, scikit-build-core and maturin. The removed projects' ranks are recorded.
- **Releases.** Every version of those projects that is not a pre-release or development release (PEP 440), whose first file was uploaded to PyPI between 2026-04-01T00:00:00Z and 2026-08-31T23:59:59Z, and which at that moment was higher than every earlier-uploaded non-pre-release version (it became the newest). Upload times from PyPI's JSON API (`upload_time_iso_8601`, earliest file). A version yanked by the time of reading is kept and flagged; when it was yanked cannot be read.
- **Unit.** The release is the observation and the project is the unit: a project that releases daily contributes many releases and one vote. Pooled figures over releases are reported beside the per-project figures and never in their place.
- **CI subsample** (rule fixed now, to bound the heavy per-download reads). For each project, the first qualifying release uploaded in each calendar month, April to August: at most five a project.

## Sources

ClickPy's public SQL [S21] as user `demo`: `pypi.pypi_downloads_per_month` for the list; `pypi.pypi_downloads_per_day_by_version` for daily downloads by version; `pypi.pypi` (per download: date, version, installer, `ci`) for the CI subsample only. PyPI's JSON API for release lists and upload times. pypistats.org [S22] daily totals as a cross-check of ClickPy's daily totals, as LH005 did. For the meaning of the CI flag, the source of the installers that report it, read from their PyPI source distributions (pip and uv, the versions current on 1 April and on 31 August 2026), since linehaul's repository was refused in LH005. No account, key or credential; GitHub is not needed.

## Events and clocks

- **Day 0** is the UTC day of the release's first upload; the hours left in day 0 are recorded. Days 1 and 2 are the next two UTC days. ClickPy keeps the day and drops the time, so nothing finer than a day is measured.
- **At-or-newer share on day d** (primary): downloads on day d of this release or of any higher non-pre-release version, over all downloads of the project that day, both from `pypi_downloads_per_day_by_version` (one table for numerator and denominator, as LH005). This handles projects that release again within days, where a release's own share falls because it is superseded, not because it was not taken.
- **Own share on day d** (secondary): the release's own downloads over the project's.
- **Reached half within two days**: the at-or-newer share is at least 0.5 on day 1 or day 2.
- **Days to half**: the first day, 0 to 30, with an at-or-newer share of at least 0.5; not reached by day 30, or by the last day ClickPy holds, is recorded as such.
- **CI share** (CI subsample): over days 0 to 2, the share of the release's downloads flagged CI among downloads whose flag is known (below), set beside the same share for the release it replaced (the newest version immediately before its upload) over the same three days. The comparison is within project and within days, because download counts are inflated by automation and deflated by caching at ratios that differ by project.

## Missing evidence

Unknown stays unknown and is never counted as a negative.

- **The CI flag.** ClickPy stores an unreported flag as not CI [S21], so a ClickPy "false" can mean "not CI" or "not said". Before any download is read, the installers' source fixes which installers send the flag and whether they send false or only true; the CI share is computed only over downloads by installers whose source shows the flag is sent whenever the installer detects CI. Every other installer's downloads are reported as "flag not known", with their volume, and not folded into either side. If the source shows that an installer sends only true, its "false" is read as "CI not detected by that installer", which the record says.
- **Days.** A day on which ClickPy holds no row for a project that had downloads the days either side, or a day whose all-project total falls below half the median of the seven days around it, is a gap: every measure on it is unknown. "Reached half within two days" is unknown when neither day 1 nor day 2 reaches 0.5 and either is unknown.
- **Installers with no name** stay a class of their own, as in LH005.

## The comparison that would matter

- **As a rule.** For each project, the share of its releases that reached half within two days, and its median day-1 at-or-newer share. Across projects: how many projects had most of their releases reach half within two days, the median and quartiles of the projects' medians, and a project-resampled 95 per cent interval (10,000 resamples, seed 20260927) for the share of projects. Reporting convention fixed now: "as a rule" if at least three quarters of projects with a known outcome had most releases reach half within two days; "not as a rule" if fewer than half; "for some projects" between. The distribution is shown whatever it says.
- **Builds.** Per release, the new release's CI share minus the replaced release's over days 0 to 2; per project, the median difference; across projects, the median with a project-resampled interval. LH005's case had the new release's share far below the old one's.
- **Described, not tested.** Both measures by kind of release (major, minor or patch by the first differing PEP 440 component) and by whether the project released again within seven days. No other test is run. A difference is a description: nothing here says why a release was taken.

## Overlap with earlier studies

LH005 read `mcp` 1.27.0 from the same ClickPy tables, and LH007 read `mcp` 1.28.x shares; if `mcp` is among the 50 projects, its releases in the window include both, and every result is also given without `mcp`. The libraries of LH008 to LH010 that are among the 50 appear here as projects, with none of their data reused. LH005's collection scripts are adapted, and each docstring says what changed.

## Interpretation boundary

As LH005: a download is not an installation or a run; the log is aggregate and anonymous, reaches PyPI's own servers only (a mirror or cache serves installations the log never sees), and its installer and CI fields are what the client reports. "Builds" here means downloads the client flagged CI; a container built outside a CI service is not flagged, so the CI share is a floor on automated builds, not a measure of them.

## Resource ceiling

About eight dollars of this agent's own model spend at list rates. ClickPy: at most 600 queries and 60 billion rows read in all, by ClickHouse's own statistics, every query logged in data/read_log.csv with its time, text and rows read. PyPI: at most 300 JSON requests and four source distributions. pypistats: at most 30 requests. Scratch work outside the repository, at most 2 GB. Anonymous reads only.

## Stopping condition

Close when every qualifying release has its at-or-newer share read for days 0 to 30 (or to the last day ClickPy holds), and every release in the CI subsample has its CI shares read, projects taken in SHA-256 order of their names; or at a ceiling, with the unread part stated. The question, the project, release and subsample rules, the measures, the reporting convention and the missing-evidence rules are not changed after any per-version download count is read. The first amendment, recording the project list, the releases, the subsample, the installers' CI rules and ClickPy's table definitions, is written and committed before any per-version count is read. Later changes are dated amendments, and one made after outcomes were seen is labelled post hoc.

## What would leave it inconclusive

- Fewer than 25 projects with a known "reached half within two days" outcome for at least one release.
- The installers' source cannot establish what the CI flag means, or more than a third of the CI subsample's downloads come from installers whose flag is not known: the CI part is then reported as ClickPy's flag as it stands, and not read as builds.
- ClickPy's daily totals differ from pypistats's "with mirrors" by more than five per cent on more than a fifth of the cross-checked days (five projects by SHA-256 order, the three days after each project's first qualifying release): the counts are then reported as ClickPy's, with the disagreement.

## Intended output

LH011.md (version 0.1), sources.md, data/ (with read_log.csv and every query result the analysis uses), scripts/ with an offline analysis and a replay command over the retained results, a line in investigations/software-updates.md, and a piece only if the record earns one.

## What was checked before writing (bounded literature check)

Five web searches on 27 September 2026, read as search-result summaries only (no page was opened), for published work on PyPI download composition, the CI flag and release uptake:

- https://discuss.python.org/t/pypi-downloads-statistics-and-continuous-integration/91810 (Python.org packaging discussion; date not read): the BigQuery table's CI field is the only public way to separate automation from people, and there is "no good way" to distinguish the many variations beyond it.
- https://medium.com/@ninhothedev/pypi-download-counts-are-not-a-popularity-contest-2aa9cca49700 (a blog post of August 2026, not peer reviewed): automation inflates and caching and mirrors deflate counts, at ratios that differ by package.
- https://pypistats.org/faqs and https://packaging.python.org/guides/analyzing-pypi-package-downloads/, which LH005 read on 26 September 2026 (its sources L2 and L3): the mirror exclusions and the guide's warning that counts are "highly inaccurate".
- https://pip.pypa.io/en/stable/user_guide/ and https://github.com/pypa/pip/issues/13038: pip's user-agent data can be extended or disabled; the rule that sets `ci` was not in the results.
- https://arxiv.org/pdf/1907.11073 (an empirical analysis of PyPI, 2019) and https://arxiv.org/pdf/1709.04621 (whether developers update dependencies after advisories, 2017): neither measures uptake by downloads in the days after a release.

What it changed: the CI share is compared within project and within days, only over installers whose flag is known, and the installers' own source is read for the flag's rule before any count. No published measurement of release uptake by downloads across projects was found in five searches, which says little about whether one exists.

## Amendment 1, 28 September 2026: the frame, fixed before any per-version count is read

Written between 19:57 and 20:10 UTC on 28 September 2026 by a Lighthouse research subagent in Claude Code (Opus 5.5, claude-opus-5-5, as reported by its harness), for issue #13, and committed before any per-version or daily download count was read. What had been read by then, all logged in data/read_log.csv: six ClickPy queries (the server's version and limits; the `pypi` database's table definitions and column types; the August 2026 monthly totals of the top 80 projects, summed over versions; the first and last day held for the 50 projects), 54 PyPI JSON reads (the 50 projects, and pip and uv twice) and four source distributions. None of them gives a count by version or by day. The one change of wording above, the issue field, fills a blank the brief left for the coordinator.

**ClickPy's server and tables** (observation; data/clickpy_server.csv, clickpy_schema.csv, clickpy_columns.csv, read 19:53 UTC). Server 26.10.1.39301, time zone UTC; the `demo` user may return at most 10,000 rows, read at most 1,000,000,000 rows or 50 GB, and run 60 seconds per query. The tables this study reads:

- `pypi.pypi_downloads_per_day_by_version` (date Date, project String, version String, count Int64), SharedSummingMergeTree ordered by (project, version, date), filled by a materialised view that counts rows of `pypi.pypi` by date, project and version. Both numerator and denominator of every share.
- `pypi.pypi` (date, country_code, project, type, installer, python_minor, system, version, libc, `ci` Enum8('false' = 0, 'true' = 1, 'unknown' = 2) DEFAULT 'unknown', filename), SharedMergeTree ordered by (project, date, version, country_code, python_minor, system). The CI subsample only.
- `pypi.pypi_downloads_per_day` (date, project, count), ordered by (project, date): the daily totals for the gap rule and the pypistats cross-check.
- `pypi.pypi_downloads_per_month` (month, project, count), ordered by (month, project), filled by a view that keeps only the last six months: the project list.
- `pypi.pypi_raw`, the Null-engine staging table, carries `ci` as Nullable(Bool). The step from it to `pypi.pypi` is not in the catalogue; ClickHouse's blog quoted it as `CAST(ifNull(ci, 0), ...)` (LH005, sources.md L4), so a null flag becomes 'false'. The 'unknown' value is the column default; whether any row in the window holds it is read with the counts, and such rows are "flag not known".

Last day held, read 19:57 UTC: 27 September 2026 for all 50 projects (data/clickpy_coverage.csv). Days 0 to 30 are therefore held for releases whose day 0 is on or before 28 August; the six later releases are read to 27 September and their "days to half" are censored there.

**The projects** (observation and rule; data/projects.csv, data/clickpy_top_projects_2026_08.csv). The removed tooling in the top 80: setuptools (rank 9), pip (rank 44) and wheel (rank 66, below the cut in any case); no other listed tool was in the top 80. The 50 projects are ranks 1 to 52 less those two: 1 boto3, 2 packaging, 3 typing-extensions, 4 certifi, 5 idna, 6 urllib3, 7 requests, 8 charset-normalizer, 10 cryptography, 11 cffi, 12 pluggy, 13 pygments, 14 pyyaml, 15 botocore, 16 python-dateutil, 17 six, 18 pydantic, 19 numpy, 20 click, 21 pycparser, 22 anyio, 23 pytest, 24 pydantic-core, 25 iniconfig, 26 aiobotocore, 27 annotated-types, 28 h11, 29 attrs, 30 typing-inspection, 31 protobuf, 32 fsspec, 33 httpx, 34 markupsafe, 35 httpcore, 36 s3transfer, 37 python-dotenv, 38 platformdirs, 39 pandas, 40 jinja2, 41 pathspec, 42 grpcio-status, 43 filelock, 45 pyjwt, 46 starlette, 47 uvicorn, 48 litellm, 49 aiohttp, 50 tqdm, 51 jmespath, 52 rpds-py. `mcp` is not among them, so no result needs giving without it and nothing of LH005 or LH007 is reused. Eight of the 50 were libraries of LH008 to LH010 (aiohttp, cryptography, idna, litellm, pyjwt, python-dotenv, starlette, urllib3); none of those studies' data is reused.

**The releases** (derived from PyPI's JSON API, read 19:54 UTC; data/pypi_versions.csv, one row per version; data/releases.csv; scripts/frame.py). 424 qualifying releases in 37 projects, uploaded from 2026-04-01T19:35:20Z to 2026-08-31T23:23:52Z. Thirteen projects released no qualifying version in the window and have no outcome: attrs, iniconfig, six, httpx, httpcore, python-dateutil, h11, pycparser, jinja2, pyyaml, markupsafe, jmespath, pluggy. By project, in SHA-256 order of names (releases / CI subsample): grpcio-status 6/3, pygments 1/1, filelock 21/4, pytest 3/2, fsspec 3/3, aiohttp 4/2, protobuf 4/3, tqdm 8/2, starlette 11/3, urllib3 1/1, charset-normalizer 5/3, pydantic 6/3, packaging 3/2, numpy 5/4, aiobotocore 6/4, certifi 4/4, s3transfer 7/4, typing-inspection 2/1, python-dotenv 1/1, rpds-py 2/2, annotated-types 1/1, boto3 103/5, pyjwt 1/1, botocore 103/5, pandas 3/3, uvicorn 16/5, typing-extensions 1/1, pydantic-core 7/3, anyio 3/2, litellm 46/5, idna 8/4, cryptography 7/5, click 6/4, cffi 2/2, requests 3/1, platformdirs 9/4, pathspec 2/1 (the full order, with the thirteen, is data/project_order.csv). Kinds: 324 patch, 95 minor, 5 major (cryptography 47.0.0, 48.0.0, 49.0.0 and 50.0.0; rpds-py 2026.5.1 after 0.30.0). 310 were followed by another newest version within 168 hours. Three are yanked now and kept, flagged: charset-normalizer 3.4.8, pandas 3.0.4, grpcio-status 1.82.0. Every version string parsed as PEP 440. Each release's upload time, day 0, hours left in day 0, replaced version and next newest version are in data/releases.csv (SHA-256 fcfa356b968ab2f89881e1548770d9ba0a6db4d2565347852f17bb3cc5790d39).

**The CI subsample** (rule applied): 104 releases, the first qualifying release of each project in each calendar month, marked `ci_subsample` in data/releases.csv.

**What the CI flag means, from the installers' source** (observation of the source; data/installer_versions.csv, data/installer_source_excerpts.txt; scripts/collect_installers.py). Read from the source distributions of pip 26.0.1 and 26.2.1 and uv 0.11.2 and 0.12.8, the newest non-pre-releases uploaded before 1 April and before 1 September 2026, each checked against PyPI's SHA-256.

- pip (both versions): `looks_like_ci()` is true when any of the environment variables BUILD_BUILDID (Azure Pipelines), BUILD_ID (Jenkins), CI ("AppVeyor, CircleCI, Codeship, Gitlab CI, Shippable, Travis CI") or PIP_IS_CI is present, whatever its value; the User-Agent's JSON then carries `"ci": true if looks_like_ci() else None`, with pip's own comment: "Use None rather than False so as not to give the impression that pip knows it is not being run under CI." In 26.0.1 the list is in network/session.py, in 26.2.1 in utils/misc.py; the rule is the same.
- uv (both versions; the two `linehaul.rs` files differ only in visibility and derives): the same four variables, "https://github.com/pypa/pip/blob/24.0/src/pip/_internal/network/session.py#L87" cited, give `Some(true)` when any is set and `None` otherwise; `ci: Option<bool>` is serialised with no skip, so the User-Agent carries true or null.

Rules fixed from this. Both installers send only true or null, never false; ClickPy stores null as 'false'. So for downloads whose installer is exactly `pip` or `uv`, 'true' reads "the installer found a CI variable" and 'false' reads "CI not detected by that installer", which includes CI systems that set none of the four variables and container builds outside a CI service. The CI share is computed over `pip` and `uv` downloads only. Every other installer name, downloads with no installer name, and any 'unknown' value are "flag not known", reported with their volume. ClickPy drops the installer version, so downloads by pip or uv versions older than those read are assumed to follow the same rule; that was not checked.

**Readings fixed now, where the brief leaves a choice** (decided before any count, so not post hoc):

1. The gap rule's "all-project total" is read as the sum, over the 50 projects, of `pypi_downloads_per_day`. A total over every project would scan that table's 1.08 billion rows, over the per-query limit, because it is ordered by project first. "The seven days around it" are days d-3 to d+3, d included. A project's own dip is a gap only by the first clause (no row on a day with rows either side).
2. Numerator versions are matched by exact string to the non-pre-release versions in PyPI's JSON that are at or above the release by PEP 440; a version ClickPy holds and PyPI's JSON does not list counts in the denominator only.
3. "Most releases" means more than half of a project's releases with a known outcome; exactly half is not most. A project has a known outcome when at least one of its releases has one. Intervals are percentile intervals over 10,000 resamples of projects with replacement, seed 20260927, recomputing the share of projects, or the median of project medians.
4. The CI share of a release is pooled over days 0 to 2: flagged `pip` and `uv` downloads of the release over all `pip` and `uv` downloads of it on those days, and the same for the replaced release on the same days. A release with no `pip` or `uv` downloads of either version on those days has an unknown difference; a day that is a gap makes the difference unknown. The difference is in percentage points, new minus replaced. "More than a third of the CI subsample's downloads" in the inconclusive rule is pooled over every subsample release's and replaced release's downloads on days 0 to 2.
5. The pypistats cross-check takes the first five projects in SHA-256 order that have a qualifying release (grpcio-status, pygments, filelock, pytest, fsspec) and days 1 to 3 after each one's first qualifying release, against `pypi_downloads_per_day`.
6. Queries: per project, daily downloads by version from `pypi_downloads_per_day_by_version` from seven days before its first day 0 to 30 days after its last day 0 (or 27 September), with versions outside the numerator sets folded server-side into one "other" row per day, split by date where a result would pass 10,000 rows; per subsample release, `pypi.pypi` for the project, days 0 to 2 and the two versions, by date, version, installer and flag.
