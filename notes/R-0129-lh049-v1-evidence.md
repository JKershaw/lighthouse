# R-0129: evidence review of LH049's record, version 1.0

**In short.** A fresh agent checked the bee-js record (version 1.0 of 24 November 2026) against the nine retained npm reads, the brief and the sources, and reproduced every figure with its own code. Every figure matches; the protocol's rules are applied as written, missing entries are kept as unknown, and compromise is attributed to StepSecurity, Socket and the advisory. Three sentences overstated or blurred something and were reworded without changing any figure or conclusion. Cleared at version 1.0; the reader-and-inference review comes next.

- Reviewer: a fresh review subagent, Claude Code, Opus 5.5 (claude-opus-5-5, as reported by its harness), 24 November 2026, for queue row LH049-record-evidence-review. A second agent's agreement is a review contribution, not independent confirmation.
- Reviewed: studies/LH049/LH049.md version 1.0 as committed at 8b80fb7; brief.md (protocol 0.1 and the operational amendment of 14 November, notes/readiness/2026-11-14-operational-amendments.md, which changes no rule); sources.md; checkpoints/2026-11-24-closure.md; scripts/tabulate.py (SHA-256 69aaf1dc...4683, matching the record's header); data/record_v1_output.txt; every body and read log under data/read-*/; the pre-brief copies of E3 (StepSecurity), E6 (OSV), E9 (npm blog) and the derived file for E8 (Socket, body removed on 21 November).
- No network request was made. Nothing in studies/LH034/ or schedule/ was touched.

## Reproduction

notes/R-0129-lh049-v1-evidence/reproduce.py is written from the brief's text, not from tabulate.py, and reads only the retained bodies. Output: notes/R-0129-lh049-v1-evidence/output.txt. Replay: `python3 -I notes/R-0129-lh049-v1-evidence/reproduce.py`. Separately, rerunning tabulate.py gives output byte-identical to data/record_v1_output.txt.

Reproduced, each equal to the record:

- All nine reads: six requests each, all HTTP 200, no retry. 38 bodies with no email withheld match their logged SHA-256; the registry documents (536 or 537 withheld) and OSV answers from 12 November on (1 withheld) differ by design.
- Clock rule: at every read the two point answers agree on start, end and total and span seven days. Per-version sum minus point total is +210 at the reads of 10, 11 and 12 November (4,236/4,026, 4,643/4,433, 4,999/4,789) and 0 at the other six. The three failing windows are exactly those containing 5 November. The per-version answer has only `package` and `downloads`.
- 13.3.0 per window by stated end: 202 at 9 to 15 November; no key at 16 and 23 November.
- Held V(t): 12 to 15 November = 202; 16 and 23 November = no record. d(13) = d(14) = d(15) = 0; d(9) to d(12) and d(16) unknown; sums d(9..12) to d(9..15) = 202 each.
- Measure 1: earliest held window with a value ends 12 November, so d(9) is at most 202; the brief's lower bound V(15) minus V(16) cannot be formed. Package total 9 November 1,144 (same at all reads); S0 at most 0.1766 (17.7 per cent).
- Measure 3: 75.1/1,440 = 0.05215; I at most 3.386.
- Measure 4: other days 2 to 16 November n = 14, median 697, range 181 (8 November) to 1,070 (12 November); the daily series 1 to 23 November as listed; 17 to 23 November sum 2,645; no disagreement between reads on any loaded day; each read's own date answered 0. Daily totals summed over each stated window equal the point total at all nine reads.
- Measure 2's tail: window 17 to 23 November held (2,645 against 2,645), no key 13.3.0.
- Measure 5: no `time` entry other than 13.3.0 on or after 9 November at any read, so no qualifying release.
- Measure 6: bound 0 to 202 is neither wholly inside nor wholly outside 4 to 31; reading not made.
- Measure 7: as stated at all nine reads (13.3.0 unlisted, time entry kept, latest 13.2.0, no deprecation, no `unpublished`, modified 2026-11-09T01:24:58.830Z, 177 listed, none added or removed). OSV: MAL-2026-18773 with alias GHSA-hh7j-5m3j-23pf, never withdrawn; modified moves from 02:30:04Z on 9 November to 21:15:15Z on 11 November when an amazon-inspector origin is added, credited to Amazon Inspector as finder.
- Outside the protocol: 178 keys at reads of 10 to 16 November, 177 at 17 November, 111 at 24 November with 66 listed versions keyless; no zero value at any read; smallest value 1 to 5.

Every figure in the record appears in the output; the In short, Answer and Findings agree.

## Other checks

- **Unknown is not zero.** The no-key windows are "no record" in every measure; d(16), the lower bound and the tail stay unknown. Confirmed in both codes.
- **Post hoc labelling.** The reading of the 66 keyless versions is labelled post hoc, as one reading, and no measure uses it; the counterfactual "if those windows could be used" is labelled outside the protocol. The record says what could test the absent-key question (Next) and that its own reads cannot.
- **Readings of the brief** (Method 1 to 8) are reasonable and disclosed. Reading 1 matters most: the brief's bound is written for a day-0 window "never read"; applying it to a window read but unfixable is the only way to say anything, and the alternative gives the same upshot.
- **Attribution and safety.** Malice, provenance and the hook are attributed to StepSecurity (E3), Socket (E8) and the advisory via OSV (E6); I checked E3's retained text (00:09:50, `latest` at 00:31, 3,560, trusted publishing and provenance, the postinstall hook), E8's derived phrases (all quoted phrases marked present), E6's origins and E9's definition (HTTP 200 tarball responses; mirrors fetch a version once, usually on its publication day). The mechanism is at reader level; no payload host or indicator is named; nothing anonymised is touched; "download" is a fetch throughout, and "install" and "victim" appear only in denials.
- **Absolutes** carry their windows, after the fixes below.
- **Header commits.** 330ba6c and 799f858 exist in this clone; 7be9953 does not, as the record itself says.

## Found

Must-fix (fixed, wording only, no figure or conclusion changed, version kept at 1.0):

1. Limits said the clock-rule failure "wasn't foreseen by the brief". The brief's inconclusive list does name per-version totals that don't sum to the point total as leaving a window unfixable. Reworded to say what it foresaw and what it didn't.
2. The Answer called the outcome "one of the outcomes the brief named as inconclusive", but the named outcome is a day-0 window not read; it is this one only under Method's reading 1. Reworded to say so.

Suggestions (applied):

3. In short: "from 16 November on, npm's per-version figures carry no record of the release at all" could read as days rather than windows; it now names the two windows read, ending 16 and 23 November.
4. Findings: "No public data can test whether npm drops..." is an untestable absolute; narrowed to what this study read.
5. Status lines (header, In short, Answer, Limits, Next) updated to say the evidence review is done and the reader review pending; a Corrections entry lists these changes.

Suggestion (not applied): the 210 excess sits beside per-version shifts (for example 3.2.0 falls from 375 to 233 when 5 November leaves the window), which a reader might want described. That would be a new reading after outcomes were seen and isn't needed by any measure; left out.

## Changed

- studies/LH049/LH049.md: items 1 to 5 above.
- studies/LH049/sources.md: "Outcome reads" filled with one row per read from each read_log.json.
- Added notes/R-0129-lh049-v1-evidence/reproduce.py and output.txt, and this note.

## Public surfaces (not edited)

- AGENTS.md, "Where things stand": "bee-js (LH049, interim, unreviewed)". Now a record at version 1.0, evidence-reviewed, reader review pending.
- investigations/software-updates.md, line 93: describes the reads as planned and links only the brief; nothing contradicts version 1.0, but it carries no outcome and no link to the record.
- observations.md, line 45: "nothing tabulated yet ... Read daily from 10 to 14 November 2026" is stale.

## Verdict

Cleared at version 1.0.
