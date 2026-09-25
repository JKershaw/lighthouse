# Lighthouse Operating Handbook

Research organisation publication and stewardship

Founding edition 0.1 | 25 September 2026 | LH F03

Lighthouse begins as a small research practice with bounded investigations and a visible evidence trail. This handbook sets initial operating defaults. Responsibilities may be combined while the project is small, but responsibility and the independence of review must remain explicit.

## A small research desk

The founding steward chooses priorities, allocates resources, and assigns an accountable owner to each investigation. The research owner defines the question and produces an evidence packet. A methods reviewer checks collection and analysis. An editor prepares the publication and records its release decision.

Agents may perform parts of each role within a declared scope. The person responsible for a study remains identifiable. If one person fills several roles, the publication records that limitation rather than implying independent review.

## The investigation lifecycle

An idea enters the question register with a reason it matters. Before work starts, its owner writes a brief specifying scope, available evidence, alternatives, intended output, resource limit, and stopping condition. The study receives a stable identifier.

Collection produces versioned observations and instrument records. Analysis produces reproducible transformations and candidate claims. Review checks whether the evidence supports those claims. Publication exposes the relevant account and its limitations. The study then closes or names a specific follow-up question.

Exploratory work is welcome and labelled. If an unexpected pattern changes the study, record the protocol amendment before treating the new question as a confirmatory test. A failed collection or inconclusive result can close a study successfully when it explains the limitation and next useful measurement.

### Suggested starting capacity

Keep one close-observation study and one outward study active. Maintain a small methods queue. Admit another investigation when an existing one closes or a documented reason justifies the additional load. These are workload defaults, not claims about team size or funding.

Each brief defines a bounded discovery allowance and a full execution ceiling before incurring new paid usage. Record existing service consumption as well as new spend. Reaching a limit produces a status record and a decision about further work; it does not silently extend the investigation.

## Harbour and the observatory

Harbour can coordinate work, while Lighthouse maintains the scientific record. Their connection should be an explicit, inspectable interface so a task's completion cannot silently become a verified research finding.

| Component | Responsibility | Durable record |
| --- | --- | --- |
| Harbour coordination | Assign and track bounded work | Task and dispatch references |
| Collection | Capture permitted readings | Observations and sensor versions |
| Analysis | Transform and compare evidence | Methods, runs, and claim records |
| Review and publication | Assess and communicate findings | Release and correction records |

## The integration contract

A research task should carry a study identifier, question, evidence references, scope, resource ceiling, stopping condition, and expected artefact. A completed task returns output locations, method version, run status, consumption, unresolved issues, and candidate claims.

Link Harbour task and run identifiers to Lighthouse study and observation identifiers where available. Retain one canonical study record and references to the operational records. Document identifiers that cannot be joined reliably rather than manufacturing continuity.

When Harbour is also the subject, record the overlap. Check collection against another observation point where possible. Sensor failures and missing operational records may share a cause, so agreement between them is not sufficient on its own.

## Initial technical shape

Use a versioned document and method repository, a protected store for observations, reproducible analysis jobs, and a static publication surface. An index can connect studies, instruments, claims, and releases. These are logical components; existing tools can supply them.

Begin with the smallest collector and analysis that answer the first question. Adopt existing telemetry conventions where they fit [S6 in LH F02]. A custom event service, graph database, or continuously running research agent should follow an observed need.

Every view shows the observation period, units, scope, sampling, freshness, missingness, and method version. Views of activity, flow, and structure share identifiers and time controls where practical. Colour represents a declared quantity; visual prominence does not silently mean importance or risk.

Tag Lighthouse collection and research traffic. Measure or estimate its overhead with the method stated. Keep a clean distinction between observed events and simulated examples in both storage and display.

## Publication practice

Lighthouse publishes at several levels of depth. The same evidence may support several forms, each with its own purpose. A short explanation should retain the qualifications that materially affect its meaning.

| Output | Reader need | Evidence expectation |
| --- | --- | --- |
| Notebook and blog | Follow work as it develops | Dated observations and open questions |
| Study | Inspect one investigation | Protocol, method, results, limitations |
| Report | Understand several findings | Traceable synthesis and implications |
| Article and essay | Explore an interpretation | Sources and clear separation of conjecture |
| Dataset or instrument | Reproduce and extend work | Version, scope, documentation, conditions |

## The release check

The editor checks that material factual claims have support, primary sources have been read where relevant, charts use stated denominators, and uncertainties remain attached to the claims they qualify. Model-generated source summaries need verification against the source.

The methods reviewer reproduces the important calculation or explains why reproduction was not possible. Review includes at least one plausible competing explanation. A second agent's agreement is a review contribution, not independent empirical confirmation.

The release record names the responsible person, versions of the evidence and method, publication date, evidence cutoff, and any restrictions on access to supporting material. Public communication and external publication follow the authority already granted to the project; drafting a publication does not itself release it.

## Corrections and retirement

Keep a stable identity for each publication. Corrected editions state what changed, why, and whether conclusions changed. Preserve earlier editions where appropriate. A withdrawn claim remains traceable with its withdrawal reason.

Time-sensitive assessments state a review trigger or expiry. A superseded map is marked with its observation period rather than silently presented as current. An instrument can be retired when its source disappears or its assumptions no longer hold.

The first public surface should make it easy to find the remit, current investigations, publications, methods, and corrections. A modest searchable archive is sufficient for the initial programme.

## Stewardship and research boundaries

Prefer metadata and aggregate readings when they answer the question. Record access scope, retention, and sharing conditions before collection. Separate private evidence from public releases. Avoid collecting credentials or raw customer content as incidental telemetry.

Observe public sources and participating systems within their permitted access. Changes to an observed system belong to a separately scoped experiment. Studies of harmful propagation begin with literature, historical evidence, or contained simulations; operational deployment of a worm is not part of this founding programme.

Lighthouse's relationship with Harbour is disclosed in studies where it matters. Commercial or organisational interests, provider visibility limits, and selection of convenient subjects should be recorded as potential sources of bias.

## Changes to the practice

The charter holds the stable purpose and commitments. Instrument specifications, research methods, and operating defaults can evolve through versioned decisions. A methods change that affects historical comparisons creates a new version and an explanation of comparability.

Use a short decision record: question, options considered, choice, reason, owner, date, and condition for revisiting it. Separate settled founding scope from provisional implementation choices. Do not let an early tool choice become a scientific assumption.

## Reviewing progress

At the end of the initial programme, review the clarity gained, instruments calibrated, claims reproduced or corrected, evidence gaps made visible, and cost of maintaining the work. Ask whether a reader or operator made a better-informed decision because of the findings.

Publication count and task completion may describe throughput, but they do not establish understanding. Useful progress can include showing that a proposed metric fails, or that an attractive metaphor does not predict the observations.

## Responsibility before launch

Name the founding steward, study owners, and release responsibility. Record actual budget and access boundaries for the first studies. These assignments are operational records to complete when execution begins; the founding documents do not presume a funded team or existing integration.

Use the templates in the editable source bundle to open the first studies, register the instruments, and preserve the initial decisions. Revise this handbook after the first completed studies reveal which parts of the process are necessary.
