title: What can public records show of AI, organisational capacity and reliability?
kind: study brief
study: LH052
version: 0.1
date: 2026-11-13
investigation: ai-cost-and-spread
status: fixed before new collection

# What can public records show of AI, organisational capacity and reliability?

**In short.** We will test what public records can establish about AI involvement, organisational knowledge, review capacity and recovery. Four already-known outages form a deliberately selected feasibility panel, not an estimate of how often AI causes failures. A second, conditional iteration reads two already-known operator research accounts if the first cannot connect the organisational links; both stop in this commissioning session.

This opening explains the protocol but does not replace it. Owner: the Codex driving session commissioned by John, 13 November 2026. The [commissioning record](../../notes/organisational-reliability/commissioning.md) records authority and the GitHub tracking issue.

## Question and prior knowledge

Can a bounded reader connect AI adoption or AI-related organisational decisions to changes in effective knowledge, verification and recovery capacity from public evidence? Or do public records expose technical failure and outcomes while leaving the organisational links unknown?

The preceding conversation and [background review](../../notes/organisational-reliability/background-review.md) already discussed Microsoft's 12-13 November 2026 outage, GitHub's August 17 outage and retry loop, Holton's latent-swarm hypothesis, and Meta's RADAR and AI-code studies. The conversation read a paper mentioning the AWS October 2025, Google June 2025 and Cloudflare November 2025 outages. Those event outcomes are known in outline. No case is a blind test, a representative draw or independent confirmation of the review. Microsoft's current outage is motivating context outside the four-case panel, not a causal test.

## Iteration 1: four purposive outage cases

Fixed cases, in this order:

1. GitHub, 17 August 2026.
2. Google Cloud, 12 June 2025.
3. AWS US-EAST-1, 19-20 October 2025.
4. Cloudflare, 18 November 2025.

For each resolve the provider's own incident or post-incident account with at most one web search. Read that account and at most one linked provider follow-up that explicitly discusses recovery or controls. If absent or inaccessible, keep that case missing; do not substitute another outage or a third-party story. Maximum eight substantive documents. Pages may be resolved from a provider's own index, but no crawling or scan. Every endpoint and any search-result account used as evidence must pass the repository robots gate for OpenAI before its substantive text is read.

Unit: one case-source claim, aggregated to a case only with source IDs retained. Record event, publication and collection clocks separately. The six fields are: technical trigger; sustaining/recovery mechanism; AI role and evidence; team or staffing change; relevant knowledge/review capacity; operational outcome. AI roles can coexist: upstream dependency, product affected, development assistance, operational execution, externally attributed load, organisational decision justified by AI, or not disclosed.

For each field classify explicit reported evidence, interpretation, not disclosed, conflicting, unavailable, or not applicable. 'Not disclosed' requires a readable relevant account; unread is unavailable. An explicit statement that AI was not involved is different from silence. No company-wide layoff is exposure evidence for a service team. No retry loop, product name or lack of malicious activity by itself establishes agent initiation or AI authorship. Preserve evidence of controls working, successful recovery and ordinary non-AI alternatives.

Primary output: cases.csv and iteration-1.md, with source passages or short paraphrases and URLs supporting each coded field. Assess which links are actually supported in this selected panel. No hypothesis significance tests, population proportions, invented severity scale or estimate of AI-caused outage frequency.

## Iteration 2: conditional measurement repair

After iteration 1 is recorded, the driver writes a checkpoint before starting a second iteration. If the outage panel does not support a staffing-to-operations chain, inspect the two already-known operator studies below to ask what additional internal measurements they possess. This is a different evidence type, not a replication of the outage panel:

- Meta RADAR, arXiv 2605.30208 (known abstract: code supply, timely review and risk-gated automation).
- Mockus et al., A Preliminary Analysis of the Impact of AI Assisted/Generated Code on Quality, Centrality and Review Time at Scale, DOI 10.4230/LIPIcs.ESEM.2026.93 (known abstract and sections: context-dependent AI use and incident associations).

For each, read at most its author/publisher record and full paper, subject to access rules, maximum four documents. Record the exposure definition, observation window, denominator, outcome, comparison, confounders, provenance coverage, human-review/knowledge measure, staffing measure, causal claims and missing information. Explicitly check whether headline summaries overstate the main text. Ask what observable protocol a willing collaborator would need; do not seek collaborators or start another experiment. If iteration 1 supplies the full organisational chain instead, stop and review it rather than automatically widening. The pilot ends after two iterations at most.

## Sources, access, retention and own footprint

Use the existing scripts/robots_gate.py with LIGHTHOUSE_PROVIDER=openai and a Lighthouse-research identifier. Log robots results, UTC times, substantive access status, original URL, source ID, hash and collector route in reads.jsonl. Respect walls, rate limits and retention preferences, including redirects; no credential use, exposed-host visit or re-identification. No bypass through another fetch route after refusal. A search rendering is labelled as such, not raw replay. A source URL must be resolved and recorded before fetching.

Keep permitted evidence as brief extracts or paraphrases, normally at most 150 words per source, with exact location and provenance. Do not commit full copyrighted articles or contact details. Redact email addresses in retained records. Full bodies used for reading may live only in temporary workspace storage where allowed; the public record says what can and cannot be replayed. The original-byte hash is not a retained full source. Log request counts and duration where measurable; missing overhead and monetary usage are unavailable, not zero.

The matrix is derived from operators' reports; its contents are attributed claims, not independently observed causes. Review may reproduce the table from its retained coding data; it cannot reproduce private operational evidence.

## Comparisons and alternatives

The relevant distinction is technical/recovery observability versus organisational causal observability within each case, not a difference in outage rates between providers. Ordinary retries, architectural coupling, changed demand, non-AI automation, staffing decisions unrelated to AI and reporting omissions are alternatives. AI may strengthen review or recovery. Better performance after staffing change would weaken a simple degradation story; silence would not.

## Resource envelope, schedule and stopping condition

One session, two research iterations at most, four outage cases and two research artefacts, no recurring watch. At most twelve analyst documents, eight extra substantive documents for verification, and eight discovery searches across analysts and reviews. Robots reads and redirects are counted separately. At most four hours active analyst/driver effort plus two hours review, within this session; stop and leave an honest partial record if reached. The operating review guides are $14 per reader/recheck and $40 per round at list rates where this harness exposes pricing. They are guides, not a representation of paid-account billing. Actual driver and subagent price is currently unavailable; do not certify a monetary ceiling from missing data.

Rows in schedule/due.csv cover protocol filing, first iteration, conditional second iteration, evidence review, reader review/recheck and close-out on 13 November with a completion window through 14 November. The retained protocol snapshot must precede all new substantive reads. The due unrelated scheduled work remains with the scheduled runner; this is John's directed commissioning session. No standing work is created beyond the bounded completion rows.

Stop at the case/document/time limit, any access prohibition for that source, or after the two iterations. If no accessible source connects team-level change, relevant expertise and the operational outcome, the answer is an access/attribution limit. Record that result, not a negative effect or a finding of safety. Do not initiate outreach, a new investigation or further data collection from a Next suggestion.

## Review and what would change the conclusion

A fresh evidence reader checks the classifications against primary sources or states access limits, then a fresh reader-and-inference check tests whether public wording implies unobserved causes. Record model/provider honestly, with unavailable costs. Fresh-agent agreement is not independent confirmation. No article, essay or released finding is promised. Any draft public claim remains marked unreviewed until the required checks and recheck pass.

A specific service-team reorganisation linked by direct records to AI expectations, loss of relevant capacity and altered incident outcomes would change the organisational attribution. Evidence of preserved understanding, successful handover or improved operational outcomes would challenge the harmful mechanism. An aggregate layoff announcement or AI code percentage alone would not.

## Corrections

0.1 fixed before new collection. Later choices, access failures, selection effects and any protocol changes are dated explicitly. The background review is prior evidence, not a fresh sample.

## Administrative renumbering, 13 November 2026, after collection

The scheduled pass independently allocated LH051 to WFX Phantom and P-0029 to its proposal before this local branch was published. This pilot is therefore LH052, proposal P-0034. Its original protocol snapshot `bb8a6e9` and checkpoint `68b7093` retain its former local identifier LH051. Raw request logs and historical review-output hashes retain their original identifiers and paths; the source IDs, question, selection, coding and stopping rules are unchanged. Current cross-links and replay scripts use LH052. This is an administrative alias correction, not a new study or a post-outcome research-design change.
