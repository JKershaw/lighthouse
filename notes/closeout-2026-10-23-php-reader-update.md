title: Close-out of the drive of 23 October 2026, evening: PHP's own notice, the reader update, a discovery pass and LH030
kind: close-out
version: 0.1
date: 2026-10-23
authors: a Claude Code driving session (Claude Opus 5.5)

## What was learned

- **PHP's own words.** PHP's news page, read at 17:00 UTC (studies/LH029), suggests `session.upload_progress.enabled=0` until the next regular bugfix release "to fully protect from an unlikely RCE vector", CVE-2026-115560, which by PHP's account needs a configuration storing sessions as `php_binary` or `php_serialize` and code that switches to `php` at runtime before `session_start()`, with upload progress on. It names no version. Observation.
  - That the 21 October releases do not close the path is an inference from PHP's advice; Cloudflare states it outright. Interpretation, labelled as such on every surface.
  - PHP's `datetime` stamp (10:12 UTC) is not a publication time: the 21 October entries carry stamps hours before the release they announced. Derived from two retained copies.
- **How the instruction is carried, at one read** (studies/LH030, baseline 17:15 UTC). No structured vulnerability record yet held the CVE. CERT-EU's advisory, at version 1.2, carried the instruction with "and restart every worker" added, a general qualification in place of PHP's condition, and a news article, not PHP, as its source. Cloudflare linked PHP's notice and stated the version scope PHP left implicit, without the instruction. Observations; no timing follows from one read.
- **Discovery** (notes/php-discovery-2026-10-23/). Six fixed searches and two first-party pages gave no reader update. They gave two bounded candidates: CISA's catalogue entries with their dates, and a vendor-appliance advisory panel. A plain-language query found far more than one naming the CVE identifiers. Observation about one search tool on one evening.

## What changed in the current account

- The PHP account went to version 1.1 with a dated "Later evidence" notice, a caption note, a "What changed after 22 October" list and a longer summary; the short form gained a notice. The front page, the investigation page, programme.md, observations.md and AGENTS.md say the same at the same certainty. No correction to version 1.0.
- Reviews: evidence (notes/R-0032-php-later-evidence.md), reader and inference (R-0033), and one recheck of the resolutions (R-0034); releases.md has the line. The branch waits for the keeper's merge, as the continuation plan asks, rather than being put on main by the session.

## What remains uncertain

- Whether PHP's advisory, promised with the next regular release, confirms the implied scope.
- When the notice became public: the interval is from 06:24 UTC on 22 October to 17:00 UTC on 23 October on Lighthouse's side.
- How many applications switch the session serialise handler at runtime. Nothing here can count it.
- Whether the institutions said anything beyond their fixed URLs.

## The next outward question

LH030 continues: one read a UTC day through 30 October, then Mondays and Thursdays until two days after PHP's next regular release, by 30 November. Its records will show whether the trackers' affected and fixed fields bear out the inference. LH024's and LH025's daily reads for 23 October and LH028's slots after 16:06 UTC were not made in this session; they resume under their own protocols, and a missed slot stays missed.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens` and `harbour/hb drivercost`: the driving session $8.89 to 17:34 UTC, before this close-out's commit (incomplete by the turns after it); subagents $6.94 (evidence review $2.96, reader-and-inference review $2.08, recheck $1.90). About $15.83 in all, within the bound of about twenty dollars. Requests to public services: 22 GETs for the reads (one for LH029, two in the discovery pass, nineteen for LH030's baseline), seven for the feasibility check and one live reread by the evidence reviewer, plus six searches.

**Later the same evening:** the evening's extra work (LH024's and LH025's 23 October reads, LH031, LH032, the Google classing) took the driving session to about $16.41 by 19:00 UTC; with the review agents' $6.94, about $23.35, over the bound of about twenty dollars. The keeper waived the bound for this session, given the significance of the PHP event. The daily runs that wake this session from 24 to 30 October also come under that waiver; each records its own spend in its commit message.
