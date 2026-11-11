# Keeping the knowledge map current

**In short.** Each site build refreshes the catalogue from the checked-out commit. Authored explanations remain tied to a reviewed source revision, and any change to that source withholds its explanation until checked. This first rule is conservative: even a formatting-only change asks for review.

11 November 2026. Knowledge Lineage version 1. The original pilot baseline and comparison remain unchanged. The maintained navigation has a separate curation reference.

## Automatic work

`npm run build --prefix site` runs `overview.mjs --live`, writes ignored `site/.generated/knowledge-map.json`, and renders it. The public JSON download is this same live file. New studies appear without registering them by hand. Only publications explicitly marked released enter the catalogue. Working records remain distinct from released findings and essays.

The live file carries its input commit, source hashes, `stale_annotations` and a stale flag for the selected visual history. A whole-file hash change in a reviewed source withholds its study summary; the current source record stays linked. Changed evidence behind any selected-history node or edge withholds that drawing. Missing explanations are not completed studies or failed findings. Historical snapshot exports and the original comparison stay in notes/knowledge-lineage and git.

## Bounded agent work when publishing or correcting

Read the live stale list. Check only the affected summaries and connections against their primary records, retaining result and consequential qualification passages. Have a fresh agent check substantive changes as part of the existing publication review. Preserve tentative, attributed, post hoc and inconclusive statements.

The authored files are backfill-a/b/c.json and overview-history.json. `curation-ref.json` identifies the revision checked for the maintained annotations; advance it after checking affected records and regenerate `overview.json`. This does not change baseline.json or the original experimental results. Regenerate the selected drawings if their content changes. Run the tests, builds, link checker and browser workflow before release. Correct or remove unsupported connections; never manufacture a connection merely to fill the map.

No recurring scout, new investigation or background collector is created. External literature expansion still needs a bounded source-selection plan. Inference cost remains incomplete in this harness.

## Reader direction, 11 November 2026

John asked to remove the dedicated homepage promotion. The intended experience is contextual discovery while reading: an inviting route beside or after a piece into related questions, evidence and other research streams. A simple flow chart belongs in supporting navigation or on its own page. Prominent homepage treatment could become appropriate when a larger visual corpus has a worthwhile shape to explore. This records the direction for a separately previewed design; it does not commission a new sidebar or related-reading implementation.
