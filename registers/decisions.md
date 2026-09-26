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
