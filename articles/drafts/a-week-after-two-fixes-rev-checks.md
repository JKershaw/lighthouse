# Checks for the month-on revision of the week-one piece (draft, 25 November 2026)

**In short.** Where every figure and citation in the draft revision of "A week after two fixes" and its short form comes from, what changed from the first edition and why, and what could not be filled. Written by the writing subagent that drafted the revision (Claude Code, Opus 5.5 as reported by the harness), schedule row piece-week-one-rev, for the evidence review that comes next. The figures come from LH033 version 1.2 and LH034 version 1.1, both reviewed; one read made for this revision (Node.js's announcements) is post-record context and unreviewed.

Files: [the draft](a-week-after-two-fixes-rev.md), [the short form](a-week-after-two-fixes-rev-short.md), [the figure](a-week-after-two-fixes-rev.svg), drawn by studies/LH034/scripts/draw_piece_figure_rev.py (replay: `python3 -I studies/LH034/scripts/draw_piece_figure_rev.py`; printed values in studies/LH034/scripts/draw_piece_figure_rev_output.txt, which match the records at days 1, 7, 14 and 30). Rendered and looked at in light and dark at 720 by 860 px with the container's headless Chromium. The first edition is at commit 16a713b (released 30 October 2026; unchanged on main since).

Record references: "LH033" is studies/LH033/LH033.md v1.2 and its data/record_v1.json; "LH034" is studies/LH034/LH034.md v1.1 and its data/record_v1.json.

## Figures, piece and short form

| Figure in the draft | Where it comes from |
| --- | --- |
| Ten Node.js flaws; PHP's two flaws and the agencies' advice | first edition, reviewed (R-0039); LH034 brief, Question ("ten CVEs") |
| PHP: newer branches half on day 2, older on day 6; older below newer every day from day 1 | LH033 Answer; m1_summary first_day_at_half |
| PHP day 30: 78.2, 75.0, 86.5, 92.2 per cent (summary: 75.0 to 92.2) | LH033 Answer and measure 1 table; m1_summary |
| PHP day 7 52.4 to 78.8, day 14 70.4 to 89.7 (figure alt text) | LH033 measure 1 table |
| Patched counts rose by about 0.6 to 1.5 million from day 7 to 14 | LH033 "What moved the later shares" (counts table: +1,461,917; +1,531,891; +598,162; +737,917) |
| Day 14 to 30: patched +55,421 (8.2), +46,896 (8.3), +19,881 (8.5); branches lost 311,749, 429,445, 81,585 ("between 81,585 and 429,445"); 8.4 +311,748 | LH033 same paragraph; m1_count_changes |
| "Patched" probably includes services first seen fixed (interpretation, not checked) | LH033 Limits |
| 8.2 and 8.3: most not-patched five or more behind; 8.3.8 dated June 2024, 11.1 per cent, 844,547 services; reasons unchecked | LH033 measure 3 and its paragraph (8.3.8 dated 6 June 2024 by php.net, read 21 November) |
| Node.js: all lines half on day 2; line 22 below half days 3 and 4 | LH034 Answer; measure 1 |
| Node.js day 30 amended 65.5, 74.3, 96.3; as written 39.8, 60.6, 85.8 | LH034 Answer; measure 1 summary table |
| New versions 42.6, 34.8, 74.2 per cent of each line on day 30 | LH034 Answer; unlisted_above_fix_by_version |
| As-written share falls because listed at-or-above downloads fell far more than below; daily counts can't show switching | LH034 Answer, "Which rule" |
| Late rise: at-or-above +18.4, +12.9, +25.8 per cent; below −4.0, −5.1, −6.5 per cent (days 13 to 20 against 21 to 30, means); post hoc | LH034 Findings, "Where the late rise ... comes from"; review/resolution_R-0131.txt; checked in review/recheck_R-0133.txt |
| "a few points higher in the last ten days than in the eight before" | LH034 Findings ranges (days 13 to 20 against 21 to 30) and share rise 4.8, 3.5, 1.3 points on means |
| Line 22 below-fix 3.92 to 4.20 million on days 5 to 7; 2.64 to 3.56 million each weekday from day 12 to 30 | LH034 Findings, same paragraph |
| Line 22: 27.7 of 34.5 per cent below the fix five or more behind (amended) | LH034 measure 3 table; one minus day 30 |
| July: line 22 took 18 days, line 24 four; October day 2 | LH034 measure 4 table; first edition |
| October above July on day 14 in every line; day 30 higher amended, lower as written | LH034 measure 4 paragraph and Answer |
| Python four fixes day 30: 57.3 to 72.3 per cent | LH033 Python comparators table; LH034 comparators |
| Node.js day 30 within or above the Python range (amended); line 22 below (as written) | LH034 comparators paragraph ("Day 30, amended: the same placements as day 14"; "Day 30, as written: line 22 below both") |
| PHP day 1 below every Python fix; days 14 and 30 above every one; crossing an interpretation, untested | LH033 Answer and Python comparators paragraph ("interpretation, untested here") |
| Unfixed PHP: 22.5 million, 51.8 per cent on 20 November; 24.4 million on day 7 | LH033 measure 2; m2_unfixed_tail days 30 (22,516,583 of 43,438,950) and 7 (24,386,744) |
| Packagist 10.0 per cent, September 2026 | LH033 measure 5 (583.7 million of 5,809.9 million) |
| Node.js unfixed lines 11.8 to 16.5 per cent on each day from day −7 to day 7; 11.5 on day 30 | LH034 measure_2 daily table in record_v1.json (min 11.8 on day 2, max 16.5 on day −2); the record's prose gives 12.7 to 16.5 for days −7 to −1 and 14.3, 11.8, 14.7 for days 0, 2, 7; R-0128's statement of the range, "11.8 to 16.5 per cent (days −7 to 7)"; day 30 in LH034 measure 2 |
| No-version services 62.3 per cent on 20 November; doubled on 23 October (looks like detection change) | LH033 measure 2 and its interpretation; first edition |
| W3Techs 43.9 to 65.8 per cent on 21 November; 2 to 8 per cent on 25 and 26 October; once-a-month visits | LH033 measure 4 table (1.9 to 8.3 on 25 and 26 October) |
| Test B: line 22 8.0 points below (amended), 18.8 (as written); PHP 8.3 points | LH034 test B (8.04, 8.03 from unrounded means, 18.83); LH033 test B (77.7 against 86.0) |
| Test A passed but adds little; reasons | LH034 Answer and test A (followed rather than LH033's "held"/"confirms", per R-0133) |
| Two comparisons under each of two rules; post hoc | LH034 Answer and test paragraphs |
| Short form: "three of the four branches ... patched count barely grew" | LH033 Answer ("in three branches, they barely moved") |

Figure: every plotted point comes from LH034 data/record_v1.json (measure_1 daily_pct, both rules), LH033 data/read-2026-11-21T1414Z/tables.json (m1_patched_share_by_branch, days 0 to 30, unrevised per LH033 "Revisions between reads") and LH011 data/analysis/release_days.csv (Python band and median, as the first edition's script and LH033's python_side.json compute them). The script's printed day-30 values are identical to the records' (Node.js 65.5/74.3/96.3 and 39.8/60.6/85.8; Python 57.3 to 72.3, median 61.6; PHP 78.2/75.0/86.5/92.2).

## Citations

| Citation | Source and read date |
| --- | --- |
| Censys ARC PHP2Shell | LH033 reads 25 October to 21 November 2026, day 30 from the read of 21 November 14:14 UTC |
| nodejs.org download summaries | LH034 reads 27 October to 22 November 2026, last 14:15 UTC |
| Node.js announcements of v22.23.5, v24.22.3, v26.13.1 | read once 25 November 2026, 15:15:06 to 15:15:07 UTC, HTTP 200 each; studies/LH034/oneoff-2026-11-25/fetch_log.json and note.md; bodies kept (robots.txt allowed under `*`, no training, archiving or `*` refusal at the path). Unreviewed, post-record |
| W3Techs PHP version and history pages | LH033 reads to 21 November 2026 (derived files since 21 November) |
| Packagist PHP statistics | LH033, read 25 October 2026 |
| Google's Apigee security bulletins page, GCP-2026-072 (published 24 October 2026) | retained by LH037: https://docs.cloud.google.com/apigee/docs/security-bulletins/security-bulletins, read 2 November 2026 15:32:02 UTC (data/read-2026-11-02T1530Z/found_log.json, SHA-256 7f29edf1...), quoted in checkpoints/2026-11-02T1530Z.md; text unchanged at the reads of 5, 9, 12, 16, 19 and 23 November (checkpoints). LH037 is unreviewed except D-Link's class (R-0068). Weighed earlier in notes/php-flags-2026-11-02-decision.md. The draft quotes it, attributed, and labels the watch unreviewed |
| Node.js October advisory | LH034 brief, read 27 October 2026 |
| Ubuntu 24.04's 8.3.6 | LH033 Limits (studies/LH018) |
| Python September figures | articles/two-days-for-most.md; LH033 python_side.json |

## What changed from the first edition, and why

1. **Day 30 replaces day 7 as the lead**, from the reviewed records. Title, summary, opening's last sentences, figure and every section rewritten. The title's claim ("most of their rising within two weeks") is the records' (LH033 Answer: "Nearly all of it came in the first two weeks"; LH034: shares on days 13 to 30 within a few points of day 14) and holds under both Node.js rules (as written, the share fell after day 21).
2. **New meaning: the late rise is mostly a change in what was counted.** PHP: fewer services counted in three branches (LH033 v1.2). Node.js: more downloads at or above the fix (LH034 v1.1, post hoc). The first edition had no late period.
3. **Node.js given two ways.** LH034 leads with the amended rule and gives the rule as written beside it every time; the draft does the same, with the post hoc label and the unchecked assumption, and the one-off announcement read as post-record context saying the record hasn't absorbed it (instruction 3).
4. **Unfixed Node.js tail corrected** from "12 to 16 per cent" to 11.8 to 16.5 (R-0128; instruction 2), with a Corrections line in the colophon and a mention in the `revised` item.
5. **Test A not leant on** (R-0131, R-0133; instructions 3 and 4): described as passing but adding little, following LH034 1.1, not LH033 1.2's "held"/"confirm".
6. **Google's Apigee bulletin added** beside "What no fix reaches" (instruction 1), as one vendor's statement from an unreviewed watch. It sits inside the first edition's "may be protected by a Linux distribution ... we haven't measured how many" (as notes/php-flags-2026-11-02-decision.md found) and narrows it: some of the old layer, by the vendor's account, has no packaged fix.
7. **Dropped:** line 26's newer release "18 of the 65" on day 7 (superseded by the day-30 account); the July "65 against 89" posting-day comparison (replaced by LH034's day-14 and day-30 July comparison); "one week is early" paragraph (now answered). **Added:** the 8.3.8 cluster, W3Techs's 21 November point, the end of collection.
8. **Kept:** the two kinds of count, the floor on Censys's shares, downloads as requests, the units drawn apart, the PHP tail's distribution caveat, Packagist's 10.0 per cent (first edition said "10").

## What could not be filled, and notes for the reviewers

- **Revision date and byline.** The draft carries 25 November 2026 as its revision date (byline and `revised` item); it should become the release date. On release the draft's relative links (`../../`) and the figure path need adjusting when it replaces articles/a-week-after-two-fixes.md, and articles/a-week-after-two-fixes.svg should be replaced or the new SVG renamed.
- **Whether the three new Node.js versions carry the October fix** is still unknown: their announcements, read once, don't mention October's release. The October advisory's CVE identifiers are not retained, so the commit lists couldn't be compared.
- **Status of the essay.** essays/seen-from-outside-seen-from-inside.md carries `status: released`, version 1.0 of 30 October, not a draft; see the hand-back for what the revised figures would contradict in it.
- **Not checked:** the Apigee bulletin's current text beyond LH037's 23 November read; how many Apigee portals face the internet; anything about the three new versions' November flaws beyond their titles.
- Review history of the colophon: reviewers to be named when the reviews run.
