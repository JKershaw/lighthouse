# R-0121: evidence review of LH033's record, version 1.0

**In short.** A fresh evidence review of the PHP fix record at version 1.0 (commit 9328321), offline, on retained files only. Every figure in the In short, Answer and Findings was reproduced by an independent script, with one wrong count (24.4 million on day 14 should be 24.2 million). Two other must-fix points: one Python comparator the brief named is missing, and the In short calls services "servers". Not cleared until those three are fixed.

Reviewer: a Claude Code subagent (Opus 5.5, claude-opus-5-5, as reported by its harness), 23 November 2026, dispatched by the Research run of 23 November. No network request was made; no source was re-read; the record was not edited.

## What was checked

- **Brief and amendments** (studies/LH033/brief.md): day 0, earliest read per completed UTC day, measures 1 to 5, the named Python comparators, amendment 2's S7, S30, L, both predictions and their fail conditions, and LH034's amendment 1 (studies/LH034/brief.md) for the Node.js side of tests A and B. Also what kinds of statement the brief allows.
- **Independent reproduction**: [R-0121-lh033-v1-evidence/reproduce.py](R-0121-lh033-v1-evidence/reproduce.py), output in [R-0121-lh033-v1-evidence/output.txt](R-0121-lh033-v1-evidence/output.txt), run as `python3 -I notes/R-0121-lh033-v1-evidence/reproduce.py` from the repository root. It does not import record_v1.py. It reads the 13 gzipped Censys bodies (`snapshot`: branch_history, history, branch_versions, branches, top_versions), the W3Techs derived files (details diagrams and day-30 history tables), the Packagist body of 25 October, php.net's release lists of 21 November, LH011's release_days.csv and LH008's lags.csv directly (not python_side.json), and studies/LH034/data/tables.json. record_v1.py was also run; data/record_v1.json came out byte-identical to the committed file.
- **Checkpoints** 2026-11-21.md and 2026-11-22-closure.md against the record.
- **Consistency** with programme.md, investigations/software-updates.md and articles/a-week-after-two-fixes.md.

## What was found

**Reproduced and agreeing** (all from output.txt):

- Zero revisions in any shared completed day across all 13 reads, in branch_history (all branches, not only the fixed ones) and in history. The inconclusive condition is not met.
- Measure 1: days 1, 2, 7, 14, 30 for all four branches; first day at half (8.4 and 8.5 day 2, 8.2 and 8.3 day 6); day-30 service counts; not counted patched 21.8, 25.0, 13.5, 7.8; rise day 14 to 30 of 2.5 to 5.5 points; rise day 23 to 30 of 1.3 (8.5) to 3.0 (8.2); the two older branches below both newer on every day 1 to 30 (not on day 0, where 8.2 at 2.1 exceeds 8.5 at 1.9; the record correctly says "from day 1"); day 29's fall in every branch's service count with a smaller fall in patched counts; day 0 shares 1.8 to 4.3 per cent ("start near zero" holds). "Most of the rise came in the first two days" holds in every branch, narrowly in 8.2 (51 per cent of the day 0 to 30 rise).
- Measure 2: 57.2, 54.3, 52.9, 51.8 per cent on days 0, 7, 14, 30; 22,516,583 of 43,438,950; unknown 28.4 per cent on day 0 and 62.3 on day 30, jumping between day 1 (32.1) and day 2 (56.0); the unfixed count's fall from day 14 to 30 of 1,710,195 ("about 1.7 million"). History holds only the four statuses, so "all targets" is affected + affected_nofix + patched + unknown.
- Measure 3: every group share, the largest single versions below the fix, 8.3.8 at 844,547 (11.1 per cent, 2.5 times the next, 8.3.35), branch totals within 0.297 per cent of the day-30 bars, no unparsed version rows. php.net dates 8.3.8 to 06 Jun 2024 and 8.2.36, 8.3.37, 8.4.28, 8.5.13 to 19 Nov 2026.
- Measure 4: every cell of the W3Techs table, including the monthly points (8.4's 1 October "0" comes only from an 8.4.28 row at "<0.1%"; 8.2, 8.3 and 8.5 have nothing listed at or above the fix on 1 October).
- Measure 5: 583,656,921 of 5,809,870,614, 10.05 per cent.
- Python comparators, recomputed from LH011's and LH008's CSVs: every range and median in the comparison table (day-30 median 0.615526, so 61.6 is right); the day 1, 7, 14 and 30 orderings; 18 and 50 of 102 LH008 fix pairs moved within 7 and 30 days (no negative lags), agreeing with LH008's own table (5 / 8 / 18 / 50).
- Amendment 2: every S7, S30 and L for PHP and both Node.js rules; PHP median L 0.275; Node.js median L −0.139 as written and 0.196 amended; all four PHP branches up at least one point day 23 to 30; test B gaps 8.30 (PHP), 18.83 and 8.03 (Node.js). Both tests hold as the record says, and the fail conditions are applied as fixed. Node.js's day 0 in LH034's tables is 21 October, as for PHP.
- Censys's fixed versions: in every read the lowest patched patch number in `top_versions` is 35, 36, 27, 12 (top 20 rows only, so partial support for "throughout").
- Labels: measures are marked observation, the comparisons derived, readings interpretation, amendment 2 and measure 6 post hoc. Absolutes ("none", "every", "on every day") were each checked against the reads held and hold.

## Must-fix

1. **Findings, "The tail no fix reaches": "24.4 million on days 7 and 14".** Day 14 is 24,226,778, 24.2 million (day 7 is 24,386,744, 24.4). Fix: "24.4 million on day 7, 24.2 million on day 14". The 1.7 million fall then agrees with the counts.
2. **A comparator the brief named is missing.** The brief names "the day-30 share still at older versions (medians 33.9 and 73.1 per cent in its two groups)" from LH011's record, so that no comparator is chosen after the PHP curves are seen. The record reports the 26 of 37 comparator but not this one, while the Answer says it sets PHP "beside the Python comparators named in the brief". Fix: add it beside measure 1's not-counted-patched shares (7.8 to 25.0 per cent on day 30), as a description in different units (LH011, Findings: 26 projects median 33.9, eleven median 73.1, one minus the day-30 median at-or-newer share).
3. **In short: "internet-facing PHP servers", "Censys's count of servers", "version-reporting servers".** The brief forbids turning a Censys count into machines, and Limits says a service is an address and a port, not a machine; the In short is read alone, and "server" reads as a machine. Fix: "services", with a short gloss (an address and port answering with a PHP version) on first use.

## Should-fix

- **LH011 comparator wording** (Findings, Python): "26 of 37 Python projects' releases reaching half of downloads by day 2" drops LH011's rule; LH011 says 26 of 37 projects had *most of* their releases reach half on day 1 or 2. Say so.
- **The interpretation that the Python and PHP shapes differ because of what is counted** (Findings, Python). It is labelled interpretation, and it follows the brief's own Units section, but the brief says the record "cannot say why either curve has the shape it has". Say that it is an untested reading of the units, not a finding, and name what (if anything) could test it, or that nothing here can.
- **W3Techs table, 8.4 on 1 October "0"**: the zero comes only from the 8.4.28 row that W3Techs lists before its release (Limits). Mark the cell (for example "0, from 8.4.28 <0.1%, see Limits") so it is not read as a measured zero beside three "not listed".
- **Measure 2 "for each day"**: the record and record_v1.json hold days 0, 1, 2, 7, 14, 28, 29, 30 only; the full daily series is in each read's tables.json. Point to it, or write all 31 days into record_v1.json.
- **Measure 1's denominator excludes in-branch unknowns.** The day-30 snapshot's `branches` lists services in each fixed branch with status unknown (253,987 in 8.2, 302,886 in 8.3, 369,144 in 8.4, 282,104 in 8.5), and branch_history's targets match affected + patched, not the three together. Add a line to Limits.
- **programme.md**: the same bullet still says LH033 and LH034 are "both at version 0.1, interim to day 7" before saying LH033 reached version 1.0. Update the first clause. The sentence "LH033's record reached version 1.0 ..." itself agrees with the record (75.0 to 92.2, 51.8, both readings held).

## Nits

- "Most of the rise came in the first two days" is true but narrow in 8.2 (51 per cent); "about half or more" would be exact.
- "their passing confirms that the week-one pattern lasted to day 30": test A is about how much arrived after week one, so "that the pattern seen in the first week was still there at day 30" is closer.
- The fixed-version constancy rests on `top_versions` (top 20 rows); say which field.

## Consistency with released surfaces

Nothing in the record contradicts articles/a-week-after-two-fixes.md: its day-7 figures (24.4 million, 54 per cent; 52.4 to 78.8 per cent patched; first days at half) are the record's. The day-30 figures extend it rather than correct it, so no Correction is needed from this record; whether a "Later evidence" notice is warranted belongs to the scheduled revision (row piece-week-one-rev), which should also weigh LH034's day-30 Node.js line 22 falling below half under the rule as written. investigations/software-updates.md says the piece is to be revised after the day-30 reads and states no LH033 figure, so nothing there conflicts.

## Verdict

Not cleared: three must-fix findings, each a small text change; no calculation needs redoing.

## Resolution, by the Research run of 23 November 2026

Numbered R-0121 by the driver (R-0100 was already taken). All three must-fix findings and all should-fix items applied in LH033 version 1.1 (its Corrections list them); programme.md's bullet no longer calls LH033 "at version 0.1" and names version 1.1. Not changed: the piece and investigation page (their revision is row piece-week-one-rev); the LH034 line-22 point is passed to that revision. What this resolution wrote goes to the fresh recheck (row LH033-v1-recheck).
