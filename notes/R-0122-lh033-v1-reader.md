# R-0122: reader-and-inference review of LH033 record version 1.1

Reviewer: a review subagent (Claude Code, Opus 5.5), 23 November 2026. Read only the header, the "In short." paragraph and the "## Answer" section of studies/LH033/LH033.md, stopping at "## Findings"; nothing else opened, no links followed.

## What a reader would believe, written before reading the record

**Principal finding, said back.** A month after PHP's emergency fix of 21 October, most internet-facing PHP servers on the still-supported branches that show their version had taken it: roughly three quarters in 8.2 and 8.3, closer to nine in ten in 8.4 and 8.5, and still climbing. But more than half of all version-reporting PHP servers, 22.5 million, run old branches that got no fix at all.

**Observed.** Censys's daily counts of services by reported PHP version, classified patched or not by Censys; the day each branch passed half; the last week's rise. Python download shares come from earlier studies.

**Explained.** Little. The text says the patched share is a floor because some distributions fix PHP without changing the version number, so the true protected share is likely higher. The older branches lagging the newer ones is described, not explained.

**Caused.** Nothing is claimed to cause anything. A reader might still drift towards "PHP caught up with and overtook Python" from "below on day 1, above on days 14 and 30", despite the warning that services and downloads are different units and say nothing about speed.

**Limits a reader would notice.** Only services reporting a version are counted; Censys's own classification is trusted; the share is a floor; the Python and Node.js comparisons are in different units, and the Node.js tests are post hoc. The record is unreviewed. A reader may not grasp what "test A" and "test B" or "amendment 2" mean, and may wonder whether the unfixed old-branch servers are vulnerable, which the text leaves unsaid.

## Stage 2

Read for this stage: the rest of studies/LH033/LH033.md (version 1.1), brief.md with its amendments, data/record_v1.json, scripts/record_v1.py, the retained Censys reads (through my own script), investigations/software-updates.md, programme.md's Next, and studies/LH034/brief.md and the Answer of LH034.md. Checkpoints were listed but not opened. Disclosure check (schedule/research-safety.md): these are aggregate counts of PHP versions from a public dashboard, with no hosts, addresses or exploit detail, so there's nothing to raise; proceed.

My calculation is studies/LH033/review/r0122_composition.py, and its output is r0122_composition.out. Using the record's rule (earliest read per day), it splits each branch's change in share into the part from a change in the patched count and the part from a change in the branch total.

### What the round establishes

The measurements hold up. The day-30 shares, the dates each branch passed half, the unfixed tail, the distance behind the fix and the amendment 2 figures match record_v1.json, and no read revised any day. The record is careful about units, floors and the post hoc label, and it assigns no cause.

### Material claim problems

1. **"Still rising" reads as services still patching, but late in the month much of the rise is the denominator shrinking.**
   - Passages: LH033.md, In short: "still rising by one to three points a week". Answer: "Every branch was still rising at the end, by 1.3 to 3.0 points over the last week". Test A: "more of PHP's day-30 share arrived after the first week".
   - Evidence (r0122_composition.out): from day 14 to day 30, Censys's patched count barely moved in three branches: +55,421 in 8.2, +46,896 in 8.3 and +19,881 in 8.5. That is 0.5 to 0.9 points at a fixed denominator. Over the same period those branches' totals fell by 311,749, 429,445 and 81,585, and that fall gives most of their 4.7, 4.6 and 2.5 point rises. Only 8.4 grew mainly through patching (+311,748).
   - Over the final week (day 23 to 30), the patched count added more than a point only in 8.2 (3.10) and 8.4 (5.89). In 8.3 it added 0.82 and in 8.5 0.58; the rest of their 2.19 and 1.31 point rises came from fewer services in the count.
   - Test A's second condition holds on shares, as it was fixed. But the reading it was meant to test, that standing services keep updating late, is supported in two branches, not four.
   - The measurements could be correct while the implied explanation (continued patching) is partly wrong: unpatched services dropping out of the count, through going offline, hiding their version or being reclassified, would produce the same shares.
   - Resolution: add the patched counts and branch totals to Findings, with this split. In the In short and Answer, say the rise is in the share, and that after day 14 it came mostly from fewer unpatched services being counted, except in 8.4. In test A, add that the share condition held but the patched count rose by a point or more in only two branches. The cause stays unassigned.

2. **What "patched" counts.** This is a lesser problem, folded into 1. Branch totals grew by up to 56 per cent (8.5, day 0 to day 14). In 8.5, the day-30 patched count exceeds the day-7 total of the whole branch (101.2 per cent). So "patched" probably includes services first seen already on a fixed version, which is not "took it" in the In short's sense; the record's Limits say this was not checked. Resolution: carry that one-line limit into the Answer, and reword the In short's question as "how many were counted on a fixed version".

### Readability

- The In short leaves out that 62 per cent of the services counted on day 30 report no version, so every share describes the minority that does. One clause would fix this.
- In the Answer, say that a stock starting near zero would always cross a flow that sits between 53 and 72 per cent. That makes the crossing with Python a consequence of the units, as Findings already suggests, and the reader will not take it as "PHP overtook Python".
- Explain "test A" and "test B" in plain words in the Answer: "later uptake" and "older branches lag".

### Next step

Go ahead with the planned recheck, but first make the problem 1 revision. The data for it is already retained, so it needs no new collection, and it should happen before the revision of the week-one piece reuses "still rising".

Before the piece is revised, a cheap step would tell continued patching apart from drop-out: compare branch_versions across the retained reads, to see whether the unpatched versions shrink while the fixed versions grow, or whether both shrink.

Measure 6 (1 December) compares ordinary and emergency releases on the same instrument at the same ages, so W3Techs's lag affects both sides equally. It can describe a difference but not explain one, and it stays post hoc. It doesn't help with problem 1.

## Resolution, by the driving session

By the Research run of 23 November 2026. The material problem is accepted and verified from the retained counts (studies/LH033/scripts/record_v1.py now writes `m1_counts` and `m1_count_changes`; they match the reviewer's r0122_composition.out). Version 1.2 adds the counts table under measure 1, qualifies the opening, the Answer and test A, and moves the "patched includes first seen fixed" limit into Limits with the 8.5 evidence, worded as our interpretation. One part is narrowed rather than taken whole: from day 7 to day 30, the span test A's L measures, every branch's patched count rose by 0.76 to 1.58 million, so test A's "after the first week" is supported by counts in all four branches; it is the last-week rise and "still rising at the end" that rest on a shrinking branch count in 8.2 (partly), 8.3 and 8.5. Readability suggestions taken: the 62.3 per cent with no version in the Answer, the crossing with Python said to follow from the units, tests A and B introduced in plain words. Next step: the comparison of branch_versions across reads is noted in the record as not made; it is a candidate for the week-one piece's revision or LH033's version 1.1 with measure 6, not done here. The recheck (row LH033-v1-recheck) reads what this resolution wrote.
