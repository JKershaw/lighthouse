# R-0076: fresh reading of what resolved R-0072's instrument findings (LH044, 16 November 2026)

**In short.** I read once what was written to settle the three instrument findings of the read-1 evidence review: brief amendments 7, 8 and 9, the code that carries them, and the checkpoint's second Correction and "(amended 16 November)" passages. Each amendment is dated, labelled post hoc, and says it was decided after read 1 and its review were seen. The new challenge signature catches P17's and P38's robots.txt pages and nothing else in the 1,178 retained files. The egress rule's reasoning rests on what the rule is for, not on the count it produces, and it says plainly that its writer knew it decides P38. Every changed count follows from the retained files, and the tests pass. **Cleared**, with no must-fix finding. I changed nothing.

**Reviewed version:** repository HEAD 6bdcd533a6f1d41808235be98c24665df24a1d5c. studies/LH044/ is identical to commit 94b8ef8, the commit that wrote the resolution (`git diff --stat 94b8ef8 HEAD -- studies/LH044` is empty).
**Reviewer:** a fresh rechecking subagent in Claude Code on Opus 5.5, dispatched by the driving session (row LH044-amend-read1). This is AGENTS.md step 4's single reading of a round that resolved a review. I share a model family with the writer, so my agreement adds to the review but does not confirm it independently.
**Date:** 16 November 2026. **Requests made:** none (offline).
**Inputs:** notes/R-0072-lh044-read-01.md; `git diff 94b8ef8~1 94b8ef8 -- studies/LH044`; brief.md amendments 7 to 9; checkpoints/2026-11-15.md; review/amend7_replay.py and its output; data/read-2026-11-15T1413Z/ and data/read-2026-11-08T1920Z/ (classes.csv, readlog.csv, summary.json, echoes.csv, bodies, rdap/).

## What I checked

1. **Dating and labels.** All three amendments carry the date 16 November 2026 and the words "post hoc". Each says it was made after read 1 and R-0072 had been seen, and says what was known:
   - Amendment 7 says the signature was "written after these two pages were seen, from them alone".
   - Amendment 8 names row 179's `powf:` echo, which the read-1 writer had found by hand.
   - Amendment 9 says it was decided "by a writer who knew it decides whether P38's closing is compared". It also gives the count before and after.

   Each amendment also says what is in force when. Amendment 7 is not retroactive: read 1 stays at classifier 0.3, matching `AMENDMENT7_FROM = '2026-11-16'` in classify.py. Amendment 8 is applied to read 1's derived tables. Amendment 9 is applied to read 1's comparison and says so.

   The checkpoint's second Correction carries the same post hoc label. It points to the earlier edition at 11d26f2, which is the right parent: that commit last changed the checkpoint before 94b8ef8.
2. **The classifier signature.** I reran `python3 -I studies/LH044/review/amend7_replay.py` and its output is identical to the kept amend7_replay-output.txt:
   - only P17 and P38 change, from `refused` to `wall_at_robots`;
   - the drawn row goes from 28 probes answered to 26, and from 3 walls at robots.txt to 5;
   - walled and read counts are unchanged;
   - closings and openings are unchanged (A11, P38 and P40 closing; A13 opening).

   The replay scans only `*.b` bodies of the two reads. I scanned every file under studies/LH044/data/ as well (1,178 files, including Wayback, statements, HTTP Archive and prebrief, gzip-decoded where needed). Both alternatives of `CHALLENGE_SIGS_04` match only read-1 bodies 0202.b and 0235.b. No file carries the title "One moment, please" without matching. The test suite also checks that the title alone, without a self-reload or check field, is not a challenge, and that a real robots.txt (P40) still parses.
3. **The egress rule.** The reasoning does not choose by verdict.
   - It rests on the rule's stated purpose: a wall that moves because our address moved.
   - It rests on the observation that the plain-HTTP route already gave each echoing request a different address at the baseline.
   - It applies alike to both routes and to either direction of change.
   - It keeps the earlier reading in the checkpoint, so a reader can apply that reading instead.

   The stated limit is honest: a block list keyed to one of a provider's networks would be missed, and the address P38 saw is unknown at both reads. The checkpoint repeats this limit beside P38.

   `compare_reads.py 2026-11-08T1920Z 2026-11-15T1413Z` prints direct-http as GOOGL-2 (Google LLC) at both reads, so unchanged. It prints egress-proxy as AP-2440 (Anthropic, PBC) at both reads, also unchanged. Both verdicts come from the kept RDAP records.

   *Not blocking:* the evidence that the route rotates is two echoes at the baseline and one at read 1. The amendment states those numbers rather than claiming more.
4. **The checkpoint's changed counts.** From classes.csv as read, against the baseline:
   - 3 closings: A11 (named), P40 and P38 (drawn);
   - 1 opening: A13 (named);
   - under the 0.4 replay, drawn reads 26 probes answered and 5 walls at robots.txt.

   These match the Correction and the amended paragraph. The counts table rightly keeps 28 and 3, the classes as read. The In short gives no closing count, and its statement that the evidence review changed none of its counts still holds, because the amendments change none either.

   The new data is regenerated correctly. echoes.csv gains only row 179 (P04, direct-http, `powf:`, 35.184.25.35). summary.json gains `robots_parsed_html` [O13, P17, P38] and the route's echo. classes.csv is not in the diff.
5. **Tests.** I ran `python3 -I studies/LH044/scripts/test_lh044.py`: 93 checks passed and 0 failed (exit 0), matching review/test_lh044-amend7-output.txt. It left the working tree unchanged.

## Verdict

**Cleared.** I found nothing that must be fixed.

## Changes I made

None.
