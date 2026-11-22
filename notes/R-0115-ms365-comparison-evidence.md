# R-0115: evidence review of the Microsoft 365 outage comparison, version 0.1

**In short.** A fresh reviewer read Microsoft's post-incident report (from the same third-party copy, whose hash matched) and checked the working comparison's quotations, facts and classifications against it, the watch's rules, the gate, the retained readings and issue #54. The quotations and page references hold, the facts about the report and the baseline posts hold, and the classifications (B1 qualified, B2 confirmed, B3 qualified) are defensible under the fixed categories. One thing must be fixed before the comparison goes on: its quotation tally is miscounted, and the true count is over the 150-word bound it says it keeps.

| | |
| --- | --- |
| Reviewed | notes/microsoft-outage-report/comparison.md, version 0.1, 22 November 2026 (file as it stood at 15:20 UTC) |
| Reviewer | a Claude Code subagent on Opus 5.5 (`claude-opus-5-5`), fresh to the comparison, 22 November 2026 |
| Against | notes/microsoft-outage-report-watch.md (rules 2, 4, 5 and the categories); notes/microsoft-outage-report/gate-2026-11-22.md; readings of 14 to 22 November; issue #54 (read with the GitHub tool, body as of its update of 14 November 09:06 UTC; nothing posted) |
| Primary source read | https://www.365fanatic.com/wp-content/uploads/2026/11/postincidentreport-mo1550821.pdf , one-off read for this review at 15:21:37 UTC on 22 November 2026 through scripts/lh_fetch.py (`access='oneoff'`, `check_redirects=True`, `LIGHTHOUSE_PROVIDER=anthropic`): HTTP 200, application/pdf, Last-Modified Sat, 21 Nov 2026 07:53:37 GMT, 252,860 bytes, SHA-256 d77e84e6d58d7eeeac7cb6416af774a399b99b2f3e782bd6928361940136e1b2, **matching** the expected hash. pdfinfo: 15 pages, Creator and Producer "Microsoft® Word voor Microsoft 365", created 21 Nov 2026 07:53:23 UTC. This is the third read of the file today (Watch 14:47, comparison 15:17, this review), each one-off; disclosed here. |
| Body kept | No. Text extracted with pdftotext -layout in the session scratchpad, read page by page, and deleted at about 15:23 UTC. This note quotes the report only where a check needs a phrase. |
| Other reads | None. No searches. |

Every statement about "the report" here means that third party's copy, as in the comparison.

## What was checked and found

**Quotations and pages.** Every quotation the comparison attributes to the report was matched against the extracted text by script and by eye, with its page. All are verbatim and on the stated pages: the title page and copyright notice (p. 1); incident IDs and impacted services, the executive summary's defect, three conditions, cyber and AI sentences (p. 2); "four main factors" (p. 5); the July sentence, safe deployment, the gateway-server update, the 14% capacity, BCDR, the 1:07 AM failover and the older-SKU load testing (p. 6); 4:00 PM peak (p. 7); the cascade, more than 80% unresponsive, automated recovery, change auditing and the safeguards for recent changes (p. 8); the 4:03, 4:17, 4:20 and 4:33 PM entries and the 24-to-48-hour retry window (p. 9; also p. 3); 5:32 PM, 6:27 PM (Copilot named) and 7:00 PM (p. 10); 9:00 PM health check and automated restart process, 1:15 AM "partially successful" (p. 11); 1:53 AM disabling some automated redirection, 7:20 AM revert (p. 12); 4:15 AM final updates and completed actions (p. 13); duplicated completed-actions rows, guardrails and "Failover testing did not identify..." (p. 14); change-auditing action CY27Q1 and the 20-minute notification finding (p. 15). Two quotations sit inside table columns that pdftotext's layout mode interleaves with timestamps (the 7:20 AM revert, p. 12; the failover-testing finding, p. 14); both were checked by eye and are verbatim.

**Statements about the report.** Checked and correct: the executive summary uses "change" nowhere before the AI sentence (it says "defect", "conditions", "the fix", "the update"); the exact phrase "The change that introduced the defect" first appears on p. 6; no occurrence of "agent", "artificial" or "machine learning" in the extracted text, and the only "AI" is the one sentence on p. 2; "Copilot" occurs only as an impacted service (pp. 2, 3, 4, 10), with the Copilot Cowork line on p. 4; the four factors are the summary's three conditions plus the defect; the completed-actions table repeats its first two rows on pp. 13 and 14; the cyber sentence carries basis words and the AI sentence carries none; no method for the AI sentence is described anywhere.

**Statements about the baseline.** Checked against the readings and issue #54: B1's wording and the 14 November 04:17 GMT final status as mirrored (readings of 20, 21 and 22 November); the Pennsylvania extract repeating it for both IDs (21 November); B3's wording (20 November); the tenant copy behind a browser challenge on every daily read of 14 to 20 November and not requested on 21 or 22 November; the X post refused by robots.txt (20 November); the two copies of the 01:04 UTC "post-incident report has been published" entry (21 November); the read times quoted for each. All correct.

**Provenance.** The third-party limit is stated in the In short, the header (with the rule that "the report" means this copy), the opening of the item-by-item section, B2's paragraph by implication and the Limits. Adequate.

**No inference from missing mention.** None drawn. Items 3 and 5 and the Limits say a missing mention settles nothing; the B1 reasoning uses the absence of any disclosure only to rule out "contradict", which is a statement about what the text says, not about operations. The automation listed in item 3 is described, not classed as AI.

**Interpretation labelled.** The referent of "This change" is labelled interpretation in item 2, the B1 reasoning and the Limits; the B3 reasoning is labelled interpretation; the "derived observation" on the three conditions and four factors is labelled.

**Classifications.**

- *B1, qualified.* Agreed. Under issue #54 item 2 ("Do not silently narrow a broad statement to direct agent execution or expand it to no AI use anywhere"), reading the report's narrower sentence as confirming B1 would be the silent narrowing the issue forbids, so "confirm" is not right. "Leave unaddressed" is wrong for the claim as a whole because the report addresses AI explicitly. "Contradict" has no textual basis. The one refinement is that the agents element of B1 is, taken alone, unaddressed; the comparison says agents aren't mentioned but doesn't name that as a sub-classification (smaller point 1). The strongest textual observation for the narrowing is also left implicit: the two adjacent sentences change subject, from "This incident" (cyber) to "This change" (AI) (smaller point 2).
- *B2, confirmed.* Agreed: same subject (the incident), same exclusion, basis words present.
- *B3, qualified.* Agreed, with the reasoning tightened. "Contradict" would need the report to say the earlier change was not a capacity upgrade, or that no recent network change was involved; it says neither. It never mentions a capacity upgrade at all, so it gives a more specific and different account without asserting incompatibility. The comparison's reason that the preliminary wording "is a loose summary" characterises Microsoft's drafting, which nothing read establishes; the classification stands better on the text alone (smaller point 3).

**Quotation tally.** Recounted with a script that pulled every double-quoted string from the comparison and matched it against the extracted report text (scratchpad script, deleted with the text; arithmetic below). The comparison's per-quotation counts are right for most items but wrong in three, and one quotation is omitted:

- cyber and AI sentences: 27 words, not 25;
- "in or introduced into a retrieval system": 7, not 6;
- "Report Date: November 20, 2026": 5, not 4;
- the title quotation on line 26, "Post Incident Report For Microsoft 365": 6 words, not in the tally.

Recount of the distinct report text quoted (longer quotations absorb their own fragments): 27 + 7 + 6 + 5 + 6 + 3 + 13 + 10 + 11 + 4 + 11 + 17 + 6 + 4 + 6 + 2 + 7 + 9 = 154 words, plus about 7 more in single-word or two-word fragments quoted in item 2 and item 3 that no longer quotation contains ("defect", "conditions", "the fix", "the update", "Copilot"), about 161 in all. The comparison states "about 144 words, within the bound of 150". Even leaving out the fragments, the count is 154, over the bound the note sets itself in its header and in the tally. Must-fix 1.

**Writing.** British spelling throughout (for example "centre"); no em or en dashes (checked by code point); an In short opening of four sentences in plain words, labelled unreviewed. Fine.

## Must-fix

1. Correct the quotation tally and bring the quoted report text within 150 words. The stated total (about 144) is wrong: three counts are low by one or two words and the title quotation is left out, so the true total is at least 154, about 161 with fragments. Trimming the title-page quotation and the date to paraphrase, or paraphrasing one or two of the longer operational quotations (for example the safe-deployment or gateway-update phrases), would bring it under; then restate the tally with the corrected counts.

## Smaller points

1. B1: say explicitly that, within "qualified", the agents element taken alone is unaddressed, so a reader of the classification line sees that the report is silent on agents rather than narrower about them.
2. B1: add, as observation, that the cyber sentence's subject is "This incident" and the next sentence's is "This change". It is the plainest textual ground for the narrowing and needs no interpretation.
3. B3: rest the choice of "qualify" over "contradict" on the text (the report never mentions a capacity upgrade and never says the preliminary account was wrong) rather than on calling the preliminary wording "a loose summary", which characterises Microsoft's drafting without evidence. The conclusion needn't change.
4. Item 1, "more than 80% of North American servers": the report's sentence says "servers", in a paragraph about the North American fleet. The reading is reasonable but is a reading; "more than 80% of servers, in the paragraph on North America" keeps it exact.
5. Item 4 lists the 9:00 PM alternative health check under "worked, or partly" without saying that the 10:00 PM entry reports the actions so far had not been effective and the 11:55 PM entry that returned servers became unresponsive again (p. 11). A clause would keep the list fair.
6. Limits, first bullet: "a Word re-export made on 21 November 2026" states as fact what the metadata only suggests; the header's "copy or re-export" is the exact form.
7. "the preliminary report of 15 November": the readings record accounts disagreeing on 15 or 16 November (18 and 19 November readings). "of 15 November (16 November in one account)" or "dated 15 November by one account" is exact.
8. Retention across the repository: the reading of 22 November's addendum already quotes the same report (the cyber and AI sentences, the July clause, the three conditions, the retrieval phrase). The watch's 150-word bound is written for each reading, so neither file breaks it once must-fix 1 is done, but the next round might say in the tally that the bound is applied per document.
9. The status of "unavailable" as a sixth category: issue #54 lists it beside the watch's five. It doesn't apply here; a half-sentence saying so would close the gap between the two lists.

Must-fix: 1. Correct the quotation tally (true total at least 154 words, not about 144) and bring the quoted report text within the 150-word bound.
