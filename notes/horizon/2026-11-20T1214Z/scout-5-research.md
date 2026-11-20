# Scout 5, Research: horizon sweep 2026-11-20T1214Z

**In short.** The arXiv listings for 20 November held several papers that bear on Lighthouse's questions: a taxonomy of how LLM vulnerability-research capability has evolved (SoK, submitted 19 November), a replication study finding most real agent-harm incidents had no attacker (19 November), and a study of AI involvement in open-source bug reports (19 November). The Thursday 19 November listings for cs.CR, cs.AI and cs.SE were only partly visible. Everything is "reported by" the paper, read through WebFetch's summariser from abstract pages; nothing here is Lighthouse's observation.

Started about 12:16Z, ended about 12:20Z, 20 November 2026 (`date -u` read 12:16:02Z and 12:17:06Z). Sonnet 5.5 scout; tools: robots_gate.py, WebFetch, WebSearch, grep against earlier sweep files. No direct publication checks assigned to this scout.

## Listings checked and coverage

All read about 12:16Z, gate allowed ("Allow: /list", decided by "*"). Summaries are title-based and partial.

| Listing | Shown | Not seen |
| --- | --- | --- |
| cs.CR /recent | Fri 20 Nov, 50 of 50 | Thu 19 Nov entries (heading only in navigation) |
| cs.AI /recent | Fri 20 Nov, first 50 of 252 | rest of 20 Nov; Thu 19 Nov and earlier (heading only) |
| cs.NI /recent | Fri 20 Nov 9 of 9; Thu 19 Nov 11 of 11 | other 44 of 64 (earlier dates) |
| cs.SE /recent | Fri 20 Nov 30 of 30; Thu 19 Nov first 20 of 99 | 79 of Thu 19 Nov |
| cs.CY /recent | Fri 20 Nov 15; Thu 19 Nov 16 (both in full) | none |

arXiv's "Fri 20 Nov" heading holds papers submitted 18 to 19 November. Gap carried forward: Thu 19 Nov cs.CR, cs.AI and the rest of cs.SE.

## Searches (WebSearch, standard, 2)

1. "arXiv November 2026 LLM agents self-propagating prompt worm multi-agent infection". No November paper. Surfaced ClawWorm 2603.15727 (March; known), prompt infection background, and 2608.10218 (opened below; in the 7 Nov sweep file only).
2. "NDSS 2027 OR IEEE S&P 2027 accepted papers LLMjacking OR AI crawler robots.txt measurement". No accepted-paper list for either venue surfaced; only preprints (2505.21733, 2510.10315, 2411.15091, an NTU repository PDF, a CCR "From robots.txt to ai.txt" DOI) and a Seer Interactive blog, none opened. Reported by snippets only: 7.42% of 582,281 robots.txt files list an LLM bot; 60.0% of reputable news sites disallow an AI crawler against 9.1% of misinformation sites. LLMjacking not searched separately, no venue list opened.

## Papers opened (abs pages, gate allowed, status 200 unless noted)

All URLs https://arxiv.org/abs/<id>. "New" means no match for the id in notes/, studies/ or proposals.md.

| id | Date | UTC read | New? | Reported claim |
| --- | --- | --- | --- | --- |
| 2611.26553 | 19 Nov 2026 | 12:17 | New | ROGUE-AI "reproduce[s] the reported harm in 89% of its 108 attempted replications"; of 72 real-harm incidents, "62 had no attacker"; agents on five current models "made the reported mistake in 18% to 33% of runs" against "at most 1%" without the blamed cause; a hazard-naming warning after each tool output lowered harm. |
| 2611.26601 | 19 Nov 2026 | 12:17 | New | SoK on LLM capability in vulnerability research: disclosed vulnerabilities in 2026 "more than doubled"; open-weight models later reached "comparable autonomy for discovery and validation"; lifecycle timing, such as report-to-fix and disclosure-to-attack, "has not shifted noticeably so far". |
| 2611.25605 | 19 Nov 2026 | 12:17 | New | "first large-scale study of 120,918 bug reports from 101 open-source projects" (Jan 2024 to Sep 2026): AI-involved reports become more complete; maintainers spend more effort on AI-assisted reports of human-found bugs; authors' 53 reports of AI-found bugs, 69.81% accepted. |
| 2611.26525 | 19 Nov 2026 | 12:17 | New | Origin, a tool to find the "compromise entry point" after agent-application incidents; case studies on five agent apps, eight incidents. |
| 2611.25086 | 18 Nov 2026 | 12:17 | New | Browser-embedded local models (Gemini Nano in Chrome) as post-exploitation engines "invisible to network monitoring"; authors report a simulated end-to-end operation. Mechanism not detailed here. |
| 2611.23664 | 18 Nov 2026 | 12:17 | New | CratesBump: about 220,000 crates, over two million consecutive release pairs, 41 features; some minor and patch releases "break the public API despite their version numbers". Dataset released openly. |
| 2611.23841 | 18 Nov 2026 | 12:17 | New | "Capability Internet" architecture for autonomous agents exchanging capabilities, federated compute and "governance and settlement"; no experimental results. |
| 2611.24983 | 17 Nov 2026 | 12:17 | New | Fixed-budget (5% of CVEs) comparison of CVSS and EPSS: 2025 EPSS captures 16 of 40 positives against 5 for CVSS; Q1 2026 CVSS 4 of 11, EPSS 3; "tie-breaking can reverse this ordering". |
| 2606.03811 | 2 Jun 2026 | 12:18 | Not new (18 Nov log, via search); now opened | Worm that "parasitically uses compromised machines to run open-weight large language models", "marginal cost per new infection is zero"; "self-sustaining AI-driven cyber-threats are no longer theoretical". Abstract reports no figures; the 18 Nov log's 82%/44%/88% did not appear on this page read. |
| 2608.10218 | 10 Aug 2026 | 12:18 | Not new (7 Nov sweep); opened now | Mind Viruses: ideas that spread via agents; harmful payloads "spread less well than benign ones"; frontier models generally less susceptible; a brief system-prompt warning gives "near-total immunity"; "a real but currently limited risk". |

## Seen on listings, not opened (all New by grep)

2611.25821 and 2611.24989 (agent commerce mandates and crypto wallet signatures), 2611.25599 (Tether, policy engine for agents), 2611.25562, 2611.25470, 2611.25056 (decentralised multi-agent attacks), 2611.25832, 2611.25718, 2611.25809 (multi-agent IoT pentest), 2611.25412 (ChainAgent PHP), 2611.26131 (SCARVA supply chain), 2611.25790 (CyberGym reliability), 2611.25590, 2611.26134 (RouterWeave, home-router activity), 2611.26086, 2611.25760 (unfaithful work reports by coding agents), 2611.26312, 2611.26311, 2611.25394 (1-day detection), 2611.24269 (LLMs adapting Linux drivers), 2611.24927 (AI supply chain mapping), 2611.25955 (web search and local news), 2611.25202. Also the earlier-sweep results not re-opened.

## Refusals and walls

None met. Closed to the gate last time and not retried: export.arxiv.org, arxiv.org/search, pam2027.net. No venue accepted-list page was opened (none located).

## Quiet

No arXiv paper this window on robots.txt or crawler compliance, LLMjacking or LLM API credential abuse, PyPI/npm download counts, GH Archive or Common Crawl as instruments; none on armed robotics. No IMC, USENIX Security, NDSS or S&P list reached.

## Five best leads

1. **2611.26601, SoK on LLM vulnerability-research capability (19 Nov).** https://arxiv.org/abs/2611.26601. Reports that report-to-fix and disclosure-to-attack timing "has not shifted noticeably so far" while disclosures doubled. Directly comparable to the core watch of the model-found-bugs investigation (LH036, LH038, LH054) and a literature check for any account there. Next step: read full text for its data sources and grading of "evidence strength".
2. **2611.26553, ROGUE-AI (19 Nov).** https://arxiv.org/abs/2611.26553. Reports 62 of 72 real agent-harm incidents had no attacker, so harm to shared systems may come from agents following tasks, not from adversaries. This bears on the charter question (and the cost-and-spread investigation's load and exposure) because unattended agents could degrade infrastructure without any worm. Next step: read for the incident source list and whether it can serve as a catalogue of agent-caused incidents.
3. **2606.03811 and 2608.10218, worm and mind-virus papers.** https://arxiv.org/abs/2606.03811, https://arxiv.org/abs/2608.10218. Two reported lab capability results on self-sustaining spread, one by exploitation with stolen compute, one by ideas passed between agents (limited risk reported). Central to the "spread" half of the charter question and the lab-capability strand of the cost-and-spread investigation; both are lab claims, not observed activity. Next step: full text of the first for its stage rates (the 18 Nov log's figures were not on the abstract page).
4. **2611.25605, AI in open-source bug reporting (19 Nov).** https://arxiv.org/abs/2611.25605. Reports 120,918 reports from 101 projects, Jan 2024 to Sep 2026, and maintainer effort shifting to AI-assisted reports. Bears on maintainer load from model-found bugs (LH036 and LH054 readings of maintainer response) as an independent measurement. Next step: read for the project list and whether its tagging could be reused.
5. **2611.23664, CratesBump (18 Nov).** https://arxiv.org/abs/2611.23664. An open dataset of over two million crates.io release pairs, with API-break audit. A candidate instrument for how releases are labelled and how far version numbers can be trusted in the software-updates investigation (uptake depends on dependents' ranges). Next step: check whether Cargo's pre-1.0 rule finding transfers to the update-uptake questions; no study currently covers crates.io.

Honourable mention: 2611.24983 (CVSS vs EPSS under fixed budget), relevant to using EPSS as an instrument.

## Urgent

None.

## Notes

No body saved, no email addresses seen, no keys read. Summariser output is partial and title-based for listings; absence means little.
