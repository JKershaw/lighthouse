# LH013 installer brief: which installers fetch boto3's older versions on Python 3.9, and do they fetch them in walks?

**In short** (not part of the protocol). Most of boto3's downloads from Python 3.9 are of old versions, spread so evenly across hundreds of versions that they look like an installer trying one version after another and throwing each away. Two things in the package index's full download log could test that: which version of the installer made each download, and whether the downloads come in quick runs of descending versions. No free public source carries the installer's version (ClickPy, the free one, drops it), so the main read needs a Google account that a task must name, and it waits until one is; a smaller check, whether the log counts requests for metadata files at all, can run on ClickPy without an account once this brief is committed.

**Brief, written before any outcome it reads, 10 November 2026.**

**study:** LH013 (a follow-up read under the same study; see "Why not a new study")
**edition:** 0.1
**status:** fixed when committed. Stage A (ClickPy, anonymous) may run from 19 November 2026. **Stage B, the main read, waits on a named account**: it runs only when a task names a Google account for BigQuery, and never with a key or token read from the environment.
**date written:** 2026-11-10
**written by:** a research subagent in Claude Code on Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driving session of scheduled run 2026-11-10T1415Z for schedule row LH013-installer-brief. Not yet reviewed.
**grounded at:** LH013.md version 0.2, brief.md edition 0.1 with its amendments, notes/R-0047-lh013-reader.md, proposals.md P-0002 with the keeper's line of 8 November 2026
**cites:** the pages listed under "Pages read for this brief", kept in data/installer-brief-docs/ with read_log.csv

## Why not a new study

The question is LH013's first Next item, on LH013's project and Python, testing an interpretation LH013 (and LH012 before it) left standing. It adds no new population. It reads a new day and a new source, so its results go into LH013's record as a new section with a version bump, not into a new LHnnn.

## Question

On one fixed UTC day, among boto3's downloads that report Python 3.9:

1. **Installer.** Which installers, by name and version, made the downloads of versions below 1.42.97 (the highest boto3 whose Requires-Python admits 3.9), and how does that split differ from the one for 1.42.97 itself?
2. **Walks.** What share of those older downloads fall in short, fast runs of descending versions with identical reported details, the trace a resolver trying candidates newest first would leave (R-0047's burst test), against a baseline in which the same timestamps carry shuffled versions?
3. **Metadata files.** Does the log carry rows for PEP 658 metadata files (file names ending `.metadata`), which decides which pips can leave a walk in the log at all?

It does not ask who or what makes the downloads, and it cannot tell a resolver's walk from a script or scanner that fetches versions in descending order with the same reported details; it can tell both from installations of chosen versions.

## Answers fixed before any read (the documentation question)

These were settled from documentation and schemas alone, read for this brief (pages under "Pages read"). They are observations of sources, not outcomes.

**Does a free public source carry the installer's version? No source read does.** (The keeper, 8 November 2026, asked for this before any account is named.)

- ClickPy's `pypi.pypi`, the per-download table its public SQL serves, has the columns date, country_code, project, type, installer, python_minor, system, version, libc, ci and filename (ClickPy schema, `system.columns`, read 14:23:05 UTC). It keeps the installer's name only, and the day, not the time.
- ClickPy's `pypi.pypi_raw` has `installer` as a pair of name and version, and a microsecond `timestamp`, but its engine is `Null` with 0 rows and 0 bytes (`system.tables`, read 14:23:20 UTC): a pass-through that stores nothing. No table in the `pypi` database visible to the `demo` user is defined from it (read 14:24:42 UTC).
- ClickPy's own README (read 14:21:35 UTC) shows the import as `INSERT INTO pypi SELECT timestamp::Date as date, ..., installer.name as installer, ...`, which drops `installer.version` and truncates the timestamp to a day. LH011 had already recorded that ClickPy drops the installer version (studies/LH011/LH011.md, Limits).
- pypistats.org's API (read 14:24:51 UTC) offers per-package series by Python major, Python minor and operating system, with and without mirrors; no installer dimension at all.
- A pip maintainer wrote on 23 July 2023 that he did not think anyone had "publicly recorded this information outside of PyPI's own BigQuery datasets", and another participant that downloads by pip version are "tracked in the BigQuery DB, but I'm not aware of a site that exposes it easily aside from a few static analyses" (discuss.python.org thread 30124, read 14:25:48 UTC). That is their opinion in 2023, not a census.
- Not checked: pepy.tech, whose installer and CI filters a 2025 post describes as for paid ("pro") accounts (thread 91810); any other mirror of the table.
- BigQuery's own free route, the sandbox, needs no credit card but does need a Google account ("Authenticate with your Google Account, or create a new one"; sandbox page, read 14:24:52 UTC). It is free in money, not free of an account, so it is the account the keeper's decision is about.

**Are metadata-file requests logged in the download table? No public source read says either way.** What the sources do say:

- The package index's BigQuery page says only that the table is "populated through the Linehaul project by streaming download logs from PyPI to BigQuery" (read 14:21:34 UTC, as LH013 found on 2 November).
- linehaul's parser (read 14:22:08 UTC for its user-agent part; its event parser as LH013 kept it, data/docs/linehaul_parser.py.txt) accepts log lines the content network marks `download` or `simple`. A download line carries the project name, version and package type as the network writes them, and the file name is taken from the last part of the URL. Nothing in it filters by file name, so a metadata-file request logged as a download line would arrive with a file name ending `.metadata`; whether the network writes such lines is set in its configuration, outside linehaul. linehaul's loader (main.py, read 14:21:35 UTC) sends download lines to `file_downloads` and `simple` lines (requests for a project's index page) to `simple_requests`.
- The network's configuration was not read: the path tried on raw.githubusercontent.com answered 404 (14:25:13 UTC); github.com's pages answer 403 from this container (CLAUDE.md, 28 September 2026); the session's GitHub tool is limited to this repository. A wall, recorded, not pursued.
- One remark (thread 91810, 13 May 2025) says that uv "might do a dozen metadata HTTP requests where pip might have done one", in a discussion of download counts. It does not say those requests become rows of the table, so it is not evidence either way.

So the question is open in the documentation, and this brief answers it from the data instead: Stage A asks whether boto3 rows with `.metadata` file names exist on the fixed day, in ClickPy, which keeps the file name and needs no account.

## What the writer already knows of the outcome, disclosed

- LH012 and LH013 (W0 21 to 27 September; W1 and W2 28 September to 11 October 2026): about 65 per cent of boto3's downloads report Python 3.9; about 95 per cent of those are of versions below 1.42.97; boto3 is fetched 7 to 8 times as often as botocore on Python 3.9 against under 3 times over all Pythons; the 3.9 profile below 1.42.97 is flat (flatness 0.0007, 0.0007, 0.0005), stepping down at the same depths each week (about 850,000 to 900,000 a version a week for the first hundred versions below the edge, then about 520,000 to 550,000, then about 106,000 to 127,000); boto3's largest cell, Python 3.9, pip, Linux, glibc, no CI flag, US, held about 61 per cent of all its downloads; boto3's older downloads were flagged CI about 6 per cent of the time against about 34 per cent for its newer ones. All of these are weekly, by Python minor and installer name; none is by installer version or by time of day.
- The reader review's reading (R-0047): a level profile in one cell fits a resolver's walk and also any steady process that fetches every version.
- From pip's own history, as LH012 recorded it (studies/LH012/LH012.md; studies/LH013/amendments.md, "The pip date"): pip's resolver has tried versions in turn by default since 20.3 (30 November 2020); from PyPI, pips older than 23.2 (15 July 2023) download each candidate in full, while 23.2 and later read PEP 658 metadata files where offered.
- Read incidentally while reading documentation today, and disclosed: (a) Hugo van Kemenade's post of 24 November 2024 prints one day's download counts for the ten most downloaded projects, boto3 first, for pip only and for all installers, with no Python, version or installer-version split; (b) thread 30124 prints the ten pip versions with most downloads over 30 days to 23 July 2023, across all of PyPI; (c) thread 91810 prints the twenty installer versions with most downloads on one day of May 2025 across all of PyPI, in which pips from 20.3 to 23.1 (for example 23.0.1, 22.3.1, 21.3.1) still made several per cent each; (d) the Packaging Guide and the BigQuery DataFrames notebook print example counts for other projects (pytest; numpy, pandas and their dependencies) from 2017 to 2024. None is for the fixed day, none splits boto3 by Python or installer version, and none enters a measure. Together they say resolver-era pips were still common across PyPI in 2025: a prior, not a finding about boto3.
- No count for the fixed day has been read by anyone in Lighthouse. The writer's expectation, from the above and not from data: older pips make a large part of boto3's 3.9 older downloads. That is a prior.

## Population, unit and the day

- **Project:** boto3. **Python:** downloads whose reported Python is 3.9.x (BigQuery `details.python` beginning `3.9.`; ClickPy `python_minor = '3.9'`).
- **The day, D:** Tuesday 17 November 2026, 00:00:00 to 23:59:59 UTC, chosen now, before any count of it exists. If Stage A finds the day not held by ClickPy for boto3 by 30 November 2026, or Stage B finds the BigQuery partition for D empty for boto3, D moves to the next Tuesday, at most twice, and the move is recorded; D is never chosen by looking at counts.
- **Unit:** the download row (a fetch), described; for the walk test, the run of rows defined below. There is one day and one project, so there is no resampling of projects and no interval across projects; shares are reported with their counts.
- **Version classes:** *edge* is 1.42.97; *older* is any non-pre-release below it; *newer* is above it (not admitted by 3.9; reported, not analysed); pre-releases and versions not in the version list are *other*. The version list is LH013's retained data/versions.csv (PyPI as read 2 November 2026), whose boto3 rows give order, pre-release flag and yanking. No PyPI JSON request is made (the keeper's decision of 8 November 2026 that the JSON API is a limit for now); in Stage B the BigQuery table `bigquery-public-data.pypi.distribution_metadata` may be read for boto3 releases after 2 November, none of which can be at or below the edge.

## Sources and event definitions

- **Stage A, ClickPy** (https://sql-clickhouse.clickhouse.com/, user `demo`, anonymous): `pypi.pypi` for project boto3 and date D, through LH013's scripts/common.py with its robots gate and overflow settings.
- **Stage B, BigQuery** `bigquery-public-data.pypi.file_downloads`, partition D, project boto3, with an account a task names. Columns read: `timestamp`, `file.project`, `file.version`, `file.filename`, `file.type`, `details.installer.name`, `details.installer.version`, `details.python`, `details.implementation.name`, `details.implementation.version`, `details.distro.name`, `details.distro.version`, `details.distro.libc.lib`, `details.distro.libc.version`, `details.system.name`, `details.system.release`, `details.cpu`, `details.openssl_version`, `details.ci`, `country_code`; and `details.installer.subcommand` if the table has it (linehaul's loader serialises a subcommand that uv sends; whether the public table carries it is checked from the table's schema before the read; whether pip sends one was not checked).
- **A fetch** is a row: one download line the content network sent and linehaul parsed. It is not an installation.
- **The clock** is `timestamp`, which linehaul parses from the log line to the second (`%d %b %Y %H:%M:%S`). Rows in the same second have no order; every rule below treats a same-second tie as unordered.
- **Installer classes** (fixed now, from pip's history as LH012 recorded it): *pip old* (pip below 20.3: no backtracking resolver by default); *pip resolver, full fetch* (pip 20.3 up to but not including 23.2); *pip metadata-capable* (pip 23.2 or later); *uv*; *other named* (each named); *version not reported* (pip with no parseable version, kept apart, never assigned).
- **Reported-details group:** rows with identical values of every Stage B column except `timestamp`, `file.*` and `country_code`, and with the same `country_code`. A group is not a machine: many machines can share one.
- **Run:** within one group, rows ordered by `timestamp`, a maximal sequence in which each row is at most 5 seconds after the one before.
- **Walk segment:** within a run, a maximal sequence of at least 5 rows, in time order with same-second ties ordered by descending version, in which each row's version is the next lower boto3 non-pre-release that is not wholly yanked, or skips at most two such versions, below the row before. A walk segment may begin at the edge or below it.
- **Walk share W:** older fetches inside walk segments over all older fetches, for Python 3.9 on D.
- **Shuffled baseline:** within each group and UTC hour, the version labels are permuted among the same timestamps, 20 times, with the permutation fixed by a hash of a row key and the seed 20261110 (no unseeded random function); W is recomputed each time; the baseline is the mean of the 20.
- **Metadata rows:** rows whose `file.filename` ends `.metadata`.

## Measures and tests (fixed now)

Stage A (ClickPy, no account):

- **A1.** Rows for boto3 on D, and the number whose filename ends `.metadata`, by python_minor 3.9 and other, and by installer name. Returned as a few aggregated rows.
- **A2.** boto3's total for D from `pypi_downloads_per_day`, for the table agreement check in Stage B.
- Result class, fixed: *metadata rows present* if `.metadata` rows are at least 1 per cent of boto3's rows on D; *absent* if there are none; *trace* otherwise (reported, treated as present for B3). Absent means that ClickPy, which keeps rows reporting a Python and a system (README's import), carries none for boto3 that day. That is strong evidence that the download table carries none, but not proof: ClickPy's filter could in principle drop them.

Stage B (BigQuery, named account):

- **B1, installer split** (derived measurement). For older and for edge fetches on 3.9: counts and shares by installer class, and by exact installer version for the twenty largest.
- **Test T1.** The *pip resolver, full fetch* class makes more than half of older fetches on 3.9 on D.
- **Test T1b, the comparison that matters.** That class's share among older fetches exceeds its share among edge fetches by at least 20 percentage points. A walk tries the edge first and the older versions after it, while an install that lands on the edge stops there, so a walk-made older profile predicts resolver-era pips overrepresented below the edge relative to at it; a frozen list predicts no such gap.
- **B2, walks** (derived measurement). W for 3.9 on D; the number of walk segments, their median length, and the median seconds between steps; the installer split inside walk segments; and how many walk segments begin at the edge.
- **Test T2.** W is above one half, and W is at least 5 times the shuffled baseline.
- **B3, metadata rows.** The Stage A count repeated in BigQuery, and by installer class. If metadata rows are *present* or *trace*: T1 and T1b are reported but described only, not tested, since pips from 23.2 could then also leave a walk in the log; B2 is computed twice, with metadata rows counted as fetches of their version and without them, the first being the one T2 tests.
- **B4, described only.** The CI flag and subcommand (where present) inside and outside walk segments; the walk share for the edge's neighbours on Python 3.8 and 3.10, if the dry run allows within the ceiling.
- **Table agreement.** boto3's BigQuery total for D against ClickPy's (A2). A difference above 2 per cent is reported and the Stage B figures stand as BigQuery's alone.
- **Number of comparisons:** three tests (T1, T1b, T2) and one classification (Stage A). Anything else read after the counts is labelled post hoc with its count.
- **Whatever comes out**, a test that holds says a pattern is present on one day, not who makes it. T1 and T1b holding with T2 holding is what the walk reading predicts; T2 holding with T1b failing fits walks by newer clients or descending scripts; T2 failing with a low baseline argues against walks on that day.

## Missing evidence

Unknown stays unknown and is never counted as a negative. Rows with no reported Python are outside the population and counted. Rows with no installer version are their own class. If more than a quarter of older 3.9 fetches have no installer version, T1 and T1b are inconclusive. If the shuffled baseline is at least 0.2, groups are too coarse to separate machines and T2 is inconclusive. A Stage A or Stage B query that fails, or is refused by the robots gate, is a missing reading, retried once in the same run, else recorded as not read.

## Overlap with earlier studies

Same project, Python and edge as LH012 and LH013, and their version list. D is a day no study has read. This is a further test, on new data, of the reading LH012 made after its counts and LH013 repeated; not a replication on other projects. The installer classes rest on pip's history as LH012 read it.

## Resource ceiling

- **Stage A:** at most 5 ClickPy queries and 1 billion rows read by ClickHouse's own statistics (`pypi.pypi` is sorted by project and date, so one project-day reads few rows).
- **Stage B, what one day scans, as documented publicly.** BigQuery bills on-demand queries by "the total data processed in the columns you select", "even if you set an explicit LIMIT", with the first 1 TiB a month free and $6.25 per TiB beyond (pricing page, read 14:24:51 UTC). The table is partitioned by day (Packaging Guide; BigQuery DataFrames notebook). No source read says it is clustered by project, and the published figures suggest a project filter does not cut the scan: one day, all projects, two columns (timestamp and project) processed 43,447,720,943 bytes in November 2024 whether 1 or 531,022 projects were returned (van Kemenade, 24 November 2024; the query window there spans parts of two days); seven days of timestamp and project for six named projects processed 270.4 GB in September 2024 (BigQuery DataFrames notebook); 30 days of installer name and version for all of PyPI processed 436.43 GB in July 2023 (thread 30124). So a one-day boto3 query bills the whole day's partition for every column it reads. Extrapolated, not documented: about 20 columns, some of them long strings such as the file name, on a day in late 2026 with more downloads than in 2024, is likely to process a few hundred GB per pass, inside the free terabyte only for one or two passes.
- **So, fixed:** a dry run before every query, whose estimate is logged; one schema query; one extraction pass that writes boto3's Python 3.9 rows for D to a table in the named project (inside the sandbox's 10 GiB lifetime storage), and every later query, including the 20 permutations, reads only that table. Ceiling: 700 GiB billed in all, and never more than the task naming the account allows. If the extraction's dry run exceeds 600 GiB, columns are dropped in this order until it fits: `details.distro.version`, `details.system.release`, `details.cpu`, `details.openssl_version`, `details.implementation.version`, `details.distro.libc.version`; each drop is recorded and makes groups coarser. If it still does not fit, Stage B stops unread.
- About $5 of the research agent's own model spend at list rates. No key or token is read from the environment; credentials are used only as the task naming the account says.

## Stopping condition

Stage A closes when A1 and A2 are read, or at its ceiling. Stage B closes when B1 to B3 and the three tests are read, or at a ceiling with the unread part stated. Nothing above is changed after any count of D is read; a later change is a dated amendment, labelled post hoc if made after counts were seen. If no account is named, the brief stays waiting; the day's partition stays in BigQuery, so waiting loses nothing but time.

## What would leave it inconclusive

- No account named (Stage B waits; Stage A still answers the metadata question).
- D and both fallback days unusable.
- More than a quarter of older 3.9 fetches without an installer version (T1, T1b).
- A shuffled baseline of 0.2 or more (T2).
- The extraction over the ceiling after every permitted column drop.
- Whatever it finds: one day; one project; fetches, not installations; a group is not a machine; a walk segment cannot be told from a script fetching descending versions with the same details; and a missing metadata row in ClickPy is not proof of its absence in the table.

## Intended output

A new section and version of studies/LH013/LH013.md (Stage A alone may be a dated note there), the queries and aggregated results in data/installer/, the scripts in scripts/ with an offline replay of the walk computation from the extracted aggregates where they are kept, and lines in programme.md and P-0002. A piece only if the record earns one.

## Pages read for this brief

All on 10 November 2026, UTC, each checked first with `scripts/robots_gate.py` (provider anthropic); each was allowed. Bodies in data/installer-brief-docs/ with email addresses withheld, and read_log.csv there gives time, URL, robots result, status and the SHA-256 of the bytes received. First attempts at the first four URLs, about 14:21, were fetched and discarded unread by a fault in this agent's helper, then fetched again; those requests are in the log.

- **P1.** PyPI User Documentation, "BigQuery Datasets", https://docs.pypi.org/api/bigquery/, 14:21:34. Undated. Names `bigquery-public-data.pypi.file_downloads`, filled by linehaul from PyPI's download logs, and `distribution_metadata`; nothing on metadata files or clustering.
- **P2.** Python Packaging User Guide, "Analyzing PyPI package downloads", https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/, 14:21:35 (page last updated 10 November 2026). Needs "a Google account" and a Cloud project; "up to 1TB of queries per month using the BigQuery free tier without a credit card"; one entry "for each download"; lists `details.installer.name` among columns; the table is partitioned; ClickPy offers "free direct SQL access".
- **P3.** linehaul-cloud-function main.py, https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/main.py, 14:21:35. Download lines to `file_downloads`, `simple` lines to `simple_requests`; serialises the installer's subcommand.
- **P4.** ClickPy README, https://raw.githubusercontent.com/ClickHouse/clickpy/main/README.md, 14:21:35. Import drops `installer.version` and truncates the timestamp to a date; export of the whole table described as 15 TB.
- **P5.** linehaul ua/datastructures.py, https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/linehaul/ua/datastructures.py, 14:21:58. Installer has name, version and subcommand.
- **P6.** linehaul ua/parser.py, https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/linehaul/ua/parser.py, 14:22:08. pip from 6.0 and uv from 0.1.22 send JSON details after their name and version.
- **P7 to P9.** ClickPy schema queries (no table rows read): `system.columns` for database `pypi`, 14:23:05; `system.tables` for `pypi` and `pypi_raw`, 14:23:20 (`pypi_raw`: engine Null, 0 rows); tables defined from `pypi_raw`, 14:24:42 (none besides itself).
- **P10.** Hugo van Kemenade, "A surprising thing about PyPI's BigQuery data", 24 November 2024, https://hugovk.dev/blog/2024/a-surprising-thing-about-pypis-bigquery-data/, 14:23:53. Bytes processed by one-day queries; the row limit does not change them; contains counts disclosed above.
- **P11.** discuss.python.org thread 837, "New PyPI Statistics - Simple API Requests", 6 February 2019 and 2020 replies, 14:23:53. `simple_requests` logs requests to `/simple/{project}/`, partitioned by timestamp and clustered on project; says nothing of the download table's clustering.
- **P12.** BigQuery DataFrames notebook on PyPI downloads, https://google.github.io/bigframes/notebooks/dataframes/pypi.html, 14:23:55. "The PyPI and deps.dev tables are partitioned by date"; 270.4 GB for seven days of two columns for six projects.
- **P13.** ClickPy ClickHouse.md, https://raw.githubusercontent.com/ClickHouse/clickpy/main/ClickHouse.md, 14:23:55. DDL of the aggregate tables; none has an installer version.
- **P14.** pypistats.org API, https://pypistats.org/api/, 14:24:51. Endpoints recent, overall, python_major, python_minor, system; no installer.
- **P15.** Google Cloud, BigQuery pricing, https://cloud.google.com/bigquery/pricing, 14:24:51 (excerpts kept). On-demand billing by columns processed, 1 TiB a month free, $6.25 per TiB beyond, 10 MB minimum per table referenced.
- **P16.** Google Cloud, BigQuery sandbox, https://cloud.google.com/bigquery/docs/sandbox, 14:24:52 (excerpts kept). No credit card or billing account; a Google account; 1 TiB of queries a month; 10 GiB lifetime storage; tables expire after 60 days.
- **P17.** discuss.python.org thread 30124, "Pip versions in the wild", July 2023, 14:25:48. Installer version is in BigQuery only; counts disclosed above; 436.43 GB for a 30-day query.
- **P18.** discuss.python.org thread 91810, "PyPI downloads statistics and continuous integration", May 2025, 14:25:49. pip has sent the CI flag since 19.1 and uv since 0.1.22; uv's metadata requests remark; counts disclosed above.
- **Not fetched:** https://raw.githubusercontent.com/pypi/infra/main/terraform/file-hosting/vcl/main.vcl answered 404 (14:25:13); the pypi/infra repository through the session's GitHub tool, refused (limited to this repository).
- **Leads not opened** (four web searches, 14:24 to 14:26): Hoffa's Medium post on a reclustered copy of the table; pypinfo's pages on PyPI and forks on GitHub; pypi-download-stats; ClickHouse's "one trillion rows" post; Fastly's logging documentation; warehouse.pypa.io's older copy of P1.
