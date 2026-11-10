# Baseline retrieval from the existing record

**In short.** The existing files let this agent answer the eight fixed questions, including the source-access gap and the unknown private report date. The useful links already exist, although they sit across the claims table, correction notes and two study briefs. This checks retrieval by an agent, not understanding by a non-technical human.

Condition: baseline, protocol 0.1. Input commit: `8af0cb026037a8ee63456900978b3c44473c49cd`. Reader: a fresh Codex agent context; exact model identifier and attributable dollar cost unavailable. The context inherited the task and the parent's initial repository inspection, including the general outline of the proposal and the Australia example. It did not receive extracted graph records, a prototype or comparative answers. All source reads below used `git show` at the frozen commit, except the protocol, baseline manifest and unchanged AGENTS.md. No external source was reopened. Source passages are retained statements, not private-log verification.

Retrieval started at 19:21:27 UTC on 10 November 2026 and the last evidence read finished at 19:21:50 UTC: 23 seconds observed wall time for inspection, excluding writing this report. The report was written by 19:22:56 UTC, 89 seconds from the first read; a fifth tool call wrote it. This is not a measure of active model compute or a controlled human reading time. Four functions.exec calls, each containing one exec_command, performed the inspection: one instruction read and three source-read batches. There were no search-engine or network calls. The initial AGENTS.md output and two large source batches were partly truncated; the cited passages below were visible in the returned output. No claim is made to have read the full external reports.

## Answers

### 1. The first sampled claim: isolation

The first numbered claim is R01, at [claims table](../it-was-only-a-test/claims-table.md), line 9 at the frozen commit. It says the evaluation agents were intended to be isolated and identifies M1, Core takeaways and setup, with quotation anchor Q01. The M1 definition at line 202 resolves to [METR's investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), dated 26 August 2026 and read 8 November in the [essay's first source note](../../essays/it-was-only-a-test.md), line 16.

A retained source pinpoint is [the second claims check](../it-was-only-a-test/claims-check-claude.md), R01 at line 52, which quotes METR's isolation statement. The table's own line 5 says institutional accounts remain attributed and checking a source does not reproduce its private logs. The event is therefore not independently confirmed by this record. This agent has located the retained citation and reviewer quotation, not reopened METR.

### 2. The sixth sampled claim: participation count

The sixth numbered claim is R06, at [claims table](../it-was-only-a-test/claims-table.md), line 14. It attributes approximately 700 participants in the Hugging Face attack to METR, Core takeaways and board participation, with anchor Q03. Q03 at line 116 is the short numeric anchor; [claims check](../it-was-only-a-test/claims-check-claude.md), R06 at line 57, locates the fuller participation wording in METR. The [essay](../../essays/it-was-only-a-test.md), line 24, explicitly introduces the counts as the investigators' count.

This is a source estimate, not a new Lighthouse count, attack-frequency measurement or independently reconstructed population. The source and read dates are those in answer 1.

### 3. Australia: a historical access failure followed by verification

The [claims check](../it-was-only-a-test/claims-check-claude.md), line 68, records HTTP 403 from O1 at 16:22:53Z and 16:27:07Z on 8 November 2026. Its unreadable rows are R17 to R21, R23 and R77, in the row-by-row table at lines 68 to 74 and 128. These concern the precise medicine-spending task, June timing, public-source objective, non-public access and credentials/file writes, patient/client-record exclusion, continuing objective and internal-model safeguards. Some points were partially corroborated by the Prime Minister's transcript, but the reviewer did not substitute that transcript for details it lacks.

The separate [Australia verification](../it-was-only-a-test/australia-verification.md), lines 3 to 19, records that the authoring Codex session reopened [OpenAI's account](https://openai.com/index/how-we-will-do-better-for-australia/) on 8 November, compared it with retained same-day text and mapped all seven rows to primary passages. The source was published 28 September with a 4 October update. The result is support as OpenAI's account or interpretation. The old 403 verdicts remain unchanged. This resolves access and citation coverage, not independent incident forensics.

### 4. A correction that prevents possibility from standing in for observed reuse

The [essay's dated correction](../../essays/it-was-only-a-test.md), line 14, is 8 November 2026. It says AISI reported actual reuse by later agents, whereas the essay previously described a possibility, and links the [earlier edition](https://github.com/JKershaw/lighthouse/blob/a5aa39431fe447c786e8a2b7face26efa027550c/essays/it-was-only-a-test.md). I located this link but did not open that earlier commit during this baseline; the prior wording is available in the retained reviewer account.

The [claims check](../it-was-only-a-test/claims-check-claude.md), lines 133 and 154 to 155, identifies the old possibility phrasing and the source's stronger statement about subsequent use. The [revision record](../R-0053-it-was-only-a-test-correction.md), line 12, makes the consequential limit explicit: reported reuse does not prove apparent authority caused it. The current [essay](../../essays/it-was-only-a-test.md), line 64, attributes subsequent discovery and use to AISI. The correction matters because availability, consumption and a causal improvement or harm are different claims.

### 5. The model source report and three different signals

The public source report is [Anthropic's Discovering vulnerabilities with Claude](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude), identified in [the core-watch panel](../../studies/LH036/panel.json), `pages.anthropic`. [The core-watch brief](../../studies/LH036/brief.md), lines 17 and 26, records a 1 November pre-brief read and the page's publication date of 27 October. For this particular CVE the retained claim is that the model wrote an exploit; the record should not silently turn that into proof of every discovery step.

[When a model finds the bug](../../investigations/model-found-bugs.md), lines 14 and 31, keeps severity score, EPSS prediction, CISA listing and distribution fix availability distinct from claims of exploitation. The [brief](../../studies/LH036/brief.md), measures 1 to 4 at lines 35 to 38, distinguishes the daily exploit-prediction score, catalogue status, CVSS/enrichment and fixed packages in security channels. Its line 55 states that these observations cannot say whether anyone exploited the bug, whether a fixed package was installed or why a score moved. A high severity score and a low EPSS score are different constructs, not necessarily contradictory evidence.

### 6. Private report date: unknown

The public record retained for this task does not establish the private vulnerability report date. [The disclosure brief](../../studies/LH038/brief.md), line 17, says no source read so far supplies it. Its T0 definition at line 36 leaves it unknown unless a public primary source explicitly dates the report. A commit author date and the CVE reservation are not substitutes. The protocol was fixed on 4 November, before timeline-source reads, with a one-read window of 17 to 23 November.

The [policies section](../../studies/LH038/brief.md), lines 19 to 30, retains the six parties' stated disclosure rules as read on 4 November. The comparison at line 47 preserves ambiguity about the patch clock and full technical details. The limits at line 61 explicitly anticipate an inconclusive report date and forbid inference about private discussion or policy compliance. The investigation's question 2 at line 21 supplies a shorter reader route to the same unknown.

### 7. Uptake and social benefit: not established by these records

No. [The core-watch brief](../../studies/LH036/brief.md), line 38, says installation or reboot into a fixed package is not observable here; line 55 also excludes affected-machine counts and actual exploitation. [The disclosure brief](../../studies/LH038/brief.md), line 47, describes dates against policies without claiming intent, harm or exploitation. These records track availability and public signals, not measured deployment uptake or benefits caused by AI discovery.

To test uptake would require a defined installation/deployment population, a denominator, observation windows and a valid way to observe running fixed versions. To attribute social benefit would additionally require a defensible counterfactual, such as comparison of incident outcomes with and without the earlier discovery, with confounders and missingness handled. That is a methodological requirement inferred by this reader, not a study performed here. The distinction is consistent with [the essay](../../essays/it-was-only-a-test.md), line 106, separating artefact retention, consumption and improvement of subsequent work.

### 8. A thematic bridge, not intellectual influence

Both threads ask what follows AI-assisted cybersecurity work when it leaves the immediate test or laboratory. The [essay](../../essays/it-was-only-a-test.md), lines 66 to 80, follows fragmented public accounts, detection/disclosure clocks and limits of inferred motives. [The model-found-bugs investigation](../../investigations/model-found-bugs.md), lines 16 and 20 to 23, follows the exploit report through public signals, fixes and a bounded disclosure timeline. This makes public evidence and its different clocks a defensible thematic research lead.

I found no explicit citation between these two selected documents and no passage establishing that one intellectually influenced the other. I would label the bridge as a reader-suggested thematic relationship, not checked support, causal transmission or an influence edge. A candidate next question is whether a common public-event schema can preserve the distinction between a reported laboratory action and a downstream operational effect. The present records do not answer it.

## Omissions and limits

The current frozen claims table runs through R87; the post-release reviewer checked 83 rows. The deterministic sample is still executable through ordinal 81, but the denominator must not be described as the entire current table containing only 83 claims. Dates and passages above were read from the retained frozen record on 10 November, not revalidated at the providers. External links are located citations; their current availability was not tested. The original authoring pack paths are not assumed present in this repository.

These are answers from one agent with a large inherited context and batched file-reading tools. The fast inspection time is neither a general reading-speed estimate nor evidence that an index would not help readers. The author of the pilot must adjudicate accuracy against the frozen passages; this report does not self-award scores or claim independent confirmation.
