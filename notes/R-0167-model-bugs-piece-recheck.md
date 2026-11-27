# R-0167: recheck of the review resolutions in the model-found flaw dates piece

**In short.** One fresh reading, as AGENTS.md step 4 asks, of what the resolutions of the evidence review (R-0163) and the reader review (R-0165) wrote into the draft piece on CVE-2026-98432's public dates, its figure and its short form, version 0.1 (f36d24c) to 0.3 (8b3ca03). Every changed passage was checked against the retained bodies and the reviewed records; every material finding of both reviews is resolved, no date or count is wrong, and no new overstatement was found. Two small balance and labelling corrections were made here. Verdict: cleared with the listed corrections.

- **Read:** `git diff f36d24c 8b3ca03 -- articles/drafts/`; notes/R-0163-model-bugs-piece-evidence.md and notes/R-0165-model-bugs-piece-reader.md, with their Resolution sections; the three files at 8b3ca03.
- **Rechecker:** a fresh Claude Code subagent on Claude Opus 5.5 (claude-opus-5-5), queue row gap-piece-model-bugs-recheck, 27 November 2026. An Anthropic model checking a piece about Anthropic's post: a review contribution, not independent confirmation.
- **No web requests.** Everything read from the repository.
- **Calculation:** `python3 -I notes/R-0163-model-bugs-piece/dates.py` rerun; output unchanged from notes/R-0163-model-bugs-piece/dates_output.txt (every day count OK). No new calculation was needed.

## What was checked

| Changed passage | Checked against | Result |
|---|---|---|
| Policy quotes: "we would generally wait 45 days before publishing full technical details"; "The purpose is to give downstream users time to deploy the fix before detailed exploitation information is public."; the shortening clause; "to share details publicly with defenders after 90 days, or after a patch is released, whichever comes first" | studies/LH038/data/policies-2026-11-04T1415Z/anthropic_cvd.raw.gz, text extracted | All verbatim. The same paragraph also has "We may extend it when patch deployment is unusually complex or the affected footprint is unusually broad", which the piece omitted (correction 1) |
| Policy "last updated on 6 March 2026"; read 4 November | same body (`<time dateTime="2026-03-06">Mar 6, 2026</time>`); LH038 header | Matches |
| Post read 17 November, modified date 30 October | studies/LH038/data/read-2026-11-17T1419Z/anthropic_post.raw.gz | `datePublished` 2026-10-27T00:00Z, `dateModified` 2026-10-30T15:24:16Z. Matches; now attached to the post, not the policy (R-0165 M2 resolved) |
| "after initial prompting, ... Claude, wrote an exploit that 'allows ...'"; "details beyond what is already included in a public advisory"; "a further 45 days" | same post body | Verbatim; "After initial prompting" is in the Linux section itself |
| Both readings of the 45-day wait: 12 to 16 days from the stable releases, 26 from the author date with its caveat; SUSE list 29 October, Red Hat 1 November, Ubuntu tracker 10 November all after the post | dates.py output; LH038 table and Finding 4; LH036 Fixes | All match. "Within 45 days of every candidate date before it" is LH038's Finding 3 wording. The distribution reading rests on the record's own rows and Finding 4; it is a reading of which patch counts, given beside the other, not a new measurement. R-0165 M1 resolved |
| Title, summary, short form now give both readings; "not a verdict either way" | LH038 Answer, investigation page | Neither reading is given as the answer; nothing reads as a verdict on Anthropic either way |
| "(Those are the release commits' dates; the changelogs on kernel.org carry server times minutes later, on the same days.)" | studies/LH038/scripts/timeline_output.txt | Last-Modified 5 to 51 minutes after each release commit, same UTC day. Matches |
| SUSE's page sentence: none of the 186 SUSE announcements stamped before the post, post hoc | dates.py output; LH038 Finding 4 | 190 items, 186 SUSE-SU ids, 0 before 27 October, earliest 29 October 12:04:53. Labelled post hoc |
| "174 of them are SUSE's ... stamps all of those 29 October or later ... the other 18, from Red Hat and Ubuntu" | LH038 Limits (174 SUSE, 12 Red Hat, 6 Ubuntu) and Finding 4 | Matches (174 + 12 followed = 186) |
| "the trackers listed fixes for Debian's security channels ... SUSE listed a released kernel for 42 of the 121 products it names with a main kernel package" | LH036 0.2, In short, Fixes and the SUSE table (16 Nov row: 121, 42) | Matches |
| Unknowns that could fall before the post now include SUSE's 24 October pages; Next names Debian and Ubuntu notices as datable, SUSE's 24 October pages as not settleable | LH038 Finding 4 and Next | Same certainty. R-0165 M3 resolved; R-0163 M1 (Ubuntu contradiction) resolved: Ubuntu's 10 November is attributed to its tracker everywhere and its notice pages stay unread |
| Comparison flaw reserved the same day; "one case, chosen after a first look", embargo through the distributions' private list, use of that list for this flaw unknown | studies/LH054/brief.md (reserved 2026-09-25T10:25:14Z, the same second as CVE-2026-98432's dateReserved in LH036's retained CVE record; "embargo agreed with the maintainers of linux-distros"; "one case chosen after a scout read it"); LH038 Limits on linux-distros | Matches. The coincidence was noticed after both records were read and was unlabelled (correction 2) |
| Short form: title "When was the Linux flaw in Anthropic's exploit post reported?"; "2 to 14 days after it"; purpose quoted in fragments | dates.py (SUSE list +2, Red Hat +5, Ubuntu +14); policy body | Matches. R-0163 M3 resolved |
| Figure | rendered 720 by 800, light and dark (rc-fig.png, rc-fig-dark.png in the session scratchpad) | Legible in both; the dashed report box sits apart from the scale with no line to it; hollow and accent marks distinct in both; no overlap; labels match the text ("Earliest notice on Ubuntu's tracker", "as we read it on 17 Nov", footer 1 to 21 November) |
| Consistency | studies/LH038/LH038.md 0.4, studies/LH036/LH036.md 0.2, investigations/model-found-bugs.md | Same certainty throughout. The piece says more than the investigation page on the distribution reading of the wait, without contradicting it |
| Piece rules | the three files | No em or en dashes (counted: 0 in each); no internal codes in the prose (study numbers and note numbers appear only behind colophon links); absolutes in the title and summary carry "we could date" and "in November"; short form body 249 words after correction 3 |

## Corrections made here

1. **The policy's extension clause** (piece, "Beside the rules people publish"). The piece quoted only the clause that lets Anthropic shorten the wait, which gives a reader one side of the paragraph. Old: `defenders identify and mitigate ongoing attacks". Whether either applied isn't stated.` New: `defenders identify and mitigate ongoing attacks", and extended "when patch deployment is unusually complex or the affected footprint is unusually broad". Whether any of these applied isn't stated.` Quoted from the retained copy of 4 November. Short form, same reason: old `the page allows it to be shortened.` new `the page allows it to be shortened or extended.`
2. **Post hoc label on the reservation hedge** (piece). Old: `had its number reserved the same day, so the date may not mark` New: `had its number reserved the same day, which we noticed only afterwards, so the date may not mark`. It is one observation made after both records were read; it weakens an inference rather than making one, and no study tests it.
3. **Short form length**, to make room for correction 1 within 250 words. Old: `The post, in prose without code when we read it on 17 November, came` New: `The post, prose without code as read on 17 November, came`.

No figure, date or count changed. The figure is unchanged.

## The title

Current: "Anthropic's exploit post came 12 to 16 days after Linux's stable fix and before every distribution announcement we could date; nothing we read in November says when the flaw was reported" (31 words). Kept. Each clause carries load: the two readings of the wait, the scope "we could date" (which keeps SUSE's 24 October release date and Debian's undated fixes out of "every"), and the window "in November" on the unknown. Shorter versions tried either dropped "we could date" (overclaiming, since Debian's advisories are unread), dropped the window, or replaced "when the flaw was reported" with "the report", which reads as a document when the title is seen alone. None was equally accurate, so none was set.

## Unresolved, outside these files

- investigations/model-found-bugs.md still says "Fixes had reached Debian", where the piece now says "the trackers listed fixes for" (R-0165 R7); LH036's In short still says "fixed on 15 October" (R-0163 aside). For the surfaces round.
- The piece's colophon and both bylines still say "recheck of those fixes pending"; the release round completes them.
- The front page's "The watch" (R-0165 stage 1) is for the release round.
- The redactor aside in R-0163 concerns a retained body, not the piece.

## Verdict

**Cleared with the listed corrections** (made in place). Every material finding of R-0163 (M1 to M3) and R-0165 (M1 to M3) is resolved; the recheck's own changes are listed above and go to no further reader, as AGENTS.md says.
