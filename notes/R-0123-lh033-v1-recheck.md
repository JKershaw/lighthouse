# R-0123: recheck of what the resolutions of R-0121 and R-0122 wrote into LH033

**In short.** One fresh reading of the text that two review resolutions added to the PHP fix record (versions 1.1 and 1.2), against the retained data. Every new figure reproduces. Four passages were stated a little more broadly than the counts allow, or were left stale by the resolutions, and are corrected here in small wording changes; no figure or conclusion changed. Cleared at version 1.2 with those changes.

Rechecker: a Claude Code subagent (Opus 5.5, claude-opus-5-5, as reported by its harness), 23 November 2026, dispatched by the Research run of 23 November. Offline; no network request; no source re-read.

## What was checked

- The diff `git diff 9328321 5c103ccd -- studies/LH033/LH033.md programme.md`, passage by passage, and both review notes with their Resolution sections.
- `python3 -I studies/LH033/scripts/record_v1.py` was rerun: data/record_v1.json came out byte-identical to the committed file (cmp).
- Every figure in the new counts table, the Answer's 18.5 to 24.3 and 0.5 to 0.9 and 9.0 points, the 14 to 30 and 23 to 30 changes (55,421, 46,896, 19,881; 311,749, 429,445, 81,585; 311,748 and 142,373; 186,517 at 3.1 points and 203,269 at 5.9), against `m1_counts` and `m1_count_changes`. All agree.
- My own arithmetic from `m1_counts`: share rise from day 14 to day 30 at a fixed denominator is 0.88 points of 4.73 in 8.2, 0.58 of 4.60 in 8.3 and 0.52 of 2.51 in 8.5, so "in three branches mostly because the count shrank" holds. Share at day 14 as a part of the day-30 share is 94 per cent or more in every branch, so the opening's "nearly all of that came in the first two weeks" holds on shares. Share rise from day 7 to day 14 is 71 to 81 per cent of the rise from day 7 to day 30 (day-7 values, not S7), so "test A's PHP side rests mostly on days 7 to 14" holds.
- Measure 2's day-14 count, 24,226,778 (24.2 million), and the fall to day 30 of about 1.7 million, from `m2_unfixed_tail`.
- LH011's day-30 medians, 33.9 and 73.1, and its wording "the 26 projects where most releases reached half" (studies/LH011/LH011.md, Findings), against the record's new sentence; the brief's naming of that comparator (studies/LH033/brief.md, Python comparators).
- The 8.5 limit: 3,423,244 patched on day 30 against 3,381,503 in the branch on day 7.
- The 253,987 unknown in 8.2 against R-0121's reading of the snapshot's `branches`.
- Amendment 2's date and timing in the brief (30 October, after day 8 was read) against the Answer's new "On 30 October, after seeing the first week".
- Labels: the counts table and the Answer's late-rise reading are marked derived with the cause left unknown; the shape reading is interpretation, now marked untested; the "first seen fixed" limit is interpretation, not checked with Censys; amendment 2 stays post hoc. Consistency of the opening, Answer, Findings, Limits and programme.md's LH033 sentence.
- Disclosure check (schedule/research-safety.md): aggregate version counts from a public dashboard, no hosts or exploit detail; nothing to raise.

## Changes made

All in studies/LH033/LH033.md unless marked programme.md.

1. **Answer, "then barely moved".** The colon's list included 8.4's 9.0 points, which is not barely moving.
   - Old: "The patched counts rose by 18.5 to 24.3 per cent of each branch from day 7 to day 14, then barely moved: from day 14 to day 30 they rose by 0.5 to 0.9 per cent of the branch in 8.2, 8.3 and 8.5, whose branch totals fell, and by 9.0 in 8.4."
   - New: "The patched counts rose by 18.5 to 24.3 per cent of each branch (of its count at the start of the span) from day 7 to day 14; then, in three branches, they barely moved: from day 14 to day 30 they rose by 0.5 to 0.9 per cent of the branch in 8.2, 8.3 and 8.5, whose branch totals fell, against 9.0 in 8.4."
2. **Findings, after test B, "after day 14 only 8.4 kept adding patched services at more than a point a week".** True as an average over days 14 to 30, but 8.2's patched count fell from day 14 (4,648,169) to day 23 (4,517,073) and then rose by 186,517, 3.1 points, in the last week, which "kept adding" hides.
   - Old: "but after day 14 only 8.4 kept adding patched services at more than a point a week,"
   - New: "but from day 14 to day 30 only 8.4 added patched services at more than a point a week on average (8.2's patched count fell from day 14 to day 23 and rose by 3.1 points in the last week),"
3. **Limits, the 8.5 bound.** "Allows only if a large share of the services that joined the branch after day 7" is stronger than the counts force: the minimum is 41,741 such services (3,423,244 minus 3,381,503), about an eighth of the net growth, if nearly every service unpatched on day 7 was later counted patched. The interpretation that follows is unchanged.
   - Old: "which the definition allows only if a large share of the services that joined the branch after day 7 were each seen first on an affected version and later on a fixed one."
   - New: "which the definition allows only if services that joined the branch after day 7 were seen first on an affected version and later on a fixed one: at least 41,741 of them, and far more unless nearly all of the 716,057 counted unpatched on day 7 were later counted patched."
4. **Review status, left stale by the resolutions.** The opening said "This version is unreviewed; its reviews come next", Limits "Not reviewed. This version has had no evidence or reader review yet.", and Next listed the three reviews as to come, at version 1.2, after two reviews.
   - Opening, new: "This version has had an evidence review, a reader-and-inference review and a recheck of what they changed, and is not a released piece; the comparison of ordinary PHP releases follows the 1 December point."
   - Limits, new: "**Reviewed, not released.** This version has had an evidence review (notes/R-0121-lh033-v1-evidence.md), a reader-and-inference review (notes/R-0122-lh033-v1-reader.md) and a recheck of what they changed (notes/R-0123-lh033-v1-recheck.md); a second agent's agreement is a review contribution, not independent confirmation."
   - Next, old: "The evidence review, reader-and-inference review and recheck of this version (rows LH033-v1-evidence-review, -reader-review, -recheck), with LH034's version 1.0; then the revision ..." New: "LH034's version 1.0 and its reviews; then the revision ...". Also "then measure 6 and version 1.1" became "then measure 6 and the next version", since 1.1 is taken.
   - programme.md, old: "after its evidence review and reader-and-inference review, before their recheck: ... held as written; its reviews come next, with LH034's version 1.0 from 24 November." New: "after its evidence review, reader-and-inference review and a recheck of what they changed: ... held as written. LH034's version 1.0 follows from 24 November."
5. **Corrections**, version 1.2 entry: one sentence added saying the recheck made these wording changes within version 1.2 and that no figure or conclusion changed.

## Left as it is, with a note

- "Their passing confirms that the week-one pattern lasted to day 30" (R-0121's nit, not taken): acceptable now that the next sentence says what the counts show.
- R-0122's Resolution says the cross-read comparison of branch_versions is "a candidate for ... LH033's version 1.1 with measure 6"; version 1.1 is now taken, so that is the next version. The note is a past record and is left; the record's Next now says "the next version".
- "Nearly all of that came in the first two weeks" in the opening is right on shares (94 per cent or more by day 14 in every branch); in patched counts 8.4 had 90 per cent by day 14. Left, since the sentence is about shares.

## Verdict

Cleared at version 1.2, with changes 1 to 5 above.
