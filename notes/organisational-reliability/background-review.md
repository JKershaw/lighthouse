# When production outruns understanding

## AI, organisational change and the reliability of shared infrastructure

**Commissioning background, retained 13 November 2026.** This is the discussion paper supplied before John authorised the pilot. Its descriptions of what had not yet been started and the then-current limits describe that earlier moment; see [commissioning](commissioning.md) for subsequent decisions. It is not a released Lighthouse review.

Prepared for John Kershaw, 13 November 2026. Exploratory literature review and assessment of fit with Lighthouse. This is a discussion paper, not a commissioned Lighthouse investigation or a released Lighthouse finding.

**In short.** This question fits Lighthouse's existing remit and has a substantial research foundation. Automation can change the work left to people, the knowledge they acquire, and the organisational controls needed to maintain reliable systems. Recent software studies also document genuine benefits, no detectable harm in some settings, and promising ways to relieve review bottlenecks. The useful question is when AI-enabled production and organisational change strengthen or exceed a team's ability to understand, verify and recover its systems. Nothing reviewed here establishes that changes in Microsoft's staff profile caused the current outage.

## 1. The question worth bringing back

The Microsoft outage prompted a broader hypothesis than an agent acting outside its instructions:

> An organisation adopts AI, increases expected output and changes its staffing or work allocation. The capacity to produce changes grows faster than the capacity to understand their consequences. Loss of relevant experience, weaker knowledge transfer or overloaded review makes failures more likely or recovery more difficult.

This is a proposed mechanism, not an observed chain at Microsoft. Its reverse is also plausible: AI could improve diagnosis, transfer knowledge, identify risky changes and make a smaller team more reliable. The research must admit both outcomes.

Three different time horizons matter. During delivery, generation can create additional review and integration work. During organisational change, departures or reassignment can remove knowledge before replacements acquire it. Over longer periods, automation can change how the next cohort develops judgement. A short coding experiment cannot establish the third effect, and an outage postmortem may reveal little about any of them.

The question should therefore be:

> **Under what conditions does AI adoption change an organisation's capacity to understand, maintain and recover the systems it operates?**

For Lighthouse, narrow the outcome to shared software and infrastructure. Otherwise this becomes an unbounded programme about AI and employment.

## 2. What Lighthouse already provides

I read the current repository on main at [2a425068454922969c94d9e6c5f03100a707ff00](https://github.com/JKershaw/lighthouse/commit/2a425068454922969c94d9e6c5f03100a707ff00), committed 12 November 2026. The file SHAs of the core documents and records listed below matched that snapshot. This is documentary inspection, not an audit or reproduction of their datasets.

### The remit already includes the question

The [charter](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/charter.md) explicitly includes information moving through humans and AI, institutions, structural change, maintenance and recovery. It does not require a complete separation of human and AI activity before measurement. Its recent physical-authority extension also recognises harm arising when systems carry out institutional instructions.

The [research design](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/design.md) already treats people, organisations, services and workflows as entities; authority and dependence as typed relationships; and rework, incidents and interventions as outcomes. It explicitly assesses health against functions and outcomes, including quiet reserves and maintenance, rather than maximum throughput.

My interpretation: no charter rewrite is needed to explore the organisational reliability question. Starting a continuing investigation would still be a programme decision.

### The closest existing home

| Existing work | Connection to this question | Boundary to preserve |
| --- | --- | --- |
| [What AI activity costs the shared internet](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/investigations/ai-cost-and-spread.md) | The strongest home for a bounded feasibility study of organisationally mediated costs, operational load and recovery | Its current strands distinguish load, exposure, human-run spread, lab capability and activity in public. Organisational degradation would be an additional proposed mechanism, not evidence of autonomous propagation |
| [Where software updates go](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/investigations/software-updates.md) | Existing methods follow changes through releases, pins, recipes and workflows | The presence or movement of code does not show who understood it or what ran in production |
| [When a model finds the bug](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/investigations/model-found-bugs.md) | Shows how to separate technical capability from the institutional response that turns it into protection | Finding a flaw and operating a reliable service are different outcomes |
| [When AI acquires physical authority](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/investigations/physical-authority.md) | Shares the principle that institutional choices and ordinary authorised behaviour can contribute to harm | Its six-week pilot and civilian-consequences question should retain their own scope and resources |

The [proposal rules](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/proposals.md) record four active investigations out of a temporary limit of four. The usual limit is three; the fourth lasts through the robotics pilot to 24 December 2026. No fifth is authorised. A small source-feasibility study could potentially deepen the costs investigation, but a continuing organisational research programme should be treated as a direction decision, not fitted into an existing label to evade capacity limits.

### Local evidence is relevant, with a narrower meaning

[LH016](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/studies/LH016/LH016.md) follows Lighthouse's own research and review rounds. It records different checks catching different problems and corrections introducing new claims that needed checking. This is useful evidence about this workflow's dependence on supervision and review design. It does not measure the effect of losing senior employees, and its replays and agent reviews do not provide independent population validation.

[LH047](https://github.com/JKershaw/lighthouse/blob/2a425068454922969c94d9e6c5f03100a707ff00/studies/LH047/LH047.md) audits one evening's requests against stated rules. Its account locates many failures in collection practices and missing shared enforcement. This makes a useful process case: instructions, harnesses and controls matter together. These were rule breaches, not demonstrated incidents of harm, and this record does not connect them to staffing changes.

Harbour's [Learning While the Tools Change](https://harbour.cat/library/learning-while-the-tools-change) supplies a useful synthesis of engineering experience, AI experience and changing tool capabilities. It warns that visible speed can conceal deferred understanding or work borne elsewhere. It is a synthesis and local conceptual framework, not a causal study of large firms' staffing decisions.

This tightens our earlier discussion: Harbour and Lighthouse motivate the hypothesis and offer possible calibration subjects. They have not established the proposed staffing-to-outage relationship.

## 3. What the literature says

This is a targeted scoping review across human factors, systems safety, empirical software engineering, learning and AI productivity, searched on 13 November 2026. It is not a systematic review or a meta-analysis. The linked annotated register in section 8 contains 26 research entries, with their methods and limits. The most consequential distinctions are these.

### Automation can leave a harder job to the people who remain

Bainbridge's *Ironies of Automation* [1] describes the difficulty of expecting people to supervise automated operation and intervene in unusual conditions while removing opportunities to practise the necessary skills. Endsley and Kiris [2] experimentally connect reduced situation awareness with impaired takeover after automation failure. Parasuraman and Manzey [3] review the interacting roles of attention, people, context and automation.

For software operations, these are mechanisms and analogies worth testing. They are not measurements of modern coding agents. They suggest examining whether on-call engineers retain a useful picture of the running system, not merely whether a human approval button exists.

### Organisational structure and knowledge have measurable relationships with defects

Naur [6] offers the conceptual argument that a program's maintainability depends on the understanding held by its developers, beyond its written artefacts. Empirical work supplies narrower tests: Nagappan and colleagues [7] find organisational metrics predictive of failure-proneness in Windows Vista; Bird and colleagues [8] relate component ownership and contribution-based expertise to faults; Mockus [9] reports associations between organisational change, recent departures and customer-reported defects.

These studies support examining knowledge continuity. They do not establish that all turnover is harmful, or that job title, age or company tenure measures the knowledge that a particular service needs. Strong ownership may improve understanding while excessive concentration makes departures dangerous. Both distribution and depth matter.

### Review capacity matters, but simple review metrics can mislead

McIntosh and colleagues [10] report relationships between review coverage, participation and post-release defects. Krutauz and colleagues' replication [11] finds those relationships sensitive to model and variable selection, with prior defects, size and authorship more consistently explanatory.

That matters for Lighthouse's instrumentation. Comment counts, approval counts and elapsed review time cannot be treated as direct measures of scrutiny. A difficult change can attract more review and still cause more incidents. That does not mean review caused the incidents.

Recent evidence reaches the proposed production-pressure mechanism more directly. Meta's RADAR paper [22] reports growing code supply and declining timely review, then describes risk-based layered automation intended to relieve that bottleneck. It is an important operator report of both the pressure and a response, not a general finding that smaller teams or automated review are safe everywhere.

### Task gains, knowledge gains and service reliability are different outcomes

Cui and colleagues [12] find substantial gains in completed development tasks, with larger gains among less-experienced developers. Brynjolfsson, Li and Raymond [13] find productivity and learning benefits in customer support. These are real reasons to consider AI a means of spreading expertise.

Shen and Tamkin [16], in a short randomised library-learning experiment, find lower immediate mastery with AI assistance. This does not demonstrate inevitable long-term deskilling. Lee and colleagues [17] find reported changes in critical-thinking effort and practices; self-report is not a longitudinal competence test.

Taken together, these studies support separating assisted task performance, retained understanding, transfer to new problems and operational outcomes. Treating one as a substitute for the others would prejudge this investigation.

### Current findings do not support inevitable degradation

Borg and colleagues' preregistered maintainability experiment [19] detects no systematic downstream disadvantage in its bounded tasks. Its work predates contemporary agentic coding.

The full text of Mockus and colleagues' Meta study [20] reports no increase in severe production incidents associated with the fraction of AI-generated code after contextual adjustment. Its observational, pre-agentic setting and partial provenance coverage limit transfer. Its abstract's simpler wording about lower incident rates should not replace the more qualified full-text interpretation. I found this distinction while checking the paper beyond its abstract.

Yang and colleagues' CRBugBench [21] documents improving review-agent performance alongside continuing difficulty with complex changes and project context. Abreu and colleagues [24] show a route by which language models can improve release-risk prediction. These are reasons to measure verification capacity including well-designed automation, rather than assume it must remain fixed while generation improves.

### Organisational choices belong inside the causal account

Rasmussen [4] describes how locally reasonable adaptations to commercial and workload pressures can collectively approach unsafe boundaries. Leveson [5] analyses safety through control structures, feedback and constraints rather than a single failed component. DORA [23] frames AI as amplifying organisational strengths and weaknesses.

The inference for Lighthouse is that tooling, staffing, incentives, system architecture and operational safeguards should be studied together. This neither removes organisational responsibility nor makes every failure at an AI-adopting firm an AI-caused failure.

Acemoglu, Kong and Ozdaglar [25] model a longer-run mechanism in which useful personalised AI assistance reduces incentives to generate shared knowledge. It sharpens the hypothesis, but is a theoretical working paper, not evidence that this process has occurred at Microsoft or across engineering organisations.

### The latent swarm is an adjacent mechanism

Holton [26] concerns correlated agents increasing diagnostic, retry or remediation activity during a shared failure. That acts over minutes and hours. Loss of knowledge or review capacity develops over different timescales. The two could interact, but a prolonged outage cannot establish either one. An incident record should distinguish the trigger, conditions that made it possible, mechanisms that sustained it, and consequences elsewhere.

## 4. A causal account that can be tested

The proposed chain has several separate links:

| Link | Evidence needed | Alternative that must remain possible |
| --- | --- | --- |
| AI adoption changes production | Comparable changes, task mix and tools before and after adoption, with provenance where available | Demand growth, a product launch or better measurement explains the increase |
| Adoption changes staffing or work allocation | A documented decision, its timing, affected team and rationale | Cuts would have happened anyway; reassignment adds relevant expertise |
| The change reduces effective understanding or review | Handover evidence, task-specific comprehension, review corrections, ownership and escalation records | Knowledge is transferred; documentation, training or AI improves capacity |
| Weaker capacity changes operations | Failed-change rates, recovery exercises, diagnosis or restoration outcomes | Architectural fragility, workload growth or a separate technical problem dominates |
| Effects reach other organisations | Dependency-specific disruption and operational records | Simultaneous symptoms arise from a common upstream fault, not cascading agent actions |

AI can be a contributor through the behaviour it enables or through expectations that influence decisions. Establishing the expectations route requires evidence that the decision relied on those expectations. A company mentioning AI in a layoff announcement is context, not sufficient attribution.

There is no need to identify one exclusive cause. There is a need to identify the mechanism and the evidence for each link. Conversely, excluding malicious activity says little about whether routine AI-assisted work or AI-related organisational choices contributed.

Evidence against the proposed harmful chain would include sustained or improved understanding and recovery under comparable workloads; review capacity keeping up as production grows; successful knowledge transfer after departures; or an incident explanation supported by detailed records that does not involve the proposed links. A successful bounded automation programme is a valuable comparison, not an inconvenient exception.

Avoid defining a numerical 'understanding gap' by dividing code volume by headcount. The units do not support it. Use several separate measures and test how they relate.

## 5. What is currently knowable about Microsoft

Microsoft's [6 July staffing announcement](https://blogs.microsoft.com/blog/2026/07/06/the-latest-in-our-company-transformation/) documents 4,800 eliminated roles, voluntary retirement uptake and organisational changes. It says the eliminated roles are not being replaced by AI while acknowledging task automation and changing work. It does not identify losses of critical knowledge in the service responsible for this outage.

The [2026 annual report](https://www.microsoft.com/investor/reports/ar26/) gives aggregate employee categories and describes AI investment. Those totals cannot establish the staffing, review or on-call capacity of an affected team.

The [official status feed](https://status.cloud.microsoft/api/feed/mac), read during the earlier discussion, carried a 07:29 GMT update on 13 November reporting improved stability after an authentication/routing component patch, no known malicious cause and a promised post-incident report. This is a timestamped part of the incident account, not a claim that it remains the latest update when this paper is read. Live notices overwrite themselves.

**Not established in the sources reviewed:** that the affected team lost senior engineers; that relevant knowledge left with them; that AI replaced that capacity; that AI authored or selected the triggering change; or that external agents sustained the failure. These are separate missing links, not findings of absence.

Microsoft is therefore a motivating case and possible future evidence source. It should not be the sole case selected to prove an explanation already proposed after seeing the outage.

GitHub's [August 17 account](https://github.blog/news-insights/company-news/the-august-17-outage-and-the-work-ahead/) supplies a documented comparison for the recovery strand: a client retry loop affecting Copilot services increased traffic during recovery. That is an operational mechanism in an AI product's software, not evidence of staffing loss or a decentralised agent swarm.

## 6. What Lighthouse could observe

The practical difficulty is access. Public sources are better at exposing outages and corporate announcements than the internal changes needed to connect them. Mapping that missing connection would itself be useful, provided a missing field never becomes an adverse score.

| Observation route | Useful evidence | What it cannot establish alone |
| --- | --- | --- |
| Public incident reports | Triggers, dependencies, recovery barriers, stated safeguards and corrections | Exhaustive causes or unreported staffing history |
| Public organisational statements | Announced changes, stated rationale and dates | Affected service expertise, actual replacement or realised gains |
| Repository and review history | Changes, ownership patterns, review events and declared AI use | Career seniority, all AI assistance, actual scrutiny or private production outcomes |
| A willing team's records | Tools, team changes, relevant experience, review and deployment outcomes | Population effects beyond that team |
| Harbour and Lighthouse | Detailed task and review traces, retained intent, corrections and local costs | The consequences of mass employee departures or large-cloud operations |
| A contained experiment | Comprehension, error detection, diagnosis and recovery under fixed conditions | Long-term institutional learning or global outage rates |

For every incident, keep AI involvement as a set of source-backed claims rather than one yes/no field. Useful categories are upstream dependency; development assistance; operational assistance or execution; organisational decision justified by AI; externally attributed agent load; and unknown. One event can have several roles.

Each claim needs a source, speaker, publication and collection dates, organisational boundary, asserted mechanism, supporting evidence and contrary evidence. A direct operator statement is still a report by that operator. An absence of mention is 'not disclosed', not 'no AI'.

Outcome measures should include incident burden per service-period as well as failures per comparable change: a lower failure rate can coexist with more incidents if volume rises. Keep severity, user impact, diagnosis time, recovery time, rework and near misses separate where records permit. Changing reporting practices can move any of them.

Relevant experience should mean knowledge of the affected system and its failure modes, alongside AI fluency. Distinguish departure, retirement, reassignment and transfer of responsibility. Do not infer a person's age, ability or employment status from public contribution patterns.

## 7. Options for discussion, not work already started

| Option | Deliverable | Value and limitation |
| --- | --- | --- |
| A. Context note or essay | A synthesis of this literature linked to Lighthouse's current observations | Explains why the issue matters; creates no new empirical result |
| B. Bounded public-evidence feasibility study | A small set of incident-source records showing which causal links public evidence can support | Tests whether an outward programme is practical before committing to it |
| C. Close-observation study | A consenting team's records or a contained task-and-recovery experiment | Can examine mechanisms closely; needs explicit access and has limited generalisability |
| D. Continuing organisational watch | A longitudinal programme across several collaborators and public sources | Potentially valuable, but requires a new capacity and direction decision |

**My recommendation for our discussion is B first, followed by C only if a measurable question emerges.** The first useful result may be a map of what public postmortems leave invisible. Avoid starting D merely because this is an important subject.

A possible feasibility question is: *Can public incident and organisational records distinguish direct AI involvement from changes in knowledge, review and recovery capacity?*

A concrete candidate design, to be agreed and fixed before collection:

- One existing investigation as the proposed home, one accountable owner, one manual pass and a small fixed case ceiling, for example eight cases. This is a suggested scope, not an authorised protocol.
- Define a frame from named providers' published incident reports within a fixed historical window, such as 1 January 2025 to 31 October 2026. Select within that frame before reading detailed outcomes. Do not choose only incidents with an AI headline.
- Record that the Microsoft outage, GitHub retry case and Meta papers are already known. They can be disclosed motivating examples outside the primary sample. Microsoft is already hypothesis-generating material, not an untouched validation case.
- Make the unit an incident-source record. Record affected function, AI role, technical trigger, sustaining effects, organisational evidence, source agreement and missing links. Preserve the denominator and inaccessible reports.
- Code whether a source supplies evidence about staffing or expertise, not whether the company probably suffered knowledge loss. Keep negative, unknown, unavailable and not applicable separate.
- Produce an evidence table and a short feasibility judgement, with a fixed time and cost ceiling agreed at commissioning. No recurring schedule is needed for this first question.
- Stop when the ceiling or case count is reached. If the records do not connect internal change to operations, report that limit and decide whether a collaborator is worth seeking. Do not quietly substitute company-wide layoffs as the exposure measure.

A later contained study could vary retained context and review budgets independently of AI assistance, then test diagnosis and recovery on held-out faults. That could test dependence on context and supervision without pretending an artificial task reproduces losing a long-serving colleague. Model, harness and tooling versions would be part of the treatment. Measuring task completion alone would miss the question.

Nothing in this paper has been added to Lighthouse's proposals, studies, schedule or publication surfaces. This paper is prepared for discussion; it has not received Lighthouse's independent review and release process.

## 8. Annotated research register

All entries were consulted on 13 November 2026. 'Abstract' below includes a primary publisher or author record retrieved by search; it does not mean the full paper or data was checked. 'Sections' means relevant full-text sections were inspected, not that every result was reproduced. No study's data was independently reanalysed for this review. Vendor research is useful evidence with interests and access advantages to disclose; multiple papers from the same organisations, authors or possibly overlapping systems are not independent replications.

### Human factors, safety and retained understanding

**[1] Bainbridge (1983), [Ironies of Automation](https://tc.ifac-control.org/4/1/newsletter/ironies-of-automation/@@download/file/Bainbridge1983_Automatica_Ironies%20of%20automation.pdf).** Peer-reviewed conceptual analysis drawing on process control and aviation; full-text sections inspected. Automation can leave people responsible for difficult exceptions while reducing practice and support. Supplies a mechanism for studying supervision and recovery. It predates LLMs and does not estimate effects in software teams.

**[2] Endsley and Kiris (1995), [The Out-of-the-Loop Performance Problem and Level of Control in Automation](https://doi.org/10.1518/001872095779064555).** Navigation-task experiment; publisher abstract inspected. Reduced situation awareness accompanied slower decisions after expert-system failure, with operator involvement affecting the result. Supports measuring takeover readiness; transfer to distributed software operations requires testing.

**[3] Parasuraman and Manzey (2010), [Complacency and Bias in Human Use of Automation](https://doi.org/10.1177/0018720810376055).** Review and attentional framework; primary abstract consulted. Automation bias and insufficient monitoring depend on interacting personal, situational and system characteristics. The lesson is to inspect the whole workflow, rather than assume either expertise or an instruction to check makes supervision effective. No universal LLM effect size follows.

**[4] Rasmussen (1997), [Risk Management in a Dynamic Society: A Modelling Problem](https://backend.orbit.dtu.dk/ws/portalfiles/portal/158016663/SAFESCI.PDF).** Systems-safety analysis; full-text sections inspected. Commercial pressures and adaptations across organisational levels can collectively erode safety margins. Provides a way to investigate organisational conditions without reducing failure to one operator or component. It is a framework, not a staffing-cut experiment.

**[5] Leveson (2004), [A New Accident Model for Engineering Safer Systems](https://ocw.mit.edu/courses/16-355j-software-engineering-concepts-fall-2005/94aad3a6f1888aeb4195cdd3f41f885b_safescien_single.pdf).** Systems-theoretic safety model; full-text sections inspected. Constraints, feedback and organisational control explain interactions that component-failure chains can miss. Useful for classifying authority and missing feedback. Applying the model does not by itself demonstrate a cause.

**[6] Naur (1985), [Programming as Theory Building](https://doi.org/10.1016/0165-6074(85)90032-8).** Conceptual argument; publisher abstract consulted, full text not inspected here. Program modification depends on the understanding maintained by programmers, not just preserved text. Helps specify what a handover or documentation system must preserve. It is not a measurement showing that AI cannot support or acquire relevant understanding.

### Organisation, ownership and review

**[7] Nagappan, Murphy and Basili (2008), [The Influence of Organizational Structure on Software Quality](https://www.microsoft.com/en-us/research/publication/the-influence-of-organizational-structure-on-software-quality-an-empirical-case-study/).** Windows Vista case study; primary abstract and report opening inspected. Organisational-complexity metrics predicted failure-prone binaries and outperformed several conventional predictors in that setting. Prediction and association do not establish the effect of a particular reorganisation, and this is one historical environment.

**[8] Bird et al. (2011), [Don't Touch My Code!](https://www.microsoft.com/en-us/research/publication/dont-touch-my-code-examining-the-effects-of-ownership-on-software-quality/).** Windows Vista and Windows 7 observational analysis; primary abstract consulted. Ownership and contribution-based expertise relate to pre-release faults and post-release failures. Component familiarity is the relevant construct; a low-contribution developer is not necessarily a junior engineer. Observational associations should not become a blanket prohibition on newcomers.

**[9] Mockus (2010), [Organizational Volatility and Its Effects on Software Defects](https://doi.org/10.1145/1882291.1882311), [author presentation](https://mockus.org/papers/orgQuality-slides.pdf).** Industrial archival study; presentation and its included abstract inspected, not the full journal/conference manuscript. Proximity to organisational changes and recent departures were associated with customer-reported defects. Supplies a directly relevant pre-AI precedent. It does not isolate AI substitution or show that all turnover has the same effect.

**[10] McIntosh et al. (2014), [The Impact of Code Review Coverage and Code Review Participation on Software Quality](https://rebels.cs.uwaterloo.ca/confpaper/2014/05/30/the-impact-of-code-review-coverage-and-code-review-participation-on-software-quality.html).** Qt, VTK and ITK case studies; author abstract and paper opening consulted. Review coverage and participation relate to post-release defects. Useful candidate measures, but their causal meaning and independence from change difficulty need examination. Read with [11].

**[11] Krutauz et al. (2020), [Do Code Review Measures Explain the Incidence of Post-Release Defects?](https://link.springer.com/article/10.1007/s10664-020-09837-4).** Replication on Qt and Chrome with regression and Bayesian networks; publisher abstract inspected. Review-predictor effects were unstable under variable selection; prior defects, size and authorship were more robust. Prevents treating simple review counts as a validated causal instrument. It does not show that code review has no value.

### Productivity, learning and calibration

**[12] Cui et al. (2025 research summary), [The Effects of Generative AI on High-Skilled Work](https://www.microsoft.com/en-us/research/publication/the-effects-of-generative-ai-on-high-skilled-work-evidence-from-three-field-experiments-with-software-developers/).** Three randomised field experiments, 4,867 developers; primary summary and abstract consulted. Pooled completed tasks rose 26.08%, with noisy individual experiments and larger gains among less-experienced developers. This concerns coding assistance, not an estimate of how much organisational expertise or on-call staffing can safely be removed.

**[13] Brynjolfsson, Li and Raymond (2025), [Generative AI at Work](https://academic.oup.com/qje/article/140/2/889/7990658).** Staggered deployment to 5,172 customer-support agents; abstract and relevant results consulted. Issues resolved per hour rose about 15%; novice benefits and evidence of learning suggest expertise can be spread rather than simply lost. Customer support and its quality measures do not establish reliability effects in software infrastructure.

**[14] Becker et al./METR (2025), [Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/).** Randomised real repository work by 16 experienced developers; primary report consulted. AI-allowed tasks took 19% longer in this sample, despite expectations of gains. Shows that perceived and measured effects can diverge. The tools, cohort and tasks are specific, and this is not a permanent estimate for later models.

**[15] METR (2026), [We Are Changing Our Developer Productivity Experiment Design](https://metr.org/blog/2026-02-24-uplift-update/).** Follow-up methodological report; text inspected. Developer and task selection, changed pay and concurrent-agent time measurement made the updated estimate unreliable. Do not cite [14] as current universal evidence or treat the follow-up as a clean reversal. Willingness to work without AI can itself select the observed population.

**[16] Shen and Tamkin (2026), [How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245), [primary study account](https://www.anthropic.com/research/AI-assistance-coding-skills).** Randomised unfamiliar-library task with 52 recruited developers; detailed primary account inspected. Average immediate quiz scores were 50% with AI and 67% without: a 17 percentage-point gap, not a 17% relative reduction. The time difference was not significant. Interaction patterns were observational within treatment. Short-term learning does not settle long-term deskilling.

**[17] Lee et al. (2025), [The Impact of Generative AI on Critical Thinking](https://www.microsoft.com/en-us/research/publication/the-impact-of-generative-ai-on-critical-thinking-self-reported-reductions-in-cognitive-effort-and-confidence-effects-from-a-survey-of-knowledge-workers/).** Survey of 319 workers and 936 examples; primary abstract consulted. Confidence in AI was associated with reported reductions in critical-thinking effort, with work shifting toward verification and integration. This identifies reported practices, not measured loss of competence or a causal effect of layoffs.

**[18] Perry et al. (2022 preprint), [Do Users Write More Insecure Code with AI Assistants?](https://arxiv.org/abs/2211.03622).** Controlled security-programming user study; author abstract consulted. Participants using the tested assistant produced less secure code and were more confident in its security. Relevant to calibration, but based on an older model and specific tasks. It is not a present-day vulnerability rate for AI-authored software.

### Recent software quality, review and operational evidence

**[19] Borg et al. (2026), [Echoes of AI](https://link.springer.com/article/10.1007/s10664-026-10889-1).** Preregistered two-phase study with 151 participants, mostly professionals; methods, results, limits and interests inspected. The randomised second phase found no significant downstream maintainability difference. First-phase speed findings are observational. Work was done in late 2024, before current coding agents. Authors disclose CodeScene and consulting interests. A bounded null result is neither proof of equivalence nor evidence of inevitable harm.

**[20] Mockus et al. (2026), [A Preliminary Analysis of the Impact of AI Assisted/Generated Code on Quality, Centrality and Review Time at Scale](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESEM.2026.93).** Over 10,000 Meta developers and 400,000 diffs; full-text methods, results and limits inspected. After adjustment, AI-code fraction was not associated with more severe incidents. Code context, provenance coverage and selective use matter. It studies pre-agentic assistance over a short window inside Meta; aggregate outcomes cannot isolate departures or review-budget changes. The main text qualifies the abstract's summary.

**[21] Yang et al. (October 2026 preprint), [(When) Should a Software Factory Be Lights-off?](https://arxiv.org/abs/2610.13668).** CRBugBench: 1,000 open-source review tasks and 800 proprietary tasks; author abstract and Microsoft research account inspected. Review agents improved but remained weaker on complex and context-dependent bugs. The reported best 71.9% top-five detection result is a benchmark result, not a production escape rate or proof of human equivalence. Useful for testing what automated review can replace.

**[22] Adams et al. (2026 preprint), [Automating Low-Risk Code Review at Meta: RADAR, Risk Calibration, and Review Efficiency](https://arxiv.org/abs/2605.30208).** Large deployment report using telemetry, policy comparisons and difference-in-differences; author abstract inspected. Reports code growth, declining timely review, and a layered risk-screened automation response. This directly bears on the supply-versus-review mechanism. Low-risk eligibility means reported comparisons with other changes do not establish that indiscriminate automation would improve safety.

**[23] DORA (2025), [State of AI-assisted Software Development](https://dora.dev/research/2025/dora-report/), [small-batch guidance](https://dora.dev/capabilities/working-in-small-batches/).** Industry research programme; official summaries and relevant capability guidance consulted, not the entire report reanalysed. Organisational capabilities condition outcomes; AI can amplify existing strengths and weaknesses. Survey associations and guidance support hypotheses and measures, not attribution of a particular outage. DORA is run by Google Cloud with industry partners.

**[24] Abreu et al. (2025), [Moving Faster and Reducing Risk: Using LLMs in Release Deployment](https://mockus.org/papers/Moving_Faster_and_Reducing_Risk_Using_LLMs_in_Release_Deployment.pdf).** Meta release-risk modelling; paper design and reported results inspected. Risk-aligned models improve identification of historically incident-causing changes at specified gating levels. Supplies a concrete alternative pathway: AI can strengthen controls. Retrospective predictive performance and one production environment do not demonstrate the safety of reducing the staff who interpret and act on those predictions.

### Long-run and network hypotheses

**[25] Acemoglu, Kong and Ozdaglar (2026 working paper, May revision), [AI, Human Cognition and Knowledge Collapse](https://shapingwork.mit.edu/research/ai-human-cognition-and-knowledge-collapse/).** Dynamic economic model; institutional account and revised paper opening inspected. Under stated assumptions, personalised assistance reduces learning effort and the shared knowledge stock despite current decision gains. A source of testable mechanisms, not an empirical forecast or measured industry trend. Distinguish this from the similarly titled literature on training-data model collapse.

**[26] Holton (October 2026 working paper), [The Latent Swarm](https://zenodo.org/records/23272003).** Hypothesis and proposed measurements; paper sections inspected during the preceding discussion. Independent agents may react similarly to shared failures and move shed load elsewhere. Active population, convergence and displacement are unmeasured, and no decentralised production event is established. Useful alongside the organisational question, with a separate causal and temporal account.

## 9. Search and interpretation limits

Searches combined terms for automation, takeover, organisational structure and volatility, ownership, developer turnover, review coverage, skill formation, cognitive effort, maintainability, severe incidents and agent review. Citation-following from the Meta paper led to older organisational work and to RADAR and release-risk modelling. Searches deliberately included productivity benefits, null findings, replications and risk-reduction uses.

Coverage favours accessible English-language work, public author pages and industrial software research. Some older publisher pages were inaccessible; the register identifies where only abstracts or author presentations were read. Candidate papers without a sufficiently checked primary account were not used to support conclusions. No comprehensive database export, duplicate-screening record or formal publication-bias assessment was made. This should not be labelled a completed systematic literature review.

Publication year and the tool's observation year must stay separate. Some of the most recent papers report 2024 or 2025 work. Completion assistance, interactive chat and agentic execution are different exposures. Customer support, controlled programming tasks, repository changes and production incidents are different outcomes. Their effect sizes should not be pooled.

The review supports a conditional organisational mechanism and a research opportunity. It does not establish a general rise in AI-caused outages, the adequacy of any company's current staff, or the cause of Microsoft's incident. The next decision is whether the public-evidence feasibility question is worth one bounded place in Lighthouse's existing work.

---

Prepared by ChatGPT/Codex for discussion with John. Sources and current repository documents inspected as stated; no independent reproduction or external review. Lighthouse repository, issues, schedules and live site unchanged.
