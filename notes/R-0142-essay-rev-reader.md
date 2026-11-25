# R-0142: reader review of the revised essay "Seen from outside, seen from inside", stage one

Reviewer: a Claude Opus 5.5 subagent, 25 November 2026, reading only essays/drafts/seen-from-outside-seen-from-inside-rev.md (version 1.1 draft).

## What a reader would believe, written before reading the record

**Argument.** PHP and Node.js released fixes on 21 October 2026. PHP could be seen only from outside, through a scanner (Censys) counting services that announce their version. Node.js could be seen only from inside, through nodejs.org download counts. The essay argues that this difference reflects two ways software exists: "standing" software that changes only when someone acts, and "rebuilt" software that changes as builds turn over. Each instrument has a blind spot on the opposite side.

**Observed.** Week-one and day-30 patched or fixed shares for each branch or line. More than half of version-reporting PHP services ran unsupported branches, against 10 per cent of Packagist installs and roughly 12 to 16 per cent of Node.js downloads. A rise in services reporting no version, which looks like an instrument change. Node.js downloads halve at weekends.

**Explained, and caused.** Weekend dips are read as builds following the working week. Late PHP rises are attributed mostly to fewer services being counted, and late Node.js rises mostly to downloads of newer versions. These are presented as decompositions, not causes. Lockfiles are offered as a possible brake, but not shown to be one.

**Measured versus interpretation.** Shares, counts and the two day-30 tests are measured, some under rules or splits chosen after the data were seen, and these are labelled. The standing and rebuilt framing, the "layers" map and the link to AI activity are all interpretation.

**Limits a reader notices.** Different units, so the numbers aren't comparable. Censys's patched share is a floor. Downstream backports are not measured. The standing/rebuilt test "passed but tells us little" and may follow from the units alone. No further data will come from these studies.

## Stage two: against the record

Read: studies/LH033 and LH034 (records 1.2 and 1.1, briefs with amendments, record_v1.json, LH034's measure 2 daily table, the Censys reads), articles/a-week-after-two-fixes.md (2.0), investigations/software-updates.md, programme.md's Next, proposals.md P-0001 and P-0008. Not opened: LH008, LH011, LH018, the September build-server piece (the 32 against 41 per cent figure is unchecked here), the review/essay-rev-2026-11-25 directories, other notes. Calculation: studies/LH033/review/R-0142_reader_checks.py, output R-0142_reader_checks.txt.

**What the round establishes.** Every figure I checked matches the records or the retained reads: week-one and day-30 shares under both Node.js rules, the patched-count changes, tests A and B (8.0, 18.8 and 8.3 points), 22.5 million and 51.8 per cent, 24.4 million on day 7, 110.9 million services and 40.5 per cent reporting on 28 October, the 56.0 per cent jump in counted services on 23 October, 62.3 per cent without a version, Node.js's unfixed share of 11.8 to 16.5 per cent on days −7 to 7, the weekend totals (no weekend day above 18.1 million, no full weekday below 19.9 million, 23 September to 20 November), the five largest unfixed branches on 25 October, the amendment timings and the collection stop. The essay states the post hoc rules and splits wherever it uses them, and it reports the weakened test A honestly. My stage-one reading matches the records, with the two exceptions below.

**Material claim problems.**

1. *What part of the scanner's view is old (a proxy treated as the whole).* The essay says: "But the same layer of old software is most of the picture from one side and a small part of it from the other" (essays/drafts/seen-from-outside-seen-from-inside-rev.md, "What each view cannot see"). Old branches are 51.8 per cent of version-reporting services, but only 19.6 per cent of all PHP services Censys counted on 20 November (22,516,583 of 115,094,397), because 62.3 per cent report no version (R-0142_reader_checks.txt; LH033 `m2_unfixed_tail`). The earlier sentence keeps the qualifier "that announced a version". "Most of the picture" drops it, and the "Side by side" sentence ("a large, old layer beneath") builds on it. Nothing is known about whether hidden-version services lean old or new. *Resolution:* say "more than half of what the scanner can place, about one in five of all the PHP services it counts". Or keep "most" and tie it explicitly to services that announce a version.

2. *The layered map is kept at full strength after its timing test failed to tell the layers apart.* "Side by side" still describes "a rebuilt layer that turns over quickly ... a standing layer that changes when someone acts on it", and "We think that is the internet AI systems now work in". It says this without the day-30 caveat that the essay gives two sections earlier. On the records, both counts did most of their moving within two weeks (LH033: patched counts +0.5 to 0.9 per cent of the branch from day 14 to 30 in three branches). Node.js's below-fix downloads also stalled after day 12 (LH034, resolution_R-0131). Test A's result "could follow from the units alone" (both records). What still separates the layers in the evidence is the size of the old tail, which is measured in different units and populations, plus a mechanism argued a priori. The measurements could all be right while "two ways for software to exist" is wrong, or is only "two ways of counting". *Resolution:* in "Side by side", add one clause saying that the month's counts did not tell the two layers apart by speed, and that the outline rests on the mechanisms and on what each instrument can see.

No other material problem found. "Censys's patched share is a floor" holds as a floor on protection. The record's caveat that "patched" may include services first seen already fixed is carried in the essay.

**Readability.**
- The opening's "PHP we could see only from outside" sits uneasily beside the Packagist figure used later. A half-clause would help: Packagist counts installs by PHP's minor version, which cannot show a patch spreading.
- The "Later evidence" box is dense. Its second half repeats test A's detail from the last section, and could be cut to the result and a link down.
- "11.5 per cent a month on" is one day. Days 8 to 30 ranged from 10.4 to 15.8 per cent, so "on 20 November" would read more exactly.

**Next step.** The essay is fit to go to its recheck and release once items 1 and 2 are reworded. Neither needs new data. On the research named in "What would test this": none of the three can separate "two ways to exist" from "two units" on timing. An outside sample of Node.js servers by version would test only what the download log misses; no source is known and none is scheduled. P-0008, the lockfile census, still has no reader ("name a reader") and isn't near. P-0001, the blind classing of instruments by vantage, is cheap desk work on pages already kept, but it waits for the LH035 map page and tests the broad reading, not the standing/rebuilt claim. The essay correctly says nothing is scheduled. I'd recommend taking P-0001 first, because it is available and cheap. A proposal is worth adding for a test that holds the unit fixed: the share of fetches from build servers against the rest, by day, for one fix, within PyPI's logs, which LH011's data already flag. Only a comparison like that could show standing and rebuilt behaviour inside one unit.

Combined disclosure check: clears. The material is aggregate public counts of version uptake, with no hosts, accounts or mechanisms.

## Resolution, by the driving session

25 November 2026, Research run 2026-11-25T151200Z-anthropic-research. Both material problems accepted.

1. "But the same layer of old software is most of the picture from one side and a small part of it from the other." became "But the same layer of old software is more than half of what the scanner can place from one side, though about one in five of all the PHP services it counts, since most announce no version, and a small part of the picture from the other." (22,516,583 of 115,094,397 on 20 November, 19.6 per cent; studies/LH033/review/R-0142_reader_checks.txt.)
2. "Side by side": after "...versions nobody has moved." added "The month's counts didn't separate the first two by speed: both did most of their moving within two weeks, and a test of it that passed may follow from the units alone. So the outline rests on how each kind of software is kept and on what each instrument can see, not on a measured difference in pace."
- Readability 3 taken ("11.5 per cent a month on" became "11.5 per cent on 20 November"); 1 and 2 not taken.
- Next step: the reviewer's proposal of a within-unit comparison (build-server fetches against the rest, day by day, for one fix in PyPI's logs) is added to proposals.md as P-0051 for the next sweep's gate; P-0001 stays where it is ranked.
