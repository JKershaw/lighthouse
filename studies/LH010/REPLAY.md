# Replaying LH010 from its retained evidence

**Command**, from the repository root:

```
sh studies/LH010/replay.sh
```

It needs a POSIX shell, `cmp`, `mktemp` and Python 3 with its standard library only; it was run with Python 3.11.15 on 27 September 2026 and passed. It reads nothing from the network and no key or credential. It exits 0 only if every step below matches; any difference or failed check exits 1 and prints `DIFF` beside the table or the failing test.

1. **Baseline.** It runs `scripts/analyse.py` with the environment variable `LH010_OUT` set to a temporary directory, so the committed tables are not touched, and compares the eight tables analyse.py writes (lags, summary_by_event, summary_by_class, hazard_by_class, library_rates, library_unit, by_authorship, within_library) with `data/` byte for byte. `LH010_OUT` is honoured by `scripts/common.py`'s table writer, added for version 0.3 of the record; without it every script writes to `data/`, as it always did, and every script reads from `data/`.
   It then runs the three other steps that need no network, `scripts/classes.py` (the classes, from the retained texts, judgements and LH009's table), `scripts/reuse.py` (the twelve reused frames, from LH008's and LH009's retained tables) and `scripts/summarise_reads.py` (from the read log), into the same kind of temporary directory, and compares `fix_classes.csv`, `reused_screen.csv`, `reused_moves.csv` and `read_summary.csv` with `data/` byte for byte.
2. **Reanalysis.** It runs `scripts/reanalyse.py --out` into a second temporary directory and compares its six tables with `data/reanalysis/`. `sh studies/LH010/replay.sh --write` rewrites `data/reanalysis/` in place, for use only after a deliberate change to the script.
3. **Checks.** It runs `python3 -m unittest` over `scripts/test_reanalyse.py`: synthetic fixtures for the earliest-advisory rule and the notes-evidence states, a check that the baseline replay equals the committed tables, and a check that the reanalysis with the original clock and every event reproduces version 0.2's library-unit figures.

The random parts are seeded: the permutation test as analyse.py has it (10,000 shuffles, seed 20260927) and the reanalysis's bootstrap (10,000 resamples, seed 20260927), so the tables are identical on every run with the same Python.

## What cannot be replayed from what is kept

- **Collection.** `select_libraries.py`, `classify.py`, `osv_ranges.py` and `collect.py` read ClickPy, OSV, PyPI, Open Source Insights and git over HTTPS (they need the network and the `requests` package, version 2.33.1 when run, and `packaging` 24.0). Run again they would read the sources as they stand on the day, not as they stood on 27 September 2026 at 09:53 to 10:04 UTC, and OSV records, PyPI descriptions, changelogs and dependents lists change.
- **The moves.** `data/moves.csv` was read from blobless clones of the dependents' repositories, which were deleted once the table was written (brief.md amendment 2), and `data/reused_moves.csv` is cut from LH008's and LH009's moves, read the same way. The moves cannot be regenerated offline; the replay starts from them.
- **The notes.** `data/fix_texts.csv` holds the texts as read (each cut to 3,000 characters); the library clones they came from, which `date_head_entries.py` also walks, were deleted. The notes-evidence states are computed from those retained texts and cannot see anything the rule did not read, such as GitHub's release pages.
- **The judgements.** `data/flaw_judgements.csv` holds judgements an agent made by reading, which no script reproduces; classes.py takes them as given.
