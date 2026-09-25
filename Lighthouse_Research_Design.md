# Lighthouse Research Design

Observation measurement and risk assessment

Founding edition 0.1 | 25 September 2026 | LH F02

Lighthouse studies a changing network through partial observations. This document defines an initial model, the readings needed to test it, and the limits on conclusions drawn from those readings. It is a design for research; it contains no new empirical findings.

## An observable model

Represent the observed environment as entities, relationships, and events over time. An entity may be a host, process, service, model endpoint, store, person, organisation, or workflow. Relationships may describe communication, data dependence, control, or resource provision. Preserve the type of each relationship: sending many bytes and having authority to change a system are different connections.

Use a declared level of detail for each view. A service may contain many processes; one process may support many tasks. Aggregated identities must retain a path to the underlying records where access allows it.

### The standard CPU approximation

For an initial activity map, imagine equal units of processing capacity. In a truly homogeneous sample, busy core seconds can be calculated by summing utilisation multiplied by elapsed seconds across cores. This is a measure of occupied capacity within that sample.

Real hardware requires the original device type, allocation, and measurement method to be retained. Virtual CPUs, physical cores, and GPU activity are separate series until a task-specific calibration supports a conversion. Tokens and electricity are also separate measures. A universal conversion between them is not assumed.

### Several views of the same observations

Absolute activity shows continuing work. Deviation from an appropriate baseline highlights change. Flow views show direction and volume. Dependency views show what relies on what. State comparisons show persistent alterations. None replaces the others.

The global now is represented through time windows. Record event time, collection time, clock uncertainty, and late arrivals. A lag between two series can suggest a relationship, but clock error, queues, or a common cause may explain it.

Information meaning and value require a separate account of purpose, context, and consequences. A study might test which constraints survive a handoff or whether a warning changes an operator's decision. Physical readings make those questions investigable; they do not answer them automatically. Health is assessed against declared functions and outcomes, including quiet reserves and maintenance, rather than maximum throughput.

## Initial measurement surfaces

Begin with readings the study can define and calibrate. Collection frequency follows the phenomenon and cost of observation. Preserve native units and the boundaries of the measured entity.

| Surface | Initial readings | Essential qualification |
| --- | --- | --- |
| Processing | Busy core seconds, accelerator utilisation, task wall time | Waiting time and occupied capacity differ |
| Electricity | Watts and energy over an interval | Declare device, facility, or allocated boundary |
| Communication | Requests, bytes, direction, latency, errors | Duplication and compression affect volume |
| State | Storage volume, reads, writes, configuration versions | Volume does not establish relevance or value |
| Inference | Calls, model, input and output tokens, cache use | Provider and tokenizer definitions vary |
| Structure | Code changes, deployments, dependency changes | Count turnover separately from net growth |
| Outcomes | Completion, rework, incidents, interventions | Define the task and beneficiary before scoring |

## Measurement rules

Record counters, gauges, and events as different types. Cumulative counters need reset detection before rates are calculated. Record collection outages and dropped events. Zero, unknown, unavailable, and not applicable remain distinguishable.

Define the observation point for every flow. The same request seen at a client, proxy, and server is three observations of one interaction, not necessarily three independent interactions. Correlate where reliable identifiers exist; otherwise state the uncertainty in totals.

Use seasonally appropriate baselines and stable cohorts. Show raw totals alongside rates with their denominators. Changes in instrumentation, cohort membership, and provider definitions can create apparent trends. Revisions to the baseline belong in the method history.

Code is one changing structure among several. Report additions and deletions separately, deduplicate where the research question requires it, and distinguish a repository change from deployment. Structural survival indicates persistence, not necessarily quality.

For operations, classify involvement as advice, approved execution, delegated autonomy, or autonomous initiation only when records support the distinction. Unknown remains a valid category. Agent invocation count does not determine the number of independent agents or completed tasks.

## Evidence and instrument records

Each reading needs an observation identifier, source and sensor version, entity or connection identifier, event interval, collection time, metric, native unit, value, and measurement status. Retain the sampling rule, collection boundary, attribution basis, missingness flags, and a reference to the underlying record or its controlled location.

The source bundle supplies reusable instrument and study records. An instrument record explains what the sensor actually detects, what it misses, how it was calibrated, its expected overhead, and which changes could invalidate comparisons.

### Four kinds of statement

An observation reports a captured event or reading. A derived measurement applies a stated transformation to observations. An interpretation proposes what the pattern means. A scenario explores what might happen under explicit assumptions. Publications label these distinctions where a reader could otherwise confuse them.

Every material claim should identify its supporting evidence, relevant method version, scope, competing explanations, and confidence rationale. Confidence increases through suitable evidence, calibration, and replication; it is not a score obtained by asking several models whether they agree.

### Calibration and validation

Use known events, repeatable workloads, and independently recorded operational outcomes to test detection and timing. Measure false positives and missed events where labels allow it. A Harbour task log is a useful comparator, but it may itself be incomplete or share a failure with the sensor.

Separate exploratory findings from tests specified in advance. Preserve failed runs and protocol changes. When comparing workflows, declare the unit of comparison, task selection, sample size rationale, exclusions, and likely confounders. A pilot calibrates a method; a small convenience sample cannot estimate internet-wide prevalence.

### Collection and interpretation boundaries

Start from metadata sufficient to answer the question. Contents, personal data, secrets, and customer material require a specific research need and an appropriate handling decision. Published datasets use a reviewed subset or aggregation, with restrictions described.

A visually important node may be a measurement artefact. A central node in an incomplete graph may simply be better observed. Test claims about criticality against dependency records or authorised controlled tests before describing the node as essential.

## Risk assessment from an incomplete map

A risk assessment connects a defined event to consequences for identified people or systems over a specified period. It states the supporting observations, assumed mechanism, exposure, controls, and uncertainties. Probability and confidence in the evidence are separate judgements.

Use numerical probabilities only when a defensible model or relevant frequency estimate supports them. Otherwise describe the mechanism and conditions, with an explicit qualitative judgement. An unknown likelihood is not zero, and uncertainty alone is not evidence of a high likelihood.

### Questions a risk assessment should answer

Which function or resource is exposed? What could initiate the event? Through which dependencies could effects spread? What prevents, detects, or reverses those effects? How long could disruption persist? Which new observation would materially change the assessment?

Assess concentration, propagation, persistence, recovery, and observability separately. A small authority-bearing connection may matter more than a high-volume stream. A finding about one system does not establish the prevalence of that condition elsewhere.

### Studying the digital Kessler hypothesis

For Lighthouse, this is a proposed scenario in which harmful digital activity creates further harmful capacity, replenishes itself after its initial support ends, and degrades the usability of shared infrastructure. The name is an analogy, not a physical law or a finding that this condition exists.

Evidence would need to distinguish continuing external support from endogenous replacement, successful reproduction from repeated attempts, and real environmental degradation from rising counts or improved detection. Benign deployment, scheduled automation, and common external triggers are competing explanations for apparent propagation.

Studies can begin with historical evidence and contained models. Any claim of a growth threshold must specify the population, resources, removal processes, and assumptions used. The thresholds in established computer-epidemic models are relevant antecedents, not universal constants for agent networks [S1].

### Decision and review

A published assessment names its author, evidence reviewer, as-of date, time horizon, expiry or review trigger, and practical implication. For example, evidence may justify adding an instrument, investigating a dependency, or revising a scenario. The report should say which decision it informs and what remains unresolved.

## Sources and scientific antecedents

These sources provide starting methods, concepts, and candidate data. They do not establish Lighthouse's proposed hypotheses. Links were checked on 25 September 2026. Documentation can change; studies should preserve the exact version they use.

### S1 Computer epidemics

Kephart and White, Directed graph epidemiological models of computer viruses, 1991. Models infection on directed networks and examines epidemic thresholds and imperfect defences. Relevant to propagation and removal; assumptions must be re-examined for each new system.

https://research.ibm.com/publications/directed-graph-epidemiological-models-of-computer-viruses

### S2 Digital ecology

Thomas S Ray, Evolution Ecology and Optimization of Digital Organisms, author-hosted account dated 1995. Describes self-replicating programs and ecological interactions in Tierra's contained virtual environment. Relevant to the distinction between replication, adaptation, and cooperation.

https://tomray.me/pubs/tierra/

### S3 Security incentives

Anderson and Moore, The Economics of Information Security, 2006. Examines misaligned incentives and costs imposed on others. Relevant to collective maintenance and the distribution of harm.

https://www.cl.cam.ac.uk/archive/rja14/Papers/sciecon2.pdf

### S4 Autonomous replication

Clymer, Wijk, and Barnes, The Rogue Replication Threat Model, METR, 2024. Examines infrastructure maintenance, resource acquisition, and resistance to shutdown. A threat analysis with stated uncertainty, rather than proof of an existing autonomous population.

https://metr.org/blog/2024-11-12-rogue-replication-threat-model/

### S5 Public software activity

GH Archive records public GitHub events. It can support a bounded activity study; event records alone do not provide all code diffs, deployments, or reliable AI attribution.

https://www.gharchive.org/

### S6 Agent telemetry

OpenTelemetry GenAI semantic conventions provide a vocabulary for model and agent instrumentation. Pin the convention version and check actual provider fields before adoption.

https://opentelemetry.io/docs/specs/semconv/gen-ai/

### S7 Identified AI traffic

Cloudflare AI Crawl Control documents measurements of identified crawler traffic within its observation boundary. Such traffic is not a census of autonomous agents or all internet activity.

https://developers.cloudflare.com/ai-crawl-control/features/analyze-ai-traffic/
