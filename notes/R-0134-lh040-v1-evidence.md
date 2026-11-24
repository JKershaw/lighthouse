# R-0134: evidence review of LH040 record 1.0

**In short.** A fresh agent checked LH040's record, version 1.0 (the poisoned LiteLLM 1.107.0 counted in fetches from PyPI), against its retained reads and sources, and reproduced every consequential figure with its own code. Every figure matched; three small text fixes were made in place and the version stays 1.0. Cleared at version 1.0 for the reader-and-inference review.

- Queue row: LH040-record-evidence-review. Reviewer: a review subagent in Claude Code, Opus 5.5 (claude-opus-5-5, as reported by the harness), 24 November 2026.
- Reviewed: studies/LH040/LH040.md version 1.0 at commit 3cc2af7, against studies/LH040/brief.md (protocol 0.1 and the amendment of 9 November), the closure checkpoint, data/read-2026-11-09T1432Z, data/read-2026-11-23T1433Z, data/readiness-2026-11-23, the pre-brief copies and derived files, data/REMOVED.md and sources.md. No network request; no downloaded code run; tabulate.py was run only on a copy, in the scratchpad.
- Code and output: [reproduce.py](R-0134-lh040-v1-evidence/reproduce.py) and [output.txt](R-0134-lh040-v1-evidence/output.txt), written from the brief and the raw files without reading tabulate.py's logic (only its mirror-tool list, which the record's Method also states). Replay: `python3 -I notes/R-0134-lh040-v1-evidence/reproduce.py`.

## What was checked

1. **Integrity.** All 8 retained bodies of each read match the SHA-256 in their readlog.csv; at both reads the five deps.dev URLs are logged NotFetched under api.deps.dev's robots.txt (`Disallow: /`, group `*`, same hash prefix). The readiness probe shows 22 November held before read 2. Replaying tabulate.py on a copy of studies/LH040 reproduced data/record_v1_output.txt and every file in tables/ byte for byte.
2. **Measure 1.** C0 49,043 (both reads), litellm total 3,465,646 (both reads; equal to pypistats with mirrors, 3,431,091 without), S0 1.4151 per cent; 48,683 wheel and 360 sdist; 43 above 49,000. Reproduced.
3. **Gaps and duplicates.** 251 days, 17 March to 22 November, no missing date and no gap day under LH011's rule (d-3 to d+3). Duplicate-row dates at read 2 (9 April, 2 August, 19 October, 2 November, 21 November, 22 November with three) and the sums against pypistats, including 19 October's 3,339,530 against 3,302,031; 5 and 8 November in 2 and 5 rows at read 1, one row each at read 2, same totals. Reproduced.
4. **pypistats check.** 14 October to 4 November: 22 days, none over 5 per cent, largest +1.14 per cent on 19 October; 5 to 22 November: 18 days, none, largest minus 1.93 per cent on 17 November. Reproduced.
5. **Comparison set.** Rebuilt from L1's derived upload times (final releases by `packaging`): exactly the brief's 17 releases, with the collector's day 0 for each.
6. **Measure 3.** My own timeline (every final release plus 1.107.0 from 11:39:51 to each end) gives h(1.107.0) 1.72, 1.67 and 1.12, I 0.1976, 0.2035 and 0.3035, comparison min 0.1722, median 0.2921, max 0.4052, ratios 0.68, 0.70 and 1.04, ranks 17, 17 and 8 of 18, inside the range under all three ends, so the pre-set reading "travelled as an ordinary newest release did" holds. Every comparison I, 1.106.2's 0.268 and 0.256, 1.106.2's 11.54 hours, 1.108.1 as the only release below under the two later ends, and the five h under 2 releases uploaded after 22:00 with I 0.172 to 0.405, all reproduced.
7. **Measure 2.** The 32 daily values; no row on 16 and 19 November, both non-gap days with totals (no record, not zero); days 1 to 30, 1,502 on 28 days; to 22 November 1,541; first 18 days 1,431 at both reads. Installers days 1 to 30: none 954 (63.5), Browser 489 (32.6), uv 33 (2.2), requests 16, Nexus 9, devpi 1; no pip fetch on any day after day 0; 1,407 wheel, 95 sdist. Reproduced.
8. **Measure 4.** All twelve cells reproduced.
9. **Measure 5.** Every count, share, median and range in the table, the three categories outside the range (mirror tools, Darwin, CI), the 17 comparisons counted, and CI 10,153 of 46,966 (21.6 per cent), not known 2,077 (4.2 per cent), comparison median 12.3, range 8.5 to 17.7. Reproduced.
10. **Measure 6.** 16,930 and 102,391 on 24 March (119,321); 120,633 to 30 April with a row on every day and no gap day; 1.01 times 119,000. Reproduced.
11. **Re-read comparison.** 237, 2,721, 700, 125, 203 and 276 common cells, none different, none only in read 1; on 21 October 1, 75, 19, 11, 23 and 4. Reproduced. I also compared Q3 (March, 115 cells, none different; its body hash is identical at both reads), which the record doesn't mention.
12. **Every figure in the record** was found in record_v1_output.txt or reproduce's output. In short, Answer and Findings agree. Pre-set labels carry their numbers. Post hoc choices (Method 1 to 9, measure 5's outliers) are labelled. Missing is unknown throughout; deps.dev is a gap, not a zero.
13. **Attributed claims against the retained copies.** R1: "live from 11:39:51 to 13:23 UTC", "By 13:23: PyPI had removed", Docker images, and its own "approximately 2 hours"; R2: "frozen by ... (13:23 UTC)", "by 13:23 ... PyPI quarantines"; R8: "13:20 PyPI quarantines"; R7: "quarantined and removed", "between 11:39 and 12:47 UTC"; R9: "about 49,000 times from PyPI before removal", the sdist "Tampered build config, no payload", AWS credentials used 16:20 to 17:01; L10: "cannot be installed by package installers"; L7: `~/.claude`; R6: "Keys for OpenAI, Anthropic"; R5: "over 119k times". All as the record says, except R5 (below). The 1.72 hours behind "about an hour and three quarters" is derived from R1's times.
14. **Voice and mechanism.** Maliciousness and harm are attributed in the Answer; no claim in Lighthouse's voice that any system fetched, ran or was compromised; a download is called a fetch throughout; the payload is described only at the level the reports give; absolutes ("none by pip", "no cell changed") carry their windows.

## Findings

Must-fix (fixed in place):

1. **In short attribution.** The In short, read without the body, called the release poisoned and gave its window in Lighthouse's voice. Now: "(malicious by its maintainers' and several security firms' accounts)" and "by its maintainers' times".
2. **R5 misdescribed.** Measure 6 said PyPI's 119k was "interval not stated"; R5 says "During the window of attack, the exploited versions of litellm were downloaded over 119k times", and gives that window as "2h 32m". Measure 6 now quotes it and notes that ClickPy's 24 March figure is a whole UTC day. The factor-of-two test and its verdict are unchanged. (The brief says the same; it is a fixed protocol and was not edited.)
3. **Rounding.** 1.105.0's I under 13:23 was printed 0.338; unrounded it is 0.33749 (tabulate.py prints 0.3375, rounded again). Now 0.337.

A Corrections entry lists the three edits; version kept at 1.0, since no figure the conclusions rest on and no conclusion changed.

Suggestions (not changed):

- Measure 1 says StepSecurity's figure has "method and interval not stated" and then quotes its "before removal"; "method not stated, interval 'before removal'" would be tighter.
- The re-read comparison could mention Q3 (unchanged, identical hash).
- The title's "poisoned" is house usage (AGENTS.md uses it); a piece should attribute it near its first use.
- The grounded_at line says tabulate.py was uncommitted; it is now committed at 3cc2af7 with the same SHA-256 (50df1607...).

## Other surfaces (listed, not edited)

- programme.md (Next, Where software updates go) and observations.md line 36 still describe LH040 as version 0.1, interim and unreviewed, read 9 November to 8 November's days. Stale, not contradictory.
- AGENTS.md "Where things stand" says LH040 "keep[s] reading"; collection has stopped at the brief's stop. Stale.
- investigations/software-updates.md lists the record and states no LH040 figure; nothing contradicts.

## Verdict

Cleared at version 1.0 (with the three in-place edits above), for the reader-and-inference review.
