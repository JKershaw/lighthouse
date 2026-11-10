# Follow an idea: the Knowledge Lineage pilot

**In short.** Two small trails let a reader follow a corrected claim and a reported model discovery back to their records. The first agent comparison found the same retrieval accuracy with and without the index, so it does not establish a research improvement. Keep this as an unreviewed prototype, repair the remaining testing gaps, and test with an unfamiliar human before expanding it.

Version 0.1, 10 November 2026. Written by OpenAI Codex, exact model identifier and attributable cost unavailable. Scope: cross-cutting method pilot under [issue #46](https://github.com/JKershaw/lighthouse/issues/46), using the still-open [proposal #47](https://github.com/JKershaw/lighthouse/pull/47). No fourth investigation, new collection or schedule. Existing released prose is unchanged.

[Open the visual prototype](../../map/knowledge-lineage/) after building the branch. The site's Map page carries an explicitly unreviewed signpost. The prototype is not a released finding and enters no release feed.

## What is here

- [Protocol and dated amendment](protocol.md), committed before extraction and comparative outcomes. [Frozen input and active selection rule](baseline.json).
- [Versioned graph](graph.json), [manual annotations](annotations.json), and [directly linked drawing](finding.svg). Markdown and retained sources remain authoritative.
- [Baseline retrieval](baseline-review.md), [graph-assisted retrieval and AI journey proxy](assisted-review.md), [technical/source review and resolutions](technical-review.md), [evaluation](evaluation.md) and [item adjudication](adjudication.json).
- [Self-contained HTML preview](preview.html) for inspection before merging; its original-record links go to the existing site and its new-record links to this branch.
- Static render proofs in [proofs/](proofs/). These are HTML print-engine proofs, not mobile-browser screenshots. Browser and unfamiliar-human checks remain open.

## Reproduce

From the repository root:

```
python3 scripts/lineage/extract.py --check
python3 scripts/lineage/draw.py
python3 scripts/lineage/check.py
cd site
npm ci
npm test
npm run build
npm run serve
```

Visit `/map/knowledge-lineage/`. `extract.py` without `--check` rebuilds the JSON from the exact commit in baseline.json plus explicitly versioned annotations. Every edge retains its passage, line span, input hash and frozen-revision URL. It fails on a missing passage. A newer source requires a deliberate input/version change; it cannot silently change this history.

The tests check source passages and edge endpoints against frozen git, sampling, candidate separation and direction. They do not decide whether an attributed external event happened. The local check validates generated links and reproducibility without making external requests. The build has existing unresolved-link warnings elsewhere; the pilot's local links are checked separately.

Static proofs can be regenerated after the site build with `python3 scripts/lineage/render_proofs.py`, requiring WeasyPrint 70 and PyMuPDF. The session used an isolated scratch install. The script prohibits network fetches. It applies the mobile layout explicitly because a print renderer is not a browser viewport engine. Use a real browser for acceptance, not these proofs.

## What the sample can and cannot say

The fixed position rule selects 17 of the current table's 87 rows. The earlier Claude review covered 83, a different denominator. Twelve external records are source-panel entries, not twelve successful source reads or a systematic literature corpus. The external provider report is retained context outside those twelve selected entries. No DOI or citation index matching was attempted, so there is no match-success metric.

Historical review verdicts, an HTTP access failure and its later resolution stay separate from the corrected claims. Original full-text source-pack paths are explicitly unresolved; a reviewer quotation or source URL does not replace a locally retained original passage. A source account is not independent incident confirmation. The thematic bridge between the two trails remains an inferred candidate; the recorded reading of the first vulnerability brief by the second is a narrower documented reuse link.

## Why this could become useful

The strongest opportunity is to make claims, caveats and revisions reusable across time. A reader could see what changed since their last visit; a researcher could find the strongest earlier evidence and the unresolved disagreement before commissioning another study. Each later observation could extend a trail rather than produce another isolated page.

Keep the record centred on bounded claims, with bibliographic links, attributed intellectual influence, evidence relations and operational outcomes in separate types. Multiple parents and incompatible accounts should survive. Unknown dates and inaccessible regions should remain visible. A citation count or central position should never substitute for truth or benefit.

The proposal points to Lancaster's thematic review, the AI-security knowledge-graph paper, OpenAlex, Semantic Scholar, OpenCitations, W3C PROV-O and nanopublications. Those are methodological leads already identified by the proposal, not sources newly validated by this pilot. The current local JSON borrows the entity, activity and provenance distinction; it claims no PROV/RDF conformance. The next literature step should choose and inspect a small antecedent-paper set under a new fixed rule, starting from existing scholarship rather than inferring a field's history from this vendor case.

## Next

Revise before expanding. Complete actual 390px light/dark, keyboard and assistive-technology checks, then give an unfamiliar human the two journeys without coaching. Preserve errors and misunderstandings. A normal evidence/reader review is still needed before any release.

If that works, add optional “earlier evidence / what changed / used later” blocks to one existing investigation, with an explicit small maintenance allowance. The twice-weekly research scout could attach existing claim IDs and a reason for reuse to leads it already produces; the existing proposals gate still decides what starts. No new crawler or timer is needed. Ask whether a real investigation choice changed before claiming better research. Only then consider wider citation coverage, multiple evidence parents and a broader landscape view.

## Corrections and cost

Protocol amendment 1 repaired the original prose-link sampling rule. Review found an ambiguous visual direction, overly short excerpts, missing date/access metadata and a missing pilot-index route; these were repaired and the review keeps its initial findings. The evaluation states its remaining limits.

No external API charge was incurred by this pilot. Inference spend and the overhead of the three fresh agent contexts are unavailable in this harness, not zero. Package installation and local computation were not metered. The existing Harbour pricing commands need a named session/account and were not used to read credentials or invent a bill. No current scientific account or release list changed.
