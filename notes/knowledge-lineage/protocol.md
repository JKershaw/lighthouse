# Can a small evidence trail make earlier knowledge easier to use?

**In short.** We will test whether linked claims and source passages make two existing Lighthouse threads easier to follow. This is a retrospective method pilot and an unreleased interface, not another investigation. A fresh agent comparison can test retrieval; understanding by a non-technical human remains a separate test.

Protocol 0.1, fixed 10 November 2026 before extraction or comparative results. Owner: Codex, exact model identifier and attributable dollar cost unavailable. Authorisation: John’s assignment and issue #46. Proposal: [PR #47](https://github.com/JKershaw/lighthouse/pull/47), still open when inspected. No publication or collection schedule is created. The scheduled watch continues separately; schedule/check.py showed no overdue row and one record window open until 4 December. This task does not take it over.

## Prior knowledge and boundary

The author has read AGENTS.md, the proposal, issue, evidence-directory introduction, the claims table's introductory five lines, and the model-found-bugs investigation page. The proposal describes 83 reviewed rows and an Australia access gap subsequently checked. These are known examples, so the corpus is not an unseen validation set. Comparative answers and sampled rows have not been inspected. The visual story will be selected retrospectively and must be labelled as such.

## Population, unit and selection

Freeze the input repository commit in baseline.json before extraction. From the numbered claim rows in notes/it-was-only-a-test/claims-table.md, take ordinals 1, 6, 11, ... up to 81 (maximum 17). Keep each row intact. Do not substitute interesting rows. Include immediate named source anchors, the evidence README, essay correction, claims check, Australia verification, session record and review notes as contextual records, without counting them as extra sampled claims. Retain omissions and unresolvable original-pack paths explicitly.

External thread: take the first six distinct HTTPS source links in document order from studies/LH036/brief.md, then the first six new ones from studies/LH038/brief.md (maximum 12, below the proposal's 25). Only metadata, excerpts and relationships already retained in the repository; no fresh crawling or full-text downloads. The investigation and these briefs supply the thread context. No oldest-paper or comprehensive literature claim. Explicit bibliography can be indexed; no claim of intellectual influence without a supporting passage. Prior reads retain their original dates; this pilot's inspection date is a separate clock. Unknown source or event dates stay null.

Unit of extraction: one bounded claim or explicit record relationship, with source path, exact passage, input SHA-256, source/event date where known, retained read date where known, pilot assertion date, asserted-by and status. An extractor can check that text occurs; that is not substantive verification of a source's claim. Source assertions, pilot-checked links, inference and unresolved candidates remain distinct. No confidence numbers. No temporal order inferred from two links appearing together.

## Eight fixed tasks

Answer each with exact record links, the passage used and limits. A missing answer is allowed.

1. For sampled claim ordinal 1, locate its asserted source and passage. Does the record independently confirm the event?
2. Repeat for sampled claim ordinal 6. Distinguish attribution from a Lighthouse measurement.
3. Locate the Australia access gap, the later verification, and what the original reviewer could not check.
4. Find a dated correction to the essay, its prior account and why the qualification matters.
5. Find the model-discovery source report and the investigation's distinction between scores, patch availability and real-world exploitation.
6. Can the public record establish the private vulnerability report date? Locate the explicit unknown and the disclosure protocol.
7. Do the selected records establish measured deployment uptake or social benefit caused by the discovery? Identify what would be required if not.
8. Show a defensible connection between the two threads and say whether it is a citation, evidence of influence, or a thematic research lead. Do not invent an influence edge.

## Comparison and adjudication

Two fresh agent contexts get the same questions and caution about source instructions. Baseline gets only tracked files from the frozen commit and normal rg/read/search. Assisted gets the export and prototype plus those same original files. They work separately with no shared answers. This between-reader assignment avoids a same-reader second-attempt advantage but does not balance different agent abilities; it is a feasibility check, not a causal estimate. Both reviewers use the available host model; this is not the Anthropic-model release review. Neither condition may collect new external evidence. Record elapsed time if actually measured, commands/tool calls if available, correct sources, omissions, false claims and caveats. The author adjudicates every answer against the original passages, accepts equivalent valid sources, retains disagreements, and cannot claim blinding. Each question gets 1 for correct answer with a valid pinpoint and limits, 0.5 for incomplete, 0 for wrong/unsupported; show the item scores, not a significance test.

Audit extracted relationships at claim ordinals 1, 11, 21, 31, 41 plus every hand-curated visual edge. Check passage, predicate, target, dates and attribution. Report incorrect, ambiguous and omitted relationships separately. Duplicates and failed ID matches remain unknown/failures. Record structural coverage across all selected rows, not just the audit.

## Reader and implementation checks

Demonstrate follow-a-finding and follow-a-topic without internal codes as prerequisites. All displayed relationships have a working local record/source link; plain text explains each line and status without colour. Distinguish reported, checked, inferred and disputed. Display event and retained-read clocks separately. No JavaScript is required for the text, figure or evidence navigation. Check 390px and desktop, light/dark, keyboard focus, headings/link names and reduced-motion behaviour. A fresh agent can attempt journeys and report misunderstandings, explicitly as a proxy. A human unfamiliar with the record is still needed before claiming human comprehension gains.

## Ceiling, stopping and decision

One session, maximum four hours active work, at most three fresh agents (baseline, assisted, technical/reader check), no paid APIs, services, database, scraper, background job or framework. Stop collection at the fixed existing records; stop after one build, review, fixes and targeted recheck, or at the ceiling with unfinished checks listed. Runtime/tool counts where available; inference dollar spend unknown rather than zero. No full-text redistribution beyond already retained material and short source anchors. Preserve evidence restrictions and email redaction.

Stop if provenance cannot be retained or if the design obscures claim status. Revise if traceability works but retrieval is mixed, maintenance is high or human comprehension is untested. Expand only after a checked retrieval improvement, no material false edges, a completed unfamiliar-human reader test and normal release review. A useful new question must change an actual investigation choice with a recorded reason before claiming research benefit. No fourth investigation or automatic obligation follows this pilot.
