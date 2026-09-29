title: Close-out of the drive of 29 September 2026: what keeps older versions downloaded
kind: close-out
version: 0.1
date: 2026-09-29
authors: the driving session (Opus 5.5)

## What was learned

- In the week of 21 to 27 September 2026, a median 37.3 per cent of each of the 37 libraries' downloads were of versions numbered below its newest of 21 August (20.0 per cent for pyjwt to 99.3 for pydantic-core; 45.6 per cent pooled). This is a derived measurement (studies/LH012/LH012.md, version 0.2).
- **Old Pythons.** For 32 of the 37 libraries, less than half of those older downloads came from a Python that no newer version supports: 86.5 per cent of libraries, interval 75.7 to 97.3, "as a rule" by the brief's convention (derived measurement).
  - Old Pythons were most of those downloads in three libraries: boto3 (76 per cent), aiobotocore (63) and numpy (63 to 67).
  - Even in boto3 and aiobotocore, most of those downloads were of versions older than the last one their Python supports.
- **Other libraries' limits.** Limits declared by the 500 most downloaded libraries were most of the older downloads in four: pydantic-core, fsspec, botocore and s3transfer. For botocore and s3transfer the estimate's assumption is strained (derived measurement).
  - They could not be the main reason in seven, and were undetermined in 26.
- **Frozen lists.** Environments rebuilt from frozen lists cannot be counted in the log. 18 of the 37 libraries show the trace fixed for them (derived measurement).
  - uv made a median 60 per cent of older downloads against 43 per cent of newer ones (derived measurement).
  - That the trace comes from such lists is interpretation.
- **The first-day share.** A new version's share settling within two days and holding for the month held as a rule on 355 releases from November 2025 to March 2026 that no earlier study read: 28 of 32 libraries, interval 75.0 to 96.9 (derived measurement; a test fixed before reading).
- **boto3 on Python 3.9.** Read after the counts, and not tested: on 23 September 2026, 62.2 per cent of boto3's downloads came from Python 3.9, 99.4 per cent of them pip on glibc Linux with no CI flag. Over the week, Python 3.9 fetched boto3 7.51 times as often as botocore (observation, post hoc).
  - That this is one population fetching again and again is interpretation.

## What changed in the current account

- The first-day pattern was a reading made after the counts. It is now a tested result for these libraries.
- The three explanations for what stays behind are now measured where the log allows: old Pythons for three libraries and ruled out for 32, other libraries' limits for four.
- The synthesis and the reading of the pace carry dated "Later evidence" notices, and so do their short forms.
- programme.md has LH012 under Answered, a "Later evidence" line after LH011 and the checkpoint of 29 September.
- The investigation page, the front page, AGENTS.md and observations.md say the same at the same certainty.
- The new piece, articles/old-versions-new-pythons.md, was released after notes/R-0016.md.

## What remains uncertain

- What the older downloads that neither testable explanation accounts for are.
- Whether other libraries' limits hold back the 26 libraries the log leaves undetermined.
- Whether boto3's Python 3.9 downloads, and what stays behind generally, hold from one week to the next.
- A download is still not an installation or a run.

## Next outward question

Is what stays behind stable from week to week, and how much of a library's downloads can one kind of machine make (issue #15)? The reasoning is in programme.md, Next, checkpoint of 29 September 2026. A census of public lockfiles waits for a reader of public code at scale that a task names.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --latest` after each subagent, and with `harbour/hb drivercost --since 2026-09-29T06:00:00Z`. Output tokens are estimated from characters produced, so these are estimates.

Two subagents cost $15.50:
- research, brief and collection, one agent over two phases: $9.59 (Opus 5.5);
- release review: $5.91 (Fable 5.1).

The driving session cost $7.24 to 08:10 UTC. That figure is incomplete: it leaves out the commit, the merge and the issue's close. The total is about $22.7 at list rates, with subagent spend within the bound of about twenty dollars.
