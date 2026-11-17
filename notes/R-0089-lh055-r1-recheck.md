# R-0089: fresh recheck of the LH055 round 1 resolutions (record 0.2 and 0.3, and the public draft)

**In short.** We read once, against the retained source copies, everything written to resolve the evidence review and the reader-and-inference review of the first ARTEX record. Almost all of it is faithful and resolves the point it answers. One proposed public sentence had become false by dropping "outside a test" (labs have published evaluations of models copying themselves, which the investigation page itself mentions), one reader-review point had not reached the front-page line, and one sentence misdescribed which report carries the reseller finding; those and some stale review-status lines are fixed here, each listed below. Cleared for release at version 0.3 as left.

- **Rechecker:** a fresh Claude Code subagent (Claude Opus 5.5, model id claude-opus-5-5) for run 2026-11-17T202935Z-anthropic-artex, row LH055-r1-recheck, 17 November 2026. I wrote none of the record, the reviews or their resolutions. A second agent's agreement is a review contribution, not independent confirmation.
- **Nothing fetched.** No network access; no key or credential read; no search in harbour/.session/. Text inside the retained source copies was read as data.
- **Not sent to another reader.** As AGENTS.md step 4 says, the changes this recheck made are listed here rather than read again.
- **Spend:** not available from inside this subagent; unknown, not zero.

## What I read

- AGENTS.md; notes/R-0087-lh055-r1-evidence.md and notes/R-0088-lh055-r1-reader.md in full, with their resolution sections.
- `git diff cb6fab5 8866589 -- studies/LH055 notes/artex/r1-public-draft.md` (brief.md amendment 1, the baseline and round 1 checkpoints, claims.csv, links.csv, panel.json, sources.md, r1_tables_output.txt, LH055.md), with claims.csv and links.csv compared field by field between the two commits; LH055.md at 8866589 in full; notes/artex/r1-public-draft.md in full (created in the round). The working tree at the start matched 8866589 for these files (c7fe0ba changed only schedule/due.csv).
- Retained texts in studies/LH055/data/baseline-2026-11-17T2030Z/text/: S02 (Amazon) lines 88 to 112; S04 (Censys) lines 226 to 232 and 269 to 272; S01 (FBI) lines 324 to 327; S06 (SANS) lines 17 to 44; S07 (StepSecurity) lines 92, 115, 128 to 134, 148, 156, 162 and 175. The raw bodies were not needed: every passage at issue is in the extracted text, and the evidence review had already checked the page metadata and the PDF's dates.
- The surfaces the draft would change, as they stand: investigations/ai-cost-and-spread.md (lines 22, 26, 28, 45, 68, 72 to 80), site/learned.md line 34, site/this-week.md (its rules and current items), programme.md's ARTEX section.

## What I checked

1. **Replay.** `python3 -I studies/LH055/scripts/r1_tables.py` ends "all checks passed" and its output is identical to scripts/r1_tables_output.txt, before and after my edits.
2. **The evidence review's resolutions (0.2), against the sources.**
   - M1: Amazon's caveat now reads as S02 line 99 gives it ("cannot verify the outcomes the agents reported, but the records show what the actors were pursuing") in the In short, Answer, C025, C046, links.csv S02 L1 to L3 and the checkpoint. No "records Amazon cannot verify" wording remains. Holds.
   - M2: the control sentence is scoped to the attack campaigns, with StepSecurity's relays of WorkOS (S07 line 162; "A researcher's ARTEX agent", line 148) and GitGuardian ("decided by itself", line 175) as exceptions; C129's passage, locator, window (25 to 30 October, line 148) and limitation are faithful. "Attack campaigns" rather than "criminal campaigns" is right, since S07 line 156 names a state-aligned group. Holds.
   - M3: "intended" and "directed" are gone from the In short and proposed line; 0.3 then replaced the 0.2 wording with "the attackers' instructions, captured by Amazon's sensors, show people set the agents' goals and limits", which S02 line 95 supports ("Threat actors instructed ARTEX agents through standing instruction prompts that set the mission objectives, targeting rules, and operational constraints"). Holds.
   - M4: L4 and C091 now say neither publisher says what its decoy returned; S02 lines 91 and 98 and S06 lines 18 and 20 say nothing about it. Holds.
   - M5: amendment 1 is dated, says it was made after the baseline's outcomes were seen and before any prospective read, and panel.json now has six endpoints with an "amended" field; the header, Method 7, Limits and both checkpoints disclose it. Holds.
   - S1 (the reseller hedge: S04 line 230 "likely bought", line 271 "bought"; S01 line 326 only labels a domain; S07 line 132 "from resellers"), S2 (clause dropped), S3 (S02 lines 92, 93 and 111), S4, S5 (S02 line 95, moderate confidence), S6, S7 and S8 hold as written, with the small exceptions under "Still to fix" below. The optional items O1 to O8 hold.
3. **The reader review's resolutions (0.3 and the draft).** Point 1 (a human-run operation filed as AI sustaining itself): the draft now says the operation was run by people; Amazon's own words support that (S02 lines 95, 100 "how threat actors are organizing", 102 "threat actors used AI agents"), and the brief says a self-sustaining loop does not establish independence from people. But the new line-80 replacement dropped "outside a test" (finding 1). Point 2 (Amazon more confident than the texts said): done on the study page, the investigation paragraph and programme.md, but not in the This week line (finding 2). Point 3 (the reseller alternative): added, but the study page sentence misdescribed it (finding 3). Readability points and the revised round 2 order are taken, and the record's Next and the checkpoint agree on the order.
4. **Absolutes on the public surfaces,** each against the six-document corpus of 17 November and, for the investigation page, against what the page itself says has been read. "Only Amazon describes that loop for ARTEX" holds: SANS (S06) describes a similar loop but not for ARTEX. "Neither confirm nor contradict" and "nothing confirms or contradicts" hold: links.csv codes the FBI, Microsoft, Censys and StepSecurity unknown on all six links, none contradicted. "Every step of it rests on the attackers' own agent records" holds at public-surface certainty: all six Amazon links are coded claimed, resting on agent records plus Amazon's reading, with the captured instructions bearing on intent only. "Nothing outside those records yet shows it worked" needed the corpus scope (finding 4). The draft's "no report read so far ... apart from the people running it" failed (finding 1). The programme line's "only Amazon's report" lacked its scope (finding 5). site/learned.md line 34 stays true, as the draft says: SANS says its data show no self-replicating system (S06 line 43), and the WorkOS agent acted outside its test without copying itself.
5. **Consistency.** After my edits, the draft's study page opening is identical to the record's In short (checked by script), both investigation paragraphs appear verbatim in the record's Next, and the round 1 checkpoint, the Answer and the draft say the same thing at the same certainty: inconclusive, one origin, outcomes Amazon says it can't verify, people set the goals and limits, a relayed reseller finding in another campaign. Before my edits, the record called itself "Unreviewed" in its Answer and Findings while the draft labelled it a "Reviewed interim record" (finding 6).
6. **Keeper boundary.** Nothing in the record, checkpoint or draft says in Lighthouse's voice that harm is happening now or that a named system is compromised. Amazon's, the FBI's and StepSecurity's reports of harm and compromise are attributed with what they rest on. The draft names no victim.
7. **Writing rules.** No em or en dashes in the three files; British spelling; no internal codes in the draft's public texts.

## What I found, and what I changed

**Finding 1 (must-fix, fixed). The line-80 replacement had become false.** The draft read: "No report read so far describes AI activity sustaining or spreading itself apart from the people running it." The line it replaces said "outside a test". On the same investigation page, line 68 says labs "have published evaluations of models copying themselves in controlled settings", and the lab-capability strand (line 77) covers exactly that, so reports read through the sweep do describe AI spreading itself, in a test. Changed in notes/artex/r1-public-draft.md, section 2:
- Old: "No report read so far describes AI activity sustaining or spreading itself apart from the people running it."
- New: "No report read so far describes AI activity sustaining or spreading itself outside a test and apart from the people running it."

The strands sentence ("nothing below is evidence of AI activity sustaining or spreading itself apart from the people running it") I left as it is: nothing below it on the page is evidence of lab self-copying (the lab strand is "Not measured"), so it stays true.

**Finding 2 (must-fix, fixed). The reader review's point 2 had not reached the This week line.** It still said Amazon "can't verify what they claim", the widening R-0088 named. The resolution note says This week was changed; it had been changed for the first half only. Draft, section 4:
- Old: "but its evidence is the agents' own records, and it says it can't verify what they claim."
- New: "but its evidence is the agents' own records, and it says it can't verify the outcomes they report."

**Finding 3 (should-fix, fixed). The reseller clause misdescribed its source.** The study page opening and the record's In short said "one, about a different campaign, says its attackers probably bought their AI computing from a reseller". None of the reports is about a different campaign: Censys's post is about ARTEX exposure and relays CrowdStrike's case (S04 line 230), and the FBI and StepSecurity also relay it (S01 line 326, S07 line 132). Changed in LH055.md (In short) and the draft (section 1):
- Old: "one, about a different campaign, says its attackers probably bought their AI computing from a reseller."
- New: "one of them relays a finding that, in a different campaign, the attacker probably bought its AI computing from a reseller."

**Finding 4 (should-fix, fixed). The closing absolute lacked its scope.** In LH055.md (In short) and the draft (section 1):
- Old: "but nothing outside those records yet shows it worked."
- New: "but nothing we've read outside those records yet shows it worked."

Amazon says it notified AWS customers after assessing activity referencing them (S02 line 92), which C047 rightly says leaves open evidence that isn't public, so the scope matters.

**Finding 5 (should-fix, fixed). The programme.md line's "only" and one misplaced scope.** Draft, section 3:
- Old: "Round 1, reviewed interim record (17 November): only Amazon's report describes the credential-to-compute loop for ARTEX;"
- New: "Round 1, reviewed interim record (17 November): of the six reports read that day, only Amazon's describes the credential-to-compute loop for ARTEX;"
- Old: "Round 2 looks first for evidence outside the agents' records for Amazon's campaign (Amazon on"
- New: "Round 2 looks first for evidence outside the agents' records (Amazon on"

Reason for the second: the list that follows includes Check Point and Microsoft's 5 November report, which the record's Next says can't confirm or contradict Amazon's campaign; the line already says new evidence is coded by campaign.

**Finding 6 (should-fix, fixed). Stale review-status lines, inconsistent with the draft's "Reviewed interim record".** In LH055.md:
- Header status. Old: "resolved in 0.2 and 0.3, awaiting the one fresh recheck of the resolutions (LH055-r1-recheck)". New: "resolved in 0.2 and 0.3, and the resolutions rechecked once by a fresh agent (notes/R-0089-lh055-r1-recheck.md, which lists its own small changes); not yet released".
- Header authors: appended "; version 0.3 revised for the same driver, resolving the reader-and-inference review notes/R-0088-lh055-r1-reader.md".
- In short, last sentence. Old: "Next, a fresh reader rechecks the changes made after both reviews, then a targeted search looks for evidence outside the agents' records." New: "Next, a targeted search looks for evidence outside the agents' records, starting with how Amazon's own sensors came to be used, while dated re-reads of the reports run to 1 December." The same sentence is added to the draft's section 1, which is meant to be the record's In short and lacked a "what happens next" sentence.
- Answer, first line. Old: "Unreviewed: the evidence review's must-fixes are resolved in version 0.2 but not yet rechecked." New: "Reviewed, not released: the evidence review's points are resolved in version 0.2 and the reader-and-inference review's in 0.3, and a fresh agent has rechecked those resolutions."
- Findings, first line. Old: "All findings are unreviewed." New: "The findings have been through the evidence review, with its resolutions rechecked; nothing here is independently confirmed."
- Limits, first bullet. Old: "**Reviewed once, not cleared.** The evidence review of version 0.1 (notes/R-0087-lh055-r1-evidence.md) found five things that had to change; version 0.2 makes those changes, which a fresh agent has not yet rechecked, and the reader-and-inference review is still to come." New: "**Reviewed, not independently confirmed.** The evidence review of version 0.1 (notes/R-0087-lh055-r1-evidence.md) found five things that had to change, and the reader-and-inference review of version 0.2 (notes/R-0088-lh055-r1-reader.md) found three material wording problems; versions 0.2 and 0.3 make those changes, and a fresh agent rechecked them once (notes/R-0089-lh055-r1-recheck.md)." The rest of the bullet is unchanged.
- Next, Reviews bullet. Old: "The evidence review of version 0.1 (R-0087) was not cleared; version 0.2 resolves its must-fix items. A fresh agent reads these changes once, then the reader-and-inference review, by 20 November. No public finding before they clear." New: "The evidence review (R-0087) and the reader-and-inference review (R-0088) are resolved in versions 0.2 and 0.3, and the one fresh recheck of those resolutions is in notes/R-0089-lh055-r1-recheck.md. No public finding before release."
- Corrections, version 0.3 entry. Old: "since Amazon says threat actors organised it and steered the agents (S02 lines 93 and 95)". New: "since Amazon says threat actors ran it and set the agents' objectives, targeting rules and constraints (S02 lines 93, 95, 100 and 102)" (line 93 is passive, "organized as a self-sustaining operation"; the actors are named at lines 95, 100 and 102, and "steered" is not Amazon's word). Appended after "Earlier edition: version 0.2 at commit da43d12.": a sentence saying this recheck made small changes within 0.3, listed in this note, with no count, claim or link status changed.

In studies/LH055/checkpoints/2026-11-17-round1.md:
- In short. Old: "Both reviews' points are resolved in record 0.3, awaiting one fresh recheck, the answer is inconclusive". New: "Both reviews' points are resolved in record 0.3 and a fresh agent has rechecked them once; the answer is inconclusive".
- Record line. Old: "version 0.2 (unreviewed round 1 record; evidence review (R-0087) must-fixes resolved, not yet rechecked)". New: "version 0.3 (round 1 record; evidence review (R-0087) and reader-and-inference review (R-0088) resolved in 0.2 and 0.3, and rechecked once (R-0089); not released)". And "Version 0.2 resolves [the evidence review](...) of version 0.1 (commit cb6fab5);" now continues "and version 0.3 [the reader-and-inference review](../../../notes/R-0088-lh055-r1-reader.md);".
- Limits carried forward. Old: "Codings by one writer, reviewed once for evidence (not cleared at 0.1; resolved in 0.2, not yet rechecked);" New: "Codings by one writer, reviewed for evidence and for reader inference (not cleared at 0.1; resolved in 0.2 and 0.3, and rechecked once), which is review, not independent confirmation;".

**Finding 7 (readability, fixed), in the investigation paragraphs** (draft section 2 and the copy in the record's Next):
- Old: "**Reviewed interim record, 17 November 2026.**" New: "**Reviewed interim record (an evidence review, a reader-and-inference review and a recheck), 17 November 2026.**", matching how the page's other lines say how far each is checked.
- Old: "using AI agents it attributes to ARTEX, an open-source AI hacking tool, with moderate confidence, ran". New: "using AI agents it attributes with moderate confidence to ARTEX, an open-source AI hacking tool, ran".
- Old: "Check Point's report on ARTEX operators hit a rate limit on the day;". New: "Our read of Check Point's report on ARTEX campaigns hit a rate limit on the day;" (the wall met our read, not the report; and what the unread report covers is known only from its title, "Inside ARTEX Cybercrime Campaigns").

No count, claim, link status, quotation or derived figure changed; the replay output is unchanged.

## Still to fix (not blocking release)

These lie in files this recheck was not asked to edit, and none touches a public sentence.

- claims.csv C025, limitation: "alongside that caveat. no count of keys" needs a capital ("No count").
- links.csv S02 L2 ("demonstrated credential validity or access"), reason: still says "the instructed grading scheme", which the evidence review's S4 resolution removed from the record's L2 ("one operation's grading scheme"), and lacks punctuation: "no count of validated credentials is given Amazon says it cannot verify". Suggested: "Validation is described in agent records and one operation's grading scheme defines a confirmed working call (L2), but no count of validated credentials is given, and Amazon says it cannot verify the outcomes the agents reported."
- panel.json's "amended" field mentions only P07's removal; P06's reason was also reworded after the lock. The record's Limits discloses it, so this is optional.
- Optional, for the publication stage: the investigation page's In short keeps "There is no reviewed finding yet" beside a "Reviewed interim record". That follows the page's existing usage (LH041 and LH042 are reviewed records too), but "no released finding", as AGENTS.md's "Where things stand" puts it, would read more plainly.
- At release, the driving session sets the record's status line and the Answer's first words to say it is released, as usual.

## Verdict

**Cleared for release at version 0.3 as left by this recheck** (record, round 1 checkpoint and notes/artex/r1-public-draft.md as they now stand). The two must-fix problems found (the line-80 replacement and the This week caveat) are fixed above; the remaining items are small record typos and an optional field, none of which changes what a reader is told.
