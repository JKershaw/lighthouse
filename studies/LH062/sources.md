# LH062 sources

**In short.** The documents LH062 considered, from six searches and two known documents, read on 27 November 2026 by a Watch subagent on Claude Opus 5.5 (row LH062-search-read). Nine candidates reached the register: three venue, six vendor. Six were read with one gated GET each; three vendor report pages were refused by the publisher's robots.txt before any request and are unavailable. Five documents were included (three venue, two vendor) and one vendor post was excluded on reading. Nothing here is a finding yet: the record will set the claims side by side.

Each read is one row in [fetchlog.csv](fetchlog.csv); each search in [searches.md](searches.md); claims in [claims.csv](claims.csv); the facts used in [derived/](derived/). No body is kept (PDFs never; the HTML pages state no licence allowing redistribution).

## Venue stream (nine GETs available; three used)

| Id | Document | Venue and version read | Read | Decision |
|---|---|---|---|---|
| A07 (V1, D01) | Demir, Vekaria, Smaragdakis and Durumeric, "Keys on Doormats: Exposed API Credentials on the Web" | arXiv 2603.12498 v3 of 14 September 2026, cs.CR; the text states ACM CCS 2026. https://arxiv.org/pdf/2603.12498 | 2026-11-27T14:17:08Z, HTTP 200, SHA-256 matches LH061's | **Included.** Known document, outcomes seen before the brief (LH061); no independent confirmation of LH061's reading. Claims V-A07-1 to V-A07-5 |
| A02 (V2, D02) | Meli, McNiece and Reaves, "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories" | NDSS 2019. https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf | 2026-11-27T14:17:09Z, HTTP 200, SHA-256 matches LH061's | **Included.** Known document, not returned under its own title by any query; outcomes seen before the brief; no independent confirmation. Claims V-A02-1, V-A02-2. Validity over time not measured by this study |
| B1 (V3, D03) | Baskaran, Zhao, Mannan and Youssef, "Measuring the Leakage and Exploitability of Authentication Secrets in Super-apps: The WeChat Case" | arXiv 2307.09317 v1 of 18 July 2023, cs.CR; the text states RAID 2023 (not one of the five), so arXiv tier. https://arxiv.org/pdf/2307.09317 (Q5 #1) | 2026-11-27T14:17:09Z, HTTP 200 | **Included.** Claims V-B1-1 to V-B1-3. A study of one platform's mini-apps: only its whole-population figures are kept. Its analysis framework and exploitability analysis are not recorded |

## Vendor stream (three GETs plus six passed from the venue stream; three used)

| Id | Document | Publisher, date | Read | Decision |
|---|---|---|---|---|
| W1 (D04) | The State of Secrets Sprawl Report 2026. https://gitguardian.com/state-of-secrets-sprawl-report-2026 | GitGuardian, 2026 | 2026-11-27T14:19:07Z: robots.txt refused (group Claude-User, Disallow: /) before any request | **Unavailable** (no GET used); unread, not evidence of anything |
| W2 (D05) | State of Secrets Sprawl report 2025. https://www.gitguardian.com/state-of-secrets-sprawl-report-2025 | GitGuardian, 2025 | 2026-11-27T14:19:08Z: robots.txt refused (as W1) | **Unavailable** |
| W3 (D06) | State of Secrets Sprawl report 2024. https://gitguardian.com/state-of-secrets-sprawl-report-2024 | GitGuardian, 2024 | 2026-11-27T14:19:08Z: robots.txt refused (as W1) | **Unavailable** |
| W4 (D07) | "74% of publicly leaked keys are never revoked". https://trufflesecurity.com/blog/most-publicly-leaked-keys-are-never-revoked | Truffle Security Co., Joe Leon, 10 January 2024 (data 28 September to 17 November 2023) | 2026-11-27T14:19:08Z, HTTP 200 | **Included** (vendor). Claims W-W4-1 to W-W4-3. Whether owners were notified is not stated. The brief knew these figures as relayed "TruffleHog's 2023 figures"; the post is dated 2024 |
| W5 (D08) | "Why Most Exposed Secrets Never Get Fixed". https://blog.gitguardian.com/why-exposed-secrets-stay-valid (redirected with a trailing slash, robots-checked) | GitGuardian, Anna Nabiullina, 5 June 2025 | 2026-11-27T14:19:09Z, HTTP 200 | **Excluded:** fails condition 3, no stated method (how exposure and validity were established is not described); it relays W2, which is unavailable |
| W6 (D09) | "Zombie Leaks: Unrevoked Secrets Lurking on GitHub". https://blog.gitguardian.com/zombie-leaks/ | GitGuardian, Thomas Segura, 29 April 2024 | 2026-11-27T14:19:10Z, HTTP 200 | **Included** (vendor), narrowly: method stated only as repeated validity checks over five days after the vendor's alert; population a frame without a count. Claims W-W6-1, W-W6-2, relayed by the vendor from W3, which is unavailable |

## Candidates not read

None: all nine candidates were read or found unavailable. Six of the twelve GETs were used.

## Excluded unread on search metadata

Listed with reasons in [searches.md](searches.md): a USENIX Security 2019 PDF and an arXiv PDF whose results showed no title, two NSF public-access links and an NDSS page with no title, two ConPro 2020 workshop papers, a TU Delft repository file, a KIT repository file, an IACR ePrint paper, an FTC event copy, a personal-site paper on users' views of breaches, a page on account compromise, a company publications page on stolen credentials, and a vendor advice post. News and secondary pages and third-party copies were locators only and were not fetched.

## Leads seen on pages read, not candidates

The two GitGuardian blog pages read list, among related articles, a post of 23 November 2026 on five months of the vendor's notification programme for companies. Truffle Security's page links a programme for revoking exposed secrets. Neither was returned by a query, so neither is a candidate under the brief; neither was opened. They are recorded only so a later study can decide whether to look.
