# CLAUDE.md

Working notes for agents in the Lighthouse repository. Read the README first; it indexes the founding documents. This file records how the practice is run from a Claude Code session, as verified on 25 September 2026.

## What this repository is

Lighthouse is an observatory for the computational world: a standing watch, kept largely by agents, on how information flows through software and AI and what that activity leaves behind. The founding documents, LH F01 to F06, define the practice. Harbour (https://harbour.cat, source at https://github.com/JKershaw/LinearViewer) is the control plane that coordinates Lighthouse's tasks and is also its first calibration subject.

## House rules for any agent working here

- British English. No em dashes or en dashes in prose; use commas, colons or full stops. Hyphens inside identifiers, file names and command output are data, not punctuation.
- Studies use the plain names: activity, residue, propagation, observation, instrument. Images such as the coral, the ripple, the afterglow, the nearest star and the standard candle belong to essays and the charter, and arrive with their literal meaning the first time they are used.
- Label a statement as observation, derived measurement, interpretation or scenario wherever a reader could confuse them.
- Leave unfillable fields blank and say what could not be filled. Never invent a timing, a count or a source.
- Study write-ups use the skeleton in LH F05: header, Answer, Findings, Method, Limits, Next, Corrections.
- Agents do not publish, do not spend beyond the stated budget, and do not change Harbour. A person reads and releases.
- Tables keep the same number of columns in every row. Identifiers: LHnnn for studies, I-nnnn for instruments, Q-nnnn for questions, D-nnnn for decisions, C-nnnn for claims, L-nnnn for ledger entries.
- Commit with a clear message and never rewrite history on a shared branch.

## Running Harbour in a Claude Code cloud session

Verified in this environment with Node 22, no MongoDB and no Linear account.

1. Clone and install outside this repository; the session scratchpad is fine.

```
git clone --depth 1 https://github.com/JKershaw/LinearViewer.git harbour
cd harbour && npm install --no-audit --no-fund
```

2. Configure and start. Two variables are enough. `HARBOUR_DATA_DIR` points the file store at a directory of your choice; unset, it is `./data` inside the clone. Do not pass the OpenRouter key unless the AI features are wanted, because they spend money.

```
printf 'SESSION_SECRET=<random string>\nPORT=3123\n' > .env
env -u OPENROUTER_API_KEY nohup node server.js > harbour.log 2>&1 &
curl -sS --retry 30 --retry-delay 1 --retry-connrefused -o /dev/null -w "%{http_code}\n" http://localhost:3123/
```

Boot warnings about missing Linear OAuth variables are expected. The web UI is not reachable from outside the container, so everything below goes through the HTTP API with curl.

3. Create a local workspace. No login is needed. The redirect names the workspace's `urlKey`, which is also its partition in the store. Keep the cookie jar: it is the human session.

```
J=cookies.txt
curl -sS -c $J -b $J -o /dev/null -w "%{redirect_url}\n" -X POST -d "name=Lighthouse" http://localhost:3123/workspace/new
```

The workspace is seeded with two issues, LOCAL-1 and LOCAL-2.

4. Mint a consumer token. It is shown once.

```
curl -sS -c $J -b $J -X POST -H "content-type: application/json" -d '{"label":"lighthouse-consumer"}' http://localhost:3123/workspace/<urlKey>/api/dispatch/tokens
```

5. Queue a task. `prompt` is required. Omit `issueId` for local issues, since the validator expects a provider id; `issueIdentifier` is enough. `kind` must be a real template key such as `research`. A second dispatch for the same issue and kind within five minutes is refused as a duplicate unless the body carries `"force": true`.

```
curl -sS -c $J -b $J -X POST -H "content-type: application/json" \
  -d '{"prompt":"...","promptName":"research","kind":"research","issueIdentifier":"LOCAL-2","target":"cli"}' \
  http://localhost:3123/workspace/<urlKey>/api/dispatch
```

6. Consume. The consumer API needs only the bearer token, no session.

```
GET  /api/dispatch/poll
POST /api/dispatch/take/<item id>
POST /api/dispatch/feedback/<item id>    {"message":"...","url":"...","urlLabel":"..."}
```

End every run with exactly one terminal marker at the start of a feedback message: `[done]`, `[failed]` or `[aborted]`. The stored status stays `taken`; the terminal status is derived from the marker. Report usage as a feedback message beginning `[usage]` followed by JSON with any of `model`, `harness`, `effort`, `inputTokens`, `outputTokens`, `cacheReadInputTokens`, `cacheCreationInputTokens` and `costUsd`. The last usage entry wins, and Harbour prices it on `GET /api/proxy/issues/<identifier>/cost`, which needs a proxy token. A `[resources]` entry with host figures (`loadAvg1`, `cpuCount`, `peakRssBytes`, `hostMemTotalBytes` and others) is parsed but nothing produces it yet; Lighthouse's host sampler could be the first producer.

7. What persists. The file store writes JSON under the data directory: `dispatch-history.json`, `dispatch-tokens.json`, `local-issues.json`, `sessions.json`, `accounts.json` and others. Sessions and the human cookie survived a server restart. `sessions.json` and the token files are secrets: if the data directory ever lives in a repository, keep them out of it or keep that repository private.

## A subagent as the consumer

A Claude Code subagent can take a dispatch. Verified with dispatch `75516e46` on 25 September 2026: taken 42 seconds after queueing, three feedback entries posted, an observation note written, queue empty afterwards. Spawn the agent with the server URL, the bearer token, the steps above, a directory it may write to, and the rule that it must not touch this repository or read keys from the environment. Ask it to report the item id, the fields it received, what it wrote and what failed.

Model choice: the consumer role needs none of Fable's judgement. Use Haiku for polling, taking, running commands and posting feedback. Use Sonnet when the task involves analysis or writing a study. Reserve Opus or Fable for review. The Agent launcher's `model` parameter takes `haiku`, `sonnet`, `opus` or `fable`. The Fable run above used about 71,000 tokens over 13 tool calls in four and a half minutes for a trivial task; a Haiku run should cost a small fraction of that. A subagent cannot see its own token usage from inside the task, so its usage entry names only the model and harness unless the launcher supplies the figures afterwards.

## Things learned that belong in Harbour requests

- No route was found to re-enter an existing local workspace from a fresh browser session. Headless use is unaffected, because tokens persist; the human view is not.
- The `[resources]` feedback kind has no producer.
- The two asks already in LH F06: a study marker beside the ticket markers, and a labelled read token so that Lighthouse's collection traffic is recognisable in the audit log.
