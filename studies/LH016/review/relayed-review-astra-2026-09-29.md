# A review of LH016 version 0.1, relayed by the keeper

**What this is:** a review of studies/LH016/LH016.md version 0.1 (commit d07fac0), written by Astra, a reviewer outside Lighthouse's workflow, and relayed by the keeper into the driving session on 29 September 2026, late evening, after LH016's release. It is kept verbatim as the session received it, including its first line and its typography, so that what LH016 version 0.2 says of Astra and of step K can be checked against it (notes/R-0024.md, should fix (b)).
**What is not known:** what Astra is, a person or an AI system, and on what model, is not stated in the report; the report speaks of what set its readings apart from the workflow's as "a difference in context, instructions, model and relationship to the project". Which of the readings the keeper relayed on 28 and 29 September were Astra's is not recorded either: the report says "much of that feedback", not which.
**What the session checked:** only that replay.sh passes, on version 0.1 and on version 0.2. The report's other statements are Astra's, as relayed.

---

From Astra: Worked for 1m 3s

This was a worthwhile inward round. It found actionable weaknesses, tested part of the review process, and kept its conclusions reasonably bounded. I’ve read LH016 at d07fac0 and run its replay; the tallies, coding comparison and two new finding checks reproduced.

The strongest lesson is that a correction is itself new, unreviewed writing. Eight of the recheck’s ten public-claim corrections concerned text written during the round in response to a review. That supports a practical change: whoever checks the original problem should also ensure the replacement text receives a fresh reading. It doesn’t justify indefinitely adding reviewers.

The historical replays were useful too. Fresh reader reviews found the central problems we had raised about download share versus speed, and Python compatibility versus actual version choice. They also missed other problems. That gives some evidence the review can reproduce useful criticism, while falling well short of a measured detection rate or proof that a particular model is best.

Two newly discovered issues deserve correction:

The apparent late uptake of six litellm releases was a shared one-day event. They crossed half on the same date and stayed below it on all subsequent observed days. Describing this simply as releases eventually reaching half suggests a progression the data do not show.

“Holds for the month” obscures continued growth. Shares rose between day two and day thirty for 339 of 355 releases. The predefined ten-point test can still pass; its plain-language description needs to communicate that tolerance rather than imply flatness.

There is one important correction I’d make to this self-study’s attribution. It treats “the keeper’s reading” as a human contribution with no model cost. Much of that feedback was analysis you relayed from me. The repository records the route by which feedback arrived, not necessarily who or what produced it.

I’d label that category external review relayed by the keeper, with the contributor recorded where known.

This matters directly to the research question: otherwise Lighthouse may infer a human-versus-agent distinction from what was actually a difference in context, instructions, model and relationship to the project. The study acknowledges that it lacks your original messages, so the appropriate result is limited attribution.

I also wouldn’t use its “cost per claim changed” figures to allocate work. Changes differ in importance, and later reviewers inherit what earlier ones already improved. The study recognises the ordering problem; those figures describe these rounds, rather than rank the reviewers.

My recommendation now: one bounded correction round, then outward work.

That round should resolve the two known published overstatements, update the synthesis that carries them, and correct the external-review attribution. The proposed review of older articles can be a finite backlog; it should not become a requirement to exhaust every possible criticism before researching again.

Then proceed to the CI workflow question. LH016 has supplied useful process lessons, but it has not yet answered our broader question about model selection and programme-level resource allocation—and we needn’t force it to. For now, it has improved the instruments Lighthouse uses to assess its own conclusions.
