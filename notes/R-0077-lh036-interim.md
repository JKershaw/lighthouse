# R-0077: LH036 interim record, evidence review

Row LH036-interim-evidence-review. A fresh evidence review of studies/LH036/LH036.md, version 0.1 (interim, to the read of 16 November 2026), against the retained raw bodies in studies/LH036/data/read-*/ and studies/LH036/brief.md with its amendment of 8 November. Reviewer: Claude Opus 5.5 (claude-opus-5-5), subagent, 16 November 2026. The exploit and the post this study follows are Anthropic's, and this reviewer runs on an Anthropic model; this is a review contribution, not independent confirmation. Cost: unknown, not measured; unknown is not zero.

Version reviewed: git HEAD 312102332f712a46ccb14d8c3e76535d49ff2b36; LH036.md sha256 a8016c7fe6f79dfc74462c49a9e4e4cb2735c985d71a77e50983a005eb66d5e7 (as committed in cc43be8). After this review's corrections, listed below: sha256 9448d786722358f0883537fd3078f409fc1cc15e5a15dce9d840a08c8b9eb723.

## What was checked, and how

- **Tabulation reproduced.** `python3 -I LH036/scripts/tabulate.py` on a scratch copy of scripts/ and data/: tables.json byte-identical to the committed file (sha256 b6c158a7...dcdaf5b9).
- **Independent recomputation from the raw bodies**, not from tables.json, kept as code and output in studies/LH036/review/: `check_signals.py` (measures 1 to 3), `check_fixes.py` (measures 4 and 5; SUSE and Debian parsed from the HTML table rows rather than tabulate.py's extracted text lines), `check_details.py` (read statuses, first-shown products, SUSE products outside the count, reference containers, AlmaLinux diffs, live-patch rows), each with `-output.txt`. Replay: `python3 -I studies/LH036/review/check_<name>.py`.
- **Measure 1, EPSS.** 31 dates, 16 October to 15 November; each date from the earliest read; later reads equal in value. One step (factor 2.352, 25 October; 10, 1, -2, -4 days from E0 to E3). Every row of the table, the percentile ranges, the factors 1.147, 1.027, 1.663, 1.022 and the overall 4.709 hold.
- **Measure 2, KEV.** Not listed in any of the six bodies (no entry and no substring); versions and release times as stated.
- **Measure 3.** CVE dateUpdated, CNA vector and 9.8, CNA dateUpdated 2026-10-24T14:08:46Z, only the CVE Program ADP container, no SSVC; NVD statuses, lastModified values, a single Secondary CNA metric, CWE-416 Primary and the 13 configuration entries at Analyzed; reference counts 11/12 and 13/14/15; related 8 to 173 with ALSA-2026:93412 to 93415; oss-security 10/31/5 in the CVE Program container at the baseline; 11/03/1 added in that container. All hold.
- **Measure 4.** Debian suites, versions and advisory ids; Ubuntu states, intervals, priority change, notice counts (15, 20) and dates; Red Hat table (0/0/0/9 to 27/27/55/1), first-shown products by read, the two rows that left Affected, RHEL AI 3, RHEL 6 and 7; SUSE table, including 73 of 121 only Affected on 16 November, 17/2/4 newly released and the live-patch figures (55; 51 = 32+19; 57). All reproduce.
- **Measure 5.** Anthropic's post: bytes changed at four of five later reads, text twice, both furniture; dateModified constant. AlmaLinux: one substantive change on 2 November (title, update notice, kernel strings equal to Red Hat's RHEL 8, 9, 10 fixed releases); later diffs menus and language lists. Kernel announcement: challenge at three reads, robots-disallowed at three. All hold.
- **Measures against the brief, labels, absolutes, missing evidence, overlap.** Measures 1 to 5 follow the brief, with two post hoc summary rules labelled as such; Ubuntu versions were missing (fixed below). Unavailable and not-fetched readings are classed as missing, never as negatives; Debian's and SUSE's undated fixes are not placed before or after E2. The LH048 overlap is accurate (LH048's brief reads NVD, EPSS and KEV for this CVE itself); it now also names LH048's reuse of this study's copy of the post. No figures to render.

## Corrections made (listed in the record's Corrections)

1. SUSE "products" counted only products listing a main kernel package; the page names 124 (first read) and 131 (16 November). In short, Answer and table header now say what is counted, with a note on the 10 to 12 left out (live patches, kernel-azure, build packages, kernel-source-rt alone; three Real Time products Affected on 16 November) and why the count rose 119 to 121 with no new product.
2. "Ubuntu's three oldest releases" became "three oldest affected releases" (trusty is older, not affected).
3. Comparison: forky and sid are not security-channel suites; now named.
4. Ubuntu per-codename versions added (measure 4 asks for them).
5. LH048 overlap extended to its reuse of the retained post.

## Must-fix findings (not edited here; for the writing session, then the recheck)

1. **Answer, first sentence: "none of the brief's exploitation signals moved after Anthropic's post of 27 October."** False as written. After E2 EPSS rose by factors 1.147 (30 October) and 1.663 (3 November, 0.00457 to 0.0076, percentile 0.397 to 0.553, an absolute rise larger than the 25 October step's), NVD's status moved through three states, and a reference was added. What holds is narrower: no EPSS step (the brief's factor-of-two rule), no KEV listing, no CISA ADP container, no NVD score. This is the kind of wording the brief asks reviews to catch, here easier on the post's effect on the signals. Suggested: "after Anthropic's post of 27 October, CISA did not list the flaw, no CISA container or NVD score appeared, and EPSS rose without a step (the brief's factor-of-two rule): by factors of 1.15 on 30 October and 1.66 on 3 November."
2. **In short: "the exploit-prediction score's only jump came on 25 October, two days before the post."** Same problem in plain words: "jump" is not the brief's "step", and the 3 November rise is larger in absolute terms. Suggested: "the exploit-prediction score's only rise by a factor of two came on 25 October, two days before the post; it rose again, by smaller factors, after it." While there, "NVD finished its analysis on 12 November" should carry "by NVD's clock" (the status was first seen as Analyzed on 16 November; 12 November is lastModified), and "CISA has not listed the flaw" could name the latest catalogue read (13 November).

## Verdict

Not cleared: two must-fix findings (1 and 2 above), both wording of the main signal claim; every figure reproduces from the raw bodies. Once resolved, the resolution goes to one fresh recheck before the reader-and-inference review.

## Resolution, by the driving session

16 November 2026, scheduled run. Both must-fix findings accepted and resolved in studies/LH036/LH036.md using the suggested wordings: the Answer's first signals sentence now says what held after the post and that EPSS rose without a step (factors 1.15 and 1.66); the In short says "only rise by a factor of two", adds that it rose again by smaller factors, dates NVD's analysis "by NVD's clock" and names the 13 November catalogue. Sent to one fresh recheck.
