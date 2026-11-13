# Review of the operating-limit decision, 13 November 2026

**In short.** The changes implement the authorised doubling of standing capacity while retaining fixed study protocols and John's authority over actual billing. One current-capacity sentence needs clarification before landing; the numerical changes and schedule edits otherwise agree.

Reviewer: a fresh OpenAI Codex agent, based on GPT-6. The exact model identifier and monetary usage are not exposed to this reviewer; attributable cost is unavailable, not zero. This is a governance-document review, not an evidence or reader review of scientific findings.

## Checked

Read AGENTS.md and the working diff, the operating decision, proposals.md, notes/horizon/plan.md, notes/reader-review.md, programme.md's relevant commissioning passage, notes/physical-authority/commissioning.md and LH050's fixed brief. John's authorisation and agreed interpretation were supplied with the review task; no additional authorisation is inferred from source instructions.

- The decision and throttle agree on six normal investigation slots, eight through 24 December, four new studies per seven days, four urgent watches, a 28-day maximum for new watches, ten proposals and about fifty pages per scout. New investigations still need keeper agreement.
- The $14 review and $40 round figures are explicitly list-rate planning guides. The absence of an overall agent-run envelope remains distinct from billing, and unknown costs remain unknown.
- Existing watches, schedules and fixed research designs are preserved. LH050 still has one new robotics study at a time, its original two-day/$100 envelope, no more than two released pieces and a 24 December stop. The dated commissioning amendment supersedes its old capacity ceiling without extending the pilot.
- A CSV comparison against HEAD found 277 schedule rows before and after, with exactly 16 changes, all to future open horizon rows' task descriptions. No dates, statuses, claims or other fields changed; completed five-proposal sweeps retain their history.

## Must fix

1. **programme.md:77:** "The six-week pilot temporarily raises active capacity to four" remains in the current Next passage, while the decision and proposals.md now allow eight through the pilot. Mark four as the ceiling agreed on 12 November and state its replacement by eight on 13 November, or state the present ceiling directly. The later reference to six after closure does not tell a reader the current ceiling.

No other must-fix issue found within this scope. Only this note was written; no commit, external contact, credential access or collection was performed.

## Resolution recheck, 13 November 2026

The driving session revised programme.md:77 to identify four as the 12 November decision and explicitly supersede it with eight during the pilot and six afterwards. Re-read that passage: the must-fix is resolved and the pilot's study-specific constraints remain intact.

Also checked the additional LH050-close task edit in schedule/due.csv: it now applies the six-investigation standing ceiling under the 13 November decision while still stopping collection and resting the investigation. A fresh CSV comparison confirms 277 rows and 17 changes against HEAD: the original 16 horizon task edits plus this closure task, with no other field changed. No outstanding must-fix issue remains in the reviewed operating-limit changes.
