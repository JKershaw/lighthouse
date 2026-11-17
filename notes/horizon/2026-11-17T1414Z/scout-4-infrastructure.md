# Scout 4, Internet infrastructure and measurement, run 2026-11-17T1414Z

**In short.** Rotation I25 to I32 (npm download counts, Node.js metrics, Packagist, GH Archive, deps.dev, CISA KEV, CVE List, OSV.dev) read 14:17 to 14:19 UTC on 17 November 2026. Only three pages carried anything new: Packagist's counters, the KEV count and entries, and a deps.dev blog post (9 June) that is not in the sources row. The npm, Node.js, GH Archive, CVE List and OSV FAQ pages were unchanged from the rows. WebFetch answers are a small model's extract, so quotations are as the extract gave them, and every claim below is reported by the page, not observed. No file other than this one was written; I did not read the environment for keys or search harbour/.session/.

## Searches (WebSearch, standard)

1. "npm registry download counts change November 2026": no official change notice; third-party trackers (Amplifying, a stats-API-bug article); none opened.
2. "CISA KEV BOD 26-04 forensic triage November 2026": only June to August secondary coverage (CyberScoop, Qualys, CSA, Paubox, others); none opened. Nothing dated November.
3. "CVE Program MITRE contract CVE Foundation November 2026": April 2025 coverage and a CVE Foundation launch item (cybersecuritynews.com, headline date "7 October 2026" as shown by the engine); nothing on what happened at the March 2026 option end. None opened.
4. "OSV.dev new ecosystems supported 2026": OSV year-in-review pages, a third-party mention of schema 1.9.2 dated 13 Oct 2026 and OSV-Scanner v2.7.0 (Oct 2026); not opened.
5. "GH Archive GitHub Events API change 2026 AI agent activity": Octoverse 2026 coverage (agents started 110 million pull requests in September, over 40%, per Visual Studio Magazine 29 Oct), GitHub changelog on Events API payloads (Oct 2025). GH Archive itself: nothing.
6. "Packagist Composer supply chain incident November 2026": May 2026 campaigns, Packagist's own post; nothing in November.
7. "Node.js download metrics AI agents CI traffic 2026": NodeSource and HeroDevs posts (Node 18 and 20 EOL still "more than 136 million" downloads in July 2026), a crates.io Foundation estimate that CI is about half its traffic and declared AI agents 0.3% of requests on one day in June 2026; none opened.
8. "deps.dev Open Source Insights new ecosystem announcement 2026": deps.dev blog items (GOSSIP signals, Gradle Plugins, RubyGems).
9. "Packagist blog artifact integrity Composer 12 November 2026": no 12 Nov post found; Composer 2.11 cooldowns (Socket), immutable tags (July 2026 per TuxCare); not opened.
10. "Ingesting CVEList 5.0 into OSV.dev": the OSV post itself (osv.dev/blog/posts/faster-cve-data/), not opened; the engine's summary only.

Search results not opened: all items above marked "not opened"; the Visual Studio Magazine Octoverse page was opened and returned 403.

## Pages opened (UTC, 17 Nov 2026)

Gate: all allowed (robots 200, or 404/403 meaning no rules for raw.githubusercontent.com, google.github.io and cisa.gov).

| # | URL | Read | Status | Page date | Reported by the page | New or seen |
|---|---|---|---|---|---|---|
| 1 | https://raw.githubusercontent.com/npm/registry/main/docs/download-counts.md (I25) | 14:18 | 200 | none | Counts loaded "once a day, shortly after UTC midnight"; earliest data 10 January 2015; bulk 128 packages and 365 days, other queries 18 months; per-version counts previous 7 days. | seen (URL in 2026-11-10T1415Z.md); unchanged |
| 2 | https://nodejs.org/metrics/ (I26) | 14:18 | 200 | none | "roughly one log file per day, starting on the 14th of May 2014"; current file "is not final"; "zero, one or two log files for a given day"; September 2015 gap. No latest date and no changelog. | new to notes/horizon; row unchanged (the two-files-a-day remark is not in the row) |
| 3 | https://packagist.org/statistics (I27) | 14:18 | 200 | none | 481,708 packages; 6,089,883 versions; 214,712,545,431 installs since 2012-04-13. Against the 6 Nov raw figures in the row (479,199; 6,040,573; 211,475,236,112): +2,509 packages, +49,310 versions, +3,237,309,319 installs in 11 days (my arithmetic). Last chart points partial. | new figures |
| 4 | https://www.gharchive.org/ (I28) | 14:18 | 200 | none | Archives from 2/12/2011; hourly; "15+ event types"; Timeline API "(now deprecated)"; payload "may be updated by GitHub at any point". | new to notes/horizon; row unchanged |
| 5 | https://docs.deps.dev/faq/ (I29) | 14:18 | 200 | footer "Copyright 2021 Google LLC" | Seven ecosystems (Cargo, Go, Maven, npm, NuGet, PyPI, RubyGems); freshness "within an hour or so"; no C or C++; resolution matches native tooling "99% or higher". | new to notes/horizon; unchanged. The FAQ does not list Gradle Plugins, which a search snippet says deps.dev added (unverified). |
| 6 | https://www.cisa.gov/known-exploited-vulnerabilities-catalog (I30) | 14:18 | 200 (the row's 6 Nov raw re-read got 403; WebFetch got through today) | latest Date Added 2026-11-13 | "Showing 1 to 20 of 1781 results" (1766 on 2 Nov: +15 in 15 days, my arithmetic). Newest: 13 Nov Check Point multiple products and UnrealIRCd; 10 Nov Chromium, Barracuda x2, Cisco BroadWorks, Openwave transcoder, Outlook; 9 Nov IBM Aspera Faspex, FreeSwitch, OpenSSH, GPUStack. A "Forensic Triage (BOD 26-04)" column ("Yes" or "No") with due dates of three days for "Yes" rows; ransomware use "Unknown"; JSON Schema "updated 09-02-2026". | new fields: forensic-triage column and short due dates; counts new |
| 7 | https://raw.githubusercontent.com/CVEProject/cvelistV5/main/README.md (I31) | 14:18 | 200 | newest note 2026-02-17 | Updated "about every 7 minutes"; daily baseline; deltaLog 30 days; 2025-10-29 record format 5.2.0 adds Package URL identifiers; 2024-09-17 about 27,000 pre-2023 records' dates corrected. | seen; unchanged (no note since February) |
| 8 | https://google.github.io/osv.dev/faq (I32) | 14:18 | 200 | none | "no more than 15 minutes stale, 99.5% of the time"; no rate limit; HTTP/1.1 responses capped at 32 MiB; withdrawn records omitted from POST queries; update aborts if more than 10% of records would be withdrawn; REST and Git source orphans "will be changed" to match, no date. | seen; two details (32 MiB cap, 10% abort) not in the row |
| 9 | https://blog.deps.dev/gossip/ (I29) | 14:19 | 200 | 9 June 2026 | GOSSIP signals via API: Dynamic Cooldown, `MALICIOUS`, `VULNERABLE`, `LOW_USAGE`, archived packages; describes "slopsquatting" (attackers registering package names LLMs hallucinate); names an "AI developer trying to make sure your LLM isn't hallucinating you into trouble"; repo carries a SKILL.md "agent-centric implementation guide". | new |
| 10 | https://osv.dev/blog (I32) | 14:19 | 200 | newest 11 Aug 2026 | Last post "Faster, Cleaner CVE Data: Ingesting CVEList 5.0 into OSV.dev"; none since; 2025 review 13 Jan 2026. | new |
| 11 | https://blog.packagist.com/an-update-on-composer-packagist-supply-chain-security (I27) | 14:19 | 200 | 27 May 2026 (sidebar shows posts of 29 Oct and 12 Nov 2026) | Aikido malware results imported since March 2026; immutability for stable versions; Composer 2.10 dependency policy; a transparency log; attacks on intercom/intercom-php (30 April) and laravel-lang (22 May); "If you maintain any package on Packagist.org and don't have MFA enabled, please enable it now." | new |
| 12 | https://visualstudiomagazine.com/articles/2026/10/29/github-octoverse-agents-started-more-than-40-percent-of-september-pull-requests.aspx | 14:19 | 403 | n/a | Not read; a wall, not tried again. | new (wall) |

## Walls and gaps

- Visual Studio Magazine: HTTP 403 (observation, not retried).
- CISA robots.txt answered 403 (gate: no rules); the page itself answered 200 today although the 6 Nov raw re-read was refused: the wall is not constant.
- Not opened for lack of a path: the OSV CVEList post, the Packagist 12 Nov post, the Composer 2.11 notes.
- No I25 to I32 page states a date for itself except KEV, the CVE README and the blogs; Node.js, GH Archive and npm pages cannot be dated by change.

## Five best leads

1. KEV's forensic-triage column and three-day due dates under BOD 26-04 (https://www.cisa.gov/known-exploited-vulnerabilities-catalog; 8 of the 12 newest entries show "Yes" or short due dates). The charter asks about harm to shared infrastructure; a per-entry flag that "triage is required" is the first public, dated record of which exploited flaws the US government treats as compromise-likely. Reported by the page only; a daily copy of the JSON feed (CISA terms to be checked) would lose nothing now but each day's additions are only visible as dated rows; the catalogue's history is kept, so the loss is slight.
2. deps.dev GOSSIP signals (https://blog.deps.dev/gossip/, 9 June 2026). A registry-adjacent service names slopsquatting by LLMs and builds a LOW_USAGE signal and agent-readable guidance for it. Matters because it is a producer-side measure of AI-driven package-name abuse, and the findings endpoint is a possible instrument (v3alpha, so it may change); first values would be lost if the alpha API moves or signals are re-tuned.
3. Packagist's counters and security programme (https://packagist.org/statistics; https://blog.packagist.com/an-update-on-composer-packagist-supply-chain-security, 27 May 2026). About 3.2 billion installs and 49,000 versions in 11 days gives a rate for PHP's software supply; the registry now keeps a public transparency log and flags malware, so attacks on abandoned packages are countable. Daily counter values are only on the live page (no history), so a dated series would be lost unless someone records it.
4. OSV ingesting CVE List records directly (https://osv.dev/blog, 11 Aug 2026; post itself unopened). Moves OSV from NVD-dependent to CVE-direct, which changes what its record counts mean for any study that trends them (LH030 queries OSV). A change in an instrument's meaning is cheap to note now, hard to reconstruct later.
5. Agents' share of GitHub activity (Octoverse via Visual Studio Magazine, 29 Oct 2026, 403 to me; "110 million pull requests in September, over 40%", from the search engine's summary only). Not a rotation instrument, but it is the largest stated share of agent-originated activity in any public record I met, and GH Archive (I28) is the instrument that could test it hour by hour; GitHub says the Events API no longer carries commit detail in payloads (October 2025 changelog, from a search summary), which limits what GH Archive can show. Needs a primary GitHub source before anything is built on it.

## Urgent

None.
