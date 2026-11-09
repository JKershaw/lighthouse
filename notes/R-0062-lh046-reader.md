# R-0062: reader-and-inference review of LH046 and its proposed "Later evidence" notices

Reviewer: a review subagent in Claude Code (Claude Opus 5.5), 9 November 2026. Stage 1 was written before reading anything of the record beyond its opening paragraph and Answer, and the proposed public texts in for-driver.md.

## What a reader would believe, written before reading the record

**Who watches the internet.** The body never names GH Archive; a reader meets it, if at all, as a box on the figure's software layer. They would believe only that public instruments exist on each layer and that each has documented edges. Nothing about GH Archive's completeness is claimed, so nothing about it is believed.

**What we can see.** A careful reader comes away believing that GH Archive "records every public event on GitHub, hour by hour, since February 2011", limited only by private projects and by not telling people from agents. Completeness of public events is presented as fact, not as the page's own claim, and was not tested ("We did not test any source against its data").

**After the notices.** The reader would believe: the files kept coming hourly; from mid-October most sampled hours held no pushes, new branches or deletions; earlier in 2026 other event types thinned (by August almost nothing but pushes); cause unknown. Observed: files present, types absent in sampled hours. Explained: nothing, explicitly. Caused: the who-watches notice's "kept its hourly cadence" and "earlier... its other kinds of event thinned" lean towards the archive as the place of loss, and the what-we-can-see notice's "GH Archive's hourly files ... are not a record" is fair, but a reader may hear "GitHub activity fell" unless told the counts are the files' contents.

**Limits a reader would notice.** "Most of the hours we sampled" and "two in three" without saying how many hours, or how they were chosen; "every hourly file we checked" is a sample, not all; "thinned sharply" has no figure; neither notice says the loss might be upstream at GitHub's feed.

## Stage 2: after reading the record

Read: studies/LH046/ (record 0.2, brief and amendment 1, searchlog, scripts, data, for-driver.md), the GH Archive lines of investigations/ai-cost-and-spread.md and investigations/software-updates.md, and programme.md's Next. I re-tallied the panel from data/hours.csv with my own few lines: 26 of 176 files without PushEvent from 1 September to 14 October and 64 of 96 from 15 October to 7 November (by hour 17, 15, 16, 16); PushEvent, CreateEvent and DeleteEvent zero together in every such file; the 64 fall in six runs. The August references match finding 8. The collector counts `type` per parsed line and the files were stable by hash, so a counting artefact is unlikely.

### What the round establishes

- Every one of 452 hourly files dated 1 January to 8 November 2026 was present, parsed and non-empty when read on 8 November (observation).
- In the 272 panel files (four fixed hours a day, 1 September to 7 November), pushes, new branches and deletions were absent together from 90; 64 of 96 from 15 October, at each sampled hour of day, including the three hours the reviewer's lead never saw (48 of 72). They go in runs whose edges fall inside an hour, while other types keep arriving (observation).
- In 16 reference files at 12:00 UTC, January to August, the non-push types fell to a few hundred by August while pushes rose to 98 per cent of events (observation, one hour of day only).
- Why, and where (GitHub's public feed, GH Archive's collector, something else), is unknown. That GitHub had the missing events is a strong but untested interpretation; no independent count of GitHub's activity was read. The record says all this.

The measurements could be right while a notice is wrong in one way that matters: the record keeps "the files hold" apart from "GitHub's activity" and from "GH Archive lost them"; the notices, as drafted, drop that boundary.

### Material claim problems

1. **The files-not-GitHub boundary disappears in both notices.** "most of the hours we sampled held no pushes" (map notice) and "are not a record of every public event" (windows notice). The first can be read as "no one pushed in those hours"; the second states as fact that GitHub had events the files lack, which the record labels an untested interpretation. Neither says the loss may lie upstream in GitHub's public events feed rather than in GH Archive. That matters most on the map, whose subject is where an instrument stops: if the feed is the cause, every reader of GitHub's feed is affected, not one archive. Fix: speak of what the files held, and add "Whether GitHub's public events feed or GH Archive's collection lost them is unknown."
2. **Absolutes not bounded by the window.** "kept its hourly cadence through November 2026" (map): files were read to 8 November only, and the notice will be dated later; "two in three of the hours we sampled from 15 October" (windows) has no end date; "GH Archive's hourly files from 2026" generalises to the year, though the January and April files held all 16 types. Fix: "to 8 November 2026", "from 15 October to 7 November", and limit the claim to the files read.
3. **"From mid-October" reads as an onset the record rejects.** The record says the lead "that this began on 15 October does not" hold; September had a four-day run. "From mid-October most..." with no earlier figure invites the onset reading. Fix: give both shares, with the earlier one.
4. **Shares without their sample.** "Most" and "two in three" are fair descriptions of 96 files spaced every six hours, and the share holds at the hours outside the lead, but they come from about six long runs, and the 15 October split came from the lead. The reader needs the counts and "four a day" to weigh them. "By August ... almost nothing but pushes" rests on two files at 12:00 UTC; say "in the hours we read".

Not problems: no notice names a cause, and "Why is unknown" is right (the map notice should carry it too); the post hoc hourly-budget reading stays in the record, labelled, and out of every public text; amendment 1 changed only the byte ceiling; the September baseline failure is handled by the brief's own rule.

Smaller, for the driver: for-driver.md and the two investigation pages, as they now stand, cite "record 0.1, unreviewed"; the record is 0.2 after its evidence review, and should be cited so once this review is done. The software-updates line calls GH Archive "the hourly record of public GitHub activity", which is the claim in question; "which keeps hourly files of GitHub's public events" is safer. Its present tense ("many of its hourly files hold no pushes") should be "held ... in the hours sampled to 7 November".

### Readability suggestions

- The map notice's last sentence, "An hourly file can be present and still incomplete", is the point for that piece; keep it, but say "can be present and still lack whole kinds of event", since "incomplete" again implies a known whole.
- Define "new branches and deletions" once as GitHub's branch-creation and branch-or-tag-deletion events, or simply say "pushes and branch events".

### Next-step recommendation

Do the re-check (every day 8 November to 6 December at 03:00, 09:00, 15:00, 21:00 UTC): its hours are disjoint from the panel and test persistence out of sample, cheaply. Before it runs, fix its reading in writing (for example, what share of files without pushes counts as "continuing", "mixed" or "ended") so December is not read post hoc. It cannot say where the loss happens, so add, by amendment fixed beforehand, a small discriminating read: GitHub's public events endpoint polled at set times over a few days, recording whether PushEvents appear there in minutes when the corresponding GH Archive file has none. Pushes present in the feed but absent from the file would point at the collector; absent from both, at the feed. A mirror of GH Archive is not independent and should not be used for this. Keep trying GH Archive's issue tracker. Checking a few January to August hours at 00:00, 06:00 and 18:00 would show whether the thinning is an artefact of reading only 12:00; that can stay a proposal.

### Verdict on each proposed notice

**articles/who-watches-the-internet.md (map row I28): release with the stated change.** Replacement text:

> **Later evidence, [date].** One of the instruments on this map, GH Archive, which keeps hourly files of GitHub's public events, kept its hourly cadence to 8 November 2026: all 452 hourly files from 2026 that we checked were there. But what the files held changed. Pushes, new branches and deletions were missing from two in three of the hours we sampled, four a day, from 15 October to 7 November (64 of 96), and from about one in seven before (26 of 176 from 1 September); earlier in 2026 its other kinds of event thinned sharply in the hours we read. Whether GitHub's public events feed or GH Archive's collection lost them is unknown, and so is why. An hourly file can be present and still lack whole kinds of event. [The record](../studies/LH046/LH046.md).

**articles/what-we-can-see.md: release with the stated change.** Replacement text:

> **Later evidence, [date].** Above we say GH Archive "records every public event on GitHub, hour by hour". For much of 2026 its files did not bear that out. In the hours we read, by August 2026 they held almost nothing but pushes, and from September pushes, new branches and deletions were missing from many hours: two in three of the hours we sampled from 15 October to 7 November, and about one in seven before. Counts of what the files hold are not counts of GitHub's activity, but a whole hour of GitHub without a single push is hard to believe. Whether GitHub's public events feed or GH Archive's collection lost them is unknown, and so is why. [The record](../studies/LH046/LH046.md).
