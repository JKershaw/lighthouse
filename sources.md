# Sources

The sources the design and the studies cite by S number.

These sources provide starting methods, concepts and candidate data. They do not establish Lighthouse's proposed hypotheses. Every link resolved on 25 September 2026; where the check could not confirm the content, the entry says so. Documentation changes, so studies preserve the exact version they use. Re-check every link monthly and note here what moved. Each source entry, and each survey row that draws on one, carries the source's publication date and observation window beside the date Lighthouse read it, so that a report can be told from its successors.

### S1 Computer epidemics

Kephart and White, Directed-graph epidemiological models of computer viruses, IEEE Symposium on Security and Privacy, 1991. Models infection on directed networks and examines epidemic thresholds and imperfect defences. Relevant to propagation and removal; assumptions must be re-examined for each new system.

https://research.ibm.com/publications/directed-graph-epidemiological-models-of-computer-viruses

### S2 Digital ecology

Thomas S Ray, Evolution, Ecology and Optimization of Digital Organisms. A 1992 Santa Fe Institute working paper; the author-hosted HTML copy carries only a 1995 conversion date, so cite the working paper. Describes self-replicating programs and ecological interactions in Tierra's contained virtual environment. Relevant to the distinction between replication, adaptation and cooperation.

https://tomray.me/pubs/tierra/

### S3 Security incentives

Anderson and Moore, The Economics of Information Security, Science, 2006. Examines misaligned incentives and costs imposed on others. Relevant to collective maintenance and the distribution of harm. The PDF's text could not be read at the check; confirm the content on first use.

https://www.cl.cam.ac.uk/archive/rja14/Papers/sciecon2.pdf

### S4 Autonomous replication

Josh Clymer, Hjalmar Wijk and Beth Barnes, The Rogue Replication Threat Model, METR, 12 November 2024. Examines infrastructure maintenance, resource acquisition and resistance to shutdown. A threat analysis with stated disagreement among its authors about likelihood, not proof of an existing autonomous population.

https://metr.org/blog/2024-11-12-rogue-replication-threat-model/

### S5 Public software activity

GH Archive records public GitHub events as hourly JSON files from February 2011. Records to 2014 came from GitHub's retired Timeline API and records from 2015 onward from the Events API; payload structure varies by event type and can change. It can support a bounded activity study; event records alone do not provide all code diffs, deployments or reliable AI attribution.

https://www.gharchive.org/

### S6 Agent telemetry

OpenTelemetry semantic conventions for generative AI provide a vocabulary for model and agent instrumentation, including spans, metrics and events for model clients and the Model Context Protocol. The conventions have moved to a dedicated repository; pin a commit and check actual provider fields before adoption.

https://github.com/open-telemetry/semantic-conventions-genai

### S7 Identified AI traffic

Cloudflare AI Crawl Control documents measurements of identified crawler traffic within one Cloudflare zone: requests, status codes, bandwidth, content types and most-requested paths, filterable by operator and crawler. Such traffic is not a census of autonomous agents or of all internet activity. Page last updated 23 April 2026.

https://developers.cloudflare.com/ai-crawl-control/features/analyze-ai-traffic/

### S8 Orbital debris

Kessler and Cour-Palais, Collision frequency of artificial satellites: the creation of a debris belt, Journal of Geophysical Research 83(A6), 1978. The origin of the analogy in the digital Kessler hypothesis. Confirmed through the DOI's Crossref record; the publisher page was not retrievable at the check.

https://doi.org/10.1029/JA083iA06p02637

### S9 Research ethics for ICT

The Menlo Report: Ethical Principles Guiding Information and Communication Technology Research, US Department of Homeland Security, August 2012. States four principles: respect for persons, beneficence, justice, and respect for law and public interest. Relevant to collection boundaries and to studies that observe people's work.

https://www.caida.org/catalog/papers/2012_menlo_report_actual_formatted/menlo_report_actual_formatted.pdf

### S10 Archived source history

Software Heritage archives source code with full development history from many forges and issues persistent identifiers for code. A candidate source of repository history for LH002 that does not depend on a live forge. The main site returned an error at the check; the documentation and API index resolved.

https://docs.softwareheritage.org/

### S11 Dependency graphs

Open Source Insights (deps.dev) resolves dependency graphs for Cargo, Go, Maven, npm, NuGet, PyPI and RubyGems, with security advisories, an HTTP and gRPC API, and a public BigQuery dataset. A candidate source of typed dependency relationships for LH002. Its graphs are resolved from manifests and do not show what is deployed.

https://docs.deps.dev/

### S12 Harbour records

Harbour's dispatch and proxy integration documentation describes the dispatch item fields, lifecycle states, feedback markers, usage entries, audit logging and retention windows referred to in the programme. Read from the main branch on 25 September 2026; verify against the running version before a study relies on a field.

https://github.com/JKershaw/LinearViewer/blob/main/docs/dispatch-integration.md
https://github.com/JKershaw/LinearViewer/blob/main/docs/proxy-integration.md

### S13 Harbour papers standard

Harbour's writing standard for papers and essays defines the header fields and the Answer, Findings, Method, Limits and Next structure that Lighthouse studies adopt.

https://github.com/JKershaw/LinearViewer/blob/main/docs/papers/standard.md

### S14 The xz backdoor report

Andres Freund, backdoor in upstream xz/liblzma leading to ssh server compromise, oss-security list, 29 March 2024. A first-hand account of detecting the compromise from ssh logins taking unusual CPU and running more slowly. The primary source for the activity-layer detection in LH004.

https://www.openwall.com/lists/oss-security/2024/03/29/4

### S15 CVE-2024-3094

National Vulnerability Database record for the xz backdoor: malicious code in upstream tarballs from version 5.6.0, published 29 March 2024, base score 10.0. Confirmed through the NVD API; the web page needs scripts to render.

https://nvd.nist.gov/vuln/detail/CVE-2024-3094

### S16 CVE-2021-44228

National Vulnerability Database record for Log4Shell: remote code execution through Log4j 2 message lookups, published 10 December 2021, base score 10.0. A propagation case through the Java dependency graph. Confirmed through the NVD API.

https://nvd.nist.gov/vuln/detail/CVE-2021-44228

### S17 The left-pad removal

npm, kik, left-pad, and npm, 23 March 2016. Account of an unpublished package causing hundreds of dependent build failures per minute, and restoration within hours. A propagation case for a removal rather than an addition.

https://blog.npmjs.org/post/141577284765/kik-left-pad-and-npm

### S18 Cloudflare Radar

Documentation for Cloudflare's published view of global traffic, attacks and technology adoption, with a free API under a non-commercial licence, derived from Cloudflare's network and its public resolver. An observation boundary, not the internet. The Radar site refused the automated check; the documentation resolved.

https://developers.cloudflare.com/radar/

### S19 OpenRouter rankings

Live model usage ranked by tokens processed through one API broker. Its population is that broker's developers, not inference generally. Data shown through 24 September 2026 at the check.

https://openrouter.ai/rankings

### S20 PyPI download records

The Python Package Index's public table of file downloads, bigquery-public-data.pypi.file_downloads, one row per file downloaded from PyPI with its version, day and time, and the installer, Python, system and CI flag the client reports; streamed by PyPI's log processor, Linehaul, since 2016. Reading it needs a Google Cloud account. The Python Packaging guide, updated 22 September 2026, calls the counts "Highly inaccurate": local caches lower them, mirrors both raise and lower them, and scripts inflate them. A download is not an installation. Pages read 26 September 2026; the table itself was not read. LH005 assesses it in studies/LH005/sources.md.

https://docs.pypi.org/api/bigquery/
https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/

### S21 ClickPy

ClickHouse's public copy of S20, queryable anonymously in SQL, with daily sums by project, version, installer, file type, Python, system and country. It keeps the day and drops the time of each download, stores an unreported CI flag as not CI, re-ingests days it finds wrong, and one of its tables keeps an arbitrary file type when rows merge (studies/LH005/LH005.md). Its account of the pipeline is ClickHouse's blog of 21 January 2026. Held data to 25 September 2026 when read on 26 September 2026.

https://clickpy.clickhouse.com/
https://clickhouse.com/blog/clickpy-2-trillion-rows

### S22 PyPI Stats

pypistats.org, operated by the Python Software Foundation: daily download totals per project from S20, with and without mirrors, and by Python version and operating system, but not by release. It keeps 180 days: when read on 26 September 2026 it held 29 March to 25 September 2026. Its "without mirrors" series also drops downloads that name no installer, which its FAQ does not say (studies/LH005/LH005.md).

https://pypistats.org/api/

### S23 pepy.tech

A third-party service giving download totals and, anonymously, per-version daily counts for the last three months: 27 June to 25 September 2026 when read on 26 September 2026. Longer history and CI filtering need a paid key. It calls downloads "installs"; Lighthouse does not.

https://pepy.tech/pepy-api

### S24 Docker Hub

Docker's public container registry: for each repository, tags with their current digest, push time and last-pull time through hub.docker.com's API, and manifests, configurations and layers through the OCI distribution API at registry-1.docker.io with an anonymous token. An image's configuration gives its build time and history, and its layers hold what was installed, down to an installer's own package records. It keeps no history of what a tag named before: an earlier build stays visible only while another tag names it. Anonymous reads are limited per address; the limit served on 26 September 2026 was 100 pulls an hour, against six hours in Docker's documentation, and through a shared address it was spent by other traffic. LH006 assesses it in studies/LH006/sources.md. Read 26 September 2026.

https://docs.docker.com/docker-hub/usage/
https://hub.docker.com/

### S25 GitHub Container Registry

GitHub's container registry at ghcr.io, readable anonymously for public packages through the OCI distribution API with a token from ghcr.io/token. Its tag list gives names only, without times or digests; the history of a package's versions is in GitHub's REST API, which needs a token. A package that is not public answers the anonymous token request with 401. LH006 assesses it in studies/LH006/sources.md. Read 26 September 2026.

https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

### S26 OSV

The Open Source Vulnerabilities database, run by Google's open source security team: advisories gathered from GitHub's advisory database, the Python Packaging Authority's and others, queryable anonymously by package and version, each with its aliases, severity, affected and fixed versions, and the time it was published and last modified. Its publication time is when the advisory entered the source it came from, not when the flaw was found or fixed. LH007 read it for `mcp` 1.28.0 and found GHSA-vj7q-gjh5-988w, published 16 July 2026, fixed in 1.28.1 (studies/LH007/sources.md, S9). Read 26 September 2026. Its exports at osv-vulnerabilities.storage.googleapis.com/<ecosystem>/all.zip carry a storage generation per version; LH041 read the npm and PyPI exports on 8 November 2026 (223,208 and 12,013 malicious-package records, MAL- ids). Some MAL- records carry a `published` time at bare midnight, so their precision is a date.

https://osv.dev/
https://google.github.io/osv.dev/api/
https://osv-vulnerabilities.storage.googleapis.com/

### S27 Amazon ECR Public

Amazon's public container registry at public.ecr.aws, readable anonymously through the OCI distribution API with a token from its own token endpoint. It answered 429 to unpaced anonymous requests on 26 September 2026 and served when they were paced to about one a second; its documentation on anonymous limits was not read. Like the other registries, it keeps no history of what a tag named before. Read 26 September 2026.

https://gallery.ecr.aws/

### S28 OpenA2A Exposure Prevalence Index

OpenA2A Research's public monthly index of internet-facing AI services from Shodan index analysis: 207 queries in ten categories, each category the sum of its queries, one point per month (the latest sweep that month), dated by the UTC day of the sweep, with the number and range of sweeps where a month held several. Its methodology page says the reports are written by OpenA2A's autonomous research system, ARIA, with a named human editor; that from 18 June 2026 totals exclude credential categories; and that the index sees what Shodan indexes. Its robots.txt allows its pages to every agent. LH042 read it on 8 November 2026 (latest sweep 1 November 2026, first listed 14 March 2026).

https://research.opena2a.org/indices/exposure-prevalence
https://research.opena2a.org/methodology

### S29 Ollama in the Wild

Zuyao Xu, Xiang Li, Yuqi Qiu and Lu Sun, Ollama in the Wild: A Longitudinal Measurement of Exposed Ollama LLM Endpoints at Internet Scale, IMC 2026 (arXiv 2609.07115, 7 September 2026). Daily sweeps of the IPv4 space on Ollama's default port from 14 February 2025 to 13 February 2026 (362 observed days); it states an aggregate data release whose location LH042 did not find. Read 8 November 2026.

https://arxiv.org/abs/2609.07115

### S30 SecurityScorecard DECLAWED

SecurityScorecard STRIKE's live dashboard of OpenClaw instances ("favicon hash and HTTP title fingerprinting" from its internet-wide scans). Its figures load from a path its robots.txt disallows to every agent, beside a block list naming AI agents' fetchers, so Lighthouse does not read its counts (LH042, Amendment 1, which records the requests made to that path before the whole robots.txt had been read). Page read 8 November 2026.

https://declawed.io/

### S31 Registered OAI-PMH base URLs (historical dump)

The Open Archives Initiative's static dump, dated 8 October 2025, of the 7,103 base URLs (5,246 hosts) registered with the OAI-PMH registry, whose registration and validation services were discontinued on 18 July 2025. Entries were never re-checked for being alive; in LH044's draw of 40, 5 answered 404 or 410 and 5 had no DNS. Read 8 November 2026 (19:09 UTC).

https://www.openarchives.org/pmh/registry/ListFriends_HISTORICAL_2025-10-08.xml

### S32 Debian mirror list

Debian's page of official mirrors by country, 387 `/debian/` URLs on 351 hosts when read, the page last modified 29 October 2025 by its own footer; most mirrors serve plain HTTP. LH044 draws part of its panel from it. Read 8 November 2026 (19:04 UTC).

https://www.debian.org/mirror/list

### S33 HTTP Archive tech report API

The API behind HTTP Archive's Technology Report, at the address its report page uses (found in the page's script on 8 November 2026). `/v1/adoption` gives monthly counts per detected technology from January 2024 (September 2026 the latest when read); the documentation (HTTPArchive/tech-report-apis, apps/report-api/README.md) gives the schema but not the unit. Its rules detect Cloudflare Bot Management, Turnstile, DataDome, PerimeterX, Kasada, Akamai Bot Manager and captchas, not Anubis. Read by LH044 on 8 November 2026.

https://cdn.httparchive.org/v1/technologies?onlyname

### S34 The Wayback Machine (CDX and capture endpoints)

The Internet Archive's index of captures by URL and its raw captures (`id_`). From the cloud container on 8 November 2026 every connection to web.archive.org was reset (four attempts, 19:04 to 19:30 UTC), and archive.org's availability API answered 200 with no capture for example.com and then 429. Unread from there (LH044).

https://web.archive.org/cdx/search/cdx

### S35 ARIN RDAP

The American Registry for Internet Numbers' registration data service, used once by LH044 to find who holds the address the container's requests leave from: 160.79.104.0/21, Anthropic, PBC. Read 8 November 2026 (19:06 UTC).

https://rdap.arin.net/registry/ip/

### S36 Operators' statements on automated load

The operators' own accounts that LH044 codes in studies/LH044/statements/coded.csv: kernel.org, "creepy-crawlies" (29 August 2026); Wikimedia, its API rate-limits page (2026) and "How crawlers impact the operations of the Wikimedia projects" (1 April 2025); Read the Docs, "AI crawlers need to be more respectful" (25 July 2024); GitHub's changelog, "Updated rate limits for unauthenticated requests" (8 May 2025); COAR's Dealing With Bots resource and its June 2026 slides. Each is the operator's account. Read 8 November 2026, 19:29 to 19:30 UTC.

https://people.kernel.org/monsieuricon/creepy-crawlies
https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits
https://diff.wikimedia.org/

### S37 Epoch AI, AI data centers

Epoch AI's hub of estimated AI data-centre construction, power, compute (H100 equivalents), cost and chips, drawn by Epoch from satellite imagery, permits and public documents, with an update log and CSV and ZIP downloads. CC BY 4.0: "free to use, distribute, and reproduce provided the source and authors are credited"; credit Epoch AI, 'AI data centers', published online at epoch.ai. On 8 November 2026 the hub covered 96 sites, the downloads were stamped 6 November 2026, and the log page's data carried entries from 14 March 2026; earlier versions of the CSVs are not offered. robots.txt allows the data paths and disallows /assets/. LH045 keeps it weekly to 3 January 2027 (studies/LH045/brief.md). Read 8 November 2026.

https://epoch.ai/data/data-centers
https://epoch.ai/data/ai-data-centers/updates

### S38 IETF Datatracker API

The IETF's read-only API over Datatracker's database (Internet-Drafts, groups, states, authors, meetings), anonymous and in JSON, described at datatracker.ietf.org/api/. A draft is filed under a working group only once the group adopts it; until then it is an individual draft whose name may carry the target group's acronym. Author records carry affiliations as authors state them, and email addresses, which LH045 does not keep. robots.txt disallows only /doc/pdf/. Internet-Drafts are governed by the IETF Trust Legal Provisions (5.0). IETF 127 runs 14 to 20 November 2026, with the draft cutoff 13 days before. LH045 takes a census from it (studies/LH045/brief.md). Read 8 November 2026.

https://datatracker.ietf.org/api/

### S39 Compute and memory price pages whose terms forbid keeping their figures

Recorded so later sessions need not re-read them: Silicon Data's GPU rental indices (silicondata.com; terms forbid storing site contents "in a database or retrieval system" or reproducing them without written consent; about 30 days public, full history paid), DRAMeXchange's DRAM and NAND spot prices (TrendForce; terms forbid reproducing or publishing any materials without written consent; current session only), Shanghai Metals Market's computing-power indices (metal.com; its notice forbids copying "single prices" for any purpose without written consent), Vast.ai's GPU marketplace (terms forbid automated retrieval and any index or benchmark built from it) and Microsoft's Azure Retail Prices API (the Microsoft APIs Terms of Use forbid building databases or copies of API data). A single attributed figure may be quoted in a dated sentence; no series may be kept. Read 8 November 2026 (studies/LH045/brief.md, Part A).

### S40 OpenSSF malicious-packages

OpenSSF's repository of malicious-package reports in OSV format (MAL- ids), merged from sources such as GitHub's malware advisories (`ghsa-malware`), Amazon Inspector, Google's open source security team, kam193, ReversingLabs and OpenSSF Package Analysis; each record names its origins and import times; OSV serves the same records in its exports (S26). Records are one per package, so a package compromised twice holds both episodes' versions. LH041 read the README, contributing guide, schema additions and configuration on 8 November 2026 (raw files via raw.githubusercontent.com) and spot-checked 20 records, all matching OSV's copies.

https://github.com/ossf/malicious-packages

### S41 The npm registry's package documents

registry.npmjs.org/<package>: per-version publish times (`time`), which LH041 found kept for many removed malicious versions, the current maintainers, dist-tags and surviving version documents. Read anonymously; deleted packages answer 404. LH041 read 2,198 on 8 November 2026 (84 answered 404).

https://registry.npmjs.org/

### S42 GitHub REST API documentation: events and event types

GitHub's pages on the public events API and its event types (undated; API version 2026-03-10 in the examples). Public events' latency is "anywhere from 30s to 6h"; a PushEvent payload carries no commits; CreateEvent's ref types are branch, tag and repository. No change notice for October or November 2026. LH046 read them on 8 November 2026 and keeps them in studies/LH046/data/sources/.

https://docs.github.com/en/rest/activity/events
https://docs.github.com/en/rest/using-the-rest-api/github-event-types

### S43 GitHub changelog, "Upcoming changes to GitHub Events API payloads"

Published 8 August 2025: push events lose commit summaries and counts from 7 October 2025, which explains the PushEvent payload LH002 and LH046 saw. Read 8 November 2026.

https://github.blog/changelog/2025-08-08-upcoming-changes-to-github-events-api-payloads/

### S44 GitHub changelog, "Email notifications for repository push events have been retired"

Published 15 October 2026. A different feature from the events API; recorded by LH046 because of its date, with no link to the archive's gaps stated. Read 8 November 2026.

https://github.blog/changelog/2026-10-15-email-notifications-for-repository-push-events-have-been-retired

### S45 GitHub status incidents API

GitHub's status page's incident feed: the last 50 incidents, 31 August to 8 November 2026, when LH046 read it on 8 November 2026. No incident names the public events API.

https://www.githubstatus.com/api/v2/incidents.json
