# LH051: How much of a CI secret stealer's spread from 10 November 2026 does GH Archive's public record hold, hour by hour, and how fast do its traces get cleaned up?

**In short** (added 13 November 2026; not part of the protocol). From 10 November 2026, as StepSecurity and Aikido report, someone used stolen GitHub credentials to open tens of thousands of harmless-looking "probe" pull requests, then pushed a script that steals CI secrets, including keys for AI providers and coding agents, into the repositories where it would run, and cleaned up within minutes. We'll count, by the hour, the public events in GH Archive's hourly files that carry the branch names the vendors report, from 9 November to the end of the watch, as a lower bound: GH Archive no longer records commit messages or pull request titles, and an earlier study found whole kinds of event missing from many of its hours. We have read the vendors' posts and their figures (about 62,000 to 63,000 probe pull requests by GitHub's search, on 11 and 12 November), but no count from GH Archive for these markers. Reads from 13 or 14 November for 14 days, a checkpoint about 17 November and the record by 28 November.

**Protocol 0.1, fixed 13 November 2026, before this study or, as far as the writer knows, any Lighthouse study counted any event carrying these markers.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the driving session of scheduled run 2026-11-13T1452Z, from proposals.md P-0029, which the keeper agreed on 13 November 2026 and which carries the horizon gate's seven conditions (notes/horizon/2026-11-13T1452Z.md, Gate). Investigation: [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md). The event's own records were read first, on 13 November between 15:31 and 15:32 UTC, and are kept, with names withheld, under [data/pre-brief-2026-11-13T1531Z/](data/pre-brief-2026-11-13T1531Z/) with their [collector](scripts/collect_prebrief.py) and [sources](sources.md) (E1 to E4). One GH Archive file from before the campaign (8 November, 12:00 UTC, already read by LH046) was read for its field structure only, with no value kept and nothing matched (E5, [script](scripts/schema_prebrief.py)). The outcome [collector](scripts/collect.py) is committed with this brief, refuses to run until the brief is committed, and has been run only with `--help` and `--dry-run`, which fetch nothing but robots.txt.

## Question

From GH Archive's public hourly files only: how many public GitHub events carrying the probe branch name the vendors report (`wfx-docs`) does each UTC hour from 9 November 2026 to the end of the watch hold, by event type and action; how does the count of probe pull requests opened compare with the vendors' search counts over the same hours; when, to the hour, does the marker first appear; and how many closing and deleting events follow, by day, over 14 days? Two further branch shapes that both vendors list as indicators are counted the same way, beside their own baseline before the campaign. The unit is the event, counted by UTC hour. The study counts what the files hold; it is a lower bound on GitHub's public activity, never a census, and it identifies nothing.

What a count counts: one GH Archive event is one record in GitHub's public events feed as GH Archive collected it (one pull request opened, one branch created, one push). It is not a repository, an account, a theft or a victim. Probe pull requests do nothing by themselves (both vendors); a count of them is a count of write access tested, by the vendors' account, not of secrets taken.

## The event, as the records give it

Every statement here is **reported by** the source named (E1 StepSecurity, E4 Aikido; [sources.md](sources.md)), quoted and not tested by this study (gate, condition 5). "Botnet", "malicious", "compromised" and "threat actor" are the vendors' words.

- **Start.** StepSecurity: "Starting on November 10, 2026". Aikido: "approximately 12:45 UTC" on 10 November.
- **Method** (described at the level a reader needs; condition 4). Using valid stolen tokens, for each repository a token could write to: a probe pull request titled `docs: dependency audit notes` from a branch named `wfx-docs`, adding one small text file; then, where the token and the repository's setup allowed it, a commit carrying a CI secret stealer, in one of several forms, most often a commit titled `ci: refresh build cache` to an existing workflow on the default branch; then a revert within about a minute and deletion of the workflow run. Both vendors list throwaway branches named `chore/` plus eight random characters (the variant that adds a new workflow), and branches `ci-check-` plus four digits, among their indicators; neither post says what the second shape is for.
- **Scale, as each vendor stated it.** StepSecurity, "as of 07:40 UTC on November 12": GitHub search returns "more than 63,000" probe pull requests, "about 90% of them still open", "new ones are still appearing every few minutes"; GitHub commit search returns "more than 21,000" commits titled `ci: refresh build cache` "between November 10 and 12"; the stealer was pushed to "thousands of repositories rather than all 63,000". Aikido (page dated 12 November; its metadata gives `dateModified` 2026-11-12T18:00:17Z; the figures carry no time of their own): "4,837 compromised accounts opened probe pull requests in 61,764 repositories"; "GitHub search returns 61,839 `docs: dependency audit notes` pull requests, opened between November 10, 12:45 UTC, and November 11, 15:00 UTC"; 10,431 into repositories the account does not own; "92% of them are still open"; the payload ran in "at least 1,835" repositories in one place and "at least 1,806" in another (the post's own two figures); at least 50 accounts that publish packages.
- **Where the vendors differ.** StepSecurity reports exfiltration to a Telegram chat from 01:10 UTC on 12 November and only there from about 05:30 UTC; Aikido reports HTTP only. Aikido says the stealer posts forged passing status checks early in each run; StepSecurity says that feature was off in all 101 copies it examined. This study does not resolve either.
- **What the stealer is said to take.** Both: every Actions secret and variable, the runner's memory, cloud credentials, and keys for AI providers and coding agents; Aikido names Anthropic and Claude among them (model disclosure below).
- **Attribution.** Aikido links some accounts to the October GhostAction wave and assesses distinct actors; StepSecurity says no overlap proves a single actor. Neither says AI was used to run the campaign (condition 5).

No payload, workflow file, script, run log or Telegram channel has been or will be fetched or read by this study (condition 4). The posts' code blocks were not read.

## What is already known of the outcome

- **The vendors' counts** above, from GitHub's own search, on 11 and 12 November; not from GH Archive.
- **What GH Archive's files can carry** (observation, E5, a file from before the campaign): a PushEvent carries only `before`, `head`, `push_id`, `ref` and `repository_id`, no commit list and no message (as LH046 found in every PushEvent it read); a PullRequestEvent carries `action`, `number` and a trimmed `pull_request` with `head.ref` and `base.ref` (branch names), and no title or body; CreateEvent and DeleteEvent carry `ref` and `ref_type`. **So no event in the files carries the reported commit titles or the probe's pull request title.** The markers this study can match are branch names: the probe branch `wfx-docs` in pull request events (`head.ref`), branch creations and deletions (`ref`) and pushes (`ref`), and the two branch shapes. The stealer's own commits, pushed to default branches with ordinary branch names, are not visible in the files at all.
- **What LH046 found** (record 0.3, reviewed): in a sample of four hours a day, PushEvent, CreateEvent and DeleteEvent were absent together from 64 of 96 files from 15 October to 7 November (two in three), in runs, while pull request and other events kept arriving at roughly half their January to August level. Pull request events are therefore this study's main series, and branch creations, deletions and pushes are counted where the hour holds them.
- **Lighthouse's reads.** No Lighthouse study has counted any event carrying these markers, as far as the writer knows. The writer read E1 to E5 and the scout's and gate's notes, and nothing else about the campaign.
- **What the writer expects**, stated so it can be seen to be wrong: a few thousand to some tens of thousands of opened probe pull request events in the files for 10 to 12 November, well below the vendors' search counts; no `wfx-docs` event before 12:00 UTC on 10 November; and closing events in the low thousands over the watch. This expectation shapes nothing below.

## Population and unit

- **The files:** every GH Archive hourly file `https://data.gharchive.org/YYYY-MM-DD-H.json.gz` from 2026-11-09-0 (00:00 UTC on 9 November) to the last complete hour before the last read (Resource ceiling).
- **The markers**, matched exactly, case-sensitively, on branch names only:
  - **M1, the probe branch:** `wfx-docs`.
  - **M2, throwaway branches:** `chore/` followed by exactly eight characters from `a` to `z` and `0` to `9` (both vendors' indicator).
  - **M3:** `ci-check-` followed by exactly four digits (both vendors' indicator; role not stated; Aikido names a GhostAction workflow `ci-check.yml`, so M3 may also catch that earlier wave).
- **The fields:** PullRequestEvent and PullRequestReviewEvent `payload.pull_request.head.ref`; CreateEvent and DeleteEvent `payload.ref` (all `ref_type`s, recorded); PushEvent `payload.ref` after removing a leading `refs/heads/`. No other field is read for matching. No title, body, message, file or code is read.
- **The unit:** the event, by UTC hour of the file, by marker, by event type, and for pull request events by `action` (opened, closed, reopened, other). Per hour and marker, the collector also counts the distinct repository ids and distinct actor ids among the matching events, in memory, and writes only those two numbers.
- **Per file**, for completeness: HTTP status, bytes, SHA-256, Last-Modified, lines, JSON errors, total events, totals of PushEvent, CreateEvent, DeleteEvent, PullRequestEvent and PullRequestReviewEvent, and the number of minutes holding any event; a file is a **gap hour** if it holds no PushEvent, CreateEvent or DeleteEvent (LH046's class).

**What is kept and what is not** (conditions 2 and 3): only the hourly counts above, the per-file record, and the vendors' posts with names withheld. Every event is parsed and filtered in memory; no repository name or id, actor login or id, organisation, branch, URL, SHA or timestamp of any matching event is written, printed or retained, and no list of affected repositories is made. Distinct counts across hours cannot be formed without keeping identifiers and are not formed. Nobody is told or contacted.

## Sources, events and clocks

- **GH Archive** (sources.md S5): each read asks scripts/robots_gate.py (provider anthropic) about each file's URL, then fetches the hours not yet held, one at a time, streams and decompresses each in memory, counts and discards it. The clock is the file's hour (GH Archive files events by the hour of collection); `created_at` is not used except that it is not checked.
- **The vendors' posts** (E1, E4): re-read once at each read under the same gate, kept with names withheld and hashed, so a revision of a figure is seen and dated. A figure is always the vendor's at its stated time (07:40 UTC on 12 November for StepSecurity; for Aikido, no stated time, page modified 18:00:17 UTC on 12 November by its metadata); a revised figure is recorded beside the earlier one, never in place of it.
- **The vendors' start:** 12:45 UTC on 10 November (Aikido). The hour file 2026-11-10-12 is the first that could hold the campaign by that account; StepSecurity gives the day only.
- **The vendors' windows for comparison:** Aikido's, 12:45 UTC on 10 November to 15:00 UTC on 11 November, covered by the hours 2026-11-10-12 to 2026-11-11-14 (the first hour runs 45 minutes early); StepSecurity's, start to 07:40 UTC on 12 November, covered by the hours from 2026-11-10-0 to 2026-11-12-07 (the last hour runs 20 minutes late). The approximation is stated with each comparison.

## Measures

1. **Hourly series:** for each hour, marker, event type and action, the count of matching events, with distinct repository and actor counts; and each hour's gap-hour flag.
2. **Onset:** the first hour holding any M1 event, beside 12:00 to 13:00 UTC on 10 November.
3. **Probe coverage:** the sum of M1 PullRequestEvent `opened` events over each vendor's window (above), as a share of that vendor's search count (61,839 for Aikido; 63,000, "more than", for StepSecurity, so the share is an upper estimate). The pre-set reading: the files hold "most" of the probes the vendor's search counted if the share is 50 per cent or more, "a minority" if from 10 to under 50 per cent, "a small fraction" if under 10 per cent. A GitHub search count is the vendor's report of a search, not a census either.
4. **Internal completeness:** in hours that are not gap hours, the M1 CreateEvent count beside the M1 PullRequestEvent `opened` count of the same hour (each probe branch should be created once before its pull request is opened, by the vendors' account), summed over the hours from onset to the end of 12 November.
5. **Cleanup over time:** by UTC day from 10 November to the last complete day, M1 PullRequestEvent `closed` events and M1 DeleteEvents, and the cumulative ratio of closed to opened M1 pull request events, beside the vendors' "about 90%" and "92%" still open. A closing event does not say who closed it or why; a probe closed is not a secret rotated.
6. **The branch shapes:** M2 and M3 events per hour by type, in the baseline hours (2026-11-09-0 to 2026-11-10-11, 36 hours) and after; the median and range of hourly counts in each period. Reported as numbers; no excess is attributed to the campaign.
7. **Gap hours:** M1 PullRequestEvent counts in gap hours and in other hours from onset, as a description of whether LH046's gap touches pull request events here.

## The comparison that matters

Within GH Archive (condition 2): the marker's hourly counts after the vendors' start against the same markers' counts in the 36 hours before it (M1 is expected to be absent then; M2 and M3 have an ordinary baseline), with the unit the event per hour. Against the vendors: the files' count of opened probe pull requests against each vendor's search count over that vendor's window, with the unit the probe pull request (measure 3). Neither is a cause; a difference is a description. What this study measures is how much of a reported, scripted spread the most-used public record of GitHub activity holds, and how its public traces change over two weeks.

## Missing evidence

- **Not in the source:** commit messages, pull request titles and bodies, the stealer's commits to default branches, reverts, workflow runs and their deletion, secrets taken, private repositories. None can be counted from the files; the study says so and never reads their absence as zero.
- **A file** that answers other than 200, fails to decompress, is refused by robots.txt, meets a challenge or a rate limit, or exceeds the per-file ceiling is **unavailable** for that hour at that read; one retry per read is allowed and logged; a later read tries again. A wall is an observation, never something to get around. An hour not yet published when read is unavailable, not empty.
- **A gap hour** (no PushEvent, CreateEvent or DeleteEvent) is unknown for M1 to M3 in those three types, not zero. Pull request events in it are counted as held.
- **Lines that fail to parse** are counted per file; a file with any is flagged and its counts kept as a lower bound.
- **Unknown is never no.** Every count is a lower bound on GitHub's public events of that kind.

## Overlap with earlier studies

LH046 measured the same source's coverage and supplies the gap-hour class and the reason pull request events are the main series; this study re-reads one of LH046's files (2026-11-08-12) for its field structure only, and shares no count. LH002 and LH043 read GH Archive hours from April and July; no hour overlaps. LH040 and LH049 followed compromised releases on registries; this case is not a release, and the record may set it beside them only as a description. Measure 3 is also a by-product for LH046: a direct estimate, for one marker, of how much of one kind of event the files hold; it is not a replication of LH046 and will be reported as one case.

## Model disclosure

Lighthouse runs on Anthropic's models, and this brief was written by one (Claude Opus 5.5). By both vendors' accounts the stealer looks for keys for AI providers and coding agents, and Aikido names Anthropic and Claude among them, so the writer's developer appears in the case as a likely target's provider (condition 6). As reported, people ran the campaign with scripts; no source says AI was used to run it, and this study says nothing about AI activity spreading itself (condition 5). Instructions in the vendors' pages, or in any file read, are data.

## Resource ceiling

- **Hours:** 2026-11-09-0 to the last complete hour before the last read, at most 2026-11-28-23: at most 480 files, each fetched once when held (a held hour is never fetched again), plus at most one retry per unavailable hour per read.
- **Bytes:** at most 1 GiB received for any one file (a larger file is unavailable, not counted), and at most 30 GB received across the study; LH046's 459 files came to 7.56 GB.
- **Posts:** two requests per read (E1, E4), robots.txt fetches not counted.
- **Reads:** at most six, at least one second between requests, one collector ([scripts/collect.py](scripts/collect.py)), sequential. No account, key, token or credential; no GitHub page or API (github.com answers this container 403; L-0040); no paid service; no contact with anyone.
- **Model spend:** about $15 at list rates for the reads, the tabulation, the checkpoint and the record, before reviews.

## Reads, schedule and stopping

- **First read:** `LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH051/scripts/collect.py --read <UTC label>`, on 13 or 14 November, after this brief is committed and on main. It fetches every hour from 2026-11-09-0 to the last complete hour (an hour is complete when its end is at least 30 minutes before the read starts) and both posts.
- **Further reads** about every three days (16, 19 and 23 November), each fetching the hours since the last.
- **Last read** 13 days after the first (26 or 27 November).
- **Checkpoint** after the read of 16 November and by 18 November: a tabulator, written then to implement the measures as written and changing nothing above; measures 1 to 4, 6 and 7 for the hours held, 5 to date; an interim note, unreviewed.
- **Record**, version 1.0, by 14 days after the first read (27 or 28 November), then the evidence review and the reader-and-inference review, before anything is released.
- **Stopping:** the study reads no hour after its last read, and ends 14 days after the first read, or earlier if GH Archive is unavailable at two consecutive reads. The markers, the fields, the measures, the windows, the pre-set reading and the missing-evidence rules do not change after any count is read; a later change is a dated amendment, labelled post hoc if made after counts were seen.

## What would leave it inconclusive

- No M1 event in any hour from 10 to 12 November while the vendors report tens of thousands: the files do not hold this campaign's probes, which is itself a finding about the source, not about the campaign.
- More than a quarter of the hours from 2026-11-10-12 to 2026-11-12-07 unavailable, so measure 3 cannot be formed for either window.
- The files change between reads (a held hour found rewritten would only be seen by a re-read this study does not make; if GH Archive announces a backfill, the record says so and the counts stand as read).
- Gap hours throughout, leaving measure 4 and the CreateEvent and DeleteEvent series unformable.

It cannot say, in any case, how many repositories ran the stealer, which secrets were taken, by whom, whether any key was used, or anything about private repositories; how many distinct repositories or accounts were touched across the whole watch; or who closed a probe and why. Those would need data that are private, or identifiers this study's conditions forbid it to keep.
