title: Close-out of the drive of 30 September 2026: whether pinned projects' CI workflows install what the pin names
kind: close-out
version: 0.1
date: 2026-09-30
authors: the driving session (Opus 5.5)

## What was learned

- **CI is kept, and reads the pin.** At 469 moments from April 2025 to August 2026 when one of 332 Python projects held an older version of a widely used library in a pin or lockfile, 395 kept GitHub Actions or GitLab CI jobs (84.2 per cent). Where the rules decided, some job installs the library from the timed file at 282 of 291 moments (96.9 per cent, interval 94.4 to 98.9, "as a rule"). The 291 moments fall in 211 projects. Derived measurement (studies/LH017/LH017.md, version 0.3).
- **The lockfile itself, mostly.** Where a lockfile held the version, some job reads it at 164 of 188 moments (87.2 per cent, "as a rule"). Derived measurement.
  - At 83 of the 164, only through commands that may re-lock. Counted strictly, 81 of 161 (50.3 per cent). Derived measurement.
- **Beside the container recipes, under one rule.** Counted the same way, one build being enough, the recipes read the timed lockfile at 71 of 113 moments and installed from the pin at 164 of 194. Asked of every build, as the recipes' study asked, CI installs from the pin at 231 of 302 (76.5 per cent), against the recipes' 129 of 167. Derived measurements, made after the counts (post hoc).
  - Interpretation: CI reads the lockfile much more often than recipes by either rule; the pin more often only by the looser rule.
- **What the download log could see.** At 236 of the 282, a job reading the pin uses pip or uv, which send the CI flag. Derived measurement.
  - At 125, every such job is set to restore a cache. By setup-uv's own READMEs, read after the counts, 55 of those have a job whose cache keeps no pre-built wheels between runs, so it fetches them again. Derived measurement, post hoc.
- **A road, not a count.** Interpretation: the pinned versions are what each test run is told to install, on services that flag automation. That is a road from the pin to the older-version downloads in PyPI's log. No run was read, so its volume is unknown.

## What changed in the current account

- The slow road now reads: pins move over weeks; container recipes install from them in most decided cases, with no label standing; CI jobs almost always, the lockfile itself mostly, half of that through commands that may re-lock.
- The comparison between tests and recipes is now stated under one rule on every surface. The earlier draft had compared two different rules.
- The synthesis and its short form carry a dated "Later evidence" notice.
- The investigation page, the front page, programme.md (LH017 under Answered, the checkpoint) and AGENTS.md say the same at the same certainty.
- The new piece, articles/tests-read-the-lockfile.md, was released after notes/R-0026.md, R-0027.md and R-0028.md.

## What remains uncertain

- How many of the log's older downloads come down this road.
- Whether jobs ran, how often, and what their caches held at each run.
- Whether the jobs that could re-lock ever did.
- The 50 undetermined moments, and whether a job installs the library at all.

## Next outward question

LH013 still comes first: is what stays behind stable from week to week (issue #15)? It may read its weeks from about 13 October 2026.

Before any of its counts, its brief takes an amendment, to be written by a session before then. It reads the CI flag's share of pip and uv downloads below and at or above the reference release. It crosses that with whether the download's Python is admitted by the newer versions. Older downloads flagged CI on an admitted Python are the trace this road predicts. A test matrix on an old Python, or a resolver's walk in CI, would lean the same way without it.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --agent` for each subagent, and `harbour/hb drivercost --since 2026-09-30T06:40:00Z`. Output tokens are estimated from characters, so these are estimates.

| Item | Model | Cost |
| --- | --- | --- |
| Release review: blind check of 40 jobs and evidence review (notes/R-0026.md) | Fable 5.1 | $6.76 |
| Reader-and-inference review, stage 1 (notes/R-0027.md) | Fable 5.1 | $1.02 |
| Reader-and-inference review, stage 2 | Fable 5.1 | $2.06 |
| Recheck of both resolutions by a fresh agent (notes/R-0028.md) | Fable 5.1 | $4.33 |
| Subagents in all | | $14.18 |
| The driving session: brief, collection, classification, record, piece, resolutions and release, to 09:38 UTC | Opus 5.5 | $43.66 |

Subagent spend was $14.18 of the drive's twenty-dollar bound. The reader review with its recheck cost $7.41, over its seven-dollar allowance by the recheck. The drive in all was about $57.8 at list rates. The driving session's figure is incomplete: it leaves out this note, the final commit, the merge and the issue's close.
