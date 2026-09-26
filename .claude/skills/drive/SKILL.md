---
name: drive
description: One tick of the Lighthouse watch. Does the next thing in the programme, releases what passes review, and reports what was learned about the internet.
argument-hint: "[max USD]"
---

# /drive

Do the next thing in programme.md, the way AGENTS.md says a session goes. The argument is the most to spend on subagents at list rates, default 20. Stop there, or when the finding is written and released, or when a subagent reports nothing usable; stopping early is not a failure.

The repository's issues are the backlog. `harbour/hb status` lists them, `hb close` closes one when its record is committed, and `hb add` files a question the work raised; harbour/README.md has the rest. Without a Harbour token, read and close them with the GitHub tools.

Commit once at the end, push the working branch, and fast-forward main from it; the site rebuilds from main. Report in a paragraph: what was learned about the internet, each point labelled observation or interpretation, and the next question. Say nothing about process unless it failed. Never create a scheduled routine.
