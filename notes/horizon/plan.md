title: The horizon sweep
kind: working plan
date: 2026-11-07

# The horizon sweep

**Set 7 November 2026, at the keeper's request**, so that Lighthouse widens and deepens what it watches without a person acting as its clock. The sweep is discovery: it finds leads and writes proposals; it measures nothing and no claim is made from it. What it proposes goes to [proposals.md](../../proposals.md), and only a gate, the throttle and the keeper turn a proposal into work.

## When

Twice a week, on Tuesdays and Fridays, as rows `horizon-<date>` in schedule/due.csv, prefilled at least eight weeks ahead. The first is 7 November 2026.

## Each sweep

1. **Read the keeper first.** proposals.md's "From the keeper" and every `Keeper, <date>:` line added since the last sweep. Act on them: an agreed proposal gets its brief and rows (step 6), a declined one moves to the end with the keeper's reason, a direction becomes a proposal or steers this sweep's searches.
2. **Look inward.** What changed since the last sweep file: the Next sections of records, checkpoints that flagged something, review notes' open questions, programme.md's Next, and rows marked missed, blocked or keeper. Each open thread not already in proposals.md or the schedule is a candidate.
3. **Look outward.** A subagent (Sonnet, or as the harness allows) runs the standing searches below in the session's web-search tool, standard mode, one search each, and writes the ranked results as returned. It lists the URLs new since every earlier sweep file in this directory and opens at most eight of them, the highest-ranked that make a claim of fact, read directly; for each it records the URL, UTC read time, status, the page's own date and the claim in a sentence with a short quotation, classed as **reported by** the page, never as an observation. It also reads CISA's catalogue of known exploited vulnerabilities (its JSON feed) for entries added since the last sweep. Tell it not to read keys from the environment, to keep searches out of harbour/.session/, and not to commit.
4. **Write the sweep file**, notes/horizon/`<UTC label>`.md: the inward threads, the searches and results, the new URLs, the pages opened, and the candidates drawn from them.
5. **Propose.** At most five new proposals a sweep, in proposals.md's form, each citing what was read with its date. A proposal is **urgent** only when its first observations are lost if nobody looks soon (a fresh advisory, a score's daily history, a page likely to change), and it states that window. Prefer what fits the charter's question and an active investigation; say plainly when it does neither.
6. **Gate.** A fresh agent (Opus 5.5 or stronger) that wrote none of the proposals reads each new one with the charter, AGENTS.md's rules and the throttle, and gives it a lane with a sentence of reason: started, waiting for the keeper, backlog or declined. The run then starts what was put in the started lane, within the throttle: a brief fixed before outcomes are read, its rows in schedule/due.csv, and for an urgent watch an end 14 days after its first read. Without a fresh agent, the run may still start an urgent watch, since waiting loses it, and leaves everything else in the backlog with "not gated".
7. **Re-rank and summarise.** Re-rank the backlog by the programme's criteria (scientific value, decision relevance, evidence access, tractability, cost), moving anything untouched for twelve weeks to parked. Rewrite "For the next review": what started since the keeper last reviewed, what waits for them, the top five of the backlog with a recommendation each, and the spend since the last review.

## Standing searches

Revisable by any sweep with a dated note here; a sweep is discovery, so the list is not frozen, but every change is written down.

1. `AI agent incident internet infrastructure`
2. `autonomous AI agents web traffic bots share`
3. `vulnerability discovered by AI model exploit`
4. `software supply chain attack package registry`
5. `exploited in the wild widely used open source library`
6. `major internet outage root cause`
7. `self-propagating malware worm`
8. `AI crawler robots.txt blocking study`
9. `Model Context Protocol security vulnerability`
10. `internet measurement research new dataset`

## Limits

One search tool, in English, on one day: absence means nothing, and media repeat each other, so a claim reported by many outlets is one claim. The sweep's choice of what to open is a judgement and is recorded as one. A proposal is an idea with its sources, not a finding; nothing from a sweep reaches a piece except through a study and its reviews.
