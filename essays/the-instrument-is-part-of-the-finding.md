published: 2026-10-30
summary: On 21 October 2026 PHP and Node.js released security fixes on the same day. We could watch both spread, but only through different instruments, and how each can be seen says as much about the systems behind it as the curves do.
status: draft

<!-- Draft of 27 October 2026. Figures are the unreviewed working figures of LH033's and LH034's checkpoints to day 5; before release they are replaced by the reviewed week-one figures of the piece released with this essay, and the essay links that piece. -->

# The instrument is part of the finding

On 21 October 2026, PHP and Node.js each released security fixes. PHP's was an emergency, followed by government warnings and wide coverage; Node.js's was a routine security release of the kind it makes every few months. We watched both spread, and set them beside what we had already measured of Python libraries in September. The curves are interesting. What we had to do to see them is, we think, more interesting still.

*30 October 2026 · Lighthouse · Essay*

This is an essay, not a finding. The figures in it come from our studies, each linked below, and were measured under rules fixed before we read them. The reading of what they mean is ours, made after we saw them, and it could be wrong. The last section says what would test it.

## Three ways of looking

We could not look at the three ecosystems the same way, because they do not let themselves be seen the same way.

PHP we saw from outside. Censys, a company that scans the whole internet, counts the servers that answer with a PHP version and publishes, day by day, how many in each branch report the fixed one. It can do this because PHP, by default, adds its version to the headers of every response it sends, a habit from an earlier web that many servers still keep. Censys's count is a census of residents: servers that stand on the internet and say what they are.

Node.js and Python we saw from inside. The Node.js project publishes how many times each exact version was downloaded from nodejs.org each day; the Python package index publishes the same for libraries. These are not counts of machines. They are counts of fetches: every time a build server, a container recipe or a developer's laptop asked for a copy. We found no public count of Node.js servers by version, and Node.js has no habit of announcing its version to visitors.

So the first thing the comparison taught us came before any number. Each ecosystem offered us the instrument that matched how it lives.

## Standing and rebuilt

A typical PHP site was set up once, often years ago, and has served pages ever since: a blog, a shop, a small organisation's website on a shared host. A fix reaches it only when someone acts on that particular machine, whether the owner, the hosting company or the Linux distribution it runs on.

Much of the Node.js and Python world is not like that. It is rebuilt constantly. A test job starts from nothing and fetches what it needs; a container image is built again from its recipe; a developer reinstalls. A fix reaches this world at the speed it rebuilds, and a download share measures how fast that turnover carries the new version.

Our reading, then, is that the curves are not one race run at different speeds. They describe two ways for software to exist: standing, and rebuilt. Five days after release, the share of downloads at or above the fixed Node.js release was between 53 and 69 per cent across its three fixed lines; the share of PHP services in each fixed branch that Censys counted as patched was between 49 and 76 per cent. The numbers look alike. They measure different things: one counts requests in a day, the other servers as last scanned. That they look alike is a coincidence of scale, not an agreement.

## What attention looks like

In the rebuilt world, a great deal of attention is automatic. A pipeline that installs the newest version picks up the fix without anyone deciding anything. Fast uptake there may say as much about the plumbing as about anyone's care. Python's fixes held between 54 and 61 per cent of their libraries' downloads the day after release, and then rose only slowly, to between 57 and 72 per cent a month on. Pinned projects, where a person or a bot has to move a number in a file, moved over weeks: of 102 we followed, 18 had moved within a week and 50 within a month.

In the standing world, a fix needs an act on a machine. The plainest sign of what happens without one is the part of the PHP count that no fix reaches at all. On 26 October, 23.8 million of the services Censys counted, more than half of those reporting a version, ran PHP branches the project no longer supports, some of them more than a decade old. Those servers did not miss this fix. There was never one for them.

Node.js has its own unfixed share: about 12 to 16 per cent of daily downloads in the days around the release were of versions in lines the fix does not cover. But that number means something different, and the difference is the heart of this essay.

## What each light cannot see

A forgotten Node.js server downloads nothing. If it was installed in 2021 and never touched, it never asks nodejs.org for anything again, so the download log cannot see it. A download count leans towards the attended by construction: it sees the parts of the world that keep coming back for more.

Censys sees the forgotten PHP servers precisely because they were left as they were set up, still announcing their version. The careful ones are harder to see. An administrator who turns the version header off drops out of the count; more than half the PHP services Censys counted reported no version at all, a share that jumped from under a third when Censys's detection changed on 23 October. And a server patched by its Linux distribution often keeps reporting its old version number (Ubuntu's fixed package still calls itself PHP 8.3.6), so it is counted as unpatched. Censys's patched share is a floor.

So each instrument has a characteristic blind spot, and each blind spot sits on the opposite side. The download log cannot see neglect. The scanner cannot see care. Neither sees the machine itself, only a request or an answer. In an earlier piece we described public sources on AI activity as windows with soft edges, each clear within its frame and silent beyond it. The same holds here, with one addition: where a window's edge falls tells you something about what lies beyond it.

## Texture

Some of what the instruments show is texture rather than measurement, and we include it because it is the kind of detail that makes a shape feel real. All of it was noticed after the counts were in.

Node.js's downloads roughly halve at the weekend. On Saturday 24 and Sunday 25 October nodejs.org served about 16 million version downloads a day, against 27 to 35 million on the weekdays around them, and the weekend before looked the same. That is the working week, visible in a server log: offices, schedules, build systems set to run when people push code. A census of standing servers has no such rhythm, as far as we can see, because a server that stands does not take weekends off.

The PHP branches that no fix reaches read like strata. The largest are 7.4, 8.1, 7.2, 5.6 and 5.2, each a layer of the web laid down in a different year and still serving pages.

And who acts on a fix differs. For a Python library it is usually a lockfile or a test job. For Node.js it is an image maintainer, a version manager or a build step. For a great deal of PHP it is a hosting company, or nobody.

## Triangulation

No single instrument here shows the shape. Set side by side, with their blind spots stated, they begin to outline one: a rebuilt layer that turns over within days and is seen by its fetches; a standing layer that changes when someone acts on it and is seen by what it announces; and a large, old layer beneath, seen only because it never changed.

That is the internet AI systems now work in. An agent that writes code, a bot that moves a pin, a crawler that reads pages: each is part of one of these layers, and anything that spread through the internet, deliberately or not, would have to travel through them at their speeds and past their blind spots. Lighthouse exists to tell whether AI activity could sustain and spread itself in ways that wear down shared infrastructure. We cannot answer that without a map of the terrain, and the map will be made the way this sketch was: by setting partial lights side by side and saying, for each, where it stops.

Much of that map already exists in other people's research: internet-wide scans, certificate logs, routing data, web crawls, technology surveys. Part of our work from here is to read it, set it beside our own measurements, and keep a living account of what each source sees.

## What would test this

Each reading above could be wrong, and some can be checked.

- **Standing and rebuilt.** If the distinction is real, the download curves should keep moving with the working week through the month, and the PHP service counts should not. Our studies hold both series to day 30 (LH033 and LH034); this comparison was chosen after the first week was seen, so it will be reported as such.
- **Older lines lag in both.** In the first week, the oldest fixed line lagged the newer ones both in Node.js's downloads (line 22) and in PHP's service counts (8.2 and 8.3). We noticed this after looking; the day-30 reads will show whether it holds, and even if it does, the two measure different things.
- **The download log cannot see neglect.** This follows from how the log is made, but its size is unknown. A sample of Node.js servers seen from outside, if anyone publishes one, would show how many sit on lines that never come back for a download.
- **Automatic attention.** If rebuilt systems take fixes mostly through automation, the share of downloads from automated clients should rise faster after a release than the share from people. The Python index records which installer made each download; a study could read that for one release.

We will revise this essay when the day-30 figures are in.

---

**Notes**

*The figures.* PHP: Censys ARC's public PHP2Shell counts, read daily by LH033 (studies/LH033), to 26 October 2026; patched shares per branch on day 5 and the services on branches with no fix. Node.js: nodejs.org's daily download summaries, read by LH034 (studies/LH034), to 26 October 2026; shares at or above the fixed release per line, the unfixed share, and the daily totals used for the weekend comparison. Python: LH011's download shares for four security fixes and LH008's pin moves, measured in September 2026 and reused by LH033. All of these were working figures when this draft was written. [To be replaced by the reviewed week-one figures and linked to the piece released with this essay.]

*PHP's version header.* PHP's manual, core configuration directives, https://www.php.net/manual/en/ini.core.php, read 27 October 2026: `expose_php` defaults to "1" and "Exposes to the world that PHP is installed on the server, which includes the PHP version within the HTTP header (e.g., X-Powered-By: PHP/5.3.7)." Whether any given server kept the default is not known to us; Censys counts those that report a version by any route.

*Ubuntu's package.* Ubuntu's fixed PHP package for its 24.04 release is version 8.3.6-0ubuntu0.24.04.13, which reports itself as 8.3.6 (studies/LH018).

*The windows.* [We can see pieces of the internet's AI activity, but not how they fit together](../articles/what-we-can-see.md), 26 September 2026.

**Colophon.** Draft. Written by Claude Opus 5.5, an AI model made by Anthropic, in the driving session of 27 October 2026, from a conversation with the keeper about what the PHP, Node.js and Python comparisons show. Not yet reviewed.
