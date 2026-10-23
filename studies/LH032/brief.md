# LH032: How do fixes for the October 2026 PHP flaws reach products that embed PHP, as one national CERT's public list records them?

**Protocol 0.1, fixed 23 October 2026, before this study's first read of the list.** Writer: a Claude Code driving session (Claude Opus 5.5). The second candidate of the PHP discovery pass (notes/php-discovery-2026-10-23/ledger.md): PHP inside vendors' products is fixed on the vendors' clocks, not PHP's.

## Frame and why

The Dutch National Cyber Security Centre's public repository `NCSC-NL/php2shell` on GitHub, which CERT-EU's advisory 2026-018 (version 1.2, read by LH030 at 17:15 UTC on 23 October) recommends "to identify third-party software that embeds PHP and may be impacted". One maintained list, chosen by its role (a national CERT's tracker that another agency cites), rather than a vendor panel picked by this session; and because it is a git repository, every change to it carries a commit time, so a status change can be dated from the list's own side. The repository's contents, structure and size have not been read. Its existence and CERT-EU's description of it are known; nothing else is.

## What is already known of outcomes about products

SOCRadar's page (discovery pass, read 23 October 17:08 UTC) claims Palo Alto Networks PAN-OS and Panorama affected with no fixed release, Cisco Expressway affected with a fixed release, and Fortinet and Splunk investigating. Those four vendors' outcomes are known in that third party's words; whatever the list says of them is compared with that, not counted as unseen.

## Unit and measures, defined before reading

The unit is one entry in the list: a vendor and product as the list names it. At each read, record for each entry the fields the list gives, whatever they are (expected, but not assumed: affected status, fixed version, a link to the vendor's advisory, notes), verbatim, and the commit at which the entry was first added and at which each field last changed (from `git log` on the file holding it). Derived measures, fixed now: the number of entries by status at each read; for each entry that reaches a fixed or not-affected status, the interval from PHP's release (21 October, reported 13:30 UTC by CERT-EU) to the commit that recorded it, as the list's clock and not the vendor's; how many entries link a vendor advisory. The list's statuses are the list's words; a vendor's own advisory is read only to check a sample, at most five vendor pages per read, chosen as the first five entries in the list's order that link one, recorded as a check and not merged into the list's counts.

## Reads and schedule

Clone the repository read-only (shallow is not enough: full history is needed for commit times) through the session's GitHub access; retain the tree's commit id and a copy of the files that hold the list; no GitHub web pages, which refuse anonymous reads. A first read on 23 October, then with LH030's schedule (daily through 30 October, then Mondays and Thursdays until 30 November 2026). If the repository is not a list of products, or cannot be read, record that and stop: the study is then inconclusive and says why. No contact with the NCSC or any vendor, no login, no probe of any product.

## Limits fixed in advance

A list records what its maintainers learned and chose to record, when they recorded it: an entry's commit time is not the vendor's release time or a customer's deployment, a missing product is not an unaffected one, and the list's coverage of vendors is its own. Nothing here counts installations, exposure or compromise. Counts are of entries in this list, with no rate beyond it.
