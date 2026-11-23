# R-0125: reader-and-inference review of LH047 record version 0.5 (the week-47 re-audit)

Reviewer: a review subagent, Claude Code, Opus 5.5 (claude-opus-5-5), on 23 November 2026. Read only the header, the "In short." paragraph and the "## Answer" section of studies/LH047/LH047.md, stopping at "## Findings"; nothing else opened, no links followed, no network requests.

## What a reader would believe, written before reading the record

**Principal finding, as a careful reader would say it back.** In the week of 16 to 22 November, Lighthouse's logged requests broke sites' rules far less often than on 8 November: 53 of 1,649 against 172 of 3,497, and only 2 (or 3) robots.txt breaches against dozens. Most of the remaining breaches were coming back too soon for a Crawl-delay, or returning on a later day to a page that had shown a wall. But the record says these two audits can't be read as a trend.

**Observed.** The requests in the committed logs for that week, each judged against rules fixed on 17 November before judging; 53 (reading A) or 54 (reading B) did not comply; 40 broke Crawl-delay (13 only because a robots.txt read counts as a request), 11 revisited a walled page.

**Explained.** The week was chosen after Lighthouse put its collectors behind a shared robots.txt check on 9 November. A reader is led, by that placement, to infer the check caused the fall in robots.txt breaches, even though the record never says so and states the populations differ.

**Caused what.** Nothing is claimed as a cause; the sequence invites one.

**Limits a reader would notice.** The count is a floor, with no transcript extract, so unlogged requests are zero by construction rather than measured (8 November found 51). The "unknown" count swings from 15 to 159 by definition. The week-47 figures are unreviewed for reader inference; the In short calls them simply "unreviewed" while the Answer says an evidence review was done. The header's version line says 0.5, but the authors line describes only up to 0.4 and the date line lists 0.4 of the same day, so a reader can't tell what 0.5 changed.

## Stage 2: against the record

Read in stage 2: the rest of studies/LH047/LH047.md (version 0.5), brief.md with amendments 1 and 2, data/reaudit-2026-W47/ (README.md, summary.json, requests-judged.csv, code/ listed), investigations/ai-cost-and-spread.md and programme.md's Next. Disclosure check (schedule/research-safety.md): this round audits Lighthouse's own requests against sites' public rules, and the material adds no capability; proceed. One calculation, kept as code and output: studies/LH047/review/r0125/gate_split.py and gate_split.out.

**What the round establishes**

The measurements hold up as described: of 1,649 logged requests in week 47, 2 broke robots.txt under reading A (3 under B), and 53 broke some rule as fixed (54 under B). Every one of the 53 is named by practice and rule (summary.json; my split reproduces 2 + 17 + 14 + 9 + 2 + 5 + 4). W5 already says the fall from 97 to 2 is a description, not an effect of the gate. Can the measurements be right while the explanation a reader takes away is wrong? Yes, on one point (problem 1).

**Material claim problems**

1. **The fall in robots.txt breaches reads as the gate's doing, but mostly comes from composition.** Passage, LH047.md, In short: "A later week, 16 to 22 November, after Lighthouse put its collectors behind a shared robots.txt check on 9 November, was re-audited ... 2 broke a robots.txt rule under our own name". Its only stated reason for not comparing the two weeks is the transcript floor. Evidence: 85 of 8 November's 97 R1 breaches were LH041's PyPI JSON requests (W5). Week 47 has no LH041 request and no PyPI JSON request (gate_split.out: 0 and 0). Leave those out and 8 November had 12 R1 breaches among about 3,412 requests, against 2 among 1,649 in week 47. Both are well under 1 per cent, so on present evidence the robots.txt rate barely changed. The direct evidence that the gate is working is a different measurement: 75 requests the gate refused (36 of them only after the post hoc reclass of LH039's rows), every gated page request either complying or unknown under R1 (719 and 12), and both R1 breaches coming from routes outside the gate (the Horizon scouts' fetch tool and curl). Resolution: in the In short and the Answer, say that the collector behind 85 of 8 November's 97 didn't run in week 47. Give the gate's own evidence (75 refused; 0 R1 breaches from gated routes; 2 from ungated ones) in place of the before-and-after juxtaposition. Keep "not a trend". Put composition alongside the transcript floor as a reason the weeks can't be compared.

2. **A wall rule written for a 90-minute evening counts next-day reads over a week.** Passage, In short: "53 broke some rule, mostly by coming sooner than a site's requested delay or by going back on a later day to a page that had answered with a wall". Evidence: brief section 5, R6 ("any later request in the window"), was fixed for one evening, and amendment 1 didn't adapt it to a week. All 11 R6 breaches are daily recurring reads on a later day (requests-judged.csv R6_why), 7 of them after a 429, where Retry-After isn't recorded. Whether a site meant "never come back" is unknown. The record says the split was made post hoc but doesn't say the rule's meaning changed with the window. Also, 13 of the 40 Crawl-delay breaches exist only because a robots.txt read counts as a request, and 2 of those 13 also rest on one reading of a SemrushBot group (W3). Resolution: one clause in the In short and the Answer saying that under the narrowest readings about 27 of the 53 are against a site's stated pacing between page requests, that the 11 wall breaches are next-day returns the rule counts because the window is a week, and that 19 of the 53 have no recorded status. No figure changes.

3. **The summaries contradict the record on review status, and Next is stale.** The In short says "(unreviewed)", but the Answer says "after an evidence review". Next (LH047.md) still says "unreviewed; its evidence review, reader-and-inference review and recheck come next". The header's authors line stops at version 0.4. Resolution: make the three agree (evidence-reviewed, reader review in progress) and add version 0.5 to the authors and date lines.

The investigation page and programme.md don't mention week 47 yet. That's consistent with keeping an unreviewed result off the reader pages, and isn't a problem until it is placed there.

**Readability**

- The In short's last two sentences carry eight numbers. Lead with the plain point (robots.txt breaches were rare among logged requests, and most of what remains is pacing and next-day returns), then the counts.
- "under our own name (3 adding Anthropic's names)" reads as if requests were sent under Anthropic's names. Say "under the rules addressed to our own name; 3 counting rules addressed to Anthropic's bots".
- The record's title still names only 8 November.

**Next step**

Repair before measuring again. The re-audit's practical findings are concrete, and fixing them is cheap: honour Crawl-delay in the shared gate (LH038's 14 and the Horizon scouts' 17); have recurring daily reads remember a wall across days and back off (11); route the Horizon scouts and ad hoc reads through the gate and log them (both R1 breaches, and all 150 unknown identities); and have each session commit a transcript extract, so the unlogged floor stops being zero by construction. A further re-audit is worth fixing only after those repairs. Fix it in advance, with the comparison by gated against ungated route as its main unit, a wall rule defined for a multi-day window (for example, a return before any Retry-After, or within a stated back-off), and the gate keeping a copy or hash of each robots.txt so verdicts don't rest on later re-reads (596 of 969 here). Otherwise the comparison with 8 November will again be mostly composition. Before that, this record needs only the resolutions above and its recheck; no new collection is needed to state week 47 correctly.

## Resolution, by the driving session

By the Research run of 23 November 2026, in record version 0.6. Problem 1 accepted and checked against gate_split.out (0 LH041 rows and 0 PyPI interface requests in the week; both R1 breaches by routes outside the gate): the opening no longer places the week after the gate as its frame, says 85 of 97 came from a collector absent from week 47, and W5 gives the 12 of 3,412 against 2 of 1,649 and the direct evidence on the gate. Problem 2 accepted as one clause in W3. Problem 3 fixed (header, opening, Part C heading, Next). Next step: the repairs to Lighthouse's own collection are already in the record's Next as driving-session work; the design points for any later re-audit are added to Next. The recheck reads what this resolution wrote.
