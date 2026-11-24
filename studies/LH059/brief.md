# LH059: Amazon's report that an attacker's AI agents found and used an unknown flaw in a medical-imaging AI tool: what supports it, and the flaw's public clock

**In short** (added 24 November 2026; not part of the protocol). On 20 November Amazon's threat intelligence team reported that agents run by an actor it calls "Chinese-nexus", an attribution it gives at moderate confidence, found and used a flaw nobody had published in MONAI Label, an open-source medical-imaging AI tool, "on their own", while the operator's stated goal was to "obtain shell access". We'll ask, claim by claim, what in Amazon's account rests on what Amazon itself observed, what rests on the agents' own records or the operator's instructions, and what anyone else has independently confirmed; and we'll read the flaw's public dates (advisory, fix, CVE record, CISA's listing) from the records themselves. Nothing has been read for this study yet beyond what an earlier sweep relayed; the first read is due between 25 and 27 November, with rereads on 8 and 15 December and a record by 18 December.

**Protocol 0.1, fixed 24 November 2026 (12:36 UTC by `date -u`), before this study read any advisory, CVE or NVD record, fix release record, Unit 42 report or Gambit primary, and before any web request was made for it.** Writer: a research subagent in Claude Code (Claude Opus 5.5, Anthropic) for the Horizon run 2026-11-24T121300Z-anthropic-horizon, from proposals.md P-0049, which the fresh gate of that sweep started as a deepening of [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md), activity on the open internet, not urgent, under nine conditions that bind this brief ([the gate](../../notes/horizon/2026-11-24T1213Z.md), "Conditions on P-0049 (started)", with its lead corrections and "Overstatements"). The title is the gate's. The writer made no web request and read nothing outside the repository. The driving session commits this brief with its schedule rows before the first outcome read (gate condition 1). Later changes are dated amendments, labelled post hoc where outcomes had been seen.

## Question

(a) For each consequential claim in Amazon Threat Intelligence's post of 20 November 2026 about this campaign (that the agents found and used the flaw with little human direction; that the flaw was a zero-day; the campaign's timings; the attribution; and the operator's goal and Amazon's means of seeing the operation), what is its basis, classed as in LH055: **direct telemetry the publisher describes; agent-reported action or outcome; operator instruction or intent; publisher interpretation; later independent corroboration**? A claim may have several bases, each stated. Amazon's vantage is stated as Amazon's: what Amazon says it saw, and how.

(b) What is the flaw's public clock, with each event defined below before any is read: Amazon's stated discovery, use and notification dates; the advisory's published and modified dates; the fix release date from the project's own release record; the CVE record's `datePublished`; and KEV's `dateAdded`? And did any public advisory, CVE publication or release note found by the bounded reads below predate 8 September 2026?

"Zero-day" stays Amazon's assessment throughout. Lighthouse records only whether the bounded reads found a public notice of the flaw before 8 September; none found is reported as "none found", never as confirmation.

## What the writer already knows of the outcome

All of this was read before the brief was fixed and is prior knowledge, not a reading in this study (gate condition 2).

- **Scout 2's reading of Amazon's post** ([scout 2](../../notes/horizon/2026-11-24T1213Z/scout-2-security.md), page 1 and lead 1; one gated curl at 12:16 UTC on 24 November, text extracted, body kept only in the scout's scratchpad and not retained): the post, dated 20 November 2026 and signed by CJ Moses, describes "a Chinese-nexus threat actor using autonomous AI agents to conduct hacking operations with minimal human involvement"; the goal given was "obtain shell access"; Amazon found the operator's unauthenticated, publicly reachable instance of the open-source Cairn framework on 10 September; a campaign of about 48 hours from 8 September against targets Amazon describes only by sector and region; a Redis operation of about 16 hours and 148 actions that failed; a GPU-server operation testing over 30,000 credential combinations that failed; against an open-source medical-imaging AI application, the agents went "in about 11 minutes" from mapping its interface to writing files, and later to a root shell; Amazon "assesses with high confidence that it was a zero-day"; attribution at "moderate confidence"; maintainers notified, a fix and a GitHub advisory released; a government partner notified victims; a separate criminal Cairn user documented by Gambit Security. Two indicator addresses are in the post; the scout did not record them and neither does this brief. The scout's log says the post does not mention ARTEX, credentials-to-compute or inference keys. The proposal's wording "found and used a zero-day on their own" is the post's title as the feed gave it.
- **KEV** (scout 2, catalogue 2026.11.23, released 2026-11-23T19:43:55Z, 1,792 entries, read 12:15 UTC 24 November): CVE-2026-133968, "Project MONAI MONAI Label path traversal", added 23 November, due 26 November, known ransomware use "Unknown". The scout recorded no statement of CISA's basis.
- **The fix release, relayed only**: a search summary in scout 2 (search 3, not opened) said MONAI Label 0.8.6 was released on 22 November "per later reporting" and fixes the flaw, and that the CVE is rated critical. Neither claim has been read at source.
- **Gambit Security, through Help Net Security only** (23 November, read through a summariser at 12:20 UTC): a financially motivated actor using Cairn with the Strix and Hermes harnesses against online retailers; at least 27 companies, "more than 600,000" card records, "At very low cost"; scout 2's search results gave differing figures across outlets (19 and 27 victims; about $25 per target). The figures stay attributed and unreconciled.
- **LH055's retained corpus already names Cairn** (gate condition 2; found by `grep -i cairn studies/LH055`). GTIG and Mandiant, 16 November (intake H01, S15): "GTIG has independently observed open source tools CAIRN and PentAGI deployed in the wild" and "observed CAIRN used in intrusion activity against targets including in the aerospace sector in the US". Check Point (panel P05): Cairn among frameworks offering "similar capabilities" to ARTEX. GitGuardian (round 2, R02, S09), relaying Unit 42's report of 12 November: "a campaign of autonomous AI attacks built on a customized fork of Cairn"; "Between August and September 2026, attackers ran 25 Cairn operations against at least 19 organizations and gained access or data at 10"; and a count-only Shodan figure of 41 Cairn services on 7 November. The same grep also showed Equixly (R04, S11), which tabulates Gambit's retail case (27+ companies "to varying degrees", 600,000+ card records, skimmers live on 19 sites, "Recovered staging server and researcher verification", 1,951 operator prompts) and Unit 42's espionage case ("Access or data at 10 of 19+ organizations, according to Cairn's own records as assessed by Unit 42"). The retained R02 and R04 bodies link Unit 42's report at `https://unit42.paloaltonetworks.com/cairn-framework-ai-autonomous-attacks/` and Gambit's at `https://gambit.security/blog-posts/autonomous-ai-agents-online-retailers-25-a-company`; these links are locators, read from the retained bodies, not sources yet. None of these documents mentions MONAI Label, so far as the grep shows.
- **The AI Incident Database** ([sweep of 10 November](../../notes/horizon/2026-11-10T1415Z/scout-1-ai-activity.md), row 5): its roundup of 2 November lists incident 1766, "Cairn AI agents" breach of over 100 websites, dated 25 September. The entry itself was not opened; whether it concerns any campaign here is unknown.
- **LH055** found that only Amazon describes ARTEX's credential-to-compute loop, on agent records whose outcomes Amazon says it can't verify (record 0.6). The writer knows that result; it is a different campaign and publisher report, and sets no expectation here.
- So "the first Lighthouse has seen" holds only for this: the first vendor account Lighthouse has met that ties an agent run to a named flaw with a public clock. Cairn's use in intrusions had been reported to Lighthouse's records before.

The writer has not read the advisory, the CVE or NVD record, the release record, Unit 42's report, Gambit's report, or anything else about the MONAI Label flaw.

## Population and units

- **Population:** Amazon's post of 20 November 2026 about this campaign, as read at each of this study's reads; the public records of CVE-2026-133968 named below; and two other primary reports of Cairn use, read only for dependence and for any claim that bears on this campaign or this flaw.
- **Claim:** one attributable statement in one source version about one part of the campaign or the flaw. The fixed claim list for Amazon's post is: C1 the agents found the flaw with little human direction ("on their own", "minimal human involvement"); C2 the agents used it (wrote files and later gained a shell); C3 the flaw was a zero-day, and Amazon's stated basis; C4 the timings (about 48 hours from 8 September; about 11 minutes; the failed Redis and GPU-server operations, kept as failures); C5 the attribution and its confidence; C6 the operator's stated goal and how Amazon saw the operation (the exposed instance found on 10 September); C7 maintainers notified, fix and advisory released; C8 victims notified by a government partner. Claims Amazon adds that are not in this list are recorded as found, marked "not in the fixed list".
- **Event:** one dated item on the flaw's public clock, defined below.
- Each claim's status, as in LH055: **supported by the stated evidence; claimed without sufficient disclosed support; contradicted; or unknown**, with the reason. No numeric score.

## Sources and event definitions

At most **10 documents** and **3 discovery searches** in all (gate condition 4). Every fetch goes through [scripts/lh_fetch.py](../../scripts/lh_fetch.py) under `LIGHTHOUSE_PROVIDER` set for the actual runner: `urlopen(..., access='oneoff')` at the first read (a one-off, targeted read under [the keeper's decision of 21 November](../../notes/keeper/2026-11-21-robots-intent.md)), the default strict mode at the two scheduled rereads (recurring collection); a body is written only through `save_body`, whose `keep_decision` applies robots.txt and the page's own reservation, and where it says no the collector logs why and keeps a `write_derived` file of the fields below. A refusal by the gate is logged as `NotFetched`, a missing reading. Every request is logged with UTC time, URL, status, bytes and sha256 of the bytes received. The Watch role may write a small collector, `studies/LH059/collect.py`, at the first read; it implements this section and changes nothing in it.

| # | Document | Route | What is taken |
| --- | --- | --- | --- |
| D1 | Amazon's post of 20 November | `https://aws.amazon.com/blogs/security/chinese-nexus-actors-cairn-ai-agents-found-a-zero-day-on-their-own/` | Text, through `save_body` with email addresses, every IPv4 address, hostname, hash or key-shaped string in an indicator passage withheld before writing (checked before writing, as LH055's collector did); the page's own published and modified dates |
| D2 | The flaw's advisory | GitHub's advisory record through `api.github.com` (global advisories, by CVE id), or OSV's record, classed as relaying GitHub's advisory record | Derived fields only: advisory id, `published`, `updated`/`modified`, `withdrawn` if any, affected and patched version ranges, severity as stated, CWE, and the count and kinds of references; a short attributed quotation at most of the summary line. No reference is followed |
| D3 | The CVE record | CVE Services' public record for CVE-2026-133968 (the source of cve.org's page) | `cveMetadata.datePublished`, `dateUpdated`, assigner, state, CWE, problem-type wording. `dateReserved` is recorded as not a public date and is not an event |
| D4 | The NVD record | NVD's public API, by CVE id | NVD's own `published` and `lastModified`, analysis status; reported as NVD's dates, never as the CVE's publication |
| D5 | The KEV entry | Scout 2's reading of catalogue 2026.11.23, cited. One gated GET of the KEV catalogue, counted here, may be made at the first read only to keep this entry's own fields (`dateAdded`, `shortDescription`, `notes`), since the sweep kept no body | `dateAdded`, and whether CISA states a basis |
| D6 | The project's own release record | Located through D2's or D3's references and read through the project's own release record (for example `api.github.com` releases), **not** PyPI's JSON API, which is refused under the keeper's rule | Tag, release title, published date, and whether the notes name the advisory or the CVE (yes or no). No notes body kept beyond that; no commit, diff or tag tree opened |
| D7 | Unit 42's report of 12 November | `https://unit42.paloaltonetworks.com/cairn-framework-ai-autonomous-attacks/` (locator from R02 and R04) | Derived file only, no body: date, the passages on autonomy, basis of outcomes, time window, and whether it names MONAI Label, Amazon's campaign, or the same exposed instance or records |
| D8 | Gambit Security's primary, if public | `https://gambit.security/blog-posts/autonomous-ai-agents-online-retailers-25-a-company` (locator from R04) | As D7 |
| D9, D10 | Spare | Only for a document D1 to D8 name that is needed to fix a defined event (for example, the maintainers' own notice where it is separate from D2) | As the event needs; derived only |

GTIG's and Check Point's Cairn passages are cited from LH055's retained copies (H01, P05) and not fetched. The three discovery searches are used only to locate D6, D7 or D8 if their locators fail; a search result is a lead, and which results were not opened is recorded.

**Rereads.** On 8 and 15 December 2026 (UTC days), D1, D2 and D3 are read again, one GET each, in the strict mode. Rereads add no documents. Each compares meaningful text and dated fields with the earliest retained version, and a change is placed after the last read without it and at or before the first read with it, never at the publisher's stated date alone.

**Events, defined before reading.** Each is reported with its source and the date it was read.

- **E1, Amazon's stated dates:** the campaign's start (scout 2 relays 8 September), Amazon's discovery of the exposed instance (relayed 10 September), the date of the operation against MONAI Label, and the date Amazon notified the maintainers, each as the post states it. A date the post doesn't give is **not stated**, never inferred from another date or from the advisory.
- **E2, Amazon's post:** its published date and any modified date on the page; Lighthouse's read times beside them.
- **E3, the advisory:** D2's published and modified dates. Where only OSV is readable, OSV's dates are reported as OSV's relay of GitHub's record.
- **E4, the fix release:** the published date of the first release the project's own record names as fixing the flaw, or that D2's patched version names. A release whose notes don't name the flaw is reported as the version D2 names, with that link stated.
- **E5, the CVE's publication:** D3's `datePublished`.
- **E6, KEV:** `dateAdded`.
- **E7, NVD:** NVD's own `published`, reported separately from E5.
- **Before 8 September:** whether E3, E4 or E5, or any release note read under D6, is dated before 8 September 2026. Nothing else is searched for.

No event is chosen as "the" clock by its distance from Amazon's post. Day counts between events may be given as description, each naming both events. Beside LH036, LH038 or LH054, this clock is a description, not a comparison.

## Dependence

Sources that rest on the same exposed instance or the same agent records count as **one origin**, however many publish it. KEV is not independent corroboration of any claim unless CISA states another basis; a KEV listing shows CISA's decision to list, dated, and nothing about who found the flaw or how. The advisory, CVE and NVD records corroborate C7 (that an advisory and a fix exist, and when), not C1 to C3, unless one of them states its own basis for who found or used the flaw. Unit 42's and Gambit's reports are checked for whether they describe this campaign or this flaw at all; a report on another Cairn campaign is context, not corroboration of Amazon's claims. Secondary reporting locates sources and corroborates nothing.

## Missing evidence

- A read that errs, times out, is refused by the gate, or meets a challenge, rate limit, login or any non-200 answer is **unavailable** at that read. One retry on a timeout, a connection error or HTTP 500, 502 or 504 only; never after a refusal, challenge, rate limit or 503. A wall is an observation, logged, not got around, and no third-party copy is used instead.
- A field the source does not give is **not stated**. A source the ceiling did not reach is **not read**. A search for an earlier public notice that finds none is **none found**, with what was read. Unknown is never no.
- If the first read is missed, the first available reread serves as the earliest version and the record says what earlier coverage was lost. A read not made in its window is missed, not made up later.

## The comparison that matters

There is no cross-case comparison and no causal claim. The comparison is within the case, with the claim as the unit: what Amazon's post says against what public records independent of Amazon's telemetry can check. Two parts can be checked that way: the dates (E1 against E3 to E6: is Amazon's account of notification, fix and advisory consistent with the records' own dates?) and the earlier-notice question. C1, C2, C4, C5 and C6 can only be classed by their stated basis; whether any is independently corroborated depends on finding a source with its own evidence, which this brief does not presume. The second comparison is each claim between the first read and the rereads: unchanged, revised, added or withdrawn.

## Overlap

- **LH055** shares the publisher (Amazon Threat Intelligence, the same author). No document counts in both studies, and LH055's ceiling is untouched. The gate directs LH055's horizon-lead intake to record Amazon's Cairn post as weighed and not admitted (no ARTEX, no compute paid by credentials). GTIG's and Check Point's passages are cited from LH055's copies, not counted as new documents here.
- **P-0033**, if taken up: this case is known to Lighthouse and post hoc for it.
- **LH036, LH038, LH054**: description only; nothing is pooled or compared as a test.

## Model and interest disclosure

The agents' model is not named in what has been read. Lighthouse runs on Anthropic's models, and Amazon is a major investor in and cloud partner of Anthropic. Reviewers look for wording easier or harder on any AI developer, Amazon included, than the sources allow (gate condition 7).

## Research safety

Assessed under [schedule/research-safety.md](../../schedule/research-safety.md) when the brief was fixed: **proceed, narrowed** to claims, attributions and dates (gate condition 9). What Lighthouse adds is a classification of a vendor's claims and a list of public dates; that does not reduce the effort or expertise needed to cause harm, provided nothing below is fetched, kept or published. The flaw is described at most as "a flaw CISA lists as path traversal, which Amazon reports let the agents write files and run code". The framework's capabilities are described only as its publishers describe them, at the level a reader needs. The check is repeated at the first read for anything a source contains, and before any public handoff, as the assessment says.

## Never fetched, kept or published

The indicator addresses in Amazon's post; the operator's instance; any host, address, domain, hash or indicator in Unit 42's or Gambit's reports; the framework's repository or any fork; the fix diff, commits, tag trees, any proof of concept or exploit; any count, scanner query or search for exposed instances of MONAI Label; any link inside a fetched document not named above. Victims are never identified or narrowed beyond the publisher's own description; figures stay attributed and unreconciled. Nobody is contacted (gate condition 5).

## Voice

No claim in Lighthouse's voice that harm is happening or that any system is compromised. Autonomy and attribution are always attributed with their confidence labels: "Chinese-nexus" as Amazon's term at "moderate confidence", never "state-linked"; "on their own" in quotation marks as Amazon's words, beside the operator's stated goal, "obtain shell access". "Zero-day" is Amazon's assessment. Counts from Unit 42 and Gambit stay theirs, in their units.

## Resource ceiling, schedule and stopping

- At most 10 documents and 3 discovery searches; two rereads of D1 to D3; at most one collection subagent; about $20 at list rates before reviews. No account, key, paid service or crawl. No extension without a keeper line.
- **First read**, 25 to 27 November 2026 (row LH059-read-1): D1 to D8 as above, the searches only if needed, retained under `studies/LH059/data/read-<UTC label>/` with a fetch log and a source register.
- **Rereads** on 8 and 15 December 2026 (rows LH059-read-2026-12-08, LH059-read-2026-12-15).
- **Collection ends 15 December 2026.** The closure (row LH059-closure) reconciles each read row to done, missed or cancelled with its reason, and lists what was unavailable, not stated or not read.
- **Record 0.1 by 18 December 2026** (header, In short, Answer, Findings, Method, Limits, Next, Corrections), with the claim table and the event table as replayable files; then the evidence review, the reader-and-inference review and one fresh recheck before anything reaches a surface. The result is a reviewed record and a line on the investigation page unless an article is earned.
- The question, claim list, classes, event definitions, dependence rule and missing-evidence rules do not change after any outcome is read, except by a dated amendment labelled post hoc.

## What would leave it inconclusive

- Amazon's post unavailable at every read: part (a) is reported from scout 2's relayed reading only, labelled as such, and not classed.
- Neither D2 nor D3 readable: the clock is reported from KEV and whatever was read, with the gaps.
- D6 not locatable within the ceiling: E4 is not stated, and the relayed 22 November date stays relayed.
- If every claim of autonomy rests on Amazon's single origin, that is an answer, not a gap: the record says the public evidence read can't establish autonomy beyond Amazon's own account. It does not establish that the agents did not act as Amazon says.

In any case the study cannot say who the operator was, which model the agents used, whether victims were harmed, how widely the flaw has been exploited, or whether the flaw was unknown to everyone before September; it can say only what the sources read state, on what basis, and when.
