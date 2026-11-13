title: What internal measurements repair the outage panel's missing links?
kind: exploratory study iteration
study: LH052
iteration: 2
version: 0.2
date: 2026-11-13
status: evidence and reader checked; final recheck complete
collector: Codex / OpenAI; exact model ID, token totals and monetary usage unavailable
protocol-and-checkpoint-commit: 68b7093b641650679e818dd226350c63acdf7645
collection-window-utc: 2026-11-13T08:59:40.986194Z to 2026-11-13T09:01:06.704685Z
instruments: scripts/robots_gate.py (OpenAI provider), Python urllib without automatic redirects, HTMLParser, Poppler pdftotext/pdfinfo/pdftoppm
publication: approval-blocked; this is local working material

# What internal measurements repair the outage panel's missing links?

**In short.** This audit finds measurements of AI code, review and incidents in two operator papers, but no direct staffing-to-expertise-to-recovery chain. Collection has stopped; evidence and reader checks are complete and the final recheck is complete.

## Answer

**Interpretation.** The two preselected operator accounts make AI exposure, review and incident associations more observable than the outage panel did. Neither supplies the missing staffing-to-knowledge-to-recovery chain. This is a limit of the audited evidence, not a finding that capacity has been preserved or lost. The second and final exploratory iteration ends here.

## Findings

The [measurement matrix](operator-measurements.csv) is the source-level record. It audits exposure, clocks, denominators, outcomes, comparisons, confounders, provenance, review/knowledge measures, staffing, causal wording and missingness. Its rows distinguish reported evidence, interpretation and non-disclosure. These are operator claims, not independently measured effects.

- **RADAR:** selected automation comparisons do not establish causal safety. Its knowledge-transfer assurance lacks a corresponding reported measurement in the paper. The claimed >330% latency reduction cannot be used as an ordinary percentage reduction (I2-S01/I2-S02; matrix I2-M03, M07-M14).
- **Mockus et al.:** preserve the distinction between raw AI-heavy comparisons and adjusted association; the abstract and main text do not state the same contrast. Neither a favourable coefficient nor a tenure proxy establishes retained understanding (I2-S03/I2-S04; I2-M18-M28).

The useful repair is linked internal measurement with explicit coverage and comparison, rather than another public outage selected after its outcome. The papers do not repair the organisational attribution on their own.

## Method

The conditional checkpoint was committed before collection. Both exact known record URLs were resolved directly; each linked one fullpaper. All four documents were readable after the repository gate allowed OpenAI and Lighthouse-research. No challenge, login, refusal or redirect occurred. No discovery query or source substitution was needed. No source instructions were followed as authority; no contact details remain in the retained text after the correction below, and no exposed host was visited.

[Sources](sources-iteration-2.json) separate publication/version dates, observation windows, collection clocks and HTTP Last-Modified headers. [Reads](reads-iteration-2.jsonl) retain individual robots decisions, request times, response hashes, bytes and measured duration. The collected_utc and evidence read_utc fields mark gate/collection-procedure start, not exact substantive-read time; the log separately records substantive request and completion clocks. Full-paper bodies and extracted text remain temporary scratch for the fresh verifier; git retains only located paraphrases and locator files under [data/iteration-2](data/iteration-2). Each source's matrix paraphrases total fewer than 150 words; locator files do not duplicate them. The PDF's model table and outcome qualification were also visually checked on pages 93:11 and 93:14.

Footprint: four substantive HTTP requests, four robots requests, zero redirects, zero discovery queries; 1,339,839 response-body bytes and 53.943 seconds summed HTTP duration. This excludes local analysis and unmeasured orchestration overhead. Codex/OpenAI is known; authoritative exact model ID, token totals and dollar pricing/usage are unavailable. Missing cost is not zero. The two papers concern the same operator, with overlapping authors; they are different evidence types from the outage panel and not independent company replications.

## Limits

The audit cannot replay private telemetry, verify incident attribution, recover undisclosed denominators or infer team departures from silence. Outcome proxies do not cover every defect, customer consequence, learning effect or recovery skill. Selected low-risk work, incomplete provenance, ordinary automation, changed demand, evolving tooling and reporting omissions remain competing explanations. The matrix's missing fields must stay missing. Source disagreement in summary wording is retained without pretending to resolve unlike statistical contrasts.

## Next: measurements a willing collaborator would need

Design suggestion only; no outreach or new experiment. Fix a service/team unit, dates, follow-up, attribution and missingness rules before reading outcomes. Link:

- Dated AI/task provenance and ordinary automation to staffing/role changes, relevant service experience, on-call coverage, handover and the documented decision rationale.
- Incoming demand and change risk to review waiting, active checking, rejected changes and errors caught; measure relevant understanding, diagnosis ability and shared coverage separately from elapsed review time.
- Deployments/service-time denominators to incident severity, customer effects, detection/diagnosis/recovery intervals, near misses and successful operations.

Compare within service and against credible contemporaneous work with similar demand and risk; assess pre-trends, selection, concurrent changes and spillovers. Declining understanding and recovery after a documented capacity change, beyond work-mix/demand changes, would support expertise loss. Preserved or improved understanding and recovery would challenge it. Review latency alone distinguishes neither expertise loss nor ordinary queue pressure. Richer observational records still require a defensible identification strategy for causal claims.

## Corrections

0.1, 13 November 2026: first local measurement audit. No further collection authorised by this note. Fresh evidence review, reader-and-inference review and any required recheck remain with the driver. No commit, push, upload, publication or issue closure was performed by this analyst.

0.2, 13 November 2026 (version 0.1 was an uncommitted working draft, with no earlier public edition): evidence review clarified HTTP timing and collection-clock labels and found that the publisher HTML cache had been saved before email redaction. The driver removed 27 email-pattern matches from that temporary HTML; public evidence and extracted texts contained none. The manifest preserves the received-byte hash separately from the corrected cache hash. Binary PDF pattern matches were not confirmed emails; its extracted text had none and it remains temporary, not a repository source. The required plain opening was added. These corrections do not change the measurement or attribution conclusion; the original-response metadata and log remain unchanged, while the raw pre-redaction HTML cache is no longer retained.
