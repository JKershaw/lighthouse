# LH053: How far did WPPConnect's compromised npm releases travel, in fetches from npm, on 15 and 16 November 2026 and after?

**In short** (added 17 November 2026; not part of the protocol). Late on 15 November 2026 the WPPConnect project's own release automation published a version of its WhatsApp library to npm, and early on 16 November a version of its server, both built from commits nobody reviewed and both carrying code that StepSecurity says sends a machine's secrets to an attacker. The library version was npm's default for about four and a half hours; both are now marked deprecated but still installable. We'll count how often npm's public download figures record those versions being fetched on the release days and in the two weeks after, using a per-version count npm keeps for only seven days, so the first read has to be today. StepSecurity reports 155 downloads of the library version in a window that held only its first 28 minutes; we have read that figure but no download count from npm. A download is a fetch, not an install or a victim. Daily reads to 22 November, one more on 29 November, then a record and its reviews.

**Protocol 0.1, fixed 17 November 2026, before this study or, as far as the writer knows, any Lighthouse study read any npm download count for @wppconnect-team/wppconnect or @wppconnect/server.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the driving session of scheduled run 2026-11-17T141414Z, from proposals.md P-0036, which the horizon gate of 17 November 2026 started as an urgent watch under seven conditions that bind this brief (notes/horizon/2026-11-17T1414Z.md, "Conditions on P-0036"). Investigation: [Where software updates go](../../investigations/software-updates.md). Model: [LH049](../LH049/brief.md) is the pattern; see "Overlap". The event's own records were read first, on 17 November between 14:41:08 and 14:41:27 UTC, and are kept raw under [data/pre-brief-2026-11-17T1441Z/](data/pre-brief-2026-11-17T1441Z/) with their read log. The [collector](scripts/collect.py) is committed with this brief, refuses to make an outcome read until the brief is committed, and had been run only in its pre-brief mode (which refuses any api.npmjs.org URL) and with `--dry-run`, which asks robots.txt and makes no request to any download endpoint.

## Question

From public data only: how many fetches of the compromised versions do npm's download counts record on the release days, 15 and 16 November 2026 (UTC), and on each later day to 21 November, and in the week 22 to 28 November; what share of each package's fetches on the release days was that; and how does the library version's share, against its time as npm's default (`latest`), compare with the ordinary release just before it in the same windows? The unit is the fetch, counted by UTC day. Two releases of one project are a case, and nothing here generalises to other compromised packages or registries.

What a count counts: by npm's account (LH049's source E9, read 10 November 2026), a download is an HTTP 200 response that served a package tarball. It is not an install, a running copy, a victim or an infection. Mirrors and scanners fetch new versions too, often once on publication day; copies installed from caches, mirrors or lockfile-pinned stores are not counted at all. The server depends on the library by a version range, so a fresh install of the server while the library version was `latest` fetched both (StepSecurity, E1), and a library fetch may be a server install. The project's Docker images are counted by Docker Hub per repository, not per tag, and are not read, so the images' reach is unknown and is said so (condition 5). This study makes no claim, in Lighthouse's voice, that any system fetched, ran or was harmed by these versions.

## The event, as the records give it

Read 17 November 2026, 14:41 UTC; each with its source id from "Event records" below. That the versions are malicious, the trusted-publishing route, the unreviewed commits and the force-push are StepSecurity's account (E1) and, for maliciousness, the OSV records' (E4, E5); this study quotes them and does not test them (condition 7).

- **Library, @wppconnect-team/wppconnect 2.4.1.** Published **2026-11-15T23:31:48.103Z** (observation, E2 `time`). StepSecurity: "npm began serving" it at 23:31 UTC and it was `latest` "for about 4.5 hours", `latest` "back to 2.4.0 by about 04:03 UTC, Nov 16" (E1). It is listed under `versions`, published by "GitHub Actions" with a trusted-publisher identity and a SLSA provenance attestation reference (observation, E2), and carries the deprecation message "SECURITY INCIDENT: This version contains code that may transmit host environment, configuration and session data to an external endpoint. Do not use. Pin 2.4.0 pending a reviewed release." (observation, E2). Current `latest`: 2.4.0 (observation). The registry document's `time.modified` is 2026-11-16T04:03:46.148Z; the registry records no deprecation time and no dist-tag history, and StepSecurity calls its deprecation time "inferred" from `modified` (E1). No `unpublished` entry.
- **Library 2.4.3.** No `time` entry and not listed (observation, E2). StepSecurity: the release workflow logged "a successful publish of 2.4.3", but npm does not list it, "We do not know why" (E1).
- **Server, @wppconnect/server 2.10.82.** Published **2026-11-16T03:09:59.433Z** (observation, E3 `time`); StepSecurity gives 03:09 UTC and says it was "Never `latest`" (E1). Listed, published by "GitHub Actions" with a trusted-publisher identity and no attestation reference (observation, E3), with the same deprecation message, ending "Pin 2.10.81 pending a reviewed release." Current `latest`: 2.10.81. `time.modified` 2026-11-16T04:06:44.433Z. No `unpublished` entry.
- **Server 2.10.83.** No `time` entry and not listed (observation, E3); StepSecurity says its publish job succeeded (E1).
- **Ordinary releases just before** (observation, E2, E3). Library 2.4.0 at 2026-11-13T21:24:32.294Z, after 2.3.6 on 23 October; server 2.10.81 at 2026-11-13T03:06:40.772Z, after 2.10.80 on 11 November (server releases came every one to three days in November).
- **Advisories** (observation, E4, E5). OSV holds MAL-2026-20044 (library, version 2.4.1 only) and MAL-2026-20043 (server, 2.10.82 only), both published 2026-11-16T04:10:00Z, modified 2026-11-17T05:45:05Z, not withdrawn, sourced from the OpenSSF malicious-packages repository. Neither lists 2.4.3 or 2.10.83.
- **Clocks used.** Publication from the registry `time` field. The end of 2.4.1's time as `latest` is the library document's `time.modified`, 04:03:46.148Z, which agrees with StepSecurity's "about 04:03" but which the registry does not label; it is labelled StepSecurity's inference wherever it is used. That 2.4.0 became `latest` at its publication and held it until 2.4.1's, and again from 04:03:46 on 16 November, is assumed (the registry keeps no dist-tag history) and labelled. This study resolves nothing finer than a UTC day except in measure 3's minutes.
- **What the payload does and how the account was reached** are described in E1 and E4 at a level this brief does not repeat (condition 6). No tarball, payload, commit, Docker layer, nightly asset, workflow or bot has been or will be fetched or read by this study.

## What is already known of the outcome

- **StepSecurity's count** (E1, read in full at 14:41 UTC; the gate read it through a summary): "npm recorded 155 downloads of it, but for a window ending November 15 that covers only about 28 minutes of that period, so 155 is a floor, not a count of affected systems." The 28 minutes match the registry: 2.4.1 was on the registry for 28.2 minutes of 15 November UTC (derived from E2). So 155 is, as StepSecurity reports it, 2.4.1's total in npm's per-version window ending 15 November, which is its fetches on 15 November alone. Lighthouse has not read that window and cannot now (npm replaced it at about 00:00 UTC on 17 November). "A floor" is the vendor's word. StepSecurity gives no figure for the server.
- **Lighthouse's reads.** No Lighthouse study has read any download count for either package, as far as the writer knows. The writer read E1 to E5, which carry no npm download figure other than StepSecurity's quoted above, and LH049's brief, collector and interim record, whose bee-js outcomes shaped the sum-check rule below (stated so a reader can judge it).
- **What the writer expects**, stated so it can be seen to be wrong: 2.4.1 in the hundreds over the two release days, most of it during its hours as `latest`; 2.10.82 in the tens; few fetches of either after deprecation. This expectation shapes nothing below.

## Population and unit

- **The case versions:** library 2.4.1 and 2.4.3; server 2.10.82 and 2.10.83: every fetch npm's per-version endpoint attributes to those version strings. 2.4.3 and 2.10.83 have no registry record; if a per-version answer carries either, it is reported as answered.
- **The comparison releases:** library 2.4.0 and server 2.10.81, the ordinary releases immediately before the case versions, both first published inside the window ending 16 November and on the same day, 13 November. Chosen here, before any count, because they are the only ordinary releases whose whole life sits inside the same per-version windows.
- **The packages:** npm's daily totals for each package, all versions, from the range answers below.
- **Days:** UTC days, as npm counts them (logs crunched once a day soon after UTC midnight, LH049's E7). Day 0 is 15 November for 2.4.1 and 16 November for 2.10.82.

## Sources, events and clocks

Each read makes eight requests, in this order, through [scripts/collect.py](scripts/collect.py) (condition 4), for the library (L) then the server (S):

1. `GET https://api.npmjs.org/downloads/range/last-week/<package>`: the package's total for each of "the last 7 available days", with the stated inclusive start and end dates.
2. `GET https://api.npmjs.org/versions/<package, slash percent-encoded>/last-week`: one total per version over the last 7 available days. In LH049's reads this answer stated no dates.
3. The same as 1 again, so a window that rolled over during the read is seen.
4. `GET https://registry.npmjs.org/<package, slash percent-encoded>`: the registry document, parsed as JSON only (publish times, versions listed, dist-tags, deprecation marks, any `unpublished` entry).

The gate's condition 4 names "point" answers; this brief uses npm's range answer for the same period instead, because it states the same start and end and its days sum to the same total, and it also gives each day's package total, which the shares need, within the same eight requests. OSV is not read at the daily reads; it is re-read once, with both registry documents and StepSecurity's post, in the collector's pre-brief mode at the closure gate (five requests).

**Clock rule** (LH049's, adapted to the range answer). The window of a per-version answer, W(t), is taken to start on day t−6 and end on day t, where t is the end date stated by requests 1 and 3 of the same read, provided both state the same start and end, seven days, and the same value for every day. If they differ in any of these, that package's window at that read is **unknown** and its differences are not used. Each read logs its UTC start and finish and the stated dates.

**Sum check, fixed before the first read** (gate condition 2; LH049's lesson). Write P(t) for the sum of the seven daily package totals in request 1, and Σ(t) for the sum of all per-version totals in request 2. D(t) = Σ(t) − P(t).

- If D(t) = 0, the window is **balanced** and every version's total V(t) is taken as exact.
- If D(t) ≠ 0, the window is still dated by the clock rule (the per-version answer is not discarded, as LH049's rule discarded it) but **unbalanced**, and each case or comparison version's total is carried as an interval: [max(0, V − D), V] if D > 0, and [V, V + |D|] if D < 0. The interval assumes the discrepancy lies on one side and in versions that the per-version answer lists; that assumption is stated beside every interval, since nothing read can check it.
- Every derived figure is computed by interval arithmetic from the windows it uses. Where all are balanced the interval is a single number and is reported as exact. Where any is unbalanced, the figure reported is the interval, with the value as npm answered it beside it, labelled "as answered, unbalanced window (D = …)", never as exact.
- No tolerance: equality is exact. No window is admitted or refused after its values are seen by any other rule than this one.

**Day counts** (derived). Write V(t) for a version's total in the window ending day t and d(t) for its fetches on day t. Consecutive windows give V(t) − V(t−1) = d(t) − d(t−7). A version has d(t) = 0 on every day before its first `time` entry. So, for 2.4.1:

- d(15) + d(16) = V(16), from the read of 17 November, the only window Lighthouse can hold that contains both release days and no later day;
- d(15) alone is not observable by Lighthouse; StepSecurity's 155 (E1) is reported beside the sum, labelled theirs, with d(16) = V(16) − 155 labelled as resting on it; if V(16) < 155 the two are reported as inconsistent, without judging which is right;
- d(t) = V(t) − V(t−1) for t from 17 to 21 November (d(t−7) falls before 15 November and is zero);
- V(28), from the weekly read, is d(22) to d(28) together (W(28) starts on 22 November, contiguous with W(21)).

For 2.10.82: d(16) = V(16); d(t) = V(t) − V(t−1) for t from 17 to 21 November; V(28) as above. For 2.4.0 and 2.10.81 (first published 13 November), V(16) is their fetches on 13 to 16 November together. 2.4.3 and 2.10.83, if they appear, are treated as if first published on 15 and 16 November respectively, the earliest days StepSecurity's account allows, and that is said.

**If the first read is made on 18 November instead** (W(17) its earliest window), V(17) for 2.4.1 is d(15) to d(17) together, the earliest count is stated as including 17 November, d(17) is not separable, and measures 1 to 3 use the three-day sums with the minutes and package totals of the same three days. A missed daily read breaks the series: a day count that needs a window not held is unknown, and the sums that can still be formed are reported as sums.

## Measures

1. **Release days.** For 2.4.1: V(16) = d(15) + d(16), its share of the package's fetches on 15 and 16 November (P's days from the same read), and StepSecurity's 155 beside it as above. For 2.10.82: d(16) and its share of the server's fetches on 16 November. 2.4.3 and 2.10.83 as answered.
2. **Fetches after deprecation:** d(t) for 17 to 21 November and V(28) for each case version. A count above zero on any of those days is reported as "npm's counts record fetches of a deprecated version on days after it was deprecated"; by what route (an exact pin, a lockfile, a mirror, a scanner) is not observable here, and the study does not guess.
3. **Time as `latest`, library only** (a description, not a test). I(2.4.1) = [V(16) / (P on 15 and 16 November)] / (271.97 / 2,880), the share of the two days' fetches against the share of the two days' minutes it was `latest` (23:31:48.103 to 04:03:46.148, the end as StepSecurity infers it). I(2.4.0) = [V_2.4.0(16) / (P on 13 to 16 November)] / (4,203.49 / 5,760), using the minutes 2.4.0 was `latest` on 13 to 16 November under the assumption above (21:24:32.294 on 13 November to 23:31:48.103 on 15 November, and 04:03:46.148 to 24:00 on 16 November). **The pre-set reading:** 2.4.1 "was fetched as the ordinary release before it was, for its time as `latest`" if I(2.4.1) is within a factor of two of I(2.4.0); "more" or "less" otherwise. If either index is an interval, the reading is made only if the whole interval of the ratio falls inside, or wholly outside, the factor-of-two band; otherwise "not made". The index assumes fetches follow `latest` evenly over the minutes, which they do not: mirrors fetch once, exact pins ignore `latest`, and the server's range pulled the library. Two releases, one each; a description, not a test.
4. **Server, beside its own predecessor** (no index, since 2.10.82 was never `latest`): d(16) for 2.10.82 and its share of 16 November's server fetches, beside V_2.10.81(16) and its share of 13 to 16 November, as numbers only.
5. **The packages' days:** each package's daily totals 10 to 28 November as the reads hold them, with 15 and 16 November beside the median and range of the other days held. No excess is attributed to the case versions.
6. **Registry state at each read:** for each case version, whether it is listed, its `time` entry, its deprecation message; `latest`; `time.modified`; any `unpublished` entry; versions added or removed since the last read; whether 2.4.3 or 2.10.83 appear. OSV's two records at the closure re-read (present, modified, withdrawn, versions affected).

## The comparison that matters

Within the same windows only: 2.4.1's release-day fetches against its package's fetches on those days, and against the ordinary 2.4.0's in the same window, normalised by time as `latest` (measure 3), with the unit the release; and 2.10.82 beside 2.10.81 as numbers (measure 4). The question is whether, in its hours as npm's default, the compromised library version was fetched any differently from the ordinary release before it. A difference in a rate is a description; a cause needs its own evidence, which this study does not collect.

## Missing evidence

- A request that errs, times out, answers other than 200, meets a challenge or a rate limit, or is refused by robots.txt is **unavailable** for that read. **No retry** (condition 4): the collector requests each target once per read and refuses a second attempt. A wall is an observation, never something to get around.
- If a range answer is unavailable, that package's window at that read is unknown. If the per-version answer is unavailable, so is every V for that package at that read.
- **A case version's key absent from a 200 per-version answer.** In a balanced window, the package's total is wholly attributed to the versions listed, so the version is recorded as **"none in npm's counts"** for that window (derived), with the note that npm might drop a deprecated version from both its tables alike, which the reads cannot tell apart. In an unbalanced or unknown window, an absent key is **no record**, not zero. (LH049 classed every absent key as no record; this rule differs, was chosen after LH049's outcome was seen and before any WPPConnect count, and is applied as written.)
- A day missing from a range answer is unknown for measure 5.
- Unknown is never no.

## Overlap with earlier studies

The design is LH049's (bee-js 13.3.0 on npm, protocol 0.1 of 10 November 2026), the same endpoints and clock rule, with three changes fixed here before any count: the range answer for the point answer, the sum-check rule above instead of discarding an unbalanced window, and the absent-key rule. LH040 (LiteLLM 1.107.0, PyPI through ClickPy) is the same question on a second registry. No data are shared: different packages, and no figure here will be pooled with LH049's or LH040's; the record may set the three cases side by side as a description, saying so. LH049's own reads continue to 24 November on a different package. This study reads no repository, lockfile, dependent, mirror, image or account, and names none beyond the two packages the reports name (condition 6). Its own requests fetch no tarball and so add nothing to the counts they read.

## Model disclosure

Lighthouse runs on Anthropic's models. No source read reports an AI system acting in this event, an AI element in the payload or any self-propagation (E1, E4, E5; condition 7). This study claims nothing about AI activity or spread, and the record will not frame it as such.

## Resource ceiling

Per read: the eight requests above, no retries, robots.txt fetches not counted; about 3 MB, almost all of it the two registry documents. Seven outcome reads at most (six daily, one weekly), so at most 56 requests, plus five event-record requests now and five at closure. No account, key, credential or paid service; no contact with anyone; nothing in the forbidden list ever (the collector refuses tarball paths, npm's package pages, github.com, Docker and Telegram hosts by URL). Model spend: about $20 at list rates for the brief, the reads and the record, before reviews (condition 4).

## Reads, schedule and stopping

- **First read,** `python3 -I studies/LH053/scripts/collect.py --read <UTC label>`, on 17 November, after this brief is committed and before about 00:00 UTC on 18 November, so the window ending 16 November is held. Failing that, on 18 November, under the rule above.
- **Daily reads,** once each UTC day from 18 to 22 November, each at least an hour after 00:00 UTC: the windows ending 17 to 21 November, the last that contain 15 November.
- **Weekly read,** on 29 November (window ending 28 November, contiguous with the last daily window), or failing that on 30 November or 1 December, its window stated as read.
- **Stopping:** no read after 1 December 2026, 14 days after the first read, and no extension without a keeper line (condition 3); earlier if npm's download endpoints are unavailable at three consecutive reads. The closure gate then re-reads the event records (pre-brief mode, five requests) and reconciles every scheduled read.
- **Record,** version 0.1 then 1.0, with a tabulator written then to implement the rules as written and changing nothing above, then its evidence review, reader-and-inference review and recheck before anything is released.
- The question, the comparison releases, the measures, the pre-set reading, the sum-check rule and the missing-evidence rules do not change after any count is read; a later change is a dated amendment, labelled post hoc if made after counts were seen.

## What would leave it inconclusive

- The read of 17 November is not made, or its library window is unknown, so d(15) + d(16) is never held alone and measures 1 and 3 rest on three-day sums.
- The window ending 16 November is unbalanced by enough that the interval for V(16), or the ratio in measure 3, straddles the reading's boundaries (measure 3 "not made").
- No per-version answer carries 2.4.1 or 2.10.82.
- The release-day counts are so small that one mirror's fetch moves the index past the factor-of-two band, which the record will say if it happens.

It cannot say, in any case, how many machines installed or ran these versions, who did, whether any secret or session was taken, how many came from mirrors, caches or the server's range, how far the Docker images or the nightly asset travelled, or which projects resolved them.

## Event records

Read by `python3 -I studies/LH053/scripts/collect.py --prebrief --read 2026-11-17T1441Z` (provider anthropic; every URL allowed by scripts/robots_gate.py), kept gzipped with email addresses withheld under data/pre-brief-2026-11-17T1441Z/, with `read_log.json` (URL, UTC start and finish, status, bytes, SHA-256 of the bytes received, emails withheld, robots decision). No download endpoint was requested.

| Id | Source | URL | Read (UTC) | Status, bytes, SHA-256 of bytes received | Date | What it gives |
|---|---|---|---|---|---|---|
| E1 | StepSecurity, "WPPConnect Compromised: Malicious Releases Steal Secrets and WhatsApp Sessions Through the Project's Own Pipeline" | https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions | 14:41:08 | 200, 189,396, aca69338…c540040aa | dated 16 November 2026; Last-Modified 17 November 13:36 GMT | The account of the event, its timeline and the 155 figure. |
| E2 | npm registry, library document | https://registry.npmjs.org/@wppconnect-team%2Fwppconnect | 14:41:25 to 14:41:26 | 200, 944,979, 0f01f296…3a093f90b (571 emails withheld) | `time.modified` 2026-11-16T04:03:46.148Z | Publish times, `latest` 2.4.0, 2.4.1 listed and deprecated, no 2.4.3. |
| E3 | npm registry, server document | https://registry.npmjs.org/@wppconnect%2Fserver | 14:41:26 | 200, 1,785,064, d8f296fc…d36eae5 (507 emails withheld) | `time.modified` 2026-11-16T04:06:44.433Z | Publish times, `latest` 2.10.81, 2.10.82 listed and deprecated, no 2.10.83. |
| E4 | OSV query, library | https://api.osv.dev/v1/query (POST, name and ecosystem npm) | 14:41:26 to 14:41:27 | 200, 3,049, 08e834f2…9ced4f376 | record published 2026-11-16T04:10:00Z | MAL-2026-20044, 2.4.1. |
| E5 | OSV query, server | https://api.osv.dev/v1/query (POST, name and ecosystem npm) | 14:41:27 | 200, 2,997, a209552b…4e4830a0b0 | record published 2026-11-16T04:10:00Z | MAL-2026-20043, 2.10.82. |

Full hashes are in the read log. Read earlier and not re-read: npm's download-count documentation and its 2014 account of what a download is (LH049's E7 and E9, 10 November 2026); scout 3's file (notes/horizon/2026-11-17T1414Z/scout-3-supply-chain.md). Not opened: the GitHub issues, commits, Actions logs, attestations and Docker Hub pages that E1 cites; the OpenSSF malicious-packages files the OSV records cite; any mirror.
