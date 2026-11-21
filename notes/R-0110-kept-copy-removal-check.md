# R-0110: fresh check of the removal of kept page bodies (21 November 2026)

**In short.** Earlier on 21 November another agent removed 201 kept page bodies from studies/, from sites whose robots.txt refuses AI-training or archiving crawlers or all bots, and put a derived file of facts beside each. This check re-ran, independently, every output that records rest on before and after the removal, spot-checked 27 derived files against the original bodies and read logs, checked coverage and the LH033 collector. Every output is byte-identical except the one LH036 line already accepted; nothing must be fixed. Three optional points follow.

Checked on 21 November 2026 (finished about 15:50 UTC) by a fresh subagent on Claude Opus 5.5 (claude-opus-5-5) under Claude Code, Anthropic cloud, at commit fe42e00 (branch claude/festive-hypatia-defc4p, working tree clean when checked; the checkpoint2_extra.py change that was uncommitted when the task was set is in fe42e00). Offline: no web request was made, no key read from the environment, nothing in harbour/.session/ searched, no study script or data edited. I read AGENTS.md (Rules that matter, including the bullet of 21 November) and notes/keeper/2026-11-21-robots-intent.md first, and read removal_check.txt only after writing and running my own scripts, to compare.

Scripts and outputs, all in notes/keeper/robots-intent-2026-11-21/:
- [r0110_verify.sh](keeper/robots-intent-2026-11-21/r0110_verify.sh), output [r0110_verify_output.txt](keeper/robots-intent-2026-11-21/r0110_verify_output.txt). Replay: `bash notes/keeper/robots-intent-2026-11-21/r0110_verify.sh <empty scratch dir>` (makes three git worktrees in the scratch dir and removes them at the end).
- [r0110_spotcheck.py](keeper/robots-intent-2026-11-21/r0110_spotcheck.py), output [r0110_spotcheck_output.txt](keeper/robots-intent-2026-11-21/r0110_spotcheck_output.txt). Replay: `python3 -I notes/keeper/robots-intent-2026-11-21/r0110_spotcheck.py`.
- [r0110_coverage.py](keeper/robots-intent-2026-11-21/r0110_coverage.py), output [r0110_coverage_output.txt](keeper/robots-intent-2026-11-21/r0110_coverage_output.txt). Replay: `python3 -I notes/keeper/robots-intent-2026-11-21/r0110_coverage.py`.

One edit to a retained output: in r0110_verify_output.txt the diff line from LH036's check_fixes.py quoted about 200 characters of git.kernel.org's challenge page (a site refusing all bots); I cut it after its first four words, as removal_check.txt does.

## 1. Outputs rebuilt before and after

Comparison A: the original scripts on the bodies (git worktree at 240e6fb; checkpoint2_extra.py taken from main's commit 453a50e, since it did not exist at 240e6fb, which has every input it reads: main's side added only checkpoint files and that script to LH033 and LH039 after 240e6fb's base) against the changed scripts on the derived files (worktree at HEAD). Comparison B: HEAD's scripts with all 201 deleted bodies restored from 240e6fb against HEAD as it is, for the scripts that changed for other reasons or did not exist at 240e6fb. Every script wrote into its scratch worktree, never the repository.

| Script (invocation) | Result |
|---|---|
| LH033 tabulate.py, every one of the 14 reads under data/ (6 hold W3Techs bodies; I ran all, removal_check ran 6) | A: identical, all 14 (stdout and exit code) |
| LH034 tabulate.py, and tables.json | A: identical |
| LH034 review/R-0039_checks.py (line numbers in `<module>` frames and the tree path masked) | A: identical; both stop with the same FileNotFoundError in section D (dist-index of the 19 November read, absent since 9 November, before and after the removal). I did not run removal_check's copy limited to reads up to 5 November. |
| LH035 reread_check.py (from the study folder), and the quote_check.json it rewrites | A: identical |
| LH036 tabulate.py, and tables.json | A: identical |
| LH036 review/check_fixes.py (PYTHONHASHSEED=0) | A: one line differs, line 150, as expected: the eight-line text diff of the Anubis challenge pages becomes "text diff: not shown, the body was removed on 21 November 2026 (text sha256 differs)" |
| LH038 review/r0091_check.py | A: identical |
| LH039 tabulate.py --packagist 2026-11-14T1415Z --until 2026-11-14T1412Z, and --packagist 2026-11-21T1415Z --until 2026-11-21T1411Z (the two checkpoints' commands) | A: identical (tabulation, packagist.csv, stdout) |
| LH039 checkpoint2_extra.py (main's original on the bodies against HEAD's on the derived files) | A: identical (extra.txt and stdout); B: identical |
| LH040 tabulate.py --read 2026-11-09T1432Z, and tables/ | A: identical |
| LH038 scripts/timeline.py, review/r0105_check.py, review/r0106_offsets.py (version 0.4, from main) | B: identical |

The HEAD runs also reproduce the retained studies/LH039/checkpoints/2026-11-21-extra.txt and 2026-11-21-tabulation.txt and studies/LH038/scripts/timeline_output.txt byte for byte. Outputs are non-trivial (exit 0, from 382 bytes to 540 kB) except LH033's read 2026-10-25T0857Z, which holds no W3Techs or Censys file and prints only its label, in both trees. This agrees with removal_check.txt in every comparison it made.

## 2. Derived files spot-checked (27, seeded sample from every study)

LH032 2, LH033 5, LH034 2, LH035 2, LH036 2, LH038 2, LH039 7, LH040 2, LH049 2, LH056 1. For each: email addresses, longest extracted string, URL, read time and SHA-256 against the read log in the same folder, SHA-256 of the original body at 240e6fb, and every extracted value looked for in the original body.

- **No email address** in any of the 201 derived files (grep over all of them).
- **No page prose.** The longest strings in "extracted" across all 201 files are the derive script's own 178-character note in LH035's files; then short attributed quotes used by records (LH049's Socket phrases, at most 151 characters, each found in the body; LH038's two policy sentences, 107 and 84 characters; LH056's 64), W3Techs diagram captions (80) and version labels. All within "short attributed quotes".
- **URL, read time and hash.** All 27 match a read-log record holding the same URL, read time and SHA-256. The SHA-256 equals the hash of the original body as stored (gunzipped where .gz) in 26 of 27. The exception, LH049 socket_post, matches its read log, which records `emails_withheld: 2`: the stored body had two addresses withheld after hashing, so the log keeps the hash of the bytes received, as AGENTS.md says. Not a defect.
- **Facts against the body.** Every extracted value was found verbatim in the body's text, with these explained exceptions: W3Techs history column labels are normalised to "1 Dec 2025" and "<day> <Mon> <year>" for the read day (the page heads its table with a year row and day-month cells); LH035's quoted segments are stored lower-cased (found ignoring case; reread_check.py's output is identical, so its comparison is case-blind); LH036's text_sha256 is a computed hash, not page text. For one LH039 history page (w3h-71, 10 November) I compared the table row by row with the page's text by hand: same rows and values. The study-wide equality in section 1 is the stronger check of the facts records use.

## 3. Coverage

- 201 bodies deleted since 240e6fb, 201 derived files at HEAD, one to one by name stem; no derived file without a deleted body.
- All 186 paths in remove_list.tsv are among the deleted; the other 15 are the 8 LH039 files of 7 November and the 7 sweep files (LH032 antagonist.nl pages, LH040 pypi /pypi/ JSON) that removal_check.txt and the REMOVED.md files name.
- None of the 201 paths exists in the working tree.
- Each deleted file is named in its study's data/REMOVED.md: exactly (file and folder) for LH032, LH034, LH035, LH036, LH038, LH040, LH049 and LH056; by stated range for LH033 (48 = 6 reads x 8 files, matching the folders and names deleted) and LH039 (120 = 2 x 8 files on 7 and 8 November plus 13 reads x 8 files, matching). LH039's note that the stats and meta .body files kept from 9 November are Lighthouse's own robots-refusal notes is true of the one I opened (raw-2026-11-12T1415Z/stats-1.body).
- No W3Techs page remains anywhere under studies/ or notes/ (no plain or gzipped file containing W3Techs's footer text).

## 4. LH033 collector and brief amendment

Read, not run (it compiles under `python3 -I -m py_compile`). For each W3Techs response the collector now calls `may_keep(final URL)` and `page_reservation(body, headers)`; where either says no it writes no `.raw.gz` and writes `<name>.derived.json` with URL, read times, status, content type, size, SHA-256 of the bytes received, `body_kept` (the reason), the note, and `extracted` from derive_kept.py's own `w3_details` / `w3_history` (importing derive_kept runs nothing: its main is guarded). Names map correctly (`details` vs `history_details`). W3Techs's refusal of Bytespider and ia_archiver falls under scripts/robots_tokens.json's retention list, which names both, so `may_keep` will say no; I did not read W3Techs's current robots.txt (no web request). LH033's tabulate.py reads `<name>.derived.json` when the body is absent and uses only `extracted`, so the collector's file (which lacks `robots_class` and `used_for`) serves it. The brief's amendment of 21 November describes exactly this, and its row LH033-w3techs-dec exists in schedule/due.csv (due 1 December).

## Findings

**Must-fix:** none.

**Optional:**
1. Other collectors that keep reading do not call `may_keep` or `page_reservation` (only LH033's does; grep over studies/*/scripts and scripts/). The robots gate stops reads that `*` refuses, so the gap is sites that refuse only a training or archiving crawler, as W3Techs, socket.dev and antagonist.nl do. I did not check which open rows (LH034, LH037, LH045, LH050 and others) read such a site; the AGENTS.md bullet says each collector must apply the check, so a sweep of the live collectors, or a check inside lh_fetch's save path, would close it.
2. The LH033 collector writes derived facts from the unredacted body; W3Techs's facts hold no addresses, but passing the extracted record through `redact_bytes` (or asserting none) would match the email rule. For non-W3Techs sources it would keep neither body nor derived file if `may_keep` said no, leaving only the log row's `body_kept`; harmless now (Censys and php.net refuse neither) but silent if that changed.
3. The sweep's "untied" files (files in read folders that no logged URL names, e.g. LH044 1,092, LH012 346) were not checked against robots.txt by anyone; most are probably tables and robots.txt files, but that's unverified.
