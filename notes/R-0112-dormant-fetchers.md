# R-0112: review of the second sweep, every remaining fetch script onto lh_fetch, 21 November 2026

**In short.** A fresh agent reviewed the uncommitted change that moves the 49 remaining fetch scripts onto `scripts/lh_fetch.py`'s gated `urlopen` and `save_body` and adds an offline self-test. Kept bodies, file names and fixed log fields come out as they did before in every script I ran, apart from the email withholding the rule asks for. Refusals log `body_kept` and write no body. The self-test passes and leaves `lh_fetch.py` and `robots_gate.py` behaving as they did. Two things must be fixed first. The note says LH012's replay shows no DIFF, but it fails at step 1, and this change adds one more file to that failure. And the curl replacements in LH005 and LH011 now follow redirects that robots.txt never checks, where curl followed none.

Reviewer: a subagent of the Watch run of 21 November 2026 (Claude Code, Claude Opus 5.5), dispatched by that run's driver. No web request was made, not even for robots.txt. No collector ran against the network, no key was read, nothing was committed, and the only file I wrote in the repository is this note (Python's git-ignored `__pycache__` files apart). I made the runs in scratch copies of the working tree and of HEAD (`git archive HEAD`, HEAD = 7523007), with urllib's `OpenerDirector.open` stubbed, sockets blocked and a stub `curl` on PATH for HEAD's curl scripts.

## What I read

AGENTS.md (Rules that matter, including the robots bullets of 8 and 21 November; Evidence; the study record rules under Writing); notes/keeper/2026-11-21-robots-intent.md; collectors_wired.md, all of it, including the new section "Every fetching script"; `git diff` of all 50 changed files; scripts/lh_fetch.py (all of it) and robots_gate.py's interface; the diffs and new versions of LH005, LH011 and LH019 common.py and collect.py, LH030 check.py, LH040 collect_prebrief.py, LH039 tabulate.py and LH006 registry.py; LH006 to LH010 common.py and their writes; LH011 and LH012 review/requery.py; LH016 review/replay-X2/x2_requery.py; LH044 collect.py, LH047 fetch.py and notes/robots-tokens-2026-11-08/fetch_sources.py where they keep bodies; LH012, LH013 and LH014 replay.sh; the snapshot hash files; and the "instruments" lines of the records whose scripts changed.

## What I ran, and what came out

| Check | Result |
|---|---|
| `py_compile` on every .py in studies/, notes/, essays/, scripts/ | all compile |
| `python3 -I scripts/lh_fetch.py --selftest` | 56 `ok`, 0 failed |
| `python3 -I scripts/robots_rules.py` | 0 failed |
| `python3 -I studies/LH044/scripts/test_lh044.py` | 0 failed |
| `git diff --quiet scripts/robots_gate.py scripts/robots_rules.py scripts/redact_emails.py` | unchanged; the diff to lh_fetch.py only adds lines (0 removed): one usage line, `_selftest`, `_FixedGate` and a `__main__` block |
| LH010, LH011, LH013 replay.sh | PASSED |
| LH041, LH042, LH046 replay.sh | ran; `git status` unchanged afterwards (outputs identical) |
| LH012 replay.sh | **replay FAILED** at step 1: `brief.md`, `scripts/collect_meta.py`, `scripts/common.py` FAILED their snapshot hashes; steps 2 to 8 same |
| LH014 replay.sh | REPLAY FAILED at step 1 only: brief.md differs from its snapshot; steps 2 to 5 same |
| LH039 tabulate.py `--packagist 2026-11-21T1415Z --out <scratch>`, new and HEAD | both outputs byte-identical |
| The note's grep (130 files, value-filtered writes) | 19 lines, as the note says |

Where the hash failures come from (`git show HEAD:<file> | sha256sum` against the snapshot files):

- LH012 at HEAD: brief.md and common.py already failed, and collect_meta.py verified. In the working tree collect_meta.py fails too. So **this change breaks collect_meta.py's snapshot hash**, and LH012's replay was already failing before it. brief.md verifies once the text from `\n- **Amendment, 9 November 2026` on is cut (checked in Python), so its failure, and very likely common.py's, comes from the 9 November robots sweep. The clone is shallow (95 commits, from 0cdcbfa on 19 November), so I couldn't get the exact commit from git log.
- LH014: brief.md is the same at HEAD and in the working tree (`git diff --quiet HEAD`), and its HEAD hash (3ec3dcef...) already differs from the snapshot (31c19166...). Cut at its 9 November amendment, it verifies. **This change didn't cause it**: it predates today, comes from the 9 November amendment, and no changed script is read by step 1. LH013's replay was fixed for the same cause on 19 November; LH012's and LH014's were not.
- No other retained hash file names a changed script: I grepped the whole repository, outside .git and harbour/.session/, for HEAD's SHA-256 of each of the 49 changed scripts, and the only hit was LH012's snapshot.

Spot runs with the network stubbed and `LIGHTHOUSE_PROVIDER=anthropic`. Modes: allow-all; `GPTBot` refused (fetching allowed, keeping refused); allow with a page carrying `<meta name="robots" content="noai">`; and `*` disallowed. Each stub page body held an email address.

| Script | HEAD vs new, allow-all | Keeping refused | Fetch refused |
|---|---|---|---|
| studies/LH019/scripts/collect.py `--snapshot` | `diff -r` of the snapshot directories empty (same .raw files, contents and log) | GPTBot: no .raw, `file` empty, `error` "body_kept: no: GPTBot (a training or archiving crawler) is refused at this path"; noai: the same with "meta robots: ..." | |
| studies/LH040/scripts/collect_prebrief.py `--third` | same file names; readlog.csv the same apart from times; each .raw differs only where the email address is now withheld (HEAD saved bodies as received); new makes 2 robots.txt requests, one per host | GPTBot and noai: no .raw for the refused bodies, `body_kept` column "no: ..."; the noai run kept the three ClickPy TSVs, which carry no reservation | `*`: "error: NotFetched: not fetched: disallowed by robots.txt ...", no body |
| studies/LH005/scripts/common.py `clickhouse()` through a driver (HEAD through stub curl) | r_q1.csv byte-identical; read_log.csv the same apart from times | GPTBot: no CSV; r_q1.csv.derived.json with the rows and "no: GPTBot ..." | |
| studies/LH030/feasibility/check.py | 7 .raw each; read_log.json the same apart from times; all 7 bodies differ only by email withholding | GPTBot: 0 .raw, no `file`, `body_kept` "no: GPTBot ..." | `*`: `error` "NotFetched: not fetched: disallowed by robots.txt ...", 0 .raw |

## Findings

### Must fix

1. **LH012's replay is reported as passing, and this change adds to its failure.** collectors_wired.md (last paragraph) says "LH011, LH012 and LH013 replay.sh (no DIFF)". LH012's replay prints `replay FAILED`: no output DIFFs, but step 1's snapshot check fails for brief.md and common.py (already failing at HEAD, from the 9 November amendment) and now for collect_meta.py too, which this change edited. Minimal fix: handle step 1 the way LH013's replay was fixed on 19 November. Verify brief.md up to `\n- **Amendment, 9 November 2026`, which I checked does verify. List `scripts/common.py` and `scripts/collect_meta.py` as changed after the snapshot and not verified, with a comment that their snapshotted versions are in git history (common.py before the 9 November sweep, collect_meta.py before this change, so at HEAD 7523007). Then correct the note's sentence. The same one-line cut would make LH014's step 1 pass, but that failure is older than this change, so it's optional (item 6).
2. **The curl replacements now follow redirects without asking robots.txt.** In LH005 and LH011 (text reads), curl ran without `-L` and followed no redirect. `lh_fetch.urlopen(req, timeout=...)` without `check_redirects=True` follows any redirect to any host with no robots.txt check. So a scheduled or manual rerun could request a URL the keeper's rule refuses. `save_body`'s keep decision uses the final URL, so keeping is still decided correctly; it's the fetch that isn't gated. LH012, LH013, LH014 and LH013's preflight already followed redirects ungated under curl `-L`, so for them this isn't a regression, but the same fix applies. Minimal fix: pass `check_redirects=True` in each `curl()` replacement and in preflight.py. Add `except NotFetched as e: return 'not fetched: ' + ..., ...` before the bare `except Exception`, so a refused redirect is logged as "not fetched", not as curl's `000`, which reads as no response. The docstrings' "urllib always does" then becomes "follows redirects, each checked against robots.txt". The other urllib collectors in this sweep (LH040, LH030, LH045 probe and so on) never checked redirects before either; giving them the same flag would be consistent but is optional.

### Historical fidelity (the main judgement)

- **No record is now wrong about how its evidence was collected.** The records' instrument lines ("curl 8.5.0", LH041's "by curl", LH006's "documentation pages were fetched with curl") describe the collection when it happened, and that stays true. Every script whose fetch mechanics changed now says in its docstring what it did before 21 November (for example LH005 and LH011: "Until 21 November 2026 this ran the curl command ... curl here did not follow redirects"; LH030: "before, urllib's urlopen with no robots check ... the 23 October bodies were saved as received"). No conclusion, figure or description of evidence changes, so **no record needs a Corrections line**. The 9 November sweep set the precedent of editing closed studies' scripts with a dated note, and this change follows it.
- **What a careful developer would add (optional):** in each script whose fetch path changed (LH005, LH011 to LH014 common.py, LH013 preflight.py, LH030, LH031, LH032, LH040, LH045 probe, the two notes/php-* collectors, LH046 refetch), one docstring line saying the evidence was collected with the earlier version, which is `git show 7523007:<path>` (HEAD before this change). Today a reader has to search history for it. LH012's and LH014's 9 November brief amendments say "every read goes through scripts/common.py's curl helper". That's accurate for its date, but a one-line dated addendum (curl helper replaced by lh_fetch's urlopen on 21 November, nothing read since) would stop a reader taking it as current. Optional.
- **Offline replays:** only LH012's breaks, through its script hash (must-fix 1). LH010, LH011, LH013, LH041, LH042 and LH046 replay as before. LH013's replay comment ("changed by the 9 November amendment") could also mention 21 November; its pointer to the pre-count versions at 4c9b77c^ is still right. Optional.

### Completeness (scripts not on lh_fetch's urlopen)

- **LH006 to LH010** (requests sessions gated by `check`): acceptable. Their only file writes are `write_csv` tables of parsed fields, and LH006's and LH007's registry caches now go through `save_body`. They aren't a second path for bodies.
- **LH011 and LH012 review/requery.py** (curl after `check`): acceptable. Neither writes a response; LH012's writes a header temp file and deletes it.
- **LH016 review/replay-X2/x2_requery.py**: the note says it writes no body. In fact it writes each ClickPy query's rows to x2_requery_data/<out>.csv. That's the response re-serialised and redacted, the same content LH005's and LH011's `clickhouse()` now save only through `save_body`. ClickPy's robots.txt answered 401 (no rules, keeping allowed) in today's survey, so nothing kept today breaks the rule. Optional: route that write through `save_body` (with the endpoint URL), or correct the note's classification. A second path in form, not in effect.
- **LH044 collect.py and prebrief.py, LH047 fetch.py, notes/robots-tokens fetch_sources.py**: acceptable. Each keeps page bodies only through `save_body` (with `robots_body=` from the robots.txt it read itself) and keeps robots.txt files directly, which is allowed.
- A broader grep (urllib, curl, requests, httpx, wget in .py, .sh and .js across studies, notes, essays, scripts, schedule and site) found no other fetcher that writes bodies. The site's service worker is the site's own.

### Self-test (item 4)

It covers what collectors_wired.md lists, and its stubs are restored in `finally`. Running `lh_fetch.py` with no argument now prints usage and exits 2, which is new but harmless. Gaps, optional: no check that a refused `urlopen` never reaches urllib (it can't, since `_require_allowed` raises first); no case for `check_redirects=False` following a redirect ungated, which would have caught must-fix 2; one provider only (`anthropic`).

### Other optional points

3. `write_derived` writes `extracted` without withholding email addresses. In the LH005 run above, the derived rows kept `someone@example.org`. `python3 -I scripts/redact_emails.py <dir>` before a commit catches JSON, so this is a backstop, not a leak. Redacting inside `write_derived` would make the one path complete.
4. LH005 `curl()`'s docstring says it returns "the response's header block". It returns only (status, body), and `head` is computed and unused.
5. LH039: packagist.py writes NAME.derived.json with the daily series, but tabulate.py stops ("readings unavailable") and doesn't read it. That's safe (unavailable, never zero) but leaves the derived file unused. repo.packagist.org's robots.txt answered 404 today, so it doesn't bite now.
6. LH014 replay step 1: cut brief.md at its 9 November amendment, as LH013's replay does. That failure predates this change.
7. LH030, LH031, LH032 and the php notes keep their own page User-Agent ("Lighthouse research observation"), which lacks the `Lighthouse-research` token the gate uses. The robots decision is right, but the request doesn't identify itself as the token whose rules it followed.

## Verdict

Not clear to release as is: two must-fix items (LH012 replay and the note's claim; redirects not gated in the curl replacements). Everything else is correct or optional.

## Recheck (21 November 2026, same reviewer, after the driver's resolution)

Same rules as before: no network, no commit, no code edits, and the only repository file written is this note. Run at about 18:55 UTC.

| Check | Result |
|---|---|
| `py_compile` on every .py in studies/, notes/, essays/, scripts/, schedule/ | all compile |
| `python3 -I scripts/lh_fetch.py --selftest` | 57 `ok`, 0 failed |
| `python3 -I scripts/robots_rules.py`; `python3 -I studies/LH044/scripts/test_lh044.py` | 0 failed; 0 failed |
| robots_gate.py | unchanged (`git diff` empty) |
| lh_fetch.py, lines removed | 2: write_derived's docstring tail and its `f.write`, now writing the JSON through `redacted()` (an intended change, covered by a new self-test check) |
| LH011 replay.sh | REPLAY PASSED |
| LH012 replay.sh | replay passed. brief.md verifies up to its 9 November amendment, 18 other files verify, and common.py and collect_meta.py are listed as changed after the snapshot |
| LH013 replay.sh | replay passed |
| LH014 replay.sh | REPLAY PASSED. brief.md, cut at its 9 November amendment, matches the snapshot; amendment 1 matches |

**Must-fix 1 (LH012 replay): resolved.** The step 1 change copies LH013's and names the reason, the dates and where the snapshotted versions live.

**Must-fix 2 (redirects): resolved.** All six call sites now pass `check_redirects=True` and catch `NotFetched` before the bare `except`. I tested them with a stubbed HTTPS handler (sockets blocked). Each `common.curl('https://start.test/a')` in LH005, LH011, LH012, LH013 and LH014 got a 302 to a host whose robots.txt says `Disallow: /`. Each returned `'not fetched: disallowed by robots.txt (robots https://refused.test/robots.txt, status 200, group *, rule Disallow: /...'` with an empty body, and each made exactly three requests: start.test/robots.txt, start.test/a and refused.test/robots.txt, never the refused page. With the redirect pointed at an allow-all host instead, each followed it and returned `'200'` and the body. I read LH013 preflight.py's handler rather than running it: a refused redirect sets status `not fetched` and the error text in `stderr`, and writes neither a .headers file nor a body (`hdrs` stays None).

**Optional changes taken: correct.** 47 of the 48 changed fetching scripts now carry the `git show 7523007:<path>` line, and each named path exists at 7523007. The 48th, LH039 tabulate.py, fetches nothing, and lh_fetch.py needs no such line. `write_derived` withholds email addresses from the whole serialised record, the JSON stays valid (the placeholder has no quotation marks), and the self-test checks this.

**Anything new:**

- **Must fix (small): one sentence in collectors_wired.md is now out of date.** Line 143 still says "LH014 replay.sh fails at step 1 only: brief.md differs from its snapshot hash ...". After the driver's fix it prints REPLAY PASSED. Correct it to say all four replays pass, and that LH014's step 1 now verifies brief.md up to its 9 November amendment.
- Optional: in LH012's and LH014's `get_text`, a read refused at a redirect (or with no response) still calls `save_body` with an empty body against the original URL, so an empty file is written to the scratch path while the log says "not fetched" or `000`. HEAD did the same on errors. The file holds no page content and the log is correct, so nothing is wrong, but skipping `save_body` when the status isn't 200 would be tidier.

**Verdict:** clear once the line-143 sentence is corrected. Nothing else must be fixed.
