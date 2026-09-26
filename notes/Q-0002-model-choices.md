title: Which model should take which kind of dispatched task?
kind: paper
version: 0.1
date: 2026-09-25
authors: Lighthouse autopilot (Claude Code subagent)
model: Sonnet 5 (claude-sonnet-5)
grounded_at: 466cb10
cites:
- https://claude.com/pricing, redirected from https://www.anthropic.com/pricing, read 2026-09-25
- https://platform.claude.com/docs/en/models/overview, redirected from https://docs.claude.com/en/docs/about-claude/models/overview, read 2026-09-25
- CLAUDE.md@466cb10:22

## Answer

For consumer chores the default is Haiku 4.5; for collection scripts, source checks, reading surveys, historical essays and study write-ups it is Sonnet 5; for review it is Opus 5.5, with Fable 5.1 in reserve. Haiku 4.5 already holds the chores role in CLAUDE.md's rule (observation, CLAUDE.md@466cb10:22). Sonnet 5 covers five of seven kinds because none is shown to need Opus or Fable tier reasoning by default (interpretation). Review keeps CLAUDE.md's escalation, following Anthropic's own guidance to start with the cheaper model (interpretation). Only one dispatch has ever been measured, a Fable 5.1 subagent on a trivial chore (observation, CLAUDE.md@466cb10:22, detailed under Findings); every other match below is interpretation, not measurement.

| Task kind | Recommended default | Fallback | Reason |
| --- | --- | --- | --- |
| Consumer chores (poll, take, run commands, post feedback) | Haiku 4.5 | Sonnet 5 | Cheapest and fastest; matches CLAUDE.md's rule |
| Collection scripts | Sonnet 5 | Haiku 4.5 | Code needs more judgement than a chore |
| Source checks | Sonnet 5 | Opus 5.5 | Escalate only if a source is contested |
| Reading surveys | Sonnet 5 | Haiku 4.5 | Breadth over depth for most surveys |
| Historical essays | Sonnet 5 | Opus 5.5 | Escalate for demanding synthesis |
| Study write-ups | Sonnet 5 | Opus 5.5 | Escalate if the evidence is contested |
| Review | Opus 5.5 | Fable 5.1 | CLAUDE.md's rule; start with the cheaper of the two |

## Findings

**Published pricing places the four models on one scale, ten times apart end to end.** Haiku 4.5 is $1 input / $5 output per million tokens, Sonnet 5 $2 / $10, Opus 5.5 $4 / $20, Fable 5.1 $10 / $50 (pricing page, read 2026-09-25); latency runs the same way, Haiku 4.5 fastest and Fable 5.1 slowest (models overview, read 2026-09-25).

**Anthropic's documentation says to start with the cheaper top-tier model and escalate only when it falls short.** It says to "start with Claude Opus 5.5 for most workloads" and use Fable 5.1 only "for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short" (models overview, read 2026-09-25).

**The one measured run was a chore, not a review, on the most expensive, slowest model.** CLAUDE.md records a Fable 5.1 subagent given a trivial chore (poll, take, sample the host, write a short note, post feedback) using about 71,000 tokens over 13 tool calls in four and a half minutes (CLAUDE.md@466cb10:22), the kind CLAUDE.md's own rule assigns to Haiku 4.5.

**Only a cost range can be derived from that run, not a single figure, since its tokens were not split into input and output.** At Fable 5.1's rates 71,000 tokens cost between about $0.71 (all input) and $3.55 (all output); derived measurement. At Haiku 4.5's rates the same count costs exactly one-tenth at either bound, since Haiku 4.5 is priced at exactly one-tenth of Fable 5.1 on both input and output. Which bound is closer is unknown.

**CLAUDE.md's rule already matches how Anthropic positions the models, and context window reinforces it.** Haiku 4.5 is "the fastest model with near-frontier intelligence" but has a 200,000 token window against 1,000,000 for the other three (models overview, read 2026-09-25); a reading survey or study write-up holding many documents at once can exceed that window before it exceeds its price.

## Method

Two Anthropic pages were fetched live on 2026-09-25 for pricing and capability description (both redirected once; see header for final URLs). A third page, claude.com/product/overview, gave only marketing copy and is not cited. CLAUDE.md's one recorded run is the only measured token and timing figure available (CLAUDE.md@466cb10:22); the cost range in Findings comes from multiplying its 71,000-token total by each model's published rate, since the input/output split was not recorded. "Fallback" means the model to move to when one instance of a kind is unusually demanding, not an outage substitute.

## Limits

Exactly one dispatch has ever been measured, and it ran on Fable 5.1, not on Haiku 4.5, Sonnet 5 or Opus 5.5. Every recommendation above, aside from what that single run cost and took, is interpretation drawn from published pricing and capability descriptions, not measurement. No task kind here has been run on more than one model, so relative cost, quality and speed on Lighthouse's actual workloads are unproven. Whether a Haiku 4.5 chore would use materially fewer tokens than the measured run, rather than the same tokens priced more cheaply, is unknown. Fable 5.1's reasoning quality against Opus 5.5 on a Lighthouse review is also unknown. Pricing and capability text can change after the date read here.

## Next

The measurement that would settle this: run the same chore-shaped task already measured once on each of Haiku 4.5, Sonnet 5, Opus 5.5 and Fable 5.1, recording input tokens, output tokens, cache read and creation tokens, wall time and tool call count through Harbour usage entries, not by estimate. A second sweep should repeat this for one collection-script task and one review task, the kinds furthest from the chore already measured.

## Corrections

2026-09-26. The 71,000 token figure in Findings and Method is the subagent's final context size, which is what the launcher reports, not what the run spent. The run's transcript records eleven API calls that read 538,203 tokens from cache, wrote 70,306 to it and produced about 4,500 output tokens (estimated from characters), which at the published rates cost about $1.24, most of it cache writes at $12.50 a million. The cost range of $0.71 to $3.55 derived from the wrong figure is withdrawn. The same method gives the two Sonnet 5 tasks run since about 6.6 and 6.9 million cache-read tokens over 45 and 48 calls, about $2.06 and $2.03 each (derived measurement). What this changes: a task's cost is its context size times its number of calls at the model's cache-read rate, plus what it writes. Sonnet 5 and Opus 5.5 publish the same cache-read rate, $0.20 a million, so a review on Opus 5.5 costs about the same to re-read as one on Sonnet 5 and twice as much to write and to produce (interpretation from the price page). The table stands. All three runs were at effort max, inherited from the driver; the launcher gives no effort control. Method: harbour/usage.py over the transcripts; prices from https://claude.com/pricing, read 2026-09-26.
