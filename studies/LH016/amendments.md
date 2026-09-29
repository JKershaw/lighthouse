# LH016 amendments

Dated changes to the brief (studies/LH016/brief.md, fixed at cb97e4e, 19:03 UTC). Each says when it was made and what had been read by then. The headings first gave times estimated by the driving session (about 19:40, 20:05 and 20:40 UTC), which were wrong; at 19:48 UTC they were corrected to the times of the commits that carry each amendment.

## Amendment 1, 29 September 2026, committed at 19:27 UTC (7fb7714)

Made after the secondary frame's reader had written its tables and reported, and before the driving session read any of its rows or any row of the primary frame.

- **The secondary frame was coded change by change.** The brief said it would not be; the reader's task text asked for one row per change in the primary table's columns, and the reader followed the task. The rows are kept, and M4 reads them.
- **Rows in both frames are counted once.** The synthesis is a secondary-frame piece, and some of its notices were added or revised inside the primary windows of P2 and P4, where the primary frame codes notices added to other pieces. The reader marked each such row "also in the primary frame"; scripts/tally.py now counts those rows in the primary frame only.
- **`passed_by` in the secondary frame** names the checks before release that read the passage, the release review notes R-0001 to R-0013 and notes/review-2026-09-26-first-articles.md, and for notices added from 28 September on, the reviews of those rounds. In the primary frame it keeps the brief's meaning, the earlier steps in the same round.
- **Steps the brief did not code.** The adversarial review of the improvement round (notes/R-0013.md) is coded E. Colophon "Update" lines that carried later evidence for LH007, LH008 and LH009 on 27 September are coded as public surfaces, although the brief excludes colophons, because on that day the evidence was carried nowhere else on those pieces.
- **The history is shallow.** This clone's history begins at db300e2 (26 September 2026, 09:24 UTC). The first drafts of 26 September and the commits the first-articles review and notes/R-0001.md were grounded at (e0b7ca4, 5a0adf3) cannot be read, so what the secondary reader says of them rests on the notes, the record headers and notes/retro-first-drive.md. No primary window is affected.

## Amendment 2, 29 September 2026, committed at 19:35 UTC (2b2f0c7): a known-answer replay of the reader review

Made after the keeper raised this drive's bound to about fifty dollars, before the driving session read any row of either frame and before any replay ran.

**Why.** The frames say what each step changed in its place in the order; they cannot say what a step would catch on its own. The keeper's reading caught problems in two released pieces (LH011's at version 1.0, LH012's at version 1.0) after the evidence review had passed them, before the reader-and-inference review existed. Replaying the reader review, as it now stands, on those two texts as released asks whether it would have caught them before release. Its stage 2 text carries a list of prompts written after those very corrections, so a second variant removes the list, to ask whether what it catches comes from its structure (read as a reader first, then the record) or from its checklist.

**Runs.** Three, each a fresh Fable 5.1 agent, dispatched by notes/reader-review.md's rules (stage 1, then stage 2 by message to the same agent after stage 1 returns; no recheck, since nothing is released):

| Run | Target, as released | Variant |
| --- | --- | --- |
| X1 | LH011's piece 1.0 (articles/two-days-for-most.md), its short form and README.md's "Current focus", at a36508d; stage 2 reads studies/LH011/, the investigation page and programme.md's Next at a36508d | V1, the task texts of notes/reader-review.md as they stand |
| X2 | the same | V0, the same texts without the stage 2 sentence of prompts ("Where they apply, and only if they matter, consider: ... These are prompts for judgement, not categories to fill.") |
| X3 | LH012's piece 1.0 (articles/old-versions-new-pythons.md), its short form and README.md's "Current focus", at 89d4aa7; stage 2 reads studies/LH012/, the investigation page and programme.md's Next at 89d4aa7 | V0 |

The texts are kept as review/replay_stage1_text.txt, review/replay_stage2_text_prompted.txt and review/replay_stage2_text_naive.txt. Each run works in a git worktree of its target commit in the session's scratchpad, is told not to run git and not to read outside that worktree, and writes its note inside the worktree; the note and any calculation are copied to review/replay-X1/ and so on. No next study's brief or issue is given, because the issues were edited after those commits; programme.md's Next at the commit stands for it. Allowance about six dollars a run at list rates.

**Known answers, fixed here.** From the revision commits' messages (6cb9051, c480bb0) and, for LH012, the three problems notes/reader-review.md's log records for its rehearsal on the corrected text.

- For X1 and X2 (LH011's piece 1.0): K11-1, the title's "never" holds only for the month read (an absolute without its window); K11-2, the brief's pre-set label given where the numbers should be; K11-3, a download counts fetches, so a low share of downloads is not by itself a slow spread; K11-4, the first-day observation was read after the counts and not labelled so; K11-5, the next question should be what keeps older versions downloaded across all 37 libraries, not only the eleven.
- For X3 (LH012's piece 1.0): K12-1, what other libraries' limits could account for is a model's estimate resting on an assumption the log cannot check, presented as what they did; K12-2, an old Python rules out the new version without saying which older versions were fetched (boto3's downloads from Python 3.9 sit mostly below the last version 3.9 can take); K12-3, downloads sharing reported fields called one kind of machine; K12-4, boto3's and aiobotocore's older downloads have the flat count-by-version profile of an installer's resolution walk; K12-5, three of the four holds by identified bounds come through older dependent versions; K12-6, the ten-point settling band is lenient for small shares.

**Scoring.** A known problem is **found** if the run's note, in either stage, names the passage or claim and the fault in substance; **partly** if it names the passage with another fault, or the fault in general terms without tying it to the passage; **missed** otherwise. Problems the run raises that are not on the list are listed and judged against the record, not scored. The driving session scores against the lists above, quoting the note, in review/replay_scores.csv; the evidence reviewer of this record checks the scores. Three runs of one model on two texts are cases, each one draw of a stochastic reviewer: they say what the instrument can catch, not how often it would.

## Amendment 3, 29 September 2026, committed at 19:41 UTC (1322a43): the first coder's conventions

Reported by the first coder with its table, and recorded before the second coder's sample was drawn and before the driving session read any row or tally. They are the coder's readings of the brief where it was silent or loose, and the tally takes them as coded.

- **Corrections on decision surfaces.** Four factual corrections on surfaces that carry decisions, which change no decision, are tier C with direction correction (P1-08, P4-07, P4-12, P4-13); a factual error in a record's Next is tier B (P2-11).
- **A plain factual description** has no type in the codebook's list; P4-20 (who maintains a library) has its type blank.
- **Step D** takes a change that only a commit message names as the driving session's own follow-up (P4-15), since outside the K windows the attribution rule credits a note.
- **The window after the blind check** (3ca1804 to c488d2a) is credited to B where notes/R-0021.md's stage A names the problem, and to D otherwise.
- **`post_release`** is yes for changes to the round's own released piece, so every P2 and P4 row, and no elsewhere; read literally, the brief's wording would have covered every row after 28 September.
- **The reader review's stage 1** changes no text, so it appears only in `passed_by`, and in `also_raised` where its note named a problem stage 2 then fixed (P4-21, P5-06, P6-19).
- **Rule corrections made after the counts** (P3-01, P6-01 to P6-03) and one sensitivity of a pre-set rule (P3-06) are coded `post_hoc` no, each with a comment; the record reports them beside M5.
- **Release bookkeeping is not coded**: status lines, versions, colophons (a piece's list of corrections included), releases.md, record header lines, and AGENTS.md outside "Where things stand".
- **The `evidence` column**, which the second coder sees, cites records and retained data and names no review, except in three rows about a review itself (P5-24, P6-04, P6-35), none of which was drawn.

## Amendment 4, 29 September 2026, committed at 20:22 UTC (1c3133a): what replay X2 read

Recorded after the evidence review (notes/R-0023.md) pointed it out; it changes no figure. The brief says the study reads no download count. Replay X2, in its stage 2, read ClickPy's by-version table four times, anonymously, at 19:52 UTC on 29 September 2026: boto3's and botocore's downloads by version on 12 August 2026 and litellm's on 4 June and 15 September 2026 (review/replay-X2/x2_requery.txt and x2_requery_data/). A reader review may make its own reads, as notes/reader-review.md allows, and the driving session did not forbid them in the replay's task text, which was the review's own. None of the four days lies in LH013's weeks (28 September to 11 October 2026), so nothing of them was read. The record's header, Method, Finding 12 and Limits now say so.
