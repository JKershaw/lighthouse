# LH058: For each of November's eight outages, what cause has its operator stated in its own public report, and who has claimed a link to patching for model-found flaws, on what evidence?

**In short** (added 20 November 2026; not part of the protocol). Between 12 and 17 November 2026 eight large services went down, from Microsoft 365 and the FAA's air traffic systems to JPMorgan Chase and the NSA's classified network. A newspaper's unnamed sources, and then two members of Congress, have tied the week to the pressure of patching flaws that AI models find; the causes operators have given on record so far, as the press relays them, name no AI link, and some outages have no stated cause at all. We'll keep a dated ledger: for each outage, the cause its operator states in its own public report as those reports land, and beside it every public claim of an AI link, by who made it and on what evidence. We read weekly from 23 November to 1 January 2027 and write the record by 8 January; a report that names no cause is never read as a denial.

**Protocol 0.1, fixed 20 November 2026, before any operator's final post-incident report, the hearing record or any letter from a member of Congress was read by this study, and before any operator's own report for these outages was read by any Lighthouse study, as far as the writer knows** (the Microsoft report watch has retained no Microsoft-authored report as of its reading of 19 November; its reading of 20 November was not read for this brief). Writer: a research subagent in Claude Code (Claude Opus 5.5, Anthropic), from proposal P-0043 in [proposals.md](../../proposals.md), which the gate of 20 November sent to the keeper ([notes/horizon/2026-11-20T1214Z.md](../../notes/horizon/2026-11-20T1214Z.md), "Gate", the paragraph "If the keeper agrees P-0043", whose minimum binds this brief) and which the keeper approved the same day ("I approve of P-0043", 12:55 UTC). One page was read before this brief, under the robots gate, to fix the outage list: the Cloud Security Alliance's research note of 18 November ([fetchlog.csv](fetchlog.csv), 12:57:56 UTC; no body kept in the repository). Nothing else was fetched.

## Question

For each outage in the fixed list below, from public documents only:

1. What cause has its operator stated in its own public report or statement, in which document, of what kind (final post-incident report, preliminary or interim report, short statement), and on what date; and does the operator's own text say that the triggering change was a security fix, that the flaw fixed was found by an AI model, or anything else about AI?
2. Who has publicly claimed a link between that outage (or the cluster as a whole) and patching for flaws found by AI models; in what route (hearing record, letter, official statement, press quoting a named or unnamed person); how strong a link (caused, contributed, could cause, pressure only); and on what evidence offered?

The unit is one outage; claims are kept in a second ledger whose unit is one claim, linked to the outages it names. The study describes; it tests nothing, estimates no rate and makes no causal finding of its own. It cannot show that patching for model-found flaws did not contribute to any outage: an operator naming another cause excludes nothing it doesn't say.

## What the writer already knows

Everything below was read before this brief, by the sweeps of 18 and 20 November or by this writer in the CSA note, and is prior knowledge, not outcome. Every item is reported by the page named, mostly through a fetch tool's summary, so quotations are as relayed. None is an operator's own report read by Lighthouse.

- **The Washington Sun, 17 November** (L-0150; scout 7 of 18 November, read about 13:03 UTC): three unnamed sources and "a congressional official briefed on the matter" say Wall Street executives and NSA officials told Congress that patching driven by model-found flaws is behind the FAA, JPMorgan, NSA network and Microsoft outages ("more than the system was designed to handle", as relayed). No hearing, committee or transcript is named. Every on-record statement it quotes gives a non-AI cause: JPMorgan software bugs, the NSA "scheduled routine maintenance", Microsoft a technical defect.
- **The CSA note, 18 November** (scout 4 of 20 November, row 8; reread by this writer at 12:57 UTC): lists eight outages (below), "finds no public evidence that such patching caused any specific outage in the cluster, and the specific causal claim is unsupported", and says the underlying pressure is real. It could not locate the Washington Sun's original and assessed it only through re-reports. It cites Anthropic's coordinated disclosure dashboard: 5,087 vulnerabilities disclosed across 680 open-source projects, upstream patches confirmed for 629, as of 2 November, and more than 37,000 candidate findings. It notes that Anthropic's Claude services recorded at least seven incidents that week and that Anthropic attributed one, its Microsoft 365 connector, to Microsoft's outage.
- **The causes the CSA note gives, as already known.** Scout 4's summary gave them in short; the reread adds the wording and the CSA's sources, which are press and commentary, not operators' own reports (the CSA's own column heads them "Stated or Reported Cause"). They are listed in the population table below. The reread also added: the FAA is quoted (via a news site) as finding "zero evidence of anything nefarious, and zero evidence of anything AI related"; DHS said it was examining whether the FAA's AI-assisted planning platform was linked, and transportation officials later ruled that out; the DNI attributed the disruptions to organisations fixing vulnerabilities and upgrading aging systems; two sources cited routine patching for the NSA network; United's cause comes from the pilots' union, not the company; and investigations at Microsoft, the FAA and the NSA were described as ongoing.
- **Reuters, 18 November, via The Star** (scout 4, row 9): experts say AI makes flaws "fast and cheap" to find and emergency patches reach core infrastructure "without full testing"; Secretary Rubio quoted that patches are "creating short-term disruption"; DNI Clayton saw no sign so far that the outages are related; the OCC's head called JPMorgan an "isolated incident". VulnCheck and Qualys counts are quoted; they are context, not used.
- **The House Homeland Security Committee hearing, 18 November**, as reported by Nextgov and CyberScoop (scout 7 of 20 November, lead 1; the hearing record was not found or read): witnesses Mullin, Clayton and Raia. The DNI: "the rate of patching, the rate of upgrading of systems is increasing"; no witness, as reported, said AI found the flaws, and witnesses saw no malicious attack. Two unnamed people told Nextgov most outages "appear to be linked to efforts to rapidly patch vulnerabilities with AI". CyberScoop quotes Sen. Warner (AI discovery is "creating enormous pressure on companies and government agencies to patch those vulnerabilities immediately") and Rep. Himes (more discovery and patching "could cause more frequent outages"). Where Sen. Warner said it is not established by what was read; a senator is not a member of a House committee. Neither, as reported, said patching caused a named outage.
- **The FAA's on-record cause** (AP, 17 November, on the Washington Sun's site; scout 7, row 19): one router recently installed in El Dorado, Arkansas, sending "excessive data … at a rate of 1,000 connection attempts every 4 to 5 seconds"; installation paused and installed routers turned off. Democrats: "Identifying the device that failed does not establish why it failed." A letter from Democrats to the Transportation Secretary on root cause, and a senators' letter, are reported (scout 7), not read.
- **The departing National Cyber Director** (Washington Sun, 19 November; scout 7, row 20) attributed the disruptions to upgrades of aging systems, "not any sort of coordinated, nefarious cyberattack".
- **Microsoft**, from the [Microsoft outage report watch](../../notes/microsoft-outage-report-watch.md) (issue #54) and its readings of 14 to 19 November: Microsoft's exclusion of AI and agents as retained in issue #54, through a tenant's copy; a preliminary post-incident report dated 15 November, known only through commentators' summaries (a latent defect in a July fix for gateway servers, triggered by failover traffic while gateway capacity was offline); a final report said to be due about 20 November. No Microsoft-authored report has been retained. A copy of the preliminary report hosted by next.ink was read by a scout in breach of robots.txt on 20 November ([incident note](../../notes/incidents/2026-11-20-ungated-pdf/README.md)); its content is not known to this writer and is never used.
- **The gate's corrections**: "denied" is too strong for the operators' statements (the FAA names a router, not why it failed); the sweep's "legislators say yes" overstated what Warner and Himes said.

What this writer expects, stated so a reader can discount it: that most operators will publish no full post-incident report in the window, that those who do will name a change or defect without saying where the fix came from, and that no operator will say a model found the flaw it was fixing. The design does not depend on that expectation being right.

## Population and unit

The outage list is the eight rows of the CSA note's table of incidents ("The table below summarizes the publicly reported incidents and the cause each organization has stated as of this writing"), read 20 November 2026 at 12:57 UTC, page dated 18 November. It is fixed now and does not grow: an outage the CSA or anyone else adds later is noted in the record and not followed.

| # | Outage (operator) | Date (2026, as the CSA gives it) | Cause as the CSA note gives it (already known; the CSA's sources are press, not the operator's report) |
| --- | --- | --- | --- |
| O1 | Microsoft 365: Exchange Online, Outlook, Teams, Copilot (Microsoft) | 12 to 13 November | Latent defect in a July gateway-server update, triggered by extra Teams failover traffic while about 14% of gateway capacity was offline (BleepingComputer on the preliminary report) |
| O2 | Workday customer tenants (Workday) | 13 to 14 November | During a disaster-recovery maintenance check, DR-site services "unexpectedly connected to Production databases" (UC Today) |
| O3 | FAA nationwide ground stop (FAA) | 13 November | A router installed by a contractor in a copper-to-fibre conversion, with a second site, flooded legacy equipment with connection attempts (GovInfoSecurity) |
| O4 | AWS us-east-1, IAM Identity Center and other services (Amazon Web Services) | 15 November | Not disclosed |
| O5 | JPMorgan Chase, with delays at other banks and Zelle (JPMorgan Chase) | 16 November | "Software bug in on-premise hardware systems" (AppleScoop) |
| O6 | United Airlines departures (United Airlines) | 16 November | Weight-and-balance system fault, per the pilots' union, not the company |
| O7 | Apple: iCloud sign-in, App Store (Apple) | 17 November | Unspecified "internal update" (IBTimes UK) |
| O8 | NSA classified internal network, NSANet (National Security Agency) | 17 November | "Temporary degradation during scheduled routine maintenance"; two sources cited routine patching (CNN, CBS) |

Not in the population: Anthropic's own incidents that week (named in the CSA's prose, not its table; Lighthouse runs on Anthropic's models, and one of them is attributed to O1); Codeberg's registrar hold of 18 November, Schwab's website and anything else the sweeps met outside the table. The Washington Sun's four named outages (O1, O3, O5, O8) are inside the list.

## Sources and event definitions

**Operator's own report** (question 1). A document published by the operator itself, on a host the operator controls: for the companies, their own newsroom, status, health, trust or post-incident pages and engineering blogs; for the FAA, faa.gov or its parent department's transportation.gov; for the NSA, nsa.gov or its parent department's defense.gov, and the Office of the Director of National Intelligence where it speaks for the intelligence community about NSANet (classed as "parent body", not "operator", and said so). A verbatim copy of an operator's document on another host counts only if the host is allowed by the robots gate and the copy is presented as the operator's document; it is classed "copy, identity with the operator's original unchecked". An operator's public social-media post counts if the gate allows the URL. Nothing behind a login, customer portal, tenant console or support contract is read.

Each operator document is classed by kind: **final** (the operator calls it a final, full or root-cause report or review), **preliminary** (preliminary, interim or initial report, or one the operator says will be replaced), **statement** (a short public statement or status update). Its date is the operator's own publication or revision date where it shows one, else the first Lighthouse read, said so.

**Event: cause stated by operator.** The operator's own document names a cause or trigger (a change, defect, failure, test, device or process) in its own words. The record keeps the cause in at most 40 words of quotation per document, located, with its date and kind. A later document from the same operator supersedes an earlier one only for "current", and both are kept.

**Three items read from each operator document,** each in the operator's words or marked "not mentioned":
- (a) whether the triggering change is described as a **security fix or patch** for a vulnerability;
- (b) whether the fixed flaw is said to have been **found by an AI model** (or by automated tools, kept distinct from AI unless the operator says AI);
- (c) any **statement about AI** at all (an exclusion, an involvement, AI in diagnosis or recovery), quoted as the operator's.

If (a) names a specific vulnerability by identifier, one read of its CVE record (cve.org or NVD) for the credit the record publishes is allowed, classed as the numbering authority's statement, never as the operator's.

**Event: AI link claimed** (question 2). A public statement that patching for flaws found by AI models caused, contributed to or could cause an outage in the list or the cluster. Each claim is recorded with: who (named person and role, or "unnamed", with the number of unnamed sources as reported); route and date; which outages it names (specific ones, the cluster, or outages in general); strength (caused, contributed, could cause, pressure only), in the claimant's words; and evidence offered (none stated; an anonymous characterisation; a document, data or report cited, named). Statements that there is **no** AI link (such as the FAA's "zero evidence of anything AI related" as relayed, or the DNI's "no sign") are kept in the same ledger as statements against, with the same fields. A claim that patching in general, without AI, caused an outage is kept separately as a **general patching** claim and never merged with an AI claim.

**Sources for claims, in order:**
1. The House Homeland Security Committee's own record of the hearing of 18 November (hearing page, written testimony, video or transcript on homeland.house.gov; the printed transcript on congress.gov or govinfo.gov when posted). Read when posted; what each witness and member said about patching and AI is quoted, located.
2. Letters and statements from members of Congress on their own or a committee's .gov site.
3. Official statements by government officials on a government host.
4. Press, only as the route by which a claim was made: a claim first or only made in a newspaper is recorded as "X, as reported by Y", attributed, with Y's date. Press is never a source for an operator's cause in question 1, which stays "operator's cause not read" if only the press carries it.

**Microsoft (O1)** is taken from the Microsoft outage report watch, never read twice. Until that watch closes (row MS365-report-close, by 12 December), LH058 makes no request to any Microsoft host, any copy of Microsoft's report, or any coverage of it; O1's row cites the watch's readings and, if the watch reaches it, its reviewed comparison. If the watch closes without a qualifying Microsoft-authored report, LH058's later reads may look for Microsoft's final report under the watch's own criteria (Microsoft-authored, or an allowed host's copy so classed), at most one search and two documents per read, and say that this continues the watch rather than repeating it. next.ink's copy is never fetched or used, and nor is anything a robots gate has refused.

## Classes

For each outage at each read, and at the end, one class for question 1:

- **Cause stated by operator**, with kind (final, preliminary, statement), date and the three items (a), (b), (c).
- **No cause stated by operator**: the operator's own documents found say the service was restored or describe impact, but name no cause. Never read as a denial of anything, and never as support.
- **Operator's cause not read**: a cause is reported only by others (union, regulator, official, press). Recorded, attributed to who said it, and kept apart from the operator's cause.

And for each claim in the second ledger: **AI link claimed** (by whom, route, strength, evidence offered or "none stated"); **AI link denied or doubted** (same fields); **general patching claim** (same fields). An **operator statement on AI**, where one exists, is quoted as the operator's and sits in the outage's row, not in the claims ledger.

## Missing evidence

- **Not found**: a read's searches and routes found no operator document. Unknown, not absent; the next read looks again.
- **Unreadable**: a document exists but the robots gate refused it, or it is behind a wall, challenge, login or rate limit. Recorded as a wall with its URL and time and never got around; the class is "not read", never "no cause".
- **Not yet posted**: the hearing record or a promised final report is not yet up. Recorded as such at each read.
- **Read missed**: a read not made in its window is missed, never made up later; the next read does not cover for it.
- A missing mention of AI, a patch or a finder in an operator's report settles nothing about any of them.

## Comparison

None beyond a description. The record may set the eight rows side by side (how many operators stated a cause in their own report by the last read, of what kind; how many said the trigger was a security fix; how many said a model found the flaw; which claims of an AI link offered any evidence beyond anonymous characterisation), as counts with their denominators, and says that eight purposively listed outages of one week are not a sample of anything. No test, no rate, no reading of whether patch volume causes outages. Any reading made after outcomes are seen is labelled post hoc with its number of comparisons.

## Overlap with earlier studies

- **The Microsoft outage report watch** (issue #54, rows MS365-report-*): O1's only source until it closes, as above. No read counted in both; LH058 adds nothing to the watch's bounds or rows.
- **LH052** (organisational capacity and reliability, stopped 13 November, issue #51): it recommended against adding known outage narratives because they could not supply team-level exposure. LH058 asks a different, narrower question (what operators state, and who claims an AI link) and seeks no staffing or capacity chain; the keeper agreed it knowing it reopens the outage strand whose next step issue #51 holds. No LH052 coding or source is reused.
- **LH036 and LH038** (the model-found Linux kernel flaw and its disclosure timeline): context for what a model-found flaw and its patch clocks look like. No data shared; LH058 says nothing about that flaw unless an operator's report names it, which would be recorded and not interpreted.
- The sweeps of 18 and 20 November (L-0150, scout 4 lead 2, scout 7 lead 1) are prior knowledge above, not reads of this study.

## Model disclosure and framing

The claim under study concerns flaws found by AI models; the CSA note's evidence of rising patch pressure is Anthropic's own disclosure dashboard; one of Anthropic's incidents that week is attributed to O1; and Lighthouse runs on Anthropic's models, as does this writer. A record that found operators blaming model-found flaws would be harder on Anthropic, and one that found none would be easier on it; neither is wanted. Reviewers look for wording easier or harder on Anthropic, or on any AI developer, than the sources allow, and for any use of the dashboard's count as evidence about these outages (the record cites it only as the CSA's citation; nothing read connects it to any operator's change). The same care applies to Microsoft, which is both an operator here (O1) and an AI developer.

## Voice

No claim in Lighthouse's voice that harm is happening now or that any named system was or is compromised; whether any outage was an attack is the operator's or an official's statement, attributed. Operators' causes and legislators' or officials' claims are always attributed to who made them, with date and route. No mechanism is described beyond what a reader needs to place a cause. Nobody is contacted: no operator, committee, member, journalist or source. No exposed host or indicator any report lists is visited.

## Retention

No body is kept in the repository. Each read writes a dated reading, `studies/LH058/readings/YYYY-MM-DD.md`, with each URL, publisher, the document's own date, UTC read time, gate answer, status, bytes and sha256 of the bytes received, and the located quotations the classes need (at most 40 words per operator document and per claim). Every request is a row in [fetchlog.csv](fetchlog.csv). Bodies read in scratch are passed through `redact_bytes` from scripts/redact_emails.py before any text is kept, and deleted after the read.

## Resource ceiling

Per read: the robots gate (`LIGHTHOUSE_PROVIDER=anthropic python3 -I scripts/robots_gate.py <url>`) immediately before every fetch, including any URL met mid-read or in a search result; at most four searches and at most twelve documents fetched (robots.txt fetches not counted), with Lighthouse's User-Agent; for O1, the limits in "Sources" above. At most seven reads. No account, key, API token, paid service or subagent for collection. Model spend: about $15 at list rates for the brief, all reads and the record, before reviews.

## Reads, schedule and stopping

- **Weekly reads**, each in a window of two days: 23 to 24 November, 30 November to 1 December, 7 to 8 December, 14 to 15 December, 21 to 22 December, 28 to 29 December 2026, and a last read on 1 to 2 January 2027. Each read checks, for every outage not already at "cause stated by operator, final", the operator's routes for a new document; checks the hearing record; looks for new letters or official statements; and records any new claim of an AI link met on the way.
- **Stopping early**: once all eight outages are at "cause stated by operator, final" and the hearing record has been read, the remaining reads are cancelled with that reason.
- **No read after 2 January 2027**, and no extension without a keeper line.
- **Closure** (row LH058-closure, 2 to 4 January 2027): reconciles every read to done, missed or cancelled with reasons, and lists what was never found or never readable.
- **Record**, version 0.1 by **8 January 2027**: header, In short, Answer, Findings, Method, Limits, Next, Corrections; the outage ledger and the claims ledger as tables, each cell dated and sourced; then its evidence review, reader-and-inference review and recheck before anything reaches a public surface.
- The question, the list, the event definitions, the classes and the missing-evidence rules do not change after any outcome is read; any later change is a dated amendment, labelled post hoc if made after outcomes were seen.

## What would leave it inconclusive

The ledger always answers in its classes, but its bearing on the claim is inconclusive for any outage whose operator states no cause in its own report by the last read, or whose report is unreadable; and for the cluster as a whole if that is true of most of the eight. Even where every operator states a cause, the study cannot say whether patching for model-found flaws contributed where an operator does not say, since a named cause excludes nothing else. A security fix named as the trigger, without a statement of who or what found the flaw, leaves the AI link unknown, not shown. If the hearing record is not posted by 2 January 2027, what witnesses said stays as reported by the press, attributed, and the record says so.

## Amendment, 26 November 2026, by the keeper's session: interim checkpoints

At the keeper's request, a study collecting for weeks gives readers a reviewed answer so far rather than waiting for its closure (schedule/runner.md, step 5). Made after the first read (23 November), so labelled post hoc; it changes no list, event definition, class, missing-evidence rule, read or stopping rule. After the reads of 7 December and 21 December 2026, an interim ledger (record 0.1, then 0.2) is written, with an evidence review, a reader-and-inference review and a recheck, **only if** the reads since the last version could change a ledger cell or its bearing on the claim (an operator publishing or upgrading a report). Otherwise the record (or, before 0.1 exists, the checkpoint) gains one dated line saying what was read and that nothing changed, and that checkpoint's review rows are cancelled with that reason. Each interim ledger is labelled as standing at its last read; the record after closure takes the next version.
