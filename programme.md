# The programme

The questions Lighthouse is asking, what it has found, and what comes next. 25 September 2026, revised 26 September 2026. The records cite this document as LH F04. Sources in square brackets are numbered in sources.md.

The programme follows the order observatories have always followed: catalogue what is visible, calibrate on known objects, explain the mechanism, then measure the dynamics. It is paced by budget and evidence, not by a calendar, and outward work does not wait for local calibration: an outward study validates its own sources within its own boundary and says whose instruments supplied the evidence. The programme is done when someone other than the analyst can reproduce at least one important result from the retained evidence and method; when the records explain a measurement failure or blind spot as clearly as a detection; when at least one outward observation has been compared with its source's coverage limits, and one interpreted through the LH001 calibration or the study says why it could not be; when Lighthouse's own consumption is recorded; and when a synthesis states what the watch would now detect of a self-sustaining propagation pattern and what it would miss. The next programme follows from what these studies teach.

## Answered

**LH003 Survey of surveys.** Who already observes the computational world, which layer does each observatory see, and where does its coverage end? Thirty-four candidate observatories were considered and seventeen have a row. Each sees one layer from one narrow population: event archives and dependency resolvers see residue, broker rankings and vendor usage reports see activity, and vulnerability databases see disclosed flaws rather than their exploitation. None observes propagation directly, and none states how its population overlaps another's, so their counts cannot be added into a total. No source read can tell a person's action from an agent's. The record is studies/LH003/, with every source's row in studies/LH003/sources.md; the piece is articles/what-we-can-see.md. What it leaves open: how much the seventeen populations overlap, which only a joint sample can say.

**LH004 A historical propagation case.** What would the three layers have shown during a documented propagation event, and which layer carried the first detectable signal? The xz backdoor of 2024. The malicious code was public in release tarballs from 24 February, and nobody detected it there. Both signals that were noticed were activity: memory checker errors in a distribution's builds from 4 March, which the attacker answered with a fix, and one engineer's slow logins on 29 March. The first fitted no surface in the design, which gained a Correctness surface as a result. The distribution package pipelines the compromise travelled through are watched by none of the public observatories. The record is studies/LH004/; the piece is articles/the-xz-backdoor.md. What it leaves open: what an undetected case of the same kind would lack, which one detected case cannot say.

**LH000 One dispatch end to end.** A first look at what Harbour records about one of Lighthouse's own tasks and what the host shows while it runs. Harbour's record is of what was asked and what the agent claimed, not of what happened on the host, and the host was close to idle. The record is studies/LH000/.

## Next

### LH002 Mapping a bounded public software neighbourhood

**Question.** What can public activity reveal about change and dependency in a small software neighbourhood, and where does it fail to reveal running activity?

**Design.** Select up to ten public repositories from a declared ecosystem and observe a fixed twenty-eight-day historical window. Record the selection criteria and the full cohort before analysis. Include a quieter or older project where feasible so that activity does not become the selection rule.

**Sources.** Use GH Archive as the candidate event source [S5]. Use accessible repository histories for the code changes the question requires; Software Heritage can supply history that does not depend on the live forge [S10]. Capture dependency manifests where available and compare them with the resolved graphs in Open Source Insights [S11]. Check event completeness and field definitions for the chosen dates: GH Archive draws on GitHub's Events API and payload structures change. Record the archives and repository snapshots used.

**Readings.** Count events and active days, distinguish additions from deletions, and identify releases and manifest dependency changes. Separate bots explicitly identified in records from unknown contributors. Do not infer AI authorship from writing style or high output.

**Identity.** Contributor names and addresses are personal data even when public. Keep raw identifiers in the protected store. Publish counts, categories (identified bot, identified human account, unknown) and pseudonymous identifiers only.

**Analysis.** Produce a time map of observed activity and a typed dependency map. Where a dependency change in one repository is followed within the window by a change in a repository that depends on it, record the pair as a candidate propagation link and test the ordinary explanations (dependency-update bots, release trains, shared maintainers) before calling it anything else. Keep forks, vendored content, generated files and repeated observations visible in the inclusion rules. Compare totals with rates per observed repository-day, showing missing intervals and cohort coverage.

**Interpretation boundary.** These readings describe public development activity. They do not establish deployed code, runtime traffic, operational importance or the fraction of software produced by AI. The missing connection between source and operation is an intended finding about observability.

**Alternatives.** Check bulk imports, release schedules, repository migrations, changed collection and normal dependency updates before explaining a spike as altered agent activity.

**Stop and output.** Close when the fixed window has been analysed and the coverage review completed. Publish the cohort, method, map and one concise account of what cannot be inferred. A failure to retrieve adequate history produces a feasibility result and a source assessment.

**Bridge outward.** Register published inference-use and identified-crawler series [S7] as separate candidate instruments. Their units, populations and sampling differ from repository events; plotting them together must not imply that one caused the other. A later study may investigate an explicit connection.

**Execution record.** Name the ecosystem, the selection rule, the dates, the collection limits, retention and the resource ceiling in the study's brief before running it, and recheck source availability and access conditions at commencement. The window is historical, so the observation is of the public record, not of live activity, and the study says so.

### LH001 Observing a known Harbour workflow

**Question.** Which parts of an ordinary workflow can our sensors reconstruct, and which consequential events do they miss?

**Role.** LH001 is Lighthouse's standard candle: a workflow whose inputs are recorded, observed by the instruments that will later observe unknown activity. Its published signature is what makes outward readings interpretable rather than merely countable.

**Design.** Select one bounded Harbour workflow with identifiable initiation, processing, communication and completion records. Prefer a test environment or an existing routine task whose normal execution can be observed without changing its purpose. Choose a dispatch target whose host can be instrumented: a command-line or local agent runs on a machine Lighthouse can observe, whereas a web session runs on a provider's infrastructure and exposes only what the provider reports. Capture an idle baseline, the workflow, and a declared follow-up window for persistent changes.

**Initial sample.** Use a calibration run of three repetitions under comparable conditions, with the ordering and collection interval recorded. Include one ordinary non-LLM operation where available, such as a CI run or a dependency install, to test whether the proposed signature is specific to inference. This is an instrument calibration, not a population estimate. Record each instance and task variation.

**Readings.** Start with Harbour's dispatch fields (identifier, kind, target, model, harness, effort, queue and claim times), feedback entries with their timestamps and terminal marker, usage entries and proxy audit entries [S12]; the repository's pull request, review, CI and merge records; host process activity where available; and versions of affected artefacts. Preserve remote calls as remote activity: local CPU readings do not measure a provider's inference compute. Add electricity only if the measurement boundary is defensible.

**Retention.** Harbour's records are time-limited: dispatch items expire after twenty-four hours, and feedback, status and audit records after thirty days, at the time of writing. Export what the study needs within them and record each export as an observation. Repository and CI records persist longer and can anchor the follow-up window, which is proposed as seven days after the last repetition.

**Comparators.** Reconcile against operator-labelled events and Harbour's operational record. That record is server-timestamped for queueing and claiming but agent-reported for progress and completion, so treat the agent-reported parts as claims to be checked, not as ground truth. Examine disagreements at the event level. Include a known small coordination event if available, so the analysis tests whether low-volume activity with broad consequences remains visible.

**Analysis.** Produce an activity timeline, a flow account with duplicate observations identified, a before-and-after state comparison, and a record of any subsequent activity the change enabled within the follow-up window, such as further dispatches, CI runs or deployments. That last record is the smallest observable instance of propagation and gives the follow-up window its purpose. Report timing error, event detection, missingness, collection overhead and the limits of inferred dependencies. Keep observed relationships separate from hypothesised causal links. Publish the calibration in a form later studies can cite: signal per token, per request and per change, with the instrument version and boundary.

**Alternatives.** Check whether bursts reflect retries, scheduled jobs, cache behaviour, shared host load or sensor overhead. Determine whether apparently persistent activity is ordinary background processing.

**Stop and output.** Close after the planned runs and reconciliation, or document why the instruments cannot answer the question. Produce a study, an instrument revision and an observation sample suitable for sharing. No favourable hypothesis result is required.

**Execution record.** Before collection, write the study's brief with the exact workflow, participating systems, dispatch target, access scope, retention, timing, resource ceiling and review responsibility. LH001 proposes no change to Harbour's production behaviour.

## Questions after these

Choose follow-up work from observed gaps. Candidate questions include whether small control signals predict large downstream changes, which state changes survive after inference ends, how much apparent growth comes from changed visibility, which layer carries the earliest detectable signal in a propagation event, whether a standard candle measured on one workflow transfers to another, and which of Harbour's own workflow findings leave a computational signature that an outside observer could detect. A later risk study could test whether the instruments distinguish benign repeated deployment from a propagation scenario in a contained model.

Prioritise questions by scientific value, decision relevance, evidence access, tractability and cost. Record the reasoning rather than hiding it behind a single numerical priority score. Keep speculative essays connected to the question register so that ideas can become testable when suitable evidence appears.

The first public collection holds the charter, LH003 and LH004 with their pieces, and will hold LH001, LH002 or its feasibility result, and an account of the instruments. Every visual identifies its sample and observation period. When the programme is reviewed, retain the methods that produced useful evidence, repair weak instruments, and close questions that cannot currently be answered. The next investigation should be smaller and clearer because the first programme happened.
