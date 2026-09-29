title: Close-out of the drive of the afternoon of 29 September 2026: the two-day pace below the top fifty
kind: close-out
version: 0.1
date: 2026-09-29
authors: the driving session (Opus 5.5)

## What was learned

- **Below the fifty most downloaded Python libraries, the two-day pace is not the rule** (derived measurement; studies/LH014/LH014.md version 0.2).
  - 80 libraries were drawn at random from ranks 51 to 500 of ClickPy's August 2026 downloads, and 80 from ranks 501 to 5,000; 52 and 35 of them put out new newest versions from April to August 2026.
  - Most of a library's new versions reached half of its downloads within two days for 25 of the 52 (48.1 per cent, interval 34.6 to 61.5) and 9 of the 35 (25.7 per cent, 11.4 to 40.0), against 26 of 37 in the top fifty.
  - Both bands read "not as a rule" by the brief's convention. Band A's interval includes one half.
- **A smaller share, mostly set early** (derived measurement). The median library's day-1 share was 57.6 per cent at the top, 48.1 in band A and 22.7 in band B. The share settling by day 2 held as a rule in band A (39 of 50) and for some projects in band B (23 of 35), where releases that reached half took a median of four days.
- **Mirrors are not the reason** (derived measurement). The mirror programs pypistats.org names made a median 148 and 62 downloads of a release on its first two days, 0.01 and 0.23 per cent of its own, and leaving them out changed no outcome. The literature check had expected them to matter at these ranks.
- **Read after the counts, by the reader-and-inference review** (post hoc; about twenty comparisons; notes/R-0020.md, studies/LH014/review/r0020_inference.txt):
  - Observation: for 172 releases that replaced a version at least two weeks old, the replaced version's share on the eve of the release had project medians of 62, 51 and 31 per cent in the three groups. The new version's day-30 share was typically within two points of it. Releases whose predecessor held less than half reached half within two days 2 times in 91, against 68 in 81 for the rest.
  - Interpretation: what differs down the rankings is mostly how much of a library's downloads follow its newest version at all, before any release, rather than how fast they move. That makes it the same question as what stays behind.
- **The instrument.** ClickPy's public `demo` user returns partial counts, without an error, once a query passes its read limit of a billion rows (observation, from the user's settings and ClickHouse's documentation). LH011's and LH012's logged queries never came within a quarter of that limit, so none of their counts was cut short. LH014 and, by amendment, LH013 now make every such query fail instead.

## What changed in the current account

- The synthesis and the reading of the pace, and their short forms, carry a "Later evidence" notice. Half the downloads within two days is common among the most downloaded libraries and not the rule below them. Further down, a typical new version holds a smaller share from its first full day, which on the post hoc reading is about the share its predecessor held.
- The new piece is articles/rarer-further-down.md, version 1.0, with its short form, released after notes/R-0019.md and notes/R-0020.md.
- programme.md (LH014 under Answered, the next step under Next), the investigation page, the front page, AGENTS.md and observations.md say the same at the same certainty.

## What remains uncertain

- Why new versions of less downloaded libraries take smaller shares. Rank is not a cause, and no dependent, pin, Python or release habit was measured.
- Whether the eve-share reading holds on releases not read.
- Whether band A sits above or below one half.
- A download is still a fetch, not an installation or a run.

## Next outward question

LH013 still comes first: is what stays behind stable from week to week (issue #15)? It may read its weeks from about 13 October 2026.

Two follow-ups are filed as issue #17:
- The next pace reading's brief will fix the eve share and the day-2 share as a fraction of it. It will use a fresh draw of releases from September 2026, whose thirty days are held from about 1 November.
- After LH013 reports, LH012's measures could be read for the 87 band libraries that released, on LH013's weeks.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --agent` after each subagent, and `harbour/hb drivercost --since 2026-09-29T11:40:00Z`. Output tokens are estimated from characters, so these are estimates.

| Item | Model | Cost |
| --- | --- | --- |
| Research, brief, frame, counts and record (one agent, three phases) | Opus 5.5 | $8.93 |
| Release review (notes/R-0019.md) | Fable 5.1 | $3.28 |
| Reader-and-inference review, stage 1 | Fable 5.1 | $0.55 |
| Reader-and-inference review, stage 2 | Fable 5.1 | $2.78 |
| Recheck by a fresh agent | Fable 5.1 | $1.85 |
| Subagents in all | | $17.39 |
| The driving session, to 13:59 UTC | Opus 5.5 | $10.63 |

Subagent spend, $17.39, is within the bound of about twenty dollars, and the drive in all was about $28.0 at list rates. The driving session's figure is incomplete: it leaves out this note, the final commit, the merge and the issues' close.
