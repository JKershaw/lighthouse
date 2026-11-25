# LH057: GreyNoise's PHP2Shell tracker: what its own sensors count of exploitation attempts and successes, read from 21 November to 3 December 2026

**In short** (added 20 November 2026; not part of the protocol). GreyNoise, a company that runs decoy servers to watch who attacks them, keeps a public page counting attacks on the two PHP flaws fixed on 21 October 2026, which people nicknamed PHP2Shell. The page gives running totals of attempts, reconnaissance and what it calls confirmed successful exploitations against its own deliberately vulnerable sensors, plus a dated list of each success and the date each attacking address was first tracked. We'll read it once a UTC day from 21 November to 3 December and describe how GreyNoise's own counts move, as GreyNoise's counts: they're about its sensors, not victims, and not about exploitation across the internet. Daily reads began on 21 November (updated 25 November; unreviewed): through 25 November, GreyNoise's list of confirmed successes had no entry after 20 November.

**Protocol 0.1, fixed 20 November 2026, before this study read any count on the page.** Writer: a research subagent in Claude Code (Claude Opus 5.5) for the Horizon run 2026-11-20T1214Z, from proposals.md P-0044, which the fresh gate of that sweep started as a deepening of [Where software updates go](../../investigations/software-updates.md), not urgent, under eight conditions that bind this brief ([the gate](../../notes/horizon/2026-11-20T1214Z.md), "Conditions on P-0044"). The driving session commits this brief and its schedule rows before the first outcome read. The design is chosen by the structure-only read below (gate condition 2).

## Question

From GreyNoise's public page at `https://php.events.greynoise.io/` only, read once a UTC day from 21 November to 3 December 2026: how do the counts GreyNoise reports for its own sensors move over the window (sessions, exploitation attempts, reconnaissance, confirmed successful exploitations, the addresses behind each, and new addresses), what dated series of successes and of newly tracked addresses does the page itself hold, by UTC day, and do the page's dated lists agree with its own running totals and with themselves from one read to the next?

Scope (gate condition 1). The study is of GreyNoise's PHP2Shell tracker as GreyNoise defines it. The page names its flaws: its summary names two CVE identifiers, and the structure read checked by comparison, without printing them, that they are CVE-2026-109618 and CVE-2026-109619, the flaws of PHP's releases of 21 October that LH033 and LH037 follow. The page does not mention PHP's releases of 19 November (strings 8.5.13 and 8.4.28 absent), and this study is not about them. If a later read's summary names other flaws, the record reports that as a change of the tracker's scope and keeps each read's own scope beside its counts. A few other CVE identifiers appear in table cells (tags on addresses); they are not the tracker's scope and are not counted.

The study says nothing about AI. No source read ties this activity to any AI system, and the record will say so.

## The structure-only read of 20 November 2026

One gated GET of the page at 12:37:54 UTC (robots.txt answered HTTP 403, which the gate treats as no rules; recorded), HTTP 200, cut at the 4 MiB ceiling, sha256 `00d1e050...63ec` of the bytes received ([fetchlog.csv](fetchlog.csv)). It was read only by scripts that printed tag names, ids, classes, headings, table headers, labels and date formats, with every digit replaced by `#` and every address-like string removed; the body was deleted at 12:40 UTC and not kept. What it showed (observation, structure only):

- **Headline.** A "Last updated" stamp (an ISO 8601 `datetime` with a minute shown in UTC); a summary sentence giving new attacker addresses "in the last ## hours", a running total of attacker addresses "as of" a date, and confirmed successful exploitations "from ## attacker IPs, against our vulnerable sensors"; a stats box: "Sessions observed", split into "Exploitation attempts" and "Reconnaissance", then the confirmed successes and their addresses; and the note "GreyNoise sensors since ## Oct #### UTC; benign sources excluded."
- **Timeline.** Five dated events: CVE identifiers reserved (by the PHP CNA), earliest observed related activity, publication to CVE.org, addition to CISA's KEV, and first successful exploitation observed, each with an ISO `datetime`; "Sources: GreyNoise sensor sessions and CVE.org." The masked print showed that the first-success entry quotes the commands GreyNoise recorded; that text is not reproduced here and the collector never extracts it (condition 6).
- **A dated list of successes.** A table, "Successful Exploitation (####)", headed "Shell started (UTC)", "Attacker IP", "Exploit session", "Process chain", "Commands run (in order)", with a four-digit number of rows (the digit count was visible, the digits were not); its shell-start cells are `YYYY-MM-DD hh:mm` in UTC. So the page holds a dated history of each success it lists.
- **Address tables.** "Indicators Associated with Successful Exploitation" (type, value, role, first and last seen, exploitations); "Block candidates"; "Newly Observed Attack Infrastructure"; "Technical Similarity Clustering" ("automatically generated investigative leads, not attribution"); "IP First Seen Versus Related Activity" (age buckets); "Observed User-Agents"; and "Observed Infrastructure", one row per tracked address with columns including `entry` (a date, `YYYY-MM-DD hh:mm`), `gn_first_seen`, `last_seen` and `sensors`, a three-digit number of rows. So the page holds the date each address entered the tracker.
- **Charts.** "Interactive charts", the first "Hourly activity: classification and sensor hits", drawn by an inline charting library. The 4 MiB cut fell inside that library, after every table and before any chart data, so whether the chart holds an hourly series of attempts and reconnaissance, and over what span, is unknown, and it cannot be read under the ceiling.
- **No links** to notes, methods or terms other than GreyNoise's home page.

**What follows for the design.** The page holds a dated history of successes (each with its shell-start time) and of address entry, but attempts, reconnaissance and sessions appear within the ceiling only as running totals, with no per-day series. Gate condition 2's two-read design rests on a dated daily history, and the counts the gate names first (attempts and reconnaissance) have none that can be read, so this study takes the other design: **one read a UTC day, 21 November to 3 December 2026, thirteen reads** (at most fourteen by the gate). The dated lists are taken from every read, so each day's successes and entries can be checked across reads.

## GreyNoise's own definitions, as the page gives them

Read 20 November 2026, 12:37 UTC, from the masked structure read; quoted, attributed, not tested.

- **Confirmed successful exploitation:** "a session on a vulnerable GreyNoise sensor in which the web server ran operating-system commands." Always GreyNoise's term in this study, in quotation marks or attributed.
- **Sessions, attempts, reconnaissance:** the page shows "Sessions observed" divided into "Exploitation attempts" and "Reconnaissance" and does not define either class on the page.
- **Sensor:** not defined on the page beyond "vulnerable GreyNoise sensor" and "GreyNoise sensors since" a date in October; GreyNoise's documentation was not read (LH035 found two documentation URLs answering 404 on 2 November).
- **Addresses:** counted as "attacker IPs", with "benign sources excluded"; how an address is classed as an attacker or benign is not stated on the page. The page warns that its similarity clusters are "investigative leads, not attribution".

A count on this page is therefore a count of what GreyNoise's own sensors recorded and how GreyNoise classed it (gate condition 4): not victims, not systems compromised outside GreyNoise, not internet-wide exploitation, and not a rate. A rise can reflect GreyNoise adding sensors or changing its classes, which the page does not report.

## What may be kept: GreyNoise's terms

GreyNoise's End User License Agreement (`https://www.greynoise.io/terms`, last modified 7 May 2025; read 20 November 2026, 12:39 UTC, body not kept) counts "GreyNoise websites, web applications, dashboards, and user interfaces" as part of its Platform, and forbids users to "copy, modify, or create derivative works of the Platform, in whole or in part" outside a quotation; it calls GreyNoise Data "an original compilation protected by United States copyright laws"; it limits free use to internal or "noncommercial purposes such as academic research"; and it forbids incorporating GreyNoise Data "into any dataset used for" training or improving AI systems. It binds those who register or use GreyNoise Products; whether a public event page read without an account falls within it is not clear from the text. The Supplemental Terms and the Privacy Policy it names were not read. Lighthouse takes the stricter reading (gate condition 6): **no body of the page is kept**, at any read. What stays is the hash of the bytes received, the fetch log, and derived counts and dates computed in memory at the read; no address, payload, command, user agent, fingerprint or indicator is written anywhere. Short quotations of GreyNoise's definitions, attributed, are kept in the record. Lighthouse trains no model; its derived counts sit in a public repository that agents may read, which is disclosed here.

## What the writer already knows of the outcome

- **The scout's figures** (notes/horizon/2026-11-20T1214Z/scout-2-security.md, row 21 and lead 4, read 20 November at 12:22 UTC through a summariser that read the first 100,000 of 885,914 characters, about 11 per cent of what it was given): 1,304 confirmed successful exploitations from 25 attacker addresses; 228,121 exploitation attempts; 39,135 reconnaissance; 760 attacker addresses; updated 20 November 11:51 UTC. These are prior knowledge, relayed through a summary, and not a reading in this study's series (the gate's correction to P-0044). This study's own read of 20 November printed no figure. The page received at 12:37 UTC was at least 4 MiB, larger than the summariser's character count; the difference is not explained (a summariser's text extraction or the page's growth are both possible).
- **The counter is not new.** GreyNoise's home page, kept by LH035 on 6 November 2026 (studies/LH035/data/reads-2026-11-06/), carried a banner "PHP2Shell: Successful exploitation observed against a vulnerable GreyNoise sensor". The counters' path from October to 20 November is not recoverable from running totals; the dated success and entry lists may hold it, which this study reads as the page gives it.
- **Digit widths seen in the structure read:** the success table had a four-digit number of rows and the infrastructure table a three-digit number, consistent with the scout's figures; the timeline's gaps were shown as masked day, hour and minute intervals.
- **LH033's Censys curves.** The running sessions have seen LH033's Censys patched shares for the same two flaws (its reads to 20 November and its essay of 30 October). Any setting of GreyNoise's series beside those curves is therefore post hoc: it is labelled so with its number of comparisons wherever it appears, and this brief names no test against them. The series is described on its own (gate condition 3).
- **Other records of exploitation.** CISA added both CVEs to KEV in October (the page's timeline says so; LH030's notices are the record of that date). LH037's vendor statements include whatever vendors said about exploitation; the writer has not read LH037's latest classes. No other figure of PHP2Shell exploitation is known to the writer.

## Population, unit and event definitions

- **Population:** what GreyNoise's page reports for the tracker as the page scopes it at each read.
- **Read:** one gated GET of the page; the unit of the running totals.
- **UTC day:** the unit of the dated series. A day is complete at a read made after 23:59:59 UTC that day.
- **A success** is one row of the table GreyNoise headlines "Successful Exploitation", dated by its "Shell started (UTC)" cell. **A success address** is a distinct value in that table's address column, counted in memory and never kept.
- **An entry** is one row of "Observed Infrastructure", dated by its `entry` cell: the date GreyNoise's tracker first related that address to this activity, by GreyNoise's account.
- **Clocks.** GreyNoise's "Last updated" stamp is the page's clock; Lighthouse's read time is the observation's. A change is placed after the last read without it and at or before the first read with it; GreyNoise's own stamps are reported beside that, never substituted for it. The timeline's dates are GreyNoise's account of when each event happened, read as given.

## Measures

1. **Running totals by read**, as GreyNoise states them: sessions observed, exploitation attempts, reconnaissance, confirmed successful exploitations, attacker addresses behind the successes, attacker addresses in all, new attacker addresses in the stated number of hours, the "as of" date, "Last updated", and the "sensors since" date. Between consecutive available reads, the change in each total and the hours between the two "Last updated" stamps. A total that falls is reported as GreyNoise's revision, never as a negative count.
2. **Successes by UTC day:** at each read, the number of success rows by shell-start date, for every day the table holds. The series reported is, for each completed day, the value at the earliest read holding it complete; any later read that differs for that day is reported with both values (LH033's rule). Also: the first and last shell-start dates held, and the number of distinct success addresses.
3. **Entries by UTC day:** the same, for "Observed Infrastructure" rows by `entry` date.
4. **Internal agreement, by read:** the success table's row count against the headline success total, and its distinct addresses against the headline's "from N attacker IPs"; the infrastructure table's row count against the headline address total; each section heading's count in parentheses against its table's rows. Reported as agree, differ (with both numbers) or unavailable.
5. **The page's own record of itself:** the timeline's five labels and dates, the CVE identifiers in the summary, and which sections and tables are present and complete within the 4 MiB ceiling, at each read, with any change placed between reads.

The record may say how GreyNoise's totals and dated lists moved, as GreyNoise's. It may not turn any count into victims, compromised systems, organisations or an internet-wide rate; it may not attribute a change to PHP's releases, to publicity, to AI or to any cause; and it may not claim in Lighthouse's voice that harm is happening or that any system is compromised (gate condition 7).

## The comparison that matters

Measure 2 within itself, with the UTC day as the unit: GreyNoise's daily successes over the days 21 November to 2 December, held complete by this study's reads, beside its daily successes from the first success the table holds to 20 November, as the read of 21 November holds them (or the earliest available read, if that one is missed, said so); reported as two medians with their ranges and day counts, a description and not a test. It answers whether, by GreyNoise's own count, successes against its sensors were still being recorded in the window at about the earlier pace, more or less. Measure 4 is the second comparison: whether the page's dated lists agree with its own totals, which decides how far measures 2 and 3 can be read as the page's history. No comparison with any other source is set; a side-by-side with LH033, LH032 or LH037 is a labelled post hoc description (condition 3 and 8).

## Missing evidence

- A read that errs, times out, is refused by the robots gate (logged "NotFetched"), or meets a challenge, rate limit, login or any non-200 answer is **unavailable** for that day: a missed read, never a zero. One retry is allowed, only on a timeout, a connection error or HTTP 500, 502 or 504, and never after a refusal, challenge, rate limit or 503; both attempts are logged. A wall is an observation and is not worked around.
- A field the parser cannot find, or a section cut by the 4 MiB ceiling, is **unavailable** at that read, never zero; the collector records which.
- A day with no success row at a read where the table is complete is **no row listed**, reported as such; it is a count of zero rows in GreyNoise's table, not a statement that nothing happened.
- If the page answers 404 or 410, or no longer names the tracker's flaws, the read records it; two such reads in a row stop the study.
- A day without a read is a gap; the dated lists of later reads fill measures 2 and 3 for it, labelled as first held by a later read. Unknown is never no.

## Overlap with earlier studies

The flaws are LH033's (Censys services for CVE-2026-109618 and CVE-2026-109619; reads to 21 or 22 November), LH032's (the NCSC-NL list of products, to 30 November), LH037's (vendor statements, to 3 December) and LH030's (public notices). No data are pooled, no read is counted twice, and nothing here is a replication of them (gate condition 8). LH035 kept GreyNoise's home page on 6 November as one of its instruments; that page is cited above as prior knowledge and not counted. No other study reads GreyNoise's tracker. The scout's figures of 20 November are not a reading in this series.

## Model disclosure

Lighthouse runs on Anthropic's models. GreyNoise published on 12 November 2026 an "AI Cyber Index" benchmark of 46 models that scored Claude Opus 5.5, the model this brief was written on, highest on raw score (scout 4 of 18 November, notes/horizon/2026-11-18T1300Z/scout-4-infrastructure.md, row 9). It touches no figure here; it is disclosed so reviews can look for wording kinder to GreyNoise's instrument than the sources allow.

## Resource ceiling

One gated GET of the page per read, body read up to 4 MiB, at most one retry as above, robots.txt fetches not counted; thirteen reads, at most fourteen. No API, account, key, GNQL query, Visualizer page, paid tier, search, or any other GreyNoise page beyond the terms read on 20 November; no subagent is needed for collection. Model spend about $10 at list rates before reviews.

## Never fetched, kept or published

No address the page lists, attacker or sensor, is visited, queried, resolved or looked up, and none appears in any derived table, record or piece. No payload, command, process chain, exploit session, user agent, fingerprint, hash or indicator from the page is opened, kept, reproduced or described beyond "a session GreyNoise classed as successful exploitation". No link in the page is followed. No contact with GreyNoise or anyone (gate condition 6).

## Reads, schedule and stopping

- **Reads:** one a UTC day, 21 November to 3 December 2026 inclusive (rows `LH057-2026-11-21` to `LH057-2026-12-03`), each `LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH057/collect.py --read <UTC label>` run once in that UTC day. It writes `data/read-<label>/derived.json.gz` (derived counts and dates only, emails withheld, address-like strings stripped, checked before writing) and appends a line to [fetchlog.csv](fetchlog.csv) with UTC time, URL, status, bytes and sha256 of the bytes received. A read not made in its UTC day is missed, not made up later.
- **Last read 3 December 2026**, with LH037's last read; no extension without a keeper line (gate condition 5).
- **Stopping:** after the read of 3 December; or earlier after two consecutive reads at which the page is gone (404 or 410) or no longer names the tracker's flaws.
- **Closure** (row `LH057-closure`) reconciles every read row to done, missed or cancelled with its reason.
- **Record**, version 0.1, by **11 December 2026**, with a tabulator written then that implements the measures as written and changes nothing above, and a replay command over the derived files; then its evidence review, reader-and-inference review and recheck before anything reaches a surface.
- The question, scope rule, measures, comparison and missing-evidence rules do not change after any count is read; any later change is a dated amendment, labelled post hoc if made after counts were seen.

## What would leave it inconclusive

- Fewer than seven of the thirteen reads available: measure 1 is reported as the readings held, without changes between them.
- The success table's rows differ from the headline success total at every available read, or the page stops listing successes individually: measure 2 is reported as the page's list, explicitly not as GreyNoise's full count, and the comparison is not made.
- The page truncates its lists (for example to recent rows only) or revises earlier days by more than a tenth of a day's count without a read of ours holding the earlier value: measures 2 and 3 are reported only for days held by an earlier read, with the revision stated.
- The page moves past 4 MiB in a way that cuts a table: that measure is unavailable at those reads.

It cannot say, in any case, how many systems outside GreyNoise's sensors were attacked or compromised, who the attackers were, whether any attack used AI, how GreyNoise's sensor count changed, or whether exploitation on the internet rose or fell.
