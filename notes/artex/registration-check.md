# ARTEX registration checks, 17 November 2026

**In short.** ARTEX has an explicit baseline, three analysis/review/publication chains and a fixed collection stop in the existing queue. Offline checks found no queue schema, dependency or reference-inventory errors. These checks validate registration, not the scientific evidence; the first capture remains work for the next daily run.

## What was checked

Prepared through the GitHub connector against main at 5de36fd3e4b6a0662e33ab3b43e897d41eefa2da. A command-line clone lacked authentication, so the driver fetched exact tracked files through the connected GitHub API. No credentials were read or requested.

The unmodified schedule/model.py and check.py were evaluated with the actual due.csv, runs.csv, proposals and new brief/commissioning files. Historical reference existence was checked against a local path-existence projection of the complete, non-truncated GitHub tree at that commit, not a full content checkout. Other file bodies in that projection were placeholders. This checks queue syntax, IDs, dates, cycles and local reference paths; it does not claim the full site's build or the advisory scan of all historical brief bodies. Re-run python3 schedule/check.py in a complete checkout before claiming research work, as usual.

- All 29 new study rows validate. Only the baseline and conditional baseline-closure gate are ready at registration; scientific analysis waits for explicit baseline disposition, and prospective reads require baseline completion and panel lock.
- Simulating completed baseline/disposition makes round 1 analysis and the same-day panel read ready.
- Simulating round 1's cleared record/reviews makes interim publication ready even while future observations remain unfinished.
- A missed baseline leaves both baseline disposition and final collection closure available. Completing the explicit disposition enables an inconclusive round 1 answer and the subsequent review chain.
- Final collection closure does not require successful observation rows; it requires a retained reconciliation of their actual outcomes. Review and publication rows retain exact-version clearance requirements.

No runner code, timer, billing setting or scientific method of an existing study was changed. No new source was fetched under this protocol, no ARTEX result is released and no scientific review is marked complete. The done registration row is for commissioning alone. Fresh registration review: [review](registration-review.md), with the driver's resolution and [one fresh recheck](registration-recheck.md). Those checks do not substitute for any scheduled study review.

The run/cost records label this preparation and unavailable pricing. A live editor visit was not performed during registration; the next daily run retains its ordinary editor step. GitHub's Site workflow is the full-checkout readiness/build verification after landing.
