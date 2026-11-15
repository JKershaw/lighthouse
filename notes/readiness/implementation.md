# Ready work through to findings

**In short.** Lighthouse now derives task readiness once for both its checker and website, then re-evaluates it after each committed outcome. The queue distinguishes observations, analysis, reviews and publication, so a later observation does not hide an answer that can already be supported. This engineering update preserves the completed daily passes and every study's scientific limits; it collects no new scientific evidence.

## What changed

The keeper commissioned the code survey and implementation on 14 November 2026. The shared standard-library model in `schedule/model.py` validates the table, dependency graph, clocks, references and public run identities. `schedule/check.py` retains the human entry point and exposes a versioned JSON contract consumed by the site. Invalid input cannot produce executable work. Stored outcomes, date constraints, evidence waits and ownership are separate facts.

The runner claims only ready work on main, commits meaningful outcomes and refreshes readiness, allowing analysis and its reviews to advance in the same existing daily pass. It no longer offers a due-rows-only mode. External predicates remain explicit evidence-backed decisions; an unavailable source does not clear a substantive-report gate, and a closure can record missing observations without inventing successful ones. Reviews clear the named version, not merely the existence of comments.

The [migration account](migration.md) and [per-row manifest](migration.csv) reconcile against main at `7a79e2906cf30a8e386553162ef4196e91f8837e`, including the 14 and 15 November scheduled passes. All 346 source rows were audited, all 136 terminal outcomes preserve their original fields, and 159 distinct stages make existing promises explicit. The LH047 draft already completed on 15 November is not commissioned again: its evidence review is ready. The new LH044 read-1 review is retained. Scientific source files are unchanged; four briefs have only appended links to dated operational amendments.

Cost summaries keep currency and accounting basis apart and display unpriced components separately. Accounting-summary failures do not gate the queue or deployment. Existing commissioned study resource stops and provider billing failsafes remain binding. Historical provisional cost-label mappings and their uncertainty are recorded in the migration account; no historical run identity or bill is fabricated.

## Engineering review

A fresh Codex technical reviewer checked the implementation and migration against the approved design and retained sources. Exact runtime model and prices were not exposed. After resolving the findings, the reviewer reported no remaining must-fix issue: the 505-row queue validates, completed work and scientific files are preserved, and substantive-evidence blocks, future observations, protocol order and version-specific review gates remain protected. Corrections included an analysis checkpoint incorrectly typed as an observation, accounting summaries accidentally acting as CI gates, incomplete run identity validation and empty completion references.

This is engineering review, not independent scientific confirmation. The code does not infer scientific approval from a graph or automate research execution.

## Verification and handover

Offline verification includes the model/site shared fixture, malformed schema and CSV, canonical dates, deterministic UTC clocks, stale ownership recovery, dependencies and manual gates, actual observation versus other work, exact public run attribution, accounting gaps, and two local checkouts racing for one Git claim. `python3 schedule/test_migration.py --audit-current` additionally checks this rollout against its source freeze, including scientific file hashes. Its normal tests preserve the migration account without freezing future legitimate research to today's queue.

The production and PR workflows explicitly provision Python. PR verification builds both the root and `/lighthouse/` layouts and runs browser acceptance without JavaScript, at mobile and desktop sizes, in light and dark. Local Chromium could not launch because this host refused a required socket; browser results therefore come from CI, not an invented local pass. The same unit, build, audit and browser commands remain available for later checks.

The external daily timer is not stored in this repository and was not changed. Its exact live kickoff configuration has not been inspected. The retained 15 November commits do show that the native pass executed its advancement step and drafted the LH047 paper. The next normal pass must refresh main, use the canonical runner and demonstrate that ready review or analysis advances while genuine future observations stay protected. No second timer or automatic renewal was created.

Rollback must retain any outcomes committed after migration and restore a coherent table and consumer set together. Never replace newer evidence or completions with the old CSV. Runtime usage pricing for this work is unavailable and is recorded as such in `schedule/costs.csv`.
