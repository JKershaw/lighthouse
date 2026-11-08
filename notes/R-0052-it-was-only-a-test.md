# Publication check: It was only a test

**In short.** The approved essay is integrated into Lighthouse’s layout, listings and release record. A fresh agent found that its body and complete source notes are unchanged after presentation-only conversions; all five quotations, both figures and the qualifications remain. The tests and build pass; the live page and source-note interaction were checked after deployment.

8 November 2026. Publication authorised by the keeper. Writer and reviewer: separate OpenAI agent contexts. Exact model identifiers and attributable cost are unknown, not zero.

## Checks and resolutions

The [fresh publication reading](it-was-only-a-test/publication-review.md) expanded the draft’s footnotes and compared them with the native source notes: the entire pre-colophon body is byte-identical after normalising only illustration paths and version label. The retained [reviewed draft](it-was-only-a-test/reviewed-draft.md) matches the final source recheck’s SHA-256. Both SVGs are byte-identical to their reviewed originals, including accessible titles and descriptions. This checks integration, not independent confirmation of private incident logs.

All 43 existing site tests passed and Eleventy built successfully. The generated page has five blockquotes, two linked figures with captions and 30 source-note controls with unique matching bodies, from 18 definitions used repeatedly. The existing script supplies tap/keyboard expansion and wide-screen margin placement; without JavaScript notes remain readable. The essay is listed on the front page, essay index and feeds. Release metadata, colophon and correction status are present. This note resolves the first build’s missing review link. The release entry now calls the reviews “fresh”, avoiding an implication of independent evidence.

## Visual check

Rendered the actual generated HTML with Lighthouse’s CSS and fonts at phone width in light and dark, and desktop width in light. Inspected the opening and both illustrations. The portrait figures are capped at 32rem with a selector confined to this essay’s assets. Other figures retain their layout. The native essay accent, serif text and captions are preserved; the illustrations retain their drawn light backgrounds and readable labels in the dark theme.

These are WeasyPrint proofs with explicit media conditions and the native script’s initial closed-note state reproduced in the proof HTML. They are not real mobile-browser or JavaScript tests. The [proof script](it-was-only-a-test/render-proofs.py) uses WeasyPrint 70, tinycss2 and PyMuPDF; run it in an environment with those dependencies after `cd site && npm ci && npm run build`. The publishing session separately checked the deployed page and source-note interaction in a browser, as recorded below.

## Evidence and scope

[Primary-source check](it-was-only-a-test/facts-review.md), [reader perspectives and resolutions](it-was-only-a-test/review-notes.md), [final prose recheck](it-was-only-a-test/final-recheck.md), and [claims and sources](it-was-only-a-test/claims-table.md). No consequential factual, reasoning or publication-integration blocker remained. Publication launches no experiment, scheduled run or third-party contact.

## Live verification

The Site workflow for merge a9f6910e3807113b3655b21e3421899eb9a533d6 completed its build and deployment successfully ([run](https://github.com/JKershaw/lighthouse/actions/runs/42497606155)). The published essay at https://lighthouse.harbour.cat/essays/it-was-only-a-test/ was opened in Chrome, its Released state and complete text observed, and its first source note expanded and collapsed successfully. Both SVGs loaded; after the updated offline assets activated and the page was refreshed, each figure rendered at the intended 512px maximum width. The browser viewport was 1363px wide with no horizontal page overflow. The opening, timeline and handover diagram with their captions were visually inspected. This was a real desktop browser check; phone light/dark checks remain the explicit render proofs described above.
