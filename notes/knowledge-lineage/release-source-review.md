# Knowledge Lineage release source review

**In short.** All 49 study navigation entries were checked against their retained passages and original lead at `8af0cb0`. All 204 passages occur exactly in their named frozen sources. The sole blocking population claim was corrected and passed its bounded recheck; no source-review blocker remains for this navigation release.

Reviewer: fresh Codex host-model evidence review, 11 November 2026. This reviews the navigation summaries, questions, limits and state labels; it is not a new research release or independent validation of the underlying studies. Read the repository's AGENTS.md. No external sources, credentials or source collection were used. No code, backfill or commit was changed by this review.

## Scope and checks

- `backfill-a.json`: all 17 entries, LH000 and LH002 to LH017.
- `backfill-b.json`: all 17 entries, LH018 to LH034.
- `backfill-c.json`: all 15 entries, LH035 to LH049.
- Every summary, question, limit and state was read against its exact evidence and frozen lead. Fuller source context was checked where the selected passages did not establish a statement, including the PHP source clocks and missing reads, image selection and censoring, unreviewed checkpoints, protocol schedules and the vendor-panel selection rule.
- All 21 publication summaries in the overview match the existing frozen `site/sections.md` editorial summaries exactly. They are reused navigation text, with the underlying publication and its source notices still the authority.

The entries retain the consequential distinctions: requests and instructions versus installation and runs; reported versions versus protection; selected examples versus rates; pooled comparisons versus libraries as units; overlap versus replication; post hoc readings versus tests; agency classifications and participant accounts versus demonstrated exploitation; and documented instruments versus measurements of the internet. The newer checkpoints are labelled unreviewed where their results are used. The day-7 PHP and Node.js records are kept distinct from later checkpoints.

“Record available” is an availability label and does not assert completed research or review. “Protocol only” describes a brief lead, including a brief with a dated checkpoint in its opening. Explicit closure language supports LH019, LH024, LH025 and LH043; LH043's limit preserves its unreviewed status. No other completion or causal overstatement was found.

## Blocking correction

**LH037, `backfill-c.json`, summary.** “The protocol follows statements and fixes from 20 vendors shipping PHP” wrongly says the panel members are known PHP shippers. The frozen brief's **The panel** says the rule chooses vendors “not vendors known to ship PHP”; **Measures** expressly says this is not a sample of vendors that ship PHP. The selection deliberately includes vendors that publish nothing about the flaws as a baseline.

Replace that opening with, for example: “The protocol follows statements and fixes from 20 vendors chosen by their counts in CISA's exploited-flaw catalogue.” The checkpoint counts, unknowns and Google timing can stay. This is the sole blocking source correction found.

## Recheck

One bounded recheck completed on 11 November 2026. The LH037 backfill now says “20 vendors chosen by their counts in CISA’s exploited-flaw catalogue”, accurately preserving the frozen panel's selection rule. The exported `overview.json` explanation contains the identical corrected summary and all its evidence still occurs exactly in the frozen brief. Its input commit remains `8af0cb026037a8ee63456900978b3c44473c49cd`.

**Final source verdict: pass for the navigation release.** The single blocking correction is resolved. This verdict does not upgrade the completion, review or evidence status of any underlying study. No build was run during the recheck.
