# LH013 study brief

**Brief, written before any outcome of its weeks was read, 29 September 2026.**

**study:** LH013
**edition:** 0.1
**status:** fixed; **waiting for data**. The study may read counts only when the eligibility condition below is met, and not before 13 October 2026. Until then nothing of its weeks is read, and no week already read may stand in for them.
**date opened:** 2026-09-29
**written by:** the driving session of 29 September 2026 in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), which also corrected LH012's record to version 0.3 the same day; no research agent was dispatched
**grounded at:** repository commit 89d4aa7 (LH012 record version 0.2), with LH012's record at version 0.3 in the same working tree
**issue:** #15 (JKershaw/lighthouse); programme.md, Next, checkpoint of 29 September 2026

## Question

Over the two weeks after LH012's, 28 September to 11 October 2026, do the 37 libraries' shares of downloads on older versions, and the part of those older downloads that came from Pythons no newer release supports, hold at the values LH012 read for 21 to 27 September; and how much of each library's downloads falls in the single largest combination of the fields the download log reports?

A combination of reported fields is called a **cell** here. A cell is not a machine, an owner or a population: many unrelated machines can share one, one machine can fall in several (for example, with two Pythons), and a cell that holds its share from week to week has not been shown to be the same machines. This study measures how concentrated downloads are in cells and whether that holds; it does not identify who or what makes them, and it does not test why older versions are downloaded.

## What the writer already knows of the outcome, disclosed

- Everything in LH012's record (version 0.3), which the writer corrected: for 21 to 27 September 2026 (W0), a median 37.3 per cent of a project's downloads were of versions below its reference release R0 (pyjwt 20.0 to pydantic-core 99.3), each project's P and its class, and the post hoc readings: on 23 September 62.2 per cent of boto3's downloads reported Python 3.9, 99.4 per cent of those pip, Linux, glibc and no CI flag; over W0 64.7 per cent of boto3's downloads reported Python 3.9, 95.4 per cent of those were of versions below 1.42.97, and boto3 was fetched 7.51 times as often as botocore on Python 3.9 against 2.94 times over all Pythons.
- No count for any day from 28 September 2026 on has been read by Lighthouse. LH012 read the most recent day ClickPy held on 29 September at 06:19 UTC (28 September), not its counts; its review's live re-reads were of W0 and earlier days (notes/R-0016.md).
- The writer's expectation, from the size of these libraries' daily downloads and not from any count of the new weeks: that older shares move by a few points from week to week. That is a prior, not a finding.

## Population, unit and reuse

- **Projects.** LH012's 37 projects, all of them (studies/LH011/data/releases.csv, as LH012 used it).
- **Unit.** The project. Pooled figures are reported beside per-project ones, never in their place. Intervals are percentile intervals over 10,000 resamples of projects with replacement, seed 20260929.
- **Reuse, disclosed.** LH012's frame, reference releases (studies/LH012/data/reference.csv), definitions and scripts, and its retained W0 tables (studies/LH012/data/analysis/week.csv, python.csv) as the baseline. The new weeks are days no study has read, so this is a repetition in time on new data, not a replication on new projects.

## The weeks, and when the study may run

- **W0**: 21 to 27 September 2026, LH012's week. Not reread, except the check below.
- **W1**: Monday 28 September to Sunday 4 October 2026. **W2**: Monday 5 to Sunday 11 October 2026. UTC days. Both are fixed now and cannot be replaced by other weeks.
- **Eligibility condition.** The study may begin reading counts when the most recent day ClickPy's per-day tables hold is 12 October 2026 or later, so that 11 October is not the most recent, possibly incomplete day, and every day of W1 and W2 is held for all 37 projects. It is checked with LH012's coverage query (the first and last day held per table and project, studies/LH012/data/clickpy_last_day_by_table.csv), which returns no count. ClickPy held the day before on 29 September, so the condition is expected to be met from about 13 October 2026.
- **If it is not met.** A session that finds the condition unmet reads nothing of W1 or W2 and leaves this study waiting. If ClickPy still does not hold 12 October 2026 by 31 October 2026, the study is recorded as blocked by its source in programme.md and issue #15, and its weeks are not replaced.
- **Check of the baseline.** Before any count of W1 or W2 is read, W0's daily totals for the 37 projects are read once from `pypi_downloads_per_day_by_version` and compared with LH012's retained totals, because ClickPy re-ingests days it finds wrong. A project whose W0 total differs by more than 2 per cent has its W0 comparisons reported as unknown. This reads totals already read, as a check, not a new outcome.

## Measures

LH012's definitions hold unless stated here (studies/LH012/brief.md, "The read week and the reference release", "Sources and events", "The three explanations and their traces" for P, and "Missing evidence").

1. **Older share O.** For each project and week, downloads of versions below LH012's R0 over all downloads, from `pypi_downloads_per_day_by_version`, with versions at or above R0 (including any uploaded since) "at or newer", and pre-releases above R0 and versions PyPI does not list "other". R0 is held fixed so that the same versions are compared across weeks.
2. **Python exclusion P.** LH012's P, lower and upper estimates, at R0, from `pypi_downloads_per_day_by_version_by_python`, with admission recomputed for each day of W1 and W2 from PyPI's metadata at the read (a version at or above R0 uploaded during the weeks can admit a Python and end its exclusion). P is a count of fetches from Pythons that no version at or above R0 admits: fetches that could not have been of R0 or later. It is not an account of why they were of the versions they were.
3. **Concentration C.** For each project and week, the share of its downloads in its largest cell of six fields of `pypi.pypi`: `python_minor`, `installer`, `system`, `libc.lib`, `ci` and `country_code`; beside it C5, the same without `country_code` (LH012's descriptor fields plus the Python minor). Each is reported with the cell's values and with the number of cells that carry half of the project's downloads. Computed server-side (the largest few cells a project, never the full grouping, which passes the `demo` user's 10,000-row limit), split by project and by day where a query would pass a limit.
4. **Secondary, described only.** O and P at each week's own reference release by LH012's rule (the highest non-pre-release, not wholly yanked, first uploaded on or before the week's first day less 31 days: 28 August for W1, 4 September for W2), which is the baseline a watch would compute week by week and which moves when R moves; C and C5 over older downloads only.

What the fields are (read before this brief was fixed): `installer`, `system`, `libc.lib` and `ci` are what the client reports, with the meanings LH011 and LH012 read in pip 26.2.1's and uv 0.12.8's source (pip and uv send `ci` true only when a build variable is set, else nothing, which ClickPy stores as false); `python_minor` is the client's reported Python, as LH012 describes; `country_code` is the country the package index's content network assigns to the requesting address, passed through by linehaul's log parser (linehaul-cloud-function, linehaul/events/parser.py, read 29 September 2026 at 10:18 UTC; the package index's BigQuery page, https://docs.pypi.org/api/bigquery/, read at 10:18 UTC, names the table and says it is filled by linehaul, and says nothing more of the field). A country is where an address is placed, which for a cloud machine, a proxy or a mirror is not where anyone is.

## Tests and conventions (fixed now)

- **O holds** for a project when its O in W1 and in W2 is each within 5 percentage points of its O in W0.
- **P holds** for a project when its class by LH012's convention (accounts for most, undetermined, cannot be the main reason, with "accounts for little" inside "cannot") is the same in W1 and W2 as in W0.
- **C holds** for a project when its C in W2 is within 5 points of its C in W1 and the largest cell has the same values in both weeks; C5 the same. W0's cells were not read with these fields, and they are not read now.
- **Across projects**, for O, P, C and C5: the number and share of projects with a known outcome that hold, with its interval. "As a rule" when at least three quarters hold, "for most projects" above one half, "for some projects" otherwise; these labels stay in the record, and a piece gives the numbers.
- **Tests of LH012's post hoc readings**, one each: boto3's share of downloads reporting Python 3.9 is above one half in both W1 and W2 (W0: 64.7 per cent); the ratio of boto3's to botocore's fetches on Python 3.9 is at least twice the ratio over all Pythons in both weeks (W0: 7.51 against 2.94); and more than three quarters of boto3's Python 3.9 downloads are of versions below 1.42.97, the highest boto3 whose Requires-Python admits 3.9, in both weeks (W0: 95.4 per cent). Whichever way they come out, they say whether a pattern holds, not who makes it.
- **Number of comparisons**: 37 projects times two weeks for O, 37 for P, 37 for C and 37 for C5 (185 per-project readings), four across-project summaries and three tests of the post hoc readings. Anything else read after counts are seen is labelled post hoc with its number of comparisons.

## Sources

ClickPy's public SQL (user `demo`, anonymous): `pypi_downloads_per_day_by_version`, `pypi_downloads_per_day_by_version_by_python` and `pypi.pypi`, for W1 and W2, and the W0 totals check; PyPI's JSON API for the 37 projects' versions uploaded since LH012's read (Requires-Python for admission, upload times, yanking), read after the eligibility check and before any count. Every query and request is logged with its time, as LH012's were. BigQuery is not read.

## Missing evidence

As LH012: unknown stays unknown and is never counted as a negative. Downloads with no Python reported enter P only through its lower and upper estimates. A day that is a gap by LH011's rule is left out of that project's week and named; with more than two gap days in a week, that project's measures for the week are unknown. A cell with an empty field is a cell like any other, with its empty values reported.

## Resource ceiling

- ClickPy: at most 300 queries and 30 billion rows read in all, by ClickHouse's own statistics. Expected use is about 20 billion, most of it two passes of `pypi.pypi`, one a week.
- PyPI JSON: at most 300 requests.
- Documentation: at most 5 page reads, only if a field's meaning has changed.
- About six dollars of the research agent's own model spend at list rates. Anonymous reads only; no key or token is read.

## Stopping condition

Close when O and P for W1 and W2, C and C5 for W1 and W2, and the three tests are read for all 37 projects, or at a ceiling, with the unread part stated. The question, the weeks, R0, the measures, the fields, the thresholds and the conventions are not changed after any count of W1 or W2 is read; a later change is a dated amendment, labelled post hoc if made after counts were seen.

## What would leave it inconclusive

- The eligibility condition not met by 31 October 2026.
- Fewer than 25 projects with a known O in both weeks, or with their W0 totals confirmed.
- ClickPy's tables disagreeing: if a project's weekly total in the by-Python table differs from the per-version table's by more than 2 per cent, its P is described only, as in LH012.
- Whatever it finds, it cannot say who or what makes a cell's downloads, or why older versions are downloaded.

## Overlap with earlier studies

The projects, R0, the definitions and the W0 baseline are LH012's, and through it LH011's. The three tests re-measure LH012's post hoc readings on weeks it did not read. No project, repository or release outside LH012's frame is read.

## Intended output

LH013.md (version 0.1), sources.md, data/ with the read logs and every query result the analysis uses, scripts/ adapted from LH012's with an offline replay, a line in investigations/software-updates.md, and a piece only if the record earns one.
