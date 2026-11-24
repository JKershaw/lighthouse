# R-0133: recheck of LH034 version 1.1 (what the resolution round wrote)

**In short.** A fresh agent read once what version 1.1 of the Node.js download study's record wrote in answer to its evidence review and its reader-and-inference review. Every new figure reproduces from the retained day files with code written for this check. The direction of the new reading holds, but "downloads below the fix stayed about level" was too strong (they fell 4 to 7 per cent between the two periods), and test A's PHP side was described by its post-day-14 part only; both were corrected in place. Cleared at version 1.1.

- Rechecker: a fresh Claude Code subagent on Opus 5.5 (claude-opus-5-5, as reported by the harness), 24 November 2026, queue row LH034-v1-recheck. It had not written or reviewed the record before. Its agreement is a review contribution, not independent confirmation.
- Read: studies/LH034/LH034.md at 4cf54dc and `git diff 584d45a 4cf54dc` of it; notes/R-0131-lh034-v1-reader.md (whole, including its resolution); notes/R-0128-lh034-v1-evidence.md; studies/LH034/review/R-0131_counts.py and .txt, resolution_R-0131.py and .txt; data/record_v1.json and record_v1_output.txt; brief.md (amendment 1's tests); studies/LH033/LH033.md (opening, Answer, measure 1 counts, amendment 2, Limits, Corrections) and its data/record_v1.json (`amendment2`). No network.
- Code and output: studies/LH034/review/recheck_R-0133.py and recheck_R-0133.txt. Replay: `python3 -I studies/LH034/review/recheck_R-0133.py`. Written from the file formats, not copied from the resolution's script; it adds a symmetric split (average of both orders) beside the one-sided split the record uses.

## What was checked

**Late-rise split (days 13 to 20 against 21 to 30, means).** Reproduced exactly: at or above the fix +18.4, +12.9, +25.8 per cent; below −4.0, −5.1, −6.5 per cent; share +4.8, +3.5, +1.3 points, of which 3.9, 2.5, 1.0 go with the change at or above and 1.0, 1.1, 0.3 with the change below. Symmetric split: 81, 70 and 77 per cent of each rise goes with the added downloads, so "mostly" holds on means in every line. Weekday triples reproduce (line 22 4.2 against −0.2; line 24 1.9 against 1.5; line 26 1.0 against 0.3); in line 24 on weekdays it is 56 per cent, so "mostly" is only just true there, now said.

**Fall in below-fix downloads, days 5 to 7 against 28 to 30.** Reproduced: −27.0, −35.6, −76.8 per cent; at or above +25.9, −23.1, +204.7; line 22's 13.0 points split 5.7 / 7.7 / −0.3. "Mostly by day 12" holds in all three lines (line 22's weekday below-fix counts: 3.92 to 4.20 million on days 5 to 7, 3.31 to 3.47 on weekdays 8 to 11, 2.64 to 3.56 on weekdays 12 to 30; lines 24 and 26 similarly).

**Other new figures.** Same-weekday below-fix counts (Tuesdays and Fridays), the day-20 and day-30 listed counts in the "which rule" paragraph, line 22's below-fix share of attributed downloads (10.4 to 11.9; 8.8 to 10.3), line 26's 0.24 to 0.38 million from day 12, the ranges moved to Findings, measure 2's 16.5 to 18.5 per cent on 1 to 13 October (13 days in record_v1.json): all match. Test B's 8.03 from unrounded means is R-0128's figure.

**Labels.** The split is labelled post hoc, after every outcome was seen, in the Answer, Findings and Limits; the amended rule keeps its count of comparisons (two under each rule) where the tests use it. The unchecked assumption that the three new versions carry the fix is now in the opening and the Answer's first paragraph, where the amended figures lead; Limits and the "which rule" paragraph keep it. No cause is claimed; a download is called a request throughout; absolutes carry their windows.

## What was found, and changed in place (within 1.1)

1. **"Stayed about level" overstated.** Below-fix downloads fell 4.0 to 6.5 per cent between the periods' means (7.1 per cent in line 24 on weekdays) and carry 19 to 30 per cent of each rise. Replaced in the opening, the Answer and Limits by "fell only a little", with the figures; "not more of each line moving to the fix" replaced by "the smaller part of the rise is fewer requests for old versions"; Limits' "not fewer below the fix" became "rather than fewer below it". "After 11 November" became "from 11 November" (day 21 is in the later window). The opening's "extra downloads of the newer versions" became "more downloads at or above the fix, arriving with the newer versions", since the net rise is at or above the fix as a whole while listed fixed versions lost downloads.
2. **Test A's PHP side misdescribed.** The Answer said "PHP's late rise came mostly from fewer services counted", and Findings put PHP's side "after day 14". PHP's L runs from days 5 to 7 to days 28 to 30 and, as LH033's record says, rests mostly on days 7 to 14, when patched counts rose by 0.6 to 1.5 million in every branch; only the rise after day 14 came mostly from fewer services counted in three branches. Both passages now say so, with LH033's limit that "patched" probably includes services first seen already fixed (which keeps "neither side is plain uptake" true). "Which moves only as services are rebuilt and rescanned" became "moves as services are rescanned, rebuilt or drop out of the count", which no longer contradicts the next sentences. Node.js's amended side: "the newer versions' added downloads after day 21" became "added downloads at or above the fix (in line 22, the median line, from day 21, as the newer versions arrived)", since line 26's added downloads came mostly from day 8.
3. **Corrections.** The 1.1 entry said "four of the evidence review's suggestions" but five were taken; now "all five", with the fifth named. A sentence lists this recheck's changes. Header, authors, opening, Limits' review status and Next brought up to date.

No figure or conclusion changed. In short, Answer, Findings, Limits and Next now agree.

## LH033's wording beside LH034 1.1

LH033 version 1.2 (not edited) says "more of PHP's day-30 share arrived after the first week than of Node.js's (test A)" and that the tests' passing "confirms that the week-one pattern lasted to day 30". No figure conflicts (its 96.4 and 8.0 are 96.36 and 8.03/8.04 rounded). The reading does: LH034 1.1 says test A adds little beyond the difference in units, and LH033's only description of the Node.js side ("a download share that can fall as newer releases take over") fits the rule as written, not the amended rule, under which Node.js's share rose. LH033 does say test A's PHP side rests on days 7 to 14 and that the units differ, so a careful reader isn't badly misled, but a reader of its Answer alone would take test A as confirmation that LH034 now disclaims. Recommended at LH033's next revision, or before the week-one piece draws on either: "passed" for "held"/"confirms" in test A's sentences, and one clause that under the amended rule Node.js's late rise is mostly added downloads.

## Combined disclosure check (schedule/research-safety.md)

Clears. Aggregate public download counts by version and public scan shares; no exploit detail, no hosts, no people or accounts; nothing new is disclosed beyond figures already in the retained record.

## Verdict

Cleared at version 1.1, with the small corrections above.
