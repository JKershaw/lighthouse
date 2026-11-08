# Choice of result to reproduce

Written 8 November 2026, about 19:00 UTC, by a fresh agent on Fable 5.1 (claude-fable-5-1, as reported by its harness), before any analysis code was written or run and before any outcome figure of the record was read.

## The result chosen

LH011's pace result: in 26 of 37 of the most downloaded Python libraries, most new releases (April to August 2026) reached half of the library's downloads within two days, and in eleven none did. The figures to reproduce are the count of projects with a known outcome, the count whose most releases reached half within two days, the count with none, and, as secondary checks, the project-resampled 95 per cent interval, the median and quartiles of the projects' median day-1 shares, and the pooled count over releases.

## Why this one

- It is the most central figure of the released work: the title claim of the pace piece (articles/two-days-for-most.md), the first figure of the synthesis's current account and the first sentence of AGENTS.md's summary of what is known.
- Everything it rests on is in the repository: data/counts/*.csv (ClickPy's daily downloads by version, read 28 September 2026), data/pypi_versions.csv (PyPI's version list with upload times), data/projects.csv, data/daily_totals_*.csv (for the gap rule) and the brief with its amendment fixing every rule. No account, key or network read is needed.
- LH013's result rests on larger data and a less compact rule; LH033 and LH034's day-14 figures are interim readings of a third-party tracker whose record is still at version 0.1.

## What was read before computing, and what was deliberately not

Read: AGENTS.md, charter.md, programme.md's opening; studies/LH011/brief.md (the brief and amendment 1, which record the frame: project list, releases, numerator rule, gap rule, "most" rule, bootstrap seed); studies/LH011/sources.md; studies/LH011/replay.sh; the headers and first rows of the data files; the module docstrings (first lines) of scripts/common.py, analyse.py, frame.py and collect_counts.py, for their inputs and outputs; the read_log's query text for one counts query and the daily-totals query, to learn how "~other" was folded.

Not read: studies/LH011/LH011.md (any part), data/analysis/*, data/piece_figure_reading.txt, data/post_hoc_reading.txt, review/*, uptake.svg, the pieces (articles/two-days-for-most.md, articles/where-software-updates-go.md and the others), investigations/software-updates.md, and the bodies of the scripts beyond their docstrings. The headline figure (26 of 37, eleven none) was given to me in the task and is also in AGENTS.md, so I knew the target before computing; nothing finer than that.

## Plan

1. Rebuild the frame (qualifying releases, replaced versions, day 0) from pypi_versions.csv and projects.csv with my own code, and compare with data/releases.csv, which amendment 1 committed before any count was read (it is method, not outcome).
2. Compute each release's at-or-newer share on days 0 to 30 from data/counts, apply the gap rule from data/daily_totals_*, classify "reached half within two days" and "days to half", aggregate by project, bootstrap.
3. Only then open LH011.md and data/analysis/ and compare; then run replay.sh.
