# Scout 5, Research: horizon sweep 2026-11-17T1414Z

**In short.** Reading arXiv's five category listings for 17 November and seven abstract pages, plus four web searches, found no paper on armed robots and nothing on agent self-propagation newer than the 13 November sweep's set. The new material is on the instruments side: a measurement of who sets AI-training opt-outs (13 November), a method for ranking automated sessions by the harm they do instead of by bot label (13 November), and several agent-security papers with reported figures. Everything is "reported by" the page, read through WebFetch's summariser (abstracts and titles only; nothing checked against data).

Started 2026-11-17T14:16Z, ended about 14:25Z (UTC). Sonnet 5.5 scout.

## Gate

robots_gate.py run before each fetch, provider anthropic. Allowed, decided by "*": arxiv.org/list/{cs.CR,cs.AI,cs.NI,cs.CY,cs.SE}/recent (rule "Allow: /list"), arxiv.org/abs/<id> for the seven abs pages (rule "Allow: /abs"), and labs.cloudsecurityalliance.org (allowed, but not fetched; see below). Not fetched, carried from earlier sweeps and not re-checked: export.arxiv.org API, arxiv.org/search/, pam2027.net.

## Searches (WebSearch, standard mode, 4)

1. "AI agent web crawler traffic measurement paper November 2026". Results opened: none. Summary reported industry figures (DataDome: about 52.7 billion AI agent and crawler requests, 82.3% growth July 2025 to June 2026 over 75,000 customer sites; RudderStack: 179 million sessions, 29 in 10,000 AI), second-hand. Not opened: digitalapplied.com agentic-crawler 30-day log study; softwareseni.com; rudderstack.com/blog/we-looked-at-179-million-web-sessions-for-ai-agents; codeitbro.com; charonhub.deeplearning.ai; technologychecker.io Q3 2026; blog.cloudflare.com/ai-search-crawl-refer-ratio-on-radar; theadspend.com two-track-internet.
2. "LLM agents self-replication autonomous propagation study 2026 arXiv". Not opened: arxiv.org/pdf/2509.25302 (Agent Matrix), 2605.06760 (already in the 10 November file), arxiv.org/html/2603.15727 (ClawWorm, multi-hop propagation over up to 5 hops, reported by the summary), aisi.gov.uk RepliBench page, ai2027-tracker.com.
3. "IMC 2026 OR USENIX Security 2026 measurement AI crawlers robots.txt compliance study". Found no 2026 venue paper. Surfaced arxiv.org/abs/2505.21733 (IMC 2025 robots.txt compliance study) and a reported "ScrapeBench" NeurIPS 2026 result ("most AI agents comply with explicit scraping prohibitions below 5% of the time") via aiweekly.co, which is second-hand and not opened.
4. "arXiv November 2026 LLM agents vulnerability discovery open source maintainers disclosure burden". Not opened: labs.cloudsecurityalliance.org CSA note of 7 October 2026 (domain seen in earlier sweeps; this note's URL not opened here), infoq.com/news/2026/10/open-source-ai-security, techround.co.uk, letsdatascience.com oss-sec thread, atlanticcouncil.org dispatch, newx.sg "Demystifying the Mythos or Disrupting Bugonomics?" (no arXiv id seen).

Search tool is US-only and summarises; absence means little.

## Listings opened (all 200, read about 14:19Z)

| URL | Page date | Claim reported | New? |
|---|---|---|---|
| https://arxiv.org/list/cs.CR/recent | 2026-11-17 | 78 entries that day, first 50 shown; agent-security titles (MCP misbinding, risky fallback, compositional exploits, LLM honeypots, agent authentication). | seen URL, new content |
| https://arxiv.org/list/cs.AI/recent | 2026-11-17 | 428 entries, first 50 shown; "Safe Resemblance, Silent Propagation" (2611.21520), "From Recursion to Convolution: Parallel Self-Improvement for Multi-Agent Systems" (2611.20891), a harness ladder for 0.75B to 4.7B local models (2611.21407). | seen URL, new content |
| https://arxiv.org/list/cs.NI/recent | 2026-11-13 to 17 | 2611.18213 and 2611.18027 on crawlers and bots; 2611.21330 a crawler-free P2P size estimate. | seen URL, new content |
| https://arxiv.org/list/cs.CY/recent | 2026-11-16 to 17 | 2611.20670 on imputing agents' acts to delegators; 2611.20378 on shoppers asking AI first; 2611.18998 "Model Maps". Nothing on weapons, robotics or crawlers. | seen URL, new content |
| https://arxiv.org/list/cs.SE/recent | 2026-11-17 | 69 entries; agent instruction file reviews (2611.18582), token and energy traces (2611.20873). | seen URL, new content |

## Abstract pages opened

All 200, read 14:20Z to 14:22Z; none of the seven IDs appears in any earlier sweep file (grepped across notes/horizon).

| # | URL | Page date | Claim reported | New? |
|---|---|---|---|---|
| 1 | https://arxiv.org/abs/2611.18213 | 2026-11-13 | Crawl of about 3.45 million sites in Poland, Czechia, Slovakia, Hungary and Germany: opt-outs from AI training "range from 0.70% to 3.82%"; platform and host defaults account for 15% to 78% of them; "delegated consent, a signal that a platform sets on behalf of its users"; Common Crawl-derived lists miss about a third of Slovak opt-outs. | new |
| 2 | https://arxiv.org/abs/2611.18027 | 2026-11-13 | Ranks sessions by attributed cache harm, not bot label; on a 12.7-million-request trace the top 1% of sessions carry 48.8% of attributed harm and 49.1% of that top tier has no bot tag; "attributed cross-session harm as an outcome-based target". | new |
| 3 | https://arxiv.org/abs/2611.21577 | 2026-11-16 | MCP "tool-provider misbinding": requests "resolved to an attacker-controlled tool" across five LLM clients; no rates in the abstract. | new |
| 4 | https://arxiv.org/abs/2611.19764 | 2026-11-15 | Compositional exploits by coding agents combining safe tools: 560-task benchmark; unprotected frontier models succeed on 72.9% to 84.5% of exploit chains; five single-tool scanners detect 0%; "isolated tool auditing is fundamentally flawed." | new |
| 5 | https://arxiv.org/abs/2611.20514 | 2026-11-16 | Incomplete-fix bypass in LLM agent frameworks: a sibling path still violated the invariant in PraisonAI 4.6.31 and CrewAI 1.11.0; "applies only to the tested probe, version, and configuration". | new |
| 6 | https://arxiv.org/abs/2611.21235 | 2026-11-16 | Agents spread rumours built from truthful posts: acceptance above 65% in 12 of 14 models over 1,090 rumour targets. | new |
| 7 | https://arxiv.org/abs/2611.19719 | 2026-11-15 | Iterative LLM pipeline from vulnerability discovery to repair; "the subsequent code repair phase remains a primary bottleneck"; no rates in the abstract. | new |

## Seen on listings, not opened

2611.20389 (privacy of exported agent traces), 2611.18582 (reviews of agent instruction files), 2611.20378, 2611.20670, 2611.20988 (Hivemind, federated knowledge sharing between agents), 2611.20891, 2611.21520, 2611.20528 (LLM honeypots), 2611.19886 (risky fallback), 2611.19598, 2611.19536 and 2611.19551 (agent authentication and payments), 2611.20045, 2611.20873, 2611.18908 (MemeEconomy), 2611.18998, 2611.21330.

## Walls

None met. Listings gave titles only, so gists for unopened items are inferred from titles.

## Five best new leads

1. **2611.18213 (13 Nov): who sets the AI-training consent signal.** Measures opt-outs over 3.45 million sites and finds platform defaults account for 15% to 78% of them, with Common Crawl-derived lists missing about a third of one country's opt-outs. It bears directly on how Lighthouse reads robots.txt and opt-out signals as instruments (the closing-web study and the rules-of-the-road paper): a robots.txt group may be a host's default, not an owner's choice. Its first observations would not be lost; the crawl is dated, but a repeat later would need the same method.
2. **2611.18027 (13 Nov): ranking automated sessions by the harm they cause, not by bot label.** In its e-commerce trace, nearly half of the worst-harm tier carried no bot tag. This is a method for the charter's cost-to-shared-infrastructure question that does not depend on identifying AI. Static paper; nothing lost by waiting, though the data is private to the authors' trace.
3. **2611.19764 (15 Nov): compositional exploits by coding agents from individually safe tools.** Reported 72.9% to 84.5% success for unprotected models and 0% detection by single-tool scanners. A mechanism for how activity can leave harmful residue without any malicious component; a lab benchmark with the authors' own defence. Static; nothing lost.
4. **2611.21577 and 2611.20514 (15 to 16 Nov): MCP provider misbinding and incomplete-fix bypasses in agent frameworks.** Both give version-pinned cases (PraisonAI 4.6.31 and 4.6.32, CrewAI 1.11.0 and 1.11.1). The framework versions fixing these will move, so a dated snapshot of which versions are affected has a short window; the papers will not vanish.
5. **Open-source disclosure strain (CSA note of 7 Oct 2026, not opened; secondary summaries only).** Reports intake channels ended or paused in 2026 because AI-assisted submissions outpaced maintainers (curl's bounty ended; HackerOne's Internet Bug Bounty paused in April 2026, as reported). It connects the 13 November model-found-bugs papers (187 and 1,050 findings) to a shared-infrastructure effect. Worth a primary-source read next sweep; policy pages and bounty terms change, so a dated capture of the programmes' current status has some risk of being lost.

## Urgent

None. No window found.

## Notes

Physical authority: nothing in the five listings on armed robots or delegated force. No rule broken that I know of; no body saved, so no email redaction needed.
