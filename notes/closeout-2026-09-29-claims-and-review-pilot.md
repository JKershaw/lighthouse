title: Close-out of the improvement round of 29 September 2026: LH012's public claims corrected, a reader-and-inference review piloted, LH013 fixed and waiting
kind: close-out
version: 0.1
date: 2026-09-29
authors: the driving session (Opus 5.5)

## What changed in the public claims

The latest piece and its short form went to version 1.1 and the record to 0.3, with no figure changed. A dated Correction notice on each piece says what changed.
- **Other libraries' limits** (identified bounds) are now what a model could account for, not what they did. The model assumes that each download of a library that sets a limit brings one download of the library it limits; the log never links downloads, and for botocore and s3transfer its own ratios strain that assumption. Only pydantic-core is held largely by its dependent's current versions. For the other three, the hold comes through older versions, which moves the question to why those older versions are downloaded.
- **An old Python rules out the new version; it does not choose among the older ones.** boto3 is no longer offered as a fit for the obvious explanation, since 95 per cent of its Python 3.9 downloads were of versions older than the last one Python 3.9 can take.
- **A combination of reported fields is not a machine, an owner or a population.** The pieces, the record's interpretation and the next study's question no longer speak of one kind of machine.
- **The reader-and-inference review raised a new point, read from the same retained counts after publication and labelled post hoc.** boto3's and aiobotocore's older downloads are nearly equal version after version, over long runs of versions, which is the mark of an installer trying versions in turn and fetching each one it rejects. On that reading, most of those downloads were never installed. Measured the reviewer's way, such fetches were 17 per cent of the 37 libraries' older downloads pooled, and none for the median library. This reading is not yet tested.
- **The first-day test** still held for 28 of 32 libraries. It is now reported with its secondary ratio: for boto3 and aiobotocore the new version's small share still grew by about two thirds after day 2.

The front page's "Current focus" was cut to the central finding, why it matters and the next question. The investigation page, programme.md, AGENTS.md and the notices on the synthesis and the pace piece say the same at the same certainty.

## Where the review pilot is implemented

notes/reader-review.md holds:
- what the reader-and-inference review is;
- its allowance;
- how to dispatch it in two stages, with a fresh context;
- both task texts;
- what happens after it;
- a log with one row for each of the next two research rounds.

AGENTS.md, step 4, points to it in one sentence. The rehearsal of this round is notes/R-0018.md.

## Budget, and how usefulness is recorded

The allowance was set at five dollars at list rates for the reviewer on Fable 5.1, both stages and one recheck, within the round's bound of about twenty dollars. The rehearsal cost $13.34: stage one $1.24, stage two $6.46 (its own analysis of all 37 libraries' version profiles, which is where the walk reading came from) and the recheck $5.64. The recheck was sent to the same agent, whose whole context was re-read on every call. The note now sets the allowance at seven dollars, about one, five and one for the three parts, and sends the recheck to a fresh agent given the note and the diff. Because of the overrun, the changes after the evidence review were checked by the reader review's recheck and by the driving session's kept code, not by a second evidence review.

Each of the next two research rounds fills one row of the log:
- the cost;
- the material problems raised;
- which of them changed the release, and which were disagreed with, and why;
- which the evidence review also raised;
- what was done with the next-step recommendation;
- a one-line judgement of whether it was worth it.

The first checkpoint after the second of those rounds decides whether to keep the review, change it or drop it.

## Whether the next study is ready

LH013 is waiting for data. Its brief (studies/LH013/brief.md) is fixed. Its SHA-256 is posted on issue #15 (https://github.com/JKershaw/lighthouse/issues/15#issuecomment-5889344866) and kept in studies/LH013/snapshot_sha256.txt; the issue's title and body now say that it waits.

It reads the weeks of 28 September to 4 October and 5 to 11 October 2026, and may run only when ClickPy holds 12 October 2026, so not before 13 October. A day ClickPy then lacks counts as a gap day, and no week already read may stand in for either week. It measures:
- the older share and the Python-exclusion share against LH012's week;
- the share of downloads in the largest combination of reported fields;
- each library's count-by-version profile, with a test that boto3's stays flat;
- three of LH012's readings made after the counts.

Before 13 October, a session reads none of those weeks. It either takes another bounded outward question on its own merits (programme.md, Next, lists what each needs) or stops and says why. The smallest new reader worth seeking is one day of the package index's BigQuery table, which records the installer's version; it needs an account that a task must name.

## Unresolved disagreement or limitation

- **No disagreement remains.** The recheck (notes/R-0018.md, "Recheck") found no material claim problem remaining and three small wordings, which were fixed. It also read 1.1 as a label kept after a substantive change; 1.1 had not been released, and it carries all of this round's changes.
- **The rehearsal is not evidence that the reviewer finds known problems.** The pieces' own Correction notices named them before it read.
- **The walk reading is a post hoc interpretation.** It rests on thresholds chosen after the profiles were seen. Whether the download log counts the small metadata files that newer pips read is not known.
- **The tooling could not stop the reviewer reading other files in stage one.** The transcript shows it did not.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --latest` after each subagent, and `harbour/hb drivercost --since 2026-09-29T10:00:00Z`; output tokens are estimated from characters, so these are estimates.

| Item | Model | Cost |
| --- | --- | --- |
| Evidence review (notes/R-0017.md) | Fable 5.1 | $5.36 |
| Reader-and-inference review, stages one and two (notes/R-0018.md) | Fable 5.1 | $7.70 |
| Its recheck, by the same agent | Fable 5.1 | $5.64 |
| Subagents in all | | $18.70 |
| The driving session, 10:00 to 11:29 UTC | Opus 5.5 | $13.97 |

Subagent spend, $18.70, is within the bound of about twenty dollars; the round in all was about $32.7 at list rates. The driving session's figure is incomplete: it leaves out this note, the final commit and the merge.
