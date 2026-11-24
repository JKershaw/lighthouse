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
week: 2026-11-18 to 2026-11-24
updated: 2026-11-24
today: 2026-11-24 | GreyNoise's decoy servers have logged no confirmed successful attack on October's PHP flaws since the one on 20 November. From 13 to 23 November, npm's counts hold no record of the tampered bee-js release.
items:
- 2026-11-24 | lighthouse | front | Our keeper confirmed that we study the defensive side: which defences work, how fast fixes arrive and how well organisations recover, never how self-spreading AI activity could be built. Two desk studies go with [the decision](notes/keeper/2026-11-24-defensive-side.md), on what research has measured about [whether containment and recovery work](studies/LH061/brief.md) and about [operators of different sizes installing fixes](studies/LH060/brief.md).
- 2026-11-24 | reported | front | [Amazon reported](https://aws.amazon.com/blogs/security/chinese-nexus-actors-cairn-ai-agents-found-a-zero-day-on-their-own/) on 20 November that AI agents run by an actor it calls "Chinese-nexus", at moderate confidence, whose stated goal was to "obtain shell access", found and used a flaw it judges unpublished in a medical-imaging AI tool that CISA lists as MONAI Label, "on their own". [We'll sort each claim](studies/LH059/brief.md) by what it rests on: Amazon's own view, the agents' records or independent confirmation.
- 2026-11-24 | lighthouse | A month after Node.js's security releases of 21 October, 65.5% to 96.3% of each fixed line's downloads from nodejs.org were the fix or newer, if three later versions are counted as carrying the fix, which we assumed without checking; without them, 39.8% to 85.8%. [Our reviewed record](studies/LH034/LH034.md)
- 2026-11-24 | lighthouse | On 21 October a poisoned LiteLLM release, software that routes requests to AI models, was up for about an hour and three quarters, and PyPI's logs as ClickPy holds them record 49,043 fetches of it that day. Per hour, by our reading, that's no faster than an ordinary new release and probably at the low end. [Our reviewed record](studies/LH040/LH040.md)
- 2026-11-24 | lighthouse | npm's public counts put 202 fetches of the tampered bee-js release on 9 to 12 November together, the day it was briefly up and the three after; under the rules we set they can't be split by day, though a check made after the counts were seen points to all 202 on the first day. [Our reviewed record](studies/LH049/LH049.md)
- 2026-11-23 | lighthouse | front | Thirty days after October's emergency PHP fix, Censys counted 75% to 92% of each fixed branch's services patched, nearly all within two weeks. [Our reviewed record](studies/LH033/LH033.md)
- 2026-11-23 | reported | The fix for PHP's newer session flaw is now listed: [the CVE record](https://www.cve.org/CVERecord?id=CVE-2026-115560), Debian, Red Hat and SUSE put it at PHP's 19 November releases, while Ubuntu lists no fix yet, CERT-EU still tells readers to switch the feature off and Cloudflare still says a fix is coming. [Our last scheduled read](studies/LH030/checkpoints/2026-11-23.md), unreviewed.
- 2026-11-23 | lighthouse | We audited our own requests again, for 16 to 22 November: of 1,649 we logged, 2 broke a robots.txt rule under our own name and 53 broke some rule, mostly by coming sooner than a site's requested delay or going back to a page that had shown a wall. That's far fewer than 8 November's 97 robots.txt breaches, mostly because one collector isn't in this week; it isn't a trend. [Our reviewed record](studies/LH047/LH047.md)
- 2026-11-22 | reported | Microsoft's report on its Microsoft 365 outage of 12 and 13 November, dated 20 November and read from [a consultancy's copy](https://www.365fanatic.com/wp-content/uploads/2026/11/postincidentreport-mo1550821.pdf), blames a Windows defect, maintenance and a surge of traffic, and says "This change was not caused by AI tooling". That's narrower than the status post's "not related to cyber or AI / agents", so [our comparison](notes/microsoft-outage-report/comparison.md) calls the exclusion qualified: neither confirmed nor contradicted. More on [the investigation's page](investigations/ai-cost-and-spread.md).
- 2026-11-22 | lighthouse | How fast did websites take WordPress's fix of 28 October? A survey of sites shows the newest branch's share on the fix climbing to 38% by day 24, but by our reading it visits each site about once a month, so it can't tell us how fast sites moved; downloads by developers and build tools switched within days on that branch. [Our reviewed record](studies/LH039/LH039.md)
- 2026-11-21 | lighthouse | We've changed how we follow the rules websites set for automated readers. A single read we make on purpose now follows what the site says about reads a person asks for, while regular collection keeps the strict rule; and where a site refuses AI training or archiving crawlers, we keep no copy of its pages, only the facts we use, since what we keep is public. [The decision](notes/keeper/2026-11-21-robots-intent.md)
- 2026-11-21 | lighthouse | We found no adopted text on autonomous weapons yet: a day after the Geneva review conference of the UN's conventional weapons treaty was due to close, its official page listed no adopted final document and no decision on further talks, and the latest draft we could read still left those passages blank. [We'll check again](studies/LH050/LH050.md) on 27 November.
- 2026-11-21 | lighthouse | Whether SUSE's fixes for the kernel flaw Anthropic's model found were public before Anthropic's post stays unknown: SUSE's own announcement list dates every SUSE advisory we follow after the post, but their pages carry earlier release dates whose meaning isn't stated. [Our timeline](studies/LH038/LH038.md)
- 2026-11-20 | lighthouse | Eight big services went down between 12 and 17 November, and a newspaper's unnamed sources, then two members of Congress, have tied the week to the strain of patching flaws that AI models find. Until 1 January [we'll keep a ledger](studies/LH058/brief.md) of each operator's stated cause beside every claim of an AI link and what it rests on, and we won't read silence as a denial.
- 2026-11-20 | lighthouse | Security firm GreyNoise keeps [a public tracker](https://php.events.greynoise.io/) of attacks on October's two emergency PHP flaws against its own decoy servers. [We'll read it daily](studies/LH057/brief.md) until 3 December, as a count of attacks on those sensors, not of victims.
- 2026-11-19 | lighthouse | Websites ask automated readers to keep out of some pages or slow down, and most of those asks are requests nothing enforces. [Our new paper](articles/rules-for-robots.md) reads what others have measured, then checks our own agents: on one November evening, 113 of the 3,497 requests we could find broke a rule we'd set down before checking.
- 2026-11-19 | reported | [PHP's news page](https://www.php.net/) lists PHP 8.5.13, 8.4.28, 8.3.37 and 8.2.36, dated 19 November, the first regular releases since October's emergency fix. PHP had suggested switching off a feature until this release to guard against a newer flaw, and promised a full advisory with it; we'll read what they say about it on Monday, [in our watch of that flaw](studies/LH030/checkpoints/2026-11-19.md).
- 2026-11-19 | reported | The US cyber agency CISA added a flaw in LiteLLM, open-source software that routes requests to AI models, to [its catalogue of vulnerabilities known to be exploited](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) on 18 November. It concerns a test endpoint, not the poisoned LiteLLM release [we've been following](studies/LH040/LH040.md); we've only read the catalogue entry.
- 2026-11-19 | lighthouse | Do requests for a package's metadata file swell Python download counts? Almost certainly not for boto3 on 17 November: a public copy of the index's log had no such row among its nearly 80 million downloads that day, most likely because the log doesn't record them. [Our record](studies/LH013/LH013.md)
- 2026-11-18 | reported | Three security firms ([Socket](https://socket.dev/blog/agent-framework-pypi-package-compromised-with-credential-stealer), [Aikido](https://www.aikido.dev/blog/two-malicious-agent-framework-releases-hit-pypi-in-33-minutes) and [StepSecurity](https://www.stepsecurity.io/blog/microsoft-agent-framework-pypi-package-compromised)) report that agent-framework 1.26.1 and 1.26.2, a Python package for AI agents published as Microsoft's, carried code that steals cloud and AI keys; PyPI has quarantined both. We don't give security advice, but we'll [count how often each was fetched](studies/LH056/brief.md).
- 2026-11-18 | lighthouse | When was the kernel flaw Anthropic's model wrote an exploit for reported? No public source we could read says. The fix reached stable kernels on 11 and 15 October, and its CVE came on 15 October, 12 days before Anthropic's post; [our dated timeline](studies/LH038/LH038.md) sets each step beside the parties' own disclosure rules.
- 2026-11-18 | reported | [A well-known Microsoft 365 commentator reports](https://office365itpros.com/2026/11/16/exchange-online-outage-nov26/) that Microsoft has issued a preliminary report on last week's outage, blaming a latent Windows defect, extra traffic and reduced capacity, with a final report still to come. We couldn't read Microsoft's own text, so [our watch](notes/microsoft-outage-report/readings/2026-11-18.md) goes on.
