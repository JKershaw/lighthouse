# Scout 5, Research, run 2026-11-27T1212Z

**In short.** The cs.CR past-week listing now shows 23 to 26 November and, on its second page of text, 20 November, so most of the earlier gap is covered; 19 November items (SoK on LLM vulnerability research, ROGUE-AI) were already in the 20 November sweep. New this run: a web agent built to evade bot defences (24 Nov), a benchmark where agents found 146 previously unknown Windows kernel flaws (24 Nov), and a cluster of agent-security papers. No paper on worms or self-propagating agents surfaced in the parts read. Everything is "reported by" the page, read through WebFetch's summariser.

Started 12:14Z, ended about 12:17Z, 27 November 2026 (`date -u`). Tools: robots_gate.py, WebFetch, WebSearch, grep of notes/horizon. No direct publication checks assigned to this scout.

## Direct publication checks

None assigned (plan: listing pages only).

## Standing-source results

arXiv cs.CR pastweek: headings Thu 26, Wed 25, Tue 24, Mon 23 and Fri 20 Nov read; Thu 19 Nov not visible and the Fri 20 Nov listing only first 10 of 50 shown; first 200000 characters of about 190000 read in two chunks (the summariser noted a 100000 cut; second chunk read via offset). cs.AI new (26 Nov): first 100000 of 751920 characters; nothing relevant beyond four partial fits. cs.NI new (26 Nov): internet measurement only (Geoflaw 2611.33365, RPKI forwarding 2603.29207), nothing on agent or crawler load. cs.SE and cs.CY listings, and venue news (IMC, USENIX Security, NDSS, PAM), not reached.

## Pages opened (all gated, all "allowed by robots.txt"; WebFetch summaries, status 200)

| URL | Read (UTC) | Page date | Reported by the page |
| --- | --- | --- | --- |
| arxiv.org/list/cs.CR/pastweek?show=250 (offset 0 and 100000) | ~12:15 | 26 Nov | Headings 20, 23 to 26 Nov; titles listed (no abstracts). |
| arxiv.org/list/cs.AI/new | ~12:15 | 26 Nov | "No papers on self-replication or propagation"; partial fits only. |
| arxiv.org/list/cs.NI/new | ~12:15 | 26 Nov | "No listing covers AI agent or crawler traffic". |
| arxiv.org/abs/2611.26601 | ~12:16 | 19 Nov | Autonomy scale for LLM vulnerability research; "the number of disclosed vulnerabilities more than doubled" in 2026; report-to-fix and disclosure-to-attack timing shows "no clear change". (Already in 20 Nov sweep.) |
| arxiv.org/abs/2611.26553 | ~12:16 | 19 Nov | ROGUE-AI: of 72 real-harm agent incidents, "62 had no attacker". (Already in 20 Nov sweep.) |
| arxiv.org/abs/2611.31962 | ~12:16 | 24 Nov | DarkAgent web agent: "89% page-access bypass rate" on a third-party stealth benchmark; timing between actions remains a defender signal. |
| arxiv.org/abs/2611.33486 | ~12:16 | 24 Nov | DeepBinary: across 12 Windows kernel binaries agents found "over 200 vulnerabilities", "146 previously unknown". |

## Searches (1, standard)

"LLM-found vulnerabilities CVE record attribution AI-discovered measurement arXiv November 2026": results were secondary (Stingrai CVE-credit attribution gap, Aug 2026; Google GTIG via Help Net Security, 1 Oct 2026; VulnCheck via TNW, 28 Jul 2026; HoF-Bench alphaxiv 2607.27030; Sonatype; CyberScoop). None opened; they are leads for P-0033 only. Snippet claims (not verified): CVE format has no AI-discovery field; VulnCheck 1,061 AI-attributed, 14 (1.3%) exploited.

## Five best leads

1. **2611.31962, DarkAgent, web agents evading bot defences** (24 Nov). https://arxiv.org/abs/2611.31962. Reports 89% bypass of bot checks on a benchmark. Bears on measuring agent load on shared sites: agent traffic that hides itself undercounts any crawler or agent census (LH044, rules-for-robots). New.
2. **2611.33486, DeepBinary** (24 Nov). https://arxiv.org/abs/2611.33486. Agents found 146 previously unknown flaws in closed-source kernel binaries. Capability evidence for model-found bugs; touches model-found-bugs investigation and P-0033. New.
3. **2611.26601, SoK on LLM vulnerability-research capability** (19 Nov). https://arxiv.org/abs/2611.26601. Disclosure counts doubled, attack timing unchanged on public records; direct comparison for LH036/LH038. Already seen 20 Nov, recorded again as still the best P-0033 anchor.
4. **2611.27567, Mjolnir, agents finding and reproducing firmware and RTL flaws** (23 Nov). https://arxiv.org/abs/2611.27567. Abstract not opened (title only). Capability lead. New.
5. **2611.27920, Autonomous Parameter Surgery** (23 Nov). https://arxiv.org/abs/2611.27920. Title only: LLMs autonomously implanting backdoors into other models. Nearest thing to agent-on-agent propagation in the listings; not opened. New.

Lower: 2611.30383 Bounded Autonomy (resource-exhaustion attacks on agents), 2611.30932 and 2611.30913 (agent skill supply chain), 2611.31010 Airlock (carried over).

## Gaps and refusals

No refusals. Thu 19 Nov cs.CR listing not visible; Fri 20 Nov only 10 of 50 entries; cs.AI and cs.SE/cs.CY mostly unread; no venue news checked; no worm or self-propagation paper found in what was read (absence in a partial read is not a negative). Nothing withheld.
