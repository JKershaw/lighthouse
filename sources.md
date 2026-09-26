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

The Python Package Index's public table of file downloads, bigquery-public-data.pypi.file_downloads, one row per file downloaded from PyPI with its version, day and time, and the installer, Python, system and CI flag the client reports; streamed by PyPI's log processor, Linehaul, since 2016. Reading it needs a Google Cloud account. The Python Packaging guide, updated 22 September 2026, calls the counts "highly inaccurate": local caches lower them, mirrors both raise and lower them, and scripts inflate them. A download is not an installation. Pages read 26 September 2026; the table itself was not read. LH005 assesses it in studies/LH005/sources.md.

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
