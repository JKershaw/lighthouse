# LH013 amendments

## Amendment 1, 29 September 2026, before any count of W1 or W2 was read

Made by the driving session of the afternoon of 29 September 2026, from a finding of LH014's research agent while it wrote LH014's brief (studies/LH014/brief.md, "Resource ceiling"). The `demo` user's `read_overflow_mode` is `break` (studies/LH014/data/clickpy_settings.csv, read 12:28 UTC), which by ClickHouse's documentation (https://clickhouse.com/docs/operations/settings/query-complexity, read by that agent at 12:30 UTC) stops a query at 1,000,000,000 rows or 50 GB read and returns the partial result "as if the source data ran out", without an error. LH013's passes over `pypi.pypi` read about 9.4 billion rows a week and are split by project and by day, so a split that still passed the limit would return a count cut short.

- Every LH013 query of the `pypi` database sets `read_overflow_mode = 'throw'`, which the `demo` user may do (checked by LH014's agent at 12:30 UTC, studies/LH014/data/clickpy_overflow_setting.csv).
- A query that reports reading either limit counts as failed and is split again.
- No measure, week, threshold, field or convention changes, and the brief's snapshot hash on issue #15 still holds for brief.md.

LH011's and LH012's logged queries were checked the same afternoon: none read more than 233,086,976 rows or came near 50 GB (studies/LH011/data/read_log.csv; studies/LH012/data/read_log.csv and read_log_phase2.csv), so none of their counts was cut short by this limit.

## Amendment 2, 29 September 2026, late evening, before any count of W1 or W2 was read

Made by the driving session of the correction round of 29 September 2026, after the reader-and-inference review of that round (notes/R-0025.md) raised two points. No count of either week has been read, and no measure, week, threshold, field or convention of the brief changes; the brief's snapshot hash on issue #15 still holds for brief.md.

- **The pip date.** The brief's Sources say that "since 22.3 (15 October 2022) it reads PEP 658 metadata files instead of downloading each candidate, where the index offers them". PyPI began to offer those files only in 2023, and in its JSON index under the key core-metadata (PEP 714, accepted 27 June 2023), which pip reads from 23.2 (15 July 2023); pip 23.1.2 reads only dist-info-metadata from a JSON index, which it asks for first. So from PyPI, pips older than 23.2 fetch each candidate in full (studies/LH012/review/v04_pip_metadata_read.txt, read 21:49 to 21:50 UTC). Where this study's Limits or its record speak of which pips can make a walk-shaped profile, they use 23.2.
- **A version that walks skip, described.** Beside the walk test, the study describes, and does not test, boto3's Python 3.9 downloads of 1.42.87 as a fraction of the mean of its neighbours 1.42.86 and 1.42.88, in each week. In W0 it was 0.55 (studies/LH012/review/r0025_walk_dip.txt, 2), with 0.99 and 0.91 on Python 3.10 and 3.11, and the three versions' metadata are alike. The reading, made after W0's counts by the review and not tested, is that a resolver walking from environments that already hold 1.42.87 installed takes that installed copy without fetching it; on that reading the dip stays at 1.42.87 until those environments are rebuilt. It is one more reading, beside the brief's comparisons, not among them.

