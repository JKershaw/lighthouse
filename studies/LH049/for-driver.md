# LH049: for the driver

Not part of the protocol. The brief subagent of scheduled run 2026-11-10T1415Z wrote this; nothing here was committed by it.

**Urgent:** the per-version window that ends on 9 November (the release day alone) is readable only until npm loads 10 November's figures, soon after 00:00 UTC on 11 November. Commit the brief and get it on main, then make the first read on 10 November, so d(9 Nov) is exact rather than bounded:

    LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH049/scripts/collect.py --read <UTC label>

The collector refuses to run while brief.md is untracked or has uncommitted changes. `--dry-run` lists the six requests and the robots.txt decisions without requesting anything else (tested at about 14:45 UTC on 10 November: all six allowed; api.npmjs.org and api.osv.dev answer 404 for robots.txt, so no rules).

## Rows for schedule/due.csv

Update the existing row:

```
P-0026-brief,P-0026,"Write and fix a brief for P-0026 (bee-js 13.3.0 on npm) under the gate's seven conditions in notes/horizon/2026-11-10T1415Z.md, with one gated collector; event records read and kept first; commit before any download count is read; then add the daily and weekly read rows",2026-11-10,2026-11-12,done,2026-11-10,"scheduled run 2026-11-10T1415Z (Claude Code, Anthropic cloud)",studies/LH049/brief.md,"brief fixed as LH049, committed before any download count was read; event records kept under studies/LH049/data/pre-brief-2026-11-10T1437Z and T1438Z"
```

Add:

```
LH049-2026-11-10,LH049,"First read: collect.py --read <label>, on 10 November (after the brief is committed and on main) so the window ending 9 November is held; log the stated window dates",2026-11-10,2026-11-10,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"urgent: if missed, d(9 Nov) is only bounded; the gate's latest first read is 12 November"
LH049-2026-11-11,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC",2026-11-11,2026-11-11,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"a missed day breaks the day-count series"
LH049-2026-11-12,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC",2026-11-12,2026-11-12,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"a missed day breaks the day-count series"
LH049-2026-11-13,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC",2026-11-13,2026-11-13,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"a missed day breaks the day-count series"
LH049-2026-11-14,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC",2026-11-14,2026-11-14,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"a missed day breaks the day-count series"
LH049-2026-11-15,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC",2026-11-15,2026-11-15,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"a missed day breaks the day-count series"
LH049-2026-11-16,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC; the last window holding 9 November",2026-11-16,2026-11-16,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,"a missed day breaks the day-count series"
LH049-2026-11-17,LH049,"Daily read: collect.py --read <label>, at least an hour after 00:00 UTC; the first window without 9 November (gives the lower bound and d(16 Nov))",2026-11-17,2026-11-17,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,last daily read
LH049-checkpoint,LH049,"Checkpoint after the read of 17 November: write a tabulator implementing the measures as written (changing nothing in the brief); measures 1 to 4, 6 and 7, and 5 if a comparison release qualified; interim record version 0.1 with an In short opening",2026-11-17,2026-11-19,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,
LH049-2026-11-24,LH049,"Weekly and last read: collect.py --read <label>, 14 days after the first read (on 25 November if the first read was on 11 November, 26 if on 12); window ending 23 November for measure 2's tail; then the study stops reading",2026-11-24,2026-11-26,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,stopping condition: end 14 days after the first read
LH049-record,LH049,"Record version 1.0 (Answer, Findings, Method, Limits, Next, Corrections), then the evidence review and the reader-and-inference review before anything is released",2026-11-24,2026-12-01,open,2026-11-10,"scheduled run 2026-11-10T1415Z (brief subagent, Claude Code, Anthropic cloud)",studies/LH049/brief.md,
```

## A line for investigations/software-updates.md (under "Beside it")

```
- [How far a compromised bee-js release travelled on npm](../studies/LH049/brief.md), from 10 November 2026: a release of a small JavaScript library, published on 9 November through the project's own trusted-publishing workflow with genuine provenance and, as StepSecurity and Socket report, a malicious install hook, removed after about 75 minutes. Daily reads of npm's seven-day per-version counts to 17 November, then one more on 24 November, count its fetches on its day and after, beside the same days' ordinary traffic; the counterpart, on a second registry, of the LiteLLM study (LH040). A download is a fetch, not an install or a victim. Brief fixed before any count was read.
```

(The page speaks without study numbers in prose; drop "(LH040)" or link it as "[the LiteLLM study](../studies/LH040/LH040.md)" if that suits the page better.)

## Notes for the driver

- Pre-brief reads: 9 requests (E1 to E9 in sources.md), 14:37:25 to 14:38:32 UTC on 10 November, all allowed by the robots.txt gate, none to a download endpoint. Two of the sources (StepSecurity, Socket) state package-level download figures and Socket an estimate for 13.3.0; the brief discloses them under "What is already known of the outcome".
- The registry holds the publish time (2026-11-09T00:09:50.630Z) and shows 13.3.0 removed (time entry kept, not listed, version document 404, `latest` back to 13.2.0); it gives no removal time. The removal time 01:24:58 UTC is Socket's, labelled as reported; the registry document's last-modified time, 01:24:58.830Z, agrees to the second.
- The kept sources name dependents; the brief and these notes name none (condition 5).
- `scripts/collect_prebrief.py` is the pre-brief reader, kept for the record; it refuses any api.npmjs.org, npmjs.com or tarball URL.
