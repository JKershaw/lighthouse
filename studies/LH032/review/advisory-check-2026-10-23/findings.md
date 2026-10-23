# Late advisory check, 23 October 2026

Observed 20:34:29–20:34:50 UTC, separately from the original 18:50 list read. Four unique GETs, 464,810 retained response bytes, no retries, no prefix truncation. [Read log](read_log.json) records actual times, response hashes, final URLs and errors; bodies are losslessly compressed with gzip. The status of a page is an access result, not its claim's truth.

## Selection deviation

[The pre-read plan](../plan.md) specified the first five advisory-linked entries in the list's case-insensitive alphabetic order: aaPanel, AWS Elastic Beanstalk, the two Arch packages and BookStack. The one-off collector instead used the source projection's case-sensitive sort. It selected AWS, Arch PHP, Arch php-legacy, BookStack and Bref's Lambda layer entry, sharing four pages. [The selection actually read](selection.json) and [collector actually used](../collect_advisories.py) are retained. **aaPanel was not attempted.** The request ceiling was reached; no replacement request was made. This incomplete check cannot be called completion of the original sample. Bref's issue is an unintended read, retained but not used to validate a product classification. The case-insensitive intended sample remains documented for a separately bounded future check.

## What the scoped pages establish

- **AWS Elastic Beanstalk:** HTTP 200, but the 195-byte body is `Site Unavailable`. No advisory claim is available to this instrument. LH024 had earlier read a substantive body at this exact URL; that earlier result is separate, not a substitute for today's late check.
- **Arch PHP and php-legacy:** one shared readable first-party notice, dated 21 October, says versions before PHP 8.5.12 and php-legacy 8.3.36 are affected by the two original CVEs and urges upgrading. This supports the list's stated fix versions at this reading. It does not verify installed package contents or date when these sentences first appeared.
- **BookStack:** one readable first-party notice, dated 21 October and reporting its last update as 23 October 13:00 UTC, says the remedy is updating the hosting PHP runtime and lists PHP's four fixed releases. The list's Fix label is scoped to the dependency/runtime; it does not identify a new BookStack application release that independently repairs PHP. The notice also discusses the related session-upload-progress advice and says BookStack does not appear to set the relevant conditions. This is newly seen context for this session, outside LH030's fixed panel; do not add it to that panel or count it as an independent diffusion observation. No reader-account revision is made here.
- **Bref:** the unintended GitHub issue request returned HTTP 200. Its contents were not classified for this audit and no claims rely on it.

The late check supplies support for three sampled entries from two distinct readable notices, one intended entry is inaccessible and one unattempted. These outcomes do not estimate the accuracy of the full list, a patch uptake rate, avoided compromises or attacker AI use. The source types 202 entries as carrying an advisory URL; that metadata count remains distinct from the pages checked here.
