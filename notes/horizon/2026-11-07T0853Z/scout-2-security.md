# Scout 2, Security and vulnerabilities, run 2026-11-07T0853Z

Started 2026-11-07 08:54 UTC, ended 2026-11-07 08:59 UTC. Every claim below is "reported by" the page named, not observed by Lighthouse, unless marked "fetched by scout" (a plain read of an API response).

## Searches

1. "Brotli CVE-2026-111497 decoder buffer overflow": osv.dev AZL-110384, osv.dev DEBIAN-CVE-2026-111497, security-tracker.debian.org/CVE-2026-111497, csoonline.com Node2Shell article, cipherssecurity.com, cve.threatint.com.
2. "AI model discovered vulnerability found by AI November 2026 CVE": nsfocusglobal.com, martincid.com Mythos, grc.com SN 1080 notes, foxxelabs (XBOW Windows CVE), threatcluster.io, vulert.com (SGLang), helpnetsecurity.com (66,000 CVEs), sonatype.com "AI Vulnerability Storm", hackread.com Mythos, blog.ogwilliam.com. None dated November; all April to August.
3. "WordPress CVE-2026-119977 core upgrade race condition exploited": socprime, picussecurity.com, pasqualepillitteri.it, bleepingcomputer.com, rescana, securityaffairs, dailysecurityreview, tech-insider.org, decryptiondigest, runtimewire (and others).
4. "Codex Security OpenAI vulnerability found Brotli Node.js disclosure": theregister.com/a/5305515, csoonline, remio.ai, runtimewire, toolnavs.
5. "Project Zero blog October 2026": projectzero.google welcome post, hackaday May 2026, Pixel 10 chain coverage. Nothing dated October.
6. "GitLab CVE-2026-97229 regular expression remote code execution exploited KEV": bleepingcomputer (two articles), getastra, socprime.
7. "NCSC UK OR CERT-EU security advisory November 2026 actively exploited": techzine (Ivanti EPMM), cloudswitched (NetScaler), cert.europa.eu advisories 2026, lovguiden.dk, vulnerabilities.ncsc.nl. Nothing from November.
8. "AI agent autonomously exploited vulnerability in the wild threat report November 2026": dev.to (Sysdig marimo), CSA notes (GTIG May, Zammad), threatcluster and craftedsignal (Hugging Face, July, disputed).
9. "Brotli exploitation in the wild OR scanning OR honeypot Node2Shell Imperva JFrog FFmpeg JPEG XL": securityweek, sentinelone, tanium, digg.
10. "critical vulnerability disclosed this week open source library proof-of-concept November 5 2026": mostly undated (protobuf.js, Exploitarium archive). Not opened.
11. "DIVD Zammad breach AI agent DIVD-2026-00014 csirt.divd.nl": CSA two notes, bleepingcomputer, sysdig.com blog, helpnetsecurity 1 October, securityaffairs, fleetdm, orcarouter.

Seen, not opened: all search-result pages not listed in the table below, including the Sysdig Zammad post, Help Net Security, SentinelOne and Tanium Node2Shell posts, Wordfence, Picus, and the CSA GTIG note.

## Sources read

| # | URL | Read (UTC) | Status | Page date | Claim reported |
|---|---|---|---|---|---|
| 1 | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | 2026-11-07 08:54 | HTTP 200 | catalogVersion 2026.11.06, released 2026-11-06 19:44Z | Catalogue holds 1769 entries; five added since 30 October: Ivanti Connect Secure CVE-2026-118527 and CVE-2026-111357 (30 Oct, chain with CVE-2026-104935), WordPress Core CVE-2026-119977 (3 Nov), Apple CVE-2024-27834 (4 Nov, pointer authentication bypass), SonicWall SonicOS SSLVPN CVE-2026-19868 (6 Nov, "may also bypass SAML-enforced multi-factor authentication (MFA)"). Added 23 to 29 Oct (fetched by scout): BeyondTrust Remote Support CVE-2026-102764 (16 Oct), Collabora CODE CVE-2026-110447 (23 Oct), Brotli CVE-2026-111497 (27 Oct), GitLab CVE-2026-97229 (29 Oct). |
| 2 | https://api.first.org/data/v1/epss (several queries, dates 2026-10-30 and 2026-11-06) | 08:55 | HTTP 200 | scores dated 2026-11-06 | Fetched by scout: among the 5000 highest scores per day, biggest rises in a week: BeyondTrust CVE-2026-102764 0.19 to 0.78; GitLab CVE-2026-97229 0.27 to 0.65; Adobe Commerce CVE-2026-75650 new at 0.35. WordPress CVE-2026-119977 rose 0.006 (3 Nov) to 0.0116 (5 Nov), a low score despite KEV listing. Pagination stopped at 5000 rows per query, so movers outside it are unseen. |
| 3 | https://cveawg.mitre.org/api/cve/CVE-2026-{102764,97229,111497,105134,105133,110447,75650,104935} | 08:55 | HTTP 200 | published 4 Sep to 22 Oct | CVE records give vendor and description; e.g. Collabora: "allows remote code execution, as exploited in the wild in September and October 2026"; Ahsay AhsayCBS CVE-2026-105133/105134 (auth bypass and OS command injection, published 4 Oct, EPSS about 0.8, not in KEV). |
| 4 | https://www.csoonline.com/article/4241027/node2shell-puts-microsoft-and-node-js-on-brotli-patch-duty.html | 08:56 | fetched | 21 to 25 Oct events | Node.js disclosed 21 Oct; researchers "doing security testing for OpenAI's Codex Security" reported it; .NET 8/9/10/11 patched out of band 25 Oct; self-contained and Native AOT apps must be rebuilt; public PoC works against Node.js 24.22.0. |
| 5 | https://www.theregister.com/a/5305515 | 08:56 | fetched | 26 Oct 2026 | Root cause "fixed in the Brotli source code in February" with no release and no recognition as a security flaw; Node.js, Python, Bun, Envoy, Istio patched; JFrog reportedly built an FFmpeg exploit via a JPEG XL image; Wiz says 91% of cloud environments rely on vulnerable components. |
| 6 | https://www.remio.ai/post/openai-brotli-vulnerability-disclosure-exposes-a-gap-between-fixed-code-and-prot | 08:56 | fetched | 24 Oct | "A source repository is a record of development, while a release is a packaged version offered to users." Secondary commentary. |
| 7 | https://www.securityweek.com/cisa-warns-of-node2shell-exploitation-as-honeypots-log-attack-attempts/ | 08:56 | fetched | 28 Oct 2026 | ELLIO and Previdian honeypots logged single attempts 25 to 27 Oct; ELLIO says the attacker's final stage "did not produce a shell in 50 tests" and the source IP ties to earlier PHP2Shell activity. |
| 8 | https://osv.dev/vulnerability/DEBIAN-CVE-2026-111497 | 08:56 | fetched | published 22 Oct, modified 6 Nov 19:00Z | Debian lists brotli, edk2, nodejs, python-brotlicffi as affected; many nodejs and edk2 builds with no fixed version. |
| 9 | https://pypi.org/pypi/{brotli,brotlicffi,brotlipy}/json and https://pypistats.org/api/packages/*/recent | 08:56 | HTTP 200 | read 7 Nov | Fetched by scout: brotli 1.2.1 uploaded 2026-10-22 13:57Z (previous 1.2.0 on 2025-11-05); brotlicffi 1.2.1.0 on 2026-10-22; pypistats last_month 82.8M (brotli), 1.66M (brotlicffi), 1.42M (brotlipy, last release 2017, unpatched). |
| 10 | https://www.bleepingcomputer.com/news/security/cisa-flags-wordpress-rce-flaw-as-actively-exploited-in-attacks/ | 08:56 | fetched | 4 Nov 2026 | WordPress 7.1.4 (28 Oct) fixes a TOCTOU in the core upgrade; Wordfence "blocked 13,095 attacks targeting this vulnerability in the past 24 hours"; CISA gave no detail on how it confirmed exploitation. |
| 11 | https://bleepingcomputer.com/news/security/over-1-000-gitlab-servers-vulnerable-to-code-execution-attacks | 08:56 | fetched | 2 Nov 2026 | Shadowserver: over 1000 GitLab instances vulnerable to CVE-2026-97229 (exploited, KEV) and over 11,300 to CVE-2026-110264, of about 39K seen daily; patches 12 Oct. |
| 12 | https://labs.cloudsecurityalliance.org/research/csa-research-note-zammad-ai-agent-breach-20261001-csa-styled/ | 08:57 | fetched | 1 Oct 2026 | DIVD "assessed that the attacker was an autonomous AI agent" that chained two Zammad zero-days (CVE-2026-102489, CVE-2026-102490) on 21 Sep; agent left explanatory code comments; secondary relay of DIVD. |
| 13 | https://api.osv.dev/v1/query (PyPI brotli) | 08:57 | HTTP 200 | read 7 Nov | Fetched by scout: OSV returns advisories for the PyPI brotli package (first was a Scrapy decompression-bomb entry; I did not check whether it lists CVE-2026-111497). |

Not opened or refused: api.github.com/advisories returned HTTP 403 ("sessions are bound to their configured repositories"), so GitHub's advisory database was not read. Project Zero, NCSC UK and CERT-EU pages were not opened (search showed nothing from October or November).

## Best leads

### 1. Brotli (CVE-2026-111497): how a decoder fix reaches the things that embed it
- Reported: Node.js disclosed 21 Oct, found by OpenAI Codex Security researchers (CSO, Register, 25 and 26 Oct); fixed upstream in February without a release, so the exploitable window predates the CVE; KEV 27 Oct, federal due date 10 Nov (CISA feed); honeypots saw a failed attempt 26 Oct (SecurityWeek, 28 Oct); Debian still lists nodejs and edk2 builds unfixed on 6 Nov (OSV).
- Why it matters: it is a patch wave through a shared, embedded library (Node, .NET, Python wheels, PHP Windows builds, Envoy, FFmpeg, container images), found by an AI-assisted team. It is the Python-release-propagation question applied to a compiled dependency that is statically linked, so updating a runtime may not replace it. Lighthouse already noted the PHP Windows rebuild (php-watch-log, 26 Oct) but not Brotli as its own subject.
- Time-sensitive: moderately. Federal deadline 10 Nov; ELLIO and honeypot histories, Shadowserver-style counts and image tags change daily; first weeks of adoption are being lost.
- Measure: PyPI and ClickPy daily downloads by version for brotli and brotlicffi (1.2.1 vs 1.2.0 shares) and wheels that bundle it; OSV and Debian fix dates per package; Docker Hub and base-image rebuild dates; npm packages vendoring brotli; the gap between the February commit and the 22 Oct release.
- Cost: one study (small to medium).
- Confidence: high that it is real; moderate that it is new to Lighthouse (partial overlap with the PHP watch).

### 2. An autonomous AI agent as the intruder: DIVD and Zammad
- Reported: CSA note of 1 Oct, relaying DIVD, says an agent chained two unknown Zammad flaws on 21 Sep, "loud and very, very messy", with commented code; search also showed BleepingComputer, Sysdig and Help Net Security coverage (not opened). CVE-2026-102489 had EPSS 0.22 and CVE-2026-102490 0.11 on 6 Nov (fetched by scout), not in KEV.
- Why it matters: a rare public case of agent-conducted intrusion into shared infrastructure, with residue (logs, code, comments) and a patch wave to follow in an under-watched help-desk product.
- Time-sensitive: yes, mildly. DIVD says the investigation continues and unpatched instance counts and EPSS move daily.
- Measure: EPSS history for the two CVEs; Zammad release and image-tag dates; exposed instance counts from Shadowserver or Censys if public; DIVD case pages (not opened, so unverified).
- Cost: small.
- Confidence: moderate. The AI attribution is DIVD's assessment as relayed by a secondary page; I did not read DIVD's own pages.

### 3. WordPress core CVE-2026-119977: a flaw that exists only while updating
- Reported: BleepingComputer, 4 Nov: 7.1.4 shipped 28 Oct; CISA KEV 3 Nov; Wordfence blocked 13,095 attempts in 24 hours. EPSS only 0.0116 on 5 Nov (fetched by scout), so the score lags the listing.
- Why it matters: WordPress core sits under a large share of sites; core auto-updates are themselves the exposure. The speed of auto-update uptake is a patch-wave measure with an unusually clean denominator. Not AI-related as reported.
- Time-sensitive: yes. Version-share data for the first fortnight after 28 Oct is being lost; wordpress.org stats pages change daily (not opened).
- Measure: wordpress.org version stats API snapshots; EPSS daily series; Wordfence counts as reported.
- Cost: small.
- Confidence: high real; moderate new. Not clearly tied to AI activity.

### 4. EPSS versus KEV lag, and scores for flaws exploited before they were scored
- Reported (fetched by scout): GitLab CVE-2026-97229 jumped 0.27 to 0.65 between 30 Oct and 6 Nov; BeyondTrust CVE-2026-102764 0.19 to 0.78; WordPress 0.006 to 0.012 after KEV listing; Ahsay CVE-2026-105133/105134 about 0.8 yet not in KEV. Collabora's CVE record itself says exploited in September and October, weeks before KEV (23 Oct).
- Why it matters: a daily-published score history is an instrument for how fast exploitation interest spreads; it is lost if not archived (FIRST publishes dated snapshots through the API, but only the current date plus a short series per CVE for time-series queries).
- Time-sensitive: yes for the daily series; start archiving now.
- Measure: daily pull of the top 5000 scores plus KEV membership, joined to CVE publication dates; lead and lag of score rise against KEV addition for the 2026 entries.
- Cost: small to one study. Caveat: the API paged out at 5000 rows, and ordering by EPSS did not sort numerically in my first query.
- Confidence: moderate that it is useful; it is an instrument idea, not a single event.

### 5. AI-found flaws as a class: where the credit appears, and what happens to the patch
- Reported: Brotli (OpenAI Codex Security, above); CSA's May note on a Google GTIG assessment of a zero-day exploit built with substantial LLM help; Sonatype counting about 60 public AI-discovered CVEs (search summary, not opened); one search summary notes "no standard CVE metadata field saying 'found by an AI agent'". Hugging Face July incident accounts were aggregator only and disputed.
- Why it matters: credit strings in CVE records (for example "Codex Security", "XBOW", "Mythos") are a public, dated trace of model-found flaws and could be counted against patch lag.
- Time-sensitive: no, but the count grows daily.
- Measure: scan CVE JSON 5 records and OSV credits for named AI tools; time from credit to fix release to downstream adoption.
- Cost: one study (medium); the credit text is inconsistent so recall will be low.
- Confidence: moderate real, low to moderate that it is cleanly measurable.

## Notes

- KEV additions since 30 Oct were only five, and only the Brotli and WordPress items touch widely used shared software. Ivanti Connect Secure, SonicWall and Apple are vendor products with no AI angle reported.
- The 2026 CVE numbering reaches six digits (for example CVE-2026-119977), so sequence numbers do not indicate order or volume reliably; I did not investigate.
- Several results (aggregators such as remio, runtimewire, toolnavs, forkast) are low-reliability; I used them only where a primary-like page agreed, or marked the claim secondary.
- NCSC UK, CERT-EU and Project Zero produced nothing dated in the window from search; that is a search limit, not evidence of absence.
- GitHub's advisory API was refused (403), and the CVE and OSV feeds were sampled by CVE id, not scanned for new critical entries.
- CISA, FIRST, MITRE CVE, PyPI, pypistats and OSV all answered anonymous reads from this container.
