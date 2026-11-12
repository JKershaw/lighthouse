# R-0068: LH037, D-Link's class at the read of 12 November 2026

**In short.** A fresh agent read D-Link's statement SAP10524 as retained at the read of 12 November (the primary source; nothing was refetched) against the brief's class definitions and the panel's earlier classes. The brief gives *affected, fixed for all listed*, not *not affected*: D-Link heads its hardware and its applications "Not Affected" but withholds that heading from its mydlink portal, where it reports PHP components and "emergency remediation" of them, and the brief's *not affected* requires "nothing affected". The checkpoint's class was changed and one wrong sentence in it was corrected (it said the statement never uses the word "affected"). Every quotation and figure in the checkpoint's D-Link section matches the body. Nothing in Lighthouse's voice says or implies that D-Link's systems were compromised or exploited. The count of 7 of 20 is unchanged: it counts statements, not classes.

Reviewer: a fresh review subagent in Claude Code on Opus 5.5 (claude-opus-5-5), 12 November 2026. It runs on the same family of models as the writer and reads the same record, so its agreement is a review contribution, not independent confirmation.

## What was read

- AGENTS.md; studies/LH037/brief.md (Routes, Measures, amendment 1, the amendments of 9 and 12 November).
- The checkpoints of 1, 2, 5 and 9 November for how vendor-run services were classed: Google's (2 and 5 November), Cisco's ISE Portal Builder, Fortinet's FortiClient cloud services.
- studies/LH037/data/read-2026-11-12T1416Z/: `d-link__SAP10524.raw.gz` (the statement), `d-link__announcements.raw.gz` (the listing), read_log.json, found_log.json; and, for one claim, the Cisco, Fortinet, Google and Splunk bodies of the same read (case-sensitive and case-insensitive search for "PHP2Shell"); Fortinet's advisory page for its cloud-services wording.
- studies/LH037/panel.json; notes/php-watch-log.md, "## 12 November 2026"; site/this-week.md.

Text was extracted from the retained HTML with a few lines of Python (tags stripped, entities unescaped). The whole-word, case-sensitive "PHP" count on the statement was recomputed: 5, as logged.

## The class

The brief (Measures, 2): *not affected* is "a statement that no product, or that named products, are not affected, with nothing affected"; then *affected, no fix*, *affected, fixed for some* listed products or versions, and *affected, fixed for all* listed; a vendor's class comes "from the vendor's own statements as read".

The statement, under "1. Security Assessment of Products and Services", has three headings: "Networking Hardware Not Affected" ("these products are not affected"), "Applications and Mobile Apps Not Affected" ("these applications and services are not affected"), and "mydlink Cloud Services Emergency Risk Mitigation Completed", which says "certain legacy web frontend components of the mydlink portal cloud platform previously utilized a PHP-based architecture". Under "2. Mitigation Measures", "D-Link has completed emergency remediation and security protection measures for the relevant cloud platform", with WAF rules, and the PHP components are being replaced, "scheduled for completion and deployment by the end of November 2026". The page shows "Resolved Status: Yes".

- *Not affected* fails its own condition. D-Link says "not affected" of two of the three things it assessed and pointedly not of the third, for which it reports remediation. "Nothing affected" is not what the statement says, and the brief's "unknown is never no" weighs against supplying it.
- The classes are per vendor and make no exception for a service the vendor runs. The panel has counted one: Cisco lists ISE Portal Builder, "Fix deployed, no customer action required", among its vulnerable products, and it is one of the listed products behind Cisco's *affected, fixed for all listed*. Fortinet's "Fortinet has remediated this issue in following FortiClient Cloud Services" (its advisory, as read) is the same kind of report; it never decided Fortinet's class, which FortiSOAR set. Google's case differs: its bulletin says "Google Cloud itself is not vulnerable", and its class came from products customers deploy (Apigee portals), so it is no precedent for treating a remediated own service as unaffected.
- *Fixed for all listed*, not *for some* or *no fix*: the portal is the only thing listed other than "not affected", and D-Link reports the remediation completed and the issue resolved. The PHP replacement is a further step it describes, not the fix it relies on.

What weighs the other way, and is said in the checkpoint: D-Link never says any product or service is "affected" and never uses "fixed"; *affected* is Lighthouse's reading, under the brief, of D-Link's report of remediation; and part of what D-Link describes (WAF rules) is a mitigation rather than a change to the software. A reader could still prefer *not affected* with a note; the brief's wording does not allow it as cleanly.

## Quotations and figures checked against the body

Checkpoint, D-Link section, table row, flags and commit-message text: every quotation matches the body (the "PHP2Shell" quotation uses straight for curly quotes). Publication ID SAP10524; published 10 November 2026 2:13 GMT, last updated 2:31 GMT; "Resolved Status: Yes"; listing title and "2026-11-10 GMT" date; HTTP 200 and 28,411 bytes received (found_log; the retained file is longer because an email address was replaced by the redaction marker); fetched 14:18:30 UTC; mentions 1, 1, 0 and PHP 5; listing PHP 0; 20 days from 21 October; the interval after 2026-11-09T14:29Z and at or before 2026-11-12T14:16Z. All hold. CVE-2026-115560, product versions, PHP versions and fixed releases are indeed not named.

Not verifiable from what is retained: "the gate found the host's robots.txt answering 404, no rules". The gate logs only refusals; nothing on disk records an allowed decision. Not refetched, as instructed.

The log line and this-week's line: their quotations ("emergency remediation", "no evidence of unauthorized data access resulting from exploitation") match; "a replacement due by the end of November" fairly renders D-Link's schedule; "unauthorised" in the checkpoint's opening and this-week is an unquoted paraphrase.

## What was changed (studies/LH037/checkpoints/2026-11-12T1416Z.md only)

1. D-Link's class, in the table, the class paragraph, the flags and the commit-message text: *not affected* (products and apps, portal noted separately) became *affected, fixed for all listed*, with the reasoning above and D-Link's words.
2. "The statement never uses the words 'affected' or 'fixed'" was wrong: it says "not affected" four times. Now: it never says any product or service is affected and never uses "fixed".
3. "Its networking hardware and apps don't use PHP" overstated the apps: D-Link says they "do not incorporate PHP components associated with these vulnerabilities", not that they use no PHP. Corrected in the opening and the commit-message text.
4. "PHP2Shell also appears in the Cisco, Fortinet, Google and Splunk bodies": Cisco's and Splunk's write "PHP2shell". Now says so.
5. The writer line notes this review.

panel.json carries no class, so nothing in it changed. The brief and schedule/due.csv were not touched.

## What must follow, not edited here

- notes/php-watch-log.md, "## 12 November 2026": the "Flagged for review" bullet ("its class (not affected, with the portal remediated) is a judgement") should give the reviewed class, *affected, fixed for all listed*, from D-Link's report of remediating its own portal; and the vendors bullet's "its hardware and apps do not use PHP" should say the apps do not use the PHP components concerned.
- site/this-week.md, the 2026-11-12 item: "its hardware and apps do not use PHP" needs the same correction, and "how to count the statement is not yet reviewed" is now out of date. If the class is mentioned, it should be attributed as Lighthouse's reading of D-Link's statement, with "affected" meaning the brief's class, never that the portal was attacked.
- The count "7 of 20" stands everywhere. Any tally of the rule panel's classes should put D-Link with Cisco and Oracle under *affected, fixed for all listed* (Splunk, in the named stratum, is tallied separately), leaving Zyxel the panel's only *not affected*.

## Lighthouse's voice

No sentence in the checkpoint, the log line or this-week says or implies that D-Link's systems were compromised or exploited. D-Link's only sentence on exploitation is quoted and attributed, and the checkpoint says it is no statement about attempts. The new class paragraph says *affected* is a class under the brief, "not a finding that anything was attacked or entered".
