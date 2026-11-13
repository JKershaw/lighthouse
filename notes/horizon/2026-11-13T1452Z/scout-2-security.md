# Scout 2, Security and vulnerabilities, run 2026-11-13T1452Z

Started 2026-11-13 14:54 UTC, ended 2026-11-13 14:58 UTC. Every claim is "reported by" the page named, not observed by Lighthouse, unless marked "fetched by scout" (a plain read of an API response). Nothing read was treated as an instruction. No email addresses are recorded. Every fetch was preceded by a separate robots gate run.

## What KEV added since catalogue version 2026.11.09

Fetched by scout at 14:54 UTC: catalogVersion 2026.11.10, released 2026-11-10T19:03Z, 1779 entries (1773 in 2026.11.09, so six added). Nothing has been added since 10 November. All six were added on 10 November:

- Barracuda Networks Email Security Gateway CVE-2026-116606 (authentication bypass by alternate path) and CVE-2026-111560 (Barracuda multiple products; command injection); due 13 November (three days).
- Microsoft Office Outlook CVE-2026-124194 (missing user interaction for a potentially unsafe action); due 24 November.
- Openwave Messaging Webtop Media Transcoder CVE-2026-111793; due 24 November.
- Cisco BroadWorks CVE-2026-20320 (XML external entity); due 24 November.
- Google Chromium CVE-2026-125350 (use after free in XML, fixed in Chrome 157.0.8103.50); due 24 November. The CVE record (fetched by scout) carries no credit and no AI mention.

Ransomware use is "Unknown" for all six. Earlier entries still in the last-twelve view: Apple CVE-2024-27834 (4 Nov), SonicWall CVE-2026-19868 (6 Nov).

EPSS fetched by scout on 13 November for the six plus GPUStack: Barracuda 116606 0.109 (percentile 0.960), Barracuda 111560 0.091 (0.954), Outlook 0.016, BroadWorks 0.0098, Chromium 0.0096, Openwave 0.0064, GPUStack CVE-2026-102895 0.0052 (0.445; it was 0.0033 on 8 November, so the score has barely moved four days after KEV listing). Only the two Barracuda entries are above the 95th percentile.

## Searches

1. "AI model found vulnerability disclosed CVE November 2026": cryptobriefing (APT flaw, seen), darkreading and bankinfosecurity/govinfosecurity (JFrog patching flaws behind an OpenAI model's escape; both robots.txt disallowed, not fetched), secnews.gr (vLLM RCE; disallowed), thehackernews label page, scworld (NemoClaw, August), forkast (Ash AI cluster), penligent (GitLab AI Gateway CVE-2026-90970, 2 October). Only the Debian/Ubuntu APT item is clearly November. Not opened: all except noted.
2. "Barracuda Email Security Gateway CVE-2026-116606 exploited": securityweek (opened), bleepingcomputer (disallowed), fieldeffect, rescana, decryptiondigest, securityonline, opencve, pentest-tools, techbytes. Aggregators report exploitation from 9 and 10 November; securityweek (4 Nov) says the advisories were silent. Not opened except securityweek.
3. "GPUStack exploited in the wild AI inference server attacks November 2026": CSA research note and PDF (note opened), dailysecurityreview (seen), cipherssecurity, ayinedjimi, techjacksolutions, craftedsignal (July GPUStack disclosure CVE-2026-58658), exploit-intel. Not opened except the CSA note.
4. "Claude Mythos OR GPT-6 Cyber vulnerabilities found open source maintainers patch this week": the-decoder, helpnetsecurity (26 May), eweek, thenextweb, CSA June note, iaps, gigazine, vicarius. All April to July; nothing from this week. Not opened. Search summary figure "23,019 candidates, 1,726 confirmed, 1,596 disclosures, 97 patches, 88 advisories" is secondary and undated here.
5. "oss-security AI-assisted discovery 2026-11 reported using LLM fuzzing": only 2024 Google OSS-Fuzz items. Nothing new. Not opened.

Direct reads (not searches): CISA KEV JSON, FIRST EPSS API, MITRE CVE API, Project Zero archive, oss-security November index and three posts.

## Pages opened

| # | URL | Read (UTC) | Status | Page date | Claim reported | New or seen |
|---|---|---|---|---|---|---|
| 1 | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | 14:54 | 200 | catalogVersion 2026.11.10, 10 Nov 19:03Z | 1779 entries; six added 10 Nov (Barracuda x2, Outlook, Openwave, BroadWorks, Chromium). Fetched by scout. | standing source; the six entries are new |
| 2 | https://api.first.org/data/v1/epss?cve=(seven CVEs) | 14:55 | 200 | scores of 2026-11-13 | Fetched by scout: Barracuda 0.109 and 0.091, others below 0.02, GPUStack 0.0052. | standing source; values new |
| 3 | https://cveawg.mitre.org/api/cve/CVE-2026-125350 | 14:55 | 200 | published 2026-11-10 | "Use after free in XML in Google Chrome prior to 157.0.8103.50"; no credit field. Fetched by scout. | new |
| 4 | https://projectzero.google/archive.html | 14:55 | 200 | latest post 2026-10-27 | No November post; newest is "Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines". | seen (same state as 10 Nov) |
| 5 | https://www.openwall.com/lists/oss-security/2026/11/ | 14:55 | 200 | index to 12 Nov | Lists Plone RCE fix (10 Nov), Apache Roller 15 CVEs, glibc advisories 11 Nov, xfs_admin command injection, dbus DoS, Emacs dir-locals, CPython sandbox escape, LLM and embargo threads. | seen (index); entries new |
| 6 | https://www.openwall.com/lists/oss-security/2026/11/10/19 | 14:55 | 200 | 10 Nov 2026 | In "LLMs and embargoes", a quoted poster says some argue LLMs "are a reason to move away from embargoes" because someone else "could rediscover the issue and use it irresponsibly". | new |
| 7 | https://www.openwall.com/lists/oss-security/2026/11/10/5 | 14:56 | 200 | 10 Nov 2026 | A poster quotes a complaint about "the number of LLM generated/assisted exploits being disclosed irresponsibly" and argues public disclosure beats sale of a 0-day. | new |
| 8 | https://www.openwall.com/lists/oss-security/2026/11/05/11 | 14:56 | 200 | 5 Nov 2026 | Relays a security firm's report of a CPython sandbox escape; CPython "does not support sandboxing untrusted Python code as a security boundary"; a fix PR exists but "upstream is not backporting it to security releases". | new |
| 9 | https://www.securityweek.com/barracuda-email-security-gateway-authentication-bypass-opens-path-to-root/ | 14:57 | fetched | 4 Nov 2026 | Mandiant published advisories for CVE-2026-116606 (CVSS 9.3) and 111560 (8.6); "neither advisory states whether the flaws have been exploited". No AI mention. | new |
| 10 | https://labs.cloudsecurityalliance.org/research/csa-research-note-gpustack-cve-2026-102895-kev-20261110-csa/ | 14:57 | fetched | 10 Nov 2026 | CISA listed GPUStack on 9 Nov; it controls what runs on GPU hosts and holds worker and cloud credentials; places it with the Ray and LiteLLM listings; "no victim counts, first-exploitation dates, or indicators of compromise". Roughly 6,000 GitHub stars, 940,000 Docker Hub pulls (not exposure). | new |

Seen from earlier files and not re-read: GHSA-gj9m-f8ph-pmhr, dailysecurityreview GPUStack, cryptobriefing APT, the Debian and Ubuntu apt notices, oss-security 5 Nov sshole post.

## Refusals and walls

Not fetched (robots.txt): bleepingcomputer.com Barracuda article; bankinfosecurity.com JFrog/OpenAI escape article; darkreading.com AI model takeover article; secnews.gr vLLM article. No walls (403, challenge, paywall) met on pages fetched. No exposed hosts visited. Not gated and not fetched: runsybil.com CPython blog (named inside the oss-security post only).

## Five best leads

1. KEV 2026.11.10, six additions including Barracuda ESG, 10 Nov (feed above). A mail gateway chain was listed with a three-day deadline while the vendor advisory was silent on exploitation; EPSS is the only one of six above the 95th percentile. Bears on software updates: how fast the patch window closes.
2. CSA note on GPUStack in KEV, 10 Nov (https://labs.cloudsecurityalliance.org/research/csa-research-note-gpustack-cve-2026-102895-kev-20261110-csa/). An AI-serving control plane with credentials for every worker is exploited in the wild, EPSS 0.005 four days on; it fits the charter question about AI infrastructure being a place where activity can sustain and spread itself.
3. oss-security "LLMs and embargoes" thread, 10 Nov (https://www.openwall.com/lists/oss-security/2026/11/10/19). Maintainers argue about whether model-found bugs break embargo norms; this is the model-found-bugs investigation seen from the people who patch.
4. oss-security "CPython sandbox escape", 5 Nov (https://www.openwall.com/lists/oss-security/2026/11/05/11). A reported escape affecting template sandboxes used in AI tooling, with upstream declining a security fix backport; a supply-chain gap, not yet read at its primary source.
5. Project Zero archive, no post since 27 Oct (https://projectzero.google/archive.html), plus Anthropic and OpenAI disclosure counts only in secondary June reports. Absence is the finding: no primary, dated count of model-found flaws this week; worth a direct look at lab disclosure dashboards next sweep.

## Urgent

None found. GPUStack and Barracuda exploitation is already reported elsewhere; no observation here is lost if left a few days.
