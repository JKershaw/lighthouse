# Bodies removed from LH035's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** www.routeviews.org and w3techs.com (refuse AI-training or archiving crawlers by name); downloads.pch.net and publicdata.caida.org (refuse all bots under `*`).

**Removed:**

- `reads-2026-11-06/07-I05-routeviews-org-routeviews.html`, `12-I07-downloads-pch-net-bgp-routing-data.html`, `32-I20-w3techs-com-technologies.html`, `33-I20-w3techs-com-disclaimer.html`
- `reads-2026-11-05/14-caida-publicdata-asfac.html` (5 files).

**What the derived files keep:** Each derived file keeps only the quoted phrases and figures of the instruments.json rows that cite the page and that the page bore out, in the normalised form `scripts/reread_check.py` compares, which reads them when the page is absent. A quotation added to a row later cannot be checked against these files.
