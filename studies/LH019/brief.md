# LH019: What do the official PHP moving image tags name over time?

**Protocol 0.1, fixed 21 October 2026 UTC before reading the four moving tags.** Writer: Codex, GPT-6 Sol in ChatGPT Work Mode. Related first snapshot: LH018, protocol commit `d35c517`; this is a separate, overlapping episode, not an independent release. Model spend in this harness is unknown.

## Question and prior knowledge

When first observed today, and again about one, three and seven days later, what linux/amd64 image manifest do four preselected moving tags in Docker Hub's official `library/php` repository name? Do their configurations declare the fixed PHP source versions? A changing digest documents a published pointer changing between observations, not when it moved or whether anyone pulled or ran it.

Before this protocol, LH018 observed the upstream fixed versions 8.5.12, 8.4.27, 8.3.36 and 8.2.35 in four *version-specific* tags with distinct Apache, FPM and CLI variants between 16:49 and 16:50 UTC on 21 October. It did not inspect the corresponding moving tags. The event was selected after the emergency release, so any already-patched moving tag at baseline is a retrospective left-censored outcome, not a measured rollout delay.

## Fixed cohort and units

The units are four exact tag and architecture pairs in `library/php`, selected to match LH018's variants: `8.5-apache`, `8.4-fpm`, `8.3-cli`, `8.2-fpm`, each on linux/amd64. The bare `8.5`, `8.4`, `8.3`, `8.2` aliases are excluded because they may select a different variant. The four variants differ, so do not rank branches by apparent speed. No missing tag is replaced. The known fixed-version counterparts and their first observed manifest digests are retained in LH018, not treated as fresh LH019 observations.

For each tag, retain the Docker Hub tag API response, its current linux/amd64 digest, the source's platform `last_pushed` and tag `tag_last_pushed` fields, and Lighthouse's retrieval timestamp. If present, fetch that digest's OCI manifest and configuration to read `PHP_VERSION` and the declared `PHP_URL`. A tag name or configuration is a publisher's declaration. Do not fetch a layer or run an executable. Preserve full response bytes and hashes, HTTP status, relevant cache and rate-limit headers. Temporary anonymous registry bearer bodies are discarded. Current metadata cannot recover an earlier digest after the tag moves.

## Comparison and missingness

Compare each moving tag's digest and declaration to its *same-variant* version-specific LH018 counterpart, and compare later LH019 digests only with that same moving tag's earlier observed digest. Equal digests at observation imply equal manifest bytes addressed by that digest, not equal past tag history. A changed digest identifies an interval bounded by the two observations; it does not identify a precise first change or prove the image contains a patched executable. Record an absent tag, missing platform, inaccessible source, missing config, or request ceiling as unknown for the affected field. Do not call a transient error an unpatched image. Keep the two CVEs as one coordinated episode; do not estimate deployed coverage, pull share, runtime adoption or AI's effect.

## Runs, ceilings and stop

Run a baseline once on 21 October after this protocol is committed, then target 22, 24 and 28 October UTC as *separate authorized runs*. If a checkpoint is missed, record the actual time; never fabricate an on-time observation. Each run uses no more than 20 external requests, four counted OCI manifest GETs, 10 MiB retained bytes and no paid API. Stop OCI reads at HTTP 429 or reported remaining allowance below ten. Finish when every tag has one attempted reading or a ceiling binds. The collector refuses to overwrite an existing run. Later runs use the same cohort and definitions, with dated amendments committed before any changed question or method is applied.

The baseline output is timestamped raw responses, a read log, an offline hash and field replay, a four-row summary and a short study record. A later checkpoint is not claimed as complete until collected. No article is released on this baseline alone. Sources and their limits are documented in `sources.md`.
