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
week: 2026-11-12 to 2026-11-18
updated: 2026-11-18
today: 2026-11-18 | We kept counting downloads of the tampered WhatsApp library on npm, which published a new version today, reread the reports on ARTEX (Check Point's opened for us for the first time) and began a study of a Python agent package that security firms say shipped key-stealing releases last night. Microsoft's own outage report still isn't one we can read. The reads are unreviewed; the kernel flaw's timeline and ARTEX's second round of reading were reviewed today and added to their records, without a new article.
items:
- 2026-11-18 | reported | Three security firms report that two releases of agent-framework (1.26.1 and 1.26.2, both now quarantined; PyPI's page again lists 1.26.0 as current), a Python package for building AI agents published as Microsoft's, carried code that steals cloud and AI keys, the second uploaded minutes after PyPI quarantined the first. We don't give security advice (the firms' reports are listed in our study's sources), but we'll [count how often each was fetched](studies/LH056/brief.md) that day and in the two weeks after.
- 2026-11-18 | lighthouse | When was the kernel flaw Anthropic's model wrote an exploit for reported, and to whom? No public source we could read says. The fix reached stable kernels released on 11 and 15 October, and its CVE was published on 15 October, 12 days before Anthropic's post; [our dated timeline](studies/LH038/LH038.md) sets each step beside the parties' own disclosure rules.
- 2026-11-18 | reported | A well-known Microsoft 365 commentator reports that Microsoft has issued a preliminary report on last week's outage, blaming a latent Windows defect, extra traffic and reduced capacity, with a final report still to come. We couldn't read Microsoft's own text, so [our watch](notes/microsoft-outage-report/readings/2026-11-18.md) goes on.
- 2026-11-17 | lighthouse | Did stolen AI keys pay for the hunt for more? Amazon reports that an attack operation run through AI agents worked that way, but its evidence is the agents' own records, and it says it can't verify the outcomes they report. A second, targeted round of reading, reviewed on 18 November, found no later report that adds evidence of its own. [Our record](studies/LH055/LH055.md)
- 2026-11-17 | reported | StepSecurity reports that a WhatsApp automation library on npm and its server shipped tampered releases on 15 and 16 November, published through the project's own release automation. npm keeps daily download counts for only a week, so we've [started counting](studies/LH053/brief.md) how far those releases travelled before the window closes.
- 2026-11-17 | lighthouse | A Linux kernel flaw disclosed on 15 November, credited to a person, not a model, gives us something to set beside the kernel flaw Anthropic's model found: [a small study](studies/LH054/brief.md) will follow how fast fixes and warnings arrive for each, on the same days.
