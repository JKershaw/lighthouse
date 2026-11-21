# R-0111: review of the collectors' keep wiring and the 11 further removals, 21 November 2026

**In short.** A fresh agent reviewed the uncommitted change that routes every live collector's page bodies through `scripts/lh_fetch.py` (`keep_decision`, `save_body`, `write_derived`) and removes or withholds 11 more bodies. The helpers are correct, every live collector listed writes page bodies only through them, nothing a kept body looks like changed, the git-ignored run copies are ignored, and every replay and tabulator I re-ran gives output identical to HEAD. Three things must be fixed first: four collectors that gate fetching on their own now make an extra, unlogged robots.txt request through `save_body`; LH042's new not-kept path leaves nothing its quotation check can read once the run copy is gone; and three downstream scripts skip records that weren't kept and still write tables that look complete. Separately, and older than this change, LH045's two scheduled collectors still fetch under `urllib.robotparser` rather than the keeper's rule.

Reviewer: a subagent of the Watch run of 21 November 2026 (Claude Code, Claude Opus 5.5), dispatched by that run's driver. No web request was made. Nothing was committed, and no file other than this note was written in the repository. Runs were made in scratch copies of the working tree and of HEAD (`git archive HEAD`), with network and robots.txt stubbed.

## What I read

AGENTS.md (Rules that matter); notes/keeper/2026-11-21-robots-intent.md; notes/keeper/robots-intent-2026-11-21/collectors_wired.md and removal_check.txt (new section); `git diff` of all 47 changed files and the untracked files; scripts/lh_fetch.py, robots_gate.py (`check`, `may_keep`, `_robots`) and robots_rules.py (`may_keep_groups`, `page_reservation`); every changed collector and downstream script in full where the diff touched it; LH044 collect.py's robots handling (`robots_outcome`, `robots_for`, `do_wayback`, `do_httparchive`, `do_statements`); LH042 check_quotes.py and extract_index.py; LH045 `derive`; LH041 tabulate.py; LH047 fetch.py `robots_for`; LH057 collect.py; the three REMOVED.md files, the derived and withheld files, and the derive_kept.py scripts; schedule/due.csv (open observe rows); .gitignore; notes/robots-tokens-2026-11-08.md (table of collectors' robots handling).

## What I ran, and what came out

1. Compile, all 42 changed or new .py files (`compile()` under `python3 -I`): 42 of 42 compile.
2. `python3 -I scripts/robots_rules.py`: 0 failed. `python3 -I studies/LH044/scripts/test_lh044.py`: 0 failed.
3. Tabulators, run in the working-tree copy and the HEAD copy, stdout and stderr concatenated: LH033 tabulate.py on read-2026-11-19T1422Z and read-2026-11-21T1414Z, LH034, LH036, LH054 and LH040 tabulate.py. 3,003 lines, byte-identical between the two copies; written output files identical to the repository's.
4. Replays, same two copies: LH041 replay.sh and groupings.py `--read 2026-11-08T1910Z`, LH042 replay.sh (problems: 0; 91 admitted counts; 57 series), LH047 replay.sh, LH048 test_tabulate.py (15 tests OK). Identical apart from the unittest timing line. The HEAD copy still holds LH042 035.body and LH047 008.body, so this also confirms the two removals change no output.
5. LH045 `--derive-only` on both epoch reads and all three IETF reads, in both copies: identical (updates.csv 727 and 749 rows; census.csv 562, 604 and 604 drafts).
6. Stubbed fetch harness (network blocked at the socket; `RobotsGate._robots` returns either `User-agent: *` allow, or GPTBot disallowed with `*` allowed; no `--read` invoked, functions called directly), with keeping forced off and then on:
   - LH049 `fetch`: off, no file, `body_kept` "no: GPTBot (a training or archiving crawler) is refused at this path"; on, meta.raw.gz holding the body with its email address withheld.
   - LH056 `attempt`: off, no file and `body_kept` set; on, q.attempt1.raw.
   - LH055 `main`: off, only fetch_log.jsonl, robots/A1.json and text/A1.txt.withheld-local, with the log carrying `body_kept`, text_sha256 and text_chars; on, bodies/A1.raw.gz and text/A1.txt.
   - LH050 `main`: off, bodies/n1.derived.json (URL, final URL, read time, status, hashes, title, standard note) and n1.html.withheld-local; on, bodies/n1.html.
   - LH044 `Recorder.get`: off, pages 0001 (host with a parsed robots.txt, `robots_body` path) and 0002 (host without one, gate path) each withheld with the keeper's placeholder, a .withheld.json record and a run copy, readlog `body_kept` set, while the robots.txt body 0003.b is kept; on, all three bodies kept and `body_kept` empty.
7. `keep_decision` cases: noai meta, `X-Robots-Tag: noai` and `tdm-reservation: 1` all refuse; `robots_body=None` keeps ("robots.txt gave no rules"), but a noai meta still refuses; `*` disallow, CCBot, ClaudeBot and ia_archiver each refuse with the right reason; a robots.txt answering 404 through the gate keeps; robots "error" through the gate refuses with "not fetched"; `gate=` uses the given gate; `save_body` gzips by suffix or `gzip_body=True` and withholds email addresses.
8. `git check-ignore -v` on a run-copy path for LH042, LH044, LH050 and LH055: each is matched by `.gitignore:7:*.withheld-local`. No `*.withheld-local` file is tracked or present, and `git add -A --dry-run` lists none. So `git add -A` can't commit them; only `git add -f` could.
9. Grep for `page_reservation|may_keep|body_removed|NOT_KEPT_NOTE` in .py files outside scripts/, excluding derive_kept.py: only the audit tools in notes/keeper/robots-intent-2026-11-21/ (sweep_may_keep.py, live_hosts_survey.py, untied_files.py) match. No collector holds its own copy.
10. The 11 removals: LH044's nine `<n>.b` files are byte-equal to `keeper_placeholder('<n>.withheld.json')`, and each has a .withheld.json record with hash, size, title and `derived` class/detail/marker/echoes. LH042 035.derived.json and LH047 008.derived.json are present, and so is each study's data/REMOVED.md. No tracked .md, .py, .csv or .sh still names 035.body or evidence-1/008.body outside the removal notes.

## Findings

### Must fix

1. **Four collectors now make an extra, unlogged robots.txt request.** `save_body` with no `robots_body` or `gate` asks lh_fetch's module gate, which reads robots.txt itself unless it already read that host to gate the fetch. Collectors that gate fetching through lh_fetch are fine. These ones aren't:
   - **LH044**, for every host whose robots.txt answered 4xx (`robots_outcome` gives state "unavailable", groups `[]`, so the page is fetched, but `robots_for` is set only for "parsed"). The same happens for web.archive.org and cdn.httparchive.org on a 4xx. LH044 logs and caps (HOST_CAP 7) every request it makes, and this one bypasses both.
   - **LH045 collect_epoch.py and collect_ietf.py**: each already reads robots.txt itself.
   - **LH047 fetch.py**: its brief allows no other request to an audited site, and LH047 exists to audit Lighthouse's own requests.
   - **LH046 fetch_sources.py** (not scheduled).

   So the change does alter what is fetched, against check (3). Where that extra read fails, the body is refused with the reason "not fetched" for a page that was in fact fetched. The fix: pass the robots.txt the collector already read (`robots_body=bytes`, or `None` for a 4xx). For LH044, record 4xx hosts in `robots_for` as `(None, n)`, which `content_signal.decide` already accepts. For LH047, pass its parsed text, or `None` for allow-all. For LH045, pass the body it read.

2. **LH042's new not-kept path leaves nothing to check quotations against after the run.** fetch.py writes no NNN.body, no .withheld.json and no derived file; only the git-ignored run copy. `check_quotes.py` (run by replay.sh) then falls through to `body.read_bytes()` and raises FileNotFoundError for any admitted count or relayed quote taken from such a body. The scheduled LH042-research-2026-12 re-search admits counts from arbitrary publishers, and axios.com already refuses keeping. The Content-Signal branch in the same file already has the right form: `content_signal.write_withheld` gives a record, a placeholder and a run copy, and check_quotes, extract_index and extract_dashboard all read that form. Use it here too, as LH044 does, with the quotations admitted from the page kept in its `extract`.

3. **Three downstream scripts skip records that weren't kept and still write tables that look complete.** The note on stderr is the only sign. LH041 tabulate.py and groupings.py `continue` past a record with `raw` null. Because `keep_export` is decided per ecosystem, a refused export would drop that whole ecosystem's records from the tables, which reads as a zero. LH045 collect_ietf.py `derive` prints "census incomplete" to stderr, then writes census.csv and authors.csv from the remaining bodies with no mark. That contradicts the change's own rule that a missing body is unavailable, never a zero. Stop with "readings unavailable", as LH040 tabulate.py does, or mark the outputs incomplete. For LH041, a better fix is to keep the record fields the tables use, not `raw`. None of these hosts refuses keeping today, so no current output is wrong.

4. **Older than this change, and outside its diff: LH045 still fetches outside the keeper's rule.** collect_epoch.py (read LH045-epoch-2026-11-22, due tomorrow) and collect_ietf.py (LH045-census-2) gate with `urllib.robotparser` for their own User-Agent only. collect_epoch.py also fetches when robots.txt answers 5xx. notes/robots-tokens-2026-11-08.md listed them as "own UA, robotparser"; the sweep of 9 November converted LH042 but not these two. The rule of 8 November (every token of the provider, strictest wins; 5xx means not fetched) isn't applied. Switch them to lh_fetch's `check`/`urlopen` before the next read. That would fix item 1 for LH045 too.

### Optional

- `keep_decision` through a gate returns `(False, 'not fetched')` whenever the gate refuses fetching the URL: a redirect's final URL, a different access mode, or an unreachable robots.txt. That string now lands verbatim in permanent logs as `body_kept: no: not fetched`. R-0109 raised the same point. Computing `may_keep` whatever the fetch decision, with an honest reason for unreachable robots.txt ("robots.txt unreachable: not kept"), would fix it.
- `lh_fetch.may_keep` is no longer used by any collector, and `keep_decision` covers its job. Remove it, or make it a thin alias, and update the module docstring, which still describes only `urlopen`, `redacted` and `UA`. The `robots_body` branch of `keep_decision` ignores truncation. LH044 passes only complete parsed files, but the docstring could say callers must.
- Double work: LH048, LH049, LH053 and LH056 run `redact_bytes` a second time only to get `emails_withheld`. `save_body` could return the count. LH042 computes `hpairs` twice in adjacent branches.
- Kept-file bytes changed in two places, though content didn't. LH038 suse_clocks.py and LH055 previously wrote with `gzip.open` (header mtime set) and now with `gzip.compress(mtime=0)`, so the decompressed content is identical. LH044 now withholds email addresses from bodies with a NUL in their first 4 KiB, which it used to keep as they were; no kept LH044 body is like that.
- LH032's read step copies software/*.md from a git clone of the NCSC-NL repository into the repo. collectors_wired.md doesn't say whether the keep rule applies to that copy. One sentence deciding it would close the question.
- LH046 fetch_sources.py makes no robots.txt check before fetching (already noted in collectors_wired.md). It isn't scheduled; gate it or retire it before reuse.
- collectors_wired.md's description of LH044 ("a host it has not parsed falls back to lh_fetch's gate") should change with must-fix 1.

## Claims checked and found true

Every study with an open observe row is covered. LH013 (BigQuery), LH057 (derived counts only, checked in its code), LH058, the MS365 watch and the media sweep keep no page body. LH039's rows aren't open. In every listed collector, every write of a fetched page body goes through `save_body`, or through `keep_decision` for LH041's JSONL lines. The only direct writes left are robots.txt copies (LH044, LH045, LH047), response headers, our own derived JSON, run copies, and LH041's OSV zip in TMPDIR outside the repository. When a body is kept, its file name, place and log fields are unchanged; new fields and `body_kept` appear only when it isn't. The User-Agent each collector uses to read robots.txt is unchanged: lh_fetch's UA is the same string the replaced RobotsGate(UA) calls used. LH038 policies.py's missing imports are fixed. The 11 removals have derived or withheld files, REMOVED.md entries and verified outputs (items 4, 5 and 10 above).

## Recheck, 21 November 2026

Same reviewer, same rules: no web request, no `--read`, nothing committed, and no file written other than this note. I took a fresh scratch copy of the working tree and stubbed the network at the socket, so `RobotsGate._robots` counts every robots.txt read it makes.

**What I ran.** All 44 changed or new .py files compile. `scripts/robots_rules.py` reports 0 failed, and so does `test_lh044.py`. The tabulators (LH033 on its two latest reads, LH034, LH036, LH054, LH040) produce output byte-identical to the HEAD copy's from the first round. The replays (LH041 replay.sh and groupings.py, LH042 replay.sh, LH047 replay.sh) give the same results as before: groupings identical to HEAD, mismatches 0; LH042 problems 0, 91 counts, 57 series. LH045 `--derive-only` on all five reads gives the same counts as HEAD. The written outputs are identical to the repository's. I also ran a new stub harness (h3), with keeping forced off and then on, over LH044 `Recorder.get`, LH042 fetch.py (`--label`), LH047 `main`, LH045 `Reader.robots`/`get` and LH046 fetch_sources.py. Finally, I made direct calls to `RobotsGate.may_keep`.

**The four must-fix items: all fixed.**
1. **No second robots.txt read.**
   - LH044 now records 4xx hosts in `robots_for` as `(None, n)`, in do_read, do_wayback, do_httparchive and do_statements. In the harness, a page on a 4xx host made no gate read and was kept ("no rules"). A page on a parsed host was withheld with the keeper's placeholder and a record.
   - LH047 passes the robots.txt it already read for the final host. A redirect to another host reads that host's file once, through its own logged `robots_for`; that request is new and is logged. Robots.txt unreachable means not kept.
   - LH045 now gates through `RobotsGate` with `save_body(gate=GATE)`. The robots.txt row is still kept and logged first, and its file names and numbering are unchanged.
   - LH046 goes through lh_fetch's `urlopen`, and `save_body` uses the same gate.

   In every case the harness counted exactly one robots.txt read per host, both ways.
2. **LH042 now leaves a record.** The not-kept path writes `content_signal.write_withheld(..., keeper=True)`: a placeholder, a .withheld.json record and the run copy. With the run copy deleted, `check_quotes.body_text` returns the record's extract instead of crashing.
3. **No more complete-looking tables.** LH041 tabulate.py and groupings.py now stop with "readings unavailable" on any `raw` that wasn't kept. The spot-check table marks an OpenSSF file that wasn't kept in its own row. LH045's census `derive` now stops rather than writing. The derives of retained reads are unchanged.
4. **LH045 is on the keeper's rule.** Brief amendment 0.3 is dated before the 22 November read and says no outcome was read for it. Both collectors now apply the 8 November rule (5xx or unreachable means not fetched) with Lighthouse's User-Agent. The amendment records that the User-Agent changed.

**The driver's three changes: correct.**
- `RobotsGate.may_keep` now answers from the cached robots.txt whatever the access mode. A `*` disallow refuses in either mode. Where only Claude-SearchBot is refused, `check` refuses fetching but `may_keep` gives (True, ...) instead of "not fetched". A 5xx or truncated file gives "robots.txt unreadable in this run; not kept".
- `lh_fetch.may_keep` is gone, and nothing imports it.
- The AGENTS.md bullet and LH033's amendment now name `save_body`, `keep_decision` and `write_derived` as the one path.

**`write_withheld(keeper=)`.** The default is unchanged for Content-Signal callers. LH044's nine withheld placeholders are byte-equal to `content_signal.keeper_placeholder(...)`. The keeper's placeholder exists in one place only; LH044's own copy is removed.

**Nothing must still be fixed.** Optional:
- (a) For a quotation admitted from a body withheld under the keeper's rule, LH042's agent must copy the quotation into the record's `extract`. Otherwise check_quotes reports "QUOTE NOT FOUND", loudly but on a correct quotation. One line in LH042's procedure would cover it.
- (b) collectors_wired.md line 54 still says an unparsed LH044 host "falls back to lh_fetch's gate". The fallback now covers only hosts LH044 never read.
- (c) lh_fetch's module docstring still describes only `urlopen`, `redacted` and `UA`.
- (d) `check()`'s `info["keep_body"]` still says "not fetched" for a refused URL. That's true there, but `may_keep` is now the authority for keeping.
