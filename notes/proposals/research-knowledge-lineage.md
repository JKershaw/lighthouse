# How knowledge becomes progress: research lineage for Lighthouse

**In short.** Lighthouse could trace how research in AI and computer security develops, how its own findings arise and change, and when one investigation uses knowledge from another. The useful asset would be a small, verifiable record of claims and their lineage, not a giant citation chart. This proposal asks for a bounded retrospective pilot before any standing collection, new investigation or public feature is promised.

Status: proposal for the keeper and the horizon gate, not an agreed study or finding.
Origin: keeper's conversation with GPT-6 on 10 November 2026, prompted by scientometrics and the lineage of useful scientific discoveries.
Scope: research method and presentation across existing investigations. It does not take a fourth active-investigation slot.
Evidence status: design hypotheses and candidate sources, not measurements by Lighthouse.

## The idea in full

There are three connected strands.

1. **Observe the world's research.** Follow relevant papers, evaluations, security advisories, incidents, methods, standards, code, and real-world responses across AI security, agent workflows, software supply chains and the internet's shared infrastructure. Ask where ideas originate, converge, contradict each other or reach practical use. Include research assisted by AI, but only label the assistance when a source discloses it or other evidence supports it.
2. **Observe Lighthouse's own research.** Show a path from a question through a protocol, source reads, observations, individual claims, reviews, corrections and publications. Preserve the evidence and status of each link. Readers should be able to trace a sentence back to its basis and see how the conclusion changed.
3. **Join the two for reuse.** When Lighthouse starts another investigation, find earlier claims, methods, contradictory evidence, failed approaches and relevant outside literature before proposing more work. Record what was reused and what new evidence the investigation added. This is a form of observatory self-measurement, not just a reading list.

The visual map is a view of the record, not the record itself. The central question is whether a growing, inspectable representation helps Lighthouse do better research rather than simply produce more material.

## Why it belongs here

Lighthouse already has an environmental map: [the design](../../design.md) describes activity, residue and propagation across partially visible networks, and [LH035](../../studies/LH035/LH035.md) describes the coverage and limits of instruments that observe the internet. Research lineage is **a different map**: it represents intellectual and evidential relationships, including what Lighthouse itself knows and how. It should not be confused with a dependency, traffic or incident-propagation map. A citation is not a causal transmission.

The [research scout](../horizon/plan.md) already watches security and AI literature twice weekly. This proposal enriches its output rather than commissioning an unbounded new scout. The existing [proposals process](../../proposals.md) and three-investigation throttle should decide what research actually starts.

The strongest first internal case is [It was only a test](../../essays/it-was-only-a-test.md) and [its evidence directory](../it-was-only-a-test/README.md): a claims table, independent agent-context readings, source verification, a session record, reviews and a subsequent correction. The 83 reviewed claim rows offer an unusually explicit seed for tracing provenance, agreement and correction without inventing a new record format. A distinct second test is [When a model finds the bug](../../investigations/model-found-bugs.md), where the question of an AI-assisted discovery is already carefully separated from advisory, disclosure, scoring, patch and real-world effect. The instrument survey offers a third candidate for later reuse testing, not a commitment to ingest all 48 instruments.

## Existing scholarship and tools to build on

A bounded literature check on 10 November 2026 found these primary starting points. They are leads for a pilot protocol, not evidence that Lighthouse's proposed method works.

- Lancaster University, commissioned by the UK Department for Science, Innovation and Technology, *Thematic review and gap analysis on AI security*, published 10 July 2026, read 10 November 2026: 9,109 publications classified across 12 themes. Relevant gaps include agent/tool interaction security, assurance and provenance. https://www.gov.uk/government/publications/thematic-review-and-gap-analysis-on-ai-security/thematic-review-and-gap-analysis-on-ai-security
- Shamshiri and colleagues, *A domain-specific knowledge graph for reasoning over AI security threats and defenses*, Knowledge-Based Systems, published 27 September 2026, read 10 November 2026: a graph built from 780 papers, with typed claims, sentence-level provenance and competing mitigation/bypass claims kept distinct. A useful methodological comparator, not an independent validation of the paper's reported performance. https://doi.org/10.1016/j.knosys.2026.116492
- OpenAlex API recipes, read 10 November 2026: references, incoming citations and related works; potential index for outward bibliography, with coverage and rate limitations to measure. https://help.openalex.org/how-to/api-recipes/
- Semantic Scholar Academic Graph API, read 10 November 2026: citation contexts and inferred intentions, useful as candidate relationships needing checking. https://api.semanticscholar.org/api-docs/
- OpenCitations Index API, read 10 November 2026: open bibliographic citation edges as another possible check. https://api.opencitations.net/index/v2
- W3C PROV-O and the nanopublication approach: established vocabulary for entities, activities, provenance and claims. Borrow a small compatible subset where it helps; do not begin with a mandatory RDF infrastructure. https://www.w3.org/TR/prov-o/ and https://nanopub.net/

Possible methods include direct citations, bibliographic coupling, co-citation, main-path analysis, citation bursts and unusual combinations across disciplines. Those are tools for generating questions. A central paper is not necessarily correct, a frequently cited paper is not necessarily useful, and later uptake does not prove the earlier paper caused it.

## A minimal evidence model

Keep the repository's existing Markdown and retained source reads authoritative. Generate a disposable graph view from them, with explicit manual annotations only where needed.

**Node kinds**

- Question or hypothesis, with scope and status.
- Source: scholarly work, preprint, standard, vendor report, advisory, source-code record or operational dataset; preserve stable IDs (DOI, OpenAlex, CVE, OSV, repository commit, URL) where available, and distinguish source type.
- Claim: a bounded statement attributed either to the source or to Lighthouse, with text, version, scope, interpretation class, and uncertainty.
- Observation or measurement: instrument, unit, population, window, read time, method, missingness and retained evidence location.
- Study or protocol, review, correction, investigation, publication, and (where supported) real-world outcome.
- Actor or process metadata for disclosed AI involvement. 'Unknown' is not 'human-only' and model-generated review is not independent confirmation.

**Edge kinds**

- Bibliographic: cites, mentions, shares references, or seems semantically related. These are leads, not support.
- Evidential: supports, challenges, reproduces, qualifies, derives-from, or revises. Each edge must name who asserted it, exactly which source passage or record supports it, and whether it was checked.
- Workflow: asks, tests, measures, reviews, corrects, publishes, uses or supersedes.
- Application: reports-use-in or observed-adoption-of. Preserve the distinction between authors' claims, real deployments, effectiveness, and measurable social benefit.

**Minimum edge fields:** subject and object IDs; predicate; source passage or file/line/record reference; source publication or event date; Lighthouse read/collection date; extraction or assertion date; assertion author/tool and AI role if known; 'reported', 'inferred', 'checked' or 'disputed' status; scope and qualifications. Do not manufacture numerical confidence probabilities. When evidence changes, add or version an edge rather than silently replacing history.

This is a *claim-centred* model with multiple intellectual parents. It should preserve incompatible accounts and missing links. It need not be a complete ontology: a JSON or CSV export and an auditable extraction script are enough for a pilot.

## What the public might see

The same evidence could support three views, eventually accessible from the existing site's Map section.

- **Landscape:** topics and clusters of external research, with their boundaries and sampling coverage visibly stated.
- **Lineage:** an idea or technique through time, separating citations and apparent influence from practical adoption and verified outcomes.
- **Evidence trail:** click a Lighthouse finding to see its protocol, supporting and challenging observations, subsequent reviews, correction history and reuse in later work.

The evidence trail is probably the first useful view to build. It should work as a simple text/tree view before a node-link graphic. If a graphic is later justified, keep the site static, accessible, mobile-friendly and readable without JavaScript; use the existing chart-style rules. Do not change a released piece's wording or illustrations outside its review process.

## Pilot: demonstrate use before scale

**Research question:** Does a claim-and-lineage index help a researcher locate valid prior evidence, notice disagreement or unsupported claims, and select worthwhile next questions, compared with the repository and literature search workflow Lighthouse already uses?

**Phase 0, inventory and protocol (no outcomes read for the comparison).**
- Inventory the existing claims table, source notes, review and correction links for *It was only a test*. Take a bounded sample, at most 20 claim rows and their immediate evidence, selected by a rule recorded before inspection.
- Select one small outside literature topic directly relevant to an active investigation, such as AI-assisted vulnerability discovery and disclosure, with a ceiling of 25 external works/records. Predeclare how results enter and which missing records are excluded or flagged.
- Before seeing the pilot's comparative outcomes, fix 6 to 10 concrete retrieval and checking questions, a baseline workflow, accuracy criteria, a cost ceiling, manual adjudication rules and a stopping condition. Keep the protocol in git first.
- Assess source access and licensing. Do not download full-text corpora or collect material a provider does not permit.

**Phase 1, retrospective graph extraction.**
- Implement a script that reads existing, specified Markdown/CSV and produces a versioned list of nodes, edges and unresolved candidate edges. Preserve link targets, hashes or source identifiers, and dates.
- First create only relationships explicit in retained records. LLM suggestions may go into a separate candidate list with the source passages needed for checking; they never silently become verified edges.
- Audit a preselected sample against original evidence, noting incorrect, ambiguous and omitted connections. Treat duplicates and failed external-ID matches as failures or unknowns, not successes.
- Build a minimal readable provenance view using this exported dataset. No database, crawler, live service or new framework is required.

**Phase 2, compare against current practice.**
- Have a fresh reviewer attempt the fixed questions using the normal repository and literature search, and then the graph-assisted version, with order or question assignment balanced where feasible.
- Record correct retrieved sources and claims, false links, important omissions, time or tool usage where available, review effort, repeatability and what was genuinely new rather than surfaced twice. Disclose learning and shared-context effects.
- Ask separately whether an actual next investigation changed for a defensible reason. A prettier picture or more nodes is not a research-quality outcome.
- Publish a candid internal evaluation with a recommendation to stop, revise or expand. Any public claims follow the ordinary review process.

**Expansion only if the pilot earns it.** Integrate a small export with the existing research scout and proposals gate, so that each scout lead can point to related prior work. Consider a public lineage view after accessible, reproducible traversal is useful to a non-technical reader. Larger bibliometric maps and retrospective metrics of Lighthouse's research process remain optional follow-ups.

## Questions worth keeping open

- Can we distinguish an idea's cited lineage, evidence lineage and practical impact without collapsing three very different relationships?
- Where do research papers, vendor claims, code, security advisories and real-world interventions disagree about AI-assisted discoveries?
- How much AI assistance in scientific work can actually be measured from disclosures, rather than guessed from style or publication volume?
- Do unusual bridges between research communities yield useful new investigations, or merely graph artefacts?
- Does prior-knowledge retrieval reduce redundant Lighthouse studies, cost or errors? What is the honest denominator?
- Can a longitudinal history of revisions reveal where AI-assisted research improves or weakens its own reliability?
- How are sources outside scholarly indexes, and sources blocked by rules, licences, paywalls or expiry, represented without treating the missing region as empty?

## Risks and boundaries

1. **Selection and visibility:** indexing favours certain disciplines, languages, accessible journals and easily cited work. The observed graph is a sample, not 'the scientific world'. A central node can be better indexed rather than more important.
2. **Citations and causality:** citation edges alone do not show agreement, truth, novelty, reproducibility or realised value. Do not use influence scores as quality rankings.
3. **Hallucinated lineage:** model-extracted relationships require evidence-gated checks; contradictory findings remain separate; every edge is inspectable and removable without destroying its audit trail.
4. **Research integrity:** keep source claims separate from Lighthouse's observations; human, AI and mixed contributions distinguishable when known; corrections and supersessions visible.
5. **Collection safety:** the same site-access, robots, credentials, privacy and security boundaries in AGENTS.md apply. This pilot reads permitted metadata and retained records, not exposed hosts or executable artefacts.
6. **Scope creep:** no indefinite research-monitoring agent, no speculative universal knowledge graph, no mandatory changes to all study templates, no paid subscriptions without the keeper, and no fourth active investigation.
7. **Cost and value:** measure ingestion, verification and maintenance effort as well as purported discovery benefits. The map could fail the pilot even if it looks impressive.

## Decision requested and next handoff

Treat this as a proposed **method/instrument repair and research pilot**, relevant across the existing investigations, not an announced discovery or new active investigation. The horizon gate should assess it against the charter and throttle, allocate the next proposal number if appropriate, and schedule no new collection before the pilot brief is fixed. Prefer using the current security-research work and the retained essay record as seeds.

The first implementable deliverable is a short protocol and a manually checked, reproducible graph of selected existing records, with a baseline comparison. A result that finds no research advantage is still useful and should be recorded rather than amplified into a larger project.

This document preserves the keeper's whole idea and its branches for future sessions, whether the work is taken forward in ChatGPT Work, another agent harness, or Harbour.