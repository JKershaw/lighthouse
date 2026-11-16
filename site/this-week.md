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
week: 2026-11-10 to 2026-11-16
updated: 2026-11-16
today: 2026-11-16 | On our Monday look at the PHP emergency fix, nothing changed in the official records, while Node.js users moved fast onto three newer releases that appeared on 11 November. We also re-read the two security firms' posts on the GitHub campaign, both of which have changed since we kept them, and Microsoft's status page, where the full outage report still hasn't appeared. None of it has been reviewed.
items:
- 2026-11-16 | reported | The review conference of the UN's conventional weapons treaty opens in Geneva today, with a proposed mandate for further talks on autonomous weapons among its papers. We kept what public sources said about three robot cases and the draft texts before it began, and from 21 November [we'll read](studies/LH050/LH050.md) what it adopts.
- 2026-11-14 | reported | Microsoft 365 was disrupted from 12 to 14 November. Microsoft's early account, as an affected university reproduced it, blamed a network change and said it was "not related to cyber or AI / agents". We're [watching for its promised full report](notes/microsoft-outage-report/readings/2026-11-16.md) to see what that rests on.
- 2026-11-14 | lighthouse | You can now reuse what we publish: our writing and our own data are free to share with credit, and our code is open source, as [About](about.md#using-and-citing) explains. We've also added a [glossary](glossary.md), a list of [every correction we've made](corrections.md) and a guide to [the data we keep and how to rerun a study](data-and-replay.md).
- 2026-11-13 | lighthouse | Our front page is new: it opens with what we've learned so far, then this week, then [our four investigations](investigations/) and where each one stands. Every piece now ends with what to read next, and the working files have [a page of their own](working/).
- 2026-11-13 | lighthouse | We've started counting, hour by hour, the public traces of a campaign that StepSecurity and Aikido say used stolen GitHub accounts from 10 November to plant a script stealing build secrets, AI keys among them. We kept both firms' posts as published first; [the study's brief](studies/LH051/brief.md) says what we count and what we won't name.
- 2026-11-13 | lighthouse | Our first study of [armed AI-powered robots](studies/LH050/brief.md) has started: before an international weapons conference opens in Geneva on 16 November, we kept what public sources say about three cases and the draft conference texts, so that we can see what the week changes. None of it is a finding yet.
- 2026-11-12 | lighthouse | We've opened [an investigation of armed AI-powered robots](investigations/physical-authority.md): what they can do, who decides when they use force, and what public evidence says about what happens to civilians.
