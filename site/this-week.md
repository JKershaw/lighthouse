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
   published (say who, and link their page or our record of it), or
   `- YYYY-MM-DD | lighthouse | sentence` for our own work (link the page).
   One or two plain sentences in Markdown, repository paths from the root.
   No internal codes (no LH, P, R or L numbers, row ids, step numbers or file
   names in the text), British English, no em or en dashes, no figure that is
   not in a released piece or the cited source, and no claim in our voice that
   harm is happening or that a named system is compromised.
5. Newest first, at most six items; drop the oldest beyond six.

The block shows no finding. Whether the editor may change it without review is
the gate's decision on proposals.md P-0018.
-->
title: This week
week: 2026-11-06 to 2026-11-12
updated: 2026-11-12
items:
- 2026-11-12 | reported | D-Link says, in a statement of 10 November, that its hardware and apps do not use PHP and were not affected by October's PHP flaws, but that older parts of its mydlink cloud portal ran on PHP and have had emergency remediation, with no evidence of unauthorised data access. It is the first vendor we follow to say it ran PHP in a service of its own; our [daily log](notes/php-watch-log.md) has the details.
- 2026-11-11 | lighthouse | We released [a knowledge map](map/knowledge-lineage/) of everything we have studied and published: it starts from our three questions and lets you follow an idea down to the records and evidence behind it.
- 2026-11-10 | reported | StepSecurity and Socket report that a release of bee-js, a small JavaScript library, was published to npm on 9 November with a malicious install step, through the project's own trusted publishing and with genuine provenance, and was removed about 75 minutes later. We've begun [a study of how far it travelled](studies/LH049/brief.md), read daily while npm's counts still cover its first day.
- 2026-11-10 | lighthouse | Google, Microsoft, OpenAI and Anthropic have each announced the same robots.txt label for sites that don't want their pages used to train AI, as trade press reported on 30 October. Our study of [shared services closing their doors](studies/LH044/brief.md) will now record that label too, as a stated wish rather than proof anyone obeys it.
- 2026-11-09 | lighthouse | We added a later-evidence notice to [who watches each layer of the internet](articles/who-watches-the-internet.md) and to [what we can see](articles/what-we-can-see.md): GH Archive's hourly files of GitHub's public events were all there in 2026, but whole kinds of event were missing from many of the hours we read, and nobody yet knows whether GitHub's feed or the archive lost them.
- 2026-11-09 | lighthouse | We fixed the plan for a new study of [the flaws behind Anthropic's five attack chains](studies/LH048/brief.md): how each is rated and whether the public signals of exploitation move, read on Mondays to 4 January. Only two of the five flaws are named by number in Anthropic's post.
