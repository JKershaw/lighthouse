title: The reader-and-inference review, a pilot for the next two research rounds
kind: working note (the pilot's instructions, dispatch text and log)
version: 0.1
date: 2026-09-29
authors: the driving session of 29 September 2026 (Opus 5.5), at the keeper's request

## What it is

A second review before release, after the evidence review of AGENTS.md step 4, which it does not replace. The evidence review asks whether the figures and the reproducibility hold. This one asks: **could these measurements be correct while the piece's explanation is wrong?** The reviewer reads the public pieces first, as an ordinary reader would, writes down what that reader would come away believing, and only then reads the study to compare.

It runs for the next two research rounds, the rounds that release a piece or change the current account after 29 September 2026. The rehearsal of 29 September on LH012's corrected pieces (notes/R-0018.md) is not one of the two. At the first checkpoint after the second, the programme decides from the log below whether to keep it, change it or drop it.

## Allowance

Up to five dollars at list rates for the reviewer on Fable 5.1, both stages and the one recheck, inside the round's bound of about twenty dollars of subagent spend. The driving session prices it from the transcript (`harbour/hb tokens --latest`) and writes the figure in the log. If the round cannot fit it beside the evidence review, the driving session says in the log and the close-out what it cut to make room, or that the pilot was skipped and why.

## How to dispatch it

- Dispatch it after the evidence review's fixes are in, on the text as it would be released.
- Give the reviewer the two task texts below, the repository path and the paths they name, and nothing else: not the working conversation, the conclusion the round hopes for, the evidence review's verdict or note, or any list of problems already known. Tell it not to read keys from the environment and to keep searches out of harbour/.session/.
- **Stage 1 paths**: the full piece, its short form, and the "Current focus" section of README.md. **Stage 2 paths**: the study's directory (record, brief, amendments, sources, data, scripts), the investigation page, programme.md's Next, and the next study's brief or, if it has none, its issue.
- The stages run in order. Where the harness can continue an agent (in Claude Code, SendMessage to the same agent), send stage 2 only after stage 1 has written its assessment and returned. Otherwise give both in one prompt and require that the stage 1 assessment be written to the note before any other file is opened. No tooling used so far can stop a reviewer opening other files, so the driving session checks the reviewer's transcript for files opened during stage 1 and says in the note what it found.
- A fresh agent is not an independent one: it runs on the same family of models and reads the same record. Its agreement is a review contribution, not independent confirmation, and no page says otherwise.

## Stage 1, the task text

> You are a reviewer for Lighthouse, an observatory kept largely by AI agents, which publishes what it finds in public records. This review has two stages; this is the first. Read only these files: [the full piece], [its short form], and the section "Current focus" of README.md. Do not open the study record, its brief or data, programme.md, the investigation page, any note in notes/, releases.md or the git history, and do not follow links out of these files. Then create [notes/R-nnnn.md] with a heading "What a reader would believe, written before reading the record", and under it, in no more than about 250 words: the principal finding as a careful ordinary reader would say it back; what appears to have been observed, what appears to have been explained, and what appears to have caused what; and the limits a reader would notice. Write what the pieces lead a reader to believe, not what you suspect the study says. Then stop and return the note's path; the second stage will follow.

## Stage 2, the task text

> Now read the study behind these pieces: [the study's directory], the investigation page, programme.md's Next, and [the next study's brief or issue]. Do not read other notes in notes/, releases.md or commit messages; they carry other reviewers' verdicts. The central question is: could these measurements be correct while the pieces' explanation is wrong? Compare what the reader would believe with what the evidence supports. Where they apply, and only if they matter, consider: a proxy treated as the thing of interest; a share read as a rate or a speed; aggregate counts read as people, machines or linked events; an assumption stated in the study that disappears in the summaries; compatibility, association or a modelled estimate presented as a demonstrated cause; a method fixed in advance that faithfully answers a different question from the one the piece appears to answer; a short form or headline implying something the full record contradicts. These are prompts for judgement, not categories to fill. You may challenge the brief itself, and you may conclude that there is no material problem. Then assess the next research decision: can the evidence it proposes distinguish the explanations in play, is that evidence available and when, and would another step materially improve understanding? Continuing, adjusting, waiting and changing direction are all valid answers. Add to the note, briefly, under these headings: **What the round establishes**; **Material claim problems**, each with the exact passage (file and quotation), the evidence (file and figure) and a proposed resolution, where a problem is material if a reader would come away believing something the evidence does not support, and "none" is a valid answer; **Readability**, at most three optional suggestions; **Next step**, a recommendation with its reasons. Keep any calculation you make as code and output under the study's review/ directory. Edit no file but the note.

## After the review

Resolve every material claim problem before release, or write in the note why the evidence supports disagreeing. Readability suggestions are optional. After revising, send the same reviewer only the changed passages, for one recheck of the claims they affect; do not restart the review and do not start a second round of it. Whatever stays disagreed is written in the note and in the close-out. The next-step recommendation is weighed at the checkpoint in programme.md's Next, with the reasons for following it or not.

## Log

One row per round. "Worth it" is the driving session's judgement in a line: did it change a public claim that the evidence review had passed, or improve the next research decision, for its cost?

| Round | Study and pieces | Reviewer and cost | Material problems raised | Changed before release | Disagreed, with reason | Also raised by the evidence review | Next-step recommendation, and what was done | Worth it |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rehearsal, 29 September 2026 (not one of the two) | LH012's pieces as corrected to version 1.1 | | | | | | | A rehearsal of the workflow on problems already known and fixed before it ran; not evidence that the reviewer finds them |
| First research round | | | | | | | | |
| Second research round | | | | | | | | |
