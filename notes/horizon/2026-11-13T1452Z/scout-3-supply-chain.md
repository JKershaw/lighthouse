# Scout 3, Software supply chain, run 2026-11-13T1452Z

Started 2026-11-13T14:56Z. Ended 2026-11-13T14:59Z on the container clock. Correction: the per-page read times in the table (15:00 to 15:11) were my estimates and run later than the container clock, which read 14:59 at close; treat them as 'within the 14:56 to 14:59 window'.

Every claim is reported by the page named, never an observation by Lighthouse. Each URL was gated with scripts/robots_gate.py (provider anthropic) in a separate command before any fetch. Searches are leads; results not opened are named below. No email addresses are recorded.

## Searches

1. "npm PyPI malicious packages compromised November 2026": no dated November item; May to August campaigns (Mini Shai-Hulud, Miasma and Hades, dYdX); one undated Namastex/CanisterWorm item (the search tool judged it uncertain).
2. "supply chain attack AI agent credentials worm npm package this week": SANDWORM_MODE, sckit (page header 25 September), keyv/cacheable (August); nothing from this week.
3. "wfx-loot campaign CI secret stealer repositories GitHub Actions compromised accounts": no "wfx-loot" hit; Gheist (Wiz, October), GhostAction (October wave), Megalodon (May), a New Stack piece on about 1,900 accounts and 30,000 repositories (not fetched, robots).
4. "StepSecurity ARTEX AI pentesting tool attackers adopted": ARTEX coverage (Check Point, CrowdStrike, GMO, eSecurityPlanet, Dark Reading, others), no StepSecurity page indexed.
5. "aikido wfx-loot ...": nothing on wfx-loot; Aikido codfish action (June), Resecurity LiteLLM/Trivy, OX Megalodon.
6. "Railway security incident November 2026 CI/CD": Railway's own reports (20-21 October incident, final report 10 November), BleepingComputer, aicybr, others.
7. "Check Point Research ARTEX autonomous AI agents attacks report" (domain-limited): Check Point's research page and blog.

## Pages opened

| # | URL | Read (UTC) | Status | Page date | Claim reported | New? |
|---|---|---|---|---|---|---|
| 1 | https://socket.dev/blog | 15:00 | fetched | undated listing | Listing now leads with "Cyberattacks Are Skyrocketing in Japan as Researchers Trace AI-Assisted Intrusions"; also "Socket Threat Intel Now Shows Which Malware Campaigns Were Blocked or Detected". No dates shown, so recency cannot be told. | seen (page); new titles |
| 2 | https://www.stepsecurity.io/blog | 15:00 | fetched | 2026-11-05 to 11-12 | Newest: "WFX Phantom: The GitHub Actions Secret Stealer" (12 Nov), "ARTEX: Attackers Adopted This AI Pentesting Tool in Three Months" (12 Nov), "GitHub Package Firewall vs. StepSecurity Secure Registry" (10 Nov; says GitHub's covers only npm). | seen (page); new posts |
| 3 | https://www.aikido.dev/blog | 15:00 | fetched | 2026-11-13 | "wfx-loot campaign pushes CI secret stealer to tens of thousands of repositories" (12 Nov): "Compromised accounts are spreading a CI secret-stealing payload"; also an Apache HTTP Server RCE (13 Nov). | seen (page); new posts |
| 4 | https://blog.pypi.org/ | 15:00 | fetched | latest 2026-11-06 | No new PyPI post since "redesigned project pages with clearer security signals are now live" (6 Nov); no incident post. | seen |
| 5 | https://github.blog/changelog/label/supply-chain-security/ | 15:00 | fetched | latest 2026-11-10 | One new entry: 10 Nov "Dependabot will pause alerts for inactive repositories" (headline only). | seen (page); one new entry |
| 6 | https://openssf.org/blog/ | 15:00 | fetched | 2026-11-09 | Nothing on malicious packages since 9 Nov; Zarf 1.0 and new AI security resources (headlines only). | seen |
| 7 | https://huggingface.co/blog | 15:00 | fetched | to 2026-11-13 | No post on malware or scanning among titles to 13 Nov. | seen (page) |
| 8 | https://ossf.github.io/malicious-packages/stats | 15:01 | fetched | "last updated 2026-11-13T00:36:09+00:00" | Chart page; the fetch returned no totals (data in all.json and all.csv, not downloaded). | seen |
| 9 | https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer | 15:04 | fetched | 2026-11-12 (figures at 07:40 UTC 12 Nov) | Campaign from 10 Nov: "a coordinated botnet of compromised GitHub accounts"; more than 63,000 probe pull requests, over 21,000 commits titled "ci: refresh build cache"; each injected run live "a minute or two before the revert"; the stealer targets AI provider and coding-agent API keys; the report does not say the attacker used AI. A Telegram exfiltration channel appears from 12 Nov 01:10 UTC. | new |
| 10 | https://thehackernews.com/2026/10/gheist-uses-stolen-github-tokens-to.html | 15:05 | fetched | 2026-10-26 | Wiz's Gheist: more than 13,500 planted branches from more than 850 compromised accounts since 15 Sep; secrets leave "through GitHub itself"; GitHub's 28 July safeguard holds suspicious runs on public repositories only; no AI element. Does not mention wfx-loot. | new |
| 11 | https://www.esecurityplanet.com/threats/news-artex-ai-agents-credential-theft/ | 15:06 | fetched | 2026-11-09 (Check Point report 5 Nov) | Operators let agents "handle much of the work, with little further human involvement"; more than 300 iOS signing certificates; 13 marketplaces; 292 crypto domains; some agent-reported cashouts "were hallucinations". | new |
| 12 | https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/ | 15:09 | fetched | 2026-11-05 | 2,557 systems hosted ARTEX panels (1,608 live); "Threat actors barely interacted with their agent fleets"; in one campaign an unauthenticated API gave write access to a bucket hosting iOS app pages, restored by the owner; "not one cent moved to the attackers pockets"; ten instances exposed their databases. | new |
| 13 | https://blog.railway.com/p/incident-report-october-security-incident | 15:10 | fetched | updated 2026-11-10 | Exploit 07:28 UTC 20 Oct, eviction 09:24 UTC 21 Oct (about 26 hours); build-isolation escape then an OIDC misconfiguration; "the attacker was specifically targeting AI provider credentials"; at most 1.85% of workspaces (about 100,000) could have had variables decrypted; about $740,000 unauthorised spend; "no indication" customer repositories were taken. | new |
| 14 | https://www.stepsecurity.io/blog/railway-security-incident-cicd-runtime-security | 15:11 | fetched | 2026-11-10 | A compromised build job's permissions "can become the attacker's access"; the post treats the route as a build credential and a trust-configuration error, not a stolen CI token. | new |
| 15 | https://www.stepsecurity.io/blog/artex-attackers-adopted-this-ai-pentesting-tool-in-three-months | 15:05 | HTTP 404 | n/a | Guessed path; observation only. | new |
| 16 | https://www.aikido.dev/blog/wfx-loot-campaign-pushes-ci-secret-stealer-to-tens-of-thousands-of-repositories | 15:05 | HTTP 404 | n/a | Guessed path; observation only. | new |
| 17 | https://www.stepsecurity.io/blog/railway-security-incident | 15:05 | HTTP 404 | n/a | Guessed path; observation only. | new |

17 requests: 14 returned content, 3 returned HTTP 404. Listing pages gave headlines; I did not open GitHub's Nov 10 entry, Socket's Japan post or the Aikido wfx-loot post (path not found, URL not known).

## Refusals and walls

- Not fetched (robots.txt, gate said allowed false): https://thenewstack.io/hackers-hijacked-1900-github-accounts-then-they-went-after-30000-repos/ ; https://www.darkreading.com/cyberattacks-data-breaches/artex-ai-pen-test-tool-hackers-weapon . Snippets only, as leads.
- Walls (403, challenge, login, rate limit, paywall): none met. Three 404s as above.
- Search results seen, not opened: GMO and CrowdStrike ARTEX items, SOCRadar, Astra, Wiz and GhostAction write-ups, OX Megalodon, SafeDep prt-scan, Resecurity LiteLLM, BleepingComputer Railway piece, Namastex/CanisterWorm items.
- Not found: no November PyPI, npm or crates.io registry-level wave in what I opened; Hugging Face blog silent on malware. One scout, one day.
- PyPI JSON API not used.

## Five best leads

1. **WFX Phantom / wfx-loot, from 10 November (StepSecurity and Aikido, both 12 Nov; https://www.stepsecurity.io/blog/wfx-phantom-the-github-actions-secret-stealer).** A scripted, token-pool operation: more than 63,000 probe pull requests in about two days, about 90% still open, injected runs live for minutes, exfiltration moved to Telegram within 30 hours. It targets AI provider and agent keys. Why: it is the fastest and largest automated spread of stolen credentials on shared infrastructure now visible, and its public footprint (open pull requests, commit messages, run-number gaps) will decay as repositories clean up. Software-updates investigation (CI trust) and AI-activity cost; no AI use by the attacker is reported.
2. **ARTEX operator fleets (Check Point 5 Nov, https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/; StepSecurity 12 Nov).** Agents run with "barely" any operator input, 2,557 panels seen, 400,000 agent messages, yet no money moved and successes were hallucinated. Why: a direct reported case of agent-driven attack activity and its real yield, including agents writing to a bucket that serves app downloads; bears on whether such activity sustains itself (it did not pay here) and on cost to shared infrastructure.
3. **Railway incident final report (10 Nov, https://blog.railway.com/p/incident-report-october-security-incident).** Build-isolation escape, then OIDC trust, then decryption of environment variables; "specifically targeting AI provider credentials"; about $740,000 unauthorised spend. Why: AI credentials are now the named prize, so the cost of AI activity falls on platforms and their customers; it also shows build systems as a path to secrets.
4. **GitHub's partial defences (Gheist article 26 Oct; changelog 20 Oct and 10 Nov; Socket 2 Nov notice that pull_request_target is blocked by default from 2 December, seen earlier).** The 28 July run-hold covers public repositories only; the firewall covers npm only. Why: the gap between what the platform holds and what campaigns use is where updates, and the dates 2 December and later, can be tested; software-updates investigation.
5. **Registry-side quiet versus CI-side noise (PyPI, OpenSSF, Hugging Face pages all silent on new malware since 6 to 9 Nov; OpenSSF malicious-packages stats updated 13 Nov 00:36 UTC).** Why: the registries may be steady while attackers move to repositories and CI; a daily read of all.csv would give a dated count of that shift. A lead, not a finding.

## Urgent

WFX Phantom: pull requests, commit messages and surviving run logs are live evidence now, and accounts and branches are being removed (Gheist's accounts were two-thirds gone after reporting). Window: days, perhaps a week. Counts need a read within about 48 hours, using only public routes and nothing from the attackers' infrastructure.
