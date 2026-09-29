# LH016 study brief

**Brief, written before any change in its frame was coded or counted, 29 September 2026.**

**study:** LH016
**edition:** 0.1
**status:** fixed at the protocol commit, before either coder reads a diff or a review note's findings
**date opened:** 2026-09-29, 18:50 UTC, on the keeper's question for this drive
**written by:** the driving session of 29 September 2026, evening, in Claude Code, model Opus 5.5 (claude-opus-5-5, as its harness reports)
**grounded at:** repository commit f17523c (LH015 released), with this study's files uncommitted in studies/LH016/
**issue:** #20 (JKershaw/lighthouse), filed with this brief

## Question

In the research rounds of 28 and 29 September 2026, which steps of Lighthouse's research and review workflow changed what its public pieces and records say about the internet, what kind of change each made, at what cost, and what kind of problem reached release without any of them catching it? For the pieces released on 26 and 27 September, which public claims were changed after release, and what caught them? What should the workflow keep, change or drop in the light of that?

Why it is asked. The keeper asked it. The workflow now spends about as much on checking a study as on doing it, and it has grown a step at a time: an evidence review from the first day, a blind check once, a reader-and-inference review from 29 September, with the keeper reading released pieces throughout. Each step was kept on the judgement of the session that added it. A watch that publishes claims is only as good as what stands between a draft and a release, so it should know which steps change claims, which kinds of error pass all of them, and where money buys accuracy.

What it cannot say. Whether any conclusion is now right: it counts changes, not truth. Whether a step prevented errors that never reached a draft, which is how a brief's rules and a research agent's own checks act, and which leave no trace in the history. Anything of rounds it does not read. Every agent involved, the coders and reviewers here included, runs on the same family of models, so their agreement is a review contribution, not independent confirmation.

## What the writer already knows of the outcome, disclosed

- **notes/reader-review.md**, read at the start of this session in full, log included: its three rounds (LH012's correction round as a rehearsal, LH014, LH015), the material problems each raised (3, 1 and 5), that each was changed before release, that the note records none of them as raised by the evidence review, the driving sessions' judgement "worth it" in each, and the costs ($13.34, $5.18, $3.95).
- **The close-outs of 27 to 29 September 2026**, read for their spend and for what changed: the keeper's reading of LH011's released piece led to version 1.1 (a low share of downloads is not a slow spread; the first-day observation labelled as read after the counts; the title's unbounded "never" removed; numbers in place of the brief's label); the keeper's reading of LH012's released piece led to the correction round (what other libraries' limits could account for stated as a model's estimate; an old Python said to rule out newer versions without choosing among older ones; downloads sharing reported fields no longer called one kind of machine); the improvement round's reanalysis of LH010's retained evidence moved its answer to "not settled"; LH015's blind check agreed on 57 of 60 classes and two classifier rules were corrected with no label moved; LH012 tested on releases not read the first-day reading LH011 had made after its counts, and it held for 28 of 32 libraries. The two revision commits' messages (6cb9051 and c480bb0) were read and say the same.
- **AGENTS.md**, which says that the errors in the first drafts came from a research pass on Sonnet and the review that caught them ran on Opus, and carries the lessons of R-0010, R-0011 and R-0014; **notes/retro-first-drive.md**, which says the first drafts still needed a person's review.
- **To define the frame:** the subject lines of every commit, the spend lines of the release commits, and the header of every review note (title, date, reviewer, grounded commit, what it cites). Not their findings, except as the documents above report them.
- **The writer's interest, disclosed.** The writer drives the rounds' successor under the workflow being assessed, and the documents above already call the reader review worth its cost. Hence the codebook fixed here, the attribution from the diffs rather than from the notes' verdicts, and a second coder who does not see which step made a change.

## Frames, unit and stages

### Primary frame: six rounds, as commit windows

Each window is a pair of commits in this repository; the diff between them is what changed while that step ran. The windows were set from the commit subjects alone.

| Round | Window | Step in the window |
| --- | --- | --- |
| P1, LH011 release | 1bc6e80 to a36508d | evidence review (notes/R-0014.md) |
| P2, LH011 revision | a36508d to 6cb9051 | the keeper's reading of the released piece, carried out by the driving session |
| | 6cb9051 to c2e4d4e | evidence review (notes/R-0015.md) |
| P3, LH012 release | 08c505b to 89d4aa7 | evidence review (notes/R-0016.md) |
| P4, LH012 correction | 89d4aa7 to c480bb0 | the keeper's reading of the released piece, carried out by the driving session |
| | c480bb0 to e26c856 | evidence review (notes/R-0017.md) and the driving session's follow-up |
| | e26c856 to abca590 | reader review, stage 1 (notes/R-0018.md) |
| | abca590 to c8d2a89 | reader review, stage 2, and the driving session's resolution |
| | c8d2a89 to 4253613 | recheck, and release |
| P5, LH014 | 9523003 to 63d8a62 | evidence review (notes/R-0019.md) |
| | 63d8a62 to 6497799 | reader review, stage 1 (notes/R-0020.md) |
| | 6497799 to be156d5 | reader review, stage 2, and the resolution |
| | be156d5 to 8d21cdd | recheck, and release |
| P6, LH015 | 2135c64 to 3ca1804 | blind check (notes/R-0021.md, stage A) |
| | 3ca1804 to c488d2a | the driving session's corrections after the blind check |
| | c488d2a to b1e2c99 | evidence review (notes/R-0021.md, stage B) |
| | b1e2c99 to 92d2013 | reader review, stage 1 (notes/R-0022.md) |
| | 92d2013 to ab2b12c | reader review, stage 2, and the resolution |
| | ab2b12c to f17523c | recheck, and release |

Any commit after f17523c up to this brief's protocol commit that changes a primary-frame piece is read too; none is known.

**Surfaces coded** in each diff: the piece and its short form; README.md; investigations/software-updates.md; programme.md (the study's answer, "Later evidence" lines and Next); AGENTS.md's "Where things stand"; observations.md; notices added to other pieces; the study's record (Answer, Findings, Method, Limits, Next, Corrections); its brief and amendments, and the next study's brief, for decisions; a figure by its caption, its title and the labels its drawing script writes. **Not coded:** data files, scripts except as they change a figure or a number in text, site code, colophons, releases.md, and the review notes themselves, which are read to attribute a change, not coded as one.

### Secondary frame: the pieces released on 26 and 27 September

The pieces of LH002 to LH010 and the synthesis, for one question only: which of their public claims were changed after release (a Correction notice, a rewrite, a "Later evidence" notice), when, on whose prompting, and whether a review before release had read the passage (notes R-0001 to R-0013 and notes/review-2026-09-26-first-articles.md). A "Later evidence" notice reports new evidence and is counted apart from a correction. This frame is not coded change by change, because several of those rounds kept no commit before their review.

### Unit

A **change**: one problem addressed in one window, however many surfaces carry it. One fix carried to five surfaces is one change with five surface edits; two problems fixed in one sentence are two changes.

### Steps a change is credited to

- **K**, the keeper's reading of a released piece, as carried out by the driving session. The keeper's own words are not in the repository; the revision commit's message and the close-out say what was asked, and a change in a K window that neither names is credited to D.
- **E**, the evidence (release) review, the edits its reviewer made itself included.
- **B**, the blind check.
- **R1**, the reader review's stage 1, which writes a note and is expected to change no text.
- **R2**, the reader review's stage 2, with the driving session's resolution of the problems it raised.
- **RC**, the recheck.
- **D**, the driving session on its own: a change in a window that no note, commit message or close-out in that window names.
- For the research steps, which leave no before and after in the history: **W**, a research pass's own check that its record says changed something; **P**, a rule fixed in a brief that set or withheld a label or a claim, where the record says so; **Lit**, a literature check that changed a design, where programme.md's Next says so; **L**, a later study that tested an earlier reading or added "Later evidence".

Attribution: a change is credited to the step whose window holds it and whose note (or, for K, whose commit message or close-out) names the problem. If a later step in the same round raises it again, that step is recorded as "also raised". A change the diff shows and no document names is D.

## Codebook, fixed before any change is coded

**Tier.**
- **A, public claim.** After the change, a careful reader of a public surface (the piece, the short form, the front page, the investigation page, the programme's answer, a notice on another piece, AGENTS.md's "Where things stand") would believe something different about the internet, or believe it with a different certainty.
- **B, record claim.** The record's Answer, Findings, Method, Limits or Corrections change in substance, and no public surface does.
- **C, decision.** The next research step changes: a brief or an amendment, an issue filed or re-scoped, programme.md's Next.
- **N, not material.** Wording, readability, order, typography, links, colophon, metadata, and any rewording a careful reader would say back the same way.

**Type**, one main type for A and B:
- **unit**: what is counted, or the denominator (a share of projects given as a share of recipes);
- **figure**: a number wrong, or computed another way;
- **certainty**: a label or a claim's strength ("as a rule", "most", "explains");
- **cause**: an association, a compatibility or a modelled estimate read as a cause or as what happened;
- **scope**: a window, a population, or an absolute without its window;
- **post hoc**: a reading's status as made after the counts;
- **new reading**: an interpretation or measure, not in the text before, that changes what the main claim means;
- **consistency**: a surface saying something at a different certainty from the record;
- **limit**: a limit a reader needs, added or restored.

**Direction**: **correction** (removes or fixes what the evidence did not support), **qualification** (adds what the evidence requires), **addition** (adds a reading the evidence did not require, pending a test), **decision**.

**Improved**: **yes** if the change moves the text towards what the retained evidence supports; **pending** for an addition; **no** if it moves the text away, with the evidence named.

## Measures

- **M1.** For each step, the A, B, C and N changes in the primary frame, by type and direction, and the A-tier surface edits.
- **M2.** For each step, how many of its A-tier changes altered text that an earlier step in the same round had read and passed.
- **M3.** Cost per A-tier change by step, from data/costs.csv, which the driving session filled from the close-outs and release commits before this brief was committed; a step with no recorded cost is left blank. The keeper's reading has no model cost, and the driving session's share of a window cannot be separated from the session's total.
- **M4.** Escapes: A-tier changes made after a piece's release, in both frames, by who raised them, and which checks before release had read the passage.
- **M5.** Readings made after the counts that entered the frames, by step, and whether a later study has tested them, with the result.
- **M6.** Reversals: a change undone or contradicted by a later change in the frames.
- **M7.** Research steps: the records whose Answer says a label was set or withheld by a rule fixed in the brief; the literature checks that programme.md says changed a design, and whether the change touched an outcome.
- **M8.** Reliability of the coding: a second coder's agreement with the first on a random sample.

## The first coder's table

data/changes.csv, one row per change, with these columns: `id` (round and number, P1-01; S for the secondary frame's rows), `round`, `window` (the two commits), `step`, `also_raised` (steps, separated by semicolons), `named_in` (the note, commit message or close-out that names the problem), `surfaces` (separated by semicolons), `surface_edits` (a count), `before` and `after` (the passage quoted from the diff, shortened with "..." where long, on the main surface), `evidence` (the record passage or retained file the change rests on, quoted or cited), `tier`, `type`, `direction`, `improved`, `passed_by` (earlier steps in the round that read the passage and did not change it), `post_release` (yes or no), `post_hoc` (yes if the change introduces or labels a reading made after the counts), and `comment`. A change the first coder cannot attribute or class is kept with the field blank and the reason in `comment`.

## The second coder

After the first coder has finished and committed its table, and before the driving session reads any tally, scripts/draw_sample.py draws 30 A, B, C or N changes of the primary frame with Python's `random.Random(16)`, 16 for LH016, from the table sorted by its identifier (all of them if there are 30 or fewer). The second coder, a Fable 5.1 subagent, is given for each sampled change the surface, the text before and after, and the record passage the change rests on, and not its step, note, window, reason or the first coder's codes. It codes tier, type and direction by this codebook. scripts/compare_blind.py reports agreement and Cohen's kappa on material or not (A, B or C against N) and on the four tiers. If kappa on material or not is below 0.6, the per-step counts are reported as the first coder's reading and the comparison between steps as inconclusive. Disagreements are listed, not settled by the first coder.

## The comparison that would matter

For each step, the A-tier changes it made that no earlier step in the round raised, and what they cost. Six rounds, no test and no rate: the comparison is a description of these rounds. The steps read different texts at different points, a later one reading what earlier ones left, so a step's count is what it added in its place in the order, not what it would find alone. No step ran without the others, so nothing here measures what the workflow would have released without a given step, except in the escapes, where a step that ran later caught what earlier ones had passed.

## Sources

The git history of this repository (commit messages and diffs), the review notes R-0001 to R-0022 and notes/review-2026-09-26-first-articles.md, the close-outs' spend tables and the release commits' spend lines (as data/costs.csv), the records' Corrections sections, the pieces' notices, and programme.md's Next. All read locally: no web page, no download count, no account and no key.

## Overlap, disclosed

The study reads the review notes and close-outs whose verdicts it reports. notes/reader-review.md's "worth it" column is the driving sessions' own judgement; this study codes from the diffs instead, and reports where it differs.

## Resource ceiling

About twenty dollars of subagent spend at list rates: the primary frame's coder (Opus 5.5) up to about $8; the secondary frame's reader (Opus 5.5) up to about $3; the second coder (Fable 5.1) up to about $2; the evidence review of the record (Fable 5.1) up to about $7. No piece is planned, so no reader-and-inference review; if the record earns a piece, the piece waits for another session.

## Stopping condition, and what would leave it inconclusive

It stops when the record is written and reviewed with nothing that must be fixed, at the ceiling, or when a subagent reports nothing usable. Inconclusive for the comparison between steps: a kappa below 0.6 on material or not; a step seen in fewer than two rounds (the blind check ran once; the reader review three times, once as a rehearsal on text the keeper had already corrected), which the record reports as a case, not a pattern.

## What the lessons will do

The record will say, as interpretation, which steps to keep, change or drop, and which kind of error the workflow is least likely to catch before release, each tied to rows of its tables. The session changes AGENTS.md or notes/reader-review.md only where a recommendation follows from a count, and puts the rest in programme.md's Next.
