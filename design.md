# Research design

Observation, measurement and risk assessment. 25 September 2026, revised 26 September 2026. The records cite this document as LH F02; the sources it numbers are in sources.md.

Lighthouse studies a changing network through partial observations. This document defines an initial model, the readings needed to test it, and the limits on conclusions drawn from those readings. It is a design for research and contains no empirical findings.

## An observable model

Represent the observed environment as entities, relationships and events over time. An entity may be a host, process, service, model endpoint, store, person, organisation or workflow. A relationship may describe communication, data dependence, control or resource provision. Preserve the type of each relationship: sending many bytes and having authority to change a system are different connections.

Use a declared level of detail for each view. A service may contain many processes; one process may support many tasks. Aggregated identities must retain a path to the underlying records where access allows it.

### Three observational layers

Activity is computation happening. Residue is the altered structure and state that activity leaves behind. Propagation is the influence of that residue on subsequent activity elsewhere. Activity and residue are measured directly on the surfaces listed below. Propagation is not a surface: it is a typed link between a residue record and later activity that the residue enabled, such as a dispatch whose prompt was produced by an earlier run, a dependency change followed by changes in a dependent, or a deployment followed by new traffic. A propagation link is a derived measurement until the enabling relationship has been tested against records or a controlled comparison.

### An illustrative sequence

The sequence below is invented to show how the model applies. It is not an observation, and no timing in it should be quoted as one.

A Harbour user marks a task ready. Harbour grounds it into a prompt and queues a dispatch at 10:02, recording the requested model and harness. An agent on a developer's machine claims the dispatch at 10:03. Over the next sixteen minutes the machine shows a burst of process activity and several hundred requests to a model provider. The provider's own compute is not visible from the machine. At 10:19 the agent opens a pull request and posts a completion marker with its token usage. Continuous integration runs on a hosted runner at 10:31. A person merges the change at 11:00. A deployment at 11:20 alters a production service, and that service's traffic pattern shifts for the rest of the day.

In the model, the user, the machine, the agent, the provider endpoint, the repository, the CI runner and the production service are entities. The dispatch, the claim, each request, the pull request, the merge and the deployment are events. The agent's permission to change the repository, the merge's effect on production, and the service's dependence on the changed code are typed relationships. The burst of activity is a set of observations. A total of busy core seconds for the burst is a derived measurement. The statement that the deployment caused the traffic shift is an interpretation. A description of what would follow if the change were reverted is a scenario.

By layer, the burst of process activity and the provider requests are activity; the merged code and the changed production service are residue; the traffic shift, and any later dispatch that the change makes necessary or possible, are propagation.

### The busy core second as a starting unit

For an initial activity map, imagine equal units of processing capacity. In a homogeneous sample, busy core seconds are the sum over cores of utilisation multiplied by elapsed seconds. This measures occupied capacity within that sample and nothing more.

Real hardware requires the device type, allocation and measurement method to be retained. Virtual CPUs, physical cores and accelerator activity are separate series until a task-specific calibration supports a conversion. Tokens and electricity are also separate measures. No universal conversion between them is assumed.

### Several views of the same observations

Absolute activity shows continuing work. Deviation from an appropriate baseline highlights change; a transient is a deviation from a reference image of the same region, and the reference, its date and its instrument are part of the observation. Flow views show direction and volume. Dependency views show what relies on what. State comparisons show persistent alterations. None replaces the others.

The global now is represented through time windows. Record event time, collection time, clock uncertainty and late arrivals. The picture of the whole network is assembled from observations with different delays and resolutions, so the apparent shape of a burst partly depends on the instruments and timescale chosen; state both. A lag between two series can suggest a relationship, but clock error, queues or a common cause may explain it.

Information meaning and value require a separate account of purpose, context and consequences. A study might test which constraints survive a handoff, or whether a warning changes an operator's decision. Physical readings make those questions investigable; they do not answer them automatically. Health is assessed against declared functions and outcomes, including quiet reserves and maintenance, rather than maximum throughput.

## Initial measurement surfaces

Begin with readings the study can define and calibrate. Collection frequency follows the phenomenon and the cost of observation. Preserve native units and the boundaries of the measured entity. Each surface belongs to a layer; outcomes sit outside the layers and score activity and residue against a declared purpose.

| Surface | Layer | Initial readings | Essential qualification |
| --- | --- | --- | --- |
| Processing | Activity | Busy core seconds, accelerator utilisation, task wall time | Waiting time and occupied capacity differ |
| Electricity | Activity | Watts and energy over an interval | Declare the device, facility or allocated boundary |
| Communication | Activity | Requests, bytes, direction, latency, errors | Duplication and compression affect volume |
| Inference | Activity | Calls, model, input and output tokens, cache use | Provider and tokenizer definitions vary |
| Correctness | Activity | Test, sanitiser and build outcomes: passes, failures, errors and their timing | Read only by whoever runs the check and visible only where results are published; a pass does not establish correctness and an error does not establish malice (D-0004) |
| State | Residue | Storage volume, reads, writes, configuration versions | Volume does not establish relevance or value |
| Structure | Residue | Code changes, deployments, dependency changes | Count turnover separately from net growth |
| Authority | Residue when held, activity when exercised | Tokens issued, scopes, write actions, approvals, actions reserved for humans | A permission is a relationship, not a volume |
| Outcomes | Consequence | Completion, rework, incidents, interventions | Define the task and beneficiary before scoring |

## Measurement rules

Record counters, gauges and events as different types. Cumulative counters need reset detection before rates are calculated. Record collection outages and dropped events. Zero, unknown, unavailable and not applicable remain distinguishable.

Define the observation point for every flow. The same request seen at a client, a proxy and a server is three observations of one interaction, not three interactions. Correlate where reliable identifiers exist; otherwise state the uncertainty in totals.

Record each source's retention window and export what the study needs before that window closes. An export is itself an observation with a collection time. A source that has since expired cannot be re-queried to settle a dispute.

Use seasonally appropriate baselines and stable cohorts. Show raw totals alongside rates with their denominators. Changes in instrumentation, cohort membership and provider definitions can create apparent trends. Revisions to the baseline belong in the method history.

Code is one changing structure among several. Report additions and deletions separately, deduplicate where the research question requires it, and distinguish a repository change from a deployment. Structural survival indicates persistence, not necessarily quality.

For operations, classify involvement as advice, approved execution, delegated autonomy or autonomous initiation only when records support the distinction. Unknown remains a valid category. Agent invocation count does not determine the number of independent agents or of completed tasks.

## Evidence and instrument records

Each reading needs an observation identifier, source and sensor version, entity or connection identifier, event interval, collection time, metric, native unit, value and measurement status. Retain the sampling rule, collection boundary, attribution basis, missingness flags and a reference to the underlying record or its controlled location.

An instrument record explains what the sensor actually detects, what it misses, how it was calibrated, its expected overhead and which changes could invalidate comparisons.

### Four kinds of statement

An observation reports a captured event or reading. A derived measurement applies a stated transformation to observations. An interpretation proposes what a pattern means. A scenario explores what might happen under explicit assumptions. Publications label these distinctions wherever a reader could otherwise confuse them.

Every material claim identifies its supporting evidence, method version, scope, competing explanations and confidence rationale. Confidence increases through suitable evidence, calibration and replication. It is not a score obtained by asking several models whether they agree.

### Calibration and validation

Use known events, repeatable workloads and independently recorded operational outcomes to test detection and timing. Measure false positives and missed events where labels allow it.

A standard candle is a source whose intrinsic output is known, so that its observed signal calibrates the instrument and scales unknown sources. LH001's workflow is Lighthouse's first: a dispatch with recorded tokens, requests and changes, observed by the same instruments that will later observe unknown activity. A standard candle is valid only within the instrument, observation point and boundary it was measured with, and only while the relation between input and signature holds; re-check it when any of those change. An outward reading interpreted through a standard candle carries the candle's version.

Harbour's records are the first comparator [S12]. They are server-timestamped for queueing and claiming, but progress and completion are reported by the agent itself, so they show what was asked and what was claimed rather than what happened on the host. They may be incomplete or share a failure with the sensor. Harbour's retention windows are short, dispatch items expiring after twenty-four hours and feedback, status and audit records after thirty days at the time of writing, so the export rule above applies.

Separate exploratory findings from tests specified in advance. Preserve failed runs and protocol changes. When comparing workflows, declare the unit of comparison, task selection, sample size rationale, exclusions and likely confounders. A calibration run tests a method; a small convenience sample cannot estimate internet-wide prevalence.

### Collection and interpretation boundaries

Start from metadata sufficient to answer the question. Contents, personal data, secrets and customer material require a specific research need and a recorded handling decision. Published datasets use a reviewed subset or aggregation, with restrictions described. The Menlo Report's principles for research on information and communication technology are the reference for these decisions [S9].

The outward map covers the luminous fraction: what emits into public data. Provider compute, private repositories and internal infrastructure are dark and are inferred from their effects. Every outward view states its luminous fraction where it can be estimated and says unknown where it cannot. A dark region is not an empty one, and a bright one is not necessarily important.

A visually important node may be a measurement artefact. A central node in an incomplete graph may simply be better observed. Test claims about criticality against dependency records or authorised controlled tests before describing a node as essential.

## Risk assessment from an incomplete map

A risk assessment connects a defined event to consequences for identified people or systems over a specified period. It states the supporting observations, assumed mechanism, exposure, controls and uncertainties. Probability and confidence in the evidence are separate judgements.

Use numerical probabilities only when a defensible model or a relevant frequency estimate supports them. Otherwise describe the mechanism and conditions with an explicit qualitative judgement. An unknown likelihood is not zero, and uncertainty alone is not evidence of a high likelihood.

### Questions a risk assessment should answer

Which function or resource is exposed? What could initiate the event? Through which dependencies could effects spread? What prevents, detects or reverses those effects? How long could disruption persist? Which new observation would materially change the assessment?

Assess concentration, propagation, persistence, recovery and observability separately. A small authority-bearing connection may matter more than a high-volume stream. A finding about one system does not establish the prevalence of that condition elsewhere.

### Studying the digital Kessler hypothesis

The name borrows from Kessler and Cour-Palais, who described how collisions between orbiting objects could generate debris faster than it decays, degrading the usability of an orbit [S8]. In the three layers, collisions are activity, debris is residue, and the further collisions the debris causes are propagation; the analogy and the frame speak the same language. For Lighthouse, the hypothesis is a proposed scenario in which harmful digital activity creates further harmful capacity, replenishes itself after its initial support ends, and degrades the usability of shared infrastructure. The name is an analogy. It is not a physical law and not a finding that the condition exists. With autonomous replication [S4], it is the question the charter keeps the watch for, which is why its signature is specified here before any instrument exists to detect it.

In the three layers, the hypothesis predicts a distinctive propagation signature: residue left by one burst of activity enabling similar activity elsewhere, repeated until the population's continuity is visible even as its individual processes disappear. Measurements could in principle reveal reproduction, persistence and expanding influence before every local action is understood. They could equally reveal an ordinary release train, which is why the competing explanations below are tested first.

Evidence would need to distinguish continuing external support from endogenous replacement, successful reproduction from repeated attempts, and real environmental degradation from rising counts or improved detection. Benign deployment, scheduled automation and common external triggers are competing explanations for apparent propagation.

Studies can begin with historical evidence and contained models. Any claim of a growth threshold must specify the population, resources, removal processes and assumptions used. The thresholds in established computer-epidemic models are relevant antecedents, not universal constants for agent networks [S1].

### Decision and review

A published assessment names its author, evidence reviewer, as-of date, time horizon, expiry or review trigger, and practical implication. Evidence might justify adding an instrument, investigating a dependency or revising a scenario. The report says which decision it informs and what remains unresolved.

