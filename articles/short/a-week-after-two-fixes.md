published: 2026-10-30
summary: A month after the PHP and Node.js fixes of 21 October 2026, both counts we followed had done most of their rising within two weeks, and what rose after came mostly from fewer PHP services counted in three branches, nearly all of them ones not counted patched, rather than more patched, and from more Node.js downloads of newer versions rather than fewer below the fix; more than half the PHP services showing a version ran branches PHP no longer fixes, though distributions may patch some under the old number.
status: released
investigation: software-updates
revised:
- 2026-11-25: Version 2.0 brings the first reading of 30 October, at day 7, to day 30; the first edition is in git at commit 16a713b.

# A month after two fixes

Does a security fix keep spreading after its first week? PHP and Node.js both released one on 21 October 2026, and we followed two public counts to 20 November.

Censys, a company that scans the internet, counted 75.0 to 92.2 per cent of the PHP services showing a version in each fixed branch as patched by then. Nearly all of that came in the first two weeks. After day 14, in three branches, the patched count barely grew; shares crept up mostly because fewer services were counted.

On Node.js's own download server, the fixed release or a newer one was 65.5 to 96.3 per cent of each fixed line's downloads. That counts three versions that appeared on 11 November as fixed, a rule we chose after seeing the counts, which assumes they carry October's fix (their own announcements, read once afterwards and not yet reviewed, don't say); without them it's 39.8 to 85.8. The late rise there was mostly more downloads at or above the fix, arriving with those versions; downloads of older versions fell only a little.

Beneath both, 22.5 million PHP services, more than half of those showing a version, ran branches PHP no longer fixes, as their versions report them; some may be patched by Linux distributions under the old number, which we haven't measured.

The counts measure different things: requests, not machines, and services seen from outside, whose patched shares are floors. Neither says which software's users are quicker, or why.

[The full piece](../a-week-after-two-fixes.md)
