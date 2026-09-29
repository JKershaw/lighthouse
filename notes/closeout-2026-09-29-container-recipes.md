title: Close-out of the drive of the evening of 29 September 2026: whether a pinned project's own container recipe reads its pin
kind: close-out
version: 0.1
date: 2026-09-29
authors: the driving session (Opus 5.5)

## What was learned

- **About half of the pinned projects keep a container recipe** (observation; studies/LH015/LH015.md version 0.3).
  - The frame was the 469 moments whose pins LH008 to LH010 had timed: one of 332 public Python projects holding an older version of one of 31 widely used libraries in a pin or lockfile as a new release came out, from April 2025 to August 2026.
  - At 247 of the 469 (52.7 per cent, interval 45.9 to 59.3) the project kept at least one Dockerfile or equivalent at its last commit before the release.
- **Where the rules could decide, most of those recipes install from the pinned file** (derived measurement).
  - The recipe installed the library from the pinned file for 129 of the 167 projects at those moments (77.2 per cent, 68.6 to 84.4; 70 per cent counting each project once).
  - 68 of the 247 could not be decided (27.5 per cent), and the bounds are 54.9 and 83.8 per cent, so the brief's label is withheld.
  - A build from the project's own recipe would have bypassed the timed pin at no fewer than 38 of the 469 moments (8.1 per cent), and at no more than 106 (22.6 per cent).
- **Lockfiles are read less often than exact pins** (derived measurement, described, not tested).
  - Where a lockfile alone held the version, 21 of 37 decided cases installed from it, against 63 of 77 for an exact pin alone. Lockfile cases were also the most often undecided (41 of 153).
  - Among the 90 decided cases where a lockfile held the version, a container build read that lockfile in 45.
  - The pattern first seen in one program's images, a lockfile in the build that the install never reads while it works the versions out afresh, was 7 of those 90.
- **Interpretation, from the reader review and made after the counts.** The gap lies mostly in where the pin lives: 89 of the 129 that followed the pin never read a timed lockfile, their pin sitting in a manifest or requirements file that the install reads.
- **Not following the pin is mostly not floating** (derived measurement, an estimate).
  - Of the 38 that did not follow it, the recipe's instructions would let a fresh build take the new release for 2 and not for 12, and for 24 they do not say.
  - 14 of the 38 installed the project's own published package, which for 8 of them named one exact version.
- **The instrument** (observation). Anonymous blobless clones of 332 public repositories all succeeded on 29 September 2026. A blind check of 60 sampled builds by a second agent agreed on 57. Its three disagreements traced to two classifier rules, which were corrected after the check with no label moved.

## What changed in the current account

- The synthesis and its short form carry a "Later evidence" notice: the pins timed there mostly describe what those projects' own recipes would build, though more than a quarter of recipes could not be decided and a recipe is not an image.
- The new piece is articles/recipes-follow-the-pin.md, version 1.0, with its short form. It was released after notes/R-0021.md (blind check and evidence review) and notes/R-0022.md (the reader-and-inference review and a recheck).
- programme.md (LH015 under Answered; the choice, issue #19 and the pilot's decision under Next), the investigation page, the front page, AGENTS.md and observations.md say the same at the same certainty.
- The reader-and-inference review is kept as a standing step before release after its two pilot rounds (notes/reader-review.md; AGENTS.md step 4).

## What remains uncertain

- The undecided 68: 26 of them sit in four projects, and 13 are undecided only by the rule for which folder a build starts from.
- Whether the lockfile gap holds once more lockfile cases are decided.
- Which recipe, if any, makes the images people run. No registry or image was read, and development recipes counted alike.
- Whether a build installs the library at all. 12 of the 38 rest only on builds that never name it.
- What a project's CI does, which is where the download log's installs come from.

## Next outward question

LH013 still comes first: is what stays behind stable from week to week (issue #15)? It may read its weeks from about 13 October 2026.

For a session before then, the reader review recommended one bounded step on the slow road (issue #19): class the install steps of the same 469 moments' CI workflows under LH015's installer table. That would show whether CI reads the lockfile a recipe leaves unread, which is what the frozen-list reading of old downloads turns on.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --agent` for each subagent, and `harbour/hb drivercost --since 2026-09-29T14:00:00Z`. Output tokens are estimated from characters, so these are estimates.

| Item | Model | Cost |
| --- | --- | --- |
| Brief, frame and sources (phase 1) | Opus 5.5 | $5.59 |
| Collection, classification, record 0.1, and correction to 0.2 (one agent, two dispatches) | Opus 5.5 | $11.17 |
| Release review, stage A: blind check of 60 builds (notes/R-0021.md) | Fable 5.1 | $7.24 |
| Release review, stage B: evidence review (notes/R-0021.md) | Fable 5.1 | $8.80 |
| Reader-and-inference review, stage 1 (notes/R-0022.md) | Fable 5.1 | $0.48 |
| Reader-and-inference review, stage 2 | Fable 5.1 | $1.92 |
| Recheck by a fresh agent | Fable 5.1 | $1.55 |
| Subagents in all | | $36.75 |
| The driving session, to 17:54 UTC | Opus 5.5 | $15.24 |

The keeper raised this drive's subagent bound from twenty to fifty dollars during the round. Subagent spend was $36.75, and the drive in all was about $52.0 at list rates. The driving session's figure is incomplete: it leaves out this note, the final commit, the merge and the issue's close.
