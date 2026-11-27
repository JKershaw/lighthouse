# Scout 3, Software supply chain, run 2026-11-27T1212Z

**In short.** GitHub's changelog entry on the `pull_request_target` default block still says enforcement starts on 2 December 2026 (read raw, nothing changed since 2 November). The StepSecurity feed has one new supply-chain item, PolinRider, reported as a self-spreading loader force-pushed into open pull requests, with GitHub suspending the account on 25 November; it does not describe AI agents as part of the attack. Nothing new turned up on bee-js, WPPConnect, the agent-framework releases or LiteLLM. Everything below is reported by the page named, never Lighthouse's observation.

Start 12:14Z, end 12:16Z (`date -u`). Tools: scripts/lh_feeds.py, scripts/robots_gate.py (provider anthropic, before every fetch), curl for the raw changelog, WebFetch (a summariser, so quotations are relayed), WebSearch. No keys read. The raw changelog body is saved under the scratchpad only (s3/prt.html), not in the repo.

## Direct publication checks

| Endpoint | UTC read | Interval covered | Outcome | Entries |
| --- | --- | --- | --- | --- |
| https://www.stepsecurity.io/blog/rss.xml (lh_feeds, --since 2026-11-24) | 12:14Z | 24 Nov to 27 Nov; feed oldest 2026-04-12, newest 2026-11-26, no skipped or undated entries | new entries, one relevant | 26 Nov 09:16 "Fail2Install (CVE-2026-132165)" Drupal installer flaw https://www.stepsecurity.io/blog/fail2install-cve-2026-132165 (not supply chain, for scout 2; new). 25 Nov 22:13 "PolinRider Malware Force-Pushed Into AsyncAPI, CircuitVerse and Open Food Facts Pull Requests" https://www.stepsecurity.io/blog/polinrider-malware-open-source-pull-requests (new). 25 Nov 08:38 "The Take-Home Test That Runs on Your Work Laptop: Inside the AccuraSoftHire Fake Interview Campaign" https://www.stepsecurity.io/blog/accurasofthire-fake-interview-developer-machines (URL seen in the 17 Nov sweep, so not new). 24 Nov 10:57 nginx2root (seen last sweep). No gap. |

## Standing-source results (brief)

- GitHub changelog, supply-chain-security label: newest 20 Nov "Security advisory permissions are now generally available"; nothing after it, nothing on `pull_request_target`. Seen last sweep.
- PyPI blog: newest still 18 Nov "Stricter checks for uploaded distributions on PyPI"; no malware or quarantine post. Seen.
- Not read this sweep: Socket blog (gate allowed it but marked bodies not to be kept, and I did not fetch it), npm changelog, crates.io, RustSec (refused last sweep), RubyGems blog, OpenSSF, Hugging Face security pages.

## Specific (a): `pull_request_target`

The raw changelog page (https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2/) is reported by itself as labelled "Retired", dated 2 November 2026: "Starting December 2, 2026, GitHub Actions will block pull_request_target events by default in all public repositories, unless an applicable Actions event policy explicitly allows them. Enforcement was previously scheduled for November 2, 2026." Brownouts listed 9 and 16 November, 16:00 to 18:00 UTC; private and internal repositories not affected. The date is unchanged; the page shows no later edit note in the text I read. Whether the brownouts happened as stated was not checked. Fixing a brief for P-0012 before 2 December is still possible per proposals.md; I make no recommendation.

## Specific (b): watched releases

Two searches found nothing dated after 20 November on bee-js, WPPConnect, agent-framework or LiteLLM. Search summaries (not opened) restate: agent-framework 1.26.1 and 1.26.2 on 17 November; WPPConnect core 2.4.1 and server 2.10.82; bee-js 13.3.0 of 9 November. A GitHub pull request in a repository named drydock (https://github.com/JoviDeCroock/drydock/pull/852, new, not opened, GitHub pages may wall) is described by the snippet as replaying the bee-js and WPPConnect compromises; its relevance is unknown. Xygeni's digest 95 (https://xygeni.io/blog/xygeni-malicious-code-digest-95/, new, not opened) is described by the snippet as counting 27 malicious versions between 15 and 19 November. Quiet, stated as quiet: a few searches are not a registry count.

## Searches

1. "compromised npm OR PyPI package malicious release November 26 2026": agent-framework write-ups (Hacker News, CSA, Wiz, Elastic, Aikido, Help Net Security, others) and Xygeni digest 95. None opened; no result dated 26 November.
2. "bee-js OR WPPConnect OR LiteLLM OR agent-framework compromised package update": as above in (b). None opened.
3. "PolinRider malware npm packages Socket OR Aikido OR Wiz": Socket's tracker https://socket.dev/supply-chain-attacks/polinrider (new, not opened), Socket blog, Abnormal, OpenSourceMalware, Corgea, boring.tools and others, mostly dated from July 2026. Not opened. The summary links PolinRider to a North Korea-linked cluster per Socket; I did not verify.

## Pages opened

| # | URL | UTC read | Gate | Status | Page's own date | Claim reported by the page | New? |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | https://www.stepsecurity.io/blog/polinrider-malware-open-source-pull-requests | 12:15Z | allowed | fetched (WebFetch relay) | 25 to 26 Nov 2026 | Rewritten commits with a hidden loader were force-pushed into open pull requests from one GitHub account; "GitHub suspends the account and removes its pull requests" on 25 Nov; CircuitVerse "confirms the loader ran in its CI"; Open Food Facts rotated a secret; later stages steal credentials and, victims report, use stolen GitHub tokens to push the loader into more repositories; the page does not describe AI agents as attackers (an AI code reviewer flagged a line, as a defender). Wider count of 576 infected repositories across 311 accounts. Relayed, quotations via summariser. | new |
| 2 | https://github.blog/changelog/label/supply-chain-security/ | 12:15Z | allowed | fetched (WebFetch relay) | newest 20 Nov | See above. | seen |
| 3 | https://blog.pypi.org/ | 12:15Z | allowed | fetched (WebFetch relay) | newest 18 Nov | See above. | seen |
| 4 | https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2/ | 12:15Z | allowed | 200, read raw by curl, text extracted locally | 2 Nov 2026 | See specific (a). | seen (URL in proposals.md) |

## Five best leads

1. **PolinRider forced-push loader (https://www.stepsecurity.io/blog/polinrider-malware-open-source-pull-requests, 25 to 26 Nov).** Reported: a self-spreading loader that uses stolen tokens to push itself into more repositories; ran in one project's CI. Charter: software spreading itself through shared build infrastructure, though the page says no AI agent took part, so it bears on spread by people-run malware, not AI activity. Touches the software-updates investigation as background only. New.
2. **`pull_request_target` enforcement on 2 December, unchanged (changelog above).** Charter: a platform closing a door a worm used. Touches P-0012; last sweep before enforcement. Decision belongs to the gate.
3. **Socket's PolinRider tracker (https://socket.dev/supply-chain-attacks/polinrider, not opened).** Would give a count across ecosystems and dates to set beside lead 1. New, unread.
4. **Xygeni digest 95 (https://xygeni.io/blog/xygeni-malicious-code-digest-95/, not opened).** Snippet: 27 malicious versions on 15 to 19 November, mostly one npm package. A weekly count for context, unread. New.
5. **drydock pull request replaying the bee-js and WPPConnect compromises (https://github.com/JoviDeCroock/drydock/pull/852, not opened).** Snippet says it checks where a gated release came from; may carry a reader's account of both compromises' mechanism relevant to LH049 and LH053. Unverified, GitHub may wall. New.

## Gaps and refusals

- No refusals this sweep. Socket's blog gate answer was allowed with keep_body false (a training or archiving crawler is refused at the path); not fetched.
- Not checked: npm changelog, crates.io, RustSec, RubyGems, OpenSSF, Hugging Face. LH056 and LH040 packages' own pages not read.

## Urgent

None found.

## Withheld under research safety

None.
