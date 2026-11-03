# R-0047: reader-and-inference review of the 3 November later-evidence notice on articles/old-versions-new-pythons.md

## What a reader would believe, written before reading the record

**Principal finding, said back.** In late September 2026 about a third of the typical big Python library's downloads were of older versions. Pythons too old for the new version explain most of that only for boto3, aiobotocore and numpy. Most of boto3's Python 3.9 downloads look like pip trying and throwing away versions, not installing them. The new notice says that when Lighthouse looked again at the next two weeks, using tests written down before reading, all of this came out the same.

**Observed.** Week-one shares and Python breakdowns. Then, for 28 September to 11 October: a typical share of about 37 per cent in each week; 32 of 37 libraries within five points; the same three old-Python libraries; and boto3's four patterns (65 per cent from Python 3.9, a boto3-to-botocore ratio of about 7 to 8, 95 in 100 below the last supported version, near-level counts that fall in steps at the same places).

**Explained.** Nothing new. The installer-search reading stays a reading. The notice says pip's own version, in the full log, could test it.

**Caused.** Old Pythons rule out new versions for three libraries. Nothing else is shown to cause anything.

**Limits a reader notices.** Only two adjacent weeks, the same libraries; the similar shapes in other libraries were not tested. A reader may take "held" (in the README line too) to mean that the explanation held, not the counts. The short form says "the tests were of boto3 alone" right after giving the 37 per cent figure, which leaves unclear whether the library-wide share was tested; the full notice implies it was. The full piece's line "whether they are there every week is for a later reading to test" now reads as answered.

## Against the record (stage 2)

Read: studies/LH013/ (LH013.md v0.2, brief.md, amendments.md, data/analysis/), the new paragraph in investigations/software-updates.md, the synthesis notice in articles/where-software-updates-go.md, and the LH013 entry in programme.md. Figures checked by studies/LH013/review/r0047_notice_figures.py, with output in r0047_notice_figures.txt.

**Figures.** Every figure in the six new texts matches the record and data/analysis/:

- median O of 37.3, 36.6 and 36.7;
- 32 of 37 within 5 points;
- the same three libraries with P "accounts for most" in all three weeks;
- 65.3 and 65.1 per cent from Python 3.9;
- ratios of 7.16 and 8.04 against 2.73 and 2.92;
- 95.2 and 95.5 per cent below the edge;
- flatness of 0.0007 and 0.0005;
- the programme entry's intervals.

Two small qualifications. "Falling in steps at the same places" (piece notice) is a description, not one of the tests (brief, "The walk"). The programme's "over these three adjacent weeks ... on every measure" covers C and C5, which compare W1 with W2 only, because W0's cells were not read.

**Could the measurements be right and the explanation wrong?** Yes, and the pieces allow for that. A level, repeating profile from one cell of reported fields (Python 3.9, pip, Linux, no CI flag) fits a resolver's walk. It also fits any steady process that fetches every version, such as a scanner or a script running `pip download` across versions. A cell is not a machine (LH013.md, Limits). The notice keeps the walk as "our reading", so a reader is not led to treat it as shown.

## What the round establishes

- Over two adjacent weeks that no study had read, the older shares (at a fixed reference) and the old-Python classes stayed close to the first week's.
- boto3's four post hoc patterns repeated close to their first-week values.
- Those patterns are therefore not an accident of one week.
- The round does not establish why older versions are downloaded or what makes the level profile. It says nothing about months or other libraries.

## Material claim problems

1. **Short form underclaims what was tested.**
   - *Passage:* articles/short/old-versions-new-pythons.md, notice: "tests fixed before we read them found the same for the same libraries: about 37 per cent ... That is two more weeks of the same libraries, and the tests were of boto3 alone."
   - *Effect:* a reader concludes that the 37 per cent and old-Python findings were not tested.
   - *Evidence:* brief.md, "Tests and conventions", fixes O and P tests for all 37 libraries; summary.csv has O 32 of 37 and P 35 of 37.
   - *Resolution:* write "the tests of the patterns first seen after the counts were of boto3 alone".
   - The synthesis's "and for boto3 alone" has the same ambiguity and needs the same fix.
2. **The piece's notice leaves out described evidence that weakens a claim in its body.**
   - *Passage:* articles/old-versions-new-pythons.md body: "grpcio-status's older downloads have the same shape ... and so, more faintly, do botocore's and litellm's". The notice says only that "the similar shapes we describe for other libraries were not tested."
   - *Effect:* a reader still believes those libraries show a steady walk-like shape.
   - *Evidence:* results.txt, measure 4: grpcio-status was walk-shaped for 10.9, 0.0 and 2.2 per cent of its older downloads across the three weeks, and litellm for 19.3, 0.0 and 10.5. Both were near the 0.05 line and crossed it from week to week (LH013.md, Limits). aiobotocore stayed steady at 84.2, 84.4 and 83.4.
   - *Resolution:* add one described clause, e.g. "described and not tested, aiobotocore's held; grpcio-status's and litellm's crossed our threshold from week to week, so for them the shape is not steady".

Nothing else is material. "What stays behind held" is followed straight away by what held and by "A pattern that holds is not thereby explained".

## Readability

- The short form's colophon still reads "Version 1.1, 29 September 2026". It names no reviews or record for the notice and has no Corrections line for it. Bring it in line with the full piece's version 1.3.
- The synthesis says the walk is a reading "that no field in the log can confirm". The piece says the installer's version in the full log "could test it". The two statements can both be true, but read together they seem to disagree. Use one wording, e.g. "could make more or less likely".
- In the README line, "held" could be read as covering the explanation. "The shares held" would be clearer.

## Next step

**Recommendation: adjust.** Put the installer question first. Do not repeat LH013 soon.

- **More adjacent weeks add little.** Three of them held with wide margins. The record's second Next item (one fixed week, a month or more later) is cheap, available now from ClickPy and worth scheduling. It is a baseline check, not a test of any explanation.
- **The first Next item can discriminate, but only partly as written.** The installer's version alone does not separate a walk from other processes that fetch every version. The record itself notes that whether metadata-file requests are logged is unknown, so a pip at 23.2 or later neither supports nor rules out a walk.
- **A stronger test from the same day of data.** The package index's BigQuery table records each download's timestamp and file name. A walk leaves short bursts of descending boto3 versions fetched within seconds, with the same reported details. A scanner leaves a different order and rhythm, and installations leave mostly single versions.
- **Write the brief now.** Fix that sequence test, the installer-version split, and the PyPI statement on metadata logging in a brief before any read.
- **Availability.** It needs a Google Cloud account named by a task. A one-day, one-project query should fit within the free quota. Until an account is provided, it waits. That is a valid state, and the programme should say so rather than repeat ClickPy reads.

## Resolution, by the driving session

Made by the scheduled run 2026-11-03T1415Z (Claude Code, Opus 5.5), 3 November 2026, after reading results.txt's measure 4 rows and the brief's holding rules.

- **Problem 1 (the short form underclaims what was tested): resolved.** The short form now says "the tests of the patterns first seen after the counts were of boto3 alone"; the synthesis notice says the same in place of "and for boto3 alone".
- **Problem 2 (the piece's notice leaves out evidence that weakens its body): resolved.** The notice now says the similar shapes described for other libraries were not tested and did not all keep: aiobotocore's stayed about as large, grpcio-status's and litellm's came and went from week to week (results.txt, measure 4: aiobotocore 84.2, 84.4, 83.4; grpcio-status 10.9, 0.0, 2.2; litellm 19.3, 0.0, 10.5). botocore's (11.6, 13.2, 12.4) is not named, since the body calls it fainter and it held.
- **Figure qualifications:** the steps are now "as we saw but did not test"; the programme entry now says the largest cells were compared across the two new weeks (brief, "C holds"), and AGENTS.md's line the same.
- **Readability:** the short form's colophon is now version 1.2, naming the record and both reviews; the README line says "the shares of downloads on older versions held". The synthesis keeps "no field in the log can confirm", which the evidence review asked to keep; the piece's "could test it" names a reader beyond the log's public copy, so the two do not conflict.
- **Next step:** taken in part. A dated row (LH013-installer-brief) asks for a brief, fixed before any read, for one day of the package index's BigQuery table for boto3 on Python 3.9, with the reviewer's burst test (descending versions fetched within seconds) beside the installer's version; it is written now and read only when a task names an account, so the row does not ask the keeper for anything. A later re-read on a week fixed in advance is left to programme.md's Next for the driving session to weigh, not scheduled here.
