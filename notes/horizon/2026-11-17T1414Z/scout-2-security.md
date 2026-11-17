# Scout 2, Security and vulnerabilities, run 2026-11-17T1414Z

**In short.** The new fact since 13 November is Project Zero's policy of 13 November, which says in its own words that AI-assisted discovery and exploitation have made its old remediation timeline "clearly insufficient", and sets a schedule of 90, 60 then 30 days. KEV gained two entries on 13 November (UnrealIRCd, Check Point), none since. oss-security carried a kernel TCP pre-auth flaw on 15 November. Every claim below is reported by the page named, not observed by Lighthouse, unless marked "fetched by scout" (a plain read of a feed). Nothing read was treated as an instruction. No email addresses are recorded. Each fetch followed a robots gate run; `LIGHTHOUSE_PROVIDER=anthropic` throughout. The container clock read about 14:17 to 14:18 UTC for every read.

## What KEV added since catalogue version 2026.11.10

Fetched by scout at 14:17 UTC: catalogVersion 2026.11.13, released 2026-11-13T20:24Z, 1781 entries (1779 on 2026.11.10, so two added). Nothing added since 13 November.

- UnrealIRCd CVE-2026-114713 (improper neutralisation of delimiters), added 13 Nov, due 16 Nov (three days).
- Check Point multiple products CVE-2026-123039 (incorrect permission assignment for a critical resource), added 13 Nov, due 16 Nov.

Ransomware use "Unknown" for both. EPSS fetched by scout, scores of 16 Nov: UnrealIRCd 0.0051 (percentile 0.439), Check Point 0.0219 (0.827). The two Barracuda entries of 10 Nov are 0.1095 (0.960) and 0.0908 (0.954), almost unchanged from 13 Nov. Both new entries carry the three-day deadline and a low EPSS, as the Barracuda pair did.

## Searches

1. "Project Zero Full 90 disclosure policy AI vulnerability discovery reaction": mostly 2025 coverage (schneier, itnews, securityweek on the 2025 trial); fourweekmba and phemex describe the 2026 schedule; cybersecuritynews page headed 8 Oct 2026 describes the 2025 trial. Search summary found no primary reaction. Opened none of these; opened the-decoder (below). Not opened: schneier, itnews, securityweek, fourweekmba, phemex, softwarereviews, itpro, techradar, cyberscoop.
2. "AI-discovered vulnerabilities exploit within hours of patch November 2026": nothing from November; May 2026 items (hivepro, CSA PDF, lmgsecurity, guptadeepak, foxxelabs, pulse.bot, threatcluster). Summary cites "Copy Fail" kernel case, Exim CVE-2026-45185 found by an AI agent, and M-Trends and DBIR figures, all secondary. Not opened.
3. "NoisyTCP CVE-2026-99288 Linux kernel": Debian tracker (opened), penligent, vulners tag pages, averlon, redhat and nixos trackers for other CVEs. Not opened except Debian.
4. "AI agent framework critical vulnerability exploited in the wild this week ...": Langflow, Ray items from March to August; nothing for this week, nothing on UnrealIRCd or Check Point. Not opened (bleepingcomputer disallowed in earlier sweeps and not gated again).
5. "NCSC OR CERT-EU advisory AI vulnerability research frontier models patch wave November 2026": NCSC "patch wave" blog of 1 May 2026 and coverage (scworld, theregister, therecord, securityaffairs, CSA note); no November advisory. Not opened.

Direct reads (not searches): CISA KEV JSON, FIRST EPSS API, Project Zero archive and the new post, oss-security November index and two posts, Debian tracker. NCSC and CERT-EU listing pages were gated (allowed) but not read, for time.

## Pages opened

| # | URL | Read (UTC) | Status | Page date | Claim reported | New or seen |
|---|---|---|---|---|---|---|
| 1 | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | 14:17 | 200 | 2026.11.13, 13 Nov 20:24Z | 1781 entries; two added 13 Nov (UnrealIRCd, Check Point), due 16 Nov. Fetched by scout. | standing source; two entries new |
| 2 | https://api.first.org/data/v1/epss?cve=(four CVEs) | 14:17 | 200 | scores of 2026-11-16 | Barracuda 0.1095 and 0.0908; Check Point 0.0219; UnrealIRCd 0.0051. Fetched by scout. | standing source; values new |
| 3 | https://projectzero.google/archive.html | 14:17 | 200 | latest post 2026-11-13 | Archive lists "2026-Nov-13 Policy and Disclosure: 2026 Edition" above the 27 Oct fuzzing post. | seen (archive); the post is new |
| 4 | https://projectzero.google/2026/11/disclosure-policy.html | 14:18 | 200 | 13 Nov 2026, Natalie Silvanovich | "The advent of AI-assisted vulnerability discovery and exploitation has changed the threat landscape such that the vulnerability remediation timeline encouraged by our disclosure policy is clearly insufficient." Replaces "90 + 30" with "Full X": disclosure X days after report; "Full 90" now, "Full 60" from 2 Feb 2027, "Full 30" from 3 Jan 2028. "We are finding several vulnerabilities a week in targets where we once found a few vulnerabilities a year." Calls zero patch-to-exploit time "a reasonable, though imperfect, model of attacker behavior". Exceptions: exploited in the wild, already public, vendor request. Page text was read to the severity section only. | new |
| 5 | https://www.openwall.com/lists/oss-security/2026/11/ (index) | 14:17 | 200 | to 17 Nov, 268 messages | Lists the NoisyTCP advisory (15 Nov), a BenchProctor release (16 Nov), a run of memory-safety CVEs in GPAC, littlefs and MicroQuickJS from one reporter (15 and 16 Nov), a vim advisory pair, and an "sshole" OpenSSH plus musl thread (16 and 17 Nov). | seen (index); entries new |
| 6 | https://www.openwall.com/lists/oss-security/2026/11/15/2 | 14:18 | 200 | posted 16 Nov 01:00 +0900 (15 Nov UTC) | "The embargo agreed with the maintainers ... has expired, so I am posting this report." NoisyTCP, CVE-2026-99288: a race in TCP lookup, triggered "pre-auth and remotely against servers that TCP packets sent by an attacker can reach directly, such as Nginx, Apache, and SSH servers running with their 'default' configuration", needing two or more receive queues or RPS. No AI mention in the part read. | new |
| 7 | https://www.openwall.com/lists/oss-security/2026/11/16/5 | 14:18 | 200 | 16 Nov 2026 | A maintainer releases BenchProctor 2026.11.16, a static-analysis benchmark of 2,142 standalone cases, after withdrawing a July corpus over "bad safe labels". | new |
| 8 | https://security-tracker.debian.org/tracker/CVE-2026-99288 | 14:18 | fetched | undated | Fixed builds listed for bookworm (6.1.192) and trixie (6.12.117); a proof of concept is linked. Impact shown is a crash. | new |
| 9 | https://the-decoder.com/ai-turns-patches-into-working-exploits-in-30-minutes-and-the-90-day-disclosure-window-is-the-casualty/ | 14:18 | fetched | 11 May 2026 | Attributes to a security researcher's blog a working exploit built from a patch diff "in about 30 minutes" and argues the 90-day model is undermined; "Right now, the attackers are winning that race." | new (old, context) |

## Refusals and walls

Nothing refused by robots.txt this sweep (the sources opened were all allowed; cisa.gov robots answered 403, which the gate treats as no rules, and its feed answered 200). No walls met. No exposed hosts visited. The NoisyTCP proof of concept on a code forge was not opened and nothing was run.

## Five best leads

1. Project Zero's "Full 90 / 60 / 30" policy, 13 Nov (https://projectzero.google/2026/11/disclosure-policy.html). A major disclosure body states that model-assisted finding and exploiting has made the remediation timeline insufficient and that it now finds "several vulnerabilities a week" where it found a few a year; this bears on the charter's question as institutional evidence that the patch window, a shared-infrastructure buffer, is shrinking. First observations that could be lost: the vendors' behaviour inside the 80 days before Full 60 (disclosure dates on the Project Zero tracker are public and persist, but the pre-change baseline of open reports and any vendor reactions would be cheapest to capture now). Not urgent in hours, worth a snapshot within days.
2. KEV three-day deadlines with low EPSS, 10 and 13 Nov (feed above). Four of eight recent entries (Barracuda x2, UnrealIRCd, Check Point) carry deadlines of three days while EPSS is below 0.03 for two of them; a time series of deadline length against EPSS and dateAdded can be built from the daily feed, whose earlier versions are overwritten, so the daily snapshot is lost if nobody saves it. Bears on how fast the patch window closes.
3. NoisyTCP, CVE-2026-99288 (https://www.openwall.com/lists/oss-security/2026/11/15/2). A pre-auth remote kernel flaw reachable through default web and SSH listeners, posted at embargo expiry with a proof of concept linked; the question for the charter is whether exploitation appears fast and how patched-kernel rollout lags. Whether it was found with a model is not stated in the part read. Exploitation signals, if any, appear in the first days and are then buried.
4. The run of memory-safety CVEs from one reporter across GPAC, littlefs and MicroQuickJS, 15 and 16 Nov (oss-security index above). A steady stream of near-identical crash reports in small, little-maintained libraries is the pattern Project Zero describes as volume; whether tooling produced it is not stated in the index and is worth checking in the posts' own wording. Low urgency; the posts persist.
5. Absence of primary counts, again: the search found no November primary figure for model-found flaws, only May to July secondary pieces (the-decoder 11 May, NCSC "patch wave" 1 May). Project Zero's sentence in lead 1 is the first primary rate seen by this scout. A direct look at the lab disclosure pages next sweep would show whether any lab publishes a dated count. Nothing is lost if left.

## Urgent

None. KEV and EPSS values are rewritten daily, so lead 2 is the one whose history is lost without a snapshot.
