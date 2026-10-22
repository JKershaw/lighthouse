# LH013 eligibility preflight, 22 October 2026

The fixed eligibility condition is met. An anonymous ClickPy coverage read found 21 October 2026 as the latest held day for each of the 37 projects in each of the five per-day tables checked, later than the required 12 October. A date-only presence query in `pypi_downloads_per_day` found all 14 days of W1 and W2 for all 37 projects; there were zero missing project-days. These are table coverage and date presence, not verified complete counts.

The six SQL texts, raw CSV bodies, headers, UTC retrieval times, response hashes and status codes are in [the preflight directory](data/preflight-2026-10-22/read_log.json). The [script](scripts/preflight.py) refuses an existing output directory. It did not request W1 or W2 download counts. Before those counts, check the amended CI-flag measure, then perform the W0 totals consistency check prescribed by the fixed brief. Eligibility permits the full study; it does not complete it.
