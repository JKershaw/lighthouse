# LH013 sources

Every read is in data/read_log.csv with its UTC time, endpoint, query or URL, HTTP status, rows returned and, for ClickPy, the rows and bytes read by ClickHouse's own summary header. All reads were anonymous; no key or token was read or sent. BigQuery was not read.

## Data

- **K1. ClickPy, ClickHouse's public SQL service**, https://sql-clickhouse.clickhouse.com/?user=demo (user `demo`). Tables `pypi.pypi_downloads_per_day`, `pypi_downloads_per_day_by_version`, `pypi_downloads_per_day_by_version_by_python`, `pypi_downloads_per_day_by_version_by_system`, `pypi_downloads_per_day_by_version_by_installer_by_type` (coverage only), `pypi.pypi` (the cell passes) and `system.parts` (one read, no rows). Read 2 November 2026, 15:30:05 to 15:38:45 UTC, 178 queries (one of them a syntax test on literal rows that reads no table), 16,597,595,796 rows read. Observation window: downloads on 21 to 27 September 2026 (W0, totals only, as a check), 28 September to 4 October 2026 (W1) and 5 to 11 October 2026 (W2); daily totals 25 September to 14 October 2026 for the gap rule. Earlier: the preflight of 22 October 2026, 03:59 to 04:00 UTC (data/preflight-2026-10-22/), dates only.
- **J1. PyPI JSON API**, https://pypi.org/pypi/<project>/json for the 37 projects. Read 2 November 2026, 15:30:25 to 15:30:35 UTC, 37 requests. The bodies (57 MB) are not retained; their SHA-256 are in data/pypi_json_sha256.txt and the per-version extract the analysis uses is data/versions.csv (scripts/meta_extract.py).
- **LH012's retained files** (studies/LH012/data/, record version 0.4): reference.csv (R0), versions.csv (PyPI as read 29 September 2026), python_admission.csv, analysis/week.csv and python.csv, and week/versions/ and week/python/ (W0's counts as read 29 September 2026, 06:40 to 07:13 UTC).

## Documentation (two of the brief's five page reads)

- **D1. PyPI User Documentation, "BigQuery Datasets"**, https://docs.pypi.org/api/bigquery/, read 2 November 2026 at 15:32:52 UTC (data/docs/bigquery.html). Undated page. Says the download statistics table is "populated through the Linehaul project by streaming download logs from PyPI to BigQuery"; says nothing of requests for PEP 658 metadata files.
- **D2. linehaul-cloud-function, linehaul/events/parser.py** (main branch), https://raw.githubusercontent.com/pypi/linehaul-cloud-function/main/linehaul/events/parser.py, read 2 November 2026 at 15:32:53 UTC (data/docs/linehaul_parser.py.txt). Parses "download" and "simple" log lines from the content network, takes the file name from the URL's last path part, and passes the country code through; it does not say which requests the network logs as downloads.
