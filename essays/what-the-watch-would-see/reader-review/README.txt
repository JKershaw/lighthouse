Reader-and-inference review of essays/what-the-watch-would-see.md, stage 2 (8 November 2026). Code and output only.
Raw downloads were kept in the reviewing session's scratchpad, not here. Run every script with python3 -I.
- fetch-log.tsv: every outside read, UTC time, HTTP status, bytes, SHA-256 prefix. Unread: BerriAI/litellm issue 47826 (HTTP 403).
- html2txt.py: HTML to text, used to read the cited pages.
- pypi_neighbours.py / pypi_neighbours_output.txt: litellm releases on PyPI, 15 Oct to 8 Nov 2026; 1.107.0 is absent.
- gharchive_hour.py / gharchive_hour_output.txt: event types and PushEvent payload fields in GH Archive's 2026-11-07 12:00 UTC hour.
- gharchive_scan.py / gharchive_scan_output.csv: events, PushEvents and CreateEvents in the 12:00 UTC hour of each day, 1 Oct to 7 Nov 2026.
- The OSV eight-day subtraction is the claims check's (../claims-check/osv_gap.py); it was not redone here.
