# LH060: What do published studies that measure deployment of available security fixes or features by operator size or capacity find, and on what data?

**In short** (added 24 November 2026; not part of the protocol). A fix being released isn't the same as a fix being installed, and people often say small operators are the ones who fall behind. We'll find out what published research has actually measured about that: a fixed set of six searches, at most fifteen documents read, and each claim sorted by whether the authors measured it, asked operators, modelled it or simply asserted it. Alongside, we'll look only at the column names of data Lighthouse already holds from its PHP and WordPress studies, to see whether anything in them could stand in for an operator's size. Nothing has been read yet beyond the summaries a sweep relayed; reading runs from 25 November to 11 December and the record follows by 15 December.

**Protocol 0.1, fixed 24 November 2026, before any study beyond the abstracts and summaries scout 5 relayed was read, and before any search for this study was run.** Writer: a research subagent in Claude Code (Claude Opus 5.5, Anthropic) for the Horizon run 2026-11-24T121300Z-anthropic-horizon, from proposals.md P-0047 (a keeper direction of 23 November 2026), which the fresh gate of that sweep started as a deepening of [Where software updates go](../../investigations/software-updates.md), not urgent, under nine conditions that bind this brief ([the gate](../../notes/horizon/2026-11-24T1213Z.md), "Conditions on P-0047 (started)"). The writer made no web request of any kind. The driving session commits this brief and its schedule rows ([rows.csv](rows.csv)) before the first search.

## Question

**What do published studies that measure deployment of available security fixes or features by operator size or capacity find, and on what data?** (gate condition 2, verbatim.)

Terms, fixed now:

- **Operator:** an organisation that runs internet-facing software or services for itself or others: a hosting provider, a network, a company, a public body, a site owner acting as an organisation. Individual consumers and their personal devices are not operators here.
- **Available security fix or feature:** a patch, fixed release or configuration that was published and obtainable at the time measured (a software update, a fixed version, or a security feature such as a protocol or setting the operator could enable).
- **Deployment or remediation outcome:** whether, how far or how fast operators applied it, as a count, share or time.
- **Breakdown by size, capacity or type:** results reported separately (or modelled) by a measure of operator size (customers, hosts, sites, staff, revenue, address space), capacity (staff, budget, security function, stated resources) or type (for example shared hosting against managed hosting, sector, ownership).

The second part of the proposal's narrow question, whether a public aggregate already held lets Lighthouse see size in its own uptake series, is answered only by the structure-only check below, never by reading values.

The study says nothing about AI unless an included document does, and then only as that document's claim.

## What the writer already knows

All of this is prior knowledge, read before the brief, and none of it is a reading in this study.

- **Scout 5's Part B** ([scout-5-research.md](../../notes/horizon/2026-11-24T1213Z/scout-5-research.md), read 24 November 2026; abstracts and summaries as the scout relayed them, not the documents): Stivala and others, IEEE S&P 2026, arXiv 2512.01891, on 24 hosting providers, incentives and where responsibility sits, qualitative, no public data stated; Tajalizadehkhoob and others, "Herding Vulnerable Cats", arXiv 1708.06693, on 1,259 hosting providers, patching factors against abuse with provider size controlled, patching factors explaining 10 to 19 per cent of abuse variance as relayed, data not stated; Kenna Security and Cyentia Institute, "Prioritization to Prediction" volume 3, a vendor sample of about 300 organisations as relayed, with a by-size result that smaller firms fix faster, data not public; Dissanayake and others, arXiv 2012.00544 and 2202.09016 (snippets only), a systematic review and a healthcare field study, coordination named the leading cause of delay; notification campaigns at USENIX Security 2016 and NDSS 2018 (snippets only), on whether notifications lead to patching; the Verizon Data Breach Investigations Report 2025 through secondary coverage, 54 per cent of edge-device flaws fully remediated with a median of 32 days, no breakdown by size found. The scout found no public dataset of patch timing by operator size; the gate notes that this is a thin search's absence.
- **L-0191** (proposals.md): a Gentoo developer (27 October, on Hacker News 23 November) says vulnerability reports from chatbot users arrive "at unprecedented rates" and force needless security updates; no figures. Context only; not a document of this study.
- **L-0192** (proposals.md): OpenAI and Cisco released, on 23 November, a runtime that shields Linux systems that can't yet be patched. Prior knowledge only; not fetched, and as a product announcement it fails the venue rule below.
- **Lighthouse's own uptake outcomes.** The writer has seen LH033's outcomes (Censys counted 75.0 to 92.2 per cent of each fixed PHP branch's services patched on day 30, nearly all by day 14, as AGENTS.md summarises record 1.2) and LH039's (W3Techs's survey read as a lagged view of WordPress sites that can't say how fast they moved, record 1.2). The writer has read the investigation page's question and LH033's and LH039's briefs, whose descriptions of the fields kept (Censys's branch, status and target counts; W3Techs's version rows; Packagist's per-version downloads) make a size proxy unlikely, as the gate also says. None of those outcomes enters this study, and no reading here splits them.
- **The writer's expectation**, from general knowledge, not read for this brief: few published studies report a deployment outcome broken down by operator size; more report it by type of operator or software; and vendor reports, where they give size, rest on their own customers.

## Search rule (fixed now)

**Tool.** The WebSearch tool of the Claude Code harness running the study, one call per query, no other search engine, catalogue or scholarly API. A search result is a lead, never a source: titles, venues, years and snippets are used only to screen candidates.

**Queries,** exactly six, run once each, verbatim, in this order:

- **Q1:** `hosting providers patch deployment provider size measurement study`
- **Q2:** `vulnerability remediation time by organization size empirical study`
- **Q3:** `security feature adoption small organizations versus large measurement`
- **Q4:** `vulnerability notification campaign remediation rate by operator type`
- **Q5:** `patch management barriers small organizations capacity survey`
- **Q6:** `vulnerability remediation by company size report Cyentia OR Kenna OR "Data Breach Investigations Report"`

No query is reworded, added or rerun. A query that errors is recorded as failed and not replaced.

**Venues.** A candidate must come from one of these:

- peer-reviewed conferences: IEEE Symposium on Security and Privacy, IEEE EuroS&P, USENIX Security Symposium, ACM CCS, NDSS, ACM Internet Measurement Conference, Passive and Active Measurement (PAM), the Workshop on the Economics of Information Security (WEIS), SOUPS, APWG eCrime, ACM CHI;
- peer-reviewed journals: Computers & Security, IEEE Transactions on Dependable and Secure Computing, ACM Transactions on Privacy and Security, ACM Computing Surveys, Journal of Cybersecurity, Empirical Software Engineering, Information and Software Technology;
- preprints on arXiv;
- reports: the Verizon Data Breach Investigations Report, the Cyentia Institute (its Kenna Security "Prioritization to Prediction" series included), ENISA, the UK's NCSC, and CISA.

News, blogs, vendor marketing pages and secondary coverage are locators only: they may name a document in a listed venue, which then enters the candidate list, but they never count as documents.

**Year range.** Published from 1 January 2012 to 11 December 2026 inclusive.

**Known documents.** The documents named in scout 5's Part B that fall in the listed venues (Stivala and others; Tajalizadehkhoob and others; Prioritization to Prediction volume 3; Dissanayake and others' two; the USENIX Security 2016 and NDSS 2018 notification studies; the Verizon DBIR 2025) enter the candidate list whether or not a query returns them, and meet exactly the same inclusion rule as any other (gate condition 2): none is included or excluded for being known.

## Inclusion and exclusion (fixed now)

**Screen, on search metadata.** A result becomes a candidate if it is in a listed venue, in the year range, and its title or snippet plausibly concerns operators' deployment or remediation of security fixes or features. A preprint and its published version are one candidate.

**Inclusion, decided only on the document read.** A document is included if it meets all three:

1. it measures (or reports a measurement of) a deployment or remediation outcome of an available security fix or feature by operators;
2. it reports a breakdown of that outcome by operator size, capacity or type, as defined above;
3. it states its method: population, how the outcome was obtained, and the period.

Every document read that meets all three is included (gate condition 2).

**Exclusion, with the reason recorded:** fails any of the three; its unit is a software project, package or repository rather than an operator (dependency updates in code are other studies' question); its population is consumers or personal devices; it is outside the venues or years; it is a duplicate of a document already read; or its full text is unavailable (a wall, refusal or error). Excluded documents stay in the source register with their reason. A document that explains non-deployment without measuring an outcome (for example interviews alone) is excluded as a document but may be cited as context in the record, labelled so, with nothing from it counted.

## Ceiling and order of reading (fixed now)

At most **six searches** and at most **fifteen documents**, each read by one gated one-off GET of its full text (gate condition 5). The abstract page is not fetched separately; for arXiv the full text is the PDF at `https://arxiv.org/pdf/<id>`. One retry is allowed only on a timeout, a connection error or HTTP 500, 502 or 504, inside the same document. A GET that meets a challenge, login, registration form, rate limit or any non-200 answer counts against the fifteen and is recorded as a wall; it is not got around, and no third-party copy is fetched instead. A URL the robots gate refuses before any request is made is recorded as unavailable and does not use a GET.

**If more candidates than fifteen GETs:** candidates are read in this order, fixed now, until the GETs are spent or the list is exhausted:

1. by tier, as the search metadata gives the venue: peer-reviewed conference or journal first, then reports from the listed publishers, then arXiv preprints not stated as published;
2. within a tier, most recent publication year first;
3. ties by order of first appearance in the results, Q1's first result before Q1's second and so on through Q6; known documents not returned by any query follow, in the order listed above.

Candidates left unread are listed in the record by title, venue and year as "candidate, not read"; nothing is claimed from them, and the record says how many there were. A document read and then excluded still used its GET.

## How fetches are made and what is kept

- Every fetch goes through `scripts/lh_fetch.py` with `access='oneoff'` (the keeper's decision of 21 November 2026), the robots gate applied before the request and before any redirect, with `LIGHTHOUSE_PROVIDER=anthropic` (or the provider actually running the session).
- A body is kept only through `save_body`, which applies the robots and page-reservation rule in one place, and only where the document also states a licence that allows redistribution (for example CC BY); otherwise no body is kept and `write_derived` keeps the URL, read time, status, sha256 of the bytes received, the facts used and short attributed quotations. Emails are withheld (`redact_bytes`; `python3 -I scripts/redact_emails.py studies/LH060` before any commit).
- Every request, including failures and robots refusals, goes in `studies/LH060/fetchlog.csv`; every search goes in `studies/LH060/searches.md` with its UTC time, the query verbatim, and each result's title, URL, venue and year as shown, marked opened or not. Snippets are not retained.
- PDFs are read as text extracted in memory; no code from any download is run, and no dataset, appendix archive or artefact a document links to is fetched.

## Classification of each claim

The unit of synthesis is a **claim about deployment or remediation broken down by size, capacity or type**. For each included document the source register records: venue and whether peer reviewed; publication date; population and unit; the size, capacity or type measure used; the outcome; the observation window; whether the data are public; and the funder or publisher's interest where stated. Each claim is then classed:

- **measured:** the outcome was counted by the authors from observation (scans, logs, telemetry, version data);
- **self-reported:** the outcome or its reason comes from operators' own answers (survey, interview);
- **modelled:** an estimate inferred from a model (regression, simulation, extrapolation), with what it controls for;
- **asserted:** stated without data shown in the document.

A claim resting on a vendor's own customers or product telemetry is also labelled **vendor**. A claim a document relays from another is classed by its origin and linked to it; two documents resting on the same dataset count as one origin.

## The comparison that matters

Across included claims, the direction each reports (larger operators deploy more or faster, less or slower, no difference, mixed), tabulated with its class, its size measure, its population and its window. The unit is the claim; documents are not pooled and no figure is combined across documents. Agreement or disagreement is a description of what the literature reports, not a test, and a difference by size is never read as size causing it (gate condition 6). The record reports separately how many claims of each class there are, and how many rest on public data.

## The structure-only check of retained data (gate condition 3)

A script written then, `studies/LH060/scripts/structure.py`, run with `python3 -I`, prints for each file named below only: for JSON, the key paths (list positions collapsed to `[*]`) and value types; for CSV, the header row; for any key that is itself data (a date, version or label used as a key), the key with every digit replaced by `#`. It never prints a value, and its output is kept as `studies/LH060/structure.txt`. For the reads named, it also prints whether every other read's file of the same name has the same key paths (same or different, no values).

- **LH033** (studies/LH033/data/): `read-2026-11-21T1414Z/censys.raw.gz` (Censys ARC's dashboard JSON, decompressed in memory), `read-2026-11-21T1414Z/tables.json`, `read-2026-11-21T1414Z/read_log.json`, `read-2026-11-21T1414Z/w3techs-details-8.3.derived.json`, `read-2026-11-21T1414Z/w3techs-history_details-8.3.derived.json`, `read-2026-10-25T0855Z/packagist.json`, `record_v1.json`, `python_side.json`.
- **LH039** (studies/LH039/): `data/raw-2026-11-21T1411Z/w3-71.derived.json`, `w3h-71.derived.json`, `cand-3.derived.json` and `readlog.csv`; one `roots-*.json` and one `johnpbloch-*.json` file and `readlog.csv` in `data/packagist-2026-11-21T1415Z/`; `data/oneoff-2026-11-22T1514Z/archive.facts.json`, `feed.facts.json` and `readlog.csv`; and the header rows of `record-1.0-packagist.csv` and `checkpoints/2026-11-21-packagist.csv`.
- **Not opened:** `.body` files (page bodies or Lighthouse's notes of a refusal), the php.net release pages (`phpnet-releases-*.raw.gz`), scripts' outputs other than the CSV headers named, and anything in git history.

**What counts as a candidate size field:** a key, column or field label naming an operator, organisation, autonomous system or network, hosting provider, customer, site rank or traffic tier, managed or self-hosted class, cloud or on-premises class, or the number of sites or services per operator. Country, branch and version labels are not size proxies.

**What follows.** If none exists, the record says so for the files named. If one exists, the record names the file and label only and writes a proposal to proposals.md for a study on data not yet read (future reads under a fixed brief); no split of data already seen is made (gate condition 3). Any reading of values made anyway is labelled post hoc in the record with its number of comparisons, and enters no finding.

## Missing evidence

- A document not read (wall, refusal, error, or beyond the ceiling) is **unread**, never evidence that no such study exists.
- No included document reporting a breakdown by size is reported as "none found in six searches and fifteen documents", never as an absence in the literature.
- A field a document doesn't report (population, window, data availability) is **not stated**.
- A file the structure check can't parse is **unavailable**, with the error, not "no proxy".

## Overlap with earlier studies

LH033 (PHP, Censys and W3Techs), LH034 (Node.js, W3Techs and others), LH039 (WordPress, W3Techs and Packagist) and proposal P-0045 (the WordPress baseline) measure how far fixes went; this study asks what the published literature says about why or for whom, and reads their retained files' structure only. No data are pooled, nothing is counted twice, and no outcome of theirs is re-read or split (gate condition 8). No other Lighthouse study reads this literature; the sweep's relayed summaries are prior knowledge, not readings. P-0046 and P-0048, waiting for the keeper, would use the same four classes on other questions; no document read here counts there without its own brief.

## Voice

Findings are the authors', attributed with their class, population and window. "Time-to-release is not time-to-protection" is the proposal's framing, not a finding of this study. No causal claim about size is made in Lighthouse's voice (gate condition 6). No operator is called weak, slow or negligent by Lighthouse, and none is named in such a characterisation even where a source names it.

## Never done

- No host is enumerated, scanned, resolved or looked up; no host-level data are joined to operators; no Censys or Shodan query of any kind (gate condition 4).
- No operator is named as weak; nobody a source anonymised is re-identified, by name or by the shape of their description, Stivala and others' interviewed providers included.
- No dataset, host list, notification target list or artefact linked from a document is fetched.
- Nobody is contacted: no author, publisher or operator.
- No body is kept except as above; no paywall, registration form or rate limit is got around.

## Model and interest disclosure (gate condition 7)

Lighthouse runs on Anthropic's models; this brief was written on Claude Opus 5.5. L-0192's runtime is OpenAI's (with Cisco), and Lighthouse sometimes runs under OpenAI's Codex. L-0191 concerns chatbot-written vulnerability reports, a category that includes reports written with Anthropic's models. Neither touches a figure here; reviewers look for wording easier or harder on any AI developer than the sources allow.

## Research safety

Assessed when the brief was fixed, under [schedule/research-safety.md](../../schedule/research-safety.md): **proceed, narrowed** to published aggregates and the structure of retained data (gate condition 9). Reading published studies of deployment by operator size adds little to anyone's ability to cause harm; the material risk would be pointing at who is unpatched. That is closed off by the rules above: no host or operator lists, no datasets, no joins, no naming of operators as weak, no re-identification, no mechanism of any flaw described. The check is repeated if a document read contains host lists, named poorly patched operators or exploit detail; such material is not kept, quoted or passed on, and the affected work stops as the assessment says.

## Resource ceiling, dates and stopping

- Six searches, fifteen documents, one gated one-off GET each as above; at most one reading subagent; no paid service, account or key. About **$15 at list rates before reviews** (gate condition 5). No extension without a keeper line.
- Brief fixed 24 November 2026 (by 1 December, as the gate requires). Searches and reading from **25 November**; **no reading after 11 December 2026**. The structure-only check any day from 25 November to 11 December.
- **Record 0.1 by 15 December 2026** (header, In short, Answer, Findings, Method, Limits, Next, Corrections; the source register and searches as files), then the evidence review, the reader-and-inference review and a recheck of what resolving them wrote, before anything reaches a surface. The result is a line on the investigation page unless an article is earned.
- **Stopping:** when the six searches are run and fifteen GETs are spent or the candidate list is exhausted, or at the end of 11 December, whichever comes first. The question, search rule, inclusion rule, order and classes do not change after any search is run; a later change is a dated amendment, labelled post hoc if made after documents were read.

## What would leave it inconclusive

- Fewer than three documents included: the record lists them and says the six searches found too little to describe the literature.
- No included claim classed measured: the record reports what is self-reported, modelled or asserted, and says nothing has been measured in the documents read.
- All measured claims rest on vendor samples: reported as vendor findings only.
- Included documents use size measures too different to set side by side: each is reported alone.
- More than five of the fifteen GETs meet walls: the record says the readable set may be biased towards open publications.

It cannot say, in any case, how fast any particular operator or class of operator deploys fixes now, why, or whether size causes it; nor whether Lighthouse's own uptake series would differ by size, beyond whether a field exists that could one day be read.
