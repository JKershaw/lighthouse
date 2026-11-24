# R-0136: recheck of LH040 version 1.1

**In short.** A fresh agent read once what the round resolving the reader-and-inference review wrote into LH040's record (the poisoned LiteLLM 1.107.0 counted in fetches from PyPI), and reproduced the new figures with its own code. Every figure held; the very long In short was cut to four sentences and one post hoc reading was narrowed to the window ends it holds under. Cleared at version 1.1.

- Queue row: LH040-record-recheck. Rechecker: a subagent in Claude Code, Opus 5.5 (claude-opus-5-5, as reported by the harness), 24 November 2026. No network; no downloaded code run.
- Read: notes/R-0135-lh040-v1-reader.md (all, including "Resolution, by the driving session"); notes/R-0134-lh040-v1-evidence.md; `git diff d707b29 138ffb7 -- studies/LH040/LH040.md`; studies/LH040/brief.md (measure 3's pre-set reading); tables/m3_index.csv, tables/m2_tail_by_installer.csv; review/resolution_r0135_checks.py and r0135_index_checks.py with their outputs; read 2's raw Q1, Q2 and Q4 bodies; L1's derived upload times (data/pre-brief-2026-11-08T1414Z/pypi_project_json.derived.json).
- Code and output: [studies/LH040/review/recheck_r0136.py](../studies/LH040/review/recheck_r0136.py) and [recheck_r0136_output.txt](../studies/LH040/review/recheck_r0136_output.txt). Replay: `python3 -I studies/LH040/review/recheck_r0136.py`. It rebuilds each release's hours as newest from L1's upload times (final releases, by `packaging`) with 1.107.0 live from 11:39:51 UTC to each end, and each day-0 share from the raw bodies, not from tables/m3_index.csv.

## What was checked

1. **Rank, ratio and band.** Under 13:23: case I 0.1976 (h 1.7192), comparison min 0.1722, median 0.2921, max 0.4052; band 0.590 to 1.387 times the median; case 0.676 times; rank 17 of 18, only 1.108.1 below (newest 0.382 hours); 10.9 per cent of the way up the band; a release at the median could lose 41.0 per cent and stay inside. Under 13:20: 0.697 times, 17th. Under 12:47: 1.039 times, 8th. "Spans more than a factor of two": 0.4052 / 0.1722 = 2.35. All as the record says.
2. **Post hoc grouping.** Nine comparison releases uploaded before 13:00 UTC, I 0.249 to 0.344 under 13:23, all above the case. Reproduced; labelled post hoc in the record, with "no brief tests it", as the rule requires.
3. **Installer split after the pull** (days 1 to 30, raw Q4): none 954, Browser 489 (together 1,443, 96.07 per cent), uv 33, requests 16, Nexus 9, devpi 1, pip 0; total 1,502, equal to Q2's sum on 28 days. uv on seven days, 13 on 22 October. Reproduced. (tables/m2_tail_by_installer.csv runs to 22 November, hence its 964 and 518; the record's figures are days 1 to 30, correctly.)
4. **Labels and voice.** The pre-set "travelled as an ordinary newest release did" stays, matching the brief's wording, with rank, ratio and band beside it in the In short, Answer and measure 3. The readings "no faster than ... probably at the low end" and "can't tell ordinary uptake from uptake held down by up to about 40 per cent" are labelled post hoc or stated as a property of the rule. Maliciousness stays attributed (R1, R2, R6 to R9, L7); no new sentence says any system fetched, ran or was compromised. A download is a fetch throughout; "whether any request was served a file isn't in the logs" is new and right. Absolutes: "none by pip" carries days 1 to 30; "no cell changed" its re-read window.
5. **Agreement.** In short, Answer, measures 2 and 3, Limits and Next agree after the edits below. The Corrections entry for 1.1 lists what changed accurately.

## Found and changed (within version 1.1)

1. **In short too long.** Rewritten to four sentences: question; count and the pre-set reading with rank 17 of 18 and the band 0.59 to 1.39 times the median, then the post hoc reading; the tail with uv 33, none by pip; fetch not install, review status, no piece planned. The day share (1.4 per cent) was dropped from it, since a reader read it as slow uptake (R-0135); it stays in the Answer.
2. **Answer's post hoc reading over-general.** It said "probably at the low end" without a window end; under Aikido's 12:47 the case is 8th of 18 at 1.04 times. Now "under the two later ends, probably at the low end", as measure 3 already said.
3. **Status lines.** Header, Answer opening, Limits and Next now say the recheck cleared 1.1; a Corrections entry lists these edits.

Not changed: the Limits line "no public source read here can explain it without hourly logs" is scoped to what was read and stands.

## Combined disclosure check

Clears. Version 1.1 adds aggregate counts, ranks and installer names already in ClickPy's public tables, and attributed high-level accounts of a public incident; no host, account, repository, join or recipe is added.

## Verdict

Cleared at version 1.1.
