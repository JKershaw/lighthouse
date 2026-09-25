# Lighthouse

Lighthouse is a proposed observatory and research practice for the computational world. It studies how information moves through software, infrastructure, humans and AI, how those structures change, and what that behaviour means for the people who depend on them. It also works on better ways to conduct that study.

This repository holds the founding documents. They are drafts. They define an intended practice; they do not grant access to any system, commit spending, or authorise a publication.

## The documents

| ID | Document | What it settles | Read it when |
| --- | --- | --- | --- |
| LH F01 | [Founding Charter](Lighthouse_Founding_Charter.md) | Purpose, scope, commitments, authority | You want to know what Lighthouse is for and what it will not do |
| LH F02 | [Research Design](Lighthouse_Research_Design.md) | The observable model, measurement surfaces and rules, evidence records, risk assessment, sources | You are designing or reviewing a study |
| LH F03 | [Operating Handbook](Lighthouse_Operating_Handbook.md) | Roles, the investigation lifecycle, the Harbour interface, publication, corrections, boundaries | You are running or publishing a study |
| LH F04 | [Initial Research Programme](Lighthouse_Initial_Research_Programme.md) | The first twelve weeks: LH001, LH002, and the decisions to make at commencement | You are about to start work |
| LH F05 | [Study Templates](Lighthouse_Study_Templates.md) | The editable records the other documents refer to | You are opening a study, registering an instrument, or recording a decision |
| LH F06 | [Harbour Workspace Plan](Lighthouse_Harbour_Workspace_Plan.md) | North star, budget rule, seed tickets, periodicals and asks of Harbour | You are opening the Lighthouse workspace in Harbour |

Read F01 first. F02 and F03 can be read in either order. F04 assumes both. F05 is reference material. F06 is the operational plan for the first workspace and assumes all of them.

[REVIEW.md](REVIEW.md) records the review that produced edition 0.2 and the questions it left open.

## Harbour

[Harbour](https://harbour.cat) is an open-source control plane for AI coding agents ([source](https://github.com/JKershaw/LinearViewer)). It reads a task backlog, grounds each task into a prompt checked against the current code, dispatches the prompt to an agent, and verifies the result on evidence such as diffs, continuous integration and merges.

Lighthouse is a complement to Harbour. Harbour is a control plane that keeps human intent in command of AI execution and verifies each task on evidence. Lighthouse is an observatory that studies what execution leaves behind and what that enables, across many tasks and beyond any one control plane.

Lighthouse uses Harbour in two ways. Harbour is the first calibration subject: its dispatch, feedback and usage records describe a known workflow that independent instruments can be tested against. Harbour may also coordinate Lighthouse's own research tasks. The documents treat that dual role as something to record and check, not to hide.

Harbour already publishes empirical papers about its own workflow under its own writing standard. Lighthouse does not duplicate that programme. Its distinct contribution is the computational and informational footprint of such workflows, and the comparison between what can be seen up close and what can be seen across the wider internet.

## Glossary

- **Activity, residue, propagation.** The three observational layers in F01 and F02: computation happening; the altered structure and state it leaves behind; and the influence of that residue on later activity elsewhere. Propagation is measured as typed links between residue and later activity, not as a surface of its own.
- **Entity, relationship, event.** The elements of the observable model in F02. An entity persists (a host, service, person or workflow). A relationship is a typed connection between entities. An event happens at a time.
- **Observation.** A captured event or reading, with its source, time and status. Harbour has a view named Observation that shows agent sessions; that is a different thing, and this glossary means the Lighthouse one.
- **Derived measurement, interpretation, scenario.** Together with observation, the four kinds of statement that Lighthouse labels in publications (F02).
- **Instrument.** A sensor or collection method together with the record that says what it detects, what it misses and what it costs.
- **Study.** One bounded investigation with a stable identifier (LH001, LH002), a brief, an owner and a stopping condition.
- **Question register, decision record, release record, correction record.** The bookkeeping forms in F05.
- **Steward, owner, methods reviewer, editor.** The four roles in F03. One person may hold several; the record says which checks were independent.
- **Close observation, outward observation.** The two directions in F01: systems Lighthouse can instrument directly, and the wider internet seen through public data.
- **Dispatch.** Harbour's unit of work: a prompt queued for an agent, with its requested model, harness, timestamps and the agent's feedback.
- **Digital Kessler hypothesis.** A proposed scenario, named by analogy with orbital debris, in which harmful digital activity replenishes itself and degrades shared infrastructure. A question, not a finding.

## Edition history

| Edition | Date | Change |
| --- | --- | --- |
| 0.1 | 25 September 2026 | First draft of F01 to F04 |
| 0.2 (draft) | 25 September 2026 | Review edition. Sources re-checked and extended; Harbour interface aligned with Harbour's documented records; templates added as F05; this index added; the three observational layers and the complement-to-Harbour framing made explicit from the originating conversation; F06 workspace plan added. Details in [REVIEW.md](REVIEW.md) |
