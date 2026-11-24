# R-0130: reader-and-inference review of LH049 version 1.0, stage one

## What a reader would believe, written before reading the record

Read from the record's header, "In short" and Answer, the proposed investigation-page line, and the first 40 lines of README.md, which has no "Current focus" section and says nothing about bee-js.

**Principal finding, as a careful reader would say it back.** A malicious version of a JavaScript library, bee-js 13.3.0, was on npm for about 75 minutes on 9 November. npm's public counts show 202 downloads of it over 9 to 12 November and none on 13, 14 or 15 November. We can't tell how many came on the first day. It could be anywhere from 0 to 202, because npm's numbers for that window don't add up. After 15 November npm shows nothing for it, and the study treats that as unknown, not zero.

**Observed.** npm's own counts: 202 across four days, and zeros on three days. The release was absent from the later windows. The Answer, outside the protocol, adds that every window covering 9 November gave exactly 202.

**Explained.** The day-0 figure is only bounded because some windows failed a pre-set consistency check. The later absence probably means no fetches were counted, but that's a post hoc reading.

**Caused what.** Nothing causal is claimed. A reader would probably infer, without being told, that most or all of the 202 came during the 75 minutes and that mirrors account for many of them, since the text says mirrors fetch new versions on publication day.

**Limits a reader would notice.** A download isn't an install or a victim. The day-0 count is unknown, so the study is inconclusive on its central figure. That the release was malicious is other firms' account. A reader may be puzzled that the figure is 202 on "9 to 12 November together" yet "0 to 202" for day 0, and may take "evidence-reviewed" as confirmation.

## Stage two, after reading the record

Read on 24 November 2026: all of studies/LH049/ (record, brief, sources, for-driver.md, closure checkpoint, data/record_v1_output.txt, REMOVED.md, scripts by name), the LH049 lines of investigations/software-updates.md and programme.md's Next, studies/LH053/brief.md ("Missing evidence", "Overlap") and notes/readiness/2026-11-14-operational-amendments.md. My calculation is in studies/LH049/review/r0130_check.py, with its output in r0130_check_output.txt. It reads only the retained bodies.

**What the round establishes.** The figures hold as stated: 202 in every per-version window holding 9 November, d(13 to 15 Nov) = 0 from held windows, the +210 gap only in the three windows holding 5 November, and no key for 13.3.0 in the balanced windows ending 16 and 23 November. The Answer follows the brief faithfully. Its measurements can be right while its framing of the day-0 count is too weak (below).

**Material claim problems.**

1. *The day-0 count is presented as open from 0 to 202, but the retained reads pin it at 202 under one assumption, and the text treats the remaining alternative as untestable.*
   - Passages: the proposed line, "bounded at 0 to 202, not exact, because npm's early windows don't add up". LH049.md, Answer: "How the 202 split between 9 November and the three days after it is unknown". LH049.md, Limits: "the reads can't tell these apart".
   - Evidence (review output, item 3): W(16 Nov) balances, 5,911 against 5,911, with no 13.3.0 key. The package daily totals for 10 to 15 November were identical at every read that held them (item 2: 923, 750, 1,070, 687, 1,017, 707). So npm counts no 13.3.0 fetch on 10 to 15 November, and later removed none from those days' totals. That holds if a balanced window's per-version table covers the same fetches as its package totals, which is the clock rule's own premise. It gives d(10 to 12) = 0, and with V(12 Nov) = 202 from a held window, d(9 Nov) = 202. The only exception is npm moving 13.3.0's fetches onto another version key while every total stays the same.
   - So the "drop from both tables" alternative is ruled out for 10 to 15 November. It stays open only for 16 November and for 17 to 23 November, days no earlier read held. A reader of the line believes the first day could hold anywhere from none to all 202. The evidence says all 202 fell on 9 November, which is the stronger answer.
   - The +210 excess sits outside 13.3.0, whose value is 202 in every window (item 1: the gap leaves when 5 November does, with large falls in old version 3.2.0). So "npm's early windows don't add up" says nothing about 13.3.0's own figure, but readers will assume it does.
   - Proposed resolution:
     - Keep the brief's answer. Add the check, labelled post hoc and outside the protocol, to Findings, with the code kept.
     - Narrow Limits' "can't tell these apart" to 16 November and 17 to 23 November.
     - Rephrase the line, for example: "By the rule we fixed in advance, the first day is bounded at 0 to 202. A later check, made after the counts were seen, finds the figures consistent only with all 202 on 9 November."
     - Make the same change in In short. Have the recheck read it.

**Readability.**
- Make it explicit in the line that "202 on 9 to 12 November together" covers the first day and the three days after it.
- Say that the early windows' mismatch lies in other versions.
- "Windows ending 16 and 23 November" means little to a reader. Try "the counts for 10 to 16 and 17 to 23 November".

**Next step.** Resolve problem 1 in the record's text. No new study is needed. LH053's absent-key rule ("none in npm's counts" in a balanced window, studies/LH053/brief.md) is already fixed, and its record can apply the same stability check before it treats the drop alternative as untestable. The study in the record's Next, of a still-listed version with low traffic, would add little. The check above already separates the explanations for the days that matter, from data in hand. Then the recheck, and release of the line.

**Combined disclosure:** clears.

## Resolution, by the driving session

Resolved on 24 November 2026 by a research subagent of the Research run (Opus 5.5), in studies/LH049/LH049.md version 1.1.

**The reasoning was checked and holds.** r0130_check.py was rerun with `python3 -I` and its output matched r0130_check_output.txt exactly. A second script, studies/LH049/review/resolution_check.py (output in resolution_check_output.txt), sets out each premise against the reads: the window for 6 to 12 November is held with 13.3.0 at 202; the window for 10 to 16 November is held, 5,911 against 5,911, with no 13.3.0 key; the package totals for 10 to 15 November are the same at every read holding them. The one premise the argument needs is the clock rule's own: a balanced window's per-version table covers the same fetches as its package totals. The argument also survives a drop made before the first read holding a day: if npm had dropped 10 to 12 November's fetches of 13.3.0 from both tables before the read of 13 November, they would not be in that window's 202 either, so the split of the 202 that were counted is the same. Nothing was found overstated. One scope note was added to the record: the check concerns fetches npm counted.

**Changed.** Findings gains a section, "A check of the day-0 split, made after the counts were seen", labelled post hoc and outside the protocol, with its one remaining alternative (npm moving fetches onto another version key with every total unchanged). The Answer's outside-the-protocol paragraph reports it and narrows "the reads can't tell that apart" to 16 November and 17 to 23 November. Limits' "No record is not zero" is narrowed the same way. The In short and the Answer now say that the 210 excess sits in other versions, not in 13.3.0's figure. The status lines, Limits' review line and Next say both reviews are done and the recheck pending. The record is bumped to 1.1 with a Corrections entry. The brief's answer is unchanged.

**Readability suggestions taken.** The In short says that "9 to 12 November together" covers the first day and the three after it, and names the later windows as "10 to 16 and 17 to 23 November".
