# Scout 3, Software supply chain, run 2026-11-07T0853Z

Started 2026-11-07T08:54Z. Ended 2026-11-07T08:58Z (the container clock; read times below are given to the nearest minute and all fell inside that window).

A grep of the repository's Markdown (excluding harbour/.session) for "shai-hulud", "chaindrop", "1.107", "pull_request_target" and "slopsquat" found no hits, so none of these leads is already in Lighthouse's notes.

## Searches

Run in order. Results are as returned; I opened only those named under "Sources read".

1. "npm worm self-propagating supply chain attack November 2026": leaddev "another npm attack..."; Gurucul "ChainDrop Supply Chain Compromise" (community.gurucul.com); CSA "CanisterSprawl: The Self-Propagating npm Supply Chain Worm"; Unit 42 chaindrop-npm-worm-analysis; VerSprite Shai-Hulud 500+; offseq radar Shai Hulud 26,000+ repos; Aviatrix ChainDrop; others. No November item.
2. "PyPI malware campaign October 2026": SecurityWeek "Malware upload attack hits PyPI"; offseq "Hades PyPI Attack: 19 Packages"; "Mini Shai-Hulud, Miasma, and Hades Worms Target Bioinformatics and MCP Developers"; winbuzzer "PyPI Malware Wave Exposes Weak AI Malware Scanner Boundary" (2026/06/21); hackingpassion xinference TeamPCP. No October item.
3. "slopsquatting hallucinated package names AI agents 2026": Endor Labs; CSA note 20260419; Xygeni; DZone; trojan-killer.net (updated 29 Oct 2026); TrendAI.
4. "supply chain attack npm PyPI compromised packages this week Socket Aikido StepSecurity" (extended): cybernews; SecurityWeek "Over 100 NPM, PyPI Packages Hit"; BleepingComputer ChainDrop; THN dYdX (Feb); SecurityWeek "Over 400 NPM Packages Infected in ChainDrop"; Security Boulevard "The Streak Continues" (July); StepSecurity Mini Shai-Hulud TanStack; THN MemTensor (Sep).
5. "Hugging Face malicious models 2026 supply chain": CSA "Model Hub Typosquatting" (May); TechRepublic Transformers RCE; securitricks "Poisoning the well: Hugging Face and OpenClaw"; pulse.bot hundreds of malicious models; others.
6. "GitHub Actions compromised tag poisoned 2026 Dependabot Renovate spread": SoftwareSeni tj-actions; devtake Trivy; Xygeni xygeni-action incident; Rankiteo May 2026.
7. "Shai-Hulud new wave October 2026 npm PyPI Claude Code hook persistence": vpncentral; cybersecurity-help.cz; lilting.ch "@antv ... Claude Code and VS Code persistence"; hivesecurity.gitlab.io; TechRadar "over 600 compromised npm packages"; Security Boulevard "campaign evolution ... AI scanner evasion".
8. "crates.io OR RubyGems malicious crates gems phishing security incident 2026": THN "RubyGems suspends new signups" (May 2026); Mend.io "Inside the RubyGems supply chain attack"; Rust blog crates.io phishing (Sept 2025); Socket crates.io phishing.
9. "MCP server malicious package registry npm PyPI agent skills poisoned October 2026": nesbitt.io (8 Apr 2026); dev.to "We scanned 448 MCP servers"; SOCRadar; policylayer.
10. "LiteLLM 1.107.0 compromised infostealer RAT PyPI quarantined": SOCRadar; Datadog Security Labs; Cloudsmith; Daily Security Review; ayinedjimi; newly.app.
11. "GitHub pull_request_target blocked by default December 2 Actions change": github.blog changelog 2026-11-02; aicybr.com audit guide; dev.classmethod.jp; the 2025-11-07 changelog.
12. "malicious Ruby gem Shai-Hulud steals credentials targets AI tools Socket": Socket SANDWORM_MODE; Techzine Tensorlake; Mishcon; BleepingComputer 60 malicious gems. The Socket headline about a Ruby gem linked to Shai-Hulud was not confirmed by this search.
13. "Cursor removed malicious Claude Code extension marketplace Open VSX": Socket blog; BleepingComputer; it-connect.fr; Openwall oss-security 2026/10/30; kucoin flash.
14. "Hugging Face malicious model OR dataset October 2026 takedown": CSA "Takedowns That Don't Hold" (31 Oct); Daily Security Review "Hugging Face Mining Malware Returns"; dev.to "Hugging Face pulled dozens of backdoored models"; Dark Reading; BleepingComputer.

## Sources read

All opened by WebFetch on 2026-11-07, status "fetched" (no HTTP error reported), times ~08:55 to 08:58Z.

| # | URL | Page date | Claim reported by the page |
|---|---|---|---|
| 1 | https://blog.pypi.org/ | latest post 2026-11-06 | PyPI's blog lists "Redesigned project pages with clearer security signals" (6 Nov), email reputation checks (16 Oct) and, on 22 Jul, a rule that "releases reject new files after 14 days" to protect releases "if publishing tokens or workflows are compromised". |
| 2 | https://www.bleepingcomputer.com/news/security/massive-chaindrop-npm-supply-chain-attack-infects-hundreds-of-packages/ | 2026-08-04 | ChainDrop, a "Shai-Hulud-based worm", hit "more than 1,300 packages" (Aikido: at least 868), pushed through a maintainer's GitHub account and published by legitimate Actions workflows so releases "carried valid provenance". |
| 3 | https://thehackernews.com/2026/09/compromised-memtensor-packages-deliver.html | 2026-09-23 | Hijacked MemTensor npm and PyPI packages (an OpenClaw agent memory plugin, MemoryOS) ran a Go credential stealer that sees "the user's prompt text"; per SafeDep the attacker got tokens via commits that made GitHub Actions release pipelines hand them over, and the implant "can spread like a worm". |
| 4 | https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem | 2026-05-11 | TanStack packages carried "valid SLSA Build Level 3 provenance attestations" despite being malicious; the payload writes a `SessionStart` hook into `.claude/settings.json` and dead-drop commits are authored as `claude@users.noreply.github.com`. (Background, six months old.) |
| 5 | https://www.securityweek.com/over-100-npm-pypi-packages-hit-in-new-shai-hulud-supply-chain-attacks/ | 2026-06-09 | Miasma (npm) and Hades (PyPI, via a `*-setup.pth` file that fetches Bun) gave "471 malicious artifacts"; stolen data goes to "new GitHub repositories". (Background.) |
| 6 | https://socket.dev/blog | undated listing, shows current items | Lists a malicious Ruby gem linked to Shai-Hulud that "targets AI tools", GitHub's planned `pull_request_target` block, Composer dependency cooldowns, and a Cursor-removed Claude Code extension. I did not open the gem item. |
| 7 | https://github.blog/changelog/label/supply-chain-security/ | entries to 2026-11-03 | GitHub's recent entries include "Unvalidated npm trusted publishing configurations will now expire" (2 Oct) and "npm staged publishing can now be used to create new packages" (2 Oct). |
| 8 | https://www.aikido.dev/blog | entries 2026-10-21 to 2026-11-05 | Aikido lists "LiteLLM compromised again" (21 Oct), "Even gem list can run someone else's code" (5 Nov) and a leaked key that "still enabled a later LiteLLM breach". |
| 9 | https://cloudsmith.com/blog/litellm-1-107-0-compromised-on-pypi | 2026-10-21 | LiteLLM 1.107.0 was uploaded at 11:39 UTC using "stolen GitHub CLI OAuth tokens"; it persisted through `cook.pth` and `sitecustomize.py`, and stolen AWS credentials were tested against LLM models "within hours". |
| 10 | https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2 | 2026-11-02 | GitHub will block `pull_request_target` by default in public repositories from 2 December, with brownouts on 9 and 16 November, 16:00 to 18:00 UTC. |
| 11 | https://www.techzine.eu/news/security/144866/shai-hulud-worm-burrows-into-ai-platform-tensorlakes-npm-sdk/ | 2026-10-09 | Tensorlake's npm SDK 0.5.144 carried a Shai-Hulud variant found on 8 Oct "within 11 minutes"; it may wipe a victim's home directory if a stolen token is revoked. |
| 12 | https://github.com/ossf/malicious-packages | undated | OpenSSF's repository of malicious-package reports in OSV format shows "15,256 commits"; the report-count badge links to ossf.github.io/malicious-packages/stats, which I did not open. |
| 13 | https://labs.cloudsecurityalliance.org/research/csa-research-note-model-hub-reupload-agent-lures-20261031-cs/ | 2026-10-31 | Citing Pluto Security, a Hugging Face miner and reverse-shell campaign of "31 malicious repositories across seven accounts" had wave 2 "still live eight days after they were reported", with 29,090 wave 2 downloads; it also cites agent lures (SolanaCry, AGENTS.md, AgentBaiting with "about 7,600 malicious GitHub repositories"). |
| 14 | https://socket.dev/blog/claude-code-extension-compromise | ~2026-10-30 (no date shown) | Cursor says a tampered Claude Code extension build was on its marketplace on 29 October for up to 5,000 users; Socket "found no Open VSX or npm publication" of the build and notes the original report was "substantially revised". |

Search results seen but not opened: CSA slopsquatting note (19 Apr 2026), Endor Labs and Xygeni slopsquatting pieces, trojan-killer.net (updated 29 Oct), Unit 42 ChainDrop analysis, CSA CanisterSprawl, Datadog and SOCRadar LiteLLM pieces, GitHub 2025 pull_request_target changelog, Mend.io and THN on RubyGems (May 2026), Pluto Security's own report, BleepingComputer on the Hugging Face miner and the Cursor extension, Openwall oss-security 2026/10/30, lilting.ch on @antv persistence.

## Best leads

### 1. GitHub's `pull_request_target` block: 9 November brownout, 2 December enforcement

- Reported: GitHub's changelog of 2 November (https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2) says public repositories will block the trigger by default, with brownouts on 9 and 16 November (16:00 to 18:00 UTC) and permanent enforcement on 2 December. StepSecurity (11 May) reported that a "Pwn Request" via this trigger started the TanStack worm.
- Why it matters: this trigger is the entry point reported for worms that publish through stolen tokens, so it is a one-off change to a path along which such residue propagates, and it comes with a natural before-and-after.
- Time-sensitive: yes, the first brownout is two days away and the counterfactual (how many public workflows still use the trigger) is lost once it is enforced and workflows are rewritten.
- Measurable: from GH Archive, the share of public repositories with workflow files using `pull_request_target`, and failed or changed runs on 9 and 16 November and after 2 December. Also the count of npm and PyPI publishes by workflows using it, from registry metadata.
- Cost: small to one study.
- Confidence real and new: high that the change is real (primary source); new to Lighthouse. Whether the data show an effect is unknown.

### 2. Worm-style campaigns with AI-agent persistence and AI-agent targets (Tensorlake, MemTensor, Shai-Hulud lineage)

- Reported: Techzine (9 Oct) on a Shai-Hulud variant in Tensorlake's SDK, found in 11 minutes; THN (23 Sep) on MemTensor, an agent memory plugin whose implant sees prompt text and "can spread like a worm"; StepSecurity (11 May) on the lineage writing `SessionStart` hooks into `.claude/settings.json` and spoofing a Claude bot as commit author; BleepingComputer (4 Aug) on ChainDrop with valid provenance. Counts differ by vendor (868 to 1,300 packages for ChainDrop).
- Why it matters: this is the clearest case of self-propagating publish-through-stolen-tokens activity, and its residue (hooks, dead-drop GitHub repositories, spoofed commits) is in public data; the August to October cadence suggests more waves.
- Time-sensitive: moderately; dead-drop repositories and malicious versions are deleted within hours or days.
- Measurable: GitHub search and GH Archive for repositories created by the campaign's reported naming patterns and `claude@users.noreply.github.com` commits; OSV and OpenSSF malicious-packages reports by date and ecosystem, giving a wave timeline; the interval from first malicious publish to removal.
- Cost: one study (a timeline and persistence-residue census); large if it tries to measure spread between maintainers.
- Confidence: high that it is real; new to Lighthouse (no existing note mentions it). Claims about AI authorship of the malware are not made by these sources.

### 3. LiteLLM compromised twice in 2026 (21 October), with a leaked-key chain

- Reported: Cloudsmith (21 Oct): 1.107.0 uploaded 11:39 UTC via "stolen GitHub CLI OAuth tokens"; Aikido (5 Nov) says a key removed from a repository "still enabled a later LiteLLM breach"; the earlier compromise was 1.82.7 and 1.82.8 on 24 March (reported by search summaries, not opened). Per a search summary, PyPI quarantined the release by about 13:20 UTC; Cloudsmith says stolen AWS credentials were tested against LLM models within hours.
- Why it matters: LiteLLM sits in AI agent stacks and holds provider keys; PyPI-side, the exposure is a short window of installs by automated systems. It also touches Lighthouse's existing watch on how Python releases spread via pins, lockfiles, containers and CI.
- Time-sensitive: mild; PyPI's BigQuery and ClickPy download counts by hour remain, but mirrors and image caches do not.
- Measurable: ClickPy or pypistats downloads for litellm in the 2 hours around 11:39 UTC on 21 October against the same hour on neighbouring days; which versions pinned lockfiles and Docker images in public repositories resolved to 1.107.0 (GitHub code search is not archive-complete); both compromises as natural experiments for the existing release-spread work.
- Cost: small to one study, reusing the existing Python release-spread instruments.
- Confidence: high on the event, medium on exposure; fits an active investigation.

### 4. Model hubs and agent lures: takedowns that do not hold (Hugging Face, 31 October)

- Reported: CSA research note of 31 October, citing Pluto Security and BleepingComputer: 31 malicious repositories in two waves; wave 2 live eight days after report, one repository holding 97.7% of 29,090 downloads; separate "agent lures" (a README-only repository ranked first by agent search, an `AGENTS.md` in Downloads triggering code execution in lab trials, about 7,600 malicious GitHub repositories, over 800 posing as skills or MCP servers). Secondary reporting; I did not open Pluto's own report.
- Why it matters: these are residue designed to be found and executed by AI agents without a person choosing it, which is close to the charter's propagation layer; the re-upload pattern shows that removal does not end it.
- Time-sensitive: yes; repositories were disabled or live at different times and counts moved from 7,354 to 28,412 downloads in days.
- Measurable: Hugging Face's public API (download counts, disabled status, account creation) for the named repositories and accounts, polled daily for two weeks; time from report to disable; whether new accounts reappear. Agent-lure repositories can be tracked by GitHub API star and existence checks.
- Cost: one study.
- Confidence: medium; the figures are from a note that relays others and counts differ between sources (19 against 31 repositories).

### 5. AI-tool distribution channels as targets: Cursor marketplace and Claude Code extension (29 October)

- Reported: Socket (about 30 Oct): Cursor says a tampered Claude Code extension was on its marketplace on 29 October for up to 5,000 users; the build added an SSH authorised key and reverse tunnel per an original report that has been "substantially revised". Socket found no Open VSX or npm trace and says provenance is "not established". Socket also lists a Shai-Hulud-linked Ruby gem that targets AI tools (headline only).
- Why it matters: it shows the developer machine, with its agent configuration and credentials, as a pivot, and the same credentials feed the worms in leads 2 and 3. The attack path (how the build entered) is not public.
- Time-sensitive: low to medium; facts are still being revised.
- Measurable: little from public data alone; extension version histories on Open VSX (public API) and the Visual Studio Marketplace could show whether tampered versions appear elsewhere. Better held as a watch than a study.
- Cost: small for a watch; one study if it grows.
- Confidence: medium that it is real, low that it adds measurable value yet.

## Notes

- Nothing dated November 2026 was found on npm, PyPI, crates.io or RubyGems incidents; the freshest items are 21 October (LiteLLM), 29 October (Cursor, Hugging Face campaign) and 6 November (PyPI project pages). Many search hits were aggregators (offseq, pulse.bot, securitricks) and I did not open them.
- A search summary reported the RubyGems signup suspension (May 2026) and a Dependabot or Renovate angle: none of the sources I saw documents automated dependency updates spreading a compromise; they appear as remediation. The plan's "spreads through automated dependency updates" thread is therefore unsupported so far. One check worth making: whether Dependabot PRs proposed LiteLLM 1.107.0 within the 11:39 to 13:23 UTC window.
- GitHub's changelog also lists npm "staged publishing" and trusted-publishing expiry (2 Oct) and PyPI's 14-day upload rule (22 Jul): defences that change how worms can publish, useful as dated breakpoints for any wave timeline.
- Slopsquatting: all sources seen are 2025 to mid-2026 (react-codeshift, 205,474 hallucinated names); I found nothing dated in the last few weeks that was new beyond the CSA note, so it is not ranked.
- OpenSSF's malicious-packages stats page was not opened; it is the obvious dataset for lead 2.
- github.com issue and release pages were not tried given the CLAUDE.md warning about 403s. socket.dev/blog showed no dates, so its items are dated only through other pages.
- Hugging Face's own notices and Cursor's own security notice were not opened.
