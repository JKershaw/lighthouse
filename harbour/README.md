# Harbour, optional

[Harbour](https://harbour.cat) ([source](https://github.com/JKershaw/LinearViewer)) is an open-source control plane for AI coding agents: it reads a backlog, grounds each ticket into a prompt, dispatches it to an agent and records what came back. Lighthouse can run its programme through a local Harbour and does not by default. It earns its keep when more than one agent works the programme at once, or when the loop itself is what a study observes, as LH000 did and LH001 will. Harbour is also Lighthouse's first calibration subject, and Lighthouse and Harbour share a keeper, which every study that relies on Harbour evidence says.

## What is here

- `hb`: boots a local Harbour with a file store under `.session/` (git-ignored), loads `north-star.md` and `tickets.json`, dispatches, takes, posts feedback, usage and host samples, closes tickets, exports and stops. Run it with no arguments for the subcommands.
- `usage.py` and `prices.json`: price a Claude Code transcript. `hb tokens --latest` runs it over the newest subagent transcript and `hb drivercost --since <time>` over the session's own; neither needs Harbour running, and neither writes a path or an id anywhere.
- `sample.py`: a host sampler that reads /proc. `instruments.md` describes it and the export, with what each detects and misses.
- `exports/`: what Harbour recorded in past sessions, one directory per export named by collection time, credentials redacted. `samples/`: host samples.
- `requests.md`: what Lighthouse has asked of Harbour, with Harbour's ticket numbers. Cite those; do not file again.
- `tickets.json` and `north-star.md`: the workspace as files, as last exported. The north star reads: "Lighthouse publishes one reproducible observation of a known workflow and an honest account of its limits."

## Running a tick through it

`hb up`, `hb load`, `hb next`. Then per ticket: `hb dispatch <ticket> <kind>`, `hb take`, hand the printed prompt to a subagent, and when it reports `hb feedback <id> "<what was done>"`, `hb usage <id> --latest`, `hb resources <id>`, then `hb done <id> "<message>"` or `hb failed <id> "<reason>"`; commit the deliverable and `hb close <ticket> "<message>"`. At the end `hb export`, `hb down`, commit. `hb status` at any time. `hb up` clones Harbour into `~/.cache/harbour-src` unless `HARBOUR_SRC` names a clone; `HARBOUR_AI=0` starts it without the OpenRouter key; `hb roadmap` and `hb next` each call a model through OpenRouter, so once a session is enough.

Things that bit. Never pipe `hb up` into another command: the boot hangs while the pipe stays open, so redirect its output to a file. Kill by an anchored pattern (`^node server.js`, `^bash harbour/hb up`), because an unanchored `pgrep -f` matches its own shell. Do not restart Harbour mid-session; the feature flags and the workspace cannot be re-entered. Subagents keep searches out of `.session/`, which holds tokens.

Facts about Harbour that matter here. The proxy, roadmap and next-run pages are per-session feature flags that `hb up` switches on, and token minting is refused until the proxy flag is on. Proxy-issued dispatches target `cli`, `web` or `dash`, and a second dispatch for the same issue and kind within five minutes is refused as a duplicate. `kind` must be one of research, plan, implementation, review, design, breakdown, look-into, triage, scoping, spike, context, retro, blocked or custom. A usage entry is a feedback entry with `"kind": "usage"` and a `[usage]` message carrying JSON (model, harness, effort, the token counts and costUsd); Harbour keeps a supplied costUsd as reported and prices an entry without one from its own rate card, which lacks Fable 5.1 and Opus 5.5. A taken item's stored status stays `taken`; the terminal status is derived from the last feedback message beginning `[done]`, `[failed]` or `[aborted]`. Harbour's own model calls use OpenRouter's `openai/gpt-5.4-mini`.

What a subagent spent is read from its transcript, not from the launcher, whose token figure is the subagent's final context size. Cache reads dominate, and every subagent writes about 45,000 tokens of harness context before it starts. notes/Q-0002-model-choices.md has the measurements and the reasoning behind the model choice in AGENTS.md.
