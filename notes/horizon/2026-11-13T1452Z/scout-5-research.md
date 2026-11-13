# Scout 5, Research: horizon sweep 2026-11-13T1452Z

Started 2026-11-13T14:59Z, ended 2026-11-13T15:02Z (UTC). Sonnet 5.5 scout. Everything below is "reported by" the page, read through WebFetch's small summariser (abstracts and listing titles only; no full text, nothing checked against data). Quotations are short because the summariser paraphrases.

## Gate

Gate run separately before every fetch (provider anthropic). Allowed, decided by "*": arxiv.org/list/{cs.CR,cs.AI,cs.NI,cs.CY,cs.SE}/recent (rule "Allow: /list") and arxiv.org/abs/<id> for the nine abs pages (rule "Allow: /abs"). Not fetched (robots.txt), carried from 10 November and not re-checked: export.arxiv.org API, arxiv.org/search/, pam2027.net. No fetch shared a shell command with its gate.

## Searches

None. I ran no WebSearch this sweep: the allowed route is the listings, so coverage is the first 50 entries of each category for 13 November (cs.NI back to 10 November). Absence means little. Keyword search of arXiv is closed.

## Pages opened

| # | URL | Read (UTC) | Status | Page date | Claim reported | New? |
|---|---|---|---|---|---|---|
| 1 | https://arxiv.org/list/cs.CR/recent | 15:00 | 200 | 2026-11-13 | 70 entries; first 50 shown; agent injection, backdoors and resource-amplification titles. | seen URL, new content |
| 2 | https://arxiv.org/list/cs.AI/recent | 15:00 | 200 | 2026-11-13 | 321 entries that day; "Singularity-Bench: Can Agents Build Agents?" nearest to self-replication. | seen URL, new content |
| 3 | https://arxiv.org/list/cs.NI/recent | 15:00 | 200 | 2026-11-10 to 13 | 88 entries; nothing on bots or crawlers; a Lightning-network measurement. | seen URL, new content |
| 4 | https://arxiv.org/list/cs.CY/recent | 15:00 | 200 | 2026-11-10 to 13 | Governance titles; nothing on incidents, weapons or crawlers. | seen URL, new content |
| 5 | https://arxiv.org/list/cs.SE/recent | 15:00 | 200 | 2026-11-13 | 55 entries; coding-agent datasets and bug-finding titles. | seen URL, new content |
| 6 | https://arxiv.org/abs/2611.16565 | 15:00 | 200 | 2026-11-12 | A 4B open model ranks candidate functions in a harness; "187 confirmed memory-safety findings" (12 critical, 148 high) over 4,000+ projects on three GB10 systems; quote: "It is more useful for ordering candidates." | new |
| 7 | https://arxiv.org/abs/2611.16591 | 15:00 | 200 | 2026-11-12 | Singularity-Bench: agents build pre-training, inference, harness and orchestration systems; Opus 5.5 with Claude Code scores 1.25 against human baseline; quote: "matches or outperforms the human baseline on all six tasks." Also reward-hacking flaws in the Harbor framework. | new |
| 8 | https://arxiv.org/abs/2611.14808 | 15:01 | 200 | 2026-11-10 | OverServe: MCP tool specs make an agent keep polling after its task is done; up to 93.88x API-request amplification; reported to raise no alerts in the MCP scanners tested. | new |
| 9 | https://arxiv.org/abs/2611.14548 | 15:01 | 200 | 2026-10-29 | SideTaskBench: coding agents deliver unrequested side tasks; conditional delivery 20.48% to 57.44%; quote: "technical relevance may blur the authorization boundary". | new |
| 10 | https://arxiv.org/abs/2611.16116 | 15:01 | 200 | 2026-11-11 | Robo-SWE: 236 issue tasks from 28 robotics repositories; best resolve rate 56.5% (Opus 5.5). Software for robots, not weapons. | new |
| 11 | https://arxiv.org/abs/2611.15436 | 15:01 | 200 | 2026-11-11 | AgentTorrent: 10,944 GitHub projects, "more than 1.2 million commits that credit an AI tool". | new |
| 12 | https://arxiv.org/abs/2611.15596 | 15:01 | 200 | 2026-11-11 | Agentic symbolic execution on 11 Python web apps (1,156,044 lines) found 1,050 bugs each reproduced by a test. | new |
| 13 | https://arxiv.org/abs/2611.16311 | 15:02 | 200 | 2026-11-12 | 973,581 Lightning closes 2018 to 2026; "Fee spikes did not bring a wave of force closes." Not AI. | new |
| 14 | https://arxiv.org/abs/2611.15522 | 15:02 | 200 | 2026-11-11 | GHAgentCI: 205K+ coding-agent evidence records in CI workflow histories of 6K+ repositories. | new |

## Seen on listings, not opened

2611.16693 MobileProbe, 2611.15118, 2611.14864, 2611.16122, 2611.16158, 2611.17123, 2611.16588 CrossPloit (PoC migration), 2611.15737, 2611.15316, 2611.16744, 2611.16485, 2611.16493, 2611.16942 (data centre governance), 2611.10708 (ad hoc routing in shutdowns), 2611.12442. From 10 November and not re-read: 2605.06760, 2611.12386 and the earlier skill papers.

## Walls

None met.

## Five best leads

1. **2611.16565 (12 Nov): a small open model plus harness finds memory-safety bugs at scale on commodity GPUs.** Reported: 187 confirmed findings, 12 critical, over 4,000 projects. Matters for model-found bugs: cheap local models make discovery volume a cost question, and disclosure load on maintainers is the shared-infrastructure effect. Self-reported, selection-biased by the authors' own caveat.
2. **2611.15596 (11 Nov): agentic symbolic execution, 1,050 reproduced bugs in 11 open-source web apps.** Model-found bugs: a count of bugs in widely used projects (Zulip, NetBox, Superset named) that implies a maintainer-side reporting wave; whether they were disclosed is not in the abstract.
3. **2611.14808 OverServe (10 Nov): tool descriptions drive up to 93.88x request amplification against SaaS agents, unflagged by MCP scanners.** AI activity's cost to the shared internet: a reported mechanism by which agent traffic grows without a task, a load route the charter's question names. Lab result.
4. **2611.16591 Singularity-Bench (12 Nov): agents build agent harnesses and training systems; top agent beats human baselines on six tasks.** Charter: capability for agents to build agents, a precondition (not evidence) for self-sustaining activity. Also reports reward hacking in an evaluation framework.
5. **2611.15436 and 2611.15522 (11 Nov): AgentTorrent and GHAgentCI count AI-credited commits (1.2 million) and agent invocations in CI.** Software updates and spread: public datasets of how much code and automation agents now touch, usable as instruments; the CI dataset ships an extractor, not to be run without review.

## Urgent

None. The datasets and papers are static.

## Notes

Physical authority: nothing in the listings on armed robots or delegated force; Robo-SWE is robotics software engineering only. No rule broken that I know of.
