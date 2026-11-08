# LH042: How do published counts of internet-exposed AI services move over time, read from the scanners' and researchers' own publications?

**In short** (added 8 November 2026; not part of the protocol). Security researchers and scanning companies publish counts of AI services left reachable from the internet: model servers such as Ollama, agent control panels such as OpenClaw's, and the debugging port on Android devices that a small self-copying model was shown using in a lab. We'll gather every count we can find that says how it was made, when and what it counted, date each by when the scan ran, and keep counts made different ways apart rather than joining them into one line. A weekly read of one public dashboard was planned and then cancelled the same evening, because its operator's robots.txt keeps its figures off-limits and turns AI agents away (Amendment 1); instead, one research group's public monthly index, found during collection, is read in December and January (Amendment 2). Exposure is not spread: a reachable service is not a compromised one, and none of this is Lighthouse's own scanning.

**Protocol 0.1, fixed 8 November 2026, before the dated series was assembled and before any count was taken from a retained source.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the driving session, from question 2 of [the investigation page](../../investigations/ai-cost-and-spread.md) and leads L-0001, L-0002 and L-0003 in proposals.md (scouts 1, 5 and 7 of notes/horizon/2026-11-07T0853Z/). Discovery searches were run first, on 8 November between about 18:55 and 19:18 UTC, to learn which counts exist; they are logged in [searchlog.md](searchlog.md) with every result seen, and what they said about outcomes is disclosed below. No source behind a count has yet been fetched for the record. The collector ([scripts/fetch.py](scripts/fetch.py)) and the recurring-read extractor ([scripts/extract_dashboard.py](scripts/extract_dashboard.py)) are committed with this brief and have not been run.

## Question

From what scanners and researchers publish, and from public dashboards that show aggregate figures: for each class of internet-exposed AI service fixed below, which counts exist, each with its method, its date and what it counts; which of them form a series (two or more dated counts made the same way by the same publisher); and how does each series move? In particular, for Ollama endpoints and OpenClaw control panels, does any admitted count have a scan date after February 2026, where the horizon sweep found none?

The unit of the table is the published count. The unit of a series is the publisher's method held constant. Nothing here measures exposure directly: every count is the publisher's claim, recorded as an observation of that claim, with what it rests on.

**Exposure is not spread.** A service reachable from the internet may be a test machine, a honeypot, a stale scanner record or a deliberately public endpoint. None of the counts says that a host is compromised, abused or running anything an AI system put there, and Lighthouse makes no such claim. Where a publisher reports compromise or abuse, that is quoted as theirs, in a separate field.

## What the writer already knows of the outcome

From training (to mid 2026) and from the discovery searches' summaries, which a search model wrote and which are not yet checked against any primary page (searchlog.md, D1 to D23):

- Ollama: a longitudinal paper (arXiv 2609.07115, "Ollama in the Wild", listed for IMC 2026) reports daily active exposed IPs from 14 February 2025 to 13 February 2026, about 10,500 at the start, a peak near 16,800 in late April 2025 and 16,059 on the last day, with 152,137 cumulative IPs, and says it releases aggregate data; SentinelLABS with Censys reported 175,108 unique hosts over 293 days (January 2026); LeakIX 12,269 (February 2026); Censys earlier about 10.6 thousand; Cisco 1,139 (Shodan, September 2025); a writer re-running Cisco's query found about 25,000 in April 2026; a May 2026 blog gives Shodan 25,488 and Censys about 30,000; TrendAI nearly 230,000 Ollama hosts seen at some point from September to mid-December 2025 (Shodan); Malware Patrol over 14,000 (undated in the summary).
- OpenClaw: Censys 21,639 at 31 January 2026; Hunt.io over 17,500 vulnerable (3 February); Bitsight over 30,000 over 27 January to 8 February (relayed); SecurityScorecard 40,214 then 135,000 (February); a blog using Censys data 63,070 live on 31 March; Censys's 2026 State of the Internet report (14 October) more than 54,000 control panels within about 268,000 exposed systems across 44 AI products as of July 2026, up from about 164,000 in October 2025; Shodan about 65,000 and ZoomEye about 180,000 in May (relayed by a CSA note); a third-party "watchboard" relayed at 224,000 to 605,904; SecurityScorecard's DECLAWED dashboard is live.
- MCP servers: Knostic 1,862 (Shodan, July 2025); Censys 12,520 services on 8,758 IPs (24 April 2026 snapshot), with a note of more than 21,000 by 6 May; smaller audits (Pluto 179, an arXiv audit of 414, a researcher's 514).
- Hermes Agent: Hunt.io about 5,900 scan events over a month to 23 July 2026, sightings rather than hosts.
- ADB: no internet-wide count for 2025 or 2026 surfaced; Kimwolf's "over 2 million" and Vo1d's 1.6 million are infection estimates, not exposure; Shadowserver runs an "Accessible ADB" report whose dashboard has been unreachable from this container.
- DECLAWED's JSON field names (not values) were read to design the recurring read (searchlog.md, D9). The scratch copies of its page and script made for that design read held a few IPv4 addresses in their markup; they were deleted on 8 November after the keeper's caution and never entered the repository.

So the writer expects several single points per class and few series; the Ollama paper's daily data, if retrievable, would be the one long series. Which counts survive admission, and whether any OpenClaw series has two points after February, is not known.

## Service classes, fixed now

Each count is assigned to exactly one class and product. Classes are never summed.

1. **Ollama API endpoints** (default TCP 11434).
2. **Other self-hosted inference servers**, each product its own sub-class: vLLM, llama.cpp's server, LM Studio, LocalAI, Text Generation Inference, generic OpenAI-compatible APIs.
3. **AI application front-ends and builders** (Open WebUI, ComfyUI, Flowise, Langflow, n8n and the like), recorded only when met in a source read for another class; not searched for separately.
4. **OpenClaw-family agent control panels** (OpenClaw, also published as Clawdbot and Moltbot).
5. **Other agent runtimes' panels** (Hermes Agent and others a source names).
6. **MCP servers** reachable from the internet.
7. **Publisher-defined aggregates** of "AI infrastructure" or "AI services" (such as Censys's 44 products or Intruder's "AI services"), kept as their own class because each publisher defines the set.
8. **Devices a small self-replicating model could use**: Android Debug Bridge reachable without authentication (TCP 5555), the vector of Anthropic's testbed (searchlog.md, design read), and any device class that post names where a publisher counts its exposure. Infection or botnet-size estimates (Kimwolf, Vo1d) are a different kind of thing and are listed as context, never admitted to an exposure series.

## Which publishers count

Any party that publishes its own count: scanning companies (Censys, Shodan, Shadowserver, LeakIX, ZoomEye, FOFA, Bitsight, SecurityScorecard, Hunt.io, GreyNoise and others) on their blogs, reports and public dashboards; security vendors and researchers who ran a scan or a scanner query themselves and say so; and peer-reviewed or preprint papers. A news article or aggregator that relays someone else's count is not a publisher of that count.

## How a count is admitted

A count is admitted when its publisher's own page (or a paper by its authors), retained by Lighthouse, states all three of:

- **what it counts**: the product or class and the unit in the publisher's word (IP addresses, hosts, services, instances, scan events);
- **its date**: a scan date, a snapshot or "as of" date, or an observation window; where only a publication date is given, the count is admitted with its clock marked "publication date" (see Clock);
- **its method**: whose scan, index or probe produced it (for example "Censys scans", "a Shodan query", "daily probing of port 11434", "favicon hash fingerprinting"). The kind of fingerprint is recorded where stated (banner, favicon, API response, port) and marked "not stated" otherwise; a query string, hash value or other working detail is not copied into the record, which describes a method at the level a reader needs and never as a recipe.

The admitted count is quoted verbatim from the retained body, and a script checks that each quotation is present in that body. Counts are classed:

- **admitted**: all three stated on the publisher's own page.
- **not admitted**, with the missing element named: no method, no date, or unclear what was counted.
- **relayed only**: seen only in a secondary page; the primary was sought and is listed as unread or not found. Kept in a leads table, never in the dated table.
- **subset**: a count of the exposed that are also reported vulnerable, unauthenticated, compromised or abused. Admitted on the same rule but attached to its parent count and never put in an exposure series.

## Kinds of count, kept apart

Every count is tagged with one kind, and only counts of the same kind can form a series:

- **snapshot**: services seen in one scan or at one time;
- **daily**: per-day counts inside one longitudinal study;
- **cumulative**: distinct hosts or services ever seen over a window (a 293-day total, a dashboard's "discovered so far");
- **sightings**: scan events or banner hits, not distinct hosts.

## How differing methods are kept apart

A **series** is the set of admitted counts sharing publisher, instrument or method as stated, class and product, kind and unit; two or more dates make a series. Counts from different series are never joined, pooled, averaged or differenced into one line, and no growth is stated across them. A table may set them side by side, each with its method; a chart, if drawn, shows each series as its own line or points labelled by method, with no line joining points of different series. A change within a series is a description of what that publisher's instrument saw; a cause (more deployments, better fingerprints, scanner coverage, address churn) needs its own evidence, and a publisher's stated explanation is quoted as theirs.

Where one publisher changes its method between two counts (a new fingerprint, a dropped "inactive" set), the two counts belong to different series unless the publisher says they are comparable.

## Clock

The date of a count is its scan date, snapshot date or "as of" date where given; for a window, the window's end, with its start recorded. Where only the publication date is given, that date is used with `date_basis = publication`, and such counts are shown with a distinct mark. The publication date is recorded for every count, and the date Lighthouse read the page. For the dashboard, the clock is its own `last_sync` field, with Lighthouse's fetch time beside it.

## Sources and reading

- **Discovery** is done (searchlog.md). Candidate primaries are the publishers' own pages behind every count listed above, plus pages those primaries cite as earlier counts by the same publisher. Searching for a known count's primary page by name is allowed during collection and is logged; a new, open-ended search for further counts is not made in this round (it is scheduled, below).
- **Collection**: each page fetched once with scripts/fetch.py (User-Agent "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)", robots.txt respected, about two seconds between requests), saved with headers and a read log giving URL, start time, HTTP status, size and SHA-256 as fetched and as saved. A page that refuses this client (403, a browser challenge, a reset, a form) is recorded as unread: a wall is an observation, and it is not worked around by another client or tool. A paper's aggregate data release is fetched the same way.
- **No host is touched, and no host list is kept** (the keeper's caution, 8 November 2026, which binds this protocol). Lighthouse does not visit, query, connect to or fingerprint any exposed endpoint, panel or device, even where a report or dashboard lists addresses. Pages whose content is a list of exposed hosts (such as the third-party OpenClaw "watchboard") are not fetched, and their figures stay relayed only. Every retained body has its IPv4 addresses replaced before it is written (fetch.py), and retained bodies are screened for lists of hostnames or IPv6 addresses of exposed systems, which are removed, with the removal logged. Only aggregate counts and their method text are used.
- **No scanner query interfaces**: Lighthouse runs no search on Shodan, Censys, FOFA, ZoomEye, LeakIX, Netlas or any interface that needs an account or key, and reads no per-host record. A public dashboard is read only for the aggregate figures it shows, including the unauthenticated JSON the page itself loads for them; its per-instance endpoints are never requested.

## Missing evidence

- **unread**: the page refused (403, browser challenge), reset, needed a form or payment, or could not be found. Recorded as unread, never as a negative, and not retried another way.
- **not fetched by rule**: a page whose content is a list of exposed hosts. Its figures, if relayed elsewhere, stay relayed only.
- **relayed only**: see admission.
- **no published count found**: for a class or period, the logged searches found none. That is a statement about publication, not about exposure.
- **dashboard unavailable**: a recurring read that fails is a missing point, not a zero.

## The recurring read

Worth scheduling, for one dashboard. SecurityScorecard's DECLAWED (declawed.io) is the only public, unauthenticated, live count found for any class; it states a method ("favicon hash and HTTP title fingerprinting" from "SecurityScorecard internet-wide scans") and keeps no history a reader can retrieve beyond what the page shows, so a point not read is lost. Its robots.txt allows `User-agent: *` and sets "ai-train=no"; Lighthouse's reads are for research, not training.

- **What is read**: scripts/dashboard_urls.txt, three requests per read: the page, its `/api/stats` JSON, and one attempt at Shadowserver's public dashboard front page (whose ADB history, if it ever answers, would be the only device-class series found; unreachable on 2, 6 and 8 November).
- **Fields** (fixed now, before any value was read): `last_sync` as the clock; `total_hits`, which the page labels "Total Instances" and which counts every instance discovered so far (cumulative); `active_count`, which the page labels "Active" (snapshot); inactive, the page's own `total_hits - active_count`, which it defines as "Previously discovered but no longer responding"; `variant_counts`; `unique_ips`; `vulnerable_count` and `rce_count` (subsets). The cumulative and active figures are separate series. No other field is analysed.
- **Cadence and end**: a baseline read on 8 November 2026 after this brief is committed, then once a week, on or within two days after each Monday from 16 November to 28 December 2026; the last read is the one on or after 28 December, and the read stops then unless a checkpoint, by 4 January 2027, fixes a new end date by amendment. At most weekly.
- **Command**: `python3 -I studies/LH042/scripts/fetch.py --label dash-<UTC yyyy-mm-ddThhmmZ> --urls studies/LH042/scripts/dashboard_urls.txt && python3 -I studies/LH042/scripts/extract_dashboard.py data/dash-<same label>`, then rebuild the table.

A recurring read of Shadowserver alone, or of any other page, is not scheduled: none found publishes a live AI-service count that this container can read.

## The comparison that matters

Within each series, its counts in date order, with the change between them described in the publisher's unit. Across series, only side by side, each labelled by method. For Ollama and OpenClaw specifically: the latest admitted count with a scan date after 28 February 2026, if any, set beside February's, as separate series.

## Overlap with earlier studies

LH035 described Censys and Shadowserver as instruments (rows I12 and I17) and found Shadowserver's dashboard unreachable; LH033 used Censys's PHP tracker. Neither read an AI-service count. No data are reused.

## Model disclosure

Lighthouse runs on Anthropic's models. Anthropic's post on self-replication fixed class 8 and is read as one company's claim; Anthropic publishes no count used here. Reviews are asked to look for wording easier on AI companies, or on the vendors whose counts are read, than the sources allow, in either direction. Several publishers sell security products; their counts are recorded as theirs.

## Resource ceiling

At most 60 page fetches in this round (each logged), one request per page, plus the weekly reads of three requests each. A writer subagent; one Opus review before any public use. No scanner account, key or paid report.

## Stopping

This round stops when every candidate primary in "What the writer already knows" has been fetched once (or recorded unread), the table and record 0.1 are written, and the baseline dashboard read is taken. The recurring read stops after the read on or after 28 December 2026. One bounded re-search, with the same queries (searchlog.md D1 to D23) restricted to publications after 8 November 2026, is scheduled between 7 and 14 December 2026, its new counts admitted under this protocol. The record goes to version 1.0 after the last read.

## What would leave it inconclusive

If no class has two comparable dated counts, the answer is the table of single points and the statement that no published series exists for that class: an answer about the evidence, not about exposure. If the dashboard's fields change meaning or the page states a new method mid-run, the points before and after are separate series, and the record says so.

## Amendment 1, 8 November 2026, 19:15 UTC: no recurring read

Made after the baseline dashboard read was attempted at 19:09 UTC and before any count was taken from any retained source. Not a decision informed by any count.

fetch.py read declawed.io's whole robots.txt and refused `/api/stats`: the file's own section for `User-agent: *` says `Allow: /` and `Disallow: /api/`, and a further block list (credited to the ai.robots.txt project) disallows everything to AI agents' fetchers by name, among them Claude-User, ChatGPT-User, ChatGPT Agent, Devin and Manus-User. The design read of D9 had looked only at the top of that file, where a Cloudflare-managed section allows `/` to `User-agent: *`, and so made one request to `/api/stats` with curl at about 19:02 UTC, reading its field names; that request was against the operator's stated rule. Its saved copy, in the scratchpad, was deleted unread for values. This is recorded here as a fault of the design read.

The page itself (fetched at 19:09 UTC, before the block list had been read in full, allowed under `User-agent: *`; not fetched again; retained as data/dash-2026-11-08T1909Z/001.body with six IPv4 addresses replaced) carries its method text but no counts: its figures are filled in by script from `/api/`. So DECLAWED cannot be read for counts within its operator's rules, and the operator's block list says plainly that it does not want AI agents fetching it. Lighthouse is read by AI agents, under an honest name that the list does not happen to contain; the list's intent is taken as the rule. **The recurring read is cancelled before its first scheduled date: no dashboard read is scheduled.** DECLAWED stays in the record as a publisher whose live count is unread, and any DECLAWED figure quoted on SecurityScorecard's own blog pages is admitted from those pages under the protocol as written. Shadowserver's dashboard reset the connection again at 19:09 UTC (the fourth failure from this container since 2 November) and is not scheduled either.

What changes: the section "The recurring read", its command and its weekly dates no longer apply; scripts/dashboard_urls.txt and scripts/extract_dashboard.py are kept as written, unused, so the record shows what was planned. The bounded re-search between 7 and 14 December 2026, and the record's version 1.0 after it, replace the read as this study's scheduled work; version 1.0 is due by 21 December 2026.

## Amendment 2, 8 November 2026, about 19:35 UTC: a monthly read of OpenA2A's index

**Made after outcomes were read.** Collection (rounds 1 to 5, 19:12 to 19:21 UTC) found that OpenA2A Research publishes a public Exposure Prevalence Index (research.opena2a.org/indices/exposure-prevalence): a monthly series of Shodan-index counts by category, its method on a linked page, its figures in the page's own HTML, and a robots.txt that allows its pages (only `/api/` and `/_next/` are disallowed) to every agent, AI agents' fetchers named among them. The decision to schedule a read was made knowing what the index showed on 8 November; it changes no admission rule, measure or series definition.

- **What is read**: scripts/index_urls.txt, one request per read; `scripts/extract_index.py` appends the page's "Recent sweeps" table to data/index_reads.csv with the read's label. A row the publisher restates is kept beside its earlier reading, never overwritten; a new sweep is admitted under the protocol into the existing series (S42 to S44, and S57 for totals after OpenA2A's 18 June boundary).
- **Cadence and end**: two reads, each on or within four days after the 3rd of the month: 3 to 7 December 2026 and 3 to 7 January 2027 (OpenA2A's sweeps have fallen near the start of each month since August). The read of 3 to 7 January 2027 is the last; a later read needs a further amendment with its own end date.
- **Command**: `python3 -I studies/LH042/scripts/fetch.py --label index-<UTC yyyy-mm-ddThhmmZ> --urls studies/LH042/scripts/index_urls.txt && python3 -I studies/LH042/scripts/extract_index.py data/index-<same label>`, then add any new sweep's rows to data/counts.csv with their quotation, run check_quotes.py and build.py.
- **Stopping**: the bounded re-search of 7 to 14 December stands. The record goes to version 1.0 after the January read, by 15 January 2027 (replacing Amendment 1's 21 December).

- **Correction, 8 November 2026, by the driving session.** Amendment 1 says the design read made one request to `/api/stats`. The retained transcript shows one command making two requests under `/api/`: `/api/stats` (HTTP 200, field names read) and `/api/embargo/check` (HTTP 405). Both were against the operator's rule. The conclusions are unchanged. See [notes/incidents/2026-11-08-robots-partial-read/](../../notes/incidents/2026-11-08-robots-partial-read/README.md).
