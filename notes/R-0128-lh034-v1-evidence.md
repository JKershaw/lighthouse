# R-0128: evidence review of LH034 version 1.0 (Node.js's October security release in nodejs.org's downloads)

**In short.** A fresh evidence review of the Node.js download study's record at version 1.0, against its brief and the retained day files. Every consequential figure reproduced from the raw counts with the reviewer's own code, and the comparisons stay within the brief's allowed form. Three labelling and wording faults were fixed in the record; no figure or conclusion changed, so it stays at version 1.0. Cleared at version 1.0.

- Reviewer: a fresh Claude Code subagent on Opus 5.5 (claude-opus-5-5, as reported by the harness), 24 November 2026, queue row LH034-v1-evidence-review. It had not written or read the record before. Its agreement is a review contribution, not independent confirmation.
- Record reviewed: studies/LH034/LH034.md, version 1.0 of 24 November 2026 (commit 0f6d490), with scripts/record_v1.py, data/record_v1.json and data/record_v1_output.txt.
- Protocol: studies/LH034/brief.md (protocol 0.1, amendment 1 of 30 October, amendments of 9 and 12 November).
- Sources read: the 98 gzipped day files and 12 read logs under studies/LH034/data/read-*/ (90 distinct days, 28 July to 27 August and 23 September to 20 November 2026, plus the 22 November re-read of days 0 to 7); the release list read on 5 November (read-2026-11-05T1414Z/dist-index.derived.json, 878 entries; body removed under data/REMOVED.md); studies/LH033/data/record_v1.json and python_side.json; studies/LH011/data/analysis/release_days.csv (for the Python medians unrounded); checkpoints/2026-11-22.md; version 0.1 at commit 2bcffa2. No network fetch.
- Code and output: [reproduce.py](R-0128-lh034-v1-evidence/reproduce.py) and [output.txt](R-0128-lh034-v1-evidence/output.txt). Replay from the repository root: `python3 -I notes/R-0128-lh034-v1-evidence/reproduce.py`. Written from the brief and the file formats; it does not import or copy record_v1.py or tabulate.py. It takes each day from the earliest read holding it, reads lines from the version key's major number, orders listed versions by the 5 November list, applies the 12 November rule (plain `vX.Y.Z` above the fix) for the amended series, treats the `unknown` key as no version, and rounds once, half up, from the counts with `Decimal`.

## What was checked, and what came out

**Measure 1, days 0 to 30, both rules, three lines.** All 186 daily values reproduce to the figure. First day at half is day 2 in every line under both rules; days below half after it are 3 and 4 (line 22, both rules) and 23 to 30 (line 22, as written); none in lines 24 and 26. Days 1, 2, 7, 14 and 30 and one minus day 30 match the summary table, recomputed from counts (60.2, 39.4, 14.2 as written; 34.5, 25.7, 3.7 amended). Day 30 line counts match (4,593,945, 6,150,254, 1,918,565 as written; 8,004,879, 9,433,439, 7,442,987 amended). The ranges in the Answer (days 13 to 20; days 21 to 30 amended) match. The rules differ on days 21 to 30 only, in all three lines: 30 of 93 line-days, as stated.

**Unlisted versions.** v22.23.5, v24.22.3 and v26.13.1 first appear on day 21, and their downloads and shares of the amended line on days 21, 22, 25, 28, 29 and 30 match the table (42.6, 34.8 and 74.2 per cent on day 30). No other unlisted key falls in a fixed line on days 0 to 30, so the amendment's exclusion was never exercised. v27.0.0 had 78,426 downloads on day 30. Within each fixed line, the 5 November list's order equals descending semantic version order.

**Measure 2.** Ranges match: 17.8 to 20.3 (23 to 30 September), 12.7 to 16.5 (days −7 to −1), 10.4 to 15.8 (days 8 to 30); day 0, 2, 7, 14 and 30 values 14.3, 11.8, 14.7, 12.6, 11.5; line 20 5.5 to 8.9 (6.1 on day 30); line 25 0.6 to 1.0 (0.8); no-version requests at most 0.0095 per cent of total (stated "at most 0.01"); day 30 total 28,111,796 with 28,110,225 attributed; weekend 15.6 to 18.1 million, weekdays 26.7 to 38.9 million. Line 27: 4.28 per cent on day 9, 0.19 to 0.51 on days 10 to 30, 0.28 on day 30 (it also had 0.07 on day 8, not mentioned; harmless).

**Measure 3, day 30, both rules.** Every group share and the largest single version below the fix match (v22.14.0, 19 behind, 8.0 and 4.6 per cent; v24.19.0, 4 behind, 7.7 and 5.0; v26.7.0, 9 behind, 6.0 and 1.5).

**Measure 4 (July).** List dates of v22.23.2, v24.18.1 and v26.5.1 are all 28 July. First day at half 18, 4, 2; days 1, 2, 7, 14, 30 match; no unlisted in-line key on 28 July to 27 August. Later listed releases within July's 30 days match (none in 22; v24.19.0, v24.20.0; v26.6.0 to v26.8.1). The posting-day alignment (July's days 2, 3, 8, 15) matches, and the "on either alignment" statements check line by line.

**Amendment 1, tests A and B.** S7, S30 and L reproduce to the figure under both rules and equal LH033's amendment2 node block. PHP median L 0.27495. Test A holds under both rules (median L −0.139 and 0.196). Test B holds: unrounded gaps 18.83 (as written) and 8.03 (amended); see suggestion 1.

**Comparators.** Python four-fix ranges, the median of 37 project medians (recomputed unrounded from LH011's table: 57.60, 57.19, 57.86, 58.87 and 61.55 per cent, so the record's 57.6, 57.2, 57.9, 58.9 and 61.6 are single roundings, half up), and PHP Censys ranges from LH033 v1.2 match. Every below, within and above placement in the Answer and Findings matches my code under both rules.

**Re-read of days 0 to 7.** All eight pairs byte-identical after decompression; every day file's read-log SHA-256 and byte count match its bytes (none of 98 differs).

**Every figure in JSON or output.** Spot checks of every table and every figure in the prose found each in record_v1.json or record_v1_output.txt, except the test B gaps, which are differences of the shown S30s.

**Agreement of In short, Answer and Findings.** They agree on every figure.

**Post hoc labelling.** The Answer's second paragraph labels the amended rule post hoc, counts what it changes (30 of 93 line-days, measure 3's denominators, two comparisons under each rule) and says the choice to lead with it was made after every outcome was seen; Findings label it in every table header and in the tests. The reasons given are true to the brief: measure 1 is "at or above the fixed release"; listed later releases (v24.22.2, v26.13.0) already counted; the as-written rule's restriction to the kept list comes from the 9 November robots.txt amendment, not from a choice about uptake. But see must-fix 1 and 3.

**Allowed form.** No ecosystem is called faster or safer, and no cause is named for any cross-ecosystem difference. A download is a request throughout. nodejs.org is called one channel. Absolutes ("no other unlisted key", "every line", "never exercised") carry their windows (days 0 to 30, or the named days). Unknowns (what the new versions fix, when published, line 27's status, the file's day boundary, robots.txt before 9 November) stay unknown and are listed under Limits.

**Corrections.** Accurate. July line 22 day 7: 2,032,506 of 6,546,683 is 31.046 per cent, 31.0 rounded once; tables.json holds 0.3105, which rounds again to 31.1, the figure version 0.1 printed (checked at 2bcffa2). Line 26 day 30 amended: 7,171,297 of 7,442,987 is 96.3497 per cent, so 96.3 rounded once; tables.json's 0.9635 gives the checkpoint's 96.4. Version 0.1's day 0 to 7 measure 1 values and its measure 2 statements are unchanged in 1.0. The 21 November entry matches data/REMOVED.md.

## Must-fix (all fixed in studies/LH034/LH034.md)

1. **In short gave the amended rule's figures without saying the rule was post hoc.** The opening a reader meets first led with 65.5, 74.3 and 96.3 per cent, from a rule made after day 21 was seen, with no label. Fixed: "counting three newer versions ... as at or above the fix, a rule chosen after those counts were seen, it was 65.5 ...".
2. **Line 27's share of day 9's tail was misdescribed.** The record said line 27's 4.28 per cent "is most of that day's high of 15.8 per cent"; it is about a quarter of it. What it is most of is the rise over the days either side. Fixed: "which is most of the difference between that day's high of 15.8 per cent and the days either side (11.6 on day 8, 13.3 on day 10)", both figures in record_v1.json's daily table.
3. **The Answer's comparator and test paragraphs used the amended rule without the label or the count of comparisons.** Fixed: "by the amended rule (post hoc)" twice in the comparator paragraph; in the tests paragraph, "Both held under both rules, the amended one made after day 21 was seen" and "They are two comparisons under each of the two rules, testing readings made after the first week was seen".

No figure or conclusion changed, so the version stays 1.0 and no Corrections entry is added.

## Suggestions (not changed)

1. **Test B's amended gap is a double rounding.** 8.04 is 74.32 minus 66.28; from unrounded S30s it is 8.0333, so 8.03 once rounded. LH033's record (reviewed) prints 8.04 too. The test's outcome is unaffected. The record could say the gap is the difference of the shown S30s, or print 8.03 in both records at their next revision.
2. **Measure 2 skips 1 to 13 October.** The brief asks for each day from 23 September. The daily values are in record_v1.json, but the prose gives 23 to 30 September and days −7 onwards only. The missing days run 16.5 to 18.5 per cent (my output), consistent with the decline the record describes. A clause would complete it.
3. **"It falls because the newer versions draw downloads mostly from versions already at or above the fix"** (Answer). The counts support the accounting: in line 22, listed at-or-above downloads went from 5,350,355 on day 20 to 1,829,805 on day 30, listed below from 3,119,227 to 2,764,140. But "draw from" reads as requesters switching, which daily counts can't show. "Falls as downloads of listed versions at or above the fix fall far more than those below" would say what was measured.
4. **"Node.js very likely published these releases on or just before 11 November"** is an interpretation, unlabelled. It's hedged, but a label would help.
5. "In line 24 the two-to-four group is close to the five-or-more group" (10.5 against 14.3 amended; 16.1 against 22.0 as written): "smaller than but comparable to" would be more exact.

## Public surfaces

Nothing public states a LH034 figure that version 1.0 contradicts. articles/a-week-after-two-fixes.md and its short form give day 7 figures (54, 72, 65 per cent; line 26's newer release 18 of the 65; July's 18 and four days to half; line 26 65 against 89 by day 7), and all are unchanged in 1.0. That piece's "12 to 16 per cent of downloads on each day around the release" for the unfixed tail, reviewed at release, sits on 11.8 to 16.5 per cent (days −7 to 7), so its upper bound, rounded half up, would be 17. That predates 1.0 and isn't new here, but the piece's planned revision should take the figure from 1.0. investigations/software-updates.md, programme.md and AGENTS.md say only that LH034's record is due or follows from 24 November, with no figures. They will need updating once 1.0 completes its reviews, and the week-one piece's revision is pending.

## Verdict

Cleared at version 1.0, after the three must-fixes above were made in the record. What the fixes wrote should be read once by a fresh agent at the recheck (row LH034-v1-recheck), with the reader-and-inference review.
