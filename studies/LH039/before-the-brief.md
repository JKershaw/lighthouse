title: WordPress core CVE-2026-119977: what the public sources can show, read before the brief
kind: working note (study LH039, proposals.md P-0017), before any brief is fixed
date: 2026-11-07
authors: the driving session of the scheduled run 2026-11-07T1413Z (Claude Code, Opus 5.5)

**In short.** WordPress fixed a flaw in its own update process on 28 October 2026, in 7.1.4 and in a release on every branch back to 4.7, and we want to know how fast sites moved to the fixed releases. Before writing a brief we read the sources' metadata, and found that WordPress.org's public version statistics count branches (7.1, 7.0), not releases (7.1.4), so they cannot by themselves tell a fixed site from an unfixed one. The brief had to choose between sources that see releases, each counting something different; it was fixed on 8 November as [brief.md](brief.md), with W3Techs's survey of websites and Packagist's developer downloads, and the raw reads from 7 November on are its first days.

## What was read, 7 November 2026, from 14:18 UTC

All with curl (User-Agent "Lighthouse-research/1.0"), kept in data/raw-2026-11-07T1418Z/ with readlog.csv (URL, UTC start, status, content type, size, SHA-256). Outcome values in the statistics and candidate bodies were not looked at, beyond the key names of the first and the list of versions in the Packagist body's header; they are kept for the brief's first day.

- WordPress.org's statistics endpoints (stats-1 to stats-4): `api.wordpress.org/stats/wordpress/1.0/` returns a JSON object of 43 keys, `3.0` to `7.2`, one per branch, no release-level key. PHP, MySQL and locale shares were kept beside it.
- Release metadata (meta-1 to meta-4): the version-check API (1.7) offers automatic updates to 25 releases, 7.1.4, 7.0.8, 6.9.11 and so on to 4.7.39; the stable-check API marks 7.1.4 "latest", 7.0.8 and 6.9.11 "outdated", and every earlier release of the 6.9, 7.0 and 7.1 branches "insecure"; WordPress's release feed dates "WordPress 7.1.4" Wed, 28 Oct 2026 17:13:02 +0000 and says sites "that support automatic background updates" update automatically; the CVE record (CNA Wordfence, published 2026-10-31T05:33Z, updated 2026-11-04T04:56Z) lists 25 affected ranges from 4.7.0 to 7.1.3 and says the flaw allows code execution "during the upgrade window", through "predictable, web-accessible staging paths used during full-package core upgrades".
- Candidate per-release sources (cand-1 to cand-6), kept unread: WordPress.org's download counter page, twice; W3Techs's WordPress pages, overall and for branch 7, which links per-branch pages; Packagist's stats for roots/wordpress and johnpbloch/wordpress-core, Composer packages of WordPress core whose per-version daily downloads Packagist publishes.

## What this means for the brief

1. **The branch statistics cannot measure the fix.** The fix went to every affected branch, and the endpoint has no key below the branch, so a site on 7.1.3 and one on 7.1.4 count alike. What it can show is the branch mix: how many sites sit on branches below 4.7, which the CVE record does not list as affected, and how the mix moves when 7.2 ships (planned for 8 December, by the release post). That is context, not uptake.
2. **Release-level views each count something else.** W3Techs reports per-release shares of the websites it surveys, but in LH033 it visited each site only about once a month, so a fortnight's movement is mostly its schedule. Packagist counts Composer fetches of each version, a channel of developers and build systems, not of sites updating themselves, which is the channel this flaw lives in. The download counter counts downloads of the current package; whether automatic updates reach it is not stated on any page read so far, and the brief must find out from WordPress's own documentation or leave it unknown.
3. **The update is the exposure.** By the CVE record, the window is the upgrade itself, so a site that updates is briefly exposed while it does. No public source read here says when sites update; the brief should not imply that uptake measures exposure.
4. **A link to another investigation.** The 7.1.4 release post credits Anthropic with reporting two of its stored cross-site-scripting flaws (privacy data removal requests, and specially crafted user logins). Those are not CVE-2026-119977, but they bear on investigations/model-found-bugs.md, which asks what happens when an AI model finds a serious flaw; whether these were found by a model is not said in the post, and that investigation should weigh them at its next checkpoint, with the model disclosure that Lighthouse runs on Anthropic's models.

## Until the brief

A raw read of the same endpoints each day, with its UTC start, so the days before the brief are not lost (rows LH039-raw-2026-11-08 to LH039-raw-2026-11-14, by scripts/collect.py). The brief decides which of these sources carry its question and says what was read before it was fixed. It was fixed on 8 November as [brief.md](brief.md).
