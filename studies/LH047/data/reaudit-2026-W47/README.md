# Re-audit of Lighthouse's own requests, 16 to 22 November 2026: checkpoint

**In short.** Unreviewed. We checked every request Lighthouse's committed logs record for the week of 16 to 22 November 2026, 1,649 requests to 353 hosts from 34 collectors and routes, against the rules this study fixed on 8 November and amended on 9 and 17 November. Under robots.txt, 2 requests broke the reading that obeys only Lighthouse's own name and 3 broke the stricter reading that adds Anthropic's names, which is also the keeper's rule of 8 November; with every rule counted, 53 requests failed under the first reading and 54 under the stricter ones, most for coming sooner than a site's requested delay or for going back to a page that had answered with a wall, and 159 couldn't be judged, mostly because the software identity sent isn't visible. Requests that no log recorded weren't seen at all: no session kept a transcript extract for the week, so that count is a floor, can't be compared with 8 November, and goes next to the record's update and its reviews.

Written 23 November 2026 (14:36 to 15:04 UTC by `date -u`) by a subagent of the Watch run (Claude Code, Claude Opus 5.5), for row LH047-reread. Not the record: version 0.2 of the record is row LH047-reread-record. Figures from `requests-judged.csv` as made by `replay.sh`.

## What was audited

- **Week:** ISO week 2026-W47, 16 November 00:00 UTC to 22 November 24:00 UTC (brief, Amendment 2).
- **Population commit:** `e74c302bb255f9d8c3ed7eee653f20a3f2dbf6ed` (2026-11-22T18:22:23Z), the last commit on main at or before 2026-11-22T23:59:59Z. Logs were read from its git objects, not the working copy. Main at the start of this work, `f5aed200cce7a4b7de1f3e312525a9f5bd683fde`, was searched the same way for logs committed later: the logs it changed (LH051, LH057, LH058) add only 23 November rows, so no request inside the week was committed after 22 November (`requests-later-only.csv`, empty).
- **Mechanical search, before any row was judged** (`code/find_logs.py`, output `candidates-raw.csv`): every file in the commit's tree, `.gz` decompressed, holding a UTC time inside the week (ISO forms, compact forms or Unix seconds) and a URL, or a week time and a file name containing "log", "fetch" or "request". 371 candidates. `code/classify.py` classes each as a request log or not, with its reason (`logs.csv`); its rules were written after seeing the candidates' paths and before judging any row. 70 entries are included: 69 logs and one file of requests hand-coded from prose notes (`handcoded.csv`, by `code/handcode.py`: the PHP media sweeps of 16 and 19 November and LH050's gate checks of 16 November, times "about" a minute).
- **Rows** (`code/normalise.py`, `requests.csv`): 1,837 rows with a time in the week. 1,649 are audited: 969 page or API requests, 372 robots.txt reads logged as rows, and 308 robots.txt reads counted from code. Counted apart: 75 requests the robots.txt gate refused (not sent), 75 web searches (a search provider's request, not ours to a site), and 38 duplicate gate-check rows in the 20 November Horizon log that one gate call served with a single robots.txt read.
- **Reads counted from code.** For each log, the collector file it names was read at the latest commit at or before the run (or its first committed version, flagged in `requests.csv`, where it was committed with or after its data). Where that version goes through `scripts/lh_fetch.py`'s gated `urlopen` or `check`, or `scripts/robots_gate.py`, one robots.txt read per host per run was added, timed at the run's first request to that host and marked "not logged (at or before)". Every gate in the repository sends a User-Agent carrying `Lighthouse-research`.

## The rules and the evidence

Section 5 as fixed, with Amendment 1 (R8's classes; R5 counted with and without robots.txt reads; reporting by request and by practice with each failing request's status; robots.txt copies in section 4's order) and Amendment 2. Reading A (R1, Lighthouse's own token), reading B (R2, Anthropic's seven tokens, by token) and the keeper's rule of 8 November (K8: `scripts/robots_rules.py` and `scripts/robots_tokens.json` as they stood at Amendment 2's commit `f4eb46a`, frozen in `code/frozen_f4eb46a/`, provider `anthropic` for every log, since the week's only Codex session collected nothing). At that commit the keeper's Anthropic tokens are the same seven as reading B's, so K8 and B give the same counts here; they differ in how a file naming one of them is read against `*`, and no request in the week falls in that gap.

**robots.txt at the time.** The shared gate records each robots.txt read's status and SHA-256 but keeps no copy, so most page requests were judged on a current re-read. Evidence used for the 969 page requests: a status other than 200 logged at the time by the same log, 148; a copy kept in the week by the same study (LH044, LH045), 66, or by another study, 97; a re-read of 23 November whose bytes match the hash logged at the time, 57; a re-read that differs from it, 5; a re-read with no hash from the time to compare, 596. The re-reads' verdicts are counted apart in every table in `tables.md`. A copy from another study is from the same week, not the same evening as on 8 November.

**The keeper's decision of 21 November** ([the decision](../../../../notes/keeper/2026-11-21-robots-intent.md)) came during the week, after Amendment 2 fixed the rules. It isn't part of this re-audit's protocol: no verdict uses it. Two context columns show what it would say. `K21_oneoff`: the week's two one-off reads (LH039's of 22 November, after the decision) are allowed under its one-off reading as well as under K8. `K21_keep`: of the 95 page requests after the decision's commit (2026-11-21T15:23:17Z) whose 2xx body is kept in the repository, all 95 may be kept under its keep rule where the file could be read (56 on a parsed file, 39 where robots.txt answered 4xx).

## Headline counts (unreviewed)

By request, of 1,649 audited (complies / does not comply / unknown):

| rule | complies | does not comply | unknown |
|---|---|---|---|
| R1, robots.txt, own token | 1,632 | 2 | 15 |
| R2, robots.txt, adding Anthropic's tokens | 1,631 | 3 | 15 |
| K8, the keeper's rule of 8 November | 1,631 | 3 | 15 |
| R4, usage preferences (15 applicable) | 15 | 0 | 0 |
| R5, Crawl-delay, robots.txt reads counted | 1,587 | 40 | 22 |
| R5, Crawl-delay, robots.txt reads not counted | 1,622 | 27 | 0 |
| R6, walls | 1,638 | 11 | 0 |
| R8, identification | 1,499 | 0 | 150 |
| Overall, reading A | 1,437 | 53 | 159 |
| Overall, reading B | 1,437 | 54 | 158 |
| Overall, keeper's rule of 8 November | 1,437 | 54 | 158 |

R7: 8 requests to Epoch comply (its terms are quoted in LH045's brief); the other 1,641 are "terms not read", which neither passes nor fails a request. With R5 counted without robots.txt reads, overall reading A would be 40.

By practice (a collector, reviewer or ad hoc route, named by its log), the failing requests under reading A, with the rule and the status each received:

- **Horizon scouts of 20 November** (`notes/horizon/2026-11-20T1214Z/requests.csv`): 19 under A, 20 under B and K8. R1: 2 requests to one page at theregister.com (the `*` group disallows it; one by the session's fetch tool, one by curl), on a re-read. R2 and K8 add one, the PDF at next.ink whose robots.txt disallows ClaudeBot, anthropic-ai and Claude-Web, on a re-read; the run's own summary already names both as breaches. R5: 17 (arxiv.org, Crawl-delay 15, judged on LH044's copy of 22 November: 14; washingtonsun.com, Crawl-delay 10, re-read: 2; one robots.txt read). No status is recorded in this log, so every one is "not recorded".
- **LH038's collector, 17 November:** 14 requests to access.redhat.com 0 to 1 s apart, against `Crawl-delay: 10`; the re-read is byte-identical to the file the gate read that day. All 2xx.
- **LH044's collector, 22 November:** 9 under R5, each the probe that followed LH044's own robots.txt read 1 to 3 s earlier against Crawl-delays of 5 to 60 (none when robots.txt reads aren't counted); on LH044's own copies. 7 2xx, one 3xx, one 404.
- **LH055's collector:** 5 under R6, the daily reads of 18 to 22 November of Check Point's report after it answered 429 on 17 November. All 2xx.
- **Microsoft report watch** (`notes/microsoft-outage-report/readings/`): 4 under R6, the daily requests of 17 to 20 November to a university help-centre page that answered 403 with a "Just a moment..." challenge from 16 November. All 403.
- **LH053's collector:** 2 under R6, requests on 22 November to an npm downloads URL that answered 429 on 21 November. Both 2xx.

All 11 R6 failures are requests on a later day by a recurring daily read, not retries within a run; the rule as fixed doesn't separate the two (a description, made after seeing the rows). No request in the week answered a challenge or switched User-Agent after a wall. Every collector's code was read for its User-Agent: none claims to be a browser or uses an unattributed name.

Unknown, overall A (159): R8 unknown for 150 requests whose User-Agent isn't visible (117 Horizon fetch-tool and curl calls, 27 Microsoft watch reads, 4 PHP sweep fetch-tool reads, LH056's readiness probe, LH058's pre-brief read); R1 unknown for 15 (12 GitHub requests answered by this container's own policy, 2 where sonicwall's robots.txt now answers with a challenge page, 1 where rustsec.org's robots.txt now answers 503); R5 unknown for 22 where the previous request was a robots.txt read whose time isn't logged.

## What could not be seen

- **Unlogged requests.** No session in the week committed a transcript extract made by `scripts/transcript_requests.py`, and no week transcript survives in this container, so no unlogged request was seen: the unlogged count is a floor of zero, and the one-off floor isn't comparable with 8 November's 51, as row LH047-reread's note says. Sessions without an extract (`schedule/runs.csv`): the runs started 2026-11-16T1417Z, 17T1414Z, 17T2029Z, 18T1300Z, 18T1414Z, 18T1512Z, 18T1810Z, 19T1414Z, 19T1513Z, 19T1811Z, 20T1214Z, 20T1413Z, 20T1513Z, 20T1811Z, 21T1410Z (with the keeper in session), 21T1511Z, 21T1810Z, 22T1410Z, 22T1511Z and 22T1810Z; the Codex commissioning of 17T20:16Z made no collection, by its own summary. Known to have made requests with no per-request time in any log: the Horizon sweeps of 17 and 18 November (scout notes only); the robots.txt surveys behind the keeper's 21 November decision (`notes/keeper/robots-intent-2026-11-21/`, one robots.txt read per host, no times); LH032's reads of 16 and 19 November (no request log in their folders); and any reviewer's or driver's ad hoc reads.
- **Status and identity.** The Horizon log records no status; prose logs give times to the minute or "about"; the session fetch tool's User-Agent is never visible.
- **robots.txt at the time** for 596 page requests: judged on files of 23 November with no hash from the time to compare. A file that changed since is a limit, not a finding.

## Choices made after seeing rows (post hoc)

Each is labelled in the code where it is applied: the rules in `code/classify.py` (written after seeing candidate paths, before judging); LH039's "error" rows reclassed as gate refusals not sent, after reading that their bodies are the gate's refusal text (this removed 36 apparent R1 failures); duplicate gate-check rows of one Horizon call at the same second counted as one read; LH044's robots.txt redirect chains resolved to their last hop; the strictest of several Crawl-delay values taken where the applicable groups give more than one (2 study-host pairs); body use (model-read or script-parsed, for R4) from the URL's form and the log's kind; the "same day / later day" split of R6. None changes a rule in section 5 or the amendments.

## Network use

One current robots.txt re-read per authority with no copy from the week, through `studies/LH047/scripts/fetch.py` with `LIGHTHOUSE_PROVIDER=anthropic`, two seconds apart, on 23 November 2026 from 14:48:04 to 14:53:26 UTC: 138 requests, 135 first reads (135 authorities on 134 hosts) and 3 redirect hops, within section 10's ceiling (at most one per audited host, at most 248, redirects up to five hops); nothing else to any audited host. Statuses: 200 103, 404 18, 403 11, 302 2, 301 1, 401 2, 503 1. One re-read (api.wordpress.org) turned out unneeded once LH039's refusals were reclassed; one robots.txt redirect (sec.cloudapps.cisco.com) led to a login page that answered 403, an observation, not got round, with the redirect's one-time query values withheld from the kept copy and log; www.openwall.com's file was read twice (once as the redirect target of its `http://` authority), and the `http://` hop's 154-byte redirect body was overwritten by the other file of the same name (its hash is in the log). Plus `git fetch --shallow-since=2026-11-12` from Lighthouse's own repository, to fix "committed by the end of 22 November". Copies in `robots-current/`, kept by `fetch.py` (robots.txt copies are always kept; email addresses withheld).

## Files

`candidates-raw.csv`, `candidates-later-raw.csv` (the mechanical search); `logs.csv` (the population of logs, with reasons); `handcoded.csv`; `requests.csv` (1,837 rows); `needs-current.txt`; `robots-current/`; `requests-judged.csv` (one row per request, every rule, with evidence and reasons); `tables.md` and `summary.json`; `normalise-report.txt` (per log: rows, collector version, gated or not); `code/` (all scripts run, and the frozen rule files); `replay.sh` and `replay-output.txt`. Replay, offline, from the repository root: `sh studies/LH047/data/reaudit-2026-W47/replay.sh` (needs history back to 12 November). A signed asset URL's signature in LH044's committed log is withheld from the files here.
