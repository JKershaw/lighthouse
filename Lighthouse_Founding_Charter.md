# Lighthouse Founding Charter

Purpose, scope and commitments

Draft | 25 September 2026 | LH F01

Lighthouse is an observatory and research practice for the computational world. We study how information moves through software, infrastructure, humans and AI, how those structures change, and what their behaviour means for the people who depend on them. We also develop better ways to conduct that study.

We keep this watch for a reason. AI systems now write code, run tasks and call one another across the internet, and what they leave behind can set the next run in motion without a person choosing it. Nobody yet knows whether such activity could sustain and spread itself in ways that degrade the infrastructure everyone shares, or how much of it already happens out of sight. Today the honest answer is that we do not know, and we intend to be able to tell. Lighthouse exists so that the shape of the internet, the flows of information through it, the compute behind them and the patterns they form are visible to the people who must decide what to do about them.

The watch is kept largely by AI agents working within a stated budget and scope. People set the questions, read what comes back, and decide what is published. That division is deliberate: agent output is the ordinary case, and a person's attention is the scarce resource.

Our promise is to make more of this world observable and to make our explanations answerable to evidence. We publish research notes, studies, reports, articles and essays, supported where possible by inspectable instruments, methods and datasets.

A lighthouse does not steer ships. It stands at the harbour mouth and makes positions and hazards visible to whoever is navigating. The name states the ambition, its limit, and where it stands in relation to Harbour.

## The world we want to observe

Software accumulates like coral: each layer built on the last by many small builders, most of them long gone, into structures that outlast the work that created them. Information circulates through it like blood through veins, carrying requests, messages and data between the parts, until somewhere it informs a decision or an action. A small signal may coordinate a great deal of activity. A busy region may be routine. A quiet connection may be essential.

Inference is a ripple of light across that surface, a brief event in which stored context becomes a next action. When the action changes code, configuration or data, the ripple leaves an afterglow, a change that persists and through which information keeps flowing after the model has stopped. Where one afterglow lights the next ripple somewhere else, the pattern spreads.

Lighthouse observes at those three layers and names them plainly in its studies. Activity is the computation happening: inference, and the processing, communication and energy it consumes. Residue is the altered structure and state that activity leaves behind: changed code, configuration, data, messages and decisions. Propagation is the influence of that residue on activity elsewhere: one event leaves a structure that enables similar activity in another place, and that activity leaves further enabling structures. The layers are observed with different instruments on different timescales, and a finding at one layer does not settle the others.

Humans and AI inhabit the same field of observation. Its origins include human knowledge, purposes, institutions and physical infrastructure. Authorship and agency are useful distinctions when they explain a mechanism. A complete division between human and AI activity is not a prerequisite for measurement.

## What success means

A successful investigation makes something clearer. It might establish a finding, improve a sensor, narrow an uncertainty, disprove an explanation, or show why a measurement cannot support the claim being made. Publication count, code volume and inference consumption are activity measures, not measures of scientific progress.

Our first durable contribution should be a trustworthy observation and an honest account of its limits. That gives the next investigation something reliable to build upon.

## Two directions of observation

Lighthouse looks inward to systems it can observe closely and outward to the wider internet. The outward direction is the purpose; the close direction is how the instruments earn the right to be believed. The two directions share methods and differ in access and certainty.

### Close observation

Harbour is the first proposed calibration subject. Harbour is an open-source control plane that reads a task backlog, grounds each task into a prompt, dispatches it to an AI coding agent, and verifies the result on evidence. Each dispatch leaves records: what was asked, when, with which model and harness, what the agent reported, and what it consumed. Those records describe a known workflow. Independent instruments can be tested against them, and the relationship between a request, its processing, its communication, the changes it makes and its later effects can be studied end to end.

Lighthouse is a complement to Harbour rather than a part of it. Harbour is a control plane: it keeps human intent in command of AI execution and verifies each task on evidence. Lighthouse is an observatory: it studies what execution leaves behind and what that enables, across many tasks, over longer periods, and beyond any one control plane. Harbour asks whether a task did what was asked. Lighthouse asks what the activity changed, and what the change made possible.

Harbour may also coordinate Lighthouse investigations. This makes it both an operational partner and a subject of study. Lighthouse and Harbour have the same keeper, the person who keeps the light lit and decides what is shown, and that overlap is a further interest to disclose. Lighthouse records the relationship in every study that relies on Harbour evidence and includes its own research footprint in its observations. Findings about Harbour require further testing before they are generalised to other systems.

Harbour publishes its own empirical papers about its workflow. Lighthouse does not repeat that work. Where a Harbour paper and a Lighthouse study touch the same events, each cites the other and states what its own evidence adds.

In astronomical terms, Harbour is the nearest star: the one source Lighthouse can resolve in detail. The first close study, LH001, observes a workflow whose inputs are recorded in order to learn the signature those inputs produce. That signature is a standard candle, a known light by which unknown ones are measured. Once it exists, an outward observation can be interpreted rather than merely counted.

### Outward observation

Public data, published measurements, passive observation and willing collaborators can provide a broader view. Each source exposes part of the environment. Coverage, sampling, revisions and inaccessible regions belong in the map itself.

What emits is already considerable. Every public event on the largest code forge is archived hourly. The dependency graphs of the major package ecosystems are resolved and queryable. One of the largest networks publishes how much of its traffic comes from identified AI crawlers, and an API broker publishes which models its developers are running, by tokens. Vulnerability databases record disclosed compromises with dates, and archived source history survives the forge it came from. None of this was collected for Lighthouse's question, and each source has its own boundary, but together they are the light by which the shape of the wider internet is first read.

An outward map records what emits into public data. Provider compute, private repositories and internal infrastructure are dark: their existence is inferred from effects such as usage reports, energy statements and patch waves, never observed directly. Each outward view states how much of its population it can see, or says that it cannot. A dark region is not an empty one.

A complete and permanently current map is not our operating assumption. The internet is more like an expanding space than a fixed territory: it can grow faster than light from its far regions reaches us, so the map is always somewhat behind. Whether activity or infrastructure is in fact growing faster than our ability to measure it is a question to investigate within a defined population and period, not a premise.

### Exchange between the two

Close observation helps establish what a signal means. Outward observation tests whether a pattern appears elsewhere and exposes cases our local instruments missed. Disagreement between the two is evidence worth investigating.

Observatories have grown in a fixed order: catalogue what is visible, calibrate on known objects, explain the mechanism, then measure the dynamics. Lighthouse follows that order. Its first programme catalogues the existing surveys and the known noteworthy events, calibrates on Harbour, and begins to explain. Dynamics come later and cannot honestly come sooner.

## Research scope

Our scope includes computational activity, information flows, persistent state, dependencies, authority, structural change, maintenance, concentration, propagation and recovery. Value and context are studied through declared purposes and observable consequences; traffic volume alone reveals neither.

Mapping, explanation and risk assessment are complementary outputs. A map describes what is visible. An explanation proposes a mechanism. A risk assessment relates evidence and possible mechanisms to consequences over a stated time horizon.

Self-replicating agents and a possible digital Kessler effect are the questions this watch is kept for, and they sit inside this wider programme rather than replacing it. Kessler's scenario is the orbital one in which debris from collisions causes further collisions until an orbit becomes unusable; the digital version asks whether harmful activity could sustain itself the same way. The three layers make such questions investigable. A self-sustaining pattern would appear not in any single burst of activity, which might be unremarkable, but in the relationship between bursts, where each leaves residue that enables the next. Such a phenomenon could endure while every individual process in it is transient; its identity would lie in the pattern being maintained and propagated. An ordinary deployment or a useful agent workflow can produce a similar pattern, so appearance alone establishes neither replication nor intent. These questions do not determine the conclusion, and they do not restrict Lighthouse to malicious activity. Beneficial automation and ordinary background behaviour provide essential comparisons.

### What Lighthouse is not

- **[BINDING] Lighthouse is a standing watch, not an alerting service.** It publishes what it sees on its own cadence; nobody subscribes to it for warnings about their own systems, and its maps are not a census. *Breach: a warning sent to anyone about their own systems on request, or a map presented as complete.*
- **[BINDING] It does not run experiments on systems without their operator's authority.** *Breach: a change made to an observed system without that operator's recorded authority.*
- **[BINDING] It does not publish a risk it cannot connect to observations and a stated mechanism.** *Breach: a published risk with neither.*

## Commitments that guide the work

The labels follow Harbour's charter. BINDING names a rule with an observable breach. PRINCIPLE names a value that guides judgement. DEFERRED names a commitment not yet in force.

- **[BINDING] We preserve the distinction between an observation, a derived measurement, an interpretation and a scenario.** A reader should be able to trace a published claim to the evidence and method supporting it. *Breach: a published claim whose kind a reader cannot tell, or that cannot be traced to its evidence and method.*
- **[BINDING] We make uncertainty visible.** Missing readings remain missing; unknown attribution remains unknown. A poorly observed system is not thereby a dangerous one. We report collection boundaries and never present a sample as a census. *Breach: a sample presented as a census, a missing reading filled in, or an unknown attribution asserted.*
- **[BINDING] We seek explanations that can fail.** Investigations name plausible alternatives and identify what would change the conclusion. Correlation, agreement between models, and repetition of the same underlying source do not independently establish a mechanism. *Breach: a published study that names no competing explanation and nothing that would change its conclusion.*
- **[BINDING] We keep correction possible.** Methods and publications have stable identities, versions and correction records. Discovering an error should improve both the public record and the instrument that produced it. *Breach: a corrected publication with no stable identity, version or correction record.*
- **[BINDING] We account for our own presence.** Collection, experiments, inference and publication create activity, and Lighthouse labels its contribution. *Breach: Lighthouse's own activity appearing in an observation without its label.*
- **[DEFERRED] We measure our collection overhead.** In force once the host sampler, I-0002, exists and reports its own cost.
- **[BINDING] We keep research proportionate.** Work begins with a bounded question, an accountable owner, a resource envelope and a stopping condition. A small team may combine roles; it still records which checks were independent. *Breach: a study open with no brief naming those four things, or a publication that implies a check was independent when it was not.*
- **[PRINCIPLE] A finding at one layer does not settle the others.** Activity, residue and propagation are observed with different instruments on different timescales, and a claim about one is not evidence about another.

## Authority and the keeper

The keeper sets direction and assigns responsibility for investigations and publication. Agents do most of the research and execution; a named person remains responsible for each study and for every release. These documents define the intended practice. They do not grant access to any system, create a spending commitment, or authorise a public release.

Work uses public sources or access granted for a specified purpose. An experiment that changes a system needs that system's operator's authority. Where Harbour is the subject, Lighthouse respects the boundary Harbour's own charter draws between actions its AI may take and actions reserved for humans. Transparency includes explaining restrictions on evidence that cannot responsibly be shared.

The charter should change when evidence or experience reveals a flaw in the remit. Changes affecting purpose, evidence standards or accountability require a recorded rationale from the keeper. Routine methods can evolve within that remit without rewriting the charter.

## The founding commitment

We will begin with a known workflow, a catalogue of the surveys that already exist, one historical case and a modest outward survey. Each will produce useful evidence even if its first hypothesis fails. Together they establish the close and broad views on which Lighthouse can grow, and bring the watch to the point where it can say what it would and would not see.

The companion documents define the research design (LH F02), the operating practice (LH F03), the first programme (LH F04), the study templates (LH F05) and the first workspace plan (LH F06). Their initial choices can be revised as the work teaches us what is useful.
