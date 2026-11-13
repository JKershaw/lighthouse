# LH051: for the driver

Not part of the protocol. The brief subagent of 13 November 2026 (keeper-requested follow-up to run 2026-11-13T1452Z) wrote this; it committed nothing.

**Order of commits:** first everything under studies/LH051/ (brief.md, sources.md, for-driver.md, scripts/, data/pre-brief-2026-11-13T1531Z/) with the schedule rows below; get it on main; only then the first read. The collector refuses to run while brief.md is untracked or modified.

**First read** (today if the brief lands today, else 14 November; GH Archive's files persist, so a day's delay loses nothing but the posts' current state):

    LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH051/scripts/collect.py --read <UTC label, e.g. 2026-11-13T1700Z>

It fetches about 110 to 130 hourly files (2026-11-09-0 to the last complete hour), likely 2 to 6 GB, one at a time; run it in the background. It resumes: a held hour is never fetched again, so a cut run is simply run again with a new label. `--dry-run` was tested at 15:40 UTC on 13 November: 111 hours, all allowed by robots.txt, both posts allowed, nothing fetched. Commit data/hours.csv, data/counts.csv, data/fetch-log.tsv and data/read-<label>/ after each read (run `python3 -I scripts/redact_emails.py studies/LH051` first).

**Note on the design:** GH Archive's events no longer carry commit messages or pull request titles (checked on a file from before the campaign, field names only), so the study matches the reported probe branch name `wfx-docs` and two branch shapes both vendors list, not the titles. The brief says so in "What is already known of the outcome".

## Rows for schedule/due.csv

Update the existing row:

```
P-0029-brief,P-0029,"Write and fix a brief for P-0029 (WFX Phantom) under the gate's seven conditions in notes/horizon/2026-11-13T1452Z.md: vendors' posts kept first under the robots.txt gate, brief committed before any count is read, one gated collector, then the first read and the watch's rows (end 14 days after the first read)",2026-11-13,2026-11-15,done,2026-11-13,"keeper-requested follow-up to the 13 November run (brief subagent, Claude Code, Anthropic cloud)",studies/LH051/brief.md,"brief fixed as LH051 before any count was read; vendors' posts kept with names withheld under studies/LH051/data/pre-brief-2026-11-13T1531Z"
```

Add:

```
LH051-first,LH051,"First read: LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH051/scripts/collect.py --read <label>, after the brief is committed and on main; every hour from 2026-11-09-0 to the last complete hour, and both vendors' posts",2026-11-13,2026-11-14,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,"starts the 14-day clock; the brief's end is 14 days after this read"
LH051-2026-11-16,LH051,"Read: collect.py --read <label>; the hours since the last read, and both posts",2026-11-16,2026-11-17,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,
LH051-checkpoint,LH051,"Checkpoint after the read of 16 November: write a tabulator implementing the measures as written (changing nothing in the brief); measures 1 to 4, 6 and 7 for the hours held, 5 to date; interim note, unreviewed, with an In short opening; name no repository, account or organisation",2026-11-17,2026-11-18,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,
LH051-2026-11-19,LH051,"Read: collect.py --read <label>; the hours since the last read, and both posts",2026-11-19,2026-11-20,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,
LH051-2026-11-23,LH051,"Read: collect.py --read <label>; the hours since the last read, and both posts",2026-11-23,2026-11-24,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,
LH051-last,LH051,"Last read, 13 days after the first (26 November if the first read was on 13 November, 27 if on 14): collect.py --read <label>; then the study reads no further hour",2026-11-26,2026-11-27,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,"stopping condition: end 14 days after the first read"
LH051-record,LH051,"Record version 1.0 (header, Answer, Findings, Method, Limits, Next, Corrections) from the held counts, with a replay command; aggregate counts only, no repository, account or organisation named",2026-11-26,2026-11-28,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,"within 14 days of the first read"
LH051-reviews,LH051,"Evidence review (Opus, a fresh agent, reproducing measures 3 and 5 from data/counts.csv) then the reader-and-inference review, each a note in notes/; nothing released before both",2026-11-27,2026-11-28,open,2026-11-13,"brief subagent, keeper-requested follow-up to run 2026-11-13T1452Z (Claude Code, Anthropic cloud)",studies/LH051/brief.md,"within 14 days of the first read; if the first read slips to 14 November the windows hold"
```

## A line for investigations/ai-cost-and-spread.md

This page fits (the proposal names it, and the stealer's stated target is AI provider and coding-agent keys); software-updates.md would be the alternative. Under "Where the evidence stands", after the registry-worms line:

```
- **Spread run by people: a CI secret stealer, from 13 November 2026 ([its brief](../studies/LH051/brief.md)).** From 10 November, as StepSecurity and Aikido report, stolen GitHub credentials were used to open about 62,000 to 63,000 probe pull requests (by GitHub's search, on 11 and 12 November) and to plant a script that steals CI secrets, keys for AI providers and coding agents among them, in repositories where it would run. We count, by the hour and in aggregate only, the public events in GH Archive's hourly files that carry the probe's branch name, for 14 days, as a lower bound: the files no longer record commit messages or pull request titles, and whole kinds of event are missing from many hours. No source says AI was used to run it. Brief fixed before any count was read; nothing counted yet.
```

## A sentence for This week

We've started counting, hour by hour, the public traces of a campaign that two security firms say used stolen GitHub accounts from 10 November to plant a script stealing build secrets, including AI keys; we kept the firms' posts as published first, and nothing has been counted yet.
