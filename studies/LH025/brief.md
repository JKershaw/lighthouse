# LH025: What do selected derived PHP image tags name each day?

**Protocol 0.1 fixed 22 October 2026 UTC before reading this panel's registry tags, except the Drupal tag already read in LH023.** Writer: Codex, GPT-6 Sol in ChatGPT Work Mode. The upstream fixed PHP versions, LH019's four PHP moving tags, LH021's consumer source sample, LH023's current Drupal `10.6-php8.3-fpm` digest and its declared PHP 8.3.36 are prior knowledge. Drupal was chosen with its result known and is not an independent confirmation. The other tags were selected by stable image family and common variant names, before their registry responses were inspected for this protocol. No absent tag is replaced.

## Question and fixed panel

On each UTC day 22–28 October, what linux/amd64 manifest does each of these exact Docker Hub `library` tags name: `wordpress:php8.2-apache`, `wordpress:php8.3-fpm`, `drupal:10.6-php8.3-fpm`, `nextcloud:apache`, `nextcloud:fpm`? For each, retain Docker Hub's tag response, its selected platform digest, platform `last_pushed` and tag `tag_last_pushed`; if present, retrieve that exact OCI manifest and configuration, verify their content digests, and report any declared `PHP_VERSION` and source label. An absent tag, missing amd64 platform, absent configuration, rate limit or inaccessible response stays unknown. Do not substitute a nearby version or variant. The unit is a tag and platform at retrieval, not a deployed site.

## Comparison

Each tag is compared only to its own prior daily observed platform digest and declared version. A changed digest bounds a pointer change between two observations; equal endpoints cannot rule out intervening changes or a reversal. A current PHP_VERSION in a derivative configuration is a publisher declaration, and inherited environment alone does not prove its executable bytes were independently checked. A moving tag's current manifest cannot reconstruct its pre-event digest. Do not compare the five families as if their build schedules or package requirements were the same. A derived tag may change for reasons unrelated to this fix; source and build records would be needed to attribute a change. LH019's corresponding upstream PHP tag snapshots are a separate, overlapping view.

## Bounds and stop

For each labelled UTC date, at most 24 external requests, five OCI manifest GETs, 10 MiB retained bodies and no layers or executable runs. Anonymous registry bearer bodies are discarded and never committed. Stop OCI reads at HTTP 429 or reported pull allowance below ten. Preserve response bytes, HTTP status, cache and rate headers, UTC retrieval times, SHA-256 and any failure. The collector refuses to overwrite a date. Finish each daily run after one attempted read of every fixed tag or a binding ceiling, reporting unattempted tracks as unknown. After 24 October give a provisional account; after 28 October summarise the measured intervals. No pull share, host coverage, patch effectiveness, deployment or AI effect is inferred.

**Note, 24 October 2026:** from 24 October the daily read is taken at about 12:30 UTC rather than about 06:30, after the registry's rate limit stopped that morning's read (checkpoints/2026-10-24.md). One read per UTC day, as before; the 24 October read stays partial and is not repeated.
