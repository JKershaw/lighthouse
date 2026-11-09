# LH039: After WordPress fixed CVE-2026-119977 on 28 October 2026, how fast did the public views of WordPress's installed base move to the fixed releases?

**In short** (added 8 November 2026; not part of the protocol). WordPress fixed a flaw in its own update process on 28 October 2026, in 7.1.4 and in a release on every branch back to 4.7, and CISA listed it as exploited on 3 November. WordPress.org's own statistics only count branches, so they can't tell a fixed site from an unfixed one; we watch two views that do see releases, W3Techs's survey of websites and Packagist's count of developer downloads, each counting something different, with WordPress.org's branch figures as context. Reads are daily until 21 November, with a checkpoint on 14 November and a record after the last read.

**Protocol 0.1, fixed 8 November 2026, before any outcome value in this study's reads was looked at.** Writer: the driving session of the scheduled run 2026-11-08T1410Z (Claude Code, Claude Opus 5.5). Proposal P-0017, started by the keeper on 7 November 2026. Investigation: [Where software updates go](../../investigations/software-updates.md). The [collector](scripts/collect.py) and the [Packagist reader](scripts/packagist.py) are committed with this brief and fix every URL. What was read before the brief is in [before-the-brief.md](before-the-brief.md).

## Question

CVE-2026-119977 is a time-of-check time-of-use race in WordPress core's full-package upgrade: by the CVE record (CNA Wordfence), an unauthenticated attacker can execute code "during the upgrade window", through "predictable, web-accessible staging paths". WordPress released fixes on 28 October 2026 for all 25 affected branches, 4.7 to 7.1. The question: **from the release, how did the share of WordPress sites on a fixed release move, within each of the branches 7.1, 7.0 and 6.9, as W3Techs's survey of websites reports it; and how did Composer downloads of WordPress core move to the fixed releases, as Packagist reports them?** The two views count different things and are reported apart.

## What is already known of the outcome

- **Before this brief** ([before-the-brief.md](before-the-brief.md), 7 November): WordPress.org's statistics endpoint has one key per branch and none per release; the fix went to every affected branch; the version-check API offers automatic updates to 25 releases; the release post says sites that support automatic background updates update automatically. Raw reads were kept on 7 November (14:18 UTC) and 8 November (14:11 UTC) with their outcome values unlooked at.
- **Read on 8 November while writing, outcome values not looked at:** WordPress.org's download counter is per branch (its script calls `/wporg/v1/core-downloads/<branch>`), not per release, so it cannot measure the fix either. W3Techs's 7.1 page links patch-level pages 7.1.0 to 7.1.5; WordPress has published no 7.1.5 (its stable-check API marks 7.1.4 "latest" on 8 November), so the 7.1.5 label is unexplained and is reported as W3Techs gives it. Packagist's per-version stats for roots/wordpress 7.1.4 return a daily series (18 labels from 20 October, keys and labels only printed). The probe bodies were not kept.
- **KEV**, read 8 November about 14:30 UTC (catalogue version 2026.11.06): CVE-2026-119977 added 2026-11-03, due 2026-11-06, ransomware use "Unknown", forensic triage "Yes". The listing links WordPress's and Wordfence's pages and no exploitation report; it is not a claim by Lighthouse that any site was attacked.
- **The writer's expectation**, from general knowledge of WordPress and not read for this brief: WordPress has applied minor and security releases automatically by default since version 3.7, so most sites that can update themselves should be on the fixed release within days; W3Techs's sampling, in which each site is visited about once a month (LH033), should make its view lag far behind that. Reported attack counts (Wordfence, relayed by the sweep's scout) are not read here and do not enter the study.

## Population and unit

- **W3Techs view:** websites in W3Techs's survey whose content management system it detects as WordPress, within each branch 7.1, 7.0 and 6.9. Unit: a branch at a read. These three branches are the ones whose releases W3Techs's pages list and that WordPress's stable-check marks "latest" or "outdated"; older branches are context only.
- **Packagist view:** Composer downloads of the packages roots/wordpress and johnpbloch/wordpress-core, the two most used Composer packagings of WordPress core, per version per day. Unit: a branch on a day. A download is a fetch by a developer or a build system, not a site updating itself, which is the channel this flaw lives in.
- **Context:** WordPress.org's branch shares (`api.wordpress.org/stats/wordpress/1.0/`), whose population is sites that contact WordPress.org, and WordPress.org's per-branch download counters.

## Events and clocks

- **E0**, the fix: "WordPress 7.1.4" in WordPress's release feed, 2026-10-28T17:13:02Z. Days since E0 are counted in whole UTC days from 28 October (day 0).
- **E1**, the CVE record's publication, 2026-10-31T05:33Z.
- **E2**, the KEV listing, 2026-11-03 (dateAdded, a day without a time).
- **E3**, any later release on branches 7.1, 7.0 or 6.9 (by the stable-check and version-check APIs and the release feed); none by 8 November. WordPress 7.2 is planned for 8 December, after the window.
- Lighthouse's clock for a change in a value is the interval between the last read without it and the first read with it. W3Techs's own page date (it says its reports are updated daily) is recorded where shown; a W3Techs value that does not change between reads is not evidence that sites did not move.

## Measures

1. **W3Techs fixed share within a branch**, at each daily read, for 7.1, 7.0 and 6.9: the share of websites W3Techs gives for the fixed release and any later release of that branch, divided by the sum of the shares it gives for every release of that branch. Values given as "less than 0.1%" are carried as bounds, and the ratio is reported as a range. Also each release's share as given, and W3Techs's monthly history points from the history pages where published (1 November; 1 December falls after the window).
2. **The comparison named in advance:** the W3Techs fixed share on 7.1 at the read nearest day 14 after E0 (11 November) and at the last read (21 November, day 24), beside LH033's W3Techs patched share for PHP's branches at the same days since PHP's fix of 21 October (from LH033's reads, reused and disclosed). Same instrument, two kinds of server software: WordPress updates itself, PHP mostly does not. A difference is a description; no cause is claimed.
3. **Packagist fixed share within a branch**, per UTC day from 14 October to the day before the read, for each package and branch: downloads of the fixed release divided by downloads of all releases of that branch that day. Reported: the series, the first day the fixed release took half of its branch's downloads, and the share on the day before each checkpoint. Read at the checkpoints only, because Packagist keeps the history.
4. **Context:** WordPress.org's branch shares at each read, including the summed share of branches below 4.7 (not affected, by the CVE record) and of 7.1, 7.0 and 6.9; the daily increments of the per-branch download counters, described as downloads of that branch's package, with whether automatic updates are counted classed as unknown.
5. **Supply:** at each read, the release each branch's stable-check and version-check entries name, so that any E3 is caught.

## Missing evidence

A failed read is a missing day, recorded with its status; it is not zero and not "no change". A W3Techs page without a row for a release counts that release as not listed, not as zero sites. If the 7.1.5 label resolves to a release WordPress publishes, it counts as fixed; while it does not, its share is reported separately and left out of both numerator and denominator, and the record says so. No source here sees whether a site's update completed, or whether a site was exposed or attacked during it.

## Overlap

LH033 uses W3Techs for PHP over the same weeks; its values are reused only for the comparison in measure 2, and the record says so. No other study reads WordPress. The raw reads of 7 and 8 November were made before the brief, by the same URLs, and are this study's first two days.

## Resources and stop

About 20 GETs a day by the collector (WordPress.org, W3Techs, Packagist), and 52 Packagist GETs at each checkpoint. No login, paid service, scan of any host, or contact with anyone. W3Techs is quoted with a dated reference and a link, as its terms require. The last daily read is on 21 November 2026, 14 days after the first, as the throttle sets for an urgent watch unless the keeper extends it. A later release on a watched branch (E3) does not stop the reads; it is recorded, and "fixed" then means 7.1.4, 7.0.8 or 6.9.11 or later.

## What would leave it inconclusive

If W3Techs's shares within the branches do not move over the window, the record says its sampling cannot resolve a fortnight and gives the monthly points instead; if more than four daily reads fail, the W3Techs series is reported as partial. Packagist's view answers a different question (developers and builds) and does not stand in for sites.

## Schedule

- Daily reads, 9 to 21 November: `python3 studies/LH039/scripts/collect.py --read <label>`, labelled with the UTC minute the collector starts.
- Checkpoint 1, 14 November (window 14 to 15 November): `scripts/packagist.py --read <label>`, measures 1 to 5 on the reads so far, `checkpoints/2026-11-14.md`.
- Checkpoint 2, 21 November (window 21 to 22 November): the same, with measure 2.
- Record, 22 to 29 November: `LH039.md`, with Answer, Findings, Method, Limits, Next and Corrections; a piece only if the record earns one.

## Amendment, 9 November 2026: the keeper's robots.txt rule

By the scheduled run of 9 November 2026 (in force from that day's read; not retroactive). The keeper decided on 8 November 2026 that Lighthouse obeys robots.txt as its own agent and as whatever runs it (AGENTS.md, Rules that matter; scripts/robots_rules.py, scripts/robots_tokens.json). The collectors (collect.py, packagist.py) now import `urlopen` from scripts/lh_fetch.py, which asks scripts/robots_gate.py before each request: each host's robots.txt is read once per run, and a URL it disallows, or whose robots.txt cannot be read, is not requested and is logged "NotFetched" with the deciding group and rule, a missing reading and never a negative. The User-Agent now carries Lighthouse's token (`Mozilla/5.0 (compatible; Lighthouse-research/1.0; +https://lighthouse.harbour.cat)`), and email addresses are withheld from kept bodies (the fetch log keeps the hash of the bytes received). Whether a site's robots.txt allowed this study's earlier requests was not checked here; those requests are for the rules-of-the-road re-audit (studies/LH047, row LH047-reread). api.wordpress.org's robots.txt, as read at 14:31 UTC on 9 November (HTTP 200), disallows every path to every crawler, so WordPress.org's statistics and version-check endpoints are not fetched from that read on: the measures that rest on them are missing from 9 November, not negative. What that does to the study's question is for checkpoint 1 (14 November) to say, without changing the question, the measures or the pre-set reading; W3Techs and Packagist reads go on.
