# LH040 sources

Every source below was read once by [scripts/collect_prebrief.py](scripts/collect_prebrief.py) on 8 November 2026, before the brief was fixed, and is kept raw under the directory named, with its read log (`readlog.csv`: URL, UTC start, HTTP status, content type, size, SHA-256). None of them is a download count read by Lighthouse; where a source itself states a count, the brief says so under "What is already known of the outcome". Global numbered sources are in [sources.md](../../sources.md); ClickPy is S21 there.

## Registry and advisory records

| Id | Source | Published or modified | Read (UTC) | Kept as | What it gives |
| --- | --- | --- | --- | --- | --- |
| L1 | PyPI JSON API, project: https://pypi.org/pypi/litellm/json | live | 2026-11-08 14:14 | [pre-brief-2026-11-08T1414Z/pypi_project_json.raw](data/pre-brief-2026-11-08T1414Z/pypi_project_json.raw) | Every release PyPI lists, with each file's upload time. Lists 1.107.0.dev1 to dev3 and 1.107.0rc1 to rc3, and no 1.107.0. |
| L2 | PyPI JSON API, version: https://pypi.org/pypi/litellm/1.107.0/json | live | 14:14 | pypi_1.107.0_json.raw | HTTP 404 (`{"message": "Not Found"}`), as the gate found on 7 November at 09:22 UTC. |
| L3 | PyPI JSON API for 1.106.7 and 1.108.0 | live | 14:14 | pypi_1.106.7_json.raw, pypi_1.108.0_json.raw | Neighbours' metadata. |
| L4 | PyPI simple index (JSON form): https://pypi.org/simple/litellm/ | live, `_last-serial` 43351258 | 14:14 | pypi_simple_json.raw | No file of 1.107.0 (final) listed; project status "active". |
| L5 | PyPI project pages, https://pypi.org/project/litellm/ and /1.107.0/ | live | 14:14 | pypi_project_page*.raw | A 3,038-byte script challenge for both: unavailable. |
| L6 | OSV query for litellm 1.107.0 (POST https://api.osv.dev/v1/query) | live | 14:14 | osv_query_1.107.0.raw | One record: MAL-2026-2144. |
| L7 | OSV MAL-2026-2144: https://api.osv.dev/v1/vulns/MAL-2026-2144 | published 2026-03-24T11:15:14Z, modified 2026-10-29T14:30:33Z | 14:14 | osv_MAL-2026-2144.raw | Affected versions 1.82.7, 1.82.8, 1.107.0. Its details say 1.107.0 was "uploaded to PyPI on 2026-10-21 between 11:39 and 11:40 UTC" and describe the payload; the 1.107.0 origin is Amazon Inspector's report IN-MAL-2026-022275, imported 2026-10-29T14:14:39Z, whose own per-source text, as kept in the record, says no malicious code path was found. No removal time. |
| L8 | OSV PYSEC-2026-2: https://api.osv.dev/v1/vulns/PYSEC-2026-2 | published 2026-03-24T15:35:32Z | 14:14 | osv_PYSEC-2026-2.raw | The March 2026 compromise of 1.82.7 and 1.82.8. |
| L9 | OSV query for every litellm record (POST, package only) | live | 14:15 | [pre-brief-2026-11-08T1415Z/osv_query_all_litellm.raw](data/pre-brief-2026-11-08T1415Z/osv_query_all_litellm.raw) | 85 records, no further page. Three concern malicious code: MAL-2026-2144, PYSEC-2026-2 and GHSA-5mg7-485q-xm76 (published 2026-03-25T14:25:42Z), the last two about the March versions only. |
| L10 | PyPI documentation, "PyPI Basics": https://docs.pypi.org/using-pypi/pypi-basics/ | live | 14:15 | pypi_docs_quarantine.raw | A quarantined release "cannot be installed by package installers ... and is excluded from PyPI's search results and index APIs". So a 404 does not tell quarantine from deletion. |

## Reports of the event

| Id | Source | Page date | Read (UTC) | Kept as | What it reports |
| --- | --- | --- | --- | --- | --- |
| R1 | LiteLLM, "Oct 21, 2026 LiteLLM release v1.107.0 Compromised": https://docs.litellm.ai/blog/security-incident-oct-21-2026 | published 21 Oct 2026, "Last updated: October 21, 2026 20:30 UTC", with a note of 23 Oct 21:50 UTC that parts were later found inaccurate | 14:15 | [pre-brief-2026-11-08T1415Z/litellm_incident_oct21.raw](data/pre-brief-2026-11-08T1415Z/litellm_incident_oct21.raw) | "all seven wheels, live from 11:39:51 to 13:23 UTC"; "By 13:23: PyPI had removed litellm==1.107.0"; Docker tags 11:46:56 to 14:20 UTC. |
| R2 | LiteLLM, attack chain report: https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain | published 23 Oct 2026 | 14:15 | litellm_incident_oct21_attack_chain.raw | Seven wheels "published to PyPI" 11:39:51 to 11:40:13; LiteLLM aware "shortly before ... (13:00 UTC)"; "The PyPi releases were frozen by ... (13:23 UTC)"; a table row "by 13:23, PyPI quarantines litellm==1.107.0". |
| R3 | LiteLLM, changes after 21 October: https://docs.litellm.ai/blog/security-changes-after-oct-21-2026 | not used for times | 14:15 | litellm_changes_after_oct21.raw | Remediation. |
| R4 | LiteLLM, March 2026 security update: https://docs.litellm.ai/blog/security-update-march-2026 | March 2026 | 14:15 | litellm_update_march2026.raw | 1.82.7 and 1.82.8 "live on March 24, 2026 from 10:39 UTC for about 40 minutes before being quarantined by PyPI". |
| R5 | PyPI blog, "Incident Report: LiteLLM/Telnyx supply-chain attacks, with guidance": https://blog.pypi.org/posts/2026-04-02-incident-report-litellm-telnyx-supply-chain-attack/ | 2 Apr 2026 | 14:15 | pypi_incident_report_march2026.raw | For the March litellm versions: upload to first report 1h 19m, report to quarantine 1h 12m, "upload to quarantine (total exposure time): 2h 32m"; and a download count (see the brief). |
| R6 | Cloudsmith, "LiteLLM 1.107.0 compromised on PyPI" (Meghan McGowan): https://cloudsmith.com/blog/litellm-1-107-0-compromised-on-pypi | 22 Oct 2026 | 14:14 | [pre-brief-2026-11-08T1414Z/cloudsmith.raw](data/pre-brief-2026-11-08T1414Z/cloudsmith.raw) | Upload "At 11:39 UTC on October 21"; "the second time we've seen an attack on LiteLLM, the first in March 2026"; stolen GitHub CLI OAuth tokens; payload. No removal time. |
| R7 | Aikido, "LiteLLM compromised again: infostealer and RAT found in version 1.107.0" (Ilyas Makari): https://www.aikido.dev/blog/litellm-compromised-infostealer-rat | published 21 Oct, updated 22 Oct 2026 | 14:14 | aikido.raw | Infostealer and RAT; "PyPI has now quarantined and removed version 1.107.0"; affected if pip installed 1.107.0 "between 11:39 and 12:47 UTC" (12:47 is not explained on the page). |
| R8 | Datadog Security Labs, "LiteLLM supply chain compromise: What you need to know" (Ian Kretz): https://securitylabs.datadoghq.com/articles/litellm-compromised-pypi-docker/ | 21 Oct 2026 | 14:14 | datadog.raw | Timeline: 11:39 published; "13:20 PyPI quarantines affected version 1.107.0"; 13:53 Docker images removed; "the second supply chain compromise of LiteLLM in 2026". |
| R9 | StepSecurity, "litellm 1.107.0 compromised" (Sai Likhith): https://www.stepsecurity.io/blog/litellm-1-107-0-compromised-pypi-backdoored-wheels-credential-stealer | dated 21 Oct 2026; it cites BerriAI's report of 23 Oct, so it was revised after that date | 14:14 | stepsecurity.raw | "11:39:51 to 11:40:13 Seven 1.107.0 wheels uploaded"; "by 13:23 1.107.0 removed from PyPI", times "from BerriAI's reports"; and a download count (see the brief). |
| R10 | PyPI blog index and RSS feed: https://blog.pypi.org/, https://blog.pypi.org/feed_rss_created.xml | latest 6 Nov 2026 | 14:14 | pypi_blog.raw, pypi_blog_feed.raw | No post about 1.107.0. The 6 November post says the JSON API now exposes a release status (quarantined, yanked, archived, pre-release). |
| R11 | Python status history feed: https://status.python.org/history.rss | live | 14:14 | python_status_history.raw | No entry naming litellm or a quarantine. |
| R12 | Aikido blog index; LiteLLM blog index | live | 14:14 | aikido_index.raw, litellm_docs_blog.raw | Used only to find R1 to R4. |

Not opened: Wiz's posts (named in L7 and in a search summary), Snyk's, the Hacker News thread, the GitHub issues BerriAI/litellm#47826, #24512 and #24518 (github.com's issue pages answered 403 from this container on 28 September), LiteLLM's post "mistral-supply-chain-attack-may-2026" (listed on its blog index; title only), SOCRadar, Help Net Security and the other search results of 8 November.

## Instruments checked for structure only

| Read (UTC) | What | Kept as |
| --- | --- | --- |
| 2026-11-08 14:14 | ClickPy (S21) `SHOW TABLES FROM pypi`; `DESCRIBE` of `pypi_downloads_per_day_by_version` and `pypi`; `max(date)` of `pypi_downloads_per_day_by_version` for `requests` (2026-11-07) | pre-brief-2026-11-08T1414Z/clickpy_*.raw |
| 2026-11-08 14:16 | ClickPy `DESCRIBE` of the per-day tables by installer and type, by file type and by system; deps.dev's version and dependents endpoints for `requests` 2.32.3 (both HTTP 200) | [pre-brief-2026-11-08T1416Z/](data/pre-brief-2026-11-08T1416Z/readlog.csv) |
| 2026-11-08, between 14:17 and 14:21 | ClickPy `EXPLAIN SYNTAX` of each query in scripts/collect.py, which parses a query and reads no table; bodies not kept | none |
