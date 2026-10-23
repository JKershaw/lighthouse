# PHP discovery pass, 23 October 2026: query plan fixed before searching

**Fixed 23 October 2026, before any search in this pass.** Writer: a Claude Code driving session (Claude Opus 5.5). This is Priority 2 of notes/php-watch-continuation-2026-10-23.md: one bounded pass to find leads beside the fixed watches, then triage. It is not a study protocol, a sample or a coverage measure, and no completeness or internet-wide percentage follows from it.

## Already known, so not a discovery here

The sources and outcomes in LH018 to LH029 (PHP's notices of 20, 21 and 23 October; NCSC, CISA (refused), CERT-EU, Cloudflare, Fastly, Akamai, the AWS and Google Cloud placeholders; The Register, BleepingComputer and Ars Technica; Amazon's MadPot account; OpenAI's coordination account; the official PHP, WordPress, Drupal and Nextcloud images; docker-library issue #1693, PRs #1694 and #22541 and official-images issue #22546; The National Archives' refused notice). The PHP Foundation's 21 October post and its claim about Chainguard's early images (notes/proposals/php-emergency-fix-investigation.md). News headlines claiming millions of attempts, with no primary aggregate found so far (LH028). PHP's 23 October instruction to set `session.upload_progress.enabled=0`, and Cloudflare's 23 October account of it.

## Bounds

At most six searches, in the order below, with the session's web-search tool in its standard mode, and at most eight new primary pages opened in total. Each result list is written to `search-results.md` as returned, in rank order, title and URL, immediately after the search; the tool exposes no raw response, so that transcription is the retained log, and any truncation is recorded. A page is opened only if it is a first-party source (sensor operator, agency, vendor, project tracker or the operator itself) not already retained in LH018 to LH029, at most two per query, choosing the highest-ranked such result. A media article is not opened; where a result is media, its claim is a lead and the primary source it names is preferred. Pages are read directly with a urllib reader that retains status, UTC times, length and SHA-256, and the raw bytes of first-party pages up to 1 MiB; a refusal or placeholder is recorded as such and not replaced by a snippet. No login, paid service, exploit, probe of any site, or contact with anyone.

**Kept out on purpose.** No query names CVE-2026-115560, session upload progress or the 23 October instruction, so that a later brief on how that instruction travels through a defined panel can be fixed before its outcomes are read. Any result that nonetheless shows a page carrying it is logged and disclosed to that brief as prior knowledge, and the page is not opened in this pass.

## Queries, fixed

1. `CVE-2026-109618 exploitation attempts telemetry` (original attempt telemetry with a sensor, unit and window)
2. `CVE-2026-109619 known exploited vulnerabilities catalog` (an agency's exploited-in-the-wild record and its date)
3. `PHP vulnerability exposed servers scan Shadowserver October 2026` (counts of exposed or unpatched hosts with a stated method, a candidate denominator)
4. `PHP critical vulnerability services taken offline precaution October 2026` (operators' precautionary actions)
5. `php2shell honeypot scanning observed` (further sensor accounts, from operators other than Amazon)
6. `PHP 8.5.12 release packaging delay distribution build problem` (publishing or CI problems in the fix's path)

## Triage

`ledger.md` gets one row per opened page or decisive lead: source, actual read time, the source's own event clock, the claim, what is new against the list above, the measurable boundary (sensor, unit, inclusion rule, numerator, denominator, window, where given), the access gap, and a decision: **reader update**, **candidate measurement**, **context only** or **inaccessible**. Attempts, successful compromise, preventive action and defensive AI use stay separate; speed or automation is not evidence of attacker AI use. A cumulative provider count is reported as such with its missing denominator, never as a rate. The pass stops after the six searches and at most eight pages, whatever they show.
