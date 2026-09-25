# Lighthouse Initial Research Programme

Launch sequence, first studies and decisions

Founding edition 0.2 (draft) | 25 September 2026 | LH F04

The initial programme establishes one close observation of Harbour, one bounded outward survey, a catalogue of the surveys that already exist, and one historical case. It follows the order observatories have always followed: catalogue, calibrate, explain, then dynamics. Its deliverable is a tested research practice: instruments with known limits, reproducible findings and publications that can be corrected. The sequence below is an indicative twelve-week plan from commencement, not a calendar booking or an approved spending commitment.

## Launch sequence

| Stage | Intended period | Work and completion evidence |
| --- | --- | --- |
| Establish | Weeks 1 and 2 | Assign owners, access and budgets; open study records; register instruments and sources; confirm Harbour's current record fields and retention; run LH003, which needs only reading |
| Calibrate | Weeks 3 and 4 | Run LH001, the standard candle; export Harbour records; reconcile readings with known events; document overhead and gaps; write LH004 |
| Compare | Weeks 5 to 8 | Run LH002; interpret one outward series through the LH001 calibration; repeat selected observations; test collection and cohort artefacts |
| Publish and review | Weeks 9 to 12 | Release reviewed studies and one synthesis; decide what to retain, change or stop |

The periods can overlap where dependencies allow. If access or data quality prevents a study, complete the feasibility note and choose a replacement question. Do not broaden the claim to compensate for a small sample.

## Minimum useful observatory

The first release needs a question register, a versioned observation format, an instrument register, reproducible analysis and a publication archive with correction history. The templates in LH F05 are the starting forms. A time-series view and a small dependency view are sufficient if their underlying readings are inspectable.

Begin with existing collection and storage tools. Build additional infrastructure only when a study demonstrates a specific limitation. Keep the work usable if Harbour integration is initially manual: study identifiers and links can precede automation.

## Completion criteria for this programme

Someone other than the analyst can reproduce at least one important result from the retained evidence and method. The documents explain a measurement failure or blind spot as clearly as a successful detection. At least one outward observation has been compared with its source's coverage limits, and one has been interpreted through the LH001 calibration, or the study says why it could not be. Lighthouse's own consumption is recorded. The next programme follows from what these studies teach us.

## LH001 Observing a known Harbour workflow

**Question.** Which parts of an ordinary workflow can our sensors reconstruct, and which consequential events do they miss?

**Role.** LH001 is Lighthouse's standard candle: a workflow whose inputs are recorded, observed by the instruments that will later observe unknown activity. Its published signature is what makes outward readings interpretable rather than merely countable.

**Design.** Select one bounded Harbour workflow with identifiable initiation, processing, communication and completion records. Prefer a test environment or an existing routine task whose normal execution can be observed without changing its purpose. Choose a dispatch target whose host can be instrumented: a command-line or local agent runs on a machine Lighthouse can observe, whereas a web session runs on a provider's infrastructure and exposes only what the provider reports. Capture an idle baseline, the workflow, and a declared follow-up window for persistent changes.

**Initial sample.** Use a calibration run of three repetitions under comparable conditions, with the ordering and collection interval recorded. Include one ordinary non-LLM operation where available, such as a CI run or a dependency install, to test whether the proposed signature is specific to inference. This is an instrument calibration, not a population estimate. Record each instance and task variation.

**Readings.** Start with Harbour's dispatch fields (identifier, kind, target, model, harness, effort, queue and claim times), feedback entries with their timestamps and terminal marker, usage entries and proxy audit entries [S12 in LH F02]; the repository's pull request, review, CI and merge records; host process activity where available; and versions of affected artefacts. Preserve remote calls as remote activity: local CPU readings do not measure a provider's inference compute. Add electricity only if the measurement boundary is defensible.

**Retention.** At the time of writing, Harbour's feedback, status and audit records are retained for thirty days and dispatch items expire after twenty-four hours. Export what the study needs within that window and record each export as an observation. Repository and CI records persist longer and can anchor the follow-up window, which is proposed as seven days after the last repetition.

**Comparators.** Reconcile against operator-labelled events and Harbour's operational record. That record is server-timestamped for queueing and claiming but agent-reported for progress and completion, so treat the agent-reported parts as claims to be checked, not as ground truth. Examine disagreements at the event level. Include a known small coordination event if available, so the analysis tests whether low-volume activity with broad consequences remains visible.

**Analysis.** Produce an activity timeline, a flow account with duplicate observations identified, a before-and-after state comparison, and a record of any subsequent activity the change enabled within the follow-up window, such as further dispatches, CI runs or deployments. That last record is the smallest observable instance of propagation and gives the follow-up window its purpose. Report timing error, event detection, missingness, collection overhead and the limits of inferred dependencies. Keep observed relationships separate from hypothesised causal links. Publish the calibration in a form later studies can cite: signal per token, per request and per change, with the instrument version and boundary.

**Alternatives.** Check whether bursts reflect retries, scheduled jobs, cache behaviour, shared host load or sensor overhead. Determine whether apparently persistent activity is ordinary background processing.

**Stop and output.** Close after the planned runs and reconciliation, or document why the instruments cannot answer the question. Produce a study, an instrument revision and an observation sample suitable for sharing. No favourable hypothesis result is required.

**Execution record.** Before collection, complete the brief in LH F05 with the owner, exact workflow, participating systems, dispatch target, access scope, retention, timing, resource ceiling and review responsibility. LH001 proposes no change to Harbour's production behaviour.

## LH002 Mapping a bounded public software neighbourhood

**Question.** What can public activity reveal about change and dependency in a small software neighbourhood, and where does it fail to reveal running activity?

**Design.** Select up to ten public repositories from a declared ecosystem and observe a fixed twenty-eight-day historical window. Record the selection criteria and the full cohort before analysis. Include a quieter or older project where feasible so that activity does not become the selection rule.

**Sources.** Use GH Archive as the candidate event source [S5 in LH F02]. Use accessible repository histories for the code changes the question requires; Software Heritage can supply history that does not depend on the live forge [S10 in LH F02]. Capture dependency manifests where available and compare them with the resolved graphs in Open Source Insights [S11 in LH F02]. Check event completeness and field definitions for the chosen dates: GH Archive draws on GitHub's Events API and payload structures change. Record the archives and repository snapshots used.

**Readings.** Count events and active days, distinguish additions from deletions, and identify releases and manifest dependency changes. Separate bots explicitly identified in records from unknown contributors. Do not infer AI authorship from writing style or high output.

**Identity.** Contributor names and addresses are personal data even when public. Keep raw identifiers in the protected store. Publish counts, categories (identified bot, identified human account, unknown) and pseudonymous identifiers only.

**Analysis.** Produce a time map of observed activity and a typed dependency map. Where a dependency change in one repository is followed within the window by a change in a repository that depends on it, record the pair as a candidate propagation link and test the ordinary explanations (dependency-update bots, release trains, shared maintainers) before calling it anything else. Keep forks, vendored content, generated files and repeated observations visible in the inclusion rules. Compare totals with rates per observed repository-day, showing missing intervals and cohort coverage.

**Interpretation boundary.** These readings describe public development activity. They do not establish deployed code, runtime traffic, operational importance or the fraction of software produced by AI. The missing connection between source and operation is an intended finding about observability.

**Alternatives.** Check bulk imports, release schedules, repository migrations, changed collection and normal dependency updates before explaining a spike as altered agent activity.

**Stop and output.** Close when the fixed window has been analysed and the coverage review completed. Publish the cohort, method, map and one concise account of what cannot be inferred. A failure to retrieve adequate history produces a feasibility result and a source assessment.

**Bridge outward.** Register published inference-use and identified-crawler series [S7 in LH F02] as separate candidate instruments. Their units, populations and sampling differ from repository events; plotting them together must not imply that one caused the other. A later study may investigate an explicit connection.

**Execution record.** Name the owner, ecosystem, selection rule, dates, collection limits, retention and resource ceiling before running the study. Recheck source availability and access conditions at commencement.

## LH003 Survey of surveys

**Question.** Who already observes the computational world, which layer does each observatory see, and where does its coverage end?

**Design.** Reading only; no collection. For each existing observatory record the layer observed (activity, residue or propagation), the population, the observation boundary, the unit, the cadence, access conditions and licence, and the revision policy. Candidates include GH Archive [S5 in LH F02], Cloudflare AI Crawl Control and Cloudflare Radar [S7, S18], Software Heritage [S10], Open Source Insights [S11], OpenRouter's rankings [S19], the vulnerability databases [S15, S16], and any others the study finds. Record each source's version at the check date.

**Output.** A table and a short report, with coverage boundaries drawn on the map rather than left in footnotes, and a register entry for each source that could serve as a Lighthouse instrument.

**Interpretation boundary.** A survey of surveys describes the luminous fraction as others have measured it. It establishes no phenomenon and estimates no total.

**Stop and output.** Close when every candidate has a row or a recorded reason for exclusion.

## LH004 A historical propagation case

**Question.** What would Lighthouse's three layers have shown during a documented propagation event, and which layer carried the first detectable signal?

**Design.** Retell one documented case from the public record. First choice is the xz backdoor of 2024 [S14, S15 in LH F02]: activity in the build-time injection and the altered behaviour of the ssh server; residue in compromised tarballs carried into distributions; propagation through distribution updates; detection by an engineer investigating unusual CPU use and slower logins. Alternatives are Log4Shell [S16], propagation through the Java dependency graph, and the left-pad removal [S17], propagation of an absence through npm within hours.

**Analysis.** For each layer, state what was observable, from where, by whom, at what delay, and which instrument in LH F02's table would have recorded it. Build the timeline from cited sources only.

**Interpretation boundary.** These are cases that were detected, so the sample has survivor bias. Say what an undetected case would lack.

**Stop and output.** One case, one essay in the Harbour standard's essay form with an annotated reading list. It is the first piece intended to be read outside the project.

## Questions to follow the first studies

Choose follow-up work from observed gaps. Candidate questions include whether small control signals predict large downstream changes, which state changes survive after inference ends, how much apparent growth comes from changed visibility, which layer carries the earliest detectable signal in a propagation event, whether a standard candle measured on one workflow transfers to another, and which of Harbour's own workflow findings leave a computational signature that an outside observer could detect. A later risk study could test whether the instruments distinguish benign repeated deployment from a propagation scenario in a contained model.

Prioritise questions by scientific value, decision relevance, evidence access, tractability and cost. Record the reasoning rather than hiding it behind a single numerical priority score. Keep speculative essays connected to the question register so that ideas can become testable when suitable evidence appears.

## Initial decision register

| Decision | Initial position | Revisit when |
| --- | --- | --- |
| Founding remit | Study computation and information flows; improve the study itself | The charter no longer supports useful inquiry |
| Observation scales | Close study of Harbour and bounded outward surveys | Evidence suggests a missing scale or subject |
| Sequence | Catalogue, calibrate, explain, then dynamics | Calibration fails to transfer, or a dynamics question becomes tractable earlier |
| Attribution | Mixed human and AI activity is valid; unknown is explicit | A question needs stronger provenance |
| Architecture | Reuse tools and keep versioned evidence and methods | The first studies expose a concrete limitation |
| Publishing | Notes, studies, reports, articles, essays and supporting artefacts | Readers cannot follow or verify the work |
| Publication format | Adopt Harbour's paper structure and header, with Lighthouse additions | Reviewers or readers find the shared form insufficient |
| Source retention | Export time-limited records within their window and record the export | A source offers durable access or its window changes |
| Risk programme | Scenario-based assessments with scope and confidence | Evidence supports a calibrated quantitative model |

## Assignments and choices for commencement

The steward records named owners, available access, a resource envelope and publication responsibility. Choose the first Harbour workflow and its dispatch target, and the public cohort. Decide the retention and sharing rules for those particular sources. These choices can be made when the studies open and need not delay use of the founding documents.

## The first public collection

Publish the founding charter, the LH003 survey of surveys, the LH004 essay, the LH001 study, the LH002 survey or feasibility result, and an account of the instruments. An accompanying essay can explain the activity, structure and propagation model through the observed examples. Every visual identifies its sample and observation period.

Review the programme before commissioning further automation. Retain methods that produced useful evidence, repair weak instruments, and close questions that cannot currently be answered. The next investigation should be smaller and clearer because the first programme happened.
