# R-0097: evidence review of LH013 version 0.3, the installer brief's Stage A

**Reviewer:** a fresh evidence reviewer, Claude Code on Opus 5.5 (claude-opus-5-5, as reported by its harness, not independently checked), dispatched by the driving session of the Research run of 19 November 2026 for schedule row LH013-installer-A-record-evidence-review. Not the writer of anything reviewed. A second agent's agreement is a review contribution, not independent confirmation.

**Reviewed:** studies/LH013/LH013.md version 0.3 at commit ff2bcfc, and every line that commit changed against 3cef7a6 (`git diff 3cef7a6 ff2bcfc -- studies/LH013/LH013.md programme.md proposals.md`): the header (version, date, authors, observation period, cites), the "In short", the new section "The installer brief, Stage A (version 0.3, 19 November 2026)", the "Unknown stays unknown" limit, Next, Corrections, the LH013 answer in programme.md and the 2026-11-19 line under P-0002 in proposals.md.

**Offline only.** No network source was queried; ClickPy was not read again. Reproduction: studies/LH013/review/r0097_stage_a_reproduce.py, output studies/LH013/review/r0097_stage_a_reproduce.txt (run from the repository root with `python3 -I`).

## What I checked

1. **The brief is the fixed one.** `git show 67eac9c:studies/LH013/installer-brief.md | sha256sum` and the current file both give 7bd05d211fbe3342e22e003b7430e9be497e2e07c5a6ca27c87e7932c86a2642; 67eac9c is dated 2026-11-10 14:30:27 UTC and is an ancestor of ff2bcfc. D (17 November 2026) was fixed in it a week before the day existed. The header's "7bd05d21...2a642" and its time are right.
2. **Figures, reproduced from the retained CSVs** (r0097 output): A1 has 20 groups; 79,782,285 rows; Python 3.9 41,777,672 and other 38,004,613, summing to the total; 0 metadata rows in every group; on 3.9, pip 41,737,447, uv 39,806, setuptools 370, blank 49, which sum to the 3.9 total; A2 79,782,285, equal to A1; two queries on 2026-11-19 (14:28:30 and 14:28:33 UTC), both HTTP 200, rows returned 20 and 1, matching the CSVs; read rows 80,199,680 + 89,958 = 80,289,638, inside one billion; 2 of the 5 queries allowed; both queries carry both overflow settings set to throw. All match the record **except the number of installer names**: there are 16 distinct installer values, 15 non-blank names plus blank, not "16 installer names and blank" (finding 1).
3. **The class follows the brief's rule.** The brief (Measures, Stage A): present at 1 per cent or more of boto3's rows on D, absent at none, trace otherwise. 0 rows gives absent. The record states the rule correctly. The A1 query matches the brief's metadata definition (`endsWith(filename, '.metadata')`) and its split (3.9 or other, by installer name). "No reading is missing" is true: neither query failed or was refused, and the read log holds no retry.
4. **Script and helper.** scripts/installer_stage_a.py issues exactly the brief's A1 and A2; scripts/common.py applies the robots gate before every request, appends both overflow settings to every `pypi` query, treats a ClickHouse exception in an HTTP 200 body as failed, and logs ClickHouse's own read statistics. Its coded ceilings are LH013's original brief's (300 queries, 30 billion rows), not Stage A's (5, one billion); Stage A's ceiling was kept by the script issuing two queries, which the record reports accurately as an observation. Fine.
5. **A2 caveat.** The record says A2's table is built from A1's and so is not an independent check; ClickPy's DDL (data/installer-brief-docs/clickpy_ClickHouse.md) supports that. Fine.
6. **The pip and PEP 658 interpretation** against installer-brief.md, studies/LH013/amendments.md ("The pip date") and studies/LH012/LH012.md (Findings, Next, Corrections 0.4): all three say pips older than 23.2 fetch each candidate from PyPI in full, and 23.2 and later read PEP 658 metadata files *where offered*. The record's section uses 23.2 throughout. Its opening sentence drops "where offered", which its Limits restore; the consequence sentences in "What it means" do not carry it (finding 3).
7. **The "strong evidence, not proof" reading.** It is the brief's own fixed interpretation (Measures, Stage A; What would leave it inconclusive), and the record keeps it. Two places on wider surfaces turn "carries no metadata-file rows" into "counts only full downloads", which is broader than what Stage A tested (finding 2). Separately, the strength of the reading rests on ClickPy's `filename` column carrying real file names on D, which Stage A did not check and the record does not say (finding 4). ClickPy's README import (data/installer-brief-docs/clickpy_README.md, line 343) does not select `file.filename` at all, though the live schema (clickpy_pypi_columns.tsv) has a `filename` column; so how the live import fills it is undocumented. Retained evidence that it is filled: LH012's file-tag pass (studies/LH012/data/read_log_phase2.csv, 29 September 2026; data/week/files/*.csv) parsed wheel tags from ClickPy file names for September 2026 days. That makes an empty column unlikely, not excluded for boto3 on D.
8. **Labels and sources.** A1, A2 and the class are labelled observation with their CSVs, read log and script linked; "What it means" is labelled interpretation. Fine, with finding 3 on how much of it is "the brief's own".
9. **Absolutes and windows.** "None has a file name ending `.metadata`" and "no metadata-file rows" each carry boto3 and D; the In short carries "one day, 17 November 2026"; the programme line carries "of 17 November". "Only the file each finally installs is logged" is unqualified (finding 3).
10. **Writing.** No em or en dashes in any added line; British spelling; no American forms found. One non sequitur (finding 5).
11. **Consistency** across record, programme.md and P-0002: same class, same day, same "unreviewed" label, same Stage B status. The programme line and the In short share finding 2's wording; P-0002 has a small unwindowed absolute (finding 6).
12. **Corrections entry** names what changed, says no earlier figure or conclusion changed (true: the diff touches no data file and no Answer or Findings line) and gives 3cef7a6 for version 0.2. Fine.

## Findings

### Must-fix

**1. The count of installer names is wrong.** A1's 20 groups carry 15 non-blank installer names and blank (16 distinct values; r0097 output lists them). The record says "which cover 16 installer names and blank".

Replace, in the section's A1 paragraph:
> 0 in each of the 20 groups of Python (3.9 or other) and installer name, which cover 16 installer names and blank.

with:
> 0 in each of the 20 groups of Python (3.9 or other) and installer name, which cover 15 installer names and blank.

### Should-fix

**2. "Counts only full downloads" goes beyond what Stage A tested.** Stage A tested one kind of non-download request, metadata files, and the brief's interpretation is that the table "carries none" of them. "Counts only full downloads" reads as a general claim about the log. Three places:

In the In short, replace:
> so the log most likely counts only full downloads (unreviewed)

with:
> so the log most likely does not record metadata-file requests at all (unreviewed)

In Limits, "Unknown stays unknown", replace:
> which is strong evidence, not proof, that the log counts only full downloads;

with:
> which is strong evidence, not proof, that the download log carries no metadata-file requests;

In programme.md's LH013 answer, replace:
> found no metadata-file requests among boto3's 79,782,285 download rows of 17 November in ClickPy, class absent: strong evidence, not proof, that the log counts only full downloads, so pips that read metadata files could not leave a walk in it

with:
> found no metadata-file rows among boto3's 79,782,285 download rows of 17 November in ClickPy, class absent: strong evidence, not proof, that the download log carries none, so pips that read metadata files, where offered, could not leave a walk in it

**3. The consequence sentences need "where offered", and part of "What it means" is the record's, not the brief's.** The brief fixes the class and the strong-evidence reading, and says the metadata question "decides which pips can leave a walk in the log at all"; the sentences about who could make the flat profile are the record's working-out of that, consistent with it but not written in the brief. And a pip from 23.2 fetching a candidate whose file offers no metadata downloads it in full, so "only the file each finally installs is logged" and the list of possible walkers are too absolute.

In the section's opening paragraph, replace:
> pips from 23.2 read a candidate's metadata file instead of downloading it, while older pips download each candidate in full.

with:
> pips from 23.2 read a candidate's metadata file, where the index offers one, instead of downloading it, while older pips download each candidate in full.

In "What it means", replace:
> **What it means** (interpretation, the brief's own, fixed before the read).

with:
> **What it means** (interpretation: the first two sentences are the brief's, fixed before the read; the rest draws out what the brief says this decides).

and replace:
> If the table carries none, pips that read metadata files leave no trace of a resolver trying their candidates; only the file each finally installs is logged. A walk in the download rows would then have to come from installers that download candidates in full, such as pips older than 23.2, or from something else that fetches many versions.

with:
> If the table carries none, pips that read metadata files leave no trace of a resolver trying candidates that offer them; only the files they download are logged. A walk in the download rows would then have to come from installers that download candidates in full, such as pips older than 23.2 or newer pips meeting files without metadata, or from something else that fetches many versions.

**4. State that the file-name column was not checked on D.** Add to "Limits of Stage A", after "a metadata request logged under some other name would not be counted.":
> Nor did A1 check that ClickPy's file-name column was filled on D: an empty column would also give no metadata rows. ClickPy's README import does not select the file name, so how its live import fills that column is undocumented; LH012's file-tag pass read real file names from it for September 2026, so an empty column is unlikely, not excluded. Stage B's repeat of the count in BigQuery (B3) would settle it.

**5. A non sequitur in the class paragraph.** "With none, no ceiling was approached" reads as though the absence of metadata rows kept the reads small. Replace:
> With none, no ceiling was approached: two queries of the five allowed,

with:
> No ceiling was approached: two queries of the five allowed,

**6. P-0002's line carries an unwindowed absolute.** The brief found no free source *among those it read* (installer-brief.md: "No source read does"; pepy.tech and other mirrors not checked). Replace:
> the brief found no free public source carrying the installer's version (ClickPy drops it).

with:
> no free public source the brief read carries the installer's version (ClickPy drops it; pepy.tech and other mirrors were not checked).

### Fine

The brief's hash and timing; every other figure (totals, splits, 3.9 by installer, A1 = A2, rows read, queries against the ceiling, HTTP statuses and rows returned); the class against the fixed rule; the A2 caveat; the observation and interpretation labels; the robots gate and overflow settings; the 23.2 date matching amendments.md and LH012; "strong evidence, not proof" as the brief fixed it; windows on the record's absolutes apart from finding 3; no dashes; British English; Corrections; the record, programme and P-0002 agreeing on the class, the day, the unreviewed label and Stage B's status.

Verdict: not cleared (must-fix: the A1 paragraph's "16 installer names and blank" should read "15 installer names and blank"; with that one change, and the should-fix items at the writer's discretion, I would clear it).
