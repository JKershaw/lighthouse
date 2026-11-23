# R-0126: recheck of what the R-0124 and R-0125 resolutions wrote into LH047 (versions 0.5 and 0.6)

**In short.** A fresh agent read every passage of studies/LH047/LH047.md that changed between version 0.4 (cc695b64) and version 0.6 (d266ed6b) against the files it cites. Most of it holds. One new figure was wrong: W5's comparison that leaves out LH041's collector removed its 85 breaches but not its 2,327 requests, so "12 of 3,412 ... both well under 1 per cent" should be 12 of 1,170, 1.0 per cent, against 0.1 per cent in week 47. That is corrected here, with three smaller fixes, all in version 0.6.

Rechecker: a subagent of the Research run of 23 November 2026 (Claude Code, Opus 5.5 as reported by the harness). Offline, no network request. A second agent's agreement is a review contribution, not independent confirmation.

## What was checked

Read: notes/R-0124-lh047-reaudit-evidence.md and notes/R-0125-lh047-reaudit-reader.md with their Resolution sections; `git diff cc695b64 d266ed6b -- studies/LH047/LH047.md`; notes/R-0124-lh047-reaudit-evidence/recount.out; studies/LH047/review/r0125/gate_split.py and .out; data/reaudit-2026-W47/README.md; review/brief_as_fixed.out; brief.md sections 5, amendments 1 and 2. One calculation of my own, on data/audit/requests-judged.csv (8 November), run inline with `python3 -I`:

```
rows by who, R1 does not comply: LH041 85, LH042 research 3, LH044 3, essay-reader-review 2, essay drafting 1, LH042 1, essay-claims-check 1, LH046 1
LH041 (the collector) requests: 2327 (all from its log; R1: 2242 complies, 85 does not)
without LH041's collector: 1170 requests, 12 R1 breaches
of those, log rows only: 1119 requests, 8 R1 breaches
```

Held against the sources:
- Answer, Part C: 53 and 54; 1,581/15, 1,454/142, 1,437/159 (recount.out; each sums to 1,649); 40 Crawl-delay, 13 only because of robots.txt reads; 11 walls. The brief's section 5 rule ("unknown if none does but R1 is unknown") is paraphrased correctly.
- W1's added window (main at f5aed20) matches R-0124.
- W2's added paragraph: the departure, the post hoc label and the two alternative splits match recount.out.
- W3: the Wikipedia and Wikidata reading (W01648, W01653 in recount.out, among the 13), 7 of the 11 wall breaches after a 429 (LH055 5, LH053 2), 150 identification unknowns (recount.out R8).
- W5: 75 gate refusals, 36 of them LH039's; 0 R1 breaches among gated page requests (719 complies, 12 unknown); both R1 breaches on routes outside the gate (Horizon, gated "n/a"); 21 gated failures, 14 Crawl-delay and 7 walls; 0 LH041 rows and 0 PyPI JSON requests in week 47 (gate_split.out). Amendment 1 changes R5, R8, reporting and copies, not R1: correct.
- Labels: the W2 rule is labelled post hoc; W5 stays a description and says the gate's effect is not measured. The opening's "mostly a change in what was audited" is supported in counts (85 of the 95 fewer breaches).
- Review-status lines, header, Part C heading, Next and Corrections now agree.

## Changes made (all in studies/LH047/LH047.md, version 0.6)

1. W5. Old: "it is 12 of 3,412 against 2 of 1,649, both well under 1 per cent." New: "it is 12 of 1,170 (1.0 per cent) against 2 of 1,649 (0.1 per cent), so a smaller gap remains, which these two audits can't attribute (a comparison made after both audits' figures were seen; one exclusion)." Why: LH041's collector made 2,327 requests on 8 November, not 85; R-0125's "about 3,412" subtracted breaches, not requests. The corrected rate isn't "well under 1 per cent", and the gap doesn't vanish. The comparison was chosen after both figures were seen, so it is labelled post hoc.
2. Opening. Old: "85 of those 97 came from one collector that week 47 doesn't include." New: adds "; without it, 8 November had 12 among 1,170 requests, against week 47's 2 among 1,649." Why: without it a reader could take "mostly composition" to mean no difference remains.
3. Opening. Old: "outside the shared robots.txt check our collectors have used since 9 November". New: "... most of our collectors ...". W5. Old: "the collectors were put behind a shared gate that reads robots.txt first." New: "most collectors were put behind ... first (LH044's collector, which reads robots.txt itself, made week 47's 88 page requests outside it)." Why: gate_split.out, pages gated "no": LH044 collect.py 88.
4. Opening. Old: "by a daily read going back to a page that had answered with a wall the day before". New: "by a daily read going back on a later day to a page that had answered with a wall". The same in W3 ("return the next day" to "return on a later day"), in Next ("the day before" to "on a later day") and in the 0.6 Correction ("next-day return" to "return on a later day"). Why: LH055's reads of 19 to 22 November (4 of the 11) followed a 200 on 18 November; the last wall was the 429 of 17 November (recount.out R6 rows).
5. Header `grounded_at`. Added that week 47's figures come from data/reaudit-2026-W47/replay.sh (history back to 12 November, population at e74c302) and the 0.5 and 0.6 splits from recount.py and gate_split.py. Why: R-0124 S1 asked for this and the resolution said S1 was applied, but only `cites` had changed.
6. Corrections, version 0.6: a sentence listing these changes.

## Disagreements left as they are

- The opening still says "under our own name (3 adding Anthropic's names)". R-0125 flagged this as readable as if requests were sent under Anthropic's names. It's a readability point, not an error, and the Answer is exact.
- "Both audits are floors, but week 47's more so" is a judgement. It's reasonable given that no transcript was read for week 47, and it's worded as a judgement.
- The opening's review status ("after an evidence review and a reader-and-inference review") doesn't mention this recheck. Next does.
- R-0124 S2 asked for a Limits line. The disclosure went into W3 instead. That's adequate.
- R-0124 S1's `instruments` point (the re-audit's code, frozen rule files) wasn't taken. `cites` names code/, so I left it.

## Verdict

Cleared at version 0.6, with the six changes above. The new W5 figure (change 1) is arithmetic on the retained 8 November table and needs no further reader.
