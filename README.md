# Lighthouse

## [The xz backdoor sat in public for nearly five weeks until a slow login gave it away](articles/the-xz-backdoor.md)

In March 2024 an engineer reported that logging in to his machines had been taking about half a second too long, and that he had followed the delay to a backdoor hidden in a compression library. For nearly five weeks the code had sat in releases that anyone could download and read, and earlier complaints from a memory checker had been explained away, with a fix supplied by the attacker. The piece asks why evidence open to everyone went unrecognised until one person felt it, and what that means for anyone keeping watch on software.

![Timeline from 24 February to 30 March 2024 in three lanes: what was released, where it was built in, and what people noticed](articles/the-xz-backdoor-timeline.svg)

*The backdoor was public from 24 February and in Debian two days later; the errors of early March were answered by the 5.6.1 release, and nobody recognised the attack until late March.*

[Read the piece.](articles/the-xz-backdoor.md)

## What we observe, and through whose instruments

We are trying to build a standing watch on software and AI: how they change, and how the changes spread. So far, almost everything we know has come through other people's instruments: archives, timelines and published figures that someone else made. The xz story rests on the public record of the case. [Our other released piece](articles/what-we-can-see.md), on how much of the internet's AI activity anyone can see, rests on seventeen public sources and what each says about itself. The two instruments we run ourselves point inward, at our own tasks and at the machine our agents work on.

| What we observe | Through whose instrument | When |
| --- | --- | --- |
| How the xz backdoor was released, spread and found, February to March 2024 | Other people's: Andres Freund's report, Russ Cox's timeline, the xz project's own account and the distributions' security notices, among others | Read on 26 September 2026 |
| What public sources can and cannot see of AI activity, as each describes itself | Other people's: seventeen sources, among them GH Archive, Open Source Insights, OpenRouter's rankings, Cloudflare's crawler figures and the vulnerability databases | Read on 26 September 2026; none of their data sampled |
| Our own tasks: what each asked for and what came back | Ours: a copy of the records kept by [Harbour](https://harbour.cat), the open-source tool that hands our tasks to AI agents | Since 25 September 2026, in snapshots |
| The machine our agents work on: its processor, memory and network connections | Ours: a sampler that reads the machine's own counters | Since 26 September 2026, in snapshots |

That is the whole map. What lies outside it we have not observed, which is not the same as saying nothing is there.

## The next question

The xz backdoor could be traced afterwards, through public records, from one project's release into the Linux distributions that took it; we want to know whether ordinary changes can be followed the same way. We mean to look at a small neighbourhood of public software, up to ten projects from one family over a fixed four weeks in the past, and ask: when something changes in one of them, where does the change appear next? The work has not begun; [its design](Lighthouse_Initial_Research_Programme.md#lh002-mapping-a-bounded-public-software-neighbourhood) is written, and its record will appear in [the studies folder](studies/), whether the answer turns out to be a pattern or a finding that public records cannot connect one change to the next.

*26 September 2026. Below: what Lighthouse is, the documents that define it, and how the work is run.*

---

## What Lighthouse is

Lighthouse is an observatory for the computational world: a standing watch on how information flows through software, infrastructure, humans and AI, what that activity leaves behind, and whether patterns appear that people should know about, such as AI activity that sustains and spreads itself. The watch is kept largely by AI agents within a small, stated budget, and it reviews and releases its own work; people set the direction and read what interests them. Lighthouse also works on better ways to conduct that study.

This repository holds the founding documents, which are drafts, and the pieces and records made under them. The documents define the practice, including how a piece is reviewed and released; they do not grant access to any system or commit spending.

## The documents

| ID | Document | What it settles | Read it when |
| --- | --- | --- | --- |
| LH F01 | [Founding Charter](Lighthouse_Founding_Charter.md) | Purpose, scope, commitments, authority | You want to know what Lighthouse is for and what it will not do |
| LH F02 | [Research Design](Lighthouse_Research_Design.md) | The observable model, measurement surfaces and rules, evidence records, risk assessment, sources | You are designing or reviewing a study |
| LH F03 | [Operating Handbook](Lighthouse_Operating_Handbook.md) | Who does the work, the investigation lifecycle, the Harbour interface, outward sources, publication, corrections, boundaries | You are running or publishing a study |
| LH F04 | [Initial Research Programme](Lighthouse_Initial_Research_Programme.md) | The first programme: LH001 to LH004 and the decisions to make at commencement | You are about to start work |
| LH F05 | [Study Templates](Lighthouse_Study_Templates.md) | The editable records the other documents refer to | You are opening a study, registering an instrument, or recording a decision |
| LH F06 | [Harbour Workspace Plan](Lighthouse_Harbour_Workspace_Plan.md) | North star, budget and seed tickets for the first workspace | You are opening the Lighthouse workspace in Harbour |

Read F01 first. F02 and F03 can be read in either order. F04 assumes both. F05 is reference material. F06 is the operational plan for the first workspace and assumes all of them.

## Harbour

[Harbour](https://harbour.cat) is an open-source control plane for AI coding agents ([source](https://github.com/JKershaw/LinearViewer)). It reads a task backlog, grounds each task into a prompt, dispatches it to an agent and verifies the result on evidence. Lighthouse is a complement to it, not a part of it: Harbour asks whether a task did what was asked; Lighthouse asks what the activity changed and what the change made possible.

Lighthouse uses Harbour in two ways, as its first calibration subject and as the coordinator of its own research tasks, and records that dual role in every study that relies on Harbour evidence. The keeper of Lighthouse is the maintainer of Harbour, named in [Harbour's charter](https://github.com/JKershaw/LinearViewer/blob/main/docs/charter/charter.md). Harbour publishes its own papers about its workflow under its own writing standard; Lighthouse adopts that standard and does not duplicate the programme. F01 has the full account.

## The wider internet

The wider internet is the reason for the watch; Harbour is how the instruments are calibrated. Lighthouse sees the internet through what emits into public data: repository events, dependency graphs, identified crawler traffic, model usage rankings, vulnerability records and archived source history. F02 lists the sources and what each can and cannot see. F04's outward studies begin with a survey of those surveys (LH003), a historical propagation case (LH004) and a bounded neighbourhood map (LH002). This edition says little about the internet that is not borrowed from those sources, because Lighthouse has not yet observed it. That is the gap the first programme is designed to close.

## Running the watch

The workspace as files lives in [harbour/](harbour/): the north star, the tickets, the boot and export script, and the exports of what Harbour recorded. [AGENTS.md](AGENTS.md) holds the house rules for any agent; [CLAUDE.md](CLAUDE.md) the procedure for a Claude Code session.

## Glossary

- **Activity, residue, propagation.** The three observational layers in F01 and F02: computation happening; the altered structure and state it leaves behind; and the influence of that residue on later activity elsewhere. Propagation is measured as typed links between residue and later activity, not as a surface of its own. The charter's images for the three are the ripple of light, its afterglow, and the spreading pattern.
- **Entity, relationship, event.** The elements of the observable model in F02. An entity persists (a host, service, person or workflow). A relationship is a typed connection between entities. An event happens at a time.
- **Observation.** A captured event or reading, with its source, time and status. Harbour has a view named Observation that shows agent sessions; that is a different thing, and this glossary means the Lighthouse one.
- **Derived measurement, interpretation, scenario.** Together with observation, the four kinds of statement that Lighthouse labels in publications (F02).
- **Instrument.** A sensor or collection method together with the record that says what it detects, what it misses and what it costs.
- **Study.** One bounded investigation with a stable identifier (LH001, LH002), a brief, an owner and a stopping condition.
- **Question register, decision record, release note, correction record.** The bookkeeping forms in F05.
- **Keeper, owner, reviewer, editor.** The four functions in F03, any of which an agent may fill; the record says which checks were independent.
- **Close observation, outward observation.** The two directions in F01: systems Lighthouse can instrument directly, and the wider internet seen through public data.
- **Watch.** Lighthouse's standing observation of the wider internet, published on its own cadence. Not an alerting service: nobody subscribes to it for warnings about their own systems.
- **Standard candle.** A source whose output is known, used to calibrate an instrument and to scale unknown sources. LH001's workflow is Lighthouse's first.
- **Luminous fraction.** The part of a population that emits into public data. The rest is dark, meaning unobserved rather than sinister, and is inferred from its effects.
- **Dispatch.** Harbour's unit of work: a prompt queued for an agent, with its requested model, harness, timestamps and the agent's feedback.
- **Autopilot.** The automated loop in a Harbour workspace that turns ready tickets into agent tasks without a person initiating each one. In the Lighthouse workspace it does the research, the review and the release; a person reads and steers.
- **Digital Kessler hypothesis.** A proposed scenario, named by analogy with orbital debris, in which harmful digital activity replenishes itself and degrades shared infrastructure. A question, not a finding.
