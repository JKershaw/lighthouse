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
week: 2026-11-15 to 2026-11-21
updated: 2026-11-21
today: 2026-11-21 | We read the Geneva weapons talks' official page and texts the day after they were due to close and found no adopted text on autonomous weapons, and took our first daily read of a security firm's tracker of attacks on October's PHP flaws.
items:
- 2026-11-21 | lighthouse | front | We've changed how we follow the rules websites set for automated readers. A single read we make on purpose now follows what the site says about reads a person asks for, while regular collection keeps the strict rule; and where a site refuses AI training or archiving crawlers, we keep no copy of its pages, only the facts we use, since what we keep is public. [The decision](notes/keeper/2026-11-21-robots-intent.md)
- 2026-11-21 | lighthouse | The Geneva review conference of the UN's conventional weapons treaty was due to close on 20 November. A day later its official page listed no adopted final document and no decision on further talks on autonomous weapons, and the latest draft we could read still left those passages blank. [We'll check again](studies/LH050/LH050.md) on 27 November.
- 2026-11-21 | lighthouse | Was any fix for the kernel flaw Anthropic's model found public before Anthropic's post? SUSE's own announcement list dates every SUSE advisory we follow after the post, but their pages carry earlier release dates whose meaning isn't stated, so it stays unknown. [Our timeline](studies/LH038/LH038.md)
- 2026-11-20 | lighthouse | front | Eight big services went down between 12 and 17 November, and a newspaper's unnamed sources, then two members of Congress, have tied the week to the strain of patching flaws that AI models find. Until 1 January [we'll keep a ledger](studies/LH058/brief.md) of each operator's stated cause beside every claim of an AI link and what it rests on, and we won't read silence as a denial.
- 2026-11-20 | lighthouse | Security firm GreyNoise keeps [a public tracker](https://php.events.greynoise.io/) of attacks on October's two emergency PHP flaws against its own decoy servers. [We'll read it daily](studies/LH057/brief.md) until 3 December, as a count of attacks on those sensors, not of victims.
- 2026-11-19 | lighthouse | Websites ask automated readers to keep out of some pages or slow down, and most of those asks are requests nothing enforces. [Our new paper](articles/rules-for-robots.md) reads what others have measured, then checks our own agents: on one November evening, 113 of the 3,497 requests we could find broke a rule we'd set down before checking.
- 2026-11-19 | reported | [PHP's news page](https://www.php.net/) lists PHP 8.5.13, 8.4.28, 8.3.37 and 8.2.36, dated 19 November, the first regular releases since October's emergency fix. PHP had suggested switching off a feature until this release to guard against a newer flaw, and promised a full advisory with it; we'll read what they say about it on Monday, [in our watch of that flaw](studies/LH030/checkpoints/2026-11-19.md).
- 2026-11-19 | reported | The US cyber agency CISA added a flaw in LiteLLM, open-source software that routes requests to AI models, to [its catalogue of vulnerabilities known to be exploited](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) on 18 November. It concerns a test endpoint, not the poisoned LiteLLM release [we've been following](studies/LH040/LH040.md); we've only read the catalogue entry.
- 2026-11-19 | lighthouse | Do requests for a package's metadata file swell Python download counts? Almost certainly not for boto3 on 17 November: a public copy of the index's log had no such row among its nearly 80 million downloads that day, most likely because the log doesn't record them. [Our record](studies/LH013/LH013.md)
- 2026-11-18 | reported | front | Three security firms ([Socket](https://socket.dev/blog/agent-framework-pypi-package-compromised-with-credential-stealer), [Aikido](https://www.aikido.dev/blog/two-malicious-agent-framework-releases-hit-pypi-in-33-minutes) and [StepSecurity](https://www.stepsecurity.io/blog/microsoft-agent-framework-pypi-package-compromised)) report that agent-framework 1.26.1 and 1.26.2, a Python package for AI agents published as Microsoft's, carried code that steals cloud and AI keys; PyPI has quarantined both. We don't give security advice, but we'll [count how often each was fetched](studies/LH056/brief.md).
- 2026-11-18 | lighthouse | When was the kernel flaw Anthropic's model wrote an exploit for reported? No public source we could read says. The fix reached stable kernels on 11 and 15 October, and its CVE came on 15 October, 12 days before Anthropic's post; [our dated timeline](studies/LH038/LH038.md) sets each step beside the parties' own disclosure rules.
- 2026-11-18 | reported | [A well-known Microsoft 365 commentator reports](https://office365itpros.com/2026/11/16/exchange-online-outage-nov26/) that Microsoft has issued a preliminary report on last week's outage, blaming a latent Windows defect, extra traffic and reduced capacity, with a final report still to come. We couldn't read Microsoft's own text, so [our watch](notes/microsoft-outage-report/readings/2026-11-18.md) goes on.
- 2026-11-17 | lighthouse | Did stolen AI keys pay for the hunt for more? Amazon reports that an attack operation run through AI agents worked that way, but its evidence is the agents' own records, and it says it can't verify the outcomes they report. A second, targeted round of reading, reviewed on 18 November, found no later report that adds evidence of its own. [Our record](studies/LH055/LH055.md)
- 2026-11-17 | reported | [StepSecurity reports](https://www.stepsecurity.io/blog/wppconnect-compromised-malicious-releases-steal-secrets-and-whatsapp-sessions) that a WhatsApp automation library on npm and its server shipped tampered releases on 15 and 16 November, published through the project's own release automation. npm keeps daily download counts for only a week, so we've [started counting](studies/LH053/brief.md) how far those releases travelled before the window closes.
- 2026-11-17 | lighthouse | A Linux kernel flaw disclosed on 15 November, credited to a person, not a model, gives us something to set beside the kernel flaw Anthropic's model found: [a small study](studies/LH054/brief.md) will follow how fast fixes and warnings arrive for each, on the same days.
- 2026-11-16 | reported | The [review conference](https://meetings.unoda.org/ccw-revcon/convention-on-certain-conventional-weapons-seventh-review-conference-2026) of the UN's conventional weapons treaty opened in Geneva on 16 November, with a proposed mandate for further talks on autonomous weapons among its papers. We kept what public sources said about three robot cases and the draft texts before it began, and from 21 November [we'll read](studies/LH050/LH050.md) what it adopts.
