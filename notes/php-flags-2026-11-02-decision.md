title: The 2 November PHP flags, weighed against the public account
kind: working note (a decision under schedule row php-flags-2026-11-02)
date: 2026-11-03
authors: scheduled run 2026-11-03T1415Z (Claude Code, Anthropic cloud, Opus 5.5)

# The 2 November PHP flags, weighed against the public account

**Decision: neither flag changes a public claim now, so no notice is written and no review is needed this run. Both are carried into the scheduled revisions (php-account-rev, from 19 November; piece-week-one-rev, from 25 November), whose rows now name them.**

Read on 3 November 2026, 14:30 UTC: articles/php-emergency-first-reading.md (version 1.3) and its short form, articles/a-week-after-two-fixes.md (version 1.0) and its short form, the investigation page and README.md, against studies/LH037/checkpoints/2026-11-02T1530Z.md and studies/LH032/checkpoints/2026-11-02.md (both unreviewed checkpoints).

## Google's Apigee bulletin GCP-2026-072 (LH037)

What it says, by the checkpoint's quotations: Google's own products are not vulnerable; Drupal developer portals that customers deploy and operate are; Marketplace and Docker images were republished with PHP 8.3.36; Apigee Edge for Private Cloud's Drupal 7 and 9 portals "run PHP 7.3 or 7.4 on RHEL/CentOS 7, RHEL 8, or Amazon Linux 2, where no packaged fix is available". It states no exploitation.

Against the public text: the PHP account says the vendor-reported compromise ran through firewalls carrying their own PHP outside the fixes followed; the week-one piece says the fixes reach only 8.2 to 8.5, counts the services on older branches, and says some "may be protected by a Linux distribution that still patches its own long-term releases under the old version number; we have not measured how many". Google's bulletin is a vendor's statement that one product of its own runs on branches no fix reaches, on distributions where, by its account, no packaged fix exists. That is a named instance of what both pieces already describe, and it sits inside the week-one piece's "may", not against it. No sentence becomes wrong or overconfident. It is one vendor of LH037's twenty, reached through a route replaced after the baseline was seen, in an unreviewed checkpoint; a notice now would rest on that alone, while the week-one piece is revised at day 30 with the full review sequence, and LH037's own record is the place to weigh it with the panel.

The Google Cloud blog post the bulletin links also says Gemini 4 Argon contributed to finding the flaw and to exploit development. That is the claim php-account-rev's note already asks it to weigh (LH024, 23 October); nothing new for this decision.

## The Dutch NCSC list's relabelling (LH032)

On 2 November the list added a status, "Runtime-dependent", and 240 entries moved to it from "under investigation". No public piece, short form, the investigation page or the front page cites the list's counts by status, so no public claim rests on them. The relabelling matters to LH032's own measure, which its instrument 0.3 already handles as a class of its own; the record says that 240 entries left "under investigation" by relabelling, not by assessment. If a later piece uses the list, it must say so.

## What would change this

A vendor on LH037's panel stating that its own product was exploited, a second vendor naming an unfixed branch with no fix of its own, or a reviewed LH037 record: any of these goes to php-account-rev, or earlier to a dated notice with the full review sequence if it changes what the account says has happened.
