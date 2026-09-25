# Lighthouse Founding Charter

Purpose, scope and commitments

Founding edition 0.2 (draft) | 25 September 2026 | LH F01

Lighthouse is an observatory and research practice for the computational world. We study how information moves through software, infrastructure, humans and AI, how those structures change, and what their behaviour means for the people who depend on them. We also develop better ways to conduct that study.

Our promise is to make more of this world observable and to make our explanations answerable to evidence. We publish research notes, studies, reports, articles and essays, supported where possible by inspectable instruments, methods and datasets.

A lighthouse does not steer ships. It makes positions and hazards visible to whoever is navigating. The name states both the ambition and its limit.

## The world we want to observe

Software accumulates into structures that outlast the work that created them. Information passes through those structures, is stored and transformed, and eventually informs a decision or an action. A small signal may coordinate a great deal of activity. A busy region may be routine. A quiet connection may be essential.

Running inference is a transient event: existing information and context are used to produce a next action. When that action changes code, configuration, data or another process, it leaves a durable alteration behind. Information can then flow through that structure long after the inference has finished, and later flows may need no further model invocation. A brief event can leave a persistent change in how a system behaves.

Lighthouse therefore observes at three layers. Activity is computation happening: inference, and the processing, communication and energy it consumes. Residue is the altered structure and state that activity leaves behind: changed code, configuration, data, messages and decisions. Propagation is how those alterations influence subsequent activity elsewhere: one event leaves a structure that enables similar activity in another place, and that activity leaves further enabling structures. The layers are observed with different instruments on different timescales, and a finding at one layer does not settle the others.

Three images help us form questions. Coral describes the accumulated residue: layers of code, configuration and data built on earlier layers. Veins describe circulation: the flows of requests, messages and data through which propagation happens. A ripple of light describes activity at a moment of change, such as a model producing an answer. These are working metaphors. They do not establish that the network is alive, conscious or governed by biological laws.

Humans and AI inhabit the same field of observation. Its origins include human knowledge, purposes, institutions and physical infrastructure. Authorship and agency are useful distinctions when they explain a mechanism. A complete division between human and AI activity is not a prerequisite for measurement.

## What success means

A successful investigation makes something clearer. It might establish a finding, improve a sensor, narrow an uncertainty, disprove an explanation, or show why a measurement cannot support the claim being made. Publication count, code volume and inference consumption are activity measures, not measures of scientific progress.

Our first durable contribution should be a trustworthy observation and an honest account of its limits. That gives the next investigation something reliable to build upon.

## Two directions of observation

Lighthouse looks inward to systems it can observe closely and outward to the wider internet. The two directions share methods and differ in access and certainty.

### Close observation

Harbour is the first proposed calibration subject. Harbour is an open-source control plane that reads a task backlog, grounds each task into a prompt, dispatches it to an AI coding agent, and verifies the result on evidence. Each dispatch leaves records: what was asked, when, with which model and harness, what the agent reported, and what it consumed. Those records describe a known workflow. Independent instruments can be tested against them, and the relationship between a request, its processing, its communication, the changes it makes and its later effects can be studied end to end.

Lighthouse is a complement to Harbour rather than a part of it. Harbour is a control plane: it keeps human intent in command of AI execution and verifies each task on evidence. Lighthouse is an observatory: it studies what execution leaves behind and what that enables, across many tasks, over longer periods, and beyond any one control plane. Harbour asks whether a task did what was asked. Lighthouse asks what the activity changed, and what the change made possible.

Harbour may also coordinate Lighthouse investigations. This makes it both an operational partner and a subject of study. Where the steward of Lighthouse also maintains Harbour, that overlap is a further interest to disclose. Lighthouse records the relationship in every study that relies on Harbour evidence and includes its own research footprint in its observations. Findings about Harbour require further testing before they are generalised to other systems.

Harbour publishes its own empirical papers about its workflow. Lighthouse does not repeat that work. Where a Harbour paper and a Lighthouse study touch the same events, each cites the other and states what its own evidence adds.

### Outward observation

Public data, published measurements, passive observation and willing collaborators can provide a broader view. Each source exposes part of the environment. Coverage, sampling, revisions and inaccessible regions belong in the map itself.

A complete and permanently current map is not our operating assumption. The internet behaves more like an expanding space than a fixed territory. Whether activity or infrastructure is growing faster than our ability to measure it is a question to investigate within a defined population and period, not a premise.

### Exchange between the two

Close observation helps establish what a signal means. Outward observation tests whether a pattern appears elsewhere and exposes cases our local instruments missed. Disagreement between the two is evidence worth investigating.

## Research scope

Our scope includes computational activity, information flows, persistent state, dependencies, authority, structural change, maintenance, concentration, propagation and recovery. Value and context are studied through declared purposes and observable consequences; traffic volume alone reveals neither.

Mapping, explanation and risk assessment are complementary outputs. A map describes what is visible. An explanation proposes a mechanism. A risk assessment relates evidence and possible mechanisms to consequences over a stated time horizon.

Self-replicating agents and a possible digital Kessler effect are research questions within this wider programme. The three layers make them investigable. A self-sustaining pattern would appear not in any single burst of activity, which might be unremarkable, but in the relationship between bursts, where each leaves residue that enables the next. Such a phenomenon could endure while every individual process in it is transient; its identity would lie in the pattern being maintained and propagated. An ordinary deployment or a useful agent workflow can produce a similar pattern, so appearance alone establishes neither replication nor intent. These questions do not determine the conclusion, and they do not restrict Lighthouse to malicious activity. Beneficial automation and ordinary background behaviour provide essential comparisons.

### What Lighthouse is not

Lighthouse is not a monitoring or alerting product, and its maps are not a census. It does not run experiments on systems without their operator's authority. It does not publish a risk it cannot connect to observations and a stated mechanism.

## Commitments that guide the work

We preserve the distinction between an observation, a derived measurement, an interpretation and a scenario. A reader should be able to trace a published claim to the evidence and method supporting it.

We make uncertainty visible. Missing readings remain missing; unknown attribution remains unknown. A poorly observed system is not thereby a dangerous one. We report collection boundaries and never present a sample as a census.

We seek explanations that can fail. Investigations name plausible alternatives and identify what would change the conclusion. Correlation, agreement between models, and repetition of the same underlying source do not independently establish a mechanism.

We keep correction possible. Methods and publications have stable identities, versions and correction records. Discovering an error should improve both the public record and the instrument that produced it.

We account for our own presence. Collection, experiments, inference and publication create activity. Lighthouse labels its contribution and measures collection overhead where feasible.

We keep research proportionate. Work begins with a bounded question, an accountable owner, a resource envelope and a stopping condition. A small team may combine roles; it still records which checks were independent.

## Authority and stewardship

The founding steward sets direction and assigns responsibility for investigations and publication. Human responsibility remains explicit when agents perform research or execution. These documents define the intended practice. They do not grant access to any system, create a spending commitment, or authorise a public release.

Work uses public sources or access granted for a specified purpose. An experiment that changes a system needs that system's operator's authority. Where Harbour is the subject, Lighthouse respects the boundary Harbour's own charter draws between actions its AI may take and actions reserved for humans. Transparency includes explaining restrictions on evidence that cannot responsibly be shared.

The charter should change when evidence or experience reveals a flaw in the remit. Changes affecting purpose, evidence standards or accountability require a recorded rationale from the steward. Routine methods can evolve within that remit without rewriting the charter.

## The founding commitment

We will begin with a known workflow and a modest outward survey. Each will produce useful evidence even if its first hypothesis fails. Together they establish the close and broad views on which Lighthouse can grow.

The companion documents define the research design (LH F02), the operating practice (LH F03), the first programme (LH F04) and the study templates (LH F05). Their initial choices can be revised as the work teaches us what is useful.
