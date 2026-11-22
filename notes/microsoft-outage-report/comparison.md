# Microsoft's "not related to cyber or AI / agents" set against its post-incident report

**In short.** On 14 November Microsoft's final status post said the Microsoft 365 outage of 12 and 13 November "was a technical issue not related to cyber or AI / agents". The 15-page report dated 20 November, read from a third party's copy, says something narrower: "This change was not caused by AI tooling." It discloses no AI involvement anywhere, but it doesn't restate the broad exclusion, doesn't mention agents, and gives no basis for the sentence, so this working comparison classes the AI and agents exclusion as **qualified**, not confirmed or contradicted. This is unreviewed: it goes next to an evidence review, a reader-and-inference review and a recheck, and nothing here is a public claim.

| | |
| --- | --- |
| Version | 0.2, 22 November 2026 (working comparison; 0.1 evidence-reviewed in R-0115, one must-fix resolved here; reader review next) |
| Schedule row | MS365-report-compare (issue [#54](https://github.com/JKershaw/lighthouse/issues/54)) |
| Written by | a Claude Code subagent on Opus 5.5 (`claude-opus-5-5`), for the Research run `2026-11-22T151100Z-anthropic-research`, Anthropic cloud |
| Rules | [notes/microsoft-outage-report-watch.md](../microsoft-outage-report-watch.md) (categories and rule 4); issue #54's prospective comparison, fixed 14 November before the report was read |
| Gate | [gate-2026-11-22.md](gate-2026-11-22.md) |
| Report read | https://www.365fanatic.com/wp-content/uploads/2026/11/postincidentreport-mo1550821.pdf , one-off read for this analysis at **15:17:38 UTC on 22 November 2026** through scripts/lh_fetch.py (`access='oneoff'`, `LIGHTHOUSE_PROVIDER=anthropic`, redirects robots-checked; none occurred). HTTP 200, application/pdf, Last-Modified Sat, 21 Nov 2026 07:53:37 GMT, **252,860 bytes**, SHA-256 **d77e84e6d58d7eeeac7cb6416af774a399b99b2f3e782bd6928361940136e1b2**. This **matches** the hash of the Watch run's read at 14:47:21 UTC the same day ([reading of 22 November, addendum](readings/2026-11-22.md)). File metadata: 15 pages, made with "Microsoft® Word voor Microsoft 365", created 21 November 2026 07:53:23 UTC. |
| Body kept | No. Microsoft's notice on page 1 forbids storage "in or introduced into a retrieval system". Text was extracted with pdftotext in the session's scratch directory, used for this note and deleted at about 15:18 UTC. Kept here: URL, read time, status, size, hash, the facts used and short located quotations (at most 150 words in total; tally at the end). |
| Baseline sources (not re-read today) | Issue #54 (the tenant copy, read directly on 14 November by an earlier session; time of read not given in the issue). Cloud Admin Hub's mirror of MO1550821, read 20 November 14:16:50, 21 November 14:14:35 and 22 November 14:13:40 UTC ([20](readings/2026-11-20.md), [21](readings/2026-11-21.md), [22 November](readings/2026-11-22.md)). University of Pennsylvania's published admin-console extract, read 21 November 14:14:38 UTC ([21 November](readings/2026-11-21.md)). |
| Provenance limit | The report is a third party's copy or re-export (365Fanatic, a Microsoft 365 consultancy) of a document presented as Microsoft's, which tenants receive in the admin centre. Whether it matches the admin-centre original word for word can't be checked from public sources, and the watch forbids the route that could. Every statement below about "the report" means this copy. |
| Other source reads | None. No searches; no other documents. |

Page numbers are the PDF's page order (1 to 15), as pdftotext split them; the copy prints no page numbers of its own that were checked.

## What the report says, item by item (watch rule 4; issue #54 items 1 to 5)

Everything in this section is **source report** (Microsoft's account, as copied by a third party) unless labelled otherwise.

### 1. Trigger and contributing changes

- Title page: "Post Incident Report For Microsoft 365", "Report Date: November 20, 2026" (p. 1). Incident IDs EX1550543 and MO1550821; impacted services listed include Exchange Online, Microsoft 365 Copilot, Teams, SharePoint Online, OneDrive, Defender, Purview and others (p. 2).
- The executive summary names a latent Windows defect, specific to a configuration Exchange Online uses, as causing gateway servers to become unresponsive under load, triggered by "the combination of three operational conditions" (p. 2): reduced capacity during planned maintenance, a shift of Teams traffic to the Exchange Online gateways, and peak North American traffic.
- The detailed section counts "four main factors" (p. 5): (1) a connection-processing defect from lock contention in an internal Windows process, worse on newer, higher-core hardware (p. 6); (2) nearly 14% of gateway capacity out of service for routine deployment (p. 6); (3) an automatic Teams failover at 1:07 AM UTC on 12 November after a routing issue in US East (p. 6); (4) peak load, with broad North American failures from about 4:00 PM UTC (p. 7). Derived observation: the summary's three conditions plus the defect make the four factors; the counts don't conflict. (The [22 November addendum](readings/2026-11-22.md) attributed "four factors" to 365Fanatic's summary; the report itself also uses it, on p. 5.)
- The change that introduced the defect: "The change that introduced the defect started deployment in July of this year." By the report's account it passed through safe deployment and reached every region over several weeks without observed issues (p. 6, paraphrased). Elsewhere it is described as an update enabled on Microsoft 365's networking gateway servers (p. 6, paraphrased) and "the connection handling change" (pp. 13 to 14).
- Spread: automatic traffic management moved load to healthy capacity units and then other regions, cascading globally; at the lowest point, by the report's sentence, more than 80% of servers were unresponsive; that these were North American servers is our reading of the context (pp. 7 to 8).
- Against the preliminary account (baseline, [20 November mirror reading](readings/2026-11-20.md)): the status post said the incident "was introduced by an issue during an earlier network capacity upgrade that surfaced following a recent network change". The report describes the earlier change as a Windows connection-handling update on gateway servers, not a capacity upgrade, and the recent conditions as maintenance capacity loss, a Teams failover and peak load. Classification of that claim is in the comparison below.

### 2. Scope and basis of the AI exclusion

- The only sentence on AI (p. 2, end of the executive summary): "This incident was confirmed not to be caused by a cyberattack, and we found no evidence of malicious activity. This change was not caused by AI tooling."
- Scope, observation: the sentence's subject is "This change". The executive summary uses the word "change" nowhere before it (it speaks of a "defect", "conditions", "the fix" and "the update", the last meaning the repair). The phrase "The change that introduced the defect" first appears on p. 6. Interpretation: the most likely referent is the July change that introduced the defect, as the [22 November addendum](readings/2026-11-22.md) also read it, but the report doesn't say so, and a looser reading (the incident as a whole) can't be excluded from the text.
- What it covers, observation: "AI tooling" as the cause of that change. It does not mention agents anywhere (no occurrence of "agent" in the extracted text), and says nothing about AI in the triggering conditions, the failover, detection, diagnosis or recovery.
- Basis, observation: none stated. The cyber sentence carries basis language ("confirmed", "found no evidence"); the AI sentence carries none, and the report describes no method (for example, review of how the change was authored) by which it was determined.

### 3. Disclosed AI in code, configuration, testing, review, deployment, diagnosis or recovery

- No disclosure of AI use in any of these (observation, from a search of the extracted text for "AI", "artificial", "agent", "machine learning" and "Copilot"). "Copilot" appears only as an impacted service (pp. 2 to 4, 10), including that prompts to Copilot Cowork might have answered but without mail, file or calendar data (p. 4).
- The report describes ordinary automation in detection and recovery: a "connectivity anomaly detection monitor" (4:03 PM, p. 9), automated failover (1:07 AM, p. 9), automated traffic redirection (4:17 PM and 5:32 PM, pp. 9 to 10), an automated restart process prepared at 9:00 PM (p. 11), and the disabling of some automated redirection at 1:53 AM on 13 November (p. 12). Whether any of these uses machine learning is not stated, and nothing here treats them as AI.
- Rule 4 and issue #54: a missing mention of AI in testing, review, deployment, diagnosis or recovery settles nothing either way.

### 4. Controls: what worked and what didn't

Source report, as the report frames them.

- Worked, or partly: safe deployment ran for weeks without observed issues (p. 6), which also means it did not catch the defect; spare capacity normally covers routine maintenance (p. 6); BCDR failover between the two gateway systems normally has no impact, by the report's account (p. 6); anomaly detection identified the rise in connectivity issues at 4:03 PM, before the first support case at 4:33 PM (p. 9); deployments and configuration changes were paused at 7:00 PM as a precaution (p. 10); an alternative health check returned a subset of servers to service at 9:00 PM (p. 11); pressure-reducing measures at 1:15 AM were "partially successful" (p. 11); the mitigation at 7:20 AM was "an update that reverted the defective change" (p. 12); the retry window was extended from 24 to 48 hours and no enterprise mail was found permanently lost (pp. 3, 9). Completed actions include reverting the change, fixing the Windows image, added capacity, monitoring and temporary guardrails against automatic traffic distribution (pp. 13 to 14).
- Didn't: load testing used "older SKU hardware with fewer cores" (p. 6); automatic redistribution spread the failure (pp. 7 to 8); "Our automated recovery processes were not equipped to restore service reliably" in this combination (p. 8); usual safeguards for recent changes could not quickly revert a months-old change (p. 8); "Failover testing did not identify the defect in isolation" (p. 14); first customer notification came about 20 minutes after broad impact (p. 15). Next steps run to CY26 Q4, CY27 Q1 or TBD (pp. 14 to 15).
- Observation about the copy: the completed-actions table shows two rows (the revert and the Windows image fix) on both p. 13 and p. 14. Whether that is in the original or an artefact of the re-export is unknown.

### 5. Staffing, handover or knowledge

- Directly evidenced: "On-call engineers received a high-priority alert" at 4:20 PM (p. 9), and the response was expanded at 7:00 PM (p. 10). On knowledge and process, not people: because the defect came from a change made months earlier, "our change auditing and diagnostics processes took longer to identify the Windows change as the root cause" (p. 8), with a diagnosis action due CY27 Q1 (p. 15).
- Not addressed: staffing levels, handovers, team changes, review capacity. Missing mention settles nothing, and company-wide announcements, which this note did not read, would not establish a service-level chain.

## The comparison

### The baseline statements

- **B1, the AI and agents exclusion.** "This was a technical issue not related to cyber or AI / agents." Microsoft's final status post of 14 November 04:17 GMT as mirrored by Cloud Admin Hub (read 20, 21 and 22 November, above) and repeated in the University of Pennsylvania extract (read 21 November); reproduced, attributed to Microsoft, on the tenant notice cited in issue #54 (read directly on 14 November by an earlier session; walled to the daily runs of 14 to 20 November). Microsoft's X post was refused by robots.txt and not read. Derived observation: the report's timeline puts the final customer updates at 4:15 AM UTC on 14 November (p. 13), two minutes before the mirror's 04:17 GMT; the difference is noted, not explained.
- **B2, the cyber exclusion**, in the same sentence.
- **B3, the preliminary cause**: "introduced by an issue during an earlier network capacity upgrade that surfaced following a recent network change" (same post, as mirrored, read 20 November).

B1 is the claim the watch was commissioned for. B2 and B3 are classified because issue #54 asks for each original claim to be classified; they are secondary here.

### B1 against the report: **qualified**

The report's statement: "This change was not caused by AI tooling." (p. 2), after the cyber sentence, with no basis stated and no mention of agents.

Reasoning (interpretation, under the watch's fixed categories):

- The report addresses AI, and nothing in it discloses AI or agent involvement in the change, the triggering conditions, testing, deployment, detection, diagnosis or recovery. So it gives no ground for contradiction.
- But its claim is narrower than B1 and differently worded. B1 says the incident, "a technical issue", was not related to "AI / agents". The report says that "This change", most likely the July change that introduced the defect, was not caused by "AI tooling". It does not restate that the incident as a whole was unrelated to AI, does not mention agents, says nothing either way about AI in the conditions that triggered the defect or in the response, and gives no evidence for the sentence. That is a narrowing of scope without a stated basis, which is what "qualify" is for. The plainest textual ground is that the two sentences change subject: the cyber sentence is about "This incident", the AI sentence about "This change" (p. 2). Taken alone, B1's "agents" is unaddressed: the word does not appear in the report's text.

Why not the others:

- **Confirm:** would need the report to restate the broad exclusion, or to support it across its scope. It does neither: it speaks only of the cause of one change, and only of "AI tooling". This is the closest alternative. A reader who takes "This change" to be the root cause, and the root cause to be what B1 meant, would read the report as confirming B1 for that cause; the watch's rule against silently narrowing a broad statement (issue #54, item 2) is why this note doesn't.
- **Contradict:** nothing in the report says or implies AI or agents played a part. A narrower statement is not an opposite one, and changed wording is not automatically a contradiction (rule 4).
- **Leave unaddressed:** the report addresses AI explicitly.
- **Non-comparable:** both statements are about AI's part in the same incident, from the same company, and can be set side by side; the difference is one of scope, which is the qualification itself.

What "qualified" does not mean: it doesn't mean B1 is wrong, that Microsoft retreated from it, or that AI was involved anywhere. Nor does it mean B1 was proved: the report is Microsoft's own account, gives no basis for the AI sentence, and Lighthouse has no independent view of the operations. No motive is inferred from the change of wording.

### B2 against the report: **confirmed**

"This incident was confirmed not to be caused by a cyberattack, and we found no evidence of malicious activity." (p. 2). It covers the incident, restates B2's exclusion in its own words, and states a basis in general terms ("confirmed", "found no evidence"), though no method. Not qualified, because its scope matches B2's; "malicious activity" is, if anything, broader than "cyberattack". Confirmed here means only that Microsoft's report says the same as Microsoft's status post; it is not independent confirmation.

### B3 against the report: **qualified**

The report keeps B3's shape (an earlier change, exposed later by a more recent condition) but replaces its content: the earlier change was a Windows connection-handling update enabled on gateway servers from July (p. 6), not described as a "network capacity upgrade", and the surfacing conditions were reduced capacity during routine deployment, a Teams failover after a routing issue and peak load (pp. 2, 6 to 7), not a single "recent network change". Interpretation: this is a more specific and partly different account; the closest alternative is contradict, on "network capacity upgrade". It is classed qualify on the text: the report never mentions a capacity upgrade, so it says nothing incompatible with the preliminary account, while it gives a more specific and different one (a routing issue and a capacity reduction are network events; a gateway server update sits in network infrastructure); the watch says changed wording is not automatically a contradiction. The evidence review (R-0115) weighed contradict and agreed with qualify.

## Limits

- **Third-party copy.** The report was read from 365Fanatic's file, a copy or re-export whose metadata says it was made with Microsoft Word on 21 November 2026, not a file served by Microsoft. Its match with the admin-centre original can't be verified from public sources, and the watch forbids tenant login. The two copies of Microsoft's posts that announce "A post-incident report has been published." at 01:04 UTC on 21 November ([reading of 21 November](readings/2026-11-21.md)) show a report exists; they don't show this text is it. Today's read matched the earlier hash, which shows only that the hosted file didn't change between 14:47 and 15:17 UTC.
- **One company's account of its own incident.** Every operational fact here, including the AI sentence, is Microsoft's say-so. Lighthouse has no independent operational verification of the trigger, the factors, the controls or the absence of AI involvement.
- **The baseline is copied too.** B1 to B3 come from a tenant's notice and two third-party copies of Microsoft's posts, not from Microsoft's own pages; the tenant notice has been walled since 14 November and wasn't re-read; the X post wasn't read.
- **The referent of "This change" is interpretation.** The executive summary doesn't name the change it refers to.
- **Absence of mention.** That the report doesn't mention AI in testing, review, deployment, diagnosis or recovery, or mention agents at all, settles nothing about whether AI or agents were used or contributed. Incidental AI use, had it been disclosed, would not by itself be causal contribution.
- **Extraction.** Text came from pdftotext; the chart on p. 7 (Figure 1) and any text inside images weren't read. Keyword searches cover only the extracted text.
- **Not checked:** the preliminary report of 15 November (never read by Lighthouse; one copy redirected, another refused by robots.txt); Microsoft's admin-centre original; journalism and commentary beyond the readings already retained; whether the report has been revised since 20 November; any Microsoft statement elsewhere on AI and this incident.
- **Purposive, not blind.** The outcome of the incident and the baseline were known before the comparison rules were fixed (issue #54). This is one incident and one statement, not a sample.

## What would change this

- Microsoft's admin-centre original, or another independent copy, differing from this copy in the AI or cyber sentences: the classification would be redone on that text.
- A Microsoft statement, revision or later report that restates the broad exclusion with scope and basis (towards confirm), or that discloses AI or agent involvement in the change, the conditions or the response (towards contradict, depending on what is disclosed and whether it contributed).
- A statement from Microsoft saying what "This change" refers to, or how it established that AI tooling did not cause it.
- The evidence review or reader review finding that the categories have been misapplied, in particular on B1 (confirm against qualify) and B3 (qualify against contradict).

## Quotation tally from the report

Located quotations from the report used above, in words, recounted after evidence review R-0115 found the first tally low: p. 1 "Post Incident Report For Microsoft 365" (6), "Report Date: November 20, 2026" (5) and "in or introduced into a retrieval system" (7); p. 2 the cyber and AI sentences (27) and "the combination of three operational conditions" (6); p. 5 "four main factors" (3); p. 6 the July sentence (13) and "older SKU hardware with fewer cores" (6); p. 8 the automated-recovery clause (11) and the change-auditing clause (17); p. 9 "connectivity anomaly detection monitor" (4) and "On-call engineers received a high-priority alert" (6); p. 11 "partially successful" (2); p. 12 "an update that reverted the defective change" (7); pp. 13 to 14 "the connection handling change" (4); p. 14 "Failover testing did not identify the defect in isolation" (9). Total 133 words, plus about 7 words of one- and two-word quoted terms ("change", "defect", "the fix" and the like), about 140 in all, within the bound of 150. Two p. 6 quotations of version 0.1 (21 words) are now paraphrases. Repeats of parts of these quotations elsewhere in the note are not counted twice.

## Changes

- **0.2, 22 November 2026, Research run (driver), after evidence review [R-0115](../R-0115-ms365-comparison-evidence.md).** Must-fix: the quotation tally was low (about 144 stated; at least 154 by the reviewer's count), so two p. 6 quotations (21 words) became paraphrases and the tally was recounted at 133 words plus about 7 of one- and two-word terms. Smaller points taken: the subject switch from "This incident" to "This change" and the unaddressed "agents" stated under B1; B3's choice based on the text, not on calling the preliminary wording loose; the "more than 80%" sentence's "North American" marked as our reading; the Limits' "Word re-export" restated as the header's "copy or re-export". Not taken here, left for the reader review: the 9:00 PM health check's later relapse and the 15 or 16 November date of the preliminary report. No classification changed. Version 0.1 is in git history (commit before this one).
