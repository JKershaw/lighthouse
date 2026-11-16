# R-0074: LH050 reader-and-inference review

Version reviewed: git HEAD 4c6c46fccd1228f395274f0120b09be26d707deb; studies/LH050/LH050.md sha256 2498be18b8991dad1d7826da7ada4de09a126f9b870ded44500e7ec4a2bbde9d (version 0.1 with R-0073's in-place corrections). Reviewer: Claude Opus 5.5 (claude-opus-5-5), subagent, 16 November 2026. Calculation: studies/LH050/review/r0074_matrix_split.py and .out.

## What a reader would believe, written before reading the record

(README.md has no section headed "Current focus"; only LH050.md's front matter, title, In short and Answer were read.)

**Principal finding, as a reader would say it back.** Public sources say a lot about what these robots are and what stage they are at, but almost nothing about who controls their use of force. Of 45 things Lighthouse looked for, only 7 had a source; none covered who picks targets or authorises force in any case.

**Observed.** Lighthouse read reports on Foundation's Phantom humanoid (a weapons-capable design, a two-robot logistics demo in Ukraine, US contracts, conflicting statements about autonomy in combat), could not read anything on the armed non-humanoid comparison, and read Singapore government descriptions of two Changi patrol robots (one operational since April 2023, one on trial since July 2025) with automated navigation, warnings, manual takeover of movement, and no weapon mentioned.

**Explained / caused.** The text implies the gap is in the public record itself: the sources relay the company or government and are silent on control. A reader would likely take the Phantom facts as reported rather than verified, and would probably infer the Changi robots are unarmed, though the text says this is not a finding.

**Limits a reader would notice.** Unreviewed; a single 36-minute read on 13 November; 14 of 45 cells unreadable, so "not established" partly reflects access failure; the comparison case is empty; the search was small and its completeness unverifiable; the cases were chosen by an earlier survey. A reader might not separate "not found in what we read" from "not public".

## Stage 2: the record behind it

Read after the section above was saved: the whole of LH050.md, brief.md with both amendments, sources.md, case_matrix.csv and case_matrix.py, panel.csv, both checkpoints, the seven retained case bodies (searched for AI, autonomy, weapon and control terms), investigations/physical-authority.md and programme.md's Next.

### What the round establishes

The measurements hold up. The tally of case_matrix.csv gives 7 supported, 23 not established, 14 unavailable and 1 conflicting, as the record says. The quotations behind the supported cells are in the retained bodies (PA-S24 "will not have full autonomy…"; PA-S27 "fully autonomous decisions"; PA-S28/S29 autonomous patrol and manual takeover). The record is careful about provenance (supplier claim relayed, official account), keeps eWeek's "far from battlefield-ready" beside the maturity claims, and does not read silence on weapons as a sign the robot is unarmed. What the round establishes is narrow. Through Lighthouse's access route (Anthropic's agent tokens, robots.txt, one query per case), the readable sources on four configurations (two Phantom, two Changi) give dated stage claims and do not describe who selects targets or authorises force.

### Material claim problems

**1. The control gap is built into the cases that could be read, but the opening presents it as a property of public records about armed robots.** Passage: LH050.md, In short, "the answer is very little about who controls force". Answer: "public records establish the stage each case has reached … much better than they establish human control … No cell for target selection or force authorisation in practice is supported by a source in any case". Under the title "armed robots and human control", my stage 1 reader took this to mean that public sources are silent on control. Evidence (r0074_matrix_split.out): 14 of the 45 cells are two whole rows lost to two failed reads (FT on robots.txt, Marine Corps HTTP 403). None of the 4 readable rows has a source showing a fielded weapon. All 8 target-selection and force-in-practice cells in those rows are therefore cells where a supported entry was hardly possible: Changi has no described weapon, and Phantom has no fielded armed configuration. The two cases that could have tested the claim (the Gaza application and the armed comparison) are the two that could not be read. The brief disclosed in advance that the writer expected this result (brief.md, Prior knowledge, last bullet). The counts can be right while the reading "public records are silent on control" is wrong. The evidence also fits "no readable case contains a fielded armed system whose control could be described" and "the access route closed the sources most likely to describe it". Resolution: say in the In short and the Answer that no readable case involves a fielded weapon. Say that the control cells could only have been filled by the two unreadable cases, so the round cannot tell silence in public records from the effects of case selection and access. Report the stage-versus-control contrast over the 4 readable rows (stage 4/4 supported, control 1/13) and give the 45-cell totals as accounting.

**2. The wording turns reported stages into established ones.** Passage: Answer, "public records establish the stage each case has reached". Evidence: Phantom's "stage" cells rest on four trade-press relays of the company (TechCentral possibly a syndicated copy). The contracts have "no award record read" (C030), the Ukraine date is "earlier this year", and nothing has been read on Changi since July 2025. Resolution: "public sources report each case's stage, mostly in the words of the company or government concerned, and as of their publication dates". The record already applies this distinction in Findings.

**3. The In short contradicts the record on Changi.** Passage: In short, "described in detail by the police without any mention of a weapon or of who decides what they do". Evidence: PA-S05 describes a two-way link to the Airport Police Operations Room for "better decision and sense-making". PA-S29 says officers summon GIBSON by app and take manual control. The Answer itself says "a manual takeover for mobility". Resolution: "…without any mention of a weapon; they describe officers directing movement, not who would decide on force".

### Readability

- Label the Answer's "45 cells" as matrix cells in the same sentence. The Findings note ("not of robots, weapons or events") comes too late for a reader of the opening.
- LH050.md Next and Limits still say no panel is locked ("the weekly change log (no panel is locked yet)"). panel.csv was locked at 2026-11-16T14:25:29Z, so Next should point to it.
- "Two reported statements of intent … that do not agree": the TechCentral sentence is the outlet's own wording, not quoted from the company. Say so.

### Next step

The locked panel (panel.csv P01 to P08) is available on 19 November and can run as fixed. It cannot tell the explanations in play apart. Four of its pages are December 2025 to June 2026 trade articles that relay the same company. A change to one of them shows only that the outlet edited it, not the robot's control. The four policy pages duplicate the separate policy reads of 21 to 23 and 27 November. No reading of these eight pages can show whether a public record of a fielded armed robot describes its control, and that is the question problem 1 leaves open. Recommendation:

1. Let the panel run as locked. It is cheap, and changing it now would be choosing by outcome.
2. Correct the opening for problems 1 to 3 before the evidence recheck.
3. Before 26 November, write a dated amendment that sets one rule-bound route to a readable first-party record of a fielded or tested armed ground robot, for the empty armed comparison, under the brief's existing bounds. Disclose any candidate already seen, such as the unadmitted August 2026 Ukrainian ministry turret notice and the eWeek "Taiwan … armed robot dogs" lead, as selection after reading. Only such a case can show whether control goes unrecorded even where a weapon is present. If no such record is readable, the final statement should say so. It should not generalise from unarmed and unfielded cases.
