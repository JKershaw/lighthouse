# LH037: the held bodies re-scored under the amended mention count, 12 November 2026

**In short.** After the 12 November read, the study's keyword count was widened so that names built on "PHP", such as "PHP2Shell", prompt a body to be opened. Re-scoring every body kept from the five reads so far finds only one body the old count passed over: D-Link's listing on 12 November, which had already been found by comparing pages. No earlier vendor statement was missed.

This is post hoc: the amended rule was written after the 12 November read, knowing what the old rule had missed, and is tested here on the bodies that showed the problem. It is the [amendment of 12 November](../brief.md#amendment-12-november-2026-the-mention-count-catches-names-derived-from-php) in brief.md. Run offline at 2026-11-12 on the bodies under `data/read-*/` as held in the repository (email addresses already withheld); nothing was fetched. The two route-documentation reads of 2 November (`data/routes-*`) are not reads of the panel and were not re-scored. Writer: a Claude Code subagent of the scheduled run of 12 November 2026 (Claude Opus 5.5), row `LH037-amend-keyword`; unreviewed. The [checkpoint of 12 November](2026-11-12T1416Z.md) and panel.json are unchanged.

## Rules

- **Original** (protocol 0.1): each CVE id counted as written in upper case; `PHP` case-sensitive, whole word (`\bPHP\b`). A body is prompted if any count is above zero.
- **Amended**: `(?i)(?<![a-z0-9.])php`, "php" in any case at the start of a word but not after a dot, so PHP, PHP2Shell, php-fpm, PHP-FPM, php_admin_value and /php/ count and `aphp`, `index.php` and `www.php.net` do not; and each CVE id in any case. Both are in [scripts/mentions.py](../scripts/mentions.py); the collector logs both from the next read, the original under its old keys.

Self-test (`python3 -I studies/LH037/scripts/mentions.py`):

```
mentions.py self-test: 11 caught, 7 not caught, 3 count checks: ok
```

## Re-scoring

Code: [scripts/rescore.py](../scripts/rescore.py). Command: `python3 -I studies/LH037/scripts/rescore.py`. Output (sums of the three CVE ids per body):

```
read-2026-11-01T1420Z: 28 log rows, 28 bodies held, 0 not held; old-rule recount differs from log for 0
  flagged by the amended rule only (old rule: nothing): 0
  whole-word PHP 0 but amended php count > 0: 2
    read_log.json Fortinet fortinet__psirt_rss {'PHP': 0, 'php_prefix': 2, 'cve_exact': 4, 'cve_any_case': 6}
    found_log.json Fortinet fortinet__FG-IR-26-186_csaf {'PHP': 0, 'php_prefix': 1, 'cve_exact': 2, 'cve_any_case': 2}
read-2026-11-02T1530Z: 31 log rows, 31 bodies held, 0 not held; old-rule recount differs from log for 0
  flagged by the amended rule only (old rule: nothing): 0
  whole-word PHP 0 but amended php count > 0: 2
    read_log.json Fortinet fortinet__psirt_rss {'PHP': 0, 'php_prefix': 2, 'cve_exact': 4, 'cve_any_case': 6}
    read_log.json Fortinet fortinet__FG-IR-26-186_csaf {'PHP': 0, 'php_prefix': 1, 'cve_exact': 2, 'cve_any_case': 2}
read-2026-11-05T1414Z: 34 log rows, 34 bodies held, 0 not held; old-rule recount differs from log for 0
  flagged by the amended rule only (old rule: nothing): 0
  whole-word PHP 0 but amended php count > 0: 1
    read_log.json Fortinet fortinet__psirt_rss {'PHP': 0, 'php_prefix': 2, 'cve_exact': 6, 'cve_any_case': 8}
read-2026-11-09T1429Z: 34 log rows, 33 bodies held, 1 not held (fortinet__FG-IR-26-186); old-rule recount differs from log for 0
  flagged by the amended rule only (old rule: nothing): 0
  whole-word PHP 0 but amended php count > 0: 1
    read_log.json Fortinet fortinet__psirt_rss {'PHP': 0, 'php_prefix': 2, 'cve_exact': 6, 'cve_any_case': 8}
read-2026-11-12T1416Z: 35 log rows, 35 bodies held, 0 not held; old-rule recount differs from log for 0
  flagged by the amended rule only (old rule: nothing): 1
    read_log.json D-Link d-link__announcements {'PHP': 0, 'php_prefix': 1, 'cve_exact': 0, 'cve_any_case': 0}
  whole-word PHP 0 but amended php count > 0: 1
    read_log.json D-Link d-link__announcements {'PHP': 0, 'php_prefix': 1, 'cve_exact': 0, 'cve_any_case': 0}
```

## What it shows

- **Derived measurement.** The original count, recomputed on every held body, equals the count each read's log recorded (0 differences in 161 bodies), so withholding email addresses changed no count and the re-scoring stands on the same bytes.
- **Derived measurement.** Per read, bodies prompted by the amended rule and not by the original: 1 November 0; 2 November 0; 5 November 0; 9 November 0; 12 November 1 (D-Link's announcements listing, "PHP2Shell", no CVE id). The D-Link listing scored 0 under both rules at every earlier read, consistent with its statement being published on 10 November.
- **Derived measurement.** Fortinet's PSIRT feed (1, 2, 5 and 9 November; by 12 November the PHP item had aged out of it) and its CSAF file for FG-IR-26-186 (1 and 2 November) score 0 for whole-word "PHP" because they say "PHP2Shell" or use "php" inside an anchor, but they name the CVE ids and so were already prompted; Fortinet's statement was found at the baseline.
- **Interpretation.** The old rule missed no statement before 12 November among the bodies held. The amended rule prompts no body beyond those the original rule or the comparison of bodies already reached, so on these bodies it costs nothing in extra openings; whether it prompts unrelated bodies on routes whose pages change later is not known.
- **Not checked.** Bodies not held: Fortinet's advisory page at 9 November (not requested under the robots.txt gate). Pages the routes never reach. Names for the flaws that share no "php" prefix and carry no CVE id, which neither rule would catch; comparing every body with the read before remains the safeguard.
