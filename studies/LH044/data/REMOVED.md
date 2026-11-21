# Bodies withheld from LH044's data, 21 November 2026

Withheld on 21 November 2026 under the keeper's decision of that day ([notes/keeper/2026-11-21-robots-intent.md](../../../notes/keeper/2026-11-21-robots-intent.md)): where a site's robots.txt refuses AI-training or archiving crawlers, or all bots, Lighthouse keeps no copy of the page in its public repository. They were found by the second run of [sweep_may_keep.py](../../../notes/keeper/robots-intent-2026-11-21/sweep_may_keep.py) (output `sweep_may_keep_output_2.json`), after its log tie was fixed: each site's robots.txt, read through the gate that day, refuses ClaudeBot by name.

LH044 already had a form for a body it may not keep (the amendment of 9 November 2026, use=reference), and these bodies were put into it by [scripts/derive_kept.py](../scripts/derive_kept.py): `<n>.b` now holds a placeholder naming the keeper's decision, and `<n>.withheld.json` the URL, read time, status, SHA-256 and size of the bytes received and of the copy kept until now, the page title, and (in `derived`) the class, detail, marker and echoes the classifier took from the whole body, which `collect.py --classify` reads when the body is gone. Run with the bodies, then with no copy at all, `--classify` gives byte-identical classes.csv, robots.csv, echoes.csv, summary.json and usage_token.csv for both reads; `test_lh044.py`, the review scripts and `scripts/robots_rules.py`'s self-test give the same results ([removal_check.txt](../../../notes/keeper/robots-intent-2026-11-21/removal_check.txt)). The bodies remain in git history before the removal commit.

**Sites:** codeberg.org, git.sr.ht, repo1.maven.org, archive.ubuntu.com, runescape.wiki, wiki.gentoo.org, ftp.eq.uc.pt, lwn.net.

**Withheld:**

- `read-2026-11-08T1920Z/0010.b` (F06, codeberg.org), `0012.b` (F07, git.sr.ht, a 502 page), `0040.b` (R06, repo1.maven.org, a rate-limit answer), `0070.b` (M02, archive.ubuntu.com), `0106.b` (D11, runescape.wiki), `0113.b` (D15, wiki.gentoo.org), `0228.b` (Q07, ftp.eq.uc.pt)
- `read-2026-11-15T1413Z/0070.b` (M02, archive.ubuntu.com)
- `statements-2026-11-08T1920Z/0011.b` (S06, lwn.net; the quotation statements/coded.csv takes from it is kept in the record's extract, checked against the page's text) (9 files in all).

The four pages withheld on 9 November for Content-Signal (read-2026-11-08T1920Z/0140.b and 0190.b, statements 0006.b and 0008.b) were already in this form; the sites of three of them (jurnal.itg.ac.id, dealing-with-bots.coar-repositories.org and coar-repositories.org) also refuse ClaudeBot today, which changes nothing, since no body of theirs is kept.
