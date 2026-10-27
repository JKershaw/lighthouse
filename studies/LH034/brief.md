# LH034: How does the Node.js security release of 21 October 2026 reach nodejs.org's downloads, beside the Python releases and the PHP fix?

**Protocol 0.1, fixed 27 October 2026, about 18:15 UTC, before this study's first read of any outcome.** Writer: a Claude Code driving session (Claude Opus 5.5), at the keeper's suggestion of the same evening that a recent Node.js fix might be a third point beside the PHP and Python studies.

## Question

From the Node.js security releases of 21 October 2026 (v22.23.4, v24.22.1 and v26.12.1, ten CVEs, the highest rated high by the project), what share of the day's nodejs.org downloads in each fixed release line is at or above the fixed release, day by day; what share of all version-attributed downloads comes from release lines the release does not fix; and how do those curves sit beside the at-or-newer download shares Python releases took in LH011, and beside the patched shares of PHP services LH033 reads from Censys for a release on the same day?

This is the first Lighthouse comparison where two ecosystems are measured in the same unit, a download share, from first-party logs. It describes shapes; it does not rank the ecosystems and cannot say why a curve has its shape.

## The event, and which clock counts

The project's advisory, `https://nodejs.org/en/blog/vulnerability/october-2026-security-releases`, read 27 October 2026 at about 18:00 UTC, dated Wednesday 21 October 2026, announced the three releases and says end-of-life versions are always affected when a security release occurs. nodejs.org's `dist/index.json` dates v22.23.4 and v24.22.1 to 20 October and v26.12.1 to 21 October, all flagged `security`; the directory listings of `/dist/v22.23.4/`, `/dist/v24.22.1/` and `/dist/v26.12.1/` show their files at 21 Oct 2026 10:32, 10:34 and 10:36 (the listing's time zone is not stated). The npm `node` package published the three versions on 22 October at 00:48 to 00:54 UTC; it is not used. **Day 0 is 21 October 2026**, the UTC day the binaries were posted, which is also LH033's day 0. Only completed UTC days enter the measures.

The fixed lines are 22, 24 and 26. Every other line, including 20 and 25, which have reached end of life, and all odd and older lines, is a line the release does not fix.

## Source, and what it counts

**nodejs.org's daily download summaries**, one JSON file per day at `https://storage.googleapis.com/access-logs-summaries-nodejs/nodejs.org-access.log.YYYYMMDD.json`, linked as the "current" metrics from `https://nodejs.org/metrics/`. Their structure was read once, at about 18:05 UTC on 27 October, from a file of 10 June 2025, printing keys and types only: `bytes`, `total`, and counts by `country`, `version` (keys such as `v22.16.0`), `os` (including `headers` and `src`) and `arch`. The version and os counts are separate tables, not crossed. A file for 20261020 to 20261024 exists, each written about 11:00 UTC the next day; no count in any file from 2026 has been read.

By the metrics page's description (written for the historic logs, assumed to hold for the current summaries, not checked against the build code, which the session's GitHub access does not reach), the data are requests matching known binary and source files in `/dist` and `/download/release`, with the version taken from the path; header tarballs, which node-gyp fetches for the version a machine runs when it builds a native addon, are among them and cannot be separated by version; requests through `latest` links have no version and are outside the version table. A download here is a request. It is not a machine, an install or a user. It sees only fetches from nodejs.org itself: installers such as nvm, n, fnm and volta fetch from it, but distribution packages, Homebrew bottles, official container images once built, corporate mirrors and caches, and runners that keep their own copy are not counted. Which day boundary the file name uses (the "last entry" day, per the page) is taken as the UTC day of the downloads and stated as an assumption.

## What is already known of the outcome

No Node.js download count of any version for any day in 2026. The session has read: the advisory (above); the search-tool summary of a web search for "Node.js security release October 2026 CVE" at about 17:55 UTC, which named the CVEs and fixed versions and relayed a secondary claim of no known exploitation, with no uptake figure; release metadata from `dist/index.json`, the three `/dist/` listings and the npm registry's `node` package times; PyPI metadata for `nodejs-wheel-binaries`, `nodejs-wheel` and `nodejs-bin` (none has published the fixed versions, so none is used); the metrics page; the summary file list; and one 2025 file's structure. LH033's PHP figures to day 5 are known to this session and are LH033's, not new evidence here. The Python figures were all read in September.

## Reads and schedule

- One GET per day's file, the raw body kept gzipped with UTC time, HTTP status and SHA-256, never overwritten. The baseline read, immediately after this brief is committed, takes the days 23 September to 26 October 2026 where published (the pre-release month and days 0 to 5) and the days 28 July to 27 August 2026 for the comparator below. Later reads take each newly published day with the PHP daily runs through 30 October, then with LH033's Monday and Thursday reads, and a read on 22 November holds day 30 (20 November).
- At the read holding day 30, days 0 to 7 are fetched again once; if any differs from the first copy, both are reported and the first is that day's value, with the revision stated.
- No login, paid service, raw log, scan of any host or contact with anyone. About 80 GETs over the study.

## Measures, fixed now

1. **At-or-newer share by line and day**: for each of lines 22, 24 and 26 and each day 0 to 30, downloads of versions in the line at or above the fixed release over all downloads of versions in that line. Summaries: the first day it reaches half, if any; the share on days 1, 2, 7, 14 and 30; one minus the day-30 share.
2. **The unfixed tail**: for each day from 23 September to day 30, downloads of versions in lines the release does not fix as a share of all version-attributed downloads, with lines 20 and 25 also given separately; and the share of `total` with no version (`total` minus the sum of the version table), stated beside it.
3. **Distance behind the fix**: on day 30, within each fixed line, the share of the line's downloads one release behind, two to four, and five or more, by release order in `dist/index.json`.
4. **The ordinary security release, same instrument**: measure 1 for the previous release in each line that `dist/index.json` flags `security`, chosen by that rule now: v22.23.2, v24.18.1 and v26.5.1, dated 28 July 2026, with day 0 the date `dist/index.json` gives v26.5.1 and the at-or-newer rule counting any later release in the line. Days 1, 2, 7, 14 and 30.

The comparators, from retained tables only, named now so that none is chosen after the Node curves are seen:

- From `studies/LH011/data/analysis/release_days.csv`, via `studies/LH033/data/python_side.json`: the at-or-newer download share on days 1, 2, 7, 14 and 30 for LH008's four Python security fixes, and the median of the 37 projects' medians on the same days. These share Node's unit, a day's download share, from a different index and population.
- From LH033's own tables: the Censys patched share for PHP 8.2 to 8.5 on the same days, as LH033 reports them. A different unit (standing services as last rescanned) for a release on the same day; set beside, not merged.

The statements the record may make are of the form "on day N, the at-or-newer share in line L was X, where the Python fixes' share was Y (same unit, different index) and the PHP branch's Censys patched share was Z (different unit)". It may describe one curve as higher or rising faster. It may not call one ecosystem faster or safer, attribute a difference to severity, publicity, exploitation reports, AI or any cause, or turn a download into a machine, a site or a user.

## Overlap

The Python figures are LH008's and LH011's retained data and the PHP figures LH033's; their reuse is disclosed, and nothing in them is new here. No Node.js release has been read before by Lighthouse.

## Stopping and what would leave it inconclusive

Stop after the read holding day 30, at the latest on 30 November 2026. An interim checkpoint after the read of 29 or 30 October may report measures 1, 2 and 4 to the last completed published day, labelled interim. Measure 1 is inconclusive for a line if a day's file is missing for days 0 to 2, if the version table changes shape, or if a re-read of days 0 to 7 differs by more than five points of share. If the summaries stop being published, the study reports what its reads hold and when they stopped. The resource ceiling is the GETs above and about $15 of model spend for the reads and checkpoints, recorded in the close-out; any public piece takes the full review sequence and its own spend.
