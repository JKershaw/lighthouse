# CLAUDE.md

Read AGENTS.md; it is the whole procedure. Notes for a Claude Code session:

- The Agent launcher's `model` parameter takes `opus`, `sonnet` and `fable`; `opus` resolved to Opus 5.5 on 26 September 2026. Subagents inherit this session's effort setting. Tell each subagent that it must not read keys from the environment and that it keeps searches out of `harbour/.session/`.
- What a subagent spent is in its transcript, not the launcher's token figure, which is its final context size. `harbour/hb tokens --latest` prices the newest subagent transcript from `harbour/prices.json`, and `harbour/hb drivercost --since <time>` prices this session's own; neither needs Harbour running.
- Commit as Claude (`-c user.name=Claude -c user.email=noreply@anthropic.com`) with the trailers the harness gives. Work on the branch the session names. A drive ends by fast-forwarding main from that branch, because the site at https://lighthouse.harbour.cat rebuilds from main and the next session clones it.
- Harbour's token is `HARBOUR_TOKEN` in the environment, or `harbour/.session/hosted-token` after a bootstrap exchange; `hb` reads either. A task that uses Harbour names it. Without one, read and close the issues with the GitHub tools instead.
- `/drive` is one tick of the watch, as AGENTS.md describes a session.
