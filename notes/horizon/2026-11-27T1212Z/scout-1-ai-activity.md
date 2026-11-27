# Scout 1, AI activity on the internet, run 2026-11-27T1212Z

**In short.** Google's feed and Anthropic's index have nothing new; OpenAI's feed lists no misuse report and its misuse index page, retried, loads but carries only a February 2025 article (the gap is closed as "no newer report visible there"). The one new primary is Microsoft's ARTEX post of 25 November, opened: Microsoft reports its own telemetry of actors using ARTEX for intrusion, and says nothing of credentials harvested to fund compute and nothing of self-spread. Nothing new bears on Cairn (LH059) beyond already-held Amazon material, and no in-the-wild self-spreading AI was found; lab results and field claims are kept apart. All quotations came via WebFetch (a summariser) unless stated.

Start 12:14 UTC, end about 12:16 UTC by `date -u` (27 Nov 2026). Tools: scripts/lh_feeds.py, scripts/robots_gate.py (LIGHTHOUSE_PROVIDER=anthropic, strict), WebFetch, WebSearch. No keys read, harbour/.session/ not searched, nothing committed, no bodies saved (scratchpad dir unused).

## Direct publication checks

| Endpoint | UTC read | Interval | Outcome | Relevant entries |
|---|---|---|---|---|
| Google feed https://feeds.feedburner.com/threatintelligence/pvexyqv7v0v | 12:14:39 | 24 to 27 Nov | No new entries (range 16 Jul to 19 Nov) | none |
| Microsoft feed https://www.microsoft.com/en-us/security/blog/feed/ | 12:14:40 | 24 to 27 Nov | 2 new entries | 25 Nov "What defenders need to know about ARTEX, the agentic AI framework threat actors abuse", https://www.microsoft.com/en-us/security/blog/2026/11/25/what-defenders-need-to-know-artex-agentic-ai-framework-threat-actors-abuse/ (opened; new URL by grep). 25 Nov Gartner email security leader post (irrelevant, not opened) |
| Anthropic index https://www.anthropic.com/threat-intelligence | ~12:15 (gate allowed) | 24 to 27 Nov | No new entries; newest "Detecting and countering misuse of AI: September 2026", 10 Sep 2026 | none |
| OpenAI feed https://openai.com/news/rss.xml | 12:14:41 | 24 to 27 Nov | 5 new entries (to 24 Nov), none a misuse report | GPT-6 protein design; Astra planets; three customer stories (iFood "scales coding agents across 15,000 repositories", not opened). Nothing relevant opened |
| OpenAI misuse index https://openai.com/global-affairs/disrupting-malicious-uses-of-ai/ | ~12:15 (gate allowed) | | Retried, loaded (no 403). Page is the 21 Feb 2025 article; no dated newer reports listed | gap closed for now |

## Standing-source results

Only the four named checks plus search. No new vendor corroboration of Google's 16 Nov exploit_agent report found. Cairn: the Amazon primary (https://aws.amazon.com/blogs/security/chinese-nexus-actors-cairn-ai-agents-found-a-zero-day-on-their-own/, 20 Nov) is already held in LH059 and the 24 Nov scout 2 log; gate allowed, not reopened.

## Searches (WebSearch)

1. "ARTEX agentic framework threat report CrowdStrike Huntress Wiz November 2026": FBI FLASH 13 Nov (ic3.gov 261113.pdf, already in 20 Nov sweep), Wiz 23 Nov agentic cloud intrusions report (via aggregator summary), CrowdStrike "VAPOR PANDA" (secondary summary only), CSA ARTEX forks note, SOCRadar, threatdefence, threadlinqs, playciso, mallory, remio. Not opened: all of these. The summariser found no standalone CrowdStrike or Huntress primary.
2. "Amazon Cairn ... on their own": coverage of Amazon's 20 Nov account (hacked.com, securityaffairs, dig.watch, japancyberwatch, breachnews, que.com, magica, pivotnews, finexus). Not opened: all. Reported by summary: second-university spread inferred by Amazon, CVE number given by outlets.
3. "AI agent crawler traffic report November 2026": HUMAN Security State of Agentic Traffic (via ppc.land, opened), Cequence (agent traffic about 0.036% to 0.087% of requests, via summary), DataDome 52.7 billion requests July 2025 to June 2026, Cloudflare Radar via marketsplash, an HUMAN Cyber Week forecast (shattered.io), a dev.to single-site anecdote. Not opened: all but ppc.land.
4. "self-propagating AI agent worm in the wild observed 2026": only lab results (Anthropic/EPFL mind-virus prompt files Aug 2026; ClawWorm Mar 2026; Toronto local-model worm Jun 2026; arXiv 2606.03811 adaptive worms; arXiv 2605.06760 self-replication). The summary says no field case; CSA's ClawWorm note reads the lab work as early in-the-wild evidence, which is CSA's interpretation. Not opened: all.

## Pages opened

| URL | UTC read | Gate | Status | Page date | Reported by the page |
|---|---|---|---|---|---|
| https://www.anthropic.com/threat-intelligence | ~12:15 | allowed | 200 | newest 10 Sep 2026 | Six entries, newest September 2026 (WebFetch listing) |
| https://openai.com/global-affairs/disrupting-malicious-uses-of-ai/ | ~12:15 | allowed | 200 | 21 Feb 2025 | Single old article plus undated "Latest Advancements" list |
| https://www.microsoft.com/en-us/security/blog/2026/11/25/what-defenders-need-to-know-artex-agentic-ai-framework-threat-actors-abuse/ | ~12:15 | allowed | 200 | 25 Nov 2026 | Reported by Microsoft: it "observed" state-sponsored and financially motivated actors (Storm-0940, Storm-3358, Onyx Sleet, Pearl Sleet, Crystal Typhoon, Salt Typhoon) integrating ARTEX; one Storm-0940 campaign had more than 151,000 failed sign-ins, peaking at 2,900 a minute; one case went from GitHub secret search to Key Vault in five minutes (all via WebFetch summary). Reports ThreatBook's claim of ownership as a claim. The summary found no claim of credentials harvested to fund compute and no self-propagation; the actor sets the scope. Lists Huntress, Wiz, GTIG and CrowdStrike reports by title only |
| https://ppc.land/ai-agent-traffic-is-now-a-two-company-town-meta-and-openai/ | ~12:16 | allowed | 200 | after 9 Nov 2026 | Reported by PPC Land of HUMAN Security's October benchmark (published 9 Nov): Meta and OpenAI 89% of agent requests, Meta's Muse 59%, total agentic traffic up 157.5% on September; HUMAN's own detection, requests not sessions, vendor interest; PPC Land notes an internal inconsistency in the checkout growth figure |

## Five best leads

1. **Microsoft ARTEX post, 25 Nov** (https://www.microsoft.com/en-us/security/blog/2026/11/25/what-defenders-need-to-know-artex-agentic-ai-framework-threat-actors-abuse/). A second vendor with first-party telemetry for ARTEX in intrusions, but by the summary it describes human-scoped operations, not the credential-to-compute loop. Touches LH055 (add to the late-read log; bears on whether anyone but Amazon reports the loop). Opened via summariser, so a direct read of the full text is the next step.
2. **Wiz 23 Nov agentic cloud intrusions report** (primary not located; seen only via an aggregator summary). Wiz is said to state that its details do not establish agentic framework involvement in every incident or a single actor. Touches LH055; find the primary on wiz.io.
3. **HUMAN Security State of Agentic Traffic, Oct benchmark, published 9 Nov** (via https://ppc.land/ai-agent-traffic-is-now-a-two-company-town-meta-and-openai/; HUMAN's own page not opened). Vendor-reported concentration (two operators 89%) and 157.5% month growth, on requests. Matters for the cost-and-load reading in the AI cost investigation (LH044/LH045); who sends agent traffic is a load question, not a spread one.
4. **Cequence agent-traffic share (about 0.036% to 0.087% of requests) and bots posing as agents** (secondary only, primary not found). A counterweight to growth claims, and a possible impersonation angle. Touches ai-cost-and-spread; locate the primary.
5. **Agentic worms: lab versus wild** (arXiv 2606.03811, 2605.06760; Anthropic/EPFL Aug 2026; none opened). Every item found is a lab or proof-of-concept result; no field case surfaced. The status of this question stays "lab only, none seen"; the Toronto 20.4-host figure is a test-network result. Next: open the primary papers in a later sweep if a study needs them.

## Gaps and refusals

No refusals. OpenAI misuse index: loaded this time but shows no newer reports. Wiz, CrowdStrike, Cequence, HUMAN primaries not located or opened. Microsoft ARTEX content is via WebFetch summary only. No bodies saved. No emails seen.

## Withheld under research safety

None.
