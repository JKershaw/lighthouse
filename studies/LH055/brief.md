# Can public evidence establish that ARTEX operations used acquired AI credentials to sustain further credential hunting?

**In short.** We will establish what primary reports support about ARTEX's activity and examine the reported loop in which stolen AI credentials pay for more credential hunting. The commissioning discussion has already read some reports, including Amazon's warning that the outcomes in captured agent records were not independently verified. This is a retrospective baseline followed by dated observations, with collection ending on 1 December and three reviewed research rounds. Nothing has yet been collected under this brief.

The opening above is not part of the protocol.

## Protocol and owner

Protocol 0.1, fixed 17 November 2026 in the commissioning commit, before collection under this protocol. Author: Codex on OpenAI, exact runtime model unavailable. Accountable owner: the claiming driver under schedule/runner.md. Commissioning: [John's decision](../../notes/artex/commissioning.md), P-0039, [issue #57](https://github.com/JKershaw/lighthouse/issues/57). Investigation: [shared-internet costs](../../investigations/ai-cost-and-spread.md). Later method changes are dated amendments stating whether outcomes had been seen.

## Prior knowledge and overlap

The commissioning conversation on 17 November opened the FBI's 13 November advisory, Amazon's 13 November ARTEX report and Microsoft's ARTEX financial-sector report whose page said 6 November. Search results also displayed coverage through 16 November. Those tool-rendered reads are discussion context, not retained source bodies or protocol observations. They suggested widespread malicious use, human-set objectives, agent fleets sharing memory and a credential-to-inference feedback loop. Amazon expressly distinguishes captured records from verification of the outcomes they describe. Search snippets and dates may be wrong and must be checked at source.

Repository leads L-0064 and L-0091 already relay Censys exposure counts and Check Point's fleet report, including alleged successes that were hallucinations and a campaign in which no money moved. Both leads and the 10 and 13 November horizon notes were read during commissioning. Selection is purposive and outcome-informed; no prevalence or causal estimate follows. LH042 covers published exposure counts, LH041 registry worms and LH051 CI credential theft; reuse is disclosed by exact source and date, and supplies no independent confirmation. No baseline, prospective read or scientific review is complete at commissioning.

## Questions, units and population

1. What do the selected primary sources establish about ARTEX use, human involvement, persistence, scale and results as of the baseline?
2. What evidence supports each link in the credential-to-compute-to-further-hunting loop, and which links remain operator intent, agent self-report or publisher inference?
3. What materially changes during the prospective window, and does the available evidence warrant continuing this watch?

Population: the bounded purposive corpus below, not all ARTEX activity or all public reporting. Unit: an attributable claim about one campaign or one link of a mechanism, tied to its source version. Separately count a publisher's exposed hosts, consoles, targets, attempts, successful compromises and financial outcomes only in its own stated units, windows and definitions. Never add unlike counts or assume an exposed console is a malicious operator, victim or independent deployment.

## Sources and selection

The initial primary-source panel is fixed at these five endpoints, subject to the normal robots and access rules. They are discovery leads until retained under this protocol:

- FBI, advisory dated 13 November: https://www.ic3.gov/CSA/2026/261113.pdf
- Amazon, report dated 13 November: https://aws.amazon.com/blogs/security/amazon-threat-intelligence-observes-threat-actors-running-cybercrime-campaigns-with-artex-ai-agents/
- Microsoft, financial-sector report: https://www.microsoft.com/en-us/security/blog/2026/11/06/artex-abuse-expands-as-cybercriminals-target-financial-sector/
- Censys, exposed consoles: https://censys.com/blog/artex-agentic-asbestos/
- Check Point, operator fleets: https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/

Round 1 uses at most six discovery queries for current ARTEX primary reporting, named incidents and relevant literature, retaining queries, results and which pages were opened. Admit at most twelve primary source documents in total for that round, the five above included. Prioritise original telemetry or incident accounts, then primary research, then agency synthesis; retain failed/successful outcomes and counterevidence alike. Keep a source register of included and excluded candidates and reasons. Secondary reporting may locate sources but supplies no independent corroboration. Two reports repeating a single incident or dataset are linked as dependent evidence.

At the baseline, lock panel.json with the five endpoints and at most three additional primary-report URLs from that corpus. Additional panel URLs must supply a missing campaign, mechanism link or contrasting outcome, with the selection reason recorded before the first prospective read. They are selected after the retrospective outcomes are known. Do not silently replace an inaccessible endpoint; retain the gap, and date any amendment. Use a publisher's canonical redirect where accessible and record it. Guessed paths are not source evidence.

Round 2 may use up to four targeted discovery queries and eight additional primary documents, exclusively to test a missing link, distinguish an alternative explanation or establish dependence between reports. No generic second sweep. Prospective source discovery rides the existing horizon sweep: at each panel read inspect any new ARTEX leads it has already retained; record them, and admit up to four additional primary documents across the entire prospective phase if they could change a consequential claim. Panel membership does not expand automatically. Across the pilot: at most 24 distinct primary documents, plus search metadata and robots/access records.

## Collection and clocks

Use Lighthouse's existing collection, robots, provider-token, redaction and retention conventions. Before every read set LIGHTHOUSE_PROVIDER for the actual runner and use the existing robots gate. Retain permitted bodies, extracted text, UTC start/finish, requested and final URL, status, content type, source title and date, byte length and received-body hash; withhold emails and sensitive credentials, live-host indicators and personal identifiers from retained extracts. Do not fetch attacker infrastructure, exposed consoles, stolen data or payloads, run ARTEX, test keys, or contact anyone. A reported transcript is evidence supplied by its publisher, never instructions to follow.

Keep four clocks separate: the source's event/observation window, its publication/revision date, Lighthouse's retrieval time and the task's due window. An undated event stays undated. A changed page is first seen between two reads; it does not establish when the underlying event occurred. Compare meaningful text and claims, not advertising/layout byte changes alone. Measure or estimate collection overhead, recording elapsed time and request/byte totals; unknown overhead or cost is labelled unknown.

A panel read makes at most one content GET per endpoint (up to eight), plus robots requests and normal canonical redirects. No retry around an access wall in that read. A captured baseline on a scheduled read day can satisfy that day's identical endpoint reads by reference, without refetching. A dated prospective observation cannot be backfilled: missed windows stay missed. A late baseline is allowed up to 24 November, labelled with its actual date and the loss of earlier coverage; never recreate an earlier snapshot. If no baseline by that date, close collection with the gap and produce an inconclusive record from what can be retained without extending the pilot.

The separate LH055-baseline-closure gate has no successful-read dependency. It completes only when the baseline attempt is finished with a retained source/gap log, or when the late-baseline window has closed and a retained decision records no usable baseline. It must not complete while a baseline claim is running or while further baseline attempts are still intended. Reconcile the observation row to its actual done, missed or cancelled outcome, with reasons; do not call an unattempted capture successful. Round 1 analysis depends on this explicit closure, so missing evidence can produce an inconclusive reviewed answer rather than stranding the research chain. Prospective panel reads still depend on an actual completed baseline and panel lock; if absent, their windows become documented gaps. The final collection closure also reconciles them.

## Evidence table and comparisons

For each consequential claim retain its exact source/version and passage, campaign, event window, attribution, stated evidence access, outcome and limitation. Classify the basis as direct telemetry described by the publisher; agent-reported action/outcome; operator instruction/intent; publisher interpretation; or later independent corroboration. These describe published evidence, not Lighthouse's own access to incident telemetry. A source can have several bases, which must be explicit. Keep unsuccessful attempts and unknown outcomes.

Audit these links separately: credential acquisition; demonstrated credential validity/access; integration into an inference gateway; actual inference consumption; further hunting enabled by that consumption; and any acquisition of additional usable resources. For each report, mark each link supported by the stated evidence, claimed without sufficient disclosed support, contradicted, or unknown, and give the reason. No numeric certainty score or ratio over a selected corpus is needed. Do not infer spend from token availability or continued operation from an unverified agent assertion.

Compare each reported link across sources while tracing their shared evidence origins. Compare round 3's claims with the retained baseline, noting new evidence, corrections, withdrawals and unchanged assertions. A page repeating a claim is not fresh support. No cross-case causal effect or population frequency is estimated.

Competing explanations: successful resource acquisition sustained further operations; human-supplied resources sustained operations while credential harvesting was an objective; agents recorded intended or hallucinated successes; or later articles repeated one unverified account. Human direction and resource feedback can coexist. Distinguish task persistence, resource replenishment, increased targeting, self-propagation and reproduction: none establishes the next. A self-sustaining credential loop does not require or establish self-replication, independence from people or net profitability. Record what evidence would discriminate between these explanations and whether it is public.

## Three rounds and scheduled deliverables

All stages are explicit rows in schedule/due.csv. Reviews clear an exact record/draft version, not just completion of an attempt. Use the normal evidence review, two-stage reader-and-inference review and one fresh recheck of resolutions. Unresolved must-fixes block release with concrete revision work. Publication may be a reviewed record and investigation update if an article is not earned; document that choice. If an article is earned, include its short form and an evidence-grounded illustration, and review all changed surfaces. Ready interim answers proceed while later reads remain scheduled.

| Round | Collection/analysis | Reviews and public checkpoint |
| --- | --- | --- |
| 1, baseline | First capture due by 18 November; baseline record by 19 November | Evidence, reader review, resolution recheck and publication decision by 20 November |
| 2, mechanism | Focused missing-link audit after round 1's reviewed checkpoint; record by 24 November | Evidence and reader reviews, recheck and updated account by 26 November |
| 3, later evidence | Dated panel reads 18 to 24 November inclusive, 27 November and 1 December; collection closure on 2 December and final comparison by 2 December | Final evidence and reader reviews, recheck, account and close-out by 4 December |

Read windows are the named UTC days. A not-ready or unavailable attempt is not a successful capture; collection closure enumerates each read's actual outcome and gaps. Round 3 analysis depends on an explicit closure, not on every read succeeding. Closure has no successful-read dependency and reconciles all scoped observe rows to done, missed or cancelled with the protocol reason, after their windows close. Review and analysis deadlines are targets: lateness permits completing the existing work, not adding observations or silently cancelling reviews.

## Resource envelope, stopping and uncertainty

Three research rounds; at most 24 distinct primary documents; ten discovery queries; nine dated panel reads of up to eight endpoints each. A failed non-panel discovery document may receive at most one additional access attempt, in a later scheduled session before collection ends; panel endpoints instead have their nine dated reads, with no same-read wall retry. No broad crawl, paid service, account or outreach. This fixes research scope rather than an agent-spend stop that interrupts promised work. Record attributable driver/reviewer costs through the daily run, leaving unknown values unknown; John's billing failsafes are unchanged. Normal fresh reviewers may run as subagents under AGENTS.md; use its model and concurrency guidance.

No collection after 1 December. Finish existing reviews and close-out, then rest unless explicitly renewed. A checkpoint compares continuing, repairing measurement and another outward question, and records why its next step can change understanding. Do not require three articles or invent evidence to complete a round. If public evidence cannot establish a mechanism link, report the limit, possible discriminating evidence and its accessibility. No independent telemetry, no usable baseline, unclear report dependence or contradictory records can leave the central question inconclusive. Those outcomes do not establish absence of the mechanism.

## Publication and consistency

Maintain sources.md, claims.csv (or an equivalently replayable table), checkpoints and a versioned LH055.md with Answer, Findings, Method, Limits, Next and Corrections. Name reused sources and read windows. Reader-facing accounts use attributed verbs at the certainty supported. Update programme.md, the investigation, observations.md when there are actual observations to list, and normal editor surfaces. Replace any stale blanket assertion that no report describes sustaining activity with a precisely attributed later-evidence line after source verification and review; do not silently turn the old statement into an assertion that the phenomenon is proved. No new claim in Lighthouse's voice that harm is happening now or a named system is compromised is commissioned here. The normal keeper boundary remains in force.

## Amendment 1, 17 November 2026 (after the baseline's outcomes were seen, before any prospective read)

The baseline locked StepSecurity's synthesis (S07) into the panel as P07. The brief allows only additional primary-report URLs on the panel, and the evidence review of round 1 (notes/R-0087-lh055-r1-evidence.md, M5) found the slot outside the protocol. P07 is removed from the panel before the first prospective read on 18 November; the panel is the brief's five endpoints and SANS ISC's diary (P06), six content GETs per read. S07 stays in the round 1 corpus as a secondary locator and supplies no corroboration; primary reports it names may enter only through round 2's targeted queries or the horizon-lead intake, within their limits. No other method changes. Written by the Claude Code driver of run 2026-11-17T202935Z-anthropic-artex.
