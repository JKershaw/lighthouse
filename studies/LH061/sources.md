# LH061 source register

**In short.** This is the list of every document the study's searches and named series put forward, and what happened to each when we tried to read it, as of the search-and-read row of 25 November 2026. For containment (Part A), six documents were read in full and included: five peer-reviewed papers or preprints that say they were published, plus one preprint, all but one measuring outcomes in the field. For recovery exercises (Part B), only two reports could be read and included, and neither measures an outcome: their claims are participants' own answers or the organisers' statements. Two of the five named exercise series couldn't be read at all, so the readable set may lean towards openly published reports. All of this is unreviewed; the record, its review and any line on the investigation page come later, as the brief sets out.

Compiled by a reading subagent in Claude Code (Claude Opus 5.5) on 25 November 2026, from searches.md, fetchlog.csv, derived/ and claims.csv in this folder. Every read was one gated one-off GET through scripts/lh_fetch.py (access 'oneoff', redirects checked, provider anthropic). No body is kept: each document read has a derived file in derived/ holding its URL, read time, status, SHA-256, the facts used and short quotations. The one document with an open licence (A07, CC BY 4.0) is a PDF whose compressed streams hold author email addresses that the redaction can't reach, so its body was not kept either. Nothing from LH060's register overlaps (its register.md and searches.md, read on 25 November, name none of these documents).

## Counts

| | Part A | Part B |
|---|---|---|
| Candidates | 9 | 11 slots (5 named series × 2 editions, plus 1 admitted series) |
| Located | 8 (one known document had no URL) | 8 (3 not located) |
| Document GETs used | 8 of up to 11 | 5 of up to 9 (plus the 3 Part A passed on, unused) |
| Robots refusals, no GET | 0 | 3 |
| Walls among GETs | 1 (HTTP 301) | 2 (HTTP 403) |
| Full text read | 6 | 3 |
| Included | 6 | 2 |
| Excluded after a GET | 2 (one wall, one page with no full text) | 3 (two walls, one fails condition 1) |
| Not read | 1 (no URL) | 6 (3 refused by robots.txt, 3 not located) |
| Claims recorded | 20: 18 measured outcome, 1 modelled, 1 asserted | 12: 0 measured outcome, 8 self-reported, 4 asserted |

13 document GETs and 4 locator requests were made (one more locator was refused before any request); 7 of the 20 document GETs were left unused because both candidate lists were exhausted. Walls and robots refusals together: 6 (three walls, three refusals), which isn't more than the brief's six; but two or more named series couldn't be read (Cyber Storm, both editions walled; Cyber Europe, refused by robots.txt; Locked Shields, no public report located), so the brief's bias statement applies to Part B. Part B has fewer than three included documents and no measured outcome claim, so both of those inconclusive conditions apply to it. None of Part A's inconclusive conditions on numbers applies: six documents included, 18 measured claims, of which 2 rest on vendor telemetry and 2 on laboratory settings.

## Part A, included

**A01. Alowaisheq, Wang, Alrwais, Liao, Wang, Alowaisheq, Mi, Tang and Liu, "Cracking the Wall of Confinement: Understanding and Analyzing Malicious Domain Take-downs".** NDSS Symposium 2019, peer reviewed (24 to 27 February 2019). Read 25 November 2026 at https://cse.buffalo.edu/faculty/xmi/files/ndss19_domain_takedown.pdf (an author's copy; QA2 result 1; known document). Measure: domain takedown by sinkholing or delisting. Population and unit: 625,692 seized domains (608,557 sinkholed, 21,757 delisted), the domain. Outcome: how long domains stayed taken down, how many were released for purchase again, re-registration and confirmed reuse. Window: passive DNS over about six years to early 2018; registrar availability queried twice weekly from October 2017 to May 2018. Data public: no (commercial passive DNS, WHOIS from an industry partner). Funder: US National Science Foundation grants, as stated. Claims A01-1 to A01-5, all measured, field. The paper also reports weaknesses in how some takedowns were run; under the brief these aren't restated. Derived: derived/A01-alowaisheq-ndss2019.json.

**A02. Meli, McNiece and Reaves, "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories".** NDSS Symposium 2019, peer reviewed. Read 25 November 2026 at https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf (the symposium's copy; known document; the URL was the reader's, not a search result's, and answered 200). Measure: the repository owner's removal of a leaked secret, which the study counts as taking content down; it doesn't measure providers' revocation, as the gate recalled. Inclusion is a judgement for review. Population: secrets found through GitHub's Search API and monitored from 4 April 2018 (count not stated in the section read). Outcome: share removed over time, and whether removal ended exposure. Window: hourly for a day, then daily to 16 days. Data public: inputs public, derived data not stated. Claims A02-1 and A02-2, measured, field. Derived: derived/A02-meli-ndss2019.json.

**A05. Nadji, Antonakakis, Perdisci, Dagon and Lee, "Beheading Hydras: Performing Effective Botnet Takedowns".** ACM CCS 2013, peer reviewed (4 to 8 November 2013). Read 25 November 2026 at https://coeus.ece.gatech.edu/articles/rza-ccs2013.pdf (QA1 result 4; known document). Measure: botnet takedowns by domain seizure and sinkholing, three studied after the fact, and a recommendation system. Population: aggregate daily successful DNS lookups at one large North American ISP; 45 active botnets for the recommendations. Window: 14 days around takedowns of 26 September 2011, 25 March 2012 and 11 September 2012. Data public: no. Interest: one author's employer was a security company that tracked the 45 botnets. Claims A05-1, A05-3 and A05-4 measured, field; A05-2 asserted; A05-5 modelled, vendor. Derived: derived/A05-nadji-ccs2013.json.

**A07. Demir, Vekaria, Smaragdakis and Durumeric, "Keys on Doormats: Exposed API Credentials on the Web".** arXiv 2603.12498, v3 of 14 September 2026 (screened as a preprint on search metadata; the v3 text states publication in the proceedings of ACM CCS 2026). Read 25 November 2026 at https://arxiv.org/pdf/2603.12498 (QA3 result 1; known document). Licence: CC BY 4.0, as stated. Measure: removal and revocation of exposed API credentials, unprompted and after the authors' notifications. That notification outcome is removal or revocation, not patching, so LH060's exclusion doesn't apply. Population: 1,748 verified credentials for 14 providers in HTTP Archive's September 2025 crawl. Window: nine HTTP Archive snapshots; after disclosure, daily for 14 days and on day 172. Data public: input crawl public. The paper describes affected organisations generally; nothing is recorded that could identify them. Claims A07-1 to A07-4, measured, field. Derived: derived/A07-arxiv2603.12498.json.

**A08. Kaya, Bozoğlan and Gündoğdu, "When an AI agent makes a mistake in a database, what decides the damage?"** arXiv 2611.30483 v1, 23 November 2026, preregistered (OSF), records on Zenodo as stated. Read 25 November 2026 at https://arxiv.org/pdf/2611.30483 (known document). Recorded, as the brief directs, for its recoverability outcome only: engine-native undo and vendors' minimum backups tested in a laboratory. Inclusion is a judgement for review, since recovery from damage sits at the edge of the containment definition. The agents were six small open-weight models, not Anthropic's or OpenAI's. Data public: yes, as stated. Claims A08-1 and A08-2, measured, laboratory. Derived: derived/A08-arxiv2611.30483.json.

**A09. Ife, Shen, Murdoch and Stringhini, "Marked for Disruption: Tracing the Evolution of Malware Delivery Operations Targeted for Takedown".** arXiv 2104.01631 v3, 7 July 2021 (screened as a preprint; the text states RAID 2021, 6 to 8 October 2021). Read 25 November 2026 at https://arxiv.org/pdf/2104.01631 (QA1 result 10). Measure: a DNS sinkhole operation and two seizure operations against three malware delivery operations in late 2015. Population: global download metadata from a security vendor's product telemetry. Window: October 2015 to September 2016. Data public: no. Interest: one author was employed by the vendor. Claims A09-1 and A09-2, measured, field, vendor. How the operations responded is not restated, under the brief. Derived: derived/A09-arxiv2104.01631.json.

## Part A, excluded after a GET

**A03. Kim, Kwon, Kozák, Gates and Dumitraș, "The Broken Shield: Measuring Revocation Effectiveness in the Windows Code-Signing PKI"** (USENIX Security 2018, as the page names it). The search result URL (QA3 result 9) redirected to the authors' project page, which gives the abstract and links but not the full text. Excluded: full text unavailable through the one GET allowed. Nothing is claimed from the abstract. Derived: derived/A03-kim-usenix2018.json.

**A04. Asghari, Ciere and van Eeten, "Post-mortem of a Zombie: Conficker Cleanup After Six Years"** (USENIX Security 2015; known document). GET of https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-asghari.pdf on 25 November 2026: HTTP 301 with no body, its Location header naming the same URL. Recorded as a wall and not retried. Unread, which isn't evidence about its findings.

## Part A, candidate not read

**A06. The Cloud Security Alliance's note of October 2026 on leaked-credential survival** (known document from scout 5's relay). No URL came from the searches or the scouts' logs, and the brief allows locator reads only for exercise series, so it wasn't located or read.

## Part B, included

**B07. SIFMA, "SIFMA QDVII After-Action Report" (Quantum Dawn VII), prepared with a consulting firm.** Named series, preceding edition. Read 25 November 2026 at https://www.sifma.org/wp-content/uploads/2024/04/SIFMA-Quantum-Dawn-VII_Public-AAR-FINAL.pdf (QB1 result 8). Publication date not stated in the document (uploaded under a 2024/04 path). Exercise: 14 to 16 November 2023, more than 1,000 participants from over 170 financial institutions in more than 20 countries. The scenario was a multi-day outage at a fictional critical third party after a data disruption event. Inclusion on condition 1 (a cyber incident) is a judgement for review: SIFMA runs it as a cybersecurity exercise series and frames it within "significant operational outages such as a cyber incident". Outcome claims: 3 self-reported (B07-1 to B07-3, from anonymous in-exercise polls, respondent count not stated) and 1 asserted (B07-4). Measured time to restore a service: no. Follow-up of earlier recommendations: the design "Incorporated after actions and lessons learned from Quantum Dawn VI (2021)"; no follow-up of implementation reported. Derived: derived/B07-quantumdawn-vii.json.

**B11. Public Safety Canada, "Cyber-Physical Capstone Exercise After-Action Report".** Admitted series (the first other series in QB1's results; a report of results on the organiser's own site). Read 25 November 2026 at https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/cpstn-xrcs-ftr-ctn-rprt-2024/index-en.aspx (QB1 result 6). Page modified 2024-07-25. Exercise: a national multi-sector virtual exercise, 24 to 26 October 2023, about 150 organisations and over 650 players; day three was on recovering data and restoring services. Method: polls, chat, feedback, a post-exercise questionnaire and a hotwash on 2 November 2023, from players, evaluators and controllers. Outcome claims: 5 self-reported, 3 asserted (B11-1 to B11-8). Exercise delivery counts, such as 848 scenario injects, are recorded in the derived file but aren't outcome claims. Measured time to restore a service: no. Follow-up of earlier recommendations: not stated (a pilot with no earlier edition). Derived: derived/B11-canada-capstone-2024.json.

## Part B, excluded after a GET

**B04. Bank of England, "SIMEX 24 - A major market-wide simulation exercise to test the UK financial sector's resilience to a major operational disruption"** (news release, 2 October 2024). Read 25 November 2026 at https://www.bankofengland.co.uk/news/2024/october/simex-24-testing-the-uk-financial-sector-resilience. Excluded, a judgement for review. The page describes the scenario as "a major infrastructure failure that would require a total shut down and restart of the sector" and never as a cyber incident, so condition 1 fails on the document read. It's also a news release without results. The brief expected it to be included as an assurance-only case if it met the three conditions; a reviewer may read the scenario differently. It reports no outcome either way. Derived: derived/B04-simex24.json.

**B01. CISA, Cyber Storm IX After-Action Report** (latest edition located; file dated October 2024). GET on 25 November 2026: HTTP 403 (access denied by the site's edge). A wall, unread.

**B06. CISA, Cyber Storm VIII After-Action Report** (August 2022; preceding edition). GET on 25 November 2026: HTTP 403. A wall, unread.

## Part B, candidates not read

**B02. SIFMA, Quantum Dawn VIII After-Action Report** (latest edition; exercise 4 to 6 November 2025; edition page published 30 March 2026). The organiser's edition page links the report at a host whose robots.txt disallows every path to every agent. Refused before any request; not read. The same file name wasn't tried on SIFMA's main host, because that would route around a refusal.

**B03. ENISA, Cyber Europe 2024 After-Action Report.** Refused by robots.txt before any request: ENISA's robots.txt has a group for Claude-User with "Disallow: /", the group that governs a one-off read. Not read.

**B08. ENISA, Cyber Europe 2022 After-Action Report** (preceding edition). Refused by the same rule. The URL was built by analogy with the 2024 one, and no request was made.

**B09. Bank of England, SIMEX 22** (preceding edition). Not located. The SIMEX 24 page doesn't link it. The one locator read allowed for SIMEX (a Bank of England page the reader guessed) redirected to an error path that robots.txt disallows.

**B05 and B10. NATO CCDCOE, Locked Shields 2026 and 2025.** Not located. The series page (https://ccdcoe.org/exercises/locked-shields/, read as a locator on 25 November 2026) gives 2026 participation figures but links no report of results.

## Named series: what was found

| Series | Latest edition's report | Preceding edition's report |
|---|---|---|
| Cyber Storm (CISA) | IX (2024): wall, HTTP 403. The series locator page also answered 403, so whether a later edition's report exists wasn't checked | VIII (2022): wall, HTTP 403 |
| Quantum Dawn (SIFMA) | VIII (November 2025): robots refusal at the linked host | VII (November 2023): read, included |
| Cyber Europe (ENISA) | 2024: robots refusal (whether a 2026 report exists wasn't checked; the locator was refused too) | 2022: robots refusal |
| SIMEX (Bank of England and UK authorities) | SIMEX 24 page: read, excluded (not described as a cyber incident; no results) | SIMEX 22: not located |
| Locked Shields (NATO CCDCOE) | no public report located | no public report located |

Admitted series: one, Public Safety Canada's Cyber-Physical exercise (B11). No other QB result met the admission rule: older editions of the named series aren't other series, a third-party archive isn't the organiser's site, and the theses, workshop paper and preprint aren't peer-reviewed evaluations as the search metadata showed them.

## Context, not counted

None was opened. The search tool's summaries named vendor figures (a takedown vendor's phishing takedown times; a secret-scanning vendor's credential survival figures) and a 2025 Web Conference study. These are locators only under the brief, and nothing is claimed from them.
