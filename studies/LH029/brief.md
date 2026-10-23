# LH029: What did PHP's own 23 October notice say about a related issue in the fixed releases?

**Protocol 0.1, fixed 23 October 2026 at 16:59 UTC (commit `a41f896`, pushed 16:59:50 UTC), before this study's direct read of any page it names.** Writer: a Claude Code driving session (Claude Opus 5.5). This is a single-source retention study for a dated reader update to the 22 October PHP account (articles/php-emergency-first-reading.md). It is separate from LH028's fixed three-URL panel and from LH024's daily panel, and changes neither.

## What is already known of the outcome

- **The notice's content, from a reader that kept no bytes.** During the keeper's assessment conversation on 23 October, a web reader opened `https://www.php.net/archive/2026.php#2026-10-23-1`. By the continuation plan's account (notes/php-watch-continuation-2026-10-23.md), PHP's notice says a related issue needs an unusual combination: configuration that initially uses `php_binary` or `php_serialize` as the session serialise handler, application code that changes the handler to `php` at runtime before `session_start()`, and session upload progress left enabled. It recommends `session.upload_progress.enabled=0` until the next regular bugfix release, says users who already applied that mitigation can keep it, says applications that never change the handler at runtime can keep the feature enabled, and says the full advisory for CVE-2026-115560 is planned with the next release. No raw response was retained. These are prior outcomes, not discoveries this study can make.
- **A third party's account of it.** LH028's 23 October 16:00 UTC snapshot retained Cloudflare's revision saying PHP published an informational advisory for related CVE-2026-115560 in the session upload progress feature, affecting fully patched releases including PHP 8.5.12 and expected to be fixed in the next regular release, with a WAF rule that does not cover sites that changed `session.upload_progress.name` (studies/LH028/checkpoints/2026-10-23T1600Z.md).
- **The mitigation's history.** LH024's retained 22 October copy of the same archive page (studies/LH024/data/snapshot-2026-10-22/php_0.raw, read 06:24:43 UTC) holds PHP's 21 October security advisory, which listed `session.upload_progress.enabled=0`, set in php.ini, an FPM pool or server configuration and with every worker restarted, as a partial measure against CVE-2026-109619 for those who could not update at once, saying it "blocks the confirmed session paths but not other variants". This session read that retained copy before fixing this protocol.

## Question and unit

At this study's read, what does PHP's own archive entry for 23 October say about (a) which releases the related issue affects; (b) the conditions under which an installation is exposed; (c) the action it recommends and for whom; (d) when a fix is expected and where the full advisory will appear; (e) how it relates to the 21 October advisories and their mitigation; and (f) its publication clock, at whatever precision the source gives? The unit is one source statement on a PHP project page or a PHP mailing-list message, with its URL, the read's UTC start and finish, HTTP status, byte length and SHA-256. A statement is PHP's claim about its software; it is not an observed exploit, an observed vulnerable deployment or an observed mitigation at any site.

## Reads and bounds

1. One direct GET of `https://www.php.net/archive/2026.php` (the fragment `#2026-10-23-1` is not sent to the server), with the urllib reader and user agent LH028 uses. Retain the bytes up to 1 MiB, the read log and the entry's extracted text.
2. At most two further direct GETs, only of pages the 23 October entry itself links to, chosen in this order: a php.announce message on news-web.php.net for the same notice, because a message carries a Date header and so a finer publication clock; then the first other link in the entry to a php.net or news-web.php.net page that is not the archive itself. Links to github.com are recorded, not read, since github.com's pages refused anonymous reads from this container on 28 September (CLAUDE.md).
3. At most three GETs and 3 MiB retained in total; no search, crawl, login, exploit, probe of any site or paid service. Stop a read at a refusal, placeholder, challenge, rate limit or the ceiling and record it.

An offline replay verifies every retained byte count and hash and re-extracts the entry's text. The archive page is also one of LH024's fixed daily selections; this read is not LH024's daily observation for 23 October and fills none of its cells.

## Classes and missing evidence

Each of (a) to (f) is classed as **stated** (with the quotation), **not stated in the retained bytes**, or **unavailable** (read refused or entry absent). A date heading is a day, not a time; a mailing-list Date header is the message's claimed send time, not proof of first public visibility. Where the retained entry differs from the web reader's account above, the retained bytes govern, the difference is recorded, and the web-reader account is not used as an observation. A notice first read by Lighthouse on 23 October is a newly observed claim, not a newly occurring event.

## The comparison that matters

The reader-facing question is whether "fixed" in the 22 October account needs qualifying: whether PHP itself says the fixed releases (8.5.12, 8.4.27, 8.3.36, 8.2.35) remain exposed to a related issue, under which conditions, and whether the 21 October mitigation is still advised and for whom. This is a comparison of PHP's statements across two retained copies of one page, not a measure of how many installations meet the conditions, which nothing here can count.

## Stopping and what would leave it inconclusive

Stop after the reads above. If the entry is absent, changed beyond the web reader's account, or the read is refused, record exactly that; the reader update then cites only what LH028 retained from Cloudflare, attributed to Cloudflare, and says PHP's own notice could not be retained. Model spend is measured from the transcripts; requests are free.
