---
name: drive
description: One bounded tick of the Lighthouse watch. Boots Harbour from the workspace files, works Harbour's next suggestions from the known programme through subagents within a count and a cost bound, records measured spend, exports, commits and reports. Invoked by the keeper, never started by an agent on its own.
argument-hint: "[max dispatches] [max USD]"
disable-model-invocation: true
---

# /drive

Run one tick of the watch, bounded. The first argument is the most dispatches this drive may make (default 3, never more than 5). The second is the most it may spend on subagents in dollars as `hb usage` measures it (default 20, per D-0001; Claude spend is subscription, priced at list rates as a measure). `/drive 1` is one dispatch. `/drive 0` boots, asks Harbour for its suggestion, reports it and stops.

## Bounds

- Dispatches: at most the count given, one subagent per dispatch. Run them one at a time when the cost limit is near, so that each cost is known before the next starts. Runs may be parallel when the limit is far, the tasks touch different files and the driver does the commits; then `hb usage <id> --agent <agent>` names each transcript rather than `--latest`.
- Cost: before each dispatch, sum the `costUsd` of the usage entries posted in this drive; at or over the limit, stop. One dispatch may overrun the limit, since its cost is known only when it ends. Report the overrun; never follow it with another dispatch.
- Programme: only tickets already in `harbour/tickets.json` whose status is not done, in the order Harbour suggests. The drive files no tickets and edits no ticket text. Proposed tickets go in the report for the keeper.
- Harbour's own model: one `hb next` per drive. `hb roadmap` only if a ticket closed in this drive and the report would change what comes next.
- Documents: the founding documents change only when a ticket asks for it.
- Never: publish, create a scheduled routine, change Harbour, alter the budget, read a credential the task does not name, or write a token, a session id or an agent id into the repository or into a Harbour entry.

## Stop early when

- a dispatch ends `[failed]`, or its subagent reports nothing usable;
- Harbour's suggestion is outside the programme, or would need a person under Harbour's charter (anything irreversible, money, a release);
- `hb up`, `hb load` or a token mint fails;
- the cost limit is reached.

Stopping early is not a failure. Say what stopped the drive and leave the rest for the next one.

## Procedure

1. Note the start time. `harbour/hb up`, `harbour/hb load`, `harbour/hb next`. Read the suggestion against the bounds.
2. For each dispatch: `hb dispatch <ticket> <kind>`, then `hb take`. Spawn one subagent with the taken prompt, the repository path, AGENTS.md, a scratch directory and the two rules in CLAUDE.md. Model by kind (D-0002): `opus` for research, essays, study write-ups and review; `sonnet` for collection scripts, source checks and tabulation; `haiku` only for a chore the driver cannot do with `hb`.
3. When it reports: `hb feedback <id> "<what was done>"`, `hb usage <id> --latest`, `hb resources <id>`, then `hb done` or `hb failed`. Commit the deliverable. `hb close <ticket> "<message naming the commit>"` when it is done.
4. After the last dispatch: `hb export`, `hb down`, `hb drivercost --since <start time>`. Commit and push.
5. Report.

## Report

Under a hundred lines, in this order: what Harbour suggested and what was dispatched; one row per dispatch with ticket, model, calls, cache read tokens, cache creation tokens and cost; the driver's own measured cost for the drive; what was learned, each point labelled observation or interpretation; what was left undone and why; proposals for the keeper, not filed.
