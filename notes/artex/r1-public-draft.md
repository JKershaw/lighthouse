title: ARTEX round 1, proposed public surfaces
kind: working draft for review (not yet on any public page)
date: 2026-11-17

# ARTEX round 1, proposed public surfaces

**In short.** Round 1 of the ARTEX study ends in a reviewed record, not an article: the answer so far is inconclusive, and a piece would mostly restate one company's report. These are the exact words proposed for each public surface once the reviews clear. Nothing here is on the site yet.

## 1. Study page opening (the record's In short, which the site shows first)

We asked whether public reports can show that people running ARTEX, an open-source AI hacking tool, used stolen AI keys to pay for the computing that powered their hunt for more keys. In the six reports we could read on 17 November, only Amazon describes that loop for ARTEX, and every step of it rests on the attackers' own agent records, captured by Amazon's decoy sensors; Amazon says it can't verify the outcomes those records report. The other ARTEX reports neither confirm nor contradict it, and a report on a different operation describes a similar loop, also mostly from the agent's own records. For now the answer is inconclusive: in the reports we've read, people directed the agents' hunt for credentials and the attackers' own records describe the loop, but nothing outside those records yet shows it worked.

## 2. Investigation page (investigations/ai-cost-and-spread.md)

**In short, last two sentences, replacing "there is no reviewed finding yet, and nothing below is evidence of AI activity sustaining or spreading itself":**

There is no reviewed finding yet. One company reports AI agents whose own records describe stolen AI keys paying for the hunt for more; that is its account, resting on records whose outcomes it says it can't verify, and nothing we've read confirms it.

**Replacing the "New work, commissioned 17 November 2026" paragraph:**

**Reviewed interim record, 17 November 2026. ARTEX and the reported credential loop.** Amazon reported on 13 November that AI agents' own records, captured by its decoy sensors and attributed by Amazon to ARTEX, an open-source AI hacking tool, with moderate confidence, describe stolen AI keys paying for the computing that powered the hunt for more keys. Amazon says it can't verify the outcomes those records report. In the other reports we kept on 17 November (the FBI's advisory, Microsoft's and Censys's reports, and a security firm's summary), nothing confirms or contradicts that loop for ARTEX, and a September account of a similar loop in another operation also rests mostly on the agent's own records. In the reports we've read, people directed the agents' hunt for credentials and the attackers' own records describe the loop; nothing outside those records yet shows it worked. Check Point's report on ARTEX operators couldn't be read on the day. Next, a targeted search for the missing reports that could test each step, and dated re-reads to 1 December. [Record](../studies/LH055/LH055.md), [commissioning](../notes/artex/commissioning.md).

**Replacing "The strands stay apart, and nothing below is evidence of AI activity sustaining or spreading itself.":**

The strands stay apart. Apart from the reported ARTEX loop above, which rests on the agents' own records, nothing below describes AI activity sustaining or spreading itself.

**Replacing "No report read so far describes AI activity sustaining itself outside a test. If one does, it is recorded as its source's claim, with what it rests on.":**

One report read so far, Amazon's of 13 November 2026, describes AI activity sustaining itself outside a test: attackers' agents whose own records say stolen AI keys paid for further key hunting. It is recorded as Amazon's claim, resting on agent records whose outcomes Amazon says it can't verify, and is followed in [the ARTEX study](../studies/LH055/LH055.md). No report read so far describes AI activity spreading itself outside a test.

## 3. programme.md, under "Commissioned, 17 November 2026: ARTEX and the evidence for a sustaining loop"

Round 1, reviewed interim record (17 November): only Amazon's report describes the credential-to-compute loop for ARTEX, and every step rests on the agents' own records, whose outcomes Amazon says it can't verify; the FBI's, Microsoft's and Censys's reports neither confirm nor contradict it, and Check Point's was unread on the day. Inconclusive, not negative. Round 2 searches for the reports that could test each step (Microsoft's of 5 November, CrowdStrike's, a code reading of the framework, and any victim-side or provider-side account).

## 4. Front page, This week (site/this-week.md)

- 2026-11-17 | lighthouse | Did stolen AI keys pay for the hunt for more? Amazon says attackers' AI agents recorded exactly that loop, but the records are the agents' own and Amazon says it can't verify what they claim. Nothing else we read confirms or contradicts it yet. [Our first look](studies/LH055/LH055.md)

## 5. Front page, "And the big question?" (site/learned.md)

Unchanged. It says no report we've read describes AI agents spreading themselves outside a test; Amazon's report describes a self-sustaining operation, not one spreading itself, so the sentence stays true. Changing it would also need the block's own review.
