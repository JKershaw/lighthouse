# R-0132: recheck of LH049 version 1.1 (resolution of R-0130)

**In short.** A fresh agent read once what the round resolving the reader review wrote into studies/LH049/LH049.md (version 1.0 to 1.1, `git diff c1cedc0 ce53012`). The new post hoc check holds, and I reproduced it with my own code: if a balanced window's per-version table covers the same fetches as its package totals, all 202 counted fetches of 13.3.0 fell on 9 November, unless npm moved some onto another version with every total unchanged. One claim went further than the reads allow, and I narrowed it within version 1.1. Cleared at version 1.1.

Recheck by a subagent of the Research run of 24 November 2026, Opus 5.5 (claude-opus-5-5, as reported by the harness). Offline; retained files only. Row LH049-record-recheck.

## What I read

notes/R-0130-lh049-v1-reader.md (all, including "Resolution, by the driving session"); notes/R-0129-lh049-v1-evidence.md; the diff above; studies/LH049/review/r0130_check.py, resolution_check.py and both outputs; studies/LH049/data/record_v1_output.txt; the brief's clock rule, missing-evidence rules and inconclusive conditions (studies/LH049/brief.md, lines 48, 77 to 78, 103 to 107); the retained bodies under studies/LH049/data/read-*; schedule/research-safety.md.

## What I checked, and found

- **The key inference, reproduced.** studies/LH049/review/recheck_day0.py (output in recheck_day0_output.txt), written without reusing the earlier scripts, reads the bodies of the reads of 13 and 17 November and all package daily totals. W(12 Nov) is balanced with 13.3.0 at 202; W(16 Nov) is balanced, 5,911 against 5,911, with no 13.3.0 key; the package totals for 10, 11 and 12 November are 923, 750 and 1,070 at both reads. Under the stated premise the only split of the 202 compatible without re-attribution is 202 on 9 November, 0.1766 of the day's 1,144. The figures in the new Findings section (the six daily totals and their read counts, the 210 excess leaving between the reads of 12 and 13 November with the largest fall in 3.2.0, 17.7 per cent) all match the retained outputs.
- **Post hoc labelling.** The check is labelled post hoc and outside the protocol in its heading, in the Answer's outside-the-protocol paragraph, in In short ("A check made after the counts were seen, outside those rules") and in Limits; no measure uses it. The brief's answer is unchanged: 202 on 9 to 12 November together, 0 on each of 13 to 15 November, d(9 Nov) at most 202 with no lower bound, no record for 16 November and 17 to 23 November, measure 6 not made, inconclusive on the central figure. The one sentence added to the protocol Answer (the 210 excess sits in other versions, 13.3.0 at 202 in every window holding 9 November) is an observation from record_v1_output.txt and changes no figure.
- **The remaining alternative.** Stated fairly where the premise is stated. The Answer's paragraph did not state the premise; I added it.
- **Overstatement found.** Four passages (Answer, Findings twice, Limits) and Next said the check "rules out" for 10 to 15 November that npm dropped a removed version's fetches from both tables, while for 16 and 17 to 23 November the reads "can't tell". The reads support less. The unchanged package totals rule out a later removal of fetches npm had already tabled. They can't show, for any day after 9 November, fetches left out of both tables before npm first tabled the day; each of 10 to 15 November has a first holding read too (recheck output, last lines). The resolution's own note says as much ("the split of the 202 that were counted is the same"), but the record turned it into an asymmetry between 10 to 15 and 16 to 23 November that the reads don't carry. This doesn't touch the day-0 split, which concerns counted fetches.
- **Agreement across sections.** In short, Answer, Findings, Limits and Next agree after the corrections below. "Spread over other versions" in In short claimed more than is known about which versions carry the 210; changed.
- **Status lines and Corrections.** Accurate as of the resolution (both reviews done, recheck pending); commits 8b80fb7 and c1cedc0 exist. When this recheck is recorded, the driver should update "recheck pending" in the version line, the Answer's opening, In short, Limits' review line and Next; I left them, since they describe the queue.
- **Absolutes and wording.** "Every", "never changed" and "no answer at any read" each carry their window or reads. Downloads are called fetches. No harm or compromise is claimed in Lighthouse's voice: the release's maliciousness stays attributed to StepSecurity, Socket and the advisory. No em or en dashes.

## What I changed, within version 1.1

1. In short: "spread over other versions rather than 13.3.0's own figure" became "in other versions' figures rather than 13.3.0's own".
2. Answer, outside the protocol: stated the clock rule's premise before "all 202 counted fetches fell on 9 November"; replaced "rules out npm dropping ... for 10 to 15 November; for 16 ... can't tell" with a removal of already tabled fetches ruled out, and a pre-tabling omission not distinguishable for any day after 9 November, which doesn't affect the split of the 202.
3. Findings, absent-key bullet: the same narrowing.
4. Findings, check section, fifth bullet: the same narrowing, with a pointer to review/recheck_day0.py.
5. Limits, "No record is not zero": the same narrowing.
6. Next: "settles only post hoc, and only for 10 to 15 November" became "bears on it only post hoc, and only for the window of 10 to 16 November".
7. Corrections, version 1.1 entry: a sentence recording these recheck changes, with no figure or conclusion changed.

## Combined disclosure

Clears. Version 1.1 adds aggregate daily and weekly fetch counts from npm's public API for one removed release, and a consistency argument over them. It names no repository, dependent, mirror or person, describes no mechanism of the compromise, and joins nothing beyond what earlier versions held.

## Verdict

Cleared at version 1.1.
