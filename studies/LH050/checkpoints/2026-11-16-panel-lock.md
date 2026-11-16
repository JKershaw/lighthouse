# Panel lock, 16 November 2026

**In short.** We locked eight pages to re-read each week from 19 November: the four news reports we hold on Foundation's Phantom and four official policy pages. The Singapore airport sources and the Ukrainian ministry notices are not in the panel, for reasons the brief gives. We chose these pages after reading the baseline, and say so.

Row LH050-panel-lock, protocol 0.1 with Amendment 1 and the operational scheduling amendment of 14 November. Locked at 2026-11-16T14:25:29Z (the time panel.csv was written). Done by Claude Opus (Anthropic, model id claude-opus-5-5) under Claude Code, as a subagent. Time spent: about 10 minutes of agent time. Cost: unknown (not measured; unknown is not zero). No document was fetched; only robots.txt files were read.

## What was locked

[panel.csv](../panel.csv), rows LH050-P01 to P08, 8 of the 12 allowed:

- Foundation/Phantom, the primary case: PA-S24, PA-S25, PA-S26, PA-S27.
- Policy: PA-S16 (UNODA conference page), PA-S15 (UN Geneva release), PA-S11 (ICRC FAQ), PA-S13 (GOV.UK JSP 936 page).

## The selection rule

The selection was made after the baseline outcomes were read; it is post hoc and labelled so in every row. To keep it from following those outcomes, one rule was applied to every source the baseline admitted (readable at read label 2026-11-13T1454Z), and no source was picked over another for what it said:

1. Every readable source for the primary case goes in. That is all four Foundation reports; the company site (PA-S03) and the FT and Wired reports were unavailable, so were not admitted.
2. Readable official policy pages go in if they are HTML pages that can be revised. Fixed PDFs (PA-S19, PA-S20) are left out, since the data dictionary says a document that cannot change need not be fetched weekly; the post-conference policy reads cover them and any adopted text. The docs.un.org viewer shells (PA-S21 to PA-S23) carry no document text, so no change in text could be read from them.
3. Context-only sources (PA-S08, PA-S09, PA-S10, PA-S12) are left out. They describe methods and research programmes, not claims about the cases or policy wording.
4. Sources for the comparison cases are left out (below).

Each locked endpoint had a fresh robots decision with `LIGHTHOUSE_PROVIDER=anthropic` at about 14:25Z: all eight allowed under the `*` group. The records are in `data/2026-11-16T1425Z/robots/`. The weekly panel reads feed the change log only; the policy comparison keeps its own reads on 21 to 23 and 27 November.

## Left out, and why

**Changi (PA-S05, PA-S28, PA-S29).** These are the civilian comparison case's sources. The brief keeps case-comparison sources out of the recurring panel unless a dated amendment explains why, and it treats the comparisons as classification checks, not cases to follow. No amendment was written. The only reasons to add them now would come from what the baseline showed (for example, that GIBSON's status after July 2025 is unknown). Adding them for that reason would be choosing by outcome. The panel was filled by its rule without them. The armed non-humanoid comparison has no admitted source.

**Ukraine ministry notices (PA-S30, PA-S31; Amendment 1).** The amendment allows up to two endpoints for this series in the panel. It does not require them. Six weekly reads of each would not fit the amendment's own bound of five document reads (three used, two kept for December), if panel reads count under it, and the amendment does not say whether they do. The amendment also says what happens without them: the December read stays the series' only further read (row `LH050-ukraine-notice-dec`). The series' index page was never admitted or gated, so it was not a candidate.

## For the next rows

The first weekly read is 19 November, window that date only, at most 8 endpoints plus one connection-failure retry each, no retries around walls. Each read compares with the previous readable snapshot. For P01 to P08 that is the baseline copy in `data/2026-11-13T1454Z/bodies/`, which is a pre-conference copy, and the read is labelled as such. A source rests after three consecutive unavailable weekly reads; there is no replacement. This checkpoint is unreviewed working material, not a finding.
