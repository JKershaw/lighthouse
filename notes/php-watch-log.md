title: PHP watch: daily log
kind: working log (unreviewed records, not a released piece)
date: 2026-10-23

# PHP watch: daily log

A few plain lines a day on what the fixed PHP panels saw, newest first, each linking the day's checkpoints. These are working records: what a source said and when Lighthouse read it, not reviewed findings. Anything that would change [the public account](../articles/php-emergency-first-reading.md) is flagged here and goes through review before it reaches that page. How the watch runs is in [the continuation plan](php-watch-continuation-2026-10-23.md).

## 25 October 2026

- **How the 23 October instruction travels:** no change; no tracker holds a record for CVE-2026-115560 at 00:33 or 06:33 UTC ([LH030](../studies/LH030/checkpoints/2026-10-25.md)).
- **CISA's catalogue:** no change; none of the three CVEs listed ([LH031](../studies/LH031/checkpoints/2026-10-25.md)).
- **Products embedding PHP:** no change; the Dutch NCSC's list has had no edit since 23 October 12:50 UTC ([LH032](../studies/LH032/checkpoints/2026-10-25.md)).
- **Institutions:** no change in any exposed field ([LH024](../studies/LH024/checkpoints/2026-10-25.md)).
- **Media sweep, 06:30 UTC:** no new coverage; the same 56 results as the evening before, so no page was opened ([sweep](php-media-sweep/2026-10-25T0630Z.md)).
- **Images:** the daily read moves to 12:33 UTC from today.
- **Flagged for review:** nothing.

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
