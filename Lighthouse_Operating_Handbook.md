# Lighthouse Operating Handbook

Research organisation, publication and responsibility

Draft | 25 September 2026 | LH F03

Lighthouse begins as a small research practice with bounded investigations and a visible evidence trail. This handbook sets initial operating defaults. Responsibilities may be combined while the project is small, but responsibility and the independence of review must remain explicit.

## A watch kept by agents, read by people

Most of Lighthouse's work is done by AI agents: collection, analysis, source checking, drafting and the upkeep of the registers, dispatched as bounded tasks within a stated budget and scope. Agents also review and release, so that publication never waits on a person. People set the direction, read what interests them, and keep the few decisions LH F01 reserves for a person. Agent output is the ordinary case; a person's reading is the scarce resource, and the practice is arranged so that it is spent on judgement. The session that drives the watch is itself an observer, and its own runs are part of the record it exports.

Four functions run through the work, and any of them may be filled by an agent. The keeper, the person who keeps the light lit and sets its direction, chooses priorities and sets the budget. The owner of a study defines its question and answers for its evidence packet. A reviewer checks collection, analysis and claims against the sources. An editor turns a record into a piece. The record of each study and each piece says which of these were done by which agent or person, and which checks were independent.

A piece is released by the process: it goes out when a review on the strongest available model finds nothing that must be fixed, and its release note says so. A person can pull anything, and the decisions LH F01 reserves for a person wait for one. If the same agent or person fills several functions, the record says so rather than implying independent review.

## The investigation lifecycle

An idea enters the question register with a reason it matters, whether a person or an agent proposed it. Before work starts, its owner writes a brief specifying scope, available evidence, alternatives, intended output, resource limit and stopping condition. The study receives a stable identifier of the form LHnnn. The templates in LH F05 provide the register entry and the brief.

Collection produces versioned observations and instrument records. Analysis produces reproducible transformations and candidate claims. Review checks whether the evidence supports those claims. Publication exposes the relevant account and its limitations. The study then closes or names a specific follow-up question.

Exploratory work is welcome and labelled. If an unexpected pattern changes the study, record the protocol amendment before treating the new question as a confirmatory test. A failed collection or an inconclusive result can close a study successfully when it explains the limitation and the next useful measurement.

### Suggested starting capacity

Keep one close-observation study and one outward study active. Maintain a small methods queue. Admit another investigation when an existing one closes or a documented reason justifies the additional load. These are workload defaults, not claims about team size or funding. The daily budget in LH F06 is the throttle on agent work; the reader's time is the throttle on publication.

Each brief defines a bounded discovery allowance and a full execution ceiling before incurring new paid usage. Record existing service consumption as well as new spend. Reaching a limit produces a status record and a decision about further work; it does not silently extend the investigation.

## Harbour and the observatory

Harbour can coordinate work, while Lighthouse maintains the scientific record. The connection is an explicit, inspectable interface, so that a task's completion cannot silently become a verified research finding.

At the time of writing, Harbour's documentation describes the following records [S12 in LH F02]. A dispatch item carries an identifier, an issue reference, the prompt, a task kind, a target (the kind of consumer expected to run it, such as a command-line agent or a web session), the requested model, harness and effort, a queue timestamp and the dispatcher. An agent claims the item and then posts feedback: progress messages, links, ticket markers, usage entries carrying model, harness and effort, and a terminal marker of done, failed, aborted or skipped. Calls through Harbour's workspace proxy are audit-logged. Dispatch items expire after twenty-four hours; feedback, status and audit records are retained for thirty days. Harbour's Observation view presents sessions assembled from these records. Verify these details against the running version before a study relies on them.

| Component | Responsibility | Durable record |
| --- | --- | --- |
| Harbour coordination | Assign and track bounded work | Dispatch items and feedback entries, time-limited, copied by Lighthouse at collection |
| Collection | Capture permitted readings | Observations and sensor versions |
| Analysis | Transform and compare evidence | Methods, runs and claim records |
| Review and publication | Assess and communicate findings | Release and correction records |

## The integration contract

A Lighthouse research task dispatched through Harbour carries a study identifier, the question, evidence references, scope, resource ceiling, stopping condition and expected artefact. The initial proposal is to use Harbour's research task kind and to place the study identifier and a link to the brief at the head of the prompt, so that both appear in Harbour's own records without any change to Harbour.

A completed task returns output locations, method version, run status, consumption, unresolved issues and candidate claims. Harbour's feedback entries can carry the first four: a link and label for each artefact, the method version in the message, the terminal marker for run status, and usage entries for consumption. Unresolved issues and candidate claims belong in the study record, because Harbour's record is operational, agent-reported and time-limited.

Lighthouse stores the dispatch identifier in the study record and copies the dispatch and feedback records it needs into the protected store before they expire. The copy is an observation with its own collection time. Retain one canonical study record and references to the operational records. Document identifiers that cannot be joined reliably rather than manufacturing continuity.

When Harbour is also the subject, record the overlap. Check collection against another observation point where possible. Sensor failures and missing operational records may share a cause, so agreement between them is not sufficient on its own.

The first workspace's north star, budget and seed tickets are in LH F06.

## Outward sources

Public sources are instruments too. Each one a study uses is registered with the instrument record in LH F05: its population, coverage boundary, unit, cadence, licence and access conditions, and its version at the date of use. A source's terms can forbid some uses and its coverage can change without notice, so a study cites the register entry and the export it made, not the live site. LH003 in LH F04 builds the first such register.

## Initial technical shape

Use a versioned document and method repository, a protected store for observations, reproducible analysis jobs and a static publication surface. An index can connect studies, instruments, claims and releases. These are logical components; existing tools can supply them.

Begin with the smallest collector and analysis that answer the first question. Adopt existing telemetry conventions where they fit [S6 in LH F02]. A custom event service, a graph database or a continuously running research agent should follow an observed need.

Every view shows the observation period, units, scope, sampling, freshness, missingness and method version. Views of activity, flow and structure share identifiers and time controls where practical. Colour represents a declared quantity; visual prominence never silently means importance or risk.

Tag Lighthouse collection and research traffic. Measure or estimate its overhead with the method stated. Keep a clean distinction between observed events and simulated examples in both storage and display.

## Publication practice

Lighthouse publishes at several levels of depth. The same evidence may support several forms, each with its own purpose. A short explanation retains the qualifications that materially affect its meaning.

| Output | Reader need | Evidence expectation |
| --- | --- | --- |
| Notebook and blog | Follow work as it develops | Dated observations and open questions |
| Study | Inspect one investigation | Protocol, method, results, limitations |
| Report | Understand several findings | Traceable synthesis and implications |
| Article and essay | Explore an interpretation | Sources and clear separation of conjecture |
| Dataset or instrument | Reproduce and extend work | Version, scope, documentation, conditions |

Harbour's papers follow a written standard [S13 in LH F02]: a header naming title, kind, version, date, authors, model, grounding date and citations, then Answer, Findings, Method, Limits and Next, with verifiable citations and numbers only where they affect a conclusion. Lighthouse studies adopt that order and header so that a reader of one programme can read the other, and add what the standard does not require: the observation period, instrument versions, the labels distinguishing observation, derived measurement, interpretation and scenario, and a correction record. Essays follow the standard's essay form. The study skeleton in LH F05 carries this structure.

### Two kinds of writing

Records are for checking and pieces are for reading, and AGENTS.md gives each its rules. A record keeps its forms, its labels and its citations, because a reviewer will inspect it. A piece has one duty first, to be a good read, because most readers meet it alone and will not open the record beneath it; friction is a failure at the communication layer even when every claim is right. The qualifications that change a claim's meaning stay beside the claim; routine provenance moves to the notes and the colophon.

Pieces are cut down a ladder: a record supports an essay or a report, which supports an article, which supports a short form. Each rung is derived from the one above and points down to it in its colophon, so a reader can descend as far as they wish. A long essay drawn from several studies is a normal rung, and the short form is cut from it later, not written first.

### Images and plain names

Three families of image run through Lighthouse's writing, and each has a job. Biological images, the coral, the veins, the ripple of light and its afterglow, describe what we observe, because it grows, circulates and accumulates. Astronomical images, the observatory, the nearest star, the standard candle, the luminous fraction and the dark, the reference image, describe how we observe, because we look from far away by partial light. Nautical images, the harbour, the pilot, the keeper, the lighthouse itself, describe what people do with the result. The hazard analogies are not a fourth family: Kessler's debris is astronomical and the epidemic is biological, and propagation looks the same through either. The name Lighthouse stands where the astronomical and the nautical meet: a light for navigators.

The practice is a habit, not a register. An image arrives with its literal meaning beside it the first time it appears in a document, then walks alone. Studies use the plain names: activity, residue, propagation, observation, instrument. Essays and the charter may extend the images. An image that cannot be given a literal meaning beside it is a sign that the idea is not yet clear.

## The release check

The editor checks that material factual claims have support, primary sources have been read where relevant, charts use stated denominators, and uncertainties remain attached to the claims they qualify. Model-generated source summaries need verification against the source.

A piece is released only with a review record (R-nnnn) that names what was checked, what was found and what was changed, and finds nothing that must be fixed.

The reviewer reproduces the important calculation or explains why reproduction was not possible. Where an agent run produced the numbers, the run, its inputs and its queries are retained so the reviewer can repeat it. Review includes at least one plausible competing explanation. A second agent's agreement is a review contribution, not independent empirical confirmation.

The release note names the reviews the piece passed, the versions of the evidence and method, the publication date, the evidence cutoff and any restrictions on access to supporting material. Drafting a piece does not itself release it; the review does.

## Corrections and retirement

Keep a stable identity for each publication. Corrected editions state what changed, why, and whether conclusions changed. Preserve earlier editions where appropriate. A withdrawn claim remains traceable with its withdrawal reason.

Time-sensitive assessments state a review trigger or expiry. A superseded map is marked with its observation period rather than silently presented as current. An instrument can be retired when its source disappears or its assumptions no longer hold.

The first public surface makes it easy to find the remit, current investigations, publications, methods and corrections. A modest searchable archive is sufficient for the initial programme.

## Responsibility and research boundaries

Prefer metadata and aggregate readings when they answer the question. Record access scope, retention and sharing conditions before collection. Separate private evidence from public releases. Avoid collecting credentials or raw customer content as incidental telemetry. Harbour's own charter commits it to store customer content only for operational need; Lighthouse does not become a route around that commitment.

Observe public sources and participating systems within their permitted access. Changes to an observed system belong to a separately scoped experiment. Studies of harmful propagation begin with literature, historical evidence or contained simulations; operational deployment of a worm is not part of this founding programme.

Lighthouse's relationship with Harbour is disclosed in studies where it matters. Commercial or organisational interests, provider visibility limits and the selection of convenient subjects are recorded as potential sources of bias.

## Changes to the practice

The charter holds the stable purpose and commitments. Instrument specifications, research methods and operating defaults evolve through versioned decisions. A methods change that affects historical comparisons creates a new version and an explanation of comparability.

Use the decision record in LH F05: question, options considered, choice, reason, owner, date and condition for revisiting. Separate settled founding scope from provisional implementation choices. Do not let an early tool choice become a scientific assumption.

## Reviewing progress

At the end of the initial programme, review the clarity gained, instruments calibrated, claims reproduced or corrected, evidence gaps made visible, and the cost of maintaining the work. Ask whether a reader or an operator made a better-informed decision because of the findings. Ask also whether the watch would now detect the kind of event it is kept for, or can say honestly that it could not.

Useful progress can include showing that a proposed metric fails, or that an attractive metaphor does not predict the observations.

## Responsibility before launch

Record the actual budget and access boundaries for the first studies. These are operational records to complete when execution begins.

Use the templates in LH F05 to open the first studies, register the instruments and preserve the initial decisions. Revise this handbook after the first completed studies reveal which parts of the process are necessary.
