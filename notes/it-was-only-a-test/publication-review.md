# Publication integration check: It was only a test

8 November 2026. Fresh agent reading of the publication changes in `lighthouse-publish`, after reading `AGENTS.md`. No essay or repository files edited. Scope: the retained reviewed draft, publication metadata and additions, existing source-note implementation, generated HTML, listings and SVG descriptions. Primary research was not repeated.

**Conclusion: no consequential prose, quotation, attribution or figure blocker.** One expected integration dependency remains in the inspected build: write `notes/R-0052-it-was-only-a-test.md` and rebuild so its three public links resolve. The publishing agent confirms that record is in progress.

## Preserved reviewed content

- Expanded the retained draft's `[^id]` references to their complete definition text. The resulting body, including every source note, is byte-for-byte identical to the published essay body after only normalising `assets/` to `it-was-only-a-test/`, version 3 to version 1.0, and excluding the new metadata/colophon/corrections section.
- The retained draft SHA-256 is `65aea2a96dcfc969f0439973063eb025e8db657485e985abd11629391f4f138f`, matching the final recheck's recorded hash.
- All five block quotations, both image alts and captions, incident attribution, the two simulated-continuation qualifications, absence of observed successor use in the local case, and proposed rather than measured mechanisms are preserved by that exact comparison.
- Both published SVGs are byte-identical to the retained reviewed SVGs. Each has `role="img"`, `aria-labelledby="title desc"`, and meaningful title/description elements. The loop explicitly identifies a hypothesis; the timeline identifies attributed clocks. The generated copies match their sources.

## Publication integration

- Header says `published: 2026-11-08`, `status: released`; version/date and explicit essay interpretation remain visible. Colophon names writing, fresh agent reviews, release direction, source/method/correction links and Lighthouse. No experiment is presented as performed. Unknown model identifiers and cost are explicitly unavailable in the record and release entry.
- Existing native `^[...]` source-note syntax is used without changing site code. The generated essay has 30 notes, 30 controls and 30 note bodies; IDs are unique, controls match their bodies, and default note content is present. There are no raw `^[...]` or `[^id]` remnants. Both external-source links and publication-local image paths render as HTML. Interaction and visual placement were not tested by this agent.
- Built front page and essay index link the new essay; README and `site/sections.md` descriptions keep the claim at interpretation/proposal certainty. Release entry is present.
- Generated essay, notes README and release entry each currently contain one unresolved span for the forthcoming R-0052 record. Other generated essay link/image destinations checked exist. Rebuild after creating R-0052, then confirm those spans become links.

## Small wording improvement

`releases.md` calls the four reader reviews “independent reader-perspective reviews”. “Four fresh reader-perspective reviews” would fit the essay/record's precise description of separate OpenAI agent contexts and avoid suggesting independence of evidence. This does not alter the reviewed essay.

## Limits

No browser or light/dark/phone visual check is claimed here, and no live site deployment was inspected. The publishing agent is separately checking theme render proofs and reports 43/43 existing tests plus a successful build. Exact model identifiers and attributable cost are unknown, not zero. This is the required fresh reading of publication changes, not a new independent validation of the incidents.
