# LH060 source register: search-read of 25 November 2026

**In short.** We wanted to know what published studies find when they measure how far operators deploy available security fixes or features, broken down by the operator's size, capacity or type. The six fixed searches and the known documents gave 15 candidates, and each got its one fetch. Three met the brief's inclusion rule: one counted from scans (a security-ratings company's own data), one survey, and one counted from rescans broken down by type of operator. Twelve were excluded, three of them because the full text didn't come back. That's the brief's bare minimum for describing the literature, and two of the three inclusions rest on judgement calls flagged below. This register records the read as made on 25 November; the evidence review of 26 November then excluded the survey and corrected one quotation from the scan paper, which leaves two inclusions (see the revision below and the record, version 0.2).

Row LH060-search-read. Read by a research subagent in Claude Code (Claude Opus 5.5, Anthropic), 25 November 2026, 14:14Z to about 15:00Z. Instruments: Claude Code's WebSearch tool (standard mode); [fetch_read.py](fetch_read.py) through scripts/lh_fetch.py (access='oneoff', LIGHTHOUSE_PROVIDER=anthropic, robots checked before the request and before each redirect); pdftotext (poppler, the system binary) for text extracted outside the repository and deleted after reading; [write_derived_read.py](write_derived_read.py) for the derived files. Searches: [searches.md](searches.md). Requests: [fetchlog.csv](fetchlog.csv). Derived files: [data/read-2026-11-25T1414Z/](data/read-2026-11-25T1414Z/). No body was kept: none of the fifteen states a licence allowing redistribution (the Snail Mail preprint says "Not for redistribution"; the USENIX papers say open access is "sponsored by USENIX"; the ACM preprints carry ACM's personal-use notice). No dataset, appendix or linked artefact was fetched, and nobody was contacted.

## Counts

- Searches run: 6 of 6, none failed. Results shown: 73 (15, 10, 10, 10, 10, 18), many of them duplicates.
- Candidates: 15 (10 from results, 5 known documents not returned by any query: C01, C03, C04, C11, C14). Known documents returned by a query: C02 (the USENIX 2016 notification study by Li and others, returned as well as the known one; see note 1), C05, C09, C15.
- GETs: 15 of 15 spent, no retries, no robots refusals.
- Read in full: 12. Walls: 1 (C01, HTTP 404). Full text not retrieved: 2 (C05, C06; the GET returned the publisher's summary page, not the report).
- Included: 3 (C07, C08, C10). Excluded: 12. Candidates not read: 0.

## Order of reading

The brief's order (tier, then most recent year, then first appearance; known documents not returned follow on ties). Tier 1 by metadata: C01 NDSS 2018, C02 USENIX Security 2016 (Q4), C03 USENIX Security 2016 (known). Tier 2: C04 DBIR 2025, C05 Prioritization to Prediction vol. 3 (Q6 #14), C06 vol. 2 (Q6 #18). Tier 3, arXiv: C07 2026 (Q3 #3), C08 2026 (Q3 #10), C09 2025, C10 2024, C11 2022, C13 2021 (Q3 #7), C12 2021 (Q4 #1), C14 2020, C15 2017. The fetch script ran C12 before C13. The tie rule puts C13 first, but with all 15 candidates read the swap changed nothing. Tier went by metadata as the brief says: C09 and C15 were placed as arXiv preprints, although prior knowledge has them at IEEE S&P 2026 and (unchecked) a 2017 conference. That changed nothing either.

## Included

| Code | Document | Venue, peer review | Published | Population and unit | Size, capacity or type measure | Outcome | Window | Data public | Interest stated |
|---|---|---|---|---|---|---|---|---|---|
| C07 | Haque, Vinberg, Edwards, Cruz, "Empirical Study of Post-Quantum Cryptography Adoption Status in SSH Infrastructure", arXiv 2611.09703v1 | arXiv preprint, not peer reviewed as far as stated | 6 November 2026 | 1,523,998 SSH services on port 22 mapped to 27,012 organisations ("entities") by the authors' company's attribution engine; unit the organisation | revenue and employee count (firmographic data "from our service providers"); SSL active count and IPv4 count (company pipelines); sector (23); region | offers a post-quantum key exchange on at least one SSH server; share of the organisation's IPs that do | one scan day, 16 February 2026 | not stated (company data) | authors employed by Bitsight, whose scans are the data |
| C08 | Deng, Inthiran, "Towards Zero Trust Architecture: A Pilot Study on Information Systems Security Readiness amongst Small and Medium Enterprises", arXiv 2605.18901 | arXiv preprint; the PDF names PACIS 2026, not a listed venue | 2026 (identifier) | 64 IT and security professionals in Asia-Pacific, purposive convenience sample; unit the respondent's organisation | employees: under 50, 50 to 250, 250 to 500, over 500 | security model in use, as reported: perimeter, zero trust or hybrid | questionnaire 20 March to 5 May 2025 | not stated | not stated |
| C10 | Nosyk, Korczyński, Gañán, Król, Lone, Duda, "Don't Get Hijacked: Prevalence, Mitigation, and Impact of Non-Secure DNS Dynamic Updates", arXiv 2405.19871v1 | arXiv preprint, no venue stated in the text read | 30 May 2024 | nameservers accepting non-secure dynamic updates in a February to March 2017 scan, notified through 44 CSIRTs (Phase 1) against 36 not notified; unit the nameserver, grouped by CSIRT | CSIRT constituency type: CIIP, government, military, national, non-commercial, research and education | remediation on rescans (Kaplan-Meier survival from notification) | Phase 1 notifications 7 September to 19 October 2017, survival plotted to 180 days; Phase 2 in 2018; rescan 2022 | not stated in the text read | academic; one author at RIPE NCC |

### Claims (unit of synthesis), with class

| Claim | Measure | Direction reported | The authors' words | Class | Notes |
|---|---|---|---|---|---|
| C07-a | revenue; employees | no difference | "Both small-scale organizations and multi-billion dollar enterprises show similar median distributions" | measured; vendor | read from box plots, no test stated |
| C07-b | SSL active count | larger more (starting deployment) | "entities with more mature web presences (i.e., higher SSL active counts) show a slightly higher propensity to initiate PQC deployment" | measured; vendor | no test stated |
| C07-c | IPv4 count | larger less (share of the organisation's servers) | "adoption density thins as network size increases" | measured; vendor | the authors' "complexity penalty" explanation is asserted, not measured |
| C07-d | sector (type) | differs by sector | adoption "driven by research-oriented and infrastructure-heavy sectors like 'Education' and 'Telecommunications'", while finance, healthcare and legal "still remain in the experimental phase" | measured; vendor | |
| C08-a | employees | no difference by test (χ² = 4.27, df = 6, p = .64); descriptively the smaller report zero trust more often | "a cross-tabulation of security model in use by organisation size shows no statistically significant association" | self-reported | zero trust row shares 0.500 (under 50, n=10), 0.417 (50 to 250, n=24), 0.250 (250 to 500, n=12), 0.231 (over 500, n=13); small cells, so the test has little power |
| C10-a | CSIRT constituency type | differs by type | "Military CSIRTs are particularly fast and efficient in remediation, contrary to research and educational entities that exhibit the slowest and worst patching rates" | measured | Gehan-Breslow-Wilcoxon test, p = 0.00076 (their figure 5); the remediation follows a notification; numbers per type not checked |

Tally (unreviewed): 6 claims from 3 documents; 5 measured (4 of them vendor, from one origin, C07), 1 self-reported, 0 modelled, 0 asserted. Public data: none stated for any of the six. Directions on size: no difference (C07-a, C08-a), larger more (C07-b), larger less (C07-c). Type differs (C07-d, C10-a). No figure is combined across documents, and no difference is read as size causing it.

### Judgement calls to review

1. **C08:** whether a reported "security model in use" (zero trust against perimeter) is the deployment of an available security feature. It was counted as one, a configuration and architecture the organisation could adopt. Read the other way, C08 fails criterion 1 and the inclusions fall to two, below the brief's threshold of three.
2. **C10:** whether CSIRT constituency type is a type of operator. It was read as the type of the networks each CSIRT serves (a military network, a research and education network). A stricter reading sees the CSIRT as an intermediary, and C10 then fails criterion 2.
3. **C02 and C15** were excluded on criterion 2, but they're close: C02 breaks remediation down by device type (servers against routers) and by country, and has one five-contact remark about internet service providers; C15 measures patching per hosting provider and uses provider size as a control for abuse, not as a breakdown of patching.

## Excluded, with reason

| Code | Document | Venue, year | Reason |
|---|---|---|---|
| C01 | NDSS 2018 notification study (known document) | NDSS 2018 | full text unavailable: HTTP 404 at a URL built from the venue's file pattern, not from a search result, so the document is unread. That's no evidence it's unavailable elsewhere (note 2) |
| C02 | Li and others, "You've Got Vulnerability: Exploring Effective Vulnerability Notifications" | USENIX Security 2016 | fails 2: remediation broken down by message, channel, country, protocol and device type, not by operator size, capacity or type (borderline, above) |
| C03 | Stock and others, "Hey, You Have a Problem: On the Feasibility of Large-Scale Web Vulnerability Notification" | USENIX Security 2016 | fails 2: fixes broken down by channel; site popularity is discussed only for reachability |
| C04 | Verizon, 2025 Data Breach Investigations Report | report, 2025 | fails 2: edge-device remediation given overall ("only about 54% ... fully remediated", median 32 days, contributors' data covering "10,000 companies"); its sections on size concern incidents, not remediation |
| C05 | Cyentia Institute with Kenna Security, Prioritization to Prediction vol. 3 | report, 2019 | full text not retrieved: the GET returned the publisher's summary page; the report PDF it links was not fetched (one GET per document) |
| C06 | Cyentia Institute with Kenna Security, Prioritization to Prediction vol. 2 | report, 2019 | full text not retrieved, as C05 |
| C09 | Stivala and others, "Behind the Curtain: How Shared Hosting Providers Respond to Vulnerability Notifications" | arXiv 2025 | fails 1: interviews alone (24 hosting providers, August 2024 to June 2025); context only |
| C11 | Dissanayake and others, "Why, How and Where of Delays in Software Security Patch Management" | arXiv 2022 (Proc. ACM HCI, CSCW) | fails 2: one operator and its contractor; delays by team, phase and reason |
| C12 | Maass and others, "Snail Mail Beats Email Any Day" | arXiv 2021 (ARES 2021) | fails 2: remediation by channel and issue type |
| C13 | Dalela and others, "A Mixed-method Study on Security and Privacy Practices in Danish Companies" | arXiv 2021 | fails 1: practices reported by SMEs and large firms, but none is the deployment of an available fix or feature; context only |
| C14 | Dissanayake and others, "Software Security Patch Management - A Systematic Literature Review" | arXiv 2020 | fails 1 and 2: a review of challenges and solutions (72 studies, 2002 to March 2020) |
| C15 | Tajalizadehkhoob and others, "Herding Vulnerable Cats" | arXiv 2017 | fails 2: patching described across 1,259 providers; size is a control for abuse, not a breakdown of patching (borderline, above) |

## Context only (nothing counted)

Labelled as context, as the brief allows for documents excluded as explaining without measuring:

- C09, interview accounts: providers' protections vary "widely based on provider size and whether hosting is in-house or outsourced"; providers serving large businesses or public administration "demonstrated significantly greater attention to security". Interviewees are not identified here.
- C11: the authors name coordination delays as the most prominent cause, in two anonymised healthcare organisations.
- C05, the publisher's summary page (not the report): "smaller firms tend to fix faster than larger ones" and "Whatever their size, firms close about one in 10 open vulnerabilities per month", on "nearly 300 organizations", "Kenna Security customers". This is vendor material, asserted on a summary page with no method or period shown. It's the only by-size remediation statement met in this read, and it comes from an unread report.

## Notes

1. **Identifying the known notification studies.** The brief names "the USENIX Security 2016 and NDSS 2018 notification studies", and scout 5's note gives "Stock et al. USENIX Security 2016 and Li et al. NDSS 2018". The 2016 study by Stock and others (C03) was taken as the known USENIX one. Li and others' USENIX 2016 paper (C02) came back from Q4 as its own candidate. For NDSS 2018, the paper fetched at C01 was the one by Stock and others (a file path built from memory). The scout's author attribution for NDSS 2018 couldn't be checked, because the GET returned 404.
2. **Walls and gaps.** One wall (C01), under the brief's threshold of five. C05 and C06 were spent on summary pages because the search results pointed there. A dated amendment could allow a GET of a report PDF already linked from a page that has been read, but that would be a decision taken after reading, labelled post hoc, and the fifteen GETs are spent. As things stand, the series' report text is unread.
3. **What this read can't say.** Three inclusions in six searches and fifteen documents describe what this read found. They're no picture of the literature, and they're no evidence that by-size measurements are rare.

## Revision of 26 November 2026, after evidence review R-0150

Added by the driving session's revision of the record to version 0.2; the tables above are left as the read made them.

- **C08 excluded** under criterion 1 (R-0150, M1): the security model in use is a self-applied label for an architecture, not the deployment of a published fix or feature as the brief defines one. Included: 2 (C07, C10); excluded: 13. Claims: 5, all measured, 4 of them vendor (C07). C08-a is no longer a claim; C08 is context only.
- **C07-b and C07-c corrected** (R-0150, M2): the key findings say "While higher SSL and IPv4 counts correlate with PQC support, adoption density thins as network size increases, reflecting the complexity of migrating legacy infrastructure"; section IV.C says "As the number of IPv4 addresses increases, the density of entities achieving 100% PQC support thins out", read from a scatter with no rate or test. C07-b now covers SSL active count (IV.C) and SSL active and IPv4 counts (key findings); C07-c is fewer entities with 100% coverage as IPv4 count rises. Quotations as R-0150 took them from its reread of the same bytes.
- **C10:** the numbers per type are not stated in the paper (not "not checked"), as far as R-0150 found.
- **Licence wording** (R-0150, N7): "none of the fifteen states a licence allowing redistribution" means none was found in the text read; fetch_read.py searched the first 20,000 characters of each text, and arXiv's abstract pages were not fetched.
- **The "body_removed" field** in every derived file is scripts/lh_fetch.py's stock sentence, which cites robots.txt or page reservation; the actual reason is in each file's "body_kept" field and in fetchlog.csv: no redistribution licence found (R-0150, N8). The derived files are not rewritten; the fix belongs in `write_derived`.
