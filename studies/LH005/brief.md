# LH005 study brief

**study:** LH005
**edition:** 0.1
**date opened:** 2026-09-26, about 17:15 UTC, written before any download count was read
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driver session for issue #1 (LH005), from the design in programme.md
**grounded at:** repository commit 892ae44

## Question

Can any public record connect a software release to its installation, and so carry an observation across the boundary LH002 found between what is offered (a release, a pin) and what is taken (what people install or run)?

The programme names the first candidate: the Python Package Index's download records by version and installer. The study asks what those records are, which copies of them can be read, and what they say about how `mcp` 1.27.0 was taken during LH002's window.

## Scope

- **Library and release:** `mcp`, the Model Context Protocol Python SDK, LH002's library (studies/LH002/brief.md). Release 1.27.0, published on PyPI at 2026-04-02T14:48:07Z (Open Source Insights, as LH002 recorded it). The release before, 1.26.0, was published on 24 January 2026; the one after, 1.27.1, on 8 May 2026.
- **Window:** LH002's, 2026-03-26T00:00:00Z to 2026-04-22T23:59:59Z, twenty-eight UTC days, with up to seven days of margin either side where a reading needs it. A contrast period after 1.26.0's publication, if the copy read holds it, of the same length from its publication day.
- **Second hop:** lean-lsp-mcp (LH002's R03) 0.26.0 and 0.26.1, which require `mcp==1.27.0` exactly; dartlab (R06) and the other LH002 cohort packages briefly, only if they add something.
- **Observation:** of a public aggregate of past download requests, read on 26 September 2026, 157 to 185 days after the events. Not of live activity.

## Interpretation boundary

A download is not an installation and an installation is not a run. The record says which of release, download, installation and run each reading reaches, and stops there.

## Access decision

The canonical dataset is Google BigQuery's `bigquery-public-data.pypi.file_downloads`, documented at https://docs.pypi.org/api/bigquery/ and https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/ (to be read and cited in sources.md). Querying it needs a Google Cloud account and credentials, and bills or draws on a free allowance per byte scanned.

**Decision: Lighthouse does not read the BigQuery dataset directly in this study.** Reasons: the dispatch forbids creating an account or reading a credential from the environment, and AGENTS.md says the same of credentials; an account is an irreversible step outside the repository of the kind the programme leaves to a person. The dataset is instead read through public copies and derivatives reachable without an account, and each is assessed as a copy before its counts are trusted:

1. ClickHouse's public ClickPy service (https://clickpy.clickhouse.com/, SQL at https://sql-clickhouse.clickhouse.com/ as user `demo`), which holds tables derived from the BigQuery dataset. Primary source for counts by version, installer and file type, if its schemas and its own statement of how it loads the data bear that out.
2. pypistats.org's API (https://pypistats.org/api/), daily totals with and without mirrors, by Python version and system; about 180 days kept. A cross-check on daily totals.
3. pepy.tech's API (https://pepy.tech/api/v2/projects/mcp), per-version totals. A cross-check on per-version totals, where it needs no key.

This means every count in the record is a copy's count, not BigQuery's, and the record says so. If a copy disagrees with another by more than a few per cent on the same days, the record reports the difference and says which it relies on and why. The linehaul source on GitHub (PyPI's log processor) returned 403 through the session proxy when the driver tried it; its behaviour is taken from documentation only, and the record says what could not be read.

## Readings, in order

1. **Source assessment** (sources.md in this directory), before any count: for BigQuery, ClickPy, pypistats and pepy, the unit, the population, the fields, retention and freshness, how each copy is derived, and the known distortions (mirrors, CI and build caches, local installer caches, corporate proxies and private indexes, `pip download`, scanners). Each statement with its source and read time; anything inferred marked as inferred. For ClickPy, the schemas (DESCRIBE, engine, create query), what the raw table holds and over which dates.
2. **Cross-copy agreement:** for days inside the window that all copies hold, `mcp`'s daily totals from ClickPy against pypistats (with and without mirrors), and per-version totals from ClickPy against pepy where comparable. Differences as derived measurements.
3. **The taken side of 1.27.0:** daily downloads of `mcp` by version across the window and margin; each day's share that was 1.27.0 with its denominator; the first day 1.27.0 appears; the days to reach 10, 25 and 50 per cent. The same by installer class and by file type. 1.26.0's uptake after 24 January for contrast, if held. Weekday and weekend pattern, as interpretation.
4. **The second hop:** lean-lsp-mcp 0.26.0 and 0.26.1 daily downloads by version and installer, set beside `mcp` 1.27.0's; what the aggregate record can and cannot link. dartlab and the rest briefly, only if they add something.
5. **What the record reaches:** release, download, installation, run; and which readings will expire or change, and when.

Every query's text is kept in scripts/, and each run writes its read time into data/. Running the scripts reproduces data/*.csv, subject to the copies' own retention.

## Resource ceiling

Small aggregate queries only against the public ClickHouse demo server, a few dozen in all, each filtered to named projects and dates; no full scan of the raw table across all projects. Stop if the server refuses or rate-limits, and record it. pypistats and pepy: a handful of API calls each. Documentation pages fetched with curl. About ten dollars of this subagent's spend at list rates. No account, no key, no credential.

## Stopping condition

Close when the source has been assessed and 1.27.0's downloads have been read against the window, or when the copies are found unreadable or untrustworthy, which produces a source assessment on its own.

## Intended output

LH005.md (version 0.1), sources.md (the source assessment), one SVG figure of the share of `mcp`'s daily downloads by version across the window with LH002's moves marked, data/ with the tables and read times, scripts/ with the queries.
