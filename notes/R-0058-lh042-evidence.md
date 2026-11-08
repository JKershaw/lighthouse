# R-0058: evidence review of LH042, exposed AI services, dated (record 0.1)

**In short.** I checked LH042's record against its retained pages, re-read eleven of those pages live, and rebuilt its series with my own code. The counts, dates and derived OpenA2A figures hold, the brief came before any count, and the horizon sweep's "no count since February" really did not hold. Two things were wrong in ways that matter: one writer's Ollama count was given a method its page does not state, and a quoted API key the record says was withheld is still in one retained page in URL-encoded form. I corrected the record (now version 0.2); the data file and the page body are outside my paths, so two must-fix items remain for the record's owner.

Reviewer: an evidence-review subagent in Claude Code (Opus 5.5), 8 November 2026, about 20:00 to 20:45 UTC. I did not write LH042. I read no other note in notes/ and not the study's for-driver.md. A second agent's agreement is a review contribution, not independent confirmation. Code and output are in studies/LH042/review/.

## What I read

Offline, from the repository at the branch head of 8 November 2026 (record commit 3d1ec7a, amended by a456290): studies/LH042/brief.md (protocol 0.1, Amendments 1 and 2, the driving session's correction about two disallowed requests), LH042.md, searchlog.md, sources.md, data/counts.csv, relayed.csv, SCREENING.md, table.md, series.csv, series_changes.txt, index_reads.csv, every readlog.csv, the retained bodies behind the counts I checked (listed under "What I checked"), scripts/*.py, replay.sh and figure.svg; git history of studies/LH042 (commit times); proposals.md lines L-0001 to L-0003 and the LH042 line of investigations/ai-cost-and-spread.md, for the horizon claim; AGENTS.md and essays/it-was-only-a-test.md.

Live, once each, with studies/LH042/review/live_fetch.py (User-Agent "Lighthouse-research/1.0 (+https://lighthouse.harbour.cat)", robots.txt read first, two seconds apart, IPv4 and email addresses withheld before saving; bodies and log in review/live/). Publishers' pages only; no exposed host, no scanner interface, no dashboard API.

| n | URL | UTC start | robots | HTTP |
|---|---|---|---|---|
| 1 | https://arxiv.org/html/2609.07115 | 2026-11-08T20:19:52Z | allowed | 200 |
| 2 | https://www.trendmicro.com/vinfo/us/security/news/threat-landscape/fault-lines-in-the-ai-ecosystem-trendai-state-of-ai-security-report | 20:19:54Z | allowed | 200 |
| 3 | https://insecurestack.substack.com/p/eus-exposed-ai-infrastructure | 20:19:57Z | allowed | 200 |
| 4 | https://www.mysteriumvpn.com/blog/data-and-research/we-exposed-ai-supply-chain | 20:20:00Z | allowed | 200 |
| 5 | https://securityscorecard.com/blog/beyond-the-hype-moltbots-real-risk-is-exposed-infrastructure-not-ai-superintelligence/ | 20:20:07Z | allowed | 200 |
| 6 | https://blog.cyberdesserts.com/openclaw-exposure-numbers-explained/ | 20:20:10Z | allowed | 200 |
| 7 | https://research.opena2a.org/indices/exposure-prevalence | 20:20:12Z | allowed | 200 |
| 8 | https://censys.com/blog/mcp-servers-on-the-internet/ | 20:20:15Z | allowed | 200 |
| 9 | https://www.knostic.ai/blog/mapping-mcp-servers-study | 20:20:18Z | allowed | 200 |
| 10 | https://pluto.security/blog/wide-open-hundreds-of-mcps-exposing-root-shells-production-data-and-citizen-records-one-call-away/ | 20:20:20Z | no robots.txt (4xx) | 200 |
| 11 | https://research.opena2a.org/reports/state-of-ai-agent-security | 20:20:23Z | allowed | 200 |

Eight were byte-identical to the record's reads (same SHA-256 as received); pages 3, 8 and 10 had changed, and every counts.csv quotation from them is still in the live text (review/live_compare_output.txt). Not re-read live: SentinelOne (429 to the record), DECLAWED's API (robots.txt), Shadowserver's dashboard (reset), and the remaining publishers' pages, which I checked only against the retained bodies.

## What I checked

1. **Brief before counts.** Commit times: brief 0916f1d at 19:09:09 UTC, Amendment 1 20ca9a9 at 19:10:25, record 3d1ec7a at 19:30:47, correction a456290 at 19:42:24. Read logs: the DECLAWED page at 19:09:17 (no counts in it; its figures load from the disallowed API), first count-bearing page at 19:11:09, last at 19:19:33. Between 0916f1d and HEAD the brief changed only in its opening (marked as not protocol) and by the two dated amendments and the correction. The D9 design reads (two requests under declawed.io's /api/, about 19:02) left no retained copy, so the account that only field names were read is the writer's and the driving session's, not something I could check.
2. **A random sample of 24 of the 91 admitted counts** (seed 20261108 fixed before the draw; review/sample.py, sample_output.txt): C01, C02, C11, C14, C29, C34, C39, C42, C43, C48, C50, C52, C55, C58, C60, C71, C78, C79, C81, C82, C83, C84, C86, C88. For each, the quotation and its context in the retained body (review/context.py), the number, the clock (scan, window or publication date) and the unit. Purposive extras because the Answer leans on them: C06, C07, C08, C13, C15 to C21, C22, C23, C25, C26, C33, C35, C36, C37, C38, C40, C41, C44, C85, C90, C91.
3. **Scripts and reproduction.** `check_quotes.py` (problems: 0) and `replay.sh` (91 counts, 57 series, 6 with two or more dates, palette check passed; tracked files unchanged after the run). review/reproduce.py, which imports nothing from the study's scripts, parses OpenA2A's index table straight from the retained HTML, compares all 36 index rows in counts.csv, regroups every admitted count by publisher, method, class, product, kind and unit, and recomputes each multi-date series. review/sources_check.py matches all 58 sources.md rows to the read logs (time, status, URL).
4. **Pooling, 42.9K, OpenA2A's restated months, post hoc labels**, read in the record, table and figure.
5. **Every absolute** in the opening, Answer and Findings, against the counts and their windows.
6. **Caution.** review/caution_grep.py over everything under studies/LH042 (counts only, never matches): IPv4- and IPv6-shaped strings, emails in plain, escaped and entity forms, key-like tokens and URL-encoded credential headers; the study's screen_hosts.py rerun; the URL lists and read logs for any exposed host; the historical blob in 20ca9a9 (counted, not printed).
7. **The figure**, rendered with the container's Chromium at 720 by 700, light and dark.

## Found

**Sample.** 23 of 24 hold on quotation, number, clock and unit. C14 does not (below). Notes on the others: C01 to C02 are the paper's stated daily counts with scan dates; C11 is "at some point" over September to mid-December 2025 and correctly tagged cumulative; C34 and the other Table I rows of arXiv 2505.02502 are dated by the table's own "As of April 20, 2025"; C39 sits inside SecurityScorecard's "24 hours we conducted this research" and is clocked by publication; C42 is Censys fingerprinting "with scan times confirmed on 31 March 2026"; C43 is a port count from a report dated 14 to 20 March; C81 is "as of April 28" on data collected from 24 April, and C82 the 6 May "in the dataset" update, kept apart as cumulative; C83 and C84 are publication-dated; C86 rests on Mysterium's "our own queries, 30-31 August 2026" to Netlas; C88's page says "Updated October 6, 2026" beside its 5 February date, so the figure may have been revised after publication (minor). The nine index rows in the sample, and all 36 in counts.csv, match my parse of the HTML exactly. Of the purposive extras, all matched their pages.

**C14 (must-fix).** insecurestack's page says: "In September 2025, Cisco Talos conducted a Shodan scan ... and found 1,139 worldwide. When I ran the same query in April 2026, I found over 25,000." Nowhere does it name Shodan's product label. counts.csv gives the method as "a Shodan product-classification query" and the fingerprint as "scanner product label", and the record's Answer called it "the same kind of query" as OpenA2A's product count and built a post hoc reading on "three publishers" reporting the product label. Cisco's own page describes Shodan retrieval plus "keyword matching against the service banner" on the default port. So the method is not stated beyond "the same query" as Cisco's, and the reading rests on two publishers, not three.

**The key (must-fix).** SCREENING.md says the one API key quoted in Synthient's page was replaced with `[redacted-by-Lighthouse]`, and the visible code line is. But the same request is repeated, URL-encoded, in the code block's `data-code` copy attribute in data/round1-2026-11-08/034.body, and the key's value (24 characters) is there once, unredacted. That body was first committed in 3d1ec7a, so the value is in history too. Emails: none left in any retained file, in any form I searched; the one SecurityScorecard address in the 20ca9a9 blob is disclosed in SCREENING.md and stays in history. IPv4: none in any body; nine IPv4-shaped strings in .headers files are all Cloudflare's cookie version token "1.0.1.1", not addresses. IPv6: none. Hostnames in visible text are as SCREENING.md lists them; no list of exposed hosts. URL lists and read logs hold publishers' pages, arXiv and two dashboards' front pages only.

**Reproduction.** All series and step counts reproduce: S42 OpenClaw category 242,379 (14 March), 267,172 (11 April, highest), 153,638 (26 June, lowest), 205,872 (1 November), six steps up and two down; S43 5,126 to 47,369; S44 889 to 2,734, seven up and one down; S01 four stated days; S45 and S57 split correctly at 18 June. 19 publishers by name, matching the record. My regrouping finds 56 groups because S45 and S57 share their method text and are split by the dated boundary in their note, which is deliberate.

**Pooling.** No series joins publishers, methods, kinds or units; no figure line joins series; cross-series figures are set side by side with methods, and CyberDesserts' own 135,000-to-63,070 "53%" comparison is reported as theirs and not made. The 42.9K (C40) is handled as the record says: a range from publication (9 February, `datePublished`) to modification (20 March, `dateModified`, also the Last-Modified header), basis "page modified date", not plotted, not in any series. OpenA2A's restated months are kept as separate series from its reports (S13, S40, S41 against S42 to S44), as the record says. But "the index states earlier months on its current categories" is the writer's inference: OpenA2A's methodology says the OpenClaw category is the sum of nine queries while Issues 1 and 2 published the single port query, and that no published figure was restated onto the June credentials definition; the index's March OpenClaw value (242,379) is below the March report's port count (249,366), which the category definition alone would not produce. It does not change any series, but it should be labelled as interpretation. The S45/S57 split is conservative: OpenA2A says the boundary moves totals by one to four detections in about 300,000.

**Post hoc labels.** The "three publishers" reading was labelled but wrong (above). Two readings made after the counts were not labelled: "Method decides the number more than the date does" and front-ends differing "as much as the Ollama counts do", an equal spread nobody measured.

**Absolutes.**
- The horizon sweep's "no count since February" (L-0003, scout 7: "no count since") did not hold, and it holds without OpenA2A: CyberDesserts' Censys fingerprint count of 63,070 OpenClaw instances on 31 March (C42); for Ollama, OpenA2A's product-matched 25,036 on 11 April (C15), CyberDesserts' three counts on 11 May (C17 to C19) and Mysterium's on 30 and 31 August (C20, C21). Attribution: the record says "scouts 5 and 7", but scout 5's lead (L-0002) says the IMC census ends in February, which is not the same claim. I did not read the scouts' notes.
- The opening's "they disagree by large factors because they count different things" states a cause for all disagreement; only the same-day CyberDesserts comparison isolates method. The opening's "the only long run made one way is ... [OpenA2A's] index" is false as written: the Ollama paper's daily sweep is a year made one way. Its "small research group" is unsupported.
- The header's observation period began on 14 February 2025 (C01, C05), not 20 April 2025. Collection ran 19:11 to 19:20 UTC by the read logs, not 19:12 to 19:21 (the same slip is in Amendment 2's text).
- Holding: "Six series have two or more dates" (reproduced); "Every other count stands alone" (51 single-date series, one count each); "no internet-wide count was read" for devices (Shadowserver unread); 58 collector requests within 60; five unread pages (two 403, one 429, one reset, one robots-disallowed API); "all 91 quotations".

**Timings in the search log (not in the record).** searchlog.md as committed in 0916f1d at 19:09:09 already contains D15 to D23 with times "about 19:10" to "about 19:18", and the brief, in that commit, says the searches ran "between about 18:55 and 19:18". Those times cannot be right. Collection search C1 ("19:13 to 19:20") found the SentinelOne URL that round 1 fetched at 19:11:14, and relayed.csv R01 gives that 429 as "19:16". None of this moves a count before the brief, since searches are not retained sources and the first count-bearing fetch followed the commit, but the logged times are not reliable.

**Figure.** Light and dark are both legible; palette check passes; each panel has its own axis from zero; points within one series are joined and nothing joins series; the Ollama panel shows the paper's four days as points. Faults, none must-fix: the first panel is titled "OpenClaw-family panels" where OpenA2A's own label is "OpenClaw gateways" and it says a hit need not be OpenClaw; no panel names its unit (hosts in a category, IPs responding per day); the subtitle still says "Unreviewed working figure, LH042 version 0.1"; the SVG is 650 high, so a 700 window shows a band of page background below it.

## Changed

In studies/LH042/LH042.md, version 0.1 to 0.2, each listed in its Corrections:
- the Answer's C14 description and the post hoc reading (two publishers, with why insecurestack is out);
- the opening: "partly because they count different things"; the only run made one way "since February"; "OpenClaw category (which it says need not be OpenClaw itself)"; "small" dropped; "unreviewed here" replaced by what was checked;
- labels on two readings made after the counts, and the unmeasured "as much as" removed;
- the observation period's start (14 February 2025) and the collection times (19:11 to 19:20);
- the Method's statement about the withheld key, pointing to the remaining copy;
- a review line in the header, and Limits and Next updated for this review.

Nothing else in studies/LH042 was edited. replay.sh still passes after the change.

## Suggestions

- For the record's owner (must-fix, outside my paths): in data/counts.csv set C14's method to "re-ran Cisco Talos's September 2025 Shodan query, which the page does not give" and its fingerprint to "not stated", then rebuild table.md; withhold the URL-encoded key in the `data-code` attribute of data/round1-2026-11-08/034.body and log it in SCREENING.md with the new hash. review/caution_grep.py reports it by count only and will show zero once it is done.
- A dated correction to searchlog.md, the brief's opening paragraph and Amendment 2, and relayed.csv R01, saying the logged times for D15 to D23, C1 and the 429 are approximate and in places impossible, and giving the read-log times.
- Label "the index states earlier months on its current categories" as interpretation, quoting OpenA2A's own account (category sums; no restatement onto the June definition).
- Give C91 (Synthient's "6 million vulnerable IPs") the brief's subset status, or say in the record why it is not one; C08's "vulnerable" already has a note.
- Strengthen check_quotes.py for bare-number quotations (C22, C23, C25, C26, C34, C35): they prove the figure is on the page but not what it counts. I checked those by hand.
- Figure: title the first panel by OpenA2A's category, add units, refresh the version line, and match the SVG height to the window used in reviews. The opening could add that 153,638 is the latest of three June sweeps whose totals ran from 245,111 to 349,424.
- Retained headers keep Cloudflare cookies set for Lighthouse's client; harmless, but the collector could drop Set-Cookie lines.
- The investigation page's LH042 line and proposals.md L-0003 repeat "because they count different things" and "the one long run made"; align them with version 0.2. Attribute "no count since February" to scout 7 (L-0003), with scout 5 (L-0002) saying the IMC census ends in February.

## Verdict

Two must-fix items remain, both outside my paths: C14's method and fingerprint in data/counts.csv (and table.md built from it), and the unredacted URL-encoded copy of the quoted API key in data/round1-2026-11-08/034.body. The record's own must-fix corrections are made in version 0.2.
