# Bodies removed from LH032's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** www.antagonist.nl (refuses ia_archiver, an archiving crawler, on the path read; found by `notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py`).

**Removed:**

- `read-2026-10-28T0634Z/advisory-check/page-4.html.gz`, `read-2026-10-29T0634Z/advisory-check/page-4.html.gz`, `read-2026-10-30T0634Z/advisory-check/page-5.html.gz`, `read-2026-11-02T1526Z/advisory-check/page-5.html.gz` (4 files, the same hosting company's advisory, sampled on four days).

**What the derived files keep:** the read's metadata only. The checkpoints record only that each sampled page answered HTTP 200, and no script reads these bodies (`scripts/advisory_check.py` writes them; `review/replay.py` reads the review folder, not these).
