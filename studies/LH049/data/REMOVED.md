# Bodies removed from LH049's data, 21 November 2026

Removed on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. Each removed body is replaced by a `.derived.json` file beside it, with the same name stem, holding the URL, read time, HTTP status, size and SHA-256 of the bytes received (from the read log), the facts the study uses, and a line saying why the body went. The derived files were written by [scripts/derive_kept.py](../scripts/derive_kept.py); the outputs of every script that read the bodies were rebuilt from the derived files and found byte-identical to the outputs from the bodies ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** socket.dev (refuses AI-training crawlers by name).

**Removed:**

- `pre-brief-2026-11-10T1437Z/socket_blog.raw.gz` and `pre-brief-2026-11-10T1438Z/socket_post.raw.gz` (2 files).

**What the derived files keep:** The post (E8) keeps the short phrases and times brief.md quotes from it, each checked against the page; the listing (E5) keeps that it links the post. No script read either body.
