# AGENTS.md

House rules for any agent working in the Lighthouse repository, whatever harness runs it. Read the README first; it indexes the founding documents. Harness-specific procedure lives in CLAUDE.md.

## What this repository is

Lighthouse is an observatory for the computational world: a standing watch, kept largely by agents, on how information flows through software and AI and what that activity leaves behind. The founding documents, LH F01 to F06, define the practice. Harbour (https://harbour.cat, source at https://github.com/JKershaw/LinearViewer) coordinates Lighthouse's tasks and is also its first calibration subject.

## Where things live

- `Lighthouse_*.md`: the founding documents. Change them only when a task asks for it.
- `harbour/`: the workspace as files. `north-star.md` and `tickets.json` are loaded into a fresh local Harbour at boot; `exports/` holds what Harbour recorded, one directory per export, named by collection time. `harbour/hb` is the boot, load, dispatch, consume and export script.
- `notes/`: research notes at the notebook level of LH F03's publication table.
- `studies/LHnnn/`: one directory per study, using the skeleton in LH F05. Created when the first study opens.
- `registers/`: the question, instrument, decision, claim and ledger registers from LH F05. Created by the tickets that start them.

## Writing

Two kinds of writing live here, and each has its own rules. Records are for checking: studies, notes, registers, and the instrument, decision and review records. Pieces are for reading: articles, essays, short forms and the front page. Text a person will read in isolation is a piece, and its first duty is to be a good read.

Both:

- British English. No em dashes or en dashes in prose; use commas, colons or full stops. Hyphens inside identifiers, file names and command output are data, not punctuation.
- Never invent a timing, a count or a source. Tables keep the same number of columns in every row.
- Identifiers: LHnnn for studies, I-nnnn for instruments, Q-nnnn for questions, D-nnnn for decisions, C-nnnn for claims, L-nnnn for ledger entries, E-nnnn for editing tasks, R-nnnn for reviews.

Records:

- Use the plain names: activity, residue, propagation, observation, instrument.
- Label a statement as observation, derived measurement, interpretation or scenario wherever a reader could confuse them.
- Leave unfillable fields blank and say what could not be filled. Cite sources by the S numbers in LH F02 where one exists, or by URL with the date read, and give each source's publication date and observation window beside the date read.
- Study write-ups use the skeleton in LH F05: header, Answer, Findings, Method, Limits, Next, Corrections. Notes follow the Harbour paper standard's form.

Pieces, under one editorial direction: write for a curious person who has never heard of Lighthouse's internal process; give them a reason to read, develop one idea at a time, and let them reach the evidence when they want it.

- A title that says the finding, a short opening that gives a reason to care, and a discreet date and byline. A small Draft label there is enough while a piece is under review.
- Open with the thing itself, a person, a moment or a surprise, never with Lighthouse or its method.
- One idea a reader could say back in a sentence, developed one thought at a time, so that the reader knows which thought to hold while the next one arrives. Say it, then qualify it once, in the sentence where the qualification matters. Routine provenance goes to the notes at the end.
- Plain words. Define a term where it is first needed, and only if it is needed; the three layers appear only where they earn their place. The charter's images are welcome, each arriving with its literal meaning the first time.
- No internal references in the prose: no document numbers, ticket or study ids, "the study" or "the keeper". The piece speaks as "we". The colophon may link to the record beneath the piece, so that a reader can reach the evidence when they want it; an id may appear there only inside the link.
- Honesty about what is known lives in the verbs, not in labels: the record shows, nobody has measured, we think.
- A colophon at the end, in the form LH F05 gives: sources, method in a sentence, authorship, review, version and corrections, and one line on what Lighthouse is. Commit hashes, task identifiers and dispatch details stay in the record beneath the piece, never in the piece.
- Illustrations drawn, not described, with a one-line caption.
- Read it aloud before handing it over; anything that trips is rewritten.
- No piece reaches the keeper without a review record.

## Conduct

- Agents do not publish, do not spend beyond the budget in LH F06, and do not change Harbour. A person reads and releases.
- Do not read or use credentials from the environment unless the task names them. Never write a token, a session id or a key into the repository.
- Tag your own activity so that it is recognisable as Lighthouse's, and measure your overhead where you can.
- Commit with a clear message that says what changed and why. Never rewrite history on a shared branch.

## Finishing a dispatched task

A task begins with its ticket identifier so that it shows in Harbour's records. It ends with the deliverable the ticket names, committed to this repository, and with feedback posted to Harbour: a short account of what was done, a usage entry, and exactly one terminal marker. If the deliverable cannot be produced, say why in the feedback, mark the task failed, and leave the ticket open.
