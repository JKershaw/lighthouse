# LH014 study brief

**Brief, written before any outcome was read, 29 September 2026.**

**study:** LH014
**edition:** 0.1
**status:** written in phase 1 of three, before the ranked list, any project's PyPI metadata or any download count was read; to be snapshotted before phase 2 reads the list
**date opened:** 2026-09-29, after reading AGENTS.md, programme.md's Next, LH011's brief, amendment 1, record 0.3 and scripts, LH012's brief and amendments, LH013's brief, and the phase 1 reads below
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), for issue #16, to a design the driving session fixed (bands, sample size, measures, ceilings); the writer's own choices, made before any outcome was read, are listed at the end
**grounded at:** repository commit 5192033, with this study's uncommitted files in studies/LH014/
**issue:** #16 (JKershaw/lighthouse); programme.md, Next, "Taken while LH013 waits"

## Question

Below the fifty most downloaded Python projects, does a new newest version reach half of its project's downloads within two days as a rule, and does its share settle by day 2? Asked of two bands of ClickPy's August 2026 ranking, positions 51 to 500 and 501 to 5,000, for versions released from April to August 2026, by the rules LH011 and LH012 applied to the top fifty.

## What the writer already knows of the outcome, disclosed

- LH011: in the top fifty, 26 of 37 projects had most releases reach half within two days (70.3 per cent, interval 54.1 to 83.8), 21 every release and 11 none, and releases that reached half usually did so on day 1; 127 of 424 releases pooled; new releases' early pip and uv downloads were flagged CI less often than the replaced ones' (median of project medians -6.6 points). LH012: shares settled by day 2 for 28 of 32 projects on November to March releases, and for 35 of 37 on LH011's releases as a description; the ten-point band let boto3's and aiobotocore's small shares grow by about two thirds.
- `mcp`: LH005 read 1.27.0 (2 April 2026) at 22 per cent of downloads on day 0, 48 on day 1 and 45 to 71 after; LH007 read 1.28.x at 43 to 62 per cent in June and July (as LH011's brief quotes them). Both are in this window.
- pypistats.org's FAQ (read 12:30 UTC) says that mirrors download each new release when they sync, which would weigh more on a small project's days 0 and 1. The writer has no other expectation.
- The writer has seen no ranking, rank column or count, and does not know which projects hold positions 51 to 5,000. Others have: LH008, LH010 and LH011 kept August rankings read on 27 and 28 September, and the driving session set the bands and the sample size. The draw rule, salt and seed are the writer's.

## Population and unit

- **Frame** (phase 2): `pypi.pypi_downloads_per_month`, month 2026-08-01, summed per project, ordered by the sum descending and then by name in byte order (LH011's tie-break), first 5,100 rows. LH011's packaging and installer tooling (its brief, Population and unit; 17 names) is removed, each with its raw rank recorded, and positions are counted after removal. LH011's 50 are positions 1 to 50 by construction: if the list places one of them below 50th, all 50 are removed by name wherever they fall, positions from 51 run over the rest, and the displacement is recorded. Names are compared with these lists after PEP 503 normalisation.
- **Bands**: A, positions 51 to 500 (450 projects); B, 501 to 5,000 (4,500). A tie in the August sum across an edge (50, 500 or 5,000) is recorded; the name order decides.
- **Draw**: in each band, projects are ordered by the hexadecimal SHA-256 of the UTF-8 bytes of `LH014-20260929:` followed by the name as ClickPy stores it, ascending. Walking that order, each project's PyPI JSON (https://pypi.org/pypi/{name}/json, redirects followed) is read, and the first 80 that PyPI serves are drawn. **Not served** is 404 or 410 on two reads a minute or more apart; any other failure is retried three times, then recorded as not read; either way the next project is taken. The population is the band's projects that PyPI served at the read. No outcome enters the draw.
- **Releases**: LH011's rule (its brief, Population and unit, as its frame.py applies it, so versions with no file or no PEP 440 parse take no part): not a pre-release or development release by PEP 440, first file uploaded from 2026-04-01T00:00:00Z to 2026-08-31T23:59:59Z, and then higher than every earlier-uploaded non-pre-release version; yanked versions kept and flagged; the replaced release is the newest before it. Added for a case LH011 never met, since each of its 424 releases replaced one: a project's first non-pre-release version replaces nothing and has a share of one by construction, so it does not qualify, and is recorded.
- **Unit**: the project. It has a known outcome when one of its releases has; "most" is more than half of its releases with a known outcome. Pooled figures over releases go beside the per-project ones, never in their place.
- **CI subsample** (LH011): each project's first qualifying release in each calendar month, April to August.

## Sources

ClickPy's public SQL [S21], user `demo`, anonymously. By its definitions (read 12:28 UTC; data/clickpy_schema.csv, clickpy_columns.csv), every table below except `pypi.pypi` is filled by a materialised view counting rows of `pypi.pypi`: `pypi_downloads_per_month` (the frame); `max(date)` of each table read, bounded at the cut (days held, no count); `pypi_downloads_per_day` (the gap rule); `pypi_downloads_per_day_by_version` (every share of the tested measures); `pypi_downloads_per_day_by_version_by_installer_by_type` (the mirror readings, and its distinct installer names, read without counts); and `pypi.pypi`, the only table that carries the CI flag, for the CI subsample. PyPI's JSON API. The flag's meaning is LH011's reading of pip 26.0.1 and 26.2.1 and uv 0.11.2 and 0.12.8, current at either end of this window, not read again. pypistats.org's FAQ (https://pypistats.org/faqs, read 12:30:56 UTC) names the mirror tools; pypistats's counts are not read, since LH011's cross-check against them agreed on all 15 days. No BigQuery, GitHub page or key.

## Events, clocks and measures

UTC days; ClickPy keeps the day, not the time.

- **Day 0** is the day of the first upload, with the hours left in it recorded.
- **The cut**: no download on any day after 2026-09-27 is read, the last day LH011 read, so nothing of LH013's weeks (28 September to 11 October) is read. Every count query bounds its dates there, and scripts/common.py refuses one that does not. A later day's measures are unknown, as LH011 treated days ClickPy did not yet hold.
- **At-or-newer share on day d** (LH011): downloads that day of the release or of any higher non-pre-release version PyPI lists (matched by exact string), over all the project's downloads that day, both from `pypi_downloads_per_day_by_version`; **own share** likewise, for the release alone. **Reached half within two days**: a share of at least 0.5 on day 1 or day 2; unknown when neither reaches it and either is unknown. **Days to half**: the first day, 0 to 30, at 0.5 or more; otherwise not reached by day 30, or by 27 September.
- **Settling** (LH012): Δ is the share on day 30 minus the share on day 2, in points; a release settles when |Δ| is at most 10; Δ is unknown when day 2 or day 30 is a gap, has no row or falls after 27 September, as for every release of 29 to 31 August. A project settles when more than half of its releases with a known Δ do. Beside it go LH012's descriptors: the ratio of the day-2 to the day-30 share, and Δ from day 1.
- **CI share** (LH011): over days 0 to 2 pooled, the share of the release's `pip` and `uv` downloads flagged true, minus the replaced release's share on the same days, in points; unknown when either has no `pip` or `uv` downloads then, or a day is a gap.
- **Mirror class**: the installer names equal, ignoring case, to `bandersnatch`, `z3c.pypimirror`, `Artifactory` or `devpi`, the FAQ's four, among the installer table's distinct names for the drawn projects from 25 March to 27 September 2026; a name that only contains one is listed and left out. **M1**: the at-or-newer share on days 0, 1 and 2 from the installer table, over all installers and without the class, and their difference; and whether each release's "reached half within two days" changes. One table gives both shares, so the difference is the mirrors'. **M2**: the class's downloads of the release's own version on day 0, on day 1 and on both, as a count and as a share of the release's own downloads, from the same table.

## Missing evidence

Unknown stays unknown and is never counted as a negative.

- **Gaps** (LH011): a day with no row for a project that has rows on the days either side, or on which the total over all drawn projects in `pypi_downloads_per_day` falls below half the median of the days read from d-3 to d+3, is a gap; its measures are unknown, as are those of a day with no downloads.
- **Coverage**: each table's last day held for each drawn project, up to the cut, is read before any count; a day not held is unknown.
- **The flag** is known only for the installers `pip` and `uv`; other installers, and downloads with none, are "flag not known", reported with their volume.
- **Versions** ClickPy holds and PyPI does not list count in denominators only. **Projects** without a qualifying release have no outcome and stay among the 80, counted.
- **Queries** that fail or reach a limit are discarded, logged and split; what no split can read is unknown.
- **Checks**: ClickPy's per-day totals against its by-version totals, as LH011 did, and its installer table against its by-version table on days 0 to 2, both reported.

## Tests, descriptions and conventions

- **Primary, tested, per band**: the share of projects with a known outcome whose releases mostly reached half within two days, with its interval. LH011's convention: **as a rule** at three quarters or more, **not as a rule** below one half, **for some projects** between. Beside it, LH011's descriptors: the median and quartiles of project median day-1 shares, the pooled share of releases, the median days to half, and the projects with no release at half by day 30.
- **Settling, tested, per band**: the share of projects with a known Δ that settle, with its interval, on releases new to Lighthouse in the window LH011 read for other projects. LH012's convention: **holds as a rule** at three quarters or more, **holds for some projects** from one half to three quarters, **fails** below one half.
- **Described only, per band**: for CI, the median of project median differences with its interval, and the projects below zero; for M1 and M2, the median and quartiles of project medians, and for M1 the projects whose "most releases reached half" changes without mirrors.
- **Beside the top fifty**: LH011's 26 of 37 (70.3 per cent, 54.1 to 83.8) and LH012's figures, as a description. No test compares the bands, or a band with the top fifty; a difference is described with both intervals and is not a cause.
- **Intervals**: percentile intervals with linear interpolation (LH011's `pct`) over 10,000 resamples of the band's projects with a known measure, with replacement, from one Python `random.Random(20260929)` in this order: A primary, B primary, A settling, B settling, A CI, B CI, then the same six without the overlap projects. No finite-population correction is made, so band A's (80 of 450) are wider than they need be.
- **No subgroup** beyond the bands: none by kind of release, and none of AI or machine-learning projects.
- **Comparisons**: four tests, each also given without the overlap projects as a sensitivity reading, not a further test, and the descriptions above. Any other reading made after counts are seen is labelled post hoc, with its number of comparisons.

## Overlap with earlier studies

- None of LH011's 50 can be drawn. The releases are new to Lighthouse; the window and the days are LH011's. This widens to new projects; it does not replicate.
- **Overlap projects** (data/overlap_projects.csv, 40 names): `mcp` (LH005, LH007); the nine other projects whose downloads LH005 read in ClickPy; and the other 30 of LH010's 43 libraries, which include LH008's and LH009's, that are neither tooling nor among LH011's 50. Any drawn is named, and every band result is also given without them.
- **LH012's dependents**: LH012 read per-version downloads of 274 projects for 21 to 27 September 2026 (studies/LH012/data/deps/versions/), chosen from LH010's top 500 and so mostly in band A; here those days are only late days of releases from 22 to 31 August. A drawn one is named, with such releases counted. LH012 read their requirements on its 37 and their version mix, not their own releases, and nothing of it is reused, so results are not given without them.
- LH013 reads LH011's 37 after 27 September: nothing is shared.

## Resource ceiling

- **ClickPy**: at most 800 queries and 60 billion rows read in all phases, by ClickHouse's own statistics, phase 1's five queries (2,128 rows) included; each logged in data/read_log.csv; every aggregation server-side. The `demo` user (data/clickpy_server.csv, read 12:28 UTC) fails a query past 10,000 result rows, 10 MB or 60 seconds, but past 1,000,000,000 rows or 50 GB read its `read_overflow_mode`, `break`, means "stop executing the query and return the partial result, as if the source data ran out" (https://clickhouse.com/docs/operations/settings/query-complexity, read 12:30:29 UTC). So every query on the `pypi` database sets `read_overflow_mode = 'throw'`, which `demo` may do (checked 12:30:47 UTC), and one that reports reading either limit counts as failed. LH011's 104 CI reads of the top fifty read 5.8 billion rows.
- **PyPI JSON**: at most 400 requests. **Documentation**: at most 5 page reads in all, phase 1's two included.
- About six dollars of the research agent's own model spend at list rates across the three phases; scratch space at most 2 GB; anonymous reads only, with no key or token.

## Stopping condition

Phase 2 reads the frame, draws, reads PyPI's JSON, derives the releases and the subsample, lists the mirror installer names, reads coverage, and compares the list with the rankings LH008, LH010 and LH011 kept (differences reported, the frame unchanged); all of it is recorded as amendment 1 and snapshotted before any daily, per-version, installer or CI count is read, which scripts/common.py's phase gate enforces. Counts are then read with projects alternating between the bands in draw order (A1, B1, A2 and so on): daily totals; per-version counts from seven days before each project's first day 0 to 30 days after its last, or to 27 September; mirror counts; CI counts. Close when all are read, or at a ceiling with the unread part stated; no description displaces a band's primary measure. The question, bands, draw, release rule, measures, conventions and missing-evidence rules do not change after any count is read; a later change is a dated amendment, labelled post hoc if made after counts were seen.

## What would leave it inconclusive

- A band's primary measure with fewer than 25 projects with a known outcome; its settling test with fewer than 20 (LH012's threshold).
- ClickPy's per-day and by-version totals differing by more than five per cent on more than a fifth of the project-days compared: the counts are then reported as ClickPy's, with the disagreement.
- Whatever it finds, it cannot say why one band is faster or slower than another: rank is not a cause, a download is a fetch weighted by how often each environment fetches, and mirrors beyond the four, scanners and caches are not separated.

## Replay and intended output

studies/LH014/replay.sh, on LH011's model, reruns the draw, the release frame and the analysis offline, compares every output byte for byte, and checks the logs against these ceilings and this brief against its snapshot hash. Also LH014.md (version 0.1), sources.md, data/, scripts/, a line in investigations/software-updates.md, and a piece only if the record earns one.

## What was read before this brief (phase 1)

On 29 September 2026 from 12:28 to 12:31 UTC, logged in data/read_log.csv and made by scripts/collect_schema.py; no download count, rank or project metadata. ClickPy, five queries on the `system` database only: the server, the `demo` user's settings, the `pypi` tables' definitions (without row totals) and columns, and whether a query may set `read_overflow_mode`. Two documentation pages, kept in scratch space only (above). From the repository beyond the header: library names from LH008's and LH010's events.csv and LH009's file names, file names in LH012's data/deps/, and the query texts in the read logs of LH005 and LH007 to LH010.

## Choices made by the writer

All made on 29 September 2026, before any outcome, list or project metadata was read.

1. LH011's 50 are removed by name wherever the list places them.
2. Ties are broken by name in byte order, as LH011's query did.
3. The draw: the SHA-256 of `LH014-20260929:` and the name, ascending; projects PyPI does not serve are skipped.
4. A project's first non-pre-release version does not qualify.
5. Reading alternates between the bands in draw order, with descriptions after both bands' primary counts.
6. The gap rule's total is over all drawn projects of both bands.
7. Seed 20260929, the brief's date, as LH011 and LH012 did; one generator in a fixed order; no finite-population correction.
8. The mirror class is the FAQ's four names, ignoring case, and nothing that only contains one; M1 is computed within the installer table.
9. LH011's and LH012's descriptors go beside the tests; no breakdown by kind of release.
10. `read_overflow_mode = 'throw'` on every query of the `pypi` database, a read-limit guard, and a code gate for the phases and the cut.
11. The overlap set adds LH005's nine other projects; LH012's dependents are named, not removed.
12. pypistats's counts are not read; ClickPy's two-table checks are kept, with the threshold LH011 set for its pypistats cross-check (five per cent on a fifth of days).
13. The list is compared with earlier studies' rankings, as a description.
