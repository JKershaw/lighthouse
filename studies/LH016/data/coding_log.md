# LH016 first coder's log, primary frame

Written 29 September 2026 by the first coder, a subagent on Opus 5.5 (claude-opus-5-5, as its harness reports), for studies/LH016/data/changes.csv. Repository at cb97e4e; nothing committed by the coder.

## Read before coding

AGENTS.md and studies/LH016/brief.md in full; studies/LH016/scripts/draw_sample.py and compare_blind.py, to match the table's columns and values to them. From notes/closeout-2026-09-28-two-day-pace.md only the section "Addendum: the revision of the same evening", and from notes/closeout-2026-09-29-claims-and-review-pilot.md only "What changed in the public claims" (headings listed with `grep -n '^#'`, then `sed -n` on the section). Not read: notes/reader-review.md, releases.md, studies/LH016/data/costs.csv, any other close-out, anything under harbour/.session/. No web request.

Commands used in every window: `git log --oneline --reverse 1bc6e80^..cb97e4e`; `git diff --stat A B`; `git log -1 --format=%B B`; `git diff --word-diff=plain A B -- <coded surfaces>` (filtered with grep for the changed spans where paragraphs were long); for figures, the drawing script's diff and the SVG's changed text only; `cat` of the window's review note.

## Conventions applied throughout

1. Not coded, as release bookkeeping or outside the brief's surfaces: `status`, version numbers, colophons (a piece's Methods, Sources and Corrections bullets included), releases.md, a record's header lines (version, authors, grounded_at), a record's Corrections entry where it documents a change coded elsewhere, programme.md's dated header line, AGENTS.md outside "Where things stand" (the rule changes in 6cb9051, c480bb0 and f17523c), CLAUDE.md, data files and scripts.
2. One row per problem per window. A change's tier is the highest its surfaces reach; `before` and `after` quote the public surface for A, the record for B, the decision surface for C.
3. `passed_by`: earlier steps in the round that read the passage while the problem was in it and did not fix it, including a step that edited the passage for another reason (said in `comment`). R-0014 and R-0016 count as the earlier step for P2 and P4, as the task directs, written E, or E(R-0016) and E(R-0017) where a round has two evidence reviews. A step that introduced the passage is not listed. Blank for pure additions and for N rows.
4. `also_raised`: a later step in the round that raised the same problem again; also R1 where stage 1 noted a problem that stage 2 then fixed (P4-21, P5-06, P6-19), since stage 1 changes no text and cannot be credited.
5. `post_release`: yes for every P2 and P4 row, since those rounds began after their piece's release (a36508d, 89d4aa7); no in P1, P3, P5 and P6, whose rows precede their piece's release. Earlier releases of other pieces were not taken to make every later change post-release. Rows in P2's and P4's later windows that fix text the K step had just written say so in `comment`.
6. `post_hoc`: yes for readings made after the counts, for changes that add or correct a post hoc label, and for decisions that schedule a test of such a reading. No for rule corrections made after the counts (P3-01, P6-01, P6-02, P6-03) and for a sensitivity of a pre-set rule (P3-06); each is noted in `comment`.
7. `improved` on C rows: yes for a correction, pending for a decision.
8. `evidence` cites the record or retained data, never a review note, because draw_sample.py shows it to the second coder; notes are in `named_in` and `comment`. In the visible columns, references to a review were cut with "..." where the quotation allowed; they remain where the text is about the review itself (P5-24, P6-04, P6-35).

## By window

**P1, 1bc6e80..a36508d (E, R-0014).** Diffs of the piece, short form, SVG desc and draw_piece_figure.py, LH011.md, brief.md, programme.md, README.md, AGENTS.md; R-0014. 10 rows. Hard: P1-02 is A because programme.md's answer changed ("stayed flat"), type scope rather than certainty; P1-03 is B because programme.md gained only "per-release"; R-0014's item 6 split into P1-06 and P1-07 (two wrong wordings); P1-08 corrects the literature grounds in programme.md's Next without changing the selection, coded C with direction correction; P1-09 and P1-10 are D (issue number, short-form link).

**P2, a36508d..6cb9051 (K).** Diffs of the piece, short form, synthesis and its short form, README.md, AGENTS.md, investigations/software-updates.md, programme.md, LH011.md; `git log -1 --format=%B 6cb9051`; the close-out's Addendum. 15 rows. Hard: the reframing split into five A rows (P2-01 to P2-05) and four C rows (P2-06 to P2-09); the piece's new paragraph on three explanations was counted under the C row P2-07, since a reader would still say the cause is unknown. P2-11 to P2-15 are D: named only in the record's or short form's own Corrections, or not at all.

**P2, 6cb9051..c2e4d4e (E, R-0015).** Diffs of the piece, short form, programme.md, LH011.md; R-0015. 8 rows (P2-16 to P2-23). P2-23's passed_by is K only: R-0014 read that sentence when it matched the record.

**P3, 08c505b..89d4aa7 (E, R-0016).** Diffs of the piece, short form, programme.md, LH012.md, amendments.md; R-0016. 6 rows.

**P4, 89d4aa7..c480bb0 (K).** Diffs of the piece, short form, the notices on the synthesis and the pace piece and their short forms, README.md, AGENTS.md, investigations/software-updates.md, programme.md, LH012.md, and LH013's new brief (read in part); `git log -1 --format=%B c480bb0`; the close-out's section. 7 rows. Hard: P4-04 (the frozen-list fit dropped from both summaries and README) is A and D, but may have been cut for length; P4-05 (README cut) is N and K, named in the close-out; P4-07 is a one-day-against-week scope fix on decision surfaces, coded C as for P1-08.

**P4, c480bb0..e26c856 (E, R-0017, and the driving session's follow-up).** Diffs of the piece, AGENTS.md, investigations/software-updates.md, programme.md, LH012.md, LH013's brief; R-0017. 9 rows. Hard: P4-15 ("kept off" to "ruled out") is named in the e26c856 message as the driving session's own follow-up and not by R-0017; coded D. P4-09 and P4-14 are credited to E, whose note names them, though the driving session made part of each edit. R-0017's item 4 (a piece's Corrections bullet) is colophon and not coded.

**P4, e26c856..abca590 (R1, R-0018 stage 1).** Only notes/R-0018.md changed. 0 rows.

**P4, abca590..c8d2a89 (R2).** Diffs of the piece, short form, synthesis notice, README.md, AGENTS.md, investigations/software-updates.md, programme.md, LH012.md, LH013's brief; R-0018 whole. 7 rows. Hard: P4-20 (aiobotocore's maintainer) has no fitting type and is left blank; R-0018 called it readability.

**P4, c8d2a89..4253613 (RC).** Diffs of the piece, investigations/software-updates.md, programme.md, LH012.md, LH013's brief; R-0018's Recheck. 4 rows. P4-24 is A although the recheck called it not material; P4-26 (flatness wording) is unnamed, so D.

**P5, 9523003..63d8a62 (E, R-0019).** Diffs of the piece, short form, AGENTS.md, LH014.md; R-0019. 5 rows.

**P5, 63d8a62..6497799 (R1).** Only notes/R-0020.md. 0 rows.

**P5, 6497799..be156d5 (R2).** Diffs of the piece, short form, README.md, AGENTS.md, the four notices, investigations/software-updates.md, programme.md, LH014.md; R-0020 whole. 9 rows. The record's post hoc block was split by reading: inherited share (P5-07), single releases (P5-08), mirrors' tail (P5-09), single days (P5-11), between groups (P5-12).

**P5, be156d5..8d21cdd (RC and release).** Diffs of the piece, short form, AGENTS.md, investigations/software-updates.md, programme.md, LH014.md; R-0020's Recheck. 10 rows, three of them N. P5-21 is credited to RC though it scopes the absolute rather than naming band A's library, as the note proposed.

**P6, 2135c64..3ca1804 (B, R-0021 stage A).** Only the note and review files. 0 rows.

**P6, 3ca1804..c488d2a (corrections after the blind check).** Diffs of the piece, short form, SVG labels, README.md, AGENTS.md, the synthesis notices, investigations/software-updates.md, programme.md, LH015.md, amendments.md, and data/pair_classes.csv (to split the figure changes by rule); R-0021 stage A. 11 rows. The brief has no step code for this window: changes whose rule or gap stage A names are credited to B, the rest to D (P6-03, P6-10, P6-11). The lock-unused count (8 to 7) moved with P6-01 and P6-03 together.

**P6, c488d2a..b1e2c99 (E, R-0021 stage B).** Diffs of the piece, short form, SVG, synthesis notice, LH015.md; R-0021 stage B. 7 rows. P6-15, P6-16 and P6-17 are not among stage B's listed changes, so D. P6-18 (chart footer) is credited to E, which proposed it without making it.

**P6, b1e2c99..92d2013 (R1).** Only notes/R-0022.md. 0 rows.

**P6, 92d2013..ab2b12c (R2).** Diffs of the piece, short form, README.md, AGENTS.md, the synthesis notices, investigations/software-updates.md, programme.md, LH015.md; R-0022 whole. 10 rows.

**P6, ab2b12c..f17523c (RC and release).** Diffs of the same surfaces; R-0022's Recheck; `git log -1 --format=%B f17523c`. 7 rows. P6-32 is N (a statement of what the study read, not of the internet). P6-34 and P6-35 are C and D: decisions recorded at release that no note names (the commit message does).

**After f17523c.** `git log --stat f17523c..cb97e4e`: only cb97e4e, which adds studies/LH016's files. No primary-frame piece changed; no rows. The gaps between rounds (c2e4d4e..08c505b, 4253613..9523003, 8d21cdd..2135c64) hold the research drafts and LH013's amendment 1 (353f17f); they lie outside the brief's windows and were not coded.

## Rows

125 in all: P1 10, P2 23, P3 6, P4 27, P5 24, P6 35.

## Problems met with the brief's windows and codebook

1. B lists Answer, Findings, Method, Limits and Corrections, and C is "the next research step changes". A factual correction on a decision surface that changes no decision (P1-08, P4-07, P4-12, P4-13) and a factual error in a record's Next (P2-11) fit no tier cleanly; coded C and B respectively, as said above.
2. The type list has no value for a plain factual description (P4-20, left blank).
3. D is "a change ... that no note, commit message or close-out in that window names", but outside the K windows the attribution rule credits only a note; a commit message that names the driving session's own follow-up (P4-15) leaves the change with no step but D.
4. The window 3ca1804..c488d2a has no step code in the brief; see P6 above.
5. Read literally, "any change after a release commit" makes every row after 28 September post-release; applied per round's piece instead.
6. The R1 windows change no text by design, so stage 1 appears only in `also_raised` and `passed_by`.
