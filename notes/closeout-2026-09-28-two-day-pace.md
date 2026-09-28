title: Close-out of the drive of 28 September 2026: the two-day pace across the most downloaded libraries
kind: close-out
version: 0.1
date: 2026-09-28
authors: the driving session (Opus 5.5)

## What was learned

- For 26 of the 37 most downloaded Python projects that released a new newest version between April and August 2026, most releases reached half of the project's downloads, at that version or newer, on the first or second day (70.3 per cent, project-resampled 95 per cent interval 54.1 to 83.8): "for some projects", not "as a rule", by the convention the brief fixed before any count was read (derived measurement; studies/LH011/LH011.md version 0.2).
- The split is sharp. 21 projects had every release reach half, 11 had none, and 5 were mixed. For ten of the eleven (among them boto3, botocore, numpy, pandas, pytest and protobuf), no release reached half within 30 days, and nearly every project's share was set on the day after release and moved little for the month (derived measurement; the 34 of 37 reading in studies/LH011/data/piece_figure_reading.txt).
- In each release's first three days, the new release's pip and uv downloads carried the build-server flag less often than the replaced release's on the same days: the median of project medians was -6.6 points (interval -11.4 to -5.0), and every project's median per-release difference was below zero (derived measurement). pip's and uv's source sends the flag only as true or not at all, so it is a floor on builds (observation).
- Why the eleven are slow was not measured. Other libraries' version bounds and dropped support for older Pythons are both candidates (interpretation).

## What changed in the current account

The synthesis's fast half, "within days, at the download log's pace", rested on one release of one library. It now carries a dated "Later evidence" notice: the pace holds for most of the top projects, not as a rule. The same notice is on articles/what-a-download-shows.md, and the two short forms beside them have it too. programme.md has LH011 under Answered and a new checkpoint. The investigation page, the front page, AGENTS.md and observations.md say the same at the same certainty. The new piece, articles/two-days-for-most.md, was released after notes/R-0014.md.

## What remains uncertain

- What holds the eleven back.
- Whether the pace holds below the top fifty.
- How much of the early uptake is automated builds that set no flag.
- A download is still not an installation or a run.

## Next outward question

What holds back the eleven libraries whose releases never reach half (issue #14): the version bounds of the libraries that depend on them, or machines on Pythons the new release no longer supports? The reasoning is in programme.md, Next, checkpoint of 28 September 2026.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --latest` after each subagent, and `harbour/hb drivercost --since 2026-09-28T19:50:00Z`. Output tokens are estimated from characters produced, so these are estimates.

Three subagents cost $9.35:
- research: $3.02 (Opus 5.5)
- writing: $2.76 (Opus 5.5)
- release review: $3.57 (Fable 5.1)

The driving session cost about $2.2 to the time of this line, which leaves out the commit and merge. The total is about $11.5, within the bound of about twenty dollars.

## Addendum: the revision of the same evening

After the keeper read the released piece, it went to version 1.1 and its record to version 0.3, reviewed in notes/R-0015.md.

- **The current account.**
  - A low share of downloads is no longer read as slow uptake, because the log counts fetches.
  - The first-day observation is labelled as a reading made after the counts, to be measured on releases not yet read. For 34 of 37 libraries, the day-30 median was within ten points of day 1.
  - Part of every library's downloads stayed on older versions for the month (derived measurement, post hoc): 18 to 47 per cent in the 26 libraries where new releases took over, and 63 to 97 per cent in the eleven.
- **The next outward question, revised.** What keeps older versions downloaded after a new release, across all 37 libraries, and which explanations the public record can rule out: dependents' version bounds, Python compatibility, or environments rebuilt from frozen lists (issue #14; programme.md, the 28 September checkpoint as revised).
- **Known before that brief, to be disclosed in it.** The same four releases read two ways: 50 of LH008's 102 pinned repository pairs moved to the fix within 30 days, while the releases' download shares rose by 3.4 to 14.7 points.
- **Instructions.** AGENTS.md gained rules on absolutes in titles, pre-set labels, search results as leads, primary sources before a brief, what a count counts, selecting on the outcome, and rendered figures. CLAUDE.md gained a fast-forward command, a render command and a note on which hosts answered.
- **Spend of the revision.**
  - The review: $3.49 (Fable 5.1).
  - The driving session: $7.22 in all since 19:50 UTC, the drive's $2.1 included, to the time of this line.
  - The session as a whole: about $20.1 at list rates, at the bound of about twenty dollars.
