title: PHP watch: daily log
kind: working log (unreviewed records, not a released piece)
date: 2026-10-23

# PHP watch: daily log

A few plain lines a day on what the fixed PHP panels saw, newest first, each linking the day's checkpoints. These are working records: what a source said and when Lighthouse read it, not reviewed findings. Anything that would change [the public account](../articles/php-emergency-first-reading.md) is flagged here and goes through review before it reaches that page. How the watch runs is in [the continuation plan](php-watch-continuation-2026-10-23.md).

## 26 October 2026

- **How the 23 October instruction travels:** no change; no tracker holds a record for CVE-2026-115560 at 06:34 UTC ([LH030](../studies/LH030/checkpoints/2026-10-26.md)).
- **CISA's catalogue:** no change; none of the three CVEs listed ([LH031](../studies/LH031/checkpoints/2026-10-26.md)).
- **Products embedding PHP:** the Dutch NCSC's list changed for the first time since 23 October, in commits early this morning, one titled "Verify eligible PHP products against official public advisories". It now has 752 entries; for CVE-2026-109618, 119 record a fix (109 yesterday), 216 vulnerable (222), 378 under investigation (389) and 38 not vulnerable (30). Still no column for CVE-2026-115560. A check of the same five sampled entries found each still supported by its vendor's page ([LH032](../studies/LH032/checkpoints/2026-10-26.md)).
- **Institutions:** no change in any exposed field ([LH024](../studies/LH024/checkpoints/2026-10-26.md)).
- **How far the fix has reached, by others' counts:** by Censys's classification, on 25 October (day 4) 48 per cent of version-reporting services were counted patched in 8.2, 48 in 8.3, 63 in 8.4 and 75 in 8.5, each up one to two points on the day before; 23.6 million services, 55 per cent of those reporting a version, run branches PHP did not fix. Censys revised no earlier day. W3Techs, which visits each website about once a month, now shows 3 to 8 per cent of sites on the fixed releases ([LH033](../studies/LH033/checkpoints/2026-10-26.md)).
- **Media sweep, 06:30 UTC:** no new coverage; all 56 results repeat earlier ones, so no page was opened ([sweep](php-media-sweep/2026-10-26T0630Z.md)).
- **Flagged for review:** nothing.
- **Images, 12:36 UTC:** a partial read; Docker's registry refused it on the first manifest. The one tag read through Docker Hub's tag page, `wordpress:php8.2-apache`, is unchanged ([LH025](../studies/LH025/checkpoints/2026-10-26.md)). Trackers and CISA: no change (Ubuntu's record timed out).
- **PHP, 18:34 UTC:** PHP's news page has a new item dated 26 October, "Updated PHP Windows builds for Brotli security fix": Windows packages 8.5.12-1, 8.4.27-1, 8.3.36-1 and 8.2.35-1 bundle Brotli 1.2.1, which fixes CVE-2026-111497, a flaw PHP says is reachable through cURL only when automatic response decompression is turned on; the PHP runtime versions are unchanged. It does not concern CVE-2026-115560 or the October flaws, and is not PHP's next regular release. Not flagged ([LH030](../studies/LH030/checkpoints/2026-10-26.md)).

## 25 October 2026

- **How the 23 October instruction travels:** no change; no tracker holds a record for CVE-2026-115560 at 00:33 or 06:33 UTC ([LH030](../studies/LH030/checkpoints/2026-10-25.md)).
- **CISA's catalogue:** no change; none of the three CVEs listed ([LH031](../studies/LH031/checkpoints/2026-10-25.md)).
- **Products embedding PHP:** no change; the Dutch NCSC's list has had no edit since 23 October 12:50 UTC ([LH032](../studies/LH032/checkpoints/2026-10-25.md)).
- **Institutions:** no change in any exposed field ([LH024](../studies/LH024/checkpoints/2026-10-25.md)).
- **Media sweep, 06:30 UTC:** no new coverage; the same 56 results as the evening before, so no page was opened ([sweep](php-media-sweep/2026-10-25T0630Z.md)).
- **Images:** the daily read moves to 12:33 UTC from today.
- **Flagged for review:** nothing.
- **New, 08:55 UTC: how far the fix has reached, by others' counts.** A new study, [LH033](../studies/LH033/brief.md), fixed before its first read at the keeper's request, follows Censys's public count of internet-facing PHP services and sets it beside the Python download and pin curves. By Censys's classification, the share of version-reporting services counted as patched by 24 October (day 3) was 46 per cent in 8.2, 46 in 8.3, 62 in 8.4 and 73 in 8.5; about 23.5 million services, over half of those reporting a version, run branches PHP did not fix at all. These are floors: distributions that backport the fix keep reporting the old version, and a service counts as patched only after a rescan. W3Techs, which visits each website about once a month, shows 2 to 6 per cent of sites on the fixed releases so far ([checkpoint](../studies/LH033/checkpoints/2026-10-25.md)).

  ![A line chart and a bar, redrawn with each daily read. The line chart shows, by days since release from 0 to 30, the share of internet-facing PHP services in each fixed branch that Censys counts as patched, beside an orange band for four Python security fixes' share of downloads and a dashed line for the median over 37 Python libraries. The bar splits the PHP services that reported a version on the latest completed day into patched, not yet patched, and on branches with no fix. The chart's own description gives the figures.](../studies/LH033/figure.svg)

  A working chart, unreviewed, redrawn with each daily read; the two sides measure different things (services as last scanned; downloads in a day).
- **Images, 12:34 UTC:** a partial read; Docker's registry rate-limited it on the fourth tag. The three WordPress and Drupal tags read name the same fixed-version images as on 23 October; Nextcloud's apache tag was pushed again at 19:50 UTC on 23 October with the same image ([LH025](../studies/LH025/checkpoints/2026-10-25.md)). Trackers and CISA: no change.

## 24 October 2026

- **How the 23 October instruction travels:** no change. No vulnerability tracker yet holds a record for CVE-2026-115560 (Ubuntu's timed out this morning); CERT-EU and Cloudflare say what they said yesterday ([LH030 checkpoint](../studies/LH030/checkpoints/2026-10-24.md)).
- **CISA's catalogue:** no change; none of the three CVEs listed, catalogue released 23 October 19:30 UTC ([LH031 checkpoint](../studies/LH031/checkpoints/2026-10-24.md)).
- **Products embedding PHP:** no change; the Dutch NCSC's list has not been edited since 12:50 UTC yesterday. A check of five sampled entries found each supported by a readable first-party notice ([LH032 checkpoint](../studies/LH032/checkpoints/2026-10-24.md)).
- **Images:** a partial read; Docker's registry rate-limited both image studies after a few requests. The tags still readable through Docker Hub's tag pages were unchanged ([LH025](../studies/LH025/checkpoints/2026-10-24.md), [LH019](../studies/LH019/checkpoints/2026-10-24.md)).
- **Institutions:** AWS's bulletin, revised 23 October 13:30 PDT by its own field, now names affected Amazon EMR releases; Google's blog added guidance from Mandiant. Neither mentions the newer flaw ([LH024 checkpoint](../studies/LH024/checkpoints/2026-10-24.md)).
- **Media sweep, 08:30 UTC** (the first; [sweep](php-media-sweep/2026-10-24T0830Z.md)), all wire and trade reports of 21 and 22 October, not read at their primary sources:
  - IT-Connect reports that the PHP Foundation said the underlying problem was flagged in a 2024 Quarkslab audit and left unfixed, calling it "a structural failure".
  - Reuters reports precautionary shutdowns: German federal sites (ITZBund, "purely preventive", no incidents known), French prefecture sites, Dutch sites including Overheid.nl and the Port of Rotterdam, and Finland's Valtori, which said it had found no attempt to exploit the flaws.
  - Reuters reports that, by Censys's count, about 1.5 million of 2.6 million hosts reporting a PHP version run one with no fix.
  - Reuters reports that Belgium's foreign ministry temporarily took its websites offline "following reports of cyberattacks exploiting the PHP vulnerabilities", while Belgium's cybersecurity centre said it "had not recorded any attacks on Belgian websites".
  - Reuters reports that tech firms warned some hackers were already exploiting the flaws; the sentence names no firm. Cloudflare (seeing early attacks) and Australia's cyber agency (not aware of active exploitation) are named in the same coverage.
  - Nothing found on the newer flaw, CVE-2026-115560.
- **18:33 UTC:** Google Cloud's bulletins page added GCP-2026-072 (published 24 October): it says the original two flaws affect Drupal-based Apigee developer portals that customers deploy, and no other Apigee product ([checkpoint](../studies/LH030/checkpoints/2026-10-24.md)). Trackers and CISA unchanged; the evening media sweep found no new coverage ([sweep](php-media-sweep/2026-10-24T1830Z.md)).
- **Flagged for review:** nothing.

## 23 October 2026

- **PHP's own notice** of a further, separately numbered flaw (CVE-2026-115560) was retained at 17:00 UTC; the public account gained a reviewed later-evidence notice ([LH029](../studies/LH029/LH029.md)).
- **How that instruction travels** ([LH030 baseline](../studies/LH030/LH030.md)): no vulnerability tracker yet has a record for it; CERT-EU's advisory repeats the instruction, citing a news article; Cloudflare links PHP's notice.
- **CISA's catalogue** of exploited vulnerabilities lists none of the three CVEs ([LH031](../studies/LH031/LH031.md)).
- **PHP-related inventory entries**, by the Dutch NCSC's list: 751 entries, 109 with a recorded fix, 389 still under investigation ([LH032](../studies/LH032/LH032.md)).
- **Images:** both Nextcloud tags were rebuilt at 16:54 UTC, still on PHP 8.5.12 ([checkpoint](../studies/LH025/checkpoints/2026-10-23.md)).
- **Institutions:** AWS's bulletin 2026-143-AWS is new and readable; Google's blog adds a second claim about AI's role in the defence, a candidate for the account's next reviewed revision ([checkpoint](../studies/LH024/checkpoints/2026-10-23.md)).

- **Measurement check:** independent review of LH032 confirms the status totals, corrects link coverage to 749 entries and changes the list-edit clock to mainline commits; the apparent pre-release resolved entry is withdrawn. [Audit and limits](../studies/LH032/LH032.md#measurement-audit-23-october).
