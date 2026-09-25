# Lighthouse Initial Research Programme

Launch sequence pilot studies and decisions

Founding edition 0.1 | 25 September 2026 | LH F04

The initial programme establishes one close observation of Harbour and one bounded outward survey. Its deliverable is a tested research practice: instruments with known limits, reproducible findings, and publications that can be corrected. The sequence below is an indicative twelve-week plan from project commencement, not a calendar booking or an approved spending commitment.

## Launch sequence

| Stage | Intended period | Work and completion evidence |
| --- | --- | --- |
| Establish | Weeks 1 and 2 | Assign owners, access and budgets; open study records; register instruments and sources |
| Calibrate | Weeks 3 and 4 | Run LH001; reconcile readings with known events; document overhead and gaps |
| Compare | Weeks 5 to 8 | Run LH002; repeat selected observations; test collection and cohort artefacts |
| Publish and review | Weeks 9 to 12 | Release reviewed studies and one synthesis; decide what to retain, change, or stop |

The periods can overlap where dependencies allow. If access or data quality prevents a study, complete the feasibility note and choose a replacement question. Do not broaden the claim to compensate for a small sample.

## Minimum useful observatory

The first release needs a question register, a versioned observation format, an instrument register, reproducible analysis, and a publication archive with correction history. A time-series view and a small dependency view are sufficient if their underlying readings are inspectable.

Begin with existing collection and storage tools. Build additional infrastructure only when a pilot demonstrates a specific limitation. Keep the work usable if Harbour integration is initially manual: study identifiers and links can precede automation.

## Completion criteria for this programme

Someone other than the analyst can reproduce at least one important result from the retained evidence and method. The documents explain a measurement failure or blind spot as clearly as a successful detection. At least one outward observation has been compared with its source's coverage limits. Lighthouse's own consumption is recorded. The next programme follows from what these studies teach us.

## LH001 Observing a known Harbour workflow

**Question.** Which parts of an ordinary workflow can our sensors reconstruct, and which consequential events do they miss?

**Design.** Select one bounded Harbour workflow with identifiable initiation, processing, communication, and completion records. Prefer a test environment or an existing routine task whose normal execution can be observed without changing its purpose. Capture an idle baseline, the workflow, and a declared follow-up window for persistent changes.

**Initial sample.** Use a calibration pilot of three repetitions under comparable conditions, with the ordering and collection interval recorded. Include one ordinary non-LLM operation where available to test whether the proposed signature is specific to inference. This is an instrument pilot, not a population estimate. Record each instance and task variation.

**Readings.** Start with task and dispatch timestamps, model-call usage where exposed, request metadata, host process activity where available, and versions of affected artefacts. Preserve remote calls as remote activity: local CPU readings do not measure a provider's inference compute. Add electricity only if the measurement boundary is defensible.

**Comparators.** Reconcile against operator-labelled events and Harbour's operational record. Examine disagreements at the event level. Include a known small coordination event if available, so the analysis tests whether low-volume activity with broad consequences remains visible.

**Analysis.** Produce an activity timeline, a flow account with duplicate observations identified, and a before-and-after state comparison. Report timing error, event detection, missingness, collection overhead, and the limits of inferred dependencies. Keep observed relationships separate from hypothesised causal links.

**Alternatives.** Check whether bursts reflect retries, scheduled jobs, cache behaviour, shared host load, or sensor overhead. Determine whether apparently persistent activity is ordinary background processing.

**Stop and output.** Close after the planned runs and reconciliation, or document why the instruments cannot answer the question. Produce a study, an instrument revision, and an observation sample suitable for sharing. No favourable hypothesis result is required.

**Execution record.** Before collection, fill in the owner, exact workflow, participating systems, access scope, retention, timing, resource ceiling, and review responsibility. LH001 proposes no change to Harbour's production behaviour.

## LH002 Mapping a bounded public software neighbourhood

**Question.** What can public activity reveal about change and dependency in a small software neighbourhood, and where does it fail to reveal running activity?

**Design.** Select up to ten public repositories from a declared ecosystem and observe a fixed twenty-eight-day historical window. Record selection criteria and the full cohort before analysis. Include a quieter or older project where feasible so activity does not become the selection rule.

**Sources.** Use GH Archive as a candidate event source and accessible repository histories for the code changes the question requires [S5 in LH F02]. Check event completeness and field definitions for the chosen dates. Capture dependency manifests only where available. Record archives and repository snapshots used.

**Readings.** Count events and active days, distinguish additions from deletions, and identify releases and manifest dependency changes. Separate bots explicitly identified in records from unknown contributors. Do not infer AI authorship from writing style or high output.

**Analysis.** Produce a time map of observed activity and a typed dependency map. Keep forks, vendored content, generated files, and repeated observations visible in the inclusion rules. Compare totals with rates per observed repository-day, showing missing intervals and cohort coverage.

**Interpretation boundary.** These readings describe public development activity. They do not establish deployed code, runtime traffic, operational importance, or the fraction of software produced by AI. The missing connection between source and operation is an intended finding about observability.

**Alternatives.** Check bulk imports, release schedules, repository migrations, changed collection, and normal dependency updates before explaining a spike as altered agent activity.

**Stop and output.** Close when the fixed window has been analysed and the coverage review completed. Publish the cohort, method, map, and one concise account of what cannot be inferred. A failure to retrieve adequate history produces a feasibility result and source assessment.

**Bridge outward.** Register published inference-use and identified-crawler series as separate candidate instruments. Their units, populations, and sampling differ from repository events; plotting them together must not imply that one caused the other. A later study may investigate an explicit connection.

**Execution record.** Name the owner, ecosystem, selection rule, dates, collection limits, retention, and resource ceiling before running the study. Recheck source availability and access conditions at commencement.

## Questions to follow the pilots

Choose follow-up work from observed gaps. Candidate questions include whether small control signals predict large downstream changes, which state changes survive after inference ends, and how much apparent growth comes from changed visibility. A later risk study could test whether the instruments distinguish benign repeated deployment from a propagation scenario in a contained model.

Prioritise questions by scientific value, decision relevance, evidence access, tractability, and cost. Record the reasoning rather than hiding it behind a single numerical priority score. Keep speculative essays connected to a question register so ideas can become testable when suitable evidence appears.

## Initial decision register

| Decision | Initial position | Revisit when |
| --- | --- | --- |
| Founding remit | Study computation and information flows; improve the study itself | The charter no longer supports useful inquiry |
| Observation scales | Close study of Harbour and bounded outward surveys | Evidence suggests a missing scale or subject |
| Attribution | Mixed human and AI activity is valid; unknown is explicit | A question needs stronger provenance |
| Architecture | Reuse tools and keep versioned evidence and methods | Pilots expose a concrete limitation |
| Publishing | Notes, studies, reports, articles, essays, and supporting artefacts | Readers cannot follow or verify the work |
| Risk programme | Scenario-based assessments with scope and confidence | Evidence supports a calibrated quantitative model |

## Assignments and choices for commencement

The steward records named owners, available access, a resource envelope, and publication responsibility. Choose the first Harbour workflow and public cohort. Decide the retention and sharing rules for those particular sources. These choices can be made when the studies open and need not delay use of the founding documents.

## The first public collection

Publish the founding charter, the LH001 study, the LH002 survey or feasibility result, and an account of the instruments. An accompanying essay can explain the activity, structure, and propagation model through the observed examples. Every visual identifies its sample and observation period.

Review the programme before commissioning further automation. Retain methods that produced useful evidence, repair weak instruments, and close questions that cannot currently be answered. The next investigation should be smaller and clearer because the first programme happened.
