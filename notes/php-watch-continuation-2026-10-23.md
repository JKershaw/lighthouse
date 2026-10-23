# PHP watch: assessment and continuation plan

**23 October 2026, 16:36 UTC.** Prepared by Codex (GPT-6.1 Sol) after the keeper agreed that Lighthouse preserves evidence well but needs stronger investigation and reader updates. This is a decision and handoff note, not a study protocol or a released article. Model spend is unknown. The keeper authorised committing and pushing continuity records so another session can continue without this conversation. Leave publication to the keeper's merge; do not merge automatically.

## Start here next session

1. Read AGENTS.md, this note and programme.md's latest Next entry.
2. Inspect https://github.com/JKershaw/lighthouse/pull/28. If open, fetch its current `lh028-rapid-20261022t1600z` head and append without force. If merged, branch from current main and open a new draft PR. Check for other open continuation work before duplicating it.
3. Read the newest LH028 checkpoint and snapshot. Do not refetch a rapid slot already retained. Carry on with **Priority 1 below**, rather than merely collecting another snapshot.
4. Before stopping, commit and push completed work, update this note's progress section and leave an exact next action. Do not depend on scratch storage or chat history for continuity.

## Where we are

- PRs #26 and #27 merged. The 22 October reader account is `articles/php-emergency-first-reading.md`, with a short form and two SVG figures. Evidence review R-0029 and reader reviews R-0030/R-0031 cover that edition.
- Draft PR #28 contains five rapid snapshots: 22 October 16:00/22:00 and 23 October 04:00/10:00/16:00 UTC, plus checkpoint notes in `studies/LH028/checkpoints/`. All have retained raw responses and successful offline replay. At this handoff its head is `4fd3e4c1d6e70d41718630f39405194e73762f27`, tree `134586f4b1569b8869d276e8c92af4597d3e30d0`. Recheck rather than assuming those remain current.
- Cloudflare's 22 October revision changed defensive rule descriptions and response-firewall wording. Its 23 October revision introduced a related vulnerability, CVE-2026-115560, and a condition on WAF coverage. The checkpoint attributes those claims to Cloudflare.
- Amazon's direct endpoint has consistently yielded the same 195-byte placeholder. The initial article was available through a separate web reader; its text is not raw-replayable in LH028. Do not treat repeated placeholders as observations of the article.
- OpenAI's visible article text has not changed across these rapid snapshots. Raw HTML hashes changed, which alone is not a claim revision.
- LH018 to LH026 provide selected packaging, publisher, CI and image evidence. A published image is not a running deployment. LH021 found that the selected CI records did not expose a complete resolved-input-to-published-output chain. LH027's selected operator notice returned 403; the service consequences remain unknown to that instrument.
- Scheduled rapid LH028 capture is intended through 24 October; LH024/LH025 have separate daily observations through 28 October; LH019 has checkpoints on 24 and 28 October. Inspect actual automation state and retained results before relying on a schedule. This note does not guarantee that future runs have available credits, tools or source access.

## Assessment and chosen direction

The fixed watch is useful for preserving source revisions and keeping unlike evidence apart. Its principal gaps are new-source discovery, following consequential leads, moving findings into the reader account, and measuring downstream effects. A fixed panel should constrain comparable measurements, not prevent a separately labelled investigation from following an important lead.

Three options were considered: continue the same captures, repair the collection-to-reader loop, or launch another outward measurement. **Repair the reader loop first while retaining the existing captures**, then conduct a bounded discovery pass and choose one feasible outward measurement. Extra unchanged snapshots cannot themselves answer uptake or AI impact. The standing LH013 baseline remains in the programme; the PHP work is a time-sensitive exception, not cancellation of it.

## Priority 1: verify and prepare a dated reader update

The immediate next action is to retain and read PHP's original 23 October notice, then draft a short dated Later evidence notice near the opening of the current PHP article. This is separate from LH028's fixed panel. Do not silently add it to that panel or retroactively change a prior checkpoint.

**New primary-source context already seen:** during the keeper's assessment conversation on 23 October, a web reader opened https://www.php.net/archive/2026.php#2026-10-23-1. PHP's notice says the related issue requires an unusual combination: configuration initially uses `php_binary` or `php_serialize`, application code changes the handler to `php` at runtime before `session_start()`, and session upload progress remains enabled. It recommends `session.upload_progress.enabled=0` until the next regular bugfix release, says users who already applied that mitigation can keep it in place, and says applications that never change the handler at runtime can keep the feature enabled. The full advisory for CVE-2026-115560 is planned with the next release. No raw response was retained from that web-reader assessment. These outcomes are prior knowledge, not prospective discoveries for a future brief.

This context qualifies the broad impression of Cloudflare's phrase about fully patched releases. The new issue does not erase the distinction between the original two fixes and a related, configuration-dependent risk. Recheck the current PHP notice and retain its bytes and read clock before relying on it in publication. Check the linked original advisory if needed to understand the mitigation history; bound and log that follow-up separately.

Deliverables and completion gate:

- A retained primary-source record with URL, response status, actual UTC read time, hash, publication clock at its available precision, and the distinction between original fixes and the related issue.
- A concise dated article notice and, where meaning changes, matching short-form, summary and figure annotations. Keep the original as-of account identifiable. Do not call a newly observed claim a newly occurring event.
- A small dated change list the reader can follow. Update the investigation page and programme at the same certainty. Add a release-log entry only when reviewed for release.
- Required evidence and reader reviews under AGENTS.md, resolving consequential changes before presenting the revision as ready. Reviewer agreement is not independent verification of provider operations.
- Push the concrete reviewed update for the keeper to merge. No automatic public release.

## Priority 2: discovery and triage beside the fixed watches

Make one bounded discovery pass: at most six targeted search queries and eight new primary-source pages, stopping after that pass. Fix and log the query plan before the searches, disclose known leads above, and retain complete ranked search results where the connector permits. An incomplete search log stays an explicit limitation. Search results are leads, not evidence.

Look for original incident telemetry, operator precautionary actions, upstream mitigation changes and publishing/CI problems. First consult `notes/proposals/php-patch-information-and-uptake.md` and completed LH020/LH021/LH027 so work is not repeated. Write a short triage ledger with source, actual read time, source's event clock, claim, new information, measurable boundary, access gap, and decision. Classify a lead as a reader update, a candidate measurement, context only, or inaccessible. No completeness or internet-wide coverage percentage follows from this pass.

For attempt telemetry retain the sensor, unit, inclusion rule, numerator, denominator where available and observation window. A cumulative provider count can be reported as such with its missing denominator explicit; do not turn it into a global rate. Keep attempts, successful compromise, preventive action and defensive AI use distinct. Speed and automation do not identify attacker AI use.

## Priority 3: choose one measurable consequence

Preferred next question: **How does a particular mitigation instruction travel through a defined set of public notices?** The 23 October session-upload-progress advice offers a concrete phrase and configuration change to trace. PHP and Cloudflare's outcomes are already known and must be disclosed as such. Before reading other panel members' outcomes, fix an explicit small frame, observation window, retrieval rule and stopping condition in a new brief. Reusing LH024's institutions should disclose overlap and known prior outcomes.

Count notices carrying the exact instruction, qualifications, version claims and explicit source links; distinguish a page's claimed publication/update time from first observation by Lighthouse. Preserve absences and access failures. An explicit citation establishes a public link, not proof of reading, causation or private coordination. Results can describe this panel's communication record, not population awareness or protection.

Run a small feasibility check of source access first. If public histories cannot time the instruction's arrival, report interval bounds or first observation rather than inventing diffusion speed. If the question cannot be measured usefully, stop and instead repair one selected CI chain only where actual runs/logs expose input and output digests. Do not start a broad deployment-uptake estimate without an observable run boundary and denominator. Do not claim a causal effect of AI from this single selected event; distinguish disclosed AI contributions from hypotheses for later comparison.

## Progress and exact next action

- [x] Five rapid snapshots retained, replayed and pushed to draft PR #28.
- [x] Assessment, original-PHP-notice context and continuation decisions recorded here.
- [ ] Retain PHP's original 23 October notice outside LH028 and prepare the reviewed dated reader update (Priority 1).
- [ ] Complete the bounded discovery ledger (Priority 2).
- [ ] Fix a feasible propagation brief before reading its remaining outcomes (Priority 3).

**Next session: start Priority 1 by retaining the original PHP notice and drafting its contextualised Later evidence update.** Preserve any newer concurrent checkpoints. Credentials are not required for the public source reads; never recover old bootstrap tokens from conversation history. Repository publication can use the connected GitHub integration if plain git push lacks credentials; compare complete Git trees and use an expected-head check without force.
