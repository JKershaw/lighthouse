# R-0061: LH041 reader-and-inference review

## What a reader would believe, written before reading the record

Read from the opening paragraph, the Answer and the proposed lines for the investigation page and programme.md. README.md has no "Current focus" section.

**Principal finding, as a reader would say it back.** Worms that steal publishing tokens spread through npm very fast. The two biggest waves jumped between many unrelated sets of maintainers within hours: Shai-Hulud 2.0 reached 88 maintainer groups in under 15 hours, ChainDrop 13 in under 4 hours. Other waves stayed in one group or a few. The AntV wave was mostly one account's 316 packages.

**Observed.** OSV lists malicious versions; npm records when each was published; seven of thirteen named waves match vendor indicators, two more match by date. PyPI's publish times are gone.

**Explained.** The groups are "maintainer groups", which a reader takes to mean distinct sets of people whose packages were poisoned, each a separate victim.

**Caused.** A reader would believe the worm itself, using tokens stolen from one group, caused the poisoning of the next group: 88 groups in 15 hours means roughly 87 hops of infection. "Upper bound on spread without a person" reads as: at most this much was automatic, perhaps less if an operator stepped in. The reader would not doubt that the clusters correspond to real infections passed from one victim to the next.

**Limits a reader would notice.** Unreviewed and interim; two choices made after the counts; the records cannot show whether a person acted between publishes or who infected whom; no install counts; PyPI unreadable; people run these worms, not AI. A reader would probably not notice that "who infected whom" being unknown undercuts the hop reading above.

## Stage 2, after reading the study

Read: studies/LH041/ (record 0.2, brief, sources, scripts, tables, StepSecurity's page w19), investigations/ai-cost-and-spread.md and programme.md's Next. Checks were run on the retained tables only; nothing was fetched.

### What the round establishes

The measurements look sound and are carefully labelled. OSV's text carries the vendors' indicators for seven waves; npm's publish times survive for many removed versions and agree with vendor clocks to the minute or second; Shai-Hulud 2.0's 1,029 dated versions all went up on 24 November 2025 under 88 groups of packages that share a current maintainer, and ChainDrop's indicator-joined versions under 13 groups in 3.7 hours. PyPI is undated. The post hoc exclusion of out-of-window versions is benign for these two waves (the group counts are the same in the brief's view), and it is labelled. Could the measurements be right and the explanation wrong? Yes, in one specific way: the counts fit a chain of worm infections, but they fit equally well one publishing run, or one operator's pool of earlier stolen tokens, spread over groups that today's maintainer lists happen to separate. The record says so in its Limits; the summaries do not carry it.

### Material claim problems

1. **"Upper bound" is stated without its condition.** Passage: opening ("these are upper bounds on spread without a person"), Answer 2, the investigation page line and for-driver.md. The count is an upper bound only on the groups OSV recorded; Limits calls each wave's count "a floor of unknown depth" (OSV's 444 ChainDrop packages against Aikido's at least 868). A reader takes it as a ceiling on the wave's self-spread. Fix: "an upper bound on how many of the groups in OSV's records were reached without a person's new act; OSV's records are themselves incomplete, so a wave's whole reach may be larger."

2. **Groups read as separate victims or steps in a chain.** Passage: "reached many separate groups of maintainers within hours" (opening, investigation page, programme). Stage 1 of this note read 88 groups as roughly 87 infections, and nothing in the summaries corrects that. The retained clusters table argues against it: in Shai-Hulud 2.0 the second group's first publish came 11 seconds after the first's; two pairs of groups began in the same second (04:25:39, 07:33:01); three began within 14 seconds at 09:12 and three within 11 seconds at 11:18; ChainDrop has two groups starting at 10:39:07 and two at 10:41:16 and 10:41:17, and one scope that StepSecurity lists as a single victim organisation falls into two groups. A group starting seconds after another was not reached by a fresh install of a poisoned package; it was the same run, a split made by today's maintainer lists, or one engine holding several tokens. StepSecurity also says one infected CI run yields every secret injected into it. Fix: say in the opening and public lines "a group is packages sharing a current maintainer; several began publishing within seconds of one another, so the groups are not counts of victims, infections or generations", and add the same-second count to the record as a derived measurement (post hoc).

3. **for-driver.md's proposed lines are stale (written for 0.1).** "Stayed mostly inside one account's 316 packages" and "the AntV wave was mainly one account" undo Correction 3, which attributes the one-account reading to Snyk; "interim, unreviewed" predates R-0057; the 15-hour and 4-hour spans are given without saying they rest on the post hoc view (Correction 4). The investigation page already carries a corrected line. Fix: regenerate the programme.md and schedule text from 0.2, using the investigation page's wording for AntV and the post hoc label.

4. **"We dated thirteen waves" overstates.** Passage: opening. Registry times exist for nine at most; W03, W04, W05 and W09 have none; W08 joins only post hoc and W10 by one record that the Answer says is not identified. "Two more by date" in the public lines hides that one of the two (Miasma) is post hoc. Fix: "We tried to date thirteen named waves; nine have registry times, one of them only under a reading chosen after the counts."

No text re-identifies anyone: maintainers are salted hashes and packages are named only where sources name them. The outward lead (exfiltration repositories) would, by its nature, enumerate victims' GitHub accounts while collecting; if taken, its brief should keep only dated counts and discard account names when collecting.

### Readability suggestions

The opening runs to one 120-word sentence; split off the "upper bound" caveat into its own sentence. Answer 2's ChainDrop bullet (the 444 and 11 coincidence) would read better as "OSV's counts equal StepSecurity's; the package lists were not compared." StepSecurity publishes its full list, so comparing them is cheap and would settle it.

### Next-step recommendation

Read 2 as written measures how OSV's records change and whether the post hoc view holds. It cannot tell a chain of worm hops from one run or one operator's token pool, so on its own it adds little understanding: the main waves are months old and their counts are unlikely to move. Keep it, since it is cheap, but before it commit a dated amendment, labelled as thought of after the counts, that (a) takes the repair (vendors' package lists as a second route for W04, W05 and W10, plus a list-to-list comparison for ChainDrop), and (b) adds two analyses of the retained data that bear directly on the explanation: how many later groups began within 60 seconds of an earlier group, and whether the group counts survive clustering by scope or with widely shared maintainer accounts dropped. Together these put a lower ceiling on how many groups could be separate steps. Until then the public lines should make no claim that implies hops.
