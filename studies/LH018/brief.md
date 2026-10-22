# LH018 brief: Which public records show the emergency PHP fix moving downstream?

**Protocol:** 0.1, fixed 21 October 2026 UTC before any of the seven downstream tracks' vulnerability statuses, package revisions, tags or manifests were read. **Issue:** #24. **Writer:** Codex, GPT-6 Sol in ChatGPT Work Mode. **Base repository:** 7828bb8. This is a selected, newsworthy event; it is not a prospective random sample of incidents.

## Question and known outcome

The upstream PHP project announced on 21 October 2026 that 8.5.12, 8.4.27, 8.3.36 and 8.2.35 fix CVE-2026-109618 and CVE-2026-109619. The PHP Foundation and OpenAI published accounts of AI-assisted discovery and coordinated disclosure. The Foundation says Chainguard pushed a patched image before the coordinated release; that was read before this brief, so Chainguard is not in the seven-track cohort. No downstream result for the selected tracks was inspected before the protocol snapshot. The release itself and the CVEs are known outcomes, not new findings.

Sources read before protocol: PHP security advisory, https://www.php.net/archive/2026.php (21 October 2026); the Foundation's account, https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/ (search retrieval on 21 October; reopen primary page before study citation); OpenAI's account, https://openai.com/index/coordinated-disclosure-of-critical-vulnerabilities/ (21 October). Method and source documentation: studies/LH006/brief.md and sources.md, studies/LH007/brief.md and sources.md, https://docs.docker.com/reference/api/hub/latest/operations/GetRepositoryTag/ and https://documentation.ubuntu.com/security/security-updates/osv/ (21 October); Ubuntu's security API docs were discovered by search but timed out when opened, so may only be cited if successfully read later. The Debian security tracker serves per-CVE pages; its entire JSON data file is over 13 MB and is not needed. The bounded discovery used four web queries, comprising Debian tracker, Ubuntu CVE API, Alpine security and Docker API, on 21 October. Only the two primary documentation pages just named were opened successfully. No literature result changed the seven-track design; more literature is not needed for this first source-feasibility reading.

## Why this task now

LH013, issue #15, remains first in programme.md's 30 September checkpoint. Its earliest possible start date, 13 October, has passed, but its ClickPy eligibility has not been checked in this session. This emergency is a short-lived opportunity to retain a contemporaneous first snapshot before moving tags erase their earlier state. That justifies one bounded observation now, without changing LH013's fixed design or claiming this task supplants it. Repairing LH001's instrument is inward and would not recover this snapshot later. The selected outward question tests whether LH006's record boundaries transfer to a different ecosystem in an urgent event; it does not transfer Python uptake rates.

## Seven fixed tracks and unit

One unit is one source-package/release or one official image-tag/linux-amd64 tuple. They are a purposive, heterogeneous reading of public records, not a census or a representative sample. No inaccessible or negative track is replaced.

| ID | Track | Pre-outcome selection reason |
| --- | --- | --- |
| D1 | Debian bookworm, source `php8.2` | Debian stable security-tracker backport path for PHP 8.2 |
| D2 | Debian trixie, source `php8.4` | the next Debian stable branch's PHP 8.4 path |
| U1 | Ubuntu 24.04 LTS (noble), source `php8.3` | an LTS backport path for PHP 8.3 |
| I1 | Docker Hub `library/php:8.5.12-apache`, linux/amd64 | upstream 8.5 fixed version, Apache variant |
| I2 | Docker Hub `library/php:8.4.27-fpm`, linux/amd64 | upstream 8.4 fixed version, FPM variant |
| I3 | Docker Hub `library/php:8.3.36-cli`, linux/amd64 | upstream 8.3 fixed version, CLI variant |
| I4 | Docker Hub `library/php:8.2.35-fpm`, linux/amd64 | upstream 8.2 fixed version, FPM variant |

The three package tracks are read for both CVEs using Debian's per-CVE tracker pages and Ubuntu's CVE records or official OSV records; if a source reports the packages under another name, record the mismatch and do not silently substitute. The four image tags are the fixed upstream version numbers, not the moving `8.5`, `8.4`, `8.3` or `8.2` tags. Variants deliberately differ and their timing must not be compared as though one controlled cohort. If a fixed tag does not exist, a single unsuccessful read is retained and no similarly named substitute is chosen.

## Records and events

Capture the HTTP retrieval UTC timestamp, status, response body or bounded excerpt, headers relevant to publication, SHA-256 of saved bytes and source URL for every request. Record the source's own `published`, `modified`, `last_pushed`, `last_updated` and package fix-status fields separately from when Lighthouse saw them. A source's modification date is not automatically its first fix publication date. If only dates are available, report dates, not precise hours or lag. Do not assume both CVEs have the same downstream status.

For D1, D2 and U1, read the two CVE records and classify each as vendor-marked fixed, affected without a fix, not affected, under investigation or unavailable, using the vendor's own release and source package. Retain version/revision and any vendor notice references. A vendor backport can fix a CVE while its upstream-looking version stays below PHP's new release; do not compare just the leading version number. A vendor tracker saying fixed supports the vendor's assertion and fix revision, not the presence of an updated package in any particular installed system. Where a dated security notice and its package publication record are accessible inside the cap, read them to date publication; otherwise the event time remains unknown, with first observation as an upper bound for availability.

For I1-I4, read the Docker Hub tag API response. If present, record the digest, tag metadata and linux/amd64 variant's reported push time. Then, within the request/pull budget, read an OCI manifest and configuration blob and inspect build metadata including `PHP_VERSION` if supplied. A version-bearing tag name alone is a registry assertion, not an independently verified installed PHP version. The configuration is a builder's declaration. No image layers or executable content are fetched or run in this first snapshot. Only an inspected installed binary or package record in a later authorized bounded study would support stronger wording. A moving tag's old digest is not recoverable from its current listing alone.

## Comparison, limits and alternatives

The primary output is seven per-track results at a single observation time, including explicit missingness and which public boundary each reaches. Descriptive lags from the upstream event are secondary only where both independent event clocks are precise enough. Both CVEs are one coordinated episode. A tag's push date, vendor advisory date and Lighthouse's first-seen time are not interchangeable. No denominator for websites, package installations, image pulls or running deployments exists; no protection rate is calculated. Do not infer active compromise, autonomous AI propagation or AI-caused faster patching. Packaging schedules, embargo access, backports, architecture-specific builds, cache and source lag are alternatives to any apparent interval; test only what the records can distinguish. Unavailable pages are unknown, not unfixed, and unobserved tags are not proof that no image was ever published.

## Ceiling, stop and possible inconclusive result

At most 60 external collection requests and 50 MiB retained bytes, no paid external APIs, no credentials beyond anonymous registry tokens. Respect Docker Hub's shared rate limit: at most four counted manifest GETs, one per selected tag, and stop at HTTP 429 or a remaining allowance below ten; metadata requests are separate. A HEAD may itself fail at exhaustion. Stop after the seven tracks have one snapshot or at the first binding ceiling. If no source provides a fix status or reliable tag metadata, write a source-feasibility result with the failed access log, not an invented account. The initial snapshot ends today; any later day is another run with a separately retained plan. A first observation cannot prove when an event first happened.

Outputs: read log, raw evidence or bounded excerpts, a replayable collector, summary tables, LH018.md with Answer, Findings, Method, Limits, Next and Corrections. A piece is optional and requires the repository's evidence and reader reviews before release. Model spend is unknown in this harness; do not use Claude transcript estimates or call it zero.
