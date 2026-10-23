# LH031: When, if ever, does CISA's catalogue of known exploited vulnerabilities list the October 2026 PHP flaws?

**Protocol 0.1, fixed 23 October 2026, before this study's first read of the catalogue.** Writer: a Claude Code driving session (Claude Opus 5.5). A candidate from the PHP discovery pass (notes/php-discovery-2026-10-23/ledger.md).

## Question and unit

For CVE-2026-109618, CVE-2026-109619 and CVE-2026-115560, does CISA's Known Exploited Vulnerabilities catalogue list each, and if so with what `dateAdded`, `dueDate`, `knownRansomwareCampaignUse`, `requiredAction` and notes? The unit is one CVE at one read. The catalogue is an agency's classification: an entry says CISA judged there to be reliable evidence of exploitation, by its own criteria; it is not a count of attacks, a measure of compromise or a statement about any named system, and an absence is not evidence that no exploitation occurred.

## What is already known of the outcome

SOCRadar's page, read on 23 October at 17:08 UTC (notes/php-discovery-2026-10-23/pages/socradar.raw), says that as of 23 October neither of the first two CVEs is in the catalogue and that CISA said on 21 October it had not observed exploitation. Two search-tool summaries on 23 October said the same, without a source opened. No read of the catalogue itself has been made. CISA's alert page refused this container's direct reader on 22 and 23 October (HTTP 403, LH024).

## Reads

One GET per read of CISA's published feed, `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`. If it refuses or returns something that is not the catalogue, one GET of CISA's own mirror of the same data, `https://raw.githubusercontent.com/cisagov/kev-data/main/known_exploited_vulnerabilities.json`, recorded as the mirror, never merged with the first as if they were one source. Retain the raw body up to 16 MiB with UTC times, status and SHA-256, and extract the feed's `catalogVersion`, `dateReleased`, `count` and the three CVEs' entries if present. Schedule: a first read on 23 October, then once a UTC day through 30 October alongside LH030, then on LH030's Monday and Thursday reads until 30 November 2026. A missed read stays missed. No search, login, paid service or contact.

## Clocks and comparison

An entry's `dateAdded` is CISA's date (a day, not a time); the feed's `dateReleased` is its own clock; Lighthouse's first read showing an entry bounds its appearance from our side. Never substitute one for another. The comparison: which of the three is added, on which date relative to PHP's notices (20, 21 and 23 October) and to the first public exploitation claims (Amazon, Cloudflare; LH028), stated as a sequence of differently sourced clocks, not as a delay to be generalised.

## Stopping and inconclusive

Stop at 30 November 2026. Inconclusive if both addresses refuse at most reads. Spend: about two requests a read; model spend in the close-out.
