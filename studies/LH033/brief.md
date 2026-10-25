# LH033: How does the PHP emergency fix reach the services others count, beside how Python releases reached downloads?

**Protocol 0.1, fixed 25 October 2026, before this study's first read of any outcome.** Writer: a Claude Code driving session (Claude Opus 5.5), at the keeper's request of the same morning to compare the PHP fix's long tail with the earlier Python findings, using projects that already track it as sources until Lighthouse can collect such data itself.

## Question

From the PHP security releases of 21 October 2026 (8.2.35, 8.3.36, 8.4.27, 8.5.12; CVE-2026-109618 and CVE-2026-109619), how does the share of version-reporting, internet-facing PHP services that Censys counts as patched change day by day in each fixed branch, how many such services sit on branches PHP did not fix at all, and how do those curves sit beside the share of downloads Python releases took in LH011 and the pin moves LH008 timed?

The comparison is of shapes measured in different units by different instruments. It describes; it does not rank the two ecosystems, and it cannot say why either curve has the shape it has.

## Sources, and what each counts

**Primary: Censys ARC's public PHP2Shell dashboard**, JSON at `https://php2shell.censys.com/api/data`, a third-party tracker used as a source, attributed, under the keeper's instruction. By its own notes it counts services (an address or hostname with a port), not machines or organisations; it classes each by the PHP version the service reports as affected, affected with no fix in its branch (`affected_nofix`), patched or unknown; it updates hourly and keeps one bar per UTC day since `tracking_since` 2026-10-21; "patched" is a service seen on an affected version and later on a fixed one; a change can lag by hours, and by up to about a week for some websites; services that hide their version are unknown; and counts of affected are an upper bound because distributions backport fixes without changing the version string. That last bias is concrete here: Ubuntu's fixed noble package is `8.3.6-0ubuntu0.24.04.13` (LH018), which reports itself as 8.3.6. So a Censys patched share is a floor on the share of these services that are protected, not an estimate of it. The fields used are `snapshot.branch_history` (day, branch, patched, targets), `snapshot.history` (day, status, targets), `snapshot.branch_versions` (branch, version, targets), `snapshot.branches` (branch, status, targets), `snapshot.kpi` and `snapshot.refreshed_at`. Censys's general terms were not read; if they forbid keeping copies, the raw files leave the repository and their hashes and the derived tables stay.

**Secondary: W3Techs**, `https://w3techs.com/technologies/details/pl-php/8.2` to `/8.5` and the matching `history_details` pages: patch-level shares among websites using each minor, from a sample of well over 20 million sites each visited about once a month, so a day's figure blends a month of crawls. Version detection is not described. Quoted with a dated reference and a link, as its terms require.

**Context: Packagist's PHP statistics**, `https://packagist.org/php-statistics`: Composer package installs by PHP minor version, daily since May 2021. Minor only, so it cannot show a patch; it is read once, for the share of installs from PHP branches with no upstream fix (8.1 and older) over September 2026, the month before the event: the flow-side size of the tail that no fix reaches.

## What is already known of the outcome

Nothing from Censys's or W3Techs's PHP 8 figures. A discovery subagent (25 October, 08:38 to 08:52 UTC; its report is kept as `discovery.md`) read the dashboard's text and JSON with every digit masked, and W3Techs's PHP 8 pages without figures. This session then read the JSON's structure once at about 08:53 UTC, printing keys, types, list lengths and category labels only, and deleted the file unread. The labels show branches from 3.0 to 8.5 in the current snapshot and five days in the daily series. The subagent saw, in search-tool summaries it did not open, host and service counts relayed by CybelAngel from Mallory's Shodan counts of 20 October (before the release), from Infrawatch and from mySites.guru, and a summary of a Censys post on WordPress sites running unsupported PHP, date unknown; it recorded none of the figures. Lighthouse's own records show fixed-version images and distributor packages on 21 and 22 October (LH018, LH019, LH025), which is supply, not uptake. The Python figures below were all read in September.

## Reads and schedule

- Censys: one GET of the JSON a read, the raw body kept gzipped with UTC time, HTTP status and SHA-256, never overwritten. A read at baseline on 25 October, then once a UTC day at about 06:30 through 30 October with LH030, then on LH030's Monday and Thursday reads, with a read on 21 or 22 November that holds day 30 (20 November) complete. A missed read stays missed. Each read is kept as it was; if a later read revises an earlier day's figures, both are reported and the earliest read holding a completed day is that day's value, with the revision stated.
- W3Techs: the four detail pages and four history pages, eight GETs, at baseline, then on Mondays (26 October, 2, 9 and 16 November) and on 21 or 22 November.
- Packagist: one GET at baseline.
- No login, paid service, search interface, scan of any host, or contact with anyone. About 40 GETs to Censys and 50 to W3Techs over the study.

## Measures, fixed now

Day 0 is 21 October 2026 (UTC), PHP's release day, as LH011's day 0 is a release's upload day. Only completed UTC days are used.

1. **Patched share by branch and day**: for each of 8.2 to 8.5 and each day 0 to 30, `patched / targets` from `branch_history`. Summaries: the day each branch first reaches half, if any; the share on days 1, 2, 7, 14 and 30; and one minus the day-30 share, the services in the branch still not counted patched a month on.
2. **The unfixed tail**: for each day, `affected_nofix` as a share of version-reporting services (`affected + affected_nofix + patched` in `history`), and unknown as a share of all `targets`, stated beside it.
3. **Distance behind the fix**: on the read holding day 30, within each fixed branch, the share of version-reporting services at each patch number below the fixed release, grouped as one release behind, two to four, and five or more (by patch number), from `branch_versions`.
4. **The second view**: W3Techs's share of websites at or above the fixed patch, within each minor, at each read, and its monthly points of 1 October, 1 November and 1 December 2026 where published.
5. **The flow-side tail**: Packagist's share of September 2026 installs from 8.1 and older.

The Python comparators, computed from retained tables only (no new Python read), named now so that none is chosen after the PHP curves are seen:

- From `studies/LH011/data/analysis/release_days.csv`, the at-or-newer download share on days 1, 2, 7, 14 and 30 for LH008's four security fixes (urllib3 2.7.0, cryptography 48.0.1, pyjwt 2.13.0, starlette 1.1.0), and, over the 37 projects, the median of project medians on the same days.
- From LH011's record, the share of releases reaching half by day 2 (26 of 37 projects by its rule) and the day-30 share still at older versions (medians 33.9 and 73.1 per cent in its two groups).
- From `studies/LH008/data/lags.csv`, the share of pinned repository pairs on the four fixes that had moved within 7 and within 30 days of the release.

The statements the record may make are of the form "on day N the Censys patched share in branch B was X, where the Python fix's at-or-newer download share was Y", each with its unit and its biases beside it. It may say that one curve is higher or rises faster as a description. It may not call one ecosystem faster or safer, attribute a difference to publicity, severity, AI or any cause, or turn a Censys count into a number of machines, sites or organisations.

## Units, and why the comparison is still worth making

A Python share counts fetches in a day, a flow weighted towards environments that fetch often. A Censys share counts services standing on the internet as last seen, a stock that changes only when a service is rescanned and on the version it reports. W3Techs counts websites crawled over a month. LH008 counts repositories. Each sees a different part of the same road: a release reaching where software is fetched, written down and finally run. The PHP event gives Lighthouse its first look at the far end, running services seen from outside, through someone else's instrument; the Python work saw only the near end. Setting them side by side says how much of the "days for most" and "weeks for pins" picture survives at the far end, and what the far end adds: branches no fix reaches.

## Overlap

The Python figures are LH008's and LH011's retained data, already published; nothing in them is new, and the comparison is disclosed as reuse. LH019 and LH025 read image tags for the same event; no image is counted here. LH030 to LH032 follow notices, records and vendor statuses and are not counted again.

## Stopping and what would leave it inconclusive

Stop after the read holding day 30, at the latest on 30 November 2026. An interim checkpoint after the read of 29 October (day 7 complete) may report measures 1 and 2 to day 7, labelled interim. Measure 1 is inconclusive for a branch if Censys's series stops, is truncated, or is revised by more than five points on any day without a read of ours holding the earlier value; if Censys withdraws the dashboard, the study reports what its reads held and says when it stopped. Measures 3 to 5 are descriptive and stand alone. CVE-2026-115560 is outside this study: no tracker found counts it, and its fixed versions are not yet released. Model spend goes in the close-out.
