# Requests to Harbour

Filed in Harbour's Linear workspace on 26 September 2026 under epic LIN-3057, "Lighthouse: agent-run Harbour", labelled `from:lighthouse`. Cite these numbers; do not file again. The priority order below is recorded on the epic: the first six are Medium, the rest Low. Several overlap Harbour's V1 work and may arrive as part of it.

| Request | Ticket | What it replaces here |
| --- | --- | --- |
| Headless init | LIN-3058 | The first third of `harbour/hb up` |
| One agent credential | LIN-3059 | The cookie jar and two tokens the script juggles |
| Workspace as files | LIN-3060 | `hb load` and most of `hb export` |
| CLI for agents | LIN-3061 | The rest of `harbour/hb` |
| Close on done | LIN-3062 | `hb close` |
| Usage ergonomics | LIN-3063 | The explicit kind field and the token totals left in feedback text |
| Feature flags at instance level | LIN-3064 | The four flag toggles in `hb up` |
| Re-enterable local workspaces | LIN-3065 | The rule against restarting Harbour mid-session |
| North star writable via the proxy | LIN-3066 | The session-only north star write in `hb load` |
| Roadmap generate-and-save verb | LIN-3067 | The stream assembly in `hb roadmap` |
| Local issue id fails the format check | LIN-3068 | The fallback in `hb dispatch` |
| Seeded welcome tasks in roadmap and next-run | LIN-3069 | Nothing yet; they show as work in the reports |
| Study marker | LIN-3070 | Nothing yet; see the field list below |
| Labelled read token | LIN-3071 | Nothing yet |
| Periodicals on a headless local workspace | LIN-3072 | Untested; research |

Requests that already had tickets, now carrying the label and this project's wording:

| Request | Ticket |
| --- | --- |
| Retention as configuration | LIN-2198 |
| Resources producer | LIN-1788, with LIN-1805 and LIN-1807 |
| Duplicate-guard retry path | LIN-2900 |

## Not yet filed

Found on 26 September 2026 while measuring spend from transcripts. To be filed under the same epic when convenient.

| Request | What it replaces here |
| --- | --- |
| Rate card rows for Fable 5.1 and Opus 5.5, with their cache-read exceptions (a fortieth and a twentieth of input on the caching page) | The `costUsd` that `hb usage` computes locally from `harbour/prices.json` |
| A workspace-level read of Harbour's own model spend through the proxy; the store can summarise it but no route an agent token can reach exposes it | Nothing yet; the export carries only the per-issue attribution |

Found on 26 September 2026 while moving the backlog to the hosted workspace, which is backed by this repository's issues. These are what would let Harbour start Lighthouse's sessions rather than only list its work, in the order they matter. To be searched against the backlog before filing, since several touch LIN-3061, LIN-3063 and LIN-3066.

| Request | What it replaces here |
| --- | --- |
| A consumer for cloud sessions: a dispatch whose target is a Claude Code session started on Anthropic's infrastructure, needing no runner on a machine of the keeper's; or, if simple-dispatcher's web target already does this, the documentation of how a workspace gets one | The person typing `/drive`, or a scheduled routine outside Harbour |
| Rulings an agent can raise through the proxy: a session that reaches a decision reserved for a person (a claim of present harm, a named compromised system, anything irreversible outside the repository) posts the question with its options and parks; today the proxy only lets an agent suggest answers to rulings that already exist | The session's report, and the person reading it in time |
| Usage on an agent status entry: let `POST /api/proxy/agent/status` carry the `[usage]` fields (model, harness, effort, token counts, costUsd) so that a self-driven session's spend joins cost per issue without a taken dispatch | The spend line in the commit message; `cost.json` in the export reads nothing for a self-driven issue |
| GitHub provider gaps: `GET /issues/{id}`, an issue list including closed issues, and label creation; today `issueDetail`, `issues`, `projects` and `viewer` answer `CAPABILITY_NOT_SUPPORTED`, so `hb issue` reads the open stack and search, and a closed issue cannot be read at all | The stack-and-search fallback in `hb issue`; nothing for closed issues |
| Periodicals declared from an issue: an issue carrying a cadence (the monthly source check, C-0001) that Harbour dispatches on schedule, rather than a server-side template registry | A session remembering the cadence, and the "stays open, comment per check" convention on the issue |

The ruling request in fields, so that it can be filed as one: `POST /api/proxy/rulings` with `{ "issueIdentifier", "question", "options": [{ "id", "label" }], "context", "effect": "record|dispatch" }`, returning the ruling's id; the ruling appears in the Observation Rulings tab like a runner-raised one; answering it, by a person only, records the answer and, when `effect` is `dispatch`, queues the issue's next step with the answer in the prompt. The session that raised it ends; it does not wait.

## Field list: study marker (LIN-3070)

A feedback marker beside `[ticket]` and `[usage]`, posted by the driver or by the agent that took the dispatch, linking the dispatch to the Lighthouse record it produced or used. Posted as a feedback entry with `"kind": "study"` and a message of the form `[study] { ...json... }`, so that the export can join a dispatch to a study and the ledger can attribute cost per study.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `study` | string | yes | The study identifier, LHnnn |
| `record` | string | yes | One of `brief`, `observation`, `instrument`, `claim`, `decision`, `release`, `note` |
| `path` | string | once committed | Repository path of the record |
| `commit` | string | once committed | Short commit hash the path is valid at |
| `instrument` | string | no | The instrument identifier, I-nnnn, when the record is a reading |
| `periodStart`, `periodEnd` | string | no | Observation period, ISO 8601 |
| `status` | string | no | One of `candidate`, `reviewed`, `published` |

Example: `[study] {"study":"LH000","record":"observation","path":"studies/LH000/observations.md","commit":"7c5344e","instrument":"I-0002"}`

Last entry wins per dispatch, as with usage. A dispatch that serves several studies posts one entry per study, and Lighthouse keeps every entry in its own export.

## Field list: resources producer (LIN-1788)

Harbour already parses a `resources` feedback entry field by field, numbers only, and nothing produced one before `harbour/hb resources`. The fields it parses today:

| Field | Meaning |
| --- | --- |
| `peakRssBytes` | Peak resident memory of the agent process |
| `hostMemAvailableBytes`, `hostMemTotalBytes`, `hostSwapUsedBytes` | Host memory |
| `oomKillDelta` | Out-of-memory kills since the previous sample |
| `loadAvg1` | One-minute load average |
| `cpuCount` | Logical CPUs |
| `activeSessionCount` | Agent sessions alive on the host |
| `cloneDiskBytes`, `cloneCount` | Disk used by repository clones, and their number |

Lighthouse posts four of these today: `loadAvg1`, `cpuCount`, `hostMemTotalBytes` and `hostMemAvailableBytes`. The fields it intends to add, all numeric so the current parser takes them without change:

| Field | Meaning |
| --- | --- |
| `sampledAtEpochSeconds` | When the sample was taken |
| `sampleIntervalSeconds` | The interval the sample covers |
| `busyCoreSeconds` | Sum over cores of utilisation multiplied by elapsed seconds since the take; the activity layer's starting unit in LH F02 |
| `processCount` | Processes on the host at the sample |
| `establishedTcpConnections` | Sockets in the established state, from `/proc/net/tcp` where `ss` is absent |
| `agentRssBytes` | Resident memory of the agent process at the sample |
| `requestsOut`, `bytesOut` | Outbound requests and bytes seen by the sampler, where a proxy is in the path |

One field Lighthouse wants that is not numeric: `requestsByDestination`, a map from host to request count. It needs a parser change, so Lighthouse keeps it in its own observation records until Harbour wants it. Harbour keeps the last entry per dispatch; Lighthouse keeps every sample in its export, and the driver posts the final one to Harbour.
