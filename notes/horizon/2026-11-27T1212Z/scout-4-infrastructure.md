# Scout 4, Internet infrastructure and measurement, run 2026-11-27T1212Z

**In short.** The Cloudflare Radar feed has nothing new since 20 November (newest entry still nginx2root), and the post-mortem feed's newest is 1 May 2026. Rotation I09 to I16 shows no change on any page read, except that the Censys PHP2Shell tracker page now names fixed releases 8.2.35, 8.3.36, 8.4.27 and 8.5.12 and two CVE ids, with its counters blank in the extract. No operator's own final report or stated cause for the November outages (LH058) turned up: AWS's post-event summary page still ends at 19 October 2025, JPMorgan's newsroom is silent, Workday's blog URL tried was 404. All quotations came via WebFetch (a small model's extract), so are as relayed.

Start 12:14 UTC, end about 12:20 UTC (`date -u`, 27 Nov 2026). Tools: lh_feeds.py, robots_gate.py (LIGHTHOUSE_PROVIDER=anthropic, strict), WebFetch, WebSearch (standard). Nothing saved, no code run, no keys read.

## Direct publication checks

| Endpoint | UTC read | Interval | Outcome | Entries |
| --- | --- | --- | --- | --- |
| https://blog.cloudflare.com/tag/cloudflare-radar/rss | 12:14, 27 Nov | 24 to 27 Nov | No new entries (ok, oldest 2026-02-27, newest 2026-11-20, 0 skipped) | none |
| https://blog.cloudflare.com/tag/post-mortem/rss (extra) | 12:15 | 24 to 27 Nov | No new entries (newest 2026-05-01) | none |

## Rotation I09 to I16 (WebFetch extracts; all gates allowed, "recurring", keep_body true)

| Id | Instrument and URL | Result | Page's own date and note |
| --- | --- | --- | --- |
| I09 | Cloudflare Radar, https://developers.cloudflare.com/radar/ (glossary URL gated allowed, not re-fetched) | no change | structured data dateModified 2026-05-21; datasets listed: traffic, attacks, technology trends, investigate; CC BY-NC 4.0 |
| I10 | RIPE Atlas, https://www.ripe.net/analyse/internet-measurements/ripe-atlas/ | no change | "Over 14,000" probes; copyright 1992 to 2026; page lists items on a 2027 charging scheme, RIPE 94 |
| I11 | CAIDA Ark /24 topology, https://www.caida.org/catalog/datasets/ipv4_routed_24_topology_dataset/ | no change | last modified 8 July 2020; most recent year restricted to academics, US government, members |
| I12 | Censys, https://docs.censys.com/docs/platform-datasets and https://php2shell.censys.com/ | docs: no change (updated 2026-03-12; "over 15 billion" certificate records). Tracker: change vs the 2 Nov read in what it names | page names 8.2.35, 8.3.36, 8.4.27, 8.5.12 and CVE-2026-109618, CVE-2026-109619; no 8.1 or older release; counters showed blank in the extract (likely client-rendered), so no figures |
| I13 | CAIDA UCSD telescope, https://www.caida.org/projects/network_telescope/ | no change | last modified 29 January 2025; "Hardware and software upgrades are underway" |
| I14 | Tranco, https://tranco-list.eu/methodology | no change | lists CrUX monthly, Radar weekly, Farsight, Majestic, Umbrella daily; five providers but text also says "all four" |
| I15 | CrUX, https://developer.chrome.com/docs/crux/methodology | no change | no date in extract; popularity threshold undisclosed |
| I16 | CT logs, https://certificate.transparency.dev/howctworks/ | no change | MMD "usually 24 hours"; robots.txt 404 |

None refused.

## Standing sources (brief)

Status and operator pages: Cloudflare status/post-mortem feed quiet. RIPE Labs, Kentik, ThousandEyes: searches returned nothing dated November 2026 (not opened). No new routing incident found.

## LH058 operator channels

| Operator | URL | Gate | Result (reported by the page, via WebFetch) |
| --- | --- | --- | --- |
| AWS | https://aws.amazon.com/premiumsupport/technology/pes/ | allowed | newest summary is "October 19, 2025"; none for 15 Nov 2026 |
| JPMorgan Chase | https://www.jpmorganchase.com/newsroom | allowed | nothing about a 16 Nov outage or "software bug" |
| Workday | https://blog.workday.com/en-us/ | allowed | HTTP 404 |
| FAA | https://www.faa.gov/newsroom | allowed (robots 403, no rules) | gated, not fetched |
| Microsoft, United, Apple, NSA | not checked this run | | |

## Searches

1. "post-incident report November 2026 outage root cause AWS OR Workday OR JPMorgan OR FAA OR United OR Apple": results, none opened: TechRepublic November 2026 outages timeline, fourweekmba.com "9 Failures, 7 Causes" and "6 US Disruptions in 6 Days", guptadeepak.com Outage Atlas cluster 2026-11-12 to 17, ABC stations on Microsoft, streamlinefeed "officials rule out coordinated attack", ThousandEyes pages. The summary relayed (not primary): no final root-cause report for the six; Microsoft's full post-incident report "still pending" per the summary (conflicts with LH058's record of a preliminary report of 15 November, so likely stale).
2. "Cloudflare Radar outage routing incident November 2026": mostly 2025 and February 2026 items; uptimerobot pages for 13 and 18 Nov 2026 (not opened); nothing major.
3. "RIPE Labs Kentik BGP incident November 2026": nothing from November 2026 (not opened).

## Five best leads

1. LH058 aggregators: fourweekmba.com "The November Outage Wave, Explained: 9 Failures, 7 Causes" (https://fourweekmba.com/ai-the-november-outage-wave-explained-9-failures-7-causes/) and guptadeepak.com Outage Atlas cluster (https://guptadeepak.com/outage-atlas/clusters/2026-11-12-to-17/): secondary, but may name a ninth failure and source operator statements; touches LH058. Not opened; check for overlap with the population (new URLs? grep earlier sweeps).
2. Censys PHP2Shell tracker now lists four fixed PHP releases and two CVEs (https://php2shell.censys.com/): fix-adoption counters by branch are an independent patch-uptake view for the PHP account, useful beside LH033 and LH057; counters need a rendered read, which the strict rule and tools here did not give.
3. AWS 15 November IAM Identity Center event: no post-event summary yet (page newest 19 October 2025); a gap to keep watching for LH058 (O4).
4. JPMorgan "software bug in on-premise hardware systems" (O5): no operator statement on its newsroom; the claim rests on press only; LH058.
5. CAIDA telescope page notes ongoing upgrades because traffic growth "sometimes causes dropped packets or failed flowtuple generation" (https://www.caida.org/projects/network_telescope/, modified 29 January 2025): a data-quality caveat for any scanning-volume reading (LH057 style); a source limit, not a finding.

## Gaps and refusals

No refusals. Gaps: Workday URL 404 (no other Workday channel tried), FAA, Microsoft, United, Apple, NSA channels unchecked; Radar outage centre and RIS/Atlas data not read; WebFetch extracts only, nothing saved.
