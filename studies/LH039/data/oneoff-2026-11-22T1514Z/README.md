# One-off read of 22 November 2026: what this folder holds

Two GETs made after LH039's collection stopped, for release dates only (studies/LH039/LH039.md, Method). readlog.csv is left as the script wrote it. Its `body_kept` column records keep_decision's answer ("yes": robots.txt and the page allowed a copy), not what the repository holds:

- `feed.body`: WordPress's release feed, kept (SHA-256 in readlog.csv). Facts used: feed.facts.json.
- `archive.body`: WordPress's release archive page, 1,320,995 bytes. It was **not committed**, because of its size (the driver's decision, 22 November 2026). The repository holds archive.facts.json, with the facts used, and readlog.csv, with the hash of the bytes received.
