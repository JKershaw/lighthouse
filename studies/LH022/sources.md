# LH022 sources

All reads 22 October 2026 UTC, with exact observation times, response status, byte hashes and full retained bodies in `data/snapshot-2026-10-22/`.

| Source | Endpoint and use | Limit |
| --- | --- | --- |
| S1 | GitHub official-images `contents/library/drupal`, production stanza selection | Current manifest only; no historic selection. |
| S2 | GitHub `docker-library/drupal` commit before 21 October 00:00 UTC, current repository and head commit | Source revisions, not image builds. |
| S3 | GitHub `docker-library/drupal` latest 20 Actions runs | A bounded recent list; run metadata cannot show base resolution. |
