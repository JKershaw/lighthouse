# Scout 4, Internet infrastructure and measurement, sweep 2026-11-18T1300Z

**In short.** The Cloudflare Radar posts index showed no entry dated 11 to 18 November 2026; its newest is 3 November (Zero Wire), so this first check found no new entries in the interval. Rotation I33 to I40 (GitHub Advisory Database, EPSS, Exploit-DB, Atlantic Council dataset, SANS ISC, GreyNoise, MAWI, M-Lab) showed no change to coverage, access or method on the pages; the only new material is GreyNoise's blog (an AI Cyber Index, 12 November, and three live exploitation reports). Microsoft's preliminary report on the 12 to 13 November outage is covered by secondary outlets, with a final report said to be expected 20 November. WebFetch answers are a small model's extract, so quotations are as the summariser relayed them; everything here is reported by a page, not observed. I read no keys and did not search harbour/.session/.

Start 13:02 UTC, end 13:05 UTC, 18 November 2026 (`date -u`).

Tools: robots_gate.py (all URLs allowed; Cloudflare blog `Allow: /`), WebFetch, WebSearch standard. No curl, nothing saved to disk.

## Direct publication checks

| Endpoint | UTC read | Outcome | Relevant entries | Gap |
| --- | --- | --- | --- | --- |
| https://blog.cloudflare.com/tag/cloudflare-radar/ | 13:03, 18 Nov 2026 | First check (no earlier log has this URL); baseline recorded; no new entries in 11 to 18 Nov | Newest visible 3 Nov 2026 "Introducing Zero Wire" (https://blog.cloudflare.com/zero-wire/, seen in 2026-11-10T1415Z); 27 Oct Q3 disruption summary; 16 Oct "Continuous accountability for Verified bots"; 14 Oct "Yandex outage: ... malicious bots went on the move"; 8 Oct Radar redesign | Page lists 18 posts back to 27 Feb 2026 with a "Load more" button; whole 11 to 18 Nov interval is shown, so no gap. Page 'modified' 12 Nov for Zero Wire per structured data. |

Baseline (18 posts, newest first as relayed): 3 Nov Zero Wire; 27 Oct Q3 disruptions; 16 Oct verified bots; 14 Oct Yandex outage; 8 Oct Radar redesign; 13 Aug eclipse traffic; 11 Aug DDoS H1 2026; 7 Aug Radar Researcher (AI tool); 6 Aug AEO; 28 Jul Q2 disruptions; 21 Jul World Cup; 1 Jul agentic internet bot report; 3 Jun first-AS enforcement; 27 May Iran restored; 28 Apr Q1; 17 Apr Agent Readiness; 17 Apr AI redirects; 27 Feb ASPA.

## Searches (WebSearch, standard)

1. "Microsoft 365 outage 12 November 2026 post-incident report root cause": many secondary outlets (BleepingComputer, Petri, ITPro, TheNextWeb, Office Watch, TechPowerUp 16 Nov) and a PDF link on next.ink. Engine summary: preliminary report names a latent bug (dormant since July), increased traffic after a Teams failover, and reduced capacity; final report "expected on November 20"; Microsoft says not a cyberattack or AI malfunction; incident EX1550543 in the admin centre (login, not read). Not opened.
2. "internet outage routing incident BGP November 2026": a NANOG post 10 Nov 2026 asking about BGP changes in Ethiopia (https://seclists.org/nanog/2026/Nov/42, not opened); rest are older items. Nothing from RIPE Labs, Kentik or ThousandEyes dated November found.
3. "Java4Shell CVE-2026-114938 exploitation": nothing matching; no corroboration of the name or CVE outside GreyNoise's own listing.

## Pages opened

| # | URL | Page date | UTC read | Status | New? | Reported by the page |
|---|---|---|---|---|---|---|
| 1 | https://blog.cloudflare.com/tag/cloudflare-radar/ | n/a | 13:03 | 200 | index new; entries see above | 18 posts, newest 3 Nov 2026 |
| 2 | https://blog.cloudflare.com/zero-wire/ | 3 Nov 2026 (modified 12 Nov) | 13:04 | 200 | seen (2026-11-10T1415Z) | "a public vulnerability intelligence feed on Cloudflare Radar"; says "AI is changing both the volume and speed of critical vulnerability discovery"; status and last-checked date per card; WAF rule matches "are not counts of compromised systems" |
| 3 | https://docs.github.com/.../about-the-github-advisory-database (I33) | none | 13:03 | 200 | page not in earlier sweeps; unchanged from row | Twelve reviewed ecosystems incl. GitHub Actions, Composer, Pub, Swift, Erlang; malware advisories from npm security team and OpenSSF; OSV format; no dates or changelog |
| 4 | https://www.first.org/epss/ (I34) | none | 13:03 | 200 | New | No model version or dated news shown; changelog on /epss/research not read |
| 5 | https://www.exploit-db.com/about-exploit-db (I35) | footer 2026 | 13:03 | 200 | page unchanged | GHDB now includes Bing and GitHub searches (the row does not say so); no access change |
| 6 | https://www.atlanticcouncil.org/.../software-supply-chain-security-the-dataset/ (I36) | 27 Sep 2023 | 13:03 | 200 | unchanged | Still Update 3, 250 entries (168 attacks, 82 disclosures); no later update |
| 7 | https://isc.sans.edu/data/ (I37) | "Last Seen" to 2026-11-18 | 13:03 | 200 | unchanged | Categories ISC/DShield API, Weblogs (404Project), SSH/Telnet logs, Threat Feeds; CC BY-NC-SA 4.0 badge; no changelog |
| 8 | https://www.greynoise.io/blog (I38) | 6 to 18 Nov entries | 13:03 | 200 (first 100,000 of 170,278 characters read) | New | Posts: 18 Nov Java4Shell (CVE-2026-114938) live activity report; 17 Nov Elastic integration; 13 Nov N-able N-central live report; 12 Nov AI Cyber Index; 6 Nov SSHole (CVE-2026-123158) live report. "No posts dated since 1 November mention AI agents specifically" (summariser) |
| 9 | https://www.greynoise.io/blog/ai-cyber-index-benchmarking-defensive-capabilities | 12 Nov 2026 | 13:04 | 200 | New | Benchmarks 46 models on Suricata rules, YARA rules and attack forensics; "Claude Opus 5.5 had the highest raw score (74.2%)", refusals (only Anthropic and Google models) pull it below the 64.5% "capable" threshold when penalised |
| 10 | http://mawi.wide.ad.jp/mawi/ (I39) | latest trace 2026/04/08 (DITL) | 13:03 | 200 | unchanged | Notes now include "The MAWILab operation was terminated in December 2024"; ICMP probing stopped 4 Dec 2020, restarted 2 Jul 2023 |
| 11 | https://www.measurementlab.net/blog/ (I40) | newest 18 Aug 2026 | 13:03 | 200 | New (index) | HERMES, "The Internet Can Be Up and Still Fail" (18 Aug); IQB reliability research (5 Aug); school-measurement community of practice. No dataset or access change since Jul 2025 (NDT7 dataset) |

Not opened as separate pages: the three GreyNoise `*.events.greynoise.io` live reports (they describe exposure and exploitation of named hosts' vulnerabilities; opening is permitted but I judged the live pages out of a scout's scope; no host lists visited).

## Refusals and walls

None. All gated URLs allowed (robots 200 for each host). No 403s.

## Search results not opened

Microsoft outage coverage (BleepingComputer, Petri, ITPro, TheNextWeb, IBTimes, Office Watch, TechPowerUp, next.ink PDF, Expert Insights); NANOG post; Cloudflare Feb 2026 BGP outage write-up (ManageEngine); Java search results.

## Quiet

RIPE Labs, Kentik, ThousandEyes and large-provider status pages: not found via search for November; not directly read this sweep (no assigned endpoint). The Cloudflare Radar blog was quiet for 11 to 18 November. I33 to I37, I39 pages unchanged from the rows.

## Five best leads

1. Microsoft 365 preliminary report and expected 20 November final report (secondary coverage only; search found a PDF named PostIncidentReport on next.ink, unopened; incident EX1550543 behind a login). Matters because a latent bug spread by an automatic failover is a concrete case of a shared-infrastructure failure spreading by its own recovery machinery, a mechanism the charter's question treats as separate from AI activity (Microsoft says no AI malfunction). Feeds the Microsoft outage report watch; nothing lost, the daily watch covers it. Next step: the watch reads the Microsoft public pages after 20 November; keep the "not AI" statement attributed.
2. GreyNoise "Global Event" live activity reports (https://java4shell.events.greynoise.io/, nable and sshole equivalents; 6, 13, 18 Nov). Dated, per-vulnerability exploitation timelines kept on a public page; "Java4Shell CVE-2026-114938" had no corroboration in my search. Could feed LH036/LH054 comparison clocks (time from disclosure to scanning) and P-0033. Event pages may be updated in place, so first values could be lost; window days to weeks. Next step: a bounded scout of what an event page records (fields, history) before any scheduling; do not visit hosts they list.
3. GreyNoise AI Cyber Index (https://www.greynoise.io/blog/ai-cyber-index-benchmarking-defensive-capabilities, 12 Nov 2026). A third-party benchmark of model defensive capability that reports refusal rates by lab; relevant to lab capability kept apart in the ai-cost-and-spread investigation. Index may be re-run and scores change. Next step: read the methodology and whether scores are versioned; a lead for LH042 or LH048 context only.
4. Cloudflare Zero Wire (https://blog.cloudflare.com/zero-wire/, modified 12 Nov) already L-0070; Radar posts since 3 November are none, so nothing new to add except that the page was modified 9 days after publication, which supports tracking it as an updating source (briefings carry last-checked dates). Window: updates overwrite; next step is a dated copy of the Zero Wire index if a study uses it.
5. M-Lab HERMES (https://www.measurementlab.net/blog/hermes, 18 Aug 2026, summary only: "The Internet Can Be Up and Still Fail"). A reliability-oriented measurement instrument that might bear on the organisational reliability question (LH052, stopped) or on measuring degradation without an outage. Not urgent. Next step: read the post and the dataset terms.

## Urgent

None.

Rule I was unsure about: none; I did not open the GreyNoise live event pages, to stay clear of lists of exposed hosts, and I recorded that choice above.
