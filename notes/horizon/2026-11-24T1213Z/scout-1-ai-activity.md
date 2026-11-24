# Scout 1, AI activity on the internet, run 2026-11-24T1213Z

**In short.** All four direct checks gave a readable answer this time. Google's feed has nothing new since 19 November, Microsoft has one irrelevant post (SIEM ranking, 20 Nov), Anthropic's index has nothing new (newest 10 Sep 2026), and OpenAI's feed lists no misuse report but one relevant post, "Combatting adversarial distillation" (20 Nov), now opened. The wider search found no new vendor corroboration of Google's 16 November exploit_agent report, no new ARTEX primary report, and no in-the-wild self-spreading AI; the one new ARTEX item is a Cloud Security Alliance note that adds a cost argument, labelled as its own inference. Everything is "reported by" the page named; WebFetch is a summariser, so quotations are as relayed.

Start 12:15 UTC, end 12:16 UTC by the container clock (read times as logged; the ~ times above are approximate), 24 November 2026 (`date -u`). Tools: scripts/lh_feeds.py (provider anthropic), scripts/robots_gate.py, WebFetch, WebSearch (standard). No keys read, harbour/.session/ not searched, nothing committed, no bodies saved.

## Direct publication checks

| Endpoint | UTC read | Interval | Outcome | Relevant entries |
|---|---|---|---|---|
| Google feed https://feeds.feedburner.com/threatintelligence/pvexyqv7v0v | 12:15:23 | 20 to 24 Nov | No new entries (feed range 16 Jul to 19 Nov) | none |
| Microsoft feed https://www.microsoft.com/en-us/security/blog/feed/ | 12:15:24 | 20 to 24 Nov | One new entry, not relevant | 20 Nov, SIEM Gartner ranking, https://www.microsoft.com/en-us/security/blog/2026/11/20/microsoft-named-a-leader-in-the-2026-gartner-magic-quadrant-for-siem/ (not opened) |
| Anthropic index https://www.anthropic.com/threat-intelligence | ~12:16 (gate allowed; WebFetch 200) | 20 to 24 Nov | No new entries; newest "Detecting and countering misuse of AI: September 2026", 10 Sep 2026 | none |
| OpenAI feed https://openai.com/news/rss.xml | 12:15:25 | 20 to 24 Nov | New entries (7), none titled as a misuse report; feed range 2015-12-11 to 2026-11-23 | https://openai.com/index/combatting-adversarial-distillation (20 Nov, opened); https://openai.com/index/introducing-shirudo (23 Nov, OpenAI and Cisco, not opened); https://openai.com/index/perplexity-and-intelligence (22 Nov, not opened) |
| OpenAI misuse index (fallback) | not tried | | Gap carried forward from 18 and 20 Nov (403 then); feed gives no sign of a new misuse report | |

## Pages opened

| URL | UTC read | Gate | Status | Page date | Reported by the page |
|---|---|---|---|---|---|
| https://www.anthropic.com/threat-intelligence | ~12:16 | allowed | 200 | newest 10 Sep 2026 | Six entries, newest September 2026 (WebFetch listing). |
| https://openai.com/index/combatting-adversarial-distillation | ~12:20 | allowed | 200 (WebFetch answered this time) | 20 Nov 2026 | Distillation lets a second model gain capability "without the original model's safeguards"; protected-reasoning extraction success fell from 54.0% (GPT-6 Astra) to 0.2% (GPT-6.2 Astra) in one adaptive evaluation; weekly enforcement "thousands to tens of thousands of accounts". Does not say the attacking campaigns use agents. Lab and platform-abuse evidence, not spread. New URL. |
| https://labs.cloudsecurityalliance.org/research/csa-research-note-self-funding-agents-ai-gateway-key-harvest/ | ~12:20 | allowed | 200 | 18 Nov 2026 | Builds on Amazon's 13 Nov account (capture 3 Oct to 5 Nov); the zero-marginal-cost reasoning is CSA's own inference; "The self-funding loop rests on Amazon's captured records" and independent sources corroborate only the broader context; $740,000 (Railway estimate) relates to platform incidents, not specifically ARTEX. New URL (not in notes/horizon or LH055 by grep). |
| https://isc.sans.edu/diary/53 | ~12:20 | allowed | 200 | 23 Nov 2026 | Search snippet suggested an AI harvesting LLM access; the page is in fact an SSH scanning analysis (159 IPs in one subnet, 152 logging in and running one fingerprint command). Not about AI. Record as a mismatched search snippet. |

Gate allowed (not opened): https://thehackernews.com/2026/11/amazon-uncovers-ai-agent-campaign.html (already in LH055 queries).

## Searches (WebSearch, standard) and what was not opened
1. ARTEX stolen API keys compute Nov 2026: results are the known Amazon/FBI/Microsoft/CSA/Cybernews/VentureBeat/Hacker News/Register set; nothing dated after 20 Nov. Not opened: VentureBeat, Cybernews, letsdatascience, dailysecurityreview, secnews.gr, explainx, aichatdaily, theoutpost, CSA LLMjacking June note, Register (refused earlier).
2. GTIG "no human in the loop" corroboration: only secondary coverage of 16 Nov. Not opened: cyberscoop, bleepingcomputer, siliconangle, thehill, helpnetsecurity, esecurityplanet, itwire, oecd.ai incident, others.
3. Cloudflare/Imperva/Akamai Nov 2026: no new November bot report; Imperva/Thales 2026 report (53% of 2025 web traffic bot-driven, per summary), Akamai AI-pulse items, Cloudflare AI Insights dashboard. Not opened.
4. MCP/agent platform in-the-wild incident Nov 2026: none found; older OX Security STDIO and Sentry MCP items. Not opened.
5. Self-propagating agents in the wild: lab work (Anthropic/EPFL memory-file propagation, Fudan contained self-replication), Dark Reading forecast that agentic worms have not appeared in the wild. Unverified items (an undated production-node incident; MindStudio "Swarm Chasers fleet on Tencent Cloud") are not opened and treated as unverified.
6. GTIG exploit_agent coverage: primary titles named in snippets, https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold and .../ai-vulnerability-exploitation-initial-access, not opened this sweep (grep shows exploit_agent already in earlier sweep files). Snippet caveats from secondary: no victim count, patch-to-exploit latency, models used or operator.

## Refused or unreached
No robots refusals. No walls this time (OpenAI 403 gap of 18 and 20 Nov did not recur for the one page tried). OpenAI misuse index not retried.

## Quiet
No Anthropic or OpenAI misuse report; no Google or Microsoft AI-activity post; no new ARTEX primary; no independent corroboration of GTIG's exploit_agent; no confirmed in-the-wild self-spreading AI.

## Five best leads
1. **OpenAI "Combatting adversarial distillation", 20 Nov** (https://openai.com/index/combatting-adversarial-distillation, new). Reports mass account-level extraction campaigns and a drop in extraction success from 54.0% to 0.2% in one evaluation. Matters as lab-reported platform abuse and lab capability transfer (cyber capability moving by distillation), kept apart from open-internet spread. Next: note for LH-lab-capability reading; no study need.
2. **CSA self-funding note, 18 Nov** (https://labs.cloudsecurityalliance.org/research/csa-research-note-self-funding-agents-ai-gateway-key-harvest/, new URL). Explicitly says the self-funding loop rests on Amazon's records alone, with the zero-marginal-cost argument CSA's inference; also reports 1,600+ exposed ARTEX consoles (FBI) and 12,000+ forks (Wiz) via secondary. Matters as an independent statement of LH055's own finding (inconclusive, one source). Next: add to LH055 source log if the study accepts late reads.
3. **GTIG exploit_agent, 16 Nov** (https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold, already seen earlier). Still uncorroborated; secondary coverage notes no victim count, latency, models or operator. Matters for "when a model finds the bug" (patch-to-exploit timing). Next: watch for vendor or CERT corroboration; check the primary for the latency claim.
4. **Agentic worm status: lab versus wild** (Dark Reading 'Adaptive, Agentic AI Worms Loom', https://www.darkreading.com/cyber-risk/adaptive-agentic-ai-worms-enterprise-cyber-threat, seen only as snippet). Reports no agentic worm in the wild yet; Anthropic/EPFL and Fudan are lab results. Matters because it is the closest statement of the sustain-and-spread question's current state. Next: the primary papers in a later sweep (driving session, 24 November: Dark Reading's robots.txt disallows this URL for Lighthouse, so the article itself is not to be opened; it was seen only as a search snippet); unverified claims (Swarm Chasers, production-node incident) stay leads only.
5. **Bot-traffic baselines for LH045-style cost reading** (Imperva/Thales 2026 Bad Bot Report https://www.imperva.com/blog/bad-bot-report-2026-bots-agentic-age/ ; Akamai: AI bot traffic up over 300% while agentic traffic reportedly fell after Cyber Week 2025, per summary). Not opened; no November vendor report. Matters as the operator-side cost context. Next: open both and check the Akamai agentic decline claim. Not checked against earlier sweeps beyond a grep of the Imperva path.

## Withheld under research safety
None.

## Rule notes
The ISC snippet misdescribed its page; recorded as such. One robots-gate per opened URL was run before every WebFetch (Shirudo and ISC gates run; Shirudo not opened). Dedup by grep over notes/horizon and studies/LH055: the isc, CSA self-funding, distillation and Shirudo URLs had no match; exploit_agent had matches.
