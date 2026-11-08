# Reproduction of LH011's pace result by a fresh agent

**In short.** The programme says it is done, among other things, when someone other than the analyst can reproduce an important result from the retained evidence and method. On 8 November 2026 an agent on a different model (Fable 5.1) that had never seen the analysis took LH011's headline, that in 26 of 37 of the most downloaded Python libraries most new releases reached half of the downloads within two days and in eleven none did, and recomputed it from the brief and the retained data alone, with its own code, before opening the record. Every figure checked came out the same: 26 of 37, eleven with none, 127 of 424 releases pooled, the 54.1 to 83.8 per cent interval, the median day-1 share of 57.6 per cent and its quartiles, and the per-release classes for all 424 releases. The record's own replay command then passed byte for byte on a newer Python. That condition of the programme is met for this result; this note says what was read, what was not, and the one labelling point found.

Written 8 November 2026, about 18:55 to 19:10 UTC, by a fresh agent in Claude Code on Fable 5.1 (claude-fable-5-1, as reported by its harness), on repository commit 3829c39 (branch claude/adoring-gauss-l5dn33). The original work was done on Opus 5.5 with a review on Fable 5.1 (studies/LH011/LH011.md, header); this agent is not that reviewer and saw none of its work before computing.

## What was chosen, and why

LH011's pace result, the first figure of the synthesis and the title claim of [the pace piece](../../articles/two-days-for-most.md). The choice and its reasons were written and committed before any code was written (choice.md, commit 36548cf). In brief: it is the most central released figure; everything it rests on is in studies/LH011/data/ (ClickPy's daily downloads by version, PyPI's version list, the project list, the daily totals for the gap rule), read on 28 September 2026 and needing no account or network read now; and the brief with its amendment 1 fixes every rule it needs.

## What was read before computing, and what was not

Read: AGENTS.md, charter.md and programme.md's opening; studies/LH011/brief.md including amendment 1 (the frame, the numerator rule, the gap rule, the "most" rule, the bootstrap's seed and size); studies/LH011/sources.md; studies/LH011/replay.sh (to learn what the original replay compares, not to run it); the headers and first rows of each data file; the module docstrings of scripts/common.py, analyse.py, frame.py and collect_counts.py, for what each reads and writes; and, from data/read_log.csv, the text of one counts query and the daily-totals query, to learn how versions outside the numerator sets were folded into `~other`.

Deliberately not read before computing: studies/LH011/LH011.md in any part; data/analysis/*; data/piece_figure_reading.txt and data/post_hoc_reading.txt; review/*; uptake.svg; the pieces and the investigation page; the bodies of the scripts. The headline figure (26 of 37, eleven none) was in the task and in AGENTS.md, so the target was known; nothing finer than that was.

data/releases.csv was read and compared after my own frame was built. It is the frame amendment 1 committed before any count was read (commit f833a4b), so it is method rather than outcome; my frame was derived from pypi_versions.csv and projects.csv first and matched it exactly (424 releases in 37 projects, every day 0 and replaced version the same).

## Code and output kept here

- code/reproduce_lh011.py: the independent analysis, written without running or reading analyse.py or frame.py. Standard library plus `packaging` 26.3 on Python 3.13.18. It rebuilds the frame, computes each release's at-or-newer share on days 0 to 30 from data/counts/, applies the brief's two gap clauses from data/daily_totals_*.csv, classifies each release, aggregates by project and bootstraps. Run as `python3 -I code/reproduce_lh011.py output` from this directory.
- output/frame_diff.txt, output/release_outcomes.csv, output/project_outcomes.csv, output/summary.txt, output/run.log: its results.
- code/compare.py and output/compare.txt: the comparison with data/analysis/, written after the record was opened.
- code/post_read_checks.py and output/post_read_checks.txt: checks of the Findings' finer sentences and of the piece's opening example, written after the record was opened, so a check rather than an independent reproduction.
- output/replay_run.log: the original `sh studies/LH011/replay.sh`, run after my own figures were in.

## The comparison

| Figure | Record (LH011.md v0.4, data/analysis/) | Reproduced here | Class |
| --- | --- | --- | --- |
| Qualifying releases, projects that released | 424 in 37 | 424 in 37, same releases, day 0s and replaced versions | reproduced exactly |
| Projects with a known outcome | 37 | 37 | exactly |
| Projects where most releases reached half within two days | 26 (70.3 per cent) | 26 (0.703) | exactly |
| Projects where none did | 11 | 11, the same eleven | exactly |
| Projects where every release did; mixed projects | 21; 5 (starlette 9/11, uvicorn 14/16, pydantic 5/6, pydantic-core 5/7, cryptography 6/7) | 21; the same 5 with the same counts | exactly |
| Reporting convention | for some projects | for some projects | exactly |
| Project-resampled 95 per cent interval (10,000, seed 20260927) | 54.1 to 83.8 per cent | 0.541 to 0.838, under two percentile conventions | exactly (see note 1) |
| Projects' median day-1 share: median, quartiles | 57.6; 29.5 and 69.0 | 0.576; 0.295 and 0.690 | exactly |
| The eleven's median day-1 shares | 2.0, 7.5, 9.5, 10.2, 21.3, 23.4, 24.6, 27.7, 29.3, 29.5, 34.0 | the same eleven values | exactly |
| Pooled over releases | 127 of 424 (30.0 per cent); unknown 0 | 127 of 424 (0.300); unknown 0 | exactly |
| Gap days under the brief's rule | none | none, either clause | exactly |
| Per-release "reached half within two days" class and days to half | 424 rows | 424 rows, 0 class mismatches, 0 days-to-half mismatches | exactly |
| Per-release shares on days 0 to 2 | 6 decimal places | 4 decimal places; largest difference 0.00005, rounding | within tolerance (rounding) |
| Releases reaching half within 30 days; on day 0; median day | 139; 23; day 1 | 139; 23; day 1 | exactly (post-reading check) |
| litellm's releases that reached half | 6 of 46, median day 25, all first on 1 May 2026 | 6, median day 25.0, all on 2026-05-01 | exactly (post-reading check) |
| The eleven's median day-30 shares | 2.5 (aiobotocore) to 37.0 (s3transfer); litellm 9.5 to 21.0 | 2.5 to 37.0; litellm 9.5 to 21.0 | exactly (post-reading check) |
| Piece's opening: requests 2.34.0 day 1 and day 30; pandas 3.0.3 | 35 of 64 million, 55 in 100, 61 per cent; 28 in 100, 32 per cent | 35,233,968 of 64,346,148 = 54.8; 60.7; 27.7; 32.3 | exactly, at the piece's rounding (post-reading check) |
| Original replay command | REPLAY PASSED expected | REPLAY PASSED, every table, figure and reading byte-identical, on Python 3.13.18 and packaging 26.3 (the record names 3.11.15 and 24.0) | exactly |

Nothing was not reproduced. No error was found in the record's figures or in the piece's.

Notes.

1. The brief fixes the bootstrap's size and seed but not the random generator or the percentile convention. I used Python's `random.Random(20260927).choices` and took both the index convention (the 250th and 9,750th of 10,000 sorted values) and inclusive quantiles; both gave 0.541 to 0.838, and the record gives 0.540541 to 0.837838. With 37 projects the share takes only 38 values, so the convention rarely matters here; a brief that wants an interval reproducible to the last digit should name the generator and the convention. This is a method under-specification, not a discrepancy.
2. The brief's pre-release rule says "not a pre-release or development release (PEP 440)". `packaging`'s `is_prerelease` already counts development releases; I applied both tests and the frame matched, so the wording caused no difference.
3. One labelling point, not an error in any public claim. data/analysis/project_outcomes.csv has a column `releases_not_reaching_half_by_day_30` that counts the five releases of 31 August (boto3 1.43.84 and 1.43.85, botocore 1.43.84 and 1.43.85, protobuf 7.36.1) whose day 30 ClickPy did not yet hold, so they are "not reached by day 27" in release_outcomes.csv but counted as not reaching by day 30 in the project table (boto3 103 where 101 are known not to reach by day 30 and 2 are censored). The record's prose handles this correctly ("or by 27 September, the last day held, for the six releases of late August"; the sixth, filelock 3.32.5, reached half and so is not censored). The column's name could say "by day 30 or the last day held". The record is not edited here; for-driver.md notes it.
4. Whether `~other` could hide a numerator version was checked: every explicit version string in data/counts/ is in PyPI's non-pre-release list for its project, and every numerator version of every release is explicit, so the server-side folding lost nothing the shares need.

## What it means for the programme's condition

The condition reads "someone other than the analyst can reproduce at least one important result from the retained evidence and method". For LH011's pace result it is now met in the strong sense: an agent on a different model, which had not seen the record, the analysis tables, the scripts' bodies or the pieces, derived the frame and every headline figure from the retained raw data and the brief alone, and the result was the same to the last digit; and the record's own replay then ran clean on a newer interpreter. What the exercise cannot speak to is the data itself: every count is ClickPy's copy of PyPI's log as read on 28 September 2026, and reproducing the analysis says nothing about whether a fresh read of ClickPy today would give the same counts (the record's Limits and sources note that ClickPy re-ingests days it finds wrong). The condition is about the analysis from retained evidence, and that is what was tested.

The same exercise has not been done for the CI-flag half of LH011's answer, for LH013, or for LH033 and LH034; one result is what the condition asks for.

## Spend

This agent's own transcript, not the launcher's figure, holds what it spent; the driving session prices it with `harbour/hb tokens --latest`.
