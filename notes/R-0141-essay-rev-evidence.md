# R-0141: evidence review of the day-30 revision of "Seen from outside, seen from inside" (draft 1.1)

**In short.** A fresh agent checked the draft revision of the first essay against the released version 1.0, the writer's check note, the two reviewed study records and their retained data, and the revised piece released today. Every new or changed figure reproduces from the retained reads, and the essay follows the Node.js record's weaker reading of the first test. One thing must be fixed before release: the Correction notice says version 1.0's "12 to 16 per cent" was wrong, but the unrounded figures behind it, 11.79 to 16.46, round to 12 to 16, so 1.0 was right in whole numbers and the notice's "rounds to 12 to 17" is a double rounding. Not cleared until that is resolved.

- Schedule row: essay-first-rev-evidence-review.
- Reviewer: a subagent of the Research run of 25 November 2026 (Claude Code), on Opus 5.5 (claude-opus-5-5) as reported by the harness. A second agent's agreement is a review contribution, not independent confirmation.
- Commit checked: 38970df (the draft as committed there; this review's four small edits are listed below and are not yet committed).
- No web request was made. No record or schedule file was edited.

## What was read

essays/drafts/seen-from-outside-seen-from-inside-rev.md (1.1 draft) against essays/seen-from-outside-seen-from-inside.md (1.0) by diff; notes/essay-first-rev-checks-2026-11-25.md; studies/LH033/LH033.md (1.2), brief.md (amendment 2) and data/; studies/LH034/LH034.md (1.1), brief.md (amendment 1 and the amendment of 12 November) and data/; articles/a-week-after-two-fixes.md (2.0); notes/R-0042-essay-checks.md (the 1.0 check of the unfixed range); notes/R-0128-lh034-v1-evidence.md (measure 2); site/README.md (notice form); proposals.md (P-0001, P-0002, P-0008, the leads); schedule/due.csv; programme.md (software updates, Next); investigations/software-updates.md; schedule/research-safety.md.

## What was reproduced

Both scripts read the retained raw bodies directly (Censys snapshots; nodejs.org daily summaries and the derived 5 November release list), not the records' JSON, then print the record's figures beside them.

- studies/LH033/review/essay-rev-2026-11-25/repro_php.py, output repro_php.txt (earliest read per completed day). Reproduced: day-30 shares 75.0 to 92.2; day 7 to 14 patched rises 598,162 to 1,531,891 ("about 0.6 to 1.5 million"); day 14 to 30 patched rises 55,421, 46,896, 19,881 against branch losses in 8.2, 8.3, 8.5, and 311,748 with growth in 8.4; share rises day 23 to 30 of 3.0, 2.2, 2.4, 1.3 points (1.3 to 3.0); patched rises day 23 to 30 as points of the day-23 branch 3.1, 0.8, 5.9, 0.6 (more than a point only in 8.2 and 8.4); unfixed tail 22,516,583 of 43,438,950 = 51.8 per cent on day 30, 24,386,744 on day 7; no version 59.55 per cent of 110,944,946 on 28 October (40.5 per cent reporting, "two in five") and 62.26 per cent on 20 November (37.7 reporting, "fewer than two in five"); 8.3.8 at 844,547 of 7,595,362 = 11.1 per cent in the snapshot of 21 November; S30 and L per branch identical to record_v1.json, PHP median L 0.275, test B gap 8.30 (77.74 against 86.04). The strata at the 25 October read (7.4, 8.1, 7.2, 5.6, 5.2 the largest unfixed branches) also checked.
- studies/LH034/review/essay-rev-2026-11-25/repro_node.py, output repro_node.txt. Reproduced: unfixed share days −7 to 7 from 11.8 to 16.5 (unrounded 11.794 on day 2, 16.462 on day −2), 11.5 on day 30; weekend days 0 to 30 15.6 to 18.1 million, weekdays 26.7 to 38.9 million; from 23 September to 20 November every weekend day (largest 18,082,722) below every weekday (smallest 19,912,263); day 30 at 65.5, 74.3, 96.3 (amended) and 39.8, 60.6, 85.8 (as written); L medians 0.196 (amended) and −0.139 (as written); test B gaps 8.03 from unrounded means (8.04 from rounded S30s; the essay's 8.0 is right either way) and 18.83.

## Findings

### Must-fix

1. **The Correction notice, and the `revised` item's "corrects", say 1.0 was wrong when it wasn't.** Version 1.0's "12 to 16 per cent" was set at the 1.0 check (R-0042, item 9) from the unrounded values, 11.79 to 16.46, which round to 12 and 16. "Rounds to 12 to 17" rounds 16.46 to 16.5 and then to 17. So the range in whole numbers was right, and a dated **Correction** notice, which says a piece "said something wrong" (AGENTS.md, step 4), misstates what changed. Suggested resolution: remove the Correction blockquote; in the `revised` item, replace "It corrects Node.js's unfixed lines from "12 to 16 per cent" to 11.8 to 16.5 per cent" with something like "It gives Node.js's unfixed lines to one decimal, 11.8 to 16.5 per cent, as the records print them (12 to 16 in whole numbers, as version 1.0 had it)"; and drop "Corrected below" wording. The text's 11.8 to 16.5 can stay. The released piece articles/a-week-after-two-fixes.md (2.0) carries the same claim in its `revised` item and its Corrections line ("which rounds to 12 to 17"); that is outside this draft but the same error, and the driving session should correct it there (a small dated change, or a note of the piece's own) so the two stay consistent. The source of the slip appears to be R-0128's remark that the record's printed 16.5 "rounded half up, would be 17".

### Should-fix

2. **Test B in the Later evidence notice is compressed.** "The oldest fixed Node.js line sat 8.0 points below the newer ones" and "PHP's older branches sat 8.3 points below the newer ones": each gap is to the nearer (lower) of the newer lines, and from the higher of the older PHP branches; line 22 is about 30 points below line 26. The body states it exactly and the piece uses the same compression ("behind the newer ones ... by 8.0 points"), so this is a wording choice, but "below the nearer of the newer ones" would be exact at little cost.
3. **"None is scheduled; the nearest is ... a census of the versions public lockfiles name."** Supported: nothing in schedule/due.csv or proposals.md follows the build-server flag through a fix's month, and P-0008 is the closest ranked proposal. P-0002 (the installer's version) is about installer versions, not the build-server flag, so it isn't nearer. "None of our studies or proposals looks for one" (Node.js servers seen from outside): no proposal, lead or row found by searching proposals.md and due.csv for Node.js, nodejs, servers and outside terms. Issues weren't searched here either (no Harbour use in this task); the driving session may check `hb status` before release.

### Notes

4. Every new or changed figure in the draft comes from LH033 1.2, LH034 1.1 or the piece 2.0, all linked, and reproduces from retained data (above). Unchanged week-one, Python and Packagist figures were checked at 1.0 (R-0042) and no record changed a day 0 to 7 figure.
5. Test A follows LH034 1.1 ("passed ... but tells us little", the units alone could produce it, the as-written pass is a counting artefact, the amended late rise mostly added volume), not LH033 1.2's "held as written"/"confirms". Test B is reported as holding under both rules. Consistent with the piece, programme.md ("test A, though it passed, adds little") and AGENTS.md's summary. The investigation page names neither test. LH033's stale "held/confirms" wording is already listed for the driving session (notes/week-one-rev-checks-2026-11-25.md) and programme.md says LH033's next version aligns it.
6. Post hoc labels: the amended Node.js rule (made after day 21), the split of the late rise, and the two tests as tests of readings made after the first week are labelled wherever used, in the notices, the body and the notes; the essay-not-finding paragraph names them. The new paragraph's reading ("adds little support", "what each instrument counted") is the essay's interpretation and reads as such.
7. The Later evidence notice follows site/README.md's form (`**Later evidence, 25 November 2026.**` blockquote) and says accurately what changed. The amendments' timing matches the briefs (LH033 amendment 2 after day 8, 29 October; LH034 amendment 1 after day 7, 28 October; both 30 October). "Stopped collecting them on 22 November" matches both records' Method (closure checkpoint of 22 November; LH033's last Censys read was 21 November, and its W3Techs read of 1 December tests nothing in the essay).
8. All 15 relative links resolve from essays/drafts/ (`../../`); on release they go back to `../` as the writer's note says.
9. British English throughout; no em or en dashes in the prose (only the Unicode minus in the notes' check code of the writer's note, not in the draft).
10. Disclosure: the combined disclosure stop of schedule/research-safety.md was applied to the draft, this note and the two reproduction scripts and outputs, together with what is already public. Everything here is aggregate public counts of versions (Censys's public dashboard, nodejs.org's published summaries) already in released or reviewed material; no host, address, exploit detail or anonymised party is named or inferable. Nothing to withhold.

## Changes made to the draft

Four small, unambiguous edits in essays/drafts/seen-from-outside-seen-from-inside-rev.md:

1. Later evidence notice: "downloads of older versions fell only a little" to "downloads of versions below the fix fell only a little". Beside "more downloads of three newer versions", "older versions" reads as everything else, including October's fixed releases, whose downloads fell sharply (LH034, Answer); the record's measure is below the fix.
2. "What the month did not show" paragraph: the same change.
3. Test B bullet: "nobody has checked whether a distribution's package" to "we haven't checked whether"; the record says only that this record didn't check (LH033, measure 3).
4. "What would test this": "after the first eight days of PHP's counts and the first seven of Node.js's had been read" to "after PHP's counts to 29 October and Node.js's to 28 October had been read"; the day counts were ambiguous (day 0 to day 8 is nine days), the dates are what the briefs say.

No figure changed.

## Verdict

**Not cleared.** One must-fix (item 1): the Correction notice and the `revised` item's "corrects" misstate version 1.0's range as wrong. Once resolved as suggested, the rest of the draft stands on the evidence; the fix is wording only and changes no figure, and a fresh agent's recheck of what the resolution writes follows, as AGENTS.md says.

## Resolution, by the driving session (25 November 2026)

- **Must-fix 1, accepted, in both the essay draft and the released piece.** The unrounded ends are 11.794 and 16.462 (studies/LH034/review/essay-rev-2026-11-25/repro_node.txt), which round to 12 and 16, so neither first edition was wrong. Essay draft: the Correction blockquote removed; the `revised` item now says it gives the range to one decimal, which is 12 to 16 in whole numbers as 1.0 had it. Released piece (articles/a-week-after-two-fixes.md, 2.0): the `revised` item reworded the same way, and the colophon's Corrections line now says "None", gives the range to one decimal with the unrounded ends, and says that an earlier wording of that line on 25 November wrongly called it a correction. The same wording fixed in investigations/software-updates.md and releases.md. The error came from R-0128's remark about rounding the printed 16.5, carried into the revision's brief.
- **Should-fixes:** test B's shortened gaps left as they are (the body is exact, and the piece uses the same wording); issues not searched (Harbour isn't named for this run), so the "nothing scheduled" claims rest on proposals.md and due.csv, as the note says.
