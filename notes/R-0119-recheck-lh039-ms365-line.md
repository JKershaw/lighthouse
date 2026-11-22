# R-0119: recheck of LH039 record 1.2 (resolution of R-0118) and the investigation page's Microsoft 365 line

Reviewer: a fresh recheck subagent (Claude Code, Claude Opus 5.5, model id claude-opus-5-5), 22 November 2026. One reading of what a round wrote to resolve reviews (AGENTS.md, step 4); these changes are not sent to another reader. No network requests; no commit.

## Part 1: LH039 1.1 to 1.2

**Read.** notes/R-0118-lh039-reader.md with its Resolution; `git diff 287661b HEAD -- studies/LH039/LH039.md`; Part G of studies/LH039/scripts/record_measures.py and studies/LH039/record-1.2-output.txt (all parts); record-1.0-tabulation.txt's 7.0 rows; record-1.1-output.txt at 287661b.

**Replay.** Ran the header's replay command. All outputs byte-identical to the kept files: `git status` clean for studies/LH039 after the run (record-1.2-output.txt and checkpoints/2026-11-21-extra.txt rewritten identically), and `cmp` of record-1.0-tabulation.txt and record-1.0-packagist.csv against checkpoints/2026-11-21-*.txt/.csv identical. Parts A to F of record-1.2-output.txt match record-1.1-output.txt at 287661b except one trailing blank line.

**Figures checked against Part G.** G1 line fits (7.1.4 slope 1.83, zero at day 1.2, residual 0.44, day 4 at 5.0; 7.0.8 zero 6.7, residual 0.47; 6.9.11 zero 6.4, residual 0.73); G2 history rows (7.0.7 20.0% to 28.4%, 6.9.10 23.8% to 28.4%, both first listed 1 November); G3 (7.1 below 8.5 by 4.2, 6.9, 12.1 to 12.2 at matched pairings; 7.0 and 6.9 below all four PHP branches at all three; day 14 v PHP 12 -0.10 to -0.08; day 14 v PHP 19 -15.2; day 24 v PHP 19 +4.26 to +4.36); G4 (7.0.4 26.4% to 10.0%, 7.0.6 15.2% to 14.4%, 7.0.7 22.6% to 28.4%). All as the record states. The Resolution's corrections of R-0118's Readability figures are right.

**Found.**
1. Header `figures-commit` said 1.2's output "replaces record-1.0-output.txt and record-1.2-output.txt"; it replaces record-1.1-output.txt (typo).
2. Answer 2: "below PHP's newest branch, 8.5, at every pairing where PHP was the same age or older (by 0.08 to 0.10 points at day 14 against PHP day 12, ...)". PHP day 12 is two days *younger* than WordPress day 14, so the first example is mislabelled by the clause it illustrates, and the clause leaves out day 14 v PHP day 19 (-15.2). The accurate statement is simpler: below 8.5 at every pairing but one, the exception being day 24 v PHP day 19. The Corrections 1.2 entry repeated the clause.
3. In short, "the older WordPress branches were below all of PHP's" (and, by extension, picking 8.5 as the referent) is the post hoc branch matching, unlabelled in the opening the site leads with.
4. In short, "to about a quarter on 7.0 and 6.9" sat in a series otherwise for the first fix alone (20% to 38%); the first-fix figures are 22.4% and 23.4%, the quarter counts the second release.
5. In short stated "visiting each site about once a month" as plain fact; it is LH033's reading of W3Techs's documentation, not re-checked (Limits).
6. Answer 1's head offered the 7.1.4 line reaching zero at about day 1 as evidence of lag without the 7.0.8 and 6.9.11 lines, which reach zero near day 6.5 and fit that picture less well (Findings 7 says so; the head didn't).
7. Findings 7: the replaced-release rows are read as the survey catching up, with "sites joining the branch" as an alternative; the record's own Answer 3 shows Composer fetches on 7.0 and 6.9 mostly stayed on unfixed releases after the fix, a visible route by which new installs could land on a replaced release. Added as a named alternative (no per-version download breakdown was checked, so 7.0.7 is not named).
8. Findings 3's "9 comparisons" counts a WordPress branch at one pairing as one comparison, each set against four PHP branches; stated, with the 36 branch pairs, so the count isn't read as smaller than it is.
9. Limits, branch membership: "without any site changing release" is wrong as worded, since sites joining or leaving a branch do change release; narrowed.

Not changed: the In short is four sentences and its absolutes hold in the window; "none of this is released yet" is right; Findings 7's interpretations are labelled; the Limits' "perhaps mostly" is hedged and pointed at post hoc evidence; Next's proposal is labelled post hoc and not commissioned; the Surfaces bar on comparing WordPress with PHP publicly is apt.

**Changes (studies/LH039/LH039.md).**
1. Header: "it replaces record-1.0-output.txt and record-1.2-output.txt, whose Parts A to F" → "it replaces record-1.0-output.txt and record-1.1-output.txt, whose Parts A to F".
2. In short: "a lagged view, visiting each site about once a month:" → "a lagged view, visiting each site about once a month by our reading of its documentation:".
3. In short: "and to about a quarter on 7.0 and 6.9" → "and to just under a quarter on 7.0 and 6.9".
4. In short: "were below all of PHP's; that comparison" → "were below all of PHP's (a branch-by-branch reading we chose after seeing the figures); that comparison".
5. Answer 1: "reaches zero at about day 1, and releases" → "reaches zero at about day 1 (on 7.0 and 6.9 the lines reach zero nearer day 6.5, which fits that picture less well), and releases".
6. Answer 2: "at every pairing where PHP was the same age or older (by 0.08 to 0.10 points at day 14 against PHP day 12, and by 4.2, 6.9 and 12.1 to 12.2 points at the matched pairings of days 12, 19 and 24 against 26)" → "at every pairing but one (by 4.2, 6.9 and 12.1 to 12.2 points at the matched pairings of days 12, 19 and 24 against 26, by 0.08 to 0.10 points at day 14 against PHP day 12, and by about 15.2 at day 14 against PHP day 19)".
7. Findings 3: "the nine branch-matched comparisons with PHP in Findings 4, which include" → "the nine branch-matched comparisons with PHP in Findings 4 (each a WordPress branch at one pairing set against all four PHP branches, so 36 branch pairs), which include".
8. Findings 7: "(interpretation; sites joining the branch, or W3Techs's detection, could also move these rows)" → "(interpretation; sites joining the branch, including new installs of a replaced release such as the Composer downloads on 7.0 and 6.9 that mostly stayed on unfixed releases (Answer 3), or W3Techs's detection, could also move these rows)".
9. Limits: "without any site changing release." → "without any of its own sites changing release."
10. Corrections 1.2: "below PHP 8.5 at every pairing where PHP was the same age or older" → "below PHP 8.5 at every pairing but day 24 against PHP day 19, where PHP was five days younger".

No figure changed; the replay output is unaffected. R-0118's Resolution still carries the "same age or older" wording as the drafter's account; the record now differs from it as above.

## Part 2: the investigation page's Microsoft 365 line

**Read.** The bullet "Reviewed working record. Microsoft's AI exclusion against its own report, 22 November 2026." in investigations/ai-cost-and-spread.md; notes/microsoft-outage-report/comparison.md version 0.4 in full; closure-2026-11-22.md (for the closure date).

**Found.** The quotes, dates, page count, report date, the narrower sentence, no mention of agents, unresolved referent, no basis, the qualified classification, the provenance limit (third party's copy, original in the admin centre, not checked) and "one company's account" all match the comparison. Three points went beyond it or dropped a qualification the reviews had added:
1. "withdraws nothing" is the wording recheck R-0117 narrowed in the comparison to "doesn't withdraw the broad line".
2. "by the watch's fixed categories the report qualifies the exclusion" states the classification as the report's act rather than the comparison's interpretation, and drops "not by itself a sign of retreat", which R-0116's material problem 2 put in.
3. The status post is quoted as Microsoft's without the comparison's limit that the baseline is known from a tenant's notice and third-party copies, not Microsoft's own pages.

**Changes (investigations/ai-cost-and-spread.md).**
1. "Microsoft's final status post called" → "Microsoft's final status post, as copied by a tenant and a mirror, called".
2. "It names no AI involvement anywhere and withdraws nothing, but it doesn't mention agents, doesn't say which change it means, and gives no basis for the sentence, so by the watch's fixed categories the report qualifies the exclusion: it neither confirms nor contradicts it." → "It names no AI involvement anywhere and doesn't withdraw the broad line, but it doesn't mention agents, doesn't say which change it means, and gives no basis for the sentence, so under the watch's fixed categories we class the exclusion as qualified: neither confirmed nor contradicted, and not by itself a sign of retreat."

## Verdicts

Part 1: changed (10)
Part 2: changed (2)
