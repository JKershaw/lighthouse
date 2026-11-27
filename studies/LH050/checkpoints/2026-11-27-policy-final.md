# Final official-policy check, 27 November 2026

**In short.** We read the final document of the UN conference on conventional weapons that met in Geneva from 16 to 20 November. The conference's page lists it as "as adopted". On autonomous weapons, it keeps the expert group going for another review cycle. The group is to draw up "by consensus" an instrument "without prejudging its nature", meeting 10 days a year and reporting to the 2028 meeting, with a recommendation on whether the instrument should be a binding protocol. That's less than the proposals we read: those asked for negotiations on a new protocol, more meeting days and an earlier date. This closes the before-and-after comparison of official texts as complete, with the limits below. It's unreviewed working material, not a finding.

Row LH050-policy-final, run id 2026-11-27T141100Z-anthropic-watch, protocol 0.1 with Amendment 1 and the operational scheduling amendment of 14 November. Read label `2026-11-27T1415Z`; two reads, at 14:14:40Z and 14:14:56Z UTC on 27 November 2026, inside the row's one-day window. Collected by Claude Opus (Anthropic, model id claude-opus-5-5) under Claude Code, as a subagent; provider set to `anthropic`; both reads were one-off reads (`access='oneoff'`, the keeper's decision of 21 November 2026). Time spent: about 11 minutes of agent time (about 14:12Z to 14:23Z, including the Assembly housekeeping below and writing). Cost: unknown (not measured by this subagent; unknown is not zero).

## What the brief asks of this check

The brief fixes "One final document check on 27 November, then close the policy comparison as complete or incomplete", and the comparison as "the accessible official documents before and after the conference: what was proposed, what wording was agreed, and what future work was committed. An appeal for negotiations is not a treaty. This is a comparison of texts, not proof of implementation." It doesn't define "complete" beyond that. This check reads "complete" as each of those three parts resting on a readable official text, and "incomplete" as one of them still missing. The brief also says there's no automatic renewal of collection, so this row doesn't extend the policy reads.

## Accounting

- Reads: 2, one GET each, no retries, no walls. PA-S16 (the conference page, LH050-R068) and PA-S44, the PDF it lists as "CCW/CONF.VII/CRP.1/Rev.3 - Final document - as adopted" (LH050-R069), one reference step from PA-S16. The bound was the brief's (one reference step from an admitted source, inside the 12-read cap the 21 November read set itself).
- Robots: meetings.unoda.org allowed (`*` group, one-off). docs-library.unoda.org's robots.txt answered 403, which the gate treats as no rules, as at every earlier read of that host (LH050-R019, R020, R049 to R058); `keep_decision` said the body may be kept. Decisions in `data/2026-11-27T1415Z/robots/`.
- Kept under `data/2026-11-27T1415Z/`: `bodies/S16_unoda.html` (2 email addresses redacted), `bodies/S44_crp1_rev3.pdf` (none), `fetch_log.jsonl` with received and kept hashes, and `collector.py` (the 21 November collector with `access='oneoff'` added to the gate check, the fetch and the keep decision).
- Hashes: PA-S16 received SHA-256 38d1f446...8159, byte-identical to the 26 November read (LH050-R064), so the page hasn't changed since then. PA-S44 received SHA-256 725afe2f7f9f7aa2791f008deccae19bb4ab91cc9bf8cda89311595be5ce6ffe, 292,993 bytes, 19 pages, dated 20 November 2026 on its face, PDF created 23 November 2026 08:25 UTC.
- Ledgers: reads LH050-R068 and R069; source PA-S44; claims LH050-C094 to C102; events LH050-E011 and E012 (the first policy events after the conference, each "as the posted final document records it").
- Not requested: CCW/CONF.VII/11, the symbol the document says it "will be issued" under; its document route on documents.un.org is disallowed by robots.txt (PA-S43, C093). The elements document CCW/GGE.1/2026/3 and the cost estimates CCW/CONF.VII/7, which the decisions cite, weren't read either: neither is listed on PA-S16, and finding them would be a new search this row doesn't authorise.

These are counts of readings for collection accounting, not counts of anything about weapons.

## What the adopted text says (observation)

All from PA-S44, read 27 November 2026 at 14:14:56Z, quoted with paragraph numbers. It's the issuing body's own account. There's no meeting record or webcast here to check it against.

**That it was adopted.** "At its final plenary meeting, on 20 November 2026, the Conference adopted its Final Document, as contained in CCW/CONF.VII/CRP.1/Rev.3, as orally amended, which will be issued as document CCW/CONF.VII/11" (para 31), and it "adopted its Final Declaration, as contained in the Final Document, Part II" (para 26) (C095). The page lists only this text as adopted (C094). Whether the posted PDF already carries the oral amendments isn't stated.

**What wasn't adopted.** As in the 20 November draft, the agenda and rules of procedure weren't adopted "as no consensus on this matter was reached" (para 16). New in this version: the preamble and declaratory part of the Final Declaration weren't adopted "as no consensus was reached", and the Conference "was not in a position to conduct a formal review of the scope and operation of the Convention and the Protocols annexed thereto, but was in a position to adopt section III of the Final Declaration" (para 17) (C096). Section III is headed "Review". We record both sentences as written and don't try to reconcile them.

**Autonomous weapons: the expert group's mandate (Decision 1).**

- The Conference "decides to endorse the set of elements of an instrument, without prejudging its nature, and other possible measures, to address emerging technologies in the area of LAWS", adopted by the expert group in 2026, "as contained in document CCW/GGE.1/2026/3" (para 48) (C097). We haven't read those elements.
- The expert group "is to continue, to strengthen the Convention" (para 49). "The Group is to elaborate, by consensus, an instrument, without prejudging its nature, that specifies international humanitarian law, including principles and requirements, applicable to lethal autonomous weapon systems, and its implementation, and other possible measures." Its report "will also make a recommendation on the legal nature and specific form of the instrument, including whether the High Contracting Parties should adopt the instrument as a binding protocol" (para 50) (C098).
- "The Group shall conduct its work and adopt its report by consensus and shall submit its report to the 2028 Meeting of High Contracting Parties"; its Chair updates the 2027 Meeting; it "shall meet for 10 days in Geneva each year" (para 54) (C099).
- 2027 sessions: "1-5 March 2027, and 30 August-3 September 2027", with the group's cost estimates (CCW/CONF.VII/7) adopted (para 61 (iii); para 27) (C100).
- Elsewhere: Article 8 "Welcomes the work of the open-ended Group of Governmental Experts related to emerging technologies in the area of lethal autonomous weapon systems" (para 80), now with no bracket after it. Item 8 of the 2027 Meeting's provisional agenda is an "Update by the Chair of the Group of Governmental Experts on emerging technologies in the area of lethal autonomous weapons systems (GGE on LAWS)" (Annex III). Para 44 acknowledges the support unit's workload "including in support of the GGE on LAWS" (C101).

**What it doesn't contain.** A text search of the whole document, made 27 November, finds no "negotiate" (the only match is an NGO's name), "moratorium", "human control", "human judgement" or "legally binding". The word "binding" appears once, in para 50's "binding protocol" as an option the report is to make a recommendation on. There's no deadline for adopting any instrument. The 2028 report is a reporting date, nothing more (C098, C099).

## The comparison, closed

| | Before and during the conference (proposed) | Adopted (as the posted final document records it) |
|---|---|---|
| Drafts | Every LAWS slot a placeholder in the pre-conference draft (C052), the Main Committee I draft (C085) and the drafts up to 20 November (C083) | Placeholders filled: Decision 1 (C097, C098, C099), the 2027 sessions (C100), Article 8 and the 2027 agenda (C101) |
| Task | Unattributed posted proposal: "negotiate a new Protocol" (C054). Seven States (WP.7): a new group to "negotiate a new Protocol" (C086). ICRC: "a mandate to negotiate a new Protocol" (C088). Holy See: a legally binding agreement and a moratorium (C089). NAM and other States: "a legally binding instrument" and a "strengthened mandate" agreed by consensus (C090) | "elaborate, by consensus, an instrument, without prejudging its nature", plus a recommendation on whether to adopt it "as a binding protocol" (C098) |
| Meeting time | Posted proposal: 15 days a year (C054). WP.7: 25 days in 2027 in 3 sessions (C086) | 10 days a year; two five-day sessions in 2027 (C099, C100) |
| Report | Posted proposal: report with a draft Protocol to the 2028 Meeting (C054). WP.7 and ICRC: a draft protocol to the 2027 Meeting (C086, C088) | A report to the 2028 Meeting; no draft protocol required (C099) |
| Human control | WP.7: requirements on human control as a negotiating aim (C087). NAM: weapons must stay under "direct control and supervision of humans" (C090) | Not mentioned (text search) |

Derived reading (interpretation, made after reading, one comparison): the adopted mandate keeps the expert group going on a consensus basis and leaves the instrument's legal form open. It doesn't adopt the negotiating mandate, meeting time or 2027 date in any of the proposals we read. In days and in the instrument's form, it's narrower than the unattributed posted proposal, which itself asked for less than the seven States and the ICRC. An appeal for negotiations isn't a treaty, and neither is this mandate. Nothing here says anything about how any state builds or uses a weapon.

**Closed as complete.** Each of the brief's three parts now rests on a readable official text. What was proposed: drafts and working papers, read on 13 and 21 November. What wording was agreed: the posted final document labelled as adopted, read today. What future work was committed: Decision 1 and Decision 5 in that document. The limits stay with it:

1. The text read is CRP.1/Rev.3 as posted. The document says it was adopted "as orally amended" and will be issued as CCW/CONF.VII/11. That issued text sits behind a route robots.txt disallows, so differences between the two are unknown.
2. The endorsed elements (CCW/GGE.1/2026/3) and the cost estimates (CCW/CONF.VII/7) are cited, not read, so what the endorsement covers in substance is unknown to this record.
3. The adoption, and what parts were or weren't adopted (paras 16, 17, 26), are the document's own account. No meeting record, press release after the close, or webcast was read. The UN Geneva release on the panel (PA-S15) is pre-conference and was unchanged on 26 November.
4. The working papers listed after 21 November (WP.11 to WP.42, among them WP.16, submitted by 41 States and the European Union) weren't read. So the "proposed" side covers the drafts and the papers listed by 21 November, not every position.

## Assembly's retained copies, replaced (housekeeping)

The 26 November handover asked for LH050's kept copies of Assembly's page (PA-S26) from 13 and 19 November to be replaced, since the keep check now refuses them (assemblymag.com's robots.txt refuses meta-externalagent, an AI-training crawler, at the path; `keep_decision` confirmed it again today). Done under the keeper's decision of 21 November. `scripts/derive_assembly.py` wrote `S26_assemblymag.derived.json` beside each body. Each holds the URL, read time, status, received and kept hashes, title, standfirst, dates, the short passages claims C022, C031 and C032 quote (each checked present) and a hash of the article's visible text, the same for both reads. The two bodies were then deleted. reads.csv rows R029 and R042 now point to the derived files. case_matrix.py names the derived file for R029, and the rebuilt case_matrix.csv differs only in the retained-path column of the 8 rows citing R029. The R-0074 review script's output is unchanged. Details in [data/REMOVED.md](../data/REMOVED.md). No claim, cell or conclusion changed. Later weekly reads can compare Assembly's article text against the stored hash by the same rule.

## For Research

Nothing here is reviewed, and nothing should go public until it is. What would change once it is:

1. **The 21 November checkpoint's opening** says the page "still shows no adopted final document, no adopted declaration and no decision on what the expert group on autonomous weapons does next". That was true at 14:14Z on 21 November. It is now superseded: the page lists an adopted final document (first seen 26 November) whose Decision 1 sets the expert group's mandate. A dated "Later evidence" line there, or in LH050.md's Corrections, would keep a reader from taking it as the outcome.
2. **AGENTS.md's orientation line** for the physical-authority investigation ("found no adopted text on autonomous weapons on the conference's page, and on 26 November the page listed a 'Final document - as adopted', not yet read") now needs updating: the final document has been read, and it continues the expert group with a consensus mandate to elaborate an instrument of open nature, 10 days a year, reporting to 2028. The comparison is closed as complete with the four limits above. That's the driver's or Editor's edit, after review.
3. **LH050.md** still says the comparison "waits for the reads of 21 to 23 and 27 November" (Official policy before the conference; Next, Policy) and lists "the post-conference policy comparison" as not filled. Those lines change at the next record update. Its Answer isn't touched here.
4. **The investigation page** doesn't mention the conference outcome. If it gains a line, the line should say "as the posted final document records it", give the mandate's terms rather than a characterisation such as "failed" or "agreed to negotiate" (it's neither), and carry limits 1 and 2.
5. **A possible bounded follow-up, not taken:** reading CCW/GGE.1/2026/3 (the endorsed elements) would say what the adopted endorsement covers. It isn't listed on PA-S16 and needs a new route, so it would need a dated amendment. The brief allows no automatic extension. Whether it's worth one inside the pilot's envelope is Research's call.
6. Any public line about what states "agreed" on autonomous weapons should quote the mandate's own words. It's the issuing body's position, not evidence of implementation.

## Next

No further policy reads are scheduled. This row closes the comparison, and the brief allows no automatic extension. The weekly panel continues: 3 December (LH050-watch-2026-12-03), then 10, 17 and 24 December. PA-S16 stays a panel endpoint (P05), so a later posting of CCW/CONF.VII/11 or a revised final document would be seen there and recorded as a panel change.
