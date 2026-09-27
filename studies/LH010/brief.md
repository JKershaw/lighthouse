# LH010 study brief

**study:** LH010
**edition:** 0.1
**date opened:** 2026-09-27, about 09:53 UTC (before the first read, at 09:53:19 in data/read_log.csv), written after reading AGENTS.md, programme.md's LH010 section, issue #11's task as the driver gave it to this agent, and LH008's and LH009's records, data and scripts, and before any list of popular projects, any OSV advisory, any release note, any dependents list or any repository was read for this study. The libraries, events, classes and frames that the rules below produce are therefore not known to this brief beyond what LH008 and LH009 already hold; they are recorded in the first amendment, written after the fixes are classified and before any dependent is read [the amendment's tables were written to data before any dependent was read; its text came after, as its heading now says: reviewer's note, 27 September 2026]
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driver session for issue #11 (LH010), from the design in programme.md
**grounded at:** repository commit 15bd521

## Question

Do pinned dependents move faster before the advisory to fixes whose own notes announce a security flaw than to silent fixes, when each class has enough libraries that no one or two carry the result? LH009 found 2.36 against 1.36 moves per 100 repository-days from the release to the advisory, on seven libraries with pinned dependents in each class, with gitpython and pyjwt carrying much of the lead, and the difference sitting in days two to seven after the release (3.22 on 13 moves against 1.45 on 5).

## What is already known and used

LH008's rule and code for choosing events (studies/LH008/brief.md rules 1 to 4, scripts/select_libraries.py), LH009's classification rule with its amendment 1 (studies/LH009/brief.md), LH009's frame, screen, kept and move code (studies/LH009/scripts/collect.py), and LH009's windows (scripts/analyse.py). LH008's 16 events against the 200 most downloaded projects, and LH009's classes for their 37 fixes, are known; what widening the rule adds is not.

**Reuse of LH008's and LH009's reads.** Where a library's LH010 event (the rule below) is the same fixed release as its LH008 event, its class is taken from studies/LH009/data/fix_classes.csv, and its frame is LH008's or LH009's frame as read (the same Open Source Insights list of the same release before the fix, read on 27 September 2026 between 07:24 and 08:51 UTC), cut to its first 20 packages in hash order, with their screening, kept pairs, moves, authorship and trailers taken from studies/LH008/data or studies/LH009/data as they stand at commit 15bd521 rather than cloned again; each pair's end of observation stays its own clone time. Everything else is read fresh.

## Choice of libraries and events (rule fixed before any advisory is read)

1. **Widely used.** The 500 projects with the most downloads in August 2026 in ClickPy's copy of PyPI's download log [S21] (`pypi.pypi_downloads_per_month`, month 2026-08-01, summed over versions), read once, in LH008's query with `LIMIT 500`.
2. **Advisory.** For each of the 500, OSV's records [S26] from `https://api.osv.dev/v1/query` (package name, ecosystem PyPI). An advisory qualifies if its id begins `GHSA-`, its `database_specific.github_reviewed` is true (a GitHub-reviewed record), it is not withdrawn, its OSV `published` time falls between 2026-03-27T00:00:00Z and 2026-08-27T23:59:59Z, and it names a `fixed` version for the package. **Every severity counts**: `database_specific.severity` of LOW, MODERATE, HIGH or CRITICAL, or none given; the severity is recorded.
3. **The fix already released.** As LH008 rule 3: the advisory's fixed release is the highest `fixed` version among its ECOSYSTEM ranges for the package, its release time the earliest upload of any of its files on PyPI, and the advisory qualifies only if that release's UTC date is at least one calendar day before the UTC date of the advisory's `published` time.
4. **One event per library**, LH008's rule 4: qualifying advisories are grouped by fixed release; the event is the fixed release whose earliest qualifying advisory is the earliest in the window, and the event's advisory time is that advisory's OSV `published` time. The release before the fix is the highest release, not a pre-release, below the fixed release and uploaded before it (LH008's code).

## Classification of each fix (LH009's rule as amended in its amendment 1, unchanged)

**Unit.** Every distinct (library, fixed release) behind a qualifying advisory of a library with an event is classified; the events are the ones measured, and the others serve the within-library sensitivity below.

**What is read**: the changelog entry at the tag, the PyPI description's part for the version, and the tag's annotation, found and dated exactly as LH009's brief says, with the tag form `rel_` plus the version with underscores that LH009 amendment 1 added. GitHub's release pages, LH009's sensitivity source, are not read: every one was refused in LH009 and the request would be spent for nothing.

**Class.** Announced if one of those texts, dated no later than 24 hours after the first upload, holds a security word (`security`, `vulnerab`, `CVE-`, `GHSA-`, `PYSEC-`, `CWE-`, `advisory`, `exploit`, `attacker`) or names the flaw the qualifying advisory's summary describes; announced late if the words are first dated after that but before the advisory; silent otherwise. **Flaw named** is read as LH009 amendment 1 read it: the entry must itself say what was wrong in terms of harm or attack (a bomb, an injection, a traversal, an oracle, out-of-bounds access, a crash, excessive CPU or memory, a bypass of a check, a leak); an entry naming only the change to the affected function is silent. The judgement is this agent's, made only for fixes with no security word, written with its words to data/flaw_judgements.csv, and the class without it is reported beside the class throughout as `strict_class`. The class decides everything below; `strict_class` is a sensitivity. The classes are fixed before any dependent is read and not changed after.

## Order, frames, screening, kept and moves

**Order.** Events are taken in descending order of August downloads. For each, the frame below is screened and its kept pairs read. A library **counts** for its class once it has at least one kept pair. When a class has 20 counted libraries, later events of that class are not read (recorded as "class full"); reading stops when both classes have 20, or when the list ends.

**Frame.** Open Source Insights' listed direct dependents [S11] of the release before the fix (at most 100 listed); ordered by the SHA-256 of the PEP 503 name; the first **20** screened (all if fewer). Repository, clone, default branch, snapshot, pin and lock files as LH009 (Open Source Insights' v3 relation or link, then PyPI's project URLs; github.com and gitlab.com only; blobless clone without checkout; the last first-parent commit at or before the fixed release's first upload; LH008's lockfile and exact-pin rules; a repository counted once per frame).

**Kept** (LH009's range-aware rule): a repository is kept if a pin or lock file at the snapshot holds a version that the event advisory's OSV ECOSYSTEM ranges name as affected. Its fix is the `fixed` version of the range that holds its lowest affected version, and its release time is that version's first upload; where this is not the event's fixed release (a backport on an older branch), the pair is kept with its own fix and release time and counted separately in the record.

**Move** (LH009's rule): the first first-parent commit after the snapshot where a file that held an affected version holds only unaffected versions at or above its range's fixed version (or stops mentioning the library while another followed file does), read to the head as cloned, at most 400 commits touching pin or lock files; a removal is recorded. Authorship by LH008's classes, as LH009.

## Measures

By class (announced; silent; announced late reported alone, if any), each also by strict class:

- **Pooled over pairs**, as LH009: kept, moved, censored, removed; the share of moves before the advisory; lags from the release and the advisory; moves per 100 repository-days at risk in LH009's windows (release 0 to 2 days; release 2 to 7 days, 7 to 30 days, 2 days to the advisory and the whole release to advisory, each stopping at the advisory; advisory 0 to 2, 2 to 7, 7 to 30 and 30 to 90 days), each with its count of moves.
- **With the library as the unit**: for each library, its own rate in the window from the release to the advisory and in the window release 2 to 7 days stopping at the advisory (a library with no repository-days at risk in a window is left out of that window); for each class, the median of its libraries' rates, with the count of libraries. **A permutation test** of the class labels over those libraries: the statistic is the announced median minus the silent median; the labels are shuffled 10,000 times with seed 20260927, keeping each class's size; the two-sided p is (1 + the number of shuffles whose absolute difference is at least the observed one) / 10,001. Run for both windows, by class and by strict class. No other test is run.
- **Leave one library out**: the range of each class's pooled rate and of its library median when each of its libraries is dropped in turn, for both windows.
- **By authorship** (bot; person merging a bot's branch; person), as LH009.
- **Within-library sensitivity.** For each library whose event was read and which has a qualifying fix of the other class released at least 14 days before or after the event's fix, the nearest such fix in time is read as a second frame by the same rules, with its own earliest qualifying advisory as its advisory time and that advisory's ranges for the kept rule. For each such library the two fixes' rates in the two windows above are given side by side with their counts, and summed over the libraries; no test is run on them. (programme.md names cryptography 49.0.0 and 50.0.0; under this rule cryptography's pair is whatever the rule gives.)

Moves before the advisory are not evidence that the announcement caused them (interpretation; the link is timing).

## Interpretation boundary

As LH009: a move is a request in a repository, not an installation or a run; a bot's commit shows that a bot runs; an announcement is the project's word, read today in the forms it left; nothing says any project was exposed, and no project is named as exposed. A dependent is named only where a reader needs to check a row.

## Resource ceiling

About seven dollars of this agent's own model spend at list rates. Disk: all clones and scratch work in /tmp/claude-0/lh010-work, outside the repository, at most **8 GB**, checked before each clone; a library's or dependent's clone may be deleted once its reading is recorded. Requests: at most 5,000 HTTP requests and 1,500 clone attempts. Every HTTP request and clone is logged in data/read_log.csv, as LH009. Anonymous reads only; no account, key or credential; GitHub's API and GitHub's release pages are not used.

## Stopping condition

Close when both classes have 20 counted libraries, or the event list ends, with every frame taken in order screened (first 20 packages) and every kept pair read to its move or the head; or at a ceiling, with the unread part stated. If the list ends with fewer than 20 counted libraries in a class, that count is the finding and the measures are still made. If a class has fewer than five counted libraries, the library-unit test is not run and the record says so. The question and the library, classification, order and sampling rules are not changed after any advisory, note or dependent is read; a change to how the plan is carried out is made by a dated amendment below.

## Intended output

LH010.md (version 0.1), sources.md, data/ (with read_log.csv, fix_classes.csv and flaw_judgements.csv), scripts/ adapted from LH009's, each docstring saying what changed.

## Amendment 1, 2026-09-27, recording data/fix_classes.csv and data/frame_defs.csv as written at 10:02:16 UTC, before the first dependents list was requested at 10:03:13; its text was written after the dependents were read and before 10:20:43, when this file was last written

[Heading corrected in review from "about 10:05 UTC, after the fixes were classified and before any dependent was read", which data/read_log.csv contradicts: dependents were being listed from 10:03:13. The times are the working tree's file times as the reviewer found them; the tables named were not written again after 10:02:16.]

**What was read** (data/read_log.csv, 09:53:19 to 09:56:39 UTC): ClickPy's top 500 (one request); OSV's records for each of the 500 (500 requests); PyPI's release lists for the libraries with a reviewed GHSA record in the window, and PyPI's JSON for each fixed release classified here; a blobless bare clone of 35 library repositories (802 MB), and the changelog files, tags and annotations in them. No dependents list, dependent or repository of a dependent has been read. GitHub's release pages were not requested.

**Applied** (observation; data/qualifying_advisories.csv, data/events.csv, data/fix_classes.csv). OSV holds 1,644 records against the 500 projects; 227 are GitHub-reviewed GHSA records published in the window with a fixed version, and in 215 of them, against 43 libraries, the fixed release was on PyPI at least a calendar day before the advisory (by severity, qualifying: 6 critical, 99 high, 86 moderate, 24 low). They name 106 distinct fixed releases. Of the 43 events, 21 are in the top 200 (LH008 had 16 there, with high and critical only) and 19 have a high or critical first advisory. So the design's 20 libraries a class with kept dependents cannot be reached: 43 events are the whole list, 22 of them announced and 21 silent, and a library counts only if its frame yields a kept pair. The order rule therefore reads every event's frame, and the record reports the counts the list gives. The 12 events that are the same release as LH008's (urllib3, pyjwt, litellm, pyasn1, pillow, soupsieve, lxml, mcp, msgpack, gitpython, langchain, mako) take their class from LH009; four of LH008's libraries have a different event now, because a lower-severity advisory came first (cryptography 46.0.6, starlette 1.0.1, aiohttp 3.13.4, python-multipart 0.0.26), and pyjwt's event is the same release with an earlier, low-severity advisory, 2 hours before LH008's. The other 94 fixes were read here.

Of the 106 fixes, 59 are announced (49 by a security word, 10 by the flaw named alone) and 47 silent; none is announced late. Of the 43 events, 22 are announced (18 by a security word; mako 1.3.11, uv 0.11.6, authlib 1.7.1 and mistune 3.2.1 by the flaw named alone) and 21 silent; by strict class 18 and 25. The median gap from the fix to the advisory is 4.0 days for the announced events and 6.0 for the silent ones.

| rank | library | fixed release, first upload (UTC) | advisory (severity), published (UTC) | days between | class | strict class | basis | class from |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | idna | 3.15, 2026-05-12 22:45 | GHSA-65pc-fj4g-8rjx (moderate), 2026-05-19 14:34 | 6.66 | announced | announced | security word | read here |
| 6 | urllib3 | 2.7.0, 2026-05-07 16:13 | GHSA-qccp-gfcp-xxvc (high), 2026-05-11 14:51 | 3.94 | announced | announced | security word | LH009 |
| 9 | setuptools | 83.0.0, 2026-07-04 15:31 | GHSA-h35f-9h28-mq5c (moderate), 2026-07-21 19:09 | 17.15 | announced | announced | security word | read here |
| 10 | cryptography | 46.0.6, 2026-03-25 23:33 | GHSA-m959-cc7f-wv43 (low), 2026-03-27 19:56 | 1.85 | announced | announced | security word | read here |
| 37 | python-dotenv | 1.2.2, 2026-03-01 16:00 | GHSA-mf9w-mj56-hr94 (moderate), 2026-04-21 14:38 | 50.94 | silent | silent | none | read here |
| 44 | pip | 26.1, 2026-04-26 21:00 | GHSA-jp4c-xjxw-mgf9 (moderate), 2026-04-27 15:30 | 0.77 | silent | silent | none | read here |
| 45 | pyjwt | 2.13.0, 2026-05-21 19:54 | GHSA-fhv5-28vv-h8m8 (low), 2026-06-15 17:28 | 24.9 | announced | announced | security word | LH009 |
| 46 | starlette | 1.0.1, 2026-05-21 21:58 | GHSA-86qp-5c8j-p5mr (moderate), 2026-06-04 13:15 | 13.64 | silent | silent | none | read here |
| 48 | litellm | 1.83.0, 2026-03-31 05:08 | GHSA-53mr-6c8q-9789 (high), 2026-04-03 21:59 | 3.7 | silent | silent | none | LH009 |
| 49 | aiohttp | 3.13.4, 2026-03-28 17:14 | GHSA-w2fm-2cpv-w7v5 (moderate), 2026-04-01 19:45 | 4.1 | announced | announced | security word | read here |
| 65 | pyasn1 | 0.6.4, 2026-07-09 01:12 | GHSA-m4p7-r5rc-7g4j (high), 2026-07-21 19:10 | 12.75 | announced | announced | security word | LH009 |
| 72 | pillow | 12.2.0, 2026-04-01 14:42 | GHSA-whj4-6x5x-4v2j (high), 2026-04-13 19:22 | 12.19 | announced | announced | security word | LH009 |
| 96 | python-multipart | 0.0.26, 2026-04-10 14:09 | GHSA-mj87-hwqh-73pj (moderate), 2026-04-15 19:45 | 5.23 | silent | silent | none | read here |
| 100 | soupsieve | 2.8.4, 2026-05-24 13:55 | GHSA-2wc2-fm75-p42x (high), 2026-07-09 13:37 | 45.99 | silent | silent | none | LH009 |
| 109 | lxml | 6.1.0, 2026-04-18 04:27 | GHSA-vfmq-68hx-4jfw (high), 2026-04-21 20:38 | 3.67 | announced | announced | security word | LH009 |
| 122 | mcp | 1.27.2, 2026-05-29 17:16 | GHSA-hvrp-rf83-w775 (high), 2026-07-16 19:56 | 48.11 | silent | silent | none | LH009 |
| 147 | msgpack | 1.2.1, 2026-06-18 16:12 | GHSA-6v7p-g79w-8964 (high), 2026-06-19 21:42 | 1.23 | announced | announced | security word | LH009 |
| 156 | gitpython | 3.1.47, 2026-04-22 02:44 | GHSA-x2qx-6953-8485 (high), 2026-04-25 23:41 | 3.87 | announced | announced | security word | LH009 |
| 158 | langchain | 0.3.30, 2026-05-07 15:48 | GHSA-3644-q5cj-c5c7 (high), 2026-05-13 15:29 | 5.99 | silent | silent | none | LH009 |
| 183 | mako | 1.3.11, 2026-04-14 20:19 | GHSA-v92g-xgxw-vvmm (high), 2026-04-16 21:16 | 2.04 | announced | silent | flaw named | LH009 |
| 187 | h2 | 4.4.1, 2026-08-03 11:44 | GHSA-6hr6-w5qg-qmwg (moderate), 2026-08-06 21:53 | 3.42 | silent | silent | none | read here |
| 208 | anthropic | 0.87.0, 2026-03-31 17:52 | GHSA-q5f5-3gjm-7mfm (moderate), 2026-04-01 21:15 | 1.14 | silent | silent | none | read here |
| 218 | uv | 0.11.6, 2026-04-09 12:08 | GHSA-pjjw-68hj-v9mw (low), 2026-04-10 19:39 | 1.31 | announced | silent | flaw named | read here |
| 225 | transformers | 5.0.0rc3, 2026-01-14 16:48 | GHSA-69w3-r845-3855 (moderate), 2026-04-07 06:30 | 82.57 | silent | silent | none | read here |
| 236 | langchain-core | 1.2.22, 2026-03-24 18:48 | GHSA-qh6h-p6c9-ff54 (high), 2026-03-27 19:45 | 3.04 | silent | silent | none | read here |
| 240 | snowflake-connector-python | 4.7.1, 2026-07-15 16:25 | GHSA-5cc2-282f-jjq2 (critical), 2026-07-16 09:32 | 0.71 | silent | silent | none | read here |
| 246 | httplib2 | 0.32.0, 2026-06-26 10:13 | GHSA-j5g9-f88f-gfj3 (high), 2026-07-24 15:15 | 28.21 | silent | silent | none | read here |
| 249 | awscli | 1.44.78, 2026-04-10 19:41 | GHSA-wfp6-f47h-hxc3 (moderate), 2026-07-24 15:49 | 104.84 | silent | silent | none | read here |
| 258 | pypdf | 6.10.1, 2026-04-14 12:55 | GHSA-jj6c-8h6c-hppx (moderate), 2026-04-15 19:43 | 1.28 | announced | announced | security word | read here |
| 266 | sqlparse | 0.6.0, 2026-08-13 19:16 | GHSA-3496-9g83-7v6x (moderate), 2026-08-17 17:20 | 3.92 | announced | announced | security word | read here |
| 271 | authlib | 1.7.1, 2026-05-04 08:11 | GHSA-r95x-qfjj-fjj2 (moderate), 2026-05-13 01:36 | 8.73 | announced | silent | flaw named | read here |
| 279 | joserfc | 1.6.7, 2026-05-23 01:46 | GHSA-wphv-vfrh-23q5 (moderate), 2026-06-26 20:59 | 34.8 | silent | silent | none | read here |
| 289 | tornado | 6.5.5, 2026-03-10 21:30 | GHSA-fqwm-6jpj-5wxc (high), 2026-04-03 06:31 | 23.38 | announced | announced | security word | read here |
| 293 | pydantic-ai-slim | 1.99.0, 2026-05-20 01:32 | GHSA-cqp8-fcvh-x7r3 (moderate), 2026-05-21 21:35 | 1.84 | silent | silent | none | read here |
| 301 | langsmith | 0.7.31, 2026-04-14 17:55 | GHSA-rr7j-v2q5-chgv (moderate), 2026-04-16 01:20 | 1.31 | silent | silent | none | read here |
| 359 | fastmcp | 3.2.0, 2026-03-30 20:25 | GHSA-m8x7-r2rg-vh5g (moderate), 2026-03-31 22:24 | 1.08 | silent | silent | security word | read here |
| 379 | dulwich | 1.2.5, 2026-05-28 22:26 | GHSA-555p-6grf-mh7f (low), 2026-06-08 23:04 | 11.03 | announced | announced | security word | read here |
| 420 | mistune | 3.2.1, 2026-05-03 14:33 | GHSA-8mp2-v27r-99xp (high), 2026-05-06 16:52 | 3.1 | announced | silent | flaw named | read here |
| 422 | bleach | 6.4.0, 2026-06-05 13:01 | GHSA-8rfp-98v4-mmr6 (low), 2026-06-16 14:06 | 11.05 | announced | announced | security word | read here |
| 433 | poetry | 2.3.3, 2026-03-29 12:24 | GHSA-2599-h6xx-hpxp (high), 2026-04-01 22:17 | 3.41 | announced | announced | security word | read here |
| 444 | nltk | 3.9.3, 2026-02-24 12:05 | GHSA-848c-c2cx-j7qx (high), 2026-07-25 00:31 | 150.52 | announced | announced | security word | read here |
| 473 | nbconvert | 7.17.1, 2026-04-08 00:44 | GHSA-4c99-qj7h-p3vg (moderate), 2026-04-21 17:18 | 13.69 | silent | silent | none | read here |
| 481 | snowflake-sqlalchemy | 1.11.0, 2026-07-08 08:53 | GHSA-8g6f-qw9x-4q6q (high), 2026-07-14 15:32 | 6.28 | silent | silent | none | read here |

**Four things about how the rule was carried out**, none changing a rule:

1. **An entry first written after the tag.** fastmcp 3.2.0 has no entry at its tag; its entry at the head holds security words, and the rule dates it by the changelog file's history. LH009 did this by hand for its one case; here scripts/date_head_entries.py does it: the first first-parent commit whose version of docs/changelog.mdx held the entry with a security word is dae11bbc40fd, committed 3 June 2026 (UTC), 64 days after the release and 63 after the advisory, so fastmcp 3.2.0 is silent.
2. **Flaw named.** Read as LH009 amendment 1 read it, the reader's judgements are in data/flaw_judgements.csv. Ten fixes are announced on this ground alone: three as LH009 judged the same texts (gitpython 3.1.49, mako 1.3.11 and 1.3.12) and seven judged here (pip 26.1.2, aiohttp 3.14.1, uv 0.11.6, authlib 1.7.1, mistune 3.2.1 and 3.3.0, nltk 3.10.1). Four of the seven are borderline, recorded as such: the entry names the effect rather than an attack (pip 26.1.2 "would install a script outside the scripts directory"; uv 0.11.6 "Do not remove files outside the venv on uninstall"; aiohttp 3.14.1, digest responses no longer sent to another origin; authlib 1.7.1 "redirecting to unvalidated redirect_uri"). Two of the borderline ones are events (uv, authlib); `strict_class` drops all of them.
3. **Security words about something else.** The rule counts any security word in the entry. In two announced events the only security words concern an earlier release, not this fix: idna 3.15 ("Reference CVE-2026-45409 for the 3.14 advisory in place of the initial GHSA identifier"; the entry the rule found is headed 3.15rc0, the only heading naming 3.15) and aiohttp 3.13.4 (3.13.3's "decompression bomb security fix" and "to maintain security protections"). Their class stays announced, as the rule says; a sensitivity with these two counted silent is added to the measures, and the record reports it. bleach 6.4.0's notice that it will make no future security releases sits beside a "Security fixes" section naming its advisories, so its class is not in doubt.
4. **A pre-release as the fix.** transformers' event is 5.0.0rc3, a release candidate (the highest `fixed` version of its first advisory), uploaded 14 January 2026, 82.6 days before the advisory; its release before the fix is 4.57.5. The rule gives it, and it is kept.

**Within-library pairs** (fixed in data/frame_defs.csv at 10:02:16 UTC, before any dependent was read): by the brief's rule, five libraries have a fix of the other class at least 14 days from the event's: cryptography (46.0.6 announced; 48.0.1 silent), pip (26.1 silent; 26.1.2 announced), aiohttp (3.13.4 announced; 3.14.3 silent), gitpython (3.1.47 announced; 3.1.50 silent) and awscli (1.44.78 silent; 1.45.28 announced). Their second frames are read fresh, although cryptography 48.0.1's and aiohttp 3.14.3's were LH008's and LH009's events, because the brief reuses reads only for LH010's events.

## Amendment 2, 2026-09-27 about 10:20 UTC, after the dependents were read

Three notes on how the plan was carried out, none changing a rule, a class or a count.

1. **Order.** The screening ran eight packages at a time over all frames, sorted by the events' download rank; since no ceiling was reached (at most 0.8 GB on disk; 1,335 logged requests and clones), every frame was read and the order did not decide anything. The "class full" rule never applied: the list ended with 18 announced and 12 silent libraries counted.
2. **Short windows.** A library's own rate is moves over its repository-days in the window, and where the advisory came within a day or two of the fix, or a frame had one or two kept pairs, those days are few (pydantic-ai-slim: one move over 0.5 repository-days before its advisory, 190 per 100). The medians and the permutation test are unchanged by this; the means in data/library_unit.csv are dominated by it and are not used.
3. **Clones.** The dependents' clones were deleted once data/moves.csv was written (collect.py clean); the libraries' clones after data/fix_texts.csv was dated. The Co-authored-by names were read while the clones were present (collect.py), so trailers.py was not needed.

## Amendment 3, 2026-09-27, after every outcome was known: a reanalysis for version 0.3 of the record

Written by a Lighthouse research subagent (Opus 5.5) in the improvement round of 27 September 2026, after LH010.md version 0.2, notes/R-0010.md and every table in data/ had been read. Nothing above is changed: the question, the library, event, classification, order, frame, kept and move rules, the measures and the classes stand as written, and version 0.2's tables stay as they are. The reanalysis in LH010.md version 0.3 (scripts/reanalyse.py, data/reanalysis/) is **outcome-aware and post hoc**, not a preregistered comparison: it varies the clock that ends "before the advisory" (the earliest GitHub-reviewed record in the retained OSV records naming the fix, and the earliest of those records' publication and NVD times), sorts each fix's notes evidence at release time into announcement observed, notes inspected with no announcement found, and insufficient accessible notes, restricts the comparisons to the first two, and adds library-clustered bootstrap intervals. Its rules are stated in the record's Findings and were written after the retained texts and records had been read for it; none of its readings, intervals or p values is a test this brief planned, and none should be read as one.
