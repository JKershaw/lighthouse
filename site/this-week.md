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
week: 2026-11-11 to 2026-11-17
updated: 2026-11-17
today: 2026-11-17 | We took the last daily reads of the bee-js and WordPress watches, followed the public timeline of the Linux kernel flaw Anthropic wrote about, and began counting downloads of two npm releases that StepSecurity says were tampered with. Microsoft's full report on last week's outage still hasn't appeared. None of it has been reviewed. This evening we also read six reports on ARTEX, an AI hacking tool, for a new study, and its first record has been reviewed.
items:
- 2026-11-17 | lighthouse | Did stolen AI keys pay for the hunt for more? Amazon reports that an attack operation run through AI agents worked that way, but its evidence is the agents' own records, and it says it can't verify the outcomes they report. Nothing else we read confirms or contradicts it yet. [Our first look](studies/LH055/LH055.md)
- 2026-11-17 | reported | StepSecurity reports that a WhatsApp automation library on npm and its server shipped tampered releases on 15 and 16 November, published through the project's own release automation. npm keeps daily download counts for only a week, so we've [started counting](studies/LH053/brief.md) how far those releases travelled before the window closes.
- 2026-11-17 | lighthouse | A Linux kernel flaw disclosed on 15 November, credited to a person, not a model, gives us something to set beside the kernel flaw Anthropic's model found: [a small study](studies/LH054/brief.md) will follow how fast fixes and warnings arrive for each, on the same days.
- 2026-11-16 | reported | The review conference of the UN's conventional weapons treaty opens in Geneva today, with a proposed mandate for further talks on autonomous weapons among its papers. We kept what public sources said about three robot cases and the draft texts before it began, and from 21 November [we'll read](studies/LH050/LH050.md) what it adopts.
- 2026-11-14 | reported | Microsoft 365 was disrupted from 12 to 14 November. Microsoft's early account, as an affected university reproduced it, blamed a network change and said it was "not related to cyber or AI / agents". We're [watching for its promised full report](notes/microsoft-outage-report/readings/2026-11-17.md) to see what that rests on.
- 2026-11-14 | lighthouse | You can now reuse what we publish: our writing and our own data are free to share with credit, and our code is open source, as [About](about.md#using-and-citing) explains. We've also added a [glossary](glossary.md), a list of [every correction we've made](corrections.md) and a guide to [the data we keep and how to rerun a study](data-and-replay.md).
