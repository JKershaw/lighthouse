# R-0075: LH050 recheck of the R-0074 resolution

Row LH050-baseline-recheck. One reading, by a fresh agent, of what the driving session wrote in commit 42cceb4 to resolve the reader-and-inference review (R-0074). Rechecker: Claude Opus 5.5 (claude-opus-5-5), subagent, 16 November 2026. Cost: unknown, not measured; unknown is not zero.

Version read: git HEAD 94b8ef803b4d4ece2c85e0d19349a1903eb7841f; studies/LH050/LH050.md sha256 0c59008b1a0fcd66d4bb646923465f2610e0126c9c4d9073be30e6ebaf46b109 (unchanged since 42cceb4). After this recheck's own changes, listed below: sha256 ea2d372afa52f051757599639f104f396a7c0a42daf4fa04e4b3f4f3251a10ad.

Inputs: notes/R-0074-lh050-reader.md and its Resolution; `git diff 42cceb4~1 42cceb4 -- studies/LH050/LH050.md`; studies/LH050/review/r0074_matrix_split.py and .out (re-run on case_matrix.csv: output identical); case_matrix.csv (every armament, deployment, target-selection, force-authorisation, intervention and supported cell read); panel.csv; checkpoints/2026-11-16-panel-lock.md; source bodies PA-S05, PA-S28, PA-S29 in data/2026-11-13T1454Z/bodies/.

## Each change checked

1. **In short, "report" for "establish"; "mostly in the words of the company or government concerned".** Matches the matrix: Phantom rows are third-party reports relaying the company, Changi rows are SPF/HTX accounts. Holds.
2. **In short, the gap "mostly reflects which cases could be read"; the Gaza use and the armed comparison "could not be read at all"; "neither readable case shows a robot fielded with a weapon".** Two rows wholly unavailable (14 cells); no readable armament cell supports a fielded weapon (script: 0). "Could have tested it" is phrased as possibility, which the evidence allows. Holds.
3. **In short, Changi: "officers direct their movement, but nothing says who would decide on force".** Overreach: only GIBSON (PA-S28, PA-S29) is described as summoned by app and taken over manually; PA-S05 gives the 2023 robot autonomous patrol with an Operations Room live view and two-way communication, and the matrix codes its intervention cell "how an operator overrides the robot is not stated". Fixed (below). "Nothing says" also narrowed to "nothing read says".
4. **Answer, "45 matrix cells (codings of this record, not robots, weapons or events)"; 7/23/14/1.** Counts unchanged from the reviewed version; label accurate. Holds.
5. **Answer, "14 of the cells are the two whole rows lost to failed reads".** Figure right; "failed reads" is inaccurate for the FT report, which robots.txt disallowed and was never requested (only the Marine Corps page returned 403). Fixed (below).
6. **Answer, "so a supported entry on force was hardly possible there".** Too broad as written: the readable rows hold a force-authorisation stated-intention cell, coded conflicting from two reported statements, so an entry on force was possible and was made. The claim holds for force in practice, which the preceding sentence is about (8 such cells in readable rows, all not-established). Fixed by adding "in practice" (below).
7. **Answer, "stage cells are supported in 4 of 4 and the control cells in 1 of 13, and that one concerns taking over a robot's movement, not force (derived, r0074_matrix_split.out)".** Reproduced: stage {supported 4}; control {not-established 11, conflicting 1, supported 1}; the supported cell is GIBSON intervention, noted in the matrix as "takeover and stop mechanisms for mobility and safety, not for force". Labelled derived, attributed to the right file. Holds.
8. **Limits, panel lock "16 November 2026 at 14:25:29 UTC, after this baseline; no weekly read has yet been made".** Matches the checkpoint ("Locked at 2026-11-16T14:25:29Z") and panel.csv; the data folder for 16 November holds only robots records. Holds.
9. **Next, Panel: eight endpoints, "four trade reports relaying Foundation, four revisable policy pages", Changi and Ukraine left out per the checkpoint; weekly reads from 19 November; R-0074's point attributed to it.** panel.csv P01 to P04 are PA-S24 to S27, P05 to P08 are PA-S16, S15, S11, S13; checkpoint gives the exclusions; the attribution paraphrases R-0074's "No reading of these eight pages can show whether a public record of a fielded armed robot describes its control" faithfully. In short's "eight fixed pages runs to 24 December" fits six weekly reads from 19 November. Holds.
10. **Next, The empty comparison.** States R-0074's recommendation 3 as a design question for a dated amendment before 26 November, not as a decision; no amendment is claimed to exist. Holds.
11. **Corrections paragraph.** Accurate summary of the changes; its Changi clause repeated item 3's overreach and is fixed to match. "No count or cell status changed" verified against the matrix and the reviewed totals.

## Changes made by this recheck (not sent to another reader)

- In short: "officers direct their movement, but nothing says who would decide on force" became "officers can summon one of the two types and take over its movement, but nothing read says who would decide on force".
- Answer: "lost to failed reads" became "lost because their only sources could not be read".
- Answer: "a supported entry on force was hardly possible there" became "a supported entry on force in practice was hardly possible there".
- Corrections: "since they describe officers directing movement" became "since they describe officers summoning one type and taking over its movement".

No count, cell status or conclusion changed.

## Verdict

Cleared, after the four wording corrections above. No must-fix finding remains. Not checked: the parts of the record the diff did not touch, and figures (the diff changes none).
