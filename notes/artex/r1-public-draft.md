title: ARTEX round 1, proposed public surfaces
kind: working draft for review (not yet on any public page)
date: 2026-11-17

# ARTEX round 1, proposed public surfaces

**In short.** Round 1 of the ARTEX study ends in a reviewed record, not an article: the answer so far is inconclusive, and a piece would mostly restate one company's report. These are the exact words proposed for each public surface once the reviews clear. Nothing here is on the site yet.

## 1. Study page opening (the record's In short, which the site shows first)

We asked whether public reports can show that people running ARTEX, an open-source AI hacking tool, used stolen AI keys to pay for the computing that powered their hunt for more keys. In the six reports we could read on 17 November, only Amazon describes that loop for ARTEX. Amazon states it as its own finding, but every step of it rests on the attackers' own agent records, captured by Amazon's decoy sensors, and Amazon says it can't verify the outcomes those records report. The other ARTEX reports neither confirm nor contradict it; one, about a different campaign, says its attackers probably bought their AI computing from a reseller. For now the answer is inconclusive: the attackers' instructions, captured by Amazon's sensors, show people set the agents' goals and limits, and the agents' own records describe the loop, but nothing outside those records yet shows it worked.

## 2. Investigation page (investigations/ai-cost-and-spread.md)

**In short, last two sentences, replacing "there is no reviewed finding yet, and nothing below is evidence of AI activity sustaining or spreading itself":**

There is no reviewed finding yet. One company reports an attack operation, run by people through AI agents, whose agents' records describe stolen AI keys paying for the hunt for more; the company states it as its finding, but it rests on records whose outcomes it says it can't verify, and nothing we've read confirms it.

**Replacing the "New work, commissioned 17 November 2026" paragraph (two paragraphs):**

**Reviewed interim record, 17 November 2026. ARTEX and the reported credential loop.** Amazon reported on 13 November that attackers, using AI agents it attributes to ARTEX, an open-source AI hacking tool, with moderate confidence, ran a credential-theft operation in which stolen AI keys paid for the computing that powered the hunt for more keys. Amazon states this as its finding, but its evidence is the agents' own records, captured by its decoy sensors, and it says it can't verify the outcomes those records report. The attackers' instructions, captured the same way, show people set the agents' goals and limits.

In the other reports we kept on 17 November (the FBI's advisory, Microsoft's and Censys's reports, and a security firm's summary), nothing confirms or contradicts that loop for ARTEX. One of them relays a finding that a different ARTEX campaign probably bought its AI computing from a reseller, and a September account of a similar loop in another operation also rests mostly on the agent's own records. Check Point's report on ARTEX operators hit a rate limit on the day; the scheduled reads try again from 18 November. Next, a targeted search for evidence outside the agents' records, starting with how Amazon's own sensors came to be used, and dated re-reads to 1 December. [Record](../studies/LH055/LH055.md), [commissioning](../notes/artex/commissioning.md).

**Replacing "The strands stay apart, and nothing below is evidence of AI activity sustaining or spreading itself.":**

The strands stay apart, and nothing below is evidence of AI activity sustaining or spreading itself apart from the people running it.

**Replacing "No report read so far describes AI activity sustaining itself outside a test. If one does, it is recorded as its source's claim, with what it rests on.":**

No report read so far describes AI activity sustaining or spreading itself apart from the people running it. The nearest is Amazon's report of 13 November 2026 on an operation it calls self-sustaining, in which people set the agents' goals and limits and, by the agents' own records, stolen AI keys paid for further key hunting. That is an operation run by people, not AI acting apart from them; it is recorded as Amazon's claim, resting on records whose outcomes Amazon says it can't verify, and followed in [the ARTEX study](../studies/LH055/LH055.md).

## 3. programme.md, under "Commissioned, 17 November 2026: ARTEX and the evidence for a sustaining loop"

Round 1, reviewed interim record (17 November): only Amazon's report describes the credential-to-compute loop for ARTEX; Amazon states it as its finding, but every step rests on the agents' own records, whose outcomes Amazon says it can't verify, and the operation was directed by people. The FBI's, Microsoft's and Censys's reports neither confirm nor contradict it, one relayed finding has a different ARTEX campaign probably buying its computing, and Check Point's report was unread on the day. Inconclusive, not negative. Round 2 looks first for evidence outside the agents' records for Amazon's campaign (Amazon on how its decoys came to be used, Check Point through the panel reads, Microsoft's report of 5 November, whether later reports only repeat Amazon, and one search for a victim or provider account), coding new evidence by campaign as well as by step.

## 4. Front page, This week (site/this-week.md)

- 2026-11-17 | lighthouse | Did stolen AI keys pay for the hunt for more? Amazon reports that an attack operation run through AI agents worked that way, but its evidence is the agents' own records, and it says it can't verify what they claim. Nothing else we read confirms or contradicts it yet. [Our first look](studies/LH055/LH055.md)

## 5. Front page, "And the big question?" (site/learned.md)

Unchanged. It says no report we've read describes AI agents spreading themselves outside a test; Amazon's report describes a self-sustaining operation, not one spreading itself, so the sentence stays true. Changing it would also need the block's own review.
