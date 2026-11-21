# LH038 checkpoint, 21 November 2026: the SUSE clocks read

**In short.** SUSE keeps two dates for the twelve kernel advisories this study follows: a Release Date on each advisory page (24 October or 2 November) and a later stamp on its CVE page (29 October or 3 November). Today's one read of SUSE's public security-announcement list found exactly one message for each advisory, and every one was posted on the same UTC day as the CVE-page stamp, not the Release Date. By the rule fixed before the read, the list supports the CVE-page clock for all twelve. Working record, unreviewed; what this means for the record goes into its version 0.4 and its reviews.

Read under the brief's amendment of 20 November (rows LH038-suse-read; result to LH038-v04). Written by the Watch run of 21 November (driver; Claude Code on Anthropic's models), which also made the read itself, with no collection subagent. Lighthouse runs on Anthropic's models, and the post this timeline is set against is Anthropic's (the brief's model disclosure).

## What was read

All GETs between 14:20:14 and 14:21:14 UTC (request starts) on 21 November 2026, each asked of scripts/robots_gate.py (provider anthropic) immediately before the fetch, User-Agent Lighthouse-research, through [scripts/suse_clocks.py](../scripts/suse_clocks.py). Bodies are kept gzipped, emails withheld, in `data/suse-clocks-2026-11-21T1420Z/`, with `readlog.csv` (URL, UTC start, status, Last-Modified, Date, length, SHA-256 of the bytes received). Every request answered HTTP 200; no wall was met and nothing was retried.

- **The list index.** `https://lists.suse.com/` answered with a 66-byte page that only redirects, by a meta refresh, to `/mailman/listinfo`; that page, the host's list of public lists, was then read as the list index. This is one GET more than the amendment's plan of 29, and brings the read to its ceiling of 30 exactly (28 content GETs and two robots.txt files, one per host). The list carrying SUSE-SU security announcements, by the index's name and description: **sle-security-updates**, "Security Update Advisories for SUSE Linux Enterprise".
- **The month indexes** (pipermail, by date): October 2026, 771 messages, 1 to 30 October (`Last-Modified` 30 October 16:31 GMT); November 2026, 581 messages, 2 to 20 November (`Last-Modified` 20 November 20:33 GMT). Each of the twelve advisory identifiers appears in exactly one subject line across the two, so no message had to be chosen between several and none was left unfetched.
- **Twelve messages,** one per advisory, and **twelve OSV records** (`api.osv.dev/v1/vulns/<identifier>`), one GET each.

A small fix after the read: the helper's GET counter printed one less than the true count (it left out the GET being made). The read stayed within 30 by the true count; the counter was corrected for any later use.

## What each date says (observation)

From [scripts/suse_clocks_tabulate.py](../scripts/suse_clocks_tabulate.py), output kept as `data/suse-clocks-2026-11-21T1420Z/tabulation.txt`:

| Advisory | List message (archive date, UTC) | Release Date in the message | CVE-2026-98432 in the message | OSV published | List day matches |
| --- | --- | --- | --- | --- | --- |
| SUSE-SU-2026:24386-1 | 29 Oct 08:45:55 | 2026-10-24T11:15:59Z | appears | 2026-10-24T10:42:33Z | CVE-page stamp |
| SUSE-SU-2026:24422-1 | 29 Oct 08:36:14 | 2026-10-24T10:42:33Z | appears | 2026-10-24T11:28:39Z | CVE-page stamp |
| SUSE-SU-2026:24437-1 | 29 Oct 16:42:30 | 2026-10-24T11:15:59Z | appears | 2026-10-24T11:15:59Z | CVE-page stamp |
| SUSE-SU-2026:24446-1 | 29 Oct 16:38:06 | 2026-10-24T10:42:33Z | appears | 2026-10-24T11:28:39Z | CVE-page stamp |
| SUSE-SU-2026:24479-1 | 3 Nov 16:44:08 | 2026-11-02T08:57:18Z | appears | 2026-11-02T08:57:05Z | CVE-page stamp |
| SUSE-SU-2026:24480-1 | 3 Nov 16:43:49 | 2026-11-02T08:57:53Z | appears | 2026-11-02T08:57:53Z | CVE-page stamp |
| SUSE-SU-2026:24481-1 | 3 Nov 16:43:32 | 2026-11-02T08:58:28Z | appears | 2026-11-02T08:58:28Z | CVE-page stamp |
| SUSE-SU-2026:24482-1 | 3 Nov 16:43:16 | 2026-11-02T08:58:28Z | appears | 2026-11-02T08:58:28Z | CVE-page stamp |
| SUSE-SU-2026:24483-1 | 3 Nov 16:42:59 | 2026-11-02T08:58:28Z | appears | 2026-11-02T08:58:28Z | CVE-page stamp |
| SUSE-SU-2026:24484-1 | 3 Nov 16:42:42 | 2026-11-02T08:58:28Z | appears | 2026-11-02T08:58:28Z | CVE-page stamp |
| SUSE-SU-2026:24485-1 | 3 Nov 16:42:23 | 2026-11-02T09:02:26Z | appears | 2026-11-02T09:02:27Z | CVE-page stamp |
| SUSE-SU-2026:24486-1 | 3 Nov 16:42:05 | 2026-11-02T09:02:26Z | appears | 2026-11-02T09:02:27Z | CVE-page stamp |

Each message shows one date in the archive, so every message is classed. The messages carry the same Release Dates as the advisory pages read on 17 November. OSV's `modified` falls on 30 October or 1 November for the four of 24 October and on 4 November for the eight of 2 November (in the tabulation). OSV's `published` falls on the Release Date's day for all twelve, at the same second for six, within 13 seconds for three more, and 33 to 46 minutes apart for the other three; by the amendment it is SUSE's data relayed by OSV, not a third side, and is not used to choose a clock. "Appears" means the identifier is in the message's text; how the message lists it was not classified further.

## By the decision rule (derived)

For each advisory the list message's UTC day is the CVE-page stamp's day (29 October for the four of 24 October, 3 November for the eight of 2 November) and not the Release Date's. **The list supports the CVE-page clock for all twelve: 4 of 4 in the 24 October group, 8 of 8 in the 2 November group.** No group is mixed. Within the day, the four October messages were posted at 08:36 to 16:42 UTC; the CVE-page stamps the amendment lists for them are 12:04:53 (two) and about 20:05 (two), so on the same day but not at the same minute. The rule compares days only.

What this does not say (from the amendment, unchanged): none of these dates says when fixed packages reached anyone, whether anyone kept to a policy, or anything about the report date, which stays unknown. No clock was chosen by its distance from the post of 27 October.

## Handover

Flagged for Research: this result can change how the record reads. Record 0.3 keeps both clocks and says which, if either, marks public release is unknown; this read gives that question an answer by the amendment's rule. It goes into LH038 version 0.4 (row LH038-v04, by 9 December) with its Corrections entry and its evidence review, reader-and-inference review and fresh recheck before any public surface changes (row LH038-v04-surfaces). Nothing public was edited here.
