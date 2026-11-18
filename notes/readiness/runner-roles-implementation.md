# Runner reliability and focused roles

**In short.** Lighthouse can now start Watch, Research, Horizon or Editor sessions against the same queue, while the original all-purpose kickoff still works. A small Git helper confirms a single eligible claim on main before authorising work and keeps a losing claim off the session branch. This is preparation for a separately approved scheduler rollout; no production trigger, study or research outcome was changed.

## Survey and decisions

Surveyed main at `60d495030be9697973ca37369ed19dc97530b9c8`, including the 17 November evening ARTEX work. Read AGENTS.md, runner.md, model.py, check.py, the claim/model tests, readiness implementation account, Horizon and Editor plans and runs.csv. The recent checker change warns about future-written timestamps; the recent session instructions bound concurrent subagents. Both are retained. The queue has 569 rows at this snapshot, including ARTEX's completed first round and pending second-round reviews; none was reinterpreted or changed.

The earlier review's central finding holds: the existing readiness and evidence machinery can be reused. The narrow weakness was the instruction to merge after a losing claim push: a locally committed losing claim could survive reconciliation and later reach main. `schedule/claim.py` isolates that tentative commit in a disposable detached Git worktree. It fetches main, requires a clean synchronised session checkout, evaluates readiness with the actual clock, checks the role, changes only the selected CSV record and attempts an ordinary fast-forward push. A successful push and local fast-forward are both required for a successful exit. A rejection or ambiguous network failure authorises no execution and never causes an automatic retry.

No task executor, lock service, worker registry or new readiness layer was added. Completion still commits retained work, verifies authoritative ownership, merges concurrent changes, validates and fast-forwards main. Six-hour recovery still requires evidence reconciliation; it does not expire ownership or license another observation. Manual reconciliation and the manual claim procedure remain documented for exceptional cases.

`roles.py` selects work from existing fields without modifying the queue or readiness contract. Horizon takes `study=horizon`; Watch takes observations and the existing watch log; Editor takes site maintenance; Research takes the remaining scientific work, including closure decisions and protocol plans. At the surveyed snapshot the unfinished selections are 158 Watch, 209 Research, 16 Horizon and two Editor rows. The daily reader visit is an Editor duty even with no ready maintenance row. Default CLI output and JSON remain compatible; an explicit role adds a selection alongside the unchanged global report.

The shared runner contains the common procedure once. The profiles say where each role stops and hands over through existing rows and retained output. Editor owns the digests and independent reader visit, reading all intervening outcomes. Necessary corrections to public claims remain reviewed, minimal patches against current main, so a known false summary never waits for a later editorial slot. The all-purpose runner retains the whole pass and reader visit for compatibility and rollback.

## Verification

- `python3 -m unittest discover -s schedule -p 'test_*.py'`: 56 tests run, 54 passed and two pre-existing opt-in migration audits skipped. Those one-time audits intentionally do not freeze subsequent legitimate research.
- Eight new integration tests use local bare Git remotes and separate checkouts. They cover competing claims from the same base, authoritative ownership on retry, lost acknowledgement after an accepted push, completion while main gains another task's claim and another file, interrupted/stale work reconciled from retained evidence, dates/blocks/review dependencies, role handovers, default CLI/JSON compatibility, dirty/unpublished work and byte preservation of unrelated multiline CSV records.
- `npm test --prefix site`: all 63 tests passed after the site was built. `node scripts/lineage/overview.mjs --check` passed.
- Site builds and `python3 scripts/lineage/check.py` passed for `/` and `/lighthouse/`, with no link-check failures. The prefixed build initially exceeded Node's default 2 GiB heap; it passed with `NODE_OPTIONS=--max-old-space-size=4096`. No runtime configuration was changed.
- Additional offline regression scripts passed: LH010 (12 tests), LH015 (30 cases), LH017 (51 cases), LH032 (five tests), LH044 (zero failures) and LH048 (15 tests). They used synthetic or retained inputs; no new scientific collection occurred.
- Local Playwright acceptance was attempted but Chromium failed before opening a page because this host denies its singleton socket. The repository's existing PR workflow runs browser acceptance on both prefixes; local browser verification is not claimed.
- `git diff --check` passed. The research queue, model, run/cost history, studies and workflow definitions are byte-unchanged from the surveyed main. Generated site-verification result files were kept out of the PR.

A [fresh independent technical review](runner-roles-review.md) found one ambiguity: an empty Editor queue could skip the daily visit. The instruction was corrected and rechecked; no remaining must-fix issue was found. The reviewer also tested the lost-acknowledgement case independently. This is engineering review, not scientific confirmation. Exact model usage prices are unavailable.

## Rollout still required

John's approval is required before merge or production scheduling changes. Separately inspect the actual external kickoff, push permissions, fresh-review and browser capabilities. Choose times that preserve every fixed observation window, provide timely Watch-to-Research and Horizon-to-Watch handovers, retain the Tuesday/Friday sweep cadence and use one Editor slot daily after the relevant site builds. Do not overlap the old all-purpose trigger with focused triggers. Check early run identities, evidence references, ownership recovery and daily costs.

The live scheduler and its timing have not been inspected in this PR. Editorial visit deduplication deliberately uses retained notes and a single rollout slot rather than a second lock mechanism. Interrupted or ambiguous work still needs evidence-based reconciliation. Rollback selects the all-purpose kickoff on the current queue, preserving all newer evidence and outcomes.
