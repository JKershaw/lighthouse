# Checks for the day-30 revision of the first essay (draft, 25 November 2026)

**In short.** Where every changed or new figure in the draft revision of "Seen from outside, seen from inside" comes from, what changed from version 1.0 and why, and what could not be filled. Written by the writing subagent that drafted it (Claude Code, Opus 5.5 as reported by the harness), schedule row essay-first-rev, for the evidence review that comes next (row essay-first-rev-evidence-review). Every figure comes from LH033 version 1.2 and LH034 version 1.1, both reviewed, or from the revised piece released today (version 2.0); one consistency check on the weekend claim was computed here and is kept below.

Files: the draft, essays/drafts/seen-from-outside-seen-from-inside-rev.md (released 25 November as essays/seen-from-outside-seen-from-inside.md and removed; in git) (`status: draft`, links one level deeper). The released essay, essays/seen-from-outside-seen-from-inside.md, is untouched; version 1.0 is at commit ea594b9 (unchanged on main since). No web request was made.

Record references: "LH033" is studies/LH033/LH033.md v1.2 and data/record_v1.json; "LH034" is studies/LH034/LH034.md v1.1 and data/record_v1.json; "the piece" is articles/a-week-after-two-fixes.md v2.0.

## Changed or new figures

| Figure in the draft | Where it comes from |
| --- | --- |
| Correction: 11.8 to 16.5 per cent, days −7 to 7; "rounds to 12 to 17" | LH034 measure_2 daily table in record_v1.json (min 11.8 on day 2, 23 October; max 16.5 on day −2, 19 October; printed below); LH034 prose gives 12.7 to 16.5 for days −7 to −1 and 14.3, 11.8, 14.7 for days 0, 2, 7; the piece's Corrections line (same wording) |
| Unfixed Node.js 11.5 per cent a month on | LH034 measure 2 (`day30_unfixed_pct`) |
| Test B: line 22 8.0 points below (amended rule), 18.8 (as written); PHP 8.3 points (77.7 against 86.0) | LH034 test B (8.04 shown; 8.03 from unrounded means, R-0128; rounded to 8.0 as the piece does); LH034 18.83; LH033 amendment 2, test B |
| Test A: typical PHP branch's late share larger than typical Node.js line's under both rules | LH033 `amendment2`: PHP median L 0.275 (record prints 0.27); LH034 test A: 0.196 amended, −0.139 as written |
| PHP shares rose 1.3 to 3.0 points from day 23 to 30 | LH033 measure 1 paragraph and test A |
| Patched count up by more than a point of the branch in the last week only in 8.2 and 8.4; 8.3 and 8.5 from shrinking branch count | LH033 "What moved the later shares" (8.2: 186,517, 3.1 points; 8.4: 203,269, 5.9 points) and its test A paragraph |
| Day 7 to 14 patched counts up about 0.6 to 1.5 million every branch; after day 14 three barely moved, shares up mostly from fewer services | LH033 Answer and counts table; the piece |
| "Patched" probably includes services first seen fixed | LH033 Limits (interpretation, not checked with Censys) |
| Node.js late rise mostly added downloads of newer versions; older fell only a little; split post hoc | LH034 Answer ("What the late rise is") and Findings (post hoc, review/resolution_R-0131.txt) |
| Both counts did most of their rising within two weeks | the piece (title and summary), LH033 Answer ("Nearly all of it came in the first two weeks"), LH034 days 13 to 30 within a few points of day 14 |
| Day 30: PHP 75.0 to 92.2 per cent; Node.js 65.5 to 96.3 amended, 39.8 to 85.8 as written; three versions first seen 11 November; rule chosen after the counts; assumes unchecked they carry October's fix | LH033 measure 1 table; LH034 Answer and measure 1 summary; LH034 brief, amendment of 12 November |
| "three newer versions first seen on 11 November" (Later evidence notice) | LH034 Findings (`unlisted_above_fix_by_version`, first in day 21's downloads). The record's wording is kept rather than "released", since only the unreviewed one-off read (studies/LH034/oneoff-2026-11-25/note.md) dates the announcements |
| Unfixed PHP 22.5 million, 51.8 per cent, 20 November; 24.4 million a week after | LH033 measure 2 (22,516,583 of 43,438,950; day 7 24,386,744) |
| No-version share 62.3 per cent on 20 November | LH033 measure 2 (`unknown_pct_of_all` 62.3) |
| "two in five" reported a version on 28 October; "fewer than two in five" by 20 November | day 7: 59.55 per cent no version, so 40.5 reported (first edition, kept); day 30: 62.26 per cent no version, so 37.7 reported. Both from the reads' tables.json (`unknown_share_of_all` 0.5955 on 28 October in read-2026-10-29T0635Z, with `all` 110,944,946, the essay's 110.9 million; 0.6226 on 20 November in read-2026-11-21T1414Z) |
| Weekend days 15.6 to 18.1 million, weekdays 26.7 to 38.9 million, days 0 to 30 | LH034 Findings (`measure_2.summary`) |
| "every weekend day from late September on was below every weekday ... it stayed that way" over the month | computed here from LH034 record_v1.json's daily totals, 23 September to 20 November (below) |
| 8.3.8: June 2024, 11.1 per cent of 8.3 version-reporting services, 21 November; reason unchecked | LH033 measure 3 and its paragraph (php.net dates it 6 June 2024, read 21 November; snapshot of 21 November 13:15 UTC) |
| Strata "at our first read, on 25 October" | first edition's note (baseline read of 25 October); now dated in the text |
| Amendments fixed after PHP's first eight days and Node.js's first seven had been read | LH033 brief, amendment 2 ("after day 8 (29 October) was read and before any later day"); LH034 brief, amendment 1 ("after day 7 (28 October) was read and before any later day") |
| Collection of these counts stopped 22 November | LH033 Method and LH034 Method (checkpoints/2026-11-22-closure.md in each). LH033 still reads W3Techs's history on 1 December for measure 6, which tests nothing in the essay; hence "these counts" |

Unchanged figures (week one, Python, Packagist 10 per cent, 5.8 billion installs, the July comparison, Ubuntu's 8.3.6, the branches' release dates) were checked at version 1.0 (R-0042) and agree with LH033 1.2 and LH034 1.1, which changed no day-0-to-7 figure.

Weekend check, kept as code and output:

```
python3 -I -c "
import json,datetime
d=json.load(open('studies/LH034/data/record_v1.json'))['measure_2']['daily']
we=[(k,v['total']) for k,v in d.items() if datetime.date.fromisoformat(k).weekday()>=5]
wd=[(k,v['total']) for k,v in d.items() if datetime.date.fromisoformat(k).weekday()<5]
print(len(we),len(wd),max(we,key=lambda x:x[1]),min(wd,key=lambda x:x[1]))"
16 43 ('2026-11-14', 18082722) ('2026-10-02', 19912263)
```

So over 23 September to 20 November the largest weekend day (18.08 million) is below the smallest weekday (19.91 million). The Node.js unfixed series, days −7 to 7, from the same file: 16.2, 15.1, 14.9, 12.7, 14.1, 16.5, 15.6, 14.3, 13.3, 11.8, 13.0, 14.8, 12.4, 13.2, 14.7.

## What changed from version 1.0, and why

1. **Correction notice** for "12 to 16 per cent" (R-0128 via the piece's revision; notes/week-one-rev-checks-2026-11-25.md, release-time work). The text now reads 11.8 to 16.5, with 11.5 a month on.
2. **Later evidence notice** on the two readings fixed as tests on 30 October, linking both amendments. Test B held. Test A passed but adds little, following LH034 1.1 rather than LH033 1.2's "held"/"confirms" (as R-0133 and the piece do).
3. **A new paragraph in "Standing and rebuilt"** saying plainly that the month didn't show the slow accumulation the essay expected of the standing world: both counts did most of their rising within two weeks, and the late weeks mostly show what each instrument counted. This weakens one reading; the essay keeps its broader reading (two ways for software to exist) but says the month's counts add little support to the claim that the standing kind changes slowly. Labelled as made after the counts.
4. **Week-one comparison** kept and dated, with day 30 added under both Node.js rules and the post hoc label and unchecked assumption.
5. **Day-7 figures** dated or joined by day 30: version-reporting share, unfixed PHP (day 30 now leads, day 7 kept), no-version share, the old-branches comparison ("a week after the release and a month after"), the weekend totals, the strata dated to 25 October.
6. **"What would test this"**: the paragraph saying the briefs didn't fix the comparisons is replaced by what happened (fixed the same day, linked); each of the first two bullets keeps its original wording and gains a "Checked at day 30" result; the last two say that nothing is scheduled (the lockfile census proposal named as nearest); a line points to the proposal that would test the essay's broadest reading (blind spots on a characteristic side, P-0001); the closing promise is replaced by the statement that with collection closed no later count from these studies will test the readings further.
7. **Opening and header**: `status: draft`, a `revised:` item for version 1.1 (earlier edition at ea594b9), byline "revised 25 November 2026", the summary given one sentence on the month's result, the essay-not-finding paragraph now naming the post hoc Node.js rule and split.
8. **Notes and colophon**: record versions, the amendments, 8.3.8's source; the colophon records the revision and fulfils its promise, with reviews and release to follow.
9. **Links** one level deeper (`../../`); "the week-one piece" renamed "our piece on the two fixes", since its title changed at version 2.0.

Not added, by choice: the Apigee bulletin (from an unreviewed watch, and not needed for the essay's argument); W3Techs's 21 November point; the July and Python day-30 comparisons beyond what the bullets need.

## What could not be filled, and notes for the reviewers

- Review and release lines of the colophon: to be named when the reviews run. On release the links go back to `../`, `status: released`, and "(draft)" leaves the version line.
- "None of our studies or proposals looks for one" (Node.js servers seen from outside) and "None is scheduled" (build-server flag study) rest on a search of proposals.md and schedule/due.csv for Node.js, lockfile, installer and CI terms on 25 November; issues weren't searched (no Harbour or GitHub access in this task).
- The proposal links go to proposals.md as a whole; the site's anchors for P-0008 and P-0001 weren't checked.
- Whether the three newer Node.js versions carry October's fix is still unknown (LH034; the one-off read doesn't say).

## Where the records disagree or are stale

- LH033 1.2 says amendment 2's readings "held as written" and that "their passing confirms that the week-one pattern lasted to day 30"; LH034 1.1 says test A "passed, but it adds little". The draft follows LH034 (as the piece and R-0133 do). LH033's wording is already listed for the driving session in notes/week-one-rev-checks-2026-11-25.md.
- LH034's `measure_2.summary` gives days 0 to 7 as 11.8 to 14.8; the record's prose doesn't state a days −7 to 7 range. The daily table supports 11.8 to 16.5 (above).
- LH033's Next still names "LH034's version 1.0 and its reviews; then the revision of the week-one piece", both now done.
