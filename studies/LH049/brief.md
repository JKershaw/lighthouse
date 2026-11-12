# LH049: How far did the compromised bee-js 13.3.0 travel, in fetches from npm, on 9 November 2026 and after?

**In short** (added 10 November 2026; not part of the protocol). Just after midnight UTC on 9 November 2026 a release of bee-js, a JavaScript library for the Swarm storage network, was published to npm through the project's own release workflow, with a genuine provenance signature, and with code that ran at install time and fetched more code from an attacker's server, as StepSecurity and Socket report. npm removed it about 75 minutes later. We'll count how often npm's public download figures record it being fetched that day and afterwards, using a per-version count npm keeps for only seven days, so the reads have to start now. Socket has guessed "on the order of ten" fetches; we have read that guess but no download figure from npm. A download is a fetch, not an install or a victim. Reads daily from 10 November to 17 November, then once more a week or so later (row LH049-2026-11-24); the record by 1 December.

**Protocol 0.1, fixed 10 November 2026, before this study or, as far as the writer knows, any Lighthouse study read any npm download count for @ethersphere/bee-js.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the driving session of scheduled run 2026-11-10T1415Z, from proposals.md P-0026, which the horizon gate of 10 November 2026 started as an urgent watch under seven conditions that bind this brief (notes/horizon/2026-11-10T1415Z.md, "Conditions on P-0026"). Investigation: [Where software updates go](../../investigations/software-updates.md). The event's own records were read first, on 10 November between 14:37 and 14:39 UTC, and are kept raw under [data/](data/) with their [collector](scripts/collect_prebrief.py) and [sources](sources.md) (E1 to E9). The outcome [collector](scripts/collect.py) is committed with this brief, refuses to run until the brief is committed, and has been run only with `--help` and `--dry-run`, which make no request to any download endpoint.

## Question

From public data only: how many fetches of @ethersphere/bee-js 13.3.0 do npm's download counts record on 9 November 2026, the UTC day it was published and removed, and on each later day to 16 November, and in the week 17 to 23 November; what share of all bee-js fetches on 9 November was that; and, if an ordinary final release of bee-js is published while the reads run, how does 13.3.0's day compare with that release's first day in the same windows? The unit is the fetch, counted by UTC day. One release of one small package is a case, and nothing here generalises to other compromised packages or registries.

What a count counts: by npm's account (E9), a download is an HTTP 200 response that served a package tarball. It is not an install, a running copy, a victim or an infection. Mirrors fetch each new version once, usually on the day it is published (E9), so a count this small may be mostly mirrors and scanners; copies installed from caches, mirrors or lockfile-pinned stores are not counted at all. This study says so wherever a count appears, and makes no claim, in Lighthouse's voice, that any system fetched, ran or was harmed by 13.3.0 (gate, condition 4).

## The event, as the records give it

Each statement carries its source id from [sources.md](sources.md). That 13.3.0 was malicious, and that its provenance was valid, is StepSecurity's account (E3) and Socket's (E8), and the GitHub advisory's as OSV carries it (E6); this study quotes it and does not test it (condition 5).

- **Published** (observation, E1). The registry document's `time` field gives 13.3.0 as **2026-11-09T00:09:50.630Z**. StepSecurity (E3) and Socket (E8) give 00:09:50 UTC, the same second. Socket says it was published under the `latest` dist-tag; StepSecurity that npm still mapped `latest` to 13.3.0 at 00:31 UTC.
- **Removed.** The registry keeps 13.3.0's `time` entry but no longer lists it under `versions` (observation, E1, 14:37 UTC on 10 November); its version document answers 404 "version not found" (E2); `latest` is 13.2.0 again; no version carries a deprecation mark and the document has no `unpublished` entry. The registry gives no removal time and does not say who removed it. **As reported by Socket** (E8), npm "removed it at 01:24:58 UTC". The registry document's `time.modified`, its last change, is 2026-11-09T01:24:58.830Z, which agrees with Socket's time to the second but is not labelled a removal by the registry. StepSecurity (E3) gives no removal time. The study takes the window on the registry as **00:09:50.630 to 01:24:58 UTC on 9 November, 75.1 minutes** (Socket's end, as reported), with StepSecurity's 00:31 as the earliest end any source supports. Whatever the end, the whole window lies in one UTC day, so nothing in this study depends on it except the per-hour index below, which uses 75.1 minutes.
- **The advisory** (observation, E6). OSV holds MAL-2026-18773, alias GHSA-hh7j-5m3j-23pf, for version 13.3.0 only, published 2026-11-09T01:25:27Z (29 seconds after the registry's last change), imported by OSV at 02:23 UTC.
- **How it got there** (reported, E3, E8; not used). A release identity of the project published a commit and a release that triggered the project's existing trusted-publishing workflow, which built and published the package with provenance pointing to the real repository and workflow; Socket verified the attestation and says the earlier release 13.2.0's has the same shape. Neither source establishes how the identity's credential was obtained.
- **What the hook was said to do** (reported, E3, E8; described at the level a reader needs, condition 6). At install, a script fetched JavaScript from an attacker's server and ran it with the installing user's permissions; the code served looked for a desktop wallet application's key files and tried to install persistent remote access. StepSecurity says that at about 00:31 UTC the server was returning decoy content or 404. No tarball, script or payload has been or will be fetched by this study.
- **Ordinary releases** (observation, E1). The last final release before 13.3.0 was 13.2.0 on 2026-10-15T14:12:06Z; final releases came about monthly in 2026 (13.0.0 on 25 August, 13.1.0 on 11 September). Pre-releases on the `upcoming` and `next` tags came in bursts, the last on 27 October. No version was published after 13.3.0 by 14:37 UTC on 10 November.

## What is already known of the outcome

- **Counts in the event's records, read before this brief** (E3, E8; none checked, none from npm's per-version data). StepSecurity says the package recorded 3,560 downloads across all versions from 1 to 7 November 2026, a figure it says predates the release. Socket: the package "had 3,741 downloads between November 1 and 8" and "averaged about 470 npm downloads a day in early November 2026"; and of 13.3.0, "per-version counts for it are not available; based on daily traffic, we estimate on the order of ten fetches of 13.3.0, including scanners and mirrors." Socket's estimate is a guess from package traffic, not a count.
- **Lighthouse's reads.** No Lighthouse study has read any download count for bee-js, as far as the writer knows. The gate read npm's documentation (E7) and robots.txt files, and nothing from bee-js's download or registry endpoints. This brief's writer read E1 to E9 and nothing else about the package.
- **What the writer expects**, stated so it can be seen to be wrong: a count in the tens on 9 November, much of it mirrors, and few or none afterwards. This expectation shapes nothing below.

## Population and unit

- **The case:** every fetch npm's per-version endpoint attributes to version string `13.3.0` of @ethersphere/bee-js.
- **The package:** npm's daily totals for @ethersphere/bee-js, all versions.
- **The comparison release, if any:** the first final release (a version string without a hyphen) higher than 13.2.0, other than 13.3.0, whose first `time` entry in the registry document falls from 2026-11-10T00:00Z to 2026-11-16T23:59Z, as read at any read. Pre-releases do not qualify. None exists at the time of writing; if none appears, measure 5 is not made.
- **Days:** UTC days, as npm counts them (E7: logs are crunched once a day soon after UTC midnight). Day 0 is 9 November for 13.3.0.

## Sources, events and clocks

Each read makes six requests, in this order, through [scripts/collect.py](scripts/collect.py) (condition 7):

1. `GET https://api.npmjs.org/downloads/point/last-week/@ethersphere/bee-js`: the package total for "the last 7 available days", with its stated inclusive start and end dates (E7).
2. `GET https://api.npmjs.org/versions/@ethersphere%2Fbee-js/last-week`: one total per version over "the last 7 available days" (E7), the scoped name's slash percent-encoded as npm's documentation requires. Whether this answer states its dates is not known before the first read.
3. The same as 1 again, so a window that rolled over during the read is seen.
4. `GET https://api.npmjs.org/downloads/range/2026-11-01:<read's UTC date>/@ethersphere/bee-js`: the package total for each available day.
5. `GET https://registry.npmjs.org/@ethersphere%2Fbee-js`: the registry document, parsed as JSON only (publish times, versions listed, dist-tags, deprecation marks).
6. `POST https://api.osv.dev/v1/query` for the package: the advisory's state.

**Clocks.** The day that counts is npm's UTC day. The window of a per-version answer, W(t), is taken to end on day t and start on day t−6, where t is the end date stated by requests 1 and 3 of the same read, provided both state the same start, end and total and the per-version totals of request 2 sum to that total. If any of these fails, that read's window is unknown and its differences are not used. Each read logs its UTC start and finish and the stated dates (condition 2). The publish and removal times above are the event's clocks; this study resolves nothing finer than a day (condition 3).

**Day counts** (derived). Write V(t) for 13.3.0's total in the per-version window ending day t, and d(t) for its fetches on day t. Consecutive windows give V(t) − V(t−1) = d(t) − d(t−7). Because 13.3.0 did not exist before 9 November, d(t) = 0 for every t before 9 November and V(8 November) = 0; this holds for 13.3.0 only, and for the comparison release only from its own publication (condition 2). So:

- d(9 Nov) = V(9 Nov), if a read holds the window ending 9 November;
- d(t) = V(t) − V(t−1) for t from 10 to 15 November;
- d(16 Nov) = V(16 Nov) − V(15 Nov) + d(9 Nov);
- if the window ending 9 November is never read, d(9 Nov) is not known exactly and is bounded: at most the V of the earliest window held, and at least V(15 Nov) − V(16 Nov) (since d(16 Nov) ≥ 0);
- a missed day breaks the series: a day count that needs a window not held is unknown, and the sums that can still be formed are reported as sums.

The window ending 9 November is readable only until npm loads 10 November's figures, soon after 00:00 UTC on 11 November (E7). **The first read must therefore be made on 10 November** if d(9 Nov) is to be exact; a first read on 11 or 12 November leaves it bounded.

## Measures

1. **Day-0 count**, d(9 Nov), exact or bounded as above, and its share S0 of the package's total on 9 November from request 4.
2. **Fetches after removal:** d(t) for 10 to 16 November, their sum, and V(23 Nov) from the weekly read (fetches of 13.3.0 recorded from 17 to 23 November). A count above zero on any day after 9 November is reported as "npm's counts record fetches of 13.3.0 on days after it was removed"; by what route (a mirror, a cache, a store npm still served from) is not observable here, and the study does not guess.
3. **Per-hour index**, I = S0 / (75.1 / 1440): 13.3.0's share of the day's fetches against its share of the day's minutes on the registry. A description, not a test; it assumes fetches spread evenly over the day, which they do not, and a mirror's single fetch is not spread at all.
4. **The package's day:** the package's total on 9 November beside the median and range of its totals on the other days 2 to 16 November that the reads hold, and beside d(9 Nov). Reported as numbers; no excess is attributed to 13.3.0.
5. **The comparison release R** (only if one qualifies): d0(R), R's fetches on its publication day derived the same way, its share S0(R) of the package's total that day, and I(R) using the minutes from R's publication to the end of that day (or to the next higher final release that day). **The pre-set reading:** 13.3.0 "was fetched as an ordinary new release was in its time on the registry" if I(13.3.0) is within a factor of two of I(R); "more" or "less" otherwise. Two cases, one each; a description of them, not a test.
6. **Socket's estimate:** d(9 Nov) beside "on the order of ten". The pre-set reading: consistent if d(9 Nov) is from 4 to 31 (within half an order of magnitude of ten); otherwise not, stated as a difference without judging which is right. If d(9 Nov) is only bounded, the reading is made only if the whole bound falls inside or outside that range.
7. **Registry state at each read:** whether 13.3.0 is listed, whether its `time` entry is kept, `latest`, any deprecation mark or `unpublished` entry, versions published since the last read; and OSV's record (still present, modified, withdrawn).

## The comparison that matters

Within the same windows only (condition 3): 13.3.0's day-0 fetches against the package's fetches that day (measures 1 and 3), and, if one is published, against an ordinary release's first day in the same series (measure 5), with the unit the release. The earlier ordinary releases' first days lie outside every per-version window npm still serves, so no per-version comparison with them is possible, and the package's daily totals around their publication days are not read. The question the comparison answers is whether, in its 75 minutes, the compromised release was fetched at all differently from what the same windows show of ordinary traffic. A difference in a rate is a description; a cause needs its own evidence, which this study does not collect.

## Missing evidence

- A request that errs, times out, answers other than 200, meets a challenge or a rate limit, or is refused by robots.txt is **unavailable** for that read; one retry is allowed per request within the read and logged. A wall is an observation, never something to get around.
- If a 200 per-version answer has no key `13.3.0`, 13.3.0 has **no record** in that window, not zero fetches: whether npm's per-version counts keep a version removed from the registry is exactly what is not known. If no read's answer has the key, measures 1 to 3, 5 and 6 are unknown for 13.3.0 and the study says so; Socket's estimate then stands as reported and unchecked.
- If an answer has the key `13.3.0` in some reads and not others, the reads without it are "no record" and their differences are unknown.
- A window whose dates cannot be fixed by the rule under "Clocks" is **unknown**, and so is every difference that uses it.
- A day missing from request 4's answer, or answered as zero for the whole package on a day when the per-version window shows fetches, is unknown for measure 4.
- Unknown is never no.

## Overlap with earlier studies

The design is LH040's on a second registry: a compromised release's fetches on its day against the same day's traffic, with a per-hour index. No data are shared: LH040 reads PyPI's logs through ClickPy, and npm counts differently (whole HTTP 200 tarball responses, by npm's account, E9; ClickPy holds PyPI's per-file download log). The record may set the two cases side by side as a description, saying so; it draws no pooled figure. No Lighthouse study has read bee-js or any npm per-version count. This study reads no repository, lockfile, dependent or mirror, and names none (condition 5). Its own requests fetch no tarball and so add nothing to the counts they read.

## Model disclosure

Lighthouse runs on Anthropic's models. StepSecurity credits the discovery to its "AI Package Analyst" (E3). As reported, the event has no AI system acting in it and no self-propagation; this study claims nothing about AI activity or spread (condition 7), and the record will not frame it as such.

## Resource ceiling

Per read: the six requests above, at most one retry each (twelve in all), robots.txt fetches not counted; about 1 MB, almost all of it the registry document. Nine reads at most (eight daily, one weekly), so at most 108 requests. No account, key, credential or paid service; no contact with anyone; no tarball, script or payload, ever (condition 6). Model spend: about $10 at list rates for the reads, the tabulation and the record, before reviews.

## Reads, schedule and stopping

- **Daily reads,** `python3 -I studies/LH049/scripts/collect.py --read <UTC label>`, once each UTC day from 10 November (no later than 12 November, condition 2) to 17 November, each at least an hour after 00:00 UTC so that npm's previous day has landed. The read of 17 November holds the window ending 16 November, the first without 9 November.
- **Weekly read,** on the day 14 days after the first read (24 November if the first read is on 10 November): the window ending 23 November, for measure 2's tail.
- **Checkpoint,** after the read of 17 November and by 19 November: a tabulator, written then to implement the measures as written and changing nothing above; measures 1 to 4, 6 and 7, and 5 if a release qualified; an interim record, version 0.1.
- **Record,** version 1.0, by 1 December 2026, then its reviews before anything is released.
- **Stopping:** after the weekly read 14 days after the first read (condition 2), or earlier if npm's download endpoints are unavailable at three consecutive reads. The question, the comparison release's rule, the measures, the pre-set readings and the missing-evidence rules do not change after any count is read; a later change is a dated amendment, labelled post hoc if made after counts were seen.

## What would leave it inconclusive

- No per-version answer carries 13.3.0 (measures 1 to 3, 5 and 6 unknown).
- The window ending 9 November is not read and the bound on d(9 Nov) is too wide to place it in measure 6's range, or a missed day leaves the bound unformable.
- The per-version answer states no dates and its totals do not sum to the point total of the same read, so no window can be fixed.
- No comparison release is published (measure 5 not made; measures 1 to 4 then describe one case with nothing like it in the same windows, and the record says so).

It cannot say, in any case, how many machines installed or ran 13.3.0, who did, whether the hook's server answered them, whether any wallet or credential was taken, how many copies came from mirrors or caches, or which projects resolved it. Those would need data that are private, or a census of dependents and lockfiles that the gate's aggregate-only condition would bind.
