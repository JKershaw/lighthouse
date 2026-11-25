# LH060 searches, 25 November 2026

**In short.** The brief's six searches were run once each, verbatim, with the WebSearch tool of Claude Code (Claude Opus 5.5, Anthropic) on 25 November 2026, between 14:14:50Z and 14:15:42Z, in order Q1 to Q6 (the six calls were made together after a clock read at 14:14:50Z; the next clock read was 14:15:42Z, so each query's own minute isn't recorded). They gave 15 candidates once the known documents were added. Each was then fetched once (see [register.md](register.md) and [fetchlog.csv](fetchlog.csv)). A search result is a lead, never a source, and nothing here is a finding. The tool showed a title and URL for each result, plus a summary paragraph written by the tool. Venue and year were rarely shown. Where this table gives them from the URL alone (an arXiv identifier, a proceedings path), it says so. Snippets and the tool's summaries are not retained. Unreviewed.

No query failed. None was reworded, added or rerun. Mode: "standard".

Screening (brief, "Screen, on search metadata"): a result becomes a candidate if it's in a listed venue, in 2012 to 2026, and its title or snippet plausibly concerns operators' deployment or remediation of security fixes or features. A result whose title the tool didn't show (a bare file or URL label) can't be screened on its title. It isn't a candidate, and the table says so (a routine decision taken here). News, blogs, vendor pages and press releases are locators only. "Opened" means the document was fetched. The candidate code shows which fetch, and that fetch may have gone to a different URL for the same document.

## Q1 `hosting providers patch deployment provider size measurement study`

| # | Title as shown | URL | Venue / year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | File 2820cd46 09c6 446b bb78 fbef546cc546 | https://repository.tudelft.nl/file/File_2820cd46-09c6-446b-bb78-fbef546cc546?preview=1 | not shown (university repository) | not a candidate: no title shown, venue not shown | no |
| 2 | Herding Vulnerable Cats: A Statistical Approach to Disentangle Joint Responsibility for Web Security in Shared Hosting | https://ar5iv.arxiv.org/html/1708.06693 | arXiv (from URL), 2017 (from identifier) | candidate (C15) | yes, as C15 via arxiv.org/pdf |
| 3 | arxiv.org | https://arxiv.org/abs/1708.06693 | arXiv | same candidate as #2 | as C15 |
| 4 | Computer Science > Cryptography and Security | https://web3.arxiv.org/abs/1708.06693 | arXiv | same candidate as #2 | as C15 |
| 5 | Herding Vulnerable Cats: ... (as #2) | https://ui.adsabs.harvard.edu/abs/2017arXiv170806693T/abstract | catalogue entry for the arXiv record | same candidate as #2 | as C15 |
| 6 | arxiv.org | https://arxiv.org/html/2512.01891 | arXiv, 2025 (from identifier) | candidate (C09); title shown under Q4 | yes, as C09 |
| 7 | arxiv.org | https://arxiv.org/html/2512.01891v1 | arXiv | same as #6 | as C09 |
| 8 | skip to main content | https://doi.org/10.1145/3613904.3642456 | not shown (an ACM DOI) | not a candidate: no title or snippet shown | no |
| 9 | How shared hosting providers responded to PHP2Shell | https://cybernews.com/best-web-hosting/how-shared-web-hosting-providers-responded-to-php2shell/ | news | locator only; names no listed-venue document | no |
| 10 | www.comp.nus.edu.sg | https://www.comp.nus.edu.sg/~bleong/p2pft/related/gkantsidis06planet.pdf | not shown; "06" in file name | not a candidate: no title; file name suggests 2006, outside years | no |
| 11 | File e5253582 c86d 4bab 95df 1f906461a472 | https://repository.tudelft.nl/file/File_e5253582-c86d-4bab-95df-1f906461a472?preview=1 | not shown | not a candidate: no title shown | no |
| 12 | www.ieee-security.org | https://www.ieee-security.org/TC/SP2015/papers-archived/6949a692.pdf | IEEE S&P 2015 (from URL) | not a candidate: no title or snippet shown | no |
| 13 | the patch reality gap how fast smbs really patch and what are the risks | https://www.acronis.com/en/tru/posts/the-patch-reality-gap-how-fast-smbs-really-patch-and-what-are-the-risks.md | vendor blog | locator only | no |
| 14 | Why vulnerability reports stall inside shared hosting companies | https://www.helpnetsecurity.com/?p=351211 | news | locator only (covers #6) | no |
| 15 | Start trial | https://patchstack.com/articles/hosting-security-tested-87-percent-of-vulnerability-exploits-bypassed-hosting-defenses/ | vendor page | locator only | no |

## Q2 `vulnerability remediation time by organization size empirical study`

| # | Title as shown | URL | Venue / year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | There May Be a Ceiling on Vulnerability Remediation | https://www.darkreading.com/vulnerabilities---threats/there-may-be-a-ceiling-on-vulnerability-remediation/d/d-id/1334142? | news | locator only (Kenna/Cyentia report) | no |
| 2 | organizations take two months to patch critical vulnerabilities | https://betanews.com/2022/03/07/organizations-take-two-months-to-patch-critical-vulnerabilities/ | news, 2022 (from URL) | locator only | no |
| 3 | big or small organizations typically remediate 1 of 10 of discovered vulnerabilities | https://www.scworld.com/news/big-or-small-organizations-typically-remediate-1-of-10-of-discovered-vulnerabilities | news | locator only (Kenna/Cyentia report) | no |
| 4 | (as #3) | https://www.scworld.com/home/security-news/big-or-small-organizations-typically-remediate-1-of-10-of-discovered-vulnerabilities/ | news | locator only | no |
| 5 | www.cyentia.com | https://www.cyentia.com/?p=13164 | Cyentia site; no title | not a candidate: no title shown | no |
| 6 | time to close the remediation gap | https://blog.barracuda.com/2019/11/04/time-to-close-the-remediation-gap | vendor blog, 2019 (from URL) | locator only | no |
| 7 | Prioritization to Prediction, Vol 3: Wade's Take | https://www.cyentia.com/p2p-vol3-wade/ | Cyentia blog post | locator for Prioritization to Prediction vol. 3 (C05) | no |
| 8 | SAN FRANCISCO, March 12, 2019 (GLOBE NEWSWIRE) -- | https://www.globenewswire.com/news-release/2019/03/12/1751746/0/en/More-Resources-Don-t-Lead-to-Better-or-Faster-Vulnerability-Management-Kenna-Security-Report-Finds.html | press release, 2019 | locator only (vol. 3) | no |
| 9 | Patching, Fast and Slow | https://www.cyentia.com/patching-fast-and-slow/ | Cyentia; the tool described it as a "post" | locator only: shown as a blog post, not a report (a routine decision taken here) | no |
| 10 | Table of Contents | https://www.blackduck.com/?p=29747 | vendor page | locator only | no |

## Q3 `security feature adoption small organizations versus large measurement`

| # | Title as shown | URL | Venue / year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | cg a001 png eng | https://www150.statcan.gc.ca/n1/daily-quotidien/140611/cg-a001-png-eng.htm | national statistics office, 2014 (from URL) | not a candidate: not a listed venue | no |
| 2 | ora.ox.ac.uk | https://ora.ox.ac.uk/objects/uuid:d6261db8-cbbe-4d55-83b2-6246fe7a3c33/files/med8ca56aa5d2d9690c1b4bd196ce33da | not shown | not a candidate: no title shown | no |
| 3 | Empirical Study of Post-Quantum Cryptography Adoption Status in SSH Infrastructure | https://arxiv.org/pdf/2611.09703 | arXiv, 2026 (from identifier) | candidate (C07) | yes, as C07 |
| 4 | new must know security research for midsize organizations\" | https://news-blogs.cisco.com/author/carriebaker/feed/... (malformed) | vendor blog | locator only | no |
| 5 | Rate of IT security incidents grows with company size | https://www.helpnetsecurity.com/2022/06/23/security-incidents-company-size/ | news, 2022 | locator only | no |
| 6 | new must know security research for midsize organizations | https://news-blogs.cisco.com/security/new-must-know-security-research-for-midsize-organizations | vendor blog | locator only | no |
| 7 | A Mixed-method Study on Security and Privacy Practices in Danish Companies | https://arxiv.org/pdf/2104.04030 | arXiv, 2021 (from identifier) | candidate (C13) | yes, as C13 |
| 8 | Most Small to Mid-Sized Organizations Don't Use Multi-Factor Authentication | https://www.esecurityplanet.com/networks/most-small-to-mid-sized-organizations-dont-use-multi-factor-authentication/ | news | locator only (names a vendor survey, not a listed venue) | no |
| 9 | IDG Research looks at this year's IT security priorities | https://www.csoonline.com/article/3249552/idg-research-large-organisations-budgets-hire-cisos.html | news | locator only | no |
| 10 | Towards Zero Trust Architecture: A Pilot Study on Information Systems Security Readiness amongst Small and Medium Enterprises | https://arxiv.org/pdf/2605.18901 | arXiv, 2026 (from identifier) | candidate (C08) | yes, as C08 |

## Q4 `vulnerability notification campaign remediation rate by operator type`

| # | Title as shown | URL | Venue / year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | Snail Mail Beats Email Any Day: On Effective Operator Security Notifications in the Internet | https://arxiv.org/pdf/2106.08024 | arXiv, 2021 (from identifier) | candidate (C12) | yes, as C12 |
| 2 | usesec16 notify | https://faculty.cc.gatech.edu/~mbailey/publications/usesec16_notify.pdf | USENIX Security 2016 (from file name; the same paper as #8) | candidate (C02) | yes, as C02 via the usenix.org PDF |
| 3 | arxiv.org | https://arxiv.org/abs/2512.1891 | arXiv (malformed identifier) | same as C09 | as C09 |
| 4 | arxiv.org | https://arxiv.org/abs/2512.01891v1 | arXiv | same as C09 | as C09 |
| 5 | arxiv.org | https://arxiv.org/html/2512.01891v1 | arXiv | same as C09 | as C09 |
| 6 | arxiv.org | https://arxiv.org/html/2512.01891 | arXiv | same as C09 | as C09 |
| 7 | Behind the Curtain: How Shared Hosting Providers Respond to Vulnerability Notifications | https://arxiv.org/pdf/2512.01891 | arXiv, 2025 (from identifier) | candidate (C09) | yes, as C09 |
| 8 | You've Got Vulnerability: Exploring Effective Vulnerability Notifications | https://usenix.org/conference/usenixsecurity16/technical-sessions/presentation/li | USENIX Security 2016 | candidate (C02) | yes, as C02 (paper PDF, not this abstract page) |
| 9 | Bondar2023 adminsSurvey madweb | https://perl.sce.carleton.ca/assets/pdfs/Bondar2023_adminsSurvey_madweb.pdf | file name suggests the MADWeb workshop, 2023 | not a candidate: venue not listed (a workshop, not NDSS's main symposium) | no |
| 10 | Don't Get Hijacked: Prevalence, Mitigation, and Impact of Non-Secure DNS Dynamic Updates | https://arxiv.org/pdf/2405.19871 | arXiv, 2024 (from identifier) | candidate (C10) | yes, as C10 |

## Q5 `patch management barriers small organizations capacity survey`

| # | Title as shown | URL | Venue / year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | patch management a key area for improvement at most smbs study shows | https://businessinsights.bitdefender.com/patch-management-a-key-area-for-improvement-at-most-smbs-study-shows | vendor blog | locator only | no |
| 2 | 2019 IT Operations Survey Results: Automated Patch Management Not Widely Adopted | https://www.kaseya.com/blog/2019-it-operations-survey-results-automated-patch-management-not-widely-adopted/ | vendor blog, 2019 | locator only | no |
| 3 | Missing Patches, Misconfiguration Top Technical Breach Causes | https://www.darkreading.com/vulnerabilities---threats/missing-patches-misconfiguration-top-technical-breach-causes/d/d-id/1337410 | news | locator only | no |
| 4 | www.kaseya.com | https://www.kaseya.com/?p=8391 | vendor | locator only | no |
| 5 | The Problem With Patching: 7 Top Complaints | https://www.darkreading.com/endpoint/the-problem-with-patching-7-top-complaints-/a/d-id/1325232 | news | locator only | no |
| 6 | 3 min read | https://www.bitdefender.com/en-au/blog/businessinsights/patch-management-a-key-area-for-improvement-at-most-smbs-study-shows | vendor blog | locator only | no |
| 7 | 3 min read | https://www.bitdefender.com/en-gb/blog/businessinsights/patch-management-a-key-area-for-improvement-at-most-smbs-study-shows | vendor blog | locator only | no |
| 8 | The Problem With Patching: 7 Top Complaints | https://www.darkreading.com/endpoint-security/the-problem-with-patching-7-top-complaints | news | locator only | no |
| 9 | File db000084 dbf5 455e b3d0 d065acf3f6be | https://repository.tudelft.nl/file/File_db000084-dbf5-455e-b3d0-d065acf3f6be | not shown (the tool described a master's thesis) | not a candidate: no title; a thesis is not a listed venue | no |
| 10 | www.infosecurity-magazine.com | https://www.infosecurity-magazine.com/news/patching-too-tortuous-for-it-pros/ | news | locator only | no |

## Q6 `vulnerability remediation by company size report Cyentia OR Kenna OR "Data Breach Investigations Report"`

| # | Title as shown | URL | Venue / year as shown | Screen | Opened |
|---|---|---|---|---|---|
| 1 | big or small organizations typically remediate 1 of 10 of discovered vulnerabilities | https://www.scworld.com/home/security-news/big-or-small-organizations-typically-remediate-1-of-10-of-discovered-vulnerabilities/ | news | locator only | no |
| 2 | (as #1) | https://www.scworld.com/news/big-or-small-organizations-typically-remediate-1-of-10-of-discovered-vulnerabilities | news | locator only | no |
| 3 | There May Be a Ceiling on Vulnerability Remediation | https://www.darkreading.com/vulnerabilities---threats/there-may-be-a-ceiling-on-vulnerability-remediation/d/d-id/1334142? | news | locator only | no |
| 4 | (as #1) | https://www.scmagazine.com/news/big-or-small-organizations-typically-remediate-1-of-10-of-discovered-vulnerabilities | news | locator only | no |
| 5 | www.slideshare.net | https://www.slideshare.net/MichaelRoytman/cybertecheuropepptx | slides | not a candidate: not a listed venue | no |
| 6 | SAN FRANCISCO, March 12, 2019 (GLOBE NEWSWIRE) -- | https://www.globenewswire.com/news-release/2019/03/12/1751746/0/en/More-Resources-Don-t-Lead-to-Better-or-Faster-Vulnerability-Management-Kenna-Security-Report-Finds.html | press release | locator only | no |
| 7 | (as #6) | https://rss.globenewswire.com/news-release/2019/03/12/1751746/0/en/More-Resources-Don-t-Lead-to-Better-or-Faster-Vulnerability-Management-Kenna-Security-Report-Finds.html | press release | locator only | no |
| 8 | www.cyentia.com | https://www.cyentia.com/?p=13164 | Cyentia; no title | not a candidate: no title shown | no |
| 9 | Should enterprises delay efforts to remediate most vulnerabilities? | https://www.helpnetsecurity.com/2019/01/23/delay-patching/ | news, 2019 | locator only | no |
| 10 | Prioritization to Prediction: Winning the Remediation Race | https://www.govinfosecurity.com/whitepapers/prioritization-to-prediction-winning-remediation-race-w-6389 | third-party white-paper listing | locator for vol. 3 (C05) | no |
| 11 | Enterprises Are Getting Smarter When It Comes to Patching Vulnerabilities – Study | https://darkreading.com/vulnerabilities-threats/enterprises-are-getting-smarter-when-it-comes-to-patching-vulnerabilities-study | news | locator only | no |
| 12 | Gotta Patch 'Em All? Not Necessarily, Experts Say | https://www.darkreading.com/vulnerabilities---threats/gotta-patch-em-all-not-necessarily-experts-say/d/d-id/1337228 | news | locator only | no |
| 13 | cyentia fast and frivolous 2 | https://securityscorecard.com/research/cyentia-fast-and-frivolous-2 | vendor site hosting a Cyentia item | not a candidate: the title doesn't plausibly concern remediation | no |
| 14 | Prioritization to Prediction, Vol. 3 | https://www.cyentia.com/?p=24352 | Cyentia Institute report (listed publisher), 2019 (prior knowledge; not shown) | candidate (C05) | yes, as C05 (the GET returned the summary page) |
| 15 | This resource is no longer available | https://bitpipe.computerweekly.com/detail/RES/1668502344_424.html | not shown | not a candidate | no |
| 16 | AuthorAbound, Jeff | https://law-journals-books.vlex.com/vid/do-most-vulnerabilities-pose-779118077 | law journal listing | not a candidate: not a listed venue | no |
| 17 | Prioritizing Vulnerabilities Is Key to Patching Success, Report Finds \| eWeek | https://www.eweek.com/de/security/prioritizing-vulnerabilities-is-key-to-patching-success-report-finds/ | news | locator only | no |
| 18 | Prioritization to Prediction, Vol. 2 | https://www.cyentia.com/?p=24354 | Cyentia Institute report (listed publisher), 2019 (prior knowledge; not shown) | candidate (C06) | yes, as C06 (the GET returned the summary page) |

The tool's summary for Q6 also mentioned a "Volume 4" of the series without any result naming it. It wasn't entered as a candidate, since no result's title or URL names it. The Verizon DBIR wasn't returned by any query. It entered as a known document (C04).
