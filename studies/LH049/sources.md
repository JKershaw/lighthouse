# LH049 sources

Every source read for this study, with the time it was read. Pre-brief reads touched no download endpoint: no request went to api.npmjs.org, to npm's package page (which shows weekly downloads) or to any tarball. Raw bodies are kept gzipped, email addresses withheld, under [data/](data/), each with a read log (`read_log.json`: URL, UTC start and finish, status, bytes received, their SHA-256, emails withheld, robots.txt decision). Collector for these reads: [scripts/collect_prebrief.py](scripts/collect_prebrief.py). Before each fetch, scripts/robots_gate.py was asked (provider anthropic); every URL below was allowed.

Some sources state download counts for the package (not for 13.3.0 from npm's own per-version data); the brief lists them under "What is already known of the outcome".

## Event records, read before the brief (10 November 2026)

| Id | Source | URL | Read (UTC) | Status, bytes | Publication date | What it gives |
|---|---|---|---|---|---|---|
| E1 | npm registry, package document | https://registry.npmjs.org/@ethersphere%2fbee-js | 14:37:25 to 14:37:26 | 200, 884,239 | live document, `time.modified` 2026-11-09T01:24:58.830Z | Publish time of every version; 13.3.0 has a `time` entry (2026-11-09T00:09:50.630Z) but is not in `versions`; dist-tag `latest` is 13.2.0; no deprecation mark on any version; no `unpublished` entry. Kept as `data/pre-brief-2026-11-10T1437Z/registry_packument.raw.gz` (536 email addresses withheld). |
| E2 | npm registry, version document | https://registry.npmjs.org/@ethersphere/bee-js/13.3.0 | 14:37:26 | 404, 27 | live | `"version not found: 13.3.0"`. |
| E3 | StepSecurity, "@ethersphere/bee-js 13.3.0 Compromised" | https://www.stepsecurity.io/blog/ethersphere-bee-js-13-3-0-compromise | 14:37:26 to 14:37:27 | 200, 173,318 | dated 8 November 2026 on the page (the event is 9 November UTC) | Published to npm at 00:09:50 UTC on 9 November; trusted publishing, valid SLSA provenance; a `postinstall` hook that fetched and ran remote code; npm still mapped `latest` to 13.3.0 at 00:31 UTC; no removal time given. |
| E4 | StepSecurity blog listing | https://www.stepsecurity.io/blog | 14:37:27 | 200, 161,546 | live | Where E3 was found (scout 3, source 5). |
| E5 | Socket blog listing | https://socket.dev/blog | 14:37:27 to 14:37:28 | 200, 526,453 | live | Link to E8. |
| E6 | OSV query for the package | https://api.osv.dev/v1/query (POST, package name and ecosystem npm) | 14:37:28 | 200, 1,627 | record modified 2026-11-09T02:30:04Z | MAL-2026-18773, alias GHSA-hh7j-5m3j-23pf, version 13.3.0, published 2026-11-09T01:25:27Z. |
| E7 | npm, download-count documentation | https://raw.githubusercontent.com/npm/registry/main/docs/download-counts.md | 14:37:28 to 14:37:29 | 200, 5,389 (sha256 6c330fe6..., identical to the gate's read at 14:32:24Z) | undated | Endpoints, inclusive start and end dates, per-version counts only for "the last 7 available days", daily data loaded soon after UTC midnight. |
| E8 | Socket, bee-js compromise | https://socket.dev/blog/bee-js-compromise | 14:38:30 to 14:38:32 | 200, 632,327 | 9 November 2026 | npm "received" 13.3.0 under `latest` at 00:09:50 UTC and "removed it at 01:24:58 UTC"; GHSA issued 01:25:27 UTC; provenance verified as genuine; package counts and an estimate (brief, "What is already known"). |
| E9 | npm blog, "numeric precision matters: how npm download counts work" | https://blog.npmjs.org/post/92574016600/numeric-precision-matters-how-npm-download-counts-work.html | 14:38:32 | 200, 7,757 | 2014 (archive) | A download is an HTTP 200 response serving a tarball; mirrors fetch each new version once, usually on its publication day. |

Read logs: `data/pre-brief-2026-11-10T1437Z/read_log.json` (E1 to E7) and `data/pre-brief-2026-11-10T1438Z/read_log.json` (E8, E9), with each body's SHA-256.

## Read earlier by Lighthouse, not re-read here

- Scout 3's file, notes/horizon/2026-11-10T1415Z/scout-3-supply-chain.md (its sources 5 and 11 are E4 and E3), and the gate's primary reads in notes/horizon/2026-11-10T1415Z.md (robots.txt for api.npmjs.org, registry.npmjs.org and others; E7).

## Not opened

- The analysis by a third firm that E8 cites; GitHub's advisory page for GHSA-hh7j-5m3j-23pf (github.com pages answered 403 from the container on 28 September; OSV's copy, E6, was read); the maintainers' issue that E3 cites; any mirror.

## Outcome reads

Listed here as they happen, by read label, from `data/read-<label>/read_log.json`.
