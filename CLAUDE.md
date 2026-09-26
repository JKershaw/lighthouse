# CLAUDE.md

Procedure for driving Lighthouse from a Claude Code session. The house rules for any agent are in AGENTS.md; read it first. Verified in a Claude Code cloud session on 25 September 2026.

## The shape of a session

A session is a tick, not a daemon. Nothing in the container survives it, and the repository is public, so Harbour's store and its tokens are never committed. The repository holds the workspace as files; each session rehydrates a fresh local Harbour from them and exports what Harbour recorded before it ends.

1. `harbour/hb up` boots Harbour with its file store under `harbour/.session/` (git-ignored), creates the workspace, switches on the proxy, roadmap and next-run features, and mints a dispatch token and a readWrite proxy token into the same directory.
2. `harbour/hb load` files every ticket in `harbour/tickets.json` and sets the north star from `harbour/north-star.md`.
3. `harbour/hb roadmap` and `harbour/hb next` ask Harbour for a roadmap report and a suggested next run. Both call an LLM through OpenRouter with the environment's key, so keep them to once per session unless the backlog has changed. The roadmap route streams its layers as server-sent events; `hb roadmap` assembles them, saves the report to Harbour as the UI would, and prints the digest and each ticket's bearing against the north star. `hb roadmap --from <stream file>` saves a report from a stream already captured without a new model call.
4. `harbour/hb dispatch <ticket>` queues a ticket. `harbour/hb take` claims the next queued item and prints its prompt.
5. Hand the taken item to a subagent, as below. When it reports, post the result: `hb feedback <id> "<what was done>"`, `hb usage <id> '<json>'` with the launcher's token figures, `hb resources <id>` for a host sample, then `hb done <id> "<message>"` or `hb failed <id> "<reason>"`. Commit the deliverable, then `hb close <ticket> "<message naming the commit>"` marks the ticket done in Harbour with a comment; Harbour does not close a ticket on its own when a dispatch ends.
6. `harbour/hb export` writes what Harbour recorded into `harbour/exports/<collection time>/` and carries ticket statuses back into `tickets.json`. `harbour/hb down` stops the server. Commit and push.

`HARBOUR_SRC` names an existing clone to reuse; otherwise `hb up` clones Harbour into `~/.cache/harbour-src` and installs it, about a minute. `HARBOUR_AI=0` starts Harbour without the OpenRouter key. `hb status` shows the server, the issues and the queue at any time. `hb up` stops any Harbour already running on the port before it starts; do not restart Harbour in the middle of a session, because the human session and its feature flags cannot be re-entered and the workspace would have to be reloaded.

## Subagents as consumers

Spawn one subagent per taken item. Give it the item's prompt, the repository path, AGENTS.md, a scratch directory, and two rules: it must not read keys from the environment, and it must not post to Harbour itself. The driver posts the feedback, because only the driver can see the subagent's token usage.

Model choice: Haiku for chores such as polling, running commands and posting results; Sonnet for analysis and writing; Opus or Fable for review. The Agent launcher's `model` parameter takes `haiku`, `sonnet`, `opus` or `fable`. A Fable subagent that took one trivial dispatch used about 71,000 tokens over 13 tool calls in four and a half minutes.

## What persists and what does not

- Persisted, in git: `tickets.json` with statuses, `north-star.md`, `exports/`, and every deliverable a task commits.
- Not persisted: Harbour's store, sessions, tokens, and the clone. Each boot creates a new workspace, so Harbour-side history lives on only through the exports, which redact any credential before writing.
- The export is an observation with a collection time, as LH F02 asks. Its manifest records the Harbour commit it was taken from.

## Harbour facts that matter here

- The proxy, roadmap and next-run pages are per-session feature flags; `hb up` switches them on, and token minting is refused until the proxy flag is on.
- Proxy-issued dispatches may target `cli`, `web` or `dash` only. A second dispatch for the same issue and kind within five minutes is refused as a duplicate.
- `kind` must be a real template key: `research`, `plan`, `implementation`, `review`, `design`, `breakdown`, `look-into`, `triage`, `scoping`, `spike`, `context`, `retro`, `blocked`, or `custom`.
- A usage entry is a feedback entry with `"kind": "usage"` and a `[usage]` message carrying JSON: `model`, `harness`, `effort`, `inputTokens`, `outputTokens`, `cacheReadInputTokens`, `cacheCreationInputTokens`, `costUsd`. The marker in the message alone is not enough. A `resources` entry carries `loadAvg1`, `cpuCount`, `hostMemTotalBytes`, `hostMemAvailableBytes` and others; Harbour parses it and nothing produced it before `hb resources`.
- A taken item's stored status stays `taken`; the terminal status is derived from the last feedback message beginning `[done]`, `[failed]` or `[aborted]`.
- Harbour's own LLM calls use OpenRouter's `openai/gpt-5.4-mini` by default.

## Requests to Harbour

Filed and tracked in Harbour's own backlog under epic LIN-3057. The list, the ticket numbers and the two shared field lists are in `harbour/requests.md`. Cite those numbers; do not file again.
