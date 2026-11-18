# Scout 5, Research: horizon sweep 2026-11-18T1300Z

**In short.** The arXiv listings for 18 November (and 17 November where visible) held no paper on agent self-propagation or armed robotics. The new papers that bear on Lighthouse's instruments are a measurement of exploitation-to-patch timing built from KEV and exploitation sightings (submitted 17 November), a study of unbackported security fixes in GitHub Actions workflows (17 November), and a coding-agent exploitation benchmark study (17 November). Everything is "reported by" the page, read through WebFetch's summariser from listings and abstract pages only.

Started 2026-11-18T13:02Z, ended about 13:04Z (UTC). Sonnet 5.5 scout. No direct publication checks assigned to this scout.

## Listing dates covered

arXiv /list/<cat>/recent, read 13:03Z. cs.CR: 18 Nov (all 42 entries) and the first 8 of 17 Nov (78); cs.AI: 18 Nov first 50 of 259, and the 17 Nov heading; cs.NI: first 50 of 79 entries across 16 and 17 Nov (page showed 13 to 17 Nov headings; nothing for 18 Nov seen); cs.CY: 18 Nov and 17 Nov sections only; cs.SE: 18 Nov (50 of 50). Unshown entries (cs.CR 17 Nov beyond 8, cs.AI beyond 50, cs.NI 51 to 79) were not seen; yesterday's sweep read 17 Nov cs.CR/cs.AI first 50. Summariser output for listings is partial and title-based.

## Gate

robots_gate.py (provider anthropic) allowed all five listing URLs ("Allow: /list", decided by "*") and the six abs pages ("Allow: /abs"). Not retried: export.arxiv.org, arxiv.org/search, pam2027.net.

## Searches (WebSearch, standard, 3)

1. "IMC 2026 Internet Measurement Conference accepted papers AI crawlers agents". Reported: IMC 2026 held 12 to 16 October 2026 in Karlsruhe; cycle 1 accepted list posted 22 July 2026 at conferences.sigcomm.org/imc/2026/ (not opened, seen in the 7 Nov sweep); no 2026 AI-crawler paper surfaced; IMC 2025 "Somesite I Used To Crawl" and the NeurIPS "ScrapeBench" claim (below 5% compliance) resurfaced.
2. "arXiv November 2026 LLM agent self-replication OR rogue deployment OR autonomous spread paper". No November paper. Surfaced 2605.06760 (known), 2603.15727, 2509.25302 (seen yesterday), and 2606.03811 "AI Agents Enable Adaptive Computer Worms" (June 2026; reported figures: vulnerability identification 82%, exploitation 44%, self-replication in 88% of compromised hosts, on one 80GB GPU; not in earlier sweep files; not opened).
3. "arXiv 2611 LLM-found vulnerabilities CVE disclosure open source maintainers measurement". No 2611 paper. Surfaced (all secondary, not opened): VulnCheck audit (model rated 91.5% of findings critical or high, maintainers 51.3%), a Patrick Garrity figure (fewer than 1% of Mythos findings marked fixed), CSA note PDF (seen in 10 and 13 Nov sweeps), lwn.net/Articles/1070698 (parallel discovery in embargo), techtarget Glasswing results article.

## Pages opened

| # | URL | Page date | UTC read | Status | New? | Claim reported |
|---|---|---|---|---|---|---|
| 1-5 | https://arxiv.org/list/{cs.CR,cs.AI,cs.NI,cs.CY,cs.SE}/recent | 2026-11-18 | 13:03 | 200 | seen URL, new content | see above and below |
| 6 | https://arxiv.org/abs/2611.22479 | 17 Nov 2026 | 13:03 | 200 | New | "Exploited Before It Was Fixed? Vulnerability Timelines from Open, Machine-Readable Evidence" (Bonhomme, Dulaunoy; Vulnerability-Lookup): 3,758 identifiers with exploitation evidence, 98% with disclosure dates, 15.7% with patch evidence; "Vendor-side dates ... entirely absent"; 1,041 exploitation dates from bulk catalogue imports; 59 with patch evidence after exploitation evidence; median exploitation-to-patch 7.6 days; one collector misclassified exploit publications as active exploitation, "40% of initial exploitation dates"; another gave publication timestamps to 11% of listings. |
| 7 | https://arxiv.org/abs/2611.22888 | 17 Nov 2026 | 13:03 | 200 | New | "Stopping Is Not the Limit" on ExploitBench with DeepSeek-V4-Flash-0731 and MiMo-V2.6-Pro: agents "often stop with budget remaining"; MiMo with the authors' SCoRe method reaches 67.0% capability coverage at 2,000 turns against 32.4% for its original stopping policy; GPT-5.5 58.6% from 300-turn reference results. Preprint. |
| 8 | https://arxiv.org/abs/2611.22519 | 17 Nov 2026 | 13:03 | 200 | New | "Missing Security-Fix Backporting for GitHub Actions Workflows": 1,903,191 workflow commits, 69,865 security fixes across 24,238 projects (zizmor); 224,392 of 474,490 audited release branches still vulnerable; median backport lag 243 days; 176 issues filed, 44 confirmed or fixed. |
| 9 | https://arxiv.org/abs/2611.21784 | 16 Nov 2026 | 13:03 | 200 | New | "Revisiting the Survival of Agent-Attributed Code": 854,139 lines, 2,802 merged PRs, 215 repos (AIDev dataset), 88 survival analyses; for Devin "measurement choices determine the verdict"; clustering by repository cuts significant specifications from 15 of 22 to 3. |
| 10 | https://arxiv.org/abs/2611.22761 | 17 Nov 2026 | 13:03 | 200 | New | Unauthenticated configuration weakness in an LLM-controlled desktop social robot (Reachy Mini Lite) changed behaviour on hardware; 11 prompt injections resisted; CVSS 6.5; authors say recurrence in sampled repositories, "not prevalence in commercial products". Consumer robot, not armed. |
| 11 | https://arxiv.org/abs/2611.21956 | 16 Nov 2026 | 13:03 | 200 | New | "Eight in Ten LLMs Leak System-Prompt Secrets": an agent steered by a human extracted a 16-character flag from 296 of 363 OpenRouter models (plus 4 newer); 170 captures used a non-English pivot. |

## Seen on listings, not opened (all New by grep)

2611.22971 (SEAM, computer-use agents commit harm they recognise), 2611.22589 (LLM-driven honeypots vs LLM attackers), 2611.22583 (evolving agent safety harnesses), 2611.22223 (privacy leaks by web agents), 2611.23202 (cross-organisation agent trust and identity architecture), 2611.22525 (stale agent skills), 2611.23067 and 2611.23068 and 2611.23138 (self-improving agents), 2611.21626, 2611.22323, 2611.21957 (agent-driven dataset factory), 2611.22835, 2611.21811 (ARC-2, continuous compliance for robotic systems), 2611.22033, 2611.21822 (vibe coding threat landscape).

## Refusals and walls

None met.

## Quiet

Nothing found on armed robots or delegated force. Nothing on self-propagation newer than the 17 November set. No crawler or robots.txt paper newer than 2611.18213 and 2611.18027 (13 to 16 Nov, covered yesterday); no cs.NI entry for 18 Nov was visible. No package-registry paper. No IMC, USENIX Security, NDSS or PAM 2026 or 2027 paper on AI crawlers found.

## Five best new leads

1. **2611.22479, exploitation-to-patch timelines from KEV and sightings (17 Nov).** https://arxiv.org/abs/2611.22479. Reports that vendor patch dates are missing and that one collector's misclassification inflates 40% of initial exploitation dates. It bears on Lighthouse's own use of KEV and EPSS as clocks (AGENTS.md: "the event or clock matches the question") and on P-0033 and LH054's comparison of time to the vulnerability record. Feeds P-0033, LH036/LH054 clock definitions. Nothing lost by waiting (static preprint). Next step: read the full text for the collector names and the classification rule.
2. **2611.22519, unbackported security fixes in GitHub Actions workflows (17 Nov).** https://arxiv.org/abs/2611.22519. Reports 224,392 of 474,490 release branches still vulnerable, median lag 243 days: a large measured version of "fixes do not reach where software is built", the software-updates theme, and context for LH051 (WFX Phantom) and P-0012 (pull_request_target, enforcement 2 December). Nothing lost by waiting. Next step: read for the pull_request_target class share and any dataset release.
3. **2611.22888, agents stopping early in long-horizon exploitation (17 Nov).** https://arxiv.org/abs/2611.22888. Reported capability gain from continuation (32.4% to 67.0%) suggests measured agent capability depends on harness stop policy, relevant to reading lab capability claims in the cost-and-spread investigation and LH048. Lab benchmark with the authors' own method; open-weight models. Nothing lost. Next step: note as a caveat on capability readings.
4. **2606.03811, "AI Agents Enable Adaptive Computer Worms" (June 2026, via search only).** Not opened; reported 82% / 44% / 88% stage rates on a single locally hosted open-weight model. Bears directly on the charter's spread question and sits beside 2605.06760 and 2603.15727. Feeds the ai-cost-and-spread investigation and a possible "lab capability" inventory. Nothing lost. Next step: gate and read the abstract page next sweep.
5. **2611.21784, how measurement choices decide the verdict on agent-attributed code (16 Nov).** https://arxiv.org/abs/2611.21784. A methods warning: repository clustering cut significant specifications from 15 of 22 to 3. It is a close analogue of Lighthouse's pooled versus per-unit lesson, and the AIDev dataset is a candidate source for agent activity in repositories. Nothing lost. Next step: check AIDev's availability and licence as an instrument.

## Urgent

None.

## Notes

Rules followed as far as I know; no body saved, no email addresses seen. Listing summaries are partial, so absence means little.
