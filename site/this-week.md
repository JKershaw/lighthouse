<!--
This file is the front page's "This week" block (read by site/lib/front.js,
thisWeek; shown by site/_includes/home-this-week.njk). It is kept here, in one
place, by the scheduled run at its editor's step (schedule/runner.md, step 7),
and by any session that releases, opens or decides something a returning
reader should hear about.

Each time you update it:
1. Set `updated` to today (UTC, YYYY-MM-DD) and `week` to the seven days
   ending today: "<today minus 6 days> to <today>".
2. Drop items dated before the week's first day. The site hides them anyway,
   and hides the whole block when `updated` is more than 8 days before the
   build, so a missed update shows nothing rather than an old week.
3. Add one item for each thing since the last update that a returning reader
   would want: a piece or essay released or corrected; an investigation
   opened or closed; a study begun (its brief fixed) or answered; a keeper
   decision that changes what Lighthouse does; an outside event Lighthouse
   follows. Not routine reads, checkpoints that change no account, or process.
4. Write each as `- YYYY-MM-DD | reported | sentence` for something others
   published (say who, link their own page so a reader can see their words,
   and link our record of it where we keep one), or
   `- YYYY-MM-DD | lighthouse | sentence` for our own work (link the page).
   Link a study by its brief or record as usual: the build sends the reader
   to the study's own page, which opens in plain words, and adds a short
   link to its investigation, so don't add either yourself. Link each item
   to its study or investigation wherever it has one: the front page's
   investigation cards show their newest linked item as "Latest".
   One or two plain sentences in Markdown, repository paths from the root.
   No internal codes (no LH, P, R or L numbers, row ids, step numbers or file
   names in the text), British English, no em or en dashes, no figure that is
   not in a released piece or the cited source, and no claim in our voice that
   harm is happening or that a named system is compromised.
   Write for a person, not an agent (the keeper, 13 November 2026): lead
   with what happened and why a reader might care, and keep any caveat to
   one short clause; the formal limits are in the page you link.
5. Newest first. Keep every item dated within the week, however many: the
   This week page is the whole week (the keeper, 18 November 2026; the
   earlier cap of six items dropped things from the middle of the week).
6. Pick the front page's three (the keeper, 18 November 2026): mark the
   items a returning reader most needs, so a busy day doesn't push the
   week's biggest news off the front page, as `- YYYY-MM-DD | kind | front |
   sentence`. At most three count; unmarked places go to the newest items.
   Review the picks at every update: drop the mark from an item a newer one
   outranks, and from any item about to leave the week.

The block shows no finding. Whether the editor may change it without review is
the gate's decision on proposals.md P-0018.
-->
title: This week
week: 2026-11-20 to 2026-11-26
updated: 2026-11-26
today: 2026-11-26 | The UN page for the Geneva conference on conventional weapons now lists a final document marked as adopted; we plan to read it on 27 November. Google now says its patched PHP runtimes also cover the session flaw PHP warned of in October.
items:
- 2026-11-26 | reported | [The UN's page](https://meetings.unoda.org/ccw-revcon/convention-on-certain-conventional-weapons-seventh-review-conference-2026) for the Geneva review conference of the conventional weapons treaty now says it "took place" and lists a "Final document - as adopted", which it didn't on 21 November. We haven't read it yet, so we can't say what, if anything, it says about autonomous weapons; [we plan to read it](studies/LH050/checkpoints/2026-11-26-read.md) on 27 November.
- 2026-11-25 | lighthouse | front | A month after [PHP's](studies/LH033/LH033.md) and [Node.js's](studies/LH034/LH034.md) security fixes of 21 October, both counts we followed had done most of their rising within two weeks. [Our revised piece](articles/a-week-after-two-fixes.md)
- 2026-11-25 | lighthouse | Our essay on watching PHP from outside and Node.js from inside now runs to day 30: one of its two readings held, and the other passed but is weaker than we first wrote it. [The essay](essays/seen-from-outside-seen-from-inside.md)
- 2026-11-25 | lighthouse | We've read Amazon's report once, unreviewed: what it says the agents did rests on the operator's own records, and it gives no date for the operation against the imaging tool. [Our study](studies/LH059/brief.md)
- 2026-11-24 | lighthouse | front | We'll study the defensive side: which defences work, how fast fixes arrive and how well organisations recover, never how self-spreading AI activity could be built. Two desk studies go with [the decision](notes/keeper/2026-11-24-defensive-side.md): what research has measured about [containment and recovery](studies/LH061/brief.md), and about [how operators of different sizes install fixes](studies/LH060/brief.md).
- 2026-11-24 | reported | front | [Amazon reported](https://aws.amazon.com/blogs/security/chinese-nexus-actors-cairn-ai-agents-found-a-zero-day-on-their-own/) on 20 November that AI agents run by an actor it calls "Chinese-nexus", at moderate confidence, whose stated goal was to "obtain shell access", found and used a flaw it judges unpublished in a medical-imaging AI tool, "on their own". [We'll sort each claim](studies/LH059/brief.md) by what it rests on: Amazon's own view, the agents' records or independent confirmation.
- 2026-11-24 | lighthouse | A month after Node.js's security releases of 21 October, 65.5% to 96.3% of each fixed line's downloads from nodejs.org were the fix or newer, if three later versions are counted as carrying the fix, which we assumed without checking; without them, 39.8% to 85.8%. [Our reviewed record](studies/LH034/LH034.md)
- 2026-11-24 | lighthouse | On 21 October a poisoned LiteLLM release, software that routes requests to AI models, was up for about an hour and three quarters, and PyPI's logs as ClickPy holds them record 49,043 fetches of it that day. Per hour, by our reading, that's no faster than an ordinary new release and probably at the low end. [Our reviewed record](studies/LH040/LH040.md)
- 2026-11-24 | lighthouse | npm's public counts put 202 fetches of the tampered bee-js release on 9 to 12 November together, the day it was briefly up and the three after; under the rules we set they can't be split by day, though a check made after the counts were seen points to all 202 on the first day. [Our reviewed record](studies/LH049/LH049.md)
- 2026-11-23 | lighthouse | Thirty days after October's emergency PHP fix, Censys counted 75% to 92% of each fixed branch's services patched, nearly all within two weeks. [Our reviewed record](studies/LH033/LH033.md)
- 2026-11-23 | reported | The fix for PHP's newer session flaw is now listed: [the CVE record](https://www.cve.org/CVERecord?id=CVE-2026-115560), Debian, Red Hat and SUSE put it at PHP's 19 November releases, while Ubuntu lists no fix yet, CERT-EU still tells readers to switch the feature off and Cloudflare still says a fix is coming. [Our last scheduled read](studies/LH030/checkpoints/2026-11-23.md), unreviewed.
- 2026-11-23 | lighthouse | We audited our own requests again, for 16 to 22 November: of 1,649 we logged, 2 broke a robots.txt rule under our own name and 53 broke some rule, mostly by coming sooner than a site's requested delay or going back to a page that had shown a wall. That's far fewer than 8 November's 97 robots.txt breaches, mostly because one collector isn't in this week; it isn't a trend. [Our reviewed record](studies/LH047/LH047.md)
- 2026-11-22 | reported | Microsoft's report on its Microsoft 365 outage of 12 and 13 November, dated 20 November and read from [a consultancy's copy](https://www.365fanatic.com/wp-content/uploads/2026/11/postincidentreport-mo1550821.pdf), blames a Windows defect, maintenance and a surge of traffic, and says "This change was not caused by AI tooling". That's narrower than the status post's "not related to cyber or AI / agents", so [our comparison](notes/microsoft-outage-report/comparison.md) calls the exclusion qualified: neither confirmed nor contradicted. More on [the investigation's page](investigations/ai-cost-and-spread.md).
- 2026-11-22 | lighthouse | How fast did websites take WordPress's fix of 28 October? A survey of sites shows the newest branch's share on the fix climbing to 38% by day 24, but by our reading it visits each site about once a month, so it can't tell us how fast sites moved; downloads by developers and build tools switched within days on that branch. [Our reviewed record](studies/LH039/LH039.md)
- 2026-11-21 | lighthouse | We've changed how we follow the rules websites set for automated readers. A single read we make on purpose now follows what the site says about reads a person asks for, while regular collection keeps the strict rule; and where a site refuses AI training or archiving crawlers, we keep no copy of its pages, only the facts we use, since what we keep is public. [The decision](notes/keeper/2026-11-21-robots-intent.md)
- 2026-11-21 | lighthouse | We found no adopted text on autonomous weapons yet: a day after the Geneva review conference of the UN's conventional weapons treaty was due to close, its official page listed no adopted final document and no decision on further talks, and the latest draft we could read still left those passages blank. [We'll check again](studies/LH050/LH050.md) on 27 November.
- 2026-11-21 | lighthouse | Whether SUSE's fixes for the kernel flaw Anthropic's model found were public before Anthropic's post stays unknown: SUSE's own announcement list dates every SUSE advisory we follow after the post, but their pages carry earlier release dates whose meaning isn't stated. [Our timeline](studies/LH038/LH038.md)
- 2026-11-20 | lighthouse | Eight big services went down between 12 and 17 November, and a newspaper's unnamed sources, then two members of Congress, have tied the week to the strain of patching flaws that AI models find. Until 1 January [we'll keep a ledger](studies/LH058/brief.md) of each operator's stated cause beside every claim of an AI link and what it rests on, and we won't read silence as a denial.
- 2026-11-20 | lighthouse | Security firm GreyNoise keeps [a public tracker](https://php.events.greynoise.io/) of attacks on October's two emergency PHP flaws against its own decoy servers. [We'll read it daily](studies/LH057/brief.md) until 3 December, as a count of attacks on those sensors, not of victims.
