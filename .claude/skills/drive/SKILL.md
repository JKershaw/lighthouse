---
name: drive
description: One tick of the Lighthouse watch. Does the next thing in the programme, releases what passes review, and reports what was learned about the internet.
argument-hint: "[optional max USD]"
---

# /drive

Follow [schedule/runner.md](../../../schedule/runner.md): it is the same tick, written so that any agent on any provider can run it from a one-line prompt, and it now leads. An argument, if given, caps subagent spend; without one there is no cap. What follows is kept for sessions started with `/drive`; where it differs from the runner, the runner wins.

Do the next thing in programme.md, the way AGENTS.md says a session goes. An argument, if given, is the most to spend on subagents at list rates; without one there is no cap. Stop there, if given, or when the finding is written and released, or when a subagent reports nothing usable; stopping early is not a failure.

The repository's issues are the backlog. `harbour/hb status` lists them, `hb close` closes one when its record is committed, and `hb add` files a question the work raised; harbour/README.md has the rest. Without a Harbour token, read and close them with the GitHub tools.

Commit once at the end, push the working branch, and fast-forward main from it; the site rebuilds from main. Report the close-out AGENTS.md describes, in a paragraph: what was learned about the internet, each point labelled observation or interpretation, what changed in the current account, what remains uncertain, the next question, and the spend. Say nothing about process unless it failed. Never create a scheduled routine.
