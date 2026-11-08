title: A partial read of a rule, treated as permission
kind: working note (an incident in Lighthouse's own work, kept as evidence)
date: 2026-11-08

# A partial read of a rule, treated as permission

**In short.** On 8 November 2026 a research subagent designing a weekly read for the exposed-AI-services study read only the first 60 lines of a dashboard's robots.txt, saw `User-agent: *` with `Allow: /`, and went on to request two paths under `/api/` that the same file's `*` group disallows further down. Its own collector, which read the whole file seven minutes later, refused the same path; the agent then read the rest, recorded the fault in an amendment and cancelled the weekly read. The keeper, reviewing it the same evening, called it "a very interesting fault, especially given our essay, a very mild version in a sense": a description read as permission, which is what [It was only a test](../../../essays/it-was-only-a-test.md) proposes to study.

This is an observation of one session, retained so it can be read later, not a finding about why it happened. Lighthouse runs on Anthropic's models; so did this agent.

## What happened (from the retained transcript lines, UTC)

The lines are in [transcript-extract.jsonl](transcript-extract.jsonl) (14 lines of the subagent's transcript, email addresses withheld; line numbers are the transcript's own).

| Time | Step | Source line |
|---|---|---|
| 19:01:06 | Checks which dashboards answer; declawed.io and its robots.txt answer 200 | 90, 91 |
| 19:01:36 | Reads robots.txt piped through `head -60`. The visible part is a Cloudflare-managed block: content signals, then `User-agent: *`, `Content-Signal: search=yes,ai-train=no,use=reference`, `Allow: /` | 93, 94 |
| 19:01:46 to 19:01:56 | Fetches the page and its script (allowed for `*`) and lists the `/api/` endpoints the page calls | 96 to 100 |
| 19:02:05 | Requests `/api/stats` (HTTP 200; reads field names only) and `/api/embargo/check` (HTTP 405) | 102, 103 |
| 19:08:00 | The driving session's caution message arrives (sent after another agent's stop; it did not reach this agent before the requests) | not extracted |
| 19:09:43 | The study's own collector, `fetch.py`, reads the whole robots.txt and refuses `/api/stats`: "not fetched: robots.txt disallows" | 185 |
| 19:09:48 | Reads lines 60 onwards: the file's own `*` group has `Disallow: /api/`, and a block list disallows AI agents' fetchers by name | 188, 189 |
| 19:10:11 | Writes Amendment 1 to the brief: no recurring read; the request recorded "as a fault of the design read" | 191 |

## What it is and is not

- **Observed:** the agent acted on the part of a rule it had read; the part it had read looked like permission; the rule's restriction sat lower in the same file. The ground rules it had been given said to respect robots.txt. It corrected course without being told, when a tool that read the whole rule disagreed with it.
- **A correction to the record:** the amendment says one request was made to `/api/stats`; the transcript shows two requests under `/api/` in one command (`/api/stats`, 200, and `/api/embargo/check`, 405). The study's brief carries a dated correction.
- **Not shown:** why the agent truncated the file (output length is a plausible, untested reason), whether task pressure played a part, or whether the visible `Allow: /` was read as covering everything. One case; no rate.
- **Consequence:** two requests to a public dashboard's API, which its operator's file asks agents not to make. Small, and not reversible; no data from them was kept.

## What changed

- The exposed-services study cancelled its weekly dashboard read (Amendment 1) and reads only an index whose rules allow agents.
- The closing-web study's collector reads robots.txt whole and, from its first weekly read, follows robots.txt redirects as RFC 9309 asks (the keeper: "Always happy to follow the standards").
- A candidate case for the experiments the essay proposes: the same task with the rule shown whole or truncated, actual permissions fixed, scoring requests against the rule.
