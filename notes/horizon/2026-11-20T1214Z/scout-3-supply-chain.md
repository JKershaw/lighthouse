# Scout 3, Software supply chain, run 2026-11-20T1214Z

**In short.** The StepSecurity feed shows one new relevant item since 18 November: an update (20 Nov) to its OPTIMJACK post, with a revised timeline and a lower loss estimate. Nothing new on agent-framework, WPPConnect or bee-js turned up on the vendor blogs or registry notices read. The most useful new find is an Aikido roundup (19 Nov) of AI-related incidents, a secondary source for the charter's question. Everything below is reported by the page named, never Lighthouse's observation. The clock ran fast relative to the work; read times are approximate.

Start 12:16Z, end about 12:18Z (`date -u`). Tools: scripts/lh_feeds.py, scripts/robots_gate.py (provider anthropic, run for every URL before fetching, all allowed), WebFetch (pages summarised by a small model, so quotations are the summariser's relay), WebSearch. No keys read; nothing saved except this file. No download counts read for agent-framework, bee-js, WPPConnect or litellm.

## Direct publication checks

| Endpoint | UTC read | Previous successful check | Outcome | Entries |
| --- | --- | --- | --- | --- |
| https://www.stepsecurity.io/blog/rss.xml (lh_feeds, --since 2026-11-18) | 12:16Z | 18 Nov 13:03Z (index) | new entries | Feed status ok, oldest 2026-04-09, newest 2026-11-20, no undated or skipped entries. Two entries after the 13:03 check: 20 Nov 08:47 "OPTIMJACK: Optimizely-Hosted Scripts Loaded a Crypto Clipper and Card Skimmer on 178 Organizations" (https://www.stepsecurity.io/blog/optimjack-optimizely-hosted-scripts-crypto-clipper-card-skimmer; the page itself says published 17 Nov, updated 20 Nov 08:19Z, so the feed date is the update); 20 Nov 08:33 "nginx2root (CVE-2026-123007): HTTP/2 Flaw Lets Attackers Run Code on Unpatched nginx Servers" (not supply chain; for scout 2). One more, 18 Nov 16:24 "StepSecurity's $20 million Series A", is a company post, not relevant. The 18 Nov entries seen at the last check are not repeated. |

Coverage: the feed reaches back to April, so the whole interval since 18 Nov 13:03Z is covered. No gap.

## Searches (2)

1. "compromised npm PyPI package credential stealer AI API keys 19 November 2026": no item dated 19 or 20 November. Returned May to July 2026 items (Mini Shai-Hulud, LiteLLM, Jscrambler, TeamPCP attribution), old and mostly known.
2. "wfx-loot OR WFX Phantom GitHub accounts CI secret stealer update": ten-plus write-ups, mostly 12 to 13 Nov. The search summary says the stealer takes "AI provider keys" and, per Rescana, leaves cloud backdoors (AWS keys, trust policies, Entra federated credentials named wfx-ci-*) that "outlast normal rotation". Counts vary by source (Aikido 4,837 accounts, 61,764 repositories probed, at least 1,806 where the stealer ran; Techaeris at least 1,835). Not opened.

## Pages opened

| # | URL | Page date | UTC read | Status | New? | Claim reported by the page |
|---|---|---|---|---|---|---|
| 1 | https://www.stepsecurity.io/blog/optimjack-optimizely-hosted-scripts-crypto-clipper-card-skimmer | 17 Nov, updated 20 Nov 08:19Z | 12:16Z | fetched | updated since last seen | Optimizely's 18 Nov statement says the attacker "impersonated users on targeted accounts" (earlier: account signup flow), limited to Web Experimentation, under 5% of customers; loss estimate lowered from $7,040 to about $2,300; exposure about 16 hours for most sites; payload domain on registry hold; first injection 16 Nov 04:21Z, all clean 23:11Z; "does not mention any AI-related element". |
| 2 | https://socket.dev/blog | undated listing | 12:16Z | fetched | seen; new titles | Newest first: "Hardening GitHub Actions Against Insider Threats", "MITRE Acknowledges Inaccurate Publication Timestamps in 87% of Its Recent CVE Records", then the Optimizely and agent-framework posts already known. No new compromised-release post above agent-framework. Also lists (seen before or old): bee-js, "Shai-Hulud Descendant Surfaces in Malicious Ruby Gem" (in 10 and 17 Nov files), Cursor/Claude Code extension (7 Nov file). |
| 3 | https://www.aikido.dev/blog | newest 2026-11-19 | 12:16Z | fetched | seen; new titles | Newest: 19 Nov "AI incidents of 2026: Rogue agents, stolen keys, and other familiar stories"; 19 Nov Ruby2Shell (CVE-2026-132825, scout 2 material); 18 Nov PHP security release; none new on compromised packages after agent-framework (17 Nov) and wfx-loot (12 Nov). |
| 4 | https://www.aikido.dev/blog/ai-incidents-root-causes-patterns | 2026-11-19 | 12:16Z | fetched | New | Roundup of 2026 incidents with root causes. Reports Cline (Feb): an AI issue-triage bot "manipulated through GitHub issue titles" contributing to an unauthorised npm release; Hugging Face (July): agents "helped ... spread to code running on 41 production servers" via exposed tokens; September card-skimming "AI agents ... at least 27 retailers"; Railway (Oct) 1,852 users' tokens; ARTEX against ConnectWise tenants. Secondary; each claim is Aikido's relay and needs its own primary. |
| 5 | https://socket.dev/blog/github-to-block-pull-request-target | 2026-11-05, modified 11-18 | 12:16Z | fetched | New | GitHub will block `pull_request_target` workflows in public repositories by default from 2 Dec 2026 (moved from 2 Nov), brownouts 9 and 16 Nov 16:00 to 18:00 UTC; cites "pwn requests" in Nx, PostHog, TanStack incidents. |
| 6 | https://blog.pypi.org/ | latest 2026-11-18 | 12:16Z | fetched | new post | 18 Nov "Stricter checks for uploaded distributions on PyPI" (rejects some non-conformant distributions); no post on malware, quarantine or agent-framework. |
| 7 | https://github.blog/changelog/label/supply-chain-security/ | latest 2026-11-16 | 12:16Z | fetched | seen | No entry after 16 Nov. |
| 8 | https://blog.rubygems.org/ | latest 2026-11-19 | 12:16Z | fetched | new post | 19 Nov "Gemstash 2.9.0 security release, and the end of Gemstash" (title only read; contents not opened); no malware or yank post. |
| 9 | https://rustsec.org/advisories/ | newest 2026-11-19 | 12:16Z | fetched (first 100k of 298k characters) | seen | Newest ten are heapless and wasmtime soundness advisories, none malicious; malicious-code removals further down are 10 Nov (RUSTSEC-2026-0464 to 0472) and 11 Nov (0483), already known. |

## Refusals and walls

None. rustsec.org's robots.txt answered 404 this time (503 on 18 Nov), so the gate allowed it. Socket, Aikido, StepSecurity, PyPI, RubyGems, GitHub, Hugging Face (gate only), OpenSSF and Snyk (gate only) all allowed. Hugging Face, OpenSSF, Snyk and the GitHub npm changelog were gated but not opened, so those are unchecked this sweep.

## Search results not opened

The wfx-loot write-ups from corgea.com, ox.security, endorlabs.com, semgrep.dev, bleepingcomputer.com, rescana.com, safeguard.sh and others (none in earlier sweep files by URL; the CSA research note was seen before); May to July Mini Shai-Hulud, LiteLLM, Jscrambler and dydx items; Socket posts on ESLint, pnpm, Composer cooldowns, OpenCode (not relevant or not supply-chain compromises).

## Quiet, stated as quiet

No new compromised npm, PyPI, RubyGems or crates release was found since 18 November on the listings read. One scout reading listings and one search each is not a registry count.

## Five best leads

1. **wfx-loot / WFX Phantom persistence and AI keys (search result; primary Aikido https://www.aikido.dev/blog/compromised-github-accounts-push-ci-secret-stealer-to-tens-of-thousands-of-repositories, StepSecurity https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer).** Reported: hijacked accounts probed tens of thousands of repositories, the stealer takes AI provider keys and leaves cloud backdoors that survive rotation. Charter: credential theft at scale that feeds on automation and could sustain itself, though no AI authorship is reported. Not read in full this sweep. Lost if nobody looks: malicious branches and workflow files in repositories get cleaned over days; the counts are still being revised.
2. **agent-framework follow-up: nothing new found.** Aikido's roundup does not mention it. Charter: the only known 2026 stealer aimed at agent packages in this window. Next: leave to LH056's reads; a Microsoft statement may still come. Lost if nobody looks: quarantine state and maintainer list on the live PyPI page.
3. **Aikido's "AI incidents of 2026" roundup (https://www.aikido.dev/blog/ai-incidents-root-causes-patterns).** A single secondary list that includes an AI triage bot enabling an unauthorised npm release (Cline, Feb) and Hugging Face agents spreading to 41 production servers (July). Charter: the closest to "AI activity spreading through shared infrastructure"; each case needs its primary read before use. Fixed publication, so not urgent. Next: trace the Hugging Face and Cline primaries.
4. **GitHub blocking `pull_request_target` by default from 2 December (https://socket.dev/blog/github-to-block-pull-request-target).** A platform change to the route used in several secret-stealing campaigns. Charter: a shared-infrastructure defence that will alter how CI-secret theft spreads; a before and after for wfx-style campaigns. Dated, so a planned event, not expiring; GitHub's own changelog primary not opened.
5. **OPTIMJACK revisions (StepSecurity update 20 Nov).** Vendor says attacker impersonated users, under 5% of customers; loss estimate down to about $2,300. No AI element reported. Low charter relevance; a note on the existing lead is enough.

## Urgent

None new. The standing window is wfx-loot residue (malicious branches, workflow files) and agent-framework's live package page, both reported to change within days.
