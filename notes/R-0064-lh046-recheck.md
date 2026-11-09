# R-0064: recheck of the LH046 review resolution and its "Later evidence" notices

**In short.** Every figure, date, count and window in the two "Later evidence" notices, the two investigation-page lines and record 0.3's revised opening and Answer matches data/hours.csv when recomputed. Two kinds of wording went further than the evidence, and I fixed both in place. First, three passages said the January to August hours read were "all at noon UTC" or "all at 12:00 UTC", though LH002's April hour, read at 14:00, is among them (software-updates.md names it in the same sentence). Second, both investigation-page lines said "whether GitHub's public events feed or GH Archive's collection lost the events", which takes it as given that the events existed, where the notices make it conditional ("If GitHub had these events"). With these six small changes the notices are fit to release.

Reviewer: a fresh recheck subagent in Claude Code (Claude Opus 5.5), 9 November 2026. One reading, not a chain. Its agreement is a review contribution, not independent confirmation.

## What I read

AGENTS.md (step 4) and notes/reader-review.md ("After the review"); notes/R-0062-lh046-reader.md whole, with its "Resolution, by the driving session"; `git diff 4c9b77c` of articles/who-watches-the-internet.md, articles/what-we-can-see.md, investigations/ai-cost-and-spread.md, investigations/software-updates.md and studies/LH046/LH046.md; studies/LH046/data/hours.csv, files.csv and minutes.csv (headers), scripts/analyse.py (definition of the control types) and brief.md (the separate re-check); the opening of notes/R-0056-lh046-evidence.md, to check the colophons' description of it. The diff of ai-cost-and-spread.md also carries LH047 changes from another round. I did not check those.

## What I checked

Recomputed with studies/LH046/review/recheck/recheck.py; the output is in recheck-output.txt next to it.

- 452 distinct files (458 rows, some read in more than one set), all HTTP 200 and non-empty, dated 2026-01-01 to 2026-11-08: matches "all 452, dated 1 January to 8 November".
- Panel: 272 files, 68 at each of 00:00, 06:00, 12:00 and 18:00 UTC, 1 September to 7 November. Without PushEvent: 26 of 176 (14.8 per cent, "about one in seven") to 14 October, 64 of 96 (66.7 per cent, "two in three") from 15 October to 7 November, 90 of 272 (about a third) overall. PushEvent, CreateEvent and DeleteEvent are zero together in every panel file, so "missing altogether" and "absent together" hold.
- Runs: 11 in the panel, from 1 to 29 consecutive sampled files; the first starts at 12:00 on 1 September and runs to 06:00 on 5 September (16 files). That fits "runs, the first we saw in early September" and the record's four-day run. Because the panel starts on 1 September, "the first we saw" is the right wording: nothing earlier was sampled at those hours.
- Other types in files without pushes: 1,328 to 81,070 events, median 4,112. That fits "typically a few thousand to a file".
- Reference files at 12:00: the four control types (PullRequestEvent, IssuesEvent, IssueCommentEvent, WatchEvent, per analyse.py) were 21,503 on 1 January, 212 on 1 August and 189 on 15 August, so "about 200 an hour" holds. Push shares were 74.8, 97.6 and 97.9 per cent ("98 in every 100"), and pushes were 115,695 against 166,990. PullRequestReviewComment and CommitComment events also fell (1,668 to 13, 93 to 1), so "comments" is not too broad.
- "Pushes did not fall" compares 1 January with 15 August. One file between them, 15 May at 12:00, held about half the events of every type (72,852 pushes). I left the sentence alone, because it is a comparison of the two named hours.
- The quoted phrase in what-we-can-see.md appears once in its body, below the notice. Commit 3508ae0 holds record version 0.2. brief.md schedules the re-check separately, as the record's "due in December" says.
- Labels: "we find a whole hour of GitHub without a single push hard to believe" is attributed to us. It sits between "counts of what the files hold, not of GitHub's activity" and the conditional "If GitHub had the missing events". It names no cause and does not say GitHub lost anything. Both notices and the record keep the files-against-GitHub boundary and say that where and why are unknown. Every share carries its count, sample and window.

## Changes made

1. articles/who-watches-the-internet.md, `revised` item. Old: "and its other kinds of event thinned earlier in the year. No figure changed." New: "and its other kinds of event thinned earlier in the year in the noon hours we read. No figure changed." (The summary line had no basis or window, where the notice has one.)
2. articles/who-watches-the-internet.md, notice. Old: "Earlier in 2026, in the hours we read, all at noon UTC, its other kinds". New: "Earlier in 2026, in the hours we read at noon UTC, its other kinds". (We also read the 14:00 hour of 2 April.)
3. investigations/ai-cost-and-spread.md. Old: "and in the hours read from January to August, all at 12:00 UTC, the other kinds thinned". New: "and in the hours read at 12:00 UTC from January to August, the other kinds thinned". (Same reason.)
4. investigations/ai-cost-and-spread.md. Old: "not of GitHub's activity; whether GitHub's public events feed or GH Archive's collection lost the events is unknown, and so is why." New: "not of GitHub's activity; if GitHub had the events, whether its public events feed or GH Archive's collection lost them is unknown, and so is why." (The old wording took it as given that the events existed, which the record calls an untested interpretation.)
5. investigations/software-updates.md. Old: "and in the hours read from January to August, all at 12:00 UTC, its other event types thinned". New: "and in the hours read at 12:00 UTC from January to August, its other event types thinned". (The same sentence names the April hour, which was read at 14:00.)
6. investigations/software-updates.md. Old: "not of GitHub's activity, and whether GitHub's public events feed or GH Archive's collection lost the events is unknown." New: "not of GitHub's activity, and if GitHub had the events, whether its public events feed or GH Archive's collection lost them is unknown." (Same reason as 4.)

No figure changed. I made no change to what-we-can-see.md or to the record.

## Verdict

Fit to release as they now stand. Both notices, the investigation-page lines and record 0.3's opening and Answer state only what hours.csv shows, within their windows, and keep the reading that GitHub had the missing events labelled as ours and conditional.
