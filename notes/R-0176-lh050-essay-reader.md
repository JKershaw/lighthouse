# R-0176: reader-and-inference review of the physical-authority essay, stage one

- Kind: review
- Row: LH050-essay-reader-review
- Date: 2026-11-28
- Reviewer: Claude Opus 5.5 (claude-opus-5-5), under Claude Code
- Reviewed: essays/when-the-machine-works-as-intended.md, SHA-256 70012567c0e3f5921b3a83161ffb3fdd2ffc2a43146f05cd2b2452aa28ad5d25
- Repository HEAD: d555135b34e787387b5a99bceb9b12161014ee55
- Read for this stage: the essay file only.

## What a reader would believe, written before reading the record

**Argument.** AI can harm people not only by escaping control or failing, but by working exactly as its controllers intend. So the question to ask of an armed or policing robot is who answers for what it's allowed to do. The essay offers three kinds of harm (accidental, autonomous, institutional), says protecting a robot's operator isn't protecting the people it's used on, and floats, as a hypothesis, that cheaper physical autonomy could loosen the link between an institution's size and its power.

**What seems observed.** Trade press, relaying the company, reports Foundation designing its Phantom humanoid to carry weapons, sending two robots to Ukraine for logistics demonstrations, holding $24 million in US military research contracts, and a chief executive saying some decisions will be fully autonomous. The Financial Times story about Gaza couldn't be read. Singapore runs unarmed patrol robots at Changi. November's weapons conference agreed only to keep working towards an instrument, with no negotiating mandate or deadline found.

**What seems explained or caused.** Nothing is shown to cause anything. The loop between military money and commercial capability is offered as a possibility. The finding the reader carries away is that public sources say almost nothing about who controls force, which the essay says mostly reflects what it could read, labelled post hoc.

**Limits a reader would notice.** No armed robot is shown fielded or used; the company sources repeat one another; the key Gaza claim is unread; the study record and the conference reading aren't yet reviewed or released; the economics claim is untested and no study is scheduled for it. A reader might also take the opening airport scene and the Gaza framing as more grounded than they are, despite the labels.

## Stage two: against the evidence

Read for this stage: studies/LH050/ (LH050.md version 0.1, brief.md with its amendments, panel.csv, the checkpoint of 27 November, the retained bodies the essay quotes); notes/physical-authority/ (essay-revision-plan.md, essay-claims.md, essay-checks/2026-11-28/fetchlog.md); investigations/physical-authority.md; programme.md's Next. Every quotation in the essay was checked against the retained copies: all present, two differing only in an initial capital ([r0176_quote_check.py](../studies/LH050/review/r0176_quote_check.py), output in [r0176_quote_check.out](../studies/LH050/review/r0176_quote_check.out)). The claim table's account of what was kept, cut and attributed matches the essay.

### What the round establishes

What I said a reader would believe mostly holds. The quotations, dates and attributions are right. The Financial Times story is clearly the commissioning essay's account, unread (403 on 28 November; refused by robots.txt at the baseline). The airport scene is labelled a thought experiment. The Gaza paragraph in "Protecting the operator" is conditional and says outright that the argument doesn't rest on the report. The Changi and conference passages carry the record's limits: no weapon described, "autonomous patrol" is the police's phrase, "as orally amended", the elements not read, the comparison unreviewed. The economics and the three kinds of harm are labelled hypothesis and proposal. Two things don't hold. The essay's one reading about the world goes further than the record allows, and the page the essay sends readers to doesn't say what the essay says it does.

### Material claim problems

1. **The closing reading turns a gap caused by access into a claim about what's public.** Essay, "What we could find out": "the questions this essay cares most about, who decides on force and who answers for it, are the ones least visible in public." The record's Answer (LH050.md) says the missing control cells "cannot be read as public records being silent on control". 14 of the 45 cells are the two rows lost to failed reads, and in the readable rows no source shows a fielded weapon, so "a supported entry on force in practice was hardly possible there" (control 1 of 13 over the readable rows, studies/LH050/review/r0074_matrix_split.out). The brief also names this as its writer's expectation going in, "disclosed, not tested as a population-level claim". The essay does say "That gap mostly reflects what we could read" and labels the reading post hoc. But a reader comes away with "public records hide who controls force" as what the watch saw. The study reaches that conclusion neither after seeing the evidence nor from it. *Resolution:* rewrite it as what the sources we could read did and didn't say, and say that we expected this going in. Say that the study can't tell a public blind spot apart from the pages it could read or the unarmed and unfielded cases it was left with. Keep the "should say so" sentence.
2. **The essay says the investigation page shows where things stand, but the page doesn't.** Essay: "[the investigation's page] says where things stand", followed by the record's account. investigations/physical-authority.md still says the baseline "is unreviewed working material". It doesn't give the reviewed record's answer or the conference outcome, and it calls this essay "background ... not a released account" that needs checking. programme.md's Next for this investigation is just as stale. That breaks the consistency rule (programme.md, investigation page and current account say the same thing at the same certainty). *Resolution:* before release, update the investigation page's opening and the programme.md line with the record's answer and the conference outcome in the essay's careful terms ("as the posted final document records it", its limits), and change the essay's pointer to the essay itself. Or, failing that, change the essay's sentence so it doesn't send readers there for the current state.

### Readability

- "paid for in part, by those reports, by military research contracts" ("From the battlefield to the airport") reads as if the contracts fund the robot. The sources report $24 million in contracts "for feasibility testing". Something like "with US military research contracts, by those reports" is closer to the source.
- The opening of "A robot its maker is reported to want to arm" spends its first paragraph on a story nobody could read. Moving the readable trade reporting first, with the Financial Times paragraph after it, would put the evidence ahead of the gap.
- In "What would test this", "such as a report of a delivery" could suggest the panel watches for new reporting. It rereads four fixed articles for edits, so "an edit to one of those articles reporting a delivery..." is more exact.

### Next step

The essay's own list is honest about how weak its tests are: the panel "can't show" control, and nothing tests the main reading. In order:
1. Fix the two problems above before release.
2. Within the pilot's envelope, the cheapest decisive read is the endorsed elements (CCW/GGE.1/2026/3). It needs a dated amendment and would settle what "what governments agreed" covers, including whether human control appears there.
3. The only thing that tests the main reading is the record's own unfinished design question: one bound route to a readable first-party record of a fielded or tested armed ground robot. Nothing I read shows that amendment was made. It should go to proposals.md at the pilot checkpoint, not be left as "no study now looks for one".
4. The essay could also name the December read of Ukraine's ministry notices (Amendment 1), which is already scheduled. It's an official count of ground-robot missions that the record notes says nothing about armament, control or civilians. It bears on the "least visible" reading without proving it.

**Disclosure check:** the version clears the combined disclosure check (schedule/research-safety.md). It holds public reporting, official pages and treaty text, at the level a reader needs, with no operational detail.

## Resolution, by the driving session (28 November 2026)

1. The closing reading ("What all this suggests to us") is rewritten: it is now called a reading, not a finding, says we half expected it before looking, states only what the sources we could read did and didn't say, and says we can't tell a blind spot in public records from a limit on what we could reach. The matching "What would test this" bullet now reads "hard to see in public" instead of "the least visible part".
2. The investigation page and programme.md's Next line for this investigation are brought up to date in this round, before the recheck (record 0.1 as reviewed, its answer, and the conference outcome as the posted final document records it, unreviewed), so the essay's "says where things stand" holds.

Readability: suggestions 1 ("paid for in part" now "military research contracts to test whether it could do the work") and 3 (the panel rereads four fixed articles for edits and doesn't look for new reporting) taken; 2 (reordering the Foundation section) not taken, since the section already labels the FT story as the commissioning essay's account. Next step: the endorsed elements document and a bounded route to a record of a fielded armed robot are left to the pilot's checkpoint and proposals.md, as the record's Next already frames the second.
