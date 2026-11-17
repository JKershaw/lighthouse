# LH055 source register

**In short.** These are the documents the ARTEX study has read or decided not to read, with why. Seven were requested at the baseline on 17 November 2026 and six retained; Check Point's report, one of the five the brief fixed, returned a rate-limit wall and is unread so far. A listed source is not a verified one: each says what its publisher reports.

Read route for every retained document: studies/LH055/scripts/collect.py, one robots-gated GET, `LIGHTHOUSE_PROVIDER=anthropic`, user agent `Lighthouse-research/1.0`; details in data/<label>/fetch_log.jsonl. Retained bodies and text withhold email addresses, IPv4 addresses, key-shaped strings and defanged indicators (counts in the fetch log); the received-body hash is of the bytes as received. Publication dates are as the page states them; the record checks each at source.

## Included (round 1 baseline: seven requested, six retained; five primary and one secondary, within the twelve allowed)

| ID | Publisher, title | URL | Published (as shown) | Read (UTC) | Outcome | Kind | Why included |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | FBI (IC3), cybersecurity advisory on ARTEX | https://www.ic3.gov/CSA/2026/261113.pdf | 13 November 2026 (PDF Last-Modified 17 Nov 2026 17:13 GMT) | 2026-11-17T20:30:48Z | 200, PDF, 540,485 bytes | agency synthesis | brief panel |
| S02 | Amazon Threat Intelligence (CJ Moses), "Amazon Threat Intelligence observes threat actors running cybercrime campaigns with ARTEX AI agents" | https://aws.amazon.com/blogs/security/amazon-threat-intelligence-observes-threat-actors-running-cybercrime-campaigns-with-artex-ai-agents/ | 13 November 2026 | 2026-11-17T20:30:50Z | 200, HTML, 1,452,605 bytes | publisher's sensor capture of agent records | brief panel |
| S03 | Microsoft Threat Intelligence, "ARTEX abuse expands as cybercriminals target financial sector" | https://www.microsoft.com/en-us/security/blog/2026/11/06/artex-abuse-expands-as-cybercriminals-target-financial-sector/ | 6 November 2026 (URL path; record to confirm on page) | 2026-11-17T20:30:51Z | 200, HTML, 310,894 bytes | publisher incident telemetry | brief panel |
| S04 | Censys, "ARTEX: agentic asbestos" | https://censys.com/blog/artex-agentic-asbestos/ | to confirm on page | 2026-11-17T20:30:52Z | 200, HTML, 181,902 bytes | internet-scan exposure counts | brief panel |
| S05 | Check Point Research, "Hacking on Autopilot: Inside ARTEX Cybercrime Campaigns" | https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/ | unknown (unread) | 2026-11-17T20:30:52Z | HTTP 429, a wall; body not retained, hash of the 5,860 error bytes in the log; robots allowed; not retried in this read | operator-console analysis (by the brief's description; unread) | brief panel; stays on the panel, read on the dated days |
| S06 | SANS Internet Storm Center (Renato Marinho), "The Self-Expanding Stolen Inference Supply Chain: An AI Agent Harvesting and Re-Serving LLM Access" | https://isc.sans.edu/diary/33332 | 11 September 2026 | 2026-11-17T20:31:36Z | 200, HTML, 42,389 bytes | publisher's honeypot capture | contrasting mechanism case (Q6); not tied to ARTEX by its publisher, to be checked |
| S07 | StepSecurity, "ARTEX: Attackers Adopted This AI Pentesting Tool in Three Months. Leaked Secrets Are Its Fastest Way In." | https://www.stepsecurity.io/blog/artex-ai-pentesting-tool-attackers-leaked-secrets | 12 November 2026 | 2026-11-17T20:31:37Z | 200, HTML, 197,119 bytes | secondary synthesis, with its own reading of a surviving source copy | locator of campaigns and primary reports missing from the five (Q5); supplies no independent corroboration; on the panel at lock, removed by amendment 1 |

## Excluded or not opened at the baseline

- Secondary coverage returned by Q1 to Q4 (eSecurityPlanet, Cybernews, Cybersecurity News, The Register, GBHackers, Aviatrix, The Record, Infosecurity Magazine, The Hacker News, BleepingComputer, Threat Landscape, Inc., TechTimes, Brandefense, The Next Web, WebProNews, Mallory, BigGo, AI Chat Daily, dev.to): secondary reporting; may locate sources but supplies no corroboration. Not opened.
- MIT AI incident database entry 1781: a secondary database entry. Not opened.
- Cloud Security Alliance research notes (two on ARTEX and LLMjacking, one on API-key implants): syntheses. Not opened; a round 2 lead if a primary source they cite is missing.
- Equixly, 16 November 2026 analysis of which ARTEX outcomes are confirmed: secondary analysis. Not opened; round 2 lead for the dependence audit.
- Unit 42 (30 October note; 2 November post on X), Google GTIG and Mandiant, Wiz, CrowdStrike, GitGuardian, CERT-EU, CERT-In, WorkOS's own account: primary reports named by results or by S07, but no canonical URL was returned by the queries; guessed paths are not evidence. Round 2 leads (four targeted queries allowed).
- The developer's 8 October notice on GitHub: GitHub's pages return 403 from this container and the repository was reported removed. Not attempted.
- Malware Must Die indicator pack: lists attacker infrastructure; not opened by the brief's rule.
- arXiv results under Q6 (2601.05293, 2509.10682, 2608.26733, 2603.20953, 2506.08693) and Help Net Security on stolen Claude keys: not about ARTEX's credential loop on their titles; not opened.
- OODAloop's report of a joint Google and FBI alert dated 17 November: secondary, uncorroborated by the search; not opened.

## Prior reads (disclosed, not evidence under this protocol)

The commissioning conversation of 17 November opened S01, S02 and S03 through tool-rendered reads (brief, Prior knowledge). Leads L-0064 (Censys exposure counts) and L-0091 (Check Point's fleet report) relay S04 and S05; LH042, LH041 and LH051 are adjacent studies and supply no independent confirmation.
