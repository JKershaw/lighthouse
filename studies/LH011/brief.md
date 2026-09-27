# LH011 study brief

**Brief, written before any outcome was read, 27 September 2026.**

**study:** LH011
**edition:** 0.1
**date opened:** 2026-09-27, written after reading AGENTS.md and programme.md as revised in the improvement round of 27 September 2026, studies/LH005/ (its brief, record, sources and schema table) and sources.md S20 to S23, and before any query was run or any page of download counts was read for this study. No ClickPy query, PyPI request or pypistats request has been made for LH011.
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), in the improvement round of 27 September 2026, as the worked example of the revised brief convention
**grounded at:** repository commit 497d4ff, with the round's uncommitted changes to AGENTS.md and programme.md
**issue:** to be filed by the coordinator; programme.md, Next

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
