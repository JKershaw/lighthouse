title: The scheduled run
kind: working instructions (for any agent, on any provider)
date: 2026-10-30

# The scheduled run

This file is the whole of a scheduled run of Lighthouse. A scheduler starts an agent, in a checkout of https://github.com/JKershaw/lighthouse, with one line: *"Follow schedule/runner.md."* A scheduler that should only keep promises adds: *"Do the due rows and the gap sweep only, not step 5."* Whatever branch the harness checked out, the run starts from `origin/main` (step 1). Several schedulers on different providers may fire at different times; the steps below are written so that two runs never do the same work twice and a run that never happens harms nothing. A person's own sessions run alongside and follow the same table.

Read AGENTS.md first: it is how Lighthouse works, and nothing here overrides it. CLAUDE.md has notes for Claude Code; other harnesses skip what does not apply.

## The table

`schedule/due.csv` holds everything Lighthouse has promised to do, one row each: `id, study, task, earliest, latest, status, updated, by, ref, note`. A row is due when today (UTC) is inside its window; an empty `latest` means open-ended. Statuses:

- `open`: not yet done.
- `running`: claimed by a run; `updated` holds the claim time (e.g. `2026-11-02T06:35Z`) and `by` the run's label. A claim older than six hours is stale and counts as open.
- `done`: `ref` names what shows it (a read directory, a file, or a commit).
- `missed`: the window closed without it; `note` says why, and the study records the gap as its brief says. Never invent a reading to fill one.
- `blocked`: cannot be done by this kind of run (for example, a review needs a fresh agent and this harness cannot start one); `note` says what it needs.
- `keeper`: waits for the keeper; `note` holds the question, the options and a recommendation.
- `cancelled`: no longer needed; `note` says why (for example, a study's stop condition was met).

`python3 schedule/check.py` lints the table and lists what is due, overdue, stale, waiting and coming up, and the gaps it can see.

## A run

1. **Start clean.** Fetch `origin/main`, make a branch `runner/<UTC label>` from it (label: the time you start, `YYYY-MM-DDTHHMMZ`), and run `python3 schedule/check.py`. Fix any problem it reports in the table first.
2. **Claim.** Pick the rows you will do this run: everything due or overdue, in order of `latest` (soonest first), including open-ended rows already due. Do them all unless your harness cannot (then mark the row `blocked` with what it needs) or the run is cut short; a row you claimed and did not finish goes back to `open` with a note on how far you got. Set them to `running` with `updated` and `by`, commit only that, and fast-forward main (`git fetch origin main && git merge-base --is-ancestor origin/main HEAD && git push origin HEAD:main`). If main has moved, merge `origin/main` into your branch (never rebase anything already pushed), re-run the check, drop any row another run has claimed or done, and try again. A claim on main is what stops two runs doing the same read.
3. **Do the rows.** Each row's study directory has its brief, its scripts and its latest checkpoint; follow the brief and do what the task says, the way the last checkpoint did it. Label every read with the UTC minute its collector starts; never refetch a retained read; collectors skip what is already held. Write the checkpoint and, for PHP watch reads, the day's line in notes/php-watch-log.md. Mark each row `done` with its `ref`, or `missed`, `blocked` or `keeper` with a note. If a row turns up something that would change a public account (examples in notes/php-watch-continuation-2026-10-23.md), record it in the checkpoint and the log, mark it flagged for review, and say so in the commit message.
4. **Sweep for gaps.** Add a row for anything promised that has none: a brief or a record's "Next" that names a date or a read with no row, a study whose newest read is older than its brief's cadence, a question a checkpoint raised. Prefill recurring rows at least eight weeks ahead, or to the brief's end. When a stop condition is met, cancel the later rows with the reason.
5. **If there is room, take the next thing.** With the due rows done, do the next item in programme.md's Next the way AGENTS.md describes a session: one item, through to its record and, if it earns one, a reviewed piece. Claim it first, as in step 2: add a row for it (`id` naming the work, for example `LH036-brief`; empty `latest`; status `running`, with `updated` and `by`), commit only that row and fast-forward main. If another run has already claimed the same item, take the one after it. Mark the row `done` with its `ref` when finished, or set it back to `open` with a note on how far you got if you stop early, so the next run can carry on. Add the work's own rows to the table when you fix its brief.
6. **Finish.** Append one line to `schedule/runs.csv` (`started,by,did,commit`: your start label, who you are and on which provider, a few words on what you did, and the commit, or empty if the line is your only change). Commit once with what was found and what was spent, merge `origin/main` if it moved, fast-forward main, and check that the site build for that commit succeeds. Always commit at least the line in `runs.csv`, even when nothing was due: every push to main rebuilds the site, which keeps the schedule page's date true, and the log shows the schedulers are alive. If two runs both appended, keep both lines.

## What waits for the keeper

AGENTS.md's three things wait for a person: a claim by Lighthouse that harm is happening now, a claim by Lighthouse that a named system is compromised, and anything irreversible outside the repository. For a run that nobody watches, these also wait:

- contacting anyone outside Lighthouse (draft the message in the repository; the keeper sends it);
- changing the charter, AGENTS.md's rules (its sections on how a session goes, rules, evidence and writing), CLAUDE.md or this file. Keeping AGENTS.md's "Where things stand", programme.md, the investigation pages and the front page current is ordinary work after a release or a finding, and does not wait;
- taking on a paid service, an account or any standing cost outside the agent runs themselves.

There is no spending limit on a run itself: do what it takes to keep the table current and the work moving, and record the spend in the commit message and the run's line. The keeper watches the total.

Mark the row `keeper`, put the question in its note with the options and your recommendation, and carry on with everything else; a block is expected and costs nothing. Where your harness can file an issue on the repository (or through Harbour), file one titled with the row's id, so the keeper sees it. The keeper answers by changing the row or adding a note, in their own session.

A piece whose reviews find nothing that must be fixed is released, as AGENTS.md says; that does not wait.

## If your harness lacks something

- **No subagents:** the reviews AGENTS.md requires need a fresh agent. Write the record and the draft, then mark the review row `blocked` ("needs a fresh agent") and leave the piece unreleased for a run that can.
- **No web search:** the media sweep and anything that searches is `blocked` for this run.
- **No push to main:** push your branch and mark nothing `done` on main; the next run will see your branch only if you say so in a row's note.
- **A network host refused:** record the read as partial or failed, as the brief says, and move on.

## Keeping the table true

Any session, scheduled or not, adds rows when it fixes a brief (every read, checkpoint and write-up the brief schedules) or notices something promised without a row. The table is the schedule; notes may explain it but never replace it.
