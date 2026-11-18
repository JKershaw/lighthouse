# Scout 2, Security and vulnerabilities, run 2026-11-18T1300Z

**In short.** The largest new item is Google's threat-intelligence report of 16 November, which says a framework found on an exposed staging server compared popular web applications before and after each patch, drafted exploits and ran them with no human in the loop. The Amazon index shows no new post since the 13 November ARTEX post. KEV gained one entry (Perforce Puppet Enterprise, 17 November) since the 13 November version. Everything below is reported by the page named; "fetched by scout" marks a plain read of a feed. Nothing read was treated as an instruction. No email addresses recorded.

Start 13:02 UTC, end about 13:06 UTC (from `date -u`). Tools: robots gate with `LIGHTHOUSE_PROVIDER=anthropic` before each fetch; WebFetch (summariser relays, so quotations are as relayed); curl with User-Agent "Lighthouse-research" for the KEV, EPSS and oss-security reads; WebSearch standard, 4 searches.

## Direct publication checks

| Endpoint | UTC read | Outcome | Entries |
| --- | --- | --- | --- |
| https://aws.amazon.com/blogs/security/ (first check; no earlier scout log read this index) | 13:03 | New entries (baseline). Index showed five posts only, the summariser said the page was truncated after the fifth, so posts older than 11 Nov are not covered by this read (11 to 18 Nov window covered, as 11 Nov is the oldest shown). | 17 Nov: WAF Bot Control onboarding; 17 Nov: "Securely exposing Amazon Bedrock AgentCore Runtime" (AI agents runtime, microVM sessions; not about credential-to-compute abuse); 17 Nov: AWS RMiT workbook; **13 Nov: "Amazon Threat Intelligence observes threat actors running cybercrime campaigns with ARTEX AI agents" (CJ Moses), https://aws.amazon.com/blogs/security/amazon-threat-intelligence-observes-threat-actors-running-cybercrime-campaigns-with-artex-ai-agents/**; 11 Nov: "Ease of use and secure defaults in the new AWS experience". |

Amazon, flag for LH055: the only post bearing on ARTEX is the 13 November one (already LH055's source; not read by this scout). No new Amazon post since. The 17 November AgentCore Runtime post is adjacent (agent hosting security) but not reported as tied to ARTEX; not opened.

## What KEV added since 2026.11.13

Fetched by scout 13:03: catalogVersion 2026.11.17, released 2026-11-17T17:53Z, 1782 entries (1781 on 2026.11.13, one added). Added 17 Nov: CVE-2026-115731 Perforce Puppet Enterprise, deserialisation of untrusted data in report processing; reported to let a client with any CA-signed agent certificate run code on the server as the service user; due 1 December (14 days, unlike the three-day deadlines of 10 and 13 Nov); ransomware use Unknown. EPSS 17 Nov (fetched by scout): this CVE 0.0037 (percentile 0.31); NoisyTCP CVE-2026-99288 0.0016 (percentile 0.05), so low scoring for a pre-auth kernel flaw. EPSS top-movers query returned only nonsense-sorted IDs (CVE-2026-99999 and similar), so no top-mover read was possible; a coverage gap.

## Searches

1. "vulnerability found by AI model exploit disclosed November 2026": OpenAI GPT-6 Cyber coverage (bleepingcomputer, disallowed by robots, not opened), Google GTIG May 2026 zero-day (old), SiliconANGLE 16 Nov (opened), others secondary and older. Not opened: letsdatascience, darkreading, govinfosecurity, decrypt, infoq, thenextweb, bankinfosecurity.
2. "critical vulnerability actively exploited 17 November 2026": Patch Tuesday coverage (Action1, OPSWAT), Hacker News weekly recap (opened), bleepingcomputer Node2Shell (seen 7 Nov sweep, disallowed). Not opened: action1, opswat, sans, cybersecuritydive Citrix, itpro, orangecyberdefense.
3. "Forescout AI vulnerability research 10 TCP/IP stacks...": forescout pages (one opened), helpnetsecurity, ciodive, cybersecuritydive, webull, securityweek. Not opened except Forescout.
4. "Linux kernel OR OpenSSH OR nginx vulnerability AI model found ... November 2026": OpenAI "a thousand fewer paths to root" (4 Nov, per summary; 403 on open), phoronix, forklog, techspot, cybernews GhostLock, cpomagazine nginx, Red Hat Mythos blog. Not opened.

## Pages opened

| # | URL | Page date | UTC read | Status | New? | Claim reported |
|---|---|---|---|---|---|---|
| 1 | https://aws.amazon.com/blogs/security/ | 17 Nov top | 13:03 | 200 | new (first check) | see table above |
| 2 | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | 17 Nov | 13:03 | 200 | version new | 1782 entries; one added 17 Nov |
| 3 | https://api.first.org/data/v1/epss?cve=... | 17 Nov scores | 13:03 | 200 | values new | EPSS as above |
| 4 | https://projectzero.google/archive.html | latest 13 Nov | 13:03 | 200 | no new post since 13 Nov | latest is "Policy and Disclosure: 2026 Edition" |
| 5 | https://www.openwall.com/lists/oss-security/2026/11/ | to 18 Nov | 13:03 | 200 | entries partly new | titles only: ingress-nginx mirror-target self-DoS (CVE-2026-116472), CPython cookiejar and imaplib CVEs, several Vim advisories, sblim-sfcb pre-auth DoS, OpenStack OSSAs; no AI mention in titles; posts not opened |
| 6 | https://cert.europa.eu/publications/security-advisories/2026 | 18 Nov | 13:04 | 200 | new | 2026-021 (18 Nov) OpenJDK CVE-2026-114938, high, "could lead... to unauthenticated Remote Code Execution"; 2026-020 (12 Nov) Citrix NetScaler, "Citrix reports no exploitation" |
| 7 | https://siliconangle.com/?p=854090 | 16 Nov | 13:04 | 200 | new | headline "Google says an AI framework turned security patches into exploits with no human in the loop" |
| 8 | https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold | 16 Nov | 13:04 | 200 | new | GTIG (Blum, Vanderlee, Xia, Mainor): exploit_agent found on "an exposed staging server" does differential analysis around patches and "drafts exploits, and automatically executes them without human intervention"; first "without a human in the loop"; no confidence level stated for that. PaperCut CVE-2026-81578 and CVE-2026-82078, exploits "within a day of disclosure", GreyNoise campaign four days after disclosure vs "hundreds of organizations", "domain administrator within minutes". PentAGI-based platform scanning Asia late Aug to early Oct. No self-propagation described. LLMjacking: over $100,000 a day, up to $1 million cumulative; "burn and rotate" short-lived service accounts; LiteLLM sandbox escape CVE-2026-40217 used to raise virtual keys; stolen access resold at $0.10 to $25 per million tokens. |
| 9 | https://thehackernews.com/2026/11/weekly-recap-n-able-0-days-windows-0.html | 16 Nov | 13:04 | 200 | new | Recap: Forescout AI research (99 vulnerabilities, 90 hours); Project Zero schedule; SOCRadar "AI agents moved from building access for ransomware brands to running live encryption"; N-able N-central miners on 21 servers; Chrome CVE-2026-125350 exploited; bee-js 13.3.0 postinstall key stealer and Swarm Desktop 0.56.2; GeoVision XMRig on 13 organisations |
| 10 | https://www.forescout.com/?p=116183 | 12 Nov | 13:05 | 200 | new | Forescout: AI-assisted harness on 10 TCP/IP stacks, 99 validated, 66 new, 52% high or critical, about 90 hours, static analysis about $935; 54 reported to vendors; no CVE IDs or fix status on the page; search coverage said the team built on Claude models (not on the page) |

## Refusals and walls

- https://openai.com/index/a-thousand-fewer-paths-to-root/ : robots allowed, page returned HTTP 403 to WebFetch. Observation; not retried. Content known only from search summary (4 Nov, 948 kernel local privilege escalation exploits, about $1.2 million).
- bleepingcomputer.com: robots disallow (gate), not fetched.
- cybersecuritynews.com: robots unreachable, not fetched.
- api.github.com/advisories: gate allowed (robots 403), but the proxy returned 403 "sessions are bound to their configured repositories". GitHub advisory database not read; coverage gap. OSV and NCSC UK not read (robots 404 for both hosts' checked paths, time).
- robots.txt answered 404 for projectzero.google, api.first.org; 403 for api.github.com; treated as no rules by the gate.

## Search results not opened

As listed under each search.

## Quiet

No new Project Zero post since 13 Nov. No new Amazon Security Blog post on ARTEX since 13 Nov. CERT-EU shows no AI-related advisory. KEV shows one new entry in five days. oss-security titles show nothing explicitly AI-found.

## Five best new leads

1. **Google GTIG "Agentic Threat Activity Crosses a Significant Threshold", 16 Nov**, https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold (New). Reports the first fully autonomous patch-diff-to-exploit pipeline seen in the wild and a detailed LLMjacking and key-resale economy; it separates what AI does from what human operators do (no self-acquisition of compute reported). Bears on the charter's question on spread and sustaining. Feeds LH055 (ARTEX: independent account of the credential-to-compute loop, resale prices) and LH048/LH036 (patch-to-exploit time) and P-0033. A report is dated and persists; lost nothing quickly, but the framework's exposure is a one-off finding. Next: read the full post, then tabulate each claim with its stated confidence for LH055's cross-check (not collection by this scout).
2. **Patch-diff exploitation, PaperCut CVE-2026-81578 / CVE-2026-82078** (same page; GreyNoise's own report is the primary). Exploit "within a day", campaign on day four. A concrete timeline for P-0037 (Project Zero's shorter deadlines). Window: GreyNoise's tags and dates persist; low urgency. Next: locate GreyNoise's primary post.
3. **Forescout AI TCP/IP stack research, 12 Nov**, https://www.forescout.com/?p=116183 (New). 66 new flaws, 54 reported, no CVEs or fix status yet; a trackable case for P-0033 (do model-found bugs reach the vulnerability record) with a baseline now and CVE assignment later. Not lost if delayed, but the baseline of "no CVEs yet" is cheapest to capture now. Next: check the research report PDF and re-look for CVE IDs in two to four weeks.
4. **OpenAI "A thousand fewer paths to root", 4 Nov** (403 on open; search summary only), https://openai.com/index/a-thousand-fewer-paths-to-root/. 948 kernel privilege-escalation exploits and patches, kernel maintainers' report load reportedly 5 to 10 a day. Bears on whether model-found bugs flood shared maintainers; feeds LH036/LH054 context and P-0033. Already partly seen in the 10 Nov sweep (948). Next: an Opus scout with a different route (the lab's own repost or the kernel list) if useful; do not work around the 403.
5. **KEV deadline pattern and the Puppet Enterprise entry, 17 Nov** (feed above). Deadlines are now 14 days for this entry after three-day ones for 10 and 13 Nov; EPSS stays low (0.004). A daily snapshot series is lost if not saved (feed overwritten); continues lead 2 of the 17 Nov scout. Next: save dated copies of the feed.

Not new but updated: SOCRadar's agentic ransomware claim (Hacker News recap, 16 Nov) and bee-js (LH049/LH053 context) appear in the recap only.

Rule uncertainty: the gate allowed api.github.com on a robots 403 (treated as no rules); I followed the gate. KEV and EPSS were read by curl, as the previous sweep did.
