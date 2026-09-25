# Lighthouse Research Design

Observation, measurement and risk assessment

Founding edition 0.2 (draft) | 25 September 2026 | LH F02

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

The study templates (LH F05) supply the instrument, observation, claim and study records. An instrument record explains what the sensor actually detects, what it misses, how it was calibrated, its expected overhead and which changes could invalidate comparisons.

### Four kinds of statement

An observation reports a captured event or reading. A derived measurement applies a stated transformation to observations. An interpretation proposes what a pattern means. A scenario explores what might happen under explicit assumptions. Publications label these distinctions wherever a reader could otherwise confuse them.

Every material claim identifies its supporting evidence, method version, scope, competing explanations and confidence rationale. Confidence increases through suitable evidence, calibration and replication. It is not a score obtained by asking several models whether they agree.

### Calibration and validation

Use known events, repeatable workloads and independently recorded operational outcomes to test detection and timing. Measure false positives and missed events where labels allow it.

A standard candle is a source whose intrinsic output is known, so that its observed signal calibrates the instrument and scales unknown sources. LH001's workflow is Lighthouse's first: a dispatch with recorded tokens, requests and changes, observed by the same instruments that will later observe unknown activity. A standard candle is valid only within the instrument, observation point and boundary it was measured with, and only while the relation between input and signature holds; re-check it when any of those change. An outward reading interpreted through a standard candle carries the candle's version.

Harbour's records are the first comparator [S12]. They are server-timestamped for queueing and claiming, but progress and completion are reported by the agent itself, so they show what was asked and what was claimed rather than what happened on the host. They may be incomplete or share a failure with the sensor. At the time of writing, dispatch items expire after twenty-four hours and feedback, status and audit records are retained for thirty days, so the export rule above applies.

Separate exploratory findings from tests specified in advance. Preserve failed runs and protocol changes. When comparing workflows, declare the unit of comparison, task selection, sample size rationale, exclusions and likely confounders. A pilot calibrates a method; a small convenience sample cannot estimate internet-wide prevalence.

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

The name borrows from Kessler and Cour-Palais, who described how collisions between orbiting objects could generate debris faster than it decays, degrading the usability of an orbit [S8]. For Lighthouse, the hypothesis is a proposed scenario in which harmful digital activity creates further harmful capacity, replenishes itself after its initial support ends, and degrades the usability of shared infrastructure. The name is an analogy. It is not a physical law and not a finding that the condition exists.

In the three layers, the hypothesis predicts a distinctive propagation signature: residue left by one burst of activity enabling similar activity elsewhere, repeated until the population's continuity is visible even as its individual processes disappear. Measurements could in principle reveal reproduction, persistence and expanding influence before every local action is understood. They could equally reveal an ordinary release train, which is why the competing explanations below are tested first.

Evidence would need to distinguish continuing external support from endogenous replacement, successful reproduction from repeated attempts, and real environmental degradation from rising counts or improved detection. Benign deployment, scheduled automation and common external triggers are competing explanations for apparent propagation.

Studies can begin with historical evidence and contained models. Any claim of a growth threshold must specify the population, resources, removal processes and assumptions used. The thresholds in established computer-epidemic models are relevant antecedents, not universal constants for agent networks [S1].

### Decision and review

A published assessment names its author, evidence reviewer, as-of date, time horizon, expiry or review trigger, and practical implication. Evidence might justify adding an instrument, investigating a dependency or revising a scenario. The report says which decision it informs and what remains unresolved.

## Sources and scientific antecedents

These sources provide starting methods, concepts and candidate data. They do not establish Lighthouse's proposed hypotheses. Links were checked on 25 September 2026 from an automated environment; each note records what the check could and could not confirm. Documentation changes, so studies preserve the exact version they use.

### S1 Computer epidemics

Kephart and White, Directed-graph epidemiological models of computer viruses, IEEE Symposium on Security and Privacy, 1991. Models infection on directed networks and examines epidemic thresholds and imperfect defences. Relevant to propagation and removal; assumptions must be re-examined for each new system. Checked: page resolves and matches.

https://research.ibm.com/publications/directed-graph-epidemiological-models-of-computer-viruses

### S2 Digital ecology

Thomas S Ray, Evolution, Ecology and Optimization of Digital Organisms. Written in 1992 as a Santa Fe Institute working paper; the author-hosted HTML copy carries a 1995 conversion date. Describes self-replicating programs and ecological interactions in Tierra's contained virtual environment. Relevant to the distinction between replication, adaptation and cooperation. Checked: page resolves; it states no venue or year itself, so cite the 1992 working paper.

https://tomray.me/pubs/tierra/

### S3 Security incentives

Anderson and Moore, The Economics of Information Security, Science, 2006. Examines misaligned incentives and costs imposed on others. Relevant to collective maintenance and the distribution of harm. Checked: the link resolves to an eleven-page PDF whose text could not be extracted in the checking environment; confirm the content on first use.

https://www.cl.cam.ac.uk/archive/rja14/Papers/sciecon2.pdf

### S4 Autonomous replication

Josh Clymer, Hjalmar Wijk and Beth Barnes, The Rogue Replication Threat Model, METR, 12 November 2024. Examines infrastructure maintenance, resource acquisition and resistance to shutdown. A threat analysis with stated disagreement among its authors about likelihood, not proof of an existing autonomous population. Checked: page resolves and matches.

https://metr.org/blog/2024-11-12-rogue-replication-threat-model/

### S5 Public software activity

GH Archive records public GitHub events as hourly JSON files from February 2011. Records to 2014 came from GitHub's retired Timeline API and records from 2015 onward from the Events API; payload structure varies by event type and can change. It can support a bounded activity study; event records alone do not provide all code diffs, deployments or reliable AI attribution. Checked: page resolves and matches.

https://www.gharchive.org/

### S6 Agent telemetry

OpenTelemetry semantic conventions for generative AI provide a vocabulary for model and agent instrumentation, including spans, metrics and events for model clients and the Model Context Protocol. Checked: the URL cited in edition 0.1 now carries a notice that the conventions have moved to a dedicated repository. Use the repository, pin a commit, and check actual provider fields before adoption. The move is itself an example of why versions are recorded.

https://github.com/open-telemetry/semantic-conventions-genai

### S7 Identified AI traffic

Cloudflare AI Crawl Control documents measurements of identified crawler traffic within one Cloudflare zone: requests, status codes, bandwidth, content types and most-requested paths, filterable by operator and crawler. Such traffic is not a census of autonomous agents or of all internet activity. Checked: page resolves; last updated 23 April 2026.

https://developers.cloudflare.com/ai-crawl-control/features/analyze-ai-traffic/

### S8 Orbital debris

Kessler and Cour-Palais, Collision frequency of artificial satellites: the creation of a debris belt, Journal of Geophysical Research 83(A6), 1978. The origin of the analogy in the digital Kessler hypothesis. Checked through the DOI's Crossref record; the publisher page was not retrievable from the checking environment.

https://doi.org/10.1029/JA083iA06p02637

### S9 Research ethics for ICT

The Menlo Report: Ethical Principles Guiding Information and Communication Technology Research, US Department of Homeland Security, August 2012. States four principles: respect for persons, beneficence, justice, and respect for law and public interest. Relevant to collection boundaries and to studies that observe people's work. Checked: PDF resolves and matches.

https://www.caida.org/catalog/papers/2012_menlo_report_actual_formatted/menlo_report_actual_formatted.pdf

### S10 Archived source history

Software Heritage archives source code with full development history from many forges and issues persistent identifiers for code. A candidate source of repository history for LH002 that does not depend on a live forge. Checked: the documentation site and API index resolved; the main site returned an error during the check.

https://docs.softwareheritage.org/

### S11 Dependency graphs

Open Source Insights (deps.dev) resolves dependency graphs for Cargo, Go, Maven, npm, NuGet, PyPI and RubyGems, with security advisories, an HTTP and gRPC API, and a public BigQuery dataset. A candidate source of typed dependency relationships for LH002. Its graphs are resolved from manifests and do not show what is deployed. Checked: documentation resolves and matches.

https://docs.deps.dev/

### S12 Harbour records

Harbour's dispatch and proxy integration documentation describes the dispatch item fields, lifecycle states, feedback markers, usage entries, audit logging and retention windows referred to in LH F03 and LH F04. Checked on 25 September 2026 against the main branch; verify against the running version before a study relies on a field.

https://github.com/JKershaw/LinearViewer/blob/main/docs/dispatch-integration.md
https://github.com/JKershaw/LinearViewer/blob/main/docs/proxy-integration.md

### S13 Harbour papers standard

Harbour's writing standard for papers and essays defines the header fields and the Answer, Findings, Method, Limits and Next structure that Lighthouse studies adopt in LH F03. Checked: page resolves and matches.

https://github.com/JKershaw/LinearViewer/blob/main/docs/papers/standard.md

### S14 The xz backdoor report

Andres Freund, backdoor in upstream xz/liblzma leading to ssh server compromise, oss-security list, 29 March 2024. A first-hand account of detecting the compromise from ssh logins taking unusual CPU and running more slowly. The primary source for the activity-layer detection in LH004. Checked: page resolves and matches.

https://www.openwall.com/lists/oss-security/2024/03/29/4

### S15 CVE-2024-3094

National Vulnerability Database record for the xz backdoor: malicious code in upstream tarballs from version 5.6.0, published 29 March 2024, base score 10.0. Checked through the NVD API on 25 September 2026; the web page renders with scripts and was not readable from the checking environment.

https://nvd.nist.gov/vuln/detail/CVE-2024-3094

### S16 CVE-2021-44228

National Vulnerability Database record for Log4Shell: remote code execution through Log4j 2 message lookups, published 10 December 2021, base score 10.0. A propagation case through the Java dependency graph. Checked through the NVD API as above.

https://nvd.nist.gov/vuln/detail/CVE-2021-44228

### S17 The left-pad removal

npm, kik, left-pad, and npm, 23 March 2016. Account of an unpublished package causing hundreds of dependent build failures per minute, and restoration within hours. A propagation case for a removal rather than an addition. Checked: page resolves and matches.

https://blog.npmjs.org/post/141577284765/kik-left-pad-and-npm

### S18 Cloudflare Radar

Documentation for Cloudflare's published view of global traffic, attacks and technology adoption, with a free API under a non-commercial licence, derived from Cloudflare's network and its public resolver. An observation boundary, not the internet. Checked: documentation resolves; the Radar site itself refused the checking environment.

https://developers.cloudflare.com/radar/

### S19 OpenRouter rankings

Live model usage ranked by tokens processed through one API broker. Its population is that broker's developers, not inference generally. Checked: page resolves; data shown through 24 September 2026.

https://openrouter.ai/rankings
