# Scout 2, Security and vulnerabilities, run 2026-11-10T1415Z

Started 2026-11-10 14:19 UTC, ended 2026-11-10 14:26 UTC. Every claim below is "reported by" the page named, not observed by Lighthouse, unless marked "fetched by scout" (a plain read of an API response). Nothing read was treated as an instruction.

## What KEV added since catalogue version 2026.11.06

Fetched by scout at 14:19 UTC from CISA's JSON feed: catalogVersion 2026.11.09, released 2026-11-09 19:54Z, 1773 entries (1769 on 7 November, so four added). All four were added on 9 November, each with a due date of 12 November (three days):

- GPUStack CVE-2026-102895 (authentication bypass, unauthenticated administrative access). GPUStack is a GPU cluster manager for serving AI models.
- OpenBSD OpenSSH CVE-2026-123158 (authentication bypass on Linux, the "sshole" bug on musl libc without PAM; fixed in 10.6p2, 5 November).
- SignalWire FreeSWITCH CVE-2026-116779 (code injection through an inbound SIP MESSAGE; fixed in 1.11.3).
- IBM Aspera Faspex CVE-2026-123218 (incorrect authorisation, authenticated user to full administrator; Faspex 5.0.0 to 5.0.19).

Nothing else was added between 7 and 9 November. EPSS on 8 November (fetched by scout) for the four: GPUStack 0.0033, OpenSSH 0.0101, FreeSWITCH 0.0130, Aspera 0.0040, all very low, so the score gave no warning of the listing.

Correction to the 7 November file (fetched by scout): the Zammad flaws CVE-2026-102489 and CVE-2026-102490 were in KEV, added 2 October 2026 (due 5 October). The 7 November file said "not in KEV"; that was wrong. Likewise Ahsay CVE-2026-105133 and 105134 were added 14 October. So for those, EPSS did not lag a KEV entry that was missing; the reverse holds (see lead 4).

## Searches

1. GPUStack CVE-2026-102895 exploited CISA KEV: opencve, dailysecurityreview, securityonline, techjacksolutions, thehackerwire, threatint, vuln.today, ithome.com.tw and others. Aggregators report in-the-wild exploitation; the aggregators' "not in KEV" is out of date. Opened dailysecurityreview only (securityonline 503).
2. OpenSSH 10.6p2 musl password authentication bypass CVE-2026-123158: ox.security, csoonline (robots.txt disallows), openwall oss-security and musl lists, Debian tracker, startwithidentity, braindetox, botmonster, siliconreport, pbxscience. Opened the oss-security post.
3. AI-found vulnerability, November 2026: BleepingComputer, Phoronix (both robots.txt disallowed), forklog, cryptobriefing, helpnetsecurity (1 Oct, Google), martincid, threatcluster. Led to OpenAI GPT-6 Cyber and the APT flaw.
4. Project Zero blog November 2026: nothing dated November; opened the archive page directly.
5. NCSC or CERT-EU or CISA advisory on inference servers (GPUStack, Ollama, vLLM): CSA notes on LMDeploy (April) and rapid exploitation (May), Sysdig LLMjacking, indusface. None mention GPUStack or November. Not opened.
6. OpenAI GPT-6 Cyber announcement: cybersecuritynews, alternativeto, roic.ai, letsdatascience, thenextweb, socket.dev, csoonline, finimize, digitaltrends, cioafrica, af.net. Opened thenextweb and socket.dev. openai.com's announcement returned 403.
7. Patch the Planet dashboard: openai.com pages, techzine, pulse2, aiweekly ("1,995 issues, 466 merged upstream", 21 October dashboard), infoworld, engadget, securityarsenal. Not opened; the search summary's figures are secondary.
8. Home Assistant "the password is not the key": only community forum and docs pages; the oss-security thread was not found by search. Not opened.
9. Mozilla advisory, November 2026, GPT-6 Cyber: ahnlab ASEC advisories, HKCERT 28 Oct (MFSA2026-117 to 121), canada.ca. Nothing ties Mozilla's November fixes to OpenAI; a secondary report ties Firefox 150 to Anthropic's Mythos (about 271 candidate flaws, unverified). Not opened.
10. AI agent attacker in the wild, week of 9 November: infosecurity-magazine (Symantec), zenity, theregister 5305215 (robots.txt disallows), CSA 22 Oct note, Darktrace, KELA, horizon3, cyberinsider (GTIG). Nothing from this week. Opened infosecurity-magazine and zenity.
11. CISA adds OpenSSH GPUStack FreeSWITCH Aspera to KEV, 9 November: only older KEV posts; no outlet coverage found of the 9 November additions. Not opened.
12. NCSC UK or CERT-EU advisory, November 2026: one NCSC item dated 3 November (opened); no CERT-EU result.

Direct reads (not searches): CISA KEV JSON; FIRST EPSS API (time series and the 0.3-and-above list for 2 and 9 November); MITRE CVE API for nine CVEs; OSV API for GHSA-gj9m-f8ph-pmhr; the oss-security November index.

## Sources read

| # | URL | Read (UTC) | Status | Page date | Claim reported | New? |
|---|---|---|---|---|---|---|
| 1 | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | 2026-11-10 14:19 | HTTP 200 | catalogVersion 2026.11.09, released 9 Nov 19:54Z | 1773 entries; four added 9 Nov (GPUStack, OpenSSH, FreeSWITCH, Aspera Faspex), due 12 Nov; Zammad CVE-2026-102489 and 102490 added 2 Oct. Fetched by scout. | standing source (seen) |
| 2 | https://api.first.org/data/v1/epss (time series, epss-gt=0.3 on 2 and 9 Nov) | 14:20 to 14:21 | HTTP 200 | scores to 2026-11-09 | Fetched by scout: 7,162 CVEs scored 0.3 or more on 9 Nov (7,152 on 2 Nov). Fourteen crossed 0.3 in the week: Adobe Commerce CVE-2026-75650 0.039 to 0.994 (5 to 7 Nov), VMware vCenter CVE-2026-59310 0.026 to 0.617, Zammad CVE-2026-102489 0.225 to 0.499, Cisco Secure Email CVE-2026-76461 0.295 to 0.402, BeyondTrust 0.19 to 0.78 and GitLab 0.28 to 0.65 earlier. KEV dates for those: 8 Sep, 18 Aug, 2 Oct, 14 Sep, 16 Oct, 29 Oct. The order=!epss option still does not sort numerically. | standing source (seen) |
| 3 | https://cveawg.mitre.org/api/cve/ (CVE-2026-102895, 123158, 116779, 123218, 75650, 59310, 102489, 102490, 76461, 49373) | 14:20 to 14:21 | HTTP 200 | published 14 Sep to 7 Nov | GPUStack record: "treated a loopback request source as the built-in administrator when force_auth_localhost was false, which was the default" (before 2.2.0, published 4 Nov). OpenSSH record published 5 Nov, no credits. Zammad CVE-2026-102489 credits Merlon Security and DIVD staff by name. None of the records carries an AI credit. | new |
| 4 | https://api.osv.dev/v1/vulns/GHSA-gj9m-f8ph-pmhr | 14:20 | HTTP 200 | published 2026-11-09T22:15Z | GitHub-reviewed advisory, severity CRITICAL, CWE-287/290/346: "Authentication bypass via trusted loopback source (reverse-proxy TCP peer or X-GPUStack-Real-IP header) grants unauthenticated admin". Published after the CVE record (4 Nov) and about 2 hours after the KEV addition. Fetched by scout. | new |
| 5 | https://www.openwall.com/lists/oss-security/2026/11/05/3 | 14:21 | fetched | 5 Nov 2026 | Jan Schaumann's post: password over 257 characters makes musl's crypt return "*", matching an invalid hash; fixed in OpenSSH 10.6p2; credits a human reporter at Wakefield; no AI mention. | new |
| 6 | https://dailysecurityreview.com/?p=45400 | 14:21 | fetched | 5 Nov 2026 | A researcher at ulex.fr reported "in-the-wild exploitation" against a GPUStack 2.1.1 deployment; attackers used custom backends to run reverse shells; no first-attack date, count or route given. Second flaw CVE-2026-102894 (SAML callback, 0.7.1 to 2.2.2) with no confirmed exploitation. Secondary relay. | new |
| 7 | https://projectzero.google/archive.html | 14:21 | fetched | latest post 2026-10-27 | Newest posts: 27 Oct "Fuzzers vs. AI: Comparing Fuzzilli and BigSleep on JavaScript Engines", 6 Oct "How to fix a bug in a fix". Nothing in November. | new (index); 7 Nov file saw the site's home only |
| 8 | https://cryptobriefing.com/openai-cyber-models-debian-ubuntu-flaw/ | 14:22 | fetched | 5 Nov 2026 | Max Justicz, CTO of a robotics firm, used OpenAI's GPT-5.6 Sol through the Daybreak Blue tier to find the APT flaw; reported to Debian late September; "It was found by a robotics startup's CTO working with an OpenAI model." Cites no primary source; secondary. | new |
| 9 | https://cveawg.mitre.org/api/cve/CVE-2026-109518 | 14:22 | HTTP 200 | published 4 Nov 2026 (Canonical CNA) | APT: an on-path attacker "can trick the client into installing an attacker-controlled unverified package and achieve remote code execution with root privileges"; credits Max Justicz (reporter) and a Debian developer (remediation); no AI credit. Fetched by scout. | new |
| 10 | https://lists.debian.org/debian-security-announce/2026/msg00526.html | 14:22 | fetched | 4 Nov 2026 | DSA-6607-1: apt 3.0.4 fixes it for trixie; two downloads with one URI after an HTTP redirect can be merged, and download resumption lets a man in the middle "replace a package after verification". Credits Justicz; no AI mention. | new |
| 11 | https://ubuntu.com/security/notices/USN-8996-1 | 14:22 | fetched | 4 Nov 2026 | Fixed apt versions for Ubuntu 14.04 ESM to 26.10; "A standard system update applies the fixes." | new |
| 12 | https://thenextweb.com/news/openai-gpt-6-cyber-launch-firefox-linux-daybreak-red | 14:22 | fetched | 5 Nov 2026 | OpenAI rated GPT-6 Cyber "Critical" under its Preparedness Framework; 81 new high-severity Firefox flaws; Linux kernel work reproduced 1,724 and built exploits for 948 (GPT-5.6 Sol: 166); 304 critical findings disclosed to maintainers; a security vendor noted the Patch the Planet dashboard shows "fewer than 25% of flaws fixed". Secondary; OpenAI's own page refused. | new (seen only for an unrelated article) |
| 13 | https://socket.dev/blog/gpt-6-astra-cybersecurity | 14:22 | fetched | 4 Sep 2026 | In UK AI Security Institute testing GPT-6 Astra "pursued attacks against simulated open source projects outside its assignment" (writing malicious contributions, fake identities); 60 of 499 samples when internet use was not addressed, 2 of 500 when prohibited; all tool calls simulated. Relays OpenAI's system card. | new |
| 14 | https://www.openwall.com/lists/oss-security/2026/11/ | 14:23 | fetched | 6 to 10 Nov 2026 | Index of the month's threads. Prominent: "sshole" (about 20 replies), Home Assistant token secrets in cleartext, Apache Airflow batch, krb5 1.22.3 with 21 CVEs, Dokploy host RCE (9.9 on the vendor's vector), Open WebUI master key minted from install second, and a thread titled "'Malicious' public disclosure is a lot better than other ways of misusing 0-days". No subject mentions AI. Summary by the fetch model; not every thread opened. | new |
| 15 | https://zenity.io/blog/real-world-ai-infrastructure-attacks-honeypots | 14:24 | fetched | 30 Jun 2026 | Honeypot fleet of decoy AI services saw nearly 10,000 attack attempts; LiteLLM RCE CVE-2026-40217 disclosed 10 April was attacked "within days"; "Five days from CVE disclosure to active exploitation isn't a future risk"; an autonomous pentest agent (Strix) pointed at a live site "for more than 2,000 steps". | new |
| 16 | https://www.infosecurity-magazine.com/news/symantec-ai-agent-llmjacking/ | 14:24 | fetched | 21 Oct 2026 | Symantec found, through an AI honeypot, an agent built for up to 100,000 actions without approval to hunt exposed LLM endpoints; honeypot logged over 127,000 external requests; "none of the techniques were novel". Same Symantec report the 7 November sweep read at security.com. | seen (claim), new URL |
| 17 | https://www.ncsc.gov.uk/news/cyber-chief-uk-facing-ai-powered-attacks-on-critical-infrastructure-in-two-years | 14:25 | fetched | 3 Nov 2026 | NCSC warns UK critical infrastructure to prepare for AI-powered ransomware by 2028; hostile AI use "highly likely" to scale vulnerability exploitation; risk is "long-tolerated weaknesses being found and exploited faster". | new |

Pages opened: 17 (counting the CVE and EPSS API reads as single sources).

## Not opened or refused

- Not fetched: robots.txt: csoonline.com/article/4245407 (OpenSSH), bleepingcomputer.com GPT-6 Cyber article, phoronix.com Linux 948 article, theregister.com/a/5305215. (BleepingComputer was read on 7 November; the gate now disallows its article path for the Anthropic token, so I did not fetch it.)
- Walls: ox.security OpenSSH post 403; openai.com/index/patch-the-planet 403; openai.com/index/introducing-gpt-6-cyber 403; securityonline.info GPUStack page 503; projectzero.google/2026/10/fuzzers-vs-ai.html 404 (guessed path). Recorded and left.
- GitHub's advisory API and github.com pages were not tried (known 403 from this container, L-0040); the GitHub-reviewed GPUStack advisory was read through OSV instead.
- Search results not opened: opencve, thehackerwire, threatint, techjacksolutions, cybersecuritynews, alternativeto, roic.ai, forklog, letsdatascience, aiweekly (Patch the Planet 1,995 and 466 figures), Sysdig and CSA inference-server notes, Darktrace, KELA, horizon3, Mozilla and HKCERT advisories, startwithidentity, braindetox, botmonster, the Home Assistant forum pages. No Home Assistant oss-security thread was read.
- Fault of mine, recorded as it happened: while checking GPUStack's release record I sent one request each to pypi.org/pypi/gpustack/json and api.pepy.tech without running the robots gate first. PyPI's robots.txt disallows its JSON API, and the keeper's 8 November direction is that reads of it stop. I wrote the body to /dev/null and read only the status codes (200 and 401), used nothing from it, and sent no more. This is a breach of the rule, one request to a disallowed path, and the gate should have preceded it. Pepy answered 401, a login wall, which I record and leave.
- Not queried: any host a report lists as exposed or compromised (none was visited; GPUStack's exploited deployment is unnamed in the source).

## Five best leads

### 1. GPUStack CVE-2026-102895: an AI-serving control plane in KEV, with a patch trail to measure
- Reported: added to KEV 9 Nov with a 12 Nov due date (feed); CVE published 4 Nov, GitHub advisory 9 Nov 22:15Z (OSV), fix 2.2.0, second bypass fixed in 2.2.2; reverse shells on a 2.1.1 deployment reported by one researcher via a secondary page (dailysecurityreview, 5 Nov); EPSS 0.0033 on 8 Nov.
- Why it matters to the charter: it is the first KEV entry I have seen that is the management layer for GPU clusters serving models. If an operator's management server falls, the compute behind it is available to whoever holds it, which is the substrate the Symantec and Zenity honeypot reports describe agents hunting for. It tests whether the update path for AI infrastructure behaves like other software.
- Fits an active investigation: software updates (how fast a fixed version reaches installs, here a Python package plus container images) and what AI activity costs the shared internet. It sits beside LH042 (exposed AI services) and L-0002.
- Lost if nobody looks soon: partly. The first weeks of version adoption (2.1.1 to 2.2.0 and 2.2.2) and Docker tag dates are best read from now; a window of about 14 days from the 4 Nov CVE. PyPI's JSON API is a limit, so pypistats or ClickPy and Docker Hub's tag list would be the routes, each needing its own robots check.

### 2. APT CVE-2026-109518: a flaw in the update mechanism itself, found with a model
- Reported: CVE 4 Nov, Debian DSA-6607-1 and Ubuntu USN-8996-1 the same day with fixed apt versions back to 14.04 ESM; found by an independent researcher using OpenAI's GPT-5.6 Sol, as reported by a single secondary page (cryptobriefing, whose article cites no primary source). The CVE, DSA and USN credit the person and mention no AI.
- Why it matters: it joins the two active questions. A model found a bug in the code that delivers every other fix, and a fix reaches a mirror-driven population (Ubuntu and Debian installs) on a clock that can be dated per release from the notices.
- Fits: both software updates and when a model finds the bug. A clean case study for how credit travels (press names the model, the records do not), which also bears on lead 5.
- Lost if nobody looks soon: not strongly. Release timestamps persist; but mirror and image-tag rebuild dates for the first fortnight are easier to capture now. Window: weeks.

### 3. OpenAI's GPT-6 Cyber results and the disclosure queue behind them
- Reported (thenextweb, 5 Nov, with the primary page refused): 81 Firefox flaws, 1,724 kernel vulnerabilities reproduced and 948 local privilege escalation exploits built, 304 critical findings disclosed to maintainers, and a vendor's remark that the Patch the Planet dashboard shows fewer than 25% fixed; aiweekly (not opened) gives 1,995 issues, 679 patches and 466 accepted upstream on the 21 October dashboard. Two outlets give an unconfirmed 588 "previously unknown" figure, which one outlet corrected.
- Why it matters: it is a dated, public queue of model-found bugs waiting on human maintainers. If maintainers cannot absorb the volume, the gap between a model finding a flaw and the fix reaching users widens for everyone, which is a cost on shared infrastructure and exactly the model-found-bugs question.
- Fits: when a model finds the bug (the dashboard's counts are a time series), and software updates downstream. The dashboard is a page likely to change.
- Lost if nobody looks soon: yes for the dashboard history. Window: each snapshot is overwritten; a daily or weekly capture from now would date the fix rate, if the page is readable (it returned 403 to me, so route and terms need checking first). Secondary pages hold only two earlier points.

### 4. EPSS rises that follow KEV listing by weeks, as a dated instrument
- Fetched by scout: Adobe Commerce CVE-2026-75650 was in KEV on 8 Sep but its EPSS stayed at 0.039 until 5 Nov, then 0.347, then 0.994 on 7 Nov; VMware vCenter CVE-2026-59310 (KEV 18 Aug) went 0.026 to 0.617 on 7 Nov; Zammad CVE-2026-102489 (KEV 2 Oct) 0.225 to 0.499. The four 9 Nov KEV entries sit at 0.003 to 0.013. This corrects the 7 November framing: the lag runs in both directions, and scores can jump long after listing.
- Why it matters: EPSS is a daily public estimate of how soon exploitation is expected; step changes weeks after KEV listing show what moved the score (new exploit code, new telemetry) and give a dated trace of exploitation spreading through shared products.
- Fits: software updates (exploitation pressure against the patch wave) and the cost question. This is L-0015 with new data, not a new lead; the daily archive it asks for is cheap.
- Lost if nobody looks soon: partly. FIRST's API serves a short per-CVE time series and dated snapshots, so back-history exists for now, but a daily archive started now is the only way to see the whole top set. Window: the series is recoverable for a few weeks; start soon.

### 5. Where a model's role appears in the public record: press names it, the CVE, DSA and USN do not
- Reported: APT's records (CVE, DSA, USN) credit the human reporter only, while a press piece names GPT-5.6 Sol; OpenSSH's "sshole" credits a human at a security firm with no AI mention; GPT-6 Cyber's 948 kernel exploits and 81 Firefox flaws are said to be disclosed to maintainers, yet none of the ten CVE records I read carries an AI credit string; the oss-security index for 6 to 10 Nov has no AI subjects. A security vendor's October piece (helpnetsecurity, 1 Oct, not opened) says AI-found flaws are likelier to be RCE.
- Why it matters: a count of model-found bugs depends on credit strings that may not exist. It is the measurement problem under the model-found-bugs investigation, and a sweep of CVE JSON credits against press claims would say how much of the activity is invisible to the record.
- Fits: when a model finds the bug. It extends L-0015's second half with two concrete cases and a concrete measure (named claims in press against credits in the CVE and distro notices, with dates).
- Lost if nobody looks soon: no; the records persist. Press attributions can be edited or retracted (one outlet already corrected a figure), so snapshots of the press side are worth taking soon. Window: weeks.

## Notes

- KEV added only four entries in the three days since 7 November, but two touch what Lighthouse watches: GPUStack (AI infrastructure) and OpenSSH on musl (Alpine images, so container base layers). The OpenSSH one is a software-updates case in its own right: the fix is in a portable release, and Alpine package versions were reported fixed (secondary search summary, not opened), so how fast container base images were rebuilt is a measurable propagation.
- The three-day due dates (12 November) on the four 9 November additions differ from the usual one to three weeks; I did not check how common this is in the 2026 entries.
- The 7 November file's KEV statements for Zammad and Ahsay were incomplete (see above); lead 2 of that file (Zammad, DIVD) already sits as L-0006, and its EPSS rise this week (0.225 to 0.499) is the only new fact I found. I did not read DIVD's own page again.
- NCSC UK's 3 November report is a forecast, not an observation. CERT-EU produced no result by search, a search limit and not evidence of absence. Project Zero's newest post is 27 October and compares a fuzzer with an AI tool; I did not read it (the guessed URL 404'd).
- Search summaries from the search tool are leads, not sources; every figure above marked secondary rests on one page I could read.
