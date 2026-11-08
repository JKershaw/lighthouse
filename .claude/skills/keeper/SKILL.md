---
name: keeper
description: The keeper's seat. Briefs the keeper on what Lighthouse did since their last review and what waits for them, takes their decisions in conversation, and records them.
---

# /keeper

The person running this is the keeper. Put them back in the driver's seat in a few minutes: a short briefing, then their decisions, recorded. This skill reads and records; it does not run studies, sweeps or reviews (that is `/drive` and the scheduled runs), and it never creates a scheduled routine.

## 1. Read, quietly

Start from `origin/main` (fetch it; work on the session's branch). If the branch carries commits not yet on main, say so and offer to push them: the scheduled run reads main, so work left on a branch is work the watch cannot see. The keeper's last review is the time on the line "Last reviewed by the keeper:" in proposals.md. Since then:

- `git log origin/main --since=<last review>` and the lines of schedule/runs.csv since then: what ran.
- releases.md: what was published.
- notes/editor/: what the day's readers made of the site.
- the newest notes/horizon/ sweep file, if it is newer than the last review: what the sweep found.
- notes/php-watch-log.md and any checkpoint that says "flagged for review".
- proposals.md: the started, agreed and waiting sections and every proposal whose Status says "waiting for the keeper", wherever it sits; the throttle; "From the keeper".
- `python3 schedule/check.py`: what is due, overdue or stale, keeper rows, proposals waiting and agreed proposals with no row yet, the next seven days.
- Spend: runs.csv lines and commit messages since then; where they differ, the larger whole-run figure, saying so. Price the keeper's own sessions since then with `harbour/hb drivercost --since <last review>` where the transcript is on this machine, else say they are not priced.

Trust statuses over summaries: "For the next review" and row notes can be older than the keeper's last decisions.

## 2. Brief, in about 400 words or fewer

Plain and warm, precise, no ceremony (AGENTS.md, Writing). Say what an internal code means the first time it appears, or leave it out. Link files by path. In this order:

1. **The one thing** the keeper most needs to know, in two or three sentences.
2. **Since your last review:** what was published, what started and why, what was found about the world (unreviewed things labelled), what readers said.
3. **Next:** what the next run and the coming days will do, with dates. The scheduled run fires daily at 14:10 UK time.
4. **Waiting for you:** each decision, its options and your recommendation. Include decisions the keeper may not know they have: a limit that is biting, a started watch whose case has weakened, a date about to pass unwatched. When a rule bites, say so in one line and suggest the change; do not debate the rule.
5. **Worth a look:** anything stuck, late or worrying, in a line each. Say "nothing" if nothing.
6. **Spend** since the last review, saying what is not priced.

End with one line offering more: "Want the detail on any of: what was published, what started, what was found, readers, waiting items, what's next, spend, anything stuck?"

## 3. Take decisions

The keeper answers in their own words. For each decision, write a dated line under the proposal in proposals.md (`Keeper, <date>: agree`, `decline: <reason>`, `later`, `extend to <date>`, or a note), update its Status and Next step, and move it to the section its status names. A direction or a new idea goes under "From the keeper", or becomes a proposal. A change to the throttle, the charter, the run instructions or AGENTS.md's rules is the keeper's to make: make it as they say it, in their words where possible. Read anything back that you are unsure you heard right.

## 4. Record and finish

Rewrite proposals.md's "For the next review" to say what the keeper decided, set "Last reviewed by the keeper:" to now (UTC, `YYYY-MM-DDTHH:MMZ`), and add a line to schedule/runs.csv (`started,by,did,commit`) with the keeper's decisions in a few words and this session's spend from `harbour/hb drivercost --since <start>`. Commit as Claude with the harness's trailers, writing the message from a quoted heredoc, push the branch and fast-forward main (`git fetch origin main && git merge-base --is-ancestor origin/main HEAD && git push origin HEAD:main`, never force). Tell the keeper in two lines what was recorded and what the next run will do with it.
