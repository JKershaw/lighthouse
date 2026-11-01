# LH037: Which of the most-exploited vendors say their products carry the PHP flaws of 21 October 2026, on which PHP branch, and when do their fixes appear?

**Draft. Only the panel rule is fixed at this commit (1 November 2026, before select.py was run and before any vendor advisory or feed was opened for this study).** The rest of the protocol is fixed in the next commit, with the panel's routes and the collector.

## The panel

From CISA's Known Exploited Vulnerabilities catalogue as LH031 retained it at 2026-10-23T1845Z (catalogVersion 2026.10.23), count entries per `vendorProject` with `dateAdded` from 2023-01-01 through 2026-10-20, the day before PHP's 21 October releases, leaving out `PHP` itself. The panel is the 20 vendors with the most entries, every vendor tied at 20th place included ([scripts/select.py](scripts/select.py), writing `selection.json`). The rule chooses vendors whose products attackers are known to use, not vendors known to ship PHP, so that vendors that publish nothing about these flaws are the baseline, not missing cases. Four vendors named by SOCRadar on 22 and 23 October as affected or investigating (Palo Alto Networks, Cisco, Fortinet, Splunk; notes/php-discovery-2026-10-23/ledger.md) are chosen on the outcome; they are read as a separate, named stratum whether or not the rule also selects them, and never counted in the rule panel's shares.
