# Scout 4, Internet infrastructure and measurement, run 2026-11-10T1415Z

Started 2026-11-10T14:19Z, ended about 2026-11-10T14:30Z. Read times are approximate (all 14:20 to 14:28 UTC on 10 November 2026; the one checked clock reading was 14:20:59). WebFetch answers are a small model's extract of the page, not raw text, so quotations are as the extract gave them. Every URL passed scripts/robots_gate.py before it was fetched.

## Searches

1. "Chrome Certificate Transparency log shutdown OR retired OR new log November 2026": ct-policy list threads (Let's Encrypt logs read-only 30 Nov 2025, shut 28 Feb 2026; DigiCert 2024 and 2025 shards shut early June 2026; Tuscolo2025h2 decommissioned January 2026), DigiCert knowledge base, vendor blogs. A rule that logs submitted for inclusion serve an updated JSON schema from 1 November 2026 (secondary). Nothing dated November 2026 about a log shutdown. Not opened.
2. "CAIDA telescope OR Ark dataset 2026 new release backscatter AI scanning": CANIS project and proposal, ITDK-2026-03, CAIDA 2025 annual report, a poster. Opened the CANIS page and ITDK release page; the others not opened.
3. "RIPE Atlas November 2026 probes anchors announcement": APNIC and RIPE Labs "A day in the life of RIPE Atlas" (April 2026), RIPE Atlas UI notices (15 July, 10 August 2026), a status notice of a controller upgrade. Nothing dated November 2026. Not opened.
4. "Cloudflare Radar AI bots crawl-to-refer November 2026 OR Zero Wire OR agents Radar new dataset": 2025 and early 2026 Radar AI-crawler posts and third-party summaries. No November Radar dataset beyond what the blog index showed. Not opened.
5. "Tranco OR CrUX ranking change 2026 top sites list AI crawlers manipulation": vendor blogs measuring AI-crawler blocking on the Tranco top 100,000 (18.5% on 9 June to 19.4% on 7 August 2026, per one vendor); nothing on Tranco or CrUX changes. Not opened.

## Sources read

| # | URL | Read (UTC) | Status | Page date | Claim reported | New? |
|---|---|---|---|---|---|---|
| 1 | https://developers.cloudflare.com/radar/release-notes/ | 10 Nov ~14:20 | 200 | page "Last updated Apr 20, 2026"; one entry 26 Oct 2026 | Radar fixed a Markdown for Agents savings bug: the metric "included conversions not served to AI bots or crawlers"; history corrected. (I09) | new |
| 2 | https://blog.cloudflare.com/tag/radar/ | ~14:20 | 404 | n/a | Guessed URL; refused by the site's structure. | new (dead) |
| 3 | https://labs.ripe.net/ | ~14:20 | 200 | newest 10 Nov 2026 | Index: 10 Nov "The Machine Majority", 9 Nov RPKI validators, 6 Nov "The Internet's New Factories", 5 Nov registrar DNSSEC. None names Atlas or RIS in the preview. (I10) | seen index; two items new |
| 4 | https://docs.censys.com/changelog | ~14:20 | 200 | entries 5 Oct to 9 Nov 2026 | Weekly changelog entries, newest 9 Nov. (I12) | new |
| 5 | https://censys.com/blog/ | ~14:20 | 200 | newest 6 Nov 2026 | Posts 2 to 6 Nov incl. "ARTEX: Agentic Asbestos", two European refrigeration-controller exposure posts, and "Thoughts on Vulnerability Response in the Era of the Vulnpocalypse and PHP2Shell". (I12) | new |
| 6 | https://developer.chrome.com/docs/crux/release-notes | ~14:20 | 200 | latest published 13 Oct 2026 | September 2026 release adds "new experimental variants of the Core Web Vitals (LCP, INP, and CLS) including soft navigation metrics". (I15) | new |
| 7 | https://tranco-list.eu/ | ~14:21 | 200 | no date on page | Daily list "by 0:00 UTC"; no news after August 2023 on the page; new API endpoints and filters (Safe Browsing, CrUX). No change found. (I14) | new |
| 8 | https://docs.censys.com/changelog/november-9-2026.md | ~14:22 | 200 | 9 Nov 2026 | Adds a PQC label and "over 200 new fingerprints"; ARC advisories 3 Nov (Control Web Panel, CVE-2026-77876) and 9 Nov (N-able N-central). (I12) | new |
| 9 | https://docs.censys.com/changelog/november-2-2026.md | ~14:22 | 200 | 2 Nov 2026 | Credits change: every UI and API action costs one credit; Starter $79 a month (500 credits) and Starter Pro $599 (4,000); credit packs no longer sold. Bears on access cost for Lighthouse. (I12) | new |
| 10 | https://labs.ripe.net/author/saber-mesgari/the-machine-majority-what-bot-traffic-looks-like-from-central-asia/ | ~14:22 | 200 | 10 Nov 2026 | Uses Cloudflare Radar's API: bots 65.3% of HTML requests 8 to 15 Oct (57.4% in early June), AI bots 6.0%; global bot share of all requests 34.7% (July) to 39.2% (November); "Most web pages are now fetched by machines rather than people, at least on the networks we can measure." Author flags one CDN's view. (I09 used by a third party) | new |
| 11 | https://labs.ripe.net/author/armanobosyan/the-internets-new-factories/ | ~14:22 | 200 | 6 Nov 2026 | AI factories make traffic that mostly never reaches public graphs; public routing data "shows only the public edge"; Fastly: over half of classified AI-bot requests reached origin versus under 9% of human; vendor figures are not measured traffic. Author discloses a commercial link. (I10 named as a limit) | new (last sweep could not open it) |
| 12 | https://censys.com/blog/artex-agentic-asbestos/ | ~14:23 | 200 | about 5 Nov 2026 | Censys reports an open-source LLM-driven penetration framework, ARTEX, with 1,465 hosts exposing a console on 3 to 4 Nov (about 650 in two identically configured blocks), 155 also running other threats it detects, 32 open directories; recommends hunting by console title. (I12) | new |
| 13 | https://blog.cloudflare.com/ | ~14:23 | 200 | newest 9 Nov 2026 | Posts 2 to 9 Nov: Zero Wire (3 Nov), personal agents controls (4 Nov), "Agents aren't humans (but they kinda are)" (5 Nov); none on outages. (I09) | new index |
| 14 | https://blog.cloudflare.com/zero-wire/ | ~14:24 | 200 | 3 Nov 2026 | "a public vulnerability intelligence feed on Cloudflare Radar": briefings on critical CVEs with WAF-rule request charts that "do not count compromised systems or successful exploits". (I09) | new |
| 15 | https://blog.cloudflare.com/q3-2026-internet-disruption-summary/ | ~14:24 | 200 | 27 Oct 2026 | 49 disruptions in Q3: 19 government-directed, 14 power, 5 disasters; no AI-related disruption described. (I09) | new |
| 16 | https://blog.cloudflare.com/agents-arent-humans/ | ~14:24 | 404 | n/a | Guessed URL. | new (dead) |
| 17 | https://blog.cloudflare.com/see-the-agents-set-the-terms/ | ~14:27 | 404 | n/a | Guessed URL (title taken from the index). | seen by scout 1 elsewhere; dead here |
| 18 | https://www.caida.org/catalog/datasets/ | ~14:24 | 303 | n/a | Redirects to catalog.caida.org; followed after a robots check. (I11, I13) | new |
| 19 | https://catalog.caida.org/search?query=types=dataset%20links=tag:caida%20 | ~14:27 | 200 | none | Extract held only the title "CAIDA Resource Catalog"; the listing is script-rendered. A limit of the reading tool. | new |
| 20 | https://labs.ripe.net/atlas/ | ~14:24 | 200 | newest Atlas-tagged 17 Sep 2026 | Atlas articles: "When Traceroutes Lie" (3 Sep: some routers alter TTL, which can distort topology), "LatencyMON, Rebuilt" (16 Jun). Nothing since 17 Sep. (I10) | new |
| 21 | https://googlechrome.github.io/CertificateTransparency/log_list.html | ~14:24 | 404 | n/a | Guessed URL. (I16) | new (dead) |
| 22 | https://www.caida.org/projects/canis/ | ~14:28 | 200 | published 29 Aug, modified 30 Aug 2026 | NSF-funded CANIS: "a suite of modules to transform the applicability of UCSD-NT in AI contexts"; no milestones on the page. (I13) | new |
| 23 | https://www.caida.org/catalog/datasets/internet-topology-data-kit/release-2026-03/ | ~14:28 | 200 | published 14 Apr, modified 6 Aug 2026 | ITDK-2026-03 built from Ark traceroutes, 5 to 19 Mar 2026, 369 IPv4 monitors in 71 countries. (I11) | new |

## Rotation I09 to I16

Reading what each has published since its last read (2 and 6 November). "Nothing found" means my pages showed nothing, not that nothing exists.

- I09 Cloudflare Radar: new. Zero Wire launched 3 Nov (vulnerability briefings with WAF-rule request charts). One release note, 26 Oct, corrected the Markdown for Agents metric, which had counted conversions not served to AI bots. A Q3 disruption review came out 27 Oct with no AI cause. The Radar outage centre was not retried (403 on 7 Nov). RIPE Labs published an analysis built on the Radar API on 10 Nov (a third party using the instrument).
- I10 RIPE Atlas: no Atlas-specific publication since 17 Sep on the Atlas tag; a 3 Sep article on TTL-altering routers bears on traceroute reading. A Search showed UI notices to 10 August only.
- I11 CAIDA Ark: nothing new on the Ark topology dataset page (not re-fetched; extract of the catalog was empty). ITDK-2026-03 (Ark traceroutes, March 2026) is the latest release found; page modified 6 Aug.
- I12 Censys: the most active. 2 Nov credit and pricing change (every action one credit; Starter plans); 9 Nov PQC label and over 200 fingerprints; ARTEX exposure count 3 to 5 Nov. The PHP2Shell tracker page was not re-read.
- I13 CAIDA telescope: CANIS page (29 Aug) describes an AI-ready telescope data project; search snippets (not opened) give planned dates of September and December 2026 for validation and a Parquet migration, which are plans, not releases. The telescope dataset page was not re-read.
- I14 Tranco: nothing new; page undated.
- I15 CrUX: the September 2026 release (published 13 Oct) added experimental soft-navigation Core Web Vitals. No October release published yet on the page.
- I16 CT logs: no source opened beyond search results; nothing dated November 2026 found. A guessed Chrome log-list URL was 404.

## Not opened or refused

- Not fetched: robots.txt: none; every URL passed the gate.
- 404s on guessed URLs: rows 2, 16, 17, 21. Radar outage centre (403 on 7 Nov) not retried.
- Search results not opened: ct-policy threads, DigiCert and Certera pages, CANIS proposal PDF, CAIDA annual report, APNIC "A day in the life of RIPE Atlas", RIPE status notice, ustechautomations and seomator crawler reports, Cloudflare 2025 AI-crawler posts.
- CAIDA's catalog was script-rendered and returned no entries.

## Five best leads

1. **ARTEX, an open-source LLM penetration framework, and its exposed consoles (Censys, 3 to 5 Nov)**
   - Why: Censys reports 1,465 exposed consoles (about 815 distinct-looking), 155 co-hosted with other threats, and 32 open directories turning over (10 closed, 15 opened in two days); CrowdStrike and Microsoft reports are cited for use in real intrusions. It is a publicly counted population of autonomous-agent tooling on the open internet, closest to the charter's "sustain and spread".
   - Fits: the cost-and-spread investigation, and LH042's exposed-services work (not a measurement of harm; note the rule against visiting exposed hosts, so only Censys's published counts, never queries to the hosts).
   - Lost if nobody looks: yes. Console counts and open directories change in days; Censys's post gives one 3 to 5 Nov snapshot. Window about 1 to 2 weeks, and the repository was reported taken down.
2. **Cloudflare Radar as a bot-share series, now used by third parties (RIPE Labs, 10 Nov)**
   - Why: reports bots at 65.3% of HTML requests (8 to 15 Oct) against 57.4% in early June, and AI bots at 6.0%; that is load on shared infrastructure by automation. The Radar release note of 26 Oct shows the metric definitions get corrected and history rewritten.
   - Fits: what AI activity costs the shared internet. Snapshot the API series and release notes weekly so rewrites are visible.
   - Lost if nobody looks: partly; history is corrected in place, so a dated snapshot preserves the earlier values. Window: from now.
3. **Censys's access change (2 Nov): every action one credit, Starter $79 a month**
   - Why: it changes what Lighthouse's keeper could buy for exposure counts (relevant to P-0022's classes of access and the keeper's route); the free tier now gives five free actions a day.
   - Fits: the access-map work (LH047) rather than an investigation. Lost if not looked at: low; the changelog persists.
4. **Zero Wire (Cloudflare Radar, 3 Nov): a dated feed of critical-CVE briefings with WAF-rule request counts**
   - Why: gives a vendor's dated exploitation-attempt series per vulnerability (explicitly not successful exploits), a candidate clock for software-update and model-found-bug studies.
   - Fits: both software updates and model-found bugs. Lost if nobody looks: "Needs attention" status and last-checked dates are likely overwritten; first observations lost within weeks.
5. **RIPE Labs on what routing data cannot see of AI factories (6 Nov)**
   - Why: reports that the public edge shows only a fraction of AI traffic and that large transfers stay in private fabrics, a stated blind spot for any routing or peering instrument; also that scraper load strains operators at modest bandwidth.
   - Fits: the cost investigation, as a limit to cite rather than a measurement. Lost if nobody looks: no.

Pages opened: 23 requests, of which 19 returned content (4 were 404s; 1 a script-rendered empty extract). No incidents of AI-caused shared-infrastructure failure were found in the rotation. Nothing went wrong beyond the dead guessed URLs.
