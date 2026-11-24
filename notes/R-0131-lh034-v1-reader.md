# R-0131: LH034 version 1.0, reader review, stage one

## What a reader would believe, written before reading the record

**The finding, said back.** A month after Node.js's 21 October security release, most of what people downloaded from nodejs.org in each fixed line was the fixed version or newer: about two thirds in line 22, about three quarters in line 24 and nearly all in line 26. Uptake was quick at first, with every line past half by day 2, and line 22 lagged the other two throughout.

**What seems observed.** Daily download counts by version from nodejs.org's own published summaries, to day 30 (20 November). Three newer versions appeared on 11 November; whether to count them as fixed changes the day-30 shares a lot (65.5, 74.3, 96.3 against 39.8, 60.6, 85.8). Much of line 22's unfixed remainder is several releases old.

**What seems explained.** The lower "as written" figures are taken as a counting artefact: the release list became unreadable after 9 November, so the new versions were never classed, and their downloads mostly came from people already fixed. The higher figures are offered as the truer reading, though the rule was chosen after the counts were seen and nobody checked that the new versions really carry the fix.

**What seems to have caused what.** Nothing causal is claimed. Comparisons with Python and PHP, and with July's release, are descriptions in different units; the two predictions that "held" say nothing about why.

**Limits a reader would notice.** A download is a request, not a machine; nodejs.org is one channel; the leading figures rest on a post hoc rule and an unchecked assumption. The record's header says "unreviewed" while the proposed line says "evidence-reviewed", which a reader would find confusing.

## Stage two: against the record (read 24 November 2026)

Read: studies/LH034/ (record, brief and amendments, data/record_v1.json and record_v1_output.txt, scripts/record_v1.py, checkpoint list), the LH033 record's opening, Answer and amendment 2, the queue rows for LH034 and piece-week-one-rev in schedule/due.csv, the week-one piece and its short form (Node.js passages), and the LH034 lines in investigations/software-updates.md and programme.md. One calculation of my own, post hoc and descriptive: studies/LH034/review/R-0131_counts.py, output in R-0131_counts.txt (absolute downloads per line, days 13 to 30).

### What the round establishes

The day-by-day shares are well grounded: built from retained day files, the re-read of days 0 to 7 byte-identical, and figures reproduced by the evidence review (due.csv row LH034-v1-evidence-review). Every line passed half on day 2. Line 22 sat below lines 24 and 26 throughout. The rule as written breaks from day 22 because the three new keys leave its denominator. Leading with the amended rule is supported. The brief's own words ("at or above the fixed release") and measure 4's rule ("counting any later release in the line") already count later releases, and the record labels the amendment post hoc wherever it uses it. That much of my stage-one reading stands.

### Material claim problems

1. **The late rise in the amended share reads as further uptake, but it is mostly added volume.** LH034.md, Answer: "on days 21 to 30, by the amended rule, at 64.6 to 68.8, 69.3 to 74.6 and 94.9 to 96.7", set after days 13 to 20 at 59.9 to 63.2 and so on. A reader takes this as more of each line moving to the fix. Evidence: R-0131_counts.txt (post hoc). Below-fix downloads in line 22 were 2.87M on Friday 6 November, 2.84M on Friday 13 November and 2.76M on Friday 20 November. Fixed-or-newer downloads were 4.64M, 5.73M and 5.24M. Line 26's below-fix count was 0.30M, 0.31M and 0.27M while the line's total rose from 6.29M to 7.44M. So the share rose mainly because the new releases drew extra fetches, not because old versions were fetched less; below-fix downloads fell only slightly as a share of all traffic (line 22: about 10.4 to 11.9 per cent on days 13 to 20, 8.8 to 10.3 on days 21 to 30). This is the mirror image of LH033's finding that PHP's late rise came mostly from shrinking branch counts. **Resolution:** add one labelled sentence to the Answer, saying that after day 21 below-fix downloads stayed roughly level and the higher share came mostly from more downloads of the newer releases (post hoc, from R-0131). Keep "a share is not a rate of uptake" in mind for the piece.

2. **Test A reads as support for a reading, but both sides are composition effects, and the units nearly fix the outcome.** LH034.md, Answer: "the median over Node.js's three lines of how much of the day-30 share arrived after the first week was smaller than the PHP branches' median (test A)". Evidence: under the amended rule, Node.js's late L comes partly from the volume effect in problem 1. Line 22's share jumps from 63.2 on day 20 to 68.8 on day 22, as v22.23.5 appears. PHP's late L is partly shrinking denominators (LH033.md, Answer and test A). And a day's share of downloads (a flow) settles sooner than a count of standing services, whatever the reason, as LH033 says of the Python crossing. The record says the tests show nothing about cause, but "arrived" and "held" still invite reading them as confirmation. **Resolution:** replace "arrived" with "came after the first week", and add one sentence: test A compares a flow with a stock, both sides include composition effects (newer releases' added downloads here, fewer services counted in PHP), so its passing adds little beyond the difference in units. Test B, a level gap on S30, means what it says (8.04 points amended, 18.83 as written).

3. **A stated assumption drops out of the summaries.** LH034.md, Answer: "it assumes that each of the three keys is a real published release that carries the October fix; that wasn't read". The "In short" paragraph and the proposed investigation-page line give the post hoc label but not this assumption. **Resolution:** add "assumed, not checked, to be releases carrying the fix" after "three newer versions first seen on 11 November" in both.

4. **The review status is out of date.** LH034.md, header ("version: 1.0 (to day 30; unreviewed)"), "In short" ("this version is unreviewed, and its reviews come next") and Limits ("Unreviewed. This version has not had its evidence review"). Evidence: due.csv row LH034-v1-evidence-review shows done and cleared at 1.0. The proposed line says "evidence-reviewed". **Resolution:** update the header, the opening and Limits to match the proposed line.

5. (Minor) **"First passed half" hides a dip below half.** The proposed line: "All three lines first passed half on day 2." Evidence: record_v1_output.txt shows line 22 below half on days 3 and 4 under both rules. **Resolution:** add "line 22 dipping below half on the weekend after", as the week-one piece already does.

### Readability

- The Answer stacks seven figure series in one paragraph. Lead with the two day-30 triples and day 2, and move the day 13 to 20 and day 21 to 30 ranges to Findings.
- "Standing and rebuilt" and "S7/S30/L" mean nothing to a reader of the Answer. Say "how much of the day-30 share came after the first week" once, then drop the jargon.

### Next step

The queue's next step is piece-week-one-rev, after this review's resolution and the recheck. It should go ahead, but without new collection, which closed at the brief's stop and would not help. Problem 1 is settled from retained data. One cheap step would remove problem 3's assumption: a one-off read of Node.js's own release announcements for v22.23.5, v24.22.3 and v26.13.1, where its robots.txt allows the blog pages (the /dist/ list is refused), to date them and say whether they carry October's fixes. This is worth doing before the piece leads with 65.5, 74.3 and 96.3. The piece should present day 30 as a description, give both rules, carry problem 1's sentence, and not lean on test A. Nothing else available before the revision would separate uptake from volume better than the counts already kept.

**Combined disclosure:** clears.
