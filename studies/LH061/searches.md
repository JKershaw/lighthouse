# LH061 searches

**In short.** The brief's eight searches, run once each and verbatim on 25 November 2026 with the WebSearch tool of the Claude Code harness (standard mode), in the brief's order. Each result is listed with its title and URL as the tool returned them; the tool showed no venue or year for any result, so "venue, year" below is what the title or URL itself shows, or "not shown". "Opened" means a gated GET of that URL for this study (see fetchlog.csv); everything else was not opened. Snippets and the tool's own summaries are not retained, and nothing in them is used as a source. Screening (candidate or not, and why) follows the brief's rule on metadata only.

Run by a reading subagent in Claude Code (Claude Opus 5.5) for the queue row LH061-search-read. No query errored; none was reworded, added or rerun. Before the reads, robots.txt was consulted for several planned URLs through the gate's check (robots.txt only, no page request); those checks are not GETs and are not in the fetch log.

## QA1, 2026-11-25T14:15:15Z

Query: `botnet takedown effectiveness measurement infection rates before and after`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | File 3f4fd3f9 4f5f 499c 8ed8 def06614af92 | https://repository.tudelft.nl/file/File_3f4fd3f9-4f5f-499c-8ed8-def06614af92 | not shown (university repository) | no | not a candidate: title and venue not shown. It may be a copy of the Conficker cleanup paper, which enters anyway as a known document |
| 2 | www.eweek.com | https://www.eweek.com/?p=58759 | news | no | locator only (news) |
| 3 | par.nsf.gov | https://par.nsf.gov/servlets/purl/10314559 | not shown (public-access repository) | no | not a candidate: title and venue not shown |
| 4 | rza ccs2013 | https://coeus.ece.gatech.edu/articles/rza-ccs2013.pdf | ACM CCS, 2013 (from file name) | yes (A05) | candidate, Part A, peer reviewed (known document: Nadji and others) |
| 5 | Hits top-three botnet Pushdo/Cutwail hard; researchers expect spam rebound | https://www.computerworld.com/article/1556071/spam-drops-15-after-ftc-pulls-plug-on-rogue-isp.html | news | no | locator only (news) |
| 6 | Rustock Botnet Size Nearly Halved Since Server Takedown: Microsoft | https://www.eweek.com/networking/rustock-botnet-size-nearly-halved-since-server-takedown-microsoft/ | news | no | locator only (news relaying a vendor's figures) |
| 7 | Beheading Hydras - Performing Effective Botnet Takedowns | https://astrolavos.gatech.edu/2013/11/14/beheading_hydras/ | lab page, 2013 | no | same candidate as #4 (page about the paper) |
| 8 | Beheading Hydras - Performing Effective Botnet Takedowns | https://coeus.ece.gatech.edu/2013/11/14/beheading_hydras | lab page, 2013 | no | same candidate as #4 |
| 9 | The war on botnets | https://www.itpro.com/637312/the-war-on-botnets | news | no | locator only (news) |
| 10 | Marked for Disruption: Tracing the Evolution of Malware Delivery Operations Targeted for Takedown | https://ar5iv.labs.arxiv.org/html/2104.01631 | arXiv 2104.01631 (2021, from the identifier) | read at https://arxiv.org/pdf/2104.01631 (A09) | candidate, Part A, arXiv tier (metadata gives arXiv; the text read states RAID '21) |

## QA2, 2026-11-25T14:15:24Z

Query: `domain sinkholing takedown outcome longitudinal measurement study`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | ndss19 domain takedown | https://cse.buffalo.edu/faculty/xmi/files/ndss19_domain_takedown.pdf | NDSS, 2019 (from file name) | yes (A01) | candidate, Part A, peer reviewed (known document: the NDSS 2019 domain takedown study) |
| 2 | Cracking the Wall of Confinement: Understanding and Analyzing Malicious Domain Take-downs | https://cse.buffalo.edu/faculty/xmi/publication/ndss19_domain_takedown/ | author page | no | same candidate as #1 |
| 3 | ndss symposium | https://ndss-symposium.org/?p=4697 | NDSS | no | same candidate as #1 (record page) |
| 4 | cracking the wall of confinement understanding and analyzing malicious domain take downs | https://www.ndss-symposium.org/ndss-paper/cracking-the-wall-of-confinement-understanding-and-analyzing-malicious-domain-take-downs | NDSS | no | same candidate as #1 |
| 5 | cracking the wall of confinement understanding and analyzing mali | https://experts.illinois.edu/en/publications/cracking-the-wall-of-confinement-understanding-and-analyzing-mali/ | university record | no | same candidate as #1 |
| 6 | dev.ndss symposium | https://dev.ndss-symposium.org/?p=4697 | NDSS | no | same candidate as #1 |
| 7 | cracking the wall of confinement understanding and analyzing malicious domain take downs | https://dev.ndss-symposium.org/ndss-paper/cracking-the-wall-of-confinement-understanding-and-analyzing-malicious-domain-take-downs | NDSS | no | same candidate as #1 |
| 8 | skip to main content | https://par.nsf.gov/biblio/10097935 | not shown | no | not a candidate: title not shown (may be a record of #1) |
| 9 | skip to main content | https://par.nsf.gov/search/author:"Liu, Baojun" | search page | no | not a candidate |
| 10 | arxiv.org | https://arxiv.org/pdf/2403.19368 | arXiv 2403.19368 (2024, from the identifier) | no | not a candidate: no title shown, so it cannot be screened as concerning the question |

## QA3, 2026-11-25T14:15:33Z

Query: `leaked credentials revocation measurement study time to revocation`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | Keys on Doormats: Exposed API Credentials on the Web | https://arxiv.org/pdf/2603.12498 | arXiv 2603.12498 (2026) | yes (A07) | candidate, Part A, arXiv tier (known document) |
| 2 | abstract davidwardle | https://royalholloway.ac.uk/media/9087/abstract-davidwardle.pdf | university page | no | not a candidate: not a listed venue |
| 3 | how to measure time to revoke for exposed credentials jwab87dk1 | https://daily.dev/posts/how-to-measure-time-to-revoke-for-exposed-credentials-jwab87dk1 | aggregator post | no | locator only |
| 4 | How to Reduce Time to Revoke for Exposed Credentials | https://blog.gitguardian.com/author/ben/ | vendor blog | no | locator only (vendor) |
| 5 | google account compromise | https://faculty.cc.gatech.edu/~frankli/papers/google_account_compromise.pdf | not shown | no | not a candidate: venue not shown |
| 6 | publica.fraunhofer.de | https://publica.fraunhofer.de/handle/publica/458497 | not shown | no | not a candidate: title and venue not shown |
| 7 | www.royalholloway.ac.uk | https://www.royalholloway.ac.uk/media/9136/davidwardleisg.pdf | university page | no | not a candidate: not a listed venue |
| 8 | how to reduce time to revoke for exposed credentials | https://blog.gitguardian.com/how-to-reduce-time-to-revoke-for-exposed-credentials | vendor blog | no | locator only (vendor) |
| 9 | The Broken Shield: | https://users.umiacs.umd.edu/~tdumitra/signedmalware/usenix18/usenix18.html | USENIX Security, 2018 (from URL path) | yes (A03); the URL returned the project page, not the paper | candidate, Part A, peer reviewed (revocation of abused code-signing certificates) |
| 10 | arxiv.org | https://arxiv.org/pdf/2603.12498v2 | arXiv 2603.12498 v2 | no | same candidate as #1 |

## QA4, 2026-11-25T14:15:42Z

Query: `phishing or malware site takedown speed measurement study`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | www.cl.cam.ac.uk | https://www.cl.cam.ac.uk/~rnc1/takedown.pdf | not shown | no | not a candidate: venue and year not shown in the metadata (the writer believes it to be a 2008 workshop paper, which would be outside the years; not checked) |
| 2 | Your Phishing Takedown Program Looks Active. But Is It Protecting Anyone? | https://www.netcraft.com/blog/phishing-takedown | vendor blog | no | locator only (vendor) |
| 3 | The Ultimate Guide to Domain Takedown Services in 2026 | https://www.netcraft.com/blog/the-ultimate-guide-to-domain-takedown-services | vendor blog | no | locator only (vendor) |
| 4 | The 72-Hour Problem: Why DMCA Takedowns Can't Protect Customers Fast Enough | https://www.netcraft.com/blog/dmca-takedowns-72-hour-problem | vendor blog | no | locator only (vendor) |
| 5 | Netcraft removes phishing attacks in less than half the industry average time | https://www.netcraft.com/blog/netcraft-removes-phishing-attacks-in-less-than-half-the-industry-average-time | vendor blog | no | locator only (vendor) |
| 6 | 12 min read | https://www.netcraft.com/blog/the-definitive-guide-on-leading-phishing-takedown-providers | vendor blog | no | locator only (vendor) |
| 7 | Netcraft threat detection and takedown platform | https://www.netcraft.com/cybercrime/fraud-detection/ | vendor page | no | locator only (vendor) |
| 8 | lightbluetouchpaper.org | https://lightbluetouchpaper.org/?p=239 | blog | no | locator only (blog) |
| 9 | Netcraft threat detection and takedown platform | https://www.netcraft.com/cybercrime | vendor page | no | locator only (vendor) |
| 10 | Brand and executive protection | https://cyble.com/articles/?p=484 | vendor page | no | locator only (vendor) |

## QA5, 2026-11-25T14:15:51Z

Query: `incident containment effectiveness empirical evaluation isolation quarantine`

All ten results concern public-health isolation and quarantine, not cyber containment; none is a candidate.

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | Evidence-Based Practice for Public Health Emergency Preparedness and Response (2020) | https://www.nationalacademies.org/read/25650/chapter/17 | National Academies, 2020 | no | not a candidate: off topic, not a listed venue |
| 2 | nationalacademies.org | https://www.nationalacademies.org/docs/DF24EA23527E4D442CF26F52E2216C7959DB3A747783 | not shown | no | not a candidate |
| 3 | nih.gov | https://ncbi.nlm.nih.gov/books/NBK563999 | not shown | no | not a candidate |
| 4 | pmc.ncbi.nlm.nih.gov | https://pmc.ncbi.nlm.nih.gov/articles/5393248 | not shown | no | not a candidate |
| 5 | nationalacademies.org | https://www.nationalacademies.org/docs/DB36857704386A302E89DC07F48E72DB2515AE3F0BDE | not shown | no | not a candidate |
| 6 | pmc.ncbi.nlm.nih.gov | https://pmc.ncbi.nlm.nih.gov/articles/PMC7109638 | not shown | no | not a candidate |
| 7 | new outbreaks of coronavirus can be halted with isolation measures according to study | https://insights.som.yale.edu/insights/new-outbreaks-of-coronavirus-can-be-halted-with-isolation-measures-according-to-study | university news | no | not a candidate |
| 8 | pmc.ncbi.nlm.nih.gov | https://pmc.ncbi.nlm.nih.gov/articles/PMC2808319 | not shown | no | not a candidate |
| 9 | Evidence-Based Practice for Public Health Emergency Preparedness and Response (2020) | https://www.nationalacademies.org/read/25650/chapter/10 | National Academies, 2020 | no | not a candidate |
| 10 | apps.dtic.mil | https://apps.dtic.mil/sti/pdfs/AD1099456.pdf | not shown | no | not a candidate: title not shown |

## QB1, 2026-11-25T14:16:02Z

Query: `cyber exercise after-action report findings cross-sector recovery`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | Cyber%20Storm%20IX%20After Action%20Report%20v00%2020241001 508 | https://cisa.gov/sites/default/files/2024-10/Cyber%20Storm%20IX%20After-Action%20Report%20v00%2020241001_508.pdf | CISA, 2024 | yes (B01): HTTP 403 | candidate, named series, Cyber Storm, latest edition located |
| 2 | CS VI AAR Final Approved | https://www.cisa.gov/sites/default/files/publications/CS_VI_AAR_Final_Approved.pdf | CISA | no | named series, older edition: not a candidate (only latest and preceding) |
| 3 | final cyber storm viii after action report 082022 | https://www.cisa.gov/sites/default/files/2023-02/final-cyber-storm-viii-after-action-report-082022.pdf | CISA, 2022 | yes (B06): HTTP 403 | candidate, named series, Cyber Storm, preceding edition |
| 4 | Document 09 | https://nsarchive.gwu.edu/sites/default/files/documents/3035772/Document-09.pdf | third-party archive | no | not a candidate: not the organiser's site |
| 5 | Cyber-Physical Capstone Exercise After-Action Report | https://publicsafety.gc.ca/cnt/rsrcs/pblctns/cpstn-xrcs-ftr-ctn-rprt-2024 | Public Safety Canada, 2024 | no (same document as #6) | admitted series 1 (first other series in QB results) |
| 6 | Cyber-Physical Capstone Exercise After-Action Report | https://www.publicsafety.gc.ca/cnt/rsrcs/pblctns/cpstn-xrcs-ftr-ctn-rprt-2024/index-en.aspx | Public Safety Canada, 2024 | yes (B11) | candidate, admitted series |
| 7 | Cyber Storm 2020 After Action Report 01052021 Final | https://www.cisa.gov/sites/default/files/publications/Cyber_Storm-2020_After-Action-Report_01052021_Final.pdf | CISA, 2021 | no | named series, older edition: not a candidate |
| 8 | SIFMA Quantum Dawn VII Public AAR FINAL | https://www.sifma.org/wp-content/uploads/2024/04/SIFMA-Quantum-Dawn-VII_Public-AAR-FINAL.pdf | SIFMA, 2024 | yes (B07) | candidate, named series, Quantum Dawn, preceding edition |
| 9 | Cybersecurity Exercise: Quantum Dawn VIII | https://www.sifma.org/resources/readiness-exercises/cybersecurity-exercise-quantum-dawn-viii | SIFMA | yes, as the Quantum Dawn locator (L2) | shows that the latest edition is VIII (November 2025); its report is the candidate (B02) |
| 10 | Cybersecurity Exercise: Quantum Dawn VII | https://sifma.org/resources/general/cybersecurity-exercise-quantum-dawn-vii | SIFMA | no | edition page; the edition's report (#8) is the candidate |

## QB2, 2026-11-25T14:16:13Z

Query: `"after-action report" national cyber exercise recovery coordination results`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | Cyber%20Storm%20IX%20After Action%20Report%20v00%2020241001 508 | (as QB1 #1) | CISA, 2024 | see QB1 | duplicate |
| 2 | final cyber storm viii after action report 082022 | (as QB1 #3) | CISA, 2022 | see QB1 | duplicate |
| 3 | CyberStormV AfterActionReport 2016vFinal %2520508%2520Compliant%2520v2 | https://www.cisa.gov/sites/default/files/publications/CyberStormV_AfterActionReport_2016vFinal-%2520508%2520Compliant%2520v2.pdf | CISA, 2016 | no | older edition: not a candidate |
| 4 | Cyber Storm 2020 After Action Report 01052021 Final | (as QB1 #7) | CISA, 2021 | no | duplicate |
| 5 | CS VI AAR Final Approved | (as QB1 #2) | CISA | no | duplicate |
| 6 | Document 09 | https://nsarchive.gwu.edu/sites/default/files/documents/3035772/Document-09.pdf | third-party archive | no | not a candidate |
| 7 | cisa.gov | https://www.cisa.gov/sites/default/files/publications/Lessons%20Learned%20from%20Cyber%20Storm%20IV.pdf | CISA | no | older edition: not a candidate |
| 8 | Document 09 | https://nsarchive.gwu.edu/sites/default/files/documents/2995027/Document-09.pdf | third-party archive | no | not a candidate |
| 9 | nsarchive.gwu.edu | https://nsarchive.gwu.edu/media/21978/ocr | third-party archive | no | not a candidate |
| 10 | Document 04 Department of Homeland Security | https://nsarchive.gwu.edu/sites/default/files/documents/2805488/Document-04-Department-of-Homeland-Security.pdf | third-party archive | no | not a candidate |

## QB3, 2026-11-25T14:16:23Z

Query: `evaluation of multi-organisation cyber crisis exercise outcomes study`

| # | Title as shown | URL | Venue, year as shown | Opened | Screening |
|---|---|---|---|---|---|
| 1 | www.enisa.europa.eu | https://www.enisa.europa.eu/sites/default/files/publications/WP2018%20O.4.1.1%20CE2018%20After%20Action%20Report.pdf | ENISA, 2018 | no | named series (Cyber Europe), older edition: not a candidate |
| 2 | enisa.europa.eu | https://enisa.europa.eu/publications/cyber-europe-2018-after-action-report/@@download/fullReport | ENISA, 2018 | no | as #1 |
| 3 | enisa.europa.eu | https://enisa.europa.eu/publications/ce2016-after-action-report/@@download/fullReport | ENISA, 2016 | no | older edition: not a candidate |
| 4 | theses.gla.ac.uk | https://theses.gla.ac.uk/7553/1/2016ArniyatiAphd.pdf | thesis, 2016 | no | not a candidate: a thesis, not a peer-reviewed venue |
| 5 | ceur-ws.org | https://ceur-ws.org/Vol-4134/paper8.pdf | CEUR-WS workshop proceedings | no | not a candidate: peer review not shown in the metadata, venue not a listed or emergency-management venue |
| 6 | phaidra.fhstp.ac.at | https://phaidra.fhstp.ac.at/api/object/o:5804/get | university repository | no | not a candidate |
| 7 | Annex%20D%20Case study CE2014 PDF.pdf | https://enisa.europa.eu/sites/default/files/all_files/Annex%20D%20Case_study_CE2014_PDF.pdf | ENISA, 2014 | no | older edition: not a candidate |
| 8 | 2017 27 06%20CE2016%20After%20action%20report | https://www.enisa.europa.eu/sites/default/files/publications/2017-27-06%20CE2016%20After%20action%20report.pdf | ENISA, 2017 | no | older edition: not a candidate |
| 9 | Multimodal Analytics of Cybersecurity Crisis Preparation Exercises: What Predicts Success? | https://arxiv.org/pdf/2603.28553 | arXiv, 2026 | no | not a candidate: a preprint, and Part B admits only peer-reviewed evaluations |
| 10 | A cyber exercise post assessment framework : in Malaysia perspectives | https://katalog.lib.cas.cz/KNAV/EdsRecord/edsndl,edsndl.bl.uk.oai.ethos.bl.uk.695127 | library catalogue (thesis record) | no | not a candidate |
