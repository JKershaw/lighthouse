published: 2026-10-30
summary: A week after the PHP and Node.js fixes of 21 October 2026, every fixed Node.js line and PHP branch had passed half in the two counts we followed each day, while more than half of the PHP services showing a version ran branches PHP no longer fixes.
status: released
investigation: software-updates

# A week after two fixes

How far does a security fix spread in a week? On 21 October 2026 PHP and Node.js both released one, and a week later, on 28 October, two kinds of public count gave an answer.

On Node.js's own download server, the fixed release or a newer one was 54 of every hundred downloads in its oldest fixed line and 72 in its most used; both had first passed half two days after release. Seen from outside, Censys, a company that scans the internet, counted 52 to 79 per cent of the PHP services that show a version in each fixed branch as patched, the newer branches well ahead of the older ones.

Beside those, 24.4 million PHP services, more than half of those showing a version, ran branches PHP no longer fixes, as their versions report them; some may be patched by Linux distributions under the old number, which we have not measured.

The two counts measure different things. A download is a request from a build server or a laptop, not a machine; Node.js's server is one channel of several, and a machine that never asks again is invisible. Censys's patched shares are floors, because Linux distributions often fix PHP without changing its version number and a service counts only once a rescan sees it. Neither is a measure of protection, and neither says which software's users are quicker, or why. We will revise this at a month.

[The full piece](../a-week-after-two-fixes.md)
