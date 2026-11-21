# R-0105: fresh evidence review of the LH038 record, version 0.4

**In short.** We checked version 0.4 of the disclosure-timeline record, which applies the rule fixed on 20 November to today's read of SUSE's public announcement list, against the retained list messages, archive indexes, OSV records, SUSE advisory pages and SUSE's CVE page. Every date, count and per-advisory classing in 0.4 is right, the rule was applied as written, with no clock chosen by its distance from Anthropic's post, and the time zones are handled correctly. Four small wording changes keep the record from implying more than the list shows about what was public on 24 October; nothing must be fixed beyond them. The reader-and-inference review and a fresh recheck come next.

- **Reviewer:** fresh evidence-review subagent in Claude Code (Claude Opus 5.5, model id claude-opus-5-5), row LH038-v04-evidence-review of run 2026-11-21T151100Z-anthropic-research; note written at about 15:25 UTC on 21 November 2026 (`date -u` read 15:23:05 UTC just before). I wrote and reviewed nothing in this study before this round. A second agent's agreement is a review contribution, not independent confirmation.
- **Model disclosure.** The study concerns Anthropic's post and I run on an Anthropic model. I looked for wording easier or harder on Anthropic than the dates allow (check 8).
- **Version reviewed:** studies/LH038/LH038.md 0.4 at commit 0f26543, compared with 0.3 at cf45810 (`git diff cf45810 -- studies/LH038/LH038.md`), with the brief's amendment of 20 November (committed in 38a024a, 20 November 12:39 UTC, before the read committed in 2174b14, 21 November 14:22 UTC), the checkpoint checkpoints/2026-11-21-suse-clocks.md, and R-0091, R-0092 and R-0094 for what earlier rounds settled.
- **Nothing fetched.** Retained bodies only; Python run with `-I`; nothing committed. No new network read is needed.
- **Spend:** not available from inside this subagent; unknown, not zero.

## What I checked

1. **Replay.** `python3 -I studies/LH038/scripts/timeline.py` reproduces scripts/timeline_output.txt byte for byte. The version 0.4 section of the script reads the Release Date from the 17 November pages, the CVE-page stamp from LH036's suse.raw.gz (CET to UTC by a fixed offset table), and the archive date from each message; the post's date is not used in the classing (diff 58c3925..0f26543 read in full).
2. **Primary bodies, read directly.** For each of the twelve advisories: the archive page's one `<I>` date (all printed as UTC by pipermail); the Release Date in the message and on the 17 November advisory page (identical for all twelve); CVE-2026-98432 in the message's Cross-References list (all twelve); the CVE-page line (e.g. "SUSE-SU-2026:24386-1, published Thu Oct 29 13:04:53 CET 2026"); OSV's `published`, `modified` and `affected[].database_specific.source` (all `https://ftp.suse.com/pub/projects/security/osv/<id>.json`; nothing in the records says a date is OSV's own). Month indexes: October 771 messages, 1 October 12:31 to 30 October 16:31 UTC; November 581, 2 November 08:30 to 20 November 20:33 UTC; each identifier in exactly one subject. readlog.csv: 28 content GETs, all 200, request starts 14:20:14 to 14:21:14 UTC; the two robots.txt GETs that make 30 are counted by the script, not logged with bodies, so the total of 30 rests on the script's count.
3. **Time zones.** European summer time ended on 25 October 2026, so CET (UTC+1) is right for 29 October and 3 November, and the page itself says CET. No stamp falls between 00:00 and 01:00 CET, so the CET and UTC days agree (Method c holds). As an extra check I did not need the rule for: each message's Message-ID begins with a centisecond Unix timestamp that equals the archive date to the second for all twelve, so the archive's UTC dates are the messages' own sending times, not a later import.
4. **The decision rule as written.** Per advisory, list day beside Release Date day and CVE-page day; same day as exactly one clock in all twelve, the CVE-page stamp; counted per group, 4 of 4 and 8 of 8, no mixed group; OSV recorded and not used; the CVE recorded as listed. No clock was chosen, and no comparison made, by distance from 27 October: the post enters only the elapsed-day lines afterwards. Method's readings (a) to (e) are faithful to the amendment; (a) holds, since each archive page's Last-Modified is 19 to 53 seconds after its archive date.
5. **Figures in the text.** 29 October 08:36:14 to 16:42:30 UTC and 3 November 16:42:05 to 16:44:08 UTC; 2 days after the post; 18 and 14 days after the first and last stable releases; +45 13 December and +90 27 January 2027; stamp minus list 3.32 to 3.48 hours, list first in 12 of 12; Release-to-stamp gap about five days (5.06 to 5.39) and about a day and a half (1.46); 186 SUSE-SU announcements on the CVE page, none stamped before 29 October, so 174 not followed. All reproduced (code below).
6. **Header, Corrections, Limits, Next.** Version, date, figures commit, observation period, instruments and cites match the files. The Corrections entry says what changed, why, that conclusions changed in one place, and where 0.3 is (cf45810 is the last commit to touch the file before 0.4 and holds version 0.3). The amendment is labelled post hoc by construction in the header and Limits.
7. **Absolutes in the title, In short and Answer.** The title is a question. "All twelve", "every message" and "none of the followed SUSE advisories" are scoped to the twelve followed advisories and the list. One sentence (see S1) let "announced in public" stand as if it settled whether anything was public before the post.
8. **Easier or harder on Anthropic.** 0.4 is no longer easier on Anthropic, as 0.2 was: it does not revive the "3 days after SUSE's release" line. The risk now runs the other way. The list and the CVE page are two SUSE channels dated 29 October, and the advisory pages and SUSE's own OSV feed are two SUSE sources dated 24 October; the rule picks the list as the mark of public announcement, which is what the amendment asked, but the record's "none was announced in public before the post" could be read as "nothing was public before the post", which no source read shows. The changes below keep both sides as the dates allow.
9. **Unknowns stay unknown.** Report date, committer dates, Debian's and Ubuntu's dates, and what the Release Date marks remain unknown; a missing message would have been "no message found". One sentence in Finding 4 said "nothing public dated that day was read", which is not right: the advisory pages and OSV records carry that date, they were just read weeks later (S2).

## Findings

**Must fix:** none outstanding.

**Should fix (applied by me, listed under Changes):**

- **S1. "Announced in public" without its limit.** The Answer's paragraph under the table and the In short could be read as saying nothing was public before the post. The list shows when SUSE posted each announcement there; whether the advisory pages were reachable on 24 October isn't shown. Harder on Anthropic than the dates allow if left bare. Fixed with a short clause in each place; Finding 4 already carried the limit.
- **S2. "Nothing public dated that day was read"** (Finding 4) was wrong as worded; reworded to say the pages and OSV records carrying 24 October were read weeks later and nothing read records what was public on the day.
- **S3. "190 announcements"** (Answer, T5) sat beside "186 SUSE announcements" in Next. The 190 items include 3 Liberty posts of Red Hat errata and 1 technical document (R-0094); now "190 items ... (186 of them SUSE-SU announcements)".

**Advisory (not changed; for the reader review or the driver):**

- **A1. The list posts this series in batches** (my observation, made after the outcomes were seen, post hoc; one look, not a test). In the October date index the 24xxx-numbered advisories run in descending-number batches: 24435 down to 24386 (about 50 messages, 08:36 to 08:46 UTC on 29 October for the two followed ones in it) and 24458 down to 24436 in the afternoon; in November 24504 down to 24478 together on 3 November. The list date may therefore reflect when a batch was mailed. That does not change the rule's result, but it fits the record's caution that what the Release Date marks isn't stated, and the reader review may want the record to say the list is one SUSE channel among several. No brief tests this; the revision after LH036 stops could read Release Dates of unfollowed batch members within its ceiling if it chose.
- **A2.** The Message-ID corroboration in check 3 could be added to Method (a) as a line, labelled as a reviewer's post hoc check.
- **A3.** The status and Next lines still say the reviews of 0.4 are to come; the driver updates them when it records this review.

## Changes made to studies/LH038/LH038.md (within version 0.4; no figures changed)

1. In short: "The 24 October release date stays on the pages, what it marks isn't stated, and no date here says..." became "The 24 October release date stays on the pages; what it marks isn't stated, whether the pages were public that day isn't shown, and no date here says..." (S1).
2. Answer, T5: "none of the 190 announcements it lists" became "none of the 190 items it lists (186 of them SUSE-SU announcements)" (S3).
3. Answer, under the table: "...none of the followed SUSE advisories was announced in public before the post." gained "(whether their advisory pages were public before it isn't shown)" (S1).
4. Finding 4: "...isn't shown, since nothing public dated that day was read." became "...isn't shown: the advisory pages and OSV records that carry that date were read weeks later, and nothing read records what was public on the day." (S2).

These are the round's own changes to public-facing wording of a record; the fresh recheck already scheduled (row for the 0.4 recheck) reads them once.

## Calculation (code and output)

Kept as studies/LH038/review/r0105_check.py with its output studies/LH038/review/r0105_check_output.txt. Replay from the repository root: `python3 -I studies/LH038/review/r0105_check.py`. It parses the bodies with its own expressions, independently of scripts/timeline.py, asserts the Release Date on each 17 November page equals the one in the message, converts CET stamps by UTC+1 after checking the zone label, classes each advisory by the amendment's rule without reference to the post, and prints the elapsed days and the index order used in A1.

Output (identifiers shortened in the last two lines; full in the kept file):

```
10 messages: 771 LI: 771 start/end: ['Thu Oct  1 12:31:02 UTC 2026', 'Fri Oct 30 16:31:04 UTC 2026', ...]
11 messages: 581 LI: 581 start/end: ['Mon Nov  2 08:30:35 UTC 2026', 'Fri Nov 20 20:33:26 UTC 2026', ...]
CVE page announcements: 186 earliest stamp date (local): 2026-10-29
SUSE-SU-2026:24386-1 idx_hits=1 list=2026-10-29 08:45:55Z msgid=2026-10-29 08:45:55Z RD(msg)=2026-10-24T11:15:59Z RD(page17Nov)=2026-10-24T11:15:59Z listed=True stampUTC=2026-10-29 12:04:53Z stampCETday=2026-10-29 OSVpub=2026-10-24T10:42:33Z -> CVE-page stamp; list-post=2d RD-post=-3d stamp-list=3.32h
SUSE-SU-2026:24422-1 idx_hits=1 list=2026-10-29 08:36:14Z msgid=2026-10-29 08:36:14Z RD(msg)=2026-10-24T10:42:33Z RD(page17Nov)=2026-10-24T10:42:33Z listed=True stampUTC=2026-10-29 12:04:53Z stampCETday=2026-10-29 OSVpub=2026-10-24T11:28:39Z -> CVE-page stamp; list-post=2d RD-post=-3d stamp-list=3.48h
SUSE-SU-2026:24437-1 idx_hits=1 list=2026-10-29 16:42:30Z msgid=2026-10-29 16:42:30Z RD(msg)=2026-10-24T11:15:59Z RD(page17Nov)=2026-10-24T11:15:59Z listed=True stampUTC=2026-10-29 20:05:46Z stampCETday=2026-10-29 OSVpub=2026-10-24T11:15:59Z -> CVE-page stamp; list-post=2d RD-post=-3d stamp-list=3.39h
SUSE-SU-2026:24446-1 idx_hits=1 list=2026-10-29 16:38:06Z msgid=2026-10-29 16:38:06Z RD(msg)=2026-10-24T10:42:33Z RD(page17Nov)=2026-10-24T10:42:33Z listed=True stampUTC=2026-10-29 20:05:43Z stampCETday=2026-10-29 OSVpub=2026-10-24T11:28:39Z -> CVE-page stamp; list-post=2d RD-post=-3d stamp-list=3.46h
SUSE-SU-2026:24479-1 idx_hits=1 list=2026-11-03 16:44:08Z msgid=2026-11-03 16:44:08Z RD(msg)=2026-11-02T08:57:18Z RD(page17Nov)=2026-11-02T08:57:18Z listed=True stampUTC=2026-11-03 20:05:00Z stampCETday=2026-11-03 OSVpub=2026-11-02T08:57:05Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.35h
SUSE-SU-2026:24480-1 idx_hits=1 list=2026-11-03 16:43:49Z msgid=2026-11-03 16:43:49Z RD(msg)=2026-11-02T08:57:53Z RD(page17Nov)=2026-11-02T08:57:53Z listed=True stampUTC=2026-11-03 20:04:57Z stampCETday=2026-11-03 OSVpub=2026-11-02T08:57:53Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.35h
SUSE-SU-2026:24481-1 idx_hits=1 list=2026-11-03 16:43:32Z msgid=2026-11-03 16:43:32Z RD(msg)=2026-11-02T08:58:28Z RD(page17Nov)=2026-11-02T08:58:28Z listed=True stampUTC=2026-11-03 20:04:59Z stampCETday=2026-11-03 OSVpub=2026-11-02T08:58:28Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.36h
SUSE-SU-2026:24482-1 idx_hits=1 list=2026-11-03 16:43:16Z msgid=2026-11-03 16:43:16Z RD(msg)=2026-11-02T08:58:28Z RD(page17Nov)=2026-11-02T08:58:28Z listed=True stampUTC=2026-11-03 20:05:03Z stampCETday=2026-11-03 OSVpub=2026-11-02T08:58:28Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.36h
SUSE-SU-2026:24483-1 idx_hits=1 list=2026-11-03 16:42:59Z msgid=2026-11-03 16:42:59Z RD(msg)=2026-11-02T08:58:28Z RD(page17Nov)=2026-11-02T08:58:28Z listed=True stampUTC=2026-11-03 20:05:05Z stampCETday=2026-11-03 OSVpub=2026-11-02T08:58:28Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.37h
SUSE-SU-2026:24484-1 idx_hits=1 list=2026-11-03 16:42:42Z msgid=2026-11-03 16:42:42Z RD(msg)=2026-11-02T08:58:28Z RD(page17Nov)=2026-11-02T08:58:28Z listed=True stampUTC=2026-11-03 20:04:58Z stampCETday=2026-11-03 OSVpub=2026-11-02T08:58:28Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.37h
SUSE-SU-2026:24485-1 idx_hits=1 list=2026-11-03 16:42:23Z msgid=2026-11-03 16:42:23Z RD(msg)=2026-11-02T09:02:26Z RD(page17Nov)=2026-11-02T09:02:26Z listed=True stampUTC=2026-11-03 20:05:01Z stampCETday=2026-11-03 OSVpub=2026-11-02T09:02:27Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.38h
SUSE-SU-2026:24486-1 idx_hits=1 list=2026-11-03 16:42:05Z msgid=2026-11-03 16:42:05Z RD(msg)=2026-11-02T09:02:26Z RD(page17Nov)=2026-11-02T09:02:26Z listed=True stampUTC=2026-11-03 20:04:58Z stampCETday=2026-11-03 OSVpub=2026-11-02T09:02:27Z -> CVE-page stamp; list-post=7d RD-post=6d stamp-list=3.38h
24 Oct group: Counter({'CVE-page stamp': 4})  2 Nov group: Counter({'CVE-page stamp': 8})
earliest list message: 2026-10-29 08:36:14+00:00 days after post: 2
first stable -> earliest list day: 18  last stable -> 14
post +45/+90 from 29 Oct: 2026-12-13 2027-01-27
stamp-list hours min/max: 3.32 3.48
OSV source hosts: ['https://ftp.suse.com']
index 10, messages 30163-30240: 24368 24367 24366 24365 4918 ... 4923 24435 24434 ... 24387 24386 4926 24458 24457 ... 24437 24436 4935
index 11, messages 30340-30366: 24504 24503 ... 24487 24486 24485 24484 24483 24482 24481 24480 24479 24478
```

("RD-post" is the Release Date's day minus the post's day; "list-post" the list day minus the post's day.)

## Verdict

Cleared at version 0.4 (with the four wording changes above, which change no figure or classing).
