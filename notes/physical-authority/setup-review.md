# Review of the physical-authority setup

**In short.** Two fresh Codex reviewers checked the commissioning and protocol setup, not the underlying deployment claims. The first found wording and traceability problems; those were corrected and the second found no must-fix issue. A final build exposed a knowledge-map assumption about the original three investigations, which was repaired and separately rechecked.

12 November 2026. Driving session and reviewers: OpenAI Codex. Exact model identifiers and attributable spend unavailable; this is not zero cost. The user approved the subject, proposal and preparation, then confirmed the concurrent scheduled work had concluded and permitted merging. No external source collection was undertaken under the new study protocol.

## First review

The reviewer read AGENTS.md, the changes, investigation, commissioning notes, brief and ledgers. It found that calling Changi's robots unarmed inferred a negative from a source that merely supplied no armament evidence. The investigation and brief now describe a civilian patrol comparison with armament not established. Historical commissioning documents are retained as received and labelled as unverified context.

It recommended an exact read ID in every claim so later snapshots remain distinguishable, and an explicit failure rule when ranked search results cannot be retained. Both were added. Minor wording was corrected: the pilot is above its earlier capacity note, and none of the missing-evidence labels means zero.

## Fresh recheck

A second reviewer checked the corrected preparation at `cef0c9e` and found no must-fix issue. It confirmed exact-snapshot references, the ranked-selection failure rule, all 15 new rows matching the brief, empty outcome ledgers, definite collection and capacity endpoints, commissioning-draft status and preservation of the completed run's existing schedule.

## Map integration and code recheck

The first local build generated four catalogue groups, but the display loader admitted only its original three. After that build, a frozen-corpus test also accidentally loaded the generated live catalogue and compared its new record count against the frozen count. The loader now displays every declared investigation, preserves the original order and supplies a fallback for future groups. Snapshot tests load an isolated retained corpus, and a new regression test checks a previously unknown investigation and its study route. No frozen evidence or annotation was changed to make a test pass.

The second reviewer read these code changes and found no must-fix issue. The 52 site tests pass. Schedule validation reports no table problems; all pre-existing schedule bytes from the completed run are preserved, with only the 15 new rows appended. The local build succeeds. Existing unresolved-link warnings elsewhere remain; the new investigation, brief and commissioning links were checked locally. The live map resolves the fourth group and its new study route.

This is a setup/protocol review. It is not the evidence review, reader review or recheck required for future empirical findings or essays. Those remain dated commitments in the schedule.
