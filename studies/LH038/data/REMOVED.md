# Bodies removed from LH038's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** git.kernel.org (refuses AI-training crawlers by name and all bots under `*`) and oss-security.openwall.org (refuses AI-training crawlers by name).

**Removed:**

- `policies-2026-11-04T1415Z/kernel_security_bugs.raw.gz`, `kernel_cve.raw.gz` (bot challenge pages), `linux_distros.raw.gz`
- `read-2026-11-17T1419Z/openwall_distros_stats.raw.gz` (4 files).

**What the derived files keep:** The challenge pages keep that fact and the title; linux_distros keeps its Last modified line and the phrases P4 quotes, each checked against the page; openwall_distros_stats keeps its Last modified line, whether it names the CVE, and the per-year paths it links. `review/r0091_check.py` reads them when the body is absent.
