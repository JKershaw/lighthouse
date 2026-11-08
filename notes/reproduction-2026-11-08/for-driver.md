# For the driving session

From the reproduction of LH011's pace result, notes/reproduction-2026-11-08/report.md, 8 November 2026.

## programme.md

The opening paragraph's first condition ("someone other than the analyst can reproduce at least one important result from the retained evidence and method") is met. Suggested line, under Answered or beside the condition, dated 8 November 2026:

> **Reproduced, 8 November 2026.** A fresh agent on a different model (Fable 5.1), which had not read LH011's record, analysis tables, script bodies or pieces, rebuilt the frame and recomputed the pace result from studies/LH011/data/ and the brief alone: 26 of 37 projects, eleven with none, 127 of 424 releases, the 54.1 to 83.8 per cent interval and every per-release class came out the same, and the record's own replay then passed on Python 3.13 ([the note](notes/reproduction-2026-11-08/report.md)). The programme's first condition for being done is met for this result; the CI-flag half of LH011, LH013 and LH033/LH034 have not had the same exercise.

## investigations/software-updates.md

One line, if the page lists checks of its evidence: "8 November 2026: LH011's pace result was reproduced from the retained data by a fresh agent on a different model, every figure the same (notes/reproduction-2026-11-08/report.md)."

## Correction a record needs

None to any public figure or claim. One labelling point in studies/LH011 (not edited here, as the task asked): the column `releases_not_reaching_half_by_day_30` in data/analysis/project_outcomes.csv also counts the five releases of 31 August whose day 30 ClickPy did not yet hold (release_outcomes.csv marks them "not reached by day 27"), so boto3 and botocore show 103 where 101 are known and 2 censored, and protobuf 4 where 3 are known and 1 censored. The prose of LH011.md says this correctly. If the record is next edited, rename the column in analyse.py and regenerate with `sh studies/LH011/replay.sh --write`, or add a sentence under Limits; a Corrections entry would say that no figure changed.

## Method note for future briefs

A brief that wants a bootstrap interval reproducible to the last digit should name the random generator and the percentile convention as well as the seed and the number of resamples; LH011's did not, and with 37 projects it happened not to matter.

## due.csv

No new row.
