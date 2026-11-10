# Scout 5, Research: horizon sweep 2026-11-10T1415Z

Started 2026-11-10T14:19Z, ended 2026-11-10T14:23Z (UTC). Sonnet 5.5 scout. Every claim below is "reported by" the page, read as an abstract or listing summary through WebFetch's small model, which paraphrased abstracts rather than quoting them; I read no full paper text and checked nothing against data. Quotations are therefore short and few.

## Method note: robots.txt gate

- The 7 November scout read arXiv through export.arxiv.org/api/query. The gate now says that host disallows everything ("Disallow: /", decided by "*"). Not fetched: robots.txt. The API is not used again; later sweeps should use arxiv.org/list and arxiv.org/abs, which the gate allows (rules "Allow: /list", "Allow: /abs").
- arxiv.org/search/ is disallowed by the gate: not fetched: robots.txt. A consequence: this scout cannot keyword-search arXiv, only read daily listings and known IDs, so coverage of 7 to 10 November is the listings' first 50 or so entries per category, and absence means little.
- pam2027.net: not fetched: robots.txt.

## Searches

1. WebSearch "arXiv November 2026 LLM agents autonomous exploitation in the wild honeypot measurement": only the 2024 Palisade LLM Agent Honeypot (2410.13919) and write-ups of it; nothing new. Not opened.
2. WebSearch "PAM 2027 accepted papers AI crawlers agents": no PAM list; trade-press items on AI crawler traffic (pebblous, ppc.land, Akamai blog, digiday) and 2601.02371 "Permission Manifests for Web Agents". Not opened.
3. WebSearch "NDSS 2027 accepted papers LLM agents vulnerability discovery": no 2027 list; LAST-X 2026 workshop page and preprints (FuzzingBrain V2, Co-RedTeam). Not opened.
4. WebSearch "paper AI agents propagate across repositories skills copying measurement arXiv 2611": led to "Skill Constellations" (read at its abstract) and 2607.00911; also aiweekly.co and UCL pages on GitSkills.
5. WebSearch "AI agent self-replication study new paper November 2026": only RepliBench (2504.18565, April 2025) and AISI pages. Not opened.
6. WebSearch "agentic crawlers web measurement study robots.txt compliance ... IMC": IMC 2025 "Scrapers Selectively Respect robots.txt" (2505.21733), 2411.15091, and trade press (TollBit via ppc.land and relevantaudience.com) reporting that about 15% of identified fetchers on European sites reached disallowed URLs, and a claim that Google's user-triggered Google-Agent fetcher "generally ignore[s] robots.txt". Search result only; none opened. Both vendor-policy claims came from one secondary source.
7. arXiv listings read directly (not searches): cs.CR, cs.NI, cs.CY, cs.SE, cs.AI "recent", dated 10 November 2026 (cs.NI back to 6 November).

## Sources read

| # | URL | Read (UTC) | Status | Page date | Claim reported | New? |
|---|---|---|---|---|---|---|
| 1 | https://arxiv.org/list/cs.CR/recent | 14:20 | 200 | 2026-11-10 | 93 entries that day; titles include agent-skill poisoning, agent swarms, MCP datasets, "Fingerprinting the LLMs and Harnesses Behind Agentic Attacks". | new |
| 2 | https://arxiv.org/list/cs.NI/recent | 14:20 | 200 | 2026-11-06 to 11-10 | 77 entries; no title on bots or crawlers; "Characterizing AI Service Traffic for 6G" (2611.07250) is the nearest. | new (2611.07250 seen as a title) |
| 3 | https://arxiv.org/list/cs.CY/recent | 14:21 | 200 | 2026-11-10 | Titles only; "FraudBench: A Legal Evaluation of AI Deception", frontier AI governance 2026; nothing on incidents or crawlers. | new |
| 4 | https://arxiv.org/list/cs.SE/recent | 14:21 | 200 | 2026-11-10 | 66 entries; "Coding Agents in KVM: Practical Containment..." and developer approval practices; nothing on AI-found vulnerabilities. | new |
| 5 | https://arxiv.org/list/cs.AI/recent | 14:21 | 200 | 2026-11-10 | "Detecting Shadow AI: Unsanctioned LLM Agents on Enterprise Endpoints" (2611.12377). | new |
| 6 | https://arxiv.org/abs/2611.12386 | 14:20 | 200 | 2026-11-09 | "Say Shibboleth": honeypot "shibboleth traps" infer an attacking agent's model (15 candidates, average 90% top-1) and harness (four harnesses, 92%) from telemetry; concealment instructions make declarations uninformative but behaviour still leaks. | new |
| 7 | https://arxiv.org/abs/2611.11455 | 14:20 | 200 | 2026-11-08 | "Coding Agents Propagate Vulnerabilities in Code Bases": insecure neighbouring code cut correct and secure outputs by 3.4% on average (backend, 96 tasks) and by 35.4% in C/C++ (20 task pairs); agents cite copying another code site in 76.5% of explanations. | new |
| 8 | https://arxiv.org/abs/2611.11861 | 14:20 | 200 | 2026-11-09 | Adaptive prompt injection with agent swarms; a stronger agentic attacker reliably gets models, including ones strong on public benchmarks, to follow instructions in tool output. No numbers in the abstract. | new |
| 9 | https://arxiv.org/abs/2611.11340 | 14:20 | 200 | 2026-11-08 | Agentic attribution of cloud resource ownership: 92.1% weighted recall, 86.6% precision on 100 AWS resources in one organisation. Defence-side, little for the charter. | new |
| 10 | https://arxiv.org/abs/2611.10948 | 14:20 | 200 | 2026-11-07 | Listing title was "Validating AI-Discovered Cloud Threats on Live Infrastructure", but the page returned a probability-theory lecture-notes abstract. Mismatch unexplained (summariser or cache fault); the paper is unread. | new |
| 11 | https://arxiv.org/abs/2611.11971 | 14:20 | 200 | 2026-11-09 | "Harness Matters": both the execution harness and the backend model significantly affect web-agent security; "harness-intrinsic security failures" occur without attack content. No numbers in the abstract. | new |
| 12 | https://aiweekly.co/alerts/agent-skill-copies-rarely-sync-upstream-github-map-finds | 14:21 | 200 | 2026-10-10 | Trade summary of "Skill Constellations"; its headline elsewhere says 50% of skills are verbatim copies (not in the abstract I read). | new |
| 13 | https://arxiv.org/abs/2610.11169 | 14:21 | 200 | 2026-10-08 | "Skill Constellations": dated copy network of SKILL.md files, 2,193,119 adoptions; copies "rarely change when their source does"; auditing 100 ranked repositories prevents 14.9% of later high-risk adoptions versus 0.5% for the 100 most-starred. | new |
| 14 | https://arxiv.org/abs/2607.00911 | 14:21 | 200 | 2026-07-01 (v2 07-06) | 18,463 registry skills and 23,199 personal skills; 3,709 reuse links; "53% are never modified after adoption". | new |
| 15 | https://arxiv.org/abs/2611.10843 | 14:22 | 200 | 2026-11-07 | SoK of attacks on agentic AI: 98 sources, 284 atomic attacks, "only 278 of 660 relationships are directly assessed". Review, not measurement. | new |
| 16 | https://arxiv.org/abs/2611.11104 | 14:22 | 200 | 2026-11-08 | MCP vulnerability dataset from CVEs: 119 records to 24 validated, 87.5% Critical or High. | new |
| 17 | https://arxiv.org/abs/2611.12377 | 14:22 | 200 | 2026-11-09 | Shadow-AI detector on endpoints: simple model suggests exponential growth of unsanctioned agent artefacts; 12 synthetic agents, one workstation; "not by behavior alone". Lab only. | new |
| 18 | https://arxiv.org/abs/2611.12823 | 14:22 | 200 | 2026-11-09 | KVM-Agent: containment of coding agents in replaceable VMs; risks remain from secrets and permitted network access. No numbers. | new |
| 19 | https://arxiv.org/abs/2611.12155 | 14:23 | 200 | 2026-11-09 | StealthyPoison: poisoned third-party skills keep advertised function; 566 target skills, over 26,000 registry entries; works in a Claude Code workflow on Opus 4.8. | new |
| 20 | https://www.ndss-symposium.org/ndss2027/accepted-papers/ | 14:22 | 200 | none shown | Returned the NDSS 2017 accepted list, not 2027. No 2027 list found. | new |
| 21 | https://www.ucl.ac.uk/engineering/news/2026/sep/ucl-led-dataset-opens-new-research-how-ai-coding-agents-are-instructed | 14:22 | 403 | n/a | Forbidden; a wall, recorded and left. The GitSkills dataset claim (MSR 2027 Mining Challenge) therefore rests on a search snippet only. | new |

## Not opened or refused

- Not fetched: robots.txt: export.arxiv.org API (disallowed for all), arxiv.org/search/, pam2027.net.
- Wall: UCL news page, 403.
- Search results seen, not opened: 2410.13919, 2504.18565, AISI RepliBench pages, 2505.21733, 2411.15091, TollBit coverage (ppc.land, relevantaudience.com), 2601.02371, LAST-X 2026 pages, FuzzingBrain V2, 2603.16572, Akamai AI-pulse blog, the aiweekly "50% verbatim" editor's blog and the Repo-To-Skill item.
- Listed on 10 November, not opened: 2611.11720 ShadowBench-MCP, 2611.12167 FraudBench, 2611.12434 frontier AI safety and governance 2026, 2611.10058 developers' approval practices, 2611.10098.
- Not re-read this sweep: IMC 2026 accepted list, USENIX Security '26 sessions, 2605.06760 (the 7 November lead 1). No new paper on in-the-wild replication surfaced; the 7 to 10 November listings carry none, which with a title-only view means little.

## Five best leads

1. **Fingerprinting the model and harness behind an agentic attack (2611.12386, 9 November).** Why it matters: it reports a way to tell which model and harness are driving an intruding agent from honeypot telemetry (90% top-1 over 15 models; 92% over four harnesses), the first step to attributing agent activity and measuring what share of hostile traffic is agentic. Fit: when a model finds the bug, and what AI activity costs the shared internet (as a method to classify traffic). Window: not lost; but one author overlaps the 2605.06760 self-replication paper's authors, so a follow-up may come soon. Use only as a method; Lighthouse would not run honeypots without a keeper decision.
2. **Skill Constellations (2610.11169, 8 October) plus 2607.00911 and StealthyPoison (2611.12155).** Why it matters: a dated copy network of 2,193,119 skill adoptions where copies "rarely change when their source does" is a measured carrier channel by which one agent's artefact reaches others, with a fix that does not travel back; it is the in-the-wild form of L-0008. Fit: software updates (copy lag as an update question) and spread. Window: GitSkills is a mining-challenge dataset, so a frozen snapshot likely persists, but the live GitHub histories keep growing; weeks, not days.
3. **Coding agents copy existing flaws (2611.11455, 8 November).** Why it matters: a lab result that insecure neighbouring code lowers secure output (35.4% in C/C++ context pairs) and that agents attribute their choices to copying (76.5%), i.e. a mechanism by which agent-written code could spread a bug already present; the charter's "sustain and spread" at code level. Fit: when a model finds or writes the bug, and software updates (does a fix reach agent-copied sites). Window: none urgent; lab study, not field data.
4. **Unsanctioned agents on endpoints (2611.12377, 9 November) with the containment paper (2611.12823) and agent swarm injection (2611.11861).** Why it matters: three papers in two days treat agent footprint, containment and injection as ordinary operations; the first models unsanctioned agent artefacts growing exponentially, a hypothesis not a measurement. Fit: weakly, what AI activity costs; mainly background for L-0007 and L-0021. Window: none.
5. **Method repair: arXiv's API is disallowed for automated readers; the 7 November scout used it.** Why it matters: the 7 November file's arXiv reading went through a host whose robots.txt (read 10 November) disallows everything for all agents. Whether it did so on 7 November was not checked; the gate's read of 10 November does not establish it. Fit: Lighthouse's own conduct under LH047 (the rules of the road) and L-0017 repair; not an investigation topic. Window: the robots.txt may change, so a dated read of both arXiv hosts' robots.txt now would preserve the evidence.

## Notes

- Scout-side limits: the summariser paraphrased abstracts and refused to quote, so figures are as it reported them; 2611.10948 returned a wrong abstract, which shows the tool can mislabel, and any figure above deserves a recheck on the page before use.
- NDSS's 2027 page URL returned the 2017 list; the 7 November file also found no official NDSS 2027 list.
- No paper in the 10 November listings measures AI-crawler traffic from CDN data; cs.NI had nothing on bots.
