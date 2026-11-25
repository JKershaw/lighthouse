# R-0143: recheck of what the essay revision's review resolutions wrote

**In short.** One fresh reading, before release, of the passages written to resolve the evidence review (R-0141) and the reader-and-inference review (R-0142) of the essay's revision to version 1.1, and of the released lines R-0141's resolution changed. Every changed passage matches the retained files it rests on; one new sentence was softened so it doesn't read as contradicting a test that passed. Cleared.

- Checked at commit b434dd3 (diff 38970df to working tree), 25 November 2026, by a subagent of the driving session on Opus 5.5. No web request. Schedule row essay-first-rev-recheck.
- Files read: studies/LH033/brief.md (amendment 2), studies/LH033/review/R-0142_reader_checks.txt, studies/LH034/LH034.md (1.1), studies/LH034/brief.md (amendment 1), studies/LH034/review/essay-rev-2026-11-25/repro_node.txt; first editions at 16a713b (piece) and ea594b9 (essay) for the "12 to 16" wording.

## Changed passages

Essay draft, essays/drafts/seen-from-outside-seen-from-inside-rev.md:

1. `revised` item, "gives Node.js's unfixed lines to one decimal, 11.8 to 16.5 per cent, which is 12 to 16 in whole numbers as version 1.0 had it". Holds: unrounded 11.794 (day 2) and 16.462 (day −2), repro_node.txt; ea594b9 has "12 to 16 per cent".
2. Correction blockquote removed. Holds; no "12 to 17" or "Corrected below" remains.
3. Later evidence notice and "What the month did not show": "downloads of versions below the fix fell only a little". Holds: LH034 Answer and Findings, below-fix downloads fell 4.0 to 6.5 per cent between days 13 to 20 and 21 to 30.
4. "11.5 per cent on 20 November". Holds: day-30 unfixed share 11.5 (repro_node.txt; record measure 2), day 30 is 20 November.
5. "more than half of what the scanner can place from one side, though about one in five of all the PHP services it counts, since most announce no version". Holds for both dates the paragraph names: no-fix branches 54.5 per cent of version-reporting and 22.3 of all services on 28 October, 51.8 and 19.6 on 20 November (R-0142_reader_checks.txt). Reads cleanly enough in context.
6. "Side by side", two added sentences. Changed: "didn't separate the first two by speed" sat awkwardly beside test A, which passed in the predicted direction (PHP median late share 0.275 against Node.js's 0.196 under the rule led with); the same sentence then says the pass may follow from the units. Softened to "didn't clearly separate". The rest holds and is interpretation in an essay that already labels its readings as made after the counts.
7. "What would test this": "after PHP's counts to 29 October and Node.js's to 28 October had been read". Holds: LH033 amendment 2 "after day 8 (29 October) was read", LH034 amendment 1 "after day 7 (28 October) was read".
8. "we haven't checked whether a distribution's package keeps reporting that number". Holds; narrower than "nobody has checked", which Lighthouse couldn't know.

Released lines (from R-0141's resolution):

9. articles/a-week-after-two-fixes.md `revised` item ("gives the range ... to one decimal ... 12 to 16 in whole numbers, as the first edition had it. No figure of the first edition changed.") Holds; 16a713b has "12 to 16 per cent".
10. Its Corrections line ("None ... 11.794 and 16.462 before rounding ... it rounds to 12 to 16, so nothing was wrong"). Holds.
11. investigations/software-updates.md and releases.md, same wording. Hold.

## Changes made

- essays/drafts/seen-from-outside-seen-from-inside-rev.md, "Side by side": "The month's counts didn't separate the first two by speed:" to "The month's counts didn't clearly separate the first two by speed:".

## Noticed, not changed

- The released piece's summary (not part of this diff) still says "downloads of older versions fell only a little", the wording R-0141 asked the essay to replace with "versions below the fix" because beside the newer versions "older" can read as including October's fixed releases. The piece's body gives the exact figures for below the fix, so it isn't wrong, only looser; a future revision of the piece could align it.
- The built site in site/_site (untracked) still shows the withdrawn "correction"; it rebuilds from main.

## Disclosure

Combined disclosure stop of schedule/research-safety.md applied to the versions that will ship: the changed text carries aggregate download shares and scanner version shares already public in released records and the piece, no host, exploit mechanism, anonymised party or reconstruction clue. Nothing to hold.

## Verdict

**Cleared** for release, with the one change above.
