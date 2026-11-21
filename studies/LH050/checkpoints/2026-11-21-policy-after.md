# Post-conference policy read, 21 November 2026

**In short.** The day after the arms-control conference in Geneva was due to close, we read the UN's conference page and the official texts it lists. The page still shows no adopted final document, no adopted declaration and no decision on what the expert group on autonomous weapons does next. In the latest draft we could read, from 20 November, every slot about autonomous weapons is still an empty placeholder, and the draft says the states couldn't agree an agenda or rules of procedure. What we have on autonomous weapons is proposals and positions, not agreed wording. This is unreviewed working material, not a finding; a final check on 27 November looks for the adopted text.

Row LH050-policy-after, run id 2026-11-21T141050Z-anthropic-watch, protocol 0.1 with Amendment 1 and the operational scheduling amendment of 14 November. Read label `2026-11-21T1414Z`; reads from 14:14:39Z to 14:16:28Z UTC on 21 November 2026, inside the 21 to 23 November window, and after the conference's scheduled close on 20 November. Collected by Claude Opus (Anthropic, model id claude-opus-5-5) under Claude Code, as a subagent; provider set to `anthropic` for the robots gate. Time spent: about 12 minutes of agent time (about 14:13Z to 14:25Z, including writing). Cost: unknown (not measured by this subagent; unknown is not zero).

## Was the preparation in place?

Yes. The row's note says not to collect before the commissioning preparation lands. The brief (protocol 0.1, written 12 November) is on `origin/main` (in this shallow clone the earliest commit holding it, 0cdcbfa, is an ancestor of `origin/main`), the push hold was lifted (brief, Protocol and authority), and collection under it has run since 13 November (baseline, panel lock, the 19 November weekly read). The brief fixes this read ("Post-conference official-policy read: 21 to 23 November") and its purpose ("what was proposed, what wording was agreed, and what future work was committed"). The documents to read come from the earlier checkpoints: the baseline said to recheck PA-S16 "for the adopted declaration and the GGE decision"; the panel lock left the fixed PDFs (PA-S19, PA-S20) and "any adopted text" to these reads; and the 19 November read said this read should retain the drafts and working papers listed on PA-S16, subject to the robots gate for docs-library.unoda.org.

## Accounting

- Bound. The brief sets no number for this read. This read set its own: at most 12 document reads, the weekly read's cap, each one reference step from PA-S16, with one connection-failure retry and no retry around a wall. 12 were made. The baseline's 30-document bound is read as the baseline's alone (it stays at 29 attempted).
- Selection. From PA-S16's Documents list on 21 November: the four draft outcome texts (PA-S33 to S36) and the six working papers listed there from States, groups of States and international organisations (PA-S37 to S42). Left out: the NGO and youth working papers (WP.4, WP.5, WP.8), the provisional agendas and programmes of the main committees, and the budget and cost papers CCW/CONF.VII/1 to 10, which link to docs.un.org shells over a document route Lighthouse can't read. The 12th read (PA-S43) was the docs.un.org page for CCW/CONF.VII/11, the symbol the drafts give the final document. Selection was made with the 21 November page open and before any draft was read.
- Access. All 12 requests returned HTTP 200; no walls. robots.txt: meetings.unoda.org allowed (`*` group); docs-library.unoda.org's robots.txt answered 403, which the gate treats as no rules, as at the baseline reads LH050-R019 and R020; docs.un.org allowed. documents.un.org was gate-checked only, at 14:16:37Z, and is disallowed (`Disallow: /doc` for `*`); nothing was requested from it. Two email addresses were redacted from PA-S16; none from the others.
- Retained under `data/2026-11-21T1414Z/`: `bodies/` (12 files), `robots/` (12 decisions and the gate-only record for documents.un.org), `fetch_log.jsonl` (received and retained hashes), and `collector.py`, the 19 November collector adapted to take a list of URLs. Ledgers: reads LH050-R048 to R059; sources PA-S33 to S43; claims LH050-C079 to C093. No events were added: no policy event (adoption, decision) is established by what was read.

## What the page shows (observation)

PA-S16, compared with the 19 November copy (LH050-R044). Added: CRP.1/Rev.2, "Draft final document (as circulated on 20 November 2026)"; working papers WP.5 (Maat for Peace, Development and Human Rights), WP.8 (IHLYI) and WP.18 (Uganda on behalf of the Non-Aligned Movement and other States); Friday webcast links; a longer UNIDIR side-event description. Not listed: an adopted final document (the drafts name it CCW/CONF.VII/11), an adopted final declaration, or any decision on the expert group's mandate. The overview still says the conference "will take place" from 16 to 20 November. Absence from the page a day after the close isn't evidence that nothing was adopted (claim C079).

## The texts, kept apart

**Agreed wording.** None read. No source read on 21 November contains text that it says was adopted. Each draft is written ahead of events, in the past tense ("At its final plenary meeting, on 20 November 2026, the Conference adopted its Final Document, as contained in CCW/CONF.VII/CRP.1/Rev.2, [as orally amended,]"; PA-S35, p.4 para 30). A draft's past tense is not an adoption (C084).

**The drafts (official working texts, not agreed).**

- CRP.1, 13 November (PA-S33): pre-written as if the conference "adopted its Agenda" and "adopted the Rules of Procedure" (p.2 paras 14, 15) (C080).
- CRP.1/Rev.1, 19 November (PA-S34): replaces that with "The High Contracting Parties were not able to adopt the agenda ... and were not able to adopt the rules of procedure ... as no consensus on this matter was reached" (p.2 para 16) (C081).
- CRP.1/Rev.2, 20 November (PA-S35): adds that "the preamble and declaratory part of the Final Declaration, as contained in CCW/CONF.VII/MC.I/CRP.1, were not adopted and the Conference was not in a position to conduct a formal review of the scope and operation of the Convention and the Protocols annexed thereto" (p.2 para 16) (C082). This is the draft's own account; we have no meeting record to check it against.
- Autonomous weapons in Rev.2: Decision 1 is "[LAWS]" (p.6 para 47); the 2027 meetings list has "iii.[Placeholder LAWS]" (para 54); Article 8 "Welcomes the work of the open-ended Group of Governmental Experts ... [LAWS]" (p.8 para 73); the 2027 agenda's item 8 is "[Placeholder LAWS]" (p.14). The same placeholders are in Rev.1 and in the Main Committee I draft declaration of 13 November (PA-S36, p.4 para 17 "[Placeholder on LAWS]", p.5 para 34 "[LAWS]"), and they match the pre-conference draft (PA-S19, claim C052) (C083, C085). Rev.2 also pre-writes the adoption of the expert group's 2027 cost estimates "in accordance with Decision 1", while Decision 1 is empty (p.3 para 26) (C084).

**Proposals and positions (not agreed).**

- Seven States (Austria, Belgium, Brazil, Ireland, New Zealand, Panama, Mexico), WP.7 (PA-S39): decision language for a new expert group to "negotiate a new Protocol to the Convention on lethal autonomous weapon systems", meeting in 2027 for "3 dedicated sessions and a total of 25 days" and reporting "a draft Protocol" to the 2027 meeting (p.3 paras 26 to 27; p.4 paras 30 to 31); human control as a negotiating aim (p.3 para 18) (C086, C087). It differs from the unattributed mandate proposal posted before the conference (PA-S20, C054: 15 days a year, a 2028 report).
- ICRC, WP.9 (PA-S40): urges a one-year negotiating mandate, with the draft protocol for adoption by the 2027 meeting; says the expert group "was unable to find consensus on the substance of prohibitions or restrictions" (p.9 paras 46 to 48) (C088).
- Holy See, WP.10 (PA-S41): a legally binding agreement and, meanwhile, "a moratorium on the development and use of LAWS" (p.5 para 21) (C089).
- Non-Aligned Movement and other States, WP.18 (PA-S42): "an urgent need to pursue a legally binding instrument", "a strengthened mandate", and agreement "by consensus on the future mandate"; weapons with autonomous functions "must always remain under the direct control and supervision of humans" (pp.1 to 2 paras 7, 9, 10) (C090).
- Austria, WP.3 (PA-S37): a recurring agenda item on science, technology and new means of warfare; no LAWS mandate proposal (C091). The Russian Federation's WP.6 (PA-S38) concerns allegations against Ukraine and has no passage on autonomous weapons found by text search; kept as that State's account and outside this comparison (C092).

**Future commitments.** None on autonomous weapons in any text read: the drafts' LAWS decision and 2027 meeting slots are placeholders. The drafts' other proposed decisions (for example, Decision 5's "Emerging Issues" agenda item for 2027, PA-S35 p.6 para 52) are draft wording, not commitments, until adopted text is read.

## Gaps

- The adopted final document, if any, is not read: not listed on PA-S16 at 14:14:39Z; its symbol's docs.un.org page (PA-S43) is a language shell with no text or date, which doesn't show the document exists; the document route on documents.un.org is disallowed by robots.txt (C093).
- Whether the conference adopted anything on 20 November, and what it decided on the expert group, is not established by any source read. No press release, meeting summary or webcast was read; the UN Geneva release on the panel (PA-S15) is read weekly, next on 26 November.
- CCW/CONF.VII/7 (the expert group's 2027 cost estimates), WP.1 and WP.2 sit behind the same disallowed document route, as at baseline.
- A full text comparison of the Main Committee I draft (PA-S36) with the pre-conference draft (PA-S19) was not made; only the LAWS placeholders were compared.
- The NGO and youth working papers were not read; no claim is made about them.

## For Research

Nothing here changes a public account. The investigation page's "no deployment or harm finding has been made" still holds. If a later summary says the conference agreed anything on autonomous weapons, it needs adopted text; none has been read. The policy comparison is so far incomplete: proposals and draft wording on one side, no agreed wording on the other.

## Next

The final document check on 27 November (row LH050-policy-final) rereads PA-S16 for an adopted final document or decision and reads it if it is posted on a permitted route, then closes the comparison as complete or incomplete. The weekly panel read on 26 November rereads PA-S16 and PA-S15 as panel endpoints.
