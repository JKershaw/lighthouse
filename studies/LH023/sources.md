# LH023 sources

All new reads 22 October 2026 UTC, exact observation times and retained bodies in `data/snapshot-2026-10-22/`; LH022's `sources.md` covers the reused selection stanza and source run list.

| Source | Endpoint and use | Limit |
| --- | --- | --- |
| S1 | GitHub `docker-library/drupal/contents/10.6/php8.3/fpm-trixie/Dockerfile` at three immutable commit SHAs | `FROM` is an instruction, not a resolved base digest. |
| S2 | Docker Hub `library/drupal` tag API for `10.6-php8.3-fpm` | Current pointer and publisher timestamps, not historical availability. |
| S3 | Docker Registry v2 anonymous manifest by exact amd64 digest and config blob | Digest-authenticated current bytes and declared environment; layers and executables unread. |
