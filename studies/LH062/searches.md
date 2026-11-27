# LH062 searches

**In short.** The six searches the brief fixes, run once each, verbatim, with the Claude Code harness's WebSearch tool (mode "standard") on 27 November 2026 by a Watch subagent on Claude Opus 5.5 (run 2026-11-27T141100Z-anthropic-watch, row LH062-search-read). Each result is listed with its title, URL, venue and year as the tool showed them, the screening decision made on that metadata, and whether it was opened. The tool's prose summaries are not retained (the brief: snippets are not retained); they were not used to screen, and where a summary attributed a figure to a source, that is a relay, not a reading.

Times are UTC from `date -u`, taken immediately before each call. "Year" is as the metadata shows it; "not shown" where the title and URL give none. Every opened document is one gated GET logged in [fetchlog.csv](fetchlog.csv).

Screening rule (brief, "Screen, on search metadata"): a candidate belongs to a stream, falls in 2015 to 14 December 2026, and its title or URL plausibly concerns exposed credentials followed over time. Results whose title is a bare host or URL fragment, with no title shown, were screened on the URL alone; where the URL gives no sign of the topic or the venue they are excluded unread with that reason. A preprint and its published version, and several copies of one document, are one candidate.

Decision recorded on 27 November 2026 before any document was read, where the brief left it open: in the vendor stream, "most recent first" is applied to the year the metadata shows; candidates whose metadata shows no year follow those with a year, in order of first appearance.

## Q1, 2026-11-27T14:14:18Z

`exposed credentials removal revocation longitudinal measurement study`

| # | Title as shown | URL | Venue, year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | License: arXiv.org perpetual non-exclusive license | https://arxiv.org/html/2603.12498v1 | arXiv, 2026 (id) | Copy of A07 (one candidate) | No (A07 read at the brief's URL) |
| 2 | License: arXiv.org perpetual non-exclusive license | https://arxiv.org/html/2603.12498v2 | arXiv, 2026 (id) | Copy of A07 | No |
| 3 | arxiv.org | https://arxiv.org/pdf/2603.12498v2 | arXiv, 2026 (id) | Copy of A07 | No |
| 4 | Keys on Doormats: Exposed API Credentials on the Web | https://arxiv.org/pdf/2603.12498 | arXiv, 2026 (id) | **Candidate V1 = A07** (known document, returned) | Yes, D01 |
| 5 | Keys on Doormats: Exposed API Credentials on the Web | https://www.alphaxiv.org/abs/2603.12498.md | third-party copy | Copy of A07; third-party site, not fetched | No |
| 6 | most publicly leaked keys are never revoked | https://trufflesecurity.com/blog/most-publicly-leaked-keys-are-never-revoked | vendor's own site (Truffle Security), year not shown | **Candidate W4** (vendor) | Yes, D07 |
| 7 | Keys on Doormats: Exposed API Credentials on the Web | https://www.alphaxiv.org/abs/2603.12498 | third-party copy | Copy of A07, not fetched | No |
| 8 | google account compromise | https://faculty.cc.gatech.edu/~frankli/papers/google_account_compromise.pdf | not shown | Excluded unread: venue not shown; title concerns account compromise, no sign of exposed credentials followed for removal or revocation | No |
| 9 | why exposed secrets stay valid | https://blog.gitguardian.com/why-exposed-secrets-stay-valid | vendor's own site (GitGuardian), year not shown | **Candidate W5** (vendor) | Yes, D08 |
| 10 | Data breaches, phishing, or malware? Understanding the risks of stolen credentials | https://research.google/pubs/data-breaches-phishing-or-malware-understanding-the-risks-of-stolen-credentials/ | company publications page; venue and year not shown | Excluded unread: title concerns the sources and risk of stolen credentials, no sign of removal or revocation over time; venue not shown | No |

## Q2, 2026-11-27T14:14:26Z

`leaked secrets public repositories how long remain valid measurement`

| # | Title as shown | URL | Venue, year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | most publicly leaked keys are never revoked | https://trufflesecurity.com/blog/most-publicly-leaked-keys-are-never-revoked | vendor | Candidate W4 (repeat) | Yes, D07 |
| 2 | www.bleepingcomputer.com | https://www.bleepingcomputer.com/news/security/over-543-000-valid-credentials-exposed-in-public-github-repositories/amp/ | news | Neither (news): locator only, not fetched | No |
| 3 | why exposed secrets stay valid | https://blog.gitguardian.com/why-exposed-secrets-stay-valid | vendor | Candidate W5 (repeat) | Yes, D08 |
| 4 | state of secrets sprawl report 2025 | https://www.gitguardian.com/state-of-secrets-sprawl-report-2025 | vendor, 2025 | **Candidate W2** (vendor) | Robots refusal, no GET (D05) |
| 5 | Introducing Forrester's AEGIS Framework: Agentic AI Enterprise Guardrails For Information Security | https://gitguardian.com/state-of-secrets-sprawl-report-2024 | vendor, 2024 (URL) | **Candidate W3** (vendor; the URL names the 2024 report, the shown title is a site banner) | Robots refusal, no GET (D06) |
| 6 | the persistence problem why exposed | https://thehackernews.com/2025/05/the-persistence-problem-why-exposed.html | news, 2025 | Neither (news): locator only | No |
| 7 | How Bad Is Secrets Leakage on GitHub? | https://www.securityscientist.net/blog/secrets-leakage-github/ | secondary blog | Neither (secondary coverage): locator only | No |
| 8 | zombie leaks | https://blog.gitguardian.com/zombie-leaks/ | vendor, year not shown | **Candidate W6** (vendor) | Yes, D09 |
| 9 | the persistence problem why exposed | https://thehackernews.com/2025/05/the-persistence-problem-why-exposed.html?m=1 | news | Neither (news), duplicate | No |
| 10 | over 543 000 valid credentials exposed in public github repositories | https://bleepingcomputer.com/news/security/over-543-000-valid-credentials-exposed-in-public-github-repositories | news | Neither (news): locator only | No |

## Q3, 2026-11-27T14:14:33Z

`exposed API keys notification revocation measurement study`

| # | Title as shown | URL | Venue, year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | arxiv.org | https://arxiv.org/pdf/2603.12498v2 | arXiv | Copy of A07 | No |
| 2 | License: arXiv.org perpetual non-exclusive license | https://arxiv.org/html/2603.12498v2 | arXiv | Copy of A07 | No |
| 3 | License: arXiv.org perpetual non-exclusive license | https://arxiv.org/html/2603.12498v1 | arXiv | Copy of A07 | No |
| 4 | File 125c8967 5670 4932 a9cf 725de66f25fb | https://repository.tudelft.nl/file/File_125c8967-5670-4932-a9cf-725de66f25fb | university repository, year not shown | Excluded unread: outside the streams (a university repository file, not one of the five conferences or arXiv; no conference shown) | No |
| 5 | most publicly leaked keys are never revoked | https://trufflesecurity.com/blog/most-publicly-leaked-keys-are-never-revoked | vendor | Candidate W4 (repeat) | Yes, D07 |
| 6 | Keys on Doormats: Exposed API Credentials on the Web | https://www.alphaxiv.org/abs/2603.12498.md | third-party copy | Copy of A07, not fetched | No |
| 7 | theregister.com | https://theregister.com/devops/2026/05/21/threat-hunters-find-google-api-keys-still-usable-23-minutes-after-deletion/5244504 | news, 2026 | Neither (news): locator only. It names a vendor's research that no query returned from the vendor's own site, so no candidate arises | No |
| 8 | truffle security launches program to revoke 14 million live secrets | https://bleepingcomputer.com/news/security/truffle-security-launches-program-to-revoke-14-million-live-secrets | news | Neither (news): locator only | No |
| 9 | Google API Keys Remain Active After Deletion | https://www.darkreading.com/identity-access-management-security/google-api-keys-active-after-deletion%0A | news | Neither (news): locator only | No |
| 10 | arxiv.org | https://arxiv.org/abs/2603.12498v2 | arXiv | Copy of A07 (abstract page, not fetched) | No |

## Q4, 2026-11-27T14:14:44Z

`leaked credentials disclosure notification remediation response rate study`

| # | Title as shown | URL | Venue, year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | Data Breaches: User Comprehension, Expectations, | https://elie.net/static/files/data-breaches-user-comprehension-expectations-and-concerns-with-handling-exposed-data/data-breaches-user-comprehension-expectations-and-concerns-with-handling-exposed-data-paper.pdf | personal site; venue and year not shown | Excluded unread: title shows a study of users' comprehension and expectations of breaches, not exposed credentials followed for removal or revocation; venue not shown | No |
| 2 | breaches conpro2020 | https://users.ece.cmu.edu/~lbauer/papers/2020/breaches-conpro2020.pdf | ConPro 2020 (URL) | Excluded unread: outside the streams (ConPro, a workshop, is not one of the five conferences) | No |
| 3 | Keys on Doormats: Exposed API Credentials on the Web | https://arxiv.org/pdf/2603.12498 | arXiv | Candidate V1 = A07 (repeat) | Yes, D01 |
| 4 | arxiv.org | https://arxiv.org/pdf/2010.09853.pdf | arXiv, 2020 (id) | Excluded unread: no title shown and the URL gives no sign of the topic | No |
| 5 | pwds breach conpro20 | https://users.cs.northwestern.edu/~srutib/papers/pwds-breach-conpro20.pdf | ConPro 2020 (URL) | Excluded unread: outside the streams (workshop) | No |
| 6 | sec19 thomas | https://usenix.org/system/files/sec19-thomas.pdf | USENIX Security 2019 (URL) | Excluded unread: no title shown and the URL gives no sign that it concerns exposed credentials followed over time | No |
| 7 | publikationen.bibliothek.kit.edu | https://publikationen.bibliothek.kit.edu/1000132793/155647009 | university repository | Excluded unread: outside the streams; no title shown | No |
| 8 | SecurityBrief UK | https://securitybrief.co.uk/story/compromised-credential-monitoring-lags-threat-awareness | news | Neither (news): locator only | No |
| 9 | Thousands of Chrome Users Won't Change Passwords They Know Are Hacked | https://www.tomsguide.com/news/thousands-of-chrome-users-wont-change-passwords-they-know-are-hacked | news | Neither (news): locator only | No |
| 10 | now im a bit angry individuals awareness perception and responses to data | https://www.Ftc.Gov/system/files/documents/public_events/1582978/now_im_a_bit_angry_-_individuals_awareness_perception_and_responses_to_data.pdf | government event copy | Excluded unread: outside the streams; title shows individuals' awareness and responses to breaches | No |

## Q5, 2026-11-27T14:15:06Z

`hardcoded secrets still valid over time measurement study`

| # | Title as shown | URL | Venue, year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | Measuring the Leakage and Exploitability of Authentication Secrets in Super-apps: The WeChat Case | https://arxiv.org/pdf/2307.09317 | arXiv, 2023 (id) | **Candidate V3** (venue, arXiv; category or acceptance to be shown by the PDF). Title is a measurement of leakage, not only a technique, so not excluded unread | Yes, D03 |
| 2 | why exposed secrets stay valid | https://blog.gitguardian.com/why-exposed-secrets-stay-valid | vendor | Candidate W5 (repeat) | Yes, D08 |
| 3 to 6 | the persistence problem why exposed (four URL variants) | https://thehackernews.com/2025/05/the-persistence-problem-why-exposed.html?hl=ru ; ?hl=en ; ?m=1 ; (plain) | news | Neither (news): locator only | No |
| 7 | 69b806d852984f61b37e9520 State of Secrets Sprawl 2026 | https://nhimg.org/wp-content/uploads/2026/03/69b806d852984f61b37e9520_State-of-Secrets-Sprawl-2026.pdf | third-party site | A third-party copy of a vendor report, not on the vendor's own site: locator only, not fetched (the vendor's own page is W1) | No |
| 8 | The State of Secrets Sprawl Report 2026 | https://gitguardian.com/state-of-secrets-sprawl-report-2026 | vendor, 2026 | **Candidate W1** (vendor) | Robots refusal, no GET (D04) |
| 9 | Public GitHub code reveals a major issue: over 500,000 secret keys are exposed | https://cybernews.com/security/github-exposed-credentials-contain-thousands-gemini-keys/ | news | Neither (news): locator only | No |
| 10 | www.bleepingcomputer.com | https://www.bleepingcomputer.com/news/security/over-543-000-valid-credentials-exposed-in-public-github-repositories/amp/ | news | Neither (news), repeat | No |

## Q6, 2026-11-27T14:15:20Z

`NDSS USENIX Security CCS IMC leaked secrets revocation after notification`

| # | Title as shown | URL | Venue, year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | par.nsf.gov | https://par.nsf.gov/servlets/purl/10515486 | public access repository; no title, venue or year shown | Excluded unread: no title, venue or year shown | No |
| 2 | how to reduce time to revoke for exposed credentials | https://blog.gitguardian.com/how-to-reduce-time-to-revoke-for-exposed-credentials | vendor, year not shown | Excluded unread: title shows advice, not a measurement | No |
| 3 | truffle security launches program to revoke 14 million live secrets | https://bleepingcomputer.com/news/security/truffle-security-launches-program-to-revoke-14-million-live-secrets | news | Neither (news), repeat | No |
| 4 | Paper 2017/234 | https://eprint.iacr.org/2017/234 | IACR ePrint | Excluded unread: outside the streams; no title shown | No |
| 5 | zombie leaks | https://blog.gitguardian.com/zombie-leaks/ | vendor | Candidate W6 (repeat) | Yes, D09 |
| 6 | Paper 2017/234 | https://eprint.iacr.org/2017/234/20170520:110117 | IACR ePrint | Duplicate of row 4 | No |
| 7 | most publicly leaked keys are never revoked | https://trufflesecurity.com/blog/most-publicly-leaked-keys-are-never-revoked | vendor | Candidate W4 (repeat) | Yes, D07 |
| 8 | nhimg.org | https://nhimg.org/?p=99215 | third-party site | Neither: locator only | No |
| 9 | par.nsf.gov | https://par.nsf.gov//servlets/purl/10429456 | public access repository; nothing shown | Excluded unread: no title, venue or year shown | No |
| 10 | www.ndss symposium | https://www.ndss-symposium.org/?p=4568 | NDSS site; no title or year shown | Excluded unread as its own candidate: no title shown. It may be a page for a known document; A02 is read at the brief's URL whatever this is | No |

## Candidate register and reading order (fixed before the first GET)

Venue stream (up to nine GETs): tier 1, conference papers, most recent first: **V1** A07 (arXiv 2603.12498, its v3 text as LH061 read it states ACM CCS 2026; returned by Q1), **V2** A02 (NDSS 2019; known, not returned under its own title). Tier 2, arXiv not stated as accepted: **V3** arXiv 2307.09317 (2023), moved to tier 1 only if its text states acceptance at one of the five, which would not change its place since it is the only remaining candidate. Three candidates, so six venue GETs pass to the vendor stream.

Vendor stream (three GETs plus six passed over): year shown first, most recent first: **W1** GitGuardian State of Secrets Sprawl 2026 (2026), **W2** the 2025 report (2025), **W3** the 2024 report (2024); then year not shown, by first appearance: **W4** Truffle Security "most publicly leaked keys are never revoked" (Q1 #6), **W5** GitGuardian "why exposed secrets stay valid" (Q1 #9), **W6** GitGuardian "zombie leaks" (Q2 #8).

Total candidates: 9 (3 venue, 6 vendor), all within the ceiling of twelve GETs.

## Outcome of reading

Six GETs used of twelve (three venue, three vendor); three vendor candidates refused by robots.txt before any request (no GET). Included: A07, A02, arXiv 2307.09317 (venue); Truffle Security 10 January 2024, GitGuardian 29 April 2024 (vendor). Excluded on reading: GitGuardian 5 June 2025 (no stated method). See [sources.md](sources.md).
