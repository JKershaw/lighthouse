# LH034, post-record context: Node.js's announcements for v22.23.5, v24.22.3 and v26.13.1

**In short.** LH034's record (version 1.1) counts three versions first seen in nodejs.org's downloads on 11 November as at or above the October fix, assuming, unchecked, that they are published releases carrying it. On 25 November 2026 we read Node.js's own announcement for each, once. Each is dated 11 November 2026 and says "This is a security release", for a new set of flaws; none of the three mentions the October release or the versions it fixed (whether they name any of October's flaws can't be checked, because October's CVE list isn't retained), so whether they carry the October fix is still not stated by any source read, though as later releases in the same lines that would be the ordinary case (interpretation). This is context read after the record was reviewed; the record has not absorbed it, and it has had no review.

- Read by: a Claude Code writing subagent of the driving session of 25 November 2026, on Opus 5.5 (as reported by the harness), for schedule row piece-week-one-rev, at the reader review's suggestion (notes/R-0131-lh034-v1-reader.md, Next step).
- How: `LIGHTHOUSE_PROVIDER=anthropic python3 -I studies/LH034/scripts/oneoff_release_pages.py`, through scripts/lh_fetch.py with `access='oneoff'`. nodejs.org's robots.txt (SHA-256 cbcd5e7d85caf581...) allowed each URL under the `*` group, with no training, archiving or `*` refusal at the path, so `save_body` kept each body (gzipped, email addresses withheld). Three URLs, one GET each, no retries. No earlier retained read of these pages was found in the repository (searched for the version strings and for `nodejs.org/en/blog/release`).
- Log: [fetch_log.json](fetch_log.json) (URL, UTC read time, status, bytes, SHA-256 of the bytes received, robots decision, body kept).

| Version | URL | Read (UTC) | Status | SHA-256 of bytes received (first 16) |
| --- | --- | --- | --- | --- |
| v22.23.5 | https://nodejs.org/en/blog/release/v22.23.5 | 2026-11-25T15:15:06Z | 200 | 0854fe0cdf4153d0 |
| v24.22.3 | https://nodejs.org/en/blog/release/v24.22.3 | 2026-11-25T15:15:06Z | 200 | 377c9e43a6e227f1 |
| v26.13.1 | https://nodejs.org/en/blog/release/v26.13.1 | 2026-11-25T15:15:07Z | 200 | f17280cb187b20e2 |

## What each announcement says (observation, the project's own words)

- **v22.23.5:** "2026-11-11, Version 22.23.5 'Jod' (LTS)"; "This is a security release." Its notable changes list 16 entries tagged with 14 distinct CVE identifiers (CVE-2026-123828 to CVE-2026-123877; three entries share CVE-2026-123872), rated High, Medium or Low, plus updates to llhttp (9.4.4) and sqlite (3.54.1).
- **v24.22.3:** "2026-11-11, Version 24.22.3 'Krypton' (LTS)"; "This is a security release." The same list plus CVE-2026-126051 ("tls: fix remotely reachable TLS server crash", High): 15 distinct CVE identifiers; the same llhttp and sqlite updates, plus updates to brotli (1.2.1) and undici (7.30.2).
- **v26.13.1:** "2026-11-11, Version 26.13.1 'Lithium' (LTS)"; "This is a security release." The same 15 distinct CVE identifiers as v24.22.3, CVE-2026-126051 among them, and the same dependency updates, except undici to 8.12.4. (Corrected 25 November after the evidence review, notes/R-0138-week-one-rev-evidence.md, should-fix 5: an earlier wording implied CVE-2026-126051 was in v26.13.1 alone; the kept bodies show it in v24.22.3 too.)
- Each page's footer reads "Last Updated Nov 11, 2026".

## What it settles, and what it doesn't

- **Settled (observation):** the three keys are real, published releases in lines 22, 24 and 26, announced by the project on 11 November 2026, the day they first appear in the downloads (LH034, day 21). That removes half of the amended rule's unchecked assumption.
- **Not settled:** none of the three announcements names the October release or the versions it fixed (v22.23.4, v24.22.1, v26.12.1), and whether they name any of its ten flaws can't be checked; release notes list changes since the previous release, and the October advisory's CVE identifiers are not retained in the repository to compare against the commit lists. That a later security release in the same line carries the earlier one's fixes is the ordinary practice for a project's patch releases, but no page read here says so (interpretation, unchecked). So whether these versions carry the October fix stays unknown from what was read, though likely.
- **New, and not in LH034's record:** from 11 November the fixed lines had a second security release. Downloads of v22.23.4, v24.22.1 and v26.12.1 after that day are of releases that, by the project's November notes, lack November's fixes. LH034's measure is about the October fix only, so this changes no figure, but it is part of why listed at-or-above downloads fell from day 22 (LH034, Answer: "which rule").
- Not read: the project's November vulnerability advisory, which would say which lines and versions are affected by November's flaws; the October advisory again.

Combined disclosure check (schedule/research-safety.md): clears. Public release notes of a widely used project; CVE identifiers and one-line titles only, no exploit detail, no hosts, people or accounts.
