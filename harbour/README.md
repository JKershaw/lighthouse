# Harbour

[Harbour](https://harbour.cat) ([source](https://github.com/JKershaw/LinearViewer)) is an open-source control plane for AI coding agents: it reads a backlog, grounds each ticket into a prompt, dispatches it to an agent and records what came back. Lighthouse's backlog is the repository's own issues, and a hosted Harbour workspace at harbour.cat reads and writes them. `hb` is Lighthouse's client for it. Harbour is also Lighthouse's first calibration subject, and Lighthouse and Harbour share a keeper, which every study that relies on Harbour evidence says.

## The backlog

One issue per study or question, its title beginning with the study's identifier where it has one (LH005, C-0001), the design or the reason it matters in the body, and the label `question` on a question no study has taken yet. The programme file is the narrative of what is answered and what is next; the issues are the queue. A session that finishes a study closes its issue with a comment naming the record and the commit.

```
hb status                                  the open stack and recent dispatches
hb issue '#1'                              one issue with its description and comments
hb add "<title>" <description file> [label]
hb comment '#1' "<body>"
hb record '#1' research completed "<summary>"   an agent status entry, the trace a session leaves when it does the work itself
hb close '#1' "<message>"                  comment, then mark done
hb export                                  the stack, dispatches, agent status, north star and per-issue cost into exports/<collection time>/
```

Identifiers on this workspace look like `#1`; quote them in a shell. The workspace's GitHub backing has no single-issue read, no issue listing outside the stack and search, no projects and no viewer, so `hb issue` reads the open stack and falls back to search, and `hb status` reads the stack's digest.

## The token

`hb` talks to the hosted workspace when it finds a token: `HARBOUR_TOKEN` in the environment, which is how a session on a new machine gets one, or `harbour/.session/hosted-token`, which a bootstrap exchange writes and git ignores. A bootstrap token handed to a session is single use and is exchanged once at `POST /api/proxy/token`; the working token it returns lives 48 hours, and an operator-minted standard token lives 90 days, so the environment should hold the latter. A task that uses Harbour names the token, which is how the credential rule in AGENTS.md is met. `hb export` redacts every token it knows before writing.

The north star is set by a person in Harbour's own pages, from the text in `north-star.md`; the proxy only reads it.

## Dispatch, and the local instance

`hb dispatch '#1' [kind]` queues an issue's description as a prompt for a dispatch consumer. The hosted workspace has no consumer polling it yet, so a session does the work itself and leaves its trace with `hb record` and `hb close`; when a consumer token exists, the same command feeds a runner. Dispatch kinds are research, plan, implementation, review, design, breakdown, look-into, triage, scoping, spike, context, retro, blocked or custom, and a second dispatch for the same issue and kind within five minutes is refused as a duplicate.

A study that observes the loop itself, as LH000 did and LH001 will, boots a local Harbour: `HARBOUR_MODE=local hb up` clones Harbour into `~/.cache/harbour-src` unless `HARBOUR_SRC` names a clone, starts it with a file store under `.session/`, creates a workspace, switches on its proxy, roadmap, next-run and dispatch features, mints its tokens and sets the north star. `hb add` then files what the study needs, and `hb dispatch`, `hb take`, `hb feedback`, `hb usage <id> --latest`, `hb resources <id>`, `hb done` or `hb failed`, `hb next`, `hb roadmap` and `hb down` work as they did on the first drives; `HARBOUR_AI=0` starts it without the OpenRouter key. Things that bit: never pipe `hb up` into another command, because the boot hangs while the pipe stays open, so redirect its output to a file; kill by an anchored pattern (`^node server.js`), because an unanchored `pgrep -f` matches its own shell; do not restart it mid-session, because the feature flags and the workspace cannot be re-entered. A usage entry is a feedback entry with `"kind": "usage"` and a `[usage]` JSON message; Harbour keeps a supplied costUsd as reported. A taken item's stored status stays `taken`; the terminal status is derived from the last `[done]`, `[failed]` or `[aborted]` message. Harbour's own model calls use OpenRouter's `openai/gpt-5.4-mini`.

## Spend

What a subagent spent is read from its transcript, not from the launcher, whose token figure is the subagent's final context size. `hb tokens --latest` prices the newest subagent transcript from `prices.json` with `usage.py`, `hb tokens --agent <id>` a named one, and `hb drivercost --since <time>` the session's own; none needs Harbour, and none writes a path or an id anywhere. Cache reads dominate, and every subagent writes about 45,000 tokens of harness context before it starts. `notes/Q-0002-model-choices.md` has the measurements.

## What else is here

- `sample.py`: a host sampler that reads /proc. `instruments.md` describes it and the export, with what each detects and misses.
- `exports/`: what Harbour recorded, one directory per export named by collection time, credentials redacted. `samples/`: host samples.
- `requests.md`: what Lighthouse has asked of Harbour, with Harbour's ticket numbers. Cite those; do not file again.
- `north-star.md`: the north star's text.
