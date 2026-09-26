# Decision register

Decisions of record, in the LH F05 form. A decision is either founding scope or a provisional implementation choice, and says when to revisit it.

```
decision: D-0001                  date: 2026-09-26      owner: the keeper
question: What bounds a drive while the ledger is not yet running, and from which pot is each cost paid?
options considered: keep the one to ten dollars a day of LH F06 as the drive limit; raise the limit and bound by count; bound by count alone
choice: A drive is bounded by its count of dispatches, default three and never more than five, and by a measured subagent cost limit whose default rises from five to twenty dollars. Claude spend is paid from the keeper's subscription and is recorded at list rates as a measure, not a bill. Harbour's own model calls through OpenRouter are paid as they go and are the only money spent per call.
reason: The keeper said on 26 September 2026 that the subscription pot is generous and twenty dollars a drive is fine, and that OpenRouter is pay as you go. The count is the working bound; the cost limit catches a runaway task.
kind: provisional implementation choice
revisit when: the ledger (L-0001) runs and shows what a drive costs, or the work moves to hosted Harbour or to OpenCode, where Claude spend would be pay as you go too.
```

```
decision: D-0002                  date: 2026-09-26      owner: the keeper
question: Which model takes a dispatched task that needs reasoning?
options considered: Sonnet 5 by default with Opus for review, as notes/Q-0002 recommends; Opus 5.5 for every task that needs reasoning, Sonnet 5 for collection and tabulation; Fable 5.1 for reasoning tasks
choice: Opus 5.5 for research, essays, study write-ups and review; Sonnet 5 for collection scripts, source checks and tabulation; Haiku 4.5 only for a chore the driver cannot do with hb. The launcher's opus alias resolved to claude-opus-5-5 on 2026-09-26.
reason: The keeper's steer on 26 September 2026, once a Sonnet task was measured at one to two dollars. Opus 5.5 reads cache at Sonnet 5's rate and doubles only writes and output, so a reasoning task costs perhaps a third more; Fable 5.1 writes cache at five times Opus 5.5's rate. A probe subagent that did nothing wrote about 45,000 tokens of harness context to cache, a floor of about $0.22 on Opus 5.5 per subagent.
kind: provisional implementation choice
revisit when: a task kind has been measured on both models, as notes/Q-0002 proposes under Next, or prices change.
```

```
decision: D-0003                  date: 2026-09-26      owner: the keeper
question: Does LH001 gate outward work?
options considered: keep the north star's sentence that outward numbers are only counts until LH001 exists; let outward studies validate their own sources within their own boundary, with LH001 calibrating the instruments Lighthouse runs itself
choice: The second. The north star now says that LH001 calibrates Lighthouse's own instruments and that an outward study validates its sources within its boundary and says whose instruments supplied the evidence. LH002 is filed as a historical window so that change can be studied without waiting to accumulate observations. Editing an article is its own ticket, E-nnnn, distinct from the study it draws on, and release stays the keeper's decision under LH F03.
reason: An observing agent's reading on 26 September 2026, which the keeper passed on, and the first drive's own result: LH003 and LH004 produced defensible records from others' observations before LH001 existed.
kind: founding scope
revisit when: LH001 exists and its calibration changes how an outward series should be read.
```

```
decision: D-0004                  date: 2026-09-26      owner: the keeper
question: Where does a correctness signal sit among LH F02's activity surfaces?
options considered: leave it out, since it is not a resource reading; add a Correctness surface for test, sanitiser and build outcomes
choice: Add the surface to the initial measurement surfaces table in LH F02.
reason: LH004 found that the earliest xz signal was a memory sanitiser's output in a distribution's build pipeline, weeks before the timing anomaly that led to detection, and that no surface in the table would have recorded it.
kind: founding scope
revisit when: a study reads the surface and finds its unit or caveat wrong.
```
