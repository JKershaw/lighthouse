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
   Write for a person, not an agent (the keeper, 13 November 2026): lead
   with what happened and why a reader might care, and keep any caveat to
   one short clause; the formal limits are in the page you link.
5. Newest first, at most six items; drop the oldest beyond six.

The block shows no finding. Whether the editor may change it without review is
the gate's decision on proposals.md P-0018.
-->
title: This week
week: 2026-11-07 to 2026-11-13
updated: 2026-11-13
items:
- 2026-11-13 | lighthouse | We've started counting, hour by hour, the public traces of a campaign that StepSecurity and Aikido say used stolen GitHub accounts from 10 November to plant a script stealing build secrets, AI keys among them. We kept both firms' posts as published first; [the study's brief](studies/LH051/brief.md) says what we count and what we won't name.
- 2026-11-13 | lighthouse | Our first study of [armed AI-powered robots](studies/LH050/brief.md) has started: before an international weapons conference opens in Geneva on 16 November, we kept what public sources say about three cases and the draft conference texts, so that we can see what the week changes. None of it is a finding yet.
- 2026-11-12 | lighthouse | We've opened [an investigation of armed AI-powered robots](investigations/physical-authority.md): what they can do, who decides when they use force, and what public evidence says about what happens to civilians.
- 2026-11-12 | reported | D-Link says, in a statement of 10 November, that its networking hardware and apps were not affected by October's PHP flaws, but that older parts of its mydlink cloud portal ran on PHP and have had emergency remediation, with no evidence of unauthorised data access. Our [daily log](notes/php-watch-log.md) has the details.
- 2026-11-11 | lighthouse | We released [a knowledge map](map/knowledge-lineage/) of everything we have studied and published: it starts from our three questions and lets you follow an idea down to the records and evidence behind it.
- 2026-11-10 | reported | StepSecurity and Socket report that a release of bee-js, a small JavaScript library, was published to npm on 9 November with a malicious install step, through the project's own trusted publishing and with genuine provenance, and was removed about 75 minutes later. We've begun [a study of how far it travelled](studies/LH049/brief.md), read daily while npm's counts still cover its first day.
