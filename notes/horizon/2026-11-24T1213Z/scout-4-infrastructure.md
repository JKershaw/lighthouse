# Scout 4, Internet infrastructure and measurement, run 2026-11-24T1213Z

**Driving session's note (24 November).** Every URL in this log was put through the robots gate again after hand-back: only the two the scout recorded as refused and did not fetch are refused (RouteViews, PCH). The 7 November read of RouteViews came the day before the keeper's rule of 8 November that obeys groups naming the running provider's tokens, which likely explains the difference; not investigated further.

**In short.** The Cloudflare Radar feed has nothing new since 20 November (its newest entry is still nginx2root). The 18 November House Homeland Security hearing is now a lead for LH058: reported by The Record, the Director of National Intelligence and FBI named patching and upgrades, not attack, and no operator gave a statement there; no new operator final report (AWS, FAA, Workday, JPMorgan) turned up. Rotation I01 to I08: Epoch AI's data-centre log has a 18 November revision (projected Rubin chips removed from five sites) and RIPE Labs published seven items since 5 November; the rest show no change, and RouteViews and PCH are refused by robots.txt. Everything is reported by a page; WebFetch answers are a small model's extract, so quotations are as relayed.

Start 12:15 UTC, end about 12:17 UTC by `date -u` (24 Nov 2026). Tools: lh_feeds.py, robots_gate.py (provider anthropic), WebFetch, WebSearch (standard). No curl, nothing saved, no code run from a download. I read no keys and did not search harbour/.session/.

## Direct publication checks

| Endpoint | UTC read | Interval | Outcome | Entries |
| --- | --- | --- | --- | --- |
| https://blog.cloudflare.com/tag/cloudflare-radar/rss | 12:15, 24 Nov | 20 to 24 Nov | No new entries (status ok, oldest 2026-02-27, newest 2026-11-20, 0 skipped, 0 undated) | Only the already-seen nginx2root, 20 Nov 2026 |

## Pages opened (all read through WebFetch, i.e. relayed extracts; all gates answered allowed unless stated)

| URL | UTC read | Gate | Status | Page date | Reported by the page |
| --- | --- | --- | --- | --- | --- |
| https://epoch.ai/data/ai-data-centers/updates (I03) | ~12:16 | allowed | 200 | newest entry 18 Nov 2026 | "Nov. 18, 2026 (Revisions)": removed projected Rubin chips at Goodnight (229.7k), Meta Bowling Green (74.4k), OpenAI Stargate UAE (200k), QTS Cedar Rapids (196.8k), YTL Johor (48.8k); 6 Nov: Huawei Horinger and Wuhu revised. No page "last updated" date. |
| https://labs.ripe.net/ (I06 context) | ~12:16 | allowed | 200 | to 23 Nov 2026 | Seven items since 5 Nov, see leads |
| https://www.peeringdb.com/blog (I01) | ~12:16 | allowed | 404 | n/a | Same 404 as 2 and 6 Nov, so no blog found; no change in access terms found |
| https://www.kentik.com/blog/ | ~12:16 | allowed | 200 | newest shown 2 Sep 2026 | First index page only; nothing dated 20 to 24 Nov visible (extract said later pages may exist; not read) |
| https://www.caida.org/catalog/datasets/as-relationships/ (I08) | ~12:16 | allowed | 200 | undated | Serial-1 "1998 to present", serial-2 "October 2015 to present"; AUA still applies; no change from the row |
| https://www2.telegeography.com/ (I02) | ~12:16 | allowed | 200 | undated | Three items (PTC'27 prep, a podcast on LEO, "The Problem With Live-Streaming Content"); no dates; nothing on the cable map |
| https://imp.cablelabs.com/ (I04) | ~12:16 | allowed | 200 | n/a | Reporting period "January 2018 through December 2024"; no new release or terms stated |
| https://ris.ripe.net/docs/ (I06) | ~12:16 | allowed | 200 | "last updated 6/2/2022" | Docs hub (collectors, MRT, beacons, RIS Live, RISwhois); no dated news |
| https://therecord.media/tech-disruptions-house-homeland-committee-testimony | ~12:17 | allowed | 200 | 18 to 19 Nov 2026 | 18 Nov House Homeland Security worldwide-threats hearing: DNI Clayton said not "an orchestrated attack by a foreign malign actor" and pointed to "rising pace of patching and system upgrades"; FBI Deputy Director Raia "no indication whatsoever" of malicious cyber activity; Secretary Mullin "98 percent confident" no adversary hacking; the article quotes no named operator; Mullin to hold a private-sector call on advance notice of upgrades; no written report promised |
| https://www.techrepublic.com/article/news-november-2026-tech-outages-timeline/ | ~12:17 | allowed | 200 | 18 Nov 2026 | Nine-row table of outages (Microsoft 365, Claude 13 Nov "not publicly established", Workday, FAA "under investigation", AWS 15 Nov no root cause, JPMorgan, United, NSA, Apple); no final report for any operator |

I03 note: 5 Nov to 6 Nov the page showed "Updated Nov. 5" and I did not record the update log's end; the 18 Nov entry is new against my 7 Nov log (which stopped at 5 Nov).

## Rotation I01 to I08 (last read 6 Nov raw, 7 Nov sweep)

- I01 PeeringDB: blog URL 404 again; not found any dated change in terms or API-key rule. Unchanged as far as I could read.
- I02 TeleGeography: no change in coverage found; undated blog items only.
- I03 Epoch AI: dated change 18 Nov (Rubin chips removed at five sites) and 6 Nov (two Huawei sites revised). Not reported by the page whether the removals reflect any change in the sites' power.
- I04 CableLabs IMP: unchanged; period ends December 2024.
- I05 RouteViews: refused by robots.txt (gate allowed=false for https://www.routeviews.org/routeviews/). The 7 Nov log read this page; its robots.txt now disallows it for this gate, or the rule was missed then. Not fetched. Worth the driver checking the 7 Nov row.
- I06 RIPE RIS: docs unchanged (last updated 2022); RIPE Labs published "Would You Have Noticed? A Blind Test of BGP Anomaly Detection" (23 Nov) built on RIS data.
- I07 PCH: refused by robots.txt (gate allowed=false for https://downloads.pch.net/BGP_Routing_Data); not fetched.
- I08 CAIDA AS Relationships: no change from the row.

## Searches (WebSearch, standard)

1. "House hearing 18 November 2026 outages AI vulnerability patching testimony". Opened: The Record. Not opened: Cyberscoop, CIO Dive, Cybersecurity Dive, Honolulu Star-Advertiser, Nextgov (gate allowed, unopened), Newsweek, govinfo CHRG-119hhrg63128 (could not tell if it is this hearing; unopened), CBS Austin, Fox5, Techaeris, implicator.ai.
2. "post-incident report outage November 2026 root cause AWS OR Workday OR JPMorgan OR Cloudflare OR Azure". Opened: TechRepublic timeline. Not opened: the next.ink PDF (struck in the 20 Nov incident; not touched), TechPowerUp, The Register (16 Nov), Expert Insights, ABC stations, GMA, fourweekmba, Network World, rootly, ThousandEyes and older postmortems.
3. "AWS us-east-1 November 2026 outage root cause report": none opened. Snippets: a 15 Nov us-east-1 incident of 2h18m with no cause given; a 11 Nov Tokyo incident with "cause identified internally" but not named (secondary page snippets, unverified).
4. "outage OR BGP OR DNS incident 21 22 23 November 2026": nothing dated 21 to 23 Nov. Snippets (not opened, unverified): an isdown.app entry on 1.1.1.1 issues in Canada (13 Nov, snippet says a BGP hijack of 1.1.1.0/24, 1.1 hours), a Link11 disruption 16 Nov, NANOG Ethiopia thread 10 Nov (seen on 20 Nov).

## Refused or unreached

- https://www.routeviews.org/routeviews/ and https://downloads.pch.net/BGP_Routing_Data: robots gate refused.
- ThousandEyes: robots.txt returned 403 so the gate allowed, but I did not fetch the blog. Cloudflare status page and homeland.house.gov gated allowed, not fetched.
- Kentik later index pages and Nextgov not read.
- Nothing behind a login read.

## Newness checks (grep of notes/horizon)

New: The Record hearing article, TechRepublic timeline, the three RIPE Labs items of 9, 19, 23 Nov, 1.1.1.1 Canada snippet (isdown incident 686900), Epoch 18 Nov revision, Link11 snippet. Seen before: RIPE Labs "Machine Majority" (10 Nov) and "Internet's New Factories" (6 Nov), isdown.app generally, the NANOG Ethiopia thread.

## Five best leads

1. House Homeland Security hearing record, 18 Nov. Secondary: https://therecord.media/tech-disruptions-house-homeland-committee-testimony; transcript or committee page not found (govinfo link unopened). Matters to LH058: officials, not operators, are stating the cause ("patching and upgrades"), with DNI Clayton separately linking the NSA outage to PHP patching in a TV interview (reported by the search summary, not opened). Distinguishes government claim from operator claim. Next step: locate the committee's own hearing page or transcript. New.
2. Operator final reports still missing as of 18 to 24 Nov: AWS 15 Nov (no cause), FAA (under investigation), Workday (disaster-recovery environment), JPMorgan (hardware bug as reported). Source: https://www.techrepublic.com/article/news-november-2026-tech-outages-timeline/. Matters to LH058 as the table of stated causes; a gap is unknown, not a negative. New.
3. RIPE Labs "Would You Have Noticed? A Blind Test of BGP Anomaly Detection" (23 Nov), https://labs.ripe.net/author/shadi-motaali/would-you-have-noticed-a-blind-test-of-bgp-anomaly-detection/, and "Your Router Trusts Its Validator" (9 Nov, RPKI). Matters as methods on RIS data for outage detection; indirect. New.
4. 1.1.1.1 route incident in Canada, 13 Nov (isdown.app snippet only, unverified). Primary would be Cloudflare's status or a post-incident note; not opened. Matters as one more November operator event whose cause is a routing hijack, not patching. New, weak.
5. Epoch AI 18 Nov revision removing projected Rubin chips at five sites (https://epoch.ai/data/ai-data-centers/updates). Matters to cost-and-load: projected compute at sites like Stargate UAE shrinks in the dataset; the page gives no reason. Dated change to I03. New.

## Withheld under research safety

None.
