# What a reader would believe, written before reading the underlying sources

**In short.** Added after stage 2: the initial reader takeaway survives comparison with the retained evidence and cached primary passages. No material inference correction is required; collection should stop, and the possible Harbour workflow measurement should remain distinct from a staffing or retained-knowledge test.

Stage 1, 13 November 2026. With no released article, shortform or homepage promotion, the working study and investigation page replace the usual piece, shortform and README surfaces.

My takeaway: this public-record pilot describes technical failures and relationships between AI-written code, review and incidents, but cannot establish that AI-driven staffing changes removed expertise and caused outages. The missing chain remains a measurement problem, not a finding that capacity was preserved or lost.

What appears observed: two of four selected outage accounts were readable, alongside two operator papers. They report technical triggers, recovery complications and code/review measures. Associations come from operator studies, rather than Lighthouse observing internal work. AI use, automated traffic and staffing decisions are explained as different exposures. AI's safety or harm is not causally established.

Limits: known outcomes selected beforehand, inaccessible cases, selective reporting, private telemetry, partial provenance, both papers concerning Meta and uncertain cohort overlap. Review time and tenure cannot establish retained understanding. The investigation connects staffing to infrastructure risk while separating it from autonomous spread and current harm. Collection has stopped; measurement feasibility is next.

Exact files opened in stage 1: `studies/LH052/LH052.md`; `investigations/ai-cost-and-spread.md`. No underlying sources opened.

Reviewer: Codex/OpenAI; exact model identifier, token usage and dollar cost unknown. Fresh same-family review, not independent confirmation.

## Stage 2: what the round establishes

The stage 1 text above is preserved unchanged; only the explicitly labelled opening and this stage 2 assessment were added after source access. The original blind account is under 250 words.

The question was whether the measurements could be correct while the explanation was wrong. Yes. More code and a smaller share reviewed promptly could reflect queue pressure, changed work mix or review practices without expertise loss. Lower incident rates among selected, eligible automated changes could coexist with either preserved or declining long-term understanding. A negative adjusted AI-code coefficient could reflect residual selection and context rather than a protective AI effect. The working record does not make those explanatory leaps.

The supported result is narrower: these selected sources provide technical/recovery accounts and reported internal code/review/incident measurements, but do not identify the proposed organisational chain. The result is about these accessible materials, not all public records. The outage cases were selected after their outcomes were known, half were inaccessible, and an unaffected comparison is absent. Non-disclosure is not a negative observation. Two papers about Meta do not become two company replications; their uncertain cohort overlap further limits synthesis.

Provenance improves the exposure measure, but landed CodeCompose bytes are conditional on code surviving editing, review and landing. They do not measure every AI influence, rejected suggestion, agentic task or worker replacement. The roughly half-covered sample, language imbalance, short completion-era window and unobserved selection constrain transfer. Incident linkage is operator-reported and covers a narrower outcome than every defect, near miss, recovery skill or customer consequence. Neither paper's private telemetry can be reproduced here.

## Material claim problems

None identified that requires a change to the current working-reader surfaces. In particular:

- Exact passage, LH052 opening: “None of these audited materials establishes a chain from AI-motivated staffing changes through lost expertise to an outage.” Evidence: the outage field matrix and located operator passages disclose technical failures and recovery, while the staffing exposure, measured expertise loss and linked comparison are missing. The paper methods and validity sections add review and incident measures without the missing chain. Proposed fix: none; retain “these audited materials” and the explicit warning against treating missing measures as preserved or lost capacity.
- Exact passage, LH052 Findings: “its knowledge-transfer assurance is not accompanied by a reported measure of retained understanding in the audited text.” Evidence: RADAR's section 5.5 asserts a favourable network analysis, but its reported metrics and results supply no corresponding retained-understanding instrument. Latency and throughput cannot fill that gap. Proposed fix: none; this is appropriately bounded to the paper's reported evidence, not a claim that knowledge transfer failed.
- Exact passage, LH052 Findings: “Their main text distinguishes the raw incident comparison from a small adjusted negative association.” Evidence: Mockus section 1.3 and the section 4.3 result box explicitly distinguish an AI-heavy raw rate that is not lower from the slightly negative adjusted association; the abstract uses broader lower-rate language. Different contrasts need not agree. Proposed fix: none; the record preserves the distinction and rejects causal safety and staffing substitution claims.
- Exact passage, LH052 Next: “A possible next design would first assess whether Harbour's own records can measure production versus verification and rework.” Evidence: this pilot demonstrates a missing measurement, not Harbour record availability or validity. The following sentences call this an agent-workflow case, require a separate understanding instrument and commission no access or experiment. Proposed fix: none for the current suggestion; a later protocol must establish those instruments rather than inherit their feasibility as a result.

The excluded RADAR percentage reduction is also handled correctly: no ordinary reduction exceeding 100 per cent can be interpreted without a different, stated normalisation. The audit does not repair or repeat it as an effect estimate.

## Readability, optional

1. “Evidence-coverage result” could be glossed once as “what these selected reports could and could not establish”. The present qualification is accurate.
2. Keep the distinction between waiting, active checking and elapsed review time visible in any subsequent design. A log interval alone does not identify attention, understanding or effort.

## Next-step recommendation

Stop this pilot after reviews. A further known-outage search would retain selection on failure and would need a new exposure-first design to test the mechanism. Stopping is a bounded value-of-information judgement, not proof that every further public account would be uninformative.

The Harbour suggestion is reasonable only as a separately commissioned feasibility question about agent-workflow production, checking and rework. First establish what records identify, how reliably they link tasks to verification and later corrections, and which intervals or activities are missing. Counts of edits, comments, dispatches or time cannot simply be renamed verification effort. Rework can indicate discovery and correction as well as poor initial work.

That workflow study would not test whether AI expectations caused employee departures or whether service understanding survived a staffing change. The former needs dated team/role exposure and rationale plus a credible comparison. The latter needs a separate instrument, such as scored explanation or diagnosis on relevant tasks, with timing and task comparability fixed in advance. Even those measures would require an identification strategy before supporting staffing causation. If Harbour lacks suitable records, a feasibility failure is a valid stopping result. No next study has been commissioned by this review.

## Access, inventory and resources

Exact stage 1 tool/file-read inventory from this reviewer's transcript:

1. One `functions.exec` call invoked `tools.exec_command` with `cat studies/LH052/LH052.md investigations/ai-cost-and-spread.md`, repository working directory `/workspace/scratch/d82030683730/lighthouse`. Those were the only existing files read in stage 1. The displayed result contained both files.
2. One `functions.exec` call invoked `tools.apply_patch` to create this note.
3. One `functions.exec` call invoked `tools.apply_patch` to shorten this note. Neither patch read an additional source. Stage 1 then stopped and returned the note path.

Stage 2 read AGENTS.md first, the LH052 brief, checkpoint, iteration records, both matrices, source manifests, all seven retained evidence/locator JSON files, and the two evidence arithmetic script bodies. It used targeted passages from the seven already-cached primary text files, not new external documents. It consulted the investigation and LH052 record already read in stage 1, programme.md's LH052 Next checkpoint and proposals.md P-0034. An initially overbroad `rg` query, and a later locator query, also displayed unrelated programme/proposal context before the reading was narrowed. No other note, standalone reviewer verdict, releases.md, git history or external link was opened. The staged separation of the blind reading remains intact.

An offline recount from the matrices, manifests and request logs reproduces 30 outage case-source-field rows, 28 operator-measurement rows, seven readable documents, 21 HTTP requests, 2,017,506 response-body bytes, 135.353 summed HTTP seconds and four discovery queries. Replay: `python3 studies/LH052/review/reader-counts.py`; output: `studies/LH052/review/reader-counts.json`. These are coding/access totals, not independent evidence of a mechanism, full compute or billing. No private source analysis, causal effect or chart was reproduced.

This review made no HTTP request or discovery search, used no credentials, visited no exposed host, attempted no re-identification, retained no source body or email, and made no source/study edits, commit, push, upload or outreach. Reusing the seven cached verification documents adds no unique external document; the stated seven-of-eight verification-document count therefore remains unchanged. This reviewer has no independent complete transcript for other agents' resource use. Complete active-time metering, token totals, dollar usage and the authoritative exact runtime model identifier are unavailable, not zero. Reviewer identity is Codex/OpenAI; this is fresh same-family scrutiny, not independent confirmation.

Verdict: no material inference fix required for these working surfaces. Stop collection; retain the uncommissioned next-step and publication boundaries.

## Resolution, by the driving session

No material inference correction was requested. The optional jargon suggestion was applied in the synthesis Answer. The recommendation to stop and to keep Harbour workflow feasibility separate from employee substitution and retained understanding is accepted; no next study starts. The two-stage working-surface adaptation is retained because no article or short form was commissioned. The reviewer reports its exact stage 1 tool/file inventory above; the parent harness does not expose a complete child-agent transcript, so the driver could not independently verify that inventory. The final fresh recheck completed after the resolution and status updates; its two obsolete-status corrections were applied as listed in notes/LH052-final-recheck.md.
