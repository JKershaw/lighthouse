# LH009 study brief

**study:** LH009
**edition:** 0.1
**date opened:** 2026-09-27, about 08:45 UTC, written after reading programme.md's LH009 section, issue #10's text (as given to this agent by the driver) and LH008's record, data and scripts, and before any release note, changelog, tag, PyPI description, dependents list or repository was read for this study. The class of each fix and the frames that the rules below produce are therefore not known to this brief; they are recorded in the first amendment, written after the fixes are classified and before any dependent is read
**written by:** a Lighthouse research subagent in Claude Code, model Opus 5.5 (claude-opus-5-5, as reported by its harness), dispatched by the driver session for issue #10 (LH009), from the design in programme.md
**grounded at:** repository commit 76043cb

## Question

When a fixed release says in its own notes that it fixes a security flaw, do pinned dependents move to it before the advisory is published, more than they move to a fix released silently? LH008 found 19 of 73 moves to a fix coming before the advisory, and read no release notes, so "before the advisory" there was not "before anyone was told".

## What is already known and used

LH008's 68 qualifying advisory records (studies/LH008/data/qualifying_advisories.csv): GitHub advisory records rated HIGH or CRITICAL, published 27 March to 27 August 2026, against 16 of the 200 most downloaded PyPI projects, each naming a fixed release uploaded at least a calendar day before the advisory. They name 37 distinct fixed releases. LH008's events.csv gives each of the 16 libraries one event by LH008's rule 4 (the fixed release whose earliest qualifying advisory is the earliest in the window; the event's advisory time is that advisory's OSV `published`), and its release before the fix.

## Classification of each fix (rule fixed before any note is read)

**Unit.** Each of the 37 distinct (library, fixed release) pairs is classified; the 16 events are the ones measured below.

**What is read, for each fixed release.** Three sources, all the project's own words:

1. **The changelog entry at the tag.** The library's repository is the one its PyPI project URLs name (source, repository, code, homepage, in that order), on github.com or gitlab.com. A blobless clone without checkout is made in /tmp/claude-0/lh009-work, outside the repository. The **tag** is the first of `v{V}`, `{V}`, `{name}-{V}`, `{name}-v{V}`, `{name}=={V}`, `release-{V}` that exists, where V is the version and name the PyPI name (any case); if none exists, the shortest tag containing V as a whole token (not followed by a digit or a dot and digit, not preceded by a digit or a dot). The **changelog files** are the text, Markdown or reStructuredText files at the tag (or with no extension), at most four directories deep, whose name (case-insensitive) begins with `change`, `history`, `news`, `release` or `whatsnew`, or which are under a directory named `changelog`, `changes`, `news`, `release-notes`, `release_notes`, `releasenotes`, `releases` or `whatsnew` and name V in their path. The **entry** is the part of such a file from the first line that begins, after markup (`#`, `*`, `` ` ``, `[`, `=`, `-`, `:`) and an optional `v`, `Version`, `Release`, `Revision`, `:version:` or the project's name, with V as a whole token, to the next line of the same kind naming a different version. Where the tag has none, the file on the default branch at the head is read instead and marked, and its history decides when the entry was written (below).
2. **The PyPI description.** `info.description` from `https://pypi.org/pypi/<name>/<V>/json`, which is fixed with the release's upload. Only the part about V is read, found by the same entry rule; a description with no part naming V carries no notes for it.
3. **The tag's annotation.** The message of the tag object, where the tag is annotated; a lightweight tag has none.

**Sensitivity source, not used for the class.** GitHub's release page for the tag, `https://github.com/<owner>/<repo>/releases/tag/<tag>`, read as HTML (not GitHub's API), where it is served anonymously; many projects put their notes only there. Its class is reported beside the main one and never replaces it.

**Class.** A fix is **announced** if the entry, the part of the description or the annotation for V contains (case-insensitive) `security`, `vulnerab`, `CVE-`, `GHSA-`, `PYSEC-`, `CWE-`, `advisory`, `exploit`, or `attacker` (a **security word**), or describes the flaw that the qualifying advisory's summary describes (**flaw named**; the reader's judgement, recorded with the words that decided it, and reported separately so a reader can drop it). Otherwise it is **silent**. The words that decided the class, or the absence of any entry, are written to data/fix_classes.csv with the source and the file or field they came from.

**When.** The announcement must be dated at or before the release: the PyPI description is dated at the upload; a changelog entry read at the tag is dated at the tag's commit's committer time, and a tag annotation at its tagger time. If that time is more than 24 hours after the release's first upload, or the entry was read at the head because the tag lacked it, the date is the committer time of the first commit on the changelog file's history (first parent, from the release onward) whose version of the entry contains the deciding words. The entry at the head is also read for every fix; where it holds a security word the tag's entry did not, the commit that added it is found the same way. A fix whose words first appear after the release is **announced late** if they appear before the advisory and **silent** otherwise, and a late fix is reported by itself, not pooled into either class.

## Choice of libraries (rule fixed before any dependent is read)

All 16 libraries, each with its LH008 event (events.csv), fixed release, advisory time and release before the fix, and no other: the whole of the frame that LH008 drew its four from. LH008's four fix frames (urllib3, cryptography, pyjwt, starlette) are not read again: their kept repositories, moves and times are taken from LH008's data as it stands at commit 76043cb (read 27 September 2026, 07:24 to 07:47 UTC), and their events are classified like the others. The twelve others are read as LH008 read its fix frames, below. No comparison frames are read; LH008's comparison is not repeated.

If, after classification, either class holds no event, the study stops there and the record says so. If either class holds fewer than three events, the measure is still made and reported by library, and no difference between the classes is claimed. The events are classified before any dependent is read, and the class of an event is not changed after.

## Frame, screening, pin and move (LH008's rules, unchanged except where named)

For each of the twelve libraries: Open Source Insights' listed direct dependents of the release before the fix (at most 100 listed); ordered by the SHA-256 of the PEP 503 name; the first **60** screened (all if fewer); repository from Open Source Insights' v3 relation or link, then PyPI's project URLs, github.com and gitlab.com only; a blobless clone without checkout over full history; the snapshot is the last first-parent commit on the default branch at or before the fixed release's first upload; pin and lock files as LH008's brief and its amendment 2 define them; a repository counted once per frame.

**Kept** (one change from LH008's code, which relied on every one of its four advisories' ranges starting at or near zero): a repository is kept if some pin or lock file at the snapshot holds a version that the event's advisory's OSV affected ranges name as affected (introduced at or below it, fixed above it, and not a later `introduced`). Its **fix** is the `fixed` version of the range that holds it, and its **release time** is that version's first upload on PyPI; normally the event's fixed release. The **move** is the first first-parent commit after the snapshot where a file that held an affected version holds its range's fixed version or later (or stops mentioning the library while another followed file does), read to the head as cloned, at most 400 commits touching pin or lock files; a removal is recorded as such. Authorship by LH008's classes (bot; person merging a bot's branch; person), read from git with its corrected branch pattern (LH008 amendment 3).

## Measures, by class

For each event and pooled by class (announced; silent; announced late, if any): kept repositories, moves, censored, removed; the **share of moves that came before the advisory** (the question's measure) and that share of the kept; median and quartiles of the lag from the release and, for moves after it, from the advisory; and the **rate of moves per 100 repository-days at risk** in the windows release 0 to 2 days (before every advisory, since each came at least a calendar day later; where an advisory came within 2 days the window stops at it), release +2 days to the advisory, advisory 0 to 2 days, 2 to 7 and 7 to 30 days, each with the number of moves it stands on. The gap from release to advisory differs from event to event, so the share of moves before the advisory is set beside the rate from release to advisory, which does not depend on the gap's length. Rates are pooled over repository and event pairs; an event with many kept repositories weighs more, so each class's rate is also given with each event's own count. No significance test is run; counts are given with every share and rate. By authorship class as LH008. Moves to the fix before the advisory are not evidence that the announcement caused them (interpretation; the link is timing).

## Interpretation boundary

As LH008: a move is a request in a repository, not an installation or a run; a bot's commit shows that a bot runs; nothing says any project was exposed, and no project is named as exposed. An announcement is the project's word, read today in the forms the project left. A dependent is named only where a reader needs to check a row.

## Resource ceiling

About six dollars of this agent's own model spend at list rates. Network: all clones in /tmp/claude-0/lh009-work, at most **4 GB** on disk, checked before each clone; at most 16 library repositories for the classification and 720 packages screened for the frames. Every HTTP request is logged in data/read_log.csv; each clone is one row. Anonymous reads only; no account, key or credential; GitHub's API is not used.

## Stopping condition

Close when all 37 fixes have been classified and every one of the twelve frames' first 60 packages (or the whole frame) has been screened and every kept repository read to its move or the head, or at the ceiling, with the unread part stated. The question, the classification rule, the library rule and the sampling rule are not changed after any note or dependent is read; a change to how the plan is carried out is made by a dated amendment below.

## Intended output

LH009.md (version 0.1), sources.md, data/ (with read_log.csv and fix_classes.csv), scripts/ adapted from LH008's.

## Amendment 1, 2026-09-27 about 08:50 UTC, after the fixes were classified and before any dependent was read

**What was read** (data/read_log.csv, 08:43:31 to 08:48:30 UTC): PyPI's JSON for each of the 37 fixed releases; a blobless bare clone of each of the 16 libraries' repositories (596 MB on disk); the changelog files, tags and annotations in them at each release's tag and at the head; GitHub's release page for each tag, which was refused (HTTP 403, every one, through this environment's proxy), so the sensitivity source gives nothing; then OSV's records for the twelve new events' advisories and PyPI's release lists for those twelve libraries. classify.py ran twice (08:43 and 08:46); the second run, with the change below, is the one in data/. The first run's reads are in the log.

**Two changes to how the rule is carried out**, neither changing a class that a reader of the first run could not predict:

1. **Tag form.** Mako tags its releases `rel_1_3_11`; the brief's forms found no tag, so the first run read its changelog at the head. The form `rel_` with the version's dots as underscores was added to the list and classify.py run again; the entry at the tag is the same as at the head, and the tag's commit (20:18 UTC on 14 April) is before the upload (20:19). This was done after the head's entry had been read.
2. **What "flaw named" was taken to mean.** The brief left this to the reader. Applied after reading the entries, and recorded here so it can be checked: the entry must itself say what was wrong in terms of harm or attack (a bomb, an injection, a traversal, an oracle, out-of-bounds access, a crash, excessive CPU, a bypass of a check); an entry that names only the change in the affected function ("Reject absolute paths in `StaticFiles.lookup_path`", "Add multipart header limits") is silent. Three fixes are announced on this ground alone (gitpython 3.1.49, mako 1.3.11 and 1.3.12), one of them an event (mako); data/fix_classes.csv gives `strict_class` without it, and the near misses are written out in data/flaw_judgements.csv. The 24-hour allowance the brief gives a tag's time is applied to every dated source.

**Applied** (observation; data/fix_classes.csv, data/fix_texts.csv). Of the 37 fixes, 19 are announced at the release (16 by a security word, 3 by the flaw named alone) and 18 are silent; none is announced late. [Corrected in review on 2026-09-27 from "18 ... (15 ... 3 ...) and 19", which did not match data/fix_classes.csv; see LH009.md Corrections.] Of the 16 events:

| library (August rank) | fixed release, first upload (UTC) | advisory (UTC) | days between | class | where the words are |
| --- | --- | --- | --- | --- | --- |
| urllib3 (6) | 2.7.0, 2026-05-07 16:13 | 2026-05-11 14:51 | 3.9 | announced | CHANGES.rst at the tag: a "Security" section naming both GHSA ids |
| cryptography (10) | 48.0.1, 2026-06-09 22:30 | 2026-06-15 20:12 | 5.9 | silent | CHANGELOG.rst: "Updated ... wheels to be compiled with OpenSSL 4.0.1" |
| pyjwt (45) | 2.13.0, 2026-05-21 19:54 | 2026-06-15 19:28 | 25.0 | announced | CHANGELOG.rst: a "Security" section naming the GHSA id |
| starlette (46) | 1.1.0, 2026-05-23 16:55 | 2026-06-15 20:16 | 23.1 | silent | docs/release-notes.md: "Reject absolute paths in `StaticFiles.lookup_path`" |
| litellm (48) | 1.83.0, 2026-03-31 05:08 | 2026-04-03 21:59 | 3.7 | silent | no changelog at the tag or the head, nothing in the description |
| aiohttp (49) | 3.14.3, 2026-07-23 01:52 | 2026-08-03 20:51 | 11.8 | silent | CHANGES.rst: "Fixed error message construction in the C HTTP parser" |
| pyasn1 (65) | 0.6.4, 2026-07-09 01:12 | 2026-07-21 19:10 | 12.8 | announced | CHANGES.rst: CVE and GHSA ids for each fix |
| pillow (72) | 12.2.0, 2026-04-01 14:42 | 2026-04-13 19:22 | 12.2 | announced | docs/releasenotes/12.2.0.rst: a "Security" section, "vulnerable to GZIP decompression bombs" |
| python-multipart (96) | 0.0.27, 2026-04-27 10:51 | 2026-05-06 21:56 | 9.5 | silent | CHANGELOG.md: "Add multipart header limits" |
| soupsieve (100) | 2.8.4, 2026-05-24 13:55 | 2026-07-09 13:37 | 46.0 | silent | changelog.md: "Limit total number of selectors processed in a pattern to prevent massive selector requests" |
| lxml (109) | 6.1.0, 2026-04-18 04:27 | 2026-04-21 20:38 | 3.7 | announced | CHANGES.txt, the tag annotation and the PyPI description: "fixes a possible external entity injection (XXE) vulnerability" |
| mcp (122) | 1.27.2, 2026-05-29 17:16 | 2026-07-16 19:56 | 48.1 | silent | no changelog file, nothing in the description |
| msgpack (147) | 1.2.1, 2026-06-18 16:12 | 2026-06-19 21:42 | 1.2 | announced | CHANGELOG.md: "Fix a segfault ..." and the GHSA id |
| gitpython (156) | 3.1.47, 2026-04-22 02:44 | 2026-04-25 23:41 | 3.9 | announced | changes.rst: "Address various security issues related to bypassing injection-protection" |
| langchain (158) | 0.3.30, 2026-05-07 15:48 | 2026-05-13 15:29 | 6.0 | silent | no changelog file, nothing in the description |
| mako (183) | 1.3.11, 2026-04-14 20:19 | 2026-04-16 21:16 | 2.0 | announced (flaw named) | changelog.rst: "could bypass the directory traversal check ..., allowing reads of arbitrary files" |

So each class holds eight events (seven announced if the flaw-named ground is dropped, mako moving to silent), and the study goes on. Two things a reader needs before the moves are read (interpretation): the announced events' advisories came sooner after their releases (median of the eight gaps about 3.9 days, against about 10.6 for the silent eight), so a share of moves before the advisory is not comparable between the classes without the rates, as the brief says; and a class is a property of one release of one library here, so class and library cannot be separated. Two announced notes named GHSA identifiers that GitHub had not yet published (urllib3, pyjwt), and one entry was edited after the release to add CVE numbers (pillow 12.2.0; the words at the tag already said "Security" and "vulnerable"). The litellm repository held a release-notes page for v1.83.0 from 16.5 hours after the upload until the documentation was moved out on 24 April; it is not at the tag or the head, so the rule does not read it, and its security words concern the 24 March supply-chain incident, not these advisories.

**Kept rule** (observation, data/event_advisory_ranges.csv). Ten of the twelve advisories' ranges start at zero; pillow's starts at 10.3.0 and mcp's at 1.23.0, so a repository holding a version below those is not kept. langchain's advisory has ranges for three packages (langsmith, langchain-classic, langchain); the langchain range is 0 to 0.3.30, so a repository on langchain 1.x is not affected and moving from 0.3.x to 1.x counts as a move.

## Amendment 2, 2026-09-27 about 09:10 UTC, after the moves were read

One correction, not changing a rule or a class. Amendment 1 says "Two announced notes named GHSA identifiers that GitHub had not yet published (urllib3, pyjwt)". Counted from data/fix_texts.csv, eleven of the 19 announced entries name GHSA identifiers ahead of GitHub's publication, four of them among the events (urllib3, pyjwt, pyasn1, msgpack). [The count of announced entries corrected in review on 2026-09-27 from 18; see LH009.md Corrections.]
