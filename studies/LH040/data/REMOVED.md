# Bodies removed from LH040's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** pypi.org (refuses all bots under `*` on these paths) and api.deps.dev (refuses all bots under `*`).

**Removed:**

- `pre-brief-2026-11-08T1414Z/pypi_project_json.raw`, `pypi_simple_json.raw`
- `pre-brief-2026-11-08T1414Z/pypi_1.107.0_json.raw`, `pypi_1.106.7_json.raw`, `pypi_1.108.0_json.raw` (added on 21 November after the sweep by `notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py`: pypi.org's robots.txt refuses `/pypi/` paths to all bots)
- `pre-brief-2026-11-08T1416Z/depsdev_requests_version.raw`, `depsdev_requests_dependents.raw` (7 files in all).

**What the derived files keep:** pypi_project_json (L1) keeps each final release's first upload time, the releases listed and the last serial; pypi_simple_json (L4) its last serial, project status and the 1.107.0 versions its files name; pypi_1.107.0_json (L2) its 404 message; pypi_1.106.7_json and pypi_1.108.0_json (L3) version, yanked flag, file count and first upload time; the deps.dev reads only their metadata. `scripts/tabulate.py` reads L1's derived file when the body is absent.
