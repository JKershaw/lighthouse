# LH013 amendments

## Amendment 1, 29 September 2026, before any count of W1 or W2 was read

Made by the driving session of the afternoon of 29 September 2026, from a finding of LH014's research agent while it wrote LH014's brief (studies/LH014/brief.md, "Resource ceiling"). The `demo` user's `read_overflow_mode` is `break` (studies/LH014/data/clickpy_settings.csv, read 12:28 UTC), which by ClickHouse's documentation (https://clickhouse.com/docs/operations/settings/query-complexity, read by that agent at 12:30 UTC) stops a query at 1,000,000,000 rows or 50 GB read and returns the partial result "as if the source data ran out", without an error. LH013's passes over `pypi.pypi` read about 9.4 billion rows a week and are split by project and by day, so a split that still passed the limit would return a count cut short.

- Every LH013 query of the `pypi` database sets `read_overflow_mode = 'throw'`, which the `demo` user may do (checked by LH014's agent at 12:30 UTC, studies/LH014/data/clickpy_overflow_setting.csv).
- A query that reports reading either limit counts as failed and is split again.
- No measure, week, threshold, field or convention changes, and the brief's snapshot hash on issue #15 still holds for brief.md.

LH011's and LH012's logged queries were checked the same afternoon: none read more than 233,086,976 rows or came near 50 GB (studies/LH011/data/read_log.csv; studies/LH012/data/read_log.csv and read_log_phase2.csv), so none of their counts was cut short by this limit.
