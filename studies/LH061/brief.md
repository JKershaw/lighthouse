# LH061: What does published evidence measure about whether containment and recovery work, and what does it only assert?

**In short** (added 24 November 2026; not part of the protocol). When something goes wrong on the internet, defenders take servers down, cut off the domains malware talks to, cancel leaked passwords and keys, and rehearse together how they'd recover. A lot is said about whether those things work; we want to know how much of it has actually been measured. We'll run eight fixed searches, look for the published reports of five named exercise series, read at most twenty documents, and sort every claim about an outcome by whether its authors measured it, asked people, modelled it or simply asserted it. Nothing has been read yet beyond the summaries a sweep relayed; reading runs from 25 November to 15 December and the record follows by 18 December.

**Protocol 0.1, fixed 24 November 2026, before any document or search result for this study was read beyond the abstracts, snippets and summaries scouts 5 and 6 relayed on 24 November, and before any search for this study was run.** Writer: a research subagent in Claude Code (Claude Opus 5.5, Anthropic) for the Horizon run 2026-11-24T121300Z-anthropic-horizon, answering proposals.md P-0046 and P-0048 together, the keeper's directions of 23 November 2026, agreed by the keeper in conversation on 24 November 2026 ([the keeper's decision](../../notes/keeper/2026-11-24-defensive-side.md)), as one desk note under one classification, as the gate recommended ([the gate](../../notes/horizon/2026-11-24T1213Z.md), "Gate": the P-0046 and P-0048 rows and "Overstatements and rule points"). The study belongs to the defensive strand of [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md). The writer made no web request of any kind. The driving session commits this brief and its schedule rows ([rows.csv](rows.csv)) before the first search.

## Question

**What does published evidence measure about whether containment and recovery work, and what does it only assert?**

Two parts under one design and one classification:

- **Part A, containment.** What do published outcome studies of containment measures report about the outcome each measure was meant to change, over what period, and on what population: takedowns of servers, sites or domains, sinkholing, revocation of leaked credentials, and any other containment measure (blocking, isolation, quarantine, suspension of accounts or services) that the search rule below finds.
- **Part B, recovery exercises.** What do published after-action or evaluation reports of cross-organisation cyber recovery exercises measure about recovery and coordination, and what do they only assert?

Terms, fixed now:

- **Containment measure:** an action taken by defenders (an operator, a registry or registrar, a hosting or service provider, a law enforcement or public body, a researcher acting with one of them) to stop or limit harmful activity already under way: taking down infrastructure or content, redirecting or sinkholing domains, revoking or rotating credentials, blocking, isolating or quarantining systems or accounts, suspending services. Deploying a security fix or feature is not containment here; it is [LH060](../LH060/brief.md)'s question.
- **Outcome of a containment measure:** a change in the thing the measure was meant to reduce (infections, abuse, malicious resolutions or traffic, the validity or use of a credential, damage), or how long a measure or its effect lasted, as a count, share, rate or time.
- **Cross-organisation cyber recovery exercise:** a planned exercise, tabletop or live, in which more than one organisation practises responding to and recovering from a cyber incident together, run or sponsored by a government, regulator, sector body or international organisation.
- **Recovery or coordination outcome:** what happened in the exercise (or after it) to restoring services, decisions, information sharing or coordination across organisations, as a time, count, share, rating or stated result, and whether earlier recommendations were followed up.

The study says nothing about AI unless an included document does, and then only as that document's claim. It does not study, rank or describe how any harmful activity, AI or otherwise, could survive containment, spread or sustain itself (see Research safety).

## What the writer already knows

All of this is prior knowledge, read before the brief, and none of it is a reading in this study. Everything below is as scouts 5 and 6 relayed it on 24 November 2026 ([scout 5](../../notes/horizon/2026-11-24T1213Z/scout-5-research.md), Part B, P-0046; [scout 6](../../notes/horizon/2026-11-24T1213Z/scout-6-policy.md), Part B), from abstracts, record pages, snippets and two PDFs read by text extraction at headline level; the writer has read the scouts' logs, not the documents.

**Part A (scout 5, Part B):**

- Nadji and others, "Beheading Hydras", ACM CCS 2013 (snippet only, not opened): a retrospective evaluation of takedowns; some effective, others with no significant long-term effect, as relayed. Public data unknown.
- Asghari, Ciere and van Eeten, "Post-mortem of a Zombie", USENIX Security 2015 (record page opened by the scout): sinkhole data on Conficker cleanup by country; national anti-botnet centres had no visible effect on infection rates, as relayed. Underlying data not stated.
- A domain takedown study at NDSS 2019 (University at Buffalo, as relayed; snippet only, not opened): sinkhole durations by the party taking a domain down, and reuse of taken-down domains.
- Meli and others, NDSS 2019 (snippet only): leaked secrets and revocation. The gate recalls it as being about secrets leaked on GitHub and whether those who leaked them removed them, not providers' automatic revocation; to be checked at source.
- TruffleHog, 2023 (a vendor): 74 per cent of leaked credentials still live at 31 days, and revocation almost always within three days or never, as relayed. A Cloud Security Alliance note of October 2026 ties survival to whether the provider revokes automatically, as relayed. arXiv 2603.12498 says leaked credentials persist for "months to years", as relayed.
- arXiv 2611.30483 (23 November 2026, preregistered): what limits the damage of an AI agent's mistake on a database; recoverability over damage prevention; small open-weight models; preliminary, as relayed.
- The scout found no aggregate outcome study of segmentation or isolation. The gate notes that this is a thin search's absence, and that the scout's bullets rest on a handful of searches, mostly snippets.
- The scout also named Shadowserver-style public dashboards as a possible aggregate source, not checked. Dashboards and datasets are outside this study (see Never done).

**Part B (scout 6, Part B):**

- CISA's Cyber Storm IX after-action report (September 2024 file dated 1 October 2024; exercise April 2024; more than 2,000 participants per a search result; 37 pages, 8 numbered findings and consolidated recommendations, TLP:CLEAR), qualitative as relayed; earlier editions public (a 2016 report, a 2020 exercise report of January 2021, a Cyber Storm VIII file of August 2022). The scout did not check for per-finding measures or follow-up of earlier recommendations.
- SIFMA's Quantum Dawn VII public after-action report (1 May 2024; exercise 14 to 16 November 2023): participant-reported poll percentages (75, 98 and 80 per cent, among them 98 per cent having plans), a third-party outage scenario, participants unnamed; statements about plans, not shown recovery.
- ENISA's Cyber Europe after-action reports (2014, 2018, 2022, 2024; the 2024 report published 10 December 2024, about 5,000 participants as relayed; headline as relayed from a snippet: reporting collaboration good, limits in showing cross-border impact). Refused to Anthropic's agents by robots.txt under the strict rule the scout gated in; not opened. Cyber Europe 2026's report not out as of the scout's read.
- The Bank of England's SIMEX 24 page (2 October 2024): no outcomes published on the page read, an assurance-only case; SIMEX 22 (November 2022) mentioned; the SWES final report (29 November 2024, about 50 firms, six conclusions) not read and not an exercise of the kind defined here unless the inclusion rule finds it is.
- NATO CCDCOE's Locked Shields 2026 (ended 24 April 2026, 41 nations as reported): scoring and press; no primary lessons report found; a weak fit for cross-organisation recovery measures, as the scout judged.
- None of the PDFs the scout read gave a measured time to restore services.

**The writer's expectation,** from general knowledge, not read for this brief: Part A's peer-reviewed literature measures takedown and sinkhole outcomes mostly for botnets and malicious domains from about 2013 to 2020, often with short observation windows; credential-revocation outcomes come mostly from vendors; Part B's reports are mostly qualitative or self-reported, and few, if any, give a measured recovery time. The writer also knows of NERC's GridEx series of grid security exercises, which is not on the named list below and enters only if the admission rule admits it.

## Search rule (fixed now)

**Tool.** The WebSearch tool of the Claude Code harness running the study, one call per query, no other search engine, catalogue or scholarly API. A search result is a lead, never a source: titles, venues, years and snippets are used only to screen candidates.

**Queries,** exactly eight, run once each, verbatim, in this order:

- **QA1:** `botnet takedown effectiveness measurement infection rates before and after`
- **QA2:** `domain sinkholing takedown outcome longitudinal measurement study`
- **QA3:** `leaked credentials revocation measurement study time to revocation`
- **QA4:** `phishing or malware site takedown speed measurement study`
- **QA5:** `incident containment effectiveness empirical evaluation isolation quarantine`
- **QB1:** `cyber exercise after-action report findings cross-sector recovery`
- **QB2:** `"after-action report" national cyber exercise recovery coordination results`
- **QB3:** `evaluation of multi-organisation cyber crisis exercise outcomes study`

No query is reworded, added or rerun. A query that errors is recorded as failed and not replaced. Results of the QA queries are candidates for Part A and of the QB queries for Part B; a result that fits the other part's definition joins that part's candidate list instead, recorded as such.

**Year range.** Published from 1 January 2012 to 15 December 2026 inclusive.

**Venues, Part A.** A candidate must come from one of these:

- peer-reviewed conferences: IEEE Symposium on Security and Privacy, IEEE EuroS&P, USENIX Security Symposium, ACM CCS, NDSS, ACM Internet Measurement Conference, Passive and Active Measurement (PAM), the Workshop on the Economics of Information Security (WEIS), APWG eCrime, RAID, ACSAC, ACM AsiaCCS, the Network Traffic Measurement and Analysis Conference (TMA);
- peer-reviewed journals: Computers & Security, IEEE Transactions on Dependable and Secure Computing, IEEE Transactions on Information Forensics and Security, ACM Transactions on Privacy and Security, Journal of Cybersecurity, ACM Computing Surveys;
- preprints on arXiv;
- reports (not press releases) of: CISA, ENISA, the UK's NCSC, Europol, the Anti-Phishing Working Group, the Cloud Security Alliance.

**Venues, Part B.** A candidate must be one of:

- a report, after-action report or published summary of results of a named or admitted exercise series (below), on the site of the organiser, sponsor or an independent evaluator named by the organiser;
- a peer-reviewed evaluation of a cross-organisation cyber exercise in a listed Part A venue, or in a peer-reviewed journal or conference on emergency management, crisis management or public administration, where the search metadata shows peer review.

News, blogs, vendor marketing pages, vendor blogs and secondary coverage are locators only, in both parts: they may name a document in a listed venue, which then enters the candidate list, but they never count as documents. TruffleHog's 2023 figures are therefore a locator only, unless it is relayed by a document in a listed venue.

**Named exercise series (Part B), fixed now:** Cyber Storm (CISA), Quantum Dawn (SIFMA), Cyber Europe (ENISA), SIMEX (the Bank of England with the UK's financial authorities), Locked Shields (NATO CCDCOE). For each, the candidates are the public report of the most recent edition published by 15 December 2026 and the public report of the edition before it, where each exists.

**Other series, admitted only if** a QB query returns one of its reports, it meets the definition of a cross-organisation cyber recovery exercise above, and its organiser or sponsor posts at least one report of results on its own site. At most three other series are admitted, in order of first appearance in the QB results; for each, only the edition the result points to is a candidate.

**Locator reads.** To find a named or admitted series' report where neither a query nor the scouts' URLs give it, at most one gated one-off GET of the organiser's own page for that series, at most eight such GETs in all. A locator read is used only for links to reports and their dates; no body is kept; it is logged in the fetch log as a locator and does not count against the twenty documents. No locator read is made of a page that is itself a candidate document.

**Known documents.** The documents scouts 5 and 6 named that fall in a listed venue enter the candidate list whether or not a query returns them, and meet exactly the same inclusion rule as any other: none is included or excluded for being known. Part A: Nadji and others (CCS 2013); Asghari, Ciere and van Eeten (USENIX Security 2015); the NDSS 2019 domain takedown study; Meli and others (NDSS 2019); arXiv 2603.12498; arXiv 2611.30483; the Cloud Security Alliance note of October 2026. Part B: Cyber Storm IX's report; Quantum Dawn VII's public report; Cyber Europe 2024's report; the SIMEX 24 page; and whatever Locked Shields report the rules above find.

## Inclusion and exclusion (fixed now)

**Screen, on search metadata.** A result becomes a candidate if it is in a listed venue (or a named or admitted series), in the year range, and its title or snippet plausibly concerns the part's question. A preprint and its published version are one candidate.

**Inclusion, Part A, decided only on the document read.** A document is included if it meets all three:

1. it concerns a containment measure as defined above, applied in the field or tested in a laboratory or simulation;
2. it measures, models or reports an outcome of that measure (a change in the thing the measure was meant to reduce, or a duration), whether or not the result favours the measure;
3. it states its method: population, how the outcome was obtained, and the period.

**Inclusion, Part B, decided only on the document read.** A document is included if it meets all three:

1. it concerns a cross-organisation cyber recovery exercise as defined above;
2. it is published by the organiser, a sponsor or an independent evaluator, or is a peer-reviewed evaluation;
3. it reports on the exercise's conduct or results (findings, lessons, outcomes, ratings, or statements of them), or is the organiser's public page for an edition that has taken place.

A report that publishes no outcome at all (the scouts' reading of SIMEX 24) is included under Part B as an assurance-only case if it meets the three conditions, and recorded as reporting no outcome.

Every document read that meets its part's three conditions is included.

**Exclusion, with the reason recorded:** fails any of its part's conditions; is a detection, attribution or measurement-of-abuse study with no containment outcome; its outcome is deployment of a security fix or feature, including notifications whose outcome is patching (LH060's question); its contribution is a technique for evading, surviving or defeating containment (excluded unread where the title or snippet shows it, and if found on reading, nothing from it is recorded beyond the exclusion reason); a press release announcing an exercise or operation before or without results; an exercise of one organisation alone, or a training exercise whose outcome is individual learning; outside the venues or years; a duplicate of a document already read; or its full text unavailable (a wall, refusal or error). Excluded documents stay in the source register with their reason. A document that discusses containment or recovery without reporting an outcome (for example, guidance, interviews alone) is excluded as a document but may be cited as context in the record, labelled so, with nothing from it counted.

## Ceiling and order of reading (fixed now)

At most **eight searches** and at most **twenty documents**, each read by one gated one-off GET of its full text, plus at most eight locator GETs. Part A has up to **eleven** of the twenty GETs and Part B up to **nine**; when one part's candidate list is exhausted, its unused GETs pass to the other part. The abstract page is not fetched separately; for arXiv the full text is the PDF at `https://arxiv.org/pdf/<id>`. One retry is allowed only on a timeout, a connection error or HTTP 500, 502 or 504, inside the same document. A GET that meets a challenge, login, registration form, rate limit or any non-200 answer counts against the twenty and is recorded as a wall; it is not got around, and no third-party copy, mirror or archive is fetched instead. A URL the robots gate refuses under the one-off rule before any request is made is recorded as unavailable (for Cyber Europe, the scouts' reading means this may happen: it is then a wall, recorded and not got around) and does not use a GET.

**If more candidates than GETs,** candidates are read in this order, fixed now, until each part's GETs are spent or its list is exhausted:

- **Part A:**
  1. by tier, as the search metadata gives the venue: peer-reviewed conference or journal first, then reports from the listed publishers, then arXiv preprints not stated as published;
  2. within a tier, most recent publication year first;
  3. ties by order of first appearance in the results, QA1's first result before QA1's second and so on through QA5; known documents not returned by any query follow, in the order listed above.
- **Part B:**
  1. the most recent edition's report of each named series, in the order Cyber Storm, Quantum Dawn, Cyber Europe, SIMEX, Locked Shields;
  2. the preceding edition's report of each named series, in the same order;
  3. admitted series' reports, in order of first appearance in the QB results;
  4. peer-reviewed evaluations, most recent first, ties by first appearance in QB1 to QB3.

Candidates left unread are listed in the record by title, venue and year as "candidate, not read"; nothing is claimed from them, and the record says how many there were. A document read and then excluded still used its GET.

## How fetches are made and what is kept

- Every fetch, locator reads included, goes through `scripts/lh_fetch.py` with `access='oneoff'` (the keeper's decision of 21 November 2026, [notes/keeper/2026-11-21-robots-intent.md](../../notes/keeper/2026-11-21-robots-intent.md)), the robots gate applied before the request and before any redirect (`check_redirects=True`), with `LIGHTHOUSE_PROVIDER=anthropic` (or the provider actually running the session).
- A body is kept only through `save_body`, which applies the robots and page-reservation rule in one place (`keep_decision`), and only where the document also states a licence that allows redistribution (for example CC BY) or states that it is in the public domain; otherwise no body is kept and `write_derived` keeps the URL, read time, status, sha256 of the bytes received, the facts used and short attributed quotations. Where `keep_decision` says no, the reason is logged. Emails are withheld (`redact_bytes`; `python3 -I scripts/redact_emails.py studies/LH061` before any commit).
- Every request, including failures, walls and robots refusals, goes in `studies/LH061/fetchlog.csv`, marked document or locator; every search goes in `studies/LH061/searches.md` with its UTC time, the query verbatim, and each result's title, URL, venue and year as shown, marked opened or not. Snippets are not retained.
- PDFs are read as text extracted in memory; no code from any download is run, and no dataset, appendix archive, dashboard, indicator list or artefact a document links to is fetched.

## Classification of each claim

The unit of synthesis is a **claim about an outcome**: in Part A, about the outcome of a containment measure; in Part B, about a recovery or coordination outcome of an exercise. For each included document the source register records: part; venue and whether peer reviewed; publication date; the measure or exercise (at the document's own level of generality); population and unit; the outcome; the observation window; whether the data are public; and the funder, organiser or publisher's interest where stated. Each claim is then classed, one class only:

- **measured outcome:** the outcome was counted or timed by the authors or evaluators from observation (scans, sinkhole or DNS data, logs, telemetry, exercise timings or evaluators' observation against stated objectives), recorded with **what was measured, on what population, over what period**;
- **self-reported:** the outcome comes from participants' or operators' own answers (survey, poll, interview, self-assessment);
- **modelled:** an estimate inferred from a model (regression, simulation, extrapolation), with what it controls for;
- **asserted:** stated without data shown in the document.

Two further labels, recorded beside the class: **setting** (field: real incidents or infrastructure; exercise: a planned exercise, whose measured outcomes are of exercise performance, not of real recovery; laboratory: a controlled test or simulation); and **vendor**, for a claim resting on a vendor's own customers or product telemetry. A claim a document relays from another is classed by its origin and linked to it; two documents resting on the same dataset count as one origin.

For Part B, each report also records two facts of the report itself: whether it gives any measured time to restore a service or function (yes, no, not stated), and whether it reports follow-up of an earlier edition's recommendations (yes, no, not stated).

## The comparison that matters

- **Part A:** across included claims, the direction each reports for its outcome (fell, fell then returned, no visible change, rose, mixed), with the duration observed, tabulated with its class, setting, measure type, population and window.
- **Part B:** for each report, the count of outcome claims in each class, and the two report facts above; across reports, how many give any measured outcome at all.
- **Both parts:** how many claims of each class there are, how many rest on public data, and how many are vendor.

The unit is the claim, reported per part; documents are not pooled, no figure is combined across documents, and the two parts are never added together. Agreement or disagreement is a description of what the documents report, not a test. A change after a measure is the authors' finding, reported in their terms; no causal claim is made in Lighthouse's voice beyond what a study itself measured and claimed, and an exercise's result is never read as evidence of real-world recovery.

## Missing evidence

- A document not read (wall, refusal, error, or beyond the ceiling) is **unread**, never evidence that no such study or report exists.
- A part with no measured outcome claim is reported as "none found in eight searches and the documents read", never as an absence in the literature or a lack of effect.
- A measure type the search did not surface (for example segmentation or isolation) is reported as **not found by this search**, not as untested.
- A field a document doesn't report (population, window, data availability, follow-up) is **not stated**.
- A named series whose report could not be found or read is listed with the reason (not located, wall, robots refusal, no public report).

## Overlap with earlier studies

- **[LH060](../LH060/brief.md)** (deployment of security fixes by operator size, reading to 11 December) uses the same four classes on another question. Its outcome is deployment; this study's is containment and recovery, and deployment outcomes are excluded here. A document that appears in both studies' registers is read under each brief separately, listed here as "also read for LH060", and no claim is counted in both. Nothing is pooled across the two.
- **The cost investigation's other studies** ([LH041](../LH041/LH041.md), worm waves; [LH042](../LH042/LH042.md), published exposure counts; [LH044](../LH044/brief.md), the closing web; [LH045](../LH045/brief.md); [LH051](../LH051/brief.md), a CI secret stealer's traces and their cleanup in GH Archive; [LH052](../LH052/LH052.md), organisational reliability; [LH055](../LH055/LH055.md), ARTEX; [LH058](../LH058/brief.md), November's outages; [LH059](../LH059/brief.md), Amazon's report) measure or read particular events, campaigns or surfaces. This study reads published literature and exercise reports only; none of their data or findings enters it, nothing is counted twice, and no record of theirs is re-read. LH051's own cleanup counts are not a document of this study.
- The scouts' relayed summaries are prior knowledge, not readings.

## Voice

Findings are the authors', attributed with their class, setting, population and window. No causal claim is made beyond what a study measured. No operator, participant, organisation or system is called weak, slow or unprepared by Lighthouse, and none is named beyond what a report says at its own level of generality. Lighthouse makes no claim that harm is happening now or that any named system is compromised.

## Never done

- No host, domain, credential or indicator is enumerated, resolved, looked up, tested or visited; no sinkhole, dashboard, takedown list or dataset is fetched; no live test of any kind.
- No catalogue of what defeated a containment measure, or of how adversaries survived or evaded one, is made or kept: where a document gives reasons a measure failed or an effect faded, the record says only that the authors give reasons, without restating them, and such reasons are never tallied across documents.
- No participant, operator or system is listed as weak or named beyond what a report says at its own level of generality; nobody a source anonymised is re-identified, by name or by the shape of their description.
- No dependency map is compiled, from one report or across reports; no combined infrastructure-failure scenario is written.
- Nothing discusses how AI activity could spread or sustain itself from the attacker's side, at any level; arXiv 2611.30483, if read, is recorded for its recoverability outcome only.
- Nobody is contacted: no author, organiser, publisher or operator.
- No body is kept except as above; no paywall, registration form, robots refusal or rate limit is got around.

## Model and interest disclosure

Lighthouse runs on Anthropic's models; this brief was written on Claude Opus 5.5. arXiv 2611.30483 concerns AI agents' mistakes and uses small open-weight models, not Anthropic's as relayed. If any included document concerns an AI developer's models (Anthropic's or those of a provider Lighthouse sometimes runs under, such as OpenAI's), the record says so beside the claim; reviewers look for wording easier or harder on any AI developer than the sources allow.

## Research safety

Assessed when the brief was fixed, under [schedule/research-safety.md](../../schedule/research-safety.md): **proceed, narrowed.** The study reports outcome measures and durations only. It never catalogues what defeated a containment measure or how adversaries survived or evaded it; never lists weak or named participants, operators or systems beyond what a report says at its own level of generality; never compiles dependency maps; and never discusses how AI activity could spread or sustain itself, from the attacker's side, at any level. Why: [the keeper's decision of 24 November 2026](../../notes/keeper/2026-11-24-defensive-side.md). The check is repeated if a document read contains evasion or survival detail, host or indicator lists, named poorly prepared participants or dependency detail; such material is not kept, quoted or passed on, and the affected work stops as the assessment says.

## Resource ceiling, dates and stopping

- Eight searches, twenty documents and eight locator GETs as above; at most one reading subagent; no paid service, account or key. About **$15 at list rates before reviews**. No extension without a keeper line.
- Brief fixed 24 November 2026. Searches and reading from **25 November 2026**; **no reading after 15 December 2026**.
- **Record 0.1 by 18 December 2026,** as `studies/LH061/LH061.md`: a header (the question as its title, version, date, writer and model, the commit the figures were taken from, the reading period, instruments and versions, what it cites, overlap), In short, Answer (Part A and Part B, each in a few sentences, with the inconclusive conditions below applied), Findings (the Part A table of claims and the Part B table of reports, each claim with its class, setting, measure, population and window), Method, Limits, Next, Corrections; with `sources.md` (the source register: included, excluded with reason, candidates not read, named series not found), `claims.csv` (one row per claim: document, part, claim in a short paraphrase, class, setting, vendor, measure, population, window, origin), `searches.md`, `fetchlog.csv` and `derived/`. Then the evidence review, the reader-and-inference review and a recheck of what resolving them wrote, before anything reaches a surface. The result is a line on [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md) unless an article is earned.
- **Stopping:** when the eight searches are run and the twenty GETs are spent or both candidate lists are exhausted, or at the end of 15 December 2026, whichever comes first. The question, search rule, named series, inclusion rule, order and classes do not change after any search is run; a later change is a dated amendment, labelled post hoc if made after documents were read.

## What would leave it inconclusive

For each part separately:

- Fewer than three documents included: the record lists them and says the searches found too little to describe that part's evidence.
- No included claim classed measured outcome: the record reports what is self-reported, modelled or asserted, and says nothing was measured in the documents read (a result about those documents, not about the field).
- All measured claims in Part A rest on vendor samples, or all on laboratory settings: reported as such only.
- Part A's measured claims concern measures or outcomes too different to set side by side: each is reported alone.
- More than six of the twenty GETs meet walls or robots refusals, or two or more named series can't be read: the record says the readable set may be biased towards open publications.

It cannot say, in any case, whether any containment measure works in general or now, whether any organisation could recover from a real incident, why a measure did or didn't work beyond what its authors measured, or anything about containment of AI activity beyond what an included document reports.
