# Bodies removed from LH034's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** nodejs.org (refuses all bots under `*` for /dist/).

**Removed:**

- `read-2026-10-27T1811Z`, `read-2026-10-28T0638Z`, `read-2026-10-29T0635Z`, `read-2026-10-30T0635Z`, `read-2026-11-02T1531Z`, `read-2026-11-05T1414Z`: `dist-index.raw.gz` (6 files).

**What the derived files keep:** Each `dist-index.derived.json` keeps the release list in its order, with each release's version, date and security flag. `scripts/tabulate.py` and `review/R-0039_checks.py` read it when the body is absent.
