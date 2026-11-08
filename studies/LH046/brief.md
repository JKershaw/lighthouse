# LH046: How complete have GH Archive's hourly files been since September 2026?

**In short** (added 8 November 2026; not part of the protocol). GH Archive keeps one file of public GitHub activity for every hour, and several of our studies and pieces lean on it. A quick scan by one of our reviewers, made today, suggests that since 15 October many of those files hold no pushes or new branches at all, while pull requests, issues and comments keep arriving. That is a lead, not a finding. We'll read about 450 hourly files from 1 September to 8 November 2026, count what each holds and when within the hour, and say which hours look whole, which look partial and which kinds of event are missing, without guessing why unless a source says.

**Protocol 0.1, fixed 8 November 2026 at about 19:45 UTC, before any GH Archive file was read for this study.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the driving session. Kind: repair of an instrument (map row I28 in studies/LH035/LH035.md; sources.md S5). Related: proposals.md P-0006 (completeness for a small cohort, issue #5), which this study does not answer: it measures the whole feed hour by hour, not a cohort's events against its git history.

## Question

In GH Archive's hourly files (https://data.gharchive.org/YYYY-MM-DD-H.json.gz) from 1 September to 8 November 2026: which files are missing or empty; which hold events of only some types where earlier files held all; which hold events from only part of their hour; and do these begin on a date, at an hour of day, or for particular event types?

The unit is the hourly file. Everything counted is what the file held when read (observation). Rates, baselines and classifications are derived. Why any file is short is interpretation, and stays unknown unless a source states it.

## What the writer already knows of the outcome

Disclosed in full, because it shaped this protocol:

- **The reviewer's scan** (essays/what-the-watch-would-see/reader-review/gharchive_scan.py and gharchive_scan_output.csv, read 8 November 2026 between about 19:27 and 19:30 UTC, after outcomes were seen, so a lead): the 12:00 UTC file of each day from 1 October to 7 November. 1 to 6 October held 77,699 to 92,611 events, 59,535 to 70,908 of them PushEvents and 9,464 to 12,483 CreateEvents. 7 October held 6,510 events and no PushEvent or CreateEvent; 8 to 10 October about 40,000 to 47,000 with pushes; 11 to 14 October 85,650 to 94,517. From 15 October to 7 November, 16 of 24 files held no PushEvent and no CreateEvent (2,598 to 6,171 events each); the other eight held 12,815 to 81,569 events with pushes. Its companion (gharchive_hour_output.txt) found in 2026-11-07-12 4,105 events, chiefly PullRequestEvent (1,439), IssueCommentEvent (753), IssuesEvent (700) and WatchEvent (364), and no DeleteEvent. The driver's task adds that one file, 2026-11-05 hour 3, "came back empty"; that file is not in the scan's output and the writer has not seen it.
- **LH002** (studies/LH002/data/gharchive_2026-04-02-14_summary.json): the file 2026-04-02-14 held 153,261 events in 35,617,941 compressed bytes, 111,213 PushEvents, 13,515 CreateEvents and 5,457 DeleteEvents; every PushEvent's payload held exactly `repository_id`, `push_id`, `ref`, `head`, `before`.
- **LH043**: the file 2026-07-01-12 was 21,587,792 bytes, sha256 1c74717a5441b202307aefb4c4ffc71f5bfd440509a062c7db387b4b427f03b1, and held no repository-creation event and no PushEvent commit list.
- **Sources read before this brief** (searchlog.md): GH Archive's page states no completeness and no gap notice; GitHub's docs still list PushEvent and CreateEvent and say the public events endpoint's latency "can be anywhere from 30s to 6h"; GitHub's changelog for September to November 2026 has no Events API entry; on 15 October 2026 GitHub retired email notifications for push events (a different feature; no link is stated or assumed); GitHub's status incidents of 31 August to 8 November name no Events API incident. GH Archive's issue tracker could not be read (HTTP 403 from this session's proxy).

So the writer expects the scan's pattern to recur across hours of the day, but does not know whether it does, whether September was whole, where within a day gaps start and stop, or whether the "other" types are themselves complete.

## Sample, fixed now

1. **Panel**: every day from 1 September to 7 November 2026 at hours 0, 6, 12 and 18 UTC: 68 days, 272 files.
2. **Whole days**: all 24 hours of 15 September, 1 October, 7 October and 14 October (before 15 October) and 15 October, 26 October, 5 November and 7 November (from 15 October): 192 files, 32 of them already in the panel. These days were chosen with the scan in view (7 October, 15 October, 26 October and 7 November are days it showed without pushes; 5 November holds the reported empty hour), so they describe the structure of gaps; they are not a random draw and no rate is computed over them.
3. **Reference hours**: hour 12 of the 1st and 15th of each month from January to August 2026 (16 files), and the two hours earlier records used: 2026-04-02-14 (LH002) and 2026-07-01-12 (LH043; the 1 July reference doubles as it).
4. **Latest**: 8 November 2026 hours 0, 6 and 12, if published when read; a file not yet published is recorded as such, not as missing.
5. **Re-read**: at the end of the run, six files read again to test whether files change after publication: 2026-10-01-12, 2026-10-15-12, 2026-10-26-12, 2026-11-05-3, 2026-11-07-12, 2026-11-07-18. Also compared with the reviewer's hash prefixes and sizes (essays/what-the-watch-would-see/reader-review/fetch-log.tsv) for the files both read, and with LH002's size and LH043's hash.

About 450 distinct files. Overlap: the scan's 38 files (hour 12, 1 October to 7 November) are all re-read in the panel, so the panel's hour 12 is not independent of the lead; hours 0, 6 and 18 and the September days are new.

## Measures, per file

From the response: HTTP status, compressed bytes, sha256, Last-Modified and ETag headers, UTC time read. From the contents (read as data, never kept): whether it decompresses and parses; lines; JSON errors; events; events by type (the 16 documented types and any other); uncompressed bytes by type; distinct repository ids; distinct actor ids (counted only, never kept); PushEvent payload keys and how many events carry each, and how many carry a non-empty `commits` list; CreateEvent `ref_type` counts; earliest and latest `created_at`; events whose `created_at` falls outside the file's hour; event id minimum and maximum; and, per minute of the hour by `created_at`, events in all, PushEvents and CreateEvents.

## Definitions

- **Baseline**: for each hour of day in the panel (0, 6, 12, 18) and each event type, the median count over the panel's 30 files at that hour from 1 to 30 September 2026. For a whole-day hour, the baseline is the median over 1 to 30 September of the nearest panel hour (hour 0 to 2 and 21 to 23 use 0; 3 to 8 use 6; 9 to 14 use 12; 15 to 20 use 18).
- **Missing file**: HTTP 404 after one retry. **Unread**: any other failure (403, 429, 5xx, timeout, broken transfer) after one retry; unread is never counted as missing.
- **Empty file**: HTTP 200 with zero parsed events (including a body that does not decompress, which is reported separately).
- **Type gap**: a file holding zero events of a type whose baseline median at that hour is at least 100. **Type shortfall**: above zero but under 25 per cent of that median.
- **Short hour**: total events under 50 per cent of the baseline median.
- **Partial hour (minute hole)**: a file with events in which some run of at least 5 consecutive minutes of its own hour has no event of any type, or whose events cover fewer than 55 of its 60 minutes. **Partial push hour**: a file with PushEvents in which a run of at least 5 consecutive minutes has none.
- Late events: events whose `created_at` falls before the file's hour are counted, not reassigned.

## The comparison that would matter

1. **Before and after 15 October, in the panel**: the share of files with a PushEvent gap (and, separately, a CreateEvent gap) from 1 September to 14 October against 15 October to 7 November, by hour of day and pooled, each with its count. Fixed reading: the scan's lead **holds** if the later share is at least 50 per cent and the earlier at most 10 per cent; it **does not hold** if the later share is at most 10 per cent; anything else is **mixed** and is described, not labelled.
2. **Whether the loss is type-specific**: on panel files from 15 October, the ratio of the control types (PullRequestEvent, IssuesEvent, IssueCommentEvent and WatchEvent, summed) to their baseline, in files with a PushEvent gap against files without. If the control types sit near baseline in gap files, the loss is specific to some types; if they fall too, the whole feed thinned. Either is described; neither names a cause.
3. **Where gaps begin and end**: in the whole days, whether gaps run hour by hour (whole files) or start and stop within an hour (minute profiles in the boundary hours).
4. **Payload shape over time**: PushEvent payload keys and CreateEvent `ref_type` across all files read, against LH002's April set.
5. **Stability**: whether re-read files and files other records read have the same size and hash.
6. **Before September**: whether any reference hour from January to August has a type gap or short hour against the September baseline (described; a different month is not a like baseline, so no rate).

## What this means for the studies and pieces that rely on GH Archive

Found with `grep -rli "gh archive\|gharchive"` across studies/, articles/, essays/ and investigations/ (harbour/.session/ excluded). Questions the record will answer, not conclusions:

- **LH002** (software updates; one hour, 2026-04-02-14): is the file still the size LH002 recorded, and does an April hour fall outside any gap pattern found?
- **LH043** (AI cost and spread; one hour, 2026-07-01-12, a format check): does the file still have the hash LH043 recorded, and was July's hour whole by these measures?
- **The map, articles/who-watches-the-internet.md, row I28** (released): the row calls GH Archive hourly; were the hourly files present, and whole, over the window?
- **articles/what-we-can-see.md** (released): it says GH Archive "records every public event on GitHub, hour by hour". Over the window, which event types did the files hold, and in what share of hours?
- **essays/what-the-watch-would-see.md** (draft): it says a push "lands in GH Archive's hourly file". In what share of sampled hours from 15 October did the file hold any push at all?
- **investigations/ai-cost-and-spread.md, question 4**, and any later use of GH Archive: which hours and types can a study rely on, and what check should precede a reading?
- **P-0006**: does this change what a cohort study of completeness would need?

## Resource ceiling and stopping

Stream and count: each file is read once into memory, counted and discarded; retained are the counts, sizes, hashes and headers (data/), not the files. Sequential requests with a pause of at least one second between them, a generic labelled User-Agent and no email address; robots.txt on data.gharchive.org sets no restriction (searchlog.md). At most 520 requests and 9 GB transferred; the run stops when either is reached. On HTTP 429 or 503, one retry after 60 seconds, then the file is recorded as unread; after 10 consecutive failures the run stops and the record says so. No figure is drawn from fewer than the files read; nothing is fetched twice except the six re-reads and single retries.

The study stops when the sample is read (or the ceiling is reached) and version 0.1 of the record is written. A re-check of whether the pattern persists, on hours not read here, is scheduled separately (for-driver.md).

## What would leave it inconclusive

- More than 10 per cent of the sample unread.
- A September baseline that itself has PushEvent gaps in more than 10 per cent of its files: then comparison 1 has no clean reference and is reported as description against the January to August references only.
- Files that change between reads in ways that alter counts: the record then describes the archive as of each read time and says the comparison is not stable.
- Any count above says what the files held, not what happened on GitHub: a file without pushes does not show that nobody pushed. Whether GitHub's public feed, GH Archive's collector or something else lost the events is outside these measures; only a statement by GH Archive or GitHub could settle it.
