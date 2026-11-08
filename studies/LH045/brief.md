# LH045: Keep it before it rolls over: Epoch AI's data-centre records and the IETF's agent drafts, captured while they are still public

**In short** (added 8 November 2026; not part of the protocol). Some public records that bear on what AI costs the shared internet keep only their present state, so a day not kept is lost. We looked at three: daily compute prices, Epoch AI's log of AI data-centre estimates, and the Internet-Drafts on agents and bots being discussed at the IETF's meeting from 14 November. The price sources all forbid keeping or republishing their figures, so that part is dropped and the wall is recorded. Epoch's data is openly licensed and is kept weekly to 3 January 2027, and the IETF drafts are counted now, on 13 November and once after the meeting; this study only keeps the records, and names the questions a later study will test on them.

**Protocol 0.1, fixed 8 November 2026, before the first capture by the collectors named below.** Writer: a subagent of the driving session of 8 November 2026 (Claude Code, Claude Opus 5.5), on the task the keeper started at the review of 8 November (proposals.md, "From the keeper": what the session starts counts as started by the keeper). Leads L-0011, L-0019 and L-0012 of the horizon sweep of 7 November 2026 ([sweep](../../notes/horizon/2026-11-07T0853Z.md), scouts [4](../../notes/horizon/2026-11-07T0853Z/scout-4-infrastructure.md), [6](../../notes/horizon/2026-11-07T0853Z/scout-6-policy.md) and [7](../../notes/horizon/2026-11-07T0853Z/scout-7-wildcard.md)). Investigation: [What AI activity costs the shared internet](../../investigations/ai-cost-and-spread.md), its load and cost strands. The collectors, [scripts/collect_epoch.py](scripts/collect_epoch.py) and [scripts/collect_ietf.py](scripts/collect_ietf.py), are committed with this brief and fix every URL and rule.

## What this study is

A capture, not an analysis. Its product is a dated, replayable archive of public records that would otherwise be overwritten, with the questions a later study will put to it named now, so that study tests them on data neither it nor this one has analysed. This study reads its captures only to check that they are complete and well formed, and reports counts of what was kept, not findings.

## Part A, compute-market prices (lead L-0011): dropped

The lead named three free daily series: Silicon Data's H100 rental index, DRAMeXchange's DRAM spot prices and Shanghai Metals Market's Chinese GPU rental indices. Each source's own terms forbid what a capture needs, which is to keep the figures and publish the archive, since Lighthouse's repository is public. Read 8 November 2026, 19:00 to 19:08 UTC; the bodies were read once and are not kept (their hashes are in [data/before-the-brief/readlog.csv](data/before-the-brief/readlog.csv), the reasons in [withheld.csv](data/before-the-brief/withheld.csv)).

- **Silicon Data** (silicondata.com, terms of use): "No Site Content or any part thereof may be modified, reverse-engineered, reproduced or distributed in any form by any means, or stored in a database or retrieval system, without the prior written consent of Silicon Derivatives." Download is allowed only "for personal and non-commercial use". robots.txt allows all. The public H100 page shows about 30 daily values; "Full history" is in a paid portal, as scout 7 reported.
- **DRAMeXchange** (TrendForce, terms of use, 6.2): "YOU MAY NOT REPRODUCE, MODIFY, CREATE DERIVATIVE WORKS FROM, DISPLAY, PERFORM, PUBLISH, DISTRIBUTE ... ANY MATERIALS CONTAINED ON THE SERVICES WITHOUT THE EXPRESS PRIOR WRITTEN CONSENT". Its robots.txt address returned the site's 404 page. The front page shows only the current session.
- **Shanghai Metals Market** (metal.com, footer notice on its terms page): "you agree that you will not copy or reproduce any part of its contents (including, but not limited to, single prices, graphs or news content) in any form or for any purpose whatsoever without the prior written consent of the publisher." robots.txt allows a generic client. The 19 indices themselves appear only through its commentary articles; the index tables were not looked for behind its sign-in.
- **Substitutes checked and also refused by their terms:** Vast.ai's marketplace (its terms forbid "any robot, spider, crawler, scraper, script ... or any other automated method to access, query, copy ... store or extract data" and any use "to construct, publish, or maintain any index, benchmark, pricing-comparison service") and Microsoft's unauthenticated Azure Retail Prices API (the Microsoft APIs Terms of Use say you may not "Scrape, build databases or otherwise create copies of any data accessed or obtained using the Microsoft APIs, except as necessary to enable an intended usage scenario for your Application", nor redistribute it). Whether those API terms bind this particular unauthenticated API was not settled; under the keeper's caution of 8 November it is treated as a wall.

So no price is captured. Asking any of these publishers for consent would be contacting a third party, which waits for a person. Lighthouse may quote a single attributed figure from such a page in a dated sentence, as the sweep did; it will not keep a series. The cost strand therefore still has no price instrument.

## Part B, Epoch AI's AI data-centre records (lead L-0019)

**Source.** Epoch AI's "AI data centers" hub ([epoch.ai/data/data-centers](https://epoch.ai/data/data-centers)), its update log ([epoch.ai/data/ai-data-centers/updates](https://epoch.ai/data/ai-data-centers/updates)) and its downloads. The hub's citation section says: "Epoch AI's data is free to use, distribute, and reproduce provided the source and authors are credited under the Creative Commons Attribution license" (CC BY 4.0, linked). Credit: Epoch AI, 'AI data centers', published online at epoch.ai. robots.txt (read 19:00:18 UTC) disallows `/assets/` (except images and docs), `/inspect-viewer/` and a benchmark path, and allows the data paths used here. No account, key or sign-in is involved.

**What is published, as read before the brief** (pages kept in data/before-the-brief/, read 19:00:36 and 19:00:38 UTC): the hub says it covers 96 data centres and links seven downloads, the "All datasets" ZIP and the CSVs of data centres, timelines and chip quantities, each "Updated Nov. 6, 2026", a chip-types CSV (21 October) and two cooling CSVs (8 June and 20 January 2026). The update log page shows entries from 8 October to 5 November 2026 and a "See more" button; the same HTML carries, in its page data, 115 dated entries from 14 March to 5 November 2026. So the free history of the log reaches back about eight months as served today; whether entries drop off the end, and how far back the page's data goes on later weeks, is one of the questions below. Earlier states of the CSVs are not offered; the Wayback Machine was unreachable from this container on 7 November (scout 7) and is not used.

**Kept at each weekly read** (by `collect_epoch.py --read <label>`): robots.txt (checked first; a disallowed URL is skipped and logged), the hub page, the update log page, the documentation page, the ZIP and the three CSVs updated with it (data centres, timelines, chip quantities), each raw with URL, UTC start, status, type, size and SHA-256; and a derived `updates.csv` (date, section, site, change text) parsed from the log page's embedded data. About eight GETs a week.

**Unit.** A site (Epoch's "data center" record) at a weekly snapshot; a log entry.

## Part C, the IETF census of agent, discovery, bot-authentication and AI-preference drafts (lead L-0012)

**Source.** The IETF Datatracker's read-only API ([datatracker.ietf.org/api/](https://datatracker.ietf.org/api/), which describes it as an autogenerated read-only API needing no key for these endpoints) and the IETF 127 agenda. robots.txt (19:00:19 UTC) disallows only `/doc/pdf/`. Internet-Drafts are IETF Contributions under the IETF Trust Legal Provisions (5.0, listed as current on the Trust's page, read 8 November; the PDF itself was not opened); this census keeps metadata and abstracts, not the drafts' text. No use restriction on Datatracker metadata was found.

**The meeting.** IETF 127, San Francisco, from 14 November 2026 for 7 days, so its last day is 20 November (Datatracker's meeting record, read 19:08:49 UTC). By the same record the Internet-Draft submission cutoff is 13 days before the meeting at 23:59:59 UTC, which is 1 November, so new drafts and revisions were closed for the meeting before this brief was written and reopen when the meeting starts.

**The census rule, fixed here.** A draft (Datatracker document of type `draft`, any state) is in the census if either:
1. **Group stratum:** its group is one of `aipref` (AI Preferences WG), `webbotauth` (Web Bot Auth WG), `agentproto` (Agent Communication Protocols WG), `dawn` (Discovery of Agents With Names WG) or `audit` (Agent Use of Delegation and Interaction Traceability, a BOF), the groups with agent, bot or AI-preference charters that meet at IETF 127 by its agenda as scout 6 read it; or
2. **Name stratum:** its name contains any of `agent`, `aipref`, `ai-pref`, `webbotauth`, `web-bot-auth`, `botauth`, `bot-auth`, `crawler`, `robots`, `llm` or `-ai-`, or ends with `-ai`.

Each row records which strata and tokens matched. The name tokens catch drafts outside the five groups (for example individual drafts aimed at oauth or wimse) and also catch unrelated names (SNMP's AgentX, "user-agent" drafts); nothing is removed at capture. A later study classes rows by a rule it fixes before reading the abstracts it classes.

**Kept at each census** (by `collect_ietf.py --read <label>`): robots.txt; the meeting record and the plain-text agenda; the five group records; every page of each document query (one query per group, one per token), raw; the draft state table, to resolve state URIs; author records for every census draft (queried by document id in batches), kept with each author's email address replaced by a placeholder, which is the one deliberate departure from raw retention, so that Lighthouse keeps no personal contact data it does not need; and two baseline counts across all of Datatracker, drafts of any name whose last change falls in the 14 days before the read and in the 30 days before it (one GET each, `limit=1`, reading `total_count`). Derived: `census.csv` (one row per draft: name, revision, title, last change, expiry, group, states, intended level, strata and tokens matched) and `authors.csv` (draft, order, affiliation, country, person id). About 40 to 45 GETs a census, paced at one a second.

**Unit.** A draft at a census; an author line on a draft.

## What is already known of the outcomes

- **Epoch:** the writer looked at the hub page and the update log while reading the sources' terms: 96 data centres; the largest by compute on the hub's cards (Colossus 2 and OpenAI Stargate Abilene above one million H100-equivalents each by Epoch's estimates); the log's entries of October and early November, several of them upward revisions of power, compute and cost (for example Meta Aiken's projected compute raised from 78k to 147k H100e on 8 October, and the Anthropic-Amazon New Carlisle site's compute from 686k to 818k H100e). Scout 4 reported upward revisions at Anthropic Lake Mariner (31 October). Lighthouse runs on Anthropic's models, and Anthropic sites are in the data; they get no special treatment in any question below. The CSVs have not been opened.
- **IETF:** a probe with `limit=1` returned `total_count` 380 for drafts whose name contains `agent` (all years; its first row was a 2013 AgentX draft). The five groups' records were read: four active WGs and `audit` in state "bof"; the group records of `dawn`, `agentproto` and `audit` were last changed between 22 October and 6 November 2026. Scout 6 reported that over 20 `agentproto` drafts and about 20 `dawn` drafts were nearly all revised in the three weeks before 7 November, and that no web-bot-auth specification had been adopted as an RFC. No census has been taken.
- **The writer's expectation,** from the cutoff rule and not from data: few census drafts will change between 8 and 13 November; many will be revised or newly submitted in the days after 14 November.

## Clocks

Each capture is labelled with the UTC minute its collector starts. A value's change is dated to the interval between the last capture without it and the first with it. Epoch's own "Updated" dates and log dates are recorded as Epoch's. A draft's revision time is Datatracker's `time` field, which changes on any metadata change, not only on a new revision; the revision number is the stricter signal.

## Schedule, with end dates

- **Epoch, weekly, for at most 8 weeks:** read 0 on 8 November 2026 (with this brief), then reads on or within two days after 15, 22 and 29 November, 6, 13, 20 and 27 December 2026 and 3 January 2027. The last read is 3 January 2027 (window to 5 January). No read after that without a new brief or the keeper's extension.
- **IETF census:** census 0 on 8 November 2026 (with this brief); census 1 on 12 or 13 November, the last before the meeting; census 2 once after the meeting ends on 20 November, between 23 and 27 November 2026. No census after census 2.
- **Checkpoints:** 8 November 2026 (the first capture, [checkpoints/2026-11-08.md](checkpoints/2026-11-08.md)); 27 November to 1 December (after census 2, completeness of the three censuses and the Epoch reads to date); 4 to 9 January 2027 (after the last Epoch read: completeness, and the hand-over to a later study). Each says what was kept and what failed, not what the data show.

## Questions named for a later study

Each is to be tested by a later study, with its own brief fixed before it reads the captures, on captures from this study that no one has analysed. Under each, the comparison is named now.

**Epoch**
- **E1, does the log roll over?** Across the weekly captures, does the earliest entry carried in the update log page's data move later, and at what rate? (Unit: a weekly capture. Testable on reads 1 to 8; read 0's earliest date, 14 March 2026, is already known.)
- **E2, which way do estimates move?** Between consecutive weekly CSV snapshots, how many sites have a changed value of current or projected power, compute (H100e) or cost, and what share of changes are increases? Compared with the log's own entries for the same weeks. (Unit: a site-week; the log entries already read before 8 November are excluded.)
- **E3, is the log a complete record?** What share of value changes between CSV snapshots has a matching log entry dated within the same interval? A low share would mean the log is not, by itself, a history of the estimates.
- **E4, the tracked total:** the sum over sites of Epoch's current power and compute at each snapshot, and how much of any change over the window is new sites against revisions of existing ones.

**IETF**
- **I1, the meeting's pulse:** of census drafts, how many had a new revision or were newly submitted between census 1 and census 2, by stratum, against the same share for all Datatracker drafts in the same interval, from the baseline counts.
- **I2, adoption by a working group:** how many individual drafts in census 1 have a successor named `draft-ietf-<group>-...` (a "replaces" relation or a WG state) by census 2. Adoption by a working group is a step in a standards process, not deployment.
- **I3, who writes them:** the share of group-stratum drafts with at least one author whose stated affiliation is among the five most frequent affiliations in census 1, at census 1 and census 2, with affiliations normalised by a rule the later study fixes before reading census 2.
- **I4, what lapses:** how many census 1 drafts reach their expiry date by census 2 without a new revision.

A question these captures cannot reach is not answered by them; the later study says so.

## What the capture cannot show

- **A price is not a cost borne by shared infrastructure.** This study keeps no price, and had it kept one, a rental rate is what a buyer pays a provider, not what automated traffic costs an operator who never sold it anything.
- **Epoch's figures are estimates,** from satellite imagery, permits and public documents by Epoch's own description, of capacity being built. They are not measured power draw, not utilisation and not AI activity on the open internet; a data centre's compute is not load on shared infrastructure, and nothing here links a site to traffic anywhere.
- **A draft is not adoption.** An Internet-Draft is a proposal anyone may submit; a WG draft is a proposal a group has agreed to work on; neither is a standard, and neither is deployment. Counting drafts measures attention in a standards body, not what agents or bots do.
- **The name rule misses and over-catches.** Drafts on these subjects whose names carry none of the tokens and whose group is not one of the five are missing; drafts that carry a token by accident are in. Both are reported, not corrected, at capture.
- **Affiliations are as stated by authors,** often blank or inconsistent, and an affiliation is not an organisation's position.

## Missing evidence

A failed request is recorded with its status and is a missing observation, not a zero or a "no change". A page whose structure changes so that the derived table cannot be parsed keeps its raw body; the derived table for that read is marked partial. A URL that robots.txt disallows at a read is skipped and logged, and is not worked around. A refusal, challenge or rate limit is recorded as what the request saw and the read moves on; Lighthouse does not retry around it beyond one retry after a connection reset.

## Overlap

No earlier study reads Epoch AI or the Datatracker. Scouts 4, 6 and 7 read some of the same pages on 7 November 2026 for the sweep; their reads are not part of this archive. The pre-brief reads of 8 November (data/before-the-brief/) are kept and disclosed above; the Epoch pages among them are earlier copies of pages read 0 keeps again.

## Resources and stop

About 8 GETs a week to epoch.ai and 40 to 45 a census to datatracker.ietf.org, paced at about one a second, identified as `Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)`. No login, account, key, paid service, scan or contact with anyone. Collector runs are short; each checkpoint is a page. The study stops at its last scheduled read (3 January 2027) or earlier if a source's terms or robots.txt change to forbid a capture, in which case that part stops at once and the checkpoint says so. It is inconclusive for its own purpose (keeping the records) if more than two Epoch reads or any census fails; the checkpoints say which.

## Amendments

**0.2, 8 November 2026, 19:15 UTC, after census 0a (19:14) and before census 0 (19:15).** Census 0a (`data/ietf/raw-2026-11-08T1914Z/`, under rule 0.1) showed that Datatracker files a draft under a working group only once the group adopts it: the group stratum held 11 drafts (aipref 9, agentproto 1, webbotauth 1, dawn and audit none), while proposals aimed at a group are individual drafts filed under no group. Those aimed at `agentproto`, `aipref` and `webbotauth` carry a name token already; those aimed at `dawn` and `audit`, such as draft-seethiraju-dawn-dan, which scout 6 read, may carry none. So the name stratum gains the tokens `-dawn-` and `-audit-` and the suffixes `-dawn` and `-audit`, following the convention that an individual draft aimed at a group carries its acronym in its name. The decision was made after seeing the per-query row counts of census 0a and no revision dates, states or abstracts; `audit` will over-catch drafts on auditing in general, which the later study classes as it does the other over-catches. Census 0a is kept and disclosed; census 0, taken next under rule 0.2, is the baseline for the questions above. Question I3's "group stratum" is too small at 11 drafts to carry it alone: I3 is to be read on group-stratum drafts together with name-stratum drafts whose names carry one of the five groups' acronyms, a reading fixed here before census 0.
