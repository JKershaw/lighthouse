# LH046 for the driving session

Record 0.1 (studies/LH046/LH046.md), unreviewed. Everything below waits on its evidence review and reader-and-inference review; nothing public should change before them. Commits: 52a44b0 (brief), 6036750 (amendment 1), 5540e97 (counts), and the record commit that adds this file.

## programme.md, Next

### Repair, 8 November 2026: how complete GH Archive's hourly files have been (LH046)

A reviewer's quick scan suggested that GH Archive's hourly files had lost their pushes since mid-October, and GH Archive is the public event record behind the map's row I28, two released pieces and question 4 of the third investigation, so the instrument came before any further reading of it. LH046 (record 0.1, unreviewed) read 452 hourly files from January to 8 November 2026 under a brief fixed before any was read. All were present and none empty, but pushes, new branches and deletions were absent together from 26 of 176 sampled hours from 1 September to 14 October and 64 of 96 from 15 October, in runs whose edges fall inside an hour, while the other types kept arriving at a few thousand an hour; and from January to August the other types had thinned instead, to a few hundred an hour by August. No notice that could be read explains either. Next: the record's two reviews; then a re-check of 8 November to 6 December on hours not read (due row below); and before any GH Archive reading, a count of what each hour used holds, by type and minute.

## investigations/ai-cost-and-spread.md

Replace the sentence about LH046 in "Where the evidence stands" (Activity on the open internet bullet) with:

> Separately, GH Archive's hourly files, the public event record question 4 would have read, were all present from January to 8 November 2026, but whole event types are missing from many hours: pushes, new branches and deletions were absent from 64 of 96 sampled hours from 15 October and 26 of 176 from 1 September to 14 October, and by August the other types had thinned to a few hundred an hour ([record](../studies/LH046/LH046.md) 0.1, unreviewed). The files are what GH Archive kept, not GitHub's activity, and the cause is unknown.

## investigations/software-updates.md

A line where the page lists what its instruments can bear (or under "Beside it"):

> GH Archive, which LH002 read for one hour, held all event types in April 2026, but from September many of its hourly files hold no pushes, and earlier in 2026 its other event types thinned sharply ([LH046](../studies/LH046/LH046.md), record 0.1, unreviewed). LH002's hour is unchanged; any further use of the archive for this investigation should count what each hour holds first. This bears on P-0006.

## Proposed "Later evidence" notice for articles/who-watches-the-internet.md (map row I28)

Released piece: this is a proposal for review, not an edit. Near the opening, after the reviews of LH046:

> **Later evidence, [date].** One of the instruments on this map, GH Archive, the hourly record of public GitHub activity, kept its hourly cadence through November 2026: every hourly file we checked was there. But from mid-October most of the hours we sampled held no pushes, new branches or deletions at all, and earlier in 2026 its other kinds of event thinned sharply. An hourly file can be present and still incomplete. [The record](../studies/LH046/LH046.md).

The same review should consider **articles/what-we-can-see.md** (released), which says GH Archive "records every public event on GitHub, hour by hour"; from the files read, that did not hold for most of 2026. A possible notice:

> **Later evidence, [date].** GH Archive's hourly files from 2026 are not a record of every public event: by August 2026 they held almost nothing but pushes, and from September many hours held no pushes at all, two in three of the hours we sampled from 15 October. Why is unknown. [The record](../studies/LH046/LH046.md).

And the writer of **essays/what-the-watch-would-see.md** (draft) should know that its line "the push lands in GH Archive's hourly file" did not hold for 64 of 96 sampled hours from 15 October.

## sources.md (next free numbers after S41)

- **GitHub REST API docs, events and event types.** https://docs.github.com/en/rest/activity/events and https://docs.github.com/en/rest/using-the-rest-api/github-event-types, read 8 November 2026 (undated pages, API version 2026-03-10 in examples). Public events latency "anywhere from 30s to 6h"; PushEvent payload without commits; CreateEvent ref types branch, tag, repository. No change notice for October or November 2026. Retained in studies/LH046/data/sources/.
- **GitHub changelog, "Upcoming changes to GitHub Events API payloads", 8 August 2025.** https://github.blog/changelog/2025-08-08-upcoming-changes-to-github-events-api-payloads/, read 8 November 2026. Push events lose commit summaries and counts from 7 October 2025. Explains the PushEvent payload LH002 and LH046 saw.
- **GitHub changelog, "Email notifications for repository push events have been retired", 15 October 2026.** https://github.blog/changelog/2026-10-15-email-notifications-for-repository-push-events-have-been-retired, read 8 November 2026. A different feature from the Events API; recorded because of its date, with no link stated.
- **GitHub status incidents API.** https://www.githubstatus.com/api/v2/incidents.json, read 8 November 2026 (last 50 incidents, 31 August to 8 November 2026). No incident names the public Events API.

## schedule/due.csv rows

```
id,study,task,earliest,latest,status,updated,by,ref,note
LH046-review,LH046,"Evidence review then reader-and-inference review of record 0.1 (reproduce analyse.py from the retained counts; check the figure rendered light and dark; check the proposed notices for the map and what-we-can-see)",2026-11-09,2026-11-16,open,2026-11-08,,studies/LH046/LH046.md,no public notice before both reviews
LH046-recheck,LH046,"Re-check on hours not read: every day 8 November to 6 December 2026 at 03:00, 09:00, 15:00, 21:00 UTC with collect.py's measures (needs a sample amendment or a short brief); record 0.2",2026-12-07,2026-12-14,open,2026-11-08,,studies/LH046/LH046.md,"ends 14 December 2026; also try GH Archive's issue tracker"
```

## proposals.md

- **P-0006** (how complete GH Archive is for a small cohort): add "LH046 (8 November 2026) measured the whole feed hour by hour: from September many hours hold no pushes, and in January to August the non-push types thinned. A cohort study would have to choose hours where the relevant types are present; LH046's data/files.csv says which sampled hours those are."
- **New lead, repair:** "When did GH Archive's non-push event types thin, and did any reach zero?" LH046's 16 reference hours show pull request events per hour falling from 11,989 (1 January 12:00) to 95 (15 August 12:00) while pushes rose. Bears on LH043's July hour (425 pull request events) and on any 2026 reading. Cost: small, the same collector on more hours. Source: LH046, finding 8.
- **New lead, from finding 9:** no tag or repository creation appeared in any of 1,808,380 CreateEvents in the 2026 files read, though GitHub's docs list both. Whether that is true of 2025 too is unread.

## What was not done

- GH Archive's issue tracker was not read (HTTP 403 from this session's proxy; the GitHub tool refused the repository). Adding it to the session was not attempted, being outside this task.
- No figure screenshot is retained in the repository (rendered and checked in the scratchpad, light and dark).
- No review was run.
