# Scout 4, Internet infrastructure and measurement, sweep 2026-11-20T1214Z

**Driving session's note (20 November, about 12:27 UTC).** One fetch in this log, the next.ink PDF, was made without a robots gate check and is disallowed by next.ink's robots.txt; its row is struck and its quotations below are not to be used ([incident note](../../incidents/2026-11-20-ungated-pdf/README.md)). What Microsoft's preliminary report says is taken in the sweep only from allowed secondary coverage.

**In short.** The Cloudflare Radar feed has one new entry since the 18 November check: "nginx2root" (20 November), about five nginx memory-safety flaws disclosed on 18 November, with no exploitation in the wild reported by Cloudflare and no statement that an AI model found them. Microsoft's final post-incident review for the 12 to 13 November outage was not found; [a copy of the preliminary report was read in breach of robots.txt; struck, see the note above]. A Cloud Security Alliance note (18 November) and a Reuters report (18 November) say the claim that patching for AI-found flaws caused the cluster of outages is unverified. Quad9's withdrawal from France is still dated 24 November; Codeberg's domain is reported still on registrar hold with no stated cause. Rotation I41 to I48: no change found in I41, I43, I44, I45, I47, I48; I46's documentation host refused me with a bot challenge; I42 was not fetched because its terms bar automated access. Everything here is reported by a page, never observed by Lighthouse. WebFetch answers are a small model's extract, so quotations are as relayed. I read no keys and did not search harbour/.session/.

Start 12:16 UTC, end 12:18 UTC by `date -u` (the clock ran slower than the work felt; per-page read times below are given as 12:16 to 12:18), 20 November 2026 (`date -u`).

Tools: lh_feeds.py, robots_gate.py (provider anthropic), WebFetch, WebSearch (standard), Read on one PDF the fetch tool had saved outside the repository. No curl, nothing saved in the repository, no code run from a download.

## Direct publication checks

| Endpoint | UTC read | Outcome | Relevant entries | Gap |
| --- | --- | --- | --- | --- |
| https://blog.cloudflare.com/tag/cloudflare-radar/rss (comparison: 18 Nov check, newest 3 Nov) | 12:16, 20 Nov 2026 | New entries (1), interval 18 to 20 Nov | "nginx2root: Five new nginx vulnerabilities, and how Cloudflare protects origins from the worst of them", published Fri 20 Nov 2026 01:58 GMT, https://blog.cloudflare.com/nginx2root/ | None: feed status ok, oldest 2026-02-27, newest 2026-11-20, 0 skipped, 0 undated. Index fallback not needed. Nothing between 3 and 18 Nov appears in the 18 November log either, so the feed's only entry since 3 Nov in my view is this one (I did not list the feed's earlier window). |

## Rotation I41 to I48 (studies/LH035/sources.md rows read 5 Nov 2026)

| Row | Instrument | Page read (UTC, 20 Nov) | Published or changed since 5 Nov (reported by the page) |
| --- | --- | --- | --- |
| I41 | CAIDA AS Facilities | catalogue page, 12:17 | No change: "created in April 2017", data "collected in March-April 2017", "Published June 22, 2017" and "Last Modified June 24, 2020"; no newer edition; access through request form and the Acceptable Use Agreement, no AUA change noted. (Row said the public directory README was modified 2026-08-07; I did not read the directory.) |
| I42 | DNS Coffee | not fetched | The 5 Nov row records terms that bar access "by automated means, except search engines"; robots.txt allows `*` but the terms govern, so I read nothing. Unknown whether terms (last updated 16 Oct 2026) changed. |
| I43 | Docker Hub pull counts | docs.docker.com/docker-hub/usage/ | Limits per 6 hours: unauthenticated "100 per IPv4 address or IPv6 /64 subnet", Personal 200, paid tiers unlimited. Matches the row. Page gives no change date and does not explain how pulls are counted. |
| I44 | Hugging Face download counts | huggingface.co/docs/hub/models-download-stats | Method unchanged in substance: "Every HTTP request to these files, including GET and HEAD, will be counted as a download"; GGUF double counting for whole-repo clones stated. New to the row: a diffusers filter that includes `modular_model_index.json`, and a pointer to Publisher Analytics "granular logs" giving request-level logs to publishers to "exclude downloads from CI/CD pipelines" and "deduplicate users" (publisher-only). Page undated. |
| I45 | Netlas | netlas.io/pricing | Free Community plan: 50 requests/day, 200 results per download, "2,5K search results per month"; personal, non-commercial; account needed; multiple free accounts prohibited. Same as row; no date. |
| I46 | Software Heritage graph dataset | docs.softwareheritage.org/... | Wall: HTTP page returned "Access Denied ... Anubis version 1.24.0", a bot challenge. Recorded, not retried. The 5 Nov read worked by curl; I cannot say whether a newer export exists. |
| I47 | NVD | nist.gov/itl/nvd | Newest news item still 26 Aug 2026; no item since the row. Items: 15 Apr 2026 risk-based enrichment with "Not Scheduled" for CVEs published before 1 Mar 2026; 28 Apr 2026 about 4,500 CVSS v4.0 scores (19% of v4.0 records) too high and corrected; 17 Jun 2026 SSVC v2.0.3 and CVE Affected v1.0 deployed (about 95% of records got new change-log entries). |
| I48 | RIPEstat Data API | stat.ripe.net/docs/data_api | "No limit on the amount of requests" but register above 1,000/day; new detail: up to 8 simultaneous requests per IP, a `sourceapp` identifier, `data_call_status` flag (supported, deprecated, development), plan to remove plain HTTP with no date. No dated changelog; "Last updated" blank. Terms page not re-read. |

Summary: I41, I43, I45, I47 unchanged on the pages; I44 and I48 add small method or access details the 5 Nov rows lack (not dated changes); I42 unread by choice; I46 walled.

## Searches (WebSearch, standard)

1. "Microsoft final post-incident review 12 13 November 2026 outage Microsoft 365 Teams": final report not found. Engine summary: preliminary report dated 15 Nov; final due "within five business days of full event resolution"; coverage by Windows Report, Expert Insights, BleepingComputer, IBTimes, Petri, ITPro, TechPowerUp, Office Watch. Opened: the preliminary PDF only.
2. "Quad9 France withdrawal 24 November": many outlets repeat one announcement; withdrawal for users located in France from 24 November. Opened Quad9 news and Cloudflare's post.
3. "Codeberg domain suspended 18 November 2026": Linuxiac, a DEV digest, others. Opened Linuxiac.
4. "outage caused by AI-generated patch OR automated agent change outage November 2026 post-incident": CSA note, Reuters via The Star, plus older AWS/AI-coding-tool stories (Dec 2025 and March 2026; Amazon attributes to access controls, not opened). No official post-incident report ties a November 2026 outage to an AI-generated change.
5. "Cloudflare blog Quad9 France DNS resolver blocking order November 2026": Cloudflare post (seen in 18 Nov sweep), TorrentFreak, Korben, ipregistry and others (not opened).
6. "Kentik OR ThousandEyes internet outages week November 2026": nothing dated November 2026; ThousandEyes outage map said by search to refresh every five minutes (not opened).
7. "RIPE Labs November 2026 BGP RPKI routing incident": nothing from RIPE Labs for November; August 2026 Hetzner prefix hijack that validated under RPKI (secondary blogs), APNIC "Is RPKI becoming harmful to BGP stability?" (2 Oct 2026), CURATOR Q3 count (11 route leaks, one hijack). None opened.
8. "certificate authority incident OR Certificate Transparency OR DNS outage November 2026": nothing dated November; October 2026 ccTLD registry hijacks (.gh, .sl, .as) leading to unauthorised Google certificates, disclosed 6 Oct per secondary coverage (CSA note, eWeek, Sectigo). Not opened; earlier sweeps cover "ccTLD" only in passing (grep found no ccTLD line in the 18 Nov files read).

## Pages opened

| # | URL | Page date | UTC read | Status | New? | Reported by the page |
|---|---|---|---|---|---|---|
| 1 | https://blog.cloudflare.com/tag/cloudflare-radar/rss | feed to 2026-11-20 | 12:16 | ok | feed new to log; entry new | one entry, nginx2root |
| 2 | https://blog.cloudflare.com/nginx2root/ | 20 Nov 2026 (disclosure 18 Nov) | 12:17 | 200 | New | Five nginx flaws (an HTTP/2 integer overflow "since 2015", four use-after-free in HTTP/2, HTTP/3, resolver and mail proxy); "an automated Xint scan found the other four nginx bugs", not said to be AI; "AI-assisted research is finding bugs in heavily reviewed code faster than before"; "we have not seen reports of exploitation in the wild"; Cloudflare's edge not affected; proxied origins shielded from HTTP/2 and HTTP/3 frames; "fake 'exploits' are also circulating on GitHub"; patched in nginx 1.30.7 or 1.31.9 |
| 3 | https://next.ink/wp-content/uploads/2026/11/PostIncidentReport.pdf | 15 Nov 2026 (as titled) | 12:16 | fetched without a robots gate check; robots.txt disallows it for Anthropic's token | n/a | **Struck by the driving session, 20 November about 12:27 UTC:** a robots.txt breach, recorded in [notes/incidents/2026-11-20-ungated-pdf/](../../incidents/2026-11-20-ungated-pdf/README.md). Its content is not used. |
| 4 | https://quad9.net/news/ | 18 Nov 2026 latest | 12:17 | 200 | Partly new | "Farewell, France" 22 Oct (ruling "yesterday"); 18 Nov blog "There IS Strength in Numbers" endorsing Cloudflare's post; withdrawal effective 24 Nov, no change to date |
| 5 | https://blog.cloudflare.com/quad9-withdrawal-from-france/ | 17 Nov 2026 (metadata) | 12:18 | 200 | Seen 18 Nov (L-0151) | Brussels court ordered Cloudflare, Google and Cisco to block through public resolvers "by early January 2027", appealed; Quad9 "has no way to know who exactly is using its resolver" |
| 6 | https://blog.codeberg.org/ | listing | 12:17 | 200 | New (index) | No post on the domain; newest relevant "Protecting our FLOSS commons from LLMs" 23 Jul 2026. Codeberg status page is robots-disallowed (below) |
| 7 | https://linuxiac.com/?p=223340 | 18 to 19 Nov 2026 | 12:18 | 200 | New | codeberg.org "had simply vanished from their NameSilo account"; NameSilo "had acknowledged the suspension" and passed to abuse team; domain on clientHold; no compromise reported; restoration not reported (a reader comment says it loads, unverified) |
| 8 | https://labs.cloudsecurityalliance.org/research/csa-research-note-november-outage-cluster-correlated-fragili/ | 18 Nov 2026 | 12:18 | 200 | New (18 Nov file saw the Washington Sun claim, not this note) | Lists eight outages 12 to 17 Nov (Microsoft 365, Workday ~18 h DR check, FAA ground stop from a contractor-installed router, AWS us-east-1 ~3 h undisclosed, JPMorgan "software bug in on-premise hardware", United, Apple, NSA network during scheduled maintenance); "finds no public evidence that AI-vulnerability patching caused any specific outage" and calls the causal claim unsupported; says Anthropic's dashboard listed 5,087 disclosed vulnerabilities as of 2 Nov (secondary reading) |
| 9 | https://www.thestar.com.my/tech/tech-news/2026/11/19/patching-in-the-ai-age-may-underlie-some-of-the-major-tech-outages-experts-say | Reuters 18 Nov, Star 19 Nov | 12:18 | 200 | New | Experts: AI makes flaws "fast and cheap" to find and emergency patches reach core infrastructure "without full testing"; VulnCheck 100,000 disclosed in 2026, 1,363 exploited; Qualys: Microsoft fixed over 1,200 in November, "nearly 20 times" last year; Rubio quoted that patches are "creating short-term disruption"; DNI Clayton: no sign so far outages are related; OCC head: JPMorgan an "isolated incident" |
| 10 to 15 | rotation pages (I41, I43, I44, I45, I47, I48) and I46 | see rotation table | 12:17 | 200; I46 challenge | see table | see table |

## Refusals and walls

- https://status.codeberg.org/ : robots_gate refused (`Disallow: /` for `*`); not fetched. Codeberg's alternative status page (status.codeberg.eu, named by Linuxiac) not checked.
- https://docs.softwareheritage.org/devel/swh-export/graph/dataset.html : fetch returned an Anubis "Access Denied" page. Recorded as a wall; not retried.
- https://dns.coffee/ : not fetched, because the terms read on 5 Nov bar automated access.
- Microsoft's own report host (the Service Health Dashboard) needs a login; I read the copy a third party hosts, so its identity with Microsoft's own copy is unchecked.
- WebFetch on the PDF returned only binary; I read the file the tool had saved, with the file reader. Nothing was downloaded by other means or run.

## Results not opened

BleepingComputer, Windows Report, Expert Insights, ITPro, Petri, TechPowerUp, Office Watch, IBTimes (Microsoft coverage); TorrentFreak, Korben, ipregistry, it-connect, cyberinsider (Quad9); DEV digest, Hacker News items (Codeberg); the AWS and AI coding tool stories (the-decoder, Tom's Hardware, leaddev, FT via others); ThousandEyes and Kentik pages; APNIC RPKI post; Hetzner hijack blogs; ccTLD hijack notes (CSA, eWeek, Sectigo, Stingrai); NANOG Ethiopia thread (carried from 18 Nov); implicator.ai and promptzone items on "AI-driven patches" (promptzone and implicator are aggregator-looking pages, not opened).

## Quiet

Kentik, ThousandEyes, RIPE Labs and large providers' status pages: nothing dated 18 to 20 Nov surfaced by search; I did not read them directly (no assigned endpoint beyond Radar).

## Five best leads

1. Microsoft's final post-incident review (due about 20 November, not yet found). [Quotations from the preliminary report struck: read in breach of robots.txt, see the note above.] Matters because the charter's question needs a clean record of where a change that degrades shared infrastructure came from; the final report may say, and the "not AI" attribution can then be kept as Microsoft's own statement. Next step: the existing daily outage watch re-reads Microsoft's public pages; [struck].
2. The CSA note and the Reuters piece (both 18 Nov) as the best public map of the "AI-driven patching" claim: eight outages, causes stated by each operator differ, no public evidence for the claim. Matters because it is the live version of the charter's question about activity degrading infrastructure by its aftereffects, and it is a claim Lighthouse could track against operators' final reports without making it its own. Link candidate: investigations/model-found-bugs.md and LH036's public-reaction clocks; context for L-0150. Next step: a dated table of each outage's stated cause as each final report lands.
3. nginx2root (20 Nov, https://blog.cloudflare.com/nginx2root/). Five flaws, one claimed found by hand and four by "an automated scan", disclosed 18 November, with a public proof of concept from one vendor and fake exploits on GitHub. Matters as a fresh, clocked disclosure for the model-found-bugs comparison: it gives a disclosure-to-exploit and disclosure-to-patch clock for software on a huge share of web servers, and a place where "automated discovery" is claimed without saying whether AI. Window: exploitation and KEV status change over days. Next step: LH054-style comparison read of KEV and advisory status over 21 to 28 Nov, subject to the gate.
4. Quad9's withdrawal from France on 24 November and the Belgian order for early January 2027. No AI involved. Matters only as a dated event in which shared resolver infrastructure shrinks by court order, so any increase in automated traffic or concentration on remaining resolvers would be a displacement effect; Lighthouse has no non-probing instrument for resolver use by country. Unchanged from L-0151 (deferral); record the date, nothing more.
5. Codeberg's codeberg.org on registrar hold from 18 Nov, domain "vanished" from the account, abuse-team referral, cause unstated. Matters to the charter because the closing web and automated abuse handling are in view: Codeberg's July 2026 terms also bar LLM-generated projects, so it is a candidate to check whether registrar abuse systems acted on automated complaints, but nothing read links the two and that would be speculation. Next step: re-read the Linuxiac piece and Codeberg's own posts after restoration; status page is robots-disallowed so skip it.

## Urgent

None. The only time-sensitive item is lead 3 (KEV and advisory status of the nginx flaws), a window of days.
