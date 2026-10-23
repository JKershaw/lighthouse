# R-0033: Reader-and-inference review of the PHP account, version 1.1

Written by a Claude Code review subagent on Claude Fable 5.1, 23 October 2026, from the full piece, its short form, the front-page section and the two rendered figures only.

## What a reader would believe, written before reading the record

PHP fixed two emergency flaws on 21 October, but Amazon says a decoy server saw an exploit attempt on 17 October, so the story starts before the patch. AI helped a researcher find a flaw; people and organisations coordinated the response; nothing shows attackers using AI. Fixes reached selected registry images within a day, but nobody knows how many sites pulled or run them.

I would now believe PHP has disclosed a third, separately numbered flaw that the 21 October releases, and so those images, do not close. PHP calls it unlikely: it needs an application configured for one of two session formats whose code switches to a third before starting a session, with upload progress on. Turning upload progress off closes it, PHP treats it as regular business, and anyone who set that on 21 October need do nothing more.

Observed: provider statements and their edit times, image manifests and layers, PHP's notice first retained at 17:00 UTC on 23 October. Explained: why a firewall rule, a published image and a honeypot hit each stop short of a fixed or compromised site, and why PHP's 10:12 stamp is not a publication time. Caused: AI-assisted discovery led to the release, the release to rules and rebuilt images, the new flaw to PHP's notice and Cloudflare's revision. How the 17 October sender knew is unexplained.

Limits: no counts of attacks, intrusions, fixed sites or affected applications; chosen images, not a sample; four of ten institutions unknown; Amazon's text not replayable offline; every clock is a source's own.
