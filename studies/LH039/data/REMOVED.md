# Bodies removed from LH039's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** w3techs.com (disallows Bytespider and ia_archiver) and api.wordpress.org (refuses all bots under `*`).

**Removed:**

- `raw-2026-11-07T1418Z` and `raw-2026-11-08T1411Z`: `cand-3.body`, `cand-4.body`, `stats-1.body` to `stats-4.body`, `meta-1.body`, `meta-4.body`
- `raw-2026-11-09T1431Z` to `raw-2026-11-21T1411Z`: `cand-3.body`, `cand-4.body`, `w3-71.body`, `w3-70.body`, `w3-69.body`, `w3h-71.body`, `w3h-70.body`, `w3h-69.body` (120 files in all).

**What the derived files keep:** W3Techs details pages keep the page's dates, headline shares and each version diagram's rows (label and percentage); history pages keep the monthly table; stats-1 keeps the branch shares; meta-1 the offered releases; meta-4 the status of each release on 7.1, 7.0 and 6.9; stats-2 to stats-4 only the read's metadata. The `.body` files still in these folders from 9 November on for api.wordpress.org are Lighthouse's own notes of a robots.txt refusal, not pages, and stay. `scripts/tabulate.py` reads the derived files when the body is absent.
