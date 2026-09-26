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

- British English. No em dashes or en dashes in prose; use commas, colons or full stops. Hyphens inside identifiers, file names and command output are data, not punctuation.
- Studies use the plain names: activity, residue, propagation, observation, instrument. Images such as the coral, the ripple, the afterglow, the nearest star and the standard candle belong to essays and the charter, and arrive with their literal meaning the first time they are used.
- Label a statement as observation, derived measurement, interpretation or scenario wherever a reader could confuse them.
- Leave unfillable fields blank and say what could not be filled. Never invent a timing, a count or a source. Cite sources by the S numbers in LH F02 where one exists, or by URL with the date read.
- Study write-ups use the skeleton in LH F05: header, Answer, Findings, Method, Limits, Next, Corrections. Notes and essays follow the Harbour paper standard's form.
- Tables keep the same number of columns in every row. Identifiers: LHnnn for studies, I-nnnn for instruments, Q-nnnn for questions, D-nnnn for decisions, C-nnnn for claims, L-nnnn for ledger entries, E-nnnn for editing tasks that turn a study into an article.

## Conduct

- Agents do not publish, do not spend beyond the budget in LH F06, and do not change Harbour. A person reads and releases.
- Do not read or use credentials from the environment unless the task names them. Never write a token, a session id or a key into the repository.
- Tag your own activity so that it is recognisable as Lighthouse's, and measure your overhead where you can.
- Commit with a clear message that says what changed and why. Never rewrite history on a shared branch.

## Finishing a dispatched task

A task begins with its ticket identifier so that it shows in Harbour's records. It ends with the deliverable the ticket names, committed to this repository, and with feedback posted to Harbour: a short account of what was done, a usage entry, and exactly one terminal marker. If the deliverable cannot be produced, say why in the feedback, mark the task failed, and leave the ticket open.
