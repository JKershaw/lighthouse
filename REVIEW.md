# Review of the Lighthouse founding documents

Reviewed: edition 0.1 of LH F01 to F04, as uploaded on 25 September 2026. Reviewer: Claude, at the steward's request. Result: edition 0.2 (draft) of each document, a README, and LH F05 (study templates), all on this branch.

## The idea as I read it

Lighthouse proposes an observatory for the computational world. Its subject is the flow of information through software, infrastructure, people and AI, and the structures that flow leaves behind. The founding insight is that a model call is a transient event with durable consequences. An agent runs for minutes, but the code, configuration and data it changes keep acting for months, and later flows need no further inference. Lighthouse wants to observe both halves and to be honest about what its instruments cannot see.

It works in two directions. Close observation instruments systems it can reach, beginning with Harbour, whose dispatch records describe a known workflow that sensors can be tested against. Outward observation uses public data to ask whether patterns seen up close recur across the internet, and to find what the close instruments missed. Disagreement between the two is treated as evidence.

Underneath sits a specific worry: that self-sustaining harmful digital activity could degrade shared infrastructure, by analogy with orbital debris. The documents deliberately hold that worry as a research question rather than a premise, and build in commitments (four kinds of statement, uncertainty made visible, explanations that can fail, self-accounting) to stop the worry from colouring the observations.

Harbour is both instrument and subject, and appears to share its steward with Lighthouse. The documents treat that as a relationship to disclose and check rather than to hide.

## Overall assessment

The four documents are unusually disciplined for a founding draft. The commitments are concrete enough that a breach would be recognisable. The hedging is honest without being timid. The two pilots are designed to yield something useful even if their hypotheses fail. The prose is plain and the terminology mostly consistent.

The weaknesses are mostly external. The documents were written without checking what Harbour actually records and for how long, what Harbour already publishes, and whether the cited sources still exist as described. Each of those checks changed something in the plan. There were also a few internal defects: a promised bundle of templates that did not exist, metaphors introduced as if the reader already knew them, and no measurement surface for a concept the charter puts in scope.

## Findings, most important first

### 1. Lighthouse was not positioned against Harbour's existing research programme

Harbour's repository carries a papers programme with a writing standard, a proposals queue and more than a dozen empirical papers about its own workflow: review loops, task generation rates, cheap-implementer trials, capability ledgers and more. Edition 0.1 said Harbour "may also organise Lighthouse investigations" but never said how Lighthouse differs from research Harbour already does, or whether Lighthouse publications would follow a second, incompatible standard.

Changed: F01 states the distinction. Lighthouse studies the computational and informational footprint and the comparison with the wider internet; it cites rather than repeats Harbour's papers. F03 adopts Harbour's paper structure and header for Lighthouse studies and adds what Lighthouse needs on top. F04's decision register records that choice. The README says it in one paragraph.

### 2. Harbour's records expire, and LH001 had no export step

Harbour's documentation states that dispatch items expire after twenty-four hours and that feedback history, agent status and proxy audit logs are retained for thirty days. LH001 planned to reconcile sensor readings against "Harbour's operational record" during weeks 3 and 4 and then observe a follow-up window, with nothing said about capturing that record before it disappears.

Changed: F02 adds a measurement rule on retention windows and exports. F03's integration contract makes the copy into the protected store explicit and calls it an observation. F04 adds a Retention paragraph to LH001, an export step in the launch table, and a decision-register row.

### 3. Host observability in LH001 depends on the dispatch target

Harbour dispatches carry a target field: command-line, web, dashboard or local. A web session runs on the provider's infrastructure, where Lighthouse has no host access. LH001 asked for "host process activity where available" without noting that the choice of target decides whether it is available at all.

Changed: F04's LH001 design and execution record require choosing an instrumentable target, and the commencement choices include it.

### 4. Harbour's operational record is partly agent-reported

Queue and claim times are server-side, but progress, completion markers and usage entries are posted by the agent. Edition 0.1 treated "Harbour's operational record" as a single comparator. For calibration it is two things: a server log of what was asked, and an agent's own account of what it did.

Changed: F02's calibration section and F04's comparators paragraph say so. The illustrative sequence in F02 shows where each kind of record comes from.

### 5. The promised source bundle did not exist

F02 said "the source bundle supplies reusable instrument and study records" and F03 said "use the templates in the editable source bundle". The repository held only the four documents.

Changed: LH F05 supplies compact templates for the question register, study brief, instrument record, observation record, claim record, decision record, release record, correction record and the study publication skeleton. If a bundle exists elsewhere, F05 can be dropped or merged. The other documents now reference F05 by name.

### 6. Sources: one moved, one misdated, one unread, six added

All seven links in F02 were fetched on 25 September 2026.

| Source | Result |
| --- | --- |
| S1 Kephart and White 1991 | Resolves and matches |
| S2 Ray, Tierra | Resolves. Edition 0.1 dated it 1995; that is the HTML conversion date in the page footer. The paper is a 1992 Santa Fe Institute working paper. Corrected |
| S3 Anderson and Moore 2006 | Resolves to an eleven-page PDF. Text extraction failed in the checking environment, so the content was not confirmed. Noted in F02 |
| S4 METR 2024 | Resolves and matches. Authors' first names added |
| S5 GH Archive | Resolves. Added the 2015 transition from the Timeline API to the Events API and the changing-payload caveat |
| S6 OpenTelemetry GenAI | The cited page now says the conventions moved to a dedicated repository. Reference updated |
| S7 Cloudflare | Resolves. Last updated 23 April 2026 |

Added and checked: S8 Kessler and Cour-Palais 1978 (origin of the analogy, confirmed through the Crossref record), S9 Menlo Report 2012 (ethics for ICT research, PDF text confirmed), S10 Software Heritage (documentation and API index resolved; main site returned an error), S11 deps.dev (documentation resolved), S12 Harbour dispatch and proxy documentation, S13 Harbour papers standard.

### 7. Metaphors arrived unintroduced

F01 said "The coral image describes this accumulated habitat. The veins describe its circulation. The ripple of light describes transient processing" with no earlier mention of coral, veins or light. This looks like a residue of an earlier draft or a visual identity. The expanding-universe line had the same problem, and the name Lighthouse was never explained.

Changed: F01 introduces the three images in one paragraph, keeps the disclaimer, rewrites the expanding-universe sentence, and adds one line on the name.

### 8. Authority was in scope but had no measurement surface

F01 lists authority in the research scope and F02 insists that "having authority to change a system" is a different connection from sending bytes, but the measurement table had no row for it. Harbour makes authority directly measurable: token scopes, single-use bootstrap tokens, and a charter line separating AI-permitted from human-only actions.

Changed: F02 adds an Authority row. F01's authority section commits Lighthouse to respect Harbour's human-only line when Harbour is the subject.

### 9. LH002 had no rule for contributor identity

Public commit and event records carry names and often email addresses. LH002 said to separate identified bots from unknown contributors but not how identities would be stored or published.

Changed: F04 adds an Identity paragraph. Raw identifiers stay in the protected store; published outputs are limited to counts, categories and pseudonyms. F02 cites the Menlo Report as the reference for such decisions.

### 10. Repetition across the set

The disclaimer that the documents grant no access, spending or release authority appeared in F01, F03 and F04. "Publication count is not progress" appeared in F01 and F03. The four kinds of statement were restated in three places.

Changed: the disclaimer lives in F01 and the README, and F03 and F04 keep one clause each. Other repetition was reduced where a cross-reference does the job. Each document still stands alone, which I took to be the intent.

### 11. Mechanical

Subtitle lines had lost their commas ("Purpose scope and commitments"). "Looks towards systems it can observe closely and outward" is now "looks inward ... and outward". "The standard CPU approximation" is retitled to say what it is: the busy core second as a starting unit. Sentences that ran two thoughts together were split. Edition headers now read 0.2 (draft).

## What I did not change, and questions for the steward

- **Clause labels.** Harbour's charter labels every clause BINDING, PRINCIPLE or DEFERRED and tests each with "how would an outsider know this was broken?" Most of F01's Commitments would pass that test. I recommend adopting the labels but did not, because it changes the document's form and is your call.
- **The steward is unnamed.** Every document says "the founding steward". Harbour's charter names its maintainer. F01 now discloses the overlap conditionally ("where the steward of Lighthouse also maintains Harbour"). Replace that with a plain statement when you are ready.
- **Is the Kessler hypothesis the real motivation?** The documents hedge it into one paragraph of the scope section. If it is why Lighthouse exists, say so near the top of F01 and then apply the commitments to it. "We are worried about X, and here is how we will stop ourselves seeing X everywhere" reads more honestly than X appearing as one item in a list.
- **Twelve weeks is heavy for one person.** Three roles, two studies, an instrument register, a synthesis and a publication surface. If the steward is also the analyst, consider making LH002 a feasibility note in the first programme and a full study in the second.
- **Should Lighthouse run inside Harbour?** Harbour supports a local task store and a research task kind. Running Lighthouse's own tasks through it would exercise the integration contract from day one and would itself generate the known workflow LH001 needs. The cost is deeper entanglement of subject and instrument, which F01 already commits to disclosing.
- **Retention could be extended for a research workspace.** As Harbour's maintainer you could lengthen the thirty-day windows. F01 treats any change to the subject as a separately scoped decision. Either way, write the decision record.
- **The word observation.** Harbour's Observation view and Lighthouse's observation record are different things. The README glossary notes it. If confusion shows up in practice, "reading" is the natural replacement for Lighthouse's unit.
- **Three repetitions.** LH001's pilot of three runs will bound timing error to a range, not estimate it. The document already calls it an instrument pilot; keep that label in the published study.

## Verification limits

Harbour's fields, states and retention windows were taken from its documentation on the main branch on 25 September 2026, not from a running instance. The feedback flow, the usage entries and the thirty-day retention are the details most likely to change; F03 says to verify them at commencement. I could not read the text of S3 or reach the Software Heritage main site from this environment.

## Change summary by document

- **README.md** (new). Index, reading order, Harbour paragraph, glossary, edition history.
- **LH F01 Charter.** Name explained; metaphors introduced; Harbour described concretely and its papers programme distinguished; "what Lighthouse is not" added; Harbour's human-only line respected; the no-authority disclaimer made canonical here; punctuation fixed.
- **LH F02 Research Design.** Illustrative sequence added and labelled; Authority surface added; retention rule added; the agent-reported parts of Harbour's record noted; Menlo Report cited for boundaries; Kessler analogy sourced; S2, S5 and S6 corrected; S8 to S13 added, each with a check note.
- **LH F03 Handbook.** Harbour section rewritten from its documented records; integration contract mapped to dispatch fields and feedback entries; publication practice adopts Harbour's paper standard with additions; agent runs retained for reproduction; references to F05.
- **LH F04 Programme.** Launch table includes record confirmation and export; LH001 gains target, retention and comparator caveats; LH002 gains Software Heritage, deps.dev, a completeness caveat and an identity rule; a Harbour-bridging follow-up question; two decision rows.
- **LH F05 Templates** (new). Nine compact templates.

## Addendum: the originating conversation

The steward supplied an extract from the conversation that produced edition 0.1. It clarified four things that the drafts implied but never stated, and each is now explicit.

- **Three observational layers.** Activity (computation happening), residue (the altered structure and state it leaves) and propagation (how that residue influences later activity elsewhere). This is the organising idea of the whole project and belongs at the front of F01 and F02, not only inside the metaphors. Added to both, with a Layer column in F02's measurement table and a statement that propagation is a typed link between residue and later activity rather than a surface of its own.
- **An enduring pattern with transient participants.** The strongest sentence in the extract: the phenomenon's identity would lie in the pattern being maintained and propagated, while every individual process disappears. Added to F01's scope section and F02's Kessler section, with the existing caveat that a release train can look the same.
- **Complement, not component.** Harbour is the control plane; Lighthouse is the observatory. Harbour asks whether a task did what was asked; Lighthouse asks what the activity changed and what the change made possible. Added to F01's close-observation section and the README.
- **The apparent ripple depends on the instrument.** The picture is assembled from observations with different delays and resolutions. F02 now says to state the instrument and timescale alongside any description of a burst.

Two consequences for the pilots. LH001's follow-up window now has a stated purpose: recording any activity the change enabled, the smallest observable instance of propagation. LH002 now records a dependency change followed by a change in a dependent as a candidate propagation link, after testing the ordinary explanations.

One naming question for the steward. Residue is precise and is the word the conversation used, but it carries a faint sense of waste. Deposit or sediment would fit the coral image; trace is neutral. The documents keep residue until you choose.
