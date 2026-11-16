# LH048: replaying the tables

`scripts/tabulate.py` was written on 16 November 2026, after the baseline read (`data/read-2026-11-10T1418Z`) and the 16 November read (`data/read-2026-11-16T1420Z`) were held, as the brief allows ("a tabulator written after the baseline implements the measures above as written and changes nothing here"). It implements measures 1 to 4, the selection classes and the brief's thresholds (bodies under 200 bytes, CVSS bands, the factor-of-two EPSS step, the 0.5 percentile) from retained bytes only. It fetches nothing, and it writes tables, not findings.

```
python3 -I studies/LH048/scripts/tabulate.py                    # every held read -> data/tables.json
python3 -I studies/LH048/scripts/tabulate.py --until 2026-11-10T1418Z --out -   # baseline only
python3 -I studies/LH048/scripts/test_tabulate.py               # constructed cases, plus a check that the replay is deterministic and matches data/tables.json
```

`data/tables.json` sorts its keys and carries no clock time, so a replay over the same bytes produces an identical file. Under `as_of`, each held read has the measures computed with that read as "the last read". Named and identified flaws, the ambiguous Chrome candidate and the linked set are kept in separate lists. Units that are unidentified or have no identifier are unknown in every measure. When a source was not requested at a read (the linked set's CVE record and NVD on a Monday read), the tables say "not read at this read", which is a different class from "unavailable" and from "no record". The Chrome page answered 503 at the baseline, so its severity word there is "unavailable at this read". The word from the discovery copy is shown beside it and never put in its place.

After a new read, rerun the first command and then the tests.
