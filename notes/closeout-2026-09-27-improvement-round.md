title: Close-out of the improvement round of 27 September 2026
kind: close-out
version: 0.1
date: 2026-09-27
authors: a Lighthouse research subagent (Opus 5.5) for the round's coordinator, who completes the spend line
grounded_at: 497d4ff, with the round's uncommitted changes

## What was learned

No new reading of the internet was made this round; everything below comes from the evidence LH010 had already retained.

- Whether pinned software moves sooner before the advisory to a fix whose own notes say so depends most on which public notice counts as the advisory (derived; studies/LH010/LH010.md version 0.3). Counted to the earliest reviewed record naming the fix, or to the NVD times those records carry, the pooled lead widens, while library by library the two kinds still cannot be told apart. NVD's time came first for 17 of the 43 events, and for nltk and pip a reviewed record came six days before the fix itself.
- Nine of the 21 silent fixes had no notes that could be read at release, so they were missing evidence rather than silent (derived).
- Every reading that did separate the two kinds was chosen after the outcomes were known, and none is claimed (interpretation).

## What changed in the current account

- The announcement question went from "not found library by library" to "not settled" (LH010 version 0.3, released after notes/R-0011.md). "Later evidence" notices were added to articles/fixes-that-said-so.md and articles/what-moves-a-pin.md. programme.md now has dated later-evidence lines under LH007, LH008 and LH009: pyjwt's earlier NVD time, and the advisory burst that did not recur.
- The synthesis, articles/where-software-updates-go.md, is the current account, released with its brief and the rewritten latest piece after notes/R-0012.md. The investigation page, investigations/software-updates.md, points to it. An adversarial review of the whole round (notes/R-0013.md) fixed four site defects and two statements in about.md and AGENTS.md.
- Instructions: AGENTS.md now opens with a short statement of where things stand, and adds a consistency rule, a fuller brief convention, the methodological lessons of R-0010 and R-0011, a checkpoint choice and this close-out. It is 1,970 words, down from 2,293 at the start of the round (f5a0021).

## What remains uncertain

- Whether a fix's own notes make any difference. The question rests with issue #12.
- Whether a new release reaching half of a library's downloads within two days is the rule or was a property of `mcp` 1.27.0. What the CI flag in the download log means, and how much of the early uptake is builds.
- Why any single project moved when it did. What was installed beyond the few published images, and whether any public record reaches a run.

## Next outward question

LH011: does a release reach half of a project's downloads within two days as a rule, and how much of that is builds? Its brief, studies/LH011/brief.md, was written before any outcome was read and is ready to launch. The checkpoint comparison under programme.md's Next says why it was chosen over continuing the announcement question or repairing the notes reading.

## Spend

Measured at list rates from the transcripts with `harbour/hb tokens --agent` and `harbour/hb drivercost --since 2026-09-27T00:00:00Z`, prices from harbour/prices.json read 26 September 2026. Output tokens are estimated from characters produced, as the tool says, so these are estimates. Ten subagents, $30.33: the site survey $0.48 (Opus 5.5), the reanalysis $6.84 (Opus), the site infrastructure $2.03 (Opus), its review $4.12 (Fable 5.1), the writing $3.11 (Opus), the site wiring $1.57 (Opus), the cold reading check $0.17 (Sonnet 5), the instructions and LH011 brief $2.26 (Opus), the release review of the pieces $3.44 (Fable) and the adversarial review $6.31 (Fable). The driving session: $5.53 (Opus 5.5) to the time of this line; the last commit and merge are not in it. About $35.9 in all, above AGENTS.md's bound of about twenty dollars a session, which this round, a maintenance round of four packages asked for by the operator, was not held to. The instructions agent also made five web searches.
