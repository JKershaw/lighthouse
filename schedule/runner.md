title: The scheduled run
kind: working instructions (for any agent, on any provider)
date: 2026-10-30

# The scheduled run

**In short.** Each daily pass preserves expiring evidence, then takes ready work through analysis, checks and publication to a meaningful checkpoint. The queue says what each task needs; a future observation does not defer an answer that can already be supported. Every study's methods, resource stops and end date remain in force. This file also supports four focused roles; it installs no triggers.

A scheduler starts an agent in a checkout of https://github.com/JKershaw/lighthouse with one line: *"Follow schedule/runner.md."* The run starts from `origin/main`. Getting a checkout that can push is the kickoff prompt's job, since it differs by harness; a run that cannot push reports that limitation. This repository does not install a timer. Read AGENTS.md first; its last section has notes for Claude Code.

## Choose a role

With no role named, this is the original all-purpose runner: all eligible work and the editor's visit. For a focused run, the kickoff is *"Follow schedule/runner.md as Watch"* (or Research, Horizon, Editor). Read the matching profile in [roles.md](roles.md), then use the shared steps below. `python3 schedule/check.py --role watch` selects that role's ready work; `--role research`, `horizon`, `editor` and `all` work the same way. The unfiltered queue, waits and warnings remain visible; `--json --role …` adds a `selection` without changing the global readiness contract.

A role is a work filter, not permission to bypass readiness or scientific rules. Do not take another role's queue work just because this run is idle. Hand it over through its existing row and retained reference, not another copy of the task. All-purpose runs remain available for rollback; do not schedule them alongside the focused roles during rollout.

## The table

`schedule/due.csv` has one row per promised deliverable:
`id,study,task,earliest,latest,status,updated,by,ref,note,kind,depends_on,run_id`.

- `kind` is `plan`, `observe`, `analyse`, `review`, `publish` or `maintain`. An observation attempt is distinct from analysis or a review.
- `depends_on` is a semicolon-separated list of row IDs, all of which must be `done`. Unknown IDs, self-dependencies and cycles are errors. Empty dependencies do not clear an explicit block.
- `earliest` is a genuine not-before date, inclusive in UTC. Leave it empty when dependencies alone determine availability. `latest` is a deadline, inclusive, not evidence that prerequisites exist. Late collection still needs the brief's permission.
- `run_id` is the public identity of the run that claimed this work. Use the same identity in `runs.csv` and `costs.csv`; `by` says who performed it. New run IDs use a UTC start instant, provider and distinguishing public suffix, for example `2026-11-14T110000Z-openai-readiness`. Never use a private provider session identifier. Creating a future row does not assign it to the creating run.

Stored statuses:

- `open`: unfinished. It is ready only when prerequisites and its not-before restriction permit action.
- `running`: owned by a claim on main; `updated` is the timezone-aware claim instant. A claim older than six hours needs reconciliation, not automatic duplicate execution.
- `done`: the promised outcome is met and `ref` names its retained evidence, file or commit. An unavailable observation can complete an attempt without satisfying a substantive-evidence gate. A review is done only when its named check clears the recorded version; unresolved fixes remain explicit work and block release.
- `missed`: the window closed without the required observation; record the gap under its brief. Never invent a reading.
- `blocked`: `note` names the unmet external, evidence or harness condition. Clear it only after retaining evidence that the condition is met.
- `keeper`: `note` holds a decision only the keeper can make, with options and a recommendation.
- `cancelled`: no longer needed; `note` records the stop condition or reason.

Historical terminal rows retain their old facts, and their run identities stay blank where unestablished. Every row has a kind: the 136 historical rows without one were given it on 18 November 2026, at the keeper's request, from later rows of the same task or from their task text ([the mapping](../notes/readiness/kind-backfill-2026-11-18.csv), [its script](../notes/readiness/kind_backfill_2026_11_18.py)); a new row always states its kind. Missed and cancelled rows do not satisfy dependencies. Where a brief permits a final answer with gaps, use an explicit collection-closure task recording those gaps and the stop decision. Split repeatable or combined deliverables into separate tasks. Publication checks the actual draft version and its cleared reviews; the graph alone does not certify scientific correctness.

`python3 schedule/check.py` validates the queue and lists ready work, waits, stale ownership and advisory coverage warnings. The site consumes the same model. `--json` gives its versioned data contract; `--root PATH --now 2026-11-14T11:00:00Z` supports deterministic fixtures. The legacy positional date means midnight UTC at the start of that date and cannot be combined with `--now`. Invalid input yields diagnostics and no executable action list. Coverage warnings prompt a brief-to-queue audit; they cannot prove that every promised stage has a row.

## A run

1. **Start clean.** Fetch `origin/main`, branch from it, choose a unique public `run_id`, and run the checker. Fix queue errors before selecting work. Reconcile stale claims against main, the owning run's branch/commits, run records and retained output before reopening anything; never refetch an existing read. More than six hours is a recovery warning, not a lease expiry. With retained output, finish or hand over from it. Reopen only after establishing that the required attempt did not happen and recording that evidence and the brief's permission for any late read. If execution or ownership remains uncertain, leave the claim in recovery or record a named block and a continuation; do not steal or refresh it merely because it is old.
2. **Claim the ready frontier.** Within the role, preserve expiring evidence first, soonest deadline first, then take the highest-priority ready analysis, reviews and publication before discretionary intake. Claim only work you will now do, not its future chain. From a clean checkout with finished work already on main, run:

   `python3 schedule/claim.py <row-id> --run-id <public-run-id> --by '<attribution>' --role <role>`

   Omit `--role` for the all-purpose runner. The helper fetches main, fast-forwards the clean session branch, evaluates the authoritative queue with the real UTC clock and publishes just this row's claim from a disposable worktree. It changes no other records. It never pushes unpublished session work or retries a rejected push. Only exit status 0 and "Claim confirmed on main" authorise execution. On any failure, start no work: fetch main and inspect the row, retained output and any ambiguous successful push. Another owner means leave it alone. A network failure may mean the claim reached main even though confirmation was lost.

   The manual equivalent remains valid: set `running`, timezone-aware `updated`, `by` and `run_id`, commit, then fetch and fast-forward main. If a push loses a race, **do not merge the losing claim commit and push it later**. Read the authoritative row first; discard only your unaccepted claim edit, retaining unrelated work. If another worker owns or completed it, do not execute. If it is still ready, make a new claim based on current main. Never force push.
3. **Do and retain the work.** Follow the brief and its latest checkpoint. Before any source read set `LIGHTHOUSE_PROVIDER` (`anthropic` under Claude Code, `openai` under Codex) and obey robots.txt under AGENTS.md; use `python3 -I scripts/robots_gate.py <url>...` for collectors not yet gated. Label reads with their collector's UTC start minute and skip retained reads. Keep source observation windows distinct from task windows. Write the checkpoint and the PHP daily log when applicable. Mark the outcome with its supporting reference, or an explicit gap/block/keeper decision. Flag anything that could change a public account for the required fresh reviews.
4. **Commit and re-evaluate.** Before committing a completion or returning unfinished work, fetch main and verify that its row is still `running` under this run's exact `run_id`. If ownership or outcome changed, reconcile the retained evidence rather than overwriting it. Commit each meaningful completion, merge current `origin/main` without rewriting history, and run the checker again before fast-forwarding main. A conflicting row is a decision to reconcile against both retained outcomes, never a reason to choose an entire "ours" or "theirs" queue. Preserve concurrent run-log and cost rows as well. If a push is rejected, repeat the fetch, ownership check, merge and validation; do not repeat the scientific work. A newly ready task for this role can proceed in this same pass; other roles see the handover through the shared queue. Keep unresolved review fixes explicit; changed claims require clearance for the actual version released. Do not extend collection to finish reviews. Return unfinished owned rows to `open` with a concrete continuation, or retain the genuine named block.
5. **Keep promises and finish ready work.** Within the role, audit active briefs and records for missing analysis, review and write-up rows, even when future observations already exist. Add a row only for commissioned work; an uncommissioned suggestion belongs in proposals.md. Prefill recurring reads to the fixed end, or eight weeks ahead for a genuinely continuing cadence. Cancel later rows when the stop condition is met. Advance the highest-value ready work to an evidenced checkpoint and a reviewed piece when earned. Some studies end in a retained record rather than an article. Preserve all fixed methods, source bounds, resource stops and end dates.
6. **Report the outcome.** Append one line to `schedule/runs.csv` (`started,by,did,commit,run_id`, retaining `plain` if present). `started` is the UTC start label; `did` says what was captured, analysed, reviewed or released, with genuine blockers separately; `commit` identifies the outcome commit or stays empty when the line is its only change. New stage counts use only rows with the exact run identity; historical narratives stay historical. Record costs below. Commit the run record, merge current main if necessary, fast-forward main and check its site build. Keep both records when concurrent runs append. Even a run with nothing ready records its outcome, so the daily site build refreshes the calendar.

7. **The editor's visit, last (Editor or all-purpose only).** Follow [the editor's plan](../notes/editor/plan.md), including the independent reader, daily updates, reviewed learned block and build checks. Watch, Research and Horizon skip this step and leave editorial handovers in their run records. They maintain the factual state of their own records, investigation pages, programme and AGENTS.md's "Where things stand" when it changes; they do not regenerate the front-page digests. A necessary correction to an existing public claim still takes precedence and needs its existing reviews, with a minimal patch reconciled against current main. Never leave a known false summary waiting for a visit.

## What waits for the keeper

AGENTS.md's three things wait for a person: a claim by Lighthouse that harm is happening now, a claim by Lighthouse that a named system is compromised, and anything irreversible outside the repository. For a run that nobody watches, these also wait:

- contacting anyone outside Lighthouse. Lighthouse works from public sources and does not contact outside organisations (the keeper, 1 November 2026): never draft outreach, and never write a row that asks a question of an outsider. Where public sources are silent, the record says the thing is unknown;
- changing the charter, AGENTS.md's rules (its sections on how a session goes, rules, evidence and writing, and its notes for Claude Code) or this file. Keeping AGENTS.md's "Where things stand", programme.md, the investigation pages and the front page current is ordinary work after a release or a finding, and does not wait;
- taking on a paid service, an account or any standing cost outside the agent runs themselves;
- opening a new investigation. Put it in proposals.md's "Waiting for the keeper" instead of a `keeper` row.

Mark the row `keeper`, put the question in its note with the options and your recommendation, and carry on with everything else; a block is expected and costs nothing. A `keeper` row holds a decision only the keeper can make; it never asks the keeper to do work, and no run creates work for the keeper. Rows come from briefs, records, proposals started or agreed in proposals.md, and what the keeper has asked for in their own words, not from a remark in conversation. Where your harness can file an issue on the repository (or through Harbour), file one titled with the row's id, once, so the keeper sees it; later runs do not raise it again in issues, commit messages or reports. The keeper answers by changing the row or adding a note, in their own session, whenever they choose; a `keeper` row never lapses and is never counted against anyone.

A piece whose reviews find nothing that must be fixed is released, as AGENTS.md says; that does not wait.

## If your harness lacks something

- **No subagents:** the reviews AGENTS.md requires need a fresh agent. Write the record and the draft, then mark the review row `blocked` ("needs a fresh agent") and leave the piece unreleased for a run that can.
- **No web search:** the media sweep and anything that searches is `blocked` for this run.
- **No push to main:** push your branch and mark nothing `done` on main; the next run will see your branch only if you say so in a row's note.
- **A network host refused:** record the read as partial or failed, as the brief says, and move on.

## Proposals

Ideas that are not yet promises live in [proposals.md](../proposals.md), not in this table: the horizon sweep (rows `horizon-<date>`, [its plan](../notes/horizon/plan.md)) adds and ranks them twice a week, and a fresh agent gates each one into a lane. A started proposal becomes rows here when its brief is fixed. Any run may add a proposal it comes across, in the same form, for the next sweep to gate.

## Daily cost reporting

Record each run’s non-overlapping cost components in [costs.csv](costs.csv), using its public `run_id`. Update a component’s row when its estimate changes, so repeated readings and overlapping totals are not counted twice. Use `provider_reported`, `list_rate_estimate` or `unavailable` for `basis`; leave amount and currency blank when unavailable. Keep private provider session identifiers out of the ledger.

Run `python3 schedule/cost_summary.py --date YYYY-MM-DD` for recorded subtotals by UTC day, currency and basis, alongside unpriced components. List further coverage gaps in the usual daily report. Use disjoint component records, never a whole-run total alongside its parts. A partial subtotal is not a total bill. Unknown costs or accounting-summary failures do not block ready work; explicitly commissioned resource stops still apply. Actual provider billing failsafes remain the keeper's control.

## Keeping the table true

Any session, scheduled or not, adds rows when it fixes a brief (every read, checkpoint and write-up the brief schedules) or notices something promised without a row. The table is the schedule; notes may explain it but never replace it.
