# Third-party trackers of PHP version uptake and exposure: how each measures

Discovery pass, 25 October 2026, 08:38 to 08:52 UTC. Written by a subagent on Opus 5.5 for Lighthouse. Scope: methodology, granularity, cadence and access only. No figure for PHP 8.x versions, the fixed releases (8.5.12, 8.4.27, 8.3.36, 8.2.35) or CVE-2026-109618, CVE-2026-109619 and CVE-2026-115560 observed or dated after 20 October 2026 is recorded here. Where a fetch would have shown such figures, it was made with digits masked, or keys only, or with a prompt that excluded figures. Nothing was saved to the repository; one temporary file in the scratchpad (a Debian rules file that turned out to be a challenge page) was deleted. Searches kept out of `harbour/.session/`; no environment keys read.

Kinds of statement: everything below is observation of a source's own description unless marked "inference" (mine) or "not checked".

## Summary table

| Source | Runs it | Population and unit | Version detection | Granularity published | Cadence | Pre-21 Oct history retrievable | Anonymous fetch from container (HTTP, UTC) | Bears on long tail |
|---|---|---|---|---|---|---|---|---|
| Censys PHP2Shell dashboard (php2shell.censys.com, JSON at /api/data) | Censys ARC | Internet-facing PHP services (IP or hostname plus port); hosts and web properties in the advisory's queries | Version the service reports in scan responses; detection method not described; honeypots reporting never-released versions excluded | Patch (versions such as 8.x.yy), with "affected", "patched", "unknown" statuses and branch distance from the fix | Hourly; one bar per UTC day, final at midnight UTC | No: tracking since 21 October 2026; a Wayback snapshot of 22 October exists | 200 (08:46 to 08:47) | Yes: "one release behind, 2 to 4 behind, 5 or more behind" per branch, plus branches with no fix |
| W3Techs PHP version pages | Q-Success DI Gelbmann GmbH | Websites (pay-level domains, subdomains folded, redirects excluded) in a sample of "well over 20 million sites"; denominator is sites whose server-side language is known, and within a minor, sites on that minor | Not stated for versions; HTTP headers are among indicators; inference: X-Powered-By | Minor on /pl-php/8; patch within each minor on /pl-php/8.N (confirmed format on 7.4) | Reports updated daily; each site visited "approximately once a month" | Monthly points (1st of month) free on history pages, plus current day; daily values not kept publicly; no Wayback snapshot found | 200 (08:40) | Yes, patch rows within a minor; but monthly crawl lags |
| WordPress.org stats API (api.wordpress.org/stats/php/1.0/) | WordPress.org (Automattic hosted) | WordPress installs that pinged api.wordpress.org update checks "within the last few months" | Core sends full PHP_VERSION in every version check (wp-includes/update.php) | Minor only (keys 4.4 to 8.6) | Daily (Expires header next day 01:00 GMT) | Wayback snapshot of 27 Sep 2026 for API, 16 Oct 2026 for stats page | 200 (08:42) | Only at minor level |
| Packagist PHP statistics (packagist.org/php-statistics; per package /packages/V/P/php-stats.json) | Packagist (Private Packagist, Jordi Boggiano) | Composer package installs logged at packagist.org; a CLI on developer machines, CI and build hosts, not web servers | Composer User-Agent carries PHP major.minor.release (no distribution suffix), Platform-PHP and a CI flag | Minor (5.3 to 8.5), daily and monthly; per-package by package version | Daily | Yes: the embedded daily series runs from 18 May 2021 | 200 (08:43) | Minor only; flow of installs, not running stock |
| Shadowserver public dashboard and reports | The Shadowserver Foundation | Scanned IPs, aggregated to country level; full IP-level reports to vetted subscribers (CERTs, network owners) | Not described on pages read; "Vulnerable HTTP" report tags hosts with a potential vulnerability by CVE tag | Country-level counts per tag; version facets not documented | Daily scans | Rolling two years on the dashboard (2022 post) | Dashboard: connection closed (curl, 08:40) and 503 (WebFetch); reporting pages 200 | Only if a CVE tag exists; none found for these CVEs |
| CybelAngel php2shell article | CybelAngel | Secondary: Shodan banner counts published by Mallory (20 Oct), plus Infrawatch services, CybelAngel's own post-release scan, WordPress.org stats via The Repository, mySites.guru monitoring | Banners for the Shodan counts; others not described | Branch level in what it relays | Article "will keep updating" | It is itself dated 20 to 21 Oct | Not tried by curl; WebFetch 200 (about 08:47) | Partly, via relayed counts |
| BuiltWith trends (trends.builtwith.com/framework/PHP) | BuiltWith | Websites, with top 1m, 100k, 10k bands | Not stated | Major (PHP-7, PHP-8 pages) publicly; lists paid | Not stated | Not checked | 200 with gzip (08:48); WebFetch got a verification screen | No |
| Wappalyzer (wappalyzer.com technologies page) | Wappalyzer | Websites | Not stated | No version breakdown public | Not stated | Not checked | 200 (08:40) | No |
| Censys and Shodan search | Censys, Shodan | Scanned hosts and services | Banners | Patch where banners show it | Continuous | Account needed for history (not checked) | 403 from Cloudflare (08:40) | Yes in principle, not anonymously |
| Homebrew analytics (formulae.brew.sh/api/analytics/...) | Homebrew | Install events on macOS and Linux Homebrew with analytics on | Formula name: php (newest minor), php@8.4 ... php@7.4 | Minor via formula; no patch | Rolling 30, 90, 365 day windows | Wayback snapshot of 12 Aug 2026 for the 30d file | 200 (08:49) | No |
| Debian popcon (popcon.debian.org) | Debian | Machines with popularity-contest installed, reporting weekly | Package name only (php8.2, php8.4 ...); report format has no package version | Minor via package name | Daily publication of weekly reports | Not checked | Front page 200; qa.debian.org per-package page 403 (08:40) | No |
| Ubuntu popcon (popcon.ubuntu.com) | Canonical | None now: page shows only "Thanks!" | n/a | n/a | n/a | n/a | 200, empty (08:49) | No |
| Docker Hub (hub.docker.com/v2/repositories/library/php/) | Docker | Pulls of the official php image | Repository pull_count; tags carry tag_last_pulled time, no per-tag count | Repository total only | Continuous | No | 200 (08:49) | No |

## Notes by source

### Censys PHP2Shell dashboard
- URLs opened: https://censys.com/php2shell/ (WebFetch about 08:46), https://php2shell.censys.com/ (curl 08:46:44, text read with every digit masked), https://php2shell.censys.com/api/data (curl 08:47:11, keys, dates and the tracking start only), https://php2shell.censys.com/static/app.js (notes strings, digits masked), https://censys.com/advisory/cve-2026-109618-cve-2026-109619/ (WebFetch about 08:47, methodology prompt).
- Advisory published 21 October 2026, updated 22 and 23 October. Queries it publishes: `(host.services.software: (vendor="php" and product="php")) and not labels:"HONEYPOT"` and the same on `web.software`. Host and web property totals are not additive. CVE-2026-115560 is not mentioned; the data's `cve` block lists only the two October CVEs and the four fixed releases.
- The dashboard's own notes, verbatim in substance: figures update hourly from scans and a daily internet snapshot and "can lag real-world changes by hours, and by up to about a week for some websites"; totals may shift as detection improves; "Status is based on reported versions, so counts are an upper bound. Linux distributions often backport security fixes without changing the PHP version"; services that hide their version are counted as unknown, not affected or patched; "Patched" means a service seen on an affected version and later on a fixed one; "Counts are services, not organizations or machines"; per-minute live chart counts scan responses, "so a service scanned twice counts twice".
- Series in the JSON: `history` (day, status, targets), `branch_history` (day, branch, patched, targets), `patched_daily`, `top_versions` (patch-level labels), `branch_versions`, `per_minute`. `tracking_since` is 2026-10-21. The JSON holds only the current snapshot with day series since tracking began; whether it keeps all days indefinitely is not stated. A Wayback snapshot of the page exists at 22 October 23:07 UTC (availability API, 08:49); whether it captured the data call was not checked.
- Terms: page links Censys general terms; not read. No licence stated for the dashboard data.

### W3Techs
- Opened: https://w3techs.com/faq, https://w3techs.com/technologies, https://w3techs.com/technologies/details/pl-php/8 (structure only), https://w3techs.com/technologies/details/pl-php/7.4, https://w3techs.com/technologies/history_details/pl-php/7.4, https://w3techs.com/terms_of_use (WebFetch, 08:40 to 08:42); https://w3techs.com/apidoc (curl 08:51). Status only for /pl-php/8.3, /8.5 and /history_details/pl-php/8.3.
- Population: "well over 20 million sites"; relevance rule; subdomains not separate websites; redirected domains excluded. Detection: several thousand indicators incl. HTTP headers; "A fair share of our data is based on such dependencies" (WordPress implies PHP), which gives PHP without a version. Version detection not described. Sites visited "approximately once a month"; reports "updated daily".
- Format, confirmed on PHP 7.4 (old version): patch rows within a minor, as a share of sites on that minor, e.g. 7.4.33 at 93.0 per cent of sites using 7.4 (read 08:41). The history page is monthly (1st of each month, back about a year in the monthly view, quarterly and yearly views also offered), patch rows above 1 per cent, plus a point for the current day.
- Terms: quoting requires a reference with a date and, online, a link. Silent on scraping or rate limits. API is paid (per-request bundles) and returns one domain's technologies, not aggregates.
- Archive: the Wayback availability API returned no snapshot for any W3Techs URL tried, including the home page; the CDX query timed out. Inference, not confirmed: W3Techs may be excluded from the Wayback Machine. Daily pre-event values are therefore probably not retrievable; the monthly point of 1 October 2026 is.
- Biases: header suppression (expose_php off) removes the version; distribution builds report the upstream version (Ubuntu and Sury builds append a package suffix, which W3Techs presumably drops: inference, not checked), so an old patch string may be patched; monthly revisit means a day's figure mixes crawls up to a month old.

### WordPress.org
- Opened: https://api.wordpress.org/stats/php/1.0/ (curl 08:42, keys only), https://make.wordpress.org/meta/2015/03/01/major-update-to-our-version-stats-for-php-mysql-and-wordpress/ (WebFetch about 08:42), https://raw.githubusercontent.com/WordPress/wordpress-develop/trunk/src/wp-includes/update.php (08:42:35). Status only for https://wordpress.org/about/stats/.
- Since 1 March 2015 stats "only reflect sites that have pinged api.wordpress.org within the last few months". Core sends `'php' => PHP_VERSION` (full string, including any distribution suffix) with each version check (about twice a day per the Codex, per a search summary not opened), but the API publishes minor only. Daily refresh. Population is WordPress sites that can reach the API, weighted one per site, with no dedup detail published.

### Packagist
- Opened: https://packagist.org/php-statistics (curl 08:43, labels and series keys only), https://packagist.org/packages/monolog/monolog/php-stats.json (structure only), https://blog.packagist.com/php-versions-stats-2020-2-edition/ (WebFetch about 08:45), https://raw.githubusercontent.com/composer/composer/main/src/Composer/Util/StreamContextFactory.php (08:50:50).
- "Package installations by PHP minor version, daily" and "monthly"; daily labels run 18 May 2021 to 25 October 2026, keyed 5.3 to 8.5. The 2020 post: logs of Composer installs, PHP version from the User-Agent, "CI environments are excluded on a best-effort basis" (whether the live page excludes CI is not stated). Composer's User-Agent carries PHP major.minor.release, so Packagist receives patch level but does not publish it. Brent Roose's twice-yearly "PHP version stats" posts on stitcher.io use Packagist data (search results, not opened).

### Shadowserver
- Opened: https://www.shadowserver.org/what-we-do/network-reporting/ (WebFetch about 08:45), https://shadowserver.org/news/shadowservers-new-public-dashboard (WebFetch about 08:46, post dated 6 September 2022). Dashboard and help pages: curl connection closed by the relay; WebFetch 503.
- Daily internet-wide scans; reports to subscribers; the public dashboard is country-level, no IPs, rolling two years, CVE tags filterable; "you are not permitted to scrape or resell the data", attribution required. No tag for these CVEs found in one search (not confirmed on the dashboard itself).

### Others
- CybelAngel article (WebFetch about 08:47, methodology prompt): relays counts from Mallory (Shodan banners, 20 October), Infrawatch (services, a different method), its own post-release scan, WordPress.org via The Repository, and mySites.guru (live Joomla and WordPress sites it monitors). Discusses backports. Primary pages of Mallory, Infrawatch and mySites.guru not found or opened.
- HackerTarget, https://hackertarget.com/php-end-of-life/: 403 Cloudflare (08:50); not read.
- GreyNoise (viz.greynoise.io 200) measures scanning and exploitation traffic, not version uptake; not examined further. Netcraft: blog reachable (200 after redirect); no PHP version series looked for.
- CIRCL vulnerability-lookup "sightings" appeared in a search; it counts mentions of a CVE, not installed versions; not opened.

## Comparable time series

Lighthouse's Python measure: share of a library's PyPI downloads (a flow of fetches) at the new version, by day after release.

- Censys PHP2Shell is the closest in shape: daily, patch-level, from release day. Unit differs: a stock of internet-facing services as seen by rescans, not a flow; "patched" requires a rescan, so it lags by days; version strings understate patching on distributions that backport (an upper bound on affected); services that hide their version fall outside both affected and patched (the share was not read); no pre-release baseline inside the series.
- W3Techs gives patch-level shares within each minor, but publishes daily values only as the current figure and history monthly; Lighthouse would have to snapshot it daily itself, and each value blends a month of crawls. Unit: websites, not services or downloads.
- Packagist daily is the nearest in unit (a flow of installs, like downloads) but is minor-level only, so it cannot show a patch release; it could show branch migration.
- WordPress.org is daily but minor-level; Homebrew, popcon and Docker Hub are minor or repository level and cannot show patch uptake.
- None found tracks CVE-2026-115560, whose fix is due in the next regular release; a version-based tracker would need the later fixed versions added.

## Searches run (25 October 2026, WebSearch, standard)

1. `api.wordpress.org stats php 1.0 how WordPress PHP version statistics are collected`
2. `Packagist blog "PHP Versions Stats" methodology Composer installs Jordi Boggiano`
3. `blog.packagist.com PHP Versions Stats 2025 edition`
4. `Shadowserver PHP CVE-2026-109618 vulnerable instances scan`
5. `Shadowserver dashboard public statistics vulnerability tag filter product version how to use`
6. `Censys advisory PHP October 2026 exposed instances version`
7. `Censys research WordPress sites PHP version X-Powered-By outdated PHP patch` (censys.com only)
8. `php2shell patch adoption tracker dashboard PHP 8.4.27 servers updated`
9. `mySites.guru PHP version statistics sites php2shell October 2026`
10. `Infrawatch PHP services php2shell exposure tracking`
11. `"PHP" patch adoption daily data emergency release October 2026 researcher time series X-Powered-By scan`

Results not opened: seld.be and other blog.packagist.com editions; stitcher.io posts (July 2024 status only, others not); freek.dev; make.wordpress.org author and 2010 core posts; generatewp.com; meta.trac ticket 8056; SANS ISC IP pages; cve.circl.lu and db.gcve.eu sightings; bsky.app Shadowserver posts; pasqualepillitteri.it; act.globalcyberalliance.org; Shadowserver dashboard help and example-query pages (503); censys.com/blog/wordpress-eol-php/; censys.com/cve-2024-4577/; Censys release notes and webinar; vpncentral.com (403); cycognito.com; invgate.com; instawp.com; wavect.io; lilting.ch; stingrai.io; konfirmity.com; dexpose.io; roic.ai; securityaffairs.com; vulmon.com; computerwoche.de; checkmarx.

## Post-event figures seen (sources only, figures not recorded)

- Search-tool summaries quoting the CybelAngel php2shell article (searches 6, 8, 9, 10, 11): host and service counts and shares by branch, mostly attributed to Mallory's Shodan counts of 20 October, plus a WordPress share and a mySites.guru share whose measurement dates I could not establish.
- A search summary quoting Infrawatch's service and IP counts (search 10), via the same coverage.
- A search summary quoting Censys's "Why Are WordPress Sites Still Running EOL PHP?" post (search 7), date not established, so possibly post-event.
- The Censys dashboard text and JSON were read with digits masked or as keys only; no figure was seen there. W3Techs PHP 8 pages were fetched with prompts excluding figures; none was returned.
