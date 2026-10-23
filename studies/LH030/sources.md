# LH030 sources

Every URL is fixed in [panel.json](panel.json) and read by [the collector](scripts/collect.py); each read's log gives, per URL, the UTC start and finish, HTTP status, content type, `Last-Modified`, length and SHA-256, with the raw body retained beside it.

- **Baseline, 23 October 2026, 17:14:55 to 17:15:16 UTC:** [read log](data/read-2026-10-23T1715Z/read_log.json), [classes](data/read-2026-10-23T1715Z/classes.json), [hand decisions on IV](data/read-2026-10-23T1715Z/hand_iv.json).
- **Feasibility check, 23 October 2026, 17:11:00 to 17:11:25 UTC**, for the unrelated CVE-2024-4577: [read log](feasibility/read_log.json).
- **Known answers**, from bodies retained earlier by LH024 (22 October 06:24 UTC), LH028 (23 October 16:06 UTC), LH029 (23 October 17:00 UTC) and the discovery pass (notes/php-discovery-2026-10-23/, 23 October 17:08 UTC): [output](data/known_answers.txt).
