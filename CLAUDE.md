# CLAUDE.md

Procedure for driving Lighthouse from a Claude Code session. The house rules for any agent are in AGENTS.md; read it first. Verified in a Claude Code cloud session on 25 September 2026.

## The shape of a session

A session is a tick, not a daemon. Nothing in the container survives it, and the repository is public, so Harbour's store and its tokens are never committed. The repository holds the workspace as files; each session rehydrates a fresh local Harbour from them and exports what Harbour recorded before it ends.

1. `harbour/hb up` boots Harbour with its file store under `harbour/.session/` (git-ignored), creates the workspace, switches on the proxy, roadmap and next-run features, and mints a dispatch token and a readWrite proxy token into the same directory.
2. `harbour/hb load` files every ticket in `harbour/tickets.json` and sets the north star from `harbour/north-star.md`.
3. `harbour/hb roadmap` and `harbour/hb next` ask Harbour for a roadmap report and a suggested next run. Both call an LLM through OpenRouter with the environment's key, so keep them to once per session unless the backlog has changed. The roadmap route streams its layers as server-sent events; `hb roadmap` assembles them, saves the report to Harbour as the UI would, and prints the digest and each ticket's bearing against the north star. `hb roadmap --from <stream file>` saves a report from a stream already captured without a new model call.
4. `harbour/hb dispatch <ticket>` queues a ticket. `harbour/hb take` claims the next queued item and prints its prompt.
5. Hand the taken item to a subagent, as below. When it reports, post the result: `hb feedback <id> "<what was done>"`, `hb usage <id> --latest` with the figures from the subagent's transcript, `hb resources <id>` for a host sample, then `hb done <id> "<message>"` or `hb failed <id> "<reason>"`. Commit the deliverable, then `hb close <ticket> "<message naming the commit>"` marks the ticket done in Harbour with a comment; Harbour does not close a ticket on its own when a dispatch ends.
6. `harbour/hb export` writes what Harbour recorded into `harbour/exports/<collection time>/` and carries ticket statuses back into `tickets.json`. `harbour/hb down` stops the server. Commit and push.

`HARBOUR_SRC` names an existing clone to reuse; otherwise `hb up` clones Harbour into `~/.cache/harbour-src` and installs it, about a minute. `HARBOUR_AI=0` starts Harbour without the OpenRouter key. `hb status` shows the server, the issues and the queue at any time. `hb up` stops any Harbour already running on the port before it starts; do not restart Harbour in the middle of a session, because the human session and its feature flags cannot be re-entered and the workspace would have to be reloaded. Never pipe `hb up` into another command: the boot hangs while the pipe stays open, so redirect its output to a file if it must be captured. When killing a process by pattern, anchor the pattern (`^node server.js`, `^bash harbour/hb up`), because an unanchored `pgrep -f` matches the shell running it.

## Subagents as consumers

Spawn one subagent per taken item. Give it the item's prompt, the repository path, AGENTS.md, a scratch directory, and two rules: it must not read keys from the environment, and it must not post to Harbour itself. Tell it to keep searches out of `harbour/.session/`, which holds dispatch records and tokens; one subagent's repository-wide grep matched files there. The driver posts the feedback, because only the driver can see the subagent's token usage.

Model choice (D-0002 in registers/decisions.md): Opus for research, essays and study write-ups; Fable for the release review; Sonnet for collection scripts, source checks and tabulation; Haiku only for a chore the driver cannot do with `hb`. The Agent launcher's `model` parameter takes `haiku`, `sonnet`, `opus` or `fable`; `opus` resolved to Opus 5.5 on 26 September 2026, and the model field of `hb tokens` says what actually ran. Every subagent writes about 45,000 tokens of harness context to cache before it starts, a floor of about $0.11 on Sonnet, $0.22 on Opus 5.5 and $0.56 on Fable 5.1 (derived from a probe that did nothing else). A subagent inherits the driver's effort setting, which was `max` in every run so far; the launcher exposes no effort control. `notes/Q-0002-model-choices.md` has the reasoning and its correction.

What a subagent spent is read from its transcript, not from the launcher. The launcher's token figure is the subagent's final context size. The transcript under `~/.claude/projects/` records every API call with its input, cache read and cache creation counts; `hb usage <id> --latest` sums the newest subagent transcript, prices it from `harbour/prices.json` and posts the usage entry, and `hb tokens --latest` prints the same without posting. Output tokens are estimated from the characters produced, because the transcript holds only the stream-start placeholder, and the entry says so. Cache reads dominate: the two Sonnet tasks run so far each read about seven million tokens from cache over about fifty calls and cost about two dollars, and the trivial Fable dispatch cost about $1.24, most of it cache writes. `hb drivercost --since <time>` does the same for the driver session's own transcript, so the ledger no longer has to enter the driver as unknown. Neither command writes a path or an id anywhere.

## The drive

`/drive [max dispatches] [max USD]` is the bounded form of "continue". The bounds, the stop list and the report format are in `.claude/skills/drive/SKILL.md`; only the keeper invokes it. A drive works Harbour's suggestions from the tickets already filed, one subagent at a time, stops at the count or the measured cost, and ends with an export, a commit and a report. It releases what passes review; it never files tickets or starts a routine.

## What persists and what does not

- Persisted, in git: `tickets.json` with statuses, `north-star.md`, `exports/`, and every deliverable a task commits.
- Not persisted: Harbour's store, sessions, tokens, and the clone. Each boot creates a new workspace, so Harbour-side history lives on only through the exports, which redact any credential before writing.
- The export is an observation with a collection time, as LH F02 asks. Its manifest records the Harbour commit it was taken from.

## Harbour facts that matter here

- The proxy, roadmap and next-run pages are per-session feature flags; `hb up` switches them on, and token minting is refused until the proxy flag is on.
- Proxy-issued dispatches may target `cli`, `web` or `dash` only. A second dispatch for the same issue and kind within five minutes is refused as a duplicate.
- `kind` must be a real template key: `research`, `plan`, `implementation`, `review`, `design`, `breakdown`, `look-into`, `triage`, `scoping`, `spike`, `context`, `retro`, `blocked`, or `custom`.
- A usage entry is a feedback entry with `"kind": "usage"` and a `[usage]` message carrying JSON: `model`, `harness`, `effort`, `inputTokens`, `outputTokens`, `cacheReadInputTokens`, `cacheCreationInputTokens`, `cacheCreation1hInputTokens`, `costUsd`. The marker in the message alone is not enough. Harbour keeps a supplied `costUsd` as reported; without one it prices the entry from its own rate card, which has rows for Sonnet 5, Opus 5, Haiku 4.5 and Fable 5 but not Fable 5.1 or Opus 5.5. The per-issue cost endpoint sums those entries and Harbour's own model calls attributed to the issue. A `resources` entry carries `loadAvg1`, `cpuCount`, `hostMemTotalBytes`, `hostMemAvailableBytes` and others; Harbour parses it and nothing produced it before `hb resources`.
- A taken item's stored status stays `taken`; the terminal status is derived from the last feedback message beginning `[done]`, `[failed]` or `[aborted]`.
- Harbour's own LLM calls use OpenRouter's `openai/gpt-5.4-mini` by default.

## Requests to Harbour

Filed and tracked in Harbour's own backlog under epic LIN-3057. The list, the ticket numbers and the two shared field lists are in `harbour/requests.md`. Cite those numbers; do not file again.
