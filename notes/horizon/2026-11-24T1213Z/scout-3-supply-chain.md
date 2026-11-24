# Scout 3, Software supply chain, run 2026-11-24T1213Z

**In short.** The StepSecurity feed shows no new supply-chain item since 20 November (one nginx flaw post on 24 November, a funding post, and the OPTIMJACK post's re-dated entry). No new compromised npm, PyPI, RubyGems or crates release turned up on the registry and vendor listings read. The one new find is a Hugging Face account-takeover demonstration on the Kokoro model (Anaconda, 20 November), reported as a researchers' test with nothing shipped. Everything below is reported by the page named, never Lighthouse's observation. Clock times are from `date -u` and the run was short (about 12:15Z to 12:17Z by that clock).

Start 12:15Z, end 12:17Z (`date -u`). Tools: scripts/lh_feeds.py, scripts/robots_gate.py (provider anthropic, run before every fetch), WebFetch (a summariser, so quotations are relayed), WebSearch. No keys read; nothing saved except this file. No download counts read for any package.

## Direct publication checks

| Endpoint | UTC read | Interval covered | Outcome | Entries |
| --- | --- | --- | --- | --- |
| https://www.stepsecurity.io/blog/rss.xml (lh_feeds, --since 2026-11-20) | 12:15Z | 20 Nov to 24 Nov; feed oldest 2026-04-09, newest 2026-11-24, no skipped or undated entries | new entries, none relevant | 24 Nov 10:57 "nginx2root (CVE-2026-123007)" https://www.stepsecurity.io/blog/cve-2026-123007-nginx-http2-rce (not supply chain, for scout 2; the 20 Nov file shows the same post at 20 Nov 08:33, so the feed date has moved, already seen by URL). 21 Nov 00:10 "StepSecurity's $20 million Series A" (company post, already seen). 21 Nov 00:10 OPTIMJACK (already seen; feed date is the update). No gap. |

## Pages opened

| # | URL | UTC read | Gate | Status | Page's own date | Claim, reported by the page (summariser relay) | New? |
|---|---|---|---|---|---|---|---|
| 1 | https://socket.dev/blog | 12:16Z | allowed | fetched | no dates shown | Newest first: "13 Malicious NuGet Packages Target .NET Developers With Fake Job Assessments", then "Hardening GitHub Actions Against Insider Threats"; also lists "Cyberattacks Are Skyrocketing in Japan as Researchers Trace AI-Assisted Intrusions" (title only). | NuGet post is a new title; the rest seen. Text of neither opened |
| 2 | https://www.aikido.dev/blog | 12:16Z | allowed | fetched | newest 23 Nov | 23 Nov "Hardened container images: STIGs, FIPS and FedRAMP explained" is newest; nothing on compromised packages after 17 Nov (agent-framework) and 12 Nov (wfx-loot). | no new relevant |
| 3 | https://blog.pypi.org/ | 12:16Z | allowed | fetched | newest 18 Nov | Newest remains "Stricter checks for uploaded distributions on PyPI" (18 Nov). No malware or quarantine post. | seen |
| 4 | https://github.blog/changelog/label/supply-chain-security/ | 12:16Z | allowed | fetched | newest 20 Nov | 20 Nov "Security advisory permissions are now generally available"; page does not mention pull_request_target. | new entry, minor |
| 5 | https://blog.rubygems.org/ | 12:16Z | allowed | fetched | newest 23 Nov | 23 Nov "content-addressable gems" (precompiled binaries packaging); no malware or yank post. | new post, not security |
| 6 | https://www.anaconda.com/blog/ai-supply-chain-security | 12:16Z | allowed | fetched | 20 Nov 2026 | Roundup of two incidents. Agent-framework recap (1.26.1 and 1.26.2, 17 Nov, "about 190,000 monthly downloads"). Second: researchers took over the lapsed domain hexgrad.com, reset the publisher's Hugging Face password and "changed the model's weights in 87 seconds"; Kokoro text-to-speech model has "nearly 13 million monthly downloads"; researchers "ran it only on their own hardware and uploaded nothing"; Hugging Face had not responded. | New (no earlier sweep mentions Kokoro or hexgrad) |
| 7 | https://cycode.com/blog/keyv-cacheable-npm-worm-ai-coding-agents/ | 12:16Z | allowed | fetched | "Last updated October 1, 2026"; incident 4 Aug | keyv/cacheable worm: 11 malicious releases across 61 packages, hundreds more republished; persistence in AI coding tools' and editors' configuration files so opening the repository or starting a Claude Code session runs the loader; harvester targets Claude, OpenAI, Codex, Cursor and Gemini credential stores. | Incident old (keyv/cacheable is in the 13 Nov scout 3 file as "August"); the Cycode URL and its AI-agent persistence detail are new to the sweep files |

## Searches

1. "malicious npm PyPI packages compromised credential stealer AI agent November 2026": only agent-framework write-ups (Wiz, Hacker News, BleepingComputer, Help Net Security, CSA, Security Boulevard, others). Nothing new on it. None opened beyond the Anaconda page found by a later query.
2. "npm worm self-propagating ... 22 November 2026": no worm dated after 20 Nov. Results were Miasma/binding.gyp (StepSecurity, Snyk), Shai-Hulud variants, xygeni, nhimg.org (describes keyv/cacheable), mallory.ai. Not opened except via query 5 (nhimg is a 403, see below).
3. "Hugging Face malicious models supply chain November 2026": nothing dated November; older items (JFrog, Transformers kernels CVE-2026-4372, Zafran diffusers, Unit 42 namespace reuse, thenextweb on HF and ClawHub). Not opened.
4. Cycode query on keyv/cacheable: gave the Cycode post (opened).
5. "wfx-loot update ... November 23": no new development; coverage is 11 to 12 Nov. Reported AI keys targeted (OpenAI, Anthropic, Gemini, Hugging Face, Cursor, Copilot) per the search summary; persistence via wfx-ci-* cloud credentials. Not opened (CSA, BleepingComputer, ox.security, SailPoint, hackread, aviatrix, darkdive, others).
6. Date-phrase search for 21 to 23 Nov: nothing new beyond agent-framework and Optimizely; a CSA daily briefing of 22 Nov (https://labs.cloudsecurityalliance.org/research/ciso-daily-briefing-20261122) and agentbeam and explainx trackers surfaced, not opened.
7. GitHub Action or container image compromise this week: none found. Surfaced React2STEAL (GitGuardian, https://blog.gitguardian.com/react2steal-hijacked-github-accounts-exploit-react2shell-and-publish-stolen-secrets, not opened, not in earlier sweep files) and the Substack "AI Agent Security Weekly" issue 43 (not opened).
8. Wiz 3,392 accounts query: confirmed from snippets only that Wiz's ARTEX write-up (https://www.wiz.io/blog/agentic-attacks-artex-offensive-ai-frameworks) is the primary; this is ARTEX material (LH055), not supply chain. Not opened.

## Refused or unreached

- https://rustsec.org/advisories/ : gate allowed=false (robots.txt returned 503, as on 18 Nov). Not fetched. RustSec is unchecked this sweep.
- https://cybersecuritynews.com/ai-powered-hackers/ : gate allowed=false. Not fetched.
- https://nhimg.org/articles/ai-coding-agent-malware-turned-npm-trust-into-a-delivery-path : gate allowed, fetch returned 403 (a wall, recorded, not worked around). The Cycode primary was read instead.
- https://socket.dev/blog/13-malicious-nuget-packages-target-net-developers-with-fake-job-assessments : gate allowed; the URL was my guess from the title, returned 404. The post text was not read.
- Not checked: npm's own changelog, OpenSSF, Phylum/Veracode, ReversingLabs, Wiz's blog index, Hugging Face's security pages, crates.io.

## Quiet, stated as quiet

No new compromised release on npm, PyPI, RubyGems or crates was found since 20 November on the listings read, and nothing new on bee-js, WPPConnect, agent-framework, LiteLLM or wfx-loot. A few listings and searches are not a registry count. Nothing found on GitHub's `pull_request_target` block beyond Socket's 5 Nov (modified 18 Nov) post, read last sweep: block from 2 Dec, no new notice.

## Five best leads

1. **Kokoro and Hugging Face account takeover via a lapsed domain (https://www.anaconda.com/blog/ai-supply-chain-security, 20 Nov; primary researcher write-up not found or opened).** Reported: researchers reset a publisher's password through an expired domain and altered the weights of a model with about 13 million monthly downloads; nothing shipped. Charter: a model hub as a supply chain whose update path is an expired domain; relevant to where updates go, but a demonstration, not an incident. New. Next: find the original researcher post and Hugging Face's reply; whether any hub-side fix follows.
2. **keyv/cacheable worm persistence in AI-agent config (https://cycode.com/blog/keyv-cacheable-npm-worm-ai-coding-agents/; incident 4 Aug, page updated 1 Oct).** Reported: a worm that plants persistence in AI coding tools' and editors' configuration files, targets AI-agent credential stores, and authors commits under a "claude" string. Charter: the nearest thing found to a self-spreading package aimed at AI agents' tooling; old incident, new detail for the sweep. Not urgent (fixed publication). Next: read Cycode's and the npm primaries before any use.
3. **Agent-framework, nothing new, but Anaconda's 20 Nov roundup restates ~190,000 monthly downloads and no entry vector (same URL as lead 1).** Charter: agent packages as a target. Leave to LH056's reads.
4. **wfx-loot: no new development found since 12 Nov;** reported targeting of AI provider keys and persistence that survives rotation stays the standing lead (Aikido https://www.aikido.dev/blog/compromised-github-accounts-push-ci-secret-stealer-to-tens-of-thousands-of-repositories). The 2 Dec `pull_request_target` block is the next dated event; no new notice found.
5. **Socket's "13 Malicious NuGet Packages ... Fake Job Assessments" and "Cyberattacks Are Skyrocketing in Japan as Researchers Trace AI-Assisted Intrusions" (https://socket.dev/blog, titles only).** The second may bear on AI-assisted activity; neither was read. Low confidence; new titles. Next: open both at their own URLs next sweep.

## Urgent

None found. Standing windows from 20 Nov (wfx-loot residue, agent-framework package page) unchanged as far as read.

## Withheld under research safety

None.
