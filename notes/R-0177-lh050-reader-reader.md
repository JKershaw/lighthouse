# R-0177: reader review of the armed-robots piece, stage one

- Kind: review (reader-and-inference, stage one: reader's belief before reading the record)
- Row: LH050-reader-reader-review
- Date: 2026-11-28
- Reviewer: Claude Opus 5.5 (model id claude-opus-5-5), under Claude Code
- Repository HEAD: 5c7ae97833a00cfb709e3dfff79ac633969678b4
- SHA-256 of the files read:
  - articles/armed-robots-who-decides.md: fcbe60119f95c1142b4596cc61c025c5bdf0f9ec8bf114a4dd78e087d2f2b32f
  - articles/armed-robots-who-decides.svg: 365dd473ac022334ab516bca1186e502c7ec4e0837d5bcbdde55f4ec3f207f3b
  - articles/short/armed-robots-who-decides.md: 0be455216a337fedf85390441157b0f5172129f5fe4e85c46d74e438db285605

## What a reader would believe, written before reading the record

**Said back.** Lighthouse looked at public sources on three hand-picked robot cases in November 2026: a humanoid (Phantom) whose maker reportedly designed it to carry weapons, an armed comparison robot, and Singapore's airport police robots. The sources it could read say how far each robot had got, but none says who would pick a target or decide to use force; the two cases most likely to say so couldn't be read. Separately, the Geneva weapons conference on 20 November kept autonomous weapons with an expert group reporting in 2028, without committing to negotiate a binding treaty.

**Observed.** What specific pages said, on stated dates: Phantom's 44-pound payload "including lethal weaponry"; a logistics-only demonstration in Ukraine; two conflicting statements of intent on autonomy; the Changi robots' navigation, intervention measures and GIBSON's manual takeover; refusals (robots.txt, HTTP 403, not found); the grid counts (7 supported, 23 not settled, 14 unreadable, 1 conflict of 45); the adopted text's wording and the absence of three phrases from it.

**Explained.** "Autonomous" in the Singapore sources means navigation, not targeting, so silence on force there is expected; the two Phantom statements may be a change of mind or a contradiction, undecided.

**Caused.** Nothing is presented as causing anything. A reader might loosely take the silence as a pattern of secrecy, but the piece says it can't separate that from inaccessibility.

**Limits a reader would notice.** Three purposive cases, not a sample; each rests on one family of sources (company-relayed trade press, or one government); the cases with weapons in play were unreadable; the grid is coding, not counts; the expert group's "elements" and later working papers were unread; the conference reads are unreviewed.

## Stage two: against the record

Read on 28 November 2026: studies/LH050/LH050.md (0.1), brief.md with its amendments, sources.md, claims.csv (C010 to C033), reads.csv, panel.csv, case_matrix output via review/r0074_matrix_split.out and review/r0176_quote_check.out, checkpoints of 21, 26 and 27 November, investigations/physical-authority.md and programme.md's Next. The figure was rendered in light and dark and checked against case_matrix codings. No new calculation was needed; the counts reproduce from r0074_matrix_split.out (14 unavailable cells in two rows; readable rows: stage 4 of 4, control 1 S, 1 C, 11 N; 8 of 8 target/force-in-practice cells not established).

### What the round establishes

The measurements and the stage-one reading match: 45 coded cells (7 S, 23 N, 14 U, 1 C); every readable row has a supported stage, no readable row has a supported fielded weapon, and no target-selection or force-in-practice cell is supported. The piece's explanation is the record's own, and it's hedged correctly: the gap is mostly a product of which cases could be read and of selection (Changi was chosen partly because an official page showed no weapon; Phantom's weapons are a design aim). So the measurements can't be right while that explanation is wrong, because the piece doesn't claim the silence shows opacity. The secrecy reading I flagged at stage one is pushed back on in the body ("we can't tell whether public records stay quiet... or whether we just couldn't reach the records"), though not in the title. The Geneva passages match the 27 November checkpoint and its quote check (unreviewed reads, as the colophon says).

### Material claim problems

1. **"In practice" drops out of the summary-level claims, and the record's one conflicting force cell contradicts them.**
   - *Passages:* armed-robots-who-decides.md summary, "none says who would pick targets or decide to use force"; the opening, "who picks the target and who decides to fire? ... none of the sources we could read says"; the figure caption, "none says who would choose a target or decide to use force"; and the short form, "None of the sources we could read ... says who would pick a target or decide to use force".
   - *Evidence:* claims.csv C025: The Next Web reports the chief executive said some weaponised uses keep human confirmation, and "In certain time-critical scenarios, the robots will need to make fully autonomous decisions" (found in S27_tnw.html, r0176_quote_check.out). That is a source saying, as an intention, who would decide on force. The matrix codes it as force authorisation "C (stated intention); N (in practice)", and LH050.md's Answer limits the absence to "target selection or force authorisation in practice". The short form even quotes both statements and then says none says.
   - *Resolution:* scope each of these to practice or to a fielded weapon. For example, the summary could read "none says who would pick targets or decide to use force for a robot actually carrying a weapon; two reports of the maker's intentions conflict", and the short form "...says who would, in practice, pick a target...". The body's "in practice" sentence already gets it right.
2. **The piece cites reads made on 28 November that the study's ledgers don't hold.**
   - *Passages:* armed-robots-who-decides.md, "A single read of the Financial Times page on 28 November, under a narrower rule we now use for one-off reads, was refused by the site itself (HTTP 403); Wired's rules still refused us", and the colophon, "Wired (refused by robots.txt on 13 and 28 November), the Financial Times (... HTTP 403 on a one-off read on 28 November)" and "The source register lists every address, read and access result".
   - *Evidence:* at HEAD 5c7ae97, reads.csv ends at LH050-R069 (27 November). There is no data/2026-11-28* directory, sources.md gives PA-S01 and PA-S02's status only as of 13 November, and the working tree has no uncommitted study change. The brief also says "A refusal ... ends that route", and no dated amendment or record line says why a re-read under the 21 November one-off rule is a new route.
   - *Resolution:* add the two reads to reads.csv, with robots decisions, hashes and the access rule used, and update sources.md. Add a dated line (record Corrections or a checkpoint) saying the re-read was a one-off read under the keeper's rule of 21 November, made after the outcome of 13 November was known. Otherwise, drop the 28 November sentences and keep the 13 November refusals.

No other material problem. The aggregate counts are labelled as codings, not robots. The Changi "autonomous" reading is the record's own and cites the ICRC. The selection is disclosed ("on purpose, not at random"). No cause is claimed.

### Readability

- The title, read alone, invites the opacity reading the body rejects. Consider carrying the access limit in it, for example "...The sources we could read in November 2026 didn't say, and the two that might have were closed to us".
- "What would change this account" sits right after "We're rereading a small set of these pages every week". A reader may infer that the rereads could find a record of who controls force on a fielded armed robot. Panel.csv holds four relayed trade reports and four policy pages, so the rereads can mostly catch revisions. Saying so in a clause would help.
- "a Wired article that the earlier survey's search turned up" refers to a survey the piece never introduces. "a Wired article found when this work was commissioned" says the same without the reference.

### Next step

The remaining panel reads (3, 10, 17 and 24 December) can't tell apart the two explanations in play: that public records say little about control even when a weapon is fielded, or that Lighthouse just couldn't reach the records that would say. The panel holds no record of a fielded armed robot, as R-0074 also noted in the record's Next. The December Ukraine notice is context, not a case. The one step that would materially improve understanding is the design change the record itself deferred: a dated amendment giving the armed comparison one rule-bound route to a readable first-party record of a tested or fielded armed ground robot, disclosing candidates already seen as chosen after reading, inside the pilot's envelope. If that window has passed, it should go to proposals.md as the successor question at the 24 December checkpoint. Reading the endorsed elements (CCW/GGE.1/2026/3) would sharpen the Geneva paragraph's "may say more about human control" but doesn't bear on the main question, so it's a lower priority. Recommendation: fix the two problems above, have a fresh agent recheck them, then release. At release, the investigation page (which doesn't yet mention the account or the Geneva outcome) and programme.md's Next need lines at the same certainty, under the consistency rule.

**Disclosure check:** this version clears the combined disclosure check (schedule/research-safety.md), figure and caption included. It's descriptive policy and press material with no operational or reconstructive detail.

## Resolution, by the driving session (28 November 2026)

1. "In practice" restored on every surface that dropped it: the title ("didn't say how it works in practice"), the summary (with the maker's reported statement of intentions set aside explicitly), the opening ("the nearest is two reported statements of what one maker intends, which don't agree"), the figure caption and the short form's summary and body.
2. The 28 November reads of the FT and Wired were fact checks for the separate essay, permitted by its revision plan and kept outside the study's ledgers; the piece now says so, that they were made after the first attempts were known to have failed, and links their log (notes/physical-authority/essay-checks/2026-11-28/fetchlog.md). They are not added to the study's reads.csv, since the plan says they enter no matrix cell; the brief's "ends that route" governs the study's collection, not these.

Readability: 3 taken ("the earlier survey" replaced by the search made when the work was commissioned); 1 taken in substance through the title's "in practice"; 2 left (the colophon and Methods already describe what the rereads are). Next step: the bounded route to a record of a fielded armed robot goes to the pilot's checkpoint; the investigation page and programme.md's Next were updated in this round, before the recheck.
