# LH062: In published measurements, how long do exposed credentials stay publicly exposed, and stay valid, unprompted and after notification?

**In short.** (Not part of the protocol.) When a password, key or token ends up somewhere public, how long does it stay there, and how long does it keep working? We'll look for published research that followed exposed credentials over time, with and without someone telling the owner, and set each study's figures side by side with what it counted, among whom and when, without adding them together. Two studies we already know of, from an earlier desk study, found most leaked secrets in one sample still up after 16 days, and exposed keys on websites halved two weeks after notification before creeping back (both the authors' findings, already seen). We'll run six fixed searches and read at most twelve documents between the commit of this brief and 14 December 2026; the record follows by 18 December.

| | |
|---|---|
| Version | Protocol 1.0, fixed 27 November 2026, before any search for this study was run and before any document other than the two LH061 had already read (A02 and A07, below) was read for it |
| Writer | A research subagent on Claude Opus 5.5 in Claude Code, for the Horizon run 2026-11-27T121200Z-anthropic-horizon. The writer made no web request and ran no search |
| Answers | proposals.md P-0053, "How long exposed credentials stay exposed, with and without notification", proposed by the reader-and-inference review of LH061 ([notes/R-0160.md](../../notes/R-0160.md), "Next step"), started by the fresh gate of 27 November 2026 under eight conditions that bind this brief (the gate's section "Conditions on P-0053 (started)"; cited below as gate condition 1 to 8) |
| Investigation | [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md), its defensive strand (item 8), under [the keeper's decision of 24 November 2026](../../notes/keeper/2026-11-24-defensive-side.md); a deepening, not urgent. Under that decision it needs no AI element of its own |
| Rows | LH062-search-read, LH062-record, LH062-record-evidence-review, LH062-record-reader-review, LH062-record-recheck, LH062-publish in schedule/due.csv. The driving session commits this brief and its rows before the first search (gate condition 1) |

## Question

**In published measurements, how long do exposed credentials stay publicly exposed, and stay valid, unprompted and after notification?** (gate condition 2, verbatim.)

Terms, fixed now:

- **Credential:** a secret that grants access to an account or service: a password, an API key, an access token, a private key, or a cloud or service account's secret, as a study defines its population.
- **Exposed:** reachable by anyone without authorisation in a public place a study names (for example a public code repository, a public website, a published package or app), as the study defines it. How credentials came to be exposed or how the study found them is not part of this question and is not recorded (see Never done).
- **Unprompted:** with no notification by the study's authors or at their request. Notices the owner may have had from elsewhere (for example a platform's own scanning) are recorded only where the study states them.
- **After notification:** after the study's authors, or a platform, provider or other party at their request, told the credential's owner or holder of the exposure.

The study says nothing about AI unless an included document does, and then only as that document's claim.

## What the writer already knows (prior knowledge, not readings of this study)

The writer read, before fixing this brief, LH061's [brief](../LH061/brief.md), [record](../LH061/LH061.md) version 0.3 (rechecked, not released), [sources.md](../LH061/sources.md) and [claims.csv](../LH061/claims.csv) entries for A02 and A07, the reader review [R-0160](../../notes/R-0160.md), the keeper's decision of 24 November 2026, the research safety assessment, P-0053 in proposals.md and the gate of 27 November 2026. The writer did not open LH061's searches.md, fetchlog.csv or derived files, so it has not seen the other titles LH061's searches returned.

**A02 and A07, as LH061 records them** (the authors' findings, read by LH061 on 25 November 2026; outcomes seen):

- **A02. Meli, McNiece and Reaves, "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories", NDSS 2019** (read by LH061 at https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf). Measure: the repository owner's removal of a leaked secret, not a provider's revocation. Population: secrets found through GitHub's Search API and monitored from 4 April 2018 (no total count in the section LH061 read; the 19 per cent "amounts of tens of thousands of secrets", per R-0158's reread). A02-1: about 6 per cent removed within an hour, over 12 per cent within a day and 19 per cent within 16 days; 81 per cent not removed (hourly for a day, then daily to 16 days). A02-2: no monitored repository whose owner removed a secret rewrote its history, so removed secrets stayed reachable. Both measured, field, not vendor. LH061 recorded A02's fit to containment as a judgement.
- **A07. Demir, Vekaria, Smaragdakis and Durumeric, "Keys on Doormats: Exposed API Credentials on the Web", arXiv 2603.12498 v3 of 14 September 2026** (the v3 text states ACM CCS 2026; CC BY 4.0; read by LH061 at https://arxiv.org/pdf/2603.12498). Population: 1,748 verified credentials for 14 providers in HTTP Archive's September 2025 crawl. A07-1: without intervention, exposed credentials stayed public an average of 12 months (1 to 60), with about 10 per cent fewer active in the first month (nine HTTP Archive snapshots to September 2025). A07-2: after notification, exposures fell 50 per cent in 14 days (1,405 to 706), still-valid credentials about 26 per cent (1,175 to 865), the two day-0 totals differing because, the authors say, three services blocked their address during verification. A07-3: by day 172, exposures not removed rose again to 1,019 while still-valid credentials fell further to 660. A07-4: revocation varied by provider (LH061 named the providers as the authors do; this study will not, see Never done). All measured, field, not vendor.

**LH061's other documents** (record 0.3): its Part A included five other documents (on domain takedowns, botnet takedowns, sinkholing, code-signing certificate revocation and a laboratory recovery test), none of them about exposed credentials' removal or revocation over time as defined here; its Part B, two exercise reports. LH061's sources.md lists the Cloud Security Alliance's note of October 2026 on leaked-credential survival as known but not located or read, and says the search tool's summaries named a secret-scanning vendor's credential survival figures, not opened. LH061's brief relayed, from scout 5 on 24 November 2026, TruffleHog's 2023 figures (74 per cent of leaked credentials still live at 31 days; revocation almost always within three days or never) and that the Cloud Security Alliance's note ties survival to whether the provider revokes automatically. These are relays, not readings; none is a document of this study unless the rules below admit it, and the TruffleHog figures are disclosed here as known.

**R-0160** found that LH061's measured share was largely built into its inclusion rule, which admitted only outcome studies and kept vendors as leads, and advised following one comparable outcome across studies rather than widening the census. **The gate** (27 November 2026) set the conditions this brief follows.

**The writer's expectation,** from general knowledge, not read for this brief: venue studies of exposed secrets mostly concern public code repositories, published packages, container images, mobile apps and websites; most report how many secrets they found, and fewer follow them over time; fewer still have a notification arm, and fewer again an unnotified comparison group, so an effect of notification will rarely be supported by design. Vendor reports are expected to give survival figures from the vendor's own scanning with little stated method. The writer knows from general knowledge that some platforms forward certain exposed tokens to their issuers for automatic revocation, which can make "unprompted" mixed in some populations.

## Population and unit

- **Population:** published measurements, in the venues below, of credentials exposed in a public place, followed over time for removal or revocation.
- **Unit of synthesis:** a **claim about an outcome** (still exposed, or still valid) for a stated population at a stated time or over a stated duration, from one included document. Each claim keeps the study's own **unit of count** (for example a credential, a distinct secret, a file, a repository, a website or domain, an app or a package), recorded beside it. Units are never converted into one another.

## Search rule (fixed now; gate condition 2)

**Tool.** The WebSearch tool of the Claude Code harness running the study, one call per query, no other search engine, catalogue or scholarly API. A search result is a lead, never a source: titles, venues, years and URLs are used only to screen candidates; snippets are not retained.

**Queries,** exactly six, run once each, verbatim, in this order:

- **Q1:** `exposed credentials removal revocation longitudinal measurement study`
- **Q2:** `leaked secrets public repositories how long remain valid measurement`
- **Q3:** `exposed API keys notification revocation measurement study`
- **Q4:** `leaked credentials disclosure notification remediation response rate study`
- **Q5:** `hardcoded secrets still valid over time measurement study`
- **Q6:** `NDSS USENIX Security CCS IMC leaked secrets revocation after notification`

No query is reworded, added or rerun. A query that errors is recorded as failed and not replaced.

**Year range.** Published from 1 January 2015 to 14 December 2026 inclusive (for a preprint, the date of the version read).

**Two streams, kept apart (gate condition 2).**

- **Venue stream.** A candidate must be a paper at the Network and Distributed System Security Symposium (NDSS), the USENIX Security Symposium, the IEEE Symposium on Security and Privacy, the ACM Conference on Computer and Communications Security (CCS) or the ACM Internet Measurement Conference (IMC), or a preprint on arXiv in cs.CR. An arXiv preprint qualifies when the search metadata or the PDF shows cs.CR, or when its text states acceptance at one of the five conferences; where neither shows, it is excluded as outside the venues, with that reason recorded. A preprint and its published version are one candidate, read once.
- **Vendor stream.** A candidate is a document published on its own site by a company that sells security, secret-scanning or credential-management products or services, presenting its own measurement (a report, research page or study post). Vendor documents are classed vendor, tabulated in their own table, and never set in the same table as the venue stream or counted with it.
- **Neither.** News, secondary coverage, industry bodies' notes (including the Cloud Security Alliance's), other journals and conferences, theses and anything else are locators only: they may name a document that belongs to a stream, which then becomes a candidate, but they never count as documents. No locator page is fetched.

**Known documents.** A02 and A07 enter the venue stream's candidate list whether or not a query returns them, and meet exactly the same inclusion rule as any other: neither is included or excluded for being known. If included, each is disclosed in the record as a known case whose outcomes were seen before this brief (gate condition 1). No other document enters for being known: TruffleHog's 2023 figures and any other vendor document enter only if a query returns them.

## Screening, inclusion and exclusion (fixed now)

**Screen, on search metadata.** A result becomes a candidate if it belongs to a stream, falls in the year range, and its title or URL plausibly concerns exposed credentials followed over time. Titles that show the contribution is a way of finding, extracting or exploiting credentials, with no sign of a follow-up over time, are excluded unread, with the reason recorded.

**Inclusion, decided only on the document read (gate condition 2).** A document is included if it meets all three:

1. it **measures removal or revocation over time**: whether exposed credentials stay publicly exposed, or stay valid as the authors checked it, at two or more points after the authors' first observation, or as a duration, unprompted or after notification;
2. **for a stated population**: what was exposed, where, and how many (a count, or a stated frame where the count is not given, recorded as not stated);
3. **with a stated method**: how exposure and validity were established, at the document's own level of generality, and the observation period.

Every document read that meets all three is included, in its stream.

**Exclusion, with the reason recorded:** fails any condition; counts exposed credentials at one time only; measures attackers' use of planted or leaked credentials (time to abuse) rather than removal or revocation; measures patching or another outcome of a notification that is not removal or revocation of the credential; its contribution is a technique for finding, extracting, validating or exploiting credentials (if found on reading, nothing from it is recorded beyond the exclusion reason); outside the streams or years; a duplicate; or full text unavailable (a wall, refusal or error), in which case it is **unread**.

## Order of reading and ceiling (gate condition 4)

- At most **six searches** and at most **twelve documents**, each read by **one gated one-off GET** of its full text; no locator reads. The venue stream has up to **nine** of the twelve GETs and the vendor stream up to **three**; when one stream's candidate list is exhausted, its unused GETs pass to the other.
- For arXiv the full text is the PDF at `https://arxiv.org/pdf/<id>`; abstract pages are not fetched separately. A02 and A07 are read afresh at the URLs LH061 used, each by one GET counted against the twelve; the record compares each SHA-256 with LH061's derived file and says whether the bytes matched. LH061's derived files are not used as readings.
- One retry is allowed only on a timeout, a connection error or HTTP 500, 502 or 504, inside the same document. A GET that meets a challenge, login, registration form, rate limit or any non-200 answer counts against the twelve and is recorded as a wall; it is not got around, and no mirror, archive or third-party copy is fetched instead. A URL the robots gate refuses before any request is recorded as unavailable and uses no GET.
- **If more candidates than GETs,** each stream reads in this order until its GETs are spent or its list is exhausted:
  - **Venue stream:** (1) papers at the five conferences, then arXiv preprints not stated as accepted at one; (2) within a tier, most recent publication year first; (3) ties by first appearance in the results, Q1's first result before Q1's second and so on through Q6; known documents not returned by any query follow, A02 then A07.
  - **Vendor stream:** most recent first; ties by first appearance in the results.
- Candidates left unread are listed in the record by title, venue and year as "candidate, not read", with their number; nothing is claimed from them. A document read and then excluded still used its GET.
- About **$15 at list rates before reviews**; at most one collection subagent; no paid service, account or key. **No extension without a keeper line.**

## How fetches are made and what is kept

- Every fetch goes through `scripts/lh_fetch.py` with `access='oneoff'` ([the keeper's decision of 21 November 2026](../../notes/keeper/2026-11-21-robots-intent.md)), the robots gate applied before the request and before any redirect (`check_redirects=True`), with `LIGHTHOUSE_PROVIDER=anthropic` (or the provider actually running the session).
- A body is kept only through `save_body`, and only where `keep_decision` allows it, the document states a licence allowing redistribution, and the body shows no credential value, even in part, and no repository, host or account identifier. PDF bodies are not kept in any case, since LH061 found email addresses in compressed streams that the redaction can't reach. Where no body is kept, `write_derived` keeps the URL, read time, status, SHA-256 of the bytes received, the facts used and short attributed quotations, with the reason logged.
- Every request, including failures, walls and robots refusals, goes in `studies/LH062/fetchlog.csv`; every search goes in `studies/LH062/searches.md` with its UTC time, the query verbatim, and each result's title, URL, venue and year as shown, marked opened or not. Emails are withheld (`redact_bytes`; `python3 -I scripts/redact_emails.py studies/LH062` before any commit).
- PDFs are read as text extracted in memory. No code from any download is run, and no dataset, appendix archive, artefact or tool a document links to is fetched.

## Events and clocks (fixed now; gate condition 2)

- **First observation (t0):** the time or snapshot at which the authors first observed a credential exposed. Durations and shares "unprompted" are read from t0. **Exposure onset** (when the credential first became public, for example a commit or publication date) is recorded only where a study states it and how it dated it, labelled "onset as the study states it", and never substituted for t0.
- **Notification date (tN):** the date or dates the authors, or a party at their request, sent notices, as the study states them; outcomes "after notification" are read from tN. Where notices went out over a period, the period is recorded; where no date is given, tN is **not stated** and the claim records the study's own reference point (for example "day 14 after disclosure").
- **Who notified,** recorded at the study's own level of generality (authors, a platform, a provider), never by named provider.
- **Observation points:** the times at which the outcome was checked (for example hourly for a day, daily to day 16, snapshot by snapshot), and the end of the window.

## Outcomes (fixed now)

- **Still exposed:** the count or share of the population still publicly reachable at a stated time after t0 or tN, or the duration of exposure, as the authors measured it. Where a study reports that a credential removed from the current view stayed reachable elsewhere in the same public place (for example in a repository's history), that is recorded as the authors report it, as still exposed in their terms.
- **Still valid as the authors checked it:** the count or share still valid at a stated time, or a duration of validity, recorded with only the fact that the authors state they checked validity and when; how they checked is not recorded.
- Each outcome is recorded with: unprompted or after notification; t0 or tN as the clock; unit of count; population (what, where, how many); window and observation points; design (below); data public or not; and the authors' interest or funder where stated.
- **Design,** for claims after notification: randomised notified and unnotified groups; a non-randomised unnotified comparison; before and after only; or none stated.

## Classification of each claim (fixed now)

Each claim is classed once:

- **measured:** counted or timed by the authors from their own observation, recorded with what was measured, on what population, over what period;
- **self-reported:** from owners' or operators' answers (a survey, replies to notices, interviews);
- **modelled:** an estimate from a model (for example a survival model, regression or extrapolation), with what it controls for;
- **asserted:** stated without data shown in the document.

Beside the class: **stream** (venue or vendor); **vendor label** for venue-stream claims, under the rule LH061 stated in its record 0.3 (Method, "The vendor rule"), fixed here before any reading: a claim is vendor when the observations it counts come in whole or in part from data a company collects and holds for itself or sells (customer or product telemetry, a sample repository, a commercial or internal database); data a company publishes openly don't make a claim vendor; authors' employment is recorded as an interest, not used for the label. Every vendor-stream claim is vendor. **Setting:** field, or laboratory. A claim relayed from another document is classed by its origin and linked to it; two documents resting on the same dataset count as one origin.

## The comparison that would matter (gate condition 2)

Each included study's claims are reported **side by side** in one table per stream, one row per claim, with its unit of count, population, window and observation points, clock (t0 or tN), unprompted or after notification, design, class and vendor label. The comparison that would matter is between rows that share a unit of count and an outcome: for each such group, what share was still exposed, or still valid, at comparable points after t0, and after tN, in each population and window. **Nothing is pooled across units, and no figure is combined, averaged or ranked across studies.** Agreement or disagreement is a description of what the studies report, not a test. A difference between unprompted and after-notification figures is an effect of notification only where a study's own design supports it (randomised or with an unnotified comparison), and then in the authors' terms; otherwise it is reported as "after notification, X", with no effect language (gate condition 5). The vendor table is never compared row for row with the venue table; the record says only what each shows.

## Missing evidence

- A document not read (wall, refusal, error, or beyond the ceiling) is **unread**, never evidence that no such study exists.
- A stream with no included document is reported as "none found in six searches and the documents read", never as an absence in the literature.
- An outcome a study doesn't measure (for example validity) is **not measured by that study**, not a zero.
- A field a document doesn't report (population count, t0, tN, design, data availability) is **not stated**.
- A population or place the searches didn't surface is **not found by this search**.

## Overlap with earlier studies (gate condition 7)

- **LH061** ([record](../LH061/LH061.md), version 0.3): A02 and A07 are shared. If included here, they are read afresh under this brief, but their outcomes were seen first, and this study gives **no independent confirmation** of LH061's readings of them; the record says so beside each. This brief records no per-provider figure, so A07-4's content is not carried over.
- **LH051** (a CI secret stealer's traces and their cleanup in GH Archive) and **LH055** (ARTEX: accounts of credentials harvested for compute): **description only**. The record may say in a sentence how their questions relate; no data, figure or finding of theirs is joined to this study's, and none of their records is re-read.
- **P-0028** (agents' working files in public repositories, waiting for the keeper) is untouched: no count of such files, and nothing read for it.
- The scouts' and LH061's relays are prior knowledge, not readings. Nothing is pooled across studies.

## Voice (gate condition 5)

Findings are the authors', attributed with their class, unit, population and window. Lighthouse never says in its own voice that containment works or fails. Durations are descriptions. An effect of notification is reported only as the authors' design supports it. No owner, operator, provider or platform is called weak, slow or negligent by Lighthouse. Lighthouse makes no claim that harm is happening now or that any named system is compromised.

## Never done (gate condition 3)

- No per-provider or per-platform breakdown or ranking of removal or revocation is made, recorded or quoted, even where a study gives one; only study-level figures for the whole population, or for groups the study defines without naming providers or platforms, are kept ([the keeper's decision of 24 November 2026](../../notes/keeper/2026-11-24-defensive-side.md): no "which systems are weak").
- No catalogue of why credentials stay exposed or valid, or of how they are found, is made or kept: where a document gives reasons, the record says only that the authors give reasons, without restating them, and reasons are never tallied across documents.
- No secret, credential, repository, host, account or domain is looked up, fetched, resolved or tested, and none a document shows is copied into any file.
- No leaked-secret dataset, appendix, artefact or tool is downloaded, even where a document links one.
- Nobody and nothing a study anonymised is re-identified, by name or by the shape of its description.
- Nobody is contacted: no author, owner, provider or platform.
- No paywall, registration form, robots refusal or rate limit is got around.

## Model and interest disclosure (gate condition 6)

Lighthouse runs on Anthropic's models, and this brief was written on Claude Opus 5.5; Lighthouse sometimes runs under OpenAI's Codex. AI providers' API keys, possibly Anthropic's and OpenAI's, may be among the credentials the studies follow; any such figure is kept at the study's level only, under the per-provider rule above, and the record says beside a claim when a study names AI providers' keys among its population. GitHub's secret scanning (GitHub is Microsoft's) may feature as a platform or a notifier; it is recorded at the study's own level of generality. Reviewers look for wording easier or harder on any AI developer or platform than the sources allow.

## Research safety (gate condition 8)

Assessed when the brief was fixed, 27 November 2026, under [schedule/research-safety.md](../../schedule/research-safety.md): **proceed, narrowed** to published aggregate durations and shares. Why: reading how long exposed credentials stay exposed or valid, as study-level figures, adds little to anyone's ability to cause harm; the material risks would be pointing at where credentials can be found, at which providers or platforms revoke slowly, or at how to find or test them, and the rules above close each of those off (no locations, no identifiers, no per-provider figures, no catalogue of reasons or methods, no datasets, no tests). The check is repeated if a document read contains credential values, repository, host or account identifiers, per-provider weakness or finding or testing detail: such material is not kept, quoted or passed on, and the affected work stops as the assessment says.

## Dates, stopping and the stop gate (gate condition 4)

- **Brief fixed 27 November 2026** (the gate asked for it by 4 December). Searches and reading **not before this brief and its rows are committed**; **no reading after 14 December 2026**.
- The reading window is just over two weeks, but the read is one pass and the record is due four days after it closes, so no interim checkpoint is scheduled; if reading is not finished by 11 December, the read row's note says what remains.
- **Stopping:** when the six searches are run and the twelve GETs are spent or both candidate lists are exhausted, or at the end of 14 December 2026, whichever comes first. The question, search rule, streams, inclusion rule, order, events, outcomes and classes do not change after any search is run; a later change is a dated amendment, labelled post hoc if made after documents were read.
- **Stop gate, checked by the LH062-record row by 18 December 2026:** searches.md holds six query entries (or failures), and fetchlog.csv shows either twelve document GETs (walls included) or every candidate in the register read, unavailable or excluded unread, and no fetchlog row is dated after 14 December 2026. If it fails because reading is incomplete, the record is written from what was read, says so, and lists the rest as candidates not read; no reading is added after 14 December.
- **Record 0.1 by 18 December 2026** (a deadline, not a start date), as `studies/LH062/LH062.md`: a header (the question as its title, version, date, writer and model, the commit the figures were taken from, the reading period, instruments and versions, what it cites, overlap), In short, Answer, Findings (the venue table and the vendor table, each claim with the fields above), Method, Limits, Next, Corrections; with `sources.md` (included, excluded with reason, candidates not read), `claims.csv`, `searches.md`, `fetchlog.csv` and `derived/`. Any tally is kept as code and output.
- Then an **evidence review**, a **reader-and-inference review**, and a **recheck** by one fresh agent of what resolving them wrote, before anything reaches a surface. The result is **a line on the investigation page** unless an article is earned.

## What would leave it inconclusive

- Fewer than two included documents in the venue stream: the record lists them and says the searches found too little to set studies side by side.
- No two included claims share a unit of count and an outcome: each is reported alone, and no comparison is drawn.
- No included study has an after-notification arm: the record says nothing about notification beyond that.
- No included study checks validity: "still valid" is unanswered, and the record says so.
- No included after-notification claim rests on a randomised or unnotified-comparison design: no effect of notification can be stated, only descriptions.
- All measured claims are vendor: reported as such only.
- More than four of the twelve GETs meet walls or robots refusals: the record says the readable set may lean towards openly published documents.

It cannot say, in any case, whether containment works in general or now, why credentials stay exposed or valid, how any provider or platform compares with another, or whether any named system is compromised.
