title: Recheck of the resolution edits to the essay "When the machine works as intended"
kind: review
row: LH050-essay-recheck
study: LH050
date: 2026-11-28
reviewer: Claude Opus 5.5 (Anthropic, model id claude-opus-5-5), under Claude Code, as a fresh subagent with no part in drafting or resolving
repository HEAD as received: 4dbc9b67dc84f28f1f3418be4b9850cace2e3188
essay SHA-256 as received: 395a60dea609698fa929de988e9cb2d6fbc05b0999ef765ecfc163ac63224839
essay SHA-256 as left: b60720aa2a043ec1bddc274e338f11ce6bec5f62b63993b84d3cdd3829e89ca2
verdict: cleared, after five small edits made here

# Recheck of the resolution edits to the essay "When the machine works as intended"

**In short.** We read once every passage the driving session changed to settle the figure-and-citation check (R-0175) and the reader-and-inference review (R-0176), against the retained final document, the study's record, its panel and the investigation page. All eight review points those resolutions took on are settled and labelled correctly. Two resolutions left a small overstatement or an unsettled part, and one new sentence went further than the record. We fixed those five places directly. Nothing further must be fixed for release.

## What was checked

Changed passages from `git diff 6cb4ab0 HEAD -- essays/when-the-machine-works-as-intended.md`, each read against:

- **The commissioning essay's opening** (notes/physical-authority/original-essay.md): it starts with the airport, says "this week" of the story, and turns to the Financial Times report in its fifth paragraph. "In the week it was written" holds; "set out from" still read as if it began there (R-0175 should-consider 1). Changed, see 1.
- **TechCentral** (retained body of PA-S24, 22 December 2025): "Experts, however, caution against the assumption that using humanoid robots will automatically lead to fewer conflicts. They argue that such technology could paradoxically make military action more likely by reducing the perceived risks and consequences". The new wording gives this as TechCentral's own summary attributed to unnamed experts, and "humanoid robots" as the subject is the article's context. R-0175 must-fix 1 resolved.
- **"Reported proposal" and "Foundation's reported proposed use in Gaza"**: R-0175 must-fix 2 resolved in substance, but "the reported proposal, which we couldn't read" still reads as if the proposal were a document we tried; R-0175 had suggested "whose report". Changed, see 2.
- **"Capable of autonomous patrol"**: in the Singapore Police Force page as retained (R-0175 quote_check.out); the description is now separated from the police's phrase, and the GIBSON page's navigation description supports it. Resolved.
- **Contracts in "From the battlefield to the airport"**: The Next Web (PA-S27) gives "$24 million in government research contracts across the Army, Navy, and Air Force for feasibility testing in inspection, logistics, and weapons handling", held by the company. The resolution's "military research contracts to test whether it could do the work" attaches them to the robot and, after "factories and for war", stretches them to factory work, which no source says. Changed, see 3.
- **The conference paragraph**, against data/2026-11-27T1415Z/bodies/S44_crp1_rev3.pdf through pdftotext: paragraph 49 ("the work of the open-ended Group ... is to continue"), 50 ("to elaborate, by consensus, an instrument, without prejudging its nature, that specifies international humanitarian law, including principles and requirements, applicable to lethal autonomous weapon systems"; "binding protocol"), 54 ("meet for 10 days in Geneva each year"; "the 2028 Meeting"), 31 ("as orally amended"), all as quoted. The reading is now dated 27 November and labelled unreviewed where made (R-0175 must-fix 4 resolved); the subject of "is to continue" is the group's work (should-consider 3 resolved). The narrowed last sentence, "the decision on autonomous weapons says nothing about how any state builds or uses one", is still too broad: paragraph 50 has the group "consider the application of existing IHL to LAWS", paragraph 52 says international law should guide its work, and paragraph 48 endorses elements we haven't read. What holds is that the decision sets no rule itself. Changed, see 4.
- **"What we could find out"**: the record is now linked as checked and unpublished, and the restatement is introduced "as that record reads"; it matches the record's In short and Answer (studies/LH050/LH050.md, 0.1) and is no stronger. R-0175 must-fix 5 resolved on the essay's side.
- **The investigation page** (investigations/physical-authority.md, read only for whether it supports the essay): its new In short and "Where it stands" give the reviewed record's answer at the same certainty, with "in practice", the two unreadable cases and no readable fielded weapon, and the conference outcome as the posted document records it, labelled unreviewed, with "as orally amended" and the elements unread. The essay's "says where things stand" now holds. programme.md's line matches. R-0176 point 2 resolved.
- **The closing reading**: now called a reading, not a finding, half expected beforehand (the commissioning essay's "Military capabilities are frequently secret" and "the absence of public reporting cannot establish the absence of harm", line 271; the brief's disclosed expectation that targeting evidence would be harder to get), and says we can't tell a blind spot in public records from a limit on what we could reach. R-0175 must-fix 6 and R-0176 point 1 resolved. But the new sentence "Among the sources we could read, nothing said who decides on force or who answers for it" overstates: the essay itself quotes two reported statements of the maker's intentions on decisions in combat, coded in the record as one conflicting control cell, and the record's claim is that no cell for target selection or force authorisation *in practice* is supported; the investigation page says "in practice" too. Changed, see 5.
- **"What would test this", first bullet**: "hard to see in public" matches the rewritten reading; the record (not the investigation page) is now cited for the panel, and the record's Limits and panel.csv give eight endpoints, four trade reports and four policy pages; "an edit to one of those four articles ... it doesn't look for new reporting" matches panel.csv's purpose (correction, update or retraction of the four fixed reports). Resolved.
- **House style and labels in changed text**: British spelling, no em or en dashes (searched the file), no internal codes in prose, every claim attributed with its date; the essay cites no figure of Lighthouse's own.
- **Safety lines**: no legality determination; the ICRC's test is attributed; no Lighthouse-voice claim of harm now or of a named system compromised; Pathak and Eric Trump appear only as readable sources report them; TechCentral's experts stay unnamed.
- **Combined disclosure check** (schedule/research-safety.md): the version as left adds public reporting, official pages and treaty text at a reader's level, with no operational detail, no risky joins and nothing about exposed hosts. It clears.

## Changes made here

1. Before: "The commissioning essay set out from a news story." After: "The commissioning essay turned early to a news story." (The original begins with the airport.)
2. Before: "Whatever the merits of the reported proposal, which we couldn't read," After: "Whatever the merits of the reported proposal, whose report we couldn't read," (It was the report we couldn't read.)
3. Before: "a robot meant for factories and for war, with, by those reports, military research contracts to test whether it could do the work." After: "a robot meant for factories and for war, from a company holding, by those reports, military research contracts for feasibility testing in inspection, logistics and weapons handling." (The source's purpose for the contracts, held by the company; nothing says they cover factory work.)
4. Before: "and the decision on autonomous weapons says nothing about how any state builds or uses one." After: "and the decision on autonomous weapons doesn't itself set any rule for how a state builds or uses one." (Paragraphs 50 and 52 do speak to how IHL applies, and the endorsed elements weren't read.)
5. Before: "Among the sources we could read, nothing said who decides on force or who answers for it." After: "Among the sources we could read, nothing said who decides on force in practice or who answers for it; the nearest were the maker's reported statements of intent, which don't agree." (Matches the record and the investigation page, and the essay's own earlier section.)

None changes the argument or a figure. These changes are listed here and not sent to another reader, as AGENTS.md's step 4 asks.

## Verdict

Cleared: nothing further must be fixed for release. The release-step items R-0175 left open stay with the release step: a `published:` field, and the reader article's title as link text if that sentence is kept.
