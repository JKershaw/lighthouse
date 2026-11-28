# R-0178: fresh recheck of the armed-robots piece after its two reviews

- kind: review (recheck: the one fresh reading of what the resolutions of R-0174 and R-0177 wrote)
- row: LH050-reader-recheck
- date: 2026-11-28
- reviewer: Claude Opus 5.5 (model id claude-opus-5-5), under Claude Code, as a subagent; no network reads
- repository HEAD as received: 4dbc9b67dc84f28f1f3418be4b9850cace2e3188 (changes since fd1c097 read with `git diff fd1c097 HEAD -- ...`)
- SHA-256 as received:
  - articles/armed-robots-who-decides.md: 155cfec2e33b5a3650d9c1f2ae31bd6460be5b473c78a4123751c062e8d4dd9a
  - articles/armed-robots-who-decides.svg: 365dd473ac022334ab516bca1186e502c7ec4e0837d5bcbdde55f4ec3f207f3b
  - articles/short/armed-robots-who-decides.md: 44fa1cbc697f45f65c6501444a512793f5981d8962e4634cb140bb92879869df
- SHA-256 as left (uncommitted edits on top of 4dbc9b6):
  - articles/armed-robots-who-decides.md: 9e99f3baf974272de0bfe6cb1165994dbfb83d75fd45305dd19bcd073f024314
  - articles/armed-robots-who-decides.svg: 365dd473ac022334ab516bca1186e502c7ec4e0837d5bcbdde55f4ec3f207f3b (unchanged; the round didn't change it either)
  - articles/short/armed-robots-who-decides.md: 2f035e23fc6c5e260a96eeefe8797d0df19711871eec105ccbb06be30d299e85
- verdict: cleared, after the seven small corrections below

**In short.** We read every passage the two review resolutions changed in the piece, its short form, the investigation page and the programme line, against the study's retained files. The resolutions hold: the access history, the Gaza lead's provenance, the dated opening, the reread caveat and the restored "in practice" are all supported. The round did introduce two errors (a row count that counted the Gaza use twice, and a summary that spoke of one statement of intentions where the body has two) and left the colophon claiming the study's register holds the 28 November reads; those and four smaller wording points are corrected here, and nothing further must be fixed before release.

## What was checked

- **Access history.** notes/physical-authority/essay-checks/2026-11-28/fetchlog.md: FT 15:14:35Z, allowed under `*` by the one-off rule, HTTP 403, not retried; Wired 15:14:37Z, refused by its Claude-User group, not requested; both reads labelled essay fact checks that enter no matrix cell. The piece's sentences, the colophon's "Not readable" line and the short form's "closed to us, by the site's robots rules and then by the site itself" match. The 13 November refusals match sources.md ("disallowed by robots.txt for our tokens") and the record's Findings.
- **Gaza and Wired provenance.** brief.md (Prior knowledge: "A search summary attributed preliminary Gaza discussions to the Financial Times"), sources.md preamble (commissioning OpenAI Codex session, 12 November, no bodies retained) and PA-S02's note ("search result only in the survey"). Supported.
- **Opening.** S28 (SPF, "On trial at the Terminal 4 Departure Hall since July 2025", developed by HTX "in partnership with" A*STAR's Institute for Infocomm Research) and S29 (HTX, "researchers from the A*STAR Institute for Infocomm Research"). Supported; the past tense now matches "nothing we read reports either robot's status after those dates".
- **Extendable mast.** S05: "Its extendable mast with 360-degree field of view". Supported.
- **Business AM credit.** S24's retained text carries "Business AM" at the article's end. Supported.
- **Rereads.** checkpoints/2026-11-26-read.md: Assembly's body not kept under `save_body` (robots.txt refuses an AI-training crawler on that path), comparison made from an unretained local copy; checkpoints of 19 and 26 November both unreviewed. The caveat and the colophon's label match.
- **Six rows.** LH050.md Findings: Foundation splits into three configurations (Gaza application, design and stated intentions, Ukraine pilot), Changi into two, plus the comparison. See change 2.
- **"In practice" and the two statements.** claims C024, C025 via LH050.md; the matrix codes force authorisation "C (stated intention); N (in practice)". The title, opening, caption and short form now scope correctly. See change 1 for the summary.
- **Investigation page and programme line.** LH050.md header (reviewed 16 November by R-0073, R-0074, R-0075; not released); S44 retained text (pdftotext 24.02.0): "is to continue", "is to elaborate, by consensus, an instrument, without prejudging its nature", "for 10 days in Geneva each year", "submit its report to the 2028 Meeting", "as a binding protocol", "as orally amended". The essay draft exists (essays/when-the-machine-works-as-intended.md, commit 6cb4ab0). Labels (reviewed record, unreviewed policy read) are right.
- **Absolutes and windows.** The new title "didn't say how it works in practice" is bounded by "the sources we could read in November 2026". The summary and short form's "none says" carry "in practice" and the reading window.
- **House style.** No em or en dashes in the four files (checked by code point); British spelling; no study codes in the prose of the piece or short form (only in link targets).
- **Figure.** Unchanged by the round (same SHA-256 as reviewed in R-0174 and R-0177); its text and the revised caption and alt text agree with the matrix. Its Gaza row label, "Report refused to our agents", describes the 13 November state the figure is dated to.
- **Consistency.** After the changes below, the piece, short form, investigation page and programme line say the same thing at the same certainty as the record and the 27 November checkpoint.
- **Disclosure check (schedule/research-safety.md, combined).** Still clears: descriptive press and policy material, no targeting, operational or reconstructive detail, no re-identification, no Lighthouse-voice claim of present harm or compromise; the Gaza use stays "neither established nor ruled out".

Not checked: anything after the retained copies (no network reads); the essay itself, which another row reviews (it changed in the working tree during this recheck, by another agent, and was left alone).

## Changes

1. **Piece, summary: one statement versus two, and "each" covering an unreadable case.** Before: "The sources we could read say how far each had got, ... but none says who picks targets or decides to use force in practice (one reported statement of the maker's intentions aside)," After: "The sources we could read say how far the humanoid and the airport robots had got, ... but none says who picks targets or decides to use force in practice (two reported statements of the maker's intentions don't agree),". Why: the body and short form speak of two conflicting statements (C024, C025); "aside" implied a statement about practice; and the armed comparison had no readable source, so "each" of the three kinds overstated.
2. **Piece, "Three kinds of robot": double count.** Before: "and Changi into its two kinds of robot, which with the Gaza use and the comparison gives six rows." After: "...which with the comparison gives six rows." Why: the Gaza use is one of Phantom's three versions in the record's matrix; the round's sentence made seven.
3. **Piece, "The two we couldn't read": garden-path sentence.** Before: "a Wired article that the search made when this work was commissioned turned up on the company's weapons ambitions, were both refused". After: "a Wired article on the company's weapons ambitions, which a search turned up when this work was commissioned, were both refused". Why: readability; meaning unchanged.
4. **Piece, colophon: register claim.** Before: "The source register lists every address, read and access result." After: "The source register lists every address and the study's own reads and access results; the reads of 28 November are in their log." (linked). Why: R-0177's point 2 was resolved by keeping the 28 November reads outside the study's ledgers; the old sentence then said the register holds them, which it doesn't.
5. **Short form: ambiguous "They" and present tense.** Before: "They say how far each robot has got," After: "The sources say how far each robot had got,". Why: the round inserted a sentence about the two statements just before, so "They" read as the statements; "had got" matches the dated sources.
6. **Investigation page, In short and "Where it stands": "each case" covering the unreadable comparison.** Before: "say how far each of three chosen cases had got" and "report the stage each case had reached". After: "say how far the two readable cases of three chosen ones had got" and "report the stage each readable case had reached". Why: the record's Answer gives the stage for the readable rows only; the comparison is wholly unavailable.
7. **programme.md, physical-authority line.** Before: "report each case's stage" and "an instrument of open nature, reporting to 2028". After: "report each readable case's stage" and "an instrument without prejudging its nature, reporting to the 2028 meeting". Why: as change 6, and to keep the document's own wording rather than a looser paraphrase.

## Review points

All four of R-0174's must-fixes and both of R-0177's material problems are resolved in the text as left. R-0174's should-consider 1 (the AI hedge) and 3, and R-0177's readability point 2 (what the weekly rereads can catch), were left by the driving session; none is a must-fix. R-0174's should-consider 11 is now met by the investigation page and programme line.

## Verdict

Cleared: with the seven corrections above, nothing further must be fixed for release. This recheck's own changes are listed here, not sent to another reader.
