# Bodies removed from LH047's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. The removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the page's title, and a line saying why the body went. It was found by the second run of [sweep_may_keep.py](../../../notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py) (output `sweep_may_keep_output_2.json`), after its log tie was fixed; the derived file was written by [scripts/derive_kept.py](../scripts/derive_kept.py). `replay.sh` gives identical output before and after the removal ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The body remains in git history before the removal commit.

**Site:** dl.acm.org (refuses GPTBot, an AI-training crawler, on that path).

**Removed:** `reads/evidence-1/008.body` (1 file). It was a bot challenge page (HTTP 403, "Just a moment..."), recorded as a wall; the record cites the paper through the authors' copy (`evidence-1/007`).
