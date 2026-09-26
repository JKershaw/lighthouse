title: The first drive: what one bounded tick of the watch showed
kind: retro
version: 0.1
date: 2026-09-26
authors: the driver (Claude Code session, Fable 5.1), for the keeper
grounded_at: ec007fd
cites: harbour/exports/20260926T075104Z/; registers/instruments.md; registers/decisions.md D-0001 to D-0004; notes/Q-0002-model-choices.md; CLAUDE.md; .claude/skills/drive/SKILL.md

## What was attempted

One bounded drive of the watch on 26 September 2026, from 07:24 to 07:51 UTC: boot a local Harbour from the workspace files, take its suggestions, work them through subagents, record what each cost, export, and report. The bound was three dispatches by default and a measured cost limit, both set the same morning. The keeper raised the cost limit to twenty dollars and steered the drive toward outward work after the two instrument tickets.

## What happened

Four dispatches closed with commits: the export's instrument record (I-0001), the host sampler with its own calibration run (I-0002), the survey of surveys (LH003) and the xz essay (LH004). One probe subagent ran to learn which model the launcher's opus alias resolves to. Every ticket was closed in Harbour against its commit, the export carried the feedback, usage and host samples back into the repository, and Harbour's cost endpoint priced every dispatch (observation).

| Dispatch | Model | Calls | Cache read | Cost | Wall |
| --- | --- | --- | --- | --- | --- |
| I-0001 | Sonnet 5 | 25 | 2.34 M | $0.89 | 7 min |
| I-0002 | Sonnet 5 | 42 | 3.81 M | $1.08 | 8 min |
| LH004 | Sonnet 5 | 24 | 2.50 M | $0.89 | 9 min |
| LH003 | Sonnet 5 | 27 | 3.08 M | $1.09 | 11 min |
| probe | Opus 5.5 | 2 | 43 k | $0.23 | 5 s |
| driver | Fable 5.1 | 36 | 8.43 M | $4.28 | 27 min |

Subagents cost $4.18 and the driver $4.28, at list rates (derived measurement; output tokens estimated from characters, all else read from transcripts).

## What worked

- The workspace-as-files loop ran end to end without restarting Harbour: boot, load, next, dispatch, take, post, close, export, down. Nothing was committed that should not have been; the tokens stayed in the ignored directory and the export redacted nothing because nothing needed redacting.
- The founding documents were enough. Four subagents that had never seen the project produced records in the house form, with the four kinds of statement labelled, unfillable fields left blank with reasons, and no dash violations, from AGENTS.md, F02 and F05 alone.
- Measured cost replaced estimates. Reading spend from transcripts corrected the previous day's note, gave Harbour real usage entries, and made the cost bound enforceable rather than nominal.
- Harbour's next-run tracked the backlog. Its first suggestion put the instruments first, which was right for the seed; after the outward tickets were filed its second boot put the articles first (observation).
- Two research records on others' observations, LH003 and LH004, came out of one morning, which is the first of the stages an observing agent set out that day.

## What did not

- The launcher's token figure is the subagent's final context size, and the previous day's note had priced it as spend. Corrected; the lesson is that a number's meaning must be checked before it is multiplied.
- The rule of one subagent at a time cost wall time for no information once the cost limit stopped binding. The keeper relaxed it; the skill should say when parallel runs are allowed (when the limit is far and the tasks touch different files, with the driver committing).
- Subagent effort cannot be set from the launcher; today's ran at xhigh, the previous day's at max, inherited from the driver.
- The driver is half the spend. Every turn re-reads a context of about a quarter of a million tokens. Fewer, longer turns are the lever, and the driver's own usage is measured but not yet in the ledger, because no Harbour dispatch represents it.
- Two ticket texts predated the day's design: I-0002 told its subagent to post to Harbour, which subagents may not do. The driver posted instead. Ticket text should be reread against the current rules when a ticket is dispatched.
- Requests per destination cannot be observed on this host, so the sampler's most outward field stays empty, and Harbour's own model spend has no workspace-level read.
- The export copied roadmap and next-run content from session files and checked no HTTP status. Fixed the same day as I-0003, version 0.2 of the instrument.

## What changes

- Opus 5.5 takes the tasks that need reasoning (D-0002). Sonnet 5 keeps collection and tabulation.
- Outward work is not gated by LH001 (D-0003). LH002 is filed on a historical window. Editing is its own ticket, E-nnnn.
- F02 gains a Correctness surface (D-0004), because the earliest xz signal was a sanitiser's output that no surface would have recorded.
- The ledger (L-0001) is next among the support tickets, so that cost per study is in the export rather than in a driver's report.
- The drive skill keeps its count and cost bounds and gains a parallel-runs clause.

## Limits

One drive on one morning, four tasks on one model. The cost figures depend on a price table read that day and on an output-token estimate. Wall times include waiting on fetches. The driver's cost is for the drive window only and excludes the tooling written before it.
