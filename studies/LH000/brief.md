# LH000 study brief

Following the study brief block in LH F05 (Lighthouse_Study_Templates.md).

**study:** LH000
**edition:** 0.1
**date opened:** 2026-09-25

**owner:** the steward (unnamed)
**methods reviewer:** (blank; none assigned)
**editor:** (blank; none assigned)
**initiated by:** unknown. The take record names a `dispatchedBy` identifier (`0b284c47-41e5-4f48-bd28-570a4ad178e4`) but does not say whether a person or Harbour's autopilot loop queued the dispatch, and this study had no access to resolve that identifier to a role.

**question:** What does Harbour record about one dispatch, what does the host show while it runs, and what does it leave behind?

**scope (systems, population, period):** This one dispatch (item id `31d61117-c85a-43dd-9bcd-9cfbb76bf41d`, issue `LOCAL-3`, ticket LH000) in the local Harbour workspace running inside this container. Population is a sample of one; no claim is made beyond it.

**evidence available:** The take response Harbour returned for this dispatch (`take.json`, handed to this study, not queried live); two host samples taken by hand during this session; the founding documents (LH F01 to F06); an observation note written by a different agent about a different dispatch (`75516e46-c767-4dd7-aac0-e65782a9c73d`, issue `LOCAL-2`) on an earlier server instance, held for structural comparison only.

**evidence needed and access status:** Harbour's end-of-session export, which will hold this dispatch's feedback, usage and any audit entries; not available while this study is being written. Its path is recorded here as `EXPORT_PATH_TBD` for the driver to fill in once `harbour/hb export` has run. This study did not call the Harbour server itself to check for it.

**readings and instruments (by instrument id):** None registered. `registers/` does not yet exist in this repository, so no instrument has an I-nnnn record. Two ad hoc instruments were used informally: the take record returned by Harbour's dispatch API, and a hand-run host sample (commands listed in LH000.md's Method). Ticket I-0002 ("Sample the host") proposes a proper sampler; this study is not that sampler.

**comparators and known events:** The other agent's observation note on the earlier dispatch, `75516e46-c767-4dd7-aac0-e65782a9c73d`, used only to compare record shape (field counts, what a take response contains), never as evidence about this dispatch's own timing or load.

**competing explanations to test:** Whether host load and established connections seen during this dispatch reflect this dispatch's own work or ordinary background and sandbox processes that would be present with no dispatch running at all (LH001's "Alternatives" question, not resolved here because no idle-only baseline was taken).

**pre-specified analyses:** None. This study was not run as LH001's three-repetition calibration; it is a single, once-only pass, exploratory throughout.

**exploratory analyses (labelled):** All findings below are exploratory. One, in particular, was not asked for by the dispatch prompt and turned up only while reading process command lines to satisfy the host-sampling instruction: a difference between the model this agent was told it runs on and the model named in the host's own process arguments (see Findings and Limits in LH000.md).

**intended output (study, dataset, instrument revision):** A study (this one). `studies/LH000/` did not exist before this task; it is new residue of this dispatch.

**discovery allowance:** (blank)
**execution ceiling:** (blank)

**stopping condition:** The write-up exists and says what could not be filled.

**retention and sharing rules:** Harbour's own records for this dispatch are retained only until the driver runs `harbour/hb export` at the end of this session, per Harbour's short retention windows (LH F03). This repository is public (CLAUDE.md), so nothing under `harbour/.session/`, no token and no credential is written into it.

**Harbour dispatch identifiers (if coordinated through Harbour):** item id / dispatch id `31d61117-c85a-43dd-9bcd-9cfbb76bf41d` (also its own `sessionGroupId` and `rootItemId`); issue `LOCAL-3` (issue id `ff234786-b52f-44c6-a6cc-95321973e07f`); ticket `LH000` in `harbour/tickets.json`.

**overlaps and interests to disclose:** The observer, the coordinator and the subject are the same workspace: this study observes a Harbour workspace booted, dispatched and consumed within one Lighthouse session, and the agent writing the study is the agent that took the dispatch. No check in this study was performed independently of the work it describes.

**protocol amendments (date, change, reason):** None. Edition 0.1 is the first.
