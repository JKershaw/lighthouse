title: Evidence review of the week-one piece's month-on revision (version 2.0 draft)
kind: review note (evidence review, schedule row piece-week-one-rev-evidence-review)
date: 2026-11-25
reviewer: a fresh review subagent of the driving session of 25 November 2026 (Claude Code, Opus 5.5 as reported by the harness, not independently checked); a second agent's agreement is a review contribution, not independent confirmation

# Evidence review: "A month after two fixes" (version 2.0 draft)

**In short.** Every figure in the draft revision, its summary, title, short form and figure matches the reviewed PHP and Node.js records, and I reproduced the important ones from the retained raw reads with code written fresh for this review. Three things must change before the next review: the Apigee sentence says more than Google's bulletin does, the post hoc readings don't carry their number of comparisons or say that nothing can now test them, and the summary leaves out the assumption the Node.js headline figures rest on. Verdict: **not cleared**, with small fixes.

## What was reviewed

At commit 01bf397 (`git log -1 --format=%h`, 25 November 2026):

- articles/drafts/a-week-after-two-fixes-rev.md (version 2.0 draft)
- articles/drafts/a-week-after-two-fixes-rev-short.md
- articles/drafts/a-week-after-two-fixes-rev.svg, drawn by studies/LH034/scripts/draw_piece_figure_rev.py (its printed output is draw_piece_figure_rev_output.txt)
- articles/drafts/a-week-after-two-fixes-rev-checks.md (the writer's check note)

Against: studies/LH033/LH033.md (1.2) and its Censys bodies under data/; studies/LH034/LH034.md (1.1) with data/record_v1.json and the raw daily summaries; studies/LH034/oneoff-2026-11-25/ (note, fetch log, the three kept bodies); LH037's retained Apigee bodies (data/read-2026-11-02T1530Z and read-2026-11-23T1425Z, google__apigee-gcp-2026-072.raw.gz) and checkpoints/2026-11-02T1530Z.md; notes/php-flags-2026-11-02-decision.md; notes/R-0128, R-0131, R-0133; the first edition articles/a-week-after-two-fixes.md (16a713b); investigations/software-updates.md; programme.md's Next; essays/seen-from-outside-seen-from-inside.md. I made no web request.

## What I reproduced (code and output kept)

All code was written fresh for this review. None of it copies the records' scripts. It runs with `python3 -I` from the repository root.

- **Node.js**, studies/LH034/review/piece-rev-2026-11-25/node_repro.py, output node_repro.txt. It reads the raw day files (earliest read holding each day) and the 5 November release list. It reproduces: shares on days 1, 2, 3, 4, 7, 14 and 30 under both rules (day 30: 65.5, 74.3, 96.3 amended; 39.8, 60.6, 85.8 as written); first day at half (day 2 in every line); line 22 below half on days 3 and 4 only (amended); the new versions at 42.6, 34.8 and 74.2 per cent of their lines on day 30, each first seen on 11 November; the late-rise split (days 13 to 20 against 21 to 30, per-day means: at or above +18.4, +12.9, +25.8 per cent; below −4.0, −5.1, −6.5) and the daily ranges; line 22's below-fix counts (3.92 to 4.20 million on days 5 to 7; 2.64 to 3.56 million on the 15 weekdays from day 12 to 30); line 22's 27.7 of 34.5 per cent five or more releases behind; July's first day at half (18 and 4). For the unfixed tail, each day from −7 to 7 lies between 11.79 (day 2) and 16.46 (day −2), so **11.8 to 16.5**, and day 30 is 11.5. Every figure agrees with the draft and with LH034 1.1.
- **PHP**, studies/LH033/review/piece_rev_2026-11-25_php_repro.py, output piece_rev_2026-11-25_php_repro.txt. It reads Censys's body of 21 November (LH033 found no revisions, and I checked day 7 against the reads of 29 and 30 October, which are identical). It reproduces: patched shares on days 1, 2, 7, 14 and 30 (day 30: 78.2, 75.0, 86.5, 92.2); first day at half (6, 6, 2, 2); the older two below the newer two on every day from 1 to 30; patched-count changes from day 7 to 14 (+1,461,917, +1,531,891, +598,162, +737,917) and from day 14 to 30 (+55,421, +46,896, +311,748, +19,881); branch changes from day 14 to 30 (−311,749, −429,445, +142,373, −81,585); the unfixed tail of 22,516,583 of 43,438,950 (51.8 per cent) on day 30 and 24,386,744 on day 7; no-version services at 62.3 per cent on day 30, and the jump on 23 October (19.7 million to 53.6 million); 8.3.8 at 844,547, 11.1 per cent of 8.3; five or more behind at 60 and 71 per cent of what isn't counted patched in 8.2 and 8.3. All agree.
- **One-off read**, oneoff_check.py and oneoff_cve051.py, outputs .txt beside them, both in studies/LH034/review/piece-rev-2026-11-25/. They decompress the kept bodies in memory and don't run them. Each body's SHA-256 matches the fetch log. Each page carries "2026-11-11, Version … (LTS)", "This is a security release." and "Last Updated Nov 11, 2026". None contains "October", v22.23.4, v24.22.1 or v26.12.1. v22.23.5 lists 14 distinct CVE identifiers, and v24.22.3 and v26.13.1 list 15 each (see should-fix 5).
- **Apigee**, apigee_check.py and apigee_check.txt in the same folder. In both retained bodies (2 and 23 November), GCP-2026-072 is "Published: 2026-10-24", and the text quoted in the draft, "run PHP 7.3 or 7.4 on RHEL/CentOS 7, RHEL 8, or Amazon Linux 2, where no packaged fix is available", appears verbatim. The advice reads "Take the portal offline, or restrict access to internal networks. … Migrate to a Drupal 10 or Drupal 11 portal". The bulletin names "Apigee Edge for Private Cloud Drupal 7 and Drupal 9 developer portals (all versions)".
- **Figure.** The script reads LH033's tables.json, LH034's record_v1.json and LH011's release_days.csv, with no hard-coded values, and its printed days 1, 7, 14 and 30 match the records. I rendered it at 720 px wide in light and dark with the container's headless Chromium and looked at both. Both are legible. Labels and leader lines match the data at day 30. The thin as-written lines start at day 20 as captioned, and the day-21 marker is labelled. The right-hand labels in the top panel are crowded ("Node.js 22 65.5%", "Python fixes, range", "Python, median", "24, as written 60.6%") but each can be read and is attached to the right line. The dark theme keeps contrast. No em or en dashes.

## Checks of claims and form

- **Title and summary absolutes.** "Most of their rising within two weeks" holds for every PHP branch and, under both rules, for every Node.js line (from day 0 to 14 against day 14 to 30; as written, the share fell after day 21). "More than half" is 51.8 per cent on 20 November, inside the window the title gives ("a month after"). No never, always, all or none appears without its window.
- **Labels.** Censys shares are called floors, downloads requests, the amended rule post hoc with its unchecked assumption (in the body), the crossing with Python an untested interpretation, test A weak, following LH034 1.1 rather than LH033 1.2's "held", and the Apigee statement one vendor's, from an unreviewed watch. The one-off read is labelled as not yet through the record or its reviews. All of this follows the row's three instructions.
- **Consistency.** The draft says the same as LH034 1.1's Answer and LH033 1.2's Answer on every figure, and on the late rise. It is weaker than LH033 1.2 and programme.md's Next on test A ("held as written"), as instructed (should-fix 6).
- **Form.** British English. No em or en dashes in prose. No study numbers or document names in the prose. The colophon has named links and a line on Lighthouse. "The study" and "the study's record or its reviews" come near internal reference, but they're plain words (note).

## Findings

### Must-fix

1. **The Apigee sentence goes beyond the bulletin.** The draft says the bulletin "names a piece of the old layer that, by the vendor's account, neither PHP nor the distributions underneath it will patch." The bulletin says only "where no packaged fix is available", in the present tense, as of 24 October. It says nothing about the future, and nothing that speaks for the distributions. Suggested: "…a piece of the old layer for which, by the vendor's account, no packaged fix was available."
2. **Post hoc readings lack their number of comparisons, and nothing says whether they can be tested** (AGENTS.md, Evidence). The late-rise split ("We worked this out after every count was in") is one of three pairs of day windows the record looked at (LH034 Findings: "three pairs of day windows, all reported here or under test A"). The piece shows one pair and gives no count. Neither it, the amended rule, nor the crossing with Python says what will test it, or that nothing can now that collection has closed. The first edition did this for its own post hoc comparison ("which no later count can test"). Suggested: give the count, for example "one of three ways we split the days, all chosen after the counts", and add a clause that collection has closed, so nothing here will test these readings. For the amended rule, name what would settle it (the project's November advisory, or the October CVE list against the November releases' contents) or say it's untested.
3. **The full summary leaves out the assumption behind the Node.js headline figures.** The summary leads Node.js with 65.5 to 96.3 per cent "counting three versions first seen on 11 November as fixed, a rule chosen after the counts were seen". It doesn't say that the rule assumes, unchecked, that those versions carry October's fix. LH034's opening and the investigation page both say so, and so do the short form and the body. A summary is read without the body. Suggested: "…as fixed, which assumes, unchecked, that they carry October's fix, a rule chosen after the counts were seen…".

### Should-fix

4. **"Between those two stretches, downloads at or above the fix rose by 18.4 …"** These are changes in per-day means over stretches of 8 and 10 days, not changes in totals. Add "on an average day" or "on average".
5. **The one-off note (not the piece)**, studies/LH034/oneoff-2026-11-25/note.md, says v26.13.1 has "one more entry, CVE-2026-126051", as if v24.22.3 lacked it. The kept bodies show CVE-2026-126051 ("tls: fix remotely reachable TLS server crash") in the notable changes of both v24.22.3 and v26.13.1 (oneoff_cve051.txt). The note also says none of the three mentions October's "flaws". Without the October CVE list, which isn't retained, that can't be checked. It can only say they don't mention October's release or the versions it fixed. I made the matching edit in the piece (below). The note should be corrected before the reader review relies on it.
6. **Consistency before release.** programme.md's Next says of LH033 "amendment 2's two post hoc readings held as written". LH033 1.2's Answer says both "held as written" and that their passing "confirms that the week-one pattern lasted". The piece, following LH034 1.1, says test A "passed too, but it tells us little". The release round should align programme.md's line and the investigation page with the weaker reading, or give LH033 a dated note. The investigation page's line for the first edition ("to be revised after the day-30 reads") needs updating at release.
7. **The essay carries the corrected figure.** essays/seen-from-outside-seen-from-inside.md (released) says "Node.js's unfixed share, 12 to 16 per cent of daily downloads around the release". When this revision's correction is released, the essay needs a dated Correction notice. Its week-one figures and testable readings, now checked at day 30, may also warrant a Later evidence notice.
8. **The distribution caveat is gone from both summaries.** The first edition's reader review (R-0040) added to the summaries that some old-branch services "may be patched by Linux distributions under the old number, which we have not measured". Both new summaries keep only "as their versions report them". The body keeps the caveat. Consider restoring it in a clause, especially now that the body adds the Apigee counter-instance.
9. **The short form's summary**, "what rose after came mostly from changes in what was counted", fits PHP (fewer services counted). For Node.js the late rise was more downloads of the newer versions, which a reader could take for a counting artefact. Suggested: "…came mostly from fewer PHP services counted and more Node.js downloads of newer versions, not from fewer left behind."
10. **W3Techs "at the end of October"**: the 2 to 8 per cent is from 25 and 26 October (LH033 measure 4), and W3Techs's 1 November point is already 10.1 to 22.8. Say "on 25 and 26 October".

### Notes

- The short form's "(their own announcements don't say)" rests on the unreviewed one-off read. It's accurate, but the short form doesn't label it unreviewed as the piece does.
- "A few points higher in the last ten days" covers a 1.3-point rise in line 26 on means. That is the record's own wording.
- "Showing a version" excludes Censys's 3.07 million "implausible" services, as LH033 does. Not an error.
- At release, the relative links (`../../`), the figure path, the revision date and the colophon's review line need setting, as the check note says.

## Changes I made

- articles/drafts/a-week-after-two-fixes-rev.md: "None of the three mentions October's release or its flaws." became "None of the three mentions October's release or the versions it fixed." Why: the October CVE identifiers aren't retained, so absence of "its flaws" wasn't checked. The kept bodies show no mention of "October" or of v22.23.4, v24.22.1 or v26.12.1 (oneoff_check.txt).

No other file under review was edited. I didn't touch the records or the schedule.

## Files written

- notes/R-0138-week-one-rev-evidence.md (this note)
- studies/LH034/review/piece-rev-2026-11-25/node_repro.py and node_repro.txt
- studies/LH034/review/piece-rev-2026-11-25/oneoff_check.py and oneoff_check.txt
- studies/LH034/review/piece-rev-2026-11-25/oneoff_cve051.py and oneoff_cve051.txt
- studies/LH034/review/piece-rev-2026-11-25/apigee_check.py and apigee_check.txt
- studies/LH033/review/piece_rev_2026-11-25_php_repro.py and piece_rev_2026-11-25_php_repro.txt

## Verdict

**Not cleared.** Must-fix 1 to 3 are small edits. After them, and after the reader-and-inference review, a fresh agent should read what the resolution writes once, as AGENTS.md step 4 requires.

## Clearance check, 25 November

Checked at commit 3281f40, by the same reviewer. I compared the draft, the short form and the one-off note against 01bf397 (`git diff 01bf397 3281f40`).

- **Must-fix 1 (Apigee): met.** The sentence now reads "a piece of the old layer for which, by the vendor's account, no packaged fix was available when it wrote, on 24 October". That matches the retained bulletin text (apigee_check.txt).
- **Must-fix 2 (post hoc readings): met.** The late-rise split is now "one of three ways the study split the days, all chosen then; collection has closed, so nothing will test it on fresh data", which matches LH034 Findings' three pairs of windows. The amended rule is "the one counting rule the study added after seeing outcomes", which matches LH034's "one post hoc rule", and the piece now says what would settle it and that nothing scheduled will. The crossing with Python is labelled post hoc and untestable now. The two predictions get "no later count from these studies will test them further".
- **Must-fix 3 (summary): met.** The full summary now says the rule "assumes, unchecked, that they carry October's fix".
- **The changed sentences, against the records.** "On an average day … 18.4, 12.9 and 25.8 per cent higher … 4.0, 5.1 and 6.5 per cent lower" matches node_repro.txt (per-day means). "On 25 and 26 October" is right for the W3Techs figure. The distribution caveat restored in both summaries is the body's own. The short form's new summary ("fewer PHP services counted and more Node.js downloads of newer versions, not from fewer left behind") matches both records. The one-off note's corrected CVE lines are right: the kept bodies give 14 distinct CVE identifiers for v22.23.5, and v24.22.3 and v26.13.1 have identical sets of 15, which add CVE-2026-126051 (checked in memory). Its "can't be checked" wording on October's flaws is right. No em or en dashes were added. I found no new factual error.
- Should-fix 6 and 7 (aligning programme.md and the investigation page, and the essay's notice) remain release-time work, as the check note says. They don't block clearance of the draft.

**Verdict: cleared.** Nothing in the evidence review must still be fixed. The reader-and-inference review and the single fresh-agent reading of its resolution still come before release.
