# Bodies removed from LH033's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** w3techs.com (disallows Bytespider and ia_archiver).

**Removed:**

- `read-*/w3techs-details-8.{2,3,4,5}.raw.gz` and `read-*/w3techs-history_details-8.{2,3,4,5}.raw.gz` in the reads of 25 and 26 October and 2, 9, 16 and 21 November 2026 (48 files).

**What the derived files keep:** Details pages keep the page's dates, the headline share and each version diagram's rows (label and percentage), from which `scripts/tabulate.py` takes measure 4; history pages keep the monthly table, for measure 6. `scripts/tabulate.py` and `review/R-0039_checks.py` in LH034 read the derived files when the body is absent.
