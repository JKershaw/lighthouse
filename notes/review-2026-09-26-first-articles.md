title: Review of the first two articles and their studies
kind: review
version: 0.1
date: 2026-09-26
authors: an observing agent, relayed by the keeper; recorded by the driver
grounded_at: e0b7ca4
cites: articles/what-we-can-see.md@e0b7ca4; articles/the-xz-backdoor.md@e0b7ca4; studies/LH003/@e0b7ca4; studies/LH004/@e0b7ca4; notes/retro-first-drive.md@e0b7ca4; registers/decisions.md@e0b7ca4

## Findings

The reviewer read all four pieces and checked several central claims against their sources. Both articles need one focused correction and editing pass before release; the xz piece is closer.

1. **LH004 lets the framework explain history.** The study says the gap in Lighthouse's surfaces, not any missing data, is why the earlier valgrind signal could be seen and still not believed. A gap in a 2026 framework cannot explain why people missed a warning in 2024. The defensible conclusion is that the historical case exposes a limit in Lighthouse's proposed instruments.
2. **LH004's opening overreaches.** It says nearly every Linux system links liblzma into sshd; its own findings say several distributions, through distribution-specific dependencies. The article already carries the narrower claim; the study must too.
3. **LH003's headline finding does not follow.** Different populations and units do not establish little overlap. The study takes distinct observation boundaries to mean the populations are almost disjoint while acknowledging that it measured no overlap, and its own table records connections: deps.dev combines package ecosystems, forge projects and OSV advisories. The defensible finding is that these are partial views whose relationships require investigation and whose counts cannot simply be added.
4. **LH003's Economic Index entry is outdated.** The Free and Pro only scope belongs to the February 2025 introductory report; later reports include first-party API traffic, and the June 2026 report separates chat, Cowork and API usage. Either describe the initial report explicitly or update the entry. A source needs its publication date and observation window beside the date Lighthouse read it.
5. **A definition is presented as a discovery.** Saying no source observes propagation directly because Lighthouse defines propagation as a derived relationship states how Lighthouse classifies evidence; it does not establish a limitation of all seventeen sources. The empirical question is which records support identifying and testing those relationships.
6. **Both articles carry the studies' machinery.** The survey's opening soon becomes a report about LH003, its candidate count and its procedure; the xz piece interrupts itself with "in the study's reading". Important qualifications stay beside the claims they constrain; routine provenance moves to notes. Both contain illustration briefs where finished illustrations should be, and the xz timeline could do substantial explanatory work.
7. **The xz payoff is sound.** Malicious material was publicly available, but runtime symptoms prompted the investigation. Availability, noticing an anomaly and recognising an attack are different events, and Freund's report supports the distinction. Watching code changes and dependency manifests would leave important observation points uncovered; test results and runtime behaviour matter too, which gives the new Correctness surface a concrete reason to exist.
8. **The retrospective is useful internal reading.** Correcting the confusion between final context size and tokens consumed is a real improvement in measurement, and the reported split between subagents and driver makes orchestration overhead visible. Both remain estimates with stated limits, and a drive's cost should stay distinct from later editing work.
9. **On the decisions.** D-0001: keep the distinction between subscription usage valued at list rates and actual API spending explicit; the subagent limit leaves driver consumption unbounded. D-0002: keep it provisional; the price argument does not yet show better research quality on comparable tasks. D-0003: strongly supported; these studies show why local calibration should not gate every outward investigation. D-0004: supported, adding that passing a check does not establish correctness and an error does not establish malice.

## What follows

Corrections to LH003 and LH004 in their Corrections sections and text, then both articles redrafted from the corrected records under the piece rules, with drawn illustrations; a review of the result before the keeper's release decision. Filed as E-0003, E-0004 and R-0001.
